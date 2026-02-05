---
name: todo-list-csv
description: 当需要修改项目（增删改文件）并希望将 update_plan 与 CSV 有机同步时使用此技能：在项目根目录创建“{任务名} TO DO list.csv”，用 TODO/IN_PROGRESS/DONE 驱动 plan 的 pending/in_progress/completed，同步推进，全部完成后删除该文件。
---

# Todo List CSV

## 目标

在需要修改项目时，用一个位于项目根目录的 CSV 文件把工作拆成可勾选的步骤；在推进过程中持续更新；全部完成后删除该 CSV，避免把临时清单遗留或提交进仓库。

## 触发条件

- 开始执行任何会改动项目内容的任务（新增/修改/删除文件、调整配置、修复 bug、实现功能等）
- 任务具有多个可独立验收的小步骤，且需要显式跟踪完成状态

## 工作流（CSV + update_plan 双轨同步）

### 0) 启用 update_plan 的条件

- 当任务包含 **≥2 个可独立验收步骤** 时，调用 `update_plan` 建立计划并在执行过程中持续更新。

### 1) 拆解步骤并建立 plan（与 CSV 一一对应）

- 拆成 3–12 条可验收步骤（动词开头，避免过长）。
- 立即调用 `update_plan` 建立初始 plan：第 1 步 `in_progress`，其余 `pending`。
- 保持 plan 的每个 `step` 文案与 CSV 的 `item` **完全一致**（便于同步与审计）。

### 2) 在项目根目录创建 `{任务名} TO DO list.csv`

- 确定“任务名”：优先取自用户请求的短标题；必要时做简化（去掉标点、过长截断）。
- 计算“项目根目录”：优先使用 Git 仓库根目录；非 Git 项目则使用当前工作目录作为根目录。
- 在项目根目录创建文件：`{任务名} TO DO list.csv`。

CSV 表头固定为（首行）：

`id,item,status,done_at,notes`

- `id`：从 1 开始的整数
- `item`：单条待办（与 plan 的 `step` 一致）
- `status`：`TODO` / `IN_PROGRESS` / `DONE`
- `done_at`：完成时间（ISO 8601，未完成留空）
- `notes`：可选备注（文件路径、验证方式、PR/commit 等）

### 3) 状态机与映射（核心约束）

- 仅允许状态流转：`TODO` → `IN_PROGRESS` → `DONE`（避免 `TODO` 直跳 `DONE`）。
- plan 映射：`TODO`→`pending`，`IN_PROGRESS`→`in_progress`，`DONE`→`completed`。
- 任意时刻 **最多 1 行** `IN_PROGRESS`；只要仍有未完成项，尽量保持 **恰好 1 行** `IN_PROGRESS`（与 plan 的唯一 `in_progress` 对齐）。

### 4) 推进时同步（每完成一项就同步一次）

- 完成当前 `IN_PROGRESS` 项后：
  1) 更新 CSV（推荐用脚本 `advance` 自动“完成当前项并启动下一项”）
  2) 从 CSV 生成 plan payload（`plan --normalize`）
  3) 调用 `update_plan` 使 plan 与 CSV 同步

### 5) 中途变更与暂停

- 新增步骤：只做“追加”，避免重排/重编号；同时更新 CSV 与 plan。
- 暂停等待反馈：保留 CSV；plan 当前步骤保持 `in_progress`，或追加“等待反馈”步骤并置为 `in_progress`。

### 6) 收尾与清理

- 确认所有行均为 `DONE`，再删除该 CSV 文件（脚本 `cleanup` 会在未全 DONE 时拒绝删除）。
- 调用 `update_plan` 将所有步骤标记为 `completed`，确保对话内计划闭环。

## 可选自动化脚本

使用 `scripts/todo_csv.py` 自动创建/更新/清理 CSV（优先用于避免手工编辑出错）。

示例命令：

- 创建清单（默认第 1 条为 IN_PROGRESS）：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py init --title "修复登录 bug" --item "复现问题" "加回归测试" "修复实现" "运行测试/构建"`
- 计算路径：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py path --title "修复登录 bug"`
- 从 CSV 生成 `update_plan` payload（推荐带 `--normalize`）：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py plan --file "{csv_path}" --normalize --explanation "同步自 TODO CSV"`
- 启动指定步骤：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py start --file "{csv_path}" --id 2`
- 推进一步（完成当前 IN_PROGRESS 并启动下一条 TODO）：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py advance --file "{csv_path}" --notes "已通过单测"`
- 查看进度：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py status --file "{csv_path}" --verbose`
- 全部完成后清理：`python3 ~/.codex/skills/todo-list-csv/scripts/todo_csv.py cleanup --file "{csv_path}"`
