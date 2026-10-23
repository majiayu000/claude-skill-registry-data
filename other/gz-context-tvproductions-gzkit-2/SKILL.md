---
name: gz-context
description: Namespace router → context preservation and orientation skills, plus the focused-context loader `gz context <ADR-ID>`. Use to pick the context/handoff intent or to load one ADR's full context bundle (body + OBPI briefs + covering tests + governance rules) before invoking the matched concrete skill or piping payload to an agent harness.
category: agent-operations
lifecycle_state: active
disable-model-invocation: true
owner: gzkit-governance
last_reviewed: 2026-09-18
metadata:
  skill-version: "0.6.0"
model: haiku
---

# gz-context

| Intent | Skill |
|---|---|
| handoff | `gz-session-handoff` |
| state | `gz-state` |
| map | `gz-adr-map` |
| parity | `airlineops-parity-scan` |
| orientation | `gz-how` |
| context diet | `gz-context-diet` |
| remember | `gz-content-remember` |
| insights remember | `gz-insights-remember` |
| compose | `gz-content-compose` |
| advisor qc | `gz-advisor-qc` |

Invoke the matched skill directly. See `gz-how` for the flows and the full catalog.

## Tool surface: `gz context <ADR-ID>` (ADR-0.28.0)

Beyond the routing table above, this namespace also wields the CLI verb `gz context <ADR-ID>` (anchored by ADR-0.28.0-focused-context-loader). The verb renders the target ADR body, every OBPI brief under its `obpis/` directory, the covering-test paths grouped by REQ, and a governance-rules section as one ANSI-free Markdown payload pipeable verbatim to any agent harness:

```bash
uv run gz context ADR-<X.Y.Z>
```

See `docs/user/manpages/context.md` for the option reference and `docs/user/runbook.md` Step 1 / `docs/governance/governance_runbook.md` Step 5c for the prescribed operator moments.
