---
name: harness
description: |
  Minimal Harness Engineering loop for a code repository: three roles — Inspector finds issues, Worker fixes them, Reviewer verifies — coordinated through a shared TODO.md board, runnable once or on a schedule. Use when the user wants an agent to continuously inspect, fix and review a codebase, or says /harness, harness engineering, 启动 harness, AI 自治循环, 自动巡检修复, 定时改进代码.
trigger: /harness
compatibility: Claude Code
license: MIT
---

# /harness

**Harness Engineering 最小实践。** 用三条约束带（Inspector、Worker、Reviewer）将 AI 的创造力约束在正确的轨道上，通过 TODO.md 共享看板驱动持续改进。灵感来自 Harness Engineering 方法论：用轻量但确定性的流程框架，让 AI Agent 从"自由发挥"变成"可预测地交付高质量成果"。

## 触发条件

### 即时执行

- 用户输入 `/harness` — 完整循环（Inspector + Worker+Reviewer loop）
- 用户输入 `/harness inspect` — 只运行 Inspector
- 用户输入 `/harness work` — 只运行 Worker+Reviewer 一次
- 用户输入 `/harness loop` — 持续运行 Worker+Reviewer 直到没有可做的任务

用户可以在命令后附带自然语言指令，作为本轮循环的额外上下文。例如：
- `/harness 这次重点关注静默数据丢失问题`
- `/harness work 先修 P0 的环境变量检测`
- `/harness inspect 只校准当前骨架目标，不执行 Worker`

### 定时调度（cron）

使用 Claude Code 内置 CronCreate/CronDelete/CronList 工具，天然 session 隔离——不同 session 的 cron 互不影响。

| 命令 | 说明 |
|------|------|
| `/harness cron "*/30 * * * *"` | 每 30 分钟跑一次 full cycle |
| `/harness cron "*/30 * * * *" inspect` | 每 30 分钟只跑 Inspector |
| `/harness cron "0 */2 * * *" work` | 每 2 小时跑一次 Worker+Reviewer |
| `/harness cron "*/15 * * * *" loop` | 每 15 分钟持续消化任务 |
| `/harness cron list` | 查看当前 session 所有 harness cron |
| `/harness cron stop <job_id>` | 删除指定 cron |
| `/harness cron stop` | 删除当前 session 所有 harness cron（交互确认后逐个删除） |

**限制说明：**
- Cron job 仅在当前 Claude Code session 存活期间有效，关闭终端后失效
- Recurring job 7 天后自动过期
- 只在 REPL idle 时触发，不会打断正在进行的对话

## 三角色协议

### 核心原则：验证产出

**每个角色都必须验证自己的产出，不能只"做完了"就交差。**

- Inspector：产出任务后，检查任务描述是否足够清晰、hint 是否可操作
- Worker：修完代码后，按项目文档（`AGENTS.md` / `CLAUDE.md` / `TODO.md` / README 等）定义的验证命令执行相关检查；如果项目定义了端到端或真实流程验证，必须执行并记录结果
- Reviewer：审查时，确认 Worker 已执行与本次改动相关的验证命令；如果项目定义了端到端或真实流程验证且改动影响该路径，Worker 未验证时应拒绝或补验

端到端验证不是可选的。如果项目没有特定的 E2E/真实流程验证，或因外部依赖不可用而无法执行，必须显式记录原因。

```
Inspector (规划师)          — 决定方向，发现任务
  ↓ 写入 TODO.md
TODO.md (共享看板)
  ↓
Worker (修复者)             — 领任务，改代码
  [待领取] → [进行中] → [待审查]
  ↓
Reviewer (审查者)           — 审查代码，按项目规则决定是否提交或打回
  通过 → Done Log + （仅在允许时）git commit
  不通过 → [被拒绝] + 修复指引
  ↓
Worker 重新领取 [被拒绝]...
```

## 任务状态机

| 标记 | 含义 | 谁可以改 |
|------|------|----------|
| `[待领取]` | 未领取 | Inspector 可新增/修改，Worker 可领取 |
| `[进行中]` | Worker 正在做 | Worker 领取时设置，其他人不动 |
| `[待审查]` | Worker 完成 | Worker 完成时设置，Reviewer 审查 |
| `[被拒绝]` | Reviewer 打回 | Reviewer 拒绝时设置，Worker 可重新领取 |

## 执行步骤

### Step 1 — 解析用户指令

从用户输入中提取：
1. **是否为 cron 模式**: 输入中包含 `cron` 关键字
2. **模式**: cron / inspect / work / loop / full（默认）
3. **额外上下文**: 命令后面的自然语言文本（如果有）

如果是 cron 模式，跳到 Step 5。否则继续 Step 2。

将额外上下文保存到临时文件：
```bash
echo "用户额外指令: <用户输入的自然语言>" > /tmp/harness-context.txt
#   生命周期：full 模式下一轮 = inspector + worker-reviewer 都会读到；
#   worker-reviewer 在本轮实际投递给 claude 后的收尾才删除（无可做任务早退时保留）
```

如果没有额外上下文，创建空文件（子进程检测到空文件就不注入）。

### Step 2 — 确认项目环境

```bash
# 确认在项目根目录
test -f TODO.md || echo "NOT_HARNESS_PROJECT"
# 确认 skill 脚本存在（相对于 skill 目录）
test -f ../harness/inspector.sh && test -f ../harness/worker-reviewer.sh || echo "SCRIPTS_MISSING"
```

如果环境不对，停止并告知用户。

运行方式示例：
```bash
cd <project> && bash ~/.codex/skills/harness/inspector.sh
cd <project> && bash ~/.codex/skills/harness/worker-reviewer.sh --loop
HARNESS_PROJECT_DIR=/abs/path/to/project bash ~/.codex/skills/harness/inspector.sh
```

如果 `TODO.md` 不存在，创建一个最小模板：
```markdown
# Project Improvement Board

## Current Phase: 初始化

## Goals
- [ ] 待 Inspector 首次巡检后填写

## Done Log
```

### Step 3 — 根据模式执行

#### 模式: inspect
```bash
cd <项目目录> && bash <skill目录>/inspector.sh
```

#### 模式: work
```bash
cd <项目目录> && bash <skill目录>/worker-reviewer.sh
```

#### 模式: loop
```bash
cd <项目目录> && bash <skill目录>/worker-reviewer.sh --loop
```

#### 模式: full（默认）
```bash
# Phase 1: Inspector 巡检
cd <项目目录> && bash <skill目录>/inspector.sh

# Phase 2: Worker+Reviewer 循环
cd <项目目录> && bash <skill目录>/worker-reviewer.sh --loop
```

### Step 4 — 输出结果

完成后向用户汇报：

```
Harness 循环完成

Inspector:
  - 当前目标: ...
  - 架构判断: ...
  - 新增/调整任务: N 个

Worker+Reviewer:
  - 完成任务: N 个
  - 被拒绝任务: N 个
  - 剩余待领取: N 个

下一轮: 输入 /harness 继续
```

### Step 5 — cron 模式（使用内置 CronCreate/CronDelete/CronList）

#### 5.1 创建定时任务: `/harness cron "<cron表达式>" [mode]`

1. 解析 cron 表达式和可选的 mode（inspect / work / loop / full）
2. 根据 mode 构建 prompt 内容：
   - **full**: `"执行 harness full cycle。依次运行：  1. cd <项目路径> && bash <skill路径>/inspector.sh  2. bash <skill路径>/worker-reviewer.sh --loop  完成后汇报结果。"`
   - **inspect**: `"执行 harness inspect。运行 cd <项目路径> && bash <skill路径>/inspector.sh。完成后汇报结果。"`
   - **work**: `"执行 harness work。运行 cd <项目路径> && bash <skill路径>/worker-reviewer.sh。完成后汇报结果。"`
   - **loop**: `"执行 harness loop。运行 cd <项目路径> && bash <skill路径>/worker-reviewer.sh --loop。完成后汇报结果。"`
3. 调用 **CronCreate**，参数：
   - `cron`: 用户提供的 cron 表达式
   - `prompt`: 上面构建的 prompt
   - `recurring: true`
4. 向用户确认创建成功，返回 job_id

#### 5.2 查看定时任务: `/harness cron list`

1. 调用 **CronList** 获取当前 session 所有 cron job
2. 过滤出 prompt 中包含 "harness" 关键字的 job
3. 以表格形式展示：job_id | cron 表达式 | mode | 创建时间（如有）
4. 如果没有 harness cron，提示"当前 session 没有 harness 定时任务"

#### 5.3 删除定时任务: `/harness cron stop [job_id]`

- **有 job_id**: 调用 **CronDelete** 删除指定 job，确认删除成功
- **无 job_id**:
  1. 调用 CronList，过滤 harness 相关 job
  2. 向用户展示将要删除的所有 job
  3. 用户确认后，逐个调用 **CronDelete** 删除
  4. 汇报删除结果

## 子进程输入机制

每个子进程（Inspector / Worker / Reviewer）通过 `claude -p` 启动，输入由三部分组成：

1. **角色提示词** — `<skill目录>/prompts/inspector.md` 等
2. **项目文档** — 脚本自动拼接 AGENTS.md、CLAUDE.md、README、TODO.md 等文件内容
3. **用户额外上下文** — 从 `/tmp/harness-context.txt` 读取，注入到 prompt 末尾

三部分拼接后传给 `claude -p`，确保子进程既有项目全貌，又有用户本轮的具体意图。

默认情况下，脚本会把**调用脚本时的当前工作目录**（`pwd -P`）视为项目目录；如果需要从别处调用，可通过 `HARNESS_PROJECT_DIR=/abs/path/to/project` 显式覆盖。skill 安装目录只用于定位脚本和 prompts，不会被当成项目目录。

## 文件清单

| 文件 | 职责 |
|------|------|
| `prompts/inspector.md` | Inspector 角色提示词 |
| `prompts/worker.md` | Worker 角色提示词 |
| `prompts/reviewer.md` | Reviewer 角色提示词 |
| `inspector.sh` | Inspector 执行脚本 |
| `worker-reviewer.sh` | Worker+Reviewer 执行脚本 |
| `TODO.md` | 共享任务看板（项目根目录） |
