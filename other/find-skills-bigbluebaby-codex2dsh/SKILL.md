---
name: find-skills
description: 检索已安装技能并给出使用方法。
---

# find-skills（示例夹具技能，脱敏虚构内容）

## 何时使用

- 用户询问"有什么技能可用"或"怎么用某个技能"时。

## 流程

1. 列出技能目录（`~/.codex/skills/`）下的全部技能名。
2. 对每个技能读取 `SKILL.md` 的 name / description。
3. 按相关性排序后输出清单。

## 注意

- 不执行任何技能内容，只做检索与摘要。
