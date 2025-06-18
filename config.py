"""
配置文件
"""
import configparser
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
MARKDOWN_DIR = STATIC_DIR / "markdown"
STATIC_HTML_DIR = STATIC_DIR / "html"

# 读取ini配置文件
config = configparser.ConfigParser()
config_file = BASE_DIR / "config.ini"
config.read(config_file, encoding='utf-8')

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
