---
name: browser
description: 用于浏览器自动化与网页抓取的最小 Chrome DevTools Protocol 工具集。当你需要启动 Chrome、导航页面、执行 JavaScript、截图或交互式选择 DOM 元素时使用。触发词包括 “browse website”、“scrape page”、“take screenshot”、“automate browser”、“extract DOM”、“web scraping”。
metadata:
  author: iamzhihuix
  version: "1.0.0"
---

# Browser Tools

一组用于协作式站点探索与抓取的最小 CDP 工具。

**鸣谢**：基于 [Mario Zechner](https://mariozechner.at) 的文章 [What if you don't need MCP?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/)，并在 [Factory.ai](https://docs.factory.ai/guides/skills/browser) 的版本基础上改编。

## Setup

首次使用前，请先安装依赖：

```bash
npm install --prefix skills/browser
```

## Start Chrome

```bash
./skills/browser/scripts/start.js              # 全新 profile
./skills/browser/scripts/start.js --profile    # 复制你的 profile（cookies、登录态）
```

在 `:9222` 启动开启远程调试的 Chrome。

## Navigate

```bash
./skills/browser/scripts/nav.js https://example.com
./skills/browser/scripts/nav.js https://example.com --new
```

在当前标签页导航，或使用新标签页打开。

## Evaluate JavaScript

```bash
./skills/browser/scripts/eval.js 'document.title'
./skills/browser/scripts/eval.js 'document.querySelectorAll("a").length'
```

在当前活动标签页中执行 JavaScript（异步上下文）。

**IMPORTANT**：代码必须是单个表达式；如果有多条语句，请使用 IIFE：

- 单个表达式：`'document.title'`
- 多条语句：`'(() => { const x = 1; return x + 1; })()'`
- 避免在代码字符串中换行，保持单行

## Screenshot

```bash
./skills/browser/scripts/screenshot.js
```

截取当前视口的截图，并返回临时文件路径。

## Pick Elements

```bash
./skills/browser/scripts/pick.js "Click the submit button"
```

交互式元素选择器。点击选择，Cmd/Ctrl+Click 可多选，按 Enter 结束。

## Workflow

1. 使用 `start.js --profile` 启动 Chrome，以复用你当前的登录状态。
2. 通过 `nav.js https://target.app` 驱动页面导航，或用 `--new` 打开辅助标签页。
3. 使用 `eval.js` 检查 DOM，用于快速计数、属性校验或提取 JSON 载荷。
4. 需要视觉证据时用 `screenshot.js`，需要精确选择器或文本快照时用 `pick.js`。

## Usage Notes

- 使用其他工具前先启动 Chrome
- `--profile` 会同步你本机真实的 Chrome profile，因此大多数站点会保持登录状态
- JavaScript 代码在页面中的异步上下文里执行
- `pick` 工具允许你通过点击的方式直观选择 DOM 元素
