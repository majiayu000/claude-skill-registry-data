---
name: vibe-batch-orchestrator
description: 批量推进编排 Skill：把“一堆事项/bug/想法/审稿意见”收口为 Assumptions → Triage Queue → Sprint Plan（含并行组/DoD/Gates/回滚）→ Next Backlog；可选将结果落盘到 `<MM_DD>/codex/intake/intake_<topic>.md`、`<MM_DD>/codex/plan/plan_<topic>.md`（以及 `<MM_DD>/codex/exec/exec_<topic>.md`）。适用于“我有一堆事想批量推进/做个冲刺计划/把 backlog 变成可执行任务”等请求。
---

# Vibe Batch Orchestrator（当天落盘版）

## 安全策略（硬约束）
- 执行任何命令/写入任何文件前：先给 3 行以内 Plan 并等待用户确认
- 破坏性操作必须二次确认：删除/覆盖大文件/强推/全仓格式化/改主分支
- 默认只做“最小必要变更”：先产出分诊与计划草案，再进入执行

## 先收口（必须问清）
- `<MM_DD>`：当天目录（例如 `12_31/`）
- `<topic>`：本轮批量事项的统一主题（短、可复用、`hyphen-case`）
- Mode：`work | research | paper | mixed`
- Vibe Level：`explore | ship | polish`
- Must-deliver（必须交付物）：文件/图表/结论/修复点（可为空）
- Forbidden（禁止项）：例如不改主分支、不全仓格式化、不删除
- Items：用户的一堆事项（允许口水化；每行一条）

## 目录协议（强制）
如用户同意“落盘”，默认写入（按需裁剪）：
- Intake：`<MM_DD>/codex/intake/intake_<topic>.md`
- Plan：`<MM_DD>/codex/plan/plan_<topic>.md`
- Exec（可选）：`<MM_DD>/codex/exec/exec_<topic>.md`
- Manifest / 日更 / 待办（可选）：分别交给 `artifact-manifest-writer`、`daily-vibe-update`

若目标文件已存在：先给差异摘要，等待用户确认后再覆盖/更新。

## 执行前先给 Plan（强制）
在真正写文件或推进执行前，先输出 3 行以内的计划，让用户确认：
1) 归一输入并输出 Triage Queue（含优先级与风险）
2) 选择本轮 Sprint（只做最值钱的 20%）并生成 Sprint Plan（含 DoD/Gates）
3) （如确认落盘）写入 intake/plan/exec，并给下一步执行建议

## Batch Intake 模板（发给用户复制填写）
```text
- <MM_DD>:
- <topic>:
- Mode: work | research | paper | mixed
- Vibe Level: explore | ship | polish
- Must-deliver:
- Forbidden:
- Items:
  1) ...
  2) ...
  3) ...
```

## 输出格式（强制）
每次执行至少在对话里按以下结构输出：
1) Assumptions（假设与范围）
2) Batch Triage（表格：ID | 类型 | 目标 | 依赖 | 风险 | 估计工作量 | 优先级 | 进入本次 Sprint(Y/N)）
3) Sprint Plan（Sprint Goal + 执行顺序/并行组 + 每项 DoD + Gates + 回滚策略）
4) Next Backlog（未进入本轮 Sprint 的事项 + 缺失信息/外部依赖）

## 操作步骤
1) 归一 Items：每条补齐“目标/最小产物/验收方式（最小证据）/风险”
2) 自动打标签（示例）：`FIX | FEAT | REFACTOR | EXP | PAPER | DOC | OPS`
3) 估计 Effort/Risk（你自己填分，不要追问用户每个分），给出优先级与进入 Sprint 建议
4) 生成 Sprint Plan：
   - 把进入 Sprint 的事项改写成可执行 Tasks（动词开头）
   - 写 Dependencies；能并行的任务分组
   - 为每个 Task 写 DoD（可验证）与最小证据（文件/命令/日志关键字）
   - 给出回滚点（高风险任务必填）
5) Gates（按 Mode 最小集合）：
   - work/code：最小可运行入口 +（按需）测试/校验
   - research：seed/配置快照 + baseline/消融（按需）
   - paper：可编译/术语一致/引用一致（按需）
6) 如用户确认“落盘”：
   - 用 `intake-normalizer` 的模板生成 `intake_<topic>.md`
   - 用 `plan-md-writer` 的模板生成 `plan_<topic>.md`
   - 如需要执行序列：用 `plan-md-executor` 生成 `exec_<topic>.md`
7) 返回下一步建议：
   - 开始执行 Sprint 的第一条任务（先低成本/快速失败项）
   - Sprint 完成后：用 `artifact-manifest-writer` 产出 manifest；用 `daily-vibe-update` 汇总日更/待办

## PHM-Vibench 门禁包（可选）
当 Sprint 涉及本仓库代码时，Gates 可优先从下列命令中选择最少集合：
- `python main.py --config configs/demo/00_smoke/dummy_dg.yaml`
- `python -m scripts.validate_configs`
- `python -m pytest test/`

## 完成判定（DoD）
- 对话输出包含：Assumptions + Triage 表 + Sprint Plan + Next Backlog
- 若用户确认落盘：对应文件已创建在约定路径
