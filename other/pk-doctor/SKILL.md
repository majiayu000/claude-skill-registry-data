---
name: pk-doctor
description: Use the pk-doctor skill to run the aggregator health check and resolve
---

Use the pk-doctor skill to run the aggregator health check and resolve
all ERROR, WARN, and actionable INFO findings by default.

Default flow:

1. Run the report.
2. Build the remediation queue from every ERROR, every WARN, and every
   finding with `action_required: true`.
3. Resolve safe, unambiguous findings immediately through the owning
   script, command, or MCP tool.
4. Ask only for destructive, policy-sensitive, external, or ambiguous
   findings.
5. Rerun pk-doctor and report the final totals.

If the user says `info-only`, `dry-run`, `report-only`, `check-only`, or
`no fixes`, stop after the report and list the next actions without
mutating anything.
