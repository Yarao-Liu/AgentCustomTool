# Mindmap 项目

基于 FastAPI 的思维导图生成和文件管理服务，支持 Markdown 转换为思维导图以及通用文件上传下载功能。

## 功能特性

### 🧠 思维导图功能
- ✅ Markdown 文本转换为思维导图
- ✅ 自动生成 HTML 格式的交互式思维导图
- ✅ 支持在线预览思维导图
- ✅ 基于 markmap-cli 的专业转换

### 📁 文件管理功能
- ✅ 通用文件上传（支持多种文件类型）
- ✅ 文件下载和在线预览
- ✅ 文件列表查看
- ✅ 智能文件类型识别
- ✅ 唯一文件名生成（避免冲突）
- ✅ 文件大小限制（50MB）

## 支持的文件类型

### 可在浏览器直接打开
- **PDF 文件**: `.pdf` - 浏览器内置查看器
- **图片文件**: `.png`, `.jpg`, `.jpeg`, `.gif` - 直接显示
- **文本文件**: `.txt` - 纯文本显示
- **网页文件**: `.html`, `.htm` - 网页渲染
- **代码文件**: `.json`, `.xml`, `.css`, `.js` - 代码显示

### 支持上传的文件类型
- **文档**: `.txt`, `.md`, `.pdf`, `.doc`, `.docx`
- **表格**: `.xls`, `.xlsx`, `.csv`
- **演示文稿**: `.ppt`, `.pptx`
- **图片**: `.png`, `.jpg`, `.jpeg`, `.gif`
- **音视频**: `.mp3`, `.mp4`, `.avi`, `.mov`
- **压缩包**: `.zip`, `.rar`
- **代码文件**: `.html`, `.css`, `.js`, `.json`, `.xml`

## 安装和运行

### 环境要求
- Python 3.7+
- Node.js (用于 markmap-cli)

### 安装依赖

1. **安装 Python 依赖**:
```bash
pip install fastapi uvicorn python-multipart
```

2. **安装 markmap-cli**:
```bash
npm install -g markmap-cli
```

### 启动服务

```bash
python markmap.py
```

服务将在 `http://0.0.0.0:5001` 启动

## API 接口

### 1. 根路径
- **GET** `/` - 获取服务状态

### 2. 思维导图功能
- **POST** `/upload` - 上传 Markdown 文本，生成思维导图
  - 请求体: Markdown 文本内容
  - 返回: 思维导图预览链接

- **GET** `/html/{filename}` - 查看生成的思维导图 HTML

### 3. 文件管理功能
- **POST** `/upload-file` - 上传文件
  - 参数: `file` (multipart/form-data)
  - 返回: 文件信息和下载链接

- **GET** `/download/{filename}` - 下载或预览文件
  - 支持浏览器直接打开 PDF、图片等文件

- **GET** `/files` - 获取所有已上传文件列表
  - 返回: 文件列表，包含文件名、大小、修改时间和下载链接

## 使用示例

### 1. 生成思维导图

```bash
curl -X POST "http://localhost:5001/upload" \
  -H "Content-Type: text/plain" \
  -d "# 我的思维导图
## 分支1
- 子项1
- 子项2
## 分支2
- 子项A
- 子项B"
```

### 2. 上传文件

```bash
curl -X POST "http://localhost:5001/upload-file" \
  -F "file=@example.pdf"
```

### 3. 获取文件列表

```bash
curl -X GET "http://localhost:5001/files"
```

### 4. 下载文件

```bash
curl -X GET "http://localhost:5001/download/filename.pdf"
```

## 目录结构

```
mindmap/
├── markmap.py              # 主服务文件
├── README.md              # 项目说明
├── .gitignore            # Git 忽略文件
├── markdown/             # Markdown 文件存储目录
│   ├── *.md             # 原始 Markdown 文件
│   └── ...
└── static/              # 静态文件目录
    ├── *.pdf            # 上传的文件
    ├── *.png            # 上传的图片
    ├── ...              # 其他上传文件
    └── html/            # 生成的思维导图 HTML
        ├── *.html       # 思维导图文件
        └── ...
```

## 配置说明

在 `markmap.py` 中可以修改以下配置：

- `MAX_FILE_SIZE`: 最大文件大小（默认 50MB）
- `ALLOWED_EXTENSIONS`: 允许的文件类型
- 服务器端口: 默认 5001

## 注意事项

1. **markmap-cli 依赖**: 思维导图功能需要安装 `markmap-cli`
2. **Windows 环境**: 在 Windows 下使用 PowerShell 执行 markmap 命令
3. **文件命名**: 上传的文件会自动重命名为 `时间戳_UUID.扩展名` 格式
4. **浏览器兼容**: PDF 和图片文件可直接在现代浏览器中打开
5. **目录自动创建**: 首次运行时会自动创建必要的目录

## 自动 API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

## 许可证

MIT License
