---
name: parallel-vibe
description: 当用户明确要求并行执行同一条 Vibe Coding 指令、让多个 Agent 或 Subagent 独立审查/设计/比较方案时使用。⚠️ 不适用：普通 shell 并发、单元测试并发、下载任务，或要求强隔离的敏感数据处理。
metadata:
  author: Bensz Conan
  keywords:
    - parallel-vibe
    - smart mode
    - code mode
    - parallel workspace
    - vibe coding
    - codex exec
    - claude -p
---

# parallel-vibe

## 目标

当用户明确要求"并行执行同一条 Vibe Coding 指令 / 多个独立 agent 或 subagent 同时审查、想方案、优化、对比多条路线 / 多线程独立尝试"时使用。默认使用智能模式：由宿主原生 subagent 独立分析并由主 agent 汇总；智能模式和代码模式必须使用同一套 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/{yyyy-mm-dd-hh-mm}/` 运行目录、`@main/plan.json`、thread `workspace/`、`RESULT.md` 与 `runner.log` 契约，区别只在底层执行机制；当用户要求脚本 runner、plan-file、resume、跨 CLI runner、退出码或无可用 subagent 时，切换到代码模式并调用 `scripts/parallel_vibe.py`。⚠️ 不适用：普通 shell 并发、单元测试并发、下载任务、要求强安全隔离或处理高度敏感数据。

## 流程

### 输入

输入为需要独立 Agent/thread 并行评估或执行的用户任务；可选输入包括线程数、智能/代码模式、`plan-file`、`project-id`/`resume`、runner 参数和源目录。普通 shell/测试并发、下载任务及高度敏感数据不使用本 Skill。

### 执行步骤

#### 模式选择

`parallel-vibe` 有两种模式：

- **智能模式（默认）**：使用宿主工具的原生 subagent / 独立上下文能力，让多个 thread 独立分析同一任务，主 agent 最后综合共识、分歧、推荐路线和验证步骤。
- **代码模式（保留）**：调用 `parallel-vibe/scripts/parallel_vibe.py`，由 CLI runner 在各 thread 的 `workspace/` 内执行，用于可追溯批处理、失败退出码和下游 skill 自动化。

目录管理是模式无关的。两种模式都使用同一套运行目录。默认 run id 为 `{yyyy-mm-dd-hh-mm}`，同一分钟重复运行时追加 `-02` 等后缀；代码模式显式传 `--project-id` 时可复用该值作为 run/project id：

- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/project.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/plan.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/plan.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/summary.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/workspace/`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/workspace/RESULT.md`（优先产物）
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/RESULT.md`（汇总用副本或兜底）
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/runner.log`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/prompt.txt`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/thread.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/done.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/exit_code.txt`

路由规则：

1. 用户只是要求多个 agent 独立想方案、审查、优化、评估风险或对比路线时，使用智能模式。
2. 用户要求固定目录、`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/`、`@main/plan.json`、`RESULT.md` 或 `runner.log` 时，仍可使用智能模式；这些是共享目录契约，不是代码模式专属触发条件。
3. 用户明确要求“代码模式”“脚本模式”“CLI runner”“plan-file”“resume”“dry-run”“退出码”、跨 `codex` / `claude` / `shell` runner，或下游 skill 需要脚本可复跑批处理时，使用代码模式。
4. 宿主没有可用 subagent 能力，或当前环境无法可靠启动独立上下文时，回退代码模式。
5. 涉及多个 agent 并行修改文件时，仍先按共享目录创建每个 thread 的 `workspace/`；如果宿主不能把 subagent 绑定到各自 `workspace/`，改用代码模式，或让智能模式只输出方案 / diff / patch 建议，由主 agent 单点落地。

`config.yaml` 中的 `defaults.mode`、`modes.smart`、`modes.code` 只表达模式口径，不要求宿主一定能以代码读取；真正执行仍以本节路由和用户意图为准。

#### 智能模式工作流

适用场景：方案探索、代码审查、风险评估、文档优化、研究假设打磨，以及“让多个独立 agent 给意见再汇总”的任务。

执行步骤：

1. 从用户消息提取任务、期望 thread 数和是否需要串行或并行；用户未指定时，按任务复杂度选择 3-5 个 thread。
2. 先创建共享运行目录。可直接按“模式选择”中的目录契约创建，也可运行代码模式脚本的 `--plan-only` 只初始化目录和 workspace，不启动 runner。
3. 为每个 thread 规划独立角色，例如保守方案、激进方案、测试边界、风险审查、用户体验审查，并写入 `@main/plan.json` / `@main/plan.md`。
4. 启动宿主原生 subagent 或等价独立上下文；每个 subagent 只读取用户任务和分配给自己的 thread prompt，不读取其他 thread 的结果。
5. 要求每个 subagent 把结论写入自己的 `<thread_id>/workspace/RESULT.md`；如果宿主无法让 subagent 直接落盘，主 agent 必须把其返回内容保存到 `<thread_id>/RESULT.md`，并在 `runner.log` 写入“由宿主 subagent 返回内容兜底落盘”的说明。
6. 每个 thread 完成后补齐 `done.json`、`exit_code.txt` 和 `runner.log`；智能模式没有真实 CLI 退出码时，成功用 `0`，失败或未完成用 `1`。
7. 主 agent 汇总共识、主要分歧、推荐路线和最小验证步骤，写入 `@main/summary.md`，再交付给用户。

智能模式与代码模式的目录管理必须一致。需要完整协议时，读取 `references/smart-mode-protocol.md`。

面向用户的输出至少包含：

- 运行模式：`智能模式`
- project 目录：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/`
- thread 数与串行/并行策略
- 每个 thread 的角色与一句话结论
- 综合结论：推荐路线、共识、主要分歧
- 验证步骤：可执行命令或人工检查点

重要边界：共享目录契约不等于强安全隔离。智能模式的独立性来自宿主 subagent / 独立上下文；代码模式的独立性来自 CLI runner + `cwd=workspace/`。实现型任务必须确保每个执行单元只写自己的 `workspace/`，否则让 subagent 输出方案或 patch 建议，由主 agent 选择并落地。

#### 代码模式工作流

适用场景：需要脚本 runner、`--plan-file`、`--resume`、`--dry-run`、失败日志、真实退出码、跨 `codex` / `claude` / `shell` runner，或被 `git-pr-review`、`research-idea`、`auto-draw-plot` 等下游 skill 作为稳定批处理接口调用。

输入：

- 必需：`prompt`（用户原始指令）或 `--plan-file`
- 可选：`n`（线程数，默认 5，范围 1-9；用户明确要求则以用户为准）
- 可选：每个 thread 的 `runner/model/prompt`（通过 `@main/plan.json` 或 `--plan-file` 自定义）
- 可选：`--project-id/--resume`（复用已有 run/project 目录）
- 可选：`--parallel/--max-parallel`（用户明确要求并行时使用）

输出：

- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/plan.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/summary.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/RESULT.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/<thread_id>/runner.log`

运行脚本（在用户当前目录或系统级 skill 目录中选择可用路径）：

```bash
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
```

```bash
python3 ~/.codex/skills/parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
# 或
python3 ~/.claude/skills/parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>"
```

常见参数：

```bash
# 指定线程数（默认 5）
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --n 5

# 复用已有 run/project
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --project-id <run_id> --resume

# 只生成计划与工作区，便于先审查 plan
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --plan-only

# 使用自定义 plan（JSON）
python3 parallel-vibe/scripts/parallel_vibe.py --plan-file /path/to/plan.json --src-dir . --out-dir .

# src_dir 存在 symlink 时的处理策略
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --symlink-policy skip

# 用户明确要求并行时才开启
python3 parallel-vibe/scripts/parallel_vibe.py --prompt "<用户指令原文>" --parallel --max-parallel 3
```

#### 代码模式软护栏

代码模式提供的是工程隔离，不是容器或沙箱级强安全隔离。当 runner 在某个 thread 的 `workspace/` 内工作时：

- 只允许读写当前 `workspace/` 及其子目录
- 禁止访问父目录（`..`）与任何绝对路径写入
- 禁止读取或写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>` 下的其他 thread 目录
- 产物必须落盘到当前 `workspace/`，便于追溯与汇总

默认拒绝 `--src-dir` 中的 symlink（可用 `--symlink-policy` 覆盖，但存在越界风险）；不要把包含敏感文件（如 `.env`、SSH key）的目录作为 `--src-dir`。

#### 自定义 thread（代码模式）

如需精确控制每个 thread 的 `runner/profile/model/prompt`，可直接编辑：

- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<run_id>/@main/plan.json`

然后用同一个 `--project-id` + `--resume` 续跑。注意：`--resume` 会复用 run/project 目录与 `@main/plan.json`，但每次运行仍会重建各 thread 的 `workspace/`。

如计划中使用 `runner.type=shell`，它会执行任意命令模板（仅对受信任的 plan 使用）；shell/工具本身可能读写用户全局缓存目录或访问绝对路径，因此不应理解为安全沙箱。

#### Runner 命令形态（代码模式）

代码模式假设“一条命令 = 一次独立执行”：

```bash
# OpenAI Codex CLI
codex -m <model_id> -c 'reasoning_effort="<effort>"' exec "你的指令内容"

# Claude CLI / Claude Code
claude --model <model_id> --effort <effort> -p "你的指令内容"
```

计划里 runner 参数约定：

- `runner.args`：全局参数，放在子命令前；适合 `codex -c ...`、`claude --effort ...`
- `runner.sub_args`：子命令参数，放在子命令后、prompt 前；适合 `codex exec --some-flag ...`

#### 清理方式

在触发目录执行：

```bash
rm -rf .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe
```

### 输出

输出包括共享运行目录、`@main/plan.json`/`plan.md`/`summary.md`、每个 thread 的 `workspace/RESULT.md`、`runner.log`、`done.json` 和 `exit_code.txt`；智能模式仍须提供线程角色、结论汇总、分歧与验证步骤，代码模式还须保留可复跑的退出码和 runner 记录。

### 输出管理

#### BenszAPI 任务工作区


### 校验

校验每个 thread 使用独立 workspace 且结果文件、退出码和日志齐全，`@main` 汇总覆盖全部有效结果；检查 plan/project ID、symlink 策略、线程数范围和路径边界符合配置/命令约束。

### 失败与恢复

thread 失败、runner 无法启动、结果缺失或 resume 状态不一致时，保留已有 workspace、日志和退出码，汇总中标记未完成并报告；可用同一 `project-id`/`--resume` 重跑，不能用空结果冒充成功。无法启动独立 subagent 时按路由切换代码模式。


## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
