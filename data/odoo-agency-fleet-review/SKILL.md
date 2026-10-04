---
name: odoo-agency-fleet-review
description: Review many client Odoo databases at once through odoo-mcp's cross-instance tools — fleet-wide accounting health, per-client aging, partial-failure triage — for agencies and partners managing 5–50 instances. Use when the user asks "which client...", "across all instances/databases", or wants a fleet/portfolio status.
---

# Odoo agency fleet review

You are answering questions across a fleet of client Odoo databases through
one odoo-mcp server with named instances. Every result is tagged with its
`_instance`; one client being down must never sink the whole answer.

## Prerequisites

- Multi-instance config (`ODOO_CONFIG_FILE` with an `instances` map).
  `list_instances` shows names, tags, and which allow cross-instance reads
  (`"cross_instance": false` opts a client out — respect it silently).
- Cross-instance tools are read-only by design. Writes happen per-instance
  through the normal gate, one client at a time.

## Playbook

1. **Map the fleet:** `list_instances` — report count, tags, default, and
   any opted-out clients (just the count, not a complaint).
2. **Fleet health:** `accounting_health_across_instances(instances="all")`
   (or `{"tags": ["managed"]}`). For fleets >10, run via
   `submit_async_task` and poll.
3. **Triage the errors map first.** The response carries per-instance
   `errors` — an unreachable client is a finding in itself (report it,
   with `diagnose_odoo_call` output if the human wants the cause), not a
   reason to retry the whole fan-out.
4. **Rank and drill down.** Present a per-client table sorted by the metric
   the human asked about (e.g. overdue AR). For the worst clients, drill
   down with instance-scoped calls:
   `receivable_payable_aging(instance="client_x")`,
   `search_records(..., instance="client_x")`.
5. **Cross-client comparisons stay honest:** averages are deliberately not
   merged across instances (different currencies/configs) — compare counts
   and per-client aggregates, never invent a fleet-wide average.
6. **Per-client actions:** anything beyond reading switches to that single
   instance and goes through the write gate there. Approval tokens are
   instance-bound; never reuse one across clients.

## Output format

Fleet summary (reachable/unreachable/opted-out counts), the ranked
per-client table with `_instance` labels, drill-down findings, and a
follow-up list grouped by client.

## Hard rules

- Never name an opted-out instance's data in results — it is opted out.
- Each instance runs under its own field ACL and rate budget; if a client's
  response says `redacted_fields`, that is policy, not an error.
- Fan-out is bounded (`ODOO_MCP_CROSS_INSTANCE_WORKERS`); for very large
  fleets prefer the async path over repeated synchronous sweeps.
