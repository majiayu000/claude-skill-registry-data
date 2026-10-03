---
name: agent-role-orchestrator
description: Route CEO-first multi-window work into owner-led role loops. Use for 总控/CEO、架构/CTO、内容主编、角色派发与复用、模型路由、来源窗口回调、role-windows 台账、skill 命中统计或 multi-window loop engineering。
---

# Agent Role Orchestrator

## Purpose

Turn a collaboration request into the smallest reliable role loop. Keep the main contract here; load only the reference file needed for the selected role or decision.

Default role tree:

```text
总控 / CEO
├─ 架构 / CTO
│  ├─ 开发
│  ├─ UI/PPT / UI/Frontend
│  ├─ 测试
│  ├─ QA
│  ├─ 安全
│  ├─ DBA
│  └─ 运维
├─ 内容主编
│  ├─ 公众号发布
│  ├─ 小红书
│  ├─ 视频
│  └─ UI/PPT 视觉资产协作
├─ 知识库
├─ 技能维护
└─ 文档/交付
```

Do not load every reference by default:

- role ownership: `references/role-cards.md`;
- current model tiers, executor tiers, and parallel policy: `references/model-routing.md`;
- implicit owner-to-executor planning details: `references/planning-contract.md`;
- script and skill routing: `references/tool-routing.md`;
- X MCP, public writing, Xiaohongshu, and content gates: `references/content-routing.md`.

## Fail-Closed Tool Layer Rule

Markdown owns principles and judgment. Scripts own enums, templates, ledgers, callback completeness, CodeGraph state, and metrics.

When `scripts/` is available:

- bootstrap/check project files with `ensure_project_role_files.py`;
- preflight plugins and generate non-trivial prompts with `prepare_role_window.py`;
- use `render_role_prompt.py` only as the lower-level generator after plugin readiness is established;
- validate prompts, callbacks, and ledgers with `validate_role_loop.py`;
- let `prepare_role_window.py` inject the real CodeGraph preflight, and use `check_codegraph.py` for standalone inspection instead of guessing;
- calculate hit rate with `aggregate_skill_hits.py` instead of chat memory.

If a required check fails, do not dispatch or close the loop. Fix it or record `待确认` with a reason. Scripts do not make architecture, product, or editorial judgment.

```bash
python skills/agent-role-orchestrator/scripts/ensure_project_role_files.py --project /path/to/project --write
python skills/agent-role-orchestrator/scripts/prepare_role_window.py --role 开发 --objective "修复筛选" --source-role 架构 --task-size small --profile auto --required-skill gstack
python skills/agent-role-orchestrator/scripts/validate_role_loop.py --project /path/to/project --prompt /path/to/prompt.md --callback /path/to/callback.md
python skills/agent-role-orchestrator/scripts/check_codegraph.py --project /path/to/project --require-ready
python skills/agent-role-orchestrator/scripts/aggregate_skill_hits.py /path/to/callbacks
```

## CEO-First Role Hierarchy Rule

One new requirement defaults to one `总控` / `CEO` window. `总控` owns outcome, scope, priority, budget, risk, and final go/no-go. It normally talks only to owner-layer roles: `架构` / `CTO`, `内容主编`, `知识库`, `技能维护`, and `文档/交付`.

Technical execution roles report to `架构` / `CTO`. Content execution roles report to `内容主编`. `总控` does not write implementation or acceptance scripts and does not directly manage execution details, except for the deliberate `tiny` or `small` routes below.

Reuse an existing role thread when its thread id is known. Unknown state is `待确认`; never invent a thread id.

## Loop Depth And Owner-Layer Routing Rule

Use the shallowest loop that can close safely:

| Depth | Route | Use |
| --- | --- | --- |
| `L0` | `用户 -> 执行角色` | Explicit, small, low-risk specialist task. |
| `L1` | `总控 -> 负责人层` | Route or owner judgment without downstream execution yet. |
| `L2` | `总控 -> 负责人 -> 执行 -> 负责人 -> 总控` | Normal multi-role work. |
| `L3` | L2 plus independent gates | Release, production, account, security, DB, critical PR, or high-risk public claims. |

负责人交互边界: `总控`只直接对接负责人层；负责人拆分、验收并压缩回流。Do not choose L2/L3 merely because multiple roles exist.

## CEO Task Dispatch Decision Rule

Before acting or dispatching, output `任务分发决策：` with size, path, and stop condition.

| Size | Default path | Boundary |
| --- | --- | --- |
| `tiny` | 总控自办 | Local, low-risk, verifiable. Stop on design, scripts, cross-file, production, account, or data risk. |
| `small` | 总控直派开发 | One short, narrow, low-risk code task; growth returns to CTO. |
| `medium` | 总控 -> 负责人层 | Owner judgment required. |
| `large` | 完整角色团队 | Owner splits execution and gates. |
| `critical` | L3 门禁团队 | Independent review required. |

Generate with `--task-size tiny|small|medium|large|critical`. Default unknown work to `medium`.

The generator derives one effective control set before routing: `large` is at least `L2`; `critical`, `risk=critical|extreme`, or an explicit `L3` becomes an `L3` gated loop, and an explicit `L3` also promotes ordinary risk to `critical`. Model, loop depth, Spark eligibility, and Token Budget Profile must all consume these effective values.

## Implicit Planning Contract Rule

Planning is an internal role contract, not a user-invoked mode or a new role. `render_role_prompt.py` adds the smallest role-specific contract automatically:

- `总控 / CEO` decides value, success criteria, non-goals, owner, budget, risk, and planning depth; it does not perform codebase recon or write technical steps.
- `架构 / CTO` performs scoped Recon and Vet, then writes the technical implementation spec; it does not implement by default.
- `开发负责人 / Dev Lead` compiles the confirmed spec into zero-context executor cards, then owns integration, re-verification, and commit.
- one-shot executors run drift checks, obey scope and STOP conditions, and never restart whole-repo planning.
- `QA` reviews the current change and direct impact surface as evidence, not as a planning or repair owner.

Task size controls contract depth, not audit breadth. `tiny` stays route-only; `small` uses a brief; `medium` uses an owner contract; `large` uses an implementation spec; `critical` adds independent gates and rollback/go-no-go fields. Whole-repo, multi-category, roadmap, or branch improvement audits require an explicit objective and must never fan out merely because a task is large.

Load `references/planning-contract.md` only when designing or auditing this handoff. The plan is an execution contract; verified delivery remains the product.

## Entry Guard And Registry Rule

For CEO, architecture, multi-role, dispatch, callback, or registry work:

1. Read this installed skill.
2. Read project `.codex/role-windows.md` when a project is known.
3. Run `ensure_project_role_files.py` when files may be missing; use `--write` only when writes are allowed.
4. Treat `.codex/role-windows.md` as the source of truth. Reuse known thread ids, record corrections, and never infer status from chat memory.

The ledger must track role, status, thread id, source window, responsibility, next step, and loop state. Update it after dispatch, callback, correction, blocking, and completion.

## Model Routing Rule

Load `references/model-routing.md` only when selecting, overriding, or auditing a model. `render_role_prompt.py` is the executable source for current defaults, executor tiers, the optional Spark lane, and escalation rules; do not copy that changing matrix into hand-written prompts.

Keep the ownership invariant: `开发负责人 / Dev Lead` owns decomposition, integration, correction, final validation, and commit. `开发执行 subagent` is an in-window one-shot worker for one narrow, independently verifiable task; it is not a durable role or ledger entry. Use `--delegation-policy auto|forbidden|optional|required`: task-specific no-subagent text and critical/high-risk work resolve to `forbidden`; an ordinary serial Dev Lead resolves to `optional`; an explicit executor tier or parallel profile resolves to `required`. Long duration changes checkpointing, not delegation eligibility. Parallel workers additionally require disjoint write scope, no shared evolving state, and independent validation. Record whether delegation happened, actual model/thinking, card/evidence handle, retries, and Dev Lead revalidation. User selection and actual availability override recommendations and must be recorded.

## Token Budget Profile Rule

Generate with `--profile auto`; override only with evidence:

- `compact`: tiny/small and ordinary medium work;
- `standard`: large, L2, architecture planning, or new-code setup;
- `full`: critical, L3, security/DB/ops risk, or irreversible work; add independent review, failure/rollback, unresolved-risk, and go/no-go fields.

`compact` must contain the closure contract but omit unrelated CTO, CodeGraph, content, and platform placeholders. Do not paste full chat history, large logs, or large source blocks into role prompts.

## Technical And Quality Rules

### Architecture

For a complex requirement, `架构` first compares credible technical routes and checks whether a current open-source solution is reusable. For a new local code project, pass `--project` and `--new-code-project` to `prepare_role_window.py`. Its default `auto` policy performs a read-only CLI freshness check and injects the result. Use `--codegraph-policy required` to fail closed; use `init` or `sync` only with explicit write authorization. Never silently install a CLI or mutate a project during `check`.

### Development

`开发负责人` and executors use first principles: restate invariants, inspect evidence, identify the smallest causal change, write or update tests where appropriate, and verify the integrated result. Repeated correction, unclear ownership, or scope growth returns to Dev Lead/CTO.

### QA

QA uses adversarial review: try to falsify readiness, inspect negative paths, boundary values, permissions, rollback, and regression risk. Ordinary QA uses Terra/high; critical release or production gates use Sol/xhigh. QA does not receive CTO-only planning placeholders.

### UI Preview Implementation Route Rule

`UI/PPT` loads `$ui-implementation-workflow`. Classify one page type, audit the existing system, use at most three active role-specific references, extract an implementation plan before code, reuse semantic tokens, build skeleton-first, and close with repaired screenshots at 1440/768/390. Marketing, brand, portfolio, and content pages may load its built-in `references/visual-direction.md`; `$design-taste-frontend` is only a compatibility adapter and must not start a second UI workflow. Start with no inherited aesthetic preference. Record explicit feedback on rendered work in `.codex/ui-visual-review-signals.md` as raw evidence, not an automatically active long-term preference. Keep the complete source inventory and a reference ledger, but do not load every site. When visual acceptance fails, replace only the failed layout, visual, component, or motion role within the switch-round budget. Operational dashboards/forms do not inherit marketing-page heroes or decorative motion.

When a preview image exists, `UI/PPT` must not `不要默认拿 CSS 硬干`. First compare CSS/components, image assets, Canvas/SVG, Three.js/WebGL, Lottie/video, proven libraries, or generated/manual assets. Record the selected route and visual verification evidence before development.

### Native Browser Routing Rule

For browser interaction, load `$browser-automation-router`. Prefer the in-app Browser for public/local visual work and the Chrome extension for an approved existing login/profile. Keep `$playwright` for deterministic CLI/CI evidence and platform scripts for explicit batch/export fallback. If the required native plugin is unavailable, fail closed to a named fallback instead of maintaining ad hoc JavaScript or profile-path logic.

## Content Routing Gates

Load `references/content-routing.md` only for public writing, platform research, or publishing work.

- `X MCP Content Research Source`: use [official X MCP docs](https://docs.x.com/tools/mcp) for authorized read-only trend, topic, benchmark-account, and public-discussion research. Writes need separate authorization.
- `Content Tone Gate`: 正式对外内容先过 `反老登味 / 反 AI 味内容闸门`, then use `$humanizer-zh` without changing facts.
- `Xiaohongshu Automation Publisher Gate`: load `$browser-automation-router`; use native Chrome for interactive logged-in work and `$xhs-automation-publisher` for deterministic Python/CDP fallback; preview/fill first, and require explicit confirmation for publish or interaction actions.

## Source-Window Callback Rule

The source window is the role/thread that assigned this task, not always `架构` or `总控`. If B delegates to C, B is C's source while B still reports its own state to A.

Completion is fail-closed. On completed, blocked, or decision-needed state, do both:

1. update `.codex/role-windows.md` and commit when project policy permits;
2. actively send a compressed callback to the source thread.

`仅完成第 1 项不算闭环`. If no sending tool exists, final output starts with `<codex_delegation>` or `压缩回调` for forwarding.

Required callback shape:

```text
压缩回调：
- 当前状态：
- 本轮变化：
- 证据链接/文件/命令：
- 需要决策：
- 下一回流对象：

技能命中回传：
- 已加载并使用：
- 来源窗口要求但未使用：
- 临时发现应补用：
- 误召/无效加载：
- 影响产出的 skill：
```

## Context Budget And Compact Handoff Rule

上下文预算 defaults to deltas and evidence handles. Before a long window approaches compaction, refresh the ledger and a compact handoff card containing objective, constraints, current state, decisions, artifacts/commits, validation, blockers, and next action. A new or resumed window reads artifacts instead of reconstructing the whole transcript.

## Skill Routing Measurement Rule

Owner layers declare candidate, required, optional, and skipped skills. Execution callbacks report actual use, omissions, misfires, and discovered should-use skills. `aggregate_skill_hits.py` reports self-declared execution data and returns not-evaluable when no required skill was declared; independent routing evaluation belongs in repository PR checks. Do not count from memory.

Route a reusable cross-role improvement to `技能维护`. Project state stays in the project ledger; reusable trigger, prompt, validation, or routing behavior belongs in the shared skill repository and should be proposed through a PR.

## Role Card Reference

Read `references/role-cards.md`, then only the thematic reference required by the task. Important defaults:

- 总控: outcome and routing, not technical implementation;
- Act as `架构` / `CTO`: technical owner and execution-team manager;
- 开发: durable Dev Lead plus optional one-shot executors;
- 内容主编: editorial owner and platform-role manager;
- QA: independent adversarial gate;
- 技能维护: reusable rules, registry, docs, prompt scripts, and hit-rate governance.

## Workflow

1. Classify the request and source window.
2. Read ledger; bootstrap files if allowed.
3. Choose task size and smallest loop depth.
4. Choose owner/executor role, model route, and Token Budget Profile.
5. Load only the relevant reference file and required downstream skills.
6. Run `prepare_role_window.py`; dispatch only after required role/skill plugins and the applicable CodeGraph policy pass. Use explicit `--delegation-policy`, `--executor-tier`, and parallel arguments when applicable.
7. Validate before dispatch.
8. On terminal state, update ledger, send callback, aggregate skill hits when useful, and route reusable improvements.

Generated prompts must include:

```text
模型建议：
- model：...
- thinking：...

任务分发决策：
技能命中回传：
```

## Concise Invocation Examples

```bash
# Durable Dev Lead, serial by default
python scripts/prepare_role_window.py --role 开发 --objective "实现订单修复" --source-role 架构 --profile auto

# New local project: read-only CodeGraph preflight injected into the prompt
python scripts/prepare_role_window.py --role 架构 --objective "设计适配方案" --project /path/to/project --new-code-project --codegraph-policy required

# Bounded one-shot Luna executor
python scripts/prepare_role_window.py --role 开发 --objective "实现独立适配器" --source-role 架构 --delegation-policy required --executor-tier bounded --profile compact

# Same bounded task using confirmed Spark preview quota
python scripts/prepare_role_window.py --role 开发 --objective "实现独立适配器" --source-role 架构 --executor-tier bounded --prefer-spark --spark-available --validation "pytest tests/test_adapter.py"

# Explicit three-worker parallel execution
python scripts/prepare_role_window.py --role 开发 --objective "实现三个独立适配器" --source-role 架构 --delegation-policy required --execution-profile parallel --worker-count 3 --disjoint-scope "每人一个目录" --independent-validation "每个目录独立测试"
```

## Quality Bar

- smallest safe loop, narrowest role, smallest model, and shortest prompt that preserve reliability;
- no invented thread ids, validation, publication state, or model tier;
- no direct CEO drift into implementation;
- no worker fanout without disjoint scope and independent validation;
- no terminal state without ledger update plus source-thread callback;
- no reusable optimization left only in chat.
