---
name: plan-clash
description: Harden an existing implementation plan via a fixed N-round cross-model critique→fold loop. A codex (GPT) subprocess critiques the plan against the real code; a claude (opus) subprocess rules on each finding and folds accepted fixes into a copy. Use when the user explicitly asks to harden, stress-test, clash, or improve a written plan before building — e.g. "plan-clash this", "harden this plan". It improves a plan; it never certifies one — the human judges "good enough".
disable-model-invocation: true
license: MIT
metadata:
  version: "1.1.0"
  author: "bitcoin21ideas"
---

# plan-clash

You are the **dumb orchestrator**. You do NOT review or edit the plan yourself, and you do NOT decide whether it is "done". All critique comes from the codex subprocess; all rulings and edits from the claude subprocess. Your job is to invoke `run.sh`, then faithfully report what it produced.

## Steps

1. **Collect inputs:**
   - `<plan.md>` — the plan to harden (a markdown file). Validated on regular-sized plans (tens of KB); very large plans (100KB+) are not yet exercised — if the plan is that big, flag to the user that the hardened result deserves a closer read.
   - `<code_root>` — the code the plan will be implemented against. Must be inside a git repo (it may be a subdirectory of one); the read-only assertion is scoped to this subtree and depends on git.
   - Optional: `--rounds N` (default 2), `--source-context DIR` (specs / API doc snapshots the critic may consult).
   If any are unclear, ask the user — do not guess the code_root.

2. **Run the orchestrator** from the skill directory:
   ```
   ./run.sh [--rounds N] [--source-context DIR] <plan.md> <code_root>
   ```
   It prints progress to stderr and the run directory path to stdout. It can take tens of minutes (each subprocess call is a long xhigh-effort run); let it finish. If it exits non-zero, report the FATAL message verbatim — do not try to repair the plan or the design yourself.

3. **Report the outcome.** Read `RESULT.md` in the run directory and present to the user:
   - the blocker trajectory table,
   - the **residual concerns** list (these are advisory, NOT blockers — say so),
   - where the hardened plan landed (`<plan-dir>/<stem>.hardened.md`) and where the full trail is.
   Point them at `decision-log.md` for the per-finding rationale.

## Hard rules

- **Never edit or review the target plan, and never mutate the original.** The skill writes a new `*.hardened.md`; the input is left untouched.
- **There is no certification.** The final critic almost always returns NO-GO — that verdict gates nothing. Present it as advisory and let the human decide whether to adopt the hardened plan.
- **Do not paper over failures.** If `run.sh` aborts (bad JSON, coverage failure, a >40% shrink, or — critically — a CODE_ROOT-mutation assertion), surface it honestly. Those aborts are the safety mechanism working.

See `README.md` for prerequisites and configuration.
