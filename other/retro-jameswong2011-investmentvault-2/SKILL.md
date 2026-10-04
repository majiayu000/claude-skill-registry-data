---
name: retro
description: Generate a backward-looking retrospective of vault activity (addressed callouts + Log entries) over a time window (1w / 1m / 1q), overlay with newsflow + earnings transcripts + price action, and rank trade ideas by the gap between official narrative and market reaction. Output is an immutable Research note. Use when user says "retro", "retrospective", "what did I do this week/month/quarter", "review activity against market", or "recommend trades from recent research".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$retro`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Produce a retrospective that answers three questions in one artifact:

1. **What was resolved?** Addressed callouts with the user↔Codex exchange.
2. **What is still open?** Fresh callouts left unresolved in the window.
3. **Did the market price the narrative?** Per-ticker overlay of **newsflow + earnings results/transcripts + price action**. Trade ideas rank by the **narrative-price delta** — the gap between what official sources signaled and what the stock did. Biggest gaps are positioning opportunities; alignment is already-priced.

Output is an **immutable Research note** — one new note per run, never overwrite. Trade recommendations are informational (link-back + suggested follow-up skill); this skill never mutates `conviction:` or `status:` (Tier 3 Confirmation-Required per AGENTS.md).

## Execution context — Codex subagent delegation (MANDATORY)

Resolve the window in the main thread, then spawn ONE Codex subagent with the available delegation tool. Prefer the project `vault_worker` agent when selectable. Pass this skill's full instructions plus the resolved window. The subagent performs Step 0 through Phase 9, including reads, current-data web research, transcript fetches, lock handling, and the specified writes. Wait for completion and render its complete Phase 9.2 report **verbatim**; never re-summarize it or drop the Trade Ideas table.

**Mental Models gate:** Do not rely on inherited project context. Embed this text in the delegated prompt: *"Before ranking trade ideas from the narrative-price gaps, read `Mental Models/Generalist - Overview.md` + the matching `Mental Models/Industry - X.md`/`Lens - X.md` for the tickers surfacing. Apply the READING PROTOCOL — the market-vs-vault gap is a hypothesis, not a verdict; run the base-rate adversarially (most gaps close because the market is right); an inverted-bear/inverted-bull signal is a disconfirm trigger on the vault's own stance, not automatic alpha."*

**Recursion guard:** Also embed: *"You are the EXECUTOR of this skill run, not a coordinator. Do not delegate any part of this work to another subagent. Perform all reads, searches, and writes yourself, and end your final message with the complete Phase 9.2 report."*

Delegation keeps the large read/search budget out of the main context. If delegation is unavailable, run inline and preserve the same report and write contract.

## Arguments

`SKILL_ARGS` parses to a **window keyword** plus an **optional trailing ticker** (scoped mode, 2026-07-08).

| Input | Canonical window | Day count |
|---|---|---|
| empty, `1w`, `w`, `week`, `weekly`, `7d` | `1w` | 7 |
| `1m`, `m`, `month`, `monthly`, `30d` | `1m` | 30 |
| `1q`, `q`, `quarter`, `quarterly`, `90d` | `1q` | 90 |

Default window: `1w`. A token that is not a window keyword is parsed as a **ticker** for scoped mode (`$retro 1w NVDA`, `$retro NVDA` → default 1w scoped to NVDA). Resolve the ticker to `Theses/TICKER - *.md`; if no thesis matches, reject: `❌ $retro no thesis for ticker "[input]" (and not a window keyword). Windows: 1w | 1m | 1q.` A recognized window with an unrecognized SECOND token that is also not a thesis ticker → same reject.

**Scoped mode (`SCOPE_TICKER` set)** changes three things vs the vault-wide default:
1. **Phase 1** reads only the scoped thesis + its `_graph.md` cluster peers' sector/macro links (not all ~60 files) — see Phase 1 scoped path.
2. **`TICKER_UNIVERSE` = { SCOPE_TICKER }** (∪ cluster peers if the graph primer is present and the user wants competitive context) — overrides the window-activity derivation in §2.4. The scoped ticker is analyzed even with zero window activity (the user asked for it explicitly), so the Phase 2.5 empty-window short-circuit does NOT fire in scoped mode.
3. **Phase 3** issues the 3-channel query for the one ticker (fits a single message; the ≤5-ticker one-message path already covers it) — no ~126-query fan-out.

The vault-wide lock is retained even in scoped mode (Invariant 7 — retro still writes a Research note + may Log-append).

## Step 0: Pre-flight (MANDATORY — runs before Phase 1)

### 0.1: Acquire vault lock

Acquire a `vault-wide` scope lock per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout budget: **10 minutes** (parallel reads across ~60 files + N parallel web searches).

Capture the token at Step 0.1, verify ownership (Procedure 1.5) at every subsequent shell block, release in the final reporting shell block via `rm -f "$LOCK_FILE"`.

### 0.2: Rename-marker pre-flight (warn-only)

Glob `.rename_incomplete.*` at vault root. If any marker exists, emit:

```
⚠️ In-flight rename repair(s) detected: [list markers]. Retro scan will proceed but its Research note's wikilinks to the affected ticker(s) use current filenames. Complete rename repair before running downstream $sync.
```

DO NOT abort. Retro is a read-mostly exploratory operation; its output is a new Research note that does not mutate existing thesis bodies. Mid-rename state does not silently split propagation the way a vault-wide `$sync` would.

### 0.3: Window computation

```bash
# Example for 1m window
DAYS=30
TODAY=$(date +%Y-%m-%d)
WINDOW_START=$(date -v-${DAYS}d +%Y-%m-%d 2>/dev/null || date -d "${DAYS} days ago" +%Y-%m-%d)
echo "WINDOW|$WINDOW_START → $TODAY"
```

Record `WINDOW_START`, `TODAY`, and window label (`1w|1m|1q`) for Phase 6 frontmatter.

### 0.4: Graph primer (optional — read if present)

Read `_graph.md` per `.agents/skills/_shared/graph-primer.md` Mode A (ticker-scoped, applied in aggregate during Phase 4 per-ticker synthesis). If absent or unparseable, proceed without primer — log `ℹ️ _graph.md absent — retro proceeds without cluster context.` Never block.

The graph orients Phase 4 synthesis (which ticker is in which cluster, shared peers) — it never replaces thesis reads.

## Phase 1: Activity-Gated Batch Read

**Scoped mode (`SCOPE_TICKER` set)**: skip the triage — read only `Theses/SCOPE_TICKER - *.md` in full, plus (if the graph primer loaded) the sector/macro notes it wikilinks. Typically 1–4 files. Proceed to Phase 2.

**Vault-wide mode — grep-triage first, then read only active files (2026-07-08):** most theses have NO activity in a given window (especially `1w`), so a blanket ~60-file full read is wasteful. Gate the reads:

1. **One grep pass** over `Theses/*.md`, `Sectors/*.md`, `Macro & Technology/*.md` for the three activity signals:
   - addressed callouts in window: `> \[!(question|error|tip|todo)\].*→ Addressed 20\d\d-\d\d-\d\d`
   - any fresh (unaddressed) callout: `> \[!(question|error|tip|todo)\] 20\d\d-\d\d-\d\d` without `→ Addressed` on the line
   - Log date headers: `^### 20\d\d-\d\d-\d\d`
   Emit filename + matched dates. (One `grep -rnE` with alternation, output_mode content — a single round-trip.)
2. **Filter to the active set**: a file is active if it has (a) an addressed-callout date within `[WINDOW_START, TODAY]`, OR (b) any fresh callout (surfaced regardless of window — §2.2), OR (c) a Log date within the window. Fresh-callout and in-window-date matching is done in the reasoning layer from the grep output — no per-file read yet.
3. **Read the active set in full**, as ONE parallel tool-call batch. For a `1w` window this is typically 5–15 files vs ~60; for `1q` it grows toward the full set (correct — more activity to review). Do NOT serialize.

Files considered: `Theses/*.md` (every status — draft/active/monitoring/closed-but-not-archived all carry callouts + Log), `Sectors/*.md`, `Macro & Technology/*.md`. Research notes are NOT read here (they carry no callouts by convention; their Log is implicit via the owning thesis).

**Why grep-gate, not section-target**: callouts are inline anywhere in a body, so you cannot narrow *within* a file — but you CAN skip files with zero window activity entirely. The grep is the cheap discriminator; full-read is reserved for files that actually changed. `TICKER_UNIVERSE` (§2.4) is still derived from the active set's extracted callouts/Log, so gating out inactive files cannot drop a ticker that had activity.

## Phase 2: Extraction (parse in-memory from Phase 1 reads)

For each file content, walk the body line-by-line. Track the current `## Heading` at each line (parent-section detection walks back to the nearest `## ` — same approach as `$archive-callouts` Phase 2.2).

### 2.1: Addressed callouts in window

Match callout blocks with header:

```
> [!<type>] <fresh_date> → Addressed <addressed_date>[ <markers>]
> <body line 1>
...
> **Response:** <response line 1>
...
```

Qualify as **in-window addressed** iff `WINDOW_START ≤ addressed_date ≤ TODAY`. Extract per block:

```yaml
- file: [path]
  ticker: [inferred from file — TICKER from "Theses/TICKER - Name.md", or null for sector/macro]
  parent_section: [nearest preceding ## heading]
  type: question | error | tip | todo
  raised_date: YYYY-MM-DD
  addressed_date: YYYY-MM-DD
  body: [joined text, `> ` prefix stripped]
  response: [joined text, `**Response:** ` prefix stripped]
  markers: [[[pinned]]] (informational only — not excluded; legacy [[preserve]] markers during deprecation transition also recorded)
```

**Skip policy**:
- Callouts inside `## Legacy Callouts` — never parse (archive section).
- Callouts inside `## Log` — never parse (defensive; Logs don't carry callouts by convention).
- Malformed headers (unparseable date, unrecognized type) — skip with `ℹ️ Skipped malformed callout in [file]:[parent_section]`.

### 2.2: Fresh callouts in window

Match callouts with header `> [!<type>] <fresh_date>` (NO `→ Addressed` token). Qualify as **in-window fresh** iff `WINDOW_START ≤ fresh_date ≤ TODAY`. Extract same schema as 2.1 with `addressed_date: null` and `response: null`.

Fresh `[[pinned]]` callouts ARE included — pinned means "do not address", not "do not report in retro". They still signal what the user was thinking about.

### 2.3: Log entries in window

Match headers `^### (YYYY-MM-DD)$` within any `## Log` section. For each date header in `[WINDOW_START, TODAY]`, collect every bullet line beneath it until the next `### ` or `## `.

Extract per bullet:

```yaml
- file: [path]
  ticker: [inferred from file]
  date: YYYY-MM-DD
  prefix: [first token-phrase before `:` if present — match against .agents/skills/_shared/log-prefixes.md registry]
  text: [full bullet body]
  skill_origin: true | false  # matches any prefix in the skill-origin list
```

Skill-origin classification (matches `.agents/skills/_shared/log-prefixes.md` skill-origin list): `Stress test`, `Deepening`, `Deepened`, `↳ CORRECTION: Deepened`, `Conviction reaffirmed`, `Status change:`, `CLOSED`, `Prune upgrade`, `Scenario `, `Initial thesis created`, `ROLLBACK to snapshot`, `Scenario REVERSED`, `Cross-thesis closure:`, `Cross-thesis closures:`, `Renamed file:`, `Comparison `, `Callout sweep:`, `Numbers refresh:`, `Cross-thesis signal via`. (`Transcript ingested:` is deliberately NON-skill-origin per log-prefixes.md — transcript-driven activity counts as high-signal manual research.)

**Sync-propagated entries are a third class, not manual signal.** A bullet whose body STARTS with a `[[Research/` wikilink under a date header annotated `($sync)` is machine propagation output (sync Step 3f format: `- [[Research/note]]: [delta] — [conviction impact]`). Classify it `sync-propagated`: it counts toward TICKER_UNIVERSE (the ticker was genuinely active) but is weighted BELOW manual entries in VAULT_DIRECTION / §4.2 alpha-reflection analysis — otherwise a `$sync all` run reads as user conviction activity across every synced ticker.

Non-skill-origin, non-sync-propagated entries are manual or user-callout-driven activity — highest signal for retro ("what I actually thought about").

### 2.4: Ticker universe

Compute `TICKER_UNIVERSE = unique set of tickers across 2.1 + 2.2 + 2.3 where ticker is non-null`. This is the set of tickers that had ANY activity in the window and require market overlay.

Sector/macro-file callouts with no clear ticker attach are tracked separately in a `portfolio_level_activity` bucket — surfaced in the output but not ticker-keyed.

### 2.5: Empty-window short-circuit

If `2.1 + 2.2 + 2.3 = 0` entries across all files:

```
No activity found in [1w|1m|1q] window ([WINDOW_START] → [TODAY]).

Possible reasons:
  - No callouts addressed or raised in window
  - No $status, $sync, $stress-test, or manual Log edits in window
  - Window may be too short — try $retro 1m or $retro 1q

No Research note written. Lock released.
```

Release lock per Step 0.1 and exit cleanly.

## Phase 3: Narrative + Price Overlay (parallel web search + targeted fetches)

**Core engine**: per ticker, collect three signals — **newsflow**, **earnings** (if any landed in window), **price action** — then compute the narrative-price delta in Phase 4. Social sentiment is NOT collected (retail chatter, Twitter, Reddit all excluded per prior spec). The narrative channels here are OFFICIAL: press releases, SEC filings, earnings results and call transcripts, analyst upgrades/downgrades, major business news.

### 3.0: Local newsflow corpus (2026-07-20 — read before any web search)

The n8n Workflow 3 sweep persists one story log per run at `.data/news_stories/*.json` (`{date, stats, stories: [{title, cluster, score, sum, members}]}` — `sum` is a factual per-story summary, `members` carry source URLs, ticker stories tag `tk-<ticker>` in member `feedId`s). If the folder exists, read the files whose `date` falls inside the retro window BEFORE issuing Phase 3 web searches:

1. **Seed the News channel**: per ticker, collect its window stories (match `tk-<ticker>` in members, or ticker/company name in title) with date + score + `sum`. These are dated, pre-scored, summary-carrying events — often richer than a web search snippet. A ticker whose window newsflow is fully covered by corpus stories still gets its **Price** query (the corpus has no price data) but may skip or narrow its **News** query — note `news_source: corpus` in the extraction schema.
2. **High-score / no-reaction signal**: any corpus story with `score ≥ 8` on a ticker whose `window_price_move_pct` lands within ±2% becomes a first-class Phase 4 input — material newsflow the market shrugged at is exactly the narrative-price delta this skill ranks. Tag these `corpus-flagged` so classification can cite the specific story (`title`, date, `sum`).
3. **Absent or empty folder**: skip silently — Phase 3 proceeds fully on web search as before. The corpus is an accelerant, never a dependency.

### 3.1: Three-channel query plan per ticker

For each `ticker ∈ TICKER_UNIVERSE`, issue three distinct queries. Each channel surfaces a separate input to classification.

| Channel | Query template | Extracts |
|---|---|---|
| **Price** | `[TICKER] stock price [WINDOW_START] to [TODAY] percentage change` | `window_price_move_pct`, intra-window volatility if visible |
| **News** | `[TICKER] news [WINDOW_START] to [TODAY] analyst rating earnings guidance M&A` | Major events (product launches, guidance updates, analyst actions, regulatory, M&A) — each with date + polarity (positive/negative/neutral) |
| **Earnings** | `[TICKER] earnings [WINDOW_START] to [TODAY] results call transcript guidance` | Results vs consensus, guidance direction, call-transcript key themes (only if an earnings event landed in the window) |

### 3.1.5: Overlay cache check (2026-07-08 — skip re-querying fresh tickers)

Overlapping runs waste web searches: `$retro 1w` on Friday then `$retro 1m` the next Monday re-fetches identical recent price/news for every shared ticker. Cache the per-ticker overlay and reuse it within a freshness window.

```bash
mkdir -p .data/retro_cache      # gitignored (.data/)
```

For each ticker in `TICKER_UNIVERSE`, before issuing its 3 queries, check `.data/retro_cache/${TICKER}.json`. **Reuse** the cached overlay (skip all 3 queries for that ticker) iff BOTH:
- `fetched_date` is within **3 days** of TODAY, AND
- the cached `window_end` ≥ this run's TODAY − 1 (the cached data already covers this run's recent edge).

Otherwise query fresh. After Phase 3 completes, write/overwrite `.data/retro_cache/${TICKER}.json` with `{fetched_date: TODAY, window_end: TODAY, price_move_pct, news_events, earnings, dominant_polarity}` (compact — the classification inputs only, not raw search text). The cache is advisory: a miss just means a normal query; staleness is bounded by the 3-day guard, so it never injects old market data into a fresh classification. Scoped mode uses the same cache for its single ticker.

### 3.2: Parallel batch issuance

Issue the three queries per **non-cached** ticker **in the same parallel tool-call batch**. For a 42-ticker universe with a cold cache this is ~126 web searches; chunk into messages of up to 25 web search invocations per message, producing ~5-6 rounds. Never serialize within a chunk — only between chunks. Mirrors `$catalyst` Phase 2's pattern at 3× the fan-out. A warm cache (e.g. a `1m` run days after a `1w` run) drops this to only the tickers with new activity.

If the non-cached set is small (≤5 tickers) — including every scoped-mode run — all queries fit in one message.

### 3.3: Targeted fetches (earnings transcripts only)

If the Earnings web search surfaces a canonical transcript URL (e.g., Seeking Alpha transcript page, company IR page, Motley Fool coverage), capture the URL but do NOT auto-fetch. Fetch selectively only when:

- An earnings event landed inside the window, AND
- The ticker already appears likely to rank in Top 5 by preliminary narrative-price gap (rough pre-screen on web search snippets), AND
- The vault thesis has an active Log entry or addressed callout from the window (i.e., we care what the earnings said relative to our thinking)

For each qualifying URL, issue `defuddle [URL]` via Bash (preferred for transcript pages — strips navigation and comment noise) or `web fetch/open` (fallback). Cap at **5 transcript fetches per retro run** — earnings transcripts are long (~8-15K tokens each); unbounded fetches would blow the context budget. If >5 tickers qualify, fetch the top 5 by preliminary gap magnitude.

### 3.4: Extraction schema per ticker

```yaml
ticker: TICKER

price:
  window_move_pct: [number | null if unavailable]
  direction: up | down | flat | unknown           # threshold: ±3% (see Phase 4)
  max_intraday_move: [if visible in snippets, else null]

news:
  events: 
    - date: YYYY-MM-DD
      headline: [text]
      polarity: positive | negative | neutral
      source: [publication or snippet origin]
  dominant_polarity: positive | negative | neutral | mixed | none
    # Aggregated across events: count polarities, take dominant; none = no material event

earnings:
  event_in_window: true | false
  date: YYYY-MM-DD | null
  surprise_direction: beat | miss | inline | null
  guidance_direction: raised | lowered | maintained | withdrawn | null
  transcript_fetched: true | false
  transcript_themes: [list of 3-5 key themes if transcript was fetched, else null]

source_snippets: [top 2-3 audit-trail snippets per channel]
```

**If a channel returns nothing** (thinly-traded ticker with no news, no earnings in window, etc.), record `null` / `none` — downstream Phase 4 handles null channels without aborting the ticker.

## Phase 4: Three-Dimensional Classification

Per ticker, synthesize across three independent dimensions:

1. **VAULT_DIRECTION** — derived from Phase 2 extraction: `strengthened | weakened | mixed | neutral`
   - Aggregate addressed-callout resolutions + non-skill-origin Log entries. Classify each as strengthen/weaken/neutral. Dominant wins; ties → `mixed`; zero activity → `neutral`.

2. **NEWS_DIRECTION** — from Phase 3.4 `news.dominant_polarity`: `positive | negative | neutral | none`
   - If earnings event in window: roll earnings `surprise_direction` + `guidance_direction` into this bucket (beat + guidance raised → positive; miss + guidance lowered → negative; mixed → neutral).
   - `none` = no material news or earnings event surfaced.

3. **PRICE_DIRECTION** — from Phase 3.4 `price.direction`: `up | down | flat | unknown`
   - Threshold: `up` iff `window_move_pct > +3%`, `down` iff `< -3%`, else `flat`. Window-agnostic (1w, 1m, 1q all use ±3%) because absolute price moves — not annualized rates — determine whether the vault conclusion mattered by window end.

### 4.1: Primary signal — NARRATIVE-PRICE DELTA

The **narrative-price delta** is the core engine's output: compare NEWS_DIRECTION against PRICE_DIRECTION independent of vault stance.

| News direction | Price direction | Delta label | Interpretation |
|---|---|---|---|
| positive | up | **aligned-up** | Narrative priced correctly; limited alpha |
| negative | down | **aligned-down** | Narrative priced correctly; limited alpha |
| positive | down | **inverted-bear** | Good news, stock fell — positioning/forward-risk signal |
| negative | up | **inverted-bull** | Bad news, stock rose — short-covering, capitulation floor, or forward-relief signal |
| positive | flat | **unreactive-good** | Priced in OR market skeptical of narrative |
| negative | flat | **unreactive-bad** | Priced in OR market dismissive of concern |
| none | up (>3%) | **flow-bull** | No news catalyst — positioning, sector rotation, or hidden signal |
| none | down (>3%) | **flow-bear** | No news catalyst — positioning, sector rotation, or hidden signal |
| none | flat | **quiet** | Nothing to say; ticker drops out of ranking |
| neutral | any | **mixed** | News was genuinely mixed; classification inconclusive |
| any | unknown | **data-gap** | Price unavailable; classification inconclusive |

**Gap magnitude** — the ranking key in Phase 5:

```
gap_magnitude = 
  | inverted-bear  → 1.5 × |price_move_pct|   # highest-signal: good news sold into
  | inverted-bull  → 1.5 × |price_move_pct|   # highest-signal: bad news bought
  | flow-bull      → 1.0 × |price_move_pct|   # unsigned flow signal
  | flow-bear      → 1.0 × |price_move_pct|
  | mixed          → 0.5 × |price_move_pct| if |price_move_pct| ≥ 3% else 0   # a big move on genuinely-mixed news (e.g. beat + guidance cut) IS the market resolving the ambiguity — do NOT zero it out
  | unreactive-*   → 2.0 + 0.5 × |price_move_pct|   # base 2.0 + scaling: range 2.0–3.5; crosses the Phase 4.4 cluster threshold (3.0) at |move| ≥ 2%
  | aligned-*      → 0                         # already priced, no alpha
  | quiet/data-gap → 0
```

The 1.5× weight on inverted deltas reflects trader intuition: price rejecting narrative is a stronger signal than price confirming it. Confirmed narrative is consensus; rejected narrative is asymmetric information. The `mixed` 0.5× rung (added 2026-07-09) closes a gap where a large-move mixed-earnings name — the single most common ambiguous-catalyst case — scored 0 and silently dropped out of the Trade Ideas ranking despite being highly actionable. The `unreactive-*` formula was changed from `max(2.0, 0.5×|move|)` to `2.0 + 0.5×|move|` (2026-07-09): with `flat` defined as |move| ≤ 3%, the old max() always evaluated to exactly 2.0 — dead code that made cluster-level unreactive signal (threshold 3.0) unreachable by construction.

### 4.2: Secondary signal — VAULT STANCE vs DELTA

Once the narrative-price delta is computed, the vault's recent stance determines whether we have alpha or reflection to do.

| Delta | Vault direction | Read |
|---|---|---|
| inverted-bear | weakened | **Vault was right, ahead of market** — recent Log entries / addressed callouts weakened the thesis while market only now reacted. Harvest (trim, lock conviction). |
| inverted-bear | strengthened | **Vault fighting market** — vault strengthened view while market rejects positive narrative. Either vault sees through the surface catalyst (alpha) OR vault is wrong (reflection). Stress test. |
| inverted-bear | neutral / mixed | **Missed signal** — market moved on something vault didn't flag. Deepen the thesis; likely behind. |
| inverted-bull | strengthened | **Vault was right, ahead of market** — vault strengthened through bad news that market bought. Reinforce position. |
| inverted-bull | weakened | **Vault fighting market** — vault weakened while market bought the dip/news. Reassess; either vault too bearish or market wrong. |
| flow-bull / flow-bear | strengthened/weakened aligned | **Vault anticipated flow** — may be leading indicator. Consider action. |
| flow-bull / flow-bear | neutral | **Vault uninformed** — flow happening without vault view. Surface candidate for `$thesis` or `$deepen`. |
| unreactive-* | weakened/strengthened | **Positioning/timing bet** — vault has conviction, market deferring. Catalyst watch (see `$catalyst`). |
| aligned-* | any | **No action** — narrative and price agree; vault context is commentary, not alpha. |

### 4.3: Output schema per ticker

```yaml
ticker: TICKER
vault_direction: strengthened | weakened | mixed | neutral
news_direction: positive | negative | neutral | none
price_direction: up | down | flat | unknown
delta_label: aligned-up | aligned-down | inverted-bear | inverted-bull | unreactive-good | unreactive-bad | flow-bull | flow-bear | quiet | mixed | data-gap
gap_magnitude: [float]
read: [one-sentence interpretation from §4.2 matrix]
earnings_event_in_window: true | false
transcript_themes: [list or null]
```

### 4.4: Graph-primer aggregation

For each ticker with material classification (gap_magnitude > threshold of 3.0), consult the graph primer (if loaded in Step 0.4) for cluster peers. If ≥2 cluster peers share the same delta label → flag as **cluster-level signal** in the trade idea; otherwise idiosyncratic. Cluster-level inverted-bear across 3+ peers = sector rotation signal, not ticker-specific.

## Phase 4.5: Calibration — persist this run's calls, score matured prior calls

**Why (closes the self-agreement loop).** Retro's core engine grades the market against the vault's own recent stance, and the vault's stance is derived by trusting prior Log/callout entries at face value (§4.2 VAULT_DIRECTION). Nothing checks whether the vault was actually *right*. Calibration is the independent check: it scores the retro's OWN past directional calls against realized price outcomes, building an empirical hit-rate over time — the vault's personal base-rate book ([[Generalist - Overview]] [G-10]: anchor to the reference class before the inside-view narrative). A retro that never scores itself is an inside-view engine with no feedback.

### 4.5a: Derive this run's directional calls

For each ticker in the Trade Ideas set (gap_magnitude > 0), derive an `implied_forward` sign from the §4.2 read + suggested action:

| Suggested action (from §4.2) | implied_forward |
|---|---|
| Reinforce / add (inverted-bull + vault strengthened) | **bullish** |
| Harvest / trim (inverted-bear + vault weakened) | **bearish** |
| Deepen / New thesis / Monitor / Stress test | **neutral** (no directional bet — logged, but excluded from hit-rate; "stress test" = vault-fighting-market, the resolution is tracked separately in 4.5c) |

`flow-bull`/`flow-bear` with an aligned vault direction → bullish/bearish respectively; unaligned → neutral.

### 4.5b: Persist (append-only JSONL)

```bash
mkdir -p .data          # gitignored
```

Append one line per Trade-Idea ticker to `.data/retro-calls.jsonl` (via `printf >>` — retro has no `Write`-to-arbitrary-path constraint here, printf is in allowed-tools):

```
{"call_date":"YYYY-MM-DD","window":"1w|1m|1q","ticker":"NVDA","delta_label":"inverted-bear","vault_direction":"weakened","implied_forward":"bearish","gap_magnitude":10.8,"scored":false}
```

Never rewrite existing lines here — this is the immutable call record. Scoring (4.5c) writes outcomes to a separate `.data/retro-outcomes.jsonl` keyed by `call_date+ticker`, so the call log stays append-only and a re-run cannot corrupt prior calls.

### 4.5c: Score matured prior calls

`cat .data/retro-calls.jsonl` (skip silently if absent — first ever run has nothing to score) and `cat .data/retro-outcomes.jsonl` (may be absent). In the reasoning layer, select calls that are:
- **Mature**: `call_date` is at least `max(window_days, 21)` days before TODAY (a directional call needs time to resolve), AND at most ~400 days old (bound lookback cost).
- **Unscored**: no matching `call_date+ticker` in `retro-outcomes.jsonl`.
- **Directional**: `implied_forward ∈ {bullish, bearish}` (neutral calls are not hit-rate-scored; "stress test" vault-fighting calls ARE resolved in 4.5c's separate tally).

**Cap at 10 calibration price queries per run** (bound web search cost — same discipline as the Phase 3.3 transcript cap). Prioritise the oldest-unscored and highest-gap_magnitude calls. Reuse `.data/retro_cache/` where fresh. For each selected call, one web search: `[TICKER] stock price [call_date] to [TODAY] percentage change`. Classify realized direction (±3% threshold, same as Phase 4). Outcome:
- `hit` — realized direction matches implied_forward.
- `miss` — realized direction opposes implied_forward.
- `push` — realized |move| ≤ 3% (flat) or price data unavailable (`data-gap`, excluded from hit-rate denominator).

For "stress test" (vault-fighting-market) calls, resolve separately: did the price ultimately move the vault's way (vault vindicated) or the market's way (vault wrong)? Tally as `vault_vindicated` / `market_right` — this is the highest-signal calibration output, since vault-fighting-market is where the vault claims non-consensus edge.

Append outcomes to `.data/retro-outcomes.jsonl`:
```
{"call_date":"YYYY-MM-DD","ticker":"NVDA","implied_forward":"bearish","realized_move_pct":-9.4,"outcome":"hit","scored_on":"TODAY"}
```

Compute for the Phase 6 scorecard: overall hit-rate (hits / (hits+misses)), hit-rate by `delta_label`, and the vault-fighting-market vindication tally. If fewer than ~8 scored calls exist total, render the scorecard but caveat `n too small — directional only`.

## Phase 5: Trade Ideas Ranking

Rank all tickers by `gap_magnitude` descending (from Phase 4.1). Top 3–5 populate the **Trade Ideas** section. Tickers with `gap_magnitude = 0` (aligned, quiet, mixed, data-gap) drop out — they carry no trade signal.

Each trade idea renders:

- **Ticker** + one-liner: `[delta_label] ([news summary] vs [price move]), vault [vault_direction]`
- **Read** (from Phase 4.2 matrix): e.g., "Vault was right, ahead of market — harvest" or "Missed signal — deepen"
- **Narrative detail**: top 1-2 news events with polarity, earnings result if applicable, key transcript theme if fetched
- **Price detail**: window move %, intraday volatility if notable
- **Suggested action** (one of, mapped from §4.2 matrix):
  - `Harvest / trim` — vault was ahead, market just caught up
  - `Reinforce / add` — vault reading contradicted by surface, aligned with price direction
  - `Stress test` — vault fighting market, needs adversarial review → `$stress-test TICKER`
  - `Deepen` — vault missed the signal → `$deepen TICKER [section]`
  - `Monitor for catalyst` — vault conviction + unreactive price → `$catalyst` watch
  - `New thesis candidate` — flow move with no vault view → `$thesis TICKER` or `$ingest`
- **Motivating evidence**: wikilinks to the specific addressed callout(s) + Log entry(ies) + news headline that drove the classification
- **Cluster flag**: if Phase 4.4 surfaced cluster-level signal (`≥2 peers same delta`), prefix the read with `[cluster signal]` and list peers. Sector rotation trumps ticker-specific action.

**Never auto-execute**. Phase 7 optionally appends a `Retro insight:` Log entry to the affected thesis (see §7.1), but conviction and status changes require explicit user `$status` invocation.

## Phase 6: Output — Research Note (immutable)

### 6.1: Filename

`Research/YYYY-MM-DD - Retrospective [window-label] - Synthesis.md`

Examples:
- `Research/2026-04-24 - Retrospective 1w - Synthesis.md`
- `Research/2026-04-24 - Retrospective 1m - Synthesis.md`

If a file with this exact name exists (same window already generated today), append numeric suffix: `... Synthesis 2.md`, `... Synthesis 3.md`. Each retro is a new immutable artifact (per user spec #3).

### 6.2: Frontmatter

```yaml
---
date: YYYY-MM-DD
tags: [research, retrospective, synthesis]
status: active
source: vault retrospective
source_type: retrospective
window: 1w | 1m | 1q
window_start: YYYY-MM-DD
window_end: YYYY-MM-DD
tickers_touched: [TICKER1, TICKER2, ...]
propagated_to: []
---
```

> **Why `propagated_to: []`**: retro notes are exploratory portfolio-level metadata, not per-thesis evidence. The body wikilinks reference many theses for context, NOT to claim each one needs a Log entry from `$sync`. The empty list is a **terminal dedup signal** to `$sync` Step 1 Check 2 — the producer skill (this `$retro` run) explicitly declares "no propagation needed." Without it, the next `$sync` would treat each body wikilink as a propagation target. Mirrors `$surface`'s pattern.

> **Graph update deferred**: `_graph.md` is owned exclusively by `$graph`. After `$retro`, run `$graph last` to register the retro research note in the dependency map.

### 6.3: Body structure

```markdown
# Retrospective: [window-label] ([WINDOW_START] → [TODAY])

## Scope
- Window: [window-label] — [N] days
- Files scanned: [N] theses + [M] sectors + [K] macros
- Tickers with activity: [N]
- Addressed callouts: [N]
- Fresh (unresolved) callouts: [N]
- Log entries (non-skill-origin): [N]

## Trade Ideas (Top 5 by Narrative-Price Gap)
[ranked table — see Phase 5]

## Calibration Scorecard
[Phase 4.5c output — the vault's own track record on prior retro calls. Renders only if ≥1 prior call was scored this run; else "No matured prior calls to score yet."]

| Delta label | Scored | Hits | Misses | Hit-rate |
|---|---|---|---|---|
| inverted-bear | 6 | 4 | 2 | 67% |
| inverted-bull | 4 | 3 | 1 | 75% |
| flow-bull/bear | 5 | 2 | 3 | 40% |
| **Overall** | **15** | **9** | **6** | **60%** |

**Vault-fighting-market resolution** (the non-consensus-edge test): [N] "stress test" calls resolved — [X] vault vindicated / [Y] market right. [One-line read: is the vault's fighting-market instinct paying off, or is it fighting the tape?]

[Caveat if <8 total scored calls: "n too small — directional only."]

## Narrative vs Price vs Vault
[per-ticker table, sorted by gap_magnitude descending]

| Ticker | News | Earnings | Price | Vault | Delta | Gap | Read |
|---|---|---|---|---|---|---|---|
| NVDA | positive (guide raise, 2 upgrades) | beat + raised | -7.2% | weakened | inverted-bear | 10.8 | Vault ahead — harvest |
| BESI | positive (design win) | none | +0.4% | strengthened | unreactive-good | 2.0 | Positioning; catalyst watch |
| APP | none | none | +8.1% | neutral | flow-bull | 8.1 | Missed signal — investigate |
| AMD | negative (guide cut) | miss + lowered | +4.5% | strengthened | inverted-bull | 6.8 | Vault right — reinforce |

Column semantics:
- **News**: dominant polarity + 1-2 key events
- **Earnings**: surprise direction + guidance direction, or `none` if no event in window
- **Price**: window move %, threshold-flagged (`up`/`down`/`flat`) by ±3%
- **Vault**: direction derived from Phase 2 callout + Log aggregation
- **Delta**: label from Phase 4.1 narrative-price matrix
- **Gap**: `gap_magnitude` (ranking key)
- **Read**: one-phrase interpretation from Phase 4.2 vault-stance matrix

## What I Resolved
[per user spec #4 — proportional to window]

## What I Still Have Open
[fresh callouts with wikilink back to source file:section]

## Activity Log
[non-skill-origin Log entries, grouped by ticker then date descending]

## Portfolio-Level Activity
[sector/macro callouts + Log entries not keyed to a single ticker]

## Follow-up Skills
[concrete `$deepen`, `$stress-test`, `$status` commands the user can run next]
```

### 6.4: "What I Resolved" — proportional rendering (user spec #4)

| Window | Rendering per addressed callout |
|---|---|
| `1w` | Full callout body + full response. Grouped by ticker, then by addressed date descending. |
| `1m` | Compressed: `YYYY-MM-DD · [ticker] · [section] — [one-line summary of question] → [one-line summary of response key insight]`. Full text archived via wikilink back to source file. |
| `1q` | Aggregated by ticker: `TICKER: [N] callouts addressed across sections [list]. Top 2 insights: [one-line each, chosen by conviction-impact proxy — prefer entries that surfaced in Trade Ideas ranking].` Full text available via wikilink. |

The rendering tier is a function of window length, not of callout count. A 1w retro with 40 callouts still renders full — the reader chose the tight window to get the full record.

### 6.5: "What I Still Have Open"

Fresh callouts in window, sorted by age descending (oldest fresh = most urgent):

```
- **[YYYY-MM-DD]** · [type] · [[file:section]] — [body one-liner]
```

Pinned fresh callouts render with `· pinned` marker — informational, signals user chose not to address.

### 6.6: Follow-up skills block

For each top-5 Trade Idea, emit the exact command(s) the user would type. Command selection is driven by the Phase 4.2 vault-stance-vs-delta matrix:

```
- [[NVDA - Nvidia]]: inverted-bear (news+, price -7.2%), vault weakened — harvest signal.
  - `$status NVDA conviction high→medium` — lock the read vault already made
  - `$brief NVDA` — generate IC-ready pitch for partial trim sizing

- [[APP - AppLovin]]: flow-bull (no news, price +8.1%), vault neutral — missed signal.
  - `$ingest https://[news-url]` — seed Research with what moved the tape
  - `$thesis APP` — vault has no view; decide whether to formalize

- [[AMD - Advanced Micro Devices]]: inverted-bull (guide cut, price +4.5%), vault strengthened — reinforce.
  - `$deepen AMD "Key Non-consensus Insights"` — articulate why vault sees through the miss

- [[BESI - BE Semiconductor]]: unreactive-good (design win, price +0.4%), vault strengthened — catalyst watch.
  - `$catalyst` — confirm BESI next catalyst date; position ahead
```

The retro never executes any of these — it lists them. The user decides which to run.

## Phase 7: Thesis Log Entries (top 3–5 only)

### 7.1: Scope

Append one `Retro insight:` Log entry to the thesis of each ticker in the Trade Ideas Top 3 (NOT all top-5 — limit Log pollution to the highest-signal divergences). Tickers ranked #4-#5 are surfaced in the retro note only.

### 7.2: Format

```
### <TODAY>
- Retro insight: [1w|1m|1q] retro — [delta_label] (news [+|-|none], price [±X.X%]) vs vault [direction]. [One-sentence read from §4.2 matrix]. See [[Research/YYYY-MM-DD - Retrospective [window] - Synthesis]].
```

Example:
```
- Retro insight: 1w retro — inverted-bear (news +, price -7.2%) vs vault weakened. Vault was ahead of market on hyperscaler demand softening — harvest signal. See [[Research/2026-04-24 - Retrospective 1w - Synthesis]].
```

**Prefix choice**: `Retro insight:` is NOT in `.agents/skills/_shared/log-prefixes.md`'s skill-origin list (unregistered prefixes default to non-skill-origin). This is deliberate — per AGENTS.md Workflow Rule 6, a non-skill-origin prefix forces the next `$sync` to treat the entry as research-driven and propagate normally to sector/macro notes. If the retro surfaces a divergence that materially changes sector-level thinking, `$sync` should pick it up.

### 7.3: Edit strategy (same-day append aware)

Use the same Case-4.3c.A / Case-4.3c.B two-path approach documented in `archive-callouts/SKILL.md` Phase 4.3c:

- If `### <TODAY>` header already exists in the thesis's `## Log`, append the bullet under the existing header. Never create a second same-day header; never reorder.
- If no `### <TODAY>` header exists, append a new dated section at end-of-file (Log is always the last section in the thesis template).

After each Edit, re-grep for the new bullet to verify it landed. Silent-failure retry with expanded context, per Phase 4.3c retry rules.

**If Log append fails after retry**: do NOT abort the retro. Body Research note is the primary artifact; Log back-references are a convenience. Report `⚠️ Log back-reference to [[TICKER]] failed — retro note persisted, manual append recommended.`

### 7.4: Open-findings register (per `.agents/skills/_shared/followups-contract.md`)

The `Retro insight:` Log entries (7.1–7.3) live inside each thesis; `_followups.md` is the cross-run index that survives so an unactioned trade idea does not evaporate. For each Top-3 Trade Idea whose delta signals a vault-market mismatch requiring action (`inverted-bear`, `inverted-bull`, `flow-bull`/`flow-bear` with a vault view, `unreactive-*` with strong vault direction — i.e. every non-`aligned` top idea), append one entry to `_followups.md` `## Open`:

```
- [ ] YYYY-MM-DD · retro · [[Theses/TICKER - Name]] · [delta_label] divergence, [suggested action] → user acts or dismisses · src [[Research/YYYY-MM-DD - Retrospective [window] - Synthesis]]
```

**Dedup** (followups-contract): grep `## Open` for an existing `retro ·` entry on the same thesis; if present, update its date rather than stacking (a weekly `$retro` must not pile the same idea). Read `_followups.md` first (create per schema if absent — retro has `Write`). Obey the 50-entry soft-cap warning. Resolvers `$status` (action taken) and `$sync` (absorbed into thesis body) close these entries later. Register-write failure is non-fatal, same as 7.3 — report and continue.

## Phase 8: `_hot.md` Update

Read `_hot.md` then edit per `.agents/skills/_shared/hot-md-contract.md`. If `_hot.md` does not exist, create it per AGENTS.md Rule #9 schema.

### 8.1: Active Research Thread

- **Same-topic continuation** (existing thread already covers `$retro` work): append a dated line `YYYY-MM-DD: [window] retro completed — top finding: [ticker + classification + key insight one-phrase].`
- **New topic**: compress the outgoing thread into a single `*Previous YYYY-MM-DD:*` line, prepend, then replace thread body with the retro summary above.

### 8.2: Open Questions

For each Top-5 Trade Idea where the delta label signals a vault-market mismatch, add an Open Question. The label → question-template mapping:

| Delta label + vault stance | Open Question template |
|---|---|
| `inverted-bear` + vault strengthened | `[[TICKER]]: narrative+ but price fell ([X%]) over [window] while vault strengthened. What forward risk is the market pricing that vault missed? (flagged by $retro YYYY-MM-DD)` |
| `inverted-bull` + vault weakened | `[[TICKER]]: narrative- but price rose ([X%]) over [window] while vault weakened. Is the bear case already discounted, or is vault over-focused on the miss? (flagged by $retro YYYY-MM-DD)` |
| `flow-bull` / `flow-bear` + vault neutral | `[[TICKER]]: stock moved [X%] over [window] with no catalyst and no vault view. What is the market seeing that vault hasn't formed a view on? (flagged by $retro YYYY-MM-DD)` |
| `unreactive-*` + vault strong direction | `[[TICKER]]: vault [direction] on [narrative] but price flat over [window]. What catalyst is needed to close the gap? (flagged by $retro YYYY-MM-DD)` |

Dedup: suppress only if an existing question contains BOTH the ticker wikilink AND the distinctive fragment `flagged by $retro`. Existing questions from `$thesis`, `$stress-test`, `$surface`, `$catalyst` must NOT suppress this — retro-specific dedup is narrow by design. Same rationale as `$catalyst` Phase 5 dedup logic (§148 of catalyst SKILL.md).

`aligned-*` deltas do NOT generate Open Questions — market agreed with narrative, no puzzle to investigate.

### 8.3: Other sections

- **Latest Sync**: not touched (owned by `$sync`).
- **Sync Archive**: not touched (owned by `$sync`).
- **Recent Conviction Changes**: not touched (owned by `$status`).
- **Portfolio Snapshot**: not touched (owned by `$sync`).

### 8.4: Word cap

After edits, count total. Over 8,000 → run compression trigger order per hot-md contract §Compression trigger order (steps 1-3: drop Sync Archive / *Previous:* / merge OQ; steps 4-5: drop pre-14d OQ cohorts + roster-compress pre-30d RCC entries; step 6: aggressive RCC fallback if still over hard cap). Over 10,000 after step 7 → abort `_hot.md` update with: `❌ _hot.md exceeds hard cap (10,000 words) after full compression — retro note still persisted.`

Retro note write is unconditional; `_hot.md` update is best-effort.

## Phase 9: Release Lock and Report

### 9.1: Release

Final shell block verifies ownership and releases:

```bash
LOCK_FILE=".vault-lock"
EXPECTED_TOKEN="<paste-token-captured-from-Step-0.1>"
if [ -f "$LOCK_FILE" ] && grep -q "token: $EXPECTED_TOKEN" "$LOCK_FILE"; then
  rm -f "$LOCK_FILE" && echo "=== LOCK RELEASED ==="
else
  echo "⚠️ Lock ownership check failed at release — skipping rm to avoid stealing another skill's lock."
fi
```

Runs unconditionally — success, empty-window, web search failures, Log-append failures all reach this step.

### 9.2: Report to user

```
## $retro [window-label] complete

Window:           [WINDOW_START] → [TODAY] ([N] days)
Files scanned:    [N] theses / [M] sectors / [K] macros
Addressed:        [N] callouts resolved
Still open:       [N] fresh callouts (oldest: [date], ticker: [X])
Log activity:     [N] non-skill-origin entries across [N] tickers
Market data:      [N] tickers with price; [N] news events; [N] earnings events; [N] transcripts fetched
Calibration:      [N] prior calls scored — overall hit-rate [X]% ([hits]/[hits+misses]); vault-fighting-market [X vindicated / Y market-right]  (or "no matured calls yet")
Open findings:    [N] entries added to _followups.md (Top-3 divergences)

Top narrative-price gaps (see full Research note for details):
  1. [TICKER] — [delta_label] ([news polarity] vs [price move]) — [one-phrase read]
  2. [TICKER] — [delta_label] ([news polarity] vs [price move]) — [one-phrase read]
  3. [TICKER] — [delta_label] ([news polarity] vs [price move]) — [one-phrase read]

Cluster signals: [list if any surfaced in Phase 4.4, else "none"]

Research note: [[Research/YYYY-MM-DD - Retrospective [window] - Synthesis]]
Log back-references appended to: [list up to 3 tickers]
_hot.md: [summary of section updates, or "no updates" if nothing changed]

Next steps:
  → Run $graph last to register the retro note in the dependency graph
  → Review Trade Ideas and decide whether to act via $status, $stress-test, $deepen, $ingest, or $thesis
```

**Runs in a delegated subagent** (see Execution context at top) — the Phase 9.2 report is produced inside the subagent and re-emitted verbatim by the main thread, so the ~60 full-file reads + up to ~126 web search results + up to 5 earnings-transcript fetches (~400K tokens) stay out of main-session context. The Research note persists to disk as the authoritative artifact regardless.

## Invariants

1. **Immutable output** — each run creates a new Research note. Never overwrite an existing retro file; append counter suffix when filename collides.
2. **No conviction/status mutations** — Phase 5 Trade Ideas are informational. `$status` changes require explicit user invocation.
3. **`propagated_to: []` is terminal** — retro notes are metadata, not evidence; do not trigger fanout `$sync` propagation.
4. **`Retro insight:` is NOT a skill-origin prefix** — deliberate choice: allows `$sync` to propagate downstream sector/macro updates if a retro-surfaced divergence materially shifts sector thinking.
5. **Graph-primer is an orientation aid, never a filter** — per `.agents/skills/_shared/graph-primer.md` anti-patterns. Retro reads every thesis in full regardless of cluster membership.
6. **Empty window exits cleanly** — Phase 2.5 short-circuit releases the lock and exits without writing.
7. **Lock is vault-wide** — prevents concurrent `$sync`, `$catalyst`, `$surface`, `$prune`, `$graph` from racing on shared reads.
8. **Calibration call log is append-only** — `.data/retro-calls.jsonl` records each run's directional calls immutably; outcomes are written to a separate `.data/retro-outcomes.jsonl` keyed by `call_date+ticker`. Scoring never rewrites the call log, so a re-run cannot corrupt or double-count prior calls. Both are gitignored (`.data/`).

## Failure modes and recovery

| Failure | Recovery |
|---|---|
| Lock acquisition fails | Hard-block with standard `/shared/preflight.md` §1.4 message. User waits or force-unlocks after verifying stale. |
| File Read fails mid-Phase-1 batch | Continue with successful reads; report `⚠️ N files unreadable — retro based on partial vault state.` Reduces signal fidelity, does not block output. |
| Price web search fails for a ticker | Record `price.direction: unknown`; ticker classified as `data-gap`, drops to gap_magnitude = 0, excluded from Trade Ideas. Still appears in the Narrative vs Price table with `price: data unavailable`. |
| News web search fails for a ticker | Record `news.dominant_polarity: none`; ticker uses price-only classification path (`flow-bull` / `flow-bear` / `quiet`). Reduced signal fidelity, still produces trade ideas if price move is material. |
| Earnings web search fails for a ticker | Record `earnings.event_in_window: false` (defensive — we can't confirm). Ticker classified on news + price only. |
| Transcript fetch fails (defuddle / web fetch/open) | Record `transcript_fetched: false`, `transcript_themes: null`. Earnings still contribute to `news_direction` via surprise + guidance fields. Note in the retro: `⚠️ transcript unavailable for [TICKER] — classification uses earnings result only.` |
| All Phase 3 web search calls rate-limited | Skill continues; Phase 4 classification emits `data-gap` for every ticker. Market overlay section shows `⚠️ Market data unavailable for this run — retro shows vault activity only, no market classification. Re-run $retro later.` Vault-activity sections (Resolved / Still Open / Activity Log) still populate fully. |
| Phase 7 Log-append fails on a specific thesis | Report the specific file; retro note persists. Manual fix: append `Retro insight:` bullet per Phase 7.2 format. |
| `_hot.md` update fails hard-cap check | Retro note still persists. `_hot.md` unchanged. Report `⚠️ _hot.md at hard cap — skipped update. Manual cleanup needed.` |
| Empty window (no activity) | Phase 2.5 short-circuit — no note written, lock released. |
| Lock ownership lost (`LOCK_STOLEN`) | Abort immediately. Report which Phase was in-flight and whether the retro note landed. If retro note partially written, leave it (reviewable); do NOT attempt cleanup. |

## Cadence (operational suggestion)

Pair with `/cron` (see the `/schedule` skill). Suggested defaults:

- `$retro 1w` — every Friday evening
- `$retro 1m` — first trading day of the month
- `$retro 1q` — first trading day of the quarter

Each run produces an independent immutable artifact. The `$graph last` reconciliation should follow each retro to register the new Research note.

## Design notes

- **Why vault-wide lock (not read-only)**: retro writes a Research note, appends Log entries to 3-5 theses, and updates `_hot.md`. These writes conflict with concurrent `$sync` or `$catalyst`. Read-only lock is insufficient.
- **Scoped mode (added 2026-07-08)**: single-ticker retro (`$retro 1w NVDA`, `$retro NVDA`) is now supported — a trailing non-window token parses as a ticker (Arguments). It sets `TICKER_UNIVERSE = {ticker}`, reads only that thesis + its graph-linked sector/macro notes in Phase 1, issues one 3-query message in Phase 3, and does NOT empty-window-short-circuit (the user asked for this ticker explicitly). The vault-wide view remains the default for portfolio-level "recommend trades." The graph primer is orientation-only here too (Invariant 5) — scoped mode narrows reads, never analysis correctness.
- **Activity-gated Phase 1 (added 2026-07-08)**: vault-wide runs grep-triage all theses/sectors/macros for in-window callout/Log activity first, then full-read only active files (~5-15 for `1w` vs ~60). Callouts are inline-anywhere so per-file section-narrowing is unsafe, but skipping zero-activity files entirely is safe and scales the read cost with actual activity. `TICKER_UNIVERSE` still derives from the active set, so no active ticker is dropped.
- **Overlay cache (added 2026-07-08)**: per-ticker price/news/earnings overlay cached to `.data/retro_cache/` with a 3-day freshness guard, so an overlapping `1w`→`1m` run doesn't re-fetch identical recent data. Advisory only — a miss is a normal query; the freshness guard prevents stale market data entering a fresh classification.
- **Fork history — frontmatter fork reverted, Agent delegation adopted**: 2026-06-07 the frontmatter `context: fork` mechanism was reverted because the harness returned the report as unrendered stdout, leaving the chat panel blank. 2026-07-08 the skill moved to **Agent-tool delegation** (see Execution context at top): the subagent does the ~400K-token read/search work and returns the full report as a tool result; the main thread re-emits it verbatim, so rendering is preserved AND main-context cost is just the returned report. The two mechanisms are distinct — do not "restore main-thread execution" on the assumption that delegation reintroduces the 2026-06-07 blank-panel bug; it does not. Revert path if delegation ever truncates: delete the Execution-context section, and the skill runs inline again (report renders, but ~400K tokens land in main context).
- **Why narrative-price delta is the core engine**: "what did the market say happened vs what did the stock do" is the classical trader signal for positioning opportunities. Aligned narrative + price = already priced, no alpha. Inverted narrative + price = market is pricing something the surface news isn't showing — positioning, forward risk, capitulation, or vault's non-consensus view is right. The vault's recent stance then separates alpha (vault predicted the divergence) from reflection (vault missed it). This is why the 1.5× weight on inverted deltas vs 1.0× on flow-only signals: rejected narrative is asymmetric information, confirmed narrative is consensus.
- **Why exclude social sentiment**: per user spec — official narrative channels (press releases, SEC filings, earnings, analyst actions) are structured, date-anchored, and polarity-classifiable. Social sentiment (X/Twitter/Reddit) is noisy, hard to polarity-classify at scale, and typically echoes official narrative with a lag. Including it would expand web search fan-out 2-3× without proportional signal gain.
- **Why cap transcript fetches at 5 per run**: earnings transcripts are ~8-15K tokens each. An uncapped fetch on a heavy-earnings week (5+ tickers reporting) would blow the context budget. Pre-screen selects the 5 most likely to rank in Trade Ideas Top 5 — low-ranking earnings contribute via the Earnings web search snippet (surprise + guidance direction) without the full transcript read.
- **Why proportional rendering** — per user spec. A 1q retro with 300 addressed callouts rendered in full would exceed the useful signal density of the note. Aggregation at long windows preserves the "what changed" signal without forcing the reader through 300 verbatim exchanges.
