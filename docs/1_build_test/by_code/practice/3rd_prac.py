#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import time
from functools import lru_cache #结果缓存装饰器
from typing import Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel # fastapi需要来定义数据结构

###################
###  logging 模块 ##
###################

#定义实例，log等级和格式
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
# 定义叫api的logger
log = logging.getLogger("api")

# 定义一个修饰器函数
def timed(fn):
    async def _inner(*a, **kw):
        """
        测试函数运行时间
        """
        t0 = time.perf_counter()
        try:
            return await fn(*a, **kw)
        finally:
            dt = (time.perf_counter() - t0) * 1000
            log.info(json.dumps({"event": "timing", "func": fn.__name__, "ms": round(dt, 2)}))
    return _inner

##  定义一个数据结构类，比dataclass更强大，会将输入改成对应的格式
class FetchResult(BaseModel):
    url: str
    status: int
    title: str

#################
## 异步建立会话 ###
#################
async def get_client() -> httpx.AsyncClient:
    """
    返回一个 httpx.AsyncClient的对象,本质是建立会话,与aiohttp类似
    """
    async with httpx.AsyncClient(headers={"User-Agent": "MiniAPI/1.0"}, timeout=8.0) as c:
        yield c

# 提取标题
def extract_title(html: str) -> str:
    import re
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "N/A"

# simple in-memory async lock for cache stampede protection
_cache = {}
#定义一个协程锁，使多协程访问同一资源时，只有一个协程在处理，其他协程 等待
_lock = asyncio.Lock()

@lru_cache(maxsize=256)
def _norm(u: str) -> str:
    """
    函数的结果缓存,最大为256M
    """
    return u.strip().lower()

# ---------- app ----------
app = FastAPI(title="Mini Async Service", version="0.1.0")

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/fetch", response_model=FetchResult)
@timed
async def fetch(url: str = Query(..., min_length=5), client: httpx.AsyncClient = Depends(get_client)):
    key = _norm(url)
    async with _lock:
        if key in _cache:
            return _cache[key]
    try:
        r = await client.get(url)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"upstream error: {e}") from e

    res = FetchResult(url=url, status=r.status_code, title=extract_title(r.text))
    async with _lock:
        _cache[key] = res
    return res