# Mindmap 项目

基于 FastAPI 的模块化思维导图生成和文件管理服务，支持 Markdown 转换为思维导图以及通用文件上传下载功能。采用清晰的模块化架构，易于维护和扩展。

## 功能特性

### 🧠 思维导图功能
- ✅ Markdown 文本转换为思维导图
- ✅ 自动生成 HTML 格式的交互式思维导图
- ✅ 支持在线预览思维导图
- ✅ 基于 markmap-cli 的专业转换
- ✅ 模块化服务架构

### 📁 文件管理功能
- ✅ 通用文件上传（支持多种文件类型）
- ✅ 文件下载和在线预览
- ✅ 文件列表查看
- ✅ 智能文件类型识别
- ✅ 唯一文件名生成（避免冲突）
- ✅ 文件大小限制（50MB）
- ✅ 流式文件处理（避免内存问题）

### 🏗️ 架构特性
- ✅ 模块化设计（功能分离）
- ✅ INI 配置文件管理（配置与代码分离）
- ✅ 统一配置管理和类型转换
- ✅ 热重载支持
- ✅ 清晰的代码结构
- ✅ 易于维护和扩展

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

### 快速启动

```bash
python main.py
```

### 配置设置

首次运行前，请确保 `config.ini` 文件存在。如果不存在，系统将使用默认配置运行。

可以根据需要修改 `config.ini` 中的配置项：
- 服务器端口和主机地址
- 文件上传大小限制
- 调试模式开关

### 启动服务

```bash
python main.py
```

服务将在 `http://0.0.0.0:6066` 启动，支持热重载

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
curl -X POST "http://localhost:6066/upload" \
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
curl -X POST "http://localhost:6066/upload-file" \
  -F "file=@example.pdf"
```

### 3. 获取文件列表

```bash
curl -X GET "http://localhost:6066/files"
```

### 4. 下载文件

```bash
curl -X GET "http://localhost:6066/download/filename.pdf"
```

## 项目架构

### 模块化设计

项目采用清晰的模块化架构，功能分离，易于维护：

- **main.py** - FastAPI 应用入口和路由注册
- **config.py** - 统一配置管理
- **module/** - 核心功能模块目录
  - **mindmap_service.py** - 思维导图生成服务
  - **file_service.py** - 文件上传下载服务

### 模块详细说明

#### 1. main.py - 应用入口
- FastAPI 应用初始化
- 路由注册和管理
- 统一的 API 文档生成
- 服务启动配置

#### 2. config.py - 配置管理
- 读取 ini 配置文件
- 集中化配置常量管理
- 目录路径管理
- MIME 类型映射
- 配置参数类型转换

#### 3. module/mindmap_service.py - 思维导图服务
- `MindmapService` 类封装所有思维导图相关功能
- Markdown 文件处理和转换
- markmap-cli 命令执行
- HTML 文件生成和管理

#### 4. module/file_service.py - 文件管理服务
- `FileService` 类封装所有文件操作
- 流式文件上传（避免内存问题）
- 智能 MIME 类型识别
- 文件列表和下载管理
- 集中化配置常量
- 目录路径管理
- MIME 类型映射
- 服务器参数配置

### 目录结构

```
mindmap/
├── main.py                 # FastAPI 启动类和路由注册
├── config.py              # 配置文件读取和管理
├── config.ini             # 项目配置文件 (NEW)
├── module/                # 核心功能模块目录
│   ├── __init__.py        # 模块初始化文件
│   ├── mindmap_service.py # 思维导图相关功能模块
│   └── file_service.py    # 文件上传下载功能模块
├── README.md              # 项目说明
├── .gitignore            # Git 忽略文件
└── static/              # 静态文件目录
    ├── *.pdf            # 上传的文件
    ├── *.png            # 上传的图片
    ├── ...              # 其他上传文件
    ├── markdown/        # Markdown 文件存储目录
    │   ├── *.md         # 原始 Markdown 文件
    │   └── ...
    └── html/            # 生成的思维导图 HTML
        ├── *.html       # 思维导图文件
        └── ...
```

## 配置说明

### 配置文件结构

项目现在采用 `config.ini` 文件进行配置管理，配置与代码分离，易于维护和部署：

#### config.ini 配置项

```ini
[server]
host = 0.0.0.0
port = 6066
debug = true

[file_upload]
max_file_size_mb = 50
chunk_size_kb = 8
```

#### 配置说明

**服务器配置 [server]**
- `host`: 服务器绑定地址（默认 0.0.0.0）
- `port`: 服务器端口（默认 6066）
- `debug`: 调试模式开关（默认 true）

**文件上传配置 [file_upload]**
- `max_file_size_mb`: 最大文件大小，单位MB（默认 50）
- `chunk_size_kb`: 文件上传分块大小，单位KB（默认 8）

#### 其他配置

在 `config.py` 中还包含以下硬编码配置：
- `ALLOWED_EXTENSIONS`: 允许的文件类型
- `MIME_TYPES`: 文件类型与 MIME 类型映射
- 目录路径配置

## 注意事项

1. **markmap-cli 依赖**: 思维导图功能需要安装 `markmap-cli`
2. **Windows 环境**: 在 Windows 下使用 PowerShell 执行 markmap 命令
3. **文件命名**: 上传的文件会自动重命名为 `时间戳_UUID.扩展名` 格式
4. **浏览器兼容**: PDF 和图片文件可直接在现代浏览器中打开
5. **目录自动创建**: 首次运行时会自动创建必要的目录
6. **模块化架构**: 功能已分离到不同模块，便于维护和扩展
7. **流式处理**: 文件上传使用流式处理，避免大文件内存问题
8. **热重载**: 开发模式支持代码热重载
9. **离线部署**: 需要是 npm install markmap --prefix ./node_modules_global 将依赖存储到当前的文件夹以备迁移

## 开发指南

### 扩展功能

由于采用模块化架构，可以轻松扩展功能：

1. **添加新的文件处理功能**：在 `module/file_service.py` 中扩展 `FileService` 类
2. **添加新的思维导图功能**：在 `module/mindmap_service.py` 中扩展 `MindmapService` 类
3. **添加新的路由**：在 `main.py` 中注册新的 API 端点
4. **修改配置**：在 `config.py` 中添加新的配置项

### 代码结构原则

- **单一职责**: 每个模块只负责特定功能
- **依赖注入**: 通过配置文件管理依赖
- **错误处理**: 统一的异常处理机制
- **类型提示**: 使用 Python 类型提示提高代码质量

## 自动 API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- **Swagger UI**: http://localhost:6066/docs
- **ReDoc**: http://localhost:6066/redoc

## 许可证

MIT License
