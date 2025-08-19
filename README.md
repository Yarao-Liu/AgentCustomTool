# Mindmap 项目

基于 FastAPI 的模块化思维导图生成和文件管理服务，支持 Markdown 转换为思维导图以及通用文件上传下载功能。采用清晰的模块化架构，易于维护和扩展。

## 🆕 最新功能特性

### 🎨 SVG矢量图下载功能
- ✅ **高质量SVG矢量图生成** - 支持任意缩放，永不失真
- ✅ **智能页面操作禁止** - 生成过程中自动禁止所有用户操作
- ✅ **美观的图标化界面** - 下载图标 + 状态提示，用户体验更佳
- ✅ **自动错误恢复** - 主方案失败时自动尝试备用方案
- ✅ **实时进度提示** - 准备中 → 分析SVG → 生成SVG → 下载中
- ✅ **超时保护机制** - 15秒超时保护，避免无限等待
- ✅ **取消功能支持** - 用户可随时取消生成过程

## 功能特性

### 🧠 思维导图功能
- ✅ Markdown 文本转换为思维导图
- ✅ 自动生成 HTML 格式的交互式思维导图
- ✅ 支持在线预览思维导图
- ✅ 基于 markmap-cli 的专业转换
- ✅ **新增：一键下载SVG矢量图**
- ✅ **新增：页面操作智能禁止**
- ✅ **新增：图标化用户界面**
- ✅ 模块化服务架构

### 📁 文件管理功能
- ✅ 通用文件上传（支持多种文件类型）
- ✅ 文件下载和在线预览
- ✅ 文件列表查看
- ✅ 智能文件类型识别
- ✅ 唯一文件名生成（避免冲突）
- ✅ 文件大小限制（50MB）
- ✅ 流式文件处理（避免内存问题）

### 🌐 静态文件暴露功能
- ✅ JS 文件通过 HTTP 端口对外暴露
- ✅ 动态配置静态文件目录
- ✅ 支持 CSS、JS、图片等静态资源
- ✅ 自动生成文件访问 URL
- ✅ 文件列表 API 接口

### 📦 打包部署功能
- ✅ PyInstaller 单文件打包
- ✅ 支持 exe 文件独立运行
- ✅ 自动包含配置文件和静态资源
- ✅ 兼容开发和生产环境

### 🏗️ 架构特性
- ✅ 模块化设计（功能分离）
- ✅ INI 配置文件管理（配置与代码分离）
- ✅ 统一配置管理和类型转换
- ✅ 热重载支持
- ✅ 清晰的代码结构
- ✅ 易于维护和扩展
- ✅ 动态静态文件挂载
- ✅ **新增：智能错误处理和恢复机制**

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
pip install fastapi uvicorn python-multipart pyinstaller
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
- 静态文件暴露配置

### 启动服务

```bash
python main.py
```

服务将在 `http://0.0.0.0:6066` 启动，支持热重载

## API 接口

### 1. 根路径
- **GET** `/` - 获取服务状态和可用功能列表

### 2. 思维导图功能
- **POST** `/upload` - 上传 Markdown 文本，生成思维导图
  - 请求体: Markdown 文本内容
  - 返回: 思维导图预览链接

- **POST** `/upload2` - 上传 Markdown 文本，生成可下载SVG的思维导图
  - 请求体: Markdown 文本内容
  - 返回: 思维导图预览链接（包含SVG下载功能）
  - **新功能**: 支持一键下载SVG矢量图

- **GET** `/html/{filename}` - 查看生成的思维导图 HTML

### 3. 文件管理功能
- **POST** `/upload-file` - 上传文件
  - 参数: `file` (multipart/form-data)
  - 返回: 文件信息和下载链接

- **GET** `/download/{filename}` - 下载或预览文件
  - 支持浏览器直接打开 PDF、图片等文件

- **GET** `/files` - 获取所有已上传文件列表
  - 返回: 文件列表，包含文件名、大小、修改时间和下载链接

### 4. 静态文件功能
- **GET** `/js-files` - 获取可用的 JS 文件列表
  - 返回: JS 文件列表和访问 URL

- **GET** `/js/{filename}` - 直接访问 JS 文件
  - 支持访问 js 目录下的所有文件

- **GET** `/static/{filename}` - 访问静态文件
  - 支持访问 static 目录下的所有文件

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

### 2. 生成可下载SVG的思维导图

```bash
curl -X POST "http://localhost:6066/upload2" \
  -H "Content-Type: text/plain" \
  -d "# 我的思维导图
## 分支1
- 子项1
- 子项2
## 分支2
- 子项A
- 子项B"
```

**新功能说明**：
- 使用 `/upload2` 接口生成的思维导图包含SVG下载功能
- 页面右上角会显示"下载SVG"按钮
- 点击按钮可下载高质量的SVG矢量图
- 支持任意缩放，永不失真

### 3. 上传文件

```bash
curl -X POST "http://localhost:6066/upload-file" \
  -F "file=@example.pdf"
```

### 4. 获取文件列表

```bash
curl -X GET "http://localhost:6066/files"
```

### 5. 下载文件

```bash
curl -X GET "http://localhost:6066/download/filename.pdf"
```

### 6. 获取 JS 文件列表

```bash
curl -X GET "http://localhost:6066/js-files"
```

### 7. 访问 JS 文件

```bash
curl -X GET "http://localhost:6066/js/index.js"
```

## 🆕 SVG下载功能详解

### 功能特点

1. **高质量矢量图**
   - 生成SVG格式，支持任意缩放
   - 自动计算最佳尺寸和边距
   - 添加白色背景，确保视觉效果

2. **智能操作禁止**
   - 生成过程中自动禁止所有页面操作
   - 半透明遮罩层，突出当前操作
   - 防止用户误操作影响生成过程

3. **美观的用户界面**
   - 下载图标 + 状态文字组合
   - 不同状态对应不同图标
   - 实时进度提示和状态更新

4. **错误处理和恢复**
   - 主方案失败时自动尝试备用方案
   - 超时保护机制（15秒）
   - 用户可随时取消操作

### 使用流程

1. **访问思维导图页面** - 使用 `/upload2` 接口生成的页面
2. **点击下载按钮** - 页面右上角的"下载SVG"按钮
3. **等待生成完成** - 系统自动禁止页面操作，显示进度
4. **自动下载文件** - 生成完成后自动下载SVG文件
5. **恢复页面操作** - 自动恢复所有页面功能

### 技术实现

- **SVG克隆和优化** - 自动计算尺寸和viewBox
- **页面操作禁止** - 事件监听器拦截所有用户操作
- **状态管理** - 图标和文字的动态更新
- **错误恢复** - 多层备用方案确保成功率

## 打包部署

### PyInstaller 打包

将项目打包成独立的 exe 文件：

```bash
python -m PyInstaller --onefile --add-data "config.ini;." --add-data "js;js" --add-data "static;static" --add-data "module;module" main.py
```

### 打包后的使用

1. **运行 exe 文件**:
   ```bash
   dist/mindmap.exe
   ```

2. **访问服务**:
   - 服务主页: `http://localhost:6066/`
   - JS 文件: `http://localhost:6066/js/index.js`

3. **部署说明**:
   - 将 `dist/mindmap.exe` 复制到目标目录
   - 确保目标目录包含 `config.ini` 文件
   - 双击运行即可启动服务

## 项目架构

### 模块化设计

项目采用清晰的模块化架构，功能分离，易于维护：

- **main.py** - FastAPI 应用入口和路由注册
- **config.py** - 统一配置管理和静态文件配置
- **module/** - 核心功能模块目录
  - **mindmap_service.py** - 思维导图生成服务（包含SVG下载功能）
  - **file_service.py** - 文件上传下载服务

### 模块详细说明

#### 1. main.py - 应用入口
- FastAPI 应用初始化
- 动态静态文件挂载
- 路由注册和管理
- 统一的 API 文档生成
- 服务启动配置

#### 2. config.py - 配置管理
- 读取 ini 配置文件
- 集中化配置常量管理
- 静态文件暴露配置
- 目录路径管理
- MIME 类型映射
- 配置参数类型转换

#### 3. module/mindmap_service.py - 思维导图服务
- `MindmapService` 类封装所有思维导图相关功能
- Markdown 文件处理和转换
- markmap-cli 命令执行
- HTML 文件生成和管理
- **新增：SVG矢量图下载功能**
- **新增：页面操作智能禁止**
- **新增：图标化用户界面**

#### 4. module/file_service.py - 文件管理服务
- `FileService` 类封装所有文件操作
- 流式文件上传（避免内存问题）
- 智能 MIME 类型识别
- 文件列表和下载管理

### 目录结构

```
mindmap/
├── main.py                 # FastAPI 启动类和路由注册
├── config.py              # 配置文件读取和管理
├── config.ini             # 项目配置文件
├── build.spec             # PyInstaller 打包配置
├── test_js_exposure.py    # JS 文件暴露测试脚本
├── JS_EXPOSURE_README.md  # JS 文件暴露功能说明
├── module/                # 核心功能模块目录
│   ├── __init__.py        # 模块初始化文件
│   ├── mindmap_service.py # 思维导图相关功能模块（包含SVG下载）
│   └── file_service.py    # 文件上传下载功能模块
├── htmljs/                # HTML和JavaScript文件目录
│   ├── browser/           # 浏览器专用文件
│   │   └── index.js       # 浏览器 JavaScript
│   ├── d3.min.js          # D3.js 库
│   ├── html2canvas.min.js # HTML转Canvas库
│   ├── index.js           # 主 JavaScript 文件
│   ├── index2.js          # 备用 JavaScript 文件
│   └── style.css          # 样式文件
├── static/                # 静态文件目录
│   ├── *.pdf             # 上传的文件
│   ├── *.png             # 上传的图片
│   ├── markdown/         # Markdown 文件存储目录
│   │   ├── *.md          # 原始 Markdown 文件
│   └── html/             # 生成的思维导图 HTML
│       ├── *.html        # 思维导图文件
└── dist/                 # 打包后的文件目录
    └── mindmap.exe       # 可执行文件
```

## 配置说明

### 配置文件结构

项目采用 `config.ini` 文件进行配置管理，配置与代码分离，易于维护和部署：

#### config.ini 配置项

```ini
[server]
host = 0.0.0.0
port = 6066
debug = true

[file_upload]
max_file_size_mb = 50
chunk_size_kb = 8

[static_files]
enable_js_exposure = true
enable_static_exposure = true
js_directory = js
static_directory = static
```

#### 配置说明

**服务器配置 [server]**
- `host`: 服务器绑定地址（默认 0.0.0.0）
- `port`: 服务器端口（默认 6066）
- `debug`: 调试模式开关（默认 true）

**文件上传配置 [file_upload]**
- `max_file_size_mb`: 最大文件大小，单位MB（默认 50）
- `chunk_size_kb`: 文件上传分块大小，单位KB（默认 8）

**静态文件配置 [static_files]**
- `enable_js_exposure`: 是否启用 JS 文件暴露（默认 true）
- `enable_static_exposure`: 是否启用静态文件暴露（默认 true）
- `js_directory`: JS 文件目录（默认 js）
- `static_directory`: 静态文件目录（默认 static）

## 🆕 SVG下载功能详解

### 功能特点

1. **高质量矢量图**
   - 生成SVG格式，支持任意缩放
   - 自动计算最佳尺寸和边距
   - 添加白色背景，确保视觉效果

2. **智能操作禁止**
   - 生成过程中自动禁止所有页面操作
   - 半透明遮罩层，突出当前操作
   - 防止用户误操作影响生成过程

3. **美观的用户界面**
   - 下载图标 + 状态文字组合
   - 不同状态对应不同图标
   - 实时进度提示和状态更新

4. **错误处理和恢复**
   - 主方案失败时自动尝试备用方案
   - 超时保护机制（15秒）
   - 用户可随时取消操作

### 使用流程

1. **访问思维导图页面** - 使用 `/upload2` 接口生成的页面
2. **点击下载按钮** - 页面右上角的"下载SVG"按钮
3. **等待生成完成** - 系统自动禁止页面操作，显示进度
4. **自动下载文件** - 生成完成后自动下载SVG文件
5. **恢复页面操作** - 自动恢复所有页面功能

### 技术实现

- **SVG克隆和优化** - 自动计算尺寸和viewBox
- **页面操作禁止** - 事件监听器拦截所有用户操作
- **状态管理** - 图标和文字的动态更新
- **错误恢复** - 多层备用方案确保成功率

## 测试功能

### JS 文件暴露测试

运行测试脚本验证 JS 文件暴露功能：

```bash
python test_js_exposure.py
```

测试内容包括：
- 基础 API 功能测试
- JS 文件列表 API 测试
- 具体 JS 文件访问测试
- 示例 URL 访问测试

## 注意事项

1. **markmap-cli 依赖**: 思维导图功能需要安装 `markmap-cli`
2. **Windows 环境**: 在 Windows 下使用 PowerShell 执行 markmap 命令
3. **文件命名**: 上传的文件会自动重命名为 `时间戳_UUID.扩展名` 格式
4. **浏览器兼容**: PDF 和图片文件可直接在现代浏览器中打开
5. **目录自动创建**: 首次运行时会自动创建必要的目录
6. **模块化架构**: 功能已分离到不同模块，便于维护和扩展
7. **流式处理**: 文件上传使用流式处理，避免大文件内存问题
8. **热重载**: 开发模式支持代码热重载
9. **静态文件暴露**: JS 文件通过 HTTP 端口对外暴露，支持跨域访问
10. **打包部署**: 支持 PyInstaller 单文件打包，便于部署
11. **离线部署**: 需要是 npm install markmap --prefix ./node_modules_global 将依赖存储到当前的文件夹以备迁移
12. **SVG下载功能**: 使用 `/upload2` 接口生成的思维导图支持SVG下载
13. **页面操作禁止**: SVG生成过程中会自动禁止所有页面操作
14. **图标化界面**: 下载按钮使用图标+文字组合，界面更美观
15. **SVG格式优势**: SVG矢量图支持任意缩放，永不失真，适合打印和展示
16. **浏览器兼容性**: SVG下载功能需要现代浏览器支持，建议使用Chrome、Firefox、Edge等

## 开发指南

### 扩展功能

由于采用模块化架构，可以轻松扩展功能：

1. **添加新的文件处理功能**：在 `module/file_service.py` 中扩展 `FileService` 类
2. **添加新的思维导图功能**：在 `module/mindmap_service.py` 中扩展 `MindmapService` 类
3. **添加新的路由**：在 `main.py` 中注册新的 API 端点
4. **修改配置**：在 `config.py` 中添加新的配置项
5. **添加新的静态文件类型**：在 `config.py` 中的 `STATIC_FILES_CONFIG` 中添加配置
6. **扩展SVG下载功能**：在 `module/mindmap_service.py` 中修改SVG生成逻辑
7. **自定义页面操作禁止**：在 `disablePageOperations()` 函数中添加更多操作限制
8. **优化用户界面**：在 `addSaveButton()` 函数中自定义按钮样式和图标

### 代码结构原则

- **单一职责**: 每个模块只负责特定功能
- **依赖注入**: 通过配置文件管理依赖
- **错误处理**: 统一的异常处理机制
- **类型提示**: 使用 Python 类型提示提高代码质量
- **配置驱动**: 通过配置文件控制功能开关
- **用户体验**: 注重用户界面的美观性和易用性
- **错误恢复**: 实现多层备用方案，确保功能稳定性
- **操作安全**: 在关键操作过程中保护用户免受误操作影响

## 自动 API 文档

启动服务后，可以访问以下地址查看自动生成的 API 文档：

- **Swagger UI**: http://localhost:6066/docs
- **ReDoc**: http://localhost:6066/redoc

## 许可证

MIT License
