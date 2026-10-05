---
name: review
preamble-tier: 4
version: 1.0.0
description: |
  落地前 PR review。按 diff 对照 base branch，查 SQL 安全、LLM 信任边界、
  条件副作用、文档漂移、scope drift，并在适合时自动修复简单问题。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /review

这是 gstack 的 pre-landing review。重点不是样式建议，而是那些“CI 能过，但一上生产就会炸”的问题。

## 核心流程

1. 检查当前分支与 base branch。
2. 做 `Scope Drift Detection`：
   - 找 plan file
   - 对照 diff 看实现是否偏离承诺
   - 识别 implementation / test / migration 三类应有项
3. 读取 checklist 与 Greptile review comments（如果有）。
4. 获取 diff，并加载 prior learnings。
5. `Critical pass`：核心审查。
6. `Review Army`：按栈和范围分派 specialist 并行审查。
7. `Fix-First Review`：
   - 自动修复 AUTO-FIX 项
   - 把 ASK 项打包问用户
8. 检查 `TODOS.md`、文档漂移、对抗式审查。
9. 持久化 review 结果，并补 learnings。

## 关键特点

- 不是只报问题，也会尽量先修掉明显问题。
- 会做 adversarial review；有 Codex 时还会做 cross-model synthesis。
- 如果没有发现，按原文要求输出 `NO FINDINGS`。

## 关键规则

- findings 优先级高于总结。
- 所有声称“已修复 / 已验证”的内容都需要证据。
- 发现 plan file 与实现脱轨时，要明确写出来。
