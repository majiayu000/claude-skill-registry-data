---
name: autoplan
preamble-tier: 3
version: 1.0.0
description: |
  自动化 plan review pipeline。依次加载 CEO、design、eng review，
  按 6 条决策原则自动作出大多数判断，只把 taste decisions 和明显冲突
  留给用户最终确认。 (gstack)
benefits-from: [office-hours]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /autoplan

`/autoplan` 是“全套计划审查流水线”：自动跑完 CEO review -> design review -> eng review，并在最后做统一的 approval gate。

## 核心价值

- 少问 15-30 个中间问题
- 让大部分明显决策自动完成
- 把真正需要用户拍板的 taste decision、边界 scope、模型分歧集中到最后一轮

## 六条决策原则

这个 skill 会用一组固定的 decision principles 做 auto-decide。简单说：

- 明显对的选择直接做
- 范围边缘、审美取舍、模型分歧留给用户
- 所有自动决定都写入 decision audit trail

## 执行顺序

必须串行执行，不能跳步：

1. `Phase 0`：保存 restore point，读取上下文与相关 skill 文件。
2. `Phase 1`：CEO review，处理战略、范围、产品方向。
3. `Phase 2`：如果有 UI scope，跑 design review。
4. `Phase 3`：eng review，并引入 dual voices / 外部挑战。
5. `Pre-Gate Verification`：检查每阶段必需产物是否都已生成。
6. `Phase 4`：最终 approval gate，展示 plan summary、taste choices、review scores、cross-phase themes。

## 用户最后要看到什么

- 总共做了多少个决策
- 哪些是 auto-decided
- 哪些是需要用户选的 taste decisions
- 哪些地方模型与用户原方向冲突，必须显式挑战
- 最终 review scores 与是否 ready

## 关键规则

- 如果缺 design doc，先提供 `/office-hours` prerequisite offer。
- 每个阶段的结果都要写回 plan file。
- 如果某个阶段的必需产物没生成出来，不能继续往下走。
