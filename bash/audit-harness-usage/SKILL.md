---
name: audit-harness-usage
tier: D
description: >-
  Audit token usage and estimated API-equivalent cost across local agent
  harness traces from Codex CLI, Claude Code, Gemini CLI, and Cursor usage
  exports, plus quota-window status from a running Google Antigravity app,
  IDE, or CLI. Ships a read-only, standard-library Python scanner that normalizes
  incompatible cache/input/output semantics, deduplicates streaming records,
  implements CodexBar-derived lineage-aware Codex accounting locally, preserves
  Cursor list cost separately from charged cost, reports pricing coverage,
  renders self-contained HTML dashboards with improvement signals, and never
  copies prompt or response content into output. USE WHEN:
  the user asks how CodexBar or ccusage-style accounting works; wants token or
  cost statistics across coding agents; wants to find expensive models, cache
  efficiency, usage concentration, anomalous spikes, or unpriced models; says
  "token usage", "agent costs", "CodexBar cost", "Claude usage", "Gemini
  stats", "Antigravity quota", "Cursor usage export", "compare harnesses", or
  "what did my agents cost", "HTML usage report", or "usage dashboard". NOT
  FOR: provider invoices, non-Antigravity
  subscription quota windows, remote API metering, prompt-content analysis, or
  scraping credentials.
---

# Audit harness usage

Treat every number as one of three different things:

1. **Trace usage** — tokens recorded by a local harness.
2. **API-equivalent estimate** — trace tokens multiplied by a versioned public
   rate card.
3. **Metered or invoiced cost** — what a provider says it actually deducted.

Never collapse those labels. A $500 API-equivalent estimate can coexist with a
fixed-price subscription and a $0 incremental invoice.

## Quick start

Run the deterministic scanner before interpreting anything:

```bash
python3 scripts/audit_harness_usage.py --days 30
python3 scripts/audit_harness_usage.py --days 30 --format json
python3 scripts/audit_harness_usage.py --provider gemini --days 7 --format csv
python3 scripts/audit_harness_usage.py --provider cursor \
  --path cursor=/path/to/cursor-usage-export.json --format json
python3 scripts/audit_harness_usage.py --provider antigravity --format json
python3 scripts/audit_harness_usage.py --provider antigravity \
  --path antigravity=/path/to/quota-response.json --format json
python3 scripts/audit_harness_usage.py --days 30 --format html \
  --output harness-usage-report.html
```

Default discovery is read-only:

- Codex: `$CODEX_HOME/{sessions,archived_sessions}` or `~/.codex/...`, scanned
  by the bundled lineage engine; CodexBar is not required
- Claude: `$CLAUDE_CONFIG_DIR/projects`, `~/.claude/projects`, and
  `~/.config/claude/projects`
- Gemini: `~/.gemini/tmp/**/chats/session-*.json` plus newer JSONL chats
- Cursor: no default. Supply an Admin API/dashboard export explicitly.
- Antigravity: probes an already-running app, IDE, or `agy` CLI over its
  localhost language-server interface; it never starts a process or reads OAuth
  credentials. An explicit quota-response JSON is also accepted.

Use `--path PROVIDER=PATH` to replace one provider's discovery root. Repeat it
for several roots. Use `--max-files N` only for a quick diagnostic sample; it
is not a complete report.

Use `--format html --output REPORT.html` for a self-contained dashboard with
summary metrics, token composition, model concentration, quota windows,
diagnostics, insights, and evidence-backed improvement opportunities. Existing
files are never replaced unless `--force` is explicit; forced replacements are
atomic, and report files are owner-only (`0600`). The HTML has inline CSS, no
external assets or scripts, and escapes every dynamic field.

## Procedure

### 1. Set the accounting question

Name the local-calendar-day window and whether the user wants trace volume, public
API-equivalent cost, actual charged cost, or all three. If they say "cost"
without qualification, report all available semantics and label each one.

### 2. Scan and inspect coverage

Prefer JSON when further analysis is required. Check, in order:

- `diagnostics.malformed_rows`
- `diagnostics.unattributed_tokens`
- `diagnostics.codex_unresolved_forks`
- `diagnostics.codex_unresolved_total_only_rows`
- `diagnostics.codex_ambiguous_copied_prefixes`
- `diagnostics.codex_owned_suffixes`
- `diagnostics.codex_interleaved_files`
- `diagnostics.backends`
- `diagnostics.quota_backends`
- `overall.pricing_coverage`
- model buckets whose `estimated_cost_usd` is `null`

`null` means unknown or partial. It never means zero. The field
`estimated_cost_usd_priced_portion` is a disclosed lower bound when pricing
coverage is below 100%.

Codex `unattributed_tokens` is a raw scanner diagnostic accumulated before
lineage deduplication. It can exceed normalized totals and must not be presented
as a normalized token bucket or used by the HTML opportunity rules.

### 3. Reconcile the hard provider edges

For Codex, the bundled Python lineage engine follows CodexBar v0.45's
accounting rules: index leaf sessions, resolve the parent snapshot at the fork
timestamp, subtract inherited totals component-wise, classify independent
versus copied-prefix subagent counters, recognize locally owned suffixes, and
contain interleaved cumulative counters with a monotonic watermark. Confirm
the receipt says `diagnostics.backends.codex: native-lineage`.

For Claude, deduplicate streaming/fork copies only when both `message.id` and
`requestId` are present. Rows missing either half stay distinct, and the nested
1-hour cache-write component is clamped to total cache creation. These details
are required for CodexBar v0.45 count parity on older traces.

An unresolved parent is never silently repaired. Rows with both cumulative and
last-usage counters use contained growth; total-only rows remain uncounted
because no safe cap exists. Ambiguous copied prefixes without a unique parent
or owned-suffix boundary are suppressed to avoid double counting. Both cases
are explicit diagnostics and headline warnings.

No CodexBar binary, subprocess, cache, or Swift runtime is required. Use an
explicit path for a redacted fixture or alternate Codex home:

```bash
python3 scripts/audit_harness_usage.py --provider codex --days 30 \
  --path codex=/path/to/codex-home --format json
```

CodexBar remains a development-time parity oracle only. Never merge its totals
with this scanner's totals; they measure the same work. See
`references/log-formats.md`.

For Cursor, prefer `tokenUsage.totalCents` for vendor list-price cost and
`chargedCents` for what the plan deducted. Never reconstruct charged cost from
tokens when the platform supplied it.

For Gemini, state the billing mode if known. Gemini CLI can run under free,
Code Assist, API-key, or Vertex arrangements; local token counts alone do not
identify the bill.

Treat Antigravity as a separate provider, not a Gemini CLI log source. Its
local language server exposes current 5-hour/weekly quota windows for Gemini
and Claude/GPT model families, with per-model quotas as a legacy fallback. It
does not expose supported trace-level token history or cost through this
interface. Read `quota_windows[]`; leave its contribution to `overall` and
`by_model[]` empty. Never convert a remaining percentage into tokens or USD.

### 4. Interpret, then recommend

Use the deterministic report as evidence and apply judgment only here. Good
insights answer one of these questions:

- **Concentration:** Which provider/model owns most tokens and estimated cost?
- **Cache economics:** What share of normalized input is cache read? Is a low
  hit rate driving uncached input spend?
- **Output pressure:** Is output/reasoning unusually large relative to input?
- **Pricing risk:** How much usage is unpriced because the model is unknown or
  the rate card is stale?
- **Accounting quality:** Do unresolved fork baselines, interleaved-counter
  containment, malformed rows, or partial Cursor cost fields make the headline unsafe?

Recommend a change only if the report supports it. Examples: route routine
tasks to a smaller model, shorten repeated uncached context, stabilize prompts
to improve caching, update the price snapshot, or investigate one anomalous
day. Do not infer productivity or code quality from token volume.

The HTML renderer turns a small, documented set of those evidence checks into
“opportunities to review.” They are conditional signals, not causal findings:
pricing coverage gaps, low cache-read share, model concentration, output-heavy
volume, unresolved Codex lineage gaps, and low Antigravity remaining quota.
Malformed rows remain scanner diagnostics. Validate the workload context before
acting on any card.

### 5. Present the receipt

Always include:

- window and providers scanned;
- total tokens with component breakdown;
- API-equivalent estimate and pricing coverage;
- platform-reported/charged cost when present;
- Antigravity quota windows when requested, explicitly separate from tokens;
- top models;
- all material quality warnings;
- price-card date and source links.

## Deterministic / latent split

**The script owns:** path discovery, boundary validation, JSON/JSONL parsing,
provider-specific token normalization, Claude stream/fork deduplication,
Codex parent-snapshot resolution, copied-prefix classification, locally owned
suffixes, interleaved-counter watermarks, model matching, long-context
thresholds, cost arithmetic, coverage, Antigravity localhost quota probing,
CSV/JSON/text/HTML output, bounded opportunity signals, and content redaction
by construction.

**The agent owns:** choosing the business-relevant window, explaining the
difference between list price and a subscription bill, judging whether an
accounting bound is decision-safe, identifying plausible causes of anomalies,
and proposing optimizations. The agent must not repair a missing mechanical
fact with a guess.

## Safety and privacy

- Read only. Do not edit, compact, move, or delete harness traces.
- Never emit prompts, responses, tool arguments, file bodies, emails, or full
  project paths. The scanner only consumes usage metadata.
- Antigravity requests are POSTed only to constant paths on `127.0.0.1`; CSRF
  tokens are used in memory and never included in output. The scanner does not
  launch `agy`, refresh OAuth, or create a persistent session.
- Do not discover or reuse Cursor cookies. Ask for an explicit export/API
  response file.
- Do not refresh the bundled price card silently. Pricing changes are a source
  update with a new `as_of` date and tests.
- Keep raw logs local unless the user explicitly authorizes sharing them.
- `--output` writes only the rendered report to the exact chosen file. It does
  not create directories and refuses to replace an existing file without
  `--force`. New reports are owner-readable only (`0600`), and symlink targets
  are refused even with `--force`.

## References

- `references/log-formats.md` — provider schemas, formulas, CodexBar internals,
  deduplication limits, and primary sources
- `references/report-schema.md` — stable report fields and cost semantics
- `references/pricing.v1.json` — offline rate snapshot with provenance
- `references/CODEXBAR-NOTICE.md` — pinned upstream attribution and MIT notice
