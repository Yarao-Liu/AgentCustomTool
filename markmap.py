import os
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

# 使用 FastAPI 初始化应用
app = FastAPI()

# 配置
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.doc', '.docx',
    '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.html', '.css', '.js',
    '.json', '.xml', '.csv', '.mp3', '.mp4', '.avi', '.mov'
}

def is_allowed_file(filename: str) -> bool:
    """检查文件类型是否允许"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename: str) -> str:
    """生成唯一文件名"""
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())[:8]
    file_extension = Path(original_filename).suffix
    return f"{timestamp}_{unique_id}{file_extension}"

# 测试根路径
@app.get('/')
def index():
    return "FastAPI server is running!"


# 上传并处理Markdown文件的路径
@app.post('/upload')
async def upload_markdown(request: Request):
    python_path = sys.executable
    print(f"python_path={python_path}")
    content = await request.body()
    content = content.decode('utf-8')
    time_name = str(int(time.time()))  # 生成时间戳作为文件名
    md_file_name = time_name + ".md"  # Markdown文件名
    html_file_name = time_name + ".html"  # HTML文件名
 
    # 创建markdown和html文件夹，如果它们不存在的话
    os.makedirs('markdown', exist_ok=True)
    os.makedirs('static/html', exist_ok=True)
 
    # 将Markdown内容写入文件
    with open(f'markdown/{md_file_name}', "w", encoding='utf-8') as f:
        f.write(content)
 
    print(f"Markdown file created: markdown/{md_file_name}")
 
    current_dir = os.getcwd()
    print(f"Current dir: {current_dir}")
    os.chdir(current_dir)
    # 使用subprocess调用markmap-cli将Markdown转换为HTML，并移动到static/html目录
    try:
 
        print(f"开始markmap")
 
        import shutil
        markmap_path = shutil.which('markmap')
        # 判断markmap是否存在
        if markmap_path is None:
            return "Error: markmap command not found. Please make sure it is installed and added to the system PATH."
 
        #  构建markdown生产html文件命令
        markdown_cmd = f"markmap markdown/{md_file_name} --output markdown/{html_file_name} --no-open"
        # 注意在windows环境下一定要使用powershell执行。默认使用的cmd，会出现生成不了html文件的情况。完全无输出，也不报错。
        if os.name == 'nt':
            # 在Windows上使用PowerShell执行命令
            markdown_cmd = f"powershell -Command markmap markdown/{md_file_name} --output markdown/{html_file_name} --no-open"
 
        print(f"即将执行的命令: {markdown_cmd}")
        # 主要shell=True必须加，不然会吧markdown_cmd里面的内容整个字符串当作一个命令，而不是markmap命令和参数，会报错windows文件不存在
        result = subprocess.run(markdown_cmd,
                                check=True, text=True, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"命令返回码: {result.returncode}")
        print(f"命令输出: {result.stdout}")
        print(f"命令错误信息: {result.stderr}")
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                                stderr=result.stderr)
 
        # 尝试将生成的HTML文件移动到static/html文件夹
        os.replace(f'markdown/{html_file_name}', f'static/html/{html_file_name}')
        print(f"HTML file moved to: static/html/{html_file_name}")
 
        # 返回转换后的HTML文件链接
        base_url = str(request.base_url)
        preview_url = f"{base_url}html/{html_file_name}"
        return f'{preview_url}'
    except subprocess.CalledProcessError as e:
        # 如果转换过程中出现错误，返回错误信息
        return f"Error generating HTML file: {e.output}\n{e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
        
# 提供HTML文件的路径
@app.get('/html/{filename}')
def get_html(filename: str):
    return FileResponse(f'static/html/{filename}')


# 文件上传接口
@app.post('/upload-file')
async def upload_file(request: Request, file: UploadFile = File(...)):
    """
    上传文件到static目录
    """
    # 检查文件是否为空
    if not file.filename:
        raise HTTPException(status_code=400, detail="没有选择文件")

    # 检查文件类型
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。支持的类型: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    try:
        # 确保static目录存在
        os.makedirs('static', exist_ok=True)

        # 生成唯一文件名
        unique_filename = generate_unique_filename(file.filename)
        file_path = Path('static') / unique_filename

        # 检查文件大小（通过file.size属性，如果可用）
        file_size = 0

        # 保存文件 - 使用流式写入避免内存问题
        with open(file_path, 'wb') as f:
            # 重置文件指针到开始位置
            await file.seek(0)

            # 分块读取和写入文件
            chunk_size = 8192  # 8KB chunks
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break

                file_size += len(chunk)

                # 检查文件大小
                if file_size > MAX_FILE_SIZE:
                    # 删除已创建的文件
                    file_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=400,
                        detail=f"文件太大。最大允许大小: {MAX_FILE_SIZE // (1024*1024)}MB"
                    )

                f.write(chunk)

        # 返回下载链接，拼接base URL
        base_url = str(request.base_url)
        download_url = f"{base_url}download/{unique_filename}"

        return {
            "message": "文件保存成功",
            "original_filename": file.filename,
            "saved_filename": unique_filename,
            "download_url": download_url,
            "file_size": file_size
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")


# 文件下载接口
@app.get('/download/{filename}')
def download_file(filename: str):
    """
    下载static目录中的文件
    """
    file_path = Path('static') / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    # 根据文件扩展名确定MIME类型
    file_extension = file_path.suffix.lower()

    # 对于可以在浏览器中直接显示的文件类型，设置正确的MIME类型
    if file_extension == '.pdf':
        media_type = 'application/pdf'
    elif file_extension in ['.png', '.jpg', '.jpeg']:
        media_type = f'image/{file_extension[1:]}'
    elif file_extension == '.gif':
        media_type = 'image/gif'
    elif file_extension in ['.html', '.htm']:
        media_type = 'text/html'
    elif file_extension == '.txt':
        media_type = 'text/plain'
    elif file_extension == '.json':
        media_type = 'application/json'
    elif file_extension == '.xml':
        media_type = 'application/xml'
    elif file_extension == '.css':
        media_type = 'text/css'
    elif file_extension == '.js':
        media_type = 'application/javascript'
    else:
        # 其他文件类型使用通用的下载类型
        media_type = 'application/octet-stream'

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type
    )


# 获取文件列表接口
@app.get('/files')
def list_files(request: Request):
    """
    获取static目录中所有文件的列表
    """
    try:
        static_path = Path('static')
        if not static_path.exists():
            return {"files": []}

        files = []
        for file_path in static_path.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                # 跳过html子目录中的文件，只列出static根目录的文件
                if file_path.parent.name == 'static':
                    stat = file_path.stat()
                    base_url = str(request.base_url)
                    files.append({
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "download_url": f"{base_url}download/{file_path.name}"
                    })

        return {"files": files}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5001)