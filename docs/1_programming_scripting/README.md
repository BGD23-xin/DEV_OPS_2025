## Programming & scripting

### python
#### 文件与目录操作
`os`:

```python
import os

# 获取当前工作目录
print(os.getcwd())

# 创建文件夹
os.makedirs("logs", exist_ok=True)

# 删除文件夹
os.rmdir("logs")

# 列出文件
for f in os.listdir("."):
    print(f)

# 创建文件
open("new.log", "w").close()
os.system("touch new.log")

# 删除文件
os.remove("old.log")

# 读取单个环境变量
api_key = os.getenv("API_KEY")

获取全局变量
os.environ


```

`pathlib`:

```python
from pathlib import Path

# 当前工作目录
path.cwd()

# 当前用户目录
path.home()

#拼接目录
Path("logs") / "app.log"

Path("logs").joinpath("app.log")

# 生成文件
Path("new.log").touch()

# 删除文件

Path("old.log").unlink()


# 写入内容
p = Path("data.txt")
p.write_text("Hello, DevOps!")

# 读取内容
content = p.read_text()
```


#### 网络请求与接口交互
`requests`
```python
import requests

#获取网路资源
requests.get(url=，params=)

# 提交数据表单
requests.post(url)

# 修改数据
requests.put(url)
# 局部修改
requests.patch(url)
# 删除数据
requests.delete(url)
#获取头部数据
requests.head(url)



```

`httpx` 直接request替换 request部分,
支持异步
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com")
        return r.status_code

# 在单元格里直接：
status = await main()
print(status)

```


#### JSON/YAML/INI 解析
`json` 
`yaml`
`configparser` 
#### 系统命令与子进程
`subprocess`
`shutil` 
#### 异步与多线程
`asyncio`
`threading` 
#### AWS SDK 
`boto3` 
#### 自动化管理资源
`EC2`
`S3`
`Lambda` 
#### Flask / FastAPI 开发轻量 
REST API 工具




### Bash / Shell

### JavaScript / Node.js

### Ruby


