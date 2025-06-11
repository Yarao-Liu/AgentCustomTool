"""
配置文件
"""
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
MARKDOWN_DIR = STATIC_DIR / "markdown"
STATIC_HTML_DIR = STATIC_DIR / "html"

# 文件上传配置
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
CHUNK_SIZE = 8192  # 8KB chunks for file upload

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.doc', '.docx',
    '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.html', '.css', '.js',
    '.json', '.xml', '.csv', '.mp3', '.mp4', '.avi', '.mov'
}

# 服务器配置
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
DEBUG = True

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
