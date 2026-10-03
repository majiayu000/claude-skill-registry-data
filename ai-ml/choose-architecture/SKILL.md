---
name: choose-architecture
description: Interview-driven selection of topology, modules and per-module recipes; writes profile.yml and the baseline ADR. Manual command.
argument-hint: "<what the system does | interview me>"
disable-model-invocation: true
---
Apply skill `architecture-selection` (act as architect; delegate a researcher first if code exists).
- Prefill answers from repository evidence; ask only what is missing, in one numbered block with defaults.
- Start from the closest `.ai/architecture/examples/*.yml` by copying it with a shell command, then edit fields.
- Write `profile.yml` (`status: draft`) and `docs/adr/0001-architecture-baseline.md` from the ADR template (copy, then edit).
Output: the architect OUT block + `NEXT: approve → set status: active → /add-fitness-tests`.
