---
name: kiro-impl
description: Implement approved tasks using TDD with massively parallel subagent dispatch. Default is Workflow/ultracode orchestration (concurrent groups, 3-lens adversarial review, completeness critic); falls back to hand-driven waves, sequential, or manual mode.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep, Agent, Workflow, WebSearch, WebFetch, Skill
argument-hint: <feature-name> [task-numbers]
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-impl` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/impl/`。

# kiro-impl Skill

## Role
You operate in four modes:
- **Workflow mode / ultracode** (no task numbers, ≥3 pending tasks — **the default**): Hand the whole task graph to `workflows/spec-exec.workflow.js` via the Workflow tool. Groups run concurrently, each task flows implement → multi-lens adversarial review (majority vote) → debug independently, and a completeness critic sweeps the batch at the end. See "Workflow Mode" below.
- **Wave mode** (no task numbers, workflow unavailable or user wants to stay in the main loop): Partition pending tasks into dependency waves and run each wave's tasks as **concurrent** implementer subagents, then **concurrent** reviewers. Barrier between waves. Same per-task contract, hand-driven.
- **Sequential autonomous mode** (few tasks, or a strictly linear dependency chain): Dispatch a fresh subagent per task, one at a time, with independent review after each
- **Manual mode** (task numbers provided): Execute selected tasks directly in the main context

Mode selection is mechanical — see "Choose autonomous sub-mode" in Step 2. When the dependency graph is unknown or ambiguous, degrade toward sequential rather than guessing at independence.

## Core Mission
- **Success Criteria**:
  - All tests written before implementation code
  - Code passes all tests with no regressions
  - Tasks marked as completed in tasks.md
  - Implementation aligns with design and requirements
  - Independent reviewer approves each task before completion

## Execution Steps

### Step 1: Gather Context

If steering/spec context is already available from conversation, skip redundant file reads.
Otherwise, load all necessary context:
- `.kiro/specs/{feature}/spec.json`, `requirements.md`, `design.md`, `tasks.md`
- Core steering context: `product.md`, `tech.md`, `structure.md`
- Additional steering files only when directly relevant to the selected task's boundary, runtime prerequisites, integrations, domain rules, security/performance constraints, or team conventions that affect implementation or validation
- Relevant local agent skills or playbooks only when they clearly match the task's host environment or use case; read the specific artifact(s) you need, not entire directories

#### Parallel Research (concurrent subagent dispatch)

Follow `../../rules/parallel-dispatch.md`. Dispatch these independent research areas as **concurrent subagents in a single message** (`subagent_type: "Explore"` — read-only):

1. **Spec context loading**: spec.json, requirements.md, design.md, tasks.md → return the sections relevant to the pending tasks, plus any `## Implementation Notes`
2. **Steering, playbooks, & patterns**: Core steering, task-relevant extra steering, matching local agent skills/playbooks, and existing code patterns for the touched boundary
3. **Validation command discovery** (see Preflight): scripts/manifests, task runners, CI configs, e2e configs → return candidate `CANONICAL_TEST_COMMANDS` / `SCOPED_TEST_COMMAND` / `TYPECHECK_COMMAND` / `LINT_COMMAND` / `BUILD_COMMANDS` / `SMOKE_COMMANDS`

Each subagent returns a findings summary under ~120 lines, not raw file contents. Skip dispatch entirely when this context is already in the conversation, or when only one small task is pending — do it inline.

After all parallel research returns, synthesize the implementation brief in the parent context before starting.

#### Preflight

**Validate approvals**:
- Verify tasks are approved in spec.json (stop if not, see Safety & Fallback)

**Discover validation commands**:
- Inspect repository-local sources of truth in this order: project scripts/manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, app manifests), task runners (`Makefile`, `justfile`), CI/workflow files, existing e2e/integration configs, then `README*`
- Prefer commands already used by repo automation over ad hoc shell pipelines
- For `SMOKE_COMMANDS`, choose the lightest trustworthy runtime-liveness check for the app shape (for example: root URL load, Electron launch, CLI `--help`, service health endpoint, mobile simulator/e2e harness if one already exists)

**Split the validation set by scope — this is what keeps the run affordable**:

| Set | Content | Who runs it |
|---|---|---|
| `SCOPED_TEST_COMMAND` | The runner invoked against **specific test file paths** (e.g. `pnpm vitest run <paths>`, `pytest <paths>`, `go test ./pkg/x/...`). Record the *pattern*; the concrete paths come from each task's `_Boundary:_` | implementer only |
| `TYPECHECK_COMMAND` / `LINT_COMMAND` | Whole-project typecheck and lint | implementer + reviewer |
| `CANONICAL_TEST_COMMANDS` | The full suite, **including every test face the repo has** (root suite, sub-package suites, integration, e2e) — a single root command that silently skips sub-package suites is not canonical | reviewer (`evidence` lens) + parent only |
| `BUILD_COMMANDS` / `SMOKE_COMMANDS` | Build and runtime-liveness checks | parent only, at wave/feature level |

- If the repo has no way to run a subset of tests, say so explicitly and set `SCOPED_TEST_COMMAND` = canonical; do not invent a filter flag that the runner does not support.
- Keep the full set in the parent context and pass each subagent **only the set its role owns** (table above). Passing implementers the canonical command is what produces N redundant full-suite runs per wave — the redundancy is in the dispatch, not in the protocol.

**Establish repo baseline**:
- Run `git status --porcelain` and note any pre-existing uncommitted changes

### Step 2: Select Tasks & Determine Mode

**Parse arguments**:
- Extract feature name from first argument
- If task numbers provided (e.g., "1.1" or "1,2,3"): **manual mode**
- If no task numbers: autonomous — then pick **wave** or **sequential** by the rule below

**Build task queue**:
- Read tasks.md, identify actionable sub-tasks (X.Y numbering like 1.1, 2.3)
- Major tasks (1., 2.) are grouping headers, not execution units
- Skip tasks with `_Blocked:_` annotation
- For each selected task, check `_Depends:_` annotations -- verify referenced tasks are `[x]`
- If prerequisites incomplete, execute them first or warn the user
- Use `_Boundary:_` annotations to understand the task's component scope

**Choose autonomous sub-mode** (mechanical, no judgment call):
- **Workflow mode (ultracode)** — the default whenever ≥3 tasks are pending. This is standing user authorization for this phase; do not stop to ask whether to use a workflow.
- **Wave mode** — ≥3 pending tasks but the Workflow tool is unavailable, a prior workflow run failed, or the user asked to stay in the main loop
- **Sequential mode** — ≤2 pending tasks, or a strictly linear `_Depends:_` chain, or `_Depends:_`/`_Boundary:_` annotations are missing across the board (never assume independence from silence)

### Step 3: Execute Implementation

#### Sequential Autonomous Mode (subagent dispatch)

This section defines the per-task contract. **Wave mode reuses all of it** and only changes the scheduling — read this first, then "Wave Mode" below.

**Iteration discipline**: One sub-task (e.g., 1.1) per subagent — never batch multiple sub-tasks into a single dispatch. In sequential mode iterations also run one at a time: dispatch implementer → review → commit → re-read tasks.md → next. (Wave mode runs several such single-task subagents concurrently; the one-task-per-subagent rule still holds.)

**Context management**: At the start of each iteration, re-read `tasks.md` to determine the next actionable sub-task. Do NOT rely on accumulated memory of previous iterations. After completing each iteration, retain only a one-line summary (e.g., "1.1: READY_FOR_REVIEW, 3 files changed") and discard the full status report and reviewer details.

For each task (one at a time):

**a) Dispatch implementer**:
- Read `templates/implementer-prompt.md` from this skill's directory
- Construct a prompt by combining the template with task-specific context:
  - Task description and boundary scope
  - Paths to spec files: requirements.md, design.md, tasks.md
  - Exact requirement and design section numbers this task must satisfy (using source numbering, NOT invented `REQ-*` aliases)
  - Task-relevant steering context, plus **only the implementer-scoped commands**: `SCOPED_TEST_COMMAND` resolved against this task's `_Boundary:_` test paths, `TYPECHECK_COMMAND`, `LINT_COMMAND`. Do **not** hand over `CANONICAL_TEST_COMMANDS`, `BUILD_COMMANDS`, or `SMOKE_COMMANDS` — the reviewer owns the regression verdict, so an implementer's full-suite run buys no evidence and costs a full suite
  - Whether the task is behavioral (Feature Flag Protocol) or non-behavioral
  - **Previous learnings**: Include any `## Implementation Notes` entries from tasks.md that are relevant to this task's boundary or dependencies (e.g., "better-sqlite3 requires separate rebuild for Electron"). This prevents the same mistakes from recurring.
- The implementer subagent will read the spec files and build its own Task Brief (acceptance criteria, completion definition, design constraints, verification method) before implementation
- Dispatch via **Agent tool** as a fresh subagent

**b) Handle implementer status**:
- Parse implementer status only from the exact `## Status Report` block and `- STATUS:` field.
- If `STATUS` is missing, ambiguous, or replaced with prose, re-dispatch the implementer once requesting the exact structured status block only. Do NOT proceed to review without a parseable `READY_FOR_REVIEW | BLOCKED | NEEDS_CONTEXT` value.
- **READY_FOR_REVIEW** → proceed to review
- **BLOCKED** → dispatch debug subagent (see section below); do NOT immediately skip
- **NEEDS_CONTEXT** → re-dispatch once with the requested additional context; if still unresolved → dispatch debug subagent

**c) Dispatch reviewer**:
- Read `templates/reviewer-prompt.md` from this skill's directory
- Construct a review prompt with:
  - The task description and relevant spec section numbers
  - Paths to spec files (requirements.md, design.md) so the reviewer can read them directly
  - The implementer's status report (for reference only — reviewer must verify independently)
  - `CANONICAL_TEST_COMMANDS`, `TYPECHECK_COMMAND`, `LINT_COMMAND` — the reviewer is the **only** per-task actor that runs the full suite, and that run is the regression verdict
- The reviewer must apply the `kiro-review` protocol to this task-local review.
- Preserve the existing task-specific context: task text, spec refs, `_Boundary:_` scope, validation commands, implementer report, and the actual `git diff` as the primary source of truth.
- The reviewer subagent will run `git diff` itself to read the actual code changes and verify against the spec
- Dispatch via **Agent tool** as a fresh subagent

**d) Handle reviewer verdict**:
- Parse reviewer verdict only from the exact `## Review Verdict` block and `- VERDICT:` field.
- If `VERDICT` is missing, ambiguous, or replaced with prose, re-dispatch the reviewer once requesting the exact structured verdict only. Do NOT mark the task complete, commit, or continue to the next task without a parseable `APPROVED | REJECTED` value.
- **APPROVED** → before marking the task `[x]` or making any success claim, apply `kiro-verify-completion` using fresh evidence from the current code state; then mark task `[x]` in tasks.md and perform selective git commit
- **REJECTED (round 1-2)** → re-dispatch implementer with review feedback
- **REJECTED (round 3)** → dispatch debug subagent (see section below)

**e) Commit** (parent-only, selective staging):
- Stage only the files actually changed for this task, plus tasks.md
- **NEVER** use `git add -A` or `git add .`
- Use `git add <file1> <file2> ...` with explicit file paths
- Commit message format: `feat(<feature-name>): <task description>`

**f) Record learnings**:
- If this task revealed cross-cutting insights, append a one-line note to the `## Implementation Notes` section at the bottom of tasks.md

**g) Debug subagent** (triggered by BLOCKED, NEEDS_CONTEXT unresolved, or REJECTED after 2 remediation rounds):

The debug subagent runs in a **fresh context** — it receives only the error information, not the failed implementation history. This avoids the context pollution that causes infinite retry loops.

- Read `templates/debugger-prompt.md` from this skill's directory
- Construct a debug prompt with:
  - The error description / blocker reason / reviewer rejection findings
  - `git diff` of the current uncommitted changes
  - The task description and relevant spec section numbers
  - Paths to spec files so the debugger can read them
- The debugger must apply the `kiro-debug` protocol to this failure investigation.
- Preserve rich failure context: error output, reviewer findings, current `git diff`, task/spec refs, and any relevant Implementation Notes.
- When available, the debugger should inspect runtime/config state and use web or official documentation research to validate root-cause hypotheses before proposing a fix plan.
- Dispatch via **Agent tool** as a fresh subagent

**Handle debug report**:
- Parse `NEXT_ACTION` from the debug report's exact structured field.
- If `NEXT_ACTION: STOP_FOR_HUMAN` → append `_Blocked: <ROOT_CAUSE>_` to tasks.md, stop the feature run, and report that human review is required before continuing
- If `NEXT_ACTION: BLOCK_TASK` → append `_Blocked: <ROOT_CAUSE>_` to tasks.md, skip to next task
- If `NEXT_ACTION: RETRY_TASK` → preserve the current worktree; do NOT reset or discard unrelated changes. Spawn a **new** implementer subagent with the debug report's `FIX_PLAN`, `NOTES`, and the current `git diff`, and require it to repair the task with explicit edits only
  - If the new implementer succeeds (READY_FOR_REVIEW → reviewer APPROVED) → normal flow
  - If the new implementer also fails → repeat debug cycle (max 2 debug rounds total). After 2 failed debug rounds → append `_Blocked: debug attempted twice, still failing — <ROOT_CAUSE>_` to tasks.md, skip
- **Max 2 debug rounds per task**. Each round: fresh debug subagent → fresh implementer. If still failing after 2 rounds, the task is blocked.
- Record debug findings in `## Implementation Notes` (this helps subsequent tasks avoid the same issue)

**Completion check**: If all remaining tasks are BLOCKED, stop and report blocked tasks with reasons to the user.

#### Workflow Mode / ultracode (default for ≥3 tasks)

The per-task contract above still governs — the workflow script encodes it. What the workflow adds is scale: many tasks in flight at once, each independently reviewed by **three concurrent adversarial lenses** instead of one reviewer, plus a completeness critic that catches what per-task review structurally cannot see.

**Step 1 — build the execution plan**:

```bash
node ~/.claude/skills/kiro/workflows/parse-tasks.mjs .kiro/specs/<feature> --parallel --ultracode \
  > /tmp/kiro-<feature>.args.json
```

`--ultracode` sets `ultracode: true` (risk-escalated multi-lens review plus the closing completeness critic) and implies `--review`.

**Review strength is escalated per task, not applied uniformly.** Every task gets one reviewer running the full 12-check `kiro-review` protocol; a task escalates to the 3-lens majority vote (`acceptance` / `boundary` / `evidence`) only when a mechanical trigger fires:

| Trigger | Why it means "worth 3× the review budget" |
|---|---|
| `impl.concerns` non-empty | The implementer itself flagged something for scrutiny |
| `impl.needs_manual_verify` | No mechanical verification exists to fall back on |
| `task.files.length >= 3` | Wide write set — more surface for boundary and coupling errors |
| `task.reqs.length >= 3` | One task carrying several requirements; acceptance coverage is the likely gap |
| boundary pre-check hit | Changed files fall outside the declared write set (see below) |

Tune with `riskThresholds: { files, reqs }` in the plan. The reason this is escalation rather than a flat 3 lenses is **concurrency budget**, not a quality trade-off: the host runs at most `min(16, cores − 2)` subagents at once (8 on a 10-core machine), so a width-3 group × 3 lenses = 9 reviewers crosses that ceiling and the ninth agent takes a whole extra batch on its own, doubling the review phase's wall clock while 7 slots idle. Voting is over the reviewers actually dispatched — 1 reviewer means 1 reject verdict rejects, so a downgraded review is not a weaker gate per vote.

Note that **2 lenses is the worst setting** under `floor(n/2)+1` (it needs a unanimous reject, i.e. looser than 3), which is why escalation switches between 1 and 3 and never lands on 2.

The **boundary pre-check** runs in the script, with no agent at all: it diffs `impl.files_changed` against the task's declared write set. A hit forces escalation and is handed to the reviewer as located evidence, saving it the round-trip of comparing paths itself. It never rejects on its own — a changed file outside the boundary is just as often `tasks.md` under-listing a test file that design required, and that is an annotation bug, not an implementer error.

The plan carries two fields that exist because **workflow subagents inherit the main session's cwd, which is not necessarily the project the spec belongs to**:

- `projectRoot` — derived from the spec path (`<root>/.kiro/specs/<feature>` → up three). Injected into every subagent prompt, and every write-set path in the plan is already absolutized against it. Do **not** hand-absolutize paths before dispatching; that was a workaround for the parser not knowing the root, and it is no longer needed.
- `isolation` — `'worktree'` when the project is inside the current working directory, **`null` when it is not**. The harness creates worktrees under the *main session repo*; when the target project lives elsewhere, subagents writing absolute paths land outside that worktree, so the isolation layer is present but nothing passes through it. Verified on a real run: the worktree came back empty and was auto-reclaimed. A protection that looks real but isn't is worse than none, so it is switched off explicitly and concurrency safety rests entirely on the grouping's disjoint write sets — which is exactly why unknown write sets must keep being treated as collisions.

stdout is the JSON plan; stderr is a human-readable grouping summary. Read the JSON back, then fill in:
- `commands.{scopedTest,typecheck,lint,test}` from `.kiro/steering/tech.md` (or from the validation-command discovery in Step 1). The plan does **not** carry these — a workflow dispatched without them leaves every subagent guessing at how to verify its own work.
  - `commands.scopedTest` — the file-scoped runner pattern; the workflow substitutes each task's own target files into it. **Implementers get only this one.**
  - `commands.test` — the canonical full suite. **Only the `evidence` lens reviewer gets it.** If you put the canonical command in `scopedTest`, every concurrent implementer runs the full suite and the wave's cost multiplies by its width.
- `debug: true` is already the script default — root-cause investigation on rejection or blockage

**Step 1.5 — check `diagnostics` before dispatching** (this is where the parallelism actually gets decided):

```
diagnostics: { totalTasks, groups, concurrentGroups, maxGroupWidth,
               tasksWithoutParallelEvidence[], serialFallback }
```

The grouping algorithm is deliberately conservative: a task with no `(P)` marker **and** no backtick-quoted target paths in its body is treated as colliding with everything. So an all-single-task plan usually means **tasks.md is under-annotated, not that the work is genuinely serial**.

**Group width is the single largest wall-clock lever.** Groups run one after another, so total time ≈ group count × (implement + review). The scheduler treats a task with no readable write set as colliding with everything, so under-annotated `tasks.md` produces narrow groups and a long serial chain — width 3 on a 28-task spec is ~10 groups where width 8 would be ~4. Aim for width ≈ the host's concurrency budget (`min(16, cores − 2)`); below that is idle capacity, and the fix is honest `_Boundary:_` paths in `tasks.md`, never a looser scheduler.

- `serialFallback: true` → **stop and say so.** Running a workflow here buys nothing over sequential mode — it's the same one-at-a-time execution with orchestration overhead on top. Two honest options: (a) go back and add `(P)` + `_Boundary:_` / target paths to the tasks that really are independent, then regenerate the plan; (b) accept serial and use sequential mode. Never silently dispatch a zero-concurrency workflow and describe it as running in parallel.
- `concurrentGroups` low relative to `totalTasks` → same conversation, smaller stakes. Report the achieved width honestly.
- Never "fix" this by relaxing the grouping rules or hand-editing tasks into the same group. Conservative grouping is what prevents two subagents writing one file; the fix is better annotations, not a looser scheduler.

**Step 2 — show the grouping summary to the user, then dispatch**:

```
Workflow({
  scriptPath: "/Users/hysios/.claude/skills/kiro/workflows/spec-exec.workflow.js",
  args: <the plan object as a real JSON value, never a stringified one>
})
```

Present which tasks run concurrently and which are serialized **before** dispatching — a bad grouping is cheap to fix now and expensive to fix after 12 subagents have written files.

**Step 3 — converge in the parent after the workflow returns** (the workflow deliberately writes no state):
- `results[].status === 'ok'` → apply `kiro-verify-completion`, mark `[x]`, selective commit per task
- `rejected` → these carry the majority-vote `reasons` with lens tags; re-run them in **sequential** mode, not another workflow
- `blocked` / `stop-for-human` → append `_Blocked: <reason>_` to tasks.md, report
- `manual` → report the verification method the implementer specified; do not mark complete
- `results[].learnings` → append to `## Implementation Notes`
- `verdict.minorityConcerns` → a lens that rejected without reaching the threshold. Not blocking, but surface it — a single dissenting lens is right often enough that silently dropping it defeats the point of multi-lens review
- `critique.gaps` → **report separately from the completion summary**. These are cross-task seams (missing integration, unverified claims, uncovered requirements, new runtime prerequisites). They are next-round input, not this round's failures. If `overall === 'gaps-found'`, do not make a feature-level success claim before either resolving them or explicitly handing them to the user.

**Rules that do not bend**:
1. **First workflow run against a given spec: `--dry-run` first**. It exercises the dispatch chain without touching code. One cheap round-trip beats debugging a 12-agent run.
2. **State writes belong to the parent, always.** The workflow's subagents are forbidden from touching `tasks.md` / `spec.json` / git — that prohibition is what makes their concurrency safe.
3. **Concurrent file writes require worktree isolation** — the script already sets `isolation:'worktree'` when `parallel && !dryRun`.
4. **Rejected tasks leave the workflow.** Remediate them sequentially with the bounded rounds below. Never loop a failing task inside the workflow.
5. **Run the canonical test suite once over the merged result** before the feature-level claim. Per-task green does not prove the batch is green.

Degrade to wave or sequential mode when the workflow errors out, when the grouping keeps colliding, or when two consecutive groups come back rejected — and say so explicitly rather than silently retrying.

**Step 4 — if the run is interrupted, recover the ledger before anything else.**

Parent-only state writes make concurrency safe, but they create one failure mode: **an interrupted workflow has already written code to disk while `tasks.md` still says nothing happened.** Killed run, crash, or a return value that scrolled out of context — same result: the disk and the ledger disagree, and every later decision is made against a false picture.

Never assume an interrupted run did nothing. Recover:

```bash
node ~/.claude/skills/kiro/workflows/recover-run.mjs <transcriptDir>   # add --json to parse
```

`<transcriptDir>` is printed in the Workflow tool result (`.../subagents/workflows/wf_xxx`). The tool reads `journal.jsonl` plus each `agent-<id>.jsonl` and rebuilds per-task verdicts. It exists because **`journal.jsonl` records results by `agentId` only — no label, no task number** — so task attribution has to come from the dispatch prompt itself.

Act on what it reports:

| Verdict | Meaning | What to do |
|---|---|---|
| `OK` | implemented + review majority passed | Verify yourself, then mark `[x]` and commit |
| `UNREVIEWED` | code landed, review never finished | **Do not mark `[x]`** — run the review, then decide |
| `INCOMPLETE` | dispatched, never returned = the interrupt point | `git status` to see how far it got; decide roll back vs. finish |
| `REJECTED` / `BLOCKED` | — | Remediate sequentially with bounded rounds |

Then converge as in Step 3. `UNREVIEWED` is the one that actually bites: the code looks finished and the tests may even pass, so it is the state most likely to get waved through — but nothing has adversarially checked it.

**When editing the prompt templates in `spec-exec.workflow.js`, update the anchors in `recover-run.mjs` too.** Task attribution parses phrases out of the prompt (`任务编号：`, `对抗性验收`, `根因优先地调查`); change the wording and recovery silently stops matching — you get an empty ledger that looks like "nothing ran."

#### Wave Mode (concurrent subagent dispatch)

Use when workflow mode is unavailable or the user wants the run to stay in the main loop.

Same per-task contract as sequential autonomous mode (implementer → reviewer → debug on failure, same structured-field parsing, same bounded rounds) — only the scheduling differs. Follow `../../rules/parallel-dispatch.md` throughout.

**`(P)` markers**: `(P)` in tasks.md means the task planner judged the task free of inter-dependencies. In wave mode `(P)` **is** an execution directive: `(P)` tasks in the same wave run concurrently. `_Depends:_` is authoritative when the two disagree — a task with an unmet `_Depends:_` never enters the current wave regardless of `(P)`.

**Per wave**:

**1. Partition** — the wave = all pending tasks whose `_Depends:_` targets are already `[x]`. Then split the wave by write-set collision:
- Union each task's `_Boundary:_` scope. Tasks with **disjoint** boundaries → run concurrently as-is.
- Tasks with **overlapping** boundaries → either dispatch them with `isolation: 'worktree'`, or keep only one in the concurrent batch and defer the rest to the next wave. Never let two concurrent implementers write the same file without worktree isolation.
- Missing `_Boundary:_` on a task → treat its write set as unknown, i.e. colliding with everything; run it alone.

**2. Announce** — before dispatching, print the wave plan: which task IDs run concurrently, which are deferred and why. This is the user's chance to stop a bad partition.

**3. Dispatch implementers concurrently** — one `Agent` call per task, **all in a single message** (`subagent_type: "task-executor"`). Each gets exactly the same prompt it would get in sequential mode (`templates/implementer-prompt.md` + task context + relevant `## Implementation Notes`), plus one addition:

> 你**禁止**修改 `tasks.md` 与 `spec.json`，**禁止** git commit / `git add`，**禁止** `git checkout .` / `git reset --hard` 等恢复类操作。本波次有其他子代理并发工作，这些操作由父层统一执行。只在你的 `_Boundary:_` 范围内改文件。
>
> 验证只跑**本任务边界内的测试文件**（命令见上）+ 类型检查 + lint，**禁止**跑全量测试套件、e2e 或构建。全量回归由复查者与父层各跑一次，你跑不构成证据。本波次有兄弟任务并发改动，全量套件里的红有一半不是你造成的——你去"修"它只会越界。若窄测试的红明显来自边界外，在 `CONCERNS` 里写清楚，不要动手。

**4. Dispatch reviewers concurrently** — collect all implementer status reports, then fan out one reviewer per `READY_FOR_REVIEW` task in a single message (`subagent_type: "spec-task-reviewer"`). Reviewers are read-only and never collide, so they always run concurrently.
- Concurrent implementers mean `git diff` shows **the whole wave's** changes, not just one task's. Give each reviewer its task's `_Boundary:_` file list explicitly and instruct it to review **only those paths** — otherwise it will reject a task for a sibling task's diff.
- Tasks whose implementer returned BLOCKED / NEEDS_CONTEXT skip review and go to remediation (step 6).

**5. Converge (parent-only, serial)** — after all reviewers return, the parent does, one at a time:
- Apply `kiro-verify-completion` to APPROVED tasks using fresh evidence
- Mark `[x]` in tasks.md
- Append learnings to `## Implementation Notes`
- Selective commit per task (`git add <explicit paths>`, never `git add -A`)
- If tasks ran in isolated worktrees, merge their work back before committing

Run the canonical test command **once** over the merged wave result before committing. Concurrent tasks that pass individually can still break each other; a green per-task run is not evidence the wave is green.

**6. Remediate** — REJECTED / BLOCKED tasks drop out of wave mode and are handled **sequentially** with the normal bounded rounds (max 2 implementer re-dispatch rounds, then debug; max 2 debug rounds). Do not re-run a failed task concurrently — remediation needs an uncontended worktree.

**7. Next wave** — re-read tasks.md (the source of truth for what is now `[x]`), recompute the wave, repeat. Retain only a one-line summary per completed task.

**Degrade to sequential** when: the wave keeps producing boundary collisions, two consecutive waves have rejections, worktree isolation is unavailable, or the user asks for tighter control. Say so explicitly when degrading.

#### Manual Mode (main context)

For each selected task:

**1. Build Task Brief**:
Before writing any code, read the relevant sections of requirements.md and design.md for this task and clarify:
- What observable behaviors must be true when done (acceptance criteria)
- What files/functions/tests must exist (completion definition)
- What technical decisions to follow from design.md (design constraints)
- How to confirm the task works (verification method)

**2. Execute TDD cycle** (Kent Beck's RED → GREEN → REFACTOR):
- **RED**: Write test for the next small piece of functionality based on the acceptance criteria. Test should fail.
- **GREEN**: Implement simplest solution to make test pass, following the design constraints.
- **REFACTOR**: Improve code structure, remove duplication. All tests must still pass.
- **VERIFY**: All tests pass (new and existing), no regressions. Confirm verification method passes.
- **REVIEW**: Apply `kiro-review` before marking the task complete. If the host supports fresh subagents in manual mode, use a fresh reviewer; otherwise perform the review in the main context using the `kiro-review` protocol. Do NOT continue until the verdict is parseably `APPROVED`.
- **MARK COMPLETE**: Only after review returns `APPROVED`, apply `kiro-verify-completion`, then update the checkbox from `- [ ]` to `- [x]` in tasks.md.

### Step 4: Final Validation

**Autonomous mode**:
- After all tasks complete, run `/kiro-validate-impl {feature}` as a GO/NO-GO gate
- If validation returns GO → before reporting feature success, apply `kiro-verify-completion` to the feature-level claim using the validation result and fresh supporting evidence
- If validation returns NO-GO:
  - Fix only concrete findings from the validation report
  - Cap remediation at 3 rounds; if still NO-GO, stop and report remaining findings
- If validation returns MANUAL_VERIFY_REQUIRED → stop and report the missing verification step

**Manual mode**:
- Suggest running `/kiro-validate-impl {feature}` but do not auto-execute

## Feature Flag Protocol

For tasks that add or change behavior, enforce RED → GREEN with a feature flag:

1. **Add flag** (OFF by default): Introduce a toggle appropriate to the codebase (env var, config constant, boolean, conditional -- agent chooses the mechanism)
2. **RED -- flag OFF**: Write tests for the new behavior. Run tests → must FAIL. If tests pass with flag OFF, the tests are not testing the right thing. Rewrite.
3. **GREEN -- flag ON + implement**: Enable the flag, write implementation. Run tests → must PASS.
4. **Remove flag**: Make the code unconditional. Run tests → must still PASS.

**Skip this protocol for**: refactoring, configuration, documentation, or tasks with no behavioral change.

## Critical Constraints
- **Strict Handoff Parsing**: Never infer implementer `STATUS` or reviewer `VERDICT` from surrounding prose; only the exact structured fields count
- **Parent-Only State Writes**: Subagents never touch `tasks.md`, `spec.json`, or git. In wave mode this is what keeps concurrency safe — state converges serially in the parent
- **No Unisolated Write Collisions**: Two concurrent implementers must never share a write path; use disjoint `_Boundary:_` scopes or `isolation: 'worktree'`
- **Test Scope by Role**: Implementers run only boundary-scoped tests + typecheck + lint. The canonical full suite runs exactly twice per task-batch: once by the `evidence` lens reviewer (the regression verdict) and once by the parent over the merged result. Never hand `CANONICAL_TEST_COMMANDS` to an implementer — it produces no evidence the reviewer will trust, and under concurrency it makes implementers chase sibling tasks' failures
- **Wave-Level Verification**: Per-task green is not wave green — run the canonical test command once over the merged wave before committing it
- **No Destructive Reset**: Never use `git checkout .`, `git reset --hard`, or similar destructive rollback inside the implementation loop
- **Selective Staging**: NEVER use `git add -A` or `git add .`; always stage explicit file paths
- **Bounded Review Rounds**: Max 2 implementer re-dispatch rounds per reviewer rejection, then debug
- **Bounded Debug**: Max 2 debug rounds per task (debug + re-implementation per round); if still failing → BLOCKED
- **Bounded Remediation**: Cap final-validation remediation at 3 rounds

## Output Description

**Autonomous mode (sequential or wave)**: For each task, report:
1. Task ID, implementer status, reviewer verdict
2. Files changed, commit hash
3. Wave mode only: per wave, which tasks ran concurrently, which were deferred for boundary collision, and the merged-wave test result
4. After all tasks: final validation result (GO/NO-GO)

**Manual mode**:
1. Tasks executed: task numbers and test results
2. Status: completed tasks marked in tasks.md, remaining tasks count

**Format**: Concise, in the language specified in spec.json.

## Safety & Fallback

### Error Scenarios

**Tasks Not Approved or Missing Spec Files**:
- **Stop Execution**: All spec files must exist and tasks must be approved
- **Suggested Action**: "Complete previous phases: `/kiro-spec-requirements`, `/kiro-spec-design`, `/kiro-spec-tasks`"

**Test Failures**:
- **Stop Implementation**: Fix failing tests before continuing
- **Action**: Debug and fix, then re-run

**All Tasks Blocked**:
- Stop and report all blocked tasks with reasons
- Human review needed to resolve blockers

**Spec Conflicts with Reality**:
- If a requirement or design conflicts with reality (API doesn't exist, platform limitation), block the task with `_Blocked: <reason>_` -- do not silently work around it

**Upstream Ownership Detected**:
- If review, debug, or validation shows that the root cause belongs to an upstream, foundation, shared-platform, or dependency spec, do not patch around it inside the downstream feature
- Route the fix back to the owning upstream spec, keep the downstream task blocked until that contract is repaired, and re-run validation/smoke for dependent specs after the upstream fix lands

**Task Plan Invalidated During Implementation**:
- If debug returns `NEXT_ACTION: STOP_FOR_HUMAN` because of task ordering, boundary, or decomposition problems, stop and return for human review of `tasks.md` or the approved plan instead of forcing a code workaround
