"""
文件上传下载服务模块
"""
import os
import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from fastapi import Request, UploadFile, HTTPException
from fastapi.responses import FileResponse, Response
from config import (
    STATIC_DIR, MAX_FILE_SIZE, CHUNK_SIZE,
    ALLOWED_EXTENSIONS, MIME_TYPES, DEFAULT_MIME_TYPE
)


class FileService:
    """文件服务类"""
    
    @staticmethod
    def create_directories():
        """创建必要的目录"""
        os.makedirs(STATIC_DIR, exist_ok=True)
    
    @staticmethod
    def is_allowed_file(filename: str) -> bool:
        """检查文件类型是否允许"""
        return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """生成唯一文件名"""
        timestamp = str(int(time.time()))
        unique_id = str(uuid.uuid4())[:8]
        file_extension = Path(original_filename).suffix
        return f"{timestamp}_{unique_id}{file_extension}"
    
    @staticmethod
    def get_mime_type(filename: str) -> str:
        """根据文件扩展名获取MIME类型"""
        file_extension = Path(filename).suffix.lower()
        return MIME_TYPES.get(file_extension, DEFAULT_MIME_TYPE)
    
    @staticmethod
    def get_preview_url(request: Request, filename: str) -> str:
        """获取文件预览URL"""
        base_url = str(request.base_url)
        return f"{base_url}preview/{filename}"
    
    @staticmethod
    async def upload_file(request: Request, file: UploadFile) -> Dict[str, Any]:
        """
        上传文件到static目录
        """
        # 检查文件是否为空
        if not file.filename:
            raise HTTPException(status_code=400, detail="没有选择文件")
        
        # 检查文件类型
        if not FileService.is_allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型。支持的类型: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        try:
            # 确保static目录存在
            FileService.create_directories()
            
            # 生成唯一文件名
            unique_filename = FileService.generate_unique_filename(file.filename)
            file_path = STATIC_DIR / unique_filename
            
            # 检查文件大小并保存文件
            file_size = 0
            
            # 保存文件 - 使用流式写入避免内存问题
            with open(file_path, 'wb') as f:
                # 重置文件指针到开始位置
                await file.seek(0)
                
                # 分块读取和写入文件
                while True:
                    chunk = await file.read(CHUNK_SIZE)
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
                "message": "文件上传成功",
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "download_url": download_url,
                "file_size": file_size
            }
            
        except HTTPException:
            # 重新抛出HTTP异常
            raise
        except Exception as e:
            # 清理可能创建的文件
            if 'file_path' in locals() and file_path.exists():
                file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    @staticmethod
    def download_file(filename: str) -> FileResponse:
        """
        下载static目录中的文件
        """
        file_path = STATIC_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 根据文件扩展名确定MIME类型
        media_type = FileService.get_mime_type(filename)
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type=media_type
        )
    
    @staticmethod
    def preview_file(filename: str) -> Response:
        """
        预览文件（在浏览器中直接显示）
        主要用于文本文件的预览
        """
        # 支持子目录路径，如 text_files/filename.txt
        file_path = STATIC_DIR / filename
        
        print(f"DEBUG: 预览文件请求: {filename}")
        print(f"DEBUG: 完整路径: {file_path}")
        print(f"DEBUG: 文件是否存在: {file_path.exists()}")
        print(f"DEBUG: STATIC_DIR: {STATIC_DIR}")
        
        if not file_path.exists():
            # 列出static目录下的所有文件来帮助调试
            if STATIC_DIR.exists():
                print(f"DEBUG: static目录内容:")
                for item in STATIC_DIR.rglob('*'):
                    if item.is_file():
                        print(f"  - {item.relative_to(STATIC_DIR)}")
            raise HTTPException(status_code=404, detail=f"文件不存在: {file_path}")
        
        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 如果还是失败，返回二进制内容
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
        
        # 根据文件扩展名确定内容类型
        file_extension = Path(filename).suffix.lower()
        
        if file_extension == '.html':
            # HTML文件，直接渲染
            media_type = 'text/html; charset=utf-8'
        elif file_extension == '.css':
            # CSS文件，直接渲染
            media_type = 'text/css; charset=utf-8'
        elif file_extension == '.js':
            # JavaScript文件，直接渲染
            media_type = 'application/javascript; charset=utf-8'
        elif file_extension in ['.txt', '.md', '.json', '.xml', '.csv', '.log']:
            # 文本文件，在浏览器中显示
            media_type = 'text/plain; charset=utf-8'
        else:
            # 其他文件类型，尝试作为文本显示
            media_type = 'text/plain; charset=utf-8'
        
        # 获取纯文件名（不包含路径）
        display_filename = Path(filename).name
        
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"inline; filename={display_filename}",
                "Cache-Control": "no-cache"
            }
        )
    
    @staticmethod
    def save_text_to_file(request: Request, text_content: str, filename: str) -> str:
        """
        将文本内容保存为文件
        """
        try:
            # 创建文本文件专用目录
            text_files_dir = STATIC_DIR / "text_files"
            text_files_dir.mkdir(exist_ok=True)
            
            # 验证文件名
            if not filename or not filename.strip():
                raise HTTPException(status_code=400, detail="文件名不能为空")
            
            # 清理文件名，移除非法字符
            import re
            clean_filename = re.sub(r'[<>:"/\\|?*]', '_', filename.strip())
            
            # 如果没有扩展名，默认添加.txt
            if not Path(clean_filename).suffix:
                clean_filename += '.txt'
            
            # 检查文件是否已存在，如果存在则添加时间戳
            file_path = text_files_dir / clean_filename
            if file_path.exists():
                timestamp = str(int(time.time()))
                name_part = Path(clean_filename).stem
                ext_part = Path(clean_filename).suffix
                clean_filename = f"{name_part}_{timestamp}{ext_part}"
                file_path = text_files_dir / clean_filename
            
            # 保存文本内容到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            
            print(f"DEBUG: 文件已保存到: {file_path}")
            print(f"DEBUG: 文件是否存在: {file_path.exists()}")
            
            # 获取文件大小
            file_size = file_path.stat().st_size
            
            # 返回预览链接
            preview_url = FileService.get_preview_url(request, f"text_files/{clean_filename}")
            print(f"DEBUG: 生成的预览URL: {preview_url}")
            
            return preview_url
            
        except HTTPException:
            # 重新抛出HTTP异常
            raise
        except Exception as e:
            # 清理可能创建的文件
            if 'file_path' in locals() and file_path.exists():
                file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"保存文本文件失败: {str(e)}")
    
    @staticmethod
    def list_files(request: Request) -> Dict[str, List[Dict[str, Any]]]:
        """
        获取static目录中所有文件的列表
        """
        try:
            if not STATIC_DIR.exists():
                return {"files": []}
            
            files = []
            base_url = str(request.base_url)
            
            # 遍历static目录及其子目录
            for file_path in STATIC_DIR.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    # 跳过html子目录中的文件，但包含text_files目录
                    if file_path.parent.name in ['static', 'text_files']:
                        # 计算相对路径
                        relative_path = file_path.relative_to(STATIC_DIR)
                        stat = file_path.stat()
                        
                        files.append({
                            "filename": str(relative_path),
                            "size": stat.st_size,
                            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "download_url": f"{base_url}download/{relative_path}",
                            "preview_url": f"{base_url}preview/{relative_path}",
                            "category": "text_files" if "text_files" in str(relative_path) else "uploaded"
                        })
            
            return {"files": files}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")
