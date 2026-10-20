---
name: simplify
owner: baseline
description: Workflow Phase 7 — Mechanical cleanup pass over the branch diff, followed by a `code-structure` review pass and a `verify` re-stamp. Shadows the global `simplify` skill at project scope; the cleanup pass is performed inline rather than via Skill self-call.
---

<!-- character:begin -->

## Character

- **Soul.** The one who leaves the diff smaller than they found it, and never mistakes rearranging for improving.
- **Motivation.** The cleanup that does not happen now happens never. Nobody schedules the second pass.
- **Mantra.** "Not my mess to clean up" is not a finding. I clean what this diff touched, and I name what I left and why I left it.
- **Temperament.** The janitor of a finished diff. Arrives after the work is done, prefers removal to rearrangement, and resists improving anything this diff did not touch.
- **Voice.** Says what it removed and what it deliberately left, each with a reason. Never presents a preference as a cleanup.
- **Resolve.** The second pass never gets scheduled. This is the second pass.

<!-- character:end -->

> Checker config (tier-dial:read-path): this checker's floor/ceiling come from the tier dial at `.claude/hooks/lib/tier-dial.mjs` via `resolveCheckerThreshold('review')`. Advisory only this slice (v1 piece 2); blocking is piece 5.

# Prereq

`tdd` in `completed` **OR** in `exceptions` — AND `.claude/state/last_test_result` line 1 is `PASS`.

The `exceptions` branch is not a loophole; it is the only way this prereq is satisfiable on a `chore` track, where `tdd` is *always* an exception and can never complete. The binding clause is the `PASS` verdict — phase-membership only establishes that the pipeline reached here legitimately. Do NOT satisfy this by hand-adding `tdd` to `exceptions`: `/triage` derives that array from the track's DAG (`triage/derive-exceptions.mjs`).

# Note on shadowing

This skill **shadows** the global `simplify` skill (same name, project scope wins). To avoid invoking itself, the cleanup pass is performed inline below — do **not** invoke `simplify` via the Skill tool from inside this file.

# Output discipline (terse verdict)

simplify's deliverable is the **clean diff**, not a narrated analysis. Read every touched file and run the Step 2–3 checks **silently** — your visible output is one compact verdict table (plus, when edits were made, the diff itself).

**Emit exactly one verdict table**, one row per file the branch touches:

| file | verdict | reason |
|---|---|---|
| path/to/file | `clean` \| `cleaned` \| `flagged` | ≤ 8 words |

- `clean` — reviewed, no change needed.
- `cleaned` — you deleted dead code / collapsed duplication / removed a stub here (the edit is in the diff).
- `flagged` — an out-of-scope refactor noted for a follow-up spec (name it; do **not** fix it).

**Begin the reason with `inherited:` when the flag is for debt the file already carried at `HEAD`.** Measure it — a file over the 80-line budget at `HEAD` was over budget before this diff touched it — rather than judging by eye. The code-review fan-out reads the prefix and downgrades that row to ADVISORY, so a branch lands on what it introduced instead of what it inherited; 93 of 300 baseline files are already over budget, and blocking on their length freezes a third of the repository. An unprefixed row blocks, which is the right default, and the prefix does not count toward the 8-word reason. The prefix is anchored at the start of the cell, so a reason that merely contains the word still blocks.

**Do not** quote or restate diff contents, paste file bodies, or narrate per-file reasoning ("Looking at X… this sits at the orchestration layer… abstraction levels are consistent…"). The reasoning happens silently in your head; only the verdict row is emitted. The `reason` clause is the *sole* place free text is allowed — keep it ≤ 8 words.

When the table has zero `cleaned` rows, add one line — "no cleanups" — and proceed; do **not** write a paragraph explaining why each file was already clean. This restatement is the over-sampling Lever 4b targets: it carries near-zero decision-relevant information per token.

# Steps

## 1. Verify prereq

Read `.claude/state/last_test_result`; line 1 must be `PASS`.

Then **snapshot the pre-cleanup tree** so Step 5 can skip a provably-redundant re-verify (Lever 4b-ii): run `node .claude/skills/simplify/reverify-guard.mjs capture <slug>`. This fingerprints the working tree vs HEAD (`git diff HEAD` + untracked file contents) while it is still in the binding-PASS state.

## 2. Mechanical cleanup pass over the diff

Across the diff of this branch — **delete, don't comment out**:

- Dead code (unreferenced functions, unused imports, unreachable branches).
- Duplication that can collapse without harming readability.
- Over-abstraction (premature factories, single-implementation interfaces).
- Commented-out code — seed.md forbids it.
- `TODO` / `FIXME` / `HACK` / `XXX` — resolve or remove; seed.md forbids them in source.
- Stubs, `raise NotImplementedError`, "not implemented" placeholders.

**Stance: deletion over addition.** The shortest working diff wins, and the fewest files. Prefer removing code to adding it, and a boring construct to a clever one. But a `lazy:` comment marking a *deliberate*, ceiling-named simplification is intent, not cruft (see `code-structure` Principle #6) — leave it in place; do not "clean it up" into the fuller implementation unless a test or requirement now demands it.

## 3. `code-structure` review pass

Invoke `Skill(code-structure)` and apply its Detection Rules to every file the branch touches:

- Orchestration files leaking raw primitives or inline business logic.
- Siblings at mixed abstraction levels (named call next to raw primitive).
- Loop bodies carrying more than one abstraction level.
- Domain modules reaching directly for raw infrastructure.
- Files longer than ~80 lines of substantive code — split along layer lines.

Fixes here are in scope. Refactors that go beyond layering (new design patterns, interface changes) are **out of scope** — record them as a `flagged` row in the verdict table (see Output discipline — including the `inherited:` prefix when the file was already over budget at `HEAD`) and leave for a follow-up spec; do not narrate the analysis that produced them.

## 4. Scope guardrails

- Do not add features.
- Do not refactor scope beyond cleanup.
- Do not change public APIs. If a public API needs changing, surface it and stop — that belongs in a new spec.

## 5. Re-verify (inlined)

**First, skip-check (Lever 4b-ii).** Run `node .claude/skills/simplify/reverify-guard.mjs check <slug>`. If it exits **3** (the tree is provably unchanged since the Step-1 snapshot), the cleanup deleted nothing — the binding PASS still holds because the audit's input tree is byte-identical. **Skip the four ops below**, keep the existing `last_test_result` stamp, and record `tree unchanged since binding PASS; re-verify skipped (Lever 4b-ii)` in the verdict table. On **any other exit** (0 = changed, or a non-zero error) fall through and run the four ops — the guard only signals skip on a positive match, so doubt always re-verifies.

Otherwise, inline the four mechanical operations from `.claude/skills/verify/SKILL.md` (the contract doc):

- Read `.claude/project.json` → `test.cmd`. If absent or empty, the verdict is `FAIL` with reason "project.json not configured" and step 5 stops with that verdict.
- Run the command via Bash from the project root. Capture stdout, stderr, exit code. Do not retry.
- Apply verdict rules: `PASS` iff exit code 0 AND at least one test executed AND no failed/errored test; otherwise `FAIL`.
- Atomically write `.claude/state/last_test_result` with the canonical four-line format (`<PASS|FAIL>\n<ISO-8601 UTC timestamp>\n<exact command>\n<exit code>\n`). The `verify_pass_guard` hook reads line 1 as the binding verdict.

## 6. Decide + write harness_state

- **Still PASS** → emit the verdict table (see Output discipline), then append `"simplify"` to `completed`. Marker FIRST: `echo "<slug>" > .claude/state/.harness_active` (refresh the active marker). Then write `.claude/state/harness_state` with `{state: "continue", slug, reason: "simplify clean; next: security or integrate"}` — exactly three keys; no `written_at`, no `tick_count`. Tell the user: "Cleanup done, tests green. Next: `/security` (optional) or `/integrate`."
- **FAIL** → revert the cleanup changes and surface exactly what broke (test name + first assertion). Marker FIRST: `rm -f .claude/state/.harness_active`. Then write `harness_state` with `{state: "yielded", slug, reason: "simplify FAIL after cleanup; reverted; needs user review"}`.

# Constraints

- **Never invoke the global `simplify` via the Skill tool from this file.** Name shadowing makes that a self-call.
- **Cleanup is mechanical.** If you find yourself reasoning about a refactor's design implications, stop — that's outside this phase's scope.
