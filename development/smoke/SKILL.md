---
name: smoke
description: Report availability of the legacy Morning Briefing smoke pipeline without executing it.
version: 0.1.1
execution-mode: advisory
category: dev-tools
status: candidate
---

# Morning Briefing Smoke Availability

## Current availability

The legacy end-to-end Morning Briefing pipeline is unavailable in the inspected
maintained package. The 2026-09-19 source assessment found no
`hummbl_governance.services.scheduler` entrypoint or its deferred briefing
dependency chain. An archived implementation is historical source, not a
maintained runtime or an authorized fallback.

This skill currently produces an advisory availability report only. It does
not execute a scheduler, health probe, adapter, model, or delivery command. A
missing pipeline is **UNAVAILABLE**, not a passing smoke test. If newer source
appears to restore it, report **NEEDS_REVIEW** until the restoration conditions
below have been satisfied and this skill has been reviewed for execution.

## When to use

- When asked whether the Morning Briefing end-to-end smoke test is available.
- When reviewing a proposed restoration of that pipeline.
- When explaining why historical briefing smoke instructions cannot be run.

## Advisory procedure

1. Read existing source-bound handoff evidence for the maintained package. If
   necessary, inspect the named package source and entrypoint metadata without
   importing or running them. Record the repository/ref or file hash and the
   evidence time. State when evidence is old or the maintained source cannot
   be identified.
2. Report **UNAVAILABLE** when the maintained entrypoint is absent or there is
   no current evidence of its availability. Report **NEEDS_REVIEW** if a
   replacement entrypoint exists but its behavior and authorization have not
   been accepted. Never discover or run archived scheduler code as a fallback.
3. Mark all adapter, generated-file and delivery checks **NOT RUN**. Existing
   briefing files may be cited as historical artifacts; their presence does
   not establish that a current pipeline ran successfully.
4. Describe the missing entrypoint or acceptance evidence and the next scoped
   review step. Do not label an availability report as PASS or claim adapter
   coverage from a different health command. An empty health-probe collector
   can report healthy without checking this pipeline.

## Intended end-to-end outcomes, preserved for restoration

The original smoke intent is to run one maintained briefing generation cycle
and establish these seven outcomes. They are requirements for future accepted
execution, not results of the current advisory skill.

| Adapter | Expected evidence after an authorized future run |
|---|---|
| GitHub Events | Source-backed activity section or an explicit unavailable-input result |
| Calendar | Meeting/calendar section or an explicit unavailable-input result |
| Linear | Work-item section or an explicit unavailable-input result |
| Cost | Source-backed cost/usage section with its reporting period |
| Priorities | Prioritized items with source attribution |
| Agent Health | Results from named, nonempty health checks and their observation time |
| Signal Delivery | Delivery receipt if separately authorized, otherwise explicitly skipped |

The run must also produce the expected briefing artifact at an explicitly
selected maintained state location, record its timestamp and source identity,
and distinguish partial adapter results from complete pipeline success.

## Restoration conditions

- A maintained owner and source-bound entrypoint exist; the selected dependency
  chain has been reviewed without relying on archived imports or state paths.
- Tests verify the intended adapter/output behavior with isolated fixtures.
  A generic healthy exit code or an empty collector is insufficient evidence.
- State/output paths, external reads, model use, credentials, and any message
  delivery are explicitly scoped for the proposed run. Current operator holds
  and provider availability limits remain binding.
- Any Signal or other external message delivery has explicit authorization;
  a stored recipient configuration alone is not permission to send.
- The execution behavior and this skill's execution-mode declaration receive
  review before enabling operational smoke steps. Until then, retain the
  advisory procedure and report NEEDS_REVIEW even if an entrypoint is present.

## Output format

```text
Morning Briefing Smoke Availability
Status: UNAVAILABLE | NEEDS_REVIEW
Maintained source: <repository/ref or file hash; unknown if not established>
Evidence time: <time of the source observation>
Entrypoint: <absent or present but pending review>
Adapter verification: NOT RUN (all seven outcomes)
Briefing generation: NOT RUN
Delivery: NOT RUN
Next step: <specific missing evidence or bounded restoration review>
```

Keep the availability finding separate from operational health. Do not start
daemons, reconfigure the host, revive archived modules, change preferences, or
trigger external services to turn this advisory report into a smoke run.
