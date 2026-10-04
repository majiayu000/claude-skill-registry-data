---
name: repo-governance-bootstrap
version: 1.5.4
description: 一次性初始化 AI 协作项目的轻量工程治理骨架。新仓库 / 文档治理初始化时调用（也是 cto-orchestration 接入新项目的第一步）。One-shot governance bootstrap for a new repo.
---

# Repo Governance Bootstrap

## 何时调用

用户说出以下任一：
- "初始化文档治理 / 项目治理 / repo governance"
- "建立 ADR / roadmap / 文档骨架"
- "新仓库接入 AI 协作"
- "整理混乱的 docs 目录"

**跳过条件**：仓库已有 `docs/INDEX.md` 和 `docs/ACTIVE_CONTEXT.md` → 提演化方案、不重新初始化；绝不覆盖既有治理文件。

## FOR

- 新仓库初始化
- 引入 AI coding workflow
- 重构混乱 docs 结构
- 建立长期演化管理

## NOT FOR

- 重型流程管理 / Jira / RFC 工作流
- 复杂审批体系
- 外部 wiki 替代 Git
- 创建 `future_plan.md` / `ideas.md` / generic TODO dump

---

## 目标结构（最小）

```text
docs/
├── INDEX.md
├── ACTIVE_CONTEXT.md                 # 当前焦点 / hot context
├── NORTH_STAR.md                     # 可选：长期架构方向（伞仓或有明确长期方向的仓）
├── decisions/
│   └── ADR-0001-<slug>.md            # 仓库边界（ADR 编号固定 4 位）
├── modules/
│   └── <module>.md                   # 每个核心模块一个 flat 文件
└── roadmap/
    ├── README.md                     # status-bucket 索引（Active / Deferred / Obsolete）
    ├── active-roadmap.md             # 单文件，inline Status
    ├── deferred/
    │   └── README.md                 # deferred 索引（Items 表 + Entry Criteria + Promotion Rule）
    └── obsolete/
        └── README.md                 # obsolete 索引（仅索引，少用）

AGENTS.md                             # repo 治理规则（Claude Code ≥ 2.1.277 / Codex / omp 原生读）

scripts/engineering-gate.sh          # 后端 repo-owned fix/check/test 稳定接口（有代码 marker 时）
scripts/engineering-gate.conf        # 初始化时固化 profile + module root，不在每次运行时猜
.githooks/pre-commit                 # docs-check → engineering check → local test

ACCESS.local.md / .env                # gitignored — 元数据+名字+gotcha / 值(KEY=VALUE, 600)
```

### 治理系统观（对抗熵增：每个产物一个寿命层、一种更新纪律、一道防腐门）

> **定位分工**：本 skill = **结构层**（一次性生成骨架 + 写入纪律 + 机检门）；**循环层**的防腐
> （收口三同步 / 复盘 / 教训分层沉淀）由编排 skill 承担（`cto-orchestration` §5 + `orchestrator-core`
> 铁律九），其项目宪法拷贝即本 skill 生成的 AGENTS.md §6。腐烂是 workflow 问题——没有门校验，
> 任何结构都会漂；**快照类整篇重写、知识类逐条增改、决策类只增不删**，三种纪律别互串。

| 产物 | 寿命层 | 更新纪律 | 防腐机制 |
|---|---|---|---|
| `AGENTS.md` 宪法 | 慢·治理变量 | 逐行准入："删了这行 agent 会犯错吗？"不会 → 删；代码能推出的不写 | 尺寸门 <200 行（超长被降权）/ 32KiB（超限被 harness 静默截断） |
| ADR | 只增·决策史 | 不可变；翻案标 `superseded by`、不删；1-2 页对未来开发者说全句 | 4 态状态机；组件 ADR 带 Owner/Sunset/Review-by |
| module FOR/NOT FOR | 慢·边界 | 随触及它的代码**同一 commit** 更新 | 边界冲突显式上报（宪法 §3） |
| roadmap | 中·映射层 | 只映射外部任务 SoT、不复制状态（任务状态是高频信息，天然不属于常驻 docs；两套账本必烂一套） | 三桶 + 6 态词汇；沿用外部 ID |
| `ACTIVE_CONTEXT` | 快·快照 | 收口**整篇重写** ~60 行，快照非日志（当日志 append 会冻结腐烂） | freshness 门 + 收口三同步（宪法 §6） |
| `ACCESS.local` | 本机·含密 | 写时脱敏；gitignored 永不提交 | gitignore + 提交前 redaction sweep |
| `INDEX` | 慢·traffic cop | 只放链接——超过一行说明的内容 = 放错了地方 | 死链门 |
| `NORTH_STAR`（可选） | 最慢·方向 | 仅 maintainer 修订、semver 版本化（细则在模板注）；ADR 记历史、它记方向 | 原则带稳定 NS-ID 被评审 brief/门禁引用（没人检查的原则是注释）；与 accepted ADR 冲突不择边、升级 maintainer |
| `governance/` GOV 正典（可选·演化项） | 慢·活规则书 | 每域一份 `GOV-NNN-<slug>.md`、随实证**增订原篇**（日期戳节）。域路由按**更新契约**判，不按主题：会原地演进的现行可执行规则 → GOV；只被 supersede 的定格裁决与理由 → ADR；冻结证据快照 → audit；在飞协调物 → orchestration；混合体拆开各归其主、互挂指针 | `docs/governance/INDEX.md` 持域登记表 + 路由判据句 + 维护协议（新域先查表——已有域增订原篇、无域才立新号）；根 `docs/INDEX.md` 只挂一行链接（traffic-cop 契约不变）；goal/评审 brief 与门禁的 Read 指针在 GOV 持有该现行规则时指 GOV，否则指实际 owner |

细则（判据级；模板全文见 `references/templates.md`）：
- **Roadmap 三桶初始化即建**：active 单文件 inline `Status:`；deferred 一项一文件
  `<PREFIX>-DEFER-NNN-<slug>.md`（`<PREFIX>` 按项目取，勿硬编码他人前缀）；obsolete 仅索引。
  **不建 generic backlog**（`future_plan.md` / `ideas.md` / TODO dump）——未来工作进 deferred。
- **Module 默认单文件** `modules/<m>.md`，复杂到三份独立维护再拆目录；**ADR 编号 4 位零填充**全仓一致。
- **`ACCESS.local.md`（gitignored）三段式**（接入凭证 / 环境拓扑 / 验证配方）：committed 骨架答
  what/why，它答"怎么真正连上"；凭证 canonical home = 外部 vault、此文件是本机缓存；拓扑与凭证有意
  同进一份（内网拓扑本身也是敏感面）。高频两坑（**凭证间接**——存 X 读 Y 必记桥接，demo-day 401 头号
  根因；**活体 auth smoke 先跑并读失败模式**）已固化在模板注释。建文件即写进 `.gitignore`。
- **治理目录值得 local-only git 化**（尤其多子仓 umbrella）：无 remote 本地 git 管 `docs/`，换来变更
  历史 + 误删恢复 + 派工漂移审计（无版本时 agent 误删关键 docs 不可恢复）；加 remote 前先 secrets sweep。
- **GOV 正典不入最小骨架**：bootstrap 不建空 `docs/governance/`；第一条会被反复引用的
  判据/SOP 出现时 → 建 `docs/governance/INDEX.md` + `docs/governance/GOV-001-<slug>.md`
  （此前该判据散在时间目录与 archive 里长不出主线，就是该建的信号）。
- **伞仓（umbrella）场景三件套**：①`NORTH_STAR.md` 放伞仓 `docs/`，子仓 AGENTS.md 指向它（按 NS-ID
  引用）；②AGENTS.md 覆盖检查——每个含自有 `.git` 的一级子仓必须有根 AGENTS.md（Tier-1 活跃仓用
  `PROJECT_AGENT.md` 全量宪法，维护型仓用 templates.md 的 **minimal 变体** <60 行即达标），一行
  shell 即可做成门（one-liner 见模板注）；③nearest-wins：伞仓根管跨仓规则，子仓管自己内部，两层各 <200 行、不复读对方。

---

## 执行步骤

1. **询问用户**（如果未提供）：
   - 项目名 / 一句话定位
   - 核心 capability（≤3 个）
   - 核心 module 名（≤3 个）
   - 是否需要 AGENTS.md（推荐：是，串联 Codex + Claude）
   同时只读识别代码 marker 与 committed wrapper：`pyproject.toml`(Python)、`go.mod`(Go)、
   `mvnw` + `pom.xml`(Java/Maven)、`gradlew` + `build.gradle[.kts]`(Java/Gradle)、`Cargo.toml`(Rust)。
   单根 / 明确多根直接固化 profile；仅 Maven/Gradle 并存或 monorepo module root 不明确时再问。

2. **创建目录骨架**：`docs/decisions/`、`docs/modules/`、`docs/roadmap/deferred/`、`docs/roadmap/obsolete/`（roadmap 三桶一次建好）。

3. **生成 `docs/INDEX.md`**：含 Decisions / Modules / Roadmap / AI Context 四节 + Traceability 表（`| Capability | Component | ADR | Roadmap |`）。

4. **生成 `docs/decisions/ADR-0001-<slug>.md`**：用 `references/templates.md` 的 ADR 模板，主题是"仓库定位与边界"——记录这个仓库 FOR 什么 / NOT FOR 什么。Status: `proposed` 起步，由用户后续确认为 `accepted`。

5. **生成 `docs/modules/<m>.md`**：每个核心模块一个文件，含 FOR / NOT FOR / Components / Evolution 节。

6. **生成 roadmap**：`roadmap/README.md`（三桶索引）+ `roadmap/active-roadmap.md`（≥1 item，每项含 `Status` / `Capability` / `Components` / `ADR` / `Acceptance Criteria`）+ `roadmap/deferred/README.md`（空 Items 索引 + Entry Criteria + Promotion Rule）+ `roadmap/obsolete/README.md`（空索引）。三桶总索引与 obsolete 索引 freeform（一行表 + 链接即可，无模板）。

7. **生成 `docs/ACTIVE_CONTEXT.md`**：当前焦点 + 在跑/在等的 workstream 表 + standing constraints + recent decisions（最近 3–5 条）。按"治理系统观"的快照契约生成，头部带契约声明（模板见 `references/templates.md`）。

8. **生成 `AGENTS.md`**（守尺寸预算：<200 行——超长文件被 agent 静默降权/截断，见治理系统观表）：以 `references/PROJECT_AGENT.md`（中文成品宪法）为准落地，按其章节：Source of Truth 优先级 / 三档工作模式 / 模块边界（FOR / NOT FOR）/ Capability vs Component / 状态词汇 / 文档治理（已含**文档生命周期 anti-rot**：ACTIVE_CONTEXT 快照契约 + 收口归档仪式）/ Code Traceability / **Engineering Gate** / 完成标准。Engineering Gate 写入实际启用的 profile/module root、repo-owned 三命令与规范指针；不复制各语言类型条文。工具偏好若全局 agent 配置未覆盖项目特定项（如子仓库 toolchain）再补。**Redaction 边界**写明一条：secret/凭证只进 `ACCESS.local.md`（gitignored）与外部 vault，永不进 committed tree / traces / 日志 / 对外消息——避免 AGENTS.md 里 "creds never in repo tree" 与本机存明文凭证的口径自相矛盾。

9. **生成 `ACCESS.local.md` + 值文件孪生 `ACCESS.local.env` 并写进 `.gitignore`**：按 `references/templates.md` 的 ACCESS.local 模板建三段式骨架（值/元数据物理分离：`.md` 只留元数据+秘密名字+gotcha，值进纯 KEY=VALUE 的 `.env` 孪生并 `chmod 600`；注入 `set -a; source; set +a`——分离与注入的判据见 agent-backend-standard 附录 E），字段留空待用户填实；`.gitignore` 加 `ACCESS.local.*` 与 `.env*` 两行（带注释说明含 creds、永不提交）。**不写 `permissions.deny` 通配规则**：子串通配把「命令文本提到文件名」当「读取」、拦不住 python / `source` 读法，`Read(X.env)` deny 连带封 Edit/Write。值的防线 = gitignore + `chmod 600` + 进程注入；要「看有什么变量」只打印 KEY 与长度/哈希，不打印值。**绝不**把真实凭证写进 stub。

10. **配置 memory-discipline hook（默认项目级，直接建）**：把 `references/memory-discipline-hook.py` 接成
    PostToolUse hook——写 `memory/*.md`(非 MEMORY.md) 时确定性注入"事实细节→ACCESS.local.md/docs、只留指针"提醒。
    **默认写项目级配置**（`.claude/settings.json` 等，blast radius 小、随 bootstrap 直接建不必问）；只有要全局跨项目
    才问用户写 `~/.claude/`。**为什么需要 hook**：该纪律在 `cto-orchestration` §5，但 skill 文本随长对话
    salience 衰减，高频纪律须 hook 强制层兜底。三 agent wiring（CC/codex/omp 实测字段与坑）见 `references/hook-wiring.md`；**绝不**把真实 secret 写进 hook。

11. **建组合 project gate**：
    - 复制 `references/docs-check.sh` → `scripts/docs-check.sh`。四检 = AGENTS/CLAUDE 尺寸门 · docs
      相对链接死链（FAIL）· ACTIVE_CONTEXT 新鲜度与行数 · 幻影路径引用；`--heal` 显式自愈同名唯一死指针（其余跳过）。
    - 发现后端代码 marker 时，复制 `references/engineering-gate.sh` → `scripts/engineering-gate.sh`，
      按 `references/engineering-gate.conf.example` 生成 `scripts/engineering-gate.conf`，显式列出每个
      Python / Go / Java-Maven / Java-Gradle / Rust profile 与相对 module root。语言命令与失败契约的
      canonical = `agent-backend-standard` 附录 C §1–§6；本 skill 只负责初始化。
    - **同时 provision + pin profile 工具链，不能赌机器 PATH**：Python dev deps 进
      `pyproject.toml` + `uv.lock`，**包管理器自身也钉**（`[tool.uv] required-version = "==<ver>"`，附录 C §3；Node 仓 `package.json` `packageManager`）；Go 的 staticcheck/golangci-lint 进 repo-owned 版本清单 / bootstrap；
      Java 只选一个 committed wrapper，固定 Spotless/Checkstyle plugin 与 lifecycle wiring；Rust 用
      `rust-toolchain.toml` 固定 channel + rustfmt/clippy components。大仓可把模板的本地 `test` 分支改成
      AGENTS 明示的 deterministic focused suite；CI 仍跑附录 C 全量收口。
    - 复制 `references/pre-commit.sh` → `.githooks/pre-commit` 并赋可执行权限。顺序固定为
      `docs-check → engineering check → engineering test`；**hook 不跑 fix**，避免 staged index 仍含旧内容。
    - 复制 `references/pre-push.template` → `.githooks/pre-push`（可执行）、
      `references/PR_SELF_CHECK.skeleton.md` → `docs/PR_SELF_CHECK.md`（评审蒸馏层）。
      **清单与关卡从空开始**——条目只准来自真实评审 finding / 事故（铁律与下沉判据见
      `agent-backend-standard` 附录 F `selfcheck-gates.md`），可机检条目落 pre-push 关卡函数、
      每关带负探针登记 AGENTS.md；CI 以 `--range` 复跑同一脚本。基线分支非 main 时
      `git config hooks.baseline origin/<trunk>`。
    - `core.hooksPath` 为空时设 `.githooks`；已存在 hooksPath、`.git/hooks/pre-commit` 或 pre-commit
      framework 时合并调用，**绝不覆盖**。CI 已存在时同步调用同一 wrapper；本地 hook 可被
      `--no-verify` 绕过，不能冒充 required CI。
    - 当场分别跑 docs-check、engineering `fix/check/test`（fix 后 review diff + re-stage），再用 hermetic
      失败探针证明工具非零、gate/config 半安装都会阻断且输出 failed/fix/retry/AGENTS + canonical 指针。
      docs-only repo 只启用 docs-check（engineering script/config 均不存在）。

12. **完成时报告**：列出已建文件 + 用户下一步建议（填实 ADR-0001 内容 / 完成首个 module 的 FOR-NOT FOR / 把第一个 roadmap item 标 `active` / 在 `ACCESS.local.md` 填本机接入凭证与验证配方 / 若配了 hook 跑一次 memory 写入确认提醒生效 / 收口后重跑 `docs-check.sh` 养成节奏）。

---

## 状态词汇

两套词汇**独立、不可互换**：ADR 4 态（Nygard）/ Roadmap 6 态。完整定义见
`references/PROJECT_AGENT.md §5`（canonical——它随成品写进项目 AGENTS.md，必须自包含）。
生成 ADR / roadmap 时按那里取值，本 skill 不复述全文，只守一条易错点：**别把 ADR 的
`accepted` 安到 roadmap 上、别把 roadmap 的 `active/completed` 安到 ADR 上。**

---

## 模板（全部下沉，按步骤取用）

生成物模板（ADR / 组件引入 ADR lifecycle 变体 / 模块 / roadmap 条目 / deferred 条目 /
deferred 索引 / ACTIVE_CONTEXT / ACCESS.local / INDEX / **NORTH_STAR** / **AGENTS.md minimal
变体**）→ `references/templates.md`（顶部有目录）。
评审蒸馏门禁骨架另立两件：`references/pre-push.template` + `references/PR_SELF_CHECK.skeleton.md`
（步骤 11 取用；方法论 canonical = `agent-backend-standard` 附录 F）。
两条主干级判据：
- **引入重依赖/重组件的 ADR 用 lifecycle 变体**——增 `Owner` / `Sunset Criteria` / `Review-by` 三段，
  防引入后无人清理沦为死基础设施（更细的 lifecycle 规则见 `agent-backend-standard` 附录 A，本骨架只建槽）。
- **ACCESS.local 模板 stub 里绝不写真实 secret**（vault/缓存关系见治理系统观节）。


---

## Success criteria

完成后：
- `docs/INDEX.md` 单文件即可定位所有 source of truth
- 至少 1 个 ADR，记录仓库边界（Status 为 proposed 或 accepted）
- 至少 1 个 module 有 FOR / NOT FOR
- Active roadmap 至少 1 个 item
- `AGENTS.md` 生效，agent 进入新对话能识别上述结构
- 有后端代码 marker 时，repo-owned `fix/check/test`、组合 pre-commit 与 actionable failure 指针均已实跑

## After bootstrap

完成后告诉用户：

- 日常开发由 `AGENTS.md` 管理（Source of Truth 优先级 / 状态词汇 / 三档工作模式 / 等）
- 新决策走 ADR，新计划进 roadmap，过时计划标 `obsolete` / `rejected` 不删
- 后端日常改动先跑 `engineering-gate.sh fix`，提交门跑 non-mutating check + local test，CI 跑全量收口
