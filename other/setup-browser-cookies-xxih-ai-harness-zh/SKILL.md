---
name: setup-browser-cookies
preamble-tier: 1
version: 1.0.0
description: |
  把真实 Chromium 浏览器中的 cookies 导入无头 browse 会话。会打开交互式选择器，
  让用户决定导入哪些域名。适用于测试需要登录态的页面。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /setup-browser-cookies

用于把你真实浏览器里的登录态导进 gstack 的 headless browse 会话。

## 先决判断

- 如果当前已经是 `CDP_MODE=true`，说明你连的是自己的真实浏览器，cookies 已经可用，不需要再导入。

## 工作方式

- 默认先找 browse 二进制并做 setup 检查。
- 然后打开 cookie picker，让用户选择要导入的 cookie domain。
- 也支持用户在命令里直接带 domain，跳过 UI，直接导入指定站点的 cookies。

## 核心步骤

1. 找到可执行的 browse binary。
2. 若未 build，先完成一次性 setup。
3. 打开交互式选择器，或使用用户显式指定的 domain。
4. 导入后做验证，确认 cookies 已进入 headless 会话。

## 适用场景

- QA 已登录页面
- 测试带权限控制的后台
- 需要用真实账号态继续自动化浏览时
