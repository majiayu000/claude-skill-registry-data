---
name: migrate-architecture
description: Plan an incremental, reversible migration of a module or area to its target recipe (strangler, characterization tests, checkpoints). Manual command.
argument-hint: "<module/area>: <current> -> <target recipe>"
disable-model-invocation: true
---
Act as orchestrator (skill `orchestration`), class XL. researcher: inventory use cases ranked by change frequency (`git log --format= --name-only | sort | uniq -c | sort -rn`) and current rule locations → architect: confirm target recipe, ADR → **G0** → planner: skill `architecture-migration`, one checkpoint row per step, characterization tests first → **G1**.
