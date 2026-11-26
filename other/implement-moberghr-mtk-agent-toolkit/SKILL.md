---
name: implement
description: Use for substantial work that adds a feature, a public contract such as an endpoint, or a multi-file behavior change; the full loop of spec, plan, batched implementation, verification and review.
type: skill
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion
argument-hint: <feature description, or a spec/plan path>
user-invocable: true
---

# MTK Implement — Full Feature Loop

## MTK File Resolution

Resolve MTK skill/reference/script paths per `.claude/references/mtk-file-resolution.md` unless the router already stated `MTK_ROOT=<path>` this session; `CLAUDE.md`, `.claude/tech-stack`, `.claude/rules/`, `tasks/`, `docs/`, `.mtk/` stay project-relative.

---

The entry point for substantial work. Stack specifics come from the active tech stack skill; the workflow detail lives in the skills each phase names (`context-engineering`, `workflow-artifacts`, `brainstorming`, `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation` / `subagent-implementation`, `security-and-hardening`, `spec-drift-detection`, `verification-before-completion`, `code-simplification`) and in the `implement-*` references.

## Phase 0: Load Context (Progressive Disclosure)

Before doing anything else:

0. Init or resume a workflow artifact (`.claude/skills/workflow-artifacts/SKILL.md`).
   - **Resolve the helper once** — plugin installs have no project-relative copy, and `CLAUDE_PLUGIN_ROOT` is never set in the Bash environment (Claude Code substitutes the braced `${CLAUDE_PLUGIN_ROOT}` into skill text at load time instead), so a bare `scripts/workflow-artifact.sh` fails. Resolve it `MTK_HELPER_ROOT`-first (a checkout you pin — see `.claude/references/env-knobs.md`), then project, then plugin, and use `"$WFA"` for every `workflow-artifact.sh` call in this skill:
     ```bash
     WFA="$([ -n "${MTK_HELPER_ROOT:-}" ] && echo "$MTK_HELPER_ROOT/scripts/workflow-artifact.sh" || ([ -f scripts/workflow-artifact.sh ] && echo scripts/workflow-artifact.sh || echo "${CLAUDE_PLUGIN_ROOT}/scripts/workflow-artifact.sh"))"
     ```
   - Run `"$WFA" list`.
   - If a single active `BUILD` workflow exists for this feature, ask via `AskUserQuestion` whether to resume that uuid or start a new one.
   - Otherwise prune expired workflows, init, and emit the phase-0 marker in **one** call — the phase goes in `--data`, not as a positional: `"$WFA" prune --older-than 30 >/dev/null; MTK_WF_UUID=$("$WFA" init BUILD --goal "<one-line user goal>") && "$WFA" event "$MTK_WF_UUID" phase_started --data '{"phase":"phase-0"}'`. Remember the uuid for the rest of the session.
   - **Bookkeeping rides along, never alone.** Every later `"$WFA"` write in this skill is appended with `&&` to the command it records (the lint, the checkpoint, the sidecar write) or grouped into one `"$WFA" batch "$MTK_WF_UUID" <op> -- <op> …` call. A standalone artifact write is a full model turn spent on one line of JSON. Only `init`, `list`, `read`, and `verify-seal` run alone.
1. Follow `.claude/skills/context-engineering/SKILL.md`: it resolves the stack for the files in scope (pass a representative `change_manifest` path when the change targets a subtree), loads the `tech-stack-{stack}` skill, and loads references per phase and per `applyTo` match. If neither `AGENTS.md` nor `CLAUDE.md` exists, stop and tell the engineer to run `/mtk-setup`. Phase 0 itself loads only the stack's coding guidelines and `architecture-principles.md` if present.
2. Query lessons for the initial scope (`learnings.sh query --phase implement`, else `tasks/lessons.md`, resolved from the main worktree).
3. Output intensity: `--terse` reports only decisions, actions, findings and evidence; `--verbose` adds rationale, alternatives and references consulted; default is brief rationale for non-obvious decisions.
4. **Worktree pre-flight (capture only).** Run `git status --porcelain` and remember the set of already-modified and untracked paths — the *pre-existing dirty set*. This is a read-only snapshot, not a gate yet. It feeds two later checks: (a) the spec's dirty-worktree risk step (`spec-driven-development` step 3b, for **out-of-manifest** paths), and (b) the **Phase 2.9 worktree collision gate** (for **in-manifest** paths — the parallel-session case). Capturing it now, before any edit, is what lets the collision gate tell "already dirty when we started" apart from "dirty because this workflow touched it."

## Phase 0.5: Brainstorm (When Needed)

If the approach is unclear, multiple designs are plausible, or the engineer asks "how should we..." — follow `.claude/skills/brainstorming/SKILL.md` before writing the spec.

Skip this phase when:
- The engineer already specified the approach
- The task is a straightforward addition following existing patterns
- The scope is narrow enough that only one viable design exists

## Phase 0.7: Ingest a Supplied Plan or Spec (When Provided)

If the engineer supplied a spec or plan as the input — a path they handed you, or an existing `docs/specs/<…>.md` / `docs/plans/<…>.md` already on disk that this run is meant to execute — **adopt it as the source of truth instead of authoring a new one.** "User supplies the plan" is a first-class entry mode, not a path collision: never write a fresh spec/plan to a path the engineer's file already occupies, and never invent a `-impl` / `-v2` suffix just to dodge overwriting their input.

1. **Detect the input.** A supplied plan/spec is one the engineer names, points the run at, or an on-disk `docs/plans|specs/*.md` the request references. If none was supplied, skip this phase — Phases 1–2 author the artifacts normally.
2. **Adopt, don't recreate.** Record the supplied path on the workflow artifact (`"$WFA" set "$MTK_WF_UUID" results.plan_path=<path>` and/or `results.spec_path=<path>`). If a JSON sidecar exists beside it, validate it against `.claude/schemas/handoff.schema.json`; if only markdown exists, derive the sidecar (`change_manifest`, `plan.batches`, `success_criteria`) via `spec-driven-development` / `planning-and-task-breakdown` **without rewriting the engineer's markdown**. Phase 2's authoring write is skipped for any artifact adopted here.
3. **Reconcile against current code (mandatory).** A supplied plan may be stale — batches already implemented since it was written. Run `prior-work-check` in its *existing-plan reconciliation mode*: classify each batch `already-satisfied` / `partially-done` / `not-started` with `file:line` evidence. Mark `already-satisfied` batches complete in the sidecar and tick them in `tasks/todo.md` with a one-line note naming what was pruned; surface `partially-done` batches for the engineer to re-scope. **Do not re-implement done work**, and never edit source in this phase.
4. **Then continue to Phase 1/2 for whatever is missing.** A supplied spec still needs a plan if none was given (and vice versa); the ambiguity gate, prior-work check, and JSON sidecar all still apply to the not-yet-authored half.

Adopting the engineer's artifact does **not** skip the approval gate — Phase 2.5 still runs, on the adopted-plus-reconciled scope, exactly as it would on a freshly authored one.

## Phase 1: Produce The Executable Spec

Follow `.claude/skills/spec-driven-development/SKILL.md`.

**Resolve ambiguity before drafting, not at the approval gate.** The spec skill's ambiguity gate (step 5) is mandatory — if two or more plausible designs, undefined scope edges, or unresolved architectural choices exist, ask via `AskUserQuestion` *before* writing the spec. The Phase 2.5 approval gate is a go/no-go on a fully-informed plan, not a place to surface open questions for the first time.

The resulting plan must include:

- scope classification
- change manifest
- test manifest
- implementation batches
- assumptions and risks

**Persist the spec to disk before continuing.** Save to `docs/specs/YYYY-MM-DD-<feature-slug>.md` using today's date and a kebab-case slug. Create `docs/specs/` if missing. This is mandatory — the engineer must be able to read and edit the spec outside of chat.

Record its path riding on the next command (`… && "$WFA" set "$MTK_WF_UUID" results.spec_path=docs/specs/<file>`). The spec is standard mode unless the engineer asks for **extended spec mode** or the rigor score lands at MAX; then the extended sections (EARS + `lint-ears.sh`, INVEST+C, Constitution Check, baseline delta) are added before the gate.

## Phase 2: Write The Task Breakdown

Follow `.claude/skills/planning-and-task-breakdown/SKILL.md`.

Write **both** files (mandatory, not optional):

1. `tasks/todo.md` — checkable batches and post-implementation review items
2. `docs/plans/YYYY-MM-DD-<feature-slug>.md` — full plan alongside the spec, same date and slug as Phase 1

Create `docs/plans/` if missing.

**Build the context pack** — the one file every implementer and reviewer subagent reads instead of CLAUDE.md + the tech-stack skill + the full coding guidelines. Build it here, once the `change_manifest` is known, and record the plan/todo paths in the same call:

```bash
bash scripts/build-context-pack.sh "$MTK_WF_UUID" docs/specs/<date>-<slug>.json \
  && "$WFA" set "$MTK_WF_UUID" results.plan_path=docs/plans/<file> results.todo_path=tasks/todo.md \
       results.context_pack=.mtk/workflows/"$MTK_WF_UUID"/context-pack.md
```

The script selects coding-guideline sections by the kinds of files in the manifest and lists every other heading with its path, so a subagent pulls a section on demand rather than reading guideline files end to end. Its `## Applicable rules` section lists the `.claude/rules/` files whose `paths:` globs match the manifest; reviewers read those and no others. Pass `results.context_pack` to every subagent prompt (implementer template and reviewer agents read it first). Rebuild it whenever the manifest is amended in Phase 3.5.

## Rigor Score (Continuous Ceremony Scaling)

Compute after Phase 2 from the JSON sidecar at `docs/specs/<date>-<slug>.json`;
recompute when the approved scope **shrinks**. Ceremony scales with blast radius.

| Score | Level | Phase 3 path | Stage 2 reviewers | `MTK_AUTO_PROCEED` |
|---|---|---|---|---|
| ≤ 3 | LIGHT | inline | conditional | eligible |
| 4–7 | STANDARD | inline | conditional | eligible |
| 8–11 | HIGH | subagent | `test-reviewer` + `context-miner` always; `architecture-reviewer` on boundary/slice | no |
| ≥ 12 | MAX | subagent | both + `silent-failure-hunter` + `context-miner` | no |

**Hard-trigger floor — overrides the score:** `batches >= 3`, `>= 6` non-mechanical
`change_manifest` entries, or `security_impact != "none"` forces **at least HIGH**.

**The Phase 3 dial names a path, not a guarantee.** Whether this session can
dispatch is probed at Phase 2.9. When it cannot, HIGH/MAX runs the *inline-MAX
profile* — it never silently becomes a STANDARD-shaped inline run, and the level
does not drop.

State the score and level in one line at the Phase 2.5 gate, e.g.
`Rigor: HIGH (score 9 — 3 batches, 8 files, security_impact=new-auth-path)`.

**Read `.claude/references/implement-rigor-scoring.md`** for the signal→points
table, the external vs internal-tooling contract-surface rule, the mechanical
definition and per-batch exception, and the scope-reduction recompute guardrails.
## Phase 2.4: Manifest Pre-Flight (Destinations)

Phase 0.7's reconciliation checks *cited anchors* — existing code the change attaches to. This phase checks the other half: the **destinations** the manifest proposes. A manifest can name a directory that does not exist, a file that lives somewhere else, or a filename shape no sibling uses, and none of that surfaces until Phase 3.5 records it as drift — after an implementer has already built against the wrong path.

Run it on the sidecar Phase 2.5 is about to seal, whether the manifest was authored in Phase 1-2 or adopted in Phase 0.7:

```bash
bash scripts/manifest-preflight.sh --human docs/specs/<date>-<slug>.json
```

- **Critical findings (MP001/MP002) block the gate.** A `modify` entry pointing at a path that does not exist is not a typo to fix later: the implementer will either create the file in the wrong place or invent a directory around it. Repoint the entry at the real path — MP002 names it when the file is tracked elsewhere — and re-run.
- **Warnings (MP003-MP006) are answered, not waived.** MP004 in particular ("the pattern this path presumes may not be used in this codebase at all") means read how the codebase does this today before sealing. If the pattern really is absent and you still want it, that is a design decision that belongs in the spec, stated — not a directory that appears silently in Phase 3.
- Record the outcome in the same call as the pre-flight script itself, so a later drift record can be told apart from an unchecked manifest:
  `bash scripts/manifest-preflight.sh <sidecar> ; "$WFA" event "$MTK_WF_UUID" manifest_preflight --data '{"critical":<n>,"warning":<n>}'`

A manifest corrected here costs one edit. The same correction found in Phase 3.5 costs a drift record, an amended sidecar, and a wasted batch.

## Phase 2.5: Approval Gate (stop here)

Mandatory. Before Phase 3, ask via `AskUserQuestion`.

**Render the plan and todo inline in the terminal first** — print the content, do
not just cite paths: a scope/batch-count/rigor header line, the full
`tasks/todo.md`, a per-batch breakdown (title, files, acceptance criteria,
boundary), a `Gate sequence:` line, then the spec/plan/todo paths as bare
repo-relative paths. Then, only if the session context has the `WORK SESSION:`
line, open the spec beside the terminal with the reference's best-effort
`work show` line before asking: silent, never blocks the gate.

Options: `Approve & run until done` · `Approve (interactive)` · `Edit first` ·
`Revise` · `Show full plan & spec in terminal`.

**Until the engineer answers: read-only Bash only — no Edit/Write on source, no
Phase 3.** In autonomous mode, never re-ask for Phases 3–7 — stop and report.

On approval, record the gate and **seal the approved scope** so a later edit
cannot silently keep the approval:

```bash
"$WFA" batch "$MTK_WF_UUID" gate plan_trust_gate pass --reason "<approve mode>" -- seal
```

`MTK_AUTO_PROCEED=1` may default the recommended option **only** when the spec has
zero open decisions and zero `[ASSUMED]` claims, no BLOCKING plan-gap findings, no
open package-legitimacy checkpoint, the scope is neither breaking-change nor high
`security_impact`, and the level is LIGHT or STANDARD (canonical list:
`implement-approval-gate.md`). Any condition failing ⇒ fall back to `AskUserQuestion`.

**Read `.claude/references/implement-approval-gate.md`** for the full rendering
spec, what counts as approval, the complete AUTO_PROCEED precondition list, harness fallbacks when
`AskUserQuestion` is unavailable, multi-spec `gate_scope` and standing-approval
expiry, and why `results.todo_path` is excluded from the seal.
## Phase 2.9: Pre-Flight (Collision, Dispatch, Baseline)

Runs after approval, before the first edit. Three checks:

1. **Collision** — is another run or a dirty tree already touching the manifest?
2. **Dispatch capability** — probe whether this session can actually dispatch
   implementer subagents; record the answer as `dispatch_capability`. HIGH/MAX with
   no dispatch runs the **inline-MAX profile** (compensations C1–C3), which keeps
   the rigor level and names what replaces isolation. `MTK_SUBAGENT_DISPATCH=0`
   declares the capability absent up front.
3. **Baseline evidence** — capture build/test/typecheck state at the base commit
   *before* the first edit, so a failure found at batch 3 is attributable. On by
   default at HIGH/MAX; `MTK_BASELINE_CAPTURE=1`/`=0` forces or skips. **If no
   baseline exists, every later checkpoint must say so** rather than implying one.

At HIGH/MAX, also recommend a dedicated worktree and a branch pin before the first edit
(`incremental-implementation` → *Batch policy*).

**Read `.claude/references/implement-preflight.md`** for the dispatch probe
procedure, the inline-MAX compensations in full, and the baseline capture and
reporting rules.
## Phase 3: Implement In Batches

**Fork — pick the implementation path from the JSON sidecar at `docs/specs/<date>-<slug>.json`:**

- **Subagent path** (`.claude/skills/subagent-implementation/SKILL.md`) — when the rigor level is HIGH or MAX (any hard trigger — `plan.batches.length >= 3`, non-mechanical `change_manifest` entries >= 6, `security_impact != "none"` — or score ≥ 8; see Rigor Score). Dispatches one fresh implementer subagent per batch with orchestrator-side drift micro-checks. In interactive mode it asks once which model (Sonnet/Opus) to use for the implementer; in autonomous mode it does **not** ask — the Sonnet policy default applies (Opus for plan-flagged novel/tricky batches), consistent with the autonomous "never ask in Phases 3-7" rule. Runs a manual Agent-per-batch loop by default; the native dynamic-workflow runtime is used only when the engineer explicitly opts in (drift/persistence/Phase-4 stay orchestrator-side either way).
- **Inline path** (`.claude/skills/incremental-implementation/SKILL.md`) — for everything below threshold. Smaller features stay in the main context.

Also follow `security-and-hardening` when scope touches auth, financial state, secrets, or infra, and `research-context` when a choice depends on current external best-practice. Test policy (failing test first, test level, no in-memory provider for DB semantics, reading a dependency's real surface) is in `incremental-implementation` → *Batch policy*; the implementer prompt carries the same rules.

Whichever path runs, every batch must:

1. implement only in-manifest files
2. add or update tests in the same batch
3. run the batch checkpoint using the build/test commands from the active tech stack skill
4. run the pre-commit review list if present
5. check the batch off in `tasks/todo.md`

After all batches:

- run the full test command from the active tech stack skill
- write an explicit behavioral diff
- emit the final `phase_exit_gate pass` (or `fail` and stop) in the same call as the full test run (`<full test cmd> && "$WFA" batch "$MTK_WF_UUID" gate phase_exit_gate pass --reason "all batches green" -- event phase_completed --data '{"phase":"phase-3"}'`); per-batch gate decisions and `results.batches_completed` are already recorded by the implementation skill, each riding on its batch checkpoint

## Phase 3.5: Spec-Drift Check

Before review, follow `.claude/skills/spec-drift-detection/SKILL.md`.

Compare the implementation against the spec's JSON sidecar at
`docs/specs/<date>-<slug>.json`:

- Files touched vs `change_manifest`
- Public contracts vs `public_contracts`
- `security_impact` vs actually-touched security-surface files
- `out_of_scope` items vs what was delivered

If critical drift is found:

1. Decide: is the implementation wrong, or was the spec incomplete?
2. If implementation wrong → fix within the manifest and re-run drift check.
3. If spec incomplete → amend the spec + JSON sidecar via
   `spec-driven-development`, re-open the Phase 2.5 approval gate for the
   scope change, then re-run drift check.
4. If the drift is a **scope reduction** — batches deferred, dropped, or split
   to a follow-up, with no new file, contract, or security surface — this is
   the one drift class that does **not** re-open the gate. Recompute the Rigor
   Score from the remaining batches (see *Rigor Score → Recompute on scope
   reduction*), record the transition on the workflow artifact, and continue at
   the recomputed level. Relaxing ceremony for work already approved needs no
   new approval; only *added* scope does.
5. Do not proceed to review until drift is clean.

Silent drift repair is forbidden. Every *increase* in scope goes through the
approval gate; a *reduction* is recorded and re-scores rigor (item 4) but does
not re-open it.

## Phase 4: Review (Two-Stage)

Run `verification-before-completion` first, then **read `.claude/references/implement-review-lanes.md`** — the single source for the lane set at each rigor level, the dispatch inputs, the silent-failure trigger, the defect-class sweep, and lane accounting (`ABSTAINED`, `NO_RESPONSE`, by-policy). Stage 1 `compliance-reviewer` checks against the sealed spec; re-check the seal with `verify-seal` — a STALE seal **refuses completion**. Stage 2 runs only after Stage 1 has no Critical findings.

Per that reference's **Review protocol** (scripts run as `bash "$MTK_ROOT/…"`, with `MTK_ROOT` per *MTK File Resolution*): collect deterministic `candidates.json` first (`compliance-reviewer` disposes of each); `review-input --record` at dispatch and `--check` before aggregating; `review-coverage.sh` on every lane result (incomplete or engine failure ⇒ `ABSTAINED`); `finding-verifier` at HIGH/MAX only; write the receipt only as its **Receipt** step qualifies.

## Phase 5: Fix Review Findings

Fix every critical issue and every warning unless you record a one-line waiver with a reason (a valid `pre_existing` finding goes to the follow-up list instead, per `review-finding-schema.md`), then:

- run the build and test commands from the active tech stack skill
- run the pre-commit review list if present
- re-run the necessary reviewer(s)

Maximum 3 review iterations; pass the merged findings to `remediation … --findings` so a stall escalates early (`implement-review-lanes.md` → Iteration cap).

## Phase 6: Cleanup

Follow `code-simplification` (built-in `/simplify` on Claude Code, with its finance carve-outs). If cleanup changes code, re-run the build and tests.

## Phase 7: Compound (Learn And Strengthen)

1. **What was learned?** A wrong spec assumption, a surprising framework/SDK behavior, a review finding that exposed a gap in the standards, an engineer correction. Append each to `tasks/lessons.md`: what happened, the rule next time, why, when it applies.
2. **Promote.** A lesson with 3+ similar entries → propose a rule in `AGENTS.md`/`CLAUDE.md`. New stable patterns (naming, structure) → propose a constitution update. Never modify it silently.
3. **Pre-commit list.** A security or compliance issue found in review → add it to `.claude/references/pre-commit-review-list.md`.
4. **Escalate a repeat reduction.** If this run recorded a ceremony reduction (a Phase 3 path, a reviewer lane, a gate) for a reason a previous run in this repo already recorded (`tasks/lessons.md`, prior workflow artifacts), do not log it a third time. Propose the durable fix — the env declaration (`MTK_SUBAGENT_DISPATCH=0`) or a lesson naming the constraint — and say which in the final report.
5. **State the compound** in the final report: what future sessions will benefit from.

## Phase 7.5: Archive (Delta Sync-Back)

Archive the run's spec/plan delta back to the durable store, then optionally write
a run receipt.

`MTK_RUN_RECEIPT=1` writes `docs/specs/<date>-<slug>.receipt.md` — a sibling of
the spec and, like it, an ignored working artifact (commit it explicitly or paste
it into the PR to keep it), holding baseline vs final figures, gates and their reasons,
dispatch path and compensations, ceremony reductions, drift/coverage/collateral
verdicts, reviewer lane outcomes, and a timing section (active minutes per phase,
engineer-wait gaps, time lost to killed dispatches) derived only from event
timestamps on the workflow artifact. The `.mtk/` workflow artifact and the
per-feature `docs/specs/` files are gitignored, so the only tracked residue of a
run is `tasks/lessons.md` and what the sync-back archived into `docs/specs/baseline/`. **Fields never recorded are written as `not recorded` — never
reconstructed.**

**Read `.claude/references/implement-archive-receipt.md`** for the sync-back
procedure and the receipt's full field list.
## Final Report

Close the workflow artifact in one call. The reason is what Phase 7 actually did
(`2 lessons appended`, `ran, nothing to capture`) — never a fixed phrase:
```bash
"$WFA" batch "$MTK_WF_UUID" gate memory_sync_gate pass --reason "<what Phase 7 did>" -- \
  set status=completed -- event workflow_completed --data '{"summary":"<short>"}'
```

**A phase that did not run is recorded as skipped, not passed.** If Phase 6 (cleanup) or
Phase 7 (compound) was not run — out of budget, engineer said to stop, anything — add one
`event phase_skipped --data '{"phase":"phase-6","reason":"<why>"}'` op per skipped phase to the
same call. If Phase 7 was skipped, drop the `gate memory_sync_gate pass` op as well: the gate
stays `pending`, which is what "Phase 7 not reached" means. Name each skipped phase in the
report below.

Report:

- scope
- files changed
- tests added or updated — **as a delta against the Phase 2.9 baseline**, not a hand count
  (`702 -> 762`); if no baseline was captured, say so instead of implying one
- Phase 3 path actually taken (`subagent` / `inline-MAX` + compensations), and
  `dispatch_capability` if it was anything other than `available`
- review agents used and stage (1 or 2)
- review iterations
- pre-existing failures carried from the baseline, named — a test red before this run began is
  reported as inherited, never as passing and never as this run's regression
- collateral churn: the `hooks/collateral-guard.sh` verdict, and what was reverted
- cleanup summary — or `Phase 6 not run: <why>`
- **what compounded** — lessons captured, rules promoted, pre-commit-review items added — or
  `Phase 7 not run: <why>`
- whether `CLAUDE.md` changed

## Critical Rules

1. Never skip planning for substantial work.
2. Skills are the workflow source of truth; do not silently replace them with ad hoc behavior.
3. Every touched file must appear in the plan.
4. New public behavior must be tested.
5. Review is mandatory for substantial work.
6. **The Phase 2.5 approval gate is always mandatory.** Spec, plan, and todo all written to disk before the gate. Ask via `AskUserQuestion` (load with `ToolSearch` if deferred; stop and say so if the harness doesn't expose it). Never assume or infer approval from the original request. The engineer chooses interactive vs autonomous at the gate, not via a flag.
