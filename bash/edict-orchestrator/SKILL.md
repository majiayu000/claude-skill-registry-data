---
name: edict-orchestrator
description: 三省六部任务状态机执行入口——唯一允许推进状态、追加 flow_log/progress_log 的 skill；所有变更通过 edict_tasks_api.py 完成
version: 0.1.0
tags: [edict, scheduler, state-machine]
---

# Edict Orchestrator

你是**三省六部任务编排**的执行入口。任何对任务状态、流转记录、进展汇报的**修改**都必须通过本 skill 所规定的 **`edict_tasks_api.py` 子命令**完成，不得直接使用 `write_file` 修改 `.edict/edict-tasks.json`。

- **只读查看**：可用 `read_file` 读取 `.edict/edict-tasks.json` 查看当前任务列表与状态。
- **任何写入/推进**：一律在项目根目录执行 `python .edict/scripts/edict_tasks_api.py <子命令> ...`（脚本由 edict 插件复制到当前项目 `.edict/scripts/`，或来自 edict-opencode 仓库）。

---

## 状态与负责人

| 任务 state | 负责 agent（caller_agent） | 可执行操作 |
|------------|----------------------------|------------|
| Pending    | taizi                      | advance → Taizi |
| Taizi      | taizi                      | advance → Zhongshu |
| Zhongshu   | zhongshu                   | advance → Menxia；progress |
| Menxia     | menxia                     | review approve/reject |
| Assigned   | shangshu                   | advance → Doing；progress |
| Doing/Next | 由 task.org 对应六部        | advance → Review；progress |
| Review     | shangshu                   | advance → Done；progress |

**权限**：只有当前状态的负责 agent 才能对该任务执行 advance/review；progress 由当前负责该任务的 agent 汇报。跨 agent 调用需符合 `agent_config.json` 的 allowAgents（可用 `can_dispatch_to` 子命令校验）。

---

## 子命令与用法

在项目根目录执行（以下 `TASK_ID`、`CALLER` 等为占位，替换为实际值）。

### 1. create — 创建任务（下旨）

- **何时用**：用户或太子要新建一条旨意，state 初始为 Pending。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py create "任务标题" [--priority normal|high|critical|low]
  ```
- **输出**：打印新任务 ID（如 JJC-20260311-001），便于后续 advance/progress。

### 2. advance — 按状态机推进

- **何时用**：当前负责 agent 完成本阶段工作，将任务推进到下一状态（如太子分拣完 → Zhongshu，中书起草完 → Menxia）。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py advance TASK_ID CALLER_AGENT [--remark "说明"]
  ```
- **约束**：`CALLER_AGENT` 必须与任务当前 state 的负责人一致（见上表），否则脚本返回错误。
- **示例**：
  ```bash
  python .edict/scripts/edict_tasks_api.py advance JJC-20260311-001 taizi --remark "分拣完毕，转中书省"
  python .edict/scripts/edict_tasks_api.py advance JJC-20260311-001 zhongshu --remark "方案已提交门下审议"
  ```

### 3. review — 门下审议（准奏/封驳）

- **何时用**：任务处于 Menxia 时，由 menxia 执行审议；approve 则进入 Assigned，reject 则回到 Zhongshu。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py review TASK_ID menxia approve [--comment "准奏说明"]
  python .edict/scripts/edict_tasks_api.py review TASK_ID menxia reject [--comment "封驳原因与修改建议"]
  ```
- **约束**：仅 menxia 可执行；任务 state 必须为 Menxia。

### 4. flow — 仅追加流转记录（不改 state）

- **何时用**：需要记录部门间流转备注，但不改变任务状态时（例如补充说明）。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py flow TASK_ID "来自部门" "去向部门" "备注内容"
  ```
- **示例**：
  ```bash
  python .edict/scripts/edict_tasks_api.py flow JJC-20260311-001 "中书省" "门下省" "方案提交审议"
  ```

### 5. progress — 汇报进展（追加 progress_log）

- **何时用**：当前负责 agent 汇报工作进展、或更新待办快照（todos）。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py progress TASK_ID CALLER_AGENT "进展说明文本" [--todos "1.事项一|2.事项二|3.事项三"]
  ```
- **todos 格式**：用 `|` 分隔多项；可用 ✅/completed、🔄/in-progress 等表示状态，例如 `1.需求分析✅|2.方案设计🔄|3.待审议`。
- **示例**：
  ```bash
  python .edict/scripts/edict_tasks_api.py progress JJC-20260311-001 zhongshu "已完成需求分析，拟定三层方案" --todos "1.需求分析✅|2.方案设计✅|3.待门下审议"
  ```

### 6. stop — 叫停（可恢复）

- **何时用**：用户或协调方暂时叫停任务，state 变为 Blocked，_prev_state 保存原状态。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py stop TASK_ID CALLER_AGENT [--reason "叫停原因"]
  ```

### 7. resume — 恢复

- **何时用**：任务此前被 stop，现要恢复为 _prev_state。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py resume TASK_ID CALLER_AGENT [--reason "恢复说明"]
  ```

### 8. cancel — 取消（不可恢复）

- **何时用**：任务作废，state 变为 Cancelled。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py cancel TASK_ID CALLER_AGENT [--reason "取消原因"]
  ```

### 9. can_dispatch_to — 权限校验

- **何时用**：在决定是否派发/调用另一 agent 前，确认当前 agent 是否有权调用目标 agent。
- **命令**：
  ```bash
  python .edict/scripts/edict_tasks_api.py can_dispatch_to FROM_AGENT TO_AGENT
  ```
- **退出码**：0 表示允许，非 0 表示禁止；标准错误会打印 FORBIDDEN 说明。

---

## 执行流程建议

1. **先读任务**：`read_file` 查看 `.edict/edict-tasks.json`，确认目标任务的 `id`、`state`、`org`。
2. **确认身份**：确认你当前扮演的 agent（caller_agent）是否与该 state 的负责人一致；若需调用其他 agent，先运行 `can_dispatch_to 当前 目标` 校验。
3. **执行一次变更**：根据用户意图或本阶段完成情况，选择上述一个子命令，在项目根目录执行。
4. **根据输出**：脚本打印 OK 或状态变化；若报错，根据 stderr 修正（如 caller 不符、state 已终态等）。

---

## 禁止行为

- 不要用 `write_file` 或任何方式直接修改 `.edict/edict-tasks.json` 的 `state`、`flow_log`、`progress_log`、`_scheduler`。
- 不要跳过门下审议：中书完成方案后必须 advance 到 Menxia，由 menxia 执行 review，不能直接 advance 到 Assigned。
- 不要越权：advance/review 的 caller_agent 必须与当前状态负责人一致；跨 agent 派发需在 allowAgents 内。
