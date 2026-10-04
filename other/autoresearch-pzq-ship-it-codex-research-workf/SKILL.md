---
name: autoresearch
description: Use when a research task must produce a bounded deliverable that passes an explicit validator, rubric, script, reviewer, or acceptance artifact; run a native Codex validator-gated research loop with repo-local artifacts, evidence ledgers, and no dependency on OMX CLI, .omx state, tmux, hooks, or automatic wakeups.
---

# Autoresearch

Run bounded research until an explicit validator says the deliverable is good enough.

This is a native Codex adaptation of OMX `$autoresearch`: keep the measured research loop, validator-gated completion, and artifact discipline; replace OMX CLI, `.omx/state`, hook persistence, and tmux assumptions with normal Codex tools, repo-local files, optional goal tools, and `D:\todo` / project work traces when durable tracking is needed.

## Use When

- The research output itself is the deliverable.
- The user wants more than quick best-practice lookup.
- Completion must be judged by an explicit script, rubric, reviewer, benchmark, or acceptance artifact.
- The work may require iterative source gathering, synthesis, critique, and revision.

Do not use this for ordinary implementation, simple repo-local analysis, or casual docs lookup. Use `$codex-best-practice-research` for read-only external guidance and `$codex-consensus-plan` for implementation planning.

## Intake Contract

Before research execution, define:

- Mission: the research question and deliverable.
- Scope: sources, domains, timeframe, language, and exclusions.
- Validator mode:
  - `script-validator`: a command or deterministic check decides pass/fail.
  - `rubric-review`: a written rubric and reviewer/critic judgment decide pass/fail.
  - `acceptance-artifact`: a required output file contains status, evidence, and approval.
- Completion artifact path: where the final validator result or review record will live.
- Evidence ledger path: where sources, attempts, failures, and decisions are recorded.

If these are unclear, run a short `$codex-deep-interview` style pass first.

## Artifact Defaults

Use the repo's existing artifact convention. If none exists, prefer:

```text
reports/autoresearch/<slug>/mission.md
reports/autoresearch/<slug>/evidence-ledger.md
reports/autoresearch/<slug>/draft.md
reports/autoresearch/<slug>/validation.md
```

In `D:\todo`-tracked work, also write a task card or work trace when the research is nontrivial or cross-session.

## Loop

1. Write or confirm mission, scope, validator, and artifact paths.
2. Gather sources from primary/official/public evidence where possible.
3. Record source quality, dates, and unresolved gaps in the evidence ledger.
4. Produce or revise the deliverable.
5. Run the validator:
   - execute the script or command,
   - apply the rubric,
   - request an independent review lane when available and useful,
   - or update the acceptance artifact.
6. If validation fails, record the failure and revise.
7. Stop only when the completion artifact records pass/approval or when a real blocker remains.

## Completion Gate

Do not declare success because the prose sounds complete. Completion requires:

- deliverable exists,
- evidence ledger exists,
- validator result is recorded,
- status is `passed` / `approved`,
- residual risks are named,
- any active Codex goal is completed only after the evidence audit passes.

## Output Shape

- Mission
- Validator mode and artifact paths
- Sources / evidence summary
- Deliverable path
- Validation result
- Iterations and failures
- Residual risk
- Next handoff, if any

## References

Read `references/native-autoresearch-checklist.html` for a compact readiness and completion checklist.
