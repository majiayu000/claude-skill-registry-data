---
name: debug
description: Systematically reproduce, isolate, fix, and verify bugs and failing tests. Use when the user reports a bug, error, stack trace, or failing test and wants a quick debug loop (not the full Spec Kit bug extension).
---

# Debug

Quick path for diagnosis and repair. For structured Spec Kit bug assess → fix → test (if installed), prefer `/speckit-bug-assess` instead.

## Loop

1. **Reproduce** — Capture the exact symptom (error text, steps, failing command). Run the failing path if possible.
2. **Isolate** — Narrow to the smallest failing unit (file, function, input). Use stack traces and nearby tests.
3. **Hypothesize** — State one primary cause; avoid shotgun changes.
4. **Fix** — Minimal change that addresses the cause. Match project style.
5. **Verify** — Re-run the failing command/test; confirm the original symptom is gone.
6. **Report** — Cause, fix, how verified. Note residual risks.

## Rules

- Do not start large refactors while debugging.
- If the bug implies a new feature or multi-system redesign, stop and route to Spec Kit SDD (`/speckit-specify`).
- Ask once for missing reproduce steps rather than guessing indefinitely.
