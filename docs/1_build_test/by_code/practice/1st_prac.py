#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging #日志模块
import re
import sqlite3
import time
from abc import ABC, abstractmethod  # 抽象基类模块 定义接口规范或抽象类
from contextlib import asynccontextmanager, contextmanager #上下文管理工具
from dataclasses import dataclass # 数据类工具
from typing import Dict, Generator, Iterable, List, Optional #  类型注解支持库

import aiohttp #异步 HTTP 客户端与服务器库

###########################
##### logging module ######
###########################

def setup_logging() -> None:
    """
    创建一个日志,等级为 INFO ,并 规定了格式，和 日志的名字(有就调用，没有就创建)
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s")

log = logging.getLogger("crawler")


################################
#####  decorators module   #####
################################

def timed(fn):
    """
    创建一个修饰器函数,第一层入参是一个函数,在异步函数的基础上,添加一个计时器,从而包装成新的函数。
    """
    async def _inner(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return await fn(*args, **kwargs)
        finally:
            log.debug("%s took %.2f ms", fn.__name__, (time.perf_counter()-t0)*1000)
    return _inner

def retry_async(retries=3, backoff=0.5, excs=(Exception,)):
    """
    重试函数,第一层参数是尝试次数和等待时间,以及异常类型
    第二层参数是修饰的函数,返回一个修饰器函数
    第三层是执行每次操作,失败打印日志,和等待时间再重试
    """
    def deco(fn):
        async def wrapper(*a, **kw):
            last = None
            for i in range(retries):
                try:
                    return await fn(*a, **kw)
                except excs as e:
                    last = e
                    sleep = backoff * (2**i)
                    log.warning("retry %d/%d for %s: %r (sleep %.1fs)",
                                i+1, retries, fn.__name__, e, sleep)
                    await asyncio.sleep(sleep)
            raise last
        return wrapper
    return deco

###################
###  数据库模块  ####
###################

# 帮助快速定义一个结构类


@dataclass
class Page:
    url: str
    status: int
    title: str
    content: str

#################
## utils model ##
#################

#筛选正则
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
WORD_RE = re.compile(r"[A-Za-z0-9]+")

def extract_title(html: str) -> str:
    """
    从html中提取数据,返回值是str, 在输入中查找与正则匹配的部分,返回第一个搜索结果,
    并去除里面的多余的空白(re.sub),strip()去除首位空格
    如果没有结果就返回 "N/A"
    """
    m = TITLE_RE.search(html)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "N/A"

def tokenize(text: str) -> Generator[str, None, None]:
    """
    生产一个生成器对象,这里只有调用值,没有输入和返回值
    可以通过 next() 每次获取生成器中的结果

    匹配连续的英文字，并返回一个可迭代对象
    """

    for m in WORD_RE.finditer(text.lower()):
        yield m.group(0)

########################################
### OPP (面对对象编程) Fecther 爬虫模块 ###
########################################

## Optional能返回 int ,str ,list[str], page, any(任意对象)，非规定对象就返回None

class BaseFetcher(ABC):
    """
    定义抽象类,抽象类不能作为实例,但可以作为参数,或者父类,返回 一个page 的对象
    """
    @abstractmethod
    async def fetch(self, url: str) -> Optional[Page]:
        pass

class HttpFetcher(BaseFetcher):
    """
    调用抽象类创建实例,抽象类是给实例类中的函数一个写法约束,所以定义的函数必须按照抽象类来写
    aiohttp.ClientSession : 异步HTTP客户端
    timeout 超时时间 默认8秒
    """
    def __init__(self, session: aiohttp.ClientSession, timeout: float = 8.0):
        self.session = session
        self.timeout = timeout

    @retry_async(retries=3, backoff=0.4, excs=(aiohttp.ClientError, asyncio.TimeoutError))
    async def fetch(self, url: str) -> Optional[Page]:
        """
        传入重试参数,哪些异常类会引发重试
        http请求, self.session 为 aiohttp.ClientSession的实例
        异步请求将response 放到 r 中
        异步 将 返回的结果 转化成 str格式 并忽略编码错误
        返回一个页面对象
        """
        async with self.session.get(url, timeout=self.timeout) as r:
            text = await r.text(errors="ignore")
            return Page(url, r.status, extract_title(text), text)


#############################
### OOP processer 处理模块 ###
#############################

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, page: Page) -> Dict[str, str]:
        ...

class WordStatProcessor(BaseProcessor):
    def __init__(self, topk: int = 8):
        self.topk = topk

    def process(self, page: Page) -> Dict[str, str]:
        """
        对返回的page进行梳理
        """
        #创建一个空字典(字符串和频次)
        freq: Dict[str, int] = {}
        # 将page中的内容转化成单词
        for t in tokenize(page.content):
            #计算出现的频次,get函数做了个比较，有就调用，没有就返回0，实际用法可以将比较部分去掉
            freq[t] = freq.get(t, 0) + 1
        # 对字典进行排序,key 是排序规则 ，选取前k个
        top = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[: self.topk]
        return {"url": page.url, "title": page.title, "status": str(page.status),
                "top_words": ", ".join(f"{w}:{c}" for w, c in top)}

################################
#### 持续化层 处理结果写入 数据库 ###
################################
# contextmanager 将一个函数封装成上下文对象，之后可以用 with 进行读写操作,这个用法是防止程序 失败而卡死。
@contextmanager
def sqlite_conn(path: str):
    """
    函数中的yield在这里相当于一个断点, 在使用 with 操作时,with 操作会自动调用 __enter__ 方法
    即 with sqlite_conn("db.sqlite3") as db: 之后可以直接操作而无需连接，最后会自动关闭

    """
    conn = sqlite3.connect(path)
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS results(
          url TEXT PRIMARY KEY, title TEXT, status INTEGER, top_words TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        conn.commit()
        yield conn
        conn.commit()
    finally:
        conn.close()

################
## 异步对话处理 ##
################
# asynccontextmanager 和 contextmanager 一样可以使用with操作
@asynccontextmanager
async def http_session(header:str = "MiniCrawler/1.0"):
    """
    创建一个会话对象, 相当于 requests 里的 requests.Session()
    headers 这里需要更像一个真实的浏览器才不容易被封
    """
    async with aiohttp.ClientSession(headers={f"User-Agent": header}) as s:
        yield s


# https 模版
# import aiohttp, ssl, certifi, asyncio
# from contextlib import asynccontextmanager

# @asynccontextmanager
# async def http_session(user_agent=None):
#     headers = {"User-Agent": user_agent or "Mozilla/5.0 ... Chrome/..."}
#     ssl_ctx = ssl.create_default_context(cafile=certifi.where())
#     connector = aiohttp.TCPConnector(ssl=ssl_ctx)
#     async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
#         yield session


#################
## 爬虫数据处理 ##
#################


class Pipeline:
    def __init__(self, fetcher: BaseFetcher, processor: BaseProcessor, db_path: str = "news.db"):
        self.fetcher = fetcher
        self.processor = processor
        self.db_path = db_path

    @timed
    async def run(self, urls: Iterable[str], concurrency: int = 10) -> None:
        """
        函数只操作不返回值
        可以并发处理一组 urls,最多并发concurrency个任务

        """
        # Semaphore 是并发限制器 
        sem = asyncio.Semaphore(concurrency)
        # 结果储存格式
        results: List[Dict[str, str]] = []

        async def worker(url: str):
            async with sem:
                #在并发限制下运行
                p = await self.fetcher.fetch(url)
                if p:
                    log.info("Fetched %s [%s] - %s", p.url, p.status, p.title)
                    results.append(self.processor.process(p))

        await asyncio.gather(*(worker(u) for u in urls))

        with sqlite_conn(self.db_path) as conn:
            conn.executemany("""INSERT INTO results(url,title,status,top_words)
              VALUES(:url,:title,:status,:top_words)
              ON CONFLICT(url) DO UPDATE SET
                title=excluded.title, status=excluded.status, top_words=excluded.top_words,
                created_at=CURRENT_TIMESTAMP
            """, results)
        log.info("Saved %d rows -> %s", len(results), self.db_path)

# ---------- main ----------
async def main():
    setup_logging()
    urls = [
        "https://example.com/",
        "https://www.python.org/",
        "https://httpbin.org/html",
        "https://www.wikipedia.org/",
    ]
    async with http_session("test") as s:
        fetcher = HttpFetcher(s)
        processor = WordStatProcessor(topk=6)
        pipe = Pipeline(fetcher, processor)
        await pipe.run(urls, concurrency=8)

if __name__ == "__main__":
    asyncio.run(main())