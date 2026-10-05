---
name: health
preamble-tier: 2
version: 1.0.0
description: |
  代码质量仪表盘。包装项目已有的 type checker、linter、test runner、
  dead code detector、shell linter，计算加权 0-10 综合分，并追踪趋势。
  当用户说“health check”“代码质量”“代码库健康度”“跑全部检查”
  或“质量分数”时使用。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /health

把代码库现有质量工具统一跑一遍，产出一个可比较、可趋势化的健康分。

## 核心流程

1. 自动检测 `Health Stack`：
   - type check
   - lint
   - tests
   - dead code
   - shell lint
2. 用 `AskUserQuestion` 向用户确认检测出的工具组合。
3. 分别执行各项工具，并解析错误 / 警告 / fail 数。
4. 按 rubric 计算每一项 0-10 分与 composite score。
5. 输出 dashboard 表格。
6. 将结果追加到 `~/.gstack/projects/$SLUG/health-history.jsonl`。
7. 做 trend analysis，并给出优先级建议。

## 仪表盘内容

- `Project`
- `Branch`
- `Date`
- 各分类 score / status / duration
- `COMPOSITE SCORE`
- 如有低于 7 分的项目，要列出 top issues

## 关键规则

- 这是诊断技能，不直接修问题。
- 每个工具独立执行，避免输出互相污染。
- 趋势分析要对比上一次记录；如果分数下滑，要明确指出下降项和可能原因。
