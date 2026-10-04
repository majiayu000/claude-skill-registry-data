---
name: gan
description: "Launch the GAN Harness: turn a one-line prompt into a fully built, tested, and iterated application."
argument-hint: "[app-description]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.4
---

# /gan — GAN Multi-Agent Harness

Build from prompt: **$ARGUMENTS**

1. **Plan** (`agents/gan-planner.md`) — Expand to full spec in `gan-harness/spec.md` + `gan-harness/eval-rubric.md`. Be ambitious: 12-16 features.
2. **Generate** (`agents/gan-generator.md`) — Scaffold, implement Sprint 1, start dev server, commit `iteration-001`
3. **Evaluate** (`agents/gan-evaluator.md`) — Test live app, score: design(0.3) + originality(0.2) + craft(0.3) + functionality(0.2). Threshold: 7.0/10.
4. **Iterate** — If <7.0: Generator fixes ALL issues → Evaluator re-scores. Max 5 iterations.
5. **Quality gate** — `/review` + `/security-audit` + update docs

Rules: Generator builds, doesn't judge. Evaluator is ruthlessly strict. Planner is ambitious.
