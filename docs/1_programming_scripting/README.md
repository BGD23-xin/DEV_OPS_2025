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

# 列出文件
for f in os.listdir("."):
    print(f)

# 删除文件
os.remove("old.log")

# 读取环境变量
api_key = os.getenv("API_KEY")
```

`pathlib`:

#### 网络请求与接口交互
`requests`
`httpx`

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


