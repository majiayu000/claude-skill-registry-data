---
name: pair-agent
version: 0.1.0
description: |
  把远端 AI agent 配对到你的浏览器里。一次命令会生成 setup key，
  并输出对方 agent 可直接照着执行的接线说明。
  兼容 OpenClaw、Hermes、Codex、Cursor，或任何可发 HTTP 请求的 agent。
  远端 agent 会拿到一个带作用域控制的独立 tab，默认 read+write，需要时可申请 admin。
  当用户说“pair agent”“connect agent”“share browser”“remote browser”
  “让另一个 agent 用我的浏览器”或“给它浏览器权限”时使用。 (gstack)
  Voice triggers（语音别名）："pair agent"、"connect agent"、"share my browser"、
  "remote browser access"。
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /pair-agent

给另一个 AI agent 发一把“浏览器钥匙”，让它在自己的 tab 里远程协作。

## 工作方式

- 同机模式：把凭据直接写给本机上的另一个 agent / host
- 远程模式：通过 ngrok 暴露连接入口，并输出可复制的 instruction block

## 主流程

1. 检查 browse server 是否已启动，必要时先拉起。
2. 询问目标 host：
   - OpenClaw
   - Codex / OpenAI Agents
   - Cursor
   - 另一个 Claude Code
   - 其他通用 HTTP agent
3. 询问是同机还是异机。
4. 执行 pairing：
   - 同机：直接写本机凭据
   - 异机：检查 ngrok 是否安装 / 已认证，并生成完整接线说明
5. 验证远端 agent 是否已连上。

## 远端 agent 能做什么

- 默认权限：导航、点击、表单、截图、读取页面、开新 tab
- `--admin`：额外允许 JS 执行、cookie / storage 访问

## 关键规则

- 遇到远程接线时，必须把完整 instruction block 输出给用户。
- token 是有作用域和时效的，过期或域名受限时要指导重新配对。
- 支持在最后撤销单个 agent，或轮换 root token 使全部连接失效。
