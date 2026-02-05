---
name: skill-pattern-capture
description: 在对话中识别可复用流程并提议沉淀为 skill。适用于出现明确步骤、重复任务、或用户表达“以后都这样做/自动化”的场景。
---

# Skill 模式捕获

## 概述

从对话中识别可复用流程，提出 skill 建议，并在用户确认后创建/更新 `SKILL.md`。

## 流程

1. 识别信号
   - 关键词：“以后都这样做”、“自动化”、“可复用”等。
   - 明确步骤（A → B → C）。
   - 同类任务在近期多次出现。

2. 提议 skill
   - 给出短小的 hyphen-case 名称。
   - 说明 skill 的用途与触发场景。
   - 向用户征求创建/更新确认。

3. 创建或更新（确认后）
   - 路径：`.codex/skills/<skill-name>/SKILL.md`（Windows/Linux 通用）
   - 必含：简述、适用场景、输入（Input）、输出（Output）、步骤（Steps）。

4. 说明与回执
   - 给出变更摘要。
   - 说明后续触发方式。

## 备注

- 未经明确同意不得改动 skills。
- 内容简洁、结构清晰。
