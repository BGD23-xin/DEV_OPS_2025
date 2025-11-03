#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse #参数解析器,添加参数交互，命令行传递参数
import csv
import logging
import os
import re
import sqlite3
from concurrent.futures import ProcessPoolExecutor, as_completed #并行线程和进程
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Tuple

# 创建一个叫log_etl的日志
LOG = logging.getLogger("log_etl")
# 正则表达
LINE_RE = re.compile(r"^(?P<ts>\S+) \| (?P<level>\w+) \| (?P<msg>.*)$")

# 创建一个叫Row的规范类
@dataclass
class Row:
    ts: str
    level: str
    msg: str

def setup_logging(level="INFO") -> None:
    """
    返回为空,只执行操作,等级为info
    """
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s | %(levelname)s | %(message)s")

def parse_line(line: str) -> Row:
    """
    返回一个Row对象,对传入的行进行正则筛选,不为空时候,返回规范的日志
    """
    m = LINE_RE.match(line.strip())
    if not m:
        return Row("NA", "UNKNOWN", line.strip())
    return Row(m.group("ts"), m.group("level"), m.group("msg"))

def read_lines(path: Path) -> Generator[str, None, None]:
    """
    返回一个生成器,里面没有返回值,只有yield值
    """
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for ln in f:
            yield ln

def summarize_file(path: str) -> Dict[str, int]:
    """CPU 方向的轻解析：统计各 level 次数。"""
    counts: Dict[str, int] = {}
    for ln in read_lines(Path(path)):
        row = parse_line(ln)
        counts[row.level] = counts.get(row.level, 0) + 1
    return counts

def save_csv(rows: Iterable[Tuple[str, str, int]], out: Path) -> None:
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "level", "count"]) # 表头
        for r in rows:
            w.writerow(r)

def save_sqlite(rows: Iterable[Tuple[str, str, int]], db: Path) -> None:
    conn = sqlite3.connect(db)
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS level_counts(
          file TEXT, level TEXT, count INTEGER,
          PRIMARY KEY(file, level))""")
        conn.executemany("""INSERT INTO level_counts(file,level,count)
          VALUES(?,?,?)
          ON CONFLICT(file,level) DO UPDATE SET count=excluded.count
        """, list(rows))
        conn.commit()
    finally:
        conn.close()

def collect_files(root: Path) -> List[str]:
    """
    返回路径下所有以.log结尾的文件
    """
    return [str(p) for p in root.rglob("*.log")]

def main():
    ap = argparse.ArgumentParser(description="ETL: parse logs and aggregate level counts.")
    ap.add_argument("--root", type=Path, default=Path("./logs"), help="log directory")
    ap.add_argument("--csv", type=Path, default=Path("level_counts.csv"))
    ap.add_argument("--db", type=Path, default=Path("logs.db"))
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--log-level", type=str, default="INFO")
    args = ap.parse_args()

    setup_logging(args.log_level)
    files = collect_files(args.root)
    if not files:
        LOG.warning("No .log files under %s", args.root)
        return

    LOG.info("Found %d files; using %d workers", len(files), args.workers)
    results: List[Tuple[str, str, int]] = []
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        # 在进程池中，并行多个进程运行函数 summarize_file(fp)
        futs = {ex.submit(summarize_file, fp): fp for fp in files}
        # 这个结果需要使用 as_completed 来管理
        for fut in as_completed(futs):
            fp = futs[fut]
            try:
                counts = fut.result()
                for level, cnt in counts.items():
                    results.append((fp, level, cnt))
            except Exception as e:
                LOG.exception("Failed on %s: %r", fp, e)

    save_csv(results, args.csv)
    save_sqlite(results, args.db)
    LOG.info("Wrote %s and %s", args.csv, args.db)

if __name__ == "__main__":
    main()