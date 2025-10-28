#!/usr/bin/env python3
"""
API 访问示例（同步 / 并发 / 异步）
=================================================

展示在“熟练阶段”常用的库与技巧：
- requests（同步 HTTP）
- concurrent.futures（线程池并发）
- asyncio + httpx（异步 HTTP）
- logging（结构化日志）
- argparse（命令行接口）
- 装饰器（重试、计时）
- 上下文管理器（Session/Client 生命周期）
- 类型标注 / Docstring / PEP8

用法（示例）：

# 单次请求
python api_tool.py sync --url https://httpbin.org/get
python api_tool.py async --url https://httpbin.org/get

# 批量并发（线程池 vs 异步）
python api_tool.py sync --urls https://httpbin.org/get https://jsonplaceholder.typicode.com/todos/1
python api_tool.py async --urls https://httpbin.org/get https://api.github.com/repos/psf/requests --concurrency 5

# 从文件批量（每行一个 URL）
python api_tool.py sync --file urls.txt --workers 8
python api_tool.py async --file urls.txt --concurrency 50

# 指定超时 / 重试次数
python api_tool.py async --url https://httpbin.org/status/503 --retries 3 --timeout 5

依赖：
  pip install requests httpx
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Iterable, List, Optional

import requests
import httpx

# ------------------------------
# 日志设置（结构化 JSON）
# ------------------------------
class JsonFormatter(logging.Formatter):
    """
    父类是logging.Formatter,保证格式符合logging的格式
    """
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        """
        对于单条日志的格式化
        """
        payload = {
            "level": record.levelname,
            "time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)),
            "msg": record.getMessage(),
            "name": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if hasattr(record, "extra"):
            payload.update(record.extra)  # type: ignore[arg-type]
        return json.dumps(payload, ensure_ascii=False)

logger = logging.getLogger("api_tool")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ------------------------------
# 装饰器：计时 + 重试（同步/异步）
# ------------------------------


def timed(fn: Callable[..., Any]) -> Callable[..., Any]:
    # wraps 保证 参数的注解和 annotations 
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            dur_ms = (time.perf_counter() - start) * 1000
            logger.info("timing", extra={"extra": {"func": fn.__name__, "dur_ms": round(dur_ms, 2)}})

    return wrapper


def aretry(retries: int = 2, base_delay: float = 0.5, factor: float = 2.0):
    """异步重试装饰器，指数退避。"""

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return await fn(*args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    attempt += 1
                    if attempt > retries:
                        logger.error("async request failed", extra={"extra": {"attempt": attempt, "error": str(e)}})
                        raise
                    logger.warning(
                        "async retry",
                        extra={"extra": {"attempt": attempt, "next_delay": delay, "error": str(e)}},
                    )
                    await asyncio.sleep(delay)
                    delay *= factor

        return inner

    return deco


def sretry(retries: int = 2, base_delay: float = 0.5, factor: float = 2.0):
    """同步重试装饰器，指数退避。"""

    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def inner(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    attempt += 1
                    if attempt > retries:
                        logger.error("sync request failed", extra={"extra": {"attempt": attempt, "error": str(e)}})
                        raise
                    logger.warning(
                        "sync retry",
                        extra={"extra": {"attempt": attempt, "next_delay": delay, "error": str(e)}},
                    )
                    time.sleep(delay)
                    delay *= factor

        return inner

    return deco

# ------------------------------
# 数据结构
# ------------------------------
@dataclass
class FetchResult:
    url: str
    status: int
    elapsed_ms: float
    length: int
    snippet: str

# ------------------------------
# 上下文管理器：requests 与 httpx 客户端生命周期
# ------------------------------
@contextmanager
def requests_session(timeout: float):
    session = requests.Session()
    try:
        yield session, timeout
    finally:
        session.close()


@asynccontextmanager
async def httpx_client(timeout: float, limits: Optional[httpx.Limits] = None):
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        yield client

# ------------------------------
# 同步实现（requests）
# ------------------------------
@sretry()
@timed
def fetch_sync(session: requests.Session, url: str, timeout: float) -> FetchResult:
    start = time.perf_counter()
    r = session.get(url, timeout=timeout)
    elapsed_ms = (time.perf_counter() - start) * 1000
    text = r.text[:200].replace("\n", " ") if r.text else ""
    res = FetchResult(url=url, status=r.status_code, elapsed_ms=elapsed_ms, length=len(r.content), snippet=text)
    logger.info("sync fetched", extra={"extra": res.__dict__})
    return res


def run_sync(urls: List[str], timeout: float, workers: int) -> List[FetchResult]:
    results: List[FetchResult] = []
    with requests_session(timeout) as (session, t):
        if len(urls) == 1:
            results.append(fetch_sync(session, urls[0], t))
            return results
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = {pool.submit(fetch_sync, session, u, t): u for u in urls}
            for fut in as_completed(futs):
                try:
                    results.append(fut.result())
                except Exception as e:  # noqa: BLE001
                    logger.error("sync task error", extra={"extra": {"url": futs[fut], "error": str(e)}})
    return results

# ------------------------------
# 异步实现（httpx + 限流 + 重试）
# ------------------------------
@aretry()
async def fetch_async(client: httpx.AsyncClient, url: str, sem: asyncio.Semaphore) -> FetchResult:
    start = time.perf_counter()
    async with sem:
        r = await client.get(url)
    elapsed_ms = (time.perf_counter() - start) * 1000
    text = r.text[:200].replace("\n", " ") if r.text else ""
    res = FetchResult(url=url, status=r.status_code, elapsed_ms=elapsed_ms, length=len(r.content), snippet=text)
    logger.info("async fetched", extra={"extra": res.__dict__})
    return res


# 设置 httpx.Limits是防止 服务端被打爆
async def run_async(urls: List[str], timeout: float, concurrency: int) -> List[FetchResult]:
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(max_keepalive_connections=concurrency, max_connections=concurrency * 2)
    async with httpx_client(timeout, limits) as client:
        tasks = [fetch_async(client, u, sem) for u in urls]
        results: List[FetchResult] = []
        for coro in asyncio.as_completed(tasks):
            try:
                results.append(await coro)
            except Exception as e:  # noqa: BLE001
                logger.error("async task error", extra={"extra": {"error": str(e)}})
        return results

# ------------------------------
# CLI
# ------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="HTTP API access examples (sync/async)")
    
    #这个命令是开一个子命令解析器
    sub = p.add_subparsers(dest="mode", required=True)

    #公共部分的参数
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--url", help="单个 URL")
    common.add_argument("--urls", nargs="*", help="多个 URL（空格分隔）")
    common.add_argument("--file", help="从文件读取 URL（每行一个）")
    common.add_argument("--timeout", type=float, default=10.0, help="请求超时（秒）")
    common.add_argument("--retries", type=int, default=2, help="重试次数（含首次外的额外重试）")

    # 同步模式下
    ps = sub.add_parser("sync", parents=[common], help="同步 + 线程池")
    ps.add_argument("--workers", type=int, default=8, help="线程池大小")

    # 异步模式下
    pa = sub.add_parser("async", parents=[common], help="异步 + httpx")
    pa.add_argument("--concurrency", type=int, default=50, help="并发限制（信号量）")

    return p.parse_args(argv)


def collect_urls(args: argparse.Namespace) -> List[str]:
    urls: List[str] = []
    if args.url:
        urls.append(args.url)
    if args.urls:
        urls.extend(args.urls)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip() and not line.startswith("#")])
    if not urls:
        raise SystemExit("请至少提供一个 URL（--url / --urls / --file）")
    return urls


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    # 动态设置重试次数
    global fetch_sync, fetch_async  # type: ignore[no-redef]
    fetch_sync = sretry(retries=args.retries)(fetch_sync)  # type: ignore[assignment]
    fetch_async = aretry(retries=args.retries)(fetch_async)  # type: ignore[assignment]

    urls = collect_urls(args)
    logger.info("start", extra={"extra": {"mode": args.mode, "n_urls": len(urls)}})

    if args.mode == "sync":
        results = run_sync(urls, timeout=args.timeout, workers=args.workers)
    else:
        results = asyncio.run(run_async(urls, timeout=args.timeout, concurrency=args.concurrency))

    # 输出结果（行式 JSON，便于被其他系统消费）
    for r in results:
        print(json.dumps(r.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv)
