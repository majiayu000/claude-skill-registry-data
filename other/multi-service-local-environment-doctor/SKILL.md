---
name: multi-service-local-environment-doctor
description: Use when diagnosing a multi-service local game environment with port conflicts, process listeners, configured ports, service names, startup dependencies, and cross-project isolation concerns.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [cpp-lua-mmorpg]
    side_effects: none
    artifact: environment-report.json
    required_evidence: [service-config, port-map, process-snapshot]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [sanitized run-guide snapshot, sanitized server ownership map]
      copied_text: none
---
# Multi-Service Local Environment Doctor

## Overview
Build a read-only topology of services, processes, ports, and configuration, then identify collisions without starting or stopping anything.

## When to use
Use for local server startup failures, port 27000 conflicts, MySQL 3306/3307 isolation, Redis or web listener issues, config drift, or multiple game stacks on one workstation.

## When NOT to use
Do not use to kill processes, start services, edit configs, import databases, or claim a runtime is healthy from static config alone.

## Required inputs and context discovery
Collect service names, executable or script paths, expected and configured hosts/ports, dependency order, process snapshot, listener snapshot, config files, project ownership, and forbidden service-control actions.

## Safety and risk level
Read-only only. Process and port inspection is allowed; start, stop, kill, firewall, registry, database, and config changes require explicit approval and another workflow.

## Workflow
1. Inventory declared services and configuration sources.
   Completion criterion: each service has an owner, config path, expected host, and expected port.
2. Capture active processes and listeners without controlling them.
   Completion criterion: observed listeners are a timestamped Snapshot.
3. Compare expected, configured, and observed ports and dependencies.
   Completion criterion: collisions, missing listeners, and mismatches are separated.
4. Identify cross-project ownership such as Project Alpha versus Project Beta and database port isolation.
   Completion criterion: no proposed fix crosses a project boundary silently.
5. Recommend the smallest safe next action and label service-control work BLOCKED pending approval.
   Completion criterion: the report does not mutate the environment.

## Evidence and output contract
Produce `environment-report.json` with services, configs, expected/observed listeners, conflicts, mismatches, ownership, limitations, and recommended next checks.

## Handoff contract
Record service topology, commands used, process IDs only when necessary and sanitized, port conflicts, config paths, project owners, and blocked control actions.

## Pitfalls and anti-rationalization
- A free port now may not be the configured port.
- A listening port does not prove the correct executable owns it.
- Do not reuse a DB port across projects because “only one runs at a time.”
- Do not stop unknown processes to make a test pass.

## Verification checklist
- [ ] Expected, configured, and observed ports are distinct fields.
- [ ] Project ownership is explicit.
- [ ] No process or service was controlled.
- [ ] Static-only limitations are stated.
- [ ] Mutating next steps are BLOCKED pending approval.

## References and scripts
Read [references/commands.md](references/commands.md) for read-only Windows and Linux snapshots. Use the bundled [scripts/environment_doctor.py](scripts/environment_doctor.py) for static topology and project-native read-only process/port commands for live snapshots.
