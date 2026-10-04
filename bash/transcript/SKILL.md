---
name: transcript
description: Pull an earnings call (or investor-event) transcript from Quartr (FMP fallback), extract qualitative signal (management commentary deltas, hedging shifts, Q&A tone), and produce a thesis-delta-first Research note. Use when user says "transcript", "pull earnings call", "transcript diff", or "ingest [TICKER] earnings".
model: opus
effort: max
allowed-tools: Read Grep Glob Edit Write ToolSearch mcp__quartr Bash(date * cp * mkdir * ls * curl * grep * cat * jq * printf * awk * sed * wc * python3 *)
---

Convert an earnings-call transcript into a thesis-delta-first Research note. **Quartr MCP is the primary transcript source** (per `.claude/skills/_shared/quartr.md` — exact prepared/Q&A split, exact speaker roles making the evasiveness signal reliably computable, timestamped paragraph deep-links for quotes, and coverage of non-earnings events FMP lacks entirely: investor updates, CMDs, firesides); **FMP is the fallback** when Quartr is unavailable or misses the company/quarter (2026-09-09 migration). Pulls the target quarter's transcript plus the prior 2 quarters for delta analysis. Extracts qualitative signals — new/dropped management language, hedging shifts, Q&A skepticism, specificity changes — then cross-references against the thesis's Bull Case, Bear Case, and Conviction Triggers. Writes a Research note, appends a Log entry, and suggests `/sync` for propagation.

**This skill creates a research note AND emits a research-driven Log prefix — `/sync` WILL propagate to affected sector and macro notes.** Run `/sync TICKER` and `/graph last` after this skill, in that order.

## Arguments

`$ARGUMENTS` should match one of:

- **Latest quarter**: `NVDA` — fetch the most recent available transcript
- **Specific quarter**: `NVDA Q4-2026` (format: `QN-YYYY` — fiscal year) — fetch a specific quarter
- **Diff two quarters**: `NVDA --diff Q3-2026 Q4-2026` — produce a side-by-side comparison research note (source_type: analyst-report)
- **List available**: `NVDA --list` — read-only; lists every transcript-bearing event Quartr has for the company (earnings AND non-earnings), with dates and transcript availability; falls back to FMP's quarter list when Quartr is unavailable. No writes.
- **Non-earnings event** (Quartr-only, no FMP equivalent): `NVDA --event <eventId>` — ingest an investor update / CMD / fireside / conference transcript. Same pipeline, but no prior-quarter comparators: the signal script runs with 0 priors (absolute densities, no deltas), source_type is `video-transcript`, and the filename is `YYYY-MM-DD - [TICKER] [Event Title] - video-transcript.md`. Find eventIds via `--list`. If Quartr is unavailable, this mode aborts (nothing to fall back to).

Ambiguous / empty → ask user to clarify ticker.

## Step 0: Pre-flight (MANDATORY)

### 0.1: Acquire vault lock

`ticker:TICKER` scope per `.claude/skills/_shared/preflight.md` Procedure 1. Timeout: 10 minutes (transcript pulls + analysis + post-write verification + sector resolution can be slow on long calls). Capture token at Step 0.1, verify ownership (Procedure 1.5) at every subsequent Bash block, release explicitly in the final block (Step 12).

**`--list` mode**: acquire `read-only` lock instead (Procedure 1.2 read-only scope). Skip Steps 5-12; only fetch + display.

### 0.2: Rename-marker pre-flight

Procedure 2. If `.rename_incomplete.TICKER` exists at vault root, hard-block per contract §2.3. The transcript ingest writes a Log entry to the thesis keyed by current filename; mid-rename split would leave Log entries on one name and inbound wikilinks on another.

### 0.3: Thesis-existence probe

```bash
ls "Theses/$TICKER - "*.md 2>/dev/null
```

- 0 matches → `❌ No thesis found for [TICKER] in Theses/. /transcript ingests earnings into an existing investment case — it does NOT create one. Run /thesis [TICKER] first.`
- 1 match → proceed. Capture path as `THESIS_PATH`.
- 2+ matches → `❌ Ambiguous ticker [TICKER] — multiple thesis files match. Disambiguate manually.`

(The bare glob leaks `no matches found` under zsh before `ls` runs; `find Theses -maxdepth 1 -name "$TICKER - *.md"` is the zsh-safe form and its empty output is the 0-match branch.)

`/transcript` deliberately requires a thesis. Earnings transcripts without a thesis to anchor the analysis are noise — use `/ingest` for orphan-earnings content if needed.

### 0.33: Quartr availability probe + company resolution (PRIMARY source)

Per `_shared/quartr.md` §1–§3: load tool schemas via ToolSearch (`select:mcp__quartr__search_companies,mcp__quartr__list_events,mcp__quartr__read_transcript`), then resolve the company: `quartr_id:` frontmatter override → `.data/quartr_ids.json` cache → `search_companies` on the company name from the thesis filename (verify ticker/name + listing-suffix country; write verified hits back to the cache). Outcomes:

- Resolved → `QUARTR_OK=1`, capture `COMPANY_ID`. Steps 1–2 run the Quartr path.
- ToolSearch surfaces no quartr tools, or calls error → `QUARTR_OK=0`, emit `⚠️ Quartr MCP unavailable — falling back to FMP transcripts (legacy path).`
- Tools live but no confident company match → `QUARTR_OK=0` for this run, emit `⚠️ Quartr has no confident match for [TICKER] — falling back to FMP.` (Never take a wrong company; the same collision discipline as the FMP name-mismatch rule.)

### 0.35: Resolve FMP symbol (fallback path + prior-quarter gap-fill)

Runs regardless of `QUARTR_OK` — the FMP symbol is needed whenever any individual quarter falls back to FMP (Step 2), not only in full-fallback mode. FMP needs an exchange-suffixed symbol for non-US listings (`6981.T`, `2383.TW`, `GAW.L`, `AIXA.DE`) but the filename ticker and the invocation `$TICKER` carry the bare local code (`6981`, `2383`) or a display ticker (`TOTO` for `5332`). Resolve the FMP symbol from the thesis frontmatter, **preferring an explicit `fmp_symbol:` field, falling back to `ticker:`** (never the filename):

```bash
FMP_SYMBOL=$(grep -m1 '^fmp_symbol:' "$THESIS_PATH" | sed 's/^fmp_symbol:[[:space:]]*//')
[ -z "$FMP_SYMBOL" ] && FMP_SYMBOL=$(grep -m1 '^ticker:' "$THESIS_PATH" | sed 's/^ticker:[[:space:]]*//' | tr -d '[]' | awk '{print $1}')
[ -z "$FMP_SYMBOL" ] && { echo "❌ No ticker:/fmp_symbol: in $THESIS_PATH — cannot resolve FMP symbol"; exit 1; }
RAW_TICKER="$FMP_SYMBOL"   # every downstream FMP call uses this, NOT the bare $TICKER
echo "FMP_SYMBOL=$FMP_SYMBOL"
```

`$TICKER` (bare) still names cache files, the thesis path, and the Log entry — only the FMP URL uses `$RAW_TICKER`. Theses needing an explicit override carry `fmp_symbol:` in frontmatter (added 2026-07-09: 2383→2383.TW, 6981→6981.T, GAW→GAW.L, 5332/TOTO→5332.T, AIXA→AIXA.DE). Theses whose `ticker:` already carries the FMP suffix (`6857.T`, `000660.KS`, `285A.T`) resolve correctly through the fallback with no override needed.

### 0.4: FMP API key probe (hard-abort only when Quartr is down)

```bash
if [ ! -f .data/config.json ]; then
  echo "❌ FMP API key config missing: .data/config.json"
  exit 1
fi
# Use jq (already in allowed-tools) — the prior `sed -E 's/...\s.../'` form relied on
# GNU `\s`, unsupported by BSD/macOS sed: it silently returned the WHOLE JSON line as
# API_KEY, passed the `-z` guard, printed FMP_KEY_OK, then every curl exited rc=3 on a
# malformed URL. jq parses the field correctly on every platform.
API_KEY=$(jq -r '.fmp_api_key // empty' .data/config.json)
[ -z "$API_KEY" ] && { echo "❌ FMP API key missing or empty in .data/config.json"; exit 1; }
echo "FMP_KEY_OK"
```

With `QUARTR_OK=1` this probe is **soft**: a missing key downgrades to `FMP_OK=0` (emit `⚠️ no FMP key — prior-quarter gap-fill via FMP disabled`) instead of aborting; the run proceeds Quartr-only. With `QUARTR_OK=0` it remains a hard abort exactly as written above — no source at all is a real failure.

### 0.5: Transcript cache directory

```bash
mkdir -p .data/transcripts
```

Two cache formats coexist (schema: `_shared/quartr.md` §5): Quartr combined caches at `.data/transcripts/TICKER_QN-YYYY.quartr.json` (`TICKER_EVENT<id>.quartr.json` for `--event` mode) and legacy FMP caches at `TICKER_QN-YYYY.json`. **Cache-first order per quarter: `.quartr.json`, then legacy `.json`** — either satisfies the quarter (the signal script auto-detects format; mixed runs are normal). Legacy caches are never rewritten or deleted. Re-runs of `/transcript` on the same quarter read from cache (no API/MCP burn). Cache is gitignored via `.data/` in `.gitignore` (confirmed in Live Portfolio's frontmatter).

## Step 1: Resolve target quarter(s) / event

### Quartr path (`QUARTR_OK=1` — primary)

One call resolves everything at once:

```
mcp__quartr__list_events {companyId: COMPANY_ID, expand: ["transcript"], limit: 20}
```

Filter to `parentEventType: "earnings_call"` (eventTypes `q_1`…`q_4`, also `h_1`/`h_2` for half-year reporters), `upcoming: false`, `transcript.available: true`. Each event carries `title` ("Q2 2026"), `eventType` (`q_2`), `fiscalYear`, `date`, and `id`. Map to the vault's `QN-YYYY` label via `eventType` + `fiscalYear` (NOT by parsing `title`). Sort descending by `date`:

- **Default mode**: target = `[0]` (most recent past earnings event with a transcript).
- **Specific quarter** (`NVDA Q4-2026`): match `eventType: q_4` + `fiscalYear: "2026"`. No match → `⚠️ Quartr has no transcript for [TICKER] Q[N]-[YYYY]` → try the FMP fallback below for THIS quarter before giving up.
- **Diff mode**: two specific-quarter resolutions; both must resolve (via either source); abort otherwise.
- **`--event <id>`**: skip filtering — `mcp__quartr__get_event` on the id to capture title/date; the event must belong to `COMPANY_ID` (abort on mismatch: wrong-company eventIds are a real paste error).
- **Prior 2 quarters** (default + specific modes; not diff/`--event`): the next two transcript-bearing earnings events after the target in the sorted list. Fewer than 2 exist (recent IPO) → proceed degraded, note it in Evidence.

**Edge cases**:
- Zero transcript-bearing earnings events → `⚠️ Quartr has no earnings transcripts for [TICKER]` → full-quarter FMP fallback below.
- Latest is older than 130 days → check upcoming events (`list_events` with `startDate: today` already in hand if `limit` covered it): `ℹ️ Latest transcript is from [date] ([N] days old). Next earnings per Quartr: [date or "unknown"]. Proceeding.`

### FMP fallback path (`QUARTR_OK=0`, or per-quarter Quartr miss; requires `FMP_OK`)

```bash
TICKER_URL=$(printf '%s' "$RAW_TICKER" | jq -sRr @uri)
BASE="https://financialmodelingprep.com/stable"

# List of available transcript dates
curl -sf "$BASE/earning-call-transcript-dates?symbol=$TICKER_URL&apikey=$API_KEY" > /tmp/transcript_dates_${TICKER}.json
```

Parse the response (array of `{quarter, fiscalYear, date}` records sorted descending by `date` — the field is `fiscalYear`, NOT `year`; a `jq .year` parse returns null → malformed fetch URL). Map `fiscalYear` → the `year` parameter of the transcript endpoint. Pick `[0]` as the target quarter (most recent reported). Specific-quarter/diff modes fetch `QN-YYYY` directly as before.

**Both sources empty** → `⚠️ No transcripts available for [TICKER] via Quartr or FMP. Possible causes: (1) non-US listing without earnings-call coverage, (2) coverage gap, (3) company doesn't host public earnings calls. Skill cannot proceed.`

**Fiscal-labeling caveat (mixed-source runs)**: both sources label by fiscal year/quarter and agreed on every checked name (NBIS Q2-2026 = Quartr "Q2 2026" = FMP fiscalYear 2026 quarter 2), but when a prior quarter comes from FMP and the target from Quartr, sanity-check the two dates are ~90 days apart — a mismatch means the fiscal mapping diverged; prefer the source whose date sequence is consistent and note the discrepancy in Evidence.

### `--list` mode

Quartr path — list ALL transcript-bearing events (the non-earnings ones are exactly what FMP cannot see), plus upcoming earnings:

```
[TICKER] — transcript-bearing events via Quartr:
  Q2-2026            2026-08-12  eventId 655490   ← most recent earnings
  Investor update    2026-07-16  eventId 702079   (non-earnings — ingest with --event)
  Q1-2026            2026-05-13  eventId 555850
  ...
  Upcoming: Q3-2026 scheduled 2026-11-10 (no transcript yet)
```

FMP fallback — the legacy quarter list (`QN-YYYY (reported date, ~word count)`). Then release lock and exit. No further steps.

## Step 2: Fetch transcripts (cache-first, per quarter)

Per quarter in target + prior 2 (default mode) or target + diff-target (diff mode), resolve in this order: **`.quartr.json` cache → legacy `.json` cache → Quartr fetch (if the quarter resolved to an eventId in Step 1) → FMP fetch (if `FMP_OK`)**. A quarter served from ANY of the four satisfies the run; record which source served each quarter for the Step 12 report.

### 2a. Quartr fetch (per quarter with an eventId and no cache hit)

Two reads per event — the qna section read is what makes the exact prepared/Q&A split possible downstream:

```
mcp__quartr__read_transcript {eventId: EVENT_ID, section: "full"}
mcp__quartr__read_transcript {eventId: EVENT_ID, section: "qna"}
```

- **Large-output rule** (`_shared/quartr.md` §4): oversized results persist to a file whose path is in the tool result — use that path directly in the jq below; never retype transcript content through context. Small results: Write the inline JSON to a /tmp file first. A `nextFromTimestamp` in a response means the transcript is windowed — loop with `fromTimestamp` and merge `paragraphs` arrays (jq `.paragraphs = (reduce inputs.paragraphs as $p (.paragraphs; . + $p))`) until absent.
- A call with no Q&A section returns empty/absent paragraphs for `section: "qna"` — build the cache with `qna: []`; the signal script falls back to the heuristic split for that file.

Assemble the combined cache (exact command validated 2026-09-09 on NBIS Q2-2026):

```bash
jq -n --slurpfile full "$FULL_JSON" --slurpfile qna "$QNA_JSON" \
  '{source:"quartr", symbol:"'$TICKER'", period:"Q'$Q'", year:'$Y', date:"'$CALL_DATE'",
    eventId:'$EVENT_ID', companyId:'$COMPANY_ID',
    eventUrl:"https://web.quartr.com/companies/'$COMPANY_ID'/events/'$EVENT_ID'/overview",
    full:$full[0].paragraphs, qna:($qna[0].paragraphs // [])}' \
  > ".data/transcripts/${TICKER}_${QY}.quartr.json"
# Validate before trusting: ≥20 full paragraphs, else delete the cache file and
# treat as a Quartr miss for this quarter (fall through to FMP).
jq -e '(.full | length) >= 20' ".data/transcripts/${TICKER}_${QY}.quartr.json" >/dev/null \
  || { rm -f ".data/transcripts/${TICKER}_${QY}.quartr.json"; echo "QUARTR_MISS ${QY}"; }
```

`--event` mode: same procedure with `period: null, year: null` plus `eventTitle` in the header; cache name `TICKER_EVENT${EVENT_ID}.quartr.json`.

### 2b. FMP fetch (fallback per remaining quarter; legacy behavior unchanged)

```bash
# Fetch to a TEMP file, NOT straight to $CACHE. `curl -sf | tee "$CACHE"`
# truncated $CACHE to empty before curl's failure was known, and the
# pipeline's exit status is tee's (0) — so a failed fetch left an empty
# $CACHE that every later run trusted as a valid cache. Promote to $CACHE
# only after validation below.
for QY in "${FMP_QUARTERS[@]}"; do
  Q=$(echo "$QY" | cut -d'-' -f1 | sed 's/Q//')
  Y=$(echo "$QY" | cut -d'-' -f2)
  curl -sf "$BASE/earning-call-transcript?symbol=$TICKER_URL&year=$Y&quarter=$Q&apikey=$API_KEY" \
    > "/tmp/transcript_${TICKER}_${QY}.json" &
done
wait

# Promote only non-empty, content-bearing responses to the persistent cache;
# delete failed/empty temps so no poisoned cache is written.
for QY in "${FMP_QUARTERS[@]}"; do
  CACHE=".data/transcripts/${TICKER}_${QY}.json"
  T="/tmp/transcript_${TICKER}_${QY}.json"
  if [ -s "$T" ] && grep -q '"content"' "$T"; then
    cp "$T" "$CACHE"
  else
    rm -f "$T"                           # failed/empty fetch — leave NO cache behind
  fi
done
```

**FMP response shape** (post-parse): `[{ symbol, period, year, quarter, date, content }]`. The `content` field is the full transcript as plain text. Length 8,000-30,000 words. **Content validation**: `content` non-empty (>500 chars); on stub/error payload clear the cache (`rm -f ".data/transcripts/${TICKER}_${QY}.json"`).

### Failure handling (both sources exhausted)

- Target quarter unfetchable → abort with the Step 1 unavailability message.
- Prior quarter unfetchable → proceed but degrade analysis (Step 4 notes which signals had only 1 prior comparator instead of 2).

## Step 3: Split transcript into prepared-remarks vs. Q&A

**Quartr-format caches split exactly** — prepared = `full` paragraphs whose `paragraphId` is not in the `qna` set; Q&A = the `qna` paragraphs; speaker turns come from `speakerName`/`speakerRole`. The script does this internally (`load_doc`); the heuristics below apply ONLY to FMP-format caches (and to a Quartr cache whose `qna` came back empty).

Per FMP-format quarter, split the `content` field into two sections:

- **Prepared remarks**: text from start of management presentation to the first analyst question marker
- **Q&A**: from first analyst question marker to end

**Detection heuristics** (in order — first match wins):
1. Literal section markers: `Q&A`, `Q & A`, `Questions and Answers`, `Question-and-Answer Session`
2. Operator transition phrases: `we'll now open the line for questions`, `we'll now open the call for questions`, `our first question comes from`
3. Speaker-pattern shift: ≥3 consecutive analyst-style speaker tags (`[Name] - [Bank/Firm]`) within a 200-word window

If no Q&A boundary detected (rare — happens for prerecorded reports without Q&A) → treat entire transcript as prepared remarks; Q&A-derived signals (skeptical-keyword density, evasiveness) marked N/A in Evidence.

Record per-quarter:
- `prepared_remarks_text`, `prepared_remarks_word_count`
- `qa_text`, `qa_word_count`, `qa_turn_count` (number of distinct speaker-change events)

## Step 4: Extract qualitative signals (delta analysis)

**Skipped entirely in `--diff` mode** — diff mode produces a different output shape (see Step 7B).

**Script-first (2026-07-08):** signals 4.1–4.7 are deterministic word-frequency / regex math — run the helper, do NOT recompute them by hand (the generate_graph.py / lint.py precedent):

```bash
# Per quarter, pass whichever cache file exists — .quartr.json preferred, legacy .json
# otherwise (the script auto-detects format per file; mixed sources are the normal case):
python3 .claude/skills/transcript/extract_transcript_signals.py \
  --current "$(ls .data/transcripts/${TICKER}_${TARGET_QY}.quartr.json .data/transcripts/${TICKER}_${TARGET_QY}.json 2>/dev/null | head -1)" \
  --prior   "$(ls .data/transcripts/${TICKER}_${PRIOR1_QY}.quartr.json .data/transcripts/${TICKER}_${PRIOR1_QY}.json 2>/dev/null | head -1)" \
  --prior   "$(ls .data/transcripts/${TICKER}_${PRIOR2_QY}.quartr.json .data/transcripts/${TICKER}_${PRIOR2_QY}.json 2>/dev/null | head -1)"
```

(`--event` mode: `--current .data/transcripts/${TICKER}_EVENT${EVENT_ID}.quartr.json` with no `--prior` flags — signals come back absolute, deltas null.)

It emits one JSON object with `new_language`, `dropped_language`, `hedging`, `specificity`, `qa_skeptical`, `evasiveness`, `guidance` — each already carrying the current/prior-2-avg values, deltas, and the ±25% / ≥20% / +50% flags that Steps 6/7/10/11/12 consume. Also `transcript_source` (`quartr`/`fmp`), `exact_split` (true = paragraph-exact prepared/Q&A boundary, no heuristics), and `prior_sources`. On Quartr input the evasiveness signal is computed from exact speaker roles (on FMP input it is usually null — labels carry no firm affiliation); its `basis` field says which. `priors_used`/`degraded_single_prior` mark the 1-prior degradation case; `qa_detected: false` marks the no-Q&A fallback (4.5/4.6 → N/A). Exit 3 (self-validation: unreadable/empty current transcript) → surface the error, do not fabricate signals.

**The LLM's job is Step 6 (cross-referencing these numbers against the thesis Bull/Bear/Triggers)** — the genuinely qualitative work — NOT re-deriving the counts. The 4.1–4.7 sub-specs below are the reference spec the script implements (and the manual fallback if `python3` is unavailable — exit ≠ 0,3). Evasiveness (4.6) carries the mandatory heuristic caveat in the script output; propagate it verbatim into the Evidence note.

### 4.1: New language (current Q only)

3+ word phrases appearing ≥2 times in current Q's prepared remarks but **0 times** in prior 2 Qs prepared remarks. Normalize: lowercase, strip punctuation, collapse whitespace.

Filter list (exclude generic phrases): `during the quarter`, `year over year`, `as we look ahead`, `let me start by`, `thank you for joining`, `as we discussed`, `going forward`. Maintain a 30-phrase exclusion list inline.

Output: top 10 by frequency in current Q, descending.

### 4.2: Dropped language (current Q only)

Inverse of 4.1: 3+ word phrases appearing ≥2 times in BOTH prior 2 Qs prepared remarks but **0 times** in current Q prepared remarks.

Output: top 10 by combined-prior-Q frequency, descending. These are the most analytically interesting — phrases management deliberately stopped using are the inverse fingerprint of new strategic framing.

### 4.3: Hedging density

Count occurrences of hedging vocabulary per 1000 words of prepared remarks. Vocabulary:

`approximately`, `roughly`, `around`, `about`, `expected to`, `expecting`, `anticipate`, `anticipating`, `we believe`, `we think`, `we feel`, `should`, `could`, `might`, `may`, `likely`, `unlikely`, `probably`, `potentially`, `if all goes well`, `assuming`, `subject to`, `pending`, `tentatively`, `roughly speaking`.

Compute per-Q rate. Report current vs. prior-2 average. Flag shifts >25% (either direction) — direction is itself the signal: management hedging less is confidence; hedging more is concern.

### 4.4: Specificity (numeric mentions in prepared remarks)

Count numeric mentions: any of `\$[0-9]`, `[0-9]+\.[0-9]+%`, `[0-9]+%`, `[0-9]+\.?[0-9]*\s*(million|billion|trillion|M|B|T)\b`, `Q[1-4]\s+(of|FY)?\s*[0-9]{2,4}`. Per 1000 words of prepared remarks.

A drop ≥20% vs prior-2 average indicates management retreated to qualitative framing — often precedes guidance walks.

### 4.5: Q&A skeptical-keyword density

Count occurrences in `qa_text` (combine all analyst questions; exclude management responses where extractable) of: `concern`, `concerned`, `headwind`, `pressure`, `slowdown`, `decel`, `moderation`, `moderating`, `softer`, `softening`, `weakness`, `disappointed`, `missed`, `below expectations`, `light vs`, `challenged`, `difficult`, `tough`, `competitive pressure`, `pricing pressure`, `margin compression`, `cyclical`, `inventory correction`.

Per 1000 words of Q&A. Compare to prior-2 average. Rising density = sell-side getting more skeptical. Falling density = capitulation (which is itself a signal — sell-side relief often marks local conviction tops).

### 4.6: Management evasiveness (Q&A turns)

For each speaker-change turn in Q&A where an analyst asks a question and management responds:
- Extract the first noun-like token sequences from the question (3-7 most-content-bearing words)
- Check whether management's first 50 words contains any of those tokens
- If 0 matches → flag as "evasive"

Compute `evasive_turns / total_qa_turns`. Compare to prior-2 average.

**Important caveat in the Research note**: this is a heuristic — disclosure-restricted topics (M&A, legal, pricing strategy) often look "evasive" by this measure but reflect legitimate non-disclosure. The skill surfaces the measure as evidence to inspect, not as a conclusion.

### 4.7: Guidance language patterns

Scan prepared remarks + Q&A for guidance constructs:
- Quarterly guidance: `Q[1-4]\s+revenue\s+(of|in)\s+`, `we expect\s+Q[1-4]`, `guiding\s+to\s+`
- Annual guidance: `full year`, `fiscal year`, `FY[0-9]{2,4}`
- Range vs. point: `between\s+\$[\d.]+\s+and\s+\$[\d.]+` (range) vs. `approximately\s+\$[\d.]+` (point)

Track: did current Q widen, narrow, or eliminate guidance ranges vs. prior Q? Did it shift from annual to quarterly framing? These are explicit confidence signals.

## Step 5: Read thesis for context (parallel reads)

Single tool-call block:

| Tool | Target | Purpose |
|---|---|---|
| `Read` | `$THESIS_PATH` (already located in Step 0.3) | Bull Case, Bear Case, Conviction Triggers, recent Log entries (last 5) |
| `Read` | `_hot.md` | Recent Conviction Changes, Open Questions for this ticker |
| `Read` | `_graph.md` | Adjacency primer (Step 6 Mode A + Step 9 Mode C fanout — read once, parse in memory) |
| `Read` | `Mental Models/Generalist - Overview` + the matching `Industry -`/`Lens -` note(s) for the thesis `sector:` | **MANDATORY reading gate** (per `_shared/mental-models-section.md`) before Step 6's judgement work — load-tiered (Generalist always; Industry/Lens by sector only), cached across the run |

Apply the READING PROTOCOL from `[[Generalist - Overview]]` to the Step 6 cross-reference: a management-language shift that appears to confirm a thesis driver is a hypothesis to test, not a verdict; run the base-rate adversarially; agreement across models is a disconfirm trigger, not confirmation.

Extract from the thesis:
- `bull_case_drivers`: parse Bull Case section; identify 3-5 named drivers (each driver typically has a sentence-opening phrase, e.g., "Rack-scale deployment economics drive NVL72 attach rate inflection")
- `bear_case_risks`: parse Bear Case section; identify 3-5 named risks
- `conviction_triggers`: parse Conviction Triggers section; extract the `→ HIGH if`, `→ LOW if`, `→ CLOSE if` falsifiable statements

These become the cross-reference targets in Step 6.

## Step 6: Cross-reference signals against thesis

For each signal extracted in Step 4, attempt to match against:

### 6.1: Bull-case driver alignment

For each `bull_case_drivers[i]`:
- Tokenize the driver phrase (significant nouns + verbs)
- Search Step 4.1 (new language) for phrases overlapping ≥2 tokens with the driver
  - Match → "Bull case driver confirmed by new framing: [driver] ↔ [new phrase]"
- Search Step 4.2 (dropped language) for phrases overlapping ≥2 tokens
  - Match → "⚠️ Bull case driver may be weakening: [driver] ↔ [dropped phrase] — management stopped framing this"

### 6.2: Bear-case risk alignment

For each `bear_case_risks[i]`:
- Same tokenization
- Match against new language → "Bear case risk surfaced in management framing: [risk] ↔ [new phrase]"
- Match against dropped language → "Bear case risk de-emphasized in framing: [risk] ↔ [dropped phrase] — may indicate management confidence OR avoidance"
- Cross-reference 4.5 (Q&A skepticism) — if analysts are now asking about a previously-mute bear-case risk: `Analyst questions surfaced bear-case risk: [risk]`

### 6.3: Conviction trigger touching

This step is the **origin pattern** for `_shared/trigger-touch.md` (the shared contract that generalises it to `/numbers`, `/sync`, `/deepen`, `/ingest`). `/transcript` owns the named-observable path: evidence bears on a trigger's variable without a number.

For each falsifiable trigger:
- Parse the trigger's named variable (e.g., `Hyperscaler capex guides flat for 2 consecutive Qs`)
- Check whether current Q transcript provides evidence on that variable
- If yes → flag the trigger as "touched" with direction (firing toward HIGH / firing toward LOW / firing toward CLOSE)
- Touched triggers are MANDATORY content in the Research note's Thesis Delta section

Flag-only — a touched trigger surfaces in the Step 11 advisories (which already suggest `/status`), never an auto-conviction-change (Tier-3, per the contract's anti-patterns).

### 6.4: Guidance vs. consensus framing

If 4.7 detects a guidance shift (widened range, eliminated annual guidance, etc.):
- Cross-reference whether the thesis Bull Case or Bear Case explicitly hinges on guidance-trajectory expectations
- If yes → flag in Thesis Delta as direct evidence

## Step 7: Write Research note

Two output shapes depending on mode.

### Step 7A: Default + specific-quarter mode

File: `Research/YYYY-MM-DD - [TICKER] [QN-YYYY] - earnings.md` (where `YYYY-MM-DD` is today's date)

Frontmatter:

```yaml
---
date: YYYY-MM-DD
tags: [research, earnings, TICKER, SECTOR_TAG]
status: active
sector: [from thesis frontmatter]
ticker: TICKER
source: [Quartr event URL (the cache's eventUrl) when transcript_source is quartr;
         https://financialmodelingprep.com/stable/earning-call-transcript?symbol=TICKER&year=YYYY&quarter=N when fmp]
source_type: earnings
transcript_source: quartr | fmp  (which source served the TARGET quarter)
transcript_quarter: QN-YYYY
transcript_date: YYYY-MM-DD  (from the cache `date` field — actual earnings call date)
transcript_word_count: [N]
prior_comparators: [QN-1-YYYY, QN-2-YYYY]
---
```

`--event` mode differences: filename `YYYY-MM-DD - [TICKER] [Event Title] - video-transcript.md`, `source_type: video-transcript`, `tags: [research, video-transcript, TICKER, SECTOR_TAG]`, `transcript_quarter` replaced by `transcript_event: "[Event Title]"`, no `prior_comparators`. Evidence tables show absolute densities only (no delta columns — there are no comparators); everything else (Thesis Delta cross-referencing, Summary, Contradiction Check, Source Excerpts) is unchanged — a CMD or investor update cross-references against Bull/Bear/Triggers exactly like an earnings call.

Body sections (in order — all required except where noted):

```markdown
# [TICKER] [Q[N] FY[YYYY]] — Earnings Transcript

## Thesis Delta

[1-2 sentences PER cross-reference hit from Step 6. Lead with the strongest signal. Use the templates:]
- **Bull case [strengthened|weakened|unchanged]** — [specific driver from Step 6.1] ↔ [evidence from Step 4]
- **Bear case [strengthened|weakened|unchanged]** — [risk from Step 6.2] ↔ [evidence]
- **Conviction trigger touched** — [trigger text from Step 6.3] — current Q [confirms/disconfirms]: [evidence]
- **Guidance shift** (if applicable per Step 6.4) — [shift type] vs. [thesis assumption]

[If zero cross-references hit: this section reads "No direct thesis-relevant deltas. Notable framing shifts logged in Evidence below for future synthesis."]

## Summary

[2-4 paragraphs. Lead with management's CORE argument for the quarter — what mechanism are they pitching to explain the results, what forward construction are they framing? NOT a press-release re-summary; the thesis owns the business description. Capture the argument structure, the named drivers, the qualifier/hedge structure. Length proportional to transcript: 2 paragraphs for short (~8,000 words), 3-4 paragraphs for long (>20,000 words).]

## Evidence

### Language deltas

**New framing (top 5 introduced this Q)**:
| Phrase | Mentions this Q | Mentions prior 2 Qs |
|---|---|---|
| [phrase] | [N] | 0 |
| ... |

**Dropped framing (top 5 retired this Q)**:
| Phrase | Mentions prior 2 Qs combined | Mentions this Q |
|---|---|---|
| [phrase] | [N] | 0 |
| ... |

### Hedging & specificity

| Metric | Current Q | Prior 2-Q avg | Δ | Direction |
|---|---|---|---|---|
| Hedging density (per 1000 words) | [N] | [N] | [Δ%] | [more confident / more hedged / unchanged] |
| Numeric mention density (per 1000 words) | [N] | [N] | [Δ%] | [more specific / less specific / unchanged] |

### Q&A signals

| Metric | Current Q | Prior 2-Q avg | Δ |
|---|---|---|---|
| Skeptical-keyword density (per 1000 words of Q&A) | [N] | [N] | [Δ%] |
| Evasive turns (% of total Q&A turns) | [N]% | [N]% | [Δpp] |
| Total Q&A turns | [N] | [N] | — |

[Caveat: evasiveness is heuristic — disclosure-restricted topics (M&A, legal, pricing) often appear evasive but reflect legitimate non-disclosure.]

### Guidance language (if Step 4.7 surfaced changes)

[Specifics: range width change, point-vs-range shift, annual-vs-quarterly shift, dropped guidance, added guidance]

## Contradiction Check

[Specific to which thesis assumption the transcript contradicts or supports. Pull from Step 6 cross-references. Examples:]
- [[Research/path-to-prior-research-note]] argued [specific thesis] — current Q transcript supports / contradicts via [evidence].
- Bear case (per [[Theses/TICKER]] §Bear Case) hinges on [risk]; current Q transcript [evidence for/against].

[If no specific contradictions: "Transcript reinforces existing thesis framing — no contradictions surfaced."]

## Source Excerpts

[3-7 verbatim quotes that anchor the Thesis Delta points. Quote blocks formatted as Obsidian blockquotes (`>`). Each quote attributed by speaker if extractable. **Quartr-sourced quotes: link the attribution to the paragraph's timestamped deep-link `url`** (pull the matching paragraph from the cache via jq — do not read the whole transcript into context to find it) — this makes every quote click-to-verify against the call audio:]

> [[CEO Name, CEO](paragraph-deep-link-url)]: "...verbatim quote..."

> [[Analyst Name, Analyst](paragraph-deep-link-url)]: "...verbatim question..."

[FMP-sourced quotes: plain attribution as before — no per-paragraph URLs exist. Quotes should be SHORT — 1-3 sentences each. The reader can read the full transcript via the source: URL if they need more.]
```

**Required `## Key Segments` section** (per `/ingest` content-quality check #5 when `source_words >15,000`):

```markdown
## Key Segments

[3-5 sub-sections mirroring the transcript's structural progression. Each 2-5 sentences. Examples:]

### Prepared Remarks - Strategic Framing
[Management's positioning of the quarter — what story are they telling about the business right now]

### Prepared Remarks - Segment Discussion
[Per-segment color: which segments management emphasized, which they de-emphasized]

### Prepared Remarks - Forward Construction
[Guidance philosophy, capex commentary, capital allocation framing]

### Q&A - Most Skeptical Exchange
[The single most-pointed analyst question and management's response — verbatim or paraphrased + commentary]

### Q&A - Most-Disclosed New Information
[Where management revealed something that wasn't in prepared remarks — often the highest-value information from any earnings call]
```

Include `## Key Segments` ONLY when `transcript_word_count > 15,000`. For shorter transcripts (rare — most US large-cap calls run 10-20k words), omit per `/ingest` Step 2 spec.

### Step 7B: `--diff` mode

File: `Research/YYYY-MM-DD - [TICKER] [Q1] vs [Q2] - transcript diff.md`

Frontmatter:

```yaml
---
date: YYYY-MM-DD
tags: [research, earnings, comparison, TICKER, SECTOR_TAG]
status: active
sector: [from thesis frontmatter]
ticker: TICKER
source: [per-quarter source URLs, comma separated — Quartr event URL for quartr-served quarters, FMP earning-call-transcript URL for fmp-served]
source_type: analyst-report
transcript_source: [quartr | fmp | mixed]
diff_quarters: [Q1-YYYY, Q2-YYYY]
---
```

Body:

```markdown
# [TICKER] [Q1-YYYY] vs [Q2-YYYY] — Transcript Diff

## Thesis Delta
[Cross-reference findings against thesis — same structure as Step 7A but framed as "between these two quarters"]

## Summary
[2-3 paragraphs framing the analytical comparison — what story does management tell differently between these two quarters? Lead with the most-load-bearing change.]

## Evidence

### Side-by-side language shift

| Theme / Phrase | [Q1-YYYY] frequency | [Q2-YYYY] frequency | Direction |
|---|---|---|---|
| [top 15 phrases with biggest absolute change] |

### Side-by-side hedging & specificity

| Metric | [Q1-YYYY] | [Q2-YYYY] | Δ |
|---|---|---|---|
| Hedging density | | | |
| Numeric density | | | |
| Q&A skeptical density | | | |
| Evasiveness % | | | |

### Strategic framing shifts (qualitative)

- **Introduced between quarters**: [list]
- **Dropped between quarters**: [list]
- **Re-framed**: [phrases that changed wording but kept meaning — e.g., "Hopper transition risk" → "Blackwell ramp velocity"]

## Contradiction Check
[Same scope as 7A]

## Source Excerpts
[Paired quotes — one from each quarter — anchoring the largest shifts]
```

## Step 7.5: Post-write verification gate

Re-read the just-written Research note. Apply the verification checks from `/ingest` Step Post-write verification:

- **Structural checks 1-4** (frontmatter parseability, required fields, body non-empty with at least one `##` section, last line not mid-sentence): block on failure → restore via deletion + abort.
- **Content-quality check 5** (proportional body word count floor): for `source_type: earnings` with transcripts typically >15,000 words → body must be ≥2,500 words AND have a `## Key Segments` section with ≥3 sub-sections. For diff mode `source_type: analyst-report` → body must be ≥800 words (1,500-5,000 source-word bucket).
- **Content-quality check 7** (section structural minimum): all 4 required sections present with non-empty content — `## Thesis Delta`, `## Summary`, `## Evidence`, `## Contradiction Check`.
- **Domain validator #8** (`source_type: earnings` signature — applies to Step 7A): MUST contain quarterly-period token, ≥2 numeric currency figures, ticker-shaped token. The transcript content itself supplies these; the Research note's restating Evidence section should also contain them.

**On verification failure**:
- Structural failure → delete the partial Research note, log failure, abort the entire skill run with diagnostic.
- Content-quality failure → delete the Research note (treat as contaminated, not partial), report which check failed with diagnostic (body words, source words, missing tokens). Retain the raw transcript cache so user can re-run after fixing the analysis prompt or content-extraction logic.

## Step 8: Append thesis Log entry

Edit `$THESIS_PATH`'s `## Log` section. Append:

```
### YYYY-MM-DD
- Transcript ingested: [QN-YYYY] — [most-significant thesis-delta finding from Step 6 in plain prose, 1 sentence]. See [[Research/YYYY-MM-DD - TICKER QN-YYYY - earnings]].
```

For `--diff` mode:
```
### YYYY-MM-DD
- Transcript diff: [Q1] vs [Q2] — [most-significant shift in plain prose]. See [[Research/YYYY-MM-DD - TICKER Q1 vs Q2 - transcript diff]].
```

**Prefix `Transcript ingested:` (or `Transcript diff:` for diff mode) is intentionally NON-skill-origin.** This is a research-driven Log entry — the Research note created in Step 7 represents real new analytical content that should propagate to sectors and macro notes. `/sync` Step 2.5 will treat the change as research-driven and run Steps 3-5 normally.

Do NOT add this prefix to `_shared/log-prefixes.md` skill-origin list. Adding it would silently break `/sync` propagation from every earnings transcript ingest — exactly the wrong behavior.

## Step 9: Graph-primer propagation fanout

Per `.claude/skills/_shared/graph-primer.md` Mode C (Propagation-fanout primer — same as `/ingest` Step 3.5).

Using `_graph.md` (already read in Step 5):
- `T` = TICKER
- `S` = thesis's `sector:` from frontmatter
- `M` = macro references found in the Research note's body (parse `[[Macro & Technology/...]]` wikilinks)

Compute:
- `direct_targets = {THESIS_PATH}` (the ticker's own thesis — always a direct target)
- `sector_candidates = sector_reverse[S] - direct_targets`
- `macro_candidates = ∪{macro_reverse[m]} for m in M - direct_targets - sector_candidates`

Surface to user in Step 12 report. Wikilinks for `direct_targets` are already in the Research note (the thesis link in `## Thesis Delta` and `## Source Excerpts`). For `sector_candidates` and `macro_candidates` — these are advisory; the user reviews and adds wikilinks before `/sync` if they want propagation to those neighbors.

**Missing-graph fallback**: per contract — log `ℹ️ _graph.md absent/unparseable — graph primer skipped` and proceed. Step 8's Log entry + Step 7's Research note still propagate via `/sync` based on body-content grep alone.

## Step 10: Update `_hot.md`

Follow `.claude/skills/_shared/hot-md-contract.md`. Read first (already read in Step 5), then edit. Do NOT touch Latest Sync / Sync Archive.

1. **Active Research Thread**: per contract's same-ticker-continuation rule — likely set to `[TICKER] earnings analysis (QN-YYYY)`.
2. **Open Questions**: if Step 6.3 surfaced touched conviction triggers OR Step 4.5 surfaced rising Q&A skepticism, append 1-2 open questions for `/surface` later: `- [TICKER] QN: [trigger touched in direction X] — re-evaluate conviction at next data point.`
3. **Latest Sync** and **Sync Archive**: do NOT touch (owned by `/sync`).
4. **Recent Conviction Changes**: do NOT touch (a transcript ingest is research input, not a conviction decision — the user calls `/status` if a conviction change is warranted).

**Cap enforcement**: per contract — apply drops if over soft cap; abort `_hot.md` update if over hard cap (DON'T block the primary `/transcript` operation).

## Step 11: Material-finding advisories

If Step 6 surfaced any of:
- **A conviction trigger fired toward LOW or CLOSE** → suggest `/status [TICKER] [field] [current]→[new]` with the rationale phrased from the trigger
- **A conviction trigger fired toward HIGH** → suggest `/status [TICKER] conviction [current]→high`
- **Bear-case risk strengthened by ≥2 evidence vectors** → suggest `/stress-test [TICKER]`
- **Bull-case driver weakened by ≥2 evidence vectors** → suggest `/deepen [TICKER] --section "Bull Case"`
- **Q&A skepticism +50% vs. prior 2-Q avg** → suggest `/stress-test [TICKER]` (analyst skepticism leading official conviction is a real edge)

These print as `→ Consider: [command]` lines in the Step 12 report. Never auto-run.

## Step 12: Release lock and report

Final Bash block — lock release per preflight §1.7.

```bash
LOCK_FILE="<paste-from-Step-0.1>"
EXPECTED_TOKEN="<paste-token-captured-from-Step-0.1>"
if [ -f "$LOCK_FILE" ] && grep -q "token: $EXPECTED_TOKEN" "$LOCK_FILE"; then
  rm -f "$LOCK_FILE" && echo "=== LOCK RELEASED ($LOCK_FILE) ==="
else
  echo "⚠️ Lock ownership check failed at release — skipping rm."
fi
# Keep cache (.data/transcripts/*) — useful for diff mode re-runs
# Only clear /tmp scratch
rm -f /tmp/transcript_*.json /tmp/transcript_dates_*.json
```

### Report

```
✓ /transcript [TICKER] [QN-YYYY | --diff Q1 Q2] complete

Research note:    [[Research/YYYY-MM-DD - TICKER QN-YYYY - earnings]]
Transcript date:  YYYY-MM-DD (Q[N] FY[YYYY])
Transcript source: quartr (exact split, exact speaker roles) | fmp (heuristic split) — per quarter if mixed
Transcript size:  ~[N] words
Prior comparators: [Q-1, Q-2]

Thesis delta findings:
  Bull case:       [strengthened | weakened | unchanged]  — [1-line summary]
  Bear case:       [strengthened | weakened | unchanged]  — [1-line summary]
  Triggers touched: [N]  ([list with direction])

Signal extracts (most analytically interesting):
  New framing introduced: [top 3 phrases]
  Dropped framing:        [top 3 phrases]
  Hedging shift:          [direction, %]
  Q&A skepticism shift:   [direction, %]
  Touched trigger(s):     [list, or "none"]

Graph primer:
  Direct targets:      [list of theses]
  Sector candidates:   [list of theses sharing sector — review for wikilinking]
  Macro candidates:    [list of theses sharing macro refs — review for wikilinking]

Thesis Log: appended ("Transcript ingested:") — research-driven prefix
_hot.md: updated (Active Research Thread, Open Questions if applicable)
Transcript cache: .data/transcripts/TICKER_QN-YYYY[.quartr].json (retained for diff mode re-runs)

Suggested next steps:
  1. /sync [TICKER]          — propagate to sector + macro notes
  2. /graph last             — reconcile adjacency
  → Consider: [Step 11 advisories, if any]
```

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **Earnings transcripts require an existing thesis.** Step 0.3 hard-aborts when no thesis exists. The whole value of `/transcript` is delta-against-thesis-context; orphan-earnings ingestion is `/ingest`'s job.

2. **The Log prefix `Transcript ingested:` is NOT skill-origin.** It must propagate via `/sync` because the Research note carries genuine new analytical content (management framing shifts, trigger touches) that affects sector competitive-dynamics framing and macro thread continuity. Adding this prefix to `_shared/log-prefixes.md` skill-origin list silently disables every transcript's propagation.

3. **Heuristic signals are flagged as heuristics in the Research note.** Hedging density, evasiveness percentage, skeptical-keyword density are all imperfect text-frequency measures. The Research note must explicitly caveat each (especially evasiveness, which is highly false-positive on disclosure-restricted topics).

4. **Transcript cache is gitignored.** `.data/transcripts/` lives under `.data/` which is in `.gitignore` per Live Portfolio's documentation. Re-runs read from cache; first runs populate it. No transcript content ever lands in version control.

5. **Diff mode is a separate output shape.** Treating diff as "two ingests then a manual side-by-side" loses the value — the cross-quarter Evidence table is the primary deliverable. Don't conflate the modes.

6. **`## Key Segments` section is required for transcripts >15,000 words.** Per `/ingest` content-quality check #5. Most US large-cap earnings calls cross this threshold. The 5-segment structure (Strategic Framing, Segment Discussion, Forward Construction, Most-Skeptical Exchange, New Information) reliably captures a 60-90 minute call's analytical substrate.

7. **Quartr is primary; FMP is the fallback, and wholesale tier is the fallback's assumed entitlement.** The FMP earnings-transcript endpoint is gated on FMP wholesale tier (or higher); lower tiers return 403/404 — the fallback aborts cleanly with an FMP error rather than silently degrading. A run that never touches FMP (Quartr served every quarter) has no tier dependency at all.

8. **Never re-fetch when cache is fresh.** First-pass writes to `.data/transcripts/TICKER_QN-YYYY.quartr.json` (Quartr) or `TICKER_QN-YYYY.json` (FMP). Subsequent runs (e.g., user iterating on prompt phrasing for the Research note) read cache — either format satisfies the quarter. Every avoided fetch is one less API/MCP touchpoint and faster per run.

9. **Transcript content never flows through context by hand.** Oversized MCP results persist to a file — `cp`/jq that file into the cache (`_shared/quartr.md` §4). The signal script reads the cache from disk; Claude reads targeted jq paragraph slices for Step 7's quotes, never the whole transcript. Retyping or summarising a transcript from memory into the cache is fabrication — abort instead.

10. **Never take a wrong company.** Quartr resolution failures (no confident search match, eventId belonging to another company) degrade to FMP or abort — the SIVE→Silver-Verde class of ticker collision applies to any source. Resolution discipline lives in `_shared/quartr.md` §3.
