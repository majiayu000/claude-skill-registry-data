---
name: story-film-eval
description: Run and interpret the story-film suite's weak-model, continuity, adapter, style, and prompt-injection evaluation cases. Use when developing or regression-testing the skill package itself.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Story Film Eval

This is a developer skill. It is not part of creative production routing.

## Workflow

1. Read `../../references/EVALS.md` and `../../evals/README.md`.
2. Run static validation first:

```bash
python scripts/run_evals.py
```

3. For a live model or harness, use `--runner` with a command that accepts the case prompt on stdin and operates inside the case workspace.
4. Inspect failed checks by case ID. Change one skill rule at a time when possible.
5. Re-run the same cases plus the full static suite.
6. Add a regression case whenever a real failure teaches a reusable lesson.

## Done

The changed skill improves the target cases without regressing unrelated suites, and the new behavior has a durable regression case when appropriate.
