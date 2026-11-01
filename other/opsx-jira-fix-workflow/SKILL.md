---
name: opsx-jira-fix-workflow
version: "1.26.0"
user-invocable: true
description: "OpenSpec-flavored end-to-end Jira bug-fix workflow that persists root cause, behavior change, fix plan, verification, and archive into OpenSpec artifacts (openspec/changes/<name>/, archived into openspec/specs/) instead of leaving them only in chat context or Jira comments. Use when a Jira issue needs long-term behavioral-contract traceability, team review, or auditability. Do NOT use for a quick fix needing no traceability — use jira-fix-workflow instead. Triggers：「opsx-jira-fix」「OpenSpec Jira 修复」「规范化修复 Jira」「opsx修复Jira」「Jira OpenSpec 修复」「opsx自动修复Jira」「用OpenSpec修复Jira」「opsx-jira-fix-workflow」；「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / opsx jira fix, OpenSpec Jira fix workflow, ai-proxy mode, switch to ai-proxy."
dependencies:
  - solution-review
  - code-design-review
  - hybrid-debug
  - runtime-evidence-debug
  - browser-debug-toolkit
  - node-version-discipline
  - workflow-mode-lifecycle
  - clarifying-question-discipline
  - known-issue-research
  - competitive-research
  - analysis-core
  - test-suite-ensure
  - merge-discipline
  - staged-review-flow
  - opsx-workspace-gate
  - jira-status-writeback
  - jira-wiki-markup
  - ai-proxy-discipline
  - completion-evidence-discipline
  - domain-language-discipline
  - test-first-discipline
  - design-approval-gate
  - delivery-discipline
  - feature-branch-closeout
  - decision-fog-discipline
  - git-worktree-discipline
  - learn-and-improve
  - figma-pixel-implement
  - figma-pixel-verify
  - runtime-verification-discipline
  - context-budget-discipline
---

# OPSX Jira Bug-Fix Workflow

> The OpenSpec-flavored version of Jira fixing: keeps `jira-fix-workflow`'s end-to-end fix capability while making OpenSpec the source of behavioral truth.
>
> **Output templates**: see [reference.md](reference.md) for each stage's format.

## Positioning

Use this skill for Jira bug fixes **worth persisting**: not just fixing the code, but also recording root cause, behavior changes, design trade-offs, task lists, verification evidence, and archive results.

Division of labor:

- **Jira**: problem source, business context, status transitions, and fix comments.
- **`openspec/changes/<change-name>/`**: Jira context, root cause, behavioral contract, solution, tasks, verification, and the final archive.
- **PR/MR**: code delivery, verification evidence, risk notes, and the review entry point.

Not a replacement for plain `jira-fix-workflow`:

- Quick fixes with no long-term traceability need — use `jira-fix-workflow`.
- Behavioral contracts, audits, team collaboration, cross-module impact, or long-term traceability — use this skill.

## Invocation conventions

- **Triggers**: opsx-jira-fix, OpenSpec Jira 修复, 规范化修复 Jira, opsx修复Jira, Jira OpenSpec 修复, opsx自动修复Jira, 用OpenSpec修复Jira, opsx-jira-fix-workflow; ai-proxy 模式, AI 代理模式, 切换 ai-proxy
- **Overlay**: 「ai-proxy 模式」「AI 代理模式」「切换 ai-proxy」 / "ai-proxy mode" / "switch to ai-proxy" request overlay per `workflow-mode-lifecycle` (overlay+freeze wins if an auto trigger is also present). Thin freeze then occupy per `ai-proxy-discipline`.
- **Auto mode**: else a trigger containing "自动" or `--auto` enters auto mode.
- **Force mode**: a trigger containing "强制" or `--force` may skip the difficulty-based stop, but never skips verification or archive checks.
- **Continue fixing**: a trigger containing "继续修复", "再次修复", "从上次继续", or `--retry` first locates the existing OpenSpec change, then recovers context from `design.md`, `tasks.md` checkboxes, the current Git branch, and PR/MR status.

**Strong-dependency skills** (frontmatter `dependencies`; must pass the "Prerequisite skill check" at startup — abort if any is missing):
- `staged-review-flow` (stage 4 review orchestration; depends on `solution-review` and `code-design-review`)
- `hybrid-debug` / `runtime-evidence-debug` / `browser-debug-toolkit` (delegated via `analysis-core`; stage 2 + stage 7)
- `analysis-core` (single source for stage-2 analysis methodology: temporary-change gate / instrumentation debug with runtime-evidence-debug as default entry / analysis step skeleton / analysis gate output block / debug-verify loop)
- `node-version-discipline` (Node version alignment before stage 6 execution verification)
- `workflow-mode-lifecycle` (auto/manual mode lifecycle), `clarifying-question-discipline` (hard active-questioning discipline and investigation-first), `known-issue-research` (stage 2 research routing / known-issue quick search / industry-wide evaluation), `competitive-research` (user-visible competitor behavior during analysis; method stays in that skill)
- `test-suite-ensure` (stage 6.2.5 test-suite ensure: complete and run tests when infra exists; scaffold with user confirmation when it doesn't)
- `test-first-discipline` (execution: failing-test-first for behavior changes; distinct from test-suite-ensure)
- `design-approval-gate` (before execution: no production impl without approval; named auto/hotfix escapes)
- `delivery-discipline` (stage 8: commit + open/update PR/MR after archive; field map via placeholders)
- `feature-branch-closeout` (stage 8: closeout menu; merge delegates to merge-discipline)
- `decision-fog-discipline` (before explore solutions: graduate fog / decision tickets first)
- `git-worktree-discipline` (before stage 1 — first artifact write: worktree gate + optional isolated workspace)
- `domain-language-discipline` (clarify/analyze: project glossary / CONTEXT.md when domain terms matter)
- `merge-discipline` (stage 8 merge discipline — after closeout selects merge)
- `opsx-workspace-gate` (stage 0 OpenSpec workspace and native-skill gate)
- `jira-status-writeback` (stage 8 post-merge writeback: status transition + fix-comment SOP, single source)
- `jira-wiki-markup` (Wiki markup for every Jira comment body; writeback loads it for the repair comment)
- `learn-and-improve` (stage 8 retrospective and knowledge sediment)
- `figma-pixel-implement` / `figma-pixel-verify` (Figma export-faithful implement + measured verify; required installed; invoke when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or the user asks for pixel restore)

## Prerequisite skill check

> At startup (before stage 0's prerequisite check), check frontmatter `dependencies`: any missing → print a structured prompt and **abort immediately** (format: `solve-workflow/reference.md`).

> **No-degradation principle**: a missing strong dependency means abort — never fall back to a simplified review or debug flow.

## Mode lifecycle

> Entry, persistence, and exit rules for auto mode, preventing mode stickiness where the user is unaware the AI is still making automatic decisions. The core rules (revert-to-manual / explicit re-entry / implicit continuation never re-activates / batch scenarios) live in the strong-dependency skill `workflow-mode-lifecycle` (already guaranteed available by the prerequisite check) — not restated here. This workflow's "full-flow completion" = a normal run through stages 0-8 (closing out at stage 8's archive); a failed termination, user-initiated stop, or a review-cap pause all count as flow interruptions and revert to manual.

### OpenSpec-specific notes

- After stage 8 archiving completes, mode auto-reverts to manual.
- `--retry` (continue fixing): resets to manual mode.
- `--resume` (checkpoint recovery): keeps the mode from the checkpoint.
- An OpenSpec archive failure counts as a flow interruption — revert to manual.

## Unattended proxy exits

When this-run contract or task card records **`Stage-exit policy: ai-proxy`** (auto carrier; queue child is sufficient but not required), each manual stop point becomes a proxy checkpoint per `ai-proxy-discipline`. Thin freeze (verbal trigger ≠ occupancy) lives there. Merge, irreversible, protected-branch, and Jira writeback stay human-only (park + ticket). Any other policy value or none → today's non-proxy behavior.

**Stop-point forecast**: if this run **starts** with a frozen contract (queue child with problem + frozen decisions, or independent thin freeze already written), open with a forecast table before analysis — every manual exit × covered-by-frozen-decisions vs will-form-a-new-ticket. If overlay is requested **mid-run**, after thin freeze output a forecast of **remaining** exits, then continue the current stage (do not restart from analysis).

## Queue-child mode (goal-driven-queue dispatch)

When dispatched by `goal-driven-queue` (explicit `queue-child` context flag in the invocation — never guessed from ambient signals), this flow adapts: the card's goal condition carries the Jira issue link; its frozen-decisions block supplies stage 0–1; `Stage-exit policy` rides along (occupancy per `ai-proxy-discipline` when policy is ai-proxy — queue child is sufficient but not required); open with a stop-point forecast (every manual exit × covered-by-frozen-decisions vs will-form-a-new-ticket). The terminal is **archive + PR-open**: archive the OpenSpec change (native to this model, never deferred), then stop at PR open — merge + Jira writeback are deferred to the human (merge authority and external-tracker writebacks are never proxied); the queue's acceptance package carries them as pending follow-ups. Independent use (no flag): overlay/occupancy still follow `Stage-exit policy`; the **archive+PR-open** queue terminal does **not** apply; closeout stays this skill's native archive-then-stage path (overlay is not naked auto through merge/writeback). When the card supply includes queue relationship-pass notes, write them as `## Related Issues` in this change's `design.md`. When this run is a queue child, the completion report includes the problem, the cause, and the completed fix, and an evidence list. Each evidence item is an opened-UI check citing a png, jpg, jpeg, or webp path, or a non-UI check citing the command and a short output summary. A missing or empty image is pending and states the capture still required. Do not invent an image. Before an opened-UI image supports the check, inspect it per `completion-evidence-discipline`. This run does not write the HTML page and does not write the evidence HTML.

## Stage 0: Prerequisite check

Any key check failing pauses the flow — do not enter the fix:

1. Parse the Jira URL / Jira ID; detect mode (manual / auto / force / retry / overlay). Overlay triggers request thin freeze then occupancy per `ai-proxy-discipline`.
2. Check Jira data is readable: prefer `jira-read {JIRA-ID} --live` or mcp-atlassian; fall back to local cache; abort if both fail.
3. Check Git status: auto mode may stash; manual mode prompts the user to handle it.
4. **OpenSpec workspace and native-skill gate**: load `opsx-workspace-gate` and run its project-root location, `openspec/` check, and exact native-OPSX-skill gate; continue this workflow once it passes.
5. Check OpenSpec commands (run from the project root): prefer `openspec list`, `openspec status`, `openspec validate`.
6. When continuing a fix, locate the OpenSpec change first: prefer inferring it from the current branch name; then search `openspec/changes/*/{proposal.md,design.md,tasks.md}` for the Jira ID; then check the PR/MR description for an OpenSpec change path; if still not uniquely determined, ask the user exactly 1 question to confirm the change name. Once located, recover progress from `openspec status --change <name>`, `openspec show <change-name>`, `design.md`, `tasks.md` checkboxes, and the current Git branch.

## OpenSpec record model

This skill creates no extra runtime directory. A single Jira bug-fix cycle should stay short and clear; engineering records all land in OpenSpec artifacts:

| Directory | Purpose | Long-term source of truth |
|------|------|----------------|
| Jira issue | Problem source, comments, status transitions | No — external process source |
| `openspec/changes/<change-name>/` | proposal, delta specs, design, tasks, pre-archive change facts | Yes — merged into `openspec/specs/` after archiving |
| PR/MR | Delivery notes, verification evidence, risk & rollback | No — delivery communication carrier |

Never create an extra local runtime directory for an OPSX Jira fix. To continue a fix, recover state from the OpenSpec change, `tasks.md` checkboxes, the Git branch, and PR/MR status.

### Stage tool-constraint table

| Stage | ✅ Allowed | ❌ Forbidden |
|------|---------|---------|
| 0 Prerequisite check | Read, Grep, Glob, Bash (read-only checks), Jira API (read-only) | Edit, Write, Git write operations |
| 1 Read Jira | Jira API, jira-read, Read, OPSX skills (create change), Bash (worktree gate) | Edit/Write business code; Bash that changes the implementation |
| 2 Analyze the problem | Read, Grep, WebSearch; analysis-assist Edit/Write per `analysis-core` §1 (must be registered for rollback) | Business-code changes made to implement the fix |
| 3 Create the change | Native OPSX skills, Write (artifacts) | Edit business code |
| 4 Explore solutions | Read, Grep | Edit/Write business code |
| 5 Make the plan | Read, Write (`tasks.md` only) | Edit business code |
| 6 Execute & verify | Everything (Edit, Write, Bash, Git, tests); before running build/lint/tsc/test, align to the project's declared Node version per `node-version-discipline` (probe chain in that skill's SOP) | Skipping verification; skipping checkbox updates |
| 7 Check verification | Read, Bash (test commands only), OPSX skills (`openspec-verify-change`) | Edit/Write business code |
| 8 Submit & close out | Git, Jira API, OPSX skills, Bash (plus the `test-coverage-analyzer` script if Part C decides to run coverage) | Skipping archive; skipping the Jira writeback |

### Mode-difference quick table

| Stage | Manual mode | Auto mode |
|------|---------|---------|
| 0 Prerequisite check | Git not clean → prompt the user | Git not clean → auto-stash |
| 1 Read Jira | Output a candidate change name, wait for confirmation | Auto-create a draft change |
| 2 Analyze the problem | Same as auto mode | Same as manual mode |
| 3 Create the change | Create after the user confirms the name | Auto-generate and create |
| 4 Explore solutions | Output the solution table and pause for the user's pick | Auto-pick the best solution |
| 5 Make the plan | Output the plan and pause for confirmation | Normal: auto-advance to stage 6; difficult/very-difficult: pause |
| 6 Execute & verify | Same as auto mode | Same as manual mode |
| 7 Check verification | Output results and pause for confirmation | Auto-judge pass/fail; on fail, auto-retry (max 2 rounds, then pause) |
| 8 Submit & close out | Same as auto mode | Same as manual mode |

## Stage 1: Read Jira

Before the first artifact write (`design.md` Jira context), load `git-worktree-discipline` (worktree gate + optional isolation).

Read the latest Jira data and write it into OpenSpec artifacts as early as possible — never leave it only in chat context.

- Jira ID, title, priority, status
- Description, repro steps, expected result, actual result
- Attachments, comments, historical context
- Data source (live / cache / user-provided)

Once stage 1 completes, an OpenSpec change must be determined or created:

- Auto mode: create a draft change per stage 3's naming rule, and write the Jira context into `design.md`.
- Manual mode: output a candidate change name and wait for confirmation; do not enter deep analysis before confirmation.
- Continue fixing: reuse the existing change located in stage 0, and merge the latest Jira context into `design.md`.

Tool limits: Jira API / jira-read allowed; Edit/Write of business code forbidden; Bash commands that change the implementation forbidden.

Auto-advance to stage 2 on completion.

> ⚠️ Active questioning: follow `clarifying-question-discipline` (one question per round, multi-round until clear; clarify first, don't rush to answer). When domain vocabulary is in play, also follow `domain-language-discipline`.
>
> 🚩 **Red Flag**: dumping several ambiguous points on the user in one message (violates the hard discipline, see `clarifying-question-discipline`) — ask only the single most critical question each time, then ask the next only after getting an answer.

### Scope breakdown (optional, when multiple subsystems are involved)

If the Jira issue spans 2+ subsystems or modules (e.g. frontend + backend + database), break it down before entering stage 2:

1. List the subsystems / modules involved.
2. For each, note: does it have an independent root cause; does it need an independent change; does it depend on the main change.
3. Strongly dependent subsystems → merge into one change; independent subsystems → consider splitting into multiple changes, each running its own fix flow.

Write the breakdown conclusion into `design.md`'s Scope section.

## Stage 2: Analyze the problem

> Single source for analysis methodology: `analysis-core`. Fix implementation belongs to the execution stage.

### Delegate to `analysis-core`

Load the strong dependency `analysis-core` and execute its §§1-3. This workflow's mapping (number + name):

- `{next-stage}` = Stage 3 "Create the OpenSpec change"
- `{root-cause step}` = step 5; `{impact-assessment step}` = step 7; `{upstream-eval step}` = step 6

The stage output MUST close with the analysis gate output block (`analysis-core` §5 — red loop / debug entry / scenario supplements / temporary changes); a missing block blocks entry to Stage 3. When the expected outcome is a result the user can see or operate, that same load runs `competitive-research` per `analysis-core`. Do not restate its method.

### This workflow's orchestration (kept)

On top of the `analysis-core` skeleton, this stage also completes:

- **Difficulty grading** (easy / medium / hard / very hard) and **path selection** (lean / incremental / full); upgrade the path if scope expands
- **Artifact landing spot**: write into `design.md`'s Problem Analysis / Root Cause / Impact (a change must already exist — otherwise go back to stage 1)
- **Existence ❌ / description mismatch**: pause; get user confirmation before writing a Jira comment (load `jira-wiki-markup`)

Grading and path table:

| Level | Trigger | Behavior |
|------|----------|------|
| Easy | ≤3 files, root cause clear | May use the lean path |
| Medium | 4-10 files, root cause mostly clear | Use the incremental path |
| Hard | Higher risk or broad impact | Pause for review after stage 5 |
| Very hard | Unknown root cause, architecture change, data migration, API contract change, cross-repo | Auto mode aborts; manual mode requires a second confirmation |

| Difficulty | Path | Requirement |
|------|------|------|
| Easy | Lean | proposal/delta specs may be lean, but verification is never skipped |
| Medium | Incremental | Full proposal/specs/design/tasks |
| Hard/very hard | Full | Run stages 1-8 in full |

> 🚩 **Red Flags**: skipped existence check; too-shallow root cause; conclusion not written into `design.md`; ambiguity present but instrumentation not triggered (`analysis-core` §3); path not upgraded; violates `analysis-core` / `known-issue-research` gates

---

## Stage 3: Create the OpenSpec change

🔌 **OPSX skills invocation discipline**: before delegating to any native OPSX skill in this or later stages, read that skill's SKILL.md first — never call from memory.

Confirm or create the Jira issue's OpenSpec change. If stage 1 already created or reused a change, this stage only validates and completes the artifacts; manual mode must confirm the change name first; auto mode may generate and continue.

- **Naming**: `fix-<jira-id-lower>-<short-topic>` (e.g. `fix-proj-12167-ai-summary-button`)
- **Creation**: delegate to `openspec-new-change` (read its SKILL.md; `/opsx:new` is an entry alias)
- **Jira completeness**: `design.md` must include at least Jira Context / Root Cause / Options / Risk / Verification Notes; proposal / delta-spec field details are in [reference.md](reference.md)「Stage 3 Artifact Field Checklist」

## Stage 4: Explore & review solutions

If the path is still foggy, follow `decision-fog-discipline` before the solution table / proposal. Based on stage 2's root cause and stage 3's artifacts, output 2-3 solutions:

- Core idea
- Files / modules involved
- Coverage of the OpenSpec requirement
- Pros, cons, complexity, risk
- Recommended solution

**YAGNI**: solutions must stay strictly focused on fixing the Jira root cause and covering the delta specs, stripping non-essential features and over-engineering. Any addition beyond the root-cause scope must be explicitly labeled "extra optimization" with a stated reason for taking on the risk.

> **Architecture-boundary precheck** (decision order): when a candidate solution crosses process or layer boundaries, answer the precheck before short-term costs (change size / reuse / single-repo) are weighed — (1) runtime initialization location: which process/layer initializes the called capability; (2) boundary legality: would a cross-layer import pull the callee's dependency tree into the caller's bundle graph (bundler static pre-scanning defeats dynamic `require`/`import` as a workaround); (3) ownership classification: system vs data/product capability vs the calling layer's positioning. The boundary verdict surfaces with the comparison table and gates auto-mode selection. Methodology: `code-design-review` Layer A dependency-direction dimension. Single-layer solutions do not trigger this precheck.

In manual mode, output the solution table and pause for the user's pick; auto mode picks the best solution automatically.

Load `staged-review-flow` and execute its full review contract. This workflow's mapping: `{next-stage}` = Stage 5 "Make the plan"; `{artifact-sink}` = `openspec/changes/<change-name>/design.md`; `{extra-dimensions}` = spec coverage (requirements/scenarios) and Jira status boundary (transition only to "fixed"); `{batch-overcap-behavior}` = `N/A`.

> 🚩 **Red Flags (stage 4)**:
> - Review covers only the root cause, without checking spec coverage or side effects
> - Skipping comparison and review just because only 1 solution exists

## Stage 5: Make the plan

Use `openspec/changes/<change-name>/tasks.md` as the single task list.

Task requirements:

- Use checkboxes: `- [ ] 1.1 ...`
- Each item small enough to verify independently.
- Cover every delta-spec requirement and scenario.
- Include necessary test, verification, rollback, OpenSpec archive, and post-merge Jira-writeback steps.
- No `TBD`, `TODO`, "handle appropriately", "similar to above", or other non-actionable descriptions.

In manual mode, output the plan and pause; in auto mode, the normal case auto-advances to stage 6 — difficult or very-difficult cases must pause for confirmation.

> 🚩 **Red Flags (stage 5)**:
> - A task item contains `TBD`, `TODO`, "handle appropriately", "similar to above", or other non-actionable text
> - Tasks don't cover every delta-spec requirement and scenario
> - Missing test, verification, rollback, archive, or post-merge Jira-writeback steps
> - A task's granularity is too large to verify independently

## Stage 6: Execute the fix & verify

Before production edits, follow `design-approval-gate` (manual: user pass; auto/force/lean: named escape + 留痕).

**Context budget**: evaluate the phase-boundary reset and the compaction threshold per `context-budget-discipline` (ledger path from the stage-5 plan / card supply); any reset requires a complete ledger entry first.

### 6.1 Create the fix branch

Branch naming:

```text
fix/jira-fix-<JIRA-ID>
```

A multi-repo scenario needs a branch per repo, listing each repo, branch, and corresponding OpenSpec change in the PR/MR description.

### 6.2 Execute tasks

**Figma pixel fidelity:** Load `figma-pixel-implement` and follow it when the goal, card, issue, or plan text contains `figma.com` or `node-id=`, or when the user asks for pixel restore (像素级还原). That substring is the scope fact. Keep those rows hard; do not place them under soft or human because the task also checks behavior. A probe of visible text, a visibility flag, or a list length does not pass the pixel rows. When that same text also contains `参考`, `match the existing`, or `same as`, pass that fact into verify so the named control's interaction states become rows. Implement is incomplete without a durable inventory+spec path in the target repo. That skill continues into `figma-pixel-verify` in the same run until overall PASS or the measurement command cannot run. Do not restate its methodology here.

Work through `tasks.md` in order:

1. Handle only the current task at a time.
2. Before touching business code, confirm the proposal, specs, design, and tasks already exist.
3. **Update the checkbox immediately after finishing a task**: use StrReplace to flip the corresponding `[ ]` to `[x]` in `tasks.md` — do not batch this until after a group of tasks. Skipping this makes the stage-7 verifier report a CRITICAL false-incomplete.
4. If a spec or design error is found, update that artifact first, then continue implementing.
5. State the reason for any deviation from the plan; if it affects the behavioral contract, return to stage 3 or 4.

Optional tracking comment:

```text
// fix <JIRA-ID>
```

If the project's convention doesn't accept fix comments, don't force it — but list the fix points in the execution report.

### 6.2.5 Test-first then test-suite ensure (mandatory, before entering stage 7)

For behavior-changing work, follow `test-first-discipline` during implementation. Once every `tasks.md` checkbox is checked, before entering stage 7 verification, this step is mandatory:

Load and call `test-suite-ensure`, declaring `mode=mandatory`, scoped to this fix's logic files; a failure or a declined necessary-scaffolding request blocks entry to stage 7. test-suite-ensure does not satisfy test-first.

## Stage 7: Check verification

**Context budget**: verify against the ledger + artifacts when a reset occurred (per `context-budget-discipline`); never replay prior-session history.

Must cover:

1. OpenSpec validation:
   - If the `openspec-verify-change` skill is detected → read its SKILL.md and delegate verification to it.
   - If absent → run `openspec validate <change-name>` or `openspec validate --changes` directly (a CLI tool call, not a degradation).

**Node version alignment (prerequisite)**: call `node-version-discipline` to align to the project's declared Node version before running the verification commands below.

2. Engineering verification: tests, lint, type check, build (under the aligned version)
3. Behavior cross-check: confirm every delta-spec requirement and scenario, one by one
4. Jira cross-check: are the repro steps and expected/actual results closed out
5. Side-effect check: are related modules and platforms affected; the verification report must disclose `Node (declared vX) ✅/⚠️ not aligned`
6. Debug-verify loop: if stage 2 used a debug skill to locate the root cause, verify the fix using that **same** skill per `analysis-core` §4 (not tests alone)
7. Figma pixel verify: when the goal, card, issue, or plan contains `figma.com` or `node-id=`, or this run implemented from Figma, load `figma-pixel-verify` and follow it; a missing measured report (the living artifact’s Verify section, or the Spec source sibling) blocks this verification stage from passing. A spec-gap FAIL does not pass verification—re-enter `figma-pixel-implement` to complete the table. Also load it when alignment checking is required without a same-run implement. This stage passes only when that report’s overall status is PASS (accepted residuals included) and its channel is a laid-out measurement (`storybook`, `isolated-harness`, `preview`, `full-app`, or `layout-probe`). Any other result fails this stage and returns to the implement stage for another fix/re-measure loop. This stage also runs `scripts/check-figma-verify-report.mjs` from the `figma-pixel-verify` skill on that report; a non-zero exit fails the stage.

**Verification execution follows `runtime-verification-discipline`** (strong dependency): the AI executes verification itself in an environment, and a step is listed as a manual-verification item only at a classified true hard boundary, with the reason stated.

> Label each result per `staged-review-flow`'s verification-report honesty rule and `completion-evidence-discipline` (no pass claims without fresh current-turn evidence).

Output format: see [reference.md](reference.md)「Stage 7 Verification Results」.

Do not submit a PR on failed verification. The execution record is `tasks.md` checkboxes, the PR/MR description, and `design.md`'s Verification Notes.

## Stage 8: Archive, submit PR, merge & close out

### 8.1 OpenSpec archive

Pre-archive sync steps:

1. **If delta specs exist**: call the `openspec-sync-specs` skill (if installed) to merge delta specs into the main `specs/<capability>/spec.md`, or let `openspec-archive-change` prompt for and handle the sync during archiving.
2. **Execute the archive**: call the `openspec-archive-change` skill (read its SKILL.md first, then follow its instructions).

If `openspec-archive-change` fails, do **not** manually manipulate the `openspec/` directory — stop and tell the user to check the OpenSpec installation.

Before merging or preparing to merge, confirm archiving is complete (consistent with `merge-discipline` Part A):

- When an active OpenSpec change is associated: **must** archive first (sync main specs + move into `openspec/changes/archive/`), confirm the diff, then merge; "archive after merge" is **never** a normal path.
- A PR with no associated change: Part A passes through, archiving not required.

Default: after verification passes, archive first, confirm the `openspec/specs/` update and the `openspec/changes/archive/` move are in the diff, then deliver and close out.

### 8.2 Commit & PR (`delivery-discipline`)

Before delivery, confirm:

- All relevant `tasks.md` checkboxes are complete.
- OpenSpec artifacts, code changes, and necessary verification notes are all in the diff or PR/MR description.
- Verification passed, or manual-verification items are explicitly listed.

Load `delivery-discipline` and follow it. Supply:

- `{commit-context}`: prefer `fix(<scope>): <JIRA-ID> <subject>`
- `{pr-body-extra}`: Jira link, root cause, fix approach, OpenSpec change path, changed-file list, verification evidence, risk & rollback

### 8.3 Branch closeout

Once archiving, delivery, and the diff check are complete, load `feature-branch-closeout` for the menu (PR / merge / keep / continue). Never declare completion while verification hasn't passed or archiving isn't complete.

> **Order constraint**: archive (8.1) → `delivery-discipline` (8.2) → `feature-branch-closeout` (8.3) → on merge, `merge-discipline` (8.3.1) → execute the merge → Jira writeback (8.4). Choosing keep/continue skips both merge discipline and Jira writeback.

#### 8.3.1 Merge discipline (`merge-discipline` skill)

> On merge (from closeout or a direct user merge command), load `merge-discipline` and run Part A → B → C → R → D; the pre-merge checklist is in `merge-discipline/reference.md`. Never implicitly skip.

### 8.4 Jira writeback (after the merge completes)

Once the PR/MR has merged and the code is on the main branch, write back the Jira status to reflect that the fix has landed. Load the strong dependency `jira-status-writeback` and follow its SOP for the status transition and fix comment (`jira-wiki-markup` composes the Wiki `body`). This workflow supplies the following field map:

| `jira-status-writeback` field | Value |
|------|------|
| Fix branch / Commit / PR/MR URL | Fix branch name / merged tip SHA / PR/MR link |
| Root cause | Stage 2 root-cause summary |
| Fix summary | Fix approach |
| Changed files | Changed-file list |
| Verification | Stage 7 verification scenarios |
| Extra | OpenSpec change path, risk, or QA follow-up items |

The closeout record is authoritative via the PR/MR, Jira comment, and OpenSpec archive result.

### 8.5 Retrospective (delegate to `learn-and-improve`)

Once archiving and branch closeout are complete (and Jira writeback when merge ran), load `learn-and-improve` and follow its framework. OpenSpec artifacts archived through the normal flow are not subject to its sediment-value gate. AI engineering knowledge (`AGENTS.md`, rules, skills, etc.) uses that skill's carrier decision tree; writing requires an explicit user request first.

> 🚩 **Red Flags (stage 8)**:
> - Submitting a PR before verification passes
> - Passing the Jira comment through `jira_transition_issue`'s `comment` parameter, or transitioning status beyond authority to "closed" / "verified" (SOP: `jira-status-writeback`)
> - Manually manipulating the `openspec/` directory after an archive failure
> - PR description missing the OpenSpec change path or verification evidence
> - Running the analyzer by default under an `ask` preference without asking the user (see `merge-discipline` Part C)
> - Triggering merge discipline before archive (8.1) completes (order: 8.1 archive → 8.2 `delivery-discipline` → 8.3 branch closeout → 8.3.1 merge discipline → merge → 8.4 Jira writeback)

## Batch OPSX Jira fixes

Use the `opsx-jira-fix-queue` skill (thin shell: parses the Jira list and enqueues into `goal-driven-queue` with `Engine: opsx-jira-fix-workflow`; does not loop this workflow or merge). Relationship judgments the queue already recorded are written here as `## Related Issues` in each change's `design.md`.

## Common mistakes

> Only this skill's non-obvious pitfalls are listed here. Merge/coverage/archive → `merge-discipline`; project-root/`openspec/`/native-skill gates → `opsx-workspace-gate`; Jira-writeback SOP → `jira-status-writeback`; comment Wiki markup → `jira-wiki-markup`. Rules already stated in the stage body are not repeated.

| Mistake | Consequence | Fix |
|------|------|------|
| Creating an extra local runtime directory | A second record system outside OpenSpec | Record everything in OpenSpec artifacts, the PR/MR, and Jira comments |
| Writing only to OpenSpec, never back to Jira | Jira process breaks, QA can't follow up | Load `jira-status-writeback` after the stage-8.4 merge to complete the writeback |
| Restating `jira-status-writeback`'s two-step API detail or status-authority logic in stage 8.4 | Drifts from `jira-status-writeback`, loses the comment or mis-closes the issue | Stage 8.4 passes only the field map; SOP detail is owned by `jira-status-writeback` |
| Taking the OPSX path for a quick fix | Flow becomes too heavy | Use `jira-fix-workflow` when no traceability sediment is needed |
| Executing a batch mechanically off a list | Duplicate fixes, dropped dependencies, or conflicting behavior | Identify issue relationships before/after execution; record them in Related Issues / Risk / Dependencies |
| Creating the proposal right after stage-2 analysis | Why/What are disconnected, the artifact needs a rewrite | Write the proposal in one pass once stage 4 picks a solution |
| `design.md` missing Jira Context / Root Cause / Options / Risk / Verification Notes | Can't retrospect per-issue | These five sections are the Jira×OPSX minimum completeness bar |
| `MODIFIED` writing only a fragment, or a wrong skill short name | Archive loses a requirement / can't find the SKILL.md | Copy the full block then edit; use exact `openspec-*-change` names |

## Minimum success criteria

One complete run: the OpenSpec change has proposal / delta specs / design / tasks via native skills; the PR/MR is created or updated; Jira has a comment and transitioned to "fixed" (if permitted); OpenSpec has been archived (or the PR states the archive strategy and owner); verification evidence is recorded.
