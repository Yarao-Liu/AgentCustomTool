"""
FastAPI 主应用程序
"""
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from module.mindmap_service import MindmapService
from module.file_service import FileService
from config import SERVER_HOST, SERVER_PORT, DEBUG, STATIC_FILES_CONFIG, get_available_js_files, get_static_file_url

# 创建FastAPI应用
app = FastAPI(
    title="Mindmap & File Management Service",
    description="思维导图生成和文件管理服务",
    version="1.0.0"
)

# 动态挂载静态文件目录
for static_type, config in STATIC_FILES_CONFIG.items():
    if config['enabled']:
        app.mount(config['url_prefix'], StaticFiles(directory=config['path']), name=static_type)
        print(f"已挂载静态文件: {config['url_prefix']} -> {config['path']}")

# ==================== 基础路由 ====================

@app.get("/")
def root():
    """根路径，返回API信息"""
    available_js_files = get_available_js_files()
    
    return {
        "message": "Mindmap & File Management Service",
        "version": "1.0.0",
        "services": {
            "mindmap": "思维导图生成服务",
            "file_management": "文件上传下载服务"
        },
        "endpoints": {
            "mindmap": {
                "upload": "POST /upload - 上传Markdown文本生成思维导图",
                "view": "GET /html/{filename} - 查看思维导图"
            },
            "file_management": {
                "upload": "POST /upload-file - 上传文件",
                "download": "GET /download/{filename} - 下载文件",
                "list": "GET /files - 获取文件列表"
            },
            "static_files": {
                "htmljs": "GET /htmljs/* - 访问JavaScript文件",
                "html": "GET /html/* - 访问HTML文件(思维导图)",
                "static": "GET /static/* - 访问静态文件"
            }
        },
        "js_files": {
            "available": available_js_files,
            "example_urls": [
                get_static_file_url("index.js", "js"),
                get_static_file_url("style.css", "js"),
                get_static_file_url("d3.min.js", "js")
            ]
        }
    }

@app.get("/htmljs-files")
def list_js_files():
    """列出所有可用的JS文件"""
    js_files = get_available_js_files()
    return {
        "message": "可用的JS文件列表",
        "files": js_files,
        "total_count": len(js_files),
        "access_urls": [get_static_file_url(f, "js") for f in js_files]
    }

# ==================== 思维导图相关路由 ====================

@app.post("/upload")
async def upload_markdown(request: Request):
    """
    上传Markdown文本，生成思维导图
    """
    content = await request.body()
    content = content.decode('utf-8')
    
    preview_url = await MindmapService.process_markdown(request, content)
    return preview_url


@app.post("/upload2")
async def upload_markdown_replace(request: Request):
    """
    上传Markdown文本，生成思维导图
    """
    content = await request.body()
    content = content.decode('utf-8')

    preview_url = await MindmapService.process_markdown_replace(request, content)
    return preview_url
@app.get("/html/{filename}")
def get_html(filename: str):
    """
    获取生成的思维导图HTML文件
    """
    return MindmapService.get_html_file(filename)

# ==================== 文件管理相关路由 ====================

@app.post("/upload-file")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """
    上传文件到static目录
    """
    return await FileService.upload_file(request, file)

@app.get("/download/{filename}")
def download_file(filename: str):
    """
    下载或预览文件
    支持浏览器直接打开PDF、图片等文件
    """
    return FileService.download_file(filename)

@app.get("/files")
def list_files(request: Request):
    """
    获取所有已上传文件列表
    """
    return FileService.list_files(request)

# ==================== 应用启动 ====================

def is_running_as_exe():
    """检查是否作为exe运行"""
    import sys
    return getattr(sys, 'frozen', False)

if __name__ == "__main__":
    import uvicorn
    
    # 如果是exe运行，强制关闭热加载
    reload_enabled = False if is_running_as_exe() else DEBUG
    
    print(f"打包后关闭热加载: reload={reload_enabled}")
    
    # 在exe环境中直接传递app对象，而不是字符串
    if is_running_as_exe():
        uvicorn.run(
            app,  # 直接传递app对象
            host=SERVER_HOST,
            port=SERVER_PORT,
            reload=False
        )
    else:
        uvicorn.run(
            "main:app",  # 开发环境使用字符串引用
            host=SERVER_HOST,
            port=SERVER_PORT,
            reload=reload_enabled
        )
