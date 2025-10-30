# asyncio

这是协程(coroutine)的模块。在学习这个模块之前，需要理清 `进程`,`线程`,`协程`这三个概念。

- 进程(process)：相当于一个软件实例(vscode,python)
- [用户级线程(thread)](https://www.cnblogs.com/Survivalist/p/11527949.html#%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%B8%8E%E5%A4%9A%E6%A0%B8): 进程中最小的执行单元,一个线程一次只能执行一个任务,进程可以有多个线程。
- 协程(coroutine)：是一个可以暂停和运行的函数，使python更高效使用CPU。

协程的作用是，在CPU 等待时间（1.网络请求 2.文件的读写 3.通信接口，APIs，timer 定时器 所产生的I/O等待），这个过程cpu是待机状态。通过暂停这个任务，来释放cpu，等接收到返回信息之后，cpu处于空闲时再重新运行。



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

asyncio.run(coro) # 运行协程

asyncio.get_event_loop() #获取当前事件循环，

asyncio.new_event_loop() #创建一个新的事件循环

#创建与调度任务
asyncio.create_task(coro) # 把协程包装成一个可调度的任务（Task）task = asyncio.create_task(fetch())
asyncio.gather(*coros) # 并行运行多个协程并等待全部完成 await asyncio.gather(task1(), task2())
asyncio.wait(tasks) # 等待多个任务完成（更底层版本） done, pending = await asyncio.wait(tasks)
asyncio.as_completed(tasks) # 谁先完成先返回结果 for f in asyncio.as_completed(tasks): res = await f

# 延迟与超时控制
await asyncio.sleep(seconds) # 暂停一段时间（不会阻塞事件循环）await asyncio.sleep(2)
asyncio.wait_for(coro, timeout) # 给协程设置超时时间 await asyncio.wait_for(fetch(), 5)
asyncio.timeout(seconds) # 上下文方式设置超时 async with asyncio.timeout(5): await fetch()

# 同步与锁机制（在协程之间共享资源）
asyncio.Lock() # 协程版的锁，防止并发修改同一资源 lock = asyncio.Lock()async with lock: # 安全区域
asyncio.Semaphore(n) #同时允许最多 n 个协程访问 sem = asyncio.Semaphore(3)
asyncio.Event() # 事件信号机制，一个任务设置事件，另一个任务等待 await event.wait()

#与外部 I/O 协作（底层）
asyncio.open_connection(host, port) #打开一个 TCP 连接 reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
asyncio.start_server(handler, host, port) #启动一个异步 TCP 服务器 server = await asyncio.start_server(handle, '127.0.0.1', 8888)
reader.read(n) / writer.write(data) # 读写网络数据（Stream API）writer.write(b'Hello')


# 辅助工具
asyncio.shield(coro) #保护任务不被取消 await asyncio.shield(fetch())
task.cancel() #取消任务 task.cancel()
asyncio.current_task() #获取当前正在执行的任务 task = asyncio.current_task()
asyncio.all_tasks() #asyncio.all_tasks() tasks = asyncio.all_tasks()



```