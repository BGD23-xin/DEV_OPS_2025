# asyncio

asyncio 是 的 异步 I/O 模块，用于处理异步任务。

基础输出
```python 
import asyncio

# 定义一个异步任务函数
async def task(name):
    print(f'{name}Hello ...')
    await asyncio.sleep(1)
    print(f'{name}... World!')

# 运行 任务，输出是两个任务的结果，是并行执行的
async def main():
    await asyncio.gather(task("A"), task("B"))
await main()
```

进阶

```python 
# 适配jupyter，因为jupyter本身有一个loop，所以一个补丁来允许嵌套
import nest_asyncio
nest_asyncio.apply()


# 脚本入口，事件循环
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    print("running...")

asyncio.run(main())

```