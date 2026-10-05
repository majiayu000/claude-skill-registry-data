---
name: retro
preamble-tier: 2
version: 2.0.0
description: |
  周度工程复盘。分析提交历史、工作时段、热点文件、测试健康与按人贡献，
  并可在 global 模式下跨项目、跨工具汇总。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /retro

`/retro` 是 gstack 的工程周报与复盘器。

## 默认模式

围绕当前仓库生成 engineering retro，主要步骤：

1. 采集原始数据：
   - commits、作者、文件改动、增删行数
   - 提交时段
   - 热点文件
   - PR / MR 编号
   - TODO backlog
   - test 文件变化
   - gstack skill usage telemetry
2. 计算指标：
   - shipping velocity
   - focus score
   - ship of the week
   - 测试健康
   - 团队拆分
3. 检测 work sessions 和时间分布。
4. 保存 retro history，并写 narrative。

## Global 模式

`/retro global` 会跨项目、跨工具（Claude Code / Codex / Gemini 等）做整体复盘：

- 自动发现仓库
- 汇总 commits、sessions、streak
- 统计 context switching
- 分析不同工具使用模式

## 产出结构

- Summary Table
- Trends vs Last Retro
- Time & Session Patterns
- Shipping Velocity
- Code Quality Signals
- Test Health
- Focus & Highlights
- Team Breakdown
- Top 3 Wins / 3 Things to Improve / 3 Habits for Next Week

## 关键规则

- 有 prior retro 时要做趋势对比。
- 只要发现非显而易见的模式或洞察，就要补进 learnings。
