---
name: numbers
description: Refresh the Key Metrics table in a thesis with current data from Financial Modeling Prep, with a scoped web-search fallback (Step 4b) when FMP has no data or resolved the wrong company. Use when user says "numbers", "refresh metrics", "update key metrics", or "refresh [TICKER]" with no other action implied. Surgical edit only — does NOT create research notes or propagate via $sync. Also flags (never auto-edits) stale price/valuation framing in the thesis Summary — see Step 10b.
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$numbers`, or infer them from the user's request when this skill is invoked implicitly.

Refresh the **`## Key Metrics`** table in a thesis using live FMP data, with a narrow, provenance-tagged web-search fallback for specific FMP gaps (Step 4b). Hygiene operation, not analysis — the skill changes only numeric cells, never the Notes column, never section text, never frontmatter analytical fields. Solves the staleness problem where every thesis's metrics are wrong 90 days after creation. It also *flags* (read-only, single-ticker mode) stale price/valuation language in the thesis Summary via Step 10b — detection only, prose is never auto-edited (Design constraint #8).

**This skill creates no research notes and emits a skill-origin Log prefix — `$sync` will NOT re-propagate to sector or macro notes.** If the refresh surfaces a material delta (e.g., gross margin dropped 500bps), the skill advises the user to follow up with `$deepen` or `$sync` manually.

## Arguments

`SKILL_ARGS` should match one of:

- **Single ticker**: `NVDA` — refresh one thesis
- **All active high-conviction**: `--all` — batch refresh every thesis where `status: active` AND `conviction: high`
- **All active**: `--all-active` — batch refresh every thesis where `status: active` (any conviction)
- **All open (any status except closed)**: `--all-open` — batch refresh every thesis where `status` is `active`, `monitoring`, or `draft` (any conviction). Always excludes `status: closed` regardless of mode — see Design constraint #9 and Recommended frequency.

Ambiguous / empty → ask user to clarify ticker or batch scope.

## Step 0: Pre-flight (MANDATORY)

### 0.1: Acquire vault lock

Per `.agents/skills/_shared/preflight.md` Procedure 1:
- **Single ticker**: `ticker:TICKER` scope. Timeout 3 minutes.
- **`--all` / `--all-active` / `--all-open`**: `vault-wide` scope. Timeout 10 minutes (one API cycle per ticker × N tickers, even at FMP wholesale tier). `--all-open` covers the largest N — pad timeout expectations accordingly if the vault has grown.

Capture token at Step 0.1, verify ownership (Procedure 1.5) at every subsequent shell block, release explicitly in the final block (Step 12).

### 0.2: Rename-marker pre-flight

Procedure 2.
- **Single ticker**: hard-block if `.rename_incomplete.TICKER` exists.
- **Batch modes**: glob `.rename_incomplete.*`; hard-block on any marker. Refresh would write to thesis files whose inbound wikilinks are still split mid-rename — surface for user resolution before proceeding.

### 0.3: FMP API key probe

```bash
if [ ! -f .data/config.json ]; then
  echo "❌ FMP API key config missing: .data/config.json"
  echo "   This skill requires .data/config.json containing fmp_api_key. See Live Portfolio.md for the canonical format."
  exit 1
fi
# jq (already used by this workflow) — the prior `sed -E 's/...\s.../'` relied on GNU `\s`,
# unsupported by BSD/macOS sed: it returned the whole JSON line as API_KEY, passed the
# guard, then every curl exited rc=3 on a malformed URL.
API_KEY=$(jq -r '.fmp_api_key // empty' .data/config.json)
if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
  echo "❌ FMP API key missing or empty in .data/config.json"
  exit 1
fi
echo "FMP_KEY_OK"
```

On failure, abort the entire skill — no fallback to web scraping. (This is a total-failure guard: no FMP key means no run at all. It does not conflict with Step 4b's narrower, per-field web-search fallback, which only engages after a successful FMP connection for specific gapped/mismatched fields on individual tickers — see Step 4b.)

### 0.4: Section existence probe (per-thesis)

For every target thesis, run Procedure 4 against the `## Key Metrics` heading:

- **Hard abort** if missing on single-ticker mode: `❌ Section "## Key Metrics" not found in [path]. $numbers refreshes existing tables only — it does NOT create the section. Add the table manually (use Templates/Thesis Template.md as reference) then re-run $numbers.`
- **Graceful skip** in batch modes: log `ℹ️ [TICKER] missing ## Key Metrics — skipped.` and continue. Report skip count in final summary.

## Step 1: Resolve target thesis files

### Single ticker mode

```bash
ls "Theses/$TICKER - "*.md 2>/dev/null
```

- 0 matches → `❌ No thesis found for [TICKER] in Theses/. Run $thesis [TICKER] first.`
- 1 match → proceed.
- 2+ matches → `❌ Ambiguous ticker [TICKER] — multiple thesis files match. Disambiguate manually.`

### Batch modes

```bash
# Filter theses by frontmatter
for f in Theses/*.md; do
  status=$(awk '/^---/{c++; if(c==2) exit} c==1 && /^status:/{print $2}' "$f")
  conviction=$(awk '/^---/{c++; if(c==2) exit} c==1 && /^conviction:/{print $2}' "$f")
  if [ "$MODE" = "--all-open" ]; then
    # any status except closed (and except missing/malformed status) — never conviction-filtered
    if [ -z "$status" ] || [ "$status" = "closed" ]; then continue; fi
    echo "$f"
    continue
  fi
  if [ "$status" = "active" ]; then
    # --all → only high-conviction
    # --all-active → any conviction
    if [ "$MODE" = "--all" ] && [ "$conviction" != "high" ]; then continue; fi
    echo "$f"
  fi
done
```

Output a deterministic list of targets. Empty list → `ℹ️ No theses match filter. Nothing to refresh.` Exit cleanly (release lock).

## Step 2: Parse existing Key Metrics table

For each target thesis, read the `## Key Metrics` section. Parse every body row (skip the header row and the separator row). For each row capture:

| Field | Notes |
|---|---|
| `metric_label` | Cell 1 verbatim (e.g., `Market Cap`, `EV/Revenue (TTM)`, `Forward P/E`) |
| `value_raw` | Cell 2 verbatim (e.g., `~$4.6T`, `18.3x`, `+65% YoY`) |
| `notes_raw` | Cell 3 verbatim — **MUST be preserved unchanged** through the entire flow |
| `format_hints` | Parsed from `value_raw`: tilde prefix, sign prefix, currency symbol, magnitude letter (T/B/M/K), decimal precision, suffix (`x`, `%`, ` YoY`, ` TTM`) |

The skill's edit operations target the **Value cell only**. Notes cells are pass-through. Metric labels are pass-through (the skill does not rename rows or reorder them).

## Step 3: Map metric labels to FMP fields

**Script-first (2026-07-08):** the label→field mapping (Step 3) AND the delta/materiality math (Step 5) are deterministic — after the Step 4 fetch lands the JSON, run the helper instead of doing the arithmetic by hand:

```bash
# rows.tsv: one line per existing Key Metrics row, tab-separated  label<TAB>value_raw
python3 .agents/skills/numbers/scripts/numbers_compute.py \
  --json-dir /tmp/numbers_${TICKER} --rows-file /tmp/numbers_${TICKER}_rows.tsv
```

(Place the six Step 4 curl outputs in `/tmp/numbers_${TICKER}/` as `quote.json ratios.json km.json growth.json income.json est.json`.) It emits a JSON array, one object per row: `status` (mapped | skipped | fetch_gap), `new_value_numeric`, `old_value_numeric`, `delta`, `delta_type` (pct/pp/abs), `material` (bool, per the Step 5 thresholds), and a `format_hint`. Derived metrics (Forward P/E, FCF Margin, FY Revenue) and the fraction→percent conversion are handled. Custom metrics with no mapping come back `status: skipped` — leave them untouched (Step 3 skip rule).

**The LLM renders the final formatted cell from `new_value_numeric` + `format_hint`** — this is deliberately NOT scripted because currency preservation (KRW/JPY/GBp/EUR, `~` prefixes, magnitude/precision conventions) carries correctness risk in thesis content. The mapping table and threshold table below are the reference spec the script implements. Maintain an internal mapping table. Match is case-insensitive on the label after stripping parenthetical qualifiers like `(TTM)`, `(GAAP)`, `(Non-GAAP)`:

| Canonical label | FMP endpoint + field | Format default |
|---|---|---|
| `Market Cap`, `Market Capitalization` | `/stable/quote` → `marketCap` | `$X.XT` / `$XB` (magnitude-scale on USD; native currency for non-USD) |
| `Stock Price`, `Price`, `Share Price` | `/stable/quote` → `price` | `$X.XX` (USD) / native unit |
| `EV/Revenue`, `EV/Sales` | `/stable/ratios-ttm` → `evToSalesTTM` (or `enterpriseValueOverRevenueTTM` if present) | `X.Xx` |
| `EV/EBITDA` | `/stable/ratios-ttm` → `evToEbitdaTTM` (or `enterpriseValueOverEBITDATTM`) | `X.Xx` |
| `Trailing P/E`, `P/E`, `P/E (TTM)` | `/stable/ratios-ttm` → `peRatioTTM` | `X.Xx` |
| `Forward P/E`, `P/E (Forward)`, `NTM P/E` | derived: `quote.price ÷ analyst-estimates.eps (next FY)` | `X.Xx` |
| `Revenue Growth`, `Revenue Growth (YoY)`, `Sales Growth` | `/stable/income-statement-growth` → most-recent annual `growthRevenue` | `+X.X% YoY` |
| `Gross Margin`, `Gross Margin (GAAP)` | `/stable/ratios-ttm` → `grossProfitMarginTTM` | `XX.X%` |
| `Operating Margin`, `Op Margin` | `/stable/ratios-ttm` → `operatingProfitMarginTTM` | `XX.X%` |
| `Net Margin` | `/stable/ratios-ttm` → `netProfitMarginTTM` | `XX.X%` |
| `FCF Yield`, `Free Cash Flow Yield` | `/stable/key-metrics-ttm` → `freeCashFlowYieldTTM` | `X.X%` |
| `FCF Margin`, `Free Cash Flow Margin` | derived: `freeCashFlowTTM ÷ revenueTTM` | `XX.X%` |
| `Net Debt / EBITDA`, `Leverage` | `/stable/key-metrics-ttm` → `netDebtToEBITDATTM` | `X.Xx` |
| `Dividend Yield` | `/stable/ratios-ttm` → `dividendYieldTTM` | `X.X%` |
| `FY[YYYY] Revenue`, `[YYYY] Revenue` | `/stable/income-statement?period=annual` → matching FY's `revenue` | `$X.XB` |

**Anything not in this table is skipped.** Custom user-defined metrics (e.g., `Q1 FY2027 Guidance`, `Data Center Revenue`, `Sovereign AI Bookings`) have no FMP mapping — leave them untouched and report in the per-thesis output: `⏭ Skipped: [N] custom metrics with no FMP mapping — refresh manually if needed: [list of labels]`.

**Format-detection-overrides-default**: if `value_raw` parsing reveals a non-default format (e.g., user wrote `$215.9B` for FY2026 Revenue rather than `$0.2T`), reuse the detected format precisely — only swap the numeric portion.

## Step 4: Fetch FMP data (one parallel batch per ticker)

**Resolve the FMP symbol per thesis (foreign-listing catch-22 fix).** FMP needs an exchange-suffixed symbol for non-US listings (`6981.T`, `2383.TW`, `GAW.L`, `AIXA.DE`, `5332.T`) but the filename ticker is the bare local code or a display ticker. Resolve from the thesis frontmatter, preferring an explicit `fmp_symbol:` field, falling back to `ticker:` (never the filename):

```bash
FMP_SYMBOL=$(grep -m1 '^fmp_symbol:' "$THESIS_PATH" | sed 's/^fmp_symbol:[[:space:]]*//')
[ -z "$FMP_SYMBOL" ] && FMP_SYMBOL=$(grep -m1 '^ticker:' "$THESIS_PATH" | sed 's/^ticker:[[:space:]]*//' | tr -d '[]' | awk '{print $1}')
[ -z "$FMP_SYMBOL" ] && { echo "⚠️ [TICKER] no ticker:/fmp_symbol: — skipping FMP fetch"; }  # batch: skip; single: abort
RAW_TICKER="$FMP_SYMBOL"   # every FMP call below uses this, NOT the bare filename ticker
```

Theses whose `ticker:` already carries the FMP suffix (`6857.T`, `000660.KS`, `285A.T`) resolve through the fallback; the rest carry `fmp_symbol:` overrides (added 2026-07-09: 2383→2383.TW, 6981→6981.T, GAW→GAW.L, 5332/TOTO→5332.T, AIXA→AIXA.DE). An empty FMP array after resolution → `skipped-forward` / `fetch_gap` handling as before, but now a foreign ticker actually resolves instead of querying a bare code that returns `[]`.

Per ticker, issue parallel curl calls:

```bash
TICKER_URL=$(printf '%s' "$RAW_TICKER" | jq -sRr @uri)
BASE="https://financialmodelingprep.com/stable"
# Write into the DIRECTORY the script reads (--json-dir /tmp/numbers_${TICKER}),
# not flat /tmp/numbers_${TICKER}_*.json files — the flat form left the script's
# json-dir empty, so every row came back fetch_gap.
mkdir -p /tmp/numbers_${TICKER}
D=/tmp/numbers_${TICKER}

curl -sf "$BASE/quote?symbol=$TICKER_URL&apikey=$API_KEY" > "$D/quote.json" &
curl -sf "$BASE/ratios-ttm?symbol=$TICKER_URL&apikey=$API_KEY" > "$D/ratios.json" &
curl -sf "$BASE/key-metrics-ttm?symbol=$TICKER_URL&apikey=$API_KEY" > "$D/km.json" &
curl -sf "$BASE/income-statement-growth?symbol=$TICKER_URL&apikey=$API_KEY" > "$D/growth.json" &
curl -sf "$BASE/income-statement?symbol=$TICKER_URL&period=annual&limit=3&apikey=$API_KEY" > "$D/income.json" &
# Forward P/E only if Forward P/E is in the parsed table — guard the call
curl -sf "$BASE/analyst-estimates?symbol=$TICKER_URL&period=annual&apikey=$API_KEY" > "$D/est.json" &
wait
```

**API failure handling**:
- HTTP error (4xx/5xx, non-empty stderr): retry once after 2s.
- Second failure: skip this ticker, report `⚠️ [TICKER] FMP fetch failed: [endpoint] [status]. Skipping refresh.` Continue to next ticker in batch mode; abort in single mode.
- Empty JSON array `[]` (FMP "no data" pattern): same as failure — FMP doesn't always return 404 for unknown tickers.

**Currency handling**:
- FMP returns market cap and revenue in the listing's native currency (KRW for `000660.KS`, JPY for `6981.T`, GBp for `GAW.L`, EUR for `BESI.AS`, etc. — confirmed via Live Portfolio).
- Format magnitude with the existing thesis's convention: if `value_raw` used `$X.XT`, output `$X.XT`; if it used `¥XB` or `£X.XB` or no currency symbol, preserve that.

## Step 4b: Web-search fallback for FMP data gaps (added 2026-07-12)

**Trigger conditions are mechanical — never "the number looks surprising."** A large real delta (a stock re-rating 100%+, a margin swinging double digits) is signal, not an error — Step 5's materiality thresholds exist precisely to surface those, and treating "big delta" as a fallback trigger would misfire on genuine moves (confirmed live in the 2026-07-12 `--all-open` batch: 6981, TER, SNDK, and 285A all had legitimate 100%+ market-cap deltas that were correctly applied, not search-worthy anomalies). Web search fires ONLY on:

1. **`status: fetch_gap`** on one of the search-friendly fields (allowlist below) — FMP returned null/empty for this ticker+field, i.e. an actual gap, not a present-but-disputed value.
2. **Name mismatch** — `quote.json`'s `name` field does not match the thesis's company name (fuzzy-match against the filename's `- Name` portion, or a `company_name:` frontmatter field if one exists). This is a near-certain ticker-collision signal, confirmed this session: bare `CSU` / `SOI` / `SIVE` resolved to unrelated micro-caps ("Capital Senior Living Corporation," "Solaris Oilfield Infrastructure, Inc.," "Silver Verde May Mining Co., Inc.") instead of Constellation Software / Soitec / Sivers Semiconductors. On a name mismatch, treat ALL of that ticker's FMP-sourced fields this run as untrustworthy — attempt web search for the allowlisted fields below; leave the rest `fetch_gap` (do not fabricate) and note in the Log entry that `fmp_symbol:` likely needs a manual override (this is very often the real fix — check first whether an exchange-suffixed symbol resolves correctly before trusting any web-search result for a mismatched ticker).

**Field allowlist — do not search for everything.** Only attempt fallback for: `Market Cap`, `Stock Price`, `Trailing P/E`, `Forward P/E`, `EV/Revenue`, `EV/EBITDA`. These are reliably surfaced by financial-data aggregator sites in a search snippet without deep extraction. Do **NOT** attempt fallback for margins, FCF Yield/Margin, Net Debt/EBITDA, Dividend Yield, or Revenue Growth — these require a specific accounting-period/GAAP-vs-non-GAAP match that a generic search snippet cannot reliably disambiguate. (This run's margin swings on PSTG/PANW/ARM/CRWD/PCOR were GAAP-vs-non-GAAP methodology mismatches, not missing data — a second unstructured source would not have resolved which convention the thesis wants, it would have added a second unreliable opinion arguing with the first.) Rows outside the allowlist that hit fetch_gap or ride along on a name-mismatched ticker stay `fetch_gap`/untouched — unchanged from current behavior.

**Execution, per triggered (ticker, field):**
1. One `web search` call, field-appropriate query (`"{company name} market cap"`, `"{company name} stock price"`, `"{company name} EV/Revenue"`, etc.). Prefer reading the figure directly out of aggregator-style snippets (stockanalysis.com, companiesmarketcap.com, macrotrends.net, Google Finance) that surface the number without a full page load.
2. If the snippet is ambiguous, conflicting across sources, or absent: ONE follow-up `web fetch/open` on the most authoritative-looking result. Do not chain further searches — one search plus at most one fetch, then decide.
3. If a confident single number still isn't obtainable (sources disagree materially, or nothing relevant surfaces): do **not** force a low-confidence number in. Fall back to the existing safe behavior — leave as `fetch_gap`, note `web search inconclusive` in the Log entry. Mirrors Step 4's own retry-then-give-up discipline.
4. Render the value with the same format-preservation rules as Step 3/8 (currency, tilde, decimals, magnitude suffix) — a web-filled cell must look identical in style to an FMP-filled one; only its provenance tag (below) marks the difference.
5. Feed the rendered value through Step 5's existing materiality thresholds exactly like an FMP-sourced value — no separate threshold table for web-filled rows.

**Provenance tagging is mandatory — a web-filled cell must never be silently indistinguishable from an FMP-sourced one:**
- The Log entry (Step 9) must name every web-filled row explicitly and cite the source, e.g.: `Numbers refresh: 6 metrics updated (5 FMP, 1 web: EV/Revenue via stockanalysis.com). ...` — never folded into the plain count unmarked.
- Never write the source URL into the Notes cell — Design constraint #1 still applies unconditionally. Provenance lives in the Log entry only.
- The Step 12 report (single and batch) carries a dedicated **Web-search-filled** section (see Step 12) — these rows are never buried inside the generic "metrics refreshed" count.

**Single-ticker mode: always pause for confirmation if any row was web-filled**, regardless of whether the resulting delta clears Step 5's materiality bar — extend Step 6's confirm gate with an OR condition (material delta present) OR (any Step 4b row present). Web-sourced values carry more extraction risk than FMP's structured response and earn a first-time human glance even when the number itself looks unremarkable. Batch modes: no per-ticker prompt (same as Step 6) — web-filled rows accumulate into the Step 12 aggregate report instead.

**Scope discipline**: single web-search attempt per (ticker, field) — no retry loops burning time/tokens on what is meant to be a hygiene operation. Never attempted for a ticker with no fetch_gap and no name-mismatch — most tickers hit neither trigger and this step is a no-op for them.

## Step 5: Compute deltas and classify materiality

For every row that mapped successfully:

| Metric | Δ classification | Material if |
|---|---|---|
| Market Cap | percent change | \|Δ\| > 25% |
| Stock Price | percent change | \|Δ\| > 25% (usually moves with Market Cap; redundant — pick one anchor) |
| Revenue Growth | percentage-point change | \|Δ\| > 10pp |
| Gross Margin | percentage-point change | \|Δ\| > 3pp |
| Operating Margin | percentage-point change | \|Δ\| > 3pp |
| Net Margin | percentage-point change | \|Δ\| > 3pp |
| FCF Yield | percentage-point change | \|Δ\| > 1pp |
| FCF Margin | percentage-point change | \|Δ\| > 3pp |
| EV/Revenue, EV/EBITDA, P/E | percent change | \|Δ\| > 25% |
| Net Debt / EBITDA | absolute change | \|Δ\| > 0.5x |
| FY Revenue | percent change | \|Δ\| > 5% |
| Dividend Yield | percentage-point change | \|Δ\| > 0.5pp |

Aggregate per-thesis: `material_count`, `material_metrics: [list of labels]`. Used in Step 6 (user confirmation), Step 9 (Log entry text), and Step 10 (advisories).

## Step 5b: Conviction-trigger touch check (per `.agents/skills/_shared/trigger-touch.md`)

The deltas from Step 5 are the exact data a thesis's pre-registered numeric triggers test. `$numbers` is the primary/concrete consumer of the trigger-touch contract — it holds `old_value_numeric` + `new_value_numeric` for every row and can mechanically check whether a refresh moved a metric across a `→ HIGH/LOW/CLOSE if` threshold. Without this, a trigger that has quietly fired sits unnoticed until the next human review.

**Read the triggers.** Probe for `## Conviction Triggers` (Procedure 4). Absent or scaffold-empty → skip this step silently and note `no triggers to test` in the Step 12 report (a `$lint #60` gap, not a `$numbers` error). Present → read the section (a targeted section read; do not full-read the thesis).

**Parse + diff (numeric handles only).** Per the trigger-touch contract, extract each trigger's numeric threshold (number + comparator: `GM < 42%`, `net debt/EBITDA > 2.0x`, `revenue growth below 20%`, `share ≥ 60%`). Map each threshold to a refreshed Key-Metrics row where the metric matches. For each mapped trigger, classify using Step 5's numbers:
- **CROSSED** — the refreshed value is now on the trigger side of the threshold (e.g. trigger `→ LOW if GM < 44%`, GM refreshed 47.1%→43.6%).
- **approaching** — the value moved ≥ halfway toward the threshold from its old value this run but has not crossed.
- **no-touch** — otherwise.

Named-observable triggers (no number — `loses the Apple N2 anchor`, `Maia 2 launch`) are out of scope for `$numbers` (no metric tests them); leave them to `$transcript`/`$sync`/`$deepen` per the contract.

**Flag-only — never edit `conviction:`.** A trigger crossing is a Tier-3 conviction signal (AGENTS.md); `$numbers` surfaces it, the user decides via `$status`. Same discipline as Design constraint #8 (never auto-edit argument-coupled state).

Store `trigger_crossings: [{ticker, trigger_verbatim, metric, old, new, class}]` for Step 6 (presentation), Step 9b (register write), and Step 12 (report). A `CROSSED` result is the strongest single output this skill produces — never let it ride silently inside the plain metric count.

## Step 6: Present deltas; confirm if material

**Single ticker, no material deltas AND no Step 4b web-filled rows**: skip confirmation; proceed silently to Step 7.

**Single ticker, ≥1 material delta OR ≥1 Step 4b web-filled row present** (whichever fires first — a web-filled row forces the pause even if its own delta is immaterial, per Step 4b): pause and present:

```
[TICKER] Key Metrics — proposed updates:

| Metric         | Old      | New      | Δ        | Material | Source |
|---|---|---|---|---|---|
| Market Cap     | ~$4.6T   | ~$5.8T   | +26.1%   | ⚠️       | FMP    |
| EV/Revenue     | 18.3x    | 16.2x    | -2.1x    |          | FMP    |
| Revenue Growth | +65% YoY | +42% YoY | -23pp    | ⚠️       | FMP    |
| Gross Margin   | 71.1%    | 71.4%    | +0.3pp   |          | FMP    |
| Trailing P/E   | 22.0x    | 24.5x    | +11.4%   |          | web (stockanalysis.com) |

⚠️ 2 material deltas — review before applying.
⚠️ 1 row web-search-filled (Step 4b: FMP fetch_gap) — confirm gate triggered regardless of materiality.
🎯 CONVICTION TRIGGER CROSSED — "→ LOW if gross margin < 44%": GM refreshed 47.1%→43.6%. Flag-only; consider $status after applying.
Notes column unchanged. Skipped: 5 custom metrics with no FMP mapping.

Confirm? (y/n)
```

Surface the `🎯 CONVICTION TRIGGER CROSSED` line (from Step 5b `trigger_crossings`) above the `Confirm?` prompt whenever any trigger CROSSED this run — it is the highest-signal output and must never be buried. `approaching` touches are reported in Step 12 only, not escalated to the confirm gate.

The `Source` column is only shown when ≥1 row is web-filled this run — omit it entirely for a pure-FMP refresh (the common case) rather than adding noise every time.

Wait for explicit y/n. (n) → abort cleanly (release lock; no edits).

**Batch modes**: do not prompt per-ticker. Present aggregated material-delta summary at the END of the run (Step 12 report) so the user can decide which theses to `$deepen` or `$sync` after. The batch flow's safety net is the snapshot taken in Step 7.

## Step 7: Snapshot (mandatory)

For every thesis the skill is about to edit, take a snapshot:

```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
cp "Theses/$TICKER - $NAME.md" "_Archive/Snapshots/$TICKER - $NAME (pre-numbers $YYYYMMDD-$HHMMSS).md"
```

Add snapshot frontmatter on the copy:

```yaml
snapshot_of: "[[Theses/TICKER - Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: numbers
snapshot_batch: numbers-YYYY-MM-DD-HHMMSS
```

Batch ID format (single-ticker): `numbers-TICKER-YYYY-MM-DD-HHMMSS`.
Batch ID format (`--all` / `--all-active` / `--all-open`): `numbers-batch-YYYY-MM-DD-HHMMSS` (shared across all theses in the batch — atomic cascade rollback via `$rollback`).

Snapshot is mandatory because the edit touches multiple table rows and a partial-write failure (rare but possible) without rollback path would corrupt the thesis's Key Metrics section.

## Step 8: Apply edits to the Key Metrics table

For each mapped row with a new value:

```
Edit:
  old_string: | [metric_label] | [value_raw] | [notes_raw] |
  new_string: | [metric_label] | [value_new] | [notes_raw] |
```

**Edit batching**: when ≥3 rows need updating in the same thesis, emit all Edits in a single tool-call block as independent parallel invocations. The harness serializes same-file Edits on the server side; this saves N round-trips vs. sequential Edits.

**Validation**: every `old_string` must contain the table-row's exact whitespace and pipe layout as read in Step 2 — no normalization, no whitespace re-collapsing. If the Edit returns `old_string not found`, do NOT retry with a normalized variant; instead abort the per-ticker edit, restore from snapshot, and report `⚠️ [TICKER] table-row Edit failed: row "[metric_label]" had unexpected layout. Snapshot retained at [path]. Skipping refresh.` Continue to next ticker in batch mode.

**Notes-column preservation invariant**: after all edits, re-read the thesis. For every metric row, verify the Notes cell content matches the captured `notes_raw` exactly. Mismatch → restore from snapshot, hard-abort: `❌ Notes column preservation invariant FAILED for [TICKER]. Restored from snapshot. This indicates a parsing bug — please report.`

## Step 9: Append Log entry

Append to the thesis `## Log` section (max 2 lines):

```
### YYYY-MM-DD
- Numbers refresh: [N] metrics updated[, M material]. [single most-significant Δ in plain prose, e.g., "revenue growth decel +65%→+42%"]. Snapshot: [[_Archive/Snapshots/...]]
```

**Prefix `Numbers refresh:` is canonical** — registered in `.agents/skills/_shared/log-prefixes.md` §18 as **skill-origin**. `$sync` Step 2.5 will see this prefix and skip sector / macro re-propagation for the thesis. Drift detection (Step 3e) also excludes it (refresh entries carry no conviction sentiment). Do not change the prefix; `$lint #29` enforces alignment.

When zero material deltas: still write the Log entry — its presence is the audit trail. Example: `Numbers refresh: 7 metrics updated, 0 material. Largest Δ: EV/Revenue 18.3x→16.2x (-11.5%). Snapshot: [[...]]`.

**When ≥1 row was web-filled (Step 4b), the Log entry must name it and its source** — this is not optional, per Step 4b's provenance-tagging rule: `Numbers refresh: 7 metrics updated (6 FMP, 1 web: Trailing P/E via stockanalysis.com), 1 material. Largest Δ: EV/Revenue 18.3x→16.2x (-11.5%). Snapshot: [[...]]`. A web-filled row never rides silently inside the plain "N metrics updated" count.

## Step 9b: Write CROSSED triggers to the open-findings register (per `.agents/skills/_shared/followups-contract.md`)

Runs only when Step 5b produced a `CROSSED` result (never for `approaching` or `no-touch`). A crossed conviction trigger is a durable actionable finding — it must outlive this run's chat report, which is exactly what `_hot.md` cannot guarantee (its Open-Questions cohorts evict after 14 days). `_followups.md` is the persistence layer.

For each `CROSSED` entry in `trigger_crossings`:
1. Read `_followups.md`. It is a durable vault file and normally exists; if absent, create it via Bash `printf` (the followups-contract schema — `$numbers` has no `Write` tool, so use `printf '%s\n' ... > _followups.md`), then Edit.
2. **Dedup** — grep `## Open` for an existing entry on this thesis with a `→ [HIGH|LOW|CLOSE] trigger` finding of the same direction. If present, update its date; do not stack a duplicate.
3. Append (prepend under `## Open`, newest first):
   ```
   - [ ] YYYY-MM-DD · numbers · [[Theses/TICKER - Name]] · [metric] crossed "[verbatim trigger]" → user runs $status or dismisses · src chat
   ```
4. `$status` is the resolver — when the user later executes the matching conviction change, it moves this entry to `## Resolved` (followups-contract resolver rules).

Only runs after the refresh is applied (post-Step 8/9). An aborted refresh (`n` at Step 6) writes nothing to the register. Batch modes write one entry per ticker with a crossing; obey the 50-entry soft cap warning. This is the ONLY file outside `Theses/` + `_Archive/Snapshots/` that `$numbers` writes, and it is append-only — Design constraint #3 (no Research notes) is unaffected.

## Step 10: Material-delta advisories (single-ticker mode only)

After the Log entry lands, if `material_count ≥ 1`, surface targeted suggestions per metric. These are SUGGESTIONS, not auto-executed.

| Material delta | Suggested follow-up |
|---|---|
| Revenue Growth dropped >10pp | `$deepen [TICKER] --section "Bull Case"` (growth slowdown reframes the bull case) |
| Gross Margin dropped >3pp | `$deepen [TICKER] --section "Industry Context"` (pricing power inflection) |
| Operating Margin or FCF Margin dropped >3pp | `$stress-test [TICKER]` (operating leverage thesis at risk) |
| EV/Revenue or P/E compressed >25% | `$brief [TICKER]` (re-evaluate vs. consensus) — possible market disagreement signal |
| Net Debt/EBITDA crossed >2.0x or up >0.5x | `$deepen [TICKER] --section "Risks"` (leverage shift) |
| Forward P/E expanded >25% | `$stress-test [TICKER]` (multiple expansion thesis vulnerable to consensus revision) |

Output these as `→ Consider: [suggestion]` lines in the final report. Never auto-run.

**Skip in batch modes** — batch advisories print in Step 12 aggregate report instead.

## Step 10b: Summary price-framing staleness check (flag-only — never auto-edited)

**Design decision (2026-07-12): thesis body prose is never auto-edited by this skill — detection only.** Numbers embedded in prose are argument-coupled: NVDA's Summary reasons "at ~30x forward P/E... the question is whether the moat justifies the premium" — swap the multiple and the conclusion may no longer follow. The same figure often recurs in a second section (AVGO's "28x forward earnings" appears in both Summary and a separate Industry Context comparison) — an auto-edit that catches one occurrence and misses the other leaves the note self-contradictory. Cross-ticker mentions add entity-resolution risk (a company name used as metaphor — e.g. AVGO's "Android to Nvidia's Apple" — is not a ticker reference). See Design constraint #8. This check exists so staleness gets surfaced, not silently ignored — the fix is a human-reviewed `$deepen`, not a find-and-replace.

**Scope: single-ticker mode only, thesis's own ticker only, `## Summary` section only.** No new FMP calls — reuses Step 4's already-fetched `quote.json`/`ratios.json`. Batch modes fold results into the Step 12 aggregate report instead of a per-ticker line.

1. Probe for `## Summary` (Procedure 4). Absent → skip this check silently (Summary is template-default, not guaranteed present).
2. Scan the section for a price/valuation framing clause — a current price, market cap, or valuation multiple stated for *this* ticker. Typical shape: `"At ~$190 (~$4.6T market cap, ~30x forward P/E)..."` or `"At 28x forward earnings..."`. **Exclude anything that isn't a valuation statement** even if numerically similar — performance/spec comparisons (`"8x-669x faster"`, `"10x lower inference cost"`, `"70% cost reduction"`) are not price or multiple references and must not be flagged. Judgment call, not blind regex: only flag a clause that states this ticker's own current price, market cap, or valuation multiple.
3. No clause found → nothing to report. Clause found → map it to the corresponding Key Metrics field (Stock Price / Market Cap / Forward P/E / EV/Revenue / EV/EBITDA) and compare the old prose figure to the new fetched value using Step 5's existing thresholds (no new thresholds). Below-threshold → do not surface (avoid advisory noise on immaterial drift).
4. Material → append one line to the report (Step 12), never to the thesis Log entry (Step 9 stays table-refresh-only, 2-line cap):
   ```
   → Consider: Summary opens "[verbatim clause]" — live data now ~$[new price] (~$[new cap], ~[new]x fwd P/E). Run `$deepen TICKER --sync-metrics` to reconcile this and any other locations referencing the same figure (prose not auto-edited by $numbers itself — see `$deepen`'s Metric-Sync Mode).
   ```
5. If the same figure also appears verbatim elsewhere in the body (quick grep, not a full re-scan), append: `Also referenced in [section name] — check for consistency if you $deepen.`

**Never**: edit the Summary text or any other section, write anything to the Log entry, resolve or fetch data for any ticker other than the thesis's own subject.

## Step 11: Update `key_metrics_last_refreshed` (frontmatter)

Add or update a frontmatter field:

```yaml
key_metrics_last_refreshed: YYYY-MM-DD
```

If absent, add as the last frontmatter field before the closing `---`. If present, update in place.

This field is consumed by `$lint #61` (staleness check, added 2026-07-14) to flag theses with stale Key Metrics — threshold 90 days: missing or >90d on a `conviction: high` active thesis → Important; >90d elsewhere → Nice to Have. It also remains a visible thesis-level signal in dataview queries.

## Step 12: Release lock and report

Release lock per preflight §1.7 in the final shell block. Then output the report.

### Single ticker report

```
✓ $numbers [TICKER] complete

Thesis updated:    [[Theses/TICKER - Name]]
Snapshot:          [[_Archive/Snapshots/TICKER - Name (pre-numbers YYYY-MM-DD-HHMMSS)]]
Batch ID:          numbers-TICKER-YYYY-MM-DD-HHMMSS

Metrics refreshed:  [N]  ([M] material — see deltas above)
Custom metrics skipped: [K]  ([list of labels, or "none"])
FMP fetch failures:     [F]  ([list, or "none"])
Web-search-filled:      [W]  ([list: label = value (source), or "none"] — Step 4b)
Trigger touches:    [🎯 CROSSED: [trigger] | ⚠️ approaching: [trigger] | none | no triggers to test]  (Step 5b)

Log entry:        appended ("Numbers refresh:")
Propagation:      $sync will SKIP this thesis (skill-origin prefix)
Frontmatter:      key_metrics_last_refreshed: YYYY-MM-DD

→ Consider: [Step 10 + Step 10b advisories, if any]
```

### Batch report

```
✓ $numbers [--all | --all-active | --all-open] complete

Tickers processed:   [total]
  Refreshed cleanly: [N]
  Skipped (no Key Metrics section): [N]
  Failed (FMP errors): [N]

Material-delta theses ([count]):
  [TICKER1]: [top 1-2 material deltas in one line]
  [TICKER2]: [...]
  ...

Sector aggregation ([count] signals, Step 5 — material deltas grouped by thesis sector: frontmatter, no new fetches):
  ⚡ Sector signal: [X] of [Y] [Sector] peers [compressed/expanded] [metric] [>Zpp/>Z%] this run ([TICKER1] [Δ1], [TICKER2] [Δ2], [TICKER3] [Δ3]) — possible sector-wide [pricing/margin/valuation] inflection; consider $scenario or $compare
  [emit ONLY when ≥3 peers in one sector moved the SAME metric the SAME direction past its Step 5 threshold; omit the whole section when no sector clears the bar — no noise on idiosyncratic single-ticker moves]

Summary framing stale ([count], Step 10b):
  [TICKER1]: cites ~[old]x, live ~[new]x
  [TICKER2]: [...]

Web-search-filled ([count], Step 4b — verify manually):
  [TICKER1]: [label] = [value] (source: [domain]) — trigger: fetch_gap | name-mismatch
  [TICKER2]: [...]

Conviction-trigger crossings ([count], Step 5b — written to _followups.md):
  [TICKER1]: [metric] crossed "[verbatim trigger]" — consider $status
  [TICKER2]: [...]

Suggested follow-ups (Step 10b flags → `$deepen TICKER --sync-metrics`; material-delta theses → single-ticker $deepen, $stress-test, $brief as appropriate):
  [list, max 5; if more, suggest "Run $numbers TICKER for per-thesis advisories"]

Batch ID:           numbers-batch-YYYY-MM-DD-HHMMSS
Snapshot directory: _Archive/Snapshots/
Rollback:           $rollback numbers-batch-YYYY-MM-DD-HHMMSS (cascade across all touched theses)
```

### Final shell block (lock release)

```bash
LOCK_FILE="<paste-from-Step-0.1>"
EXPECTED_TOKEN="<paste-token-captured-from-Step-0.1>"
if [ -f "$LOCK_FILE" ] && grep -q "token: $EXPECTED_TOKEN" "$LOCK_FILE"; then
  rm -f "$LOCK_FILE" && echo "=== LOCK RELEASED ($LOCK_FILE) ==="
else
  echo "⚠️ Lock ownership check failed at release — skipping rm."
fi
# Clean up FMP temp files — the per-ticker DIRECTORY (/tmp/numbers_TICKER/) and
# the rows file, not just flat *.json (which the dir layout no longer produces).
rm -rf /tmp/numbers_*
```

Runs unconditionally — whether all targets refreshed cleanly, some failed FMP fetches, or section-existence-probe excluded some theses.

## Recommended frequency

- **`conviction: high` theses**: monthly. Capital concentrated here moves with the numbers — a 20%+ market-cap drift, a 10pp revenue-growth deceleration, or a 300bps margin compression is a real signal. Pair with `/loop 1m $numbers --all` if the user wants automated recurrence.
- **`conviction: medium` theses**: quarterly (post-earnings). Lower stakes; the qualitative thesis hasn't reached the conviction inflection where every quarterly number matters.
- **`conviction: low` theses**: opportunistically (when running `$surface`, `$prune`, or `$brief`). Keep numbers fresh only when actively reviewing.
- **`status: monitoring` theses**: monthly is fine — the watchlist exists to catch inflections, and stale Key Metrics defeat the purpose.
- **`status: draft` theses**: opportunistically — same as low conviction. Draft theses in this vault are frequently full-depth (not stubs), so a stale Key Metrics table is a real cost, but they haven't been promoted to active tracking either.
- **`status: closed` theses**: never. Closed theses are archived; their Key Metrics tables are historical records — enforced structurally, not just recommended: `--all-open` excludes `status: closed` unconditionally (Design constraint #9), and no batch mode ever includes it.

`--all-open` is the single command that respects this whole cadence table in one run (active + monitoring + draft, any conviction) except closed, which no mode ever touches. This cadence is the basis for `$sync` Step 3e's drift-window exclusion of `Numbers refresh:` entries (per `.agents/skills/_shared/log-prefixes.md` §18) — monthly refresh on a high-conviction thesis would otherwise consume every slot of the 5-entry drift window.

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **Never edit a Notes column cell.** The Notes column holds the user's analytical context — `data center segment +217% YoY`, `multiple compression risk`, `up from 65% pre-AI cycle`. Overwriting it destroys the thesis's interpretive layer. Validated by Step 8's post-edit invariant check.

2. **Never create a `## Key Metrics` section.** If absent, skip (batch) or hard-abort (single) per Step 0.4. Structural thesis changes require explicit user action.

3. **Never create a Research note.** The Log entry IS the audit trail. A refresh has no source URL, no qualitative claim, nothing to remember beyond the snapshot. Polluting `/Research/` with N refresh notes per quarter destroys the folder's signal-to-noise.

4. **Never reorder or rename metric rows.** The skill is row-value-cell-only. If a user has `EV/Revenue` and `EV/Revenue (TTM)` as separate rows (e.g., as a record of methodology change), the skill matches and refreshes both independently.

5. **Never propagate via $sync.** The `Numbers refresh:` prefix is skill-origin (registry §18). Material deltas surface as advisories for the user to act on — auto-propagation of routine metric refreshes would flood sector notes with "TICKER market cap updated" entries.

6. **Wholesale tier is the assumed entitlement.** The skill issues 6 endpoint calls per ticker in parallel; lower FMP tiers may rate-limit. Add per-ticker retry logic but do not silently downshift to fewer endpoints — that produces silently-incomplete refreshes.

7. **Snapshot before every per-thesis edit.** Even though the edit is small, partial-write recovery is the rollback path. Snapshot is the only guarantee that the user can `$rollback` if a Notes-column invariant trips.

8. **Never auto-edit thesis body prose.** Step 10b flags Summary price/valuation staleness — it never rewrites the sentence. Numbers embedded in prose reason toward a conclusion (unlike an inert table cell) and often recur in a second section; silent find-and-replace risks an internally contradictory thesis, and for cross-ticker mentions risks false-positive entity resolution (a company name used as metaphor, not a ticker reference). Considered and explicitly scoped down from "auto-edit all referenced tickers" to flag-only on 2026-07-12 at the user's direction — if full auto-edit is reconsidered later, it belongs in a new skill with mandatory per-file human review (`$deepen`-shaped), not inside `$numbers`.

9. **No batch mode ever includes `status: closed`.** `--all-open` was added 2026-07-12 to broaden batch refresh beyond `status: active` (to `active` + `monitoring` + `draft`, any conviction) — it does not broaden it to *every* thesis file. Closed theses hold their Key Metrics table as a historical record of the position at closure (Recommended frequency, above); refreshing it would silently overwrite that record with numbers from after the position was exited. If a future request asks for closed theses too, treat it as reopening this exact constraint, not a bug — confirm explicitly before implementing, since it reverses a deliberate, documented choice rather than extending one.

10. **Step 4b's web-search fallback is scope-limited by design — widening it silently is a regression, not an improvement.** Added 2026-07-12 at the user's explicit direction after a root-cause check showed that same day's `--all-open` batch "data quality issues" (CSU/SOI/SIVE market caps off 10-160x, GAW's GBp scale, KAMBI's ~100% gross margin, PSTG/PANW/ARM/CRWD/PCOR margin swings) were actually ticker collisions, an already-documented currency convention, correct-but-surprising data, and GAAP-vs-non-GAAP methodology differences respectively — zero of which a web search would have fixed, and two of which (the margin mismatches) a second unstructured source could easily make *worse* by supplying a plausible-looking wrong number with no FMP-vs-web disagreement signal to catch it. The guardrails below are load-bearing, not incidental:
    - Trigger ONLY on `status: fetch_gap` or a confirmed `quote.name` mismatch — never on "the delta looks big," since large real deltas (this vault has seen genuine 100-285% moves) are signal, not error.
    - Field allowlist ONLY (`Market Cap`, `Stock Price`, `Trailing P/E`, `Forward P/E`, `EV/Revenue`, `EV/EBITDA`) — never margins, yields, leverage, or growth rates, which need period/convention context a search snippet can't carry.
    - One search + at most one fetch per (ticker, field), then give up to `fetch_gap` rather than force a low-confidence number — no retry loops.
    - Provenance tag mandatory in the Log entry and Step 12 report for every web-filled row, every time — never silently indistinguishable from FMP-sourced data.
    - Single-ticker confirm gate fires on ANY web-filled row regardless of materiality (Step 6) — the one data source in this skill without a structured-API correctness guarantee always gets a first human look before it lands.
    
    If a future change proposes dropping any of these five guardrails (broader triggers, more fields, more retries, no provenance tag, no confirm gate), treat that as reopening this constraint deliberately — not a routine extension.
