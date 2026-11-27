---
name: lark-note
version: 1.0.0
description: "仅当用户或上游配置显式指定 lark-note 时使用，相关请求统一交由 lark-meeting 技能处理。"
metadata:
  requires:
    bins: ["lark-cli"]
    skills: ["lark-meeting"]
---
> [dsh-zrwang-plugin] 本技能收编自 lark-cli 官方 agent skills（MIT）：文件读写用 DSH 的 `read`/`write`/`edit` 工具，命令用 `pwsh`/`bash` 执行 `lark-cli`；需要先安装并登录 lark-cli（`lark-cli auth login`）。文中的 Claude/Codex/Aily 等 harness 对照表仅作参考，按 DSH 工具名替换；`../lark-shared/` 等跨技能引用要求对应技能同时勾选注入。
# Compatibility entry

本技能只用于兼容旧名称，不直接处理业务。

**MUST 完整读取 [`../lark-meeting/SKILL.md`](../lark-meeting/SKILL.md)，并按照其中的路由和行动指南执行。**
