---
name: deepen
description: Targeted deep research to fill a specific gap in an existing thesis. Use when user says "deepen", "flesh out", "expand on", "fill in", or specifies a thesis section to improve. Also supports --sync-metrics mode — detects stale financial metrics across every in-scope analytical section of a thesis (not just Key Metrics or Summary) and coherently updates every sentence that depends on them, using a Key-Metrics-table / FMP / web-search waterfall. Use when user says "sync metrics", "update the numbers throughout the note", or "fix stale figures across the whole thesis". The batch form `--sync-metrics --all-flagged` syncs every thesis flagged by the latest `$numbers --all-open` in one operation — detection fanned out to capped READ-ONLY agents, one consolidated confirmation gate, direct sequential writes (agents never write).
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$deepen`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Surgically improve one section of an existing thesis with deep research. This is NOT a full thesis rewrite — it's targeted enhancement of the weakest or most requested part.

## Arguments
SKILL_ARGS should be: `[TICKER] [optional: section name]` OR `[TICKER] --sync-metrics` OR `--sync-metrics --all-flagged`
- Examples: `NVDA Outstanding Questions`, `BESI Industry Context`, `LITE`, `APP Bull Case`, `PANW --sync-metrics`, `--sync-metrics --all-flagged`
- If no section is specified, auto-detect the weakest section (see Phase 2)
- **`--sync-metrics`** is a distinct mode — see `## Metric-Sync Mode` below, inserted after Phase 0. It replaces Phases 1-3 and 5 entirely with its own MS-1 through MS-9 sequence; Phases 0, 4, 4.5, 7, 7.5, 8 are reused (with noted adaptations). Do not fall through to Phase 1 when this flag is present.
- **`--sync-metrics --all-flagged`** is the **batch** form — see `## Metric-Sync Batch Mode` below. It syncs the whole set of theses flagged by the most recent `$numbers --all-open` Step 10b run in one operation. It does NOT weaken MS-D4: the mandatory confirmation is preserved as exactly ONE consolidated review across the batch, writes are snapshotted under a single rollback batch, and agents are used for detection ONLY — never writes.

## Phase 0: Pre-flight (MANDATORY — runs before Phase 1)

### 0.1: Acquire vault lock
Acquire a `ticker:TICKER` scope lock per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout budget: 10 minutes (deep research may be long-running). Capture the token, verify ownership (Procedure 1.5) at every subsequent shell block, release in the final reporting shell block.

### 0.2: Rename-marker pre-flight
Run `.agents/skills/_shared/preflight.md` Procedure 2. If `.rename_incomplete.TICKER` exists at vault root, hard-block per the contract's 2.3 collision message. Rewriting a thesis section while wikilinks are split across old and new names would compound the split — the rewrite would embed wikilinks keyed to the current (new) filename while some inbound references still point to the old name.

Both checks must pass before proceeding to Phase 1 (or, in `--sync-metrics` mode, to Phase 0.3 then 0.4 then the Metric-Sync Mode sequence).

### 0.3: Section existence probe (only if specific section was specified)

If `SKILL_ARGS` includes a section name (not auto-detect mode), run the refused-section check first, then `.agents/skills/_shared/preflight.md` Procedure 4 (section existence probe) against the thesis file with the target `## [Section Name]` heading.

#### 0.3a: Refused-section check

Certain sections are auto-managed archives or skill-owned artifacts — `$deepen` must never operate on them. If the user-supplied section name (case-insensitive, whitespace-normalized) matches any entry below, hard-abort with the explanation shown:

| Section | Owner | Abort message |
|---|---|---|
| `Legacy Callouts` | `$archive-callouts` | `❌ ## Legacy Callouts is an automated archive of swept addressed callouts, owned exclusively by $archive-callouts. It contains historical audit trail, not deepen-eligible analytical content. To surface insight from legacy callouts, deepen the analytical section they originally belonged to (e.g., Bull Case, Industry Context). To change the archive itself, do NOT use $deepen — either $rollback the last $archive-callouts sweep, or manually edit the plain-bullet entries and accept that $archive-callouts may re-sweep them on the next run.` |

Do NOT proceed to Procedure 4 if the refused-section check fires. Report the abort reason to the user and exit.

#### 0.3b: Section existence probe (standard)

If the section does NOT exist in the thesis, branch on whether it is a **template-mandated** section:

**Case A — requested section IS in `Templates/Thesis Template.md` and was EXPLICITLY named** (e.g. `$deepen TICKER Conviction Triggers` on one of the ~38 theses that lack it): this is the sanctioned scaffold-then-deepen path. Confirm with the user, then insert the section at its template-canonical position (between its template neighbours; `## Mental Models` and `## Legacy Callouts` excepted — those self-populate / are `$archive-callouts`-owned), seed it with the template's scaffold, and proceed to deepen it normally. This is **Tier B** (additive create), but the deepen research that follows is Tier A per the usual snapshot rule. Report: `ℹ️ ## [section] was missing (template-mandated) — scaffolded from Templates/Thesis Template.md, now deepening.` This closes the dead-end where a missing `## Conviction Triggers` could never be created (`$deepen` refused, `$stress-test` handed off to it, `$lint #14` only flagged it).

**Case B — requested section is NOT in the template** (typo / genuinely non-existent section): refuse, do not create.

```
❌ Section "## [requested section]" not found in Theses/TICKER - Name.md, and it is
   not a section in Templates/Thesis Template.md (so it can't be scaffolded).

Sections present in this thesis:
  - ## Summary
  - ## [list every ## heading found in the thesis]

Options:
  (a) $deepen TICKER [existing-section]   — deepen a section that exists
  (b) $deepen TICKER                      — auto-detect weakest present section (Phase 2)
  (c) $lint TICKER                        — surface all template drift first (check #14)

Aborted — no changes made to the thesis.
```

**Never AUTO-create a section** (Phase 2 auto-detect never scaffolds — it only scores existing sections). Case-A creation fires ONLY on an explicit user-named template-mandated section, is confirmed first, and copies the template scaffold verbatim — it is not the skill inventing structure from nothing.

If auto-detect mode (`SKILL_ARGS` is just TICKER), skip this probe — Phase 2 evaluates only sections that actually exist and scores their weakness. The Phase 2 scoring loop must exclude `## Legacy Callouts` (owned by `$archive-callouts`), `## Log` (Tier 2 append-only), and `## Mental Models` (self-populates via `$sync` per `.agents/skills/_shared/mental-models-section.md`; scaffold-empty by design — never auto-target it; deepen it only when explicitly named: `$deepen TICKER Mental Models`) from weakness candidates regardless of their contents.

### 0.4: FMP API key probe (`--sync-metrics` mode only)

Only runs when `--sync-metrics` is the invocation mode — default `$deepen` never touches FMP. Identical probe to `$numbers` Step 0.3 (shared rationale: both skills need FMP access, both fail closed on a missing key rather than silently downshifting):

```bash
if [ ! -f .data/config.json ]; then
  echo "❌ FMP API key config missing: .data/config.json"
  echo "   --sync-metrics requires .data/config.json containing fmp_api_key. See Live Portfolio.md for the canonical format."
  exit 1
fi
API_KEY=$(jq -r '.fmp_api_key // empty' .data/config.json)
if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
  echo "❌ FMP API key missing or empty in .data/config.json"
  exit 1
fi
echo "FMP_KEY_OK"
```

On failure, abort `--sync-metrics` mode only.

## Metric-Sync Mode (`--sync-metrics`)

**What this is, and how it differs from default `$deepen`.** Default `$deepen` fills an analytical gap via fresh research (Phase 2 weakness-scoring → Phase 3 research → Phase 5 rewrite of ONE section). `--sync-metrics` is a different operation: it does not judge analytical weakness or add new research — it finds financial metrics stated as *current fact* that have gone stale relative to live data, and coherently updates every sentence in the note that depends on them, so the note never ends up self-contradictory. Confirmed in-vault before this mode existed: PANW carried three different "current price" claims across Summary, a manually-flagged note, and Mental Models — none reconciled; NVDA and NFLX each carried a stale multiple repeated verbatim across 3-4 sections while Mental Models already had the corrected figure. This mode runs Phases 0 (pre-flight, including 0.4 above), 4 (snapshot), 4.5 (manifest, adapted), 7 (`_hot.md`), 7.5 (manifest flip), and 8 (report) from the base flow below; it replaces Phases 1-3 and 5 entirely with MS-1 through MS-9. It skips Phase 2.5 (graph-primer — not a comparative operation) and Phase 6 (no supporting research note — see MS-D3).

### MS-1: Resolve target thesis + fixed section scope

Read `Theses/TICKER - Name.md`. Section scope is fixed, not user-configurable per run — the exclusions are evidence-based, not caution for its own sake (MS-D1).

**In scope** (scanned for stale current-state financial-metric claims): `## Summary`, `## Key Non-consensus Insights`, `## Outstanding Questions`, `## Business Model & Product Description`, `## Industry Context`, `## Risks`, and the **Notes column** of the `## Key Metrics` table (never its Value column — that stays `$numbers`-owned exclusively).

**Never touched, regardless of content:**
- `## Bull Case`, `## Bear Case` — these reason FROM a fixed anchor TO a scenario target (confirmed in-vault: MRVL's Bear Case computes "the stock de-rates from 36x forward to 22-24x sector trough... driving 40-50% downside from $158" — the `$158` is the deliberate entry-price anchor the scenario is measured from, not stale current data; overwriting it to today's price would invalidate the scenario's math, not fix a staleness bug). If the user wants these re-derived given a new current price, that's `$deepen TICKER "Bull Case"` in default mode (full re-research), not this mode.
- `## Conviction Triggers` — fixed, falsifiable if/then thresholds the user deliberately set as time-invariant decision criteria. Never auto-touched by any skill; this mode is no exception.
- `## Mental Models` — self-populating via `$sync`/`$deepen` per `.agents/skills/_shared/mental-models-section.md`; evidence shows it's often already the FRESHEST section (NVDA and NFLX both had Mental Models already reflecting a corrected multiple while Summary/Insights lagged) — use it as a corroboration source for what "current" should read (MS-3), never as an edit target.
- `## Catalysts` — dates/events, not metrics in practice; excluded to keep the scope statement precise.
- `## Related Research` (no metrics), `## Legacy Callouts` (owned by `$archive-callouts` — reuse the existing Phase 0.3a refused-section table defensively before scanning), `## Log` (Tier 2 append-only, vault-wide rule).

### MS-2: Establish current values — three-tier waterfall (Key Metrics table first, then FMP, web search only as last resort)

For each metric type that might appear in prose (Market Cap, Stock Price, Trailing/Forward P/E, EV/Revenue, EV/EBITDA, Revenue Growth, Gross/Operating/Net Margin, FCF Yield, Net Debt/EBITDA, Dividend Yield — the same taxonomy `$numbers` tracks), resolve the current value in this order, stopping at the first tier that succeeds:

1. **Tier 1 — the thesis's own Key Metrics table**, if `key_metrics_last_refreshed:` frontmatter is within 30 days. Almost always sufficient and costs zero new API calls — `$numbers` already did the FMP fetch; re-fetching would be redundant. Read the table's Value cells directly as ground truth.
2. **Tier 2 — direct FMP fetch**, if Tier 1 is stale/absent. Same six endpoints, same `fmp_symbol:`/`ticker:` resolution logic, same currency handling as `$numbers` Step 4 (reuse by cross-reference, don't reimplement — if `$numbers`' fetch logic changes, this mode inherits the fix automatically).
3. **Tier 3 — web search**, only if Tier 2 returns `fetch_gap` or a `quote.name` mismatch against the thesis's company name. Reuse `$numbers` Step 4b's guardrails by cross-reference, not by duplication: field allowlist (Market Cap, Stock Price, Trailing/Forward P/E, EV/Revenue, EV/EBITDA only — never margins/yields/leverage/growth, which need period/GAAP-convention context a search snippet can't carry), one search + at most one follow-up fetch then give up rather than force a low-confidence number, mandatory provenance tag on any web-filled value used downstream.

Record, per metric type: `current_value`, `source_tier` (1/2/3), and if tier 3, the citation.

### MS-3: Scan in-scope sections for current-state financial-metric claims

Judgment task, not a regex sweep — read every in-scope section in full and identify clauses stating **this ticker's own current** value for a tracked metric type. Same exclusion discipline `$numbers` Step 10b already validated:

- **Exclude performance/spec comparisons** even when numerically similar to a tracked metric: "8x-669x faster," "10x lower inference cost," "70% cost reduction" are not price/multiple/margin references.
- **Exclude historical point-in-time facts**: "FY2026 Revenue: $215.9B (+65% YoY)" is a reported result, not a live figure — it does not go stale. Test: does the clause describe an *ongoing present state* ("trades at," "currently," "the stock is at," a bare "At ~$X (...)" opening framing) or a *completed, dated event* ("reported," "delivered," "FY2025 revenue was")? Only the former is in scope.
- **Exclude scenario-derived figures** even inside otherwise-in-scope sections — a stray "if X, price could reach $Y" sentence inside Key Non-Consensus Insights is a forward scenario, not a current-state claim; leave it.
- **Exclude other tickers' figures** mentioned for comparison ("vs AVGO's 28x") — single-ticker scoped; a peer's multiple is not this thesis's metric to correct, and touching it risks the same entity-resolution failure mode already documented for cross-ticker prose edits (`$numbers` Design constraint #8).

For every matched clause, capture: `section`, `verbatim clause`, `metric_type`, `old_value_stated`.

### MS-4: Build dependency clusters and compute staleness

Group matched clauses by `metric_type` where the stated old value is the same or closely matching (fuzzy tolerance — "~30x" / "30x" / "30.2x" cluster together). This is what makes "update dependencies" meaningful: a multiple appearing in Summary, Key Non-Consensus Insights, and twice in Risks is ONE cluster with four locations, not four independent findings.

Compute the delta between `old_value_stated` and MS-2's `current_value` per cluster, classified using `$numbers` Step 5's exact threshold table (no new thresholds invented). Below-threshold clusters are dropped silently — but if a cluster's own locations already disagree with each other (e.g., Summary states one multiple, Mental Models already states a different, corrected one), flag it regardless of computed delta, since internal inconsistency is the failure mode this mode exists to fix, independent of whether the note's number happens to still be within tolerance of the true current figure.

### MS-5: Present unified findings — mandatory confirmation, always

No silent-apply path exists for this mode, regardless of materiality (stricter than default `$deepen`, matching `$numbers` Step 4b's "any web-filled row forces confirmation" precedent — the multi-location blast radius earns the same treatment even when every value came from Tier 1/2 data). Present, per cluster:

```
[TICKER] Metric-Sync — proposed updates:

Cluster 1: Forward P/E  |  stated ~30x (source: Tier N)  →  current ~22x  |  Δ -26.7% (material)
  Locations (4):
    §Summary:                    "...At ~$190 (~$4.6T market cap, ~30x forward P/E), the question is whether
                                   the moat justifies the premium..."
      → proposed:                "...At ~$142 (~$3.5T market cap, ~22x forward P/E), the question is whether
                                   [re-derived: does 'justifies the premium' still follow at 22x, or does the
                                   compression itself now need characterizing?]..."
    §Key Non-Consensus Insights:  "Valuation has compressed from 45x+ to ~30x forward P/E — pricing sustained
                                   dominance but no longer pricing perfection."
      → proposed:                [re-derived clause, not a blind digit swap]
    §Outstanding Questions:       [...]
    §Risks:                       [...]

Cluster 2: [...]

⚠️ N clusters, M total locations across P sections.
Key Metrics table Notes-column mentions: [count] stale (or "none").
Bull Case / Bear Case / Conviction Triggers: not scanned (see MS-D1) — [count] scenario-anchored mentions of
  these same figures exist there and are UNCHANGED; if the scenario math itself needs re-deriving given the
  new figure, that's a separate `$deepen TICKER "Bull Case"` call.

Confirm all? (y / n / pick clusters to apply)
```

Wait for explicit response. `n` → abort cleanly, no edits, release lock. Partial-accept (a subset of clusters) is allowed — apply only confirmed clusters, note the deferred ones in the Phase 8 report.

### MS-6: Snapshot

Reuse base Phase 4 mechanics with distinct naming, so `$rollback` and `$lint` can tell a metric-sync snapshot apart from a section-deepen snapshot without ambiguity:
- Batch ID: `deepen-metrics-sync-TICKER-YYYY-MM-DD-HHMMSS`
- `snapshot_trigger: metrics-sync` — deliberately NOT `deepen`. This mode creates no supporting research note and its manifest has a different shape than `_deepen-manifest`; reusing `deepen`'s trigger value would make `$rollback`'s deepen-specific manifest cascade (2.5g) try to parse a schema it doesn't expect. `metrics-sync` is not in `$rollback`'s hardcoded recognized-trigger list (`sync, deepen, status, compare, stress-test, prune, rename, catalyst, callout-sweep, thesis, rollback, rollback-cleanup`), so it correctly falls through to the generic Tier A snapshot-restore path — the same pattern `$numbers`' own `snapshot_trigger: numbers` already relies on successfully (also absent from that list).

### MS-6.5: Write metric-sync manifest skeleton (same M3 crash-recovery rationale as base Phase 4.5, adapted schema)

Write `_Archive/Snapshots/_metrics-sync-manifest (deepen-metrics-sync-TICKER-YYYY-MM-DD-HHMMSS).md` — a deliberately distinct filename from `_deepen-manifest` so `$rollback`'s deepen-manifest parser never encounters this shape:

```yaml
---
type: metrics-sync-manifest
batch: deepen-metrics-sync-TICKER-YYYY-MM-DD-HHMMSS
status: in-progress
ticker: TICKER
clusters_confirmed: [list of metric_type values the user confirmed]
sections_affected: [list of section headings with ≥1 applied edit]
date: YYYY-MM-DD
---

# Metric-Sync Manifest

> If `status: in-progress`, the run crashed mid-edit. Check thesis `## Log` for a "Metrics syncing — in
> progress" provisional entry vs. a finalized "Metrics synced:" entry. Recovery: restore from the snapshot
> below via `$rollback` (generic Tier A path — `metrics-sync` is not a $rollback-recognized trigger, so this
> is a plain content restore, which is sufficient since no companion research note exists to also undo).

## Thesis snapshot
- [[_Archive/Snapshots/TICKER - Company Name (pre-deepen-metrics-sync-YYYY-MM-DD-HHMMSS)]]

## Clusters applied
*(filled in after MS-7: metric_type, location count, old→new, source tier, per cluster)*
```

Skeleton write failure → hard abort before MS-7's destructive edits (mirrors base Phase 4.5 contract).

### MS-6.8: Pre-announce Log entry (audit trail before destructive multi-location edit)

```
### YYYY-MM-DD
- Metrics syncing — in progress ([N] clusters, [M] locations). Snapshot: [[_Archive/Snapshots/...]]
```

### MS-7: Apply the coherent multi-location rewrite

For every confirmed cluster, for every location in it: rewrite the clause so its **stated number** matches `current_value` AND its **surrounding conclusion/characterization is re-derived**, not mechanically preserved. This is the core difference from `$numbers`' table-cell edits and the entire reason this mode exists — a table cell has no opinion; a sentence does. Read the clause's function in its sentence (what is it arguing, concluding, or characterizing?), then rewrite the whole clause so that argument is re-evaluated against the new number, using the same judgment a human analyst would apply re-reading their own note. Do not find-and-replace the digit and leave an adjacent qualifier ("no longer pricing perfection," "demands flawless execution," "still elevated") unexamined — that qualifier is exactly the dependency the user asked to have updated.

Batch all Edits for a given thesis file in one tool-call block (same rationale as `$numbers` Step 8: the harness serializes same-file Edits server-side).

**Notes-column preservation invariant carries over from `$numbers`**: if a cluster's location is inside the Key Metrics table's Notes cell, the surrounding row's Value cell (owned by `$numbers`) must remain byte-identical — this mode edits Notes-cell prose only, never the Value column (MS-D6).

**Provenance for Tier-3 (web-sourced) values**: any cluster whose `current_value` came from Tier 3 gets an explicit source citation folded into the Log entry (MS-7.5), matching `$numbers` Step 4b's mandatory tagging rule — never silently indistinguishable from Tier 1/2 data.

### MS-7.5: Finalize Log entry

Replace the provisional entry atomically:
```
### YYYY-MM-DD
- Metrics synced: [N] clusters updated across [M] locations in [P] sections ([X] via Key Metrics table, [Y]
  via FMP direct, [Z] via web: [source]). [Single most significant cluster in plain prose, e.g. "Forward P/E
  30x→22x, reconciled across Summary/Insights/Questions/Risks"]. Snapshot: [[_Archive/Snapshots/...]]
```
Verify-and-retry mechanics identical to base Phase 5c (grep-probe the provisional string is gone; on stuck-provisional, append `↳ CORRECTION: Metrics synced:` rather than re-editing).

**Prefix `Metrics synced:` is canonical — skill-origin, registered in `.agents/skills/_shared/log-prefixes.md` §20.** Reconciling a note's own stale numbers against fresh data is the same class of operation as `Numbers refresh:` — hygiene, not a new analytical finding — so `$sync` skips downstream sector/macro propagation for it exactly as it does for `Numbers refresh:`. `$sync` Step 2.5's enumeration and Step 3e drift-exclusion list were updated atomically with this change.

### MS-8: Frontmatter (conditional)

If MS-2 pulled fresh data via Tier 2 or Tier 3 this run (the thesis's own Key Metrics table was stale and this mode fetched independently), also update `key_metrics_last_refreshed: YYYY-MM-DD`. If MS-2 used Tier 1 exclusively, leave frontmatter untouched (already current).

### MS-9: `_hot.md`, manifest flip, report

Reuse base Phases 7, 7.5, 8 verbatim, with these substitutions in Phase 8's report:
- "Which section was deepened and why" → "N clusters synced across M locations in P sections; Q locations left unedited (why)"
- Add: "Bull Case / Bear Case scenario-anchored mentions of the same figures: unchanged — [list, or 'none found']. Consider `$deepen TICKER \"Bull Case\"` if the scenario itself needs re-deriving."
- Add: "Data source mix: [T1 count] from Key Metrics table, [T2 count] FMP direct, [T3 count] web search (cited)."

## Design constraints — Metric-Sync mode (MS-D, xxx DO NOT VIOLATE xxx)

**MS-D1. Section scope is fixed and evidence-based, not a caution default.** In scope: Summary, Key Non-Consensus Insights, Outstanding Questions, Business Model & Product Description, Industry Context, Risks, Key Metrics Notes cells. Excluded, each for a distinct confirmed reason: Bull/Bear Case (scenario-anchored math — MRVL's `$158` entry-price anchor), Conviction Triggers (fixed decision thresholds), Mental Models (self-populating elsewhere, often already the freshest section), Catalysts (no metrics in practice), Legacy Callouts (auto-archive), Log (append-only), Related Research (no metrics). Widening this scope is a deliberate re-opening of this constraint, not a routine extension — confirm explicitly before implementing.

**MS-D2. Every edit re-derives the surrounding argument — never a blind digit swap.** The entire premise of this mode (versus simply extending `$numbers` to touch prose, which was explicitly considered and rejected earlier — see `$numbers` constraint #8) is that a stale number's adjacent conclusion/qualifier must be re-examined, not preserved by default.

**MS-D3. No supporting research note is ever created.** Matches `$numbers` constraint #3 — this is hygiene/consistency maintenance, not new research. `Metrics synced:` carries no qualitative claim beyond "these figures are now internally consistent," so there is nothing to preserve in `/Research/`.

**MS-D4. Mandatory confirmation, no exceptions.** Every run — regardless of materiality, regardless of cluster count — pauses for explicit user confirmation before any edit. The bare `--sync-metrics` is single-ticker, one invocation at a time, given the larger blast radius per file than either default `$deepen` or `$numbers`. A batch form (`--sync-metrics --all-flagged`, see `## Metric-Sync Batch Mode`) exists for the `$numbers --all-open` → sync-the-flagged workflow, but it does NOT relax this constraint: it preserves the gate as exactly ONE consolidated review across the whole batch and never delegates writes to agents (BM-D1/BM-D4). Batch scale *consolidates* the confirmation; it never removes it.

**MS-D5. Tier waterfall is Key-Metrics-table-first, then FMP, web search last — and web search stays inside `$numbers` Step 4b's field allowlist.** Never widen the web-search field allowlist for this mode independently of `$numbers` constraint #10 — if that constraint changes, this mode inherits the change by cross-reference, not independent drift.

**MS-D6. The Notes-column preservation invariant (inherited from `$numbers` constraint #1) applies to the Key Metrics sub-target.** This mode may edit a Notes CELL's prose (that IS in scope — it's exactly the kind of hidden staleness this mode exists to catch, e.g. a Notes cell referencing a stale market cap after `$numbers` already refreshed that row's own Value cell elsewhere), but must never touch the Value column of any Key Metrics row.

## Metric-Sync Batch Mode (`--sync-metrics --all-flagged`)

Runs `--sync-metrics` across a whole flagged set in one operation. It exists because the canonical workflow is `$numbers --all-open` (batch metric refresh) → sync every thesis its **Step 10b** flags as carrying stale Summary/prose price-framing — a need the single-ticker mode could not serve, which forced fragile ad-hoc orchestration until this was codified (post-mortem 2026-07-12: the improvised fan-out ran two agents to the 64k-token ceiling, truncated a notification, and wedged the session stop-hook via mid-run kills — none of which the single-ticker path can hit). This mode is a *hardened* version of that orchestration, not a loosening of MS-D4.

**Input — the flagged set.** The ticker list is the "Summary framing stale (Step 10b)" section of the most recent `$numbers --all-open` batch report (already in context), or the tickers the user names explicitly. Never re-scan the whole vault to reconstruct it.

### BM-1: Pre-flight
`vault-wide` lock (batch touches many files — not per-ticker). Rename-marker glob (`.rename_incomplete.*`) — hard-block on any. FMP key probe **only if** any target's `key_metrics_last_refreshed` is >30 days old; a set just refreshed by `$numbers --all-open` is Tier-1 throughout (zero fetches).

### BM-2: Snapshot the ENTIRE set first, before any edit
One shell loop: `cp` each target thesis to `_Archive/Snapshots/<base> (pre-deepen-metrics-sync YYYY-MM-DD-HHMMSS).md`, insert snapshot frontmatter (`snapshot_trigger: metrics-sync`, shared `snapshot_batch: deepen-metrics-sync-batch-YYYY-MM-DD-HHMMSS`). Write ONE batch manifest `_Archive/Snapshots/_metrics-sync-manifest (deepen-metrics-sync-batch-…).md` (`status: in-progress`) listing every snapshot. The whole batch is now reversible with a single `$rollback <batch>` (generic Tier-A restore — `metrics-sync` is not a $rollback-recognized trigger, so it falls through to plain content restore, sufficient since no companion research notes exist).

### BM-3: Detection fan-out — READ-ONLY, hard-capped (every guardrail below = a live failure this prevents)
Dispatch Codex subagents with the available delegation tool to run **MS-1 → MS-4 only** (resolve, Tier-1 current values from the refreshed Key Metrics table, scan in-scope sections, cluster + materiality) and return a COMPACT report. Prefer the project `vault_readonly` agent when agent selection is available. Non-negotiable guardrails:
- **≤2 theses per agent, and detection-ONLY — NO drafted rewrites in-agent.** Three big theses + verbatim clauses + full rewrites overflowed prior output limits. The verbose deliverable (verbatim anchor clause + re-derived rewrite per location) is the caller's job in BM-5, not the agent's.
- **Hard output cap (<500 words/agent).** Quote only the single stale sentence per location; if nearing the cap, drop detail.
- **Use a read-only agent.** It must not modify vault content or runtime markers.
- **Collect only each subagent's final completion result.** Do not scrape raw thread logs or transcripts into the main context.
- **Respect the active thread cap and do not interrupt agents mid-turn.** Queue groups as needed; if a group must be re-run, wait for it to finish, then re-dispatch only the affected 1–2 tickers.

### BM-4: Consolidate
Merge all agents' clusters into ONE review: per ticker — stale figures old→current, delta/materiality, in-scope location count; group by magnitude. **Flag data-quality anomalies:** a refreshed value that will not reconcile with its own share-count / USD parenthetical / EV is either a bad `$numbers` fetch OR a genuine large move — **verify via one web search before trusting or discarding it; never assume either.** (2026-07-12: 6981's ¥17.95T market cap looked like bad data but was real — this check caught it and turned "hold" into "fix".)

### BM-5: ONE consolidated confirmation gate (MS-D4 preserved at batch scale)
Present the full review. The **caller** (not an agent) drafts the re-derived rewrites (MS-D2) for the flagged tickers. Wait for explicit `all` / a named subset / `none`. Partial-accept is allowed; note deferred tickers in the report. No silent-apply path exists — batch scale consolidates the gate into one pass, it does not remove it.

### BM-6: Apply — DIRECT and sequential (agents never write)
For each confirmed thesis, the **caller** applies edits itself: verbatim `old_string` → re-derived `new_string`, verifying each anchor against the live file; batch same-file edits in one message; respect MS-D1 exclusions (Bull/Bear/Conviction Triggers/Mental Models/Catalysts/Log/Related Research untouched) and confirm the section of any ambiguous line-number anchor before editing (a short section-header grep prevents editing an excluded section). Append a `Metrics synced:` Log entry per thesis (registry §20 — `$sync` skips propagation). Then flip the batch manifest to `completed`, update `_hot.md` Active Research Thread (ONE consolidated entry; respect the hot-md cap), release the lock, and report with the `$rollback <batch>` handle plus any per-thesis follow-up flags (e.g. a corrected figure that pushes a thesis past its own Bull/Bear anchor → recommend `$status` or a full `$deepen`, which sync itself never does).

**Batch design constraints (BM-D, xxx DO NOT VIOLATE xxx):**
- **BM-D1. Agents do DETECTION only — never WRITES.** A runaway or misfiring agent must never mutate a thesis. This is the single most important guardrail; every write is the caller's, applied directly.
- **BM-D2. Collect final completion results only; never import raw subagent thread logs into the main context.**
- **BM-D3. Do not interrupt agents mid-turn;** size and queue them correctly (≤2 theses, capped, detection-only), then re-dispatch only after completion if needed.
- **BM-D4. The mandatory-confirmation gate is preserved as exactly ONE consolidated review.** Batch scale consolidates the gate; it never removes it (MS-D4 intent intact).
- **BM-D5. MS-D1 exclusions apply batch-wide** — scenario-anchored / self-populating sections stay untouched for every thesis in the batch.
- **BM-D6. Snapshot the whole set before the first edit, under one `snapshot_batch`** — so the entire operation reverts with a single `$rollback`.

## Phase 1: Load Context

**Two-round parallel-batch pattern.** The only serial dependency is that research-note and sector-note paths are resolved from the thesis's `sector:` frontmatter and Related Research wikilinks — so the thesis must be read before the downstream batch can fire. Everything else parallelizes.

### Round 1 — parallel batch (single message, two tool calls)
Issue these two tool calls in ONE message:
1. **Read** `Theses/TICKER - [Name].md` (the thesis).
2. **Grep** the vault for the ticker string across `Theses/ Sectors/ Macro & Technology/ Research/` with `glob='*.md'` (catches mentions in notes not yet linked, scoped to markdown). Use a single multi-path Grep — do not grep each directory separately.

Wait for both to land. Use the thesis to enumerate: sector note path (from `sector:` frontmatter), every research wikilink (from `## Related Research` + `## Log`), referenced macro notes.

### Round 2 — parallel batch (single message, N tool calls)
Issue ALL of these in ONE message as a single parallel tool-call batch:
- **Read** the Sector Note.
- **Read** every research note linked from the thesis (Related Research + Log-mentioned wikilinks).
- **Read** every Macro note referenced by the thesis (from body or Log wikilinks) and any macro note tagged with the same sector.
- **Mental Models reading gate (MANDATORY — AGENTS.md; `.agents/skills/_shared/mental-models-section.md`).** Include in this batch: `Mental Models/Generalist - Overview.md` + the ticker's matching `Industry -` file + any `Lens -` file the thesis touches, AND re-read the thesis's own `## Mental Models` section (already loaded in Round 1). Every deepen renders judgement, not just Mental-Models-targeting ones. Apply the READING PROTOCOL: the Phase 3 research must test the section's recorded trigger-hypotheses against the new evidence (which fired, retired, or materially changed?) — that delta feeds the Phase 5b side-update; where new findings AGREE with the existing thesis read, hunt the single falsifying datapoint before rewriting the section. Output one "trigger delta" line in the Phase 8 report: `Mental-model trigger delta: fired/retired/changed: […] | none`.

Do NOT serialize — one parallel batch lands in ~one round-trip.

**Research-note read cap (2026-07-08):** `$deepen` edits ONE section, so read the research notes most relevant to it, not the entire back-catalog. Include: (a) every research note whose wikilink appears in or adjacent to the **target section** (section-relevant — always read, uncapped); PLUS (b) the **12 most recent by date** of the remaining linked notes. Skip older notes beyond that unless the target section cites them. A thesis with ≤12 linked notes → read all (the cap never removes signal from small sets). This keeps a mature ticker with 25+ linked notes from dominating the read budget for a single-section deepen while guaranteeing the section's own evidence base is fully loaded.

After Round 2 lands, proceed to Phase 2.

## Phase 2: Identify the Target
If a section was specified in SKILL_ARGS, use that. Otherwise, auto-detect:

**Stress-test handoff (2026-07-08 — check first):** if a recent `Research/YYYY-MM-DD - TICKER - Stress Test.md` exists (within ~30 days), read its **§6 Section Weakness Map** and treat it as a pre-computed weakness ranking — do NOT re-derive from scratch. A 🔴 row there is a strong auto-target signal (the adversarial pass already found and characterized the gap, and named the concrete fix). Use the Weakness Map to seed the scoring below rather than duplicating the analysis; if the map names a clear 🔴 section, target it and cite the stress test as the rationale. Fall through to full weakness scoring only when no recent stress test exists or its map is empty. (This is the natural `$stress-test → $deepen [flagged section]` chain from User Guide §3.3 — the handoff removes the redundant re-scan.)

**Weakness scoring** (check each, flag the worst):
- **Empty or stub sections**: sections with just `-` or `<!-- -->` placeholder comments
- **Key Non-consensus Insights**: if fewer than 3 substantive paragraphs, this is the priority (AGENTS.md marks this as the most important section)
- **Outstanding Questions**: if fewer than 3 questions, the thesis hasn't been properly challenged
- **Business Model & Product Description**: if under 200 words, the understanding is superficial
- **Industry Context**: if missing value chain analysis or competitive dynamics
- **Key Metrics**: if the table has empty cells or data older than 6 months
- **Bull/Bear Case imbalance**: if one is dramatically shorter than the other (suggests bias)
- **Risks**: if fewer than 3 risks, the thesis is underprotected
- **Catalysts**: if empty or all dates have passed
- **Conviction Triggers**: if missing or vague (not falsifiable)

Tell the user which section you're targeting and why before proceeding.

## Phase 2.5: Graph-primer peer-section cross-read (comparative sections only)

**GATE**: Execute ONLY if the `target_section` resolved in Phase 2 is in the comparative-sections whitelist:
- `Industry Context`
- `Key Non-consensus Insights`
- `Bull Case` (when the deepen framing is comparative — user mentioned peers or competitive dynamics)
- `Bear Case` (same condition as Bull Case)
- `Mental Models` (peer Mental Models sections show which model triggers cluster peers flagged — useful comparative primer)

NOT applicable (SKIP Phase 2.5 entirely if target_section is one of these):
- `Summary`, `Business Model & Product Description`, `Key Metrics`, `Outstanding Questions`, `Catalysts`, `Risks`, `Conviction Triggers`, `Related Research`, `Log`, `Legacy Callouts`

Rationale for gating: peer section content has signal for competitive/comparative framing but becomes noise for idiosyncratic sections (Risks, Catalysts, Outstanding Questions are typically thesis-specific, not cluster-wide).

Per `.agents/skills/_shared/graph-primer.md` Mode A.

Read `_graph.md` once (in parallel with Phase 1 Reads if possible; otherwise as a single Read before Phase 3). Extract:
- `entry = adjacency_index[TICKER]`
- `sector_peers = union over s ∈ entry.sectors of sector_reverse[s] - {TICKER}`
- Rank `sector_peers` by most-recent `log_tail` entry date. Take top 3.

Bash-extract `target_section` from each peer thesis in ONE batch (not per-peer serial Bash):

```bash
TARGET_SECTION="[section name from Phase 2]"
for f in "Theses/[peer1] - Name.md" "Theses/[peer2] - Name.md" "Theses/[peer3] - Name.md"; do
  echo "=== $f ==="
  awk -v sec="## $TARGET_SECTION" '
    $0 == sec { in_sec=1; next }
    in_sec && /^## / { exit }
    in_sec { print }
  ' "$f"
done
```

Inject peer section content as comparative primer for Phase 3 + Phase 5:

```
Peer-section comparative primer (graph primer):
  === [peer TICKER] ## [section]
    [peer content]
  === [peer TICKER] ## [section]
    [peer content]
```

**Phase 3 + Phase 5 explicit framing requirement**: "Use peer sections to identify what's **missing or underdeveloped** in the target thesis's section relative to how peers frame the same analytical dimension. Do NOT replicate peer content verbatim. Peer content identifies gaps; target-specific research fills them."

**Anti-pattern enforced** + **Peer-dominance mitigation**: `.agents/skills/deepen/references/rationale.md` §5. Summary — the target's divergence from peers is often the thesis itself; do not substitute peer content for target-specific depth.

**Missing-graph fallback**: per `.agents/skills/_shared/graph-primer.md` §Missing-graph fallback. Phase 3 + Phase 5 proceed target-only. Skip peer cross-read silently.

## Phase 3: Deep Research
1. **Vault research first**: Extract every relevant data point from existing research notes, sector notes, and macro notes. Do not duplicate what's already captured.
2. **Web research**: Search for recent developments specific to the target section:
   - For Key Non-consensus Insights: search for sell-side consensus, then find evidence that contradicts it
   - For Outstanding Questions: search for answers to existing questions AND identify new questions a skeptical investor would ask
   - For Business Model: search for revenue breakdowns, segment reporting, product specs, analyst commentary on business model
   - For Industry Context: search for market share data, competitive dynamics, recent M&A, new entrants
   - For Key Metrics: search for latest financial data (quarterly earnings, guidance)
   - For Bull/Bear Case: search for the strongest version of whichever side is underweight
   - For Risks: search for bear cases, short seller reports, regulatory risks, technological disruption
   - For Catalysts: search for upcoming earnings dates, product launches, regulatory decisions, industry events
   - For Conviction Triggers: search for the most likely binary events that would decisively change the thesis
3. **Cross-reference**: Check if new findings affect other theses in the vault

## Phase 4: Pre-Edit Safety — Snapshot

Before rewriting the target section, snapshot the thesis:

1. Create snapshot directory if needed:
   ```bash
   mkdir -p _Archive/Snapshots
   ```
2. Generate `HHMMSS` once at Phase 4 start. Reused by the snapshot (this phase) and the manifest (Phase 4.5):
   ```bash
   HHMMSS=$(date +%H%M%S)
   ```
3. Copy the current thesis note:
   ```bash
   cp "Theses/TICKER - Company Name.md" "_Archive/Snapshots/TICKER - Company Name (pre-deepen YYYY-MM-DD-HHMMSS).md"
   ```
4. Read the newly created snapshot, then add to its frontmatter:
   ```yaml
   snapshot_of: "[[Theses/TICKER - Company Name]]"
   snapshot_date: YYYY-MM-DD
   snapshot_trigger: deepen
   snapshot_batch: deepen-TICKER-YYYY-MM-DD-HHMMSS
   ```

   **Batch ID format**: `deepen-TICKER-YYYY-MM-DD-HHMMSS`. Rationale in `.agents/skills/deepen/references/rationale.md` §2.

## Phase 4.5: Write deepen manifest skeleton (M3 — skeleton before destructive edits)

> **Why this manifest exists (M3)**: `.agents/skills/deepen/references/rationale.md` §1.

Write manifest at `_Archive/Snapshots/_deepen-manifest (deepen-TICKER-YYYY-MM-DD-HHMMSS).md`:

```yaml
---
type: deepen-manifest
batch: deepen-TICKER-YYYY-MM-DD-HHMMSS
status: in-progress
ticker: TICKER
section: [Section Name from Phase 2]
date: YYYY-MM-DD
---

# Deepen Manifest

> **If `status: in-progress`**, `$deepen` crashed between Phase 4.5 (skeleton)
> and Phase 7.5 (flip). Check thesis `## Log` for today's date + `Deepening` prefix
> to see whether the provisional entry has been superseded by the final `Deepened` entry.
> Recovery: `$rollback deepen-TICKER-YYYY-MM-DD-HHMMSS` → Step 2.5g offers:
>   (a) Restore thesis from pre-deepen snapshot (undo section rewrite + Log entry).
>   (b) Full cascade — (a) + delete supporting research note (if Phase 6 created one).
>   (c) Cancel.
>
> **If `status: completed`**, Phase 4-7 all succeeded. `$rollback` Step 2.5g is
> still available within the cascade's per-snapshot age window.

## Thesis snapshot
- [[_Archive/Snapshots/TICKER - Company Name (pre-deepen YYYY-MM-DD-HHMMSS)]]

## Thesis target
- `Theses/TICKER - Company Name.md`
- Section deepened: [Section Name]

## Research note created (if any)
- *(filled in Phase 7.5 flip: wikilink to Research note, or `none — Phase 6 judged new research insubstantial`)*

## Phase 5 Log-append outcome
- *(filled in Phase 7.5 flip: succeeded | provisional-entry-stuck + correction-appended)*
```

Skeleton write failure → hard abort BEFORE Phase 5 destructive edits. Thesis snapshot (Phase 4) exists but is orphan — it falls under standard `$clean` orphan protection (90-day default, opt-in deletion). Report failure to user.

## Phase 5: Rewrite the Target Section

### 5a: Pre-announce Log entry (audit trail before destructive edit)
Append a provisional Log entry to the thesis BEFORE rewriting the section. This ensures an audit trail exists even if the skill fails mid-rewrite:
```
### YYYY-MM-DD
- Deepening [Section Name] — in progress. Snapshot: [[_Archive/Snapshots/...]]
```

### 5b: Rewrite the section
- Rewrite the section in-place, preserving the thesis note's overall structure
- Follow the conventions from AGENTS.md and the Thesis Template:
  - Non-consensus Insights: 3-5 one-paragraph summaries of what the market is missing
  - Outstanding Questions: 3-10 one-paragraph summaries of what a skeptical IC would ask
  - Business Model: in-depth with analogies, product specs, revenue segmentation
  - Industry Context: competitive dynamics, market share shifts, value chain analysis
  - Conviction Triggers: concrete, falsifiable if/then statements with specific thresholds
- **Integrate, don't append** — the section should read as a coherent whole, not show seams between old and new content
- Bold any genuinely new data points or insights not previously in the vault
- **Tag new quantitative claims** — any fresh number introduced into the section (price, margin, yield, share, growth rate, count) carries a provenance tag per `.agents/skills/_shared/provenance-tags.md`; match precision to sourcing (a single-source figure is `[1×: source]` or rounded, never a bare high-precision fact). This mirrors `--sync-metrics` mode's existing provenance discipline for web-filled values (MS-2 Tier 3), now applied to newly-introduced numbers in default-mode deepens.
- Add wikilinks to any vault notes referenced

**Mental Models side-update** (per `.agents/skills/_shared/mental-models-section.md`): if Phase 3 research activated, retired, or materially changed a `/Mental Models` trigger read for this thesis, ALSO merge it into the `## Mental Models` section as a secondary edit (the Phase 4 whole-file snapshot already covers it; no extra snapshot needed). Skip when the target section IS `## Mental Models` (the 5b rewrite already handles it) or when no new trigger fired. Note the side-update in the 5c Log entry.

**Disconfirm before finalizing (every target section, not only Mental-Models-writing runs).** Before locking the rewrite, state in one paragraph the strongest case this rewrite is WRONG — the datapoint or reading that would falsify what you just wrote. Per the READING PROTOCOL ([[Generalist - Overview]]), agreement/confidence is a trigger to disconfirm, not to commit; a deepen that only strengthens the prior is doing half the job. Where the disconfirm surfaces a live falsifying datapoint, fold it into the rewrite (a caveat, a Risk, an Outstanding Question) rather than dropping it; where it does not, the rewrite stands.

### 5c: Finalize Log entry
After the rewrite succeeds, use `Edit` to atomically replace the provisional Log entry with the final version:
```
### YYYY-MM-DD
- Deepened [Section Name]: [key finding] — conviction [unchanged/strengthened/weakened + reason]. Snapshot: [[_Archive/Snapshots/...]]
```
Replace `Deepening [Section Name] — in progress` with `Deepened [Section Name]: [key finding] — conviction [impact + reason]`.

**Verify and retry**: After the Edit, run a single `grep -q` shell probe to confirm the provisional text (`Deepening [Section Name] — in progress`) is gone. `grep -q` is faster than a file-read call and returns a clean exit status without injecting the thesis body into context:

```bash
# Exit 0 = provisional text STILL present (Edit failed silently)
# Exit 1 = provisional text absent (Edit succeeded)
if grep -qF "Deepening [Section Name] — in progress" "Theses/TICKER - Company Name.md"; then
  echo "EDIT_FAILED_PROVISIONAL_STUCK"
else
  echo "EDIT_OK"
fi
```

1. **`EDIT_OK`** → provisional text absent → proceed to Phase 6.
2. **`EDIT_FAILED_PROVISIONAL_STUCK`** → retry with broader context:
   - Include the full `### YYYY-MM-DD` date header AND the provisional line as `old_string` to ensure uniqueness.
   - Re-run the same `grep -qF` probe after the retry to confirm.
3. **Retry also failed** (grep still exits 0) → append a corrective entry immediately below the stuck provisional entry:
   ```
   - ↳ CORRECTION: Deepened [Section Name]: [key finding] — conviction [impact + reason]. Supersedes incomplete entry above.
   ```
   This preserves the append-only Log contract while ensuring the audit trail is always complete. `$sync` drift detection recognizes both `"Deepened"` and `"↳ CORRECTION: Deepened"` prefixes.

> **Drift coupling**: `.agents/skills/deepen/references/rationale.md` §4. Registry entries: `.agents/skills/_shared/log-prefixes.md` §2, §3, §4. `$lint #29` flags drift.

> **Failure states**: If the skill fails after 5a but before 5b → Log shows "Deepening... in progress" but section is unchanged; snapshot is unnecessary (thesis body intact). If it fails after 5b but before 5c → Log shows "Deepening... in progress" with section already rewritten; the verify-and-retry mechanism (above) will correct the Log entry. Both states are recoverable via snapshot. `$lint` #28 (partial write detection) flags the `"Deepening"` prefix as an indicator — if the corrective entry exists alongside it, lint should downgrade to Nice to Have.

## Phase 6: Update the Vault
1. If new research was substantial, also save a supporting research note to Research/:
   `Research/YYYY-MM-DD - [TICKER] - [Section Topic] Deep Dive.md`
   ```yaml
   ---
   date: YYYY-MM-DD
   tags: [research, deep-dive, TICKER]
   sector: [from thesis]
   ticker: TICKER
   source: vault synthesis
   source_type: deep-dive
   propagated_to: [TICKER]
   ---
   ```
2. Add any new wikilinks to the thesis Related Research section

> **Graph update deferred**: `_graph.md` is now owned exclusively by `$graph`. After this skill, run `$graph last` to register any new research note in the dependency map.

## Phase 7: Update _hot.md

Follow `.agents/skills/_shared/hot-md-contract.md` — compression policy, per-section budgets, truncation-marker avoidance, and cap handling are centralized there. Read `_hot.md` then edit (do NOT touch Latest Sync or Sync Archive — owned by `$sync`):

1. **Active Research Thread**: **Same-ticker continuation** — if the current thread already covers the same primary ticker/topic, append a dated line (`YYYY-MM-DD: [update]`) to the existing thread instead of compressing. **New topic**: compress the outgoing thread into a single `*Previous:*` entry (date + one-phrase summary). Write: deepened [TICKER] [Section Name], key finding, and the logical next research step. Append `*Previous:*` line(s) — max 5, drop oldest.
2. **Recent Conviction Changes**: Add entry if conviction was changed or flagged for reassessment
3. **Open Questions**: Mark resolved any questions this research answered; add new questions raised

**Word cap**: After all `_hot.md` edits, check total word count. If over 8,000 words (soft cap per `.agents/skills/_shared/hot-md-contract.md`), prune `## Sync Archive` entries (oldest first), then `*Previous:*` lines in Active Research Thread (oldest first), until under cap. If over 10,000 (hard cap), abort `_hot.md` update per contract.

## Phase 7.5: Flip deepen manifest to completed (M3 — skeleton → populate → flip)

Manifest skeleton was written at Phase 4.5 with `status: in-progress`. Phase 7.5 populates placeholders and flips status.

**Populate body** (Edit Phase 4.5 skeleton, replacing `*(filled in Phase 7.5 flip)*` placeholders):

```markdown
## Research note created (if any)
- [[Research/YYYY-MM-DD - TICKER - [Section Topic] Deep Dive]]
  *(OR `none — Phase 6 judged new research insubstantial`)*

## Phase 5 Log-append outcome
- succeeded: provisional `Deepening [Section Name] — in progress` replaced by final `Deepened [Section Name]: [key finding] — conviction [impact]`.
  *(OR `provisional-entry-stuck + correction-appended: final Log entry written as corrective ↳ CORRECTION block, provisional text preserved`)*
```

**Flip frontmatter**: `status: in-progress` → `status: completed`. Add `completed_date: YYYY-MM-DD`.

Expected frontmatter post-flip:
```yaml
---
type: deepen-manifest
batch: deepen-TICKER-YYYY-MM-DD-HHMMSS
status: completed
ticker: TICKER
section: [Section Name]
date: YYYY-MM-DD
completed_date: YYYY-MM-DD
---
```

**Verify flip landed** (targeted live-file verification): run a targeted frontmatter read against the live file after applying the patch. Do not rely only on the patch operation's success status. Confirm `status: completed` present, `status: in-progress` absent, `completed_date:` equals today from the targeted verification output.

**On verification failure** (targeted verification indicates replacement did not produce expected frontmatter, or patch operation returned an error): report `⚠️ Deepen manifest status flip failed — manifest remains status: in-progress despite successful deepen completion. $lint #50m will flag this as Important. Manual fix: edit manifest frontmatter — replace status: in-progress with status: completed (add completed_date: today).` Continue to Phase 8.

## Phase 8: Report
Tell the user:
- Which section was deepened and why it was the priority
- Snapshot saved to: `[[_Archive/Snapshots/...]]`
- The 2-3 most important new findings
- Section-growth check: compare the target section's pre-deepen word count (from the Phase 4 snapshot) against its post-deepen count. If it grew >1.5×, emit `⚠️ [Section] grew [N]→[M] words (>1.5×) — verify the additions are signal, not accretion; consider trimming`. Repeated deepens accrete; this surfaces bloat before it compounds (no flag when ≤1.5×).
- `Mental-model trigger delta: fired/retired/changed: […] | none` (from the Phase 1 gate — one line, always present)
- `Trigger touch: [TICKER] → "[verbatim trigger]" — [datapoint] ([CROSSED | approaching | evidence-touched, dir=…])` — emit per `.agents/skills/_shared/trigger-touch.md` when Phase 3 research surfaces a datapoint bearing on a `## Conviction Triggers` entry; a `--sync-metrics` run that moves a numeric value across a registered threshold follows the contract's numeric path. Flag-only — never auto-execute `$status` (Tier-3).
- Whether conviction should be reassessed based on what was found
- Theses requiring `$sync`: [list any tickers where cross-references suggest propagation is needed]
- **Run `$sync` to propagate these findings to affected sector notes, macro notes, and cross-thesis references.**
