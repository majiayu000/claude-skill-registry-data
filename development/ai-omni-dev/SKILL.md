---
name: ai-omni-dev
description: AI Omni VSCode Extension 开发指南系统。当需要开发、修改、调试或扩展 AI Omni 插件时使用。优先查阅 ./skills-list.md 确定子模块。支持 Extension 后端开发、Webview Vue3 前端开发、共享层设计、通信机制和 codeXray 功能开发。当用户提到插件开发、webview、extension、命令注册、消息通信、Vue3 组件时使用。
---

# AI Omni 开发指南系统

AI Omni 是一个基于 VSCode 的多功能 AI 插件，集成 Extension 后端 + Vue3 Webview 前端架构。本系统指导整个插件的开发、维护和功能扩展。

## Quick Start

```bash
# 安装依赖
npm install && cd webview && npm install && cd ..

# 构建项目
npm run build

# 调试运行：按 F5 或选择 "Run Extension"
```

## 项目结构总览

```
ai-omni/
├─ package.json              # VS Code 插件主配置
├─ tsconfig.json             # Extension TypeScript 配置
├─ .vscode/
│   ├─ launch.json           # 调试配置
│   └─ tasks.json            # 构建任务
│
├─ extension/                # 插件后端 (Node / VS Code API)
│   ├─ index.ts              # 入口 activate/deactivate
│   ├─ commands/             # 命令注册
│   │   └─ openWebview.ts
│   └─ webview/              # Webview 管理
│       ├─ WebviewPanel.ts
│       └─ getHtml.ts
│
├─ webview/                  # 前端 (Vue3 + Vite)
│   ├─ package.json
│   ├─ vite.config.ts
│   └─ src/
│       ├─ main.ts           # Vue 入口
│       ├─ App.vue           # 根组件
│       ├─ api/vscode.ts     # 通信 API
│       └─ styles/
│
├─ shared/                   # 前后端共享层
│   ├─ types/message.ts      # 消息类型定义
│   └─ constants/
│
├─ prd/                      # 产品需求文档
│   └─ codeXray/brief.md
│
└─ dist/                     # 构建输出
```

## Instructions

### 开发工作流

1. **阅读 [skills-list.md](skills-list.md)** 确定要使用的子模块
2. **根据任务类型路由到对应子模块**：
   - Extension 后端开发 → `modules/extension-dev`
   - Webview 前端开发 → `modules/webview-dev`
   - 共享层与通信 → `modules/shared-layer`
   - codeXray 功能开发 → `modules/codexray`
3. **遵循子模块的开发指南**执行任务
4. **构建并测试**：`npm run build` + F5 调试

### 开发命令

| 命令 | 说明 |
|------|------|
| `npm run build` | 构建整个项目 (Extension + Webview) |
| `npm run build:ext` | 只构建 Extension |
| `npm run build:web` | 只构建 Webview |
| `npm run watch:ext` | 监听模式构建 Extension |
| `npm run dev:web` | Webview 开发模式 (Vite HMR) |

### 添加新功能的标准流程

1. **定义消息类型** (`shared/types/message.ts`)
2. **实现 Extension 处理逻辑** (`extension/`)
3. **实现 Webview UI** (`webview/src/`)
4. **注册命令** (`package.json` contributes + `extension/commands/`)
5. **构建测试** (`npm run build` + F5)

## Best Practices

### 代码规范
- 使用 TypeScript 严格模式
- 共享类型定义放在 `shared/types/`
- Extension 和 Webview 通过 postMessage 通信
- Webview 资源使用 `webview.asWebviewUri()` 转换

### 安全规范
- Webview 启用 CSP (Content Security Policy)
- 使用 nonce 白名单脚本
- 限制 `localResourceRoots`

### 性能规范
- 大文件操作使用流式处理
- AI 调用控制上下文大小，避免 token 溢出
- Webview 组件按需加载

## Requirements

### 环境依赖
- Node.js >= 18
- VS Code >= 1.85.0
- npm 或 pnpm

### 安装步骤
```bash
# 根目录
npm install

# Webview
cd webview && npm install
```

## Advanced Usage

详细的模块开发指南请参阅各子模块：
- [Extension 开发](modules/extension-dev/SKILL.md)
- [Webview 开发](modules/webview-dev/SKILL.md)
- [共享层设计](modules/shared-layer/SKILL.md)
- [codeXray 功能](modules/codexray/SKILL.md)
- [开发工作流](modules/workflow/SKILL.md) - 📌 **推荐先阅读**

### 核心工作流文档

- [Extension ↔ Webview 通信机制](modules/workflow/extension-webview-communication.md)
- [功能点开发标准流程](modules/workflow/feature-development-guide.md)

## 技术栈

- **Extension**: TypeScript + VS Code Extension API
- **Webview**: Vue 3 + Vite + TypeScript
- **通信**: postMessage API + 共享类型
- **AI 引擎**: GitHub Copilot Language Model API (计划)
- **工作流**: LangGraph.js (计划)
