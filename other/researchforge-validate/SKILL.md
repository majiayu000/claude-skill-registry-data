---
name: researchforge-validate
description: Run repeated validation benchmarks on a run's finalists so a result can honestly be called validated. Use after a run has a promising winner, or when the user asks to confirm/validate a result.
---

# Validate finalists

"Validated" is a structural claim in ResearchForge: it requires the full
benchmark **plus** the contract's configured number of repeated validation
runs. A one-off result can never be called validated — the engine enforces
this, and so should your language.

Validation repeats the full benchmark, so it costs real time. Tell the user
how many repeats the contract configures, get their go-ahead in chat, then:

```bash
researchforge validate <run-id> --json
```

(The command asks for a typed confirmation; only pass `--yes` if the user
explicitly approved validation in this conversation.)

Afterwards, report from the JSON:

- per-attempt measurements and their spread (mean/stdev) — repeated runs
  exist precisely to expose variance, so show it;
- whether hard constraints held on every attempt;
- the final status: an experiment that survives becomes `validated`; one
  that regresses stays honest too — report that as the finding it is.

Next: the researchforge-ship skill turns a validated winner into a clean
branch, report, and optional draft PR.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
