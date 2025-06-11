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
from fastapi.responses import FileResponse
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
    def list_files(request: Request) -> Dict[str, List[Dict[str, Any]]]:
        """
        获取static目录中所有文件的列表
        """
        try:
            if not STATIC_DIR.exists():
                return {"files": []}
            
            files = []
            base_url = str(request.base_url)
            
            for file_path in STATIC_DIR.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    # 跳过html子目录中的文件，只列出static根目录的文件
                    if file_path.parent.name == 'static':
                        stat = file_path.stat()
                        files.append({
                            "filename": file_path.name,
                            "size": stat.st_size,
                            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "download_url": f"{base_url}download/{file_path.name}"
                        })
            
            return {"files": files}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")
