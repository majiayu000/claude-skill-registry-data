---
name: connect-chrome
version: 0.1.0
description: |
  启动由 gstack 控制、自动加载 Side Panel extension 的真实 Chrome。
  用户可以实时看到 AI 的点击、输入与导航。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /connect-chrome

把 gstack 从纯 headless 浏览器升级成“你看得见的真实 Chrome”。

## 核心流程

1. 做 pre-flight cleanup：
   - 关掉已有 browse server
   - 清理 Chromium profile lock
2. 启动带 Side Panel 扩展的 Chrome，并完成连接。
3. 验证连接状态是否正常。
4. 指导用户打开 Side Panel、理解活动流和聊天侧栏。
5. 跑一个 demo，让用户确认自己能看到实时操作。
6. 说明后续可以怎样继续使用 sidebar chat 和 browser handoff。

## 适用场景

- 需要处理 CAPTCHA、MFA、复杂登录
- 想一边看 agent 操作一边协作
- 需要从 side panel 直接给浏览器内子 agent 发自然语言指令

## 关键点

- 每个 tab 可以有自己的 agent。
- 这是 headed browser，不是隐藏在后台的无头实例。
- 适合与 `/browse`、`/qa`、`/qa-only`、`/design-review` 配合。
