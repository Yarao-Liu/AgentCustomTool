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

# 静态文件配置
JS_DIR = BASE_DIR / "htmljs"
CSS_DIR = BASE_DIR / "htmljs"  # CSS文件也在htmljs目录中

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

# 服务器配置
SERVER_HOST = config.get('server', 'host')
SERVER_PORT = config.getint('server', 'port')
DEBUG = config.getboolean('server', 'debug')

# 静态文件暴露配置
STATIC_FILES_CONFIG = {
    'js': {
        'path': str(JS_DIR),
        'url_prefix': '/htmljs',
        'enabled': config.getboolean('static_files', 'enable_js_exposure') if 'static_files' in config else True,
        'files': [
            'index.js',
            'd3.min.js',
            'style.css',
            'browser/index.js'
        ]
    },
    'html': {
        'path': str(STATIC_HTML_DIR),
        'url_prefix': '/html',
        'enabled': config.getboolean('static_files', 'enable_js_exposure') if 'static_files' in config else True,
        'files': [
            '*.html'
        ]
    },
    'static': {
        'path': str(STATIC_DIR),
        'url_prefix': '/static',
        'enabled': config.getboolean('static_files', 'enable_static_exposure') if 'static_files' in config else True
    }
}

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.doc', '.docx',
    '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.html', '.css', '.js',
    '.json', '.xml', '.csv', '.mp3', '.mp4', '.avi', '.mov'
}

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

# 获取可用的JS文件列表
def get_available_js_files():
    """获取可用的JS文件列表"""
    js_files = []
    if JS_DIR.exists():
        for file_path in JS_DIR.rglob('*.js'):
            relative_path = file_path.relative_to(JS_DIR)
            js_files.append(str(relative_path))
        for file_path in JS_DIR.rglob('*.css'):
            relative_path = file_path.relative_to(JS_DIR)
            js_files.append(str(relative_path))
    return js_files

# 获取静态文件访问URL
def get_static_file_url(file_path: str, static_type: str = 'js') -> str:
    """获取静态文件的访问URL"""
    if static_type == 'js':
        return f"http://{SERVER_HOST}:{SERVER_PORT}/htmljs/{file_path}"
    elif static_type == 'html':
        return f"http://{SERVER_HOST}:{SERVER_PORT}/html/{file_path}"
    elif static_type == 'static':
        return f"http://{SERVER_HOST}:{SERVER_PORT}/static/{file_path}"
    return None
