"""
FastAPI 主应用程序
"""
from fastapi import FastAPI, Request, File, UploadFile
from module.mindmap_service import MindmapService
from module.mindmap_service_python import MindmapServicePython
from module.file_service import FileService
from config import SERVER_HOST, SERVER_PORT, DEBUG, USE_PYTHON_VERSION

# 创建FastAPI应用
app = FastAPI(
    title="Mindmap & File Management Service",
    description="思维导图生成和文件管理服务",
    version="1.0.0"
)

# ==================== 基础路由 ====================

@app.get("/")
def root():
    """根路径，返回API信息"""
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
            }
        }
    }

# ==================== 思维导图相关路由 ====================

@app.post("/upload")
async def upload_markdown(request: Request):
    """
    上传Markdown文本，生成思维导图
    """
    content = await request.body()
    content = content.decode('utf-8')
    
    # 根据配置选择使用哪个版本的思维导图服务
    if USE_PYTHON_VERSION:
        preview_url = await MindmapServicePython.process_markdown(request, content)
    else:
        preview_url = await MindmapService.process_markdown(request, content)
    return preview_url

@app.get("/html/{filename}")
def get_html(filename: str):
    """
    获取生成的思维导图HTML文件
    """
    # 根据配置选择使用哪个版本的思维导图服务
    if USE_PYTHON_VERSION:
        return MindmapServicePython.get_html_file(filename)
    else:
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
