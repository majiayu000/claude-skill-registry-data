---
name: plan-md-writer
description: 基于当天的 Intake 文件生成可执行计划 `plan_<topic>.md`，并落盘到 `<MM_DD>/codex/plan/`；计划包含 Tasks+DoD+Dependencies、可选 Gates、Deliverables（当天目录路径）与 Rollback。适用于“基于intake写计划/生成plan_<topic>.md/补DoD和门禁”等请求。
---

# Plan MD Writer（当天落盘版）

## 目录协议（强制）
- 输入：`<MM_DD>/codex/intake/intake_<topic>.md`
- 输出：`<MM_DD>/codex/plan/plan_<topic>.md`
- Deliverables 必须指向当天目录下的具体文件路径
- 若目标文件已存在：先给差异摘要，等待用户确认后再覆盖/更新

## 执行前先给 Plan（强制）
在写文件前，先输出 3 行以内的计划，让用户确认：
1) 读取 intake 并抽取 Tasks/Goal/Scope
2) 生成 plan 模板并补齐 DoD/Gates/Deliverables/Rollback
3) 写入 `plan_<topic>.md`

## 输出模板（必须块）
```md
# Plan: <topic>

## Goal
...

## Scope
- In:
- Out:

## Tasks
- [ ] T1 ...
  - DoD:
  - Dependencies:
- [ ] T2 ...
  - DoD:
  - Dependencies:

## Gates (optional)
- Gate1:
- Gate2:

## Deliverables
- <MM_DD>/codex/report/report_<topic>.md
- <MM_DD>/codex/artifact/manifest_<topic>.json
- (if needed) <MM_DD>/codex/daily/daily.md

## Rollback
- ...

## Execution Log
- (leave blank)
```

## 操作步骤
1) 要求用户给出（或确认）`<MM_DD>` 与 `<topic>`
2) 读取 `intake_<topic>.md`，抽取并规范化：
   - Goal：一句话目标
   - Scope：In/Out（若 intake 没写，补 “TBD” 并列出假设）
   - Tasks：改写为动词开头、可执行；必要时拆分为 2-5 条
3) 为每个 Task 补 DoD：
   - 以可验证为准（文件/命令/日志/指标）
4) Gates：
   - 默认留空；若用户同意，可从下列门禁中选择加入（按任务相关性选择最少集合）
     - `python main.py --config configs/demo/00_smoke/dummy_dg.yaml`
     - `python -m scripts.validate_configs`
     - `python -m pytest test/`
5) Deliverables：
   - 固定至少包含 manifest 路径；report 若本轮不产出则标注 “TBD/由后续生成”
6) Rollback：
   - 写清“失败如何回退到安全状态”（例如撤销变更/恢复文件/仅保留草案）
7) 创建目录（如不存在）：`<MM_DD>/codex/plan/`
8) 写入 `plan_<topic>.md`

## 完成判定（DoD）
- `plan_<topic>.md` 已创建在约定路径
- 每个 Task 都有 DoD；Deliverables 全部是当天目录路径
