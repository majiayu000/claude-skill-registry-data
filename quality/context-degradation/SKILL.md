---
name: context-degradation
description: Detect and recover from declining accuracy in long tasks caused by stale assumptions, contradictory summaries, excessive tool metadata, duplicated.
license: MIT
---

# Context Degradation

## Warning signs

- repeated questions or redoing completed work;
- path/tool/model names that do not exist in the active host;
- contradictions with user corrections or current files;
- unverified claims inherited from summaries;
- broad reads and irrelevant tools crowding out task evidence;
- skipped validation, vague next steps, or lost rollback information;
- mutable external/file state assumed unchanged after a long delay.

## Recovery

1. Stop mutations when authority, target, or current state is uncertain.
2. Re-read the latest user request, project instructions, task ledger, plan, and current working tree.
3. Verify critical facts from source: paths, configs, versions, running processes, tests, and external status.
4. Mark stale assumptions and contradictions explicitly; discard unsupported narrative.
5. Reduce active tools/references to the current step and move large evidence to artifacts with pointers.
6. Produce a fresh compressed handoff containing constraints, decisions, failures, artifacts, validation, and next action.
7. Resume with one small verifiable step, then reassess.

Use subagents for bounded independent investigation, not as a way to replicate degraded context. A fresh reviewer should receive source artifacts and acceptance criteria, not the desired conclusion.

## Prevention

Keep a decision/evidence ledger, validate after risky steps, report exact paths and commands, update summaries when facts change, and avoid loading many overlapping skills. Never wait for a fabricated percentage threshold; recover when observed behavior or evidence shows degradation.
