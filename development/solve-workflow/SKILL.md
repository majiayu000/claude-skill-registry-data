---
name: solve-workflow
version: "1.32.0"
user-invocable: true
description: "Eight-stage PDCA workflow for systematically solving bugs, refactors, and feature-development tasks: clarify → analyze → explore solutions → review → plan → execute → verify → retrospect. Manual mode (default) pauses for user confirmation at each stage exit; auto mode runs end-to-end; ai-proxy overlay (thin freeze then occupy) is available independently. Triggers — 「明确问题」「分析问题」「探索方案」「审查方案」「制定计划」「执行计划」「检查验证」「复盘改进」(alias「回顾总结」)；「继续分析」「深入分析」「修改方案」「完善方案」「优化方案」「更新计划」「修订计划」「修改计划」；「自动模式」「自动分析」「自动解决」；「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / clarify problem, analyze problem, explore solutions, review solution, make plan, execute plan, verify, retrospective, auto mode, ai-proxy mode, switch to ai-proxy."
dependencies:
  - solution-review
  - code-design-review
  - hybrid-debug
  - runtime-evidence-debug
  - browser-debug-toolkit
  - learn-and-improve
  - workflow-mode-lifecycle
  - clarifying-question-discipline
  - known-issue-research
  - competitive-research
  - analysis-core
  - test-suite-ensure
  - node-version-discipline
  - staged-review-flow
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

# Eight-Stage Problem-Solving Workflow

> An eight-stage PDCA flow. Stages 1, 3, 4, 5 are read-only. Stage 2's analysis methodology lives in `analysis-core` (including the temporary-change gate). Default is manual mode; say "自动模式" or "自动分析" to run the full flow automatically. On completion, enter stage 7; if stage 8 concludes the goal is not met, loop back to "分析问题" / "探索方案" / "审查方案" for another cycle.
> **Output templates**: each stage's output format is in [reference.md](reference.md).

## Invocation Conventions

- **Trigger words** (per `description`): 明确问题, 分析问题, 探索方案, 审查方案, 制定计划, 执行计划, 检查验证, 复盘改进 (alias 回顾总结); 继续分析, 深入分析, 修改方案, 完善方案, 优化方案, 更新计划, 修订计划, 修改计划; 自动模式, 自动分析, 自动解决; ai-proxy 模式, AI 代理模式, 切换 ai-proxy
- **Command form**: `/solve-workflow xxx`, `/solve xxx`, where `xxx` is the follow-up content
- **Default behavior**: when `xxx` contains none of the above triggers, default to stage 1 (clarify the problem), treating `xxx` as the problem description to analyze
- **Matching rule**: a trigger word appearing anywhere in `xxx` counts as a match — exact phrasing is not required
- **Not applicable**: single-step edits (e.g. renaming one variable) or when the user only wants a quick suggestion rather than the full flow — skip this workflow and handle directly

**Strong dependencies** (frontmatter `dependencies`; the prerequisite skill check below must pass at startup, or the flow aborts):
- `staged-review-flow` (stage 4 review orchestration; depends on `solution-review` and `code-design-review`)
- `hybrid-debug` / `runtime-evidence-debug` / `browser-debug-toolkit` (debug skills delegated to via `analysis-core`; stage 2 + stage 7)
- `analysis-core` (single source of truth for stage 2's methodology: temporary-change gate / instrumentation debug with runtime-evidence-debug as default entry / analysis step skeleton / analysis gate output block / debug-verify loop)
- `learn-and-improve` (stage 8 retrospective and knowledge sediment)
- `workflow-mode-lifecycle` (manual/auto mode lifecycle), `clarifying-question-discipline` (hard clarifying-question discipline and investigation-first), `known-issue-research` (stage 2 research routing / known-issue quick search / industry-wide evaluation), `competitive-research` (user-visible competitor behavior during analysis; method stays in that skill)
- `test-suite-ensure` (stage 6 test completion: generate and run tests when test infrastructure exists; scaffold with user confirmation when it doesn't)
- `test-first-discipline` (stage 6: failing-test-first for behavior changes; distinct from test-suite-ensure)
- `design-approval-gate` (before stage 6: no production impl without approval; named auto/hotfix escapes)
- `delivery-discipline` (stage 8: optional commit + open/update PR/MR before closeout; not every run delivers)
- `feature-branch-closeout` (stage 8: post-verify branch menu; merge delegates to merge-discipline when used)
- `decision-fog-discipline` (before explore solutions: graduate fog / decision tickets first)
- `git-worktree-discipline` (before stage 6: worktree gate + optional isolated workspace)
- `domain-language-discipline` (clarify/analyze: project glossary / CONTEXT.md when domain terms matter)
- `node-version-discipline` (Node-version alignment before running tests in stage 7)
- `figma-pixel-implement` / `figma-pixel-verify` (Figma export-faithful implement + measured verify; required installed; invoke when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or the user asks for pixel restore)

**Related skills** (informational, not a strong dependency): `perf-optimize-workflow` (dedicated performance optimization paradigm), `jira-fix-workflow` (end-to-end Jira fix flow that embeds this workflow)

## Prerequisite Skill Check

> Run this check at startup, before entering stage 1, against every strong dependency declared in frontmatter `dependencies`.

1. Scan available skills (check `<available_items>` or use the `skill` tool)
2. All present → continue
3. Any missing → print the missing-dependency notice (format in [reference.md](reference.md) § Prerequisite Skill Check — Missing Notice) and **abort immediately**

> **No-downgrade principle**: a missing strong dependency aborts the flow — never fall back to a simplified review. This keeps solve-workflow's review depth consistent across every environment.

---

## Triggers and Modes

| Phrasing | Mode | Note |
|---------|------|------|
| "分析问题", "探索方案", `/solve xxx` | 👤 Manual | Default; pauses for confirmation between stages |
| "自动分析 xxx", "自动解决 xxx", "自动模式" | 🤖 Auto | Runs the full flow with no confirmation |
| "ai-proxy 模式", "AI 代理模式", "切换 ai-proxy" | overlay | Auto carrier; thin freeze then occupy per `ai-proxy-discipline` |

**Mode detection**: overlay triggers (「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / "ai-proxy mode" / "switch to ai-proxy") request overlay per `workflow-mode-lifecycle` — if both an auto trigger and an overlay trigger appear, overlay+freeze wins over naked auto. Else a trigger containing "自动" (auto) selects auto mode; otherwise manual. Mid-run: "切换自动模式" / "切换手动模式" / "切换 ai-proxy". 👤 Manual pauses at every stage exit for confirmation; 🤖 Auto proceeds throughout, pausing only when stage 4's review loop exceeds 3 rounds; overlay occupies those exits per `ai-proxy-discipline` after thin freeze.

## Mode Lifecycle

> The core rules (auto always reverts to manual / explicit re-entry only / implicit continuation never re-activates it / batch scenarios) live in the strong dependency `workflow-mode-lifecycle` (guaranteed available by the prerequisite check) and are not repeated here. solve-workflow-specific: "full flow completes" means stage 8 finishes normally (including looping back into a new PDCA cycle at stage 3/4, which defaults to manual). Failure abort, user-initiated stop, and termination after a review-cap pause all count as interruption and revert to manual.

---

## ⚡ Quick Reference (read before executing; update alongside any stage change)

> This table is a gate overview; the per-stage body is authoritative for rule details.

| Stage | Tool permissions | 👤 Manual stop point | Required output |
|------|---------|-------------|--------|
| 1 Clarify the problem | ❌ Read/Grep (exceptions in the stage 1 body) | ⛔ Stop after output, wait for confirmation | Restatement / key elements / open questions |
| 2 Analyze the problem | Per `analysis-core` (Read/Grep/WebSearch; Edit/Write limited to analysis-assist) | Continue to stage 3 | Existence / root cause / impact / temporary-change rollback verification (format per `analysis-core`) |
| 3 Explore solutions | ✅ Read; ❌ Edit/Write | ⛔ Stop after the comparison table, wait for the user's choice | Solution comparison table (≥2 options) |
| 4 Review the solution | ✅ Read; ❌ Edit/Write | ⛔ Stop after the review report, wait for the user's verdict | Review report + pass/fail |
| 5 Make a plan | ✅ Read; ❌ Edit/Write/Bash | ⛔ Stop after the plan, wait for confirmation | File change list + order |
| 6 Execute the plan | ✅ Everything | Auto-advance to stage 7 when clean | Execution report |
| 7 Verify | ✅ Bash; ❌ Edit/Write | ⛔ Stop after the results, wait for confirmation | Verification results |
| 8 Retrospective | ❌ Edit/Write (unless the user confirms writing, delivery, or a new cycle starts) | End / or loop back to stage 3/4 | Optional delivery + closeout + improvement suggestions |

---

## General Principles

### ⚠️ Clarifying Questions

> ⚠️ Follow `clarifying-question-discipline` (one question per turn; multi-round until clear; clarify first, do not rush to answer). When domain vocabulary is in play, also follow `domain-language-discipline` (glossary / CONTEXT.md).

---

## Path Selection

Choose a path by task complexity, and declare it when confirming the problem in stage 1:

| Path | When to use | Requirement |
|------|----------|------|
| Full | New feature development, multi-module coordination, ambiguous requirements | Run stages 1–8 in full |
| Incremental | Behavior changes to existing code, refactors, ordinary bugs | Run stages 1–8, but solutions and plans may stay lean |
| Lean | Hotfixes, single-file high-certainty changes | Lean output; 1 solution + a risk note is enough, and the plan can fold into the solution description. Stages 7/8 are never skipped |

If scope grows mid-execution, upgrade the path: lean → incremental, incremental → full. In manual mode, upgrading requires user confirmation.

On the lean path, stage 3 (explore solutions) may output just 1 solution + a risk note, and stage 5 (make a plan) may fold into the solution description. Stage 7 (verify) and stage 8 (retrospective) are never skipped.

---

## Unattended proxy exits

When this-run contract or task card records **`Stage-exit policy: ai-proxy`** (auto carrier; queue child is sufficient but not required), each manual stop point above becomes a proxy checkpoint per `ai-proxy-discipline`. Thin freeze (verbal trigger ≠ occupancy) lives there. At the pre-execution approval point the proxy's bounded pre-authorization replaces the bare auto escape of `design-approval-gate`; merge, irreversible, and protected-branch decisions stay human-only (park + ticket on hit). Any other policy value or none → behavior identical to today.

**Stop-point forecast**: if this run **starts** with a frozen contract (queue child with problem + frozen decisions, or independent thin freeze already written), open with a forecast before analysis — every manual exit × covered-by-frozen-decisions vs will-form-a-new-ticket. If overlay is requested **mid-run**, after thin freeze output a forecast of **remaining** exits, then continue the current stage (do not restart from analysis).

---

## Stage 1: Clarify the Problem

> ⚠️ Edit/Write are forbidden in this stage. Only output your understanding of the problem — do not modify any file.

> Principle: clarify the problem before technical analysis; this stage only aligns on the problem, it does not touch implementation logic.

> **Domain routing**: if the problem is performance-domain (slow / jank / resource growth), suggest entering `perf-optimize-workflow` — its evidence-gated paradigm fits the domain; its analysis output can flow back into this workflow for fix execution. Note: its campaigns create per-project artifacts (benchmark log + harness, and seeded `code-insight`/`code-optimizer` skills); the optimize-verify loop additionally requires an environment loop runner — analysis stages always run. Informational reference, not a dependency.

> **[🤖 Auto]** Skip this stage and go straight to stage 2, treating the user's input as an already-confirmed problem description.
>
> **[👤 Manual]** This stage must complete and be confirmed by the user before entering stage 2.

1. **Restate the problem** — describe the user's problem in your own words
2. **Extract key elements** — goal, constraints, background, expected outcome
3. **List open questions** — points that need confirmation; **if asking the user, ask exactly ONE most critical question at a time** (see "General Principles" hard discipline), then ask the next only after getting an answer
4. **Scope breakdown** (if applicable) — when the problem spans multiple independent subsystems (e.g. "chat + file storage + billing"), help break it down first: independent modules, dependencies, suggested order — then analyze the first sub-problem. **This step still belongs to stage 1: no proactive code exploration; content the user already referenced may be read**, and the breakdown is based mainly on the user's description.
5. **Wait for user confirmation**

**Tool restrictions**: Read/Grep/SemanticSearch are forbidden, **except**:
- The user's message contains `@file-path` (optionally with line numbers, e.g. `@SKILL.md:83-89`)
- The user pasted a code snippet
- The user explicitly named a "function/class + containing file" combination

When an exception applies: **read only the file and lines the user directly referenced** — do not expand to other files.
Use the read result only to understand the problem — **no technical-analysis conclusions may appear in this stage's output**.

### Output Format

Output format is in [reference.md](reference.md) § Stage 1 — Clarify the Problem.

> ⛔ **[Manual mode — stage 1 exit]** **Stop immediately** after this output and wait for the user to explicitly confirm the understanding is correct before entering stage 2.
> 🤖 **[Auto mode]** Skip stage 1 and start directly from stage 2.

### Red Flags

- Using Read/Grep to explore code before stage 1 completes, when the user has referenced nothing
- Skipping stage 1 because "the user was already clear enough"
- Exploring code before stage 1 completes under the guise of "clarify while analyzing"
- Exploring code before stage 1 completes under the guise of "look at the code first, then confirm"
- Mixing technical-analysis conclusions (root-cause judgment, fix suggestions) into stage 1's "restatement" or "open questions"
- Dumping multiple open questions on the user at once in stage 1 (violates the "Clarifying Questions" hard discipline) — ask exactly one most critical question at a time, then the next after an answer

**Any of the above violates the stage's contract. [👤 Manual] Stage 1 must complete and be confirmed before entering stage 2. [🤖 Auto] Skipping stage 1 is not subject to this restriction.**

---

## Stage 2: Analyze the Problem

> Single source of truth for the methodology: `analysis-core`. This stage leaves no implementation changes behind — fixes belong to stage 6.

### Delegate to `analysis-core`

Load the strong dependency `analysis-core` and run its §§1–3. This workflow's mapping (number + name):

- `{next-stage}` = stage 3 "Explore Solutions"
- `{root-cause step}` = step 5 "Root cause"; `{impact-assessment step}` = step 7 "Impact"; `{upstream-eval step}` = step 6 "Upstream dependency fix evaluation"

Output format per `analysis-core` and `known-issue-research/reference.md`; the output MUST close with the analysis gate output block (`analysis-core` §5) — missing block blocks stage 3. If any temporary change was made, its list + rollback verification rides in the block's temporary-changes line. When the expected outcome is a result the user can see or operate, that same load runs `competitive-research` per `analysis-core`. Do not restate its method.

---

## Stage 3: Explore Solutions

> Principle: based on stage 2's analysis, offer 2–5 solutions; strip non-essential features and over-engineering (YAGNI). If the path is still foggy, follow `decision-fog-discipline` before the solution table.

> **Architecture-boundary precheck** (decision order): when a candidate solution crosses process or layer boundaries, answer the precheck before short-term costs (change size / reuse / single-repo) are weighed — (1) runtime initialization location: which process/layer initializes the called capability; (2) boundary legality: would a cross-layer import pull the callee's dependency tree into the caller's bundle graph (bundler static pre-scanning defeats dynamic `require`/`import` as a workaround); (3) ownership classification: system vs data/product capability vs the calling layer's positioning. The boundary verdict surfaces with the comparison table and gates auto-mode selection. Methodology: `code-design-review` Layer A dependency-direction dimension. Single-layer solutions do not trigger this precheck.

### [🤖 Auto mode] Solution selection

Generate 2–5 solutions automatically; the AI recommends and selects the best one (priority: more thorough fix > best-practice alignment > code-quality improvement > smallest change), then proceeds directly to stage 4.

### [👤 Manual mode] Solution selection

Output the solution comparison table and wait for the user to choose before entering stage 4.

### Output Format

1. **Opening**: solution list (number + name for each)
2. **Middle**: each solution expanded in detail (see "Each solution includes" below)
3. **Closing**: solution comparison table (appears exactly once, right at the decision point)

| Solution | Description | Pros | Cons | Complexity | Recommendation |
|------|------|------|------|--------|--------|
| Solution 1 | ... | ... | ... | Low/Med/High | ⭐⭐⭐⭐⭐ |
| Solution 2 | ... | ... | ... | Low/Med/High | ⭐⭐⭐ |

### Each solution includes

- Core idea (1–2 sentences)
- Files/modules to change
- Implementation difficulty, potential risks, applicable scenarios

**Tool restrictions**: Edit/Write are forbidden; Read is allowed to inspect code details

> ⛔ **[Manual mode — stage 3 exit]** **Stop immediately** after the comparison table and wait for the user to pick a solution number before entering stage 4.
> 🤖 **[Auto mode]** Auto-select the best solution and proceed directly to stage 4.

### Red Flags

- Producing only 1 solution and skipping the comparison because "the direction is already clear"
- **[👤 Manual]** Advancing to review before the user has chosen a solution

---

## Stage 4: Review the Solution

Load `staged-review-flow` and run its full review contract. This workflow's mapping: `{next-stage}` = stage 5 "Make a Plan"; `{artifact-sink}` = the stage 4 review report (format in [reference.md](reference.md)); `{extra-dimensions}` = none; `{batch-overcap-behavior}` = `N/A`. Tool restrictions: Edit/Write forbidden; Read allowed to inspect code details.

---

## Stage 5: Make a Plan

> Principle: a detailed, executable modification plan — output plan text only, do not execute any code change.

1. **Target solution recap** — the core idea of the reviewed, confirmed solution
2. **File change list** — file path, location, and specific change description
3. **Change order** — execution order accounting for dependencies

### Output Format

Output format is in [reference.md](reference.md) § Stage 5 — Make a Plan.

**Tool restrictions**: Edit/Write/Bash are forbidden; Read is allowed to confirm details

> ⛔ **[Manual mode — stage 5 exit]** **Stop immediately** after the plan and wait for the user to confirm it before entering stage 6.
> 🤖 **[Auto mode]** Auto-confirm and proceed directly to stage 6.

### Update the plan (sub-stage)

When the user says "更新计划" / "修订计划" / "修改计划" (update/revise/modify the plan), run this stage again, additionally noting the **change comparison** and **reason for change**.

---

## Stage 6: Execute the Plan

> Principle: execute strictly per the plan, confirm on completion. Before production edits, follow `design-approval-gate` (manual: user pass; auto/lean: named escape + 留痕). Before the first non-trivial write (docs or code), load `git-worktree-discipline` (worktree gate + optional isolation).

**Context budget**: evaluate the phase-boundary reset and the compaction threshold per `context-budget-discipline` (ledger path from the stage-5 plan); any reset requires a complete ledger entry first.

**Figma pixel fidelity:** Load `figma-pixel-implement` and follow it when the goal, card, issue, or plan text contains `figma.com` or `node-id=`, or when the user asks for pixel restore (像素级还原). That substring is the scope fact. Keep those rows hard; do not place them under soft or human because the task also checks behavior. A probe of visible text, a visibility flag, or a list length does not pass the pixel rows. When that same text also contains `参考`, `match the existing`, or `same as`, pass that fact into verify so the named control's interaction states become rows. Implement is incomplete without a durable inventory+spec path in the target repo. That skill continues into `figma-pixel-verify` in the same run until overall PASS or the measurement command cannot run. Do not restate its methodology here.

### Execution flow

1. Modify files in the plan's order
2. State what was completed after each change
3. If stage 5's plan used checkbox format (`- [ ]` / `- [x]`), **flip the corresponding `[ ]` to `[x]` immediately after finishing each item** — do not batch the updates until the end
4. Output an execution report once everything is done
5. **Auto-advance to stage 7**: when execution goes smoothly with no blockers, enter stage 7 immediately after the report; if a problem or decision arises, confirm with the user first

### Execution report

- List of modified files, key changes
- Suggested test steps
- Any deviation from the plan (with reason, if applicable)
- Verification checklist (for stage 7 to use)

### Test-first then test-suite ensure (before the execution report)

For behavior-changing work, follow `test-first-discipline` (failing test observed before production code). Separately, for changes touching business logic that lack test coverage, load and call `test-suite-ensure` with `mode=advisory`, scoped to this change's logic files. If the user declines scaffolding, note it in the execution report as a non-blocking reminder. test-suite-ensure does not satisfy test-first.

**Tool permissions**: ✅ Edit/Write/Bash allowed; use TodoWrite to track progress

---

## Stage 7: Verify (Check)

> Principle: output only the verification results — improvement suggestions belong to stage 8.

**Context budget**: if the run crossed the compaction threshold or restarted from a ledger, verify against the ledger + artifacts — never by replaying prior-session history (per `context-budget-discipline`).

1. **Goal achievement** — whether stage 1's expected outcome was met
2. **Comparison with the plan** — compare against stage 5's plan
3. **Verification and tests** — may cite stage 6's execution report; **run tests if anything test-related applies**
4. **Side-effect verification** — check whether the change introduced new problems or unexpected behavior changes elsewhere (functional side effects), and any unexpected performance/security/maintainability impact (non-functional side effects)
5. **Logic and process review** — check for gaps or omissions
6. **Debug-verify loop** — if stage 2 used a debug skill to locate the root cause, verify the fix with **that same skill** per `analysis-core` §4 (not tests alone)
7. **Figma pixel verify** — when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or this run implemented from Figma, load `figma-pixel-verify` and follow it; a missing measured report (the living artifact’s Verify section, or the Spec source sibling) blocks this verification stage from passing. A spec-gap FAIL does not pass verification—re-enter `figma-pixel-implement` to complete the table. Also load verify when the user/plan requires alignment checking without a same-run implement. This stage passes only when that report’s overall status is PASS (accepted residuals included) and its channel is a laid-out measurement (`storybook`, `isolated-harness`, `preview`, `full-app`, or `layout-probe`). Any other result fails this stage and returns to the implement stage for another fix/re-measure loop. This stage also runs `scripts/check-figma-verify-report.mjs` from the `figma-pixel-verify` skill on that report; a non-zero exit fails the stage. Do not restate its methodology.

### Running tests

If stage 5's plan or stage 6's execution report involves testing (unit tests, integration tests, manual verification steps):

> For Node / JavaScript / TypeScript projects, invoke `node-version-discipline` to align the Node version before running tests.

**Verification execution follows `runtime-verification-discipline`** (strong dependency): the AI executes verification itself in an environment, and hands a step to the user only at a classified true hard boundary, with the reason stated.

- **AI can execute**: run the test command via Bash (e.g. `npm test`, `pytest`, `go test`) and fold the result into the verification conclusion
- **Otherwise**: classify the blocker per `runtime-verification-discipline`; only a true hard boundary becomes a user step, stated with its reason.

### Verification-report honesty

Follow `staged-review-flow`'s verification-report honesty rule and `completion-evidence-discipline` (fresh current-turn evidence before pass claims) to label each result.

When this turn's dispatch inlines a frozen task card, the verification report includes the problem, the cause, and the completed fix, and an evidence list. Each evidence item is an opened-UI check citing a png, jpg, jpeg, or webp path, or a non-UI check citing the command and a short output summary. A missing or empty image is pending and states the capture still required. Do not invent an image. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. This run does not write the HTML page and does not write the evidence HTML.

### Output Format

Output format is in [reference.md](reference.md) § Stage 7 — Verification Results.

**Tool restrictions**: Edit/Write forbidden; ✅ Bash allowed to run test commands

> ⛔ **[Stage 7 exit]** **Stop immediately** after the verification results and wait for the user to confirm before entering stage 8 (or decide, based on the conclusion, whether another fix cycle is needed).

---

## Stage 8: Retrospective (Act)

> After verify: optional code delivery → branch closeout → retrospective. Load `delivery-discipline` when this run may need commit + PR/MR (not every run — that skill's need-delivery gate may skip). Then load `feature-branch-closeout` for the menu (PR / merge / keep / continue; merge loads `merge-discipline`). Then load `learn-and-improve` for retrospective and knowledge sediment. Do not write rule/skill files by default; only proceed to "make a plan → execute the plan" when the user explicitly requests writing or a new cycle.

### Optional delivery (`delivery-discipline`)

Load `delivery-discipline` and follow it. Pass `{pr-body-extra}` / `{commit-context}` when useful. If the gate skips delivery, continue to closeout (user may still choose open PR via the menu, which re-enters `delivery-discipline`).

### Branch closeout (`feature-branch-closeout`)

Load `feature-branch-closeout` for the closeout menu. Choosing keep/continue does not trigger merge discipline.

### Delegate to `learn-and-improve` (retrospective)

Load `learn-and-improve` and run its framework; the full methodology lives in that skill.

### solve-workflow-specific orchestration

- **Next step when the goal isn't met**: if `learn-and-improve`'s improvement loop concludes the goal wasn't achieved, decide whether to loop back to "分析问题" / "探索方案" / "审查方案" for another PDCA cycle.
- **Wrap-up and optional summary doc**: after the improvement suggestions, proactively ask "是否需要生成总结文档？" (want a summary doc?). If yes, generate one (path chosen by the user or suggested by the AI) covering: problem restatement, solution choice, execution result, open items and improvements.

### Output Format

Output format is in [reference.md](reference.md) § Stage 8 — Improvement Suggestions.

After the output, proactively ask: "是否需要生成总结文档？" / "Do you want a summary document?"

### Pre-merge coverage reminder (conditional, non-gating)

> ⚠️ solve-workflow **does not own protected-branch merge** as a mandatory stage step — merge only happens if closeout selects merge (via `merge-discipline`). Optional commit/PR is owned by `delivery-discipline`. The coverage reminder is **advisory, not a mandatory gate** — it does not run a script, does not block the flow, and is not a capability-discovery table entry. Full trigger conditions and reminder text are in [reference.md](reference.md) § Stage 8 — Pre-Merge Coverage Reminder (Non-Gating).

**Boundary with mandatory gates**: solve-workflow only suggests "run this before merging" — it never runs the coverage script or judges pass/fail on its own. The mandatory coverage gate belongs to `merge-discipline` Part C when merge is selected (also used by `jira-fix-workflow` / the `opsx-*` family).

**Tool restrictions**: Edit/Write forbidden except when executing `delivery-discipline` / closeout git operations the user confirmed; do not write rule/skill files unless the user explicitly asks to "write to rules" / "create a skill" / "update docs", or a new cycle begins.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|------|------|------|
| Continuing analysis after the existence check concludes "doesn't exist / description mismatch" | Wrong direction from the start | Stop immediately, report, wait for user confirmation |
| Stage 8 writes to rule files or creates a skill by default | Pollutes long-term rules; breaks the summarize-only boundary | Stage 8 only outputs sediment suggestions; only proceed to "make a plan → execute the plan" after the user explicitly asks |
| Stage 8 treats the coverage reminder as a mandatory gate (runs a script / blocks the flow) | Coverage preference belongs to merge-discipline Part C when merge is selected | The reminder is advisory only: print the text, never run `test-coverage-analyzer` from solve alone; never block |

---
