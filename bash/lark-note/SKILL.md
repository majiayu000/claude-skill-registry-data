---
name: lark-note
version: 1.0.0
description: "仅当用户或上游配置显式指定 lark-note 时使用，相关请求统一交由 lark-meeting 技能处理。"
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-meeting"]
---

<!-- cowork-exec-note -->
> **⚙️ Cowork / Claude Desktop 执行环境说明（自动注入）**
>
> 本技能依赖本地 `lark-cli`（`@larksuite/cli`，可用 `command -v lark-cli` 定位）及其 `~/.lark-cli` 登录态（应用密钥存于 macOS keychain）。
>
> 在 Cowork 中运行任何 `lark-cli` 命令时，**必须在本地 macOS 上执行**（使用 Desktop Commander 的 `start_process` / `interact_with_process`，或其它本地 shell 工具），**不要用隔离的 Linux 沙箱** `mcp__workspace__bash`——沙箱里没有 lark-cli、也读不到 keychain。
> 执行前确保 npm 全局 bin 目录（`npm prefix -g` 输出目录下的 `bin`）在 PATH 中。
>
> （在 Claude Code 中可忽略本说明，lark-cli 在本机 shell 直接可用。）


# Compatibility entry

本技能只用于兼容旧名称，不直接处理业务。

**MUST 完整读取 [`../lark-meeting/SKILL.md`](../lark-meeting/SKILL.md)，并按照其中的路由和行动指南执行。**
