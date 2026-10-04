---
name: agent-browser
description: >
  Browser automation CLI for AI agents. Use for opening pages, snapshots with
  @e refs, clicking, filling forms, testing web apps, screenshots, PDFs,
  extraction, console/errors, network logs, auth state, Electron app automation,
  Slack automation, exploratory QA, and repeatable browser workflows. Chinese
  triggers include 浏览器自动化, 打开网页, 点按钮, 填表单, 截图, 页面快照,
  accessibility tree, @e 引用, 测网页, QA, 冒烟测试, 浏览器回归, 抓页面文本,
  提取页面数据, Electron 自动化, Slack 自动化.
tags:
  - browser
  - automation
  - cdp
  - qa
  - screenshot
  - extraction
  - electron
  - slack
version: 1
source:
  repo: https://github.com/vercel-labs/agent-browser
  package: agent-browser@0.26.0
  commit: 918d40741151410f6461b13bcb1f8ba4baf1b7f9
license: Apache-2.0
---

# agent-browser

Use `agent-browser` for ordinary browser automation where the agent can own an
isolated Chrome session:

- open a URL, inspect the page, click/fill/type/select/upload/scroll
- take screenshots, PDFs, traces, videos, console logs, and page errors
- extract visible text, HTML, attributes, URLs, counts, boxes, styles, cookies,
  storage, and network requests
- test local web apps with repeatable, command-line browser steps
- run exploratory QA or bug hunts
- automate Electron or Slack when the specialized `agent-browser skills get ...`
  content says to do so

## Runtime

Installed CLI:

```bash
agent-browser --version
agent-browser skills get core
agent-browser skills list
```

Current installation source: npm global package `agent-browser@0.26.0` at
`~/.npm-global/bin/agent-browser`.

## Core Loop

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e3
agent-browser snapshot -i
```

Refs such as `@e3` are fresh per snapshot. Re-snapshot after navigation, form
submit, render changes, dialogs, or tab switches.

If the page loads but basic browser calls time out, treat the rendered app as
untrusted but inspectable: fetch the entry HTML, extract bundled JS assets,
search route strings, and reproduce only the requested UI flow through same-origin
API calls with verification. See `references/react-app-api-fallback.md`.

For Web3 wallet-gated flows, use isolated browser automation only for reconnaissance, then switch to a real Chrome session with wallet extensions via Browser Relay/CDP. See `references/web3-wallet-gated-flows.md`.

Prefer this order:

1. `snapshot -i` and `@e` refs.
2. Semantic locators: `find role`, `find text`, `find label`, `find testid`.
3. CSS selectors.
4. `eval --stdin` for structured extraction or page-specific JS.

## Thinking Triggers

Route here when the reasoning step sounds like:

- "需要实际打开页面看 DOM"
- "先截个图/页面快照"
- "用 accessibility tree 找按钮"
- "我需要点一下/填一下/提交表单"
- "本地 web app 要冒烟测一下"
- "需要确认 UI 是否真的渲染"
- "用浏览器拿页面文本/链接/表格"
- "Electron/Slack 也许可以用浏览器自动化"

## Boundaries

- If the user says 当前浏览器, 真实 Chrome, 已登录态, 复用登录态, 我的浏览器,
  or wants an already-open tab, route first to `devops/badboy-br-aa-routing`.
  Use a npm-global `browser-relay` route only after its binary and MCP wrapper
  are confirmed present.
- For Web3 sites that require wallet extensions (MetaMask, Phantom, Trust,
  Coinbase Wallet), isolated agent-browser sessions often cannot complete the
  flow. Use agent-browser for reconnaissance, but switch to real Chrome via
  Browser Relay/CDP before connecting wallets, signing, claiming points, or
  submitting wallet-gated contributions.
- If the task is front-end signature tracing, JS hook injection, CDP debugger
  breakpoints, AST/source-map/deobfuscation, WASM, or crypto detection, route
  first to `devops/jshookmcp`.
- If the target is web-novel rank scanning or the oh-story browser-CDP workflow,
  prefer the more specific `comm/oh/browser-cdp`.

Use `agent-browser close` or `agent-browser close --all` when the browser
session is no longer needed.
