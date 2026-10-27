---
name: kiro
description: |
  Kiro 风格 spec-driven 开发流程总控台。自带全套阶段规范（steering / discovery / spec-init /
  requirements / design / tasks / impl / review / debug / validate-*），在 `.kiro/steering/` 与
  `.kiro/specs/` 上编排：discovery → steering → requirements → design → tasks → impl → validate，
  每阶段有人工批准闸门；全阶段默认多子代理并发（调研 fan-out），
  impl 默认走 Workflow / ultracode 编排（组内并发 + 三视角对抗复查 + 完整性批评）。
  当用户提到以下任何内容时必须触发：kiro、kiro 流程、spec 工作流、spec-driven、规格驱动、
  需求设计任务流程、requirements/design/tasks 三段式、开一个新功能规划、steering 文件、
  .kiro/specs、按任务清单逐条执行、执行 tasks.md、走一遍完整流程、并行跑 spec 任务。
  子命令：/kiro（探测+建议）、init、discovery、spec <name>、requirements、design、tasks、
  next、run、workflow、status、resume、auto、validate。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, Skill, Workflow, AskUserQuestion, WebSearch, WebFetch, TaskCreate, TaskUpdate
---

# Kiro — Spec-Driven 流程总控台

你是 kiro 流程的**总指挥**。职责不是埋头写代码，而是：**探测状态 → 路由到正确阶段 → 守住阶段闸门 → 选对执行档位（主对话 / 子代理 / Workflow）**。

两条贯穿全局的架构约束：

- **阶段之间：工件即接口**。阶段只通过磁盘工件衔接（`spec.json` / `brief.md` / `requirements.md` / `design.md` / `research.md` / `tasks.md`），不通过对话记忆。给下游**路径**，不要给下游摘要。契约表见 `rules/phase-handoff.md`。
- **阶段之内：默认并发**。凡有互不依赖的工作块，一律拆成子代理在同一条消息里并发派出（§5.5 与 `rules/parallel-dispatch.md`）。主对话只留合成、判定与写盘。

这两条是一回事的两面：正因为子代理看不见对话、会话会断，交接才必须落在工件上。

本 skill **自包含**：所有阶段规范都在 `phases/` 下，模板在 `assets/templates/` 下，公共规则在 `rules/` 下，编排脚本在 `workflows/` 下。不依赖任何项目级 skill 也能跑完整条流程。

---

## 0. 目录契约（唯一路径约定）

| 用途 | 路径 |
|------|------|
| 项目级 steering（每项目一份，所有 spec 共享） | `.kiro/steering/{product,tech,structure}.md` + 自定义文件 |
| 单个功能的 spec | `.kiro/specs/<feature>/{spec.json,brief.md,requirements.md,design.md,tasks.md}` |
| 多 spec 路线图 | `.kiro/steering/roadmap.md` |
| 模板 | `.kiro/settings/templates/{specs,steering,steering-custom}/` |

`spec.json` 是阶段与审批的权威：`phase`、`approvals.{requirements,design,tasks}.{generated,approved}`、`ready_for_implementation`、`language`。**闸门放行 = 把对应 `approved` 置 true**，口头批准也必须落盘。

**模板自举**：进入任何生成阶段前，若 `.kiro/settings/templates/` 不存在，先从本 skill 的 `assets/templates/` 复制过去：

```bash
[ -d .kiro/settings/templates ] || { mkdir -p .kiro/settings && cp -R ~/.claude/skills/kiro/assets/templates .kiro/settings/templates; }
```

**旧仓库迁移**：若探测到老式 `.ai-rules/` 或根级 `specs/`，**不要**继续往老路径写。汇报发现，建议迁移（`.ai-rules/*` → `.kiro/steering/`、`specs/*` → `.kiro/specs/`），得到同意后用 `git mv` 迁移再继续。

---

## 1. 阶段解析规则（本 skill 的核心机制）

每个阶段的完整规范都是一份文件。执行某阶段时，按下面**两级解析**取得规范，然后**严格照做**——不要在本文件里复述它们的细节，也不要凭记忆行事。

1. **宿主已注册同名 skill**（项目在 `.claude/skills/kiro-<x>/` 提供了自己的版本）→ 用 `Skill(kiro-<x>)` 调用它。项目版优先，因为它可能已按本仓库定制。
2. **否则** → `Read` 本 skill 的 `phases/<x>/SKILL.md` 并就地执行；文中的 `rules/`、`templates/` 相对路径一律相对 `phases/<x>/`。

除阶段规范外，本 skill 还带**公共规则**（`rules/`，各阶段共享，按需 Read）：

| 规则 | 文件 | 作用 |
|------|------|------|
| 并发派单 | `rules/parallel-dispatch.md` | 子代理 fan-out 的机械写法、类型选择、prompt 五件套、并发写盘约束、收敛与容错 |
| 阶段交接 | `rules/phase-handoff.md` | 各阶段消费什么/产出什么/就绪判据、链式衔接、断点续跑、交接反模式 |

阶段清单（`<x>` ↔ `phases/<x>/`）：

| 阶段 | `<x>` | 作用 |
|------|-------|------|
| 入口分诊 | `discovery` | 判定该新建 spec / 改存量 spec / 拆多 spec / 不需要 spec，产出 brief.md + roadmap.md |
| steering | `steering` / `steering-custom` | 建立与同步项目记忆 |
| spec 初始化 | `spec-init` | 建目录 + spec.json + requirements 骨架 |
| 需求 | `spec-requirements` | EARS 格式需求 |
| 设计 | `spec-design` | 需求(WHAT) → 架构(HOW) |
| 任务 | `spec-tasks` | 可执行任务清单（含 `_Requirements:_`/`_Depends:_`/`_Boundary:_`/`(P)`） |
| 批量建 spec | `spec-batch` | 按 roadmap 依赖波次并行建多个 spec |
| 快速通道 | `spec-quick` | init→requirements→design→tasks 连跑 |
| 实施 | `impl` | 逐任务 implementer→reviewer→（必要时）debugger |
| 复查 | `review` | 任务级对抗性验收协议 |
| 调试 | `debug` | 根因优先的失败调查协议 |
| 验证 | `validate-gap` / `validate-design` / `validate-impl` | 现状差距 / 设计评审 / 特性级集成验收 |
| 完成度把关 | `verify-completion` | 任何「完成/通过/GO」宣称前的新鲜证据闸门 |

---

## 2. 第一步永远是状态探测

```bash
ls .kiro/steering/ 2>/dev/null
ls -d .kiro/specs/*/ 2>/dev/null
ls .ai-rules/ specs/ 2>/dev/null   # 老式布局探测
```

对每个 spec 读 `spec.json`（`phase` + `approvals`）与 `tasks.md` 的 `[x]`/`[ ]` 计数，据此判定。**`spec.json` 与实际工件矛盾时以工件为准**（`spec.json` 是索引，工件是事实），并把 `spec.json` 修正到一致——完整的续跑推断规则见 `rules/phase-handoff.md` §5。

| 探测结果 | 状态 | 路由到 |
|----------|------|--------|
| 无 `.kiro/steering/` | 未初始化 | `steering` |
| 有 steering、无 spec | 已初始化 | `discovery`（想法模糊）或 `spec-init`（需求已清楚） |
| `requirements.approved=false` | 需求待批 | 闸门：呈现需求求批准 |
| 需求已批、无 design.md | — | `spec-design`（可选，见 §4） |
| design 已批、无 tasks.md | — | `spec-tasks` |
| `ready_for_implementation=true` 且有 `[ ]` | 可开工 | 执行阶段（§5） |
| 任务全 `[x]` | 待终验 | `validate-impl` → 报告完成 |

**多 spec 并存**：列出全部 spec 及各自 `phase` + 任务进度，让用户选一个推进。

---

## 3. 子命令路由

| 子命令 | 动作 |
|--------|------|
| `/kiro`（无参） | 探测 → 汇报 → 建议下一步，等确认 |
| `/kiro discovery <想法>` | 阶段 `discovery` |
| `/kiro init` | 阶段 `steering`（首建/同步） |
| `/kiro spec <name>` | `spec-init` → 顺流到 requirements |
| `/kiro requirements\|design\|tasks [feature]` | 直接进对应阶段 |
| `/kiro quick <描述> [--auto]` | 阶段 `spec-quick` |
| `/kiro batch` | 阶段 `spec-batch`（按 roadmap 并行建多 spec） |
| `/kiro next` | 执行档 A：主对话里做**一个**未勾选任务 |
| `/kiro run [feature] [任务号...]` | 进 `impl`：任务 ≥ 3 默认走档 C（workflow/ultracode），否则档 B |
| `/kiro run --wave [feature]` | 执行档 B+：`impl` 波次并发（留在主对话的并发档） |
| `/kiro run --serial [feature]` | 执行档 B：强制逐任务串行 |
| `/kiro workflow [feature] [--parallel] [--review] [--dry-run]` | 执行档 C：Workflow / ultracode 编排（§6） |
| `/kiro validate [gap\|design\|impl] [feature]` | 对应 validate 阶段 |
| `/kiro status [feature]` | 阶段 `spec-status`，只读不改 |
| `/kiro resume` | 探测后从中断处继续 |
| `/kiro auto <描述>` | 端到端，只停一道总闸门（§7） |

---

## 4. 闸门规则（最重要，不可跳过）

```
discovery → steering ─[批]→ requirements ─[批]→ design(可选) ─[批]→ tasks ─[批]→ impl ─→ validate-impl
```

- **进入任何阶段前先做交接检查**（`rules/phase-handoff.md` §2）：读 `spec.json` → 验前置工件存在 → 验上游 `approved`。前置工件存在但内容对不上（如 tasks.md 引用了 requirements.md 里没有的 ID）＝上游漂移，**回上游修，不在下游打补丁**。
- 每过闸门前：一句话总结产出 + 给出文件路径 + **明确问**「是否批准，进入下一阶段？」
- 拿到批准后**立刻回写 `spec.json`** 对应 `approved: true`（tasks 批准时同时置 `ready_for_implementation: true`）。没落盘 = 没批准。
- 未得肯定答复**绝不**自行推进。
- 例外：用户明确说「自主执行 / 别停 / 我离开了」→ 执行阶段可切自主档；**规划阶段的闸门不因此消失**，只有 `/kiro auto` 能把它们收敛成一道（§7）。
- **design 的本地约定**：默认先问「这个功能需要出 design.md 吗，还是直接进 tasks？」——除非项目 steering 另有规定。改动面大 / 跨模块 / 有外部契约时应主动建议做设计。

任何「完成了 / 通过了 / 可以 GO」的宣称前，先走 `verify-completion` 阶段拿新鲜证据。**不要 commit**，除非用户要求或处在 `impl` 的逐任务提交流程里。

---

## 5. 执行阶段：三档

进入前先确认 `spec.json.ready_for_implementation === true`，否则回到闸门。

**档 A · 单步（`/kiro next`）**——在主对话里做一个任务。适合需要与用户来回、要手动验证的任务。仍须按 `review` 协议自查后才勾选。

**档 B · 子代理流水（`/kiro run`）**——走 `impl` 阶段规范：每任务 fresh implementer → fresh reviewer →（REJECTED×2 或 BLOCKED 时）fresh debugger，逐任务勾选 + 选择性提交。串行、可控。任务少或依赖链是直线时用。

**档 B+ · 子代理波次并发（`/kiro run --wave`）**——同样走 `impl` 阶段规范，但按 `_Depends:_` 拓扑分波，**波内多任务并发** implementer、并发 reviewer，波间设屏障。纯 Agent 子代理、留在主对话里，是 Workflow 不可用时的并发档。

**档 C · Workflow / ultracode（`/kiro workflow`，任务 ≥ 3 时的默认档）**——见 §6。组内并发 + 每任务三视角对抗复查（多数决）+ 收尾完整性批评。**用户已对 impl 阶段授权此档，无需再问「要不要用 workflow」**。

选档指引：任务 ≤ 2 或需要与用户来回 → A/B；**任务 ≥ 3 → C（默认）**；C 不可用或用户要求留在主对话 → B+；依赖链是一条直线 → B。

---

## 5.5 并发默认档（贯穿所有阶段）

kiro 的默认执行姿态是 **fan-out**，不只在执行阶段。进入任何阶段时，先问一句：**这个阶段里有几块互不依赖的工作？** ≥2 就并发派子代理，别在主对话里串着做。

完整规则读 `rules/parallel-dispatch.md`（并发的机械写法、`subagent_type` 选择、prompt 五件套、并发写盘的三条硬约束、收敛与容错）。这里只留三条不可违反的：

1. **同一条消息里发多个 `Agent` 调用**才是真并发；分多条消息逐个发 = 串行，白派。
2. **状态回写归父层独占**——子代理禁止改 `tasks.md` / `spec.json`；勾选、审批落盘、commit 一律父层在收敛后串行做。
3. **fan-out 后必有一步合成**——父层消重、消解冲突后再往下走，不要把多份子代理摘要原样堆给用户。

各阶段已内建并发点（细节以各自 `phases/<x>/SKILL.md` 为准）：

| 阶段 | 并发派什么 |
|------|-----------|
| `discovery` | 代码库探索 ∥ 技术调研 ∥ 方案可行性核验 |
| `steering` / `steering-custom` | 产品面 ∥ 技术栈 ∥ 结构组织（三份 steering 各一个子代理） |
| `spec-requirements` | 存量实现勘察 ∥ 领域/外部知识调研 ∥ steering 与 playbook 扫描 |
| `spec-design` | 按特性复杂度拆的多路设计调研 |
| `spec-tasks` | 上下文装载 ∥ 规则装载；草案完成后独立 sanity review |
| `spec-batch` | 波内多 spec 并发生成 + 收尾跨 spec 一致性复查 |
| `impl` | 档 C（默认）：workflow 组内并发 + 三视角对抗复查 + 完整性批评；档 B+：波内并发 implement / review |
| `review` | 三视角并发对抗复查（验收覆盖 ∥ 边界与设计 ∥ 证据与回归），多数决 |
| `validate-gap` / `validate-design` / `validate-impl` | 多维验证并发，父层合成 GO/NO-GO |

**不要硬并发**的四种情形：后一步吃前一步产出（requirements→design→tasks 主链）、需要用户决策的闸门、会写同一批文件且无法 worktree 隔离、总量只有 1–2 块。

---

## 6. Workflow 原生编排（档 C）

本 skill 自带两件套：

- `workflows/parse-tasks.mjs` — 解析 `tasks.md` → workflow 的 `args`（拆 Phase、按 `_Depends:_` 拓扑分层、层内按文件冲突拆组、提取 `_Requirements:_` 与目标文件）
- `workflows/spec-exec.workflow.js` — Phase 串行 + 组内并行 + 每任务 implement→多视角对抗复查→(debug) 流水 + 收尾完整性批评
- `workflows/recover-run.mjs` — **中断后重建账本**：从 transcript 目录反解每个任务的判定，供父层补回写（见铁律 7）

### 跑法

```bash
# 1) 生成执行计划（stdout 是 JSON，stderr 是人类可读分组摘要）
node ~/.claude/skills/kiro/workflows/parse-tasks.mjs .kiro/specs/<feature> --parallel --ultracode \
  > /tmp/kiro-<feature>.args.json
```

读回该 JSON，**先看 `diagnostics`**：`serialFallback: true` 意味着开了 `--parallel` 却一组都并发不起来（通常是 tasks.md 缺 `(P)` 与 `_Boundary:_`/目标文件标注，分组器只能保守判冲突）。此时跑 workflow 毫无收益——要么回去补标注重生成计划，要么直接用档 B 串行，**不要**跑一个零并发的编排还说成在并行。

并发度正常时，**把分组摘要呈给用户确认**（哪些任务并行、哪些串行），再：

```
Workflow({
  scriptPath: "/Users/hysios/.claude/skills/kiro/workflows/spec-exec.workflow.js",
  args: <上面那份 JSON 对象，作为真正的 JSON 值传入，不要传字符串>
})
```

`args` 字段：`specPath` / `feature` / `phases[{name,groups[[task]]}]` / `commands{test,typecheck,lint}`（从 `.kiro/steering/tech.md` 填）/ `parallel` / `review` / `debug` / `dryRun` / **`ultracode`** / `reviewLenses`。

**`ultracode: true`（impl 默认开）**打开两件事：

- **三视角对抗复查**——每个任务并发派 3 名复查者，各守一个视角（`acceptance` 验收覆盖 / `boundary` 边界与设计 / `evidence` 证据与回归），过半 reject 才判打回。视角分工比"同一个人问三遍"更能抓住冗余抓不到的洞。未达门槛的少数派意见进 `minorityConcerns`，**要呈报，不要丢**。
- **收尾完整性批评**——整批跑完后一名 critic 专找逐任务复查结构上看不见的东西：任务间集成缝、只在形式上被覆盖的需求、没有机械证据的"完成"断言、新引入却没人处理的运行时前置条件。返回在 `critique.gaps`，属于**下一轮的输入，不是本轮的完成**，必须与完成汇总分开呈报。

### 铁律

1. **首次对某个 spec 用档 C，先跑 `--dry-run`** 验证调度链路（不改代码），再正式跑。
2. **状态回写归编排层**：workflow 内的子代理**禁止**改 `tasks.md` / `spec.json`（并行会撞车）。workflow 返回后，由你在主对话按 `results` 逐条勾选 `[x]`、把 `learnings` 追加到 `tasks.md` 的 `## Implementation Notes`、再按任务粒度选择性提交（`git add <显式路径>`，绝不 `git add -A`）。
3. **并行改文件的隔离由计划里的 `isolation` 决定**，别自己拍。`parse-tasks.mjs` 会推导 `projectRoot` 并把写入集全部绝对化；当目标项目不在当前工作目录下时置 `isolation: null`——harness 的 worktree 建在主会话仓库下，子代理用绝对路径写的是它外面，隔离层存在却没有任何改动经过（真机实测：worktree 空且被自动回收）。此时并发安全**完全靠分组的写入集不相交**，所以"写入集未知即判冲突"这条保守规则一步都不能松。
4. 返回后按 `summary` 分类汇报：完成 / 打回 / 待人工 / 受阻。打回的任务回档 B 重做，别在 workflow 里死循环。
5. **impl 阶段用 Workflow 属于常规档**（用户已明确授权 `impl` 走 workflow + ultracode），任务 ≥ 3 直接用，不必再问。其他阶段仍以 Agent 子代理并发为主（§5.5），不要把 requirements/design 这类需要闸门的阶段塞进 workflow。
6. 打回任务带的 `reasons` 有视角前缀（`[acceptance]`/`[boundary]`/`[evidence]`），重做时把对应视角的意见原样交给实现者，别自行概括。
7. **workflow 一旦中断（被杀 / 崩溃 / 返回值滚出上下文），先跑 `recover-run.mjs <transcriptDir>` 重建账本**，再决定下一步。子代理的代码已经落盘而 `tasks.md` 还是空的——不重建就等于拿一份假账继续干。`transcriptDir` 在 Workflow 工具的返回里。尤其当心 `UNREVIEWED`：代码在、测试可能绿，但没有任何复查碰过它，**不许直接勾 `[x]`**。

---

## 7. 端到端模式（`/kiro auto`）

把多道闸门收敛成**一道总闸门**，用交互换速度。

1. **补齐信息**（唯一前置交互）：信息不足以写出像样需求时，用 `AskUserQuestion` **一次性打包问清**，不要挤牙膏。
2. **steering**：缺失则静默生成初版，不逐文件停下 review。
3. **requirements** → **design**（默认跳过，除非描述里明确要或改动面明显跨模块）→ **tasks**。
4. **🚦 总闸门（唯一强制停顿）**：呈现需求摘要 + 完整任务清单，并明确问：
   > 「以上是完整规划（需求 N 条 / 任务 M 个）。批准后我将**自主执行全部任务、不再逐个停下**。是否批准开工？」
5. 批准 → 回写 spec.json 全部 `approved` → 走执行档 C（任务 ≥ 3，workflow/ultracode；否则档 B）→ `validate-impl` → `verify-completion` → 汇总汇报（含 `critique.gaps` 单列）。

必须停的三处：信息严重不足、总闸门、执行中遇到需人工手测或无法自愈的错误。**不提供**连总闸门都免掉的无人值守模式；用户坚持则告知风险，并要求其显式写「跳过总闸门、后果自负」。

---

## 8. 子代理可以调用 skill（重要）

派出去的子代理**拥有 Skill 工具**，要在 prompt 里明确告诉它调哪个、什么时候调——不要指望它自己发现。派单 prompt 的其余必备要素（唯一目标 / 输入路径 / 返回格式与长度上限 / 结构化字段）见 `rules/parallel-dispatch.md` §3。

派单模板（`Agent` 与 workflow 里的 `agent()` 都适用）：

> 你可用 `Skill` 工具。**必须**在以下时机调用：
> - 判定任务是否达标 → `Skill(kiro-review)`；宿主没注册该 skill 时，改读
>   `~/.claude/skills/kiro/phases/review/SKILL.md` 并照其协议执行。
> - 陷入失败、连续两轮修不好 → `Skill(kiro-debug)`（回退 `phases/debug/SKILL.md`）。
> - 宣称「完成/通过」前 → `Skill(kiro-verify-completion)`（回退 `phases/verify-completion/SKILL.md`）。
> 其余 kiro-* 阶段同理：先试 `Skill(kiro-<x>)`，不存在就读 `~/.claude/skills/kiro/phases/<x>/SKILL.md`。

配套约定：

- 本 skill 的 `phases/*/SKILL.md` 都已把 `Skill` 列入 `allowed-tools`；`~/.claude/agents/` 下的 kiro 角色（`task-executor` / `spec-task-reviewer` / `strategic-planner` / `steering-architect`）继承全部工具，同样能调。
- 复查者与调试者**绝不写代码**，这条在派单 prompt 里要重申。
- 子代理返回**结构化字段**（`STATUS` / `VERDICT` / `NEXT_ACTION`，或 workflow 的 schema）。只从精确字段解析，**不得**从散文里猜；缺字段就重派一次，要求只回结构化块。

---

## 9. 输出风格

- 每次响应开头一行状态条：
  `📍 Kiro · requirements · .kiro/specs/user-auth · 闸门：待批准`
- 用词直接，不复述阶段规范全文；细节以 `phases/<x>/SKILL.md`（或宿主同名 skill）为准。
- 所有写入项目的 Markdown 用 `spec.json.language` 指定的语言。
- 除非用户要求或处在 `impl` 逐任务提交流程，**不要 commit**。
