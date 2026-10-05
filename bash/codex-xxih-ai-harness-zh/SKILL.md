---
name: codex
preamble-tier: 3
version: 1.0.0
description: |
  OpenAI Codex CLI 包装器。支持 review、challenge、consult 三种模式：
  独立 code review、对抗式挑战、以及带会话连续性的开放咨询。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /codex

这是 gstack 的“第二模型视角”。目的不是重复 Claude 的判断，而是引入一个真正独立的审查声音。

## 三种模式

### review

- 对当前 diff 或 plan 做独立审查
- 有 pass / fail gate
- 可把结构化结果写回 plan file 或 review 报告

### challenge

- 用更对抗的姿态去“试图打爆你的代码”
- 适合部署前、复杂重构后、或者你怀疑还有隐藏坑时

### consult

- 把 Codex 当作带 session continuity 的外部顾问
- 适合开放讨论、追问、连续咨询

## 核心流程

1. 检查 codex binary 是否可用，不可用就直接停下。
2. 识别当前运行模式。
3. 针对不同模式选择模型与 reasoning level。
4. 在 review / challenge 场景下，对 diff 或 plan 生成结构化输出。
5. 在 consult 模式下，尝试复用历史 session，保持上下文连续。

## 特别说明

- 用户可以指定模型，或用 `--xhigh` 提高 reasoning。
- 大 diff 会估算 cost。
- 当 `/review` 和 `/codex` 都跑过时，gstack 倾向于做 cross-model synthesis。
