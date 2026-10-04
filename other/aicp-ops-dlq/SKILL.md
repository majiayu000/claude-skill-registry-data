---
name: aicp-ops-dlq
description: Inspect or retry the AICP dead-letter queue (~/.aicp/dlq/<UTC-date>.jsonl) via the CLI surface. Replaces the deprecated aicp_dlq_status MCP tool per `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`. Loads when the operator says "what's in the DLQ" / "retry failed tasks" / "did anything get DLQ'd" / "DLQ growing" / "show pending failures" / "reliability incident — what's queued up".
allowed-tools: Bash, Read
effort: low
---

# aicp-ops-dlq

Operate on the AICP Dead-Letter Queue via the `aicp` CLI. AICP's reliability
stack (circuit breaker → failover chain → DLQ — see
`wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md`) persists
failed tasks that exhausted the failover chain. This skill teaches the
inspection and retry workflow using the CLI surface, NOT the deprecated
`aicp_dlq_status` MCP tool.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "what's in the DLQ", "show pending failures",
  "retry the queue", "did anything get DLQ'd today", "DLQ growing", "clear out
  the queue", "anything stuck in DLQ"
- **Post-incident**: backend outage just resolved → check DLQ for tasks that
  failed during the outage and retry them
- **Pre-cleanup**: before archiving old DLQ files, list what's pending so the
  operator confirms it's safe to discard
- **Reliability audit**: monitor DLQ growth rate over time as a signal of
  upstream backend health

Do NOT load when:

- The concern is "why did this task fail in the first place" (load
  `systematic-debugging` — the DLQ entry has the error string, but root cause
  analysis lives elsewhere)
- The concern is monitoring/alerting setup (load `infra-monitoring` to add a
  DLQ-growth alert)
- The concern is the underlying DLQ implementation (the
  `per-day-jsonl-dlq-with-retry-budget` pattern doc covers it; this skill is
  about USING the queue, not changing its design)

## Operations

### Operation 1 — Inspect pending entries

**When**: operator wants to see what's in the queue without modifying it.

**Process**:

1. Run `aicp --dlq-status`
2. Output shows `Dead-Letter Queue: N pending entries` plus up to the first 10
   entries (timestamp, mode, truncated error string)
3. The output's closing `NEXT:` line will recommend `aicp --retry-dlq` if
   entries are present — follow that recommendation only if the operator has
   confirmed the upstream cause is fixed
4. If `N > 10`, the output indicates how many additional entries exist; full
   inspection requires reading the JSONL files directly:
   `ls -la ~/.aicp/dlq/` then `cat ~/.aicp/dlq/<UTC-date>.jsonl | jq`

**Quality bar**: never retry without confirming the upstream cause is fixed —
otherwise retries fail again, increment retry_count, and exhaust the retry
budget on already-failing entries.

### Operation 2 — Retry pending entries

**When**: upstream backend was down, has recovered, and operator wants to
process the failed tasks.

**Process**:

1. Confirm with operator that the upstream cause is fixed (e.g., LocalAI is
   back up — verify with `aicp --check`)
2. Run `aicp --retry-dlq`
3. Output shows `Retrying N pending DLQ entries...` then `Retried: <result>`
4. Per the DLQ pattern, entries are filtered by `retry_delay_seconds` (default
   300s = 5min) — recently-enqueued entries may be skipped on first call.
   Re-run after the delay window if expected entries weren't retried
5. Re-run `aicp --dlq-status` to confirm pending count dropped

**Quality bar**: after a retry, the pending count should fall and `succeeded`
status should rise. If it doesn't, investigate — entries may be hitting the
same failure (poison pills), in which case `retry_count` increments toward
`max_retries` (default 3, profile-tunable to 5).

### Operation 3 — Diagnose a stuck entry

**When**: an entry has been pending for hours/days and isn't being retried.

**Process**:

1. List entries: `ls -la ~/.aicp/dlq/` shows files by date
2. Find the entry: `cat ~/.aicp/dlq/<date>.jsonl | jq 'select(.status == "pending" and .retry_count >= 3)'`
3. If `retry_count >= max_retries`, the entry is exhausted (poison pill) —
   the retry pipeline correctly excludes it. Decision: investigate the error
   string, fix root cause, manually edit `retry_count` back to 0 if the cause
   is fixed, or delete the entry if the task is no longer relevant
4. If the entry is "fresh" but not being retried, check `retry_delay_seconds`
   in `config/default.yaml` `dlq:` section — the entry may not yet be eligible

**Quality bar**: never silently delete entries unless the operator confirms
the task is no longer needed. Exhausted entries are signal, not noise.

### Operation 4 — Tune the DLQ policy

**When**: operator wants to change retry budgets or pruning thresholds.

**Process**:

1. Edit `config/default.yaml` (or the active profile YAML) `dlq:` section:
   - `enabled` (default true) — disable to skip persistence entirely
   - `max_retries` (default 3, reliable profile uses 5) — bump for more
     forgiving retry budget
   - `retry_delay_seconds` (default 300) — shorten for faster retry cadence
   - `max_entries` (default 1000) — bump if expecting high failure volume
2. The profile system (per `wiki/patterns/01_drafts/profile-as-coordination-bundle.md`)
   means changes can be scoped per profile — don't edit `default.yaml` if the
   change is for production-only; edit `config/profiles/reliable.yaml` instead
3. No restart needed — values are read on each enqueue/retry

**Quality bar**: increasing `max_retries` past 5 is rare — the retry budget
exists to prevent infinite reprocessing. If 5 retries aren't enough, the
upstream issue is structural (not transient) and tuning the budget is the
wrong fix.

## Gotchas

- **Detection**: agent uses `aicp_dlq_status` MCP tool instead of `aicp --dlq-status` CLI.
  **Rule**: NEVER call `aicp_dlq_status` MCP tool — it's deprecated and will be removed.
  **Reasoning**: per audit decision, MCP overhead is paid per turn for tools used during
  specific workflows; CLI+Skills loads on demand only when this skill is invoked.

- **Detection**: agent retries after every `--dlq-status` without checking upstream.
  **Rule**: only retry when the operator confirms upstream cause is fixed.
  **Reasoning**: retrying against still-broken upstream burns retry budget and reaches
  `max_retries` faster — the entry then becomes "exhausted" and won't auto-retry
  even after upstream recovers.

- **Detection**: agent assumes empty `--dlq-status` output means all retries succeeded.
  **Rule**: empty output means zero pending; doesn't say anything about historical retries.
  **Reasoning**: succeeded entries' status is "succeeded", not removed; for retry
  history, parse the JSONL files directly with `jq 'select(.status == "succeeded")'`.

- **Detection**: agent inspects `~/.aicp/dlq/` files manually first instead of using CLI.
  **Rule**: prefer `aicp --dlq-status` for the standard summary; only drop to file
  inspection (Operation 3) when investigating a specific stuck entry.
  **Reasoning**: the CLI summary is the standard read; direct file inspection is the
  diagnostic escape hatch, not the routine path.

- **Detection**: agent runs `aicp --retry-dlq` repeatedly in a tight loop.
  **Rule**: respect `retry_delay_seconds` window (default 300s = 5min); a single
  retry call processes all entries that are eligible at that moment, repeated calls
  in <5min add nothing.
  **Reasoning**: the delay filter intentionally throttles retries to give transient
  failures time to clear; tight-loop retries defeat that.

## Reference exemplars

- `aicp/core/dlq.py` — full DLQ implementation (per-day JSONL, retry filter, status tracking)
- `aicp/cli/main.py` `_run_check()` line 771+ for similar CLI pattern shape
- `wiki/patterns/01_drafts/per-day-jsonl-dlq-with-retry-budget.md` — pattern doc with full design rationale
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` — Category D rationale for this skill's existence
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md` — explains the `NEXT:` lines this skill's commands produce

## Domain context

AICP's DLQ is part of the **three-layer reliability stack**: per-backend
circuit breakers (fast-fail per backend) → failover chain (cross-backend
recovery) → DLQ (durable persistence when chain exhausts). All three layers
are profile-tunable. The DLQ pattern doc explains why per-day JSONL was chosen
over SQLite/Redis (operator-inspectable, no daemon, append-only safe).

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-monitoring` | When the concern is alerting on DLQ growth rate, not the queue contents |
| `systematic-debugging` | When the concern is "why did this task fail" — DLQ entry has the error; root cause analysis is elsewhere |
| `aicp-ops-metrics` | When the concern is broader system metrics (DLQ growth IS one signal among many) |
