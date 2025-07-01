"""
配置文件
"""
import configparser
import sys
from pathlib import Path

def get_base_dir():
    """获取基础目录，兼容exe和开发环境"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe，使用exe所在目录
        return Path(sys.executable).parent
    else:
        # 如果是开发环境，使用脚本所在目录
        return Path(__file__).parent

# 基础配置
BASE_DIR = get_base_dir()
STATIC_DIR = BASE_DIR / "static"
MARKDOWN_DIR = STATIC_DIR / "markdown"
STATIC_HTML_DIR = STATIC_DIR / "html"

# 读取ini配置文件
config = configparser.ConfigParser()
config_file = BASE_DIR / "config.ini"

# 添加调试信息
print(f"Base directory: {BASE_DIR}")
print(f"Config file path: {config_file}")
print(f"Config file exists: {config_file.exists()}")

config.read(config_file, encoding='utf-8')

# 检查配置文件是否成功读取
if not config.sections():
    raise FileNotFoundError(f"配置文件未找到或为空: {config_file}")

# 文件上传配置
MAX_FILE_SIZE = config.getint('file_upload', 'max_file_size_mb') * 1024 * 1024  # 转换为字节
CHUNK_SIZE = config.getint('file_upload', 'chunk_size_kb') * 1024  # 转换为字节

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.doc', '.docx',
    '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.html', '.css', '.js',
    '.json', '.xml', '.csv', '.mp3', '.mp4', '.avi', '.mov'
}

# 服务器配置
SERVER_HOST = config.get('server', 'host')
SERVER_PORT = config.getint('server', 'port')
DEBUG = config.getboolean('server', 'debug')

# 思维导图配置
USE_PYTHON_VERSION = config.getboolean('mindmap', 'use_python_version', fallback=True)

# MIME类型映射
MIME_TYPES = {
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.txt': 'text/plain',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.css': 'text/css',
    '.js': 'application/javascript',
}

# 默认MIME类型
DEFAULT_MIME_TYPE = 'application/octet-stream'
