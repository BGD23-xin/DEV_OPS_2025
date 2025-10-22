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
```python
import json

# 读取 JSON 文件
with open("config.json") as f:
    data = json.load(f)

# 写入 JSON 文件
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)

# 字符串解析
obj = json.loads('{"key": "value"}')
print(obj["key"])

# 转换成json格式的字符串
json.dumps()

```
`yaml`
```python
import yaml

# 读取 YAML
with open("config.yaml") as f:
    data = yaml.safe_load(f)

# 写入 YAML
with open("output.yaml", "w") as f:
    yaml.dump(data, f)
```


`configparser` (INI (Initialization) 配置文件)
```python
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

# 获取值
db_host = config["database"]["host"]

# 修改并保存
config["database"]["port"] = "3306"
with open("settings.ini", "w") as f:
    config.write(f)
```

#### 系统命令与子进程
`subprocess`
```python
import subprocess

# 运行命令并获取输出
result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
print(result.stdout)

# 简写方式
output = subprocess.getoutput("df -h")
print(output)


# 执行命令并检查是否成功
subprocess.check_call(["ls", "-l"])



# 等效命令 `ping google.com`
process = subprocess.Popen(
    ["ping", "-c", "3", "google.com"],
    stdout=subprocess.PIPE,
    text=True
)

for line in process.stdout:
    print(line.strip())

```

`shutil` 
```python
import shutil

# 复制文件
shutil.copy("a.txt", "backup/a.txt")
# 复制并保留修改时间、权限
shutil.copy2("test.txt", "backup/")
#复制整个目录
shutil.copytree("project", "project_backup")


# 移动文件
shutil.move("backup/a.txt", "final/a.txt")

# 删除整个目录
shutil.rmtree("temp")

# 打包压缩
shutil.make_archive("backup", "zip", "project_folder")
# 解压文件
shutil.unpack_archive("backup.zip", "restored")

#修改文件使用者
shutil.chown("file.txt", user="root", group="admin")

#磁盘使用情况
usage = shutil.disk_usage("/")
print(usage.total, usage.used, usage.free)


```


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


