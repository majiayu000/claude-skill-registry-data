---
name: plan
description: Discover target files and write an implementation plan from spec + rules + cache. Runs after /sdd:start and before /sdd:implement. Optional for most tiers (/sdd:implement falls back to in-line discovery when no plan exists), but required for high-risk/architectural work.
allowed-tools: Read, Write, Edit, Bash(cat .specwork/_spec/*), Bash(cat .specwork/_state/*), Bash(git rev-parse:*), Bash(mkdir .specwork/_plan:*), Bash(python3:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/plan.py:*), Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*)
---

# Plan

Write the implementation plan that `/sdd:implement` will follow.

`/sdd:plan` moves the *discovery* phase out of `/sdd:implement` and into a dedicated step: it reads the spec + rules + cache, then does targeted file discovery in the repo and produces a reviewable plan. `/sdd:implement` later reads the plan instead of re-discovering files, which makes multi-pass implementation cheaper and gives the user a checkpoint before any code is written.

`/sdd:plan` is **optional for most work** — if you skip it, `/sdd:implement` falls back to its current in-line discovery. The **exception is high-risk / architectural work**: triage stamps `plan_required` on the high-risk tier, and `/sdd:implement`'s Plan Required Gate blocks until a plan exists. Trivial, focused, and standard tiers keep the optional path.

---

## When to use

- Medium-to-large features (3+ files touched)
- When you want a review checkpoint before code is generated
- Before any multi-pass `/sdd:implement` run

When **not** to use:
- One-file changes where the target is obvious
- Quick bugfixes

---

## Prerequisites

Required artifacts (created by `/sdd:start`):

```text
.specwork/_state/<slug>-state.json
.specwork/_state/<slug>-rules.json
.specwork/_state/<slug>-implementation-cache.json
.specwork/_spec/<slug>-spec.md
```

All `## Open Questions` in the spec must be resolved (`- [x]`). Same gate as `/sdd:handoff`.

---

## Execution

| Step | Action |
|------|--------|
| 0 | Pipeline precondition — abort if `.specwork/` is missing or uninitialized via `gates.py precheck` |
| 1 | Detect branch, resolve slug |
| 2 | Check required artifacts exist; abort with no writes if any are missing |
| 3 | Open Questions gate via `gates.py check-oqs` |
| 4 | Run `python3 ${CLAUDE_PLUGIN_ROOT}/lib/plan.py <slug>` |
| 5 | Draft plan file at `.specwork/_plan/<slug>-plan.md` using the JSON output |
| 6 | Print concise summary |

---

## Non-Interactive Behavior (STRICT)

If `SDD_NON_INTERACTIVE=1`, `/sdd:plan` must continue automatically and must not
request extra confirmation to proceed.

Allowed stops in this skill are only technical gates/failures:

- No active pipeline (`gates.py precheck` fails)
- Missing required artifacts
- Unresolved Open Questions gate (`gates.py check-oqs` fails)
- Discovery engine errors/blockers from `plan.py`

Outside those cases, `/sdd:plan` must complete and print the summary without
asking whether to continue.

---

## Step 0 — Pipeline Precondition Gate (STRICT)

Before anything else, confirm a pipeline exists here:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

If the exit code is non-zero, abort with no writes:

```text
✗ Cannot plan.
No active pipeline (.specwork/ missing or uninitialized). Run /sdd:start first.
```

---

## Step 3 — Open Questions Gate (STRICT)

Run the unified gate check:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-oqs <slug>
```

If the exit code is non-zero, abort with no writes:

```text
✗ Cannot plan.
Unresolved Open Questions detected. Resolve them first, then re-run /sdd:plan.
```

Reason: planning depends on settled behavior. Same gate as `/sdd:implement` and `/sdd:handoff`.

---

## Step 4 — Run Discovery Engine

Run the unified discovery engine that handles all heuristics:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/plan.py <slug>
```

The script reads the spec, runs all gates (OQ, artifacts, consistency), executes
every heuristic (mock-consumer, HTTP status, existing tests, reference grep, spec
consistency), assesses risk, and outputs a JSON payload.

Several heuristics are **currently Java-focused** and no-op on other stacks — the
engine detects the stack and skips them (see *Heuristic discovery → Stack scope* in
`README.md`). On a TS/React/Node repo, expect fewer `[infra]`/`[mock-consumer]` rows;
this is by design, not a failure.

### Handling the output:

1. **Errors / Blockers:** If `open_questions_blocked` is `true`, or `errors` contains
   items, print the errors and abort with no writes.
2. **Drafting the Plan:** Use the JSON payload (`target_files`, `risk_signals`,
   `consistency_issues`, `plan_oqs`, `infra_hints`) to write the plan.
3. **Cache:** The script updates `implementation-cache.json` automatically.

---

## Step 5 — Write Plan File

Create `.specwork/_plan/<slug>-plan.md` (create `.specwork/_plan/` if missing).

The plan file structure is documented in `${CLAUDE_PLUGIN_ROOT}/skills/plan/REFERENCE.md` § **Plan file template**. Read that section before generating the plan.

Rules:
- Each Target Files row must reference a concrete, confirmed-or-marked path. No invented filenames.
- The Approach steps must be derivable from the spec's `## Behavior` (not new business decisions).
- If the spec is large or ambiguous about ordering, list 3-7 steps; do not expand further.
- If discovery reveals an ambiguity you cannot resolve from the spec/rules/cache alone, write it as an unresolved item in `## Open Questions`. **Do not guess.** Discovery-level ambiguity belongs here; business-behavior ambiguity belongs in the spec.

---

## Step 5.5 — Stamp the Spec Fingerprint

Immediately after the plan file is written, record which spec it was built against:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py record-fingerprint <slug>
```

This stamps a `<!-- spec-fingerprint: … -->` marker into the plan. `/sdd:implement`'s
staleness gate compares it against the live spec **by content**, so the gate stays
correct after `git stash`/`checkout`/`rebase` and after `/sdd:pause` → `/sdd:restore`
(which round-trip `.specwork/` through `git stash --all` and reset mtimes). Skipping
this is non-fatal — the gate falls back to mtime — but always run it.

---

## Step 6 — Summary

The summary output template is documented in `${CLAUDE_PLUGIN_ROOT}/skills/plan/REFERENCE.md` § **Step 6 summary template**. Read that section to see the canonical layout of all blocks.

Conditional-print rules (applied to the template in REFERENCE.md):

- Print the `Heuristic additions` block only when at least one tagged row was added.
- Print `Test path resolution` only when the existing-test-file guard adjusted at least one proposed path or skipped a duplicate.
- Print `Spec consistency` only when the consistency check added at least one plan OQ.
- Print `⚠ HIGH RISK detected` only when the discovery engine (Step 4) fired at least one signal.
- Do not print empty headers.
- Do not print the full plan content.

---

## Hard Rules

- Do not edit source code (Java, JS, configs, etc.). `/sdd:plan` is read-only with respect to the codebase.
- Do not run repo-wide scans. All `find`/`grep` calls must be scoped to a path.
- Do not invent file paths. Use `[UNVERIFIED]` for candidate paths that discovery couldn't confirm.
- Do not introduce new business decisions. The Approach must be derivable from the spec.
- If required artifacts are missing, exit cleanly with no writes (same pattern as `/sdd:handoff`).
- If **spec** Open Questions are unresolved, exit cleanly with no writes — block before planning.
- If discovery surfaces a planning-level ambiguity you cannot resolve, write it as an unresolved item under the plan's `## Open Questions` section. `/sdd:implement` will block on it just like spec Open Questions.
- Do not invent risk signals. Only mark Approach steps as `⚠ HIGH RISK` when the discovery engine (Step 4) fired on the spec body or a target file path.

---

## Re-running `/sdd:plan`

`/sdd:plan` is **idempotent**: re-running overwrites `.specwork/_plan/<slug>-plan.md` with a fresh draft. The `implementation-cache.json` remains append-only — re-running does not erase prior cache entries.

Run again after:
- Spec was significantly edited
- A new Open Question was added and resolved
- `/sdd:implement` reported drift that you want to consolidate into a fresh plan

---

## Related Skills

- `start` — writes the state that `/sdd:plan` consumes
- `spec` — drafts and refines the spec `/sdd:plan` reads; when it warns "plan is stale", re-run `/sdd:plan` (it is idempotent)
- `implement` — reads the plan and implements (falls back to in-line discovery if no plan)
- `handoff` — packages spec + cache for an external executor; if a plan exists, the executor benefits from the pre-populated cache
