---
name: start-workflow
version: 1.0.0
description: '[Skill Management] Use when starting a detected workflow, initializing workflow state, or activating a workflow sequence.'
---

## Quick Summary

**Goal:** Activate a selected workflow or custom pipeline from its canonical contract with a complete TaskCreate plan.

**Summary:** Accept an explicitly named workflow or a workflow selected by the opt-in runtime route payload, then resolve the exact canonical mode through the shared manifest resolver—including non-empty `preActions.injectContext`—and read every `preActions.readFiles` file (the workflow's own SKILL.md) before creating tasks on every host. Persist the resolver fingerprint and occurrence IDs with the run so resume cannot silently switch modes or sequences.

**Workflow:**

1. **Select** — Use the exact workflow named by the user, or one the route payload matched after the user picks it in the workflow question (Key Rules)
2. **Confirm identity** — Resolve the workflow ID and requested mode/output; when neither source supplies an ID, stop and request the missing workflow identity
3. **Activate** — Resolve the selected mode/output to a complete canonical manifest (`intent`, `outcomeGates`, ordered occurrence IDs with `role`, skill/args, applicability, barriers, fingerprint and context); create ALL TaskCreate items for the selected occurrences; materialize every declared `parallelGroups` group as a wave; mark first `in_progress`
4. **Execute intent-first** — `gate` steps always run; `core` and `optional` steps are recommendations; every deviation is logged (Step Execution Protocol)

**Key Rules:**

- **MUST ATTENTION resolve host-native execution first.** Skill execution means loading the skill and performing its protocol through the active host, not requiring a tool from another host. Canonical `.claude/**` reads establish source ownership, not the session's runtime; use registered Codex skill paths when running on Codex.
- MUST ATTENTION define success criteria before execution and loop until observable verification passes.
- MUST ATTENTION when creating/reviewing specs or tests, name `Business Intent / Invariant Guarded` or the protected business intent/invariant and ensure the test would fail if that intent breaks.

- MUST ATTENTION automatic selection applies only when the runtime route payload is present (a host that delivers none is unsupported). When it is absent, this skill requires an explicit workflow ID.
- **Route mode** — set per person, stated by the route block the hook delivers: `ask` (the default, and the mode when no block was delivered) applies the workflow question below; `auto` starts a self-matched workflow without asking, by its tier (`auto` starts; `confirm` asks the question only when a leaner route would also do; `manual` never starts on its own); `off` (the `CK:RUNTIME-WORKFLOW-ROUTE-OFF` state) activates nothing the user did not explicitly request — when you reach this skill in `off` mode without an explicit request, stop and run the request directly, reporting that workflow routing is off. An explicit request, and a workflow that a skill step, the user's named skill or a running parent workflow requires, run in every mode.
- Explicit `/workflow-*` or `/start-workflow <id>` invocation counts as the user choosing that workflow; execute it directly.
- **Workflow question** (mode `ask`) — asked ONLY when your route is to start a catalog workflow; a direct, single-skill or custom-simple route (a Catalog-fit downgrade included) asks nothing. A catalog workflow you route to yourself, whatever its tier, is NEVER activated before the user answers ONE question: `AskUserQuestion` where available, else the host's own question tool, else plain text followed by a stop until the user answers. Offer three options, the recommended one first with a one-line reason: (a) the full workflow `<id>` with its step count; (b) a slimmer custom route (Custom Pipeline Option) listing its steps and keeping every required gate — root-cause investigation for bugs, tests, review, spec/doc sync on behavior or public-contract change; (c) execute directly, no workflow or skill. Follow the answer without re-asking. The effective tier — the tier its runtime catalog row shows (the entry's `activation`, absent = `auto`, which project config `portability.workflowActivation` may tighten or override; resolver `resolveActivationTier` in `.claude/scripts/lib/workflow-routing-config.cjs`) — only orders the recommendation: `auto` by catalog fit (>80% of unconditional steps do real work → (a), else (b)); `confirm` recommends (a) only when no leaner route would satisfy the request; `manual` never recommends (a) first. An explicit request (a `/workflow-*` or `/start-workflow <id>` call, `$workflow-*` on Codex, the user asking in words, or the user picking (a) in the question) activates any tier with no question. A `/start-workflow <id>` call you issue yourself — including a workflow skill's hand-off after you chose to invoke that skill — is your own selection, never an explicit request. A workflow (or workflow skill) that an explicit skill step, the user's named skill or an already-running parent workflow requires is part of that run, not a self-matched workflow: it neither asks the workflow question nor is skipped by `off`; `off`/`ask` govern only a workflow YOU choose to start for the task.
- **Mid-session: never auto-activate a workflow or ask to start one.** The workflow question applies only to the first task of a session (its first user prompt; compaction or resume does not reset it). Once work is under way (follow-up, correction, next step, or a new ask), do it directly or with the best-fit skill or a lean chain of at most 3 skills; required gates (root-cause investigation for a bug, test, review, spec/doc sync, and any other required quality gate) still run and do not count toward that cap, and continuing a workflow already running is not activating one. An explicit workflow request always runs, mid-session included — a `/workflow-*` or `/start-workflow <id>` call, or the user asking in words to use a workflow; follow it.
- Auto-select a Custom Pipeline when the route matches no catalog workflow (a focused change); declare it, never ask the user to choose. When the route matched a catalog workflow that fails catalog fit (>80% of its unconditional steps do real work = use catalog), take the Custom Pipeline as your route and proceed without a question; if you still choose to start the catalog workflow, its workflow question offers the Custom Pipeline as option (b)
- `workflows.json` `workflows` field is an **OBJECT** — use `workflows[workflowId]`, NEVER `.find()` or `[index]`; resolve `variants[mode]` through `.claude/scripts/lib/workflow-manifest.cjs`
- Create ALL `TaskCreate` items BEFORE marking the first task `in_progress` — batch creation, then execute
- Read the selected manifest's `occurrences` and `parallelGroups` at activation and tag its member tasks as one wave — 1:1 occurrence tasks still stand (a group never collapses members into one task)
- No `parallelGroups` = `sequence` is the order — surface only adjacent read-only steps as a `Candidate wave`, NEVER a wave that contradicts `sequence`
- **Intent-first step contract** — read the manifest's `intent` and `outcomeGates` first. `gate` steps always run. `core` and `optional` steps are recommendations: skip, merge, simplify or reorder one only when the outcome gates stay satisfiable and data dependencies hold. Log every deviation in the run's deviation log; never delete a task. Full rule: Step Execution Protocol (this skill is its single owner)
- When the runtime `## Workflow Catalog` is present, use it for Tier 1. Otherwise use the exact user-supplied workflow ID. Then load and resolve the complete selected canonical entry (Tier 2) before TaskCreate for EVERY standard workflow. `preActions.injectContext` is required execution context, not optional hook output; this rule applies to every host. Never expose the full `workflows.json` to context
- EVERY workflow entry MUST have a non-empty `preActions.injectContext`; a missing or blank value is catalog drift and blocks activation
- If another workflow is active, it auto-switches (ends current, starts new) — no manual cleanup needed

**NOT for:** Manual step execution (follow TaskCreate items), workflow design (use `plan`), catalog management.

**Related:** `/start-workflow <workflowId>` | Catalog: opt-in runtime route payload derived from `.claude/workflows.json`

---

## Custom Pipeline Option

When the prompt doesn't cleanly match a single catalog workflow — or combining steps from multiple workflows serves the request better — the AI auto-selects a **Custom Pipeline** instead of the catalog workflow.

### When to choose

| Condition                                    | Example                                                                              |
| -------------------------------------------- | ------------------------------------------------------------------------------------ |
| No catalog workflow matches well             | "Review hook changes and update skill docs" — spans review + docs                    |
| Best-match has significant unnecessary steps | Focused policy change in one module; `workflow-feature` adds spec, scenario, seed-data and demo steps that would do no real work |
| Prompt combines 2+ workflow domains          | "Audit performance and write integration tests for the slow query"                   |
| User explicitly requests a step sequence     | "Just run investigate, plan, and feature-implement — nothing else"                         |

**Use the catalog workflow** when it is a strong match (>80% of its unconditional steps would do real work for this request). The gate's Signals → Route table is the default; catalog fit may downgrade it to a custom pipeline, trimming only steps that would do no real work. Catalog workflows encode validated best-practice sequences — prefer them.

### How to build

1. **Valid steps only** — Use only canonical step ids — those appearing in a resolved workflow manifest's `occurrences` (legacy `sequence` entries are normalized by the resolver; variant entries are selected by mode). Each maps to a real `.claude/skills/<step>/SKILL.md` and is invoked with the active host's syntax. No invented step names.
2. **Logical order** — Investigate → Plan → Implement → Test. Never reverse dependency order.
3. **Minimal** — Include only steps the prompt needs. No "just in case" additions.
4. **Keep required gates** — A behavior change keeps its test and review steps; a downgraded route also keeps root-cause investigation for bugs and spec/doc sync when behavior or a public contract changes (`investigate --mode=debug` for a bug, `spec`/`docs-manager --mode=update` per the project's spec-test-code cycle reference). A custom pipeline never drops a quality gate the change still requires.
5. **Name it** — Short descriptive name: "Quick Fix + Docs", "Audit + Test Coverage".

### How to declare

Declare the chosen route with its full step list and key signals. When no catalog workflow is your route (none matched, or a Catalog-fit downgrade), activate it immediately — Do NOT use `AskUserQuestion` to choose between routes; the declaration is the user's override point. When your route is to start a catalog workflow, this pipeline is option (b) of the one workflow question (Key Rules → Workflow question), asked before anything starts; never add a second question.

```
Route: custom-simple "Quick Fix + Docs" [investigate → fix → changes-review → test → docs-manager --mode=update] — because known location, one module, no contract change; workflow-bugfix adds spec, integration-test and demo steps this request does not need
```

**Rules:**

- Always show the full step list and one-sentence rationale naming the key signals
- Name the closest catalog workflow in the rationale when you skipped it, so the user can override
- If the user redirects to the catalog workflow (or other steps), re-route and continue — no re-confirmation
- For project-specific architecture, test, documentation, naming, or workflow rules, read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`; keep this reusable start-workflow protocol generic.

### Task creation for Custom Pipeline

Same 1:1 protocol — one `TaskCreate` per step. Use `[Custom]` prefix to distinguish from catalog tasks:

```
TaskCreate: subject="[Custom] {step-name} — {brief description}", description="Custom pipeline step N/{total}.", activeForm="Executing {step-name}"
```

---

## Workflow Lookup — Tier 1 Selection, Tier 2 Execution

Use Tier 1 only when the opt-in runtime catalog is present; an exact user-supplied workflow ID is also sufficient. Use Tier 2 before TaskCreate for EVERY standard workflow to materialize the complete selected-mode execution contract, including ordered `occurrences`, non-empty `preActions.injectContext`, `parallelGroups`, and the resume `fingerprint`.

### Tier 1: Runtime Context or Explicit ID

When automatic routing is enabled, the prompt hook supplies the workflow catalog in runtime context. When it is disabled, the user must name the workflow ID explicitly.

1. Search the available catalog surface for the exact workflow ID: `{workflowId}`.
2. Use its name and `whenToUse` summary only to confirm the route.
3. Do NOT parse the runtime catalog sequence or command syntax for TaskCreate; Tier 1 is route selection only for every standard workflow.

✅ Use Tier 1 for: route selection only.
⚠️ Tier 2 is required immediately after selection and **before TaskCreate for every standard workflow**. The complete canonical entry resolves the requested `--mode`/`--output`, loads ordered `occurrences`, non-empty `preActions.injectContext`, `parallelGroups`, and a `fingerprint`.

### Tier 2: Complete Canonical Entry Read (JSON-aware)

After Tier 1 or an explicit ID identifies a standard workflow, use this selected-entry read before creating tasks. The selected canonical entry remains the execution contract:

```
node .claude/scripts/codex/read-workflow-entry.mjs <workflowId> [--mode <mode> | --output <mode>]
```

This JSON-aware helper resolves the complete selected manifest and prints the parent entry plus `mode`, `fingerprint`, `intent`, `outcomeGates`, `occurrences`, `sequence`, `parallelGroups`, and `stepMeta`. It accepts the exact Tier-1-selected workflow ID and mode as data arguments; it does not interpolate them into a shell command.
Parse: `intent` → the goal the run must achieve; `outcomeGates` → the results `workflow-end` must prove (`[]` when undeclared); the returned `occurrences` array → one stable occurrence ID, `role` (`gate` | `core` | `optional`), skill and opaque args per task; `applicability` → exact run/skip condition and cited skip reason; `parallelGroups` → all-return waves; `fingerprint` → the run/resume identity; and non-empty `preActions.injectContext` → workflow-level execution input. Invoke each skill with the active host's command syntax.

### Tier 3: Missing Entry (stop)

If the JSON-aware lookup cannot return the exact selected entry, stop and report catalog drift or a missing canonical workflow. Do not fall back to a fixed-context grep, and do not expose the full file to context.

---

## After Activation — Task Creation Protocol (ZERO TOLERANCE)

**Active-goal resolution (BEFORE child task creation):** resolve the active Goal Contract per `SYNC:goal-contract-satisfaction-loop` — active plan `goal.md`, else `goals/{YYMMDD-HHmm}-{slug}/goal.md` under the plans root (default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides), else create one from the current user request using `.claude/templates/goal-contract-template.md`. Record the resolved goal path and pass it to every child step/sub-agent so the whole workflow executes against the same saved success criteria. The workflow may end only when the goal's Goal Satisfaction matrix passes or a blocker is escalated.

**Owned-baseline capture (BEFORE child task creation):** create a run-scoped metadata baseline with
`.claude/scripts/lib/workflow-baseline.cjs capture` (or its equivalent API) before any step runs. Capture
the starting HEAD, index identity, tracked/untracked status metadata, selected mode, manifest
fingerprint, goal path, and an explicit empty/approved ownership scope. Do not read or hash repository
content at activation. A nested workflow inherits the parent run ID and may expand ownership only
through an explicit `claim`; it never claims all current dirty files by default. Optional before-images
require an approved regular UTF-8 path and the bounded policy (≤256 KiB/file, ≤2 MiB/run, ≤64 files)
in a user-private OS temp directory; otherwise remain metadata-only.

FIRST action after activation: create EXACTLY one `TaskCreate` for EACH entry in the selected manifest's `occurrences` array. The task subject carries the stable occurrence ID; the task description carries the resolved skill, opaque args, applicability and workflow fingerprint. Persist the run ID, mode, fingerprint and ordered occurrence IDs with the task ledger before marking the first task `in_progress`.

### Reading `workflows.json`

Never read the file directly: Tier 2 (`read-workflow-entry.mjs`) resolves the selected entry and mode. `workflows` is an OBJECT keyed by workflow ID, and `variants[mode]` resolves through `.claude/scripts/lib/workflow-manifest.cjs` (Key Rules).

### Task creation steps

1. **Tier 1 first (no file read):** search the available static catalog surface for `{workflowId}` only to select the route.
2. **Tier 2 required before TaskCreate for every standard workflow:** `node .claude/scripts/codex/read-workflow-entry.mjs <workflowId> [--mode <mode> | --output <mode>]` → treat the complete selected manifest's `occurrences`, non-empty `preActions.injectContext`, `parallelGroups`, `applicability`, and `fingerprint` as canonical. If the static preview differs, stop and report catalog drift rather than choosing one silently.
3. **Read every `preActions.readFiles` file BEFORE TaskCreate** — the workflow's own SKILL.md is listed there and owns its purpose, required gates and triage; `injectContext` is only a digest of it.
4. **Apply selected-workflow pre-actions to task context:** preserve the selected entry's `preActions.injectContext` as workflow-level execution context. For every conditional step it governs, put the exact run condition and evidence-backed skip transition in that task's description; never infer or drop a predicate because the static catalog rendered only a step name.
5. Create one `TaskCreate` per selected manifest occurrence IN ORDER; persist the manifest fingerprint and ordered occurrence IDs in the workflow run record before the first step starts.

**Task format:**

```
TaskCreate: subject="[Workflow] [{role}] {step-name} — {brief description}", description="Workflow step N/{total}. {conditional note}", activeForm="Executing {step-name}"
```

**Rules (NON-NEGOTIABLE):**

- **1:1 mapping** — each selected occurrence entry = exactly one task, even when the skill repeats with different args. No consolidation, no invented tasks. A merge or skip later changes a task's status, never the task list.
- **Role per task** — every subject shows its occurrence `role` (`gate`, `core` or `optional`) so the unskippable steps stay visible.
- **Conditional steps still get tasks** — add the exact canonical run condition and evidence-backed skip transition to the description; a skip then follows the Step Execution Protocol. Never use a generic skip label.
- **Recursive self-calls get tasks** — e.g., `[Workflow] /workflow-review-changes — Recursive re-review (conditional)`
- **Count verification** — after creation: `task count == len(manifest.occurrences)` and the ordered task occurrence IDs exactly equal the manifest IDs. Fix mismatch before proceeding.

### Resume and mode-integrity contract

Persist a small run record before executing the first occurrence:

```json
{
  "workflow": "workflow-id",
  "mode": "selected-mode",
  "fingerprint": "manifest sha256",
  "occurrenceIds": ["stable-id-1", "stable-id-2"],
  "status": "active"
}
```

On resume, resolve the workflow again with the recorded mode/output and compare the new fingerprint
and ordered occurrence IDs before restoring task state. A changed fingerprint, missing occurrence,
or changed order invalidates the prior run and stops activation; never silently resume the old task
list or fall back to the default mode. Record the mismatch and require a fresh activation. A
skipped or merged occurrence is still recorded as `skipped` with its deviation kind and counts
as returned for any barrier.

### Parallel waves from `parallelGroups` (compute at activation, BEFORE the first task runs)

A workflow MAY declare barrier groups in `parallelGroups` (schema: `.claude/workflows.schema.json` → `WorkflowEntry.parallelGroups`; live example: `workflow-review-changes`, groups `initial-reviews` and `reviewers`). Materialize each declared group as a wave IN THE TASK LIST, so the barrier is visible in the tasks and not only in prose.

1. **Read `parallelGroups` alongside `occurrences`.** Tier 1 (the runtime workflow catalog) renders members FLAT and carries no group data. Tier 2's JSON-aware selected-manifest lookup supplies barrier member occurrence IDs with the ordered list.
2. **Expand any barrier token you were given.** The catalog a Codex host receives collapses a group into ONE `[parallel ⇉ all-return barrier: a, b*]` token (`*` = conditional member). That token is a barrier marker, NOT a step — expand it back to its member steps and create one task per member.
3. **Task count is still `len(manifest.occurrences)`.** A group NEVER collapses its members into a single task; it only adds wave metadata to the member tasks.
4. **Tag each member task** — subject `[Workflow] [{role}] [wave: {groupId}] /{step} — {brief description}`, description `Workflow step N/{total}. Parallel group '{groupId}' — spawned together with {other members}; barrier: advance only after ALL members return. {conditional note}`.
5. **Conditional members still get their own task** — add "Conditional — a skipped member still counts as returned for the barrier"; skip via `in_progress` → comment → deviation-log line → `completed`, never delete.
6. **Execute a group as ONE wave** — spawn every member in ONE message, barrier on all returns, then advance to the first step after the group. That next step is a SEQ boundary: never start it — and never start any code-mutating step — while a member is still in flight.
7. **Malformed group → STOP, do not repair.** An occurrence ID absent from the selected manifest, an occurrence in two groups, or `barrier ≠ true` means the workflow definition is broken: report it and run the occurrence list strictly in order rather than guessing the intended grouping.

### When a workflow declares NO `parallelGroups`

`sequence` is the source of truth. Absence of `parallelGroups` is NOT permission to invent groups.

- **NEVER** co-schedule steps in a self-authored wave that contradicts `sequence` — no such wave may run a step ahead of a step that precedes it in `sequence`. Reordering, merging or skipping a `core`/`optional` step is governed only by the Step Execution Protocol (outcome gates, data dependencies, deviation log), never by inferred independence.
- **DO surface a candidate wave** when adjacent steps are obviously independent — ALL of: (a) contiguous in `sequence`, (b) read-only / report-producing (review, scan, investigation, research — each writes only its own `tmp/reports/` file), (c) neither consumes the other's output. Announce it as `Candidate wave (not declared): [...]` and keep the 1:1 tasks unchanged.
- **NEVER** put in a candidate wave: any step that writes source files, any gate awaiting user approval, any step consuming a previous step's output, or any non-adjacent pair. When in doubt → run sequentially; a wrong wave silently reorders the workflow, a missed wave only costs time.
- **Persist what proves right** — if a candidate wave was correct, tell the user to add a `parallelGroups` entry to `.claude/workflows.json` (never edit it mid-run). An undeclared wave must never become the de-facto sequence.

Create ALL tasks first → then `TaskUpdate` first task to `in_progress`.

---

## Step Execution Protocol

This section is the single owner of the flex rules (BR-GWF-16); `workflows.json` supplies their data (`intent`, `outcomeGates`, per-occurrence `role`). Wrappers and hooks carry at most a one-line pointer here, never a copy.

1. **Intent first.** Before the first step, read the manifest's `intent` (the goal) and `outcomeGates` (the results `workflow-end` must prove). Choose steps to reach that intent.
2. **`gate` steps ALWAYS run and are NEVER skipped, merged away, simplified away or reordered** (BR-GWF-01). They execute their skill protocol through the active host in every run. Gate outcomes never flex: changed behaviour is tested and green, the review converged, the spec is synced when behaviour or a public contract changed, a bug has a root-cause trace, and the run closes.
3. **`core` and `optional` steps are recommendations** (BR-GWF-13). Intent first, you may skip, merge, simplify or reorder one when every applicable outcome gate can still be satisfied and the data dependencies hold. An `optional` step whose `applicability.when` is false is skipped with its declared `skipReason`; when it holds, the step flexes like a `core` step. Unannotated steps are `core`.
4. **Data dependencies never flex** (BR-GWF-14): a change is made before it is reviewed and before its tests run; the spec sync runs before the review that checks it; the close runs last; a nested `workflow-review-changes` runs inline. A reorder or merge that breaks one of these is not allowed.
5. **Tests are recommendations of which, never of whether** (BR-GWF-15). The choice of test steps and test cases may flex; every behaviour the run changed is covered by tests that ran green in this run. A skip or merge that would leave changed behaviour untested or failing is not allowed.
6. **Deviation log (the skip log) — every deviation writes one line** to `tmp/workflow-runs/<runId>/skips.md`: `<occurrence-id> · <deviation-kind> · <evidence>` (BR-GWF-08). `runId` is the baseline run id captured at activation (a nested workflow writes to its parent's log); there is no other id format. Deviation kinds (closed set; the reason code): `when-false` (an optional step's `applicability.when` was false; its `skipReason` applies) · `pre-action` (skip pre-authorized by the selected `preActions.injectContext`) · `intent-skip` (a step the intent does not need) · `merged` (folded into another occurrence; the evidence names it) · `simplified` (run in a reduced form; the evidence says how) · `reordered` (run at another position; the evidence names the new neighbour) · `review-report` (written only by `workflow-end`). `evidence` is a short note; never write secrets. With no recorded baseline run, the task comment is the only record — say so at close.
7. **Mechanics.** Run: mark the task `in_progress` → **execute the skill protocol through the active host** → mark the task `completed`. Use native task tools or the documented equivalent ledger. Skip or merge: mark the task `in_progress` → comment "Skipped — {deviation-kind}: {evidence}" → deviation-log line → mark the task `completed`. A skipped or merged task, including a conditionally skipped task, completes without skill execution only after both the comment and the deviation-log line. Simplified and reordered steps still execute their skill protocol and add their line. Never delete a task.
8. **Validation gates** (`/plan --mode=validate`, `/plan --mode=review`, `/why-review`) MUST use explicit evidence and local project protocol — NEVER auto-approve inferred decisions. Explicit user approval in the prompt may satisfy the gate only when the gate's skill permits it.
9. **Close.** `workflow-end` checks evidence for every outcome gate before the run closes.
10. **Verify-last loop** (`SYNC:verify-last-order`). A code-changing workflow reviews statically, then verifies once. When a step after the review edits the tree, re-invoke the review gate with its same args; when that re-review applies a fix, re-invoke the verify gates. A re-invocation reuses the existing task row (comment `rerun N: <reason>`) and is a loop iteration, never a new step or a deviation. The verify ↔ re-review alternation is capped at 3 turns; a fourth turn, or the same failure returning, escalates via `AskUserQuestion`. `workflow-end` checks the review receipt (`review-converged`, a stale one is flagged) and requires the cited green run to be newer than the last source or test edit (`tests-pass`).

---

## Workflow-in-Workflow Gate (HARD GATE)

Some workflow steps ARE themselves full workflows. The DEFAULT for a step that activates a multi-step workflow is sub-agent delegation — running it inline causes the parent session to absorb the entire nested workflow's tool calls, file reads, and sub-agent reports (context overflow on long sequences). The sub-agent runs the nested workflow in isolation and returns ONLY a `SYNC:subagent-return-contract` summary (full findings to `tmp/reports/`).

**Default protocol (sub-agent delegation) for a nested-workflow step:**

1. NEVER execute the nested workflow inline
2. Spawn via `Agent` tool with the appropriate `subagent_type`
3. Agent prompt must include: current git diff context + feature/task description
4. Sub-agent runs the full nested workflow in its isolated context
5. Return ONLY SYNC:subagent-return-contract summary — write full findings to `tmp/reports/`
6. Main agent reads the full `tmp/reports/` file before synthesis, acceptance, deduplication, or repair planning, including every severity and all findings beyond the envelope cap. The bounded envelope limits transport, never report consumption.

**EXCEPTION — `workflow-review-changes` runs INLINE in the main session (never a sub-agent):**

| Step                       | Workflow activated        | Execution mode                  | Why                                                                                          |
| -------------------------- | ------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------- |
| `/workflow-review-changes` | `workflow-review-changes` | **INLINE — main session agent** | Its Step 0 `/goal` gate binds the session Stop hook + its post-fix re-review is inline by design; a sub-agent cannot own the Stop hook, so delegating it silently breaks the unabandonable review→fix→re-review loop. Context stays bounded because its OWN step 2 and steps 3–9 reviewers are sub-agents writing to `tmp/reports/`. |

When `/workflow-review-changes` appears in any workflow sequence (e.g. `workflow-feature`, `workflow-bugfix`, `workflow-refactor`), execute its skill protocol INLINE through the active host — do NOT spawn it as an `Agent` sub-agent.

> The ⚠️ **[WORKFLOW-IN-WORKFLOW GATE]** is model-driven: apply it (default sub-agent, or the `workflow-review-changes` inline exception) yourself whenever the next step activates a nested workflow — no hook emits this warning.

---

**IMPORTANT MANDATORY Steps:** detect-workflow -> analyze-best-match -> select-execution-path -> ask-workflow-question (self-matched workflow only) -> activate-workflow -> create-task-tracking -> execute-sequence

> **[MANDATORY]** `TaskCreate` FIRST — break every workflow into tasks before any action. NEVER skip.
> **[MANDATORY]** In mode `ask`, when your route is to start a catalog workflow, never activate it, whatever its tier, before the user answers the one workflow question (full workflow · slimmer custom route · execute directly); ask no other route question. Mode `auto` follows its route block; mode `off` activates no self-matched workflow. Explicit workflow invocation executes directly in every mode.
> **[MANDATORY]** Host-native skill execution REQUIRED for every step that runs. A step completes without it only when skipped or merged with a deviation-log line; `gate` steps never skip. A foreign-host tool name is not a missing capability.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `incremental-persistence` — Persist results per file or section while the work proceeds; a sub-agent or heavy step processes more than three files → .claude/skills/shared/protocols/incremental-persistence.md
- `session-goal-ledger` — Keep the original goal and every user prompt of the session; running a long or multi-prompt session → .claude/skills/shared/protocols/session-goal-ledger.md
- `subagent-return-contract` — Sub-agents return a structured envelope and a report path, never an inline report; spawning a sub-agent → .claude/skills/shared/protocols/subagent-return-contract.md
- `verify-last-order` — Build all phases and write tests, review statically, then verify once with a mutation check; planning or running any code-changing task → .claude/skills/shared/protocols/verify-last-order.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:goal-contract-satisfaction-loop:reminder -->

- **MANDATORY** Resolve the active Goal Contract BEFORE work (active plan `goal.md` → `<plans root>/goals/{YYMMDD-HHmm}-{slug}/goal.md`, plans root default `plans` and overridable via a `docsRoots.plans.path` entry in `docs/project-config.json` → create from current request) and read saved success criteria before editing.
- **MANDATORY** Append iteration evidence after execution; emit a Goal Satisfaction matrix (PASS/FAIL/BLOCKED) before reporting PASS; loop on validated FAIL; escalate repeated no-progress or blockers. NEVER store secrets in goal files.

<!-- /SYNC:goal-contract-satisfaction-loop:reminder -->


<!-- SYNC:session-goal-ledger:reminder -->

- **MANDATORY** Session goal ledger per the `Task Planning Rules`: pin `Original goal:`, keep `User prompts this session: P1…Pn`, and map the result to every prompt before claiming done; full text: `.claude/skills/shared/protocols/session-goal-ledger.md`.

<!-- /SYNC:session-goal-ledger:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Detect intent, select the direct/skill/workflow/custom route (a self-matched workflow only after the workflow question), then activate the canonical contract with a complete TaskCreate plan.

**IMPORTANT MUST ATTENTION — Main steps (execute in order, NEVER skip/merge):** detect workflow or route → analyze the best match → select direct/skill/standard/custom execution (ask the workflow question only before starting a standard workflow; direct, skill and custom routes ask nothing) → load Tier 1 catalog context and Tier 2 complete canonical selected-mode manifest (`occurrences`, non-empty `preActions.injectContext`, `parallelGroups`, `fingerprint`) → read every `preActions.readFiles` file → create exactly one task per occurrence → materialize declared waves and barriers → execute intent-first: `gate` steps always, `core`/`optional` steps as recommendations, every deviation logged, task status synchronized.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Incremental Persistence:** append findings to report per file; NEVER hold in memory.
- **Sub-Agent Return Contract:** sub-agents return summary only; NEVER inline full output.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**MUST ATTENTION** explicit `/workflow-*` or `/start-workflow <id>` invocation executes directly; a catalog workflow you route to yourself, of ANY tier, waits for the one workflow question (full · slimmer custom route · direct, recommended first); direct, single-skill and custom-simple routes ask nothing. Mid-session, never auto-activate a workflow or ask to start one — do the work directly or with a lean skill chain; required gates still run.
**MUST ATTENTION** create ALL `TaskCreate` items for the full sequence BEFORE marking the first task `in_progress`
**MUST ATTENTION** execute skills through the active host; a source read does not switch hosts and a foreign-host tool name is not a blocker. `gate` steps never skip; a `core`/`optional` step completes without skill execution only when skipped or merged with a deviation-log line (`<occurrence-id> · <deviation-kind> · <evidence>` in `tmp/workflow-runs/<runId>/skips.md`) and the outcome gates still hold; simplified and reordered steps log too — never delete a task — why: an unlogged deviation is invisible to review and to the close check
**MUST ATTENTION** custom pipeline steps must be canonical step ids (each maps to a real `.claude/skills/<step>/SKILL.md`) — never invent step names
**MUST ATTENTION** use Tier 1 context selection FIRST, then Tier 2 JSON-aware complete canonical-entry read before TaskCreate for EVERY standard workflow — resolve the selected mode and load `occurrences`, non-empty `preActions.injectContext`, `parallelGroups`, and `fingerprint`, and read every `preActions.readFiles` file; never use fixed-context grep output
**MUST ATTENTION** materialize every declared `parallelGroups` group as a wave in the task list — one task per member, wave-tagged, spawned in ONE message, all-return barrier before the next step — why: a barrier that lives only in prose gets executed one step at a time
**MUST ATTENTION** no `parallelGroups` → `sequence` IS the order — never invent a group that contradicts it; only adjacent read-only steps may be surfaced as a `Candidate wave (not declared)` — why: a self-authored wave silently reorders a validated workflow, and that costs more than the time it saves

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.
