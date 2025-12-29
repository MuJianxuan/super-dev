# 领域知识库: 桌面端开发 (Electron/Tauri)

> **上下文**: 适用于 `platform="desktop"`，技术栈 Electron 或 Tauri。

## 1. 操作系统集成

### 1.1 窗口管理
- **无边框窗口**: 自定义标题栏需要处理拖拽区域 (`-webkit-app-region: drag`)。
- **多窗口**: 渲染进程间通信必须通过 IPC (主进程中转)。
- **托盘/菜单**: 后台应用必须集成原生系统托盘。

### 1.2 文件系统
- **沙盒机制**: Mac App Store 发布必须开启 App Sandbox，严格限制文件读写。
- **路径**: 严禁硬编码。必须通过 API 获取 `app_data` 或 用户主目录。

## 2. 安全红线
- **Node 集成**: 渲染进程 **严禁** 开启 `nodeIntegration: true`。
- **上下文隔离**: 必须开启 `contextIsolation: true`。
- **预加载脚本**: 仅通过 `contextBridge` 暴露必要的安全 API。
- **CSP**: 加载本地文件必须配置严格的 CSP。

## 3. 分发与升级
- **签名**:
    - macOS: 必须通过公证 (Notarization)，否则无法运行。
    - Windows: 推荐购买 EV 证书 (防止 SmartScreen 拦截)。
- **自动更新**:
    - Electron: 使用 electron-updater。
    - Tauri: 内置 Updater，需配置公钥验签。

## 4. 性能
- **内存占用**: Electron 内存消耗大。
    - *缓解*: 懒加载模块；及时销毁不可见窗口。
- **启动时间**: 使用 V8 Snapshot。
- **原生模块**: 推荐使用 Rust (Tauri) 或 N-API，避免 Python/C++ 编译依赖链问题。
