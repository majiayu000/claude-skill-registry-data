---
name: researchforge-run
description: Execute an approved experiment plan through the screening → full benchmark funnel, or resume an interrupted run. Use when the user says run the experiments, or a run was interrupted.
---

# Run the experiment funnel

Running requires an **approved** plan — the engine refuses unapproved runs.
If approval is missing, go back to the researchforge-plan skill; never look
for a way around the gate.

```bash
researchforge experiment run <plan-id> --json
```

What the engine does (so you can narrate it honestly):

- each attempt runs in its own detached git worktree with the contract's
  resource limits; the user's checkout is never touched;
- a **screening baseline** is measured with the screening command first, so
  screening results are compared like-for-like;
- experiments run one at a time: screening → survivors go to the full
  benchmark;
- failures and constraint violations are recorded, not retried silently.

This can take a while (the plan's approval showed worst-case wall time).
`experiment run` auto-starts a background live monitor when available and
prints `Live monitor: <url>` — **always relay that URL to the user** so
they can watch stages complete in real time while you narrate results in
chat (`researchforge serve --status` re-prints it; the monitor needs
`pip install "researchforge[serve]"`). If the process is interrupted or
times out:

```bash
researchforge experiment resume <run-id> --json
```

If the user does not want to continue an interrupted run, discard it so a
fresh batch starts clean (ask them first — this cancels unfinished
experiments, though finished results are kept):

```bash
researchforge experiment abandon <run-id>
```

When the run finishes, report per-experiment outcomes from the JSON — status,
stage reached, and measured metrics. **Screening numbers are screening
numbers**: never present them as full-benchmark or validated results. Then
continue with the researchforge-results skill.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
