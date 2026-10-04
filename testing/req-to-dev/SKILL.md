---
name: req-to-dev
description: 将需求/原则文档转成可执行开发落地包：计划(含W1-W6任务清单)、安全网(Safety Net)、契约(contracts)、验收(BDD)+单测(TDD)、任务索引与子代理(owner)分工；适用于“换agent也能立刻开干”的项目初始化与文档先行。
---

# Req-to-Dev（从需求到可执行开发）

## 概述

当用户给出需求/原则/计划类文档（或一个仓库）并要求“给我计划/落地/可换 agent 接手”，使用本技能将其转化为**可执行的工程落地包**：

- Safety Net（硬约束/门控/密钥/离线测试/发布清单/事故处置）
- Contracts（CLI/错误/审计等稳定契约）
- Execution Plan（W1-W6 任务级 checklist，TDD/BDD 驱动）
- Task Index（按模块索引任务）
- Subagents（并行开发分工与 owner 标注）
- Git 基础设施（如需要：init/分支/提交节奏）

核心目标：**不依赖单个 agent 的 context memory**，换人/换 agent 只要读文档就能继续工作。

## 触发条件（什么时候用）

满足任意一条就应触发：

- 用户提供需求文档并要求“按文档给计划/落地”。
- 用户强调 BDD/TDD、验收标准、可复现/审计、安全门控。
- 用户要求“即便切换 agent 也能立刻工作”。
- 用户要求建立/补齐项目管理文档与任务追踪。

## 工作流（需求 -> 计划 -> 文档落地 -> 可执行）

### Step 0：环境落地（先探索，后提问）

1. 定位并阅读用户提到的文档（支持文件名拼写差异）。
2. 探索仓库现状：是否已有 git、是否已有 docs 结构、是否已有测试入口。
3. 记录“缺口”：哪些信息无法从仓库得出（例如真实数据源消息 schema）。

输出：

- `DISCOVERED.md`（可选，不强制）：列出已发现的关键文件与缺口。

### Step 1：锁定不可破坏边界（Safety Net 先于实现）

建立并优先落地 Safety Net 文档集，至少覆盖：

- Hard Invariants：禁止自动签名/发送、越权禁止、panic 禁止、密钥禁止落盘
- Tiered Gate：高风险显式门控（confirm/summary/cooldown）
- BDD/TDD 策略：BDD scope（推荐 headless CLI），TDD 覆盖率阈值
- Secrets：环境变量注入、fixtures 脱敏、日志/审计/错误输出禁泄漏
- Error contract：稳定 `error_type` + JSON error envelope
- Release checklist + incident playbook

输出（建议目录结构，必要时用 `references/templates.md` 模板）：

- `SECURITY.md` + `SECURITY.zh-CN.md`
- `docs/safety-net/en/*` + `docs/safety-net/zh/*`

### Step 2：把“接口”定成可测试契约（Contracts）

将关键对外接口写成可断言的契约文档（实现必须满足，测试必须锁死）：

- CLI contract：命令语法即接口（Command Grammar = API），`--json`/`--stdin`/pipeability
- Errors contract：`error_type` 触发条件与输出格式
- Audit contract：JSONL 事件类型、字段、禁止字段、回放期望

输出：

- `docs/contracts/cli.md`
- `docs/contracts/errors.md`
- `docs/contracts/audit.md`

### Step 3：把计划压到“无需决策的任务级”（Execution Plan）

把高层计划（里程碑/路径）升级为任务级 checklist：

每条任务必须包含：

- Depends on
- Owner（subagent tag）
- Code（文件落点）
- Tests (TDD)（先写哪些测试，测试名固定）
- BDD（哪些场景必须绿）
- Acceptance（怎么运行验证）

输出：

- `docs/plan/W1-W6.md`（任务级）
- `docs/plan/TASK_INDEX.md`（模块索引）

### Step 4：并行开发就绪（Subagents + 归属）

当任务足够多且可按契约切分时，建立 subagent roster 与协作规则，并把 owner 写入计划：

- 新增 `AGENTS.md`：角色列表、边界、协调规则、分支命名建议
- 在 `docs/plan/W1-W6.md` 的每条任务写 `Owner:`
- 在 `docs/plan/TASK_INDEX.md` 每个模块写 Primary/Support

### Step 5：把“不确定的外部世界”固化成事实基线（Fixtures + Schema）

涉及网络数据源（WS/HTTP/RPC/LLM）时，必须建立 offline-first：

- fixtures：`tests/fixtures/.../*.jsonl`
- schema：从 fixtures 推导字段表，回写 `docs/data-sources/<source>.md`
- mock server：BDD 用本地 server 回放 fixtures

输出：

- `tests/fixtures/README.md`
- `docs/data-sources/<source>.md`

### Step 6：证据链（Runner + Verification Log）

建立单一验证入口与可审计证据：

- `scripts/test_runner.py`：按阶段运行（secret-scan -> unit -> integration -> bdd -> coverage）失败即停
- `TEST_VERIFICATION.md`：每次运行追加时间戳、命令、结果、覆盖率摘要

目的：换 agent 不需要“相信你跑过”，只看证据。

## Git 与提交策略（建议）

- 若目录不是 git 仓库：`git init -b main`。
- 分支：`codex/<topic>` 或 `codex/<agent>/<topic>`。
- 提交节奏：
  - 文档落地一笔 commit
  - 计划升级一笔 commit
  - subagent/owner 分工一笔 commit
  - 每次变更都保持工作区干净（便于切换 agent）。

## 完成定义（DoD：具备去记忆化开发能力）

满足以下条件即可认为“换 agent 可立即开干”：

- Safety Net + Contracts + Execution Plan + Task Index + ADR 均存在且互相链接。
- W1-W6 任务级 checklist 不留关键决策空洞（Owner/Tests/Acceptance 明确）。
- 外部数据源有 fixtures + schema + offline 回放策略。
- 有单一验证入口 + 证据链文档。

## 参考模板

需要快速生成标准目录/文档骨架时，读取：

- `references/templates.md`
