---
name: plan-execution-inline-skill
description: >-
  Execute PLAN.md phase-by-phase fully in-session — zero worker subagents.
  Same --gate loop as plan-execution-skill (tiered verification gate,
  fix-on-fail, per-phase commit+push) with testing, linting, docs, and
  responsive audit routed to the inline skills. Triggers: run plan inline,
  inline plan execution, implement PLAN-*.md without subagents.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
  mirrors: plan-execution-skill
category: Git/Workflow
---

## What I do

I execute PLAN.md files phase-by-phase **entirely in this session** — the
inline twin of `plan-execution-skill` `--gate`. Same loop, same gate
semantics, same commit discipline; the only difference is the delegate
matrix: where the subagent flavor spawns worker subagents, I load and follow
the matching inline skill. Which flavor to run is the caller's choice at
invocation — neither skill is a trial variant of the other.

**Accepting the inline trade:** you keep the session's context and full tool
access instead of a fresh subagent window. There is no harness-enforced
isolation, so the discipline below is advisory — follow it anyway.

**Sibling routing (arm selection):** this skill is the DEFAULT executor for
`/run-plan` and worktree-pipeline Step 8. The subagent sibling
`plan-execution-skill` (--gate) runs only on explicit user request + OpenCode
harness + its deps resolving; any unmet condition → this skill executes the
plan inline with a note (never abort).

## Shared PLAN contract

Identical to `plan-execution-skill` — parse the same structure:

- **Plan resolution**: explicit path wins; else branch-derived — `feat/GIT-123` → `PLANS/PLAN-GIT-123.md`; `feat/issue-123` / `feat/123` (legacy) → `PLANS/PLAN-GIT-123.md`; `feat/PROJECT-123` (tracker key per `ticketing-skill`) → `PLANS/PLAN-PROJECT-123.md`. Missing → stop with the expected path.
- **Parse**: phases = `^### Phase`; steps = `- [ ] **N.M**`; completed = `- [x]`.
- **Rationale triple**: every atomic step carries `— **Why:**` / `— **Done when:**` / `— **Consumers affected:**` — parse all three. Surface a step's `Consumers affected` BEFORE mutating its target. Verify `Done when` objectively before `[x]` — "looks done" is not done.
- **Read `## Dependency & Consumer Map` before executing** so order and blast radius are known up front.
- **Verbatim playbook discipline (anti-drift):** transcribe the PLAN's steps into the session todolist VERBATIM before any task todos; skipped steps STAY as `skip: <reason>` entries; at each phase boundary, diff todolist vs PLAN — every deviation must be a visible `skip:` or a completed step.

## The gate loop

1. **Resolve the plan** (shared contract above).
2. **Discover verification commands ONCE** from project manifests (`package.json` scripts, Makefile, pyproject, Cargo…) into `GATE.lint/.typecheck/.build/.test/.e2e`. Discovery order, pass semantics (incl. the scoped-lint rule), and INCONCLUSIVE handling are defined by `verification-loop-skill` §The gate contract — defer there, don't restate.
3. **Clean baseline**: `git status --porcelain` clean, correct branch (never `main`/`master`), work committed. Dirty tree → commit/stash first (ask if ambiguous).
4. **Per phase, in order:**
   - [guardrail] `phases_done >= MAX_PHASES` (12) or `total_fixes >= MAX_FIXES` (20) → HALT + `[goal:blocked]`
   - 4a. IMPLEMENT — every atomic step; route per the inline delegate matrix below; keep a per-step WORK LOG. Restate the step's intent in one line before touching its target so drift stays visible in-session.
   - 4b. TEST NEW CODE — new/modified source files (`git diff --name-only --diff-filter=AM`, minus configs/docs/PLAN) get tests (TS: `bar.test.ts` sibling; PY: `tests/foo/test_bar.py`; mirror the nearest existing test). Trivial pure-data additions exempt.
   - 4c. VERIFY — the gate per `verification-loop-skill` §The gate contract, at the tier it selects: **light** (scoped lint + typecheck + affected tests) is the per-phase default; **full** when the phase hit a critical-area anchor, judgment says high risk, or you are unsure; the **ticket exit gate** — the last gate of this PLAN run — runs full unconditionally. E2E per the E2E rule. On green, append the memo line `GATE <short-sha> tier=light|full lint=t typecheck=t build=t|- unit=t|-|n.a e2e=t|-|n.a` to the PLAN's `## Trace` section (memo format: §Gate memo there); per full-gate escalation, append one LOG line naming the anchor or judgment reason to `## Trace` (nothing for light). The **final** pushed SHA of the run must carry a green `tier=full` memo (the ticket exit gate provides it); intermediate phase pushes carry their tier memo as phase evidence.
   - 4d. FIX-ON-FAIL — max 3 attempts per gate step: read full output → root cause → fix → append a LOG line to the PLAN's `## Trace` section → re-run failed step then the whole tier-selected gate. Each attempt increments `total_fixes`. After 3 failures: STOP — no checkbox, no commit, no push; report blocker + ask user. **Never push red code.**
   - 4e. ON GREEN — tick ALL checkboxes (phase-level, every sub-step, satisfied acceptance criteria) + write the `— Done:` line per step (see Traceability); deliberate deviations append a `SKIP <N.M> <reason>` line to `## Trace` (mirroring the todolist `skip:` entries)
   - 4f/4g. COMMIT + PUSH — one atomic commit: phase files + PLAN update together (see Commit + push)
   - 4h. REPORT — one-line phase status, continue

**A phase advances ONLY when its applicable gate tier is green.** Red gate = no checkbox, no Done line, no commit, no push.

### Inline delegate matrix (4a)

Load and follow each named skill in this session — no Task/subagent calls:

| Task type | Inline route |
|---|---|
| Test generation | `testing-inline-skill` (decision tree, scope bounds, output contract) |
| Refactor / DRY | Handle directly (review happens upstream/downstream in the pipeline, never inline-mutated by a reviewer) |
| Lint setup/fix | `linting-inline-skill` |
| Docstrings for new/changed functions/classes | `civiltekk-documentation-inline-skill` (before the gate, same-phase commit; skip pure-data/trivial) |
| Other docs (README, ADRs) | `civiltekk-documentation-inline-skill` |
| Build/deploy/git · simple implementation | Handle directly |

### E2E rule

Run e2e ONLY IF both: Playwright configured (`playwright.config.*` + `@playwright/test`) AND the phase touched frontend code (`components/**/*.{tsx,jsx,vue,svelte}`, `app|pages|routes|src/ui`, route handlers affecting rendered pages). Backend-only phase → skip e2e and say so. Frontend but no Playwright → note + skip (never install unprompted). **Visual/responsive scope → follow the `responsive-audit-inline-skill` loop** (detect → fix → re-verify tiers) in this session instead of a bare `npx playwright test` pass (a bare pass misses the tiered defect classes); if even that is impossible, note + skip visual scope.

### Traceability

`— Done:` line per completed step, indented with the Why block:

```text
— **Done:** <one-line work summary>; files: <files>; fixes: <fixes applied or "none">
```

Rules: `fixes:` MUST list every gate fix for that step; one logical line; only tick `[x]` when `Done when` is objectively satisfied AND the gate passed; note deliberate deviations. A completed phase leaves zero unchecked boxes (`grep -n "^- \[ \]" <PLAN>` within it → empty). Requires bash (git-bash/WSL on Windows).

Split: the `— Done:` lines above are **per-step** evidence tied to the rationale triple; **run-level** events (GATE memos, full-gate-escalation and fix-on-fail LOG lines, deliberate-deviation SKIP lines) append to the PLAN's `## Trace` section — append-only, newest last, never rewritten (declared in the canonical template, `grilling-skill` §PLAN emission; create the section if absent when appending to a legacy PLAN).

### Commit + push

`git add <phase files> PLANS/PLAN-*.md` → `git commit -m "<type>(<scope>): implement Phase N — <summary>" -m "Plan: <file>. Gate: … green. Trace: per-step Done lines."` → `git push`. PLAN ticks, Done lines, and gate memos ride inside this one atomic commit — a standalone `docs(plan)` commit mid-run is never allowed. LEARNINGS writes never do: they stay working-tree only through the run (canonical rule: `continuous-learning-skill` step 6) and the run lands one trailing `chore(learnings)` commit at end of run — a standalone run commits + pushes it right after the exit gate (`--soft`: before the end-of-run tick commit); a run invoked as a pipeline subroutine leaves the sweep to the pipeline's end-of-ticket commit. In repos that ignore `LEARNINGS/**/*.md`, that sweep commit also appends each new body's `!LEARNINGS/<category>/<slug>.md` negation to `.gitignore`. Conventions per `civiltekk-git-commits-skill`; project commitlint overrides; never mix style-only with logic. Push rejected (non-FF) → stop and ask, never force-push.

### Final validation

`grep -n "^- \[ \]" <PLAN>` — empty → success. Any residue → report exactly which items are unmet and ask; never fabricate completion. Requires bash (git-bash/WSL on Windows).

### Guardrails & Budget (soft, instruction-level)

| Guardrail | Default | Override | On breach |
|---|---|---|---|
| Max phases per run | 12 | `--max-phases N` | HALT + `[goal:blocked]`, report + resume cmd |
| Max fix attempts per gate step | 3 | — | halt that phase |
| Max TOTAL fix attempts | 20 | `--max-fixes N` | HALT `[goal:blocked] budget exhausted` |
| Protected branch | `main`/`master` | — | stop before first commit |

Parse overrides from `$ARGUMENTS`; garbage flags ignored. HALT is terminal for the invocation — summarize done/remaining/next step + resume command. The run is idempotent (completed phases stay `[x]`).

### Completion markers

End every run with exactly one block (the inter-skill terminal protocol — `worktree-pipeline-skill` halts on `[goal:blocked]`):

```text
[goal:evidence] <phases done, gate results, key files, commit range>
[goal:complete]

[goal:blocked] <concrete reason — failing gate, budget exhausted, needs user input>
```

`[goal:complete]` only valid right after a non-empty `[goal:evidence]` line. Markers on their own final line(s); `[plan:*]` aliases acceptable without the plugin.

Capability binding for marker handling and skill loading:
- OpenCode: markers read by the orchestrating skill (goal plugin, when installed); inline skills loaded via the skill loader
- Claude Code: markers consumed by the orchestrating workflow; skills via the Skill tool
- Other/none: emit markers as plain final lines; follow referenced skills if present, else their documented behavior inline

### Stop conditions

Gate red after 3 attempts → report + ask · phase/fix budget hit → HALT `[goal:blocked]` · unrecoverable error → report + ask · user intervention needed → ask, resume · "stop/pause/halt" → clean stop at phase boundary · protected branch → stop before first commit · all phases complete → final report.

## Integration

| Skill | Integration |
|-------|-------------|
| `plan-execution-skill` | Subagent-delegating twin — same loop, worker subagents instead of inline routes; caller picks the flavor |
| `worktree-pipeline-skill` | Pipeline Step 8 may invoke this skill (inline arm) with an explicit PLAN path; §6d reuses `plan-execution-skill`'s malformed-step flag primitive |
| `verification-loop-skill` | Canonical gate contract + memo format — the gate loop defers there |
| `error-resolver-workflow-skill` | Gate-red diagnosis during fix-on-fail |
| `civiltekk-git-commits-skill` | Commit formats for the per-phase atomic commit |
| `testing-inline-skill` / `linting-inline-skill` / `civiltekk-documentation-inline-skill` / `responsive-audit-inline-skill` | The inline delegate family — matrix routes here |
| `tdd-workflow-skill` | 4b mandates tests for new code before the gate |
| `civiltekk-context-optimization-skill` | PLAN.md files are natural compaction anchors |
