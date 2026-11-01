---
name: opsx-solve-workflow
version: "1.26.0"
user-invocable: true
description: "Eight-stage PDCA problem-solving workflow that persists analysis, proposal, design review, plan, execution, and verification into OpenSpec artifacts (openspec/changes/<name>/, archived into openspec/specs/) instead of leaving them only in chat context. Use for feature work, bug fixes, refactors, and complex engineering tasks that need long-term behavioral-contract traceability, team review, or auditability. Do NOT use for a quick one-off edit with no traceability need — use solve-workflow instead. Triggers：「opsx解决」「OpenSpec解决」「规范化解决」「创建OpenSpec变更」「创建opsx变更」「用OpenSpec分析」「用OpenSpec修复」「opsx自动解决」「OpenSpec自动解决」「opsx-solve」「opsx-solve-workflow」；「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / opsx solve, OpenSpec solve workflow, create an OpenSpec change, ai-proxy mode, switch to ai-proxy."
dependencies:
  - solution-review
  - code-design-review
  - hybrid-debug
  - runtime-evidence-debug
  - browser-debug-toolkit
  - node-version-discipline
  - learn-and-improve
  - workflow-mode-lifecycle
  - clarifying-question-discipline
  - known-issue-research
  - competitive-research
  - analysis-core
  - test-suite-ensure
  - merge-discipline
  - staged-review-flow
  - opsx-workspace-gate
  - completion-evidence-discipline
  - domain-language-discipline
  - test-first-discipline
  - design-approval-gate
  - delivery-discipline
  - feature-branch-closeout
  - decision-fog-discipline
  - git-worktree-discipline
  - figma-pixel-implement
  - figma-pixel-verify
  - runtime-verification-discipline
  - ai-proxy-discipline
  - context-budget-discipline
---

# OPSX Eight-Stage Problem-Solving Workflow

> Combines `solve-workflow`'s eight-stage PDCA discipline with OpenSpec/OPSX artifact persistence. The goal: never let the AI skip analysis, proposal, review, or verification, and never let the key conclusions live only in chat context.
>
> **Output templates**: see [reference.md](reference.md) for each stage's format.

## Positioning

Use this skill for engineering changes that are **worth persisting**: requirements, root cause, behavior changes, technical trade-offs, task lists, and verification results should all be written to `openspec/changes/<change-name>/`, then merged into `openspec/specs/` via archive on completion.

Division of labor:

- **OpenSpec**: the source of truth and archive system — answers "what, and why".
- **solve-workflow-style gates**: stage gating — answers "when is it allowed to move to the next step".

Not a replacement for plain `solve-workflow`:

- Quick fixes, single-file lightweight edits, or tasks needing no long-term traceability — prefer `solve-workflow`.
- Tasks involving long-term behavioral contracts, team review, concurrent changes, requirement audits, or later traceability — use this skill.

## Invocation conventions

- **Triggers**: opsx解决, OpenSpec解决, 规范化解决, 创建OpenSpec变更, 创建opsx变更, 用OpenSpec分析, 用OpenSpec修复, opsx自动解决, OpenSpec自动解决, opsx-solve, opsx-solve-workflow; ai-proxy 模式, AI 代理模式, 切换 ai-proxy
- **Mode**: overlay triggers (「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / "ai-proxy mode" / "switch to ai-proxy") request overlay per `workflow-mode-lifecycle` (overlay+freeze wins if an auto trigger is also present). Else a trigger containing "自动" (auto) enters auto mode; otherwise manual mode by default.
- **Manual mode**: the key exits of stages 1, 2, 3, 4, 5, 7, 8 must wait for user confirmation.
- **Auto mode**: auto-advances through to verification; the stage 4 review loop caps at 3 rounds, then pauses.

**Unattended proxy exits**: when this-run contract or task card records `Stage-exit policy: ai-proxy` (auto carrier; queue child is sufficient but not required), each manual exit above becomes a proxy checkpoint per `ai-proxy-discipline`. Thin freeze (verbal trigger ≠ occupancy) lives there. The pre-execution approval point takes the proxy's bounded pre-authorization instead of the bare auto escape of `design-approval-gate`; merge, irreversible, and protected-branch decisions stay human-only (park + ticket). Any other policy value or none → behavior identical to today.

**Stop-point forecast**: if this run **starts** with a frozen contract (queue child with problem + frozen decisions, or independent thin freeze already written), open with a forecast table before analysis — every manual exit × covered-by-frozen-decisions vs will-form-a-new-ticket. If overlay is requested **mid-run**, after thin freeze output a forecast of **remaining** exits, then continue the current stage (do not restart from analysis).

**Strong-dependency skills** (frontmatter `dependencies`; must pass the "Prerequisite skill check" at startup — abort if any is missing):
- `staged-review-flow` (stage 4 review orchestration; depends on `solution-review` and `code-design-review`)
- `hybrid-debug` / `runtime-evidence-debug` / `browser-debug-toolkit` (delegated via `analysis-core`; stage 2 + stage 7)
- `analysis-core` (single source for stage-2 analysis methodology: temporary-change gate / instrumentation debug with runtime-evidence-debug as default entry / analysis step skeleton / analysis gate output block / debug-verify loop)
- `context-budget-discipline` (stage 6/7 entry: phase-boundary reset evaluation, proactive compaction threshold, ledger handoff before any reset)
- `node-version-discipline` (stage 7 Node version alignment)
- `learn-and-improve` (stage 8 retrospective and knowledge sediment)
- `workflow-mode-lifecycle` (auto/manual mode lifecycle)
- `clarifying-question-discipline` (hard discipline for active questioning + investigation-first)
- `known-issue-research` (stage 2 research routing / known-issue quick search / industry-wide evaluation)
- `competitive-research` (user-visible competitor behavior during analysis; method stays in that skill)
- `test-suite-ensure` (stage 6 test-suite ensure: complete and run tests when infra exists; scaffold with user confirmation when it doesn't)
- `test-first-discipline` (stage 6: failing-test-first for behavior changes; distinct from test-suite-ensure)
- `design-approval-gate` (before stage 6: no production impl without approval; named auto/hotfix escapes)
- `delivery-discipline` (stage 8: optional commit + open/update PR/MR after archive; not every run delivers)
- `feature-branch-closeout` (stage 8: post-archive closeout menu; merge delegates to merge-discipline)
- `decision-fog-discipline` (before explore solutions: graduate fog / decision tickets first)
- `git-worktree-discipline` (before stage 3 — first artifact write: worktree gate + optional isolated workspace)
- `domain-language-discipline` (clarify/analyze: project glossary / CONTEXT.md when domain terms matter)
- `merge-discipline` (stage 8 merge discipline — after closeout selects merge)
- `opsx-workspace-gate` (stage 0 OpenSpec workspace and native-skill gate)
- `figma-pixel-implement` / `figma-pixel-verify` (Figma export-faithful implement + measured verify; required installed; invoke when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or the user asks for pixel restore)

## Prerequisite skill check

> At startup (after the stage-0 gate passes, before stage 1), check frontmatter `dependencies`: scan available skills, and if any is missing → print a structured prompt and **abort immediately** (format: solve-workflow/reference.md「Prerequisite Skill Check — Missing Notice」).

> **No-degradation principle**: a missing strong dependency means abort — never fall back to a simplified review or debug flow.

## Mode lifecycle

> Entry, persistence, and exit rules for auto mode, preventing mode stickiness where the user is unaware the AI is still making automatic decisions. The core rules (revert-to-manual / explicit re-entry / implicit continuation never re-activates / batch scenarios) live in the strong-dependency skill `workflow-mode-lifecycle` (already guaranteed available by the prerequisite check) — not restated here.

### OpenSpec-specific notes

- After stage 8 archiving completes, mode auto-reverts to manual.
- If the user decides to start another PDCA round (back to stage 3/4/5), it defaults to manual mode.
- An archive interruption (e.g. the `openspec-archive-change` skill fails) also counts as a flow interruption — revert to manual.

---

## Stage 0: Environment check & path selection

This skill requires a fully initialized OpenSpec workspace; there is no degraded path. Load `opsx-workspace-gate` and run its project-root location, `openspec/` check, and exact native-OPSX-skill gate; once it passes, this workflow keeps its own stage gating and downstream orchestration.

### Prep steps after passing the gate

1. Decide whether to use an existing change or create a new one, and prepare only a candidate name:
   - If the user names a change, prefer using it.
   - Otherwise generate a kebab-case candidate name for the new work, and confirm it with the user in manual mode.
2. Prepare the creation method, but do not create the directory before the stage-1 user confirmation: create the change via the `openspec-new-change` skill (read its SKILL.md, then follow its instructions).

### Path selection

Pick a path per the task and declare it before continuing:

| Path | Fits | Requirements |
|------|------|---------------|
| Full | Brand-new feature, complex module, fuzzy requirements | Run stages 1-8 in full |
| Incremental | Existing-behavior change, refactor, ordinary bug | Run stages 1-8, but proposal/spec may stay lean |
| Lean | Hotfix, small high-certainty change | Keep proposal, delta spec, tasks, verification, and archive — never skip verification |

If scope expands mid-execution, the path must be upgraded: lean → incremental, incremental → full. In manual mode, an upgrade needs user confirmation.

## Stage-to-artifact mapping

| Stage | Goal | OpenSpec landing spot | Code writes |
|------|------|---------------|----------|
| 1. Clarify the problem | Align on the problem, extract elements, resolve open questions | Analysis only, no artifact | Forbidden |
| 2. Analyze the problem | Confirm existence, locate root cause, assess impact | Analysis only, no artifact (conclusions land in `proposal.md` after stage 3) | Forbidden |
| 3. Explore solutions | Present 2-5 solutions and pick one | `proposal.md` (complete) + `specs/<capability>/spec.md` (delta specs), via `openspec-continue-change` | Forbidden |
| 4. Review the solution | Review validity, risk, feasibility | `design.md` (via `openspec-continue-change`) | Forbidden |
| 5. Make the plan | Break into executable tasks | `tasks.md` (via `openspec-continue-change`) | Forbidden |
| 6. Execute the plan | Implement per task and check them off; once all tasks are done call `test-suite-ensure` to make sure the test suite is in place | Update `tasks.md` checkboxes (via `openspec-apply-change`); test files (generated by `test-suite-ensure`) | Allowed |
| 7. Check & verify | Test, validate, cross-check against artifacts | Verification conclusions (via the `openspec-verify-change` skill or `openspec validate`) | Forbidden |
| 8. Review & archive | Land the result or start another round | `openspec/specs/` update + move into `openspec/changes/archive/` (via the `openspec-archive-change` skill) | Archive/docs only |

Stages 1-5 forbid modifying business code but allow creating and updating OpenSpec artifacts. If the user asks to "just analyze, don't persist", output stage conclusions only and skip writing artifacts.

## Stage 1: Clarify the problem

**⚠️ Active questioning**: follow `clarifying-question-discipline` (one question per round, multi-round until clear; clarify first, don't rush to answer). When domain vocabulary is in play, also follow `domain-language-discipline`.

> **Domain routing**: if the problem is performance-domain (slow / jank / resource growth), suggest entering `perf-optimize-workflow` — its evidence-gated paradigm fits the domain; its analysis output can flow back into this workflow (artifacts still land in OpenSpec per this workflow). Note: its campaigns create per-project artifacts (benchmark log + harness, and seeded `code-insight`/`code-optimizer` skills); the optimize-verify loop additionally requires an environment loop runner — analysis stages always run. Informational reference, not a dependency.

Manual mode must complete the following steps in order:

1. **Restate the problem** — describe the user's problem in your own words.
2. **Extract key elements** — goal, constraints, background, expected outcome.
3. **List open questions** — enumerate points needing further confirmation; if asking the user, ask only the single most critical one at a time, then ask the next only after getting an answer.
3.5. **Scope breakdown** (if applicable) — if the problem spans multiple independent subsystems, help break it down first: independent modules, dependencies, suggested handling order — then enter stage-2 technical analysis for the first sub-problem.
4. **Wait for user confirmation.**

**Tool restriction**: Read/Grep/SemanticSearch are forbidden, with these **exceptions**:
- The user's message contains `@file-path` (optionally with line numbers)
- The user's message pastes a code snippet
- The user explicitly names a "function/class name + its file" combination

Under an exception: **read only the file and lines the user directly referenced**, never expand to other files. The read result only aids understanding of the problem — **no technical-analysis conclusion may appear in the stage-1 output**.

Output format for manual mode: see [reference.md](reference.md)「Stage 1 Clarify the Problem」.

Do not create a change or modify any file before user confirmation. After confirmation:

1. Create the change directory via the `openspec-new-change` skill (read its SKILL.md, then follow its instructions).
2. Record this round's path choice (full / incremental / lean).
3. Then proceed to stage-2 technical analysis.

Auto mode may skip the confirmation, but must still generate the candidate name first, then create the change immediately and continue.

## Stage 2: Analyze the problem

> Single source for analysis methodology: `analysis-core`. This stage leaves no implementation change — fixes belong in stage 6.

### Delegate to `analysis-core`

Load the strong dependency `analysis-core` and execute its §§1-3. This workflow's mapping (number + name):

- `{next-stage}` = Stage 3 "Explore solutions"
- `{root-cause step}` = step 5; `{impact-assessment step}` = step 7; `{upstream-eval step}` = step 6

🔌 **OPSX**: this stage creates **no artifact**; Why / Impact are written into `proposal.md` once stage 3 selects a solution.

The stage output MUST close with the analysis gate output block (`analysis-core` §5 — red loop / debug entry / scenario supplements / temporary changes); a missing block blocks entry to Stage 3. When the expected outcome is a result the user can see or operate, that same load runs `competitive-research` per `analysis-core`. Do not restate its method.

If the existence check fails or the description mismatches the code, pause for user confirmation and do not proceed to solution exploration.

---

## Stage 3: Explore solutions

> Principle: based on the stage-2 analysis, offer 2-5 solutions; strip non-essential features and over-engineering from every solution (YAGNI). If the path is still foggy, follow `decision-fog-discipline` before the solution table / proposal.

> **Architecture-boundary precheck** (decision order): when a candidate solution crosses process or layer boundaries, answer the precheck before short-term costs (change size / reuse / single-repo) are weighed — (1) runtime initialization location: which process/layer initializes the called capability; (2) boundary legality: would a cross-layer import pull the callee's dependency tree into the caller's bundle graph (bundler static pre-scanning defeats dynamic `require`/`import` as a workaround); (3) ownership classification: system vs data/product capability vs the calling layer's positioning. The boundary verdict surfaces with the comparison table and gates auto-mode selection. Methodology: `code-design-review` Layer A dependency-direction dimension. Single-layer solutions do not trigger this precheck.

Produce 2-5 solutions based on stage 2, each including:

- Core idea
- Capabilities or behavior changes involved
- OpenSpec capabilities to add or modify
- Pros, cons, complexity, risk
- Recommended solution

In manual mode, output the comparison table and then pause for the user's pick.

Before the first artifact write (`proposal.md`), load `git-worktree-discipline` (worktree gate + optional isolation).

🔌 **OPSX skills integration**: once a solution is selected, complete the following two steps via the `openspec-continue-change` skill (each call creates one artifact — read its SKILL.md first, then follow its instructions):

1. **Create `proposal.md`** (the change's first ready artifact): merge stage 2's root-cause analysis (Why / Impact) with this stage's solution selection (What Changes / Capabilities) into a complete proposal.
2. **Create delta specs** (specs become ready once the proposal is complete): write behavior changes into `specs/<capability>/spec.md`.

Delta-spec conventions (enforced by the `openspec-continue-change` skill):

- Only behavior changes: `## ADDED`, `## MODIFIED`, `## REMOVED`, `## RENAMED Requirements`
- Every requirement heading must be `### Requirement: <description containing SHALL or MUST>`
- Every requirement must include at least one `#### Scenario:` block

> Common mistakes: `### REQ-001:` (wrong format), `### Requirement: Initialize` (missing SHALL/MUST), no Scenario block.
> All three fail `openspec validate`. Format examples live in the `openspec-continue-change` skill.

### Red flags — forbidden in stage 3

- Generating only 1 solution and skipping the comparison on the grounds that "the direction is already clear"
- Advancing to review in manual mode before the user picked a solution
- A solution carrying non-essential features or over-engineering (violates YAGNI)

## Stage 4: Review the solution

Load `staged-review-flow` and execute its full review contract. This workflow's mapping: `{next-stage}` = Stage 5 "Make the plan"; `{artifact-sink}` = `design.md` created via `openspec-continue-change`; `{extra-dimensions}` = spec compliance (proposal's why, delta specs' behavior, design's risk, tasks' coverage of requirements); `{batch-overcap-behavior}` = `N/A`. After the review passes, create `design.md` via the native skill.

**Non-blocking issues** (may be noted as suggestions but don't block passing; blocking/non-blocking criteria are owned by `solution-review` and, for code solutions, `code-design-review` — a marginally better architecture with no material long-term maintainability gain does not block; a clearly superior feasible one does, per those skills):

- Low-risk items with an existing mitigation
- Code-style preferences that don't affect correctness or structure
- Non-structural performance improvements deferrable to a later iteration
- Explicitly accepted Prudent-Deliberate technical debt (with a repayment plan)

### Red flags — forbidden in stage 4

- Skipping the solution review and going straight to stage 5 (risks unidentified)
- Modifying code during the review stage (violates the read-only constraint)
- Not optimizing the solution when auto-mode review fails, and advancing to stage 5 anyway
- Auto-mode review loop exceeding the 3-round cap without pausing
- Auto-mode optimizing the solution without recording the optimization rationale, breaking review traceability
- The AI advancing on its own in manual mode when the user hasn't given an explicit pass/fail verdict

## Stage 5: Make the plan

🔌 **OPSX skills integration**: generate `tasks.md` via the `openspec-continue-change` skill (read its SKILL.md first, then follow its instructions; tasks become ready once both specs and design are complete). This skill never hand-writes `tasks.md` content directly.

`tasks.md` conventions (enforced by the skill):

- Use checkboxes; tasks fine-grained enough; ordering reflects dependencies
- Include necessary test, verification, documentation, or migration steps
- No `TBD`, `TODO`, "handle appropriately", "similar to above", or other non-actionable descriptions

In manual mode, output the plan and pause; wait for user confirmation before entering stage 6.

## Stage 6: Execute the plan

Before production edits, follow `design-approval-gate` (manual: user pass; auto/lean: named escape + 留痕).

**Context budget**: evaluate the phase-boundary reset and the compaction threshold per `context-budget-discipline` (ledger path from the stage-5 plan); any reset requires a complete ledger entry first.

**Figma pixel fidelity:** Load `figma-pixel-implement` and follow it when the goal, card, issue, or plan text contains `figma.com` or `node-id=`, or when the user asks for pixel restore (像素级还原). That substring is the scope fact. Keep those rows hard; do not place them under soft or human because the task also checks behavior. A probe of visible text, a visibility flag, or a list length does not pass the pixel rows. When that same text also contains `参考`, `match the existing`, or `same as`, pass that fact into verify so the named control's interaction states become rows. Implement is incomplete without a durable inventory+spec path in the target repo. That skill continues into `figma-pixel-verify` in the same run until overall PASS or the measurement command cannot run. Do not restate its methodology here.

Read `tasks.md` and implement in order:

1. Work on the single smallest current task at a time.
2. Before touching business code, confirm the relevant proposal, specs, design, and tasks already exist.
3. **Update the checkbox immediately after finishing a task**: use StrReplace to flip the corresponding `[ ]` to `[x]` in `tasks.md` — do not batch this until after a group of tasks. Skipping this makes the stage-7 verifier report a CRITICAL false-incomplete.
4. If implementation reveals the design or spec is inaccurate, update that artifact first, then continue implementing.
5. State the reason for any deviation from the plan; if the deviation affects scope or the behavioral contract, return to stage 4 or stage 5.

### Test-first then test-suite ensure (mandatory, before the execution report)

For behavior-changing work, follow `test-first-discipline` (failing test observed before production code). Once every `tasks.md` checkbox is checked, before outputting the execution report, this step is mandatory:

Load and call `test-suite-ensure`, declaring `mode=mandatory`, scoped to this change's logic files; a failure or a declined necessary-scaffolding request blocks entry to stage 7. test-suite-ensure does not satisfy test-first.

🔌 **OPSX skills integration**: call the `openspec-apply-change` skill to execute the tasks (read its SKILL.md first, then complete each task per its instructions). `openspec-apply-change` queries change status and execution instructions via the CLI internally; this skill never calls the CLI directly to drive execution.

## Stage 7: Check & verify

**Context budget**: verify against the ledger + artifacts when a reset occurred (per `context-budget-discipline`); never replay prior-session history.

Verification must cover three layers:

1. **OpenSpec validation**:
   - If the `openspec-verify-change` skill is detected → read its SKILL.md and delegate verification to it.
   - If it's absent → run `openspec validate <change-name>` or `openspec validate --changes` directly (a CLI tool call, not a degradation).

**Node version alignment (prerequisite)**: call `node-version-discipline` to align to the project's declared Node version before running the engineering-verification commands below.

2. **Engineering verification**: run the project's tests, type check, lint, or build (under the aligned version).
3. **Behavior cross-check**: confirm the implementation covers every delta-spec requirement and scenario, one by one.
4. **Debug-verify loop**: if stage 2 used a debug skill to locate the root cause, verify the fix using that **same** skill per `analysis-core` §4 (not tests alone).
5. **Figma pixel verify**: when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or this run implemented from Figma, load `figma-pixel-verify` and follow it; a missing measured report (the living artifact’s Verify section, or the Spec source sibling) blocks this verification stage from passing. A spec-gap FAIL does not pass verification—re-enter `figma-pixel-implement` to complete the table. Also load verify when the user/plan requires alignment checking without a same-run implement. This stage passes only when that report’s overall status is PASS (accepted residuals included) and its channel is a laid-out measurement (`storybook`, `isolated-harness`, `preview`, `full-app`, or `layout-probe`). Any other result fails this stage and returns to the implement stage for another fix/re-measure loop. This stage also runs `scripts/check-figma-verify-report.mjs` from the `figma-pixel-verify` skill on that report; a non-zero exit fails the stage. Do not restate its methodology.

Verification conclusions must be based on commands you ran and personally read the output of this round — never report "a scenario was designed" as "passed".

When this turn's dispatch inlines a frozen task card, the verification report includes the problem, the cause, and the completed fix, and an evidence list. Each evidence item is an opened-UI check citing a png, jpg, jpeg, or webp path, or a non-UI check citing the command and a short output summary. A missing or empty image is pending and states the capture still required. Do not invent an image. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. This run does not write the HTML page and does not write the evidence HTML.

Output format: see [reference.md](reference.md)「Stage 7 Check & Verify」.

> Label each result per `staged-review-flow`'s verification-report honesty rule and `completion-evidence-discipline` (no pass claims without fresh current-turn evidence).

Manual mode pauses here to wait for user confirmation before archiving. Do not archive on a failed verification — return to stage 4, 5, or 6 instead.

### Test execution

If the stage-6 execution report involves tests (unit tests, integration tests, manual verification steps):

**Verification execution follows `runtime-verification-discipline`** (strong dependency): the AI executes verification itself in an environment, and hands a step to the user only at a classified true hard boundary, with the reason stated.

- **AI can execute**: use Bash to run test commands (e.g. `npm test`, `pytest`, `go test`) and fold the result into the check conclusion.
- **Otherwise**: classify the blocker per `runtime-verification-discipline`; only a true hard boundary becomes a user step, stated with its reason.

## Stage 8: Review & archive

If verification passed, run the pre-archive check:

- Are all `tasks.md` items complete?
- Do the delta specs represent the actual implementation?
- Will the main specs be updated correctly?
- Has the user confirmed archiving?

🔌 **OPSX skills integration**: before archiving:

1. **If delta specs exist**: call the `openspec-sync-specs` skill (if installed) to merge delta specs into the main `specs/<capability>/spec.md`, or let `openspec-archive-change` prompt for and handle the sync during archiving.
2. **Execute the archive**: call the `openspec-archive-change` skill (read its SKILL.md first, then follow its instructions).

If `openspec-archive-change` fails, do **not** manually manipulate the `openspec/` directory — stop and tell the user to check the OpenSpec installation.

After archiving, always check the diff to confirm both the main-specs update and the archive-directory move landed in the project root's git working-tree changes. Then load `delivery-discipline` when this run may need commit + PR/MR (archive diffs usually need delivery; the skill's need-delivery gate may still skip). Then load `feature-branch-closeout` for the closeout menu (PR / merge / keep / continue). Never declare completion while tests haven't passed, archiving isn't complete, or the diff hasn't been reviewed.

> **Order constraint**: archive + diff check → optional `delivery-discipline` → `feature-branch-closeout` → on merge, `merge-discipline` A→B→C→R→D. Choosing keep/continue does not trigger merge discipline.

#### Merge discipline (`merge-discipline` skill)

> On merge (from closeout or a direct user merge command), load `merge-discipline` and run Part A → B → C → R → D; the pre-merge checklist is in `merge-discipline/reference.md`. Never implicitly skip.

### Retrospective (delegate to `learn-and-improve`)

Once archiving and branch closeout are complete, load `learn-and-improve` and follow its framework; OpenSpec artifacts archived through the normal flow are not subject to its sediment-value gate.

> **OpenSpec artifacts** (`proposal.md`, `specs/`, `design.md`, `tasks.md`) are this skill's core deliverables, landed through the normal archive flow — not subject to `learn-and-improve`'s sediment-value gate.
> **AI engineering knowledge** (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, project-local skills, etc.) has its sediment-value judgment and carrier selection owned by `learn-and-improve`'s decision tree; writing requires an explicit user request first.

Output format after archiving: see [reference.md](reference.md)「Stage 8 Review & Archive」.

If archiving isn't appropriate, keep the change active and state the blockers and next steps.

## Common mistakes

> Only non-obvious pitfalls specific to this skill are listed here. Merge/coverage/tip pinning → `merge-discipline`; project-root/`openspec/`/native-skill gates → `opsx-workspace-gate`. Rules already stated in the stage body are not repeated.

| Mistake | Consequence | Fix |
|------|------|------|
| Creating the change before manual-mode confirmation | Breaks the stage-1 gate, may create the wrong directory | Stage 0 only prepares a candidate name; create it only after confirmation |
| Creating the proposal right after root-cause analysis (solution not yet chosen) | Why/What are disconnected, the artifact needs a rewrite | Create the proposal only after stage 3 picks a solution, in one pass via `openspec-continue-change` |
| Treating an old/short name as passing the gate (e.g. `openspec-propose`, `openspec-apply`) | Hand-written against a stale schema, or its SKILL.md can't be found | Accept only the exact four names: `openspec-new-change` / `openspec-continue-change` / `openspec-apply-change` / `openspec-archive-change` (`verify` is optional) |
| `MODIFIED` writing only a fragment | The archived requirement loses its original content | Copy the full requirement block, then edit |
| Running the coverage gate when branch closeout picked "keep / continue development" | Wrongly triggers the gate on a non-merge decision | The gate only fires on a "merge" decision |
| Running the analyzer by default under `ask` or when unconfigured | Forces a project with no coverage need through the gate | See `merge-discipline` Part C: resolve the preference first — `ask` must ask |
| Batching `tasks.md` checkbox updates until a group of tasks finishes | The verifier reports a CRITICAL false-incomplete | Flip the corresponding `[ ]` to `[x]` the moment each item finishes |
| Writing "a scenario was designed" as "verification passed" | The user accepts a false pass | Label each item "executed (command + output summary)" or "pending (action needed)" |
| A delta requirement without SHALL/MUST or without a Scenario | `openspec validate` keeps failing | Use SHALL/MUST in the description; add a `#### Scenario:` |
| Browser assertions based on assumed DOM instead of observed state | `waitForFunction` times out | Read the real value via `evaluate` before asserting |

## Minimum success criteria

A complete run must produce or update at least:

- `openspec/changes/<change-name>/proposal.md`
- `openspec/changes/<change-name>/specs/<capability>/spec.md`
- `openspec/changes/<change-name>/design.md`
- `openspec/changes/<change-name>/tasks.md`

On completion:

- All tasks are checked off.
- `test-suite-ensure` has run: unit tests all pass; E2E tests pass or a skip reason is stated.
- OpenSpec validation passes.
- Project verification passes, or manual-verification items are explicitly listed.
- Archived after user confirmation, or the change is kept active with the reason for not archiving stated.
