"""
思维导图服务模块
"""
import os
import sys
import time
import subprocess
import shutil
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse
from config import MARKDOWN_DIR, STATIC_HTML_DIR


class MindmapService:
    """思维导图服务类"""
    
    @staticmethod
    def create_directories():
        """创建必要的目录"""
        os.makedirs(MARKDOWN_DIR, exist_ok=True)
        os.makedirs(STATIC_HTML_DIR, exist_ok=True)
    
    @staticmethod
    def check_markmap_available():
        """检查markmap命令是否可用"""
        markmap_path = shutil.which('markmap')
        return markmap_path is not None
    
    @staticmethod
    def generate_filename():
        """生成基于时间戳的文件名"""
        return str(int(time.time()))
    
    @staticmethod
    async def process_markdown(request: Request, content: str):
        """
        处理Markdown内容，生成思维导图
        """
        try:
            # 创建目录
            MindmapService.create_directories()
            
            # 检查markmap是否可用
            if not MindmapService.check_markmap_available():
                raise HTTPException(
                    status_code=500, 
                    detail="Error: markmap command not found. Please make sure it is installed and added to the system PATH."
                )
            
            # 生成文件名
            time_name = MindmapService.generate_filename()
            md_file_name = f"{time_name}.md"
            html_file_name = f"{time_name}.html"
            
            # 保存Markdown文件
            md_file_path = MARKDOWN_DIR / md_file_name
            with open(md_file_path, "w", encoding='utf-8') as f:
                f.write(content)
            
            print(f"Markdown file created: {md_file_path}")
            
            # 构建markmap命令
            markdown_cmd = f"markmap {md_file_path} --output {MARKDOWN_DIR / html_file_name} --no-open"
            
            # Windows环境使用PowerShell
            if os.name == 'nt':
                markdown_cmd = f"powershell -Command {markdown_cmd}"
            
            print(f"即将执行的命令: {markdown_cmd}")
            
            # 执行markmap命令
            result = subprocess.run(
                markdown_cmd,
                check=True, 
                text=True, 
                shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                universal_newlines=True
            )
            
            print(f"命令返回码: {result.returncode}")
            print(f"命令输出: {result.stdout}")
            print(f"命令错误信息: {result.stderr}")
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, 
                    result.args, 
                    output=result.stdout,
                    stderr=result.stderr
                )
            
            # 移动HTML文件到static/html目录
            source_path = MARKDOWN_DIR / html_file_name
            target_path = STATIC_HTML_DIR / html_file_name
            
            os.replace(str(source_path), str(target_path))
            print(f"HTML file moved to: {target_path}")
            
            # 返回预览链接
            base_url = str(request.base_url)
            preview_url = f"{base_url}html/{html_file_name}"
            
            return preview_url
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Error generating HTML file: {e.output}\n{e.stderr}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

    @staticmethod
    async def process_markdown_replace(request: Request, content: str):
        """
        处理Markdown内容，生成思维导图
        """
        try:
            # 创建目录
            MindmapService.create_directories()

            # 检查markmap是否可用
            if not MindmapService.check_markmap_available():
                raise HTTPException(
                    status_code=500,
                    detail="Error: markmap command not found. Please make sure it is installed and added to the system PATH."
                )

            # 生成文件名
            time_name = MindmapService.generate_filename()
            md_file_name = f"{time_name}.md"
            html_file_name = f"{time_name}.html"

            # 保存Markdown文件
            md_file_path = MARKDOWN_DIR / md_file_name
            with open(md_file_path, "w", encoding='utf-8') as f:
                f.write(content)

            print(f"Markdown file created: {md_file_path}")

            # 构建markmap命令
            markdown_cmd = f"markmap {md_file_path} --output {MARKDOWN_DIR / html_file_name} --no-open"

            # Windows环境使用PowerShell
            if os.name == 'nt':
                markdown_cmd = f"powershell -Command {markdown_cmd}"

            print(f"即将执行的命令: {markdown_cmd}")

            # 执行markmap命令
            result = subprocess.run(
                markdown_cmd,
                check=True,
                text=True,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            print(f"命令返回码: {result.returncode}")
            print(f"命令输出: {result.stdout}")
            print(f"命令错误信息: {result.stderr}")

            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode,
                    result.args,
                    output=result.stdout,
                    stderr=result.stderr
                )

            # 移动HTML文件到static/html目录
            source_path = MARKDOWN_DIR / html_file_name
            target_path = STATIC_HTML_DIR / html_file_name

            os.replace(str(source_path), str(target_path))
            print(f"HTML file moved to: {target_path}")
            #替换文本内容
            # 读取并替换HTML文件内容
            with open(target_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 替换CDN链接为本地路径
            html_content = html_content.replace('https://cdn.jsdelivr.net/npm/d3@7.9.0/dist', '../html')
            html_content = html_content.replace('https://cdn.jsdelivr.net/npm/markmap-toolbar@0.18.10/dist', '../htmljs')
            html_content = html_content.replace('https://cdn.jsdelivr.net/npm/markmap-view@0.18.10/dist/browser/index.js', '../htmljs/index2.js')
            html_content = html_content.replace('https://cdn.jsdelivr.net/npm/markmap-toolbar@0.18.10/dist', '../htmljs')
            # 写回文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("已替换HTML文件中的CDN链接为本地路径")

            # 返回预览链接
            base_url = str(request.base_url)
            preview_url = f"{base_url}html/{html_file_name}"

            return preview_url

        except subprocess.CalledProcessError as e:
            error_msg = f"Error generating HTML file: {e.output}\n{e.stderr}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

    @staticmethod
    def get_html_file(filename: str):
        """获取HTML文件"""
        file_path = STATIC_HTML_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        return FileResponse(str(file_path))
