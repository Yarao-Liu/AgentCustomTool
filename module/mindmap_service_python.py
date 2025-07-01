"""
思维导图服务模块 - Python 版本（无需外部依赖）
"""
import os
import time
import re
from pathlib import Path
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse
from config import MARKDOWN_DIR, STATIC_HTML_DIR


class MindmapServicePython:
    """思维导图服务类 - Python 版本"""
    
    @staticmethod
    def create_directories():
        """创建必要的目录"""
        os.makedirs(MARKDOWN_DIR, exist_ok=True)
        os.makedirs(STATIC_HTML_DIR, exist_ok=True)
    
    @staticmethod
    def generate_filename():
        """生成基于时间戳的文件名"""
        return str(int(time.time()))
    
    @staticmethod
    def parse_markdown_to_mindmap(markdown_content):
        """将Markdown内容解析为思维导图数据结构"""
        lines = markdown_content.split('\n')
        mindmap_data = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 解析标题层级
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                mindmap_data.append({
                    'level': level,
                    'title': title,
                    'type': 'heading'
                })
            # 解析列表项
            elif line.startswith('- ') or line.startswith('* '):
                content = line[2:].strip()
                mindmap_data.append({
                    'level': 1,
                    'title': content,
                    'type': 'list'
                })
            # 解析数字列表
            elif re.match(r'^\d+\.\s', line):
                content = re.sub(r'^\d+\.\s', '', line).strip()
                mindmap_data.append({
                    'level': 1,
                    'title': content,
                    'type': 'list'
                })
        
        return mindmap_data
    
    @staticmethod
    def generate_html_content(mindmap_data):
        """生成HTML思维导图内容"""
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>思维导图</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .mindmap-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 1200px;
            margin: 0 auto;
        }
        .mindmap-title {
            text-align: center;
            color: #333;
            font-size: 2em;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .mindmap-tree {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .node {
            margin: 10px 0;
            padding: 15px 25px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            text-align: center;
            min-width: 200px;
        }
        .node:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .node.level-1 {
            background: linear-gradient(45deg, #2196F3, #1976D2);
            font-size: 1.2em;
            font-weight: bold;
        }
        .node.level-2 {
            background: linear-gradient(45deg, #FF9800, #F57C00);
            font-size: 1.1em;
        }
        .node.level-3 {
            background: linear-gradient(45deg, #9C27B0, #7B1FA2);
            font-size: 1em;
        }
        .node.level-4 {
            background: linear-gradient(45deg, #607D8B, #455A64);
            font-size: 0.9em;
        }
        .node.level-5 {
            background: linear-gradient(45deg, #795548, #5D4037);
            font-size: 0.85em;
        }
        .node.level-6 {
            background: linear-gradient(45deg, #9E9E9E, #757575);
            font-size: 0.8em;
        }
        .children {
            margin-left: 30px;
            border-left: 3px solid #ddd;
            padding-left: 20px;
        }
        .empty-message {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 50px;
        }
        .generated-info {
            text-align: center;
            color: #999;
            font-size: 0.8em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="mindmap-container">
        <div class="mindmap-title">🧠 思维导图</div>
        <div class="mindmap-tree">
            {content}
        </div>
        <div class="generated-info">
            生成时间: {timestamp}<br>
            由 Mindmap Service 自动生成
        </div>
    </div>
    
    <script>
        // 添加点击展开/收起功能
        document.querySelectorAll('.node').forEach(node => {
            node.addEventListener('click', function() {
                const children = this.nextElementSibling;
                if (children && children.classList.contains('children')) {
                    children.style.display = children.style.display === 'none' ? 'block' : 'none';
                }
            });
        });
        
        // 添加键盘导航
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                // ESC键关闭所有子节点
                document.querySelectorAll('.children').forEach(child => {
                    child.style.display = 'none';
                });
            }
        });
    </script>
</body>
</html>
        """
        
        if not mindmap_data:
            content = '<div class="empty-message">暂无内容</div>'
        else:
            content = MindmapServicePython._build_tree_html(mindmap_data)
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        return html_template.format(content=content, timestamp=timestamp)
    
    @staticmethod
    def _build_tree_html(mindmap_data, level=0):
        """递归构建HTML树结构"""
        html = ""
        i = 0
        
        while i < len(mindmap_data):
            item = mindmap_data[i]
            
            # 如果当前项的层级小于等于当前处理的层级，跳过
            if item['level'] < level:
                break
            
            # 如果当前项的层级等于当前处理的层级
            if item['level'] == level:
                html += f'<div class="node level-{min(item["level"], 6)}">{item["title"]}</div>'
                i += 1
                
                # 查找子项
                children = []
                j = i
                while j < len(mindmap_data) and mindmap_data[j]['level'] > level:
                    children.append(mindmap_data[j])
                    j += 1
                
                if children:
                    html += '<div class="children">'
                    html += MindmapServicePython._build_tree_html(children, level + 1)
                    html += '</div>'
                
                i = j
            else:
                i += 1
        
        return html
    
    @staticmethod
    async def process_markdown(request: Request, content: str):
        """
        处理Markdown内容，生成思维导图
        """
        try:
            # 创建目录
            MindmapServicePython.create_directories()
            
            # 生成文件名
            time_name = MindmapServicePython.generate_filename()
            md_file_name = f"{time_name}.md"
            html_file_name = f"{time_name}.html"
            
            # 保存Markdown文件
            md_file_path = MARKDOWN_DIR / md_file_name
            with open(md_file_path, "w", encoding='utf-8') as f:
                f.write(content)
            
            print(f"Markdown file created: {md_file_path}")
            
            # 解析Markdown并生成思维导图
            mindmap_data = MindmapServicePython.parse_markdown_to_mindmap(content)
            html_content = MindmapServicePython.generate_html_content(mindmap_data)
            
            # 保存 HTML 文件
            html_file_path = STATIC_HTML_DIR / html_file_name
            with open(html_file_path, "w", encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML file created: {html_file_path}")
            
            # 返回预览链接
            base_url = str(request.base_url)
            preview_url = f"{base_url}html/{html_file_name}"
            
            return preview_url
            
        except Exception as e:
            error_msg = f"Error generating HTML file: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    @staticmethod
    def get_html_file(filename: str):
        """获取HTML文件"""
        file_path = STATIC_HTML_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        return FileResponse(str(file_path)) 