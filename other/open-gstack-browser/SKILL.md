---
name: open-gstack-browser
version: 0.2.0
description: |
  启动 GStack Browser，这是一套内置 sidebar extension 的 AI 控制 Chromium。
  会打开一个可见浏览器窗口，让用户实时看到每一步操作。
  侧栏会显示活动流和聊天面板，并默认带上反爬 stealth。
  当用户说“open gstack browser”“launch browser”“connect chrome”
  “open chrome”“real browser”“side panel”或“control my browser”时使用。
  Voice triggers（语音别名）："show me the browser"。
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /open-gstack-browser

把 gstack 的浏览器体验升级成一个你能亲眼看到、还能在 side panel 里继续协作的真实浏览器窗口。

## 核心流程

1. `Pre-flight cleanup`
   - 关掉旧 browse server
   - 清理 Chromium profile lock
2. `Connect`
   - 启动带 sidebar extension、stealth patch 和自定义 branding 的 headed browser
3. `Verify`
   - 确认 `Mode: headed`
   - 读取端口、extension path
4. `Guide the user`
   - 让用户打开 Side Panel
   - 若找不到扩展，则给出手动加载指引
5. `Demo`
   - 跑一次快速导航 / snapshot 演示
6. `Sidebar chat`
   - 告诉用户可以直接在侧栏里给浏览器内 agent 发指令

## 适用场景

- 需要可见浏览器而不是后台 headless
- 需要处理登录、验证码、复杂多步交互
- 想实时观察 agent 动作，或在浏览器侧栏继续协作

## 关键点

- 这是 GStack Browser，不会污染用户平时的主 Chrome。
- side panel 既能看活动流，也能作为聊天入口。
- 成功启动后，后续可和 `/browse`、`/qa`、`/design-review` 等流程配合。
