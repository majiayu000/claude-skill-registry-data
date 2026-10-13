---
name: browser-use-zh-cloud
description: >
  使用 Browser Use Cloud 的文档参考 — 浏览器自动化的托管 API 和 SDK。
  当用户需要帮助使用 Cloud REST API（v2 或 v3）、browser-use-sdk（Python 或
  TypeScript）、X-Browser-Use-API-Key 认证、云会话、浏览器配置文件、配置文件
  同步、CDP WebSocket 连接、隐身浏览器、住宅代理、CAPTCHA 处理、Webhook、
  工作区、技能市场、liveUrl 流式传输、定价或集成模式（聊天界面、子代理、
  为现有代理添加浏览器工具）时使用此技能。也适用于 n8n/Make/Zapier 集成、
  云基础设施上的 Playwright/Puppeteer/Selenium、或 1Password 保管库集成
  相关的问题。请勿将此技能用于开源 Python 库（Agent、Browser、Tools
  配置） — 请使用 open-source 技能。
allowed-tools: Read
---

# Browser Use Cloud 参考

Cloud REST API、SDK 和集成模式的参考文档。
根据用户需求阅读相关文件。

## API 与平台

| 主题 | 阅读 |
|------|------|
| 设置、首个任务、定价、常见问题 | `references/quickstart.md` |
| v2 REST API：全部 30 个端点、cURL 示例、Schema | `references/api-v2.md` |
| v3 BU Agent API：会话、消息、文件、工作区 | `references/api-v3.md` |
| 会话、配置文件、认证策略、1Password | `references/sessions.md` |
| CDP 直接访问、Playwright/Puppeteer/Selenium | `references/browser-api.md` |
| 代理、Webhook、工作区、Skills、MCP、实时视图 | `references/features.md` |
| 并行执行、流式传输、地理位置爬取、教程 | `references/patterns.md` |

## 集成指南

| 主题 | 阅读 |
|------|------|
| 构建带有实时浏览器视图的聊天界面 | `references/guides/chat-ui.md` |
| 将 browser-use 作为子代理使用（任务输入 → 结果输出） | `references/guides/subagent.md` |
| 为现有代理添加 browser-use 工具 | `references/guides/tools-integration.md` |

## 重要提示

- Cloud API 基础 URL：`https://api.browser-use.com/api/v2/`（v2）或 `https://api.browser-use.com/api/v3`（v3）
- 认证头：`X-Browser-Use-API-Key: <key>`
- 获取 API Key：https://cloud.browser-use.com/new-api-key
- 设置环境变量：`BROWSER_USE_API_KEY=<key>`
- Cloud SDK：`uv pip install browser-use-sdk`（Python）或 `npm install browser-use-sdk`（TypeScript）
- Python v2：`from browser_use_sdk import AsyncBrowserUse`
- Python v3：`from browser_use_sdk.v3 import AsyncBrowserUse`
- TypeScript v2：`import { BrowserUse } from "browser-use-sdk"`
- TypeScript v3：`import { BrowserUse } from "browser-use-sdk/v3"`
- CDP WebSocket：`wss://connect.browser-use.com?apiKey=KEY&proxyCountryCode=us`
