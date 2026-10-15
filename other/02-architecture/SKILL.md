---
name: win-02-architecture
description: Windows App Workflow 阶段 2 —— 技术选型与软件架构。适用场景：需求已定，需要决定用 Electron / Tauri / 原生技术栈，设计进程模型、特权边界与 IPC 契约，并用 ADR 记录每个决策。提炼自 Desktop App Engineer 与 Software Architect。
---

# 阶段 2：技术选型与架构设计

> 目标：在写代码之前确定运行时、进程模型和模块边界。桌面应用的难点不在 UI，而在**不可信渲染内容与操作系统之间的进程边界**——这个边界必须先设计。

## 1. 运行时选型（必须书面记录理由）

### 决策表（来自 Desktop App Engineer）

| 关注点 | Electron | Tauri | 原生（WPF/WinUI3/C# 或 Qt/C++）* |
|---|---|---|---|
| 安装包体积 | ~80–150MB（自带 Chromium） | ~3–15MB（用系统 WebView2） | 通常最小，依赖 .NET 运行时或自包含发布 |
| 空闲内存 | 较高（每应用独立 Chromium） | 较低（共享系统 WebView） | 最低 |
| 渲染一致性 | 全平台一致（自带浏览器） | 随系统 WebView 变化，需测试 | 原生控件，与系统风格一致 |
| 特权侧语言 | Node.js（生态大、招人易） | Rust（内存安全、攻击面小） | C#/C++（系统 API 直达、性能最优） |
| 生态成熟度 | 最深：更新器、崩溃上报、原生模块 | 较年轻，逐个验证插件 | .NET/Qt 生态成熟，但现代化打包工具较少 |
| 适用场景 | 需要像素级一致渲染、重原生模块、团队是 JS 栈 | 体积/内存预算紧、接受 Rust、WebView 差异可测 | 重度系统集成、极致性能、无 web 技术需求 |

\* 原生选项为本 skill 包对仓库内容的补充（仓库聚焦 Electron/Tauri）；只要目标是 Windows 单一平台，原生栈值得纳入比较。

**选型必须回答的 4 个问题**（写进 ADR-001）：
1. 体积和内存预算是多少？
2. 需要哪些系统级集成（托盘、全局快捷键、文件关联、开机自启）？
3. 团队（包括 AI 辅助）最顺手的技术栈？
4. 更新分发方式（自带更新器 vs 手动下载）？

### 架构模式速选（来自 Software Architect）

| 场景 | 选择 |
|---|---|
| 小型本地工具、功能直白 | 分层架构（UI / 应用服务 / 本地数据），别过度设计 |
| 核心逻辑要与 UI、存储、系统 API 解耦以便测试 | 六边形架构（Ports & Adapters）：域逻辑在内，系统调用都是可替换适配器 |
| 有插件/扩展需求 | 模块化单体，显式契约 |
| 简单 CRUD/记录型应用 | 别上 DDD，事务脚本 + 清晰分层即可 |

## 2. 特权边界设计（桌面应用的核心设计，先于任何 UI）

铁律（来自 Desktop App Engineer）：

1. **渲染进程视为不可信**：Electron 必须 `contextIsolation: true`、`nodeIntegration: false`、`sandbox: true`；Tauri 严格按 capability 授权；"这是我们自己的代码"不是例外——XSS 一旦发生它就不是你的代码了。
2. **IPC 是公共 API 面**：
   - 每个通道在**特权侧**校验输入（用 zod / 显式类型校验）
   - 暴露最窄的动词：`saveUserExport(data)`，**绝不**提供 `writeFile(path, data)` 这类通用通道
   - 文件路径由系统对话框让用户选，应用不接受渲染层传来的任意路径
   - 全部 IPC 通道清单必须能在**一个文件里枚举**（安全审计目标：零边界发现）
3. **远程内容永远没有特权**：加载远程 URL 的窗口必须沙箱化、无 IPC，或默认拒绝的白名单。
4. **离线是一等状态**：数据本地优先，联网功能要有明确的同步状态显示。

### 交付物：IPC 契约文档

在写 UI 之前，先写出完整契约（类型化、已校验的动词列表）：

```
通道名                  方向          输入（校验规则）          输出            备注
project:create         renderer→main { name: string ≤120 }     ProjectMeta     写入 %APPDATA%\<app>\projects
project:export         renderer→main { id: uuid, format: csv|json } ExportReceipt  路径由保存对话框决定
update:ready           main→renderer { version }                 —               更新器事件
```

## 3. 数据与存储决策

- **本地数据库**：SQLite（通过 better-sqlite3 / sql.js / Tauri sql 插件 / Microsoft.Data.Sqlite）——桌面默认选择
- **用户数据位置**：`%APPDATA%\<AppName>\`（漫游慎用）或 `%LOCALAPPDATA%\`；导出文件让用户选位置
- **配置**：用户可编辑的配置与内部状态分文件存放
- **备份/导出**：用户数据必须可导出——这是桌面软件的信任底线
- 需要账号同步时才引入云端，且写清冲突解决策略

## 4. ADR（架构决策记录，每个重要决策一份）

```markdown
# ADR-NNN: [决策标题]
## 状态: Proposed | Accepted | Superseded by ADR-XXX
## 背景: 什么问题迫使我们决策？
## 决定: 我们选了什么？
## 后果: 这个决定让什么变容易、什么变难？（权衡，不只写好处）
```

最低限度要写的 ADR：运行时选型、本地存储方案、打包格式、更新策略、是否引入遥测。

## 5. 质量门

| # | 判据 | 证据 | 通过？ |
|---|------|------|--------|
| 1 | 运行时选型有书面理由（4 问全答） | ADR-001 | ☐ |
| 2 | 特权边界与完整 IPC 契约已定义 | 契约文档 | ☐ |
| 3 | 数据存储位置与导出方案已定 | ADR | ☐ |
| 4 | 每个架构决策都有权衡说明 | ADR 集合 | ☐ |
| 5 | 架构复杂度与项目规模匹配（小项目没有微服务/过度抽象） | 自审 | ☐ |

通过后 → 阶段 3（UI/UX 设计）。
