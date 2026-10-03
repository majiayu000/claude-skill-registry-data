---
name: issue-driven-delivery
description: 用于管理“先有方案、再写 todolist/issues、待用户审核方案、再按 issue 顺序实现并逐项 review”的交付流程。方案可以来自用户直接提供、用户与 Codex 共创、或 Codex 按需整理生成。当用户希望把方案落到仓库根目录 `.work-plans/` 下，并在审核通过后按 issue 顺序推进实现与 review 时，使用这个 skill。
---

# Issue Driven Delivery

把一轮交付收敛为固定流程：
1. 确认或补齐方案。
2. 在仓库根目录创建 `.work-plans/`。
3. 把方案写成 `.work-plans/<topic>-todolist.md`。
4. 把方案拆成 `.work-plans/<topic>-issues.csv`。
5. 用户要求先审核时，停在文档阶段等待确认。
6. 审核通过后按 issue 顺序实现、更新进度、完成 review。
7. 默认不做阶段性总结，等全部 issue 完成后统一汇报；只有用户明确要求时才中途汇报。

## 规则

- 方案来源不限：用户可直接提供，也可与 Codex 共创；只有方案不完整或有冲突时，才按需补读代码、文档、规范。
- 触发 skill 后，可以先通过多轮对话与用户共同收敛方案；方案未定稿前，不进入 issue 执行阶段。
- 本轮交付物默认都写在 `.work-plans/` 下，后续补充、审核、执行、review 都以这里的文件为基准。
- `todolist` 负责记录目标、范围、基线、阶段计划、验收标准和执行顺序。
- `issues` 负责记录可执行切片、依赖、完成标准、review 标准、进度和状态。
- 顺序执行 issue 时，每完成一项就先更新跟踪文件，再进入下一项。
- review 只有在代码、文档、验证结果都对齐后才能标记通过。
- 需要字段级检查和更新纪律时，读取 [references/artifact-checklist.md](references/artifact-checklist.md)。

## 触发示例

- `用 $issue-driven-delivery 先和我一起把方案讨论清楚，再写 todolist 和 issues`
- `按 $issue-driven-delivery 流程推进这轮需求，先出方案给我审核`
- `我已经有方案了，用 $issue-driven-delivery 把它落成 todolist/issues`
- `用 $issue-driven-delivery 继续执行 `.work-plans/` 里这轮 issue，全部完成后统一汇报`
