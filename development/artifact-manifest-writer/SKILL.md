---
name: artifact-manifest-writer
description: 将一次执行的改动/命令/验证/产物整理成结构化 `manifest_<topic>.json`，并落盘到 `<MM_DD>/codex/artifact/`，用于证据链与可追溯交付。适用于“写manifest/记录证据链/把今天做了什么落成json/生成artifact清单”等请求。
---

# Artifact Manifest Writer（当天落盘版）

## 目录协议（强制）
- 输出：`<MM_DD>/codex/artifact/manifest_<topic>.json`
- `deliverables[]` 中的路径必须位于 `<MM_DD>/` 下
- 若目标文件已存在：先给差异摘要，等待用户确认后再覆盖/更新

## 执行前先给 Plan（强制）
在写文件前，先输出 3 行以内的计划，让用户确认：
1) 收集 changes/commands/verification/deliverables
2) 填充 manifest schema 并校验路径
3) 写入 `manifest_<topic>.json`

## Schema（必须字段；key 必须在）
```json
{
  "run_id": "",
  "date": "<MM_DD>",
  "mode": "mixed",
  "topic": "<topic>",
  "tasks": [],
  "inputs": {},
  "changes": { "files_changed": [], "summary": "" },
  "commands": [],
  "verification": { "gates_passed": [], "gates_failed": [], "results": "" },
  "deliverables": [],
  "risks": "",
  "rollback": "",
  "next_backlog": []
}
```

## 操作步骤
1) 要求用户给出（或确认）`<MM_DD>` 与 `<topic>`
2) 让用户提供材料（或从对话中提取）：
   - 改了哪些文件（路径列表）
   - 跑了哪些命令（按顺序）
   - 结果/验证（通过了哪些门禁、失败了哪些、关键输出）
   - 产物路径（必须在当天目录）
   - 风险/回滚/下一步
3) 按 schema 填充：
   - `changes.files_changed[]`：文件路径数组
   - `commands[]`：命令数组（字符串）
   - `verification`：gates_passed/gates_failed/results
   - `deliverables[]`：路径数组（强制检查都以 `<MM_DD>/` 开头）
4) 创建目录（如不存在）：`<MM_DD>/codex/artifact/`
5) 写入 JSON（确保合法 JSON：双引号、无尾逗号）

## 完成判定（DoD）
- `manifest_<topic>.json` 已创建在约定路径且为合法 JSON
- `deliverables[]` 路径全部位于当天目录
