#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
async_socket_demo.py

一个中型、工程化风格的 asyncio socket 示例：
- 服务端：异步 echo server，优雅关停，跟踪 client 任务。
- 客户端：并发连接、超时与重试（指数退避），异步上下文管理器封装连接。
- 工具：结构化日志、装饰器计时、退避生成器、类型注解、PEP8。
用法见文件顶部注释或运行 `-h`。
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import functools
import json
import logging
import signal
import sys
import time
from dataclasses import dataclass
from typing import AsyncIterator, Awaitable, Callable, Generator, Optional, Tuple


# =========================
# 日志初始化
# =========================

def setup_logging(level: str = "INFO") -> None:
    """Setup structured logging with JSON-like messages."""
    lvl = getattr(logging, level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            payload = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created)),
                "level": record.levelname,
                "name": record.name,
                "msg": record.getMessage(),
            }
            if record.exc_info:
                payload["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(payload, ensure_ascii=False)

    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.setLevel(lvl)
    root.handlers.clear()
    root.addHandler(handler)


logger = logging.getLogger("async-socket-demo")


# =========================
# 工具：装饰器/生成器
# =========================

F = Callable[..., Awaitable]


def async_timed(fn: F) -> F:
    """Async decorator: measure coroutine runtime and log it."""
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return await fn(*args, **kwargs)
        finally:
            dur = (time.perf_counter() - start) * 1000
            logger.debug(f"{fn.__name__} took {dur:.2f} ms")
    return wrapper  # type: ignore[return-value]


def exponential_backoff(
    base: float = 0.2, factor: float = 2.0, max_delay: float = 3.0, cap_retries: int = 5
) -> Generator[float, None, None]:
    """
    退避生成器：yield 0.2, 0.4, 0.8, 1.6, 3.0, 3.0, ...
    """
    delay = base
    count = 0
    while True:
        yield min(delay, max_delay)
        delay = min(delay * factor, max_delay)
        count += 1
        if cap_retries > 0 and count >= cap_retries:
            # 固定在 max_delay
            while True:
                yield max_delay


# =========================
# 异步上下文管理器：连接
# =========================

@dataclass
class AsyncConnection:
    """
    封装 asyncio.open_connection 的异步上下文管理器。

    Attributes:
        host: 目标主机
        port: 目标端口
        timeout: 连接与单次 I/O 的超时（秒）
    """
    host: str
    port: int
    timeout: float = 5.0

    reader: asyncio.StreamReader | None = None
    writer: asyncio.StreamWriter | None = None

    async def __aenter__(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        self.reader, self.writer = await asyncio.wait_for(
            asyncio.open_connection(self.host, self.port),
            timeout=self.timeout,
        )
        return self.reader, self.writer

    async def __aexit__(self, exc_type, exc, tb) -> Optional[bool]:
        if self.writer is not None:
            try:
                self.writer.close()
                with contextlib.suppress(Exception):
                    await asyncio.wait_for(self.writer.wait_closed(), timeout=self.timeout)
            except Exception:
                logger.warning("closing writer failed", exc_info=True)
        self.reader, self.writer = None, None
        # 不吞异常
        return None


# =========================
# 服务端
# =========================

class EchoServer:
    """
    简单的异步 Echo Server。
    - 记录活跃任务，优雅退出（CTRL+C 或 SIGTERM）
    - 每个客户端单独 handler，带超时/错误处理
    """
    def __init__(self, host: str, port: int, client_timeout: float = 30.0) -> None:
        self._host = host
        self._port = port
        # 返回一个server 对象
        self._server: Optional[asyncio.base_events.Server] = None
        
        # 记录和客户端所有的任务
        self._client_tasks: set[asyncio.Task] = set()
        self._client_timeout = client_timeout
        
        # 服务停止信号
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle_client, self._host, self._port)
        addr = ", ".join(str(sock.getsockname()) for sock in self._server.sockets or [])
        logger.info(f"server listening on {addr}")

    async def serve_forever(self) -> None:
        assert self._server is not None
        async with self._server:
            await self._server.start_serving()
            await self._stop_event.wait()

    async def stop(self) -> None:
        logger.info("server shutting down...")
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()

        # 取消所有 client 任务
        for t in list(self._client_tasks):
            t.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.gather(*self._client_tasks, return_exceptions=True)
        logger.info("server closed")

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        peer = writer.get_extra_info("peername")
        task = asyncio.current_task()
        if task:
            self._client_tasks.add(task)
        logger.info(f"client connected: {peer}")
        try:
            while True:
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=self._client_timeout)
                except asyncio.TimeoutError:
                    logger.info(f"client timeout: {peer}")
                    break
                if not data:
                    break
                # echo 回去
                writer.write(data)
                await writer.drain()
        except asyncio.CancelledError:
            logger.debug(f"client handler cancelled: {peer}")
            raise
        except Exception as e:  # noqa: BLE001
            logger.warning(f"client error {peer}: {e}", exc_info=True)
        finally:
            with contextlib.suppress(Exception):
                writer.close()
                await writer.wait_closed()
            if task:
                self._client_tasks.discard(task)
            logger.info(f"client disconnected: {peer}")

    def request_stop(self) -> None:
        self._stop_event.set()


# =========================
# 客户端
# =========================

@async_timed
async def run_client_once(
    host: str,
    port: int,
    message: str,
    timeout: float = 3.0,
) -> str:
    """单次请求：连接、发送一行、读取 echo。"""
    async with AsyncConnection(host, port, timeout=timeout) as (reader, writer):
        writer.write((message + "\n").encode("utf-8"))
        await writer.drain()
        data = await asyncio.wait_for(reader.readline(), timeout=timeout)
        return data.decode("utf-8").rstrip("\n")


async def run_clients_burst(
    host: str,
    port: int,
    message: str,
    messages: int,
    concurrency: int,
    timeout: float,
    retries: int,
) -> None:
    """
    并发执行 messages 次请求，限制最大并发 concurrency。
    对于连接/超时错误进行重试（指数退避）。
    """
    sem = asyncio.Semaphore(concurrency)

    async def one_call(i: int) -> Tuple[int, Optional[str]]:
        attempt = 0
        backoff = exponential_backoff()
        while True:
            attempt += 1
            try:
                async with sem:
                    resp = await run_client_once(host, port, f"{message}-{i}", timeout)
                return i, resp
            except (asyncio.TimeoutError, ConnectionError, OSError) as e:
                if attempt > retries:
                    logger.error(f"request {i} failed after {retries} retries: {e}")
                    return i, None
                delay = next(backoff)
                logger.warning(f"request {i} attempt {attempt} failed: {e}, retry in {delay:.2f}s")
                await asyncio.sleep(delay)

    tasks = [asyncio.create_task(one_call(i)) for i in range(messages)]
    done = 0
    for coro in asyncio.as_completed(tasks):
        idx, resp = await coro
        done += 1
        if resp is not None:
            logger.info(f"[{done}/{messages}] ok: {resp}")
        else:
            logger.info(f"[{done}/{messages}] failed: {idx}")


# =========================
# CLI 入口
# =========================

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Async socket demo with asyncio.")
    sub = p.add_subparsers(dest="mode", required=True)

    # server
    ps = sub.add_parser("server", help="Run echo server")
    ps.add_argument("--host", default="127.0.0.1", help="bind host")
    ps.add_argument("--port", type=int, default=8765, help="bind port")
    ps.add_argument("--client-timeout", type=float, default=30.0, help="per-connection idle timeout (s)")
    ps.add_argument("--log-level", default="INFO", help="logging level")

    # client
    pc = sub.add_parser("client", help="Run client load")
    pc.add_argument("--host", default="127.0.0.1", help="server host")
    pc.add_argument("--port", type=int, default=8765, help="server port")
    pc.add_argument("--message", default="hello", help="base message")
    pc.add_argument("--messages", type=int, default=20, help="number of requests")
    pc.add_argument("--concurrency", type=int, default=10, help="max concurrent requests")
    pc.add_argument("--timeout", type=float, default=3.0, help="per-request timeout (s)")
    pc.add_argument("--retries", type=int, default=2, help="retries on failure")
    pc.add_argument("--log-level", default="INFO", help="logging level")

    return p


async def main_async(args: argparse.Namespace) -> None:
    if args.mode == "server":
        setup_logging(args.log_level)
        server = EchoServer(args.host, args.port, client_timeout=args.client_timeout)

        loop = asyncio.get_running_loop()
        # 优雅关停（SIGINT/SIGTERM）
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, server.request_stop)

        await server.start()
        try:
            await server.serve_forever()
        finally:
            await server.stop()

    elif args.mode == "client":
        setup_logging(args.log_level)
        await run_clients_burst(
            host=args.host,
            port=args.port,
            message=args.message,
            messages=args.messages,
            concurrency=args.concurrency,
            timeout=args.timeout,
            retries=args.retries,
        )
    else:
        raise ValueError(f"unknown mode: {args.mode}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        logger.info("Interrupted by user")


if __name__ == "__main__":
    main()
