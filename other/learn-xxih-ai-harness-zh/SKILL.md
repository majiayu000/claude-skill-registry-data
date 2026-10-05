---
name: learn
preamble-tier: 1
version: 1.0.0
description: |
  管理 gstack 跨会话沉淀下来的 learnings。支持查看、搜索、清理、导出、
  统计与手工补录。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /learn

`/learn` 用来管理 gstack 在这个项目上积累下来的“可复用经验”：模式、坑点、偏好、架构洞察。

## 子命令

- `/learn`：查看最近 20 条 learnings，按类型分组。
- `/learn search <query>`：按关键词搜索。
- `/learn prune`：检查过期项与冲突项，逐条决定删、留或更新。
- `/learn export`：导出成适合贴进 `CLAUDE.md` 或项目文档的 Markdown。
- `/learn stats`：看总量、去重后数量、类型分布、来源分布、平均置信度。
- `/learn add`：人工补录一条 learning。

## prune 规则

- 如果 learning 关联的文件已经不存在，标记为 `STALE`。
- 如果同一个 `key` 出现冲突洞察，标记为 `CONFLICT`。
- 对每条问题项都通过 `AskUserQuestion` 决定删、留或追加修正版。

## export 结果

导出时按几类组织：

- `Patterns`
- `Pitfalls`
- `Preferences`
- `Architecture`

适合直接纳入项目级约束文档。

## manual add

手工添加时，需要采集：

1. 类型
2. kebab-case 的 key
3. 一句话 insight
4. 置信度
5. 关联文件（可选）
