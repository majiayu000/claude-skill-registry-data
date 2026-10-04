---
name: catalyst
description: Extract and maintain a cross-portfolio catalyst calendar from all thesis notes. Use when user says "catalyst", "calendar", "what's coming up", "upcoming events", or "what could move the portfolio".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$catalyst`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Build a comprehensive catalyst calendar aggregating every upcoming event across the portfolio.

## Progress Reporting Contract (MANDATORY)

`$catalyst` is a long-running command (~71 thesis + macro reads, FMP fetches, retries) whose intermediate work would otherwise stay silent until the final Phase 6 report — a 5–30+ minute silent window during which errors, retries, FMP timeouts, and degraded-mode downshifts are invisible. To close this gap, emit a one-line status message **as plain text between tool calls** (not buried inside shell `echo`, not as a tool argument) at every phase boundary and every retry / error / degraded-path event.

**Why plain text, not shell echo**: shell `echo` is visible but rendered inside collapsed tool-output blocks. Plain text between tool calls is the primary signal the user reads to track progress mid-run. Keep the existing `echo` statements (they're the audit trail) AND add plain-text emits (they're the live progress feed) — both are required.

**Format**:
- Phase start: `📍 Phase X.Y: [what's starting + expected scale]` — e.g. `📍 Phase 1: launching parallel read batch (65 theses + 6 macros)`
- Phase complete: `✅ Phase X.Y: [what completed + key metric]` — e.g. `✅ Phase 2a: FMP matched 58/64 tickers, 6 queued for web search`
- Soft failure / degraded path: `⚠️ Phase X.Y: [what failed + what's happening next]` — e.g. `⚠️ Phase 2a: FMP first attempt failed (rc=99 empty array), retrying in 5s`
- Hard failure / abort: `❌ Phase X.Y: [what failed + abort reason]` — e.g. `❌ Phase 0.2: snapshot cp failed, aborting before any destructive write`

**Cadence**: every phase boundary (Phase 0.1, 0.2, 0.3, 1, 2a, 2b, 3, 4, 5, 6) + every retry / error / cap-activation event. Aim for one status line every 10–30 seconds of wall-clock work; silences longer than that mean the user wonders if the skill is stuck.

**Do not** emit per-file progress within a parallel batch (e.g., "read thesis 1 of 65", "web search 3 of 20"). Batch-level start/complete is enough; per-file noise drowns the signal.

**Reference scale (2026-05-23 portfolio)**: 65 theses, 6 macro notes, ~64 active/monitoring tickers for FMP enrichment. Phases 1 and 2 are the two longest segments — emit start AND complete messages for both even if they feel redundant.

## Phase 0: Pre-flight (MANDATORY — runs before Phase 1)

### 0.1: Acquire vault lock
Acquire a `vault-wide` scope lock per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout budget: 5 minutes. Capture the token, verify ownership (Procedure 1.5) at every subsequent shell block, release in the final reporting shell block.

📍 **Emit before**: `📍 Phase 0.1: acquiring vault-wide lock`
✅ **Emit after**: `✅ Phase 0.1: lock acquired (token <token>)`
⚠️ **Emit on stale-lock break-in or contention**: `⚠️ Phase 0.1: existing lock found — [stale (broken) | active (waiting Xs)]`

### 0.2: Snapshot existing `_catalyst.md` (mandatory pre-regenerate snapshot — H2 fix: hard-abort on failure)

Before regenerating `_catalyst.md`, snapshot the prior version. **If the snapshot cp fails, HARD ABORT `$catalyst`** — do not proceed to regenerate, because a regenerate failure after a failed pre-snapshot loses the prior calendar with no recovery path.

📍 **Emit before**: `📍 Phase 0.2: snapshotting prior _catalyst.md`
✅ **Emit after**: `✅ Phase 0.2: snapshot written to _Archive/Snapshots/_catalyst (pre-catalyst <date>-<HHMMSS>).md`
ℹ️ **Emit when no prior file**: `ℹ️ Phase 0.2: no prior _catalyst.md — first run, snapshot skipped`
❌ **Emit on hard abort**: `❌ Phase 0.2: snapshot failed (<cp error | empty file>) — aborting before any destructive write`

```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
SNAPSHOT_PATH="_Archive/Snapshots/_catalyst (pre-catalyst YYYY-MM-DD-$HHMMSS).md"

if [ -f "_catalyst.md" ]; then
  if ! cp "_catalyst.md" "$SNAPSHOT_PATH"; then
    echo "SNAPSHOT_FAILED|$SNAPSHOT_PATH"
    exit 1
  fi
  # Verify the copy actually landed with non-zero size (cp can silently no-op on some filesystems)
  if [ ! -s "$SNAPSHOT_PATH" ]; then
    echo "SNAPSHOT_EMPTY|$SNAPSHOT_PATH"
    rm -f "$SNAPSHOT_PATH"
    exit 1
  fi
fi
```

Then add snapshot frontmatter to the newly created file:
```yaml
snapshot_of: "[[_catalyst.md]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: catalyst
snapshot_batch: catalyst-YYYY-MM-DD-HHMMSS
```

**Snapshot failure handling (H2)**: if either the cp fails or the resulting file is empty, abort with:

```
❌ $catalyst pre-regenerate snapshot failed: [path]
   Reason: [cp error | empty file after copy]

No regeneration attempted. The current _catalyst.md is unchanged. Fix the
underlying filesystem issue (disk space, permissions, _Archive/Snapshots/
directory writability) and re-run $catalyst. Prior calendar is intact.
```

Exit the skill cleanly — do NOT proceed to Phase 1. The prior `_catalyst.md` is preserved at its current path; the next successful `$catalyst` run will snapshot and regenerate.

**Frontmatter-add failure**: if the cp succeeds but the subsequent frontmatter Edit fails, proceed with regeneration anyway — the snapshot file content is preserved (bit-exact copy of the prior `_catalyst.md`), just without the `snapshot_of:` metadata. `$rollback` can still restore it via direct cp-back; it won't appear in `$rollback` cascade detection by batch ID, but the user can locate it by filename pattern (`_catalyst (pre-catalyst *)`).

**Why the hard abort matters**: prior behavior proceeded with regeneration after silent cp failure. If web search then failed mid-regenerate, the partial calendar overwrote the prior version with no snapshot to roll back to. Daily backup was the only fallback. Hard-abort guarantees the prior calendar is always recoverable from the pre-regenerate snapshot before any destructive write.

If no prior `_catalyst.md` exists (first run), skip the snapshot step (the `[ -f "_catalyst.md" ]` guard handles this) and proceed to Phase 1.

### 0.3: FMP API key probe (soft — degrade-on-failure)

Try to load the FMP API key. Unlike `$numbers` and `$transcript`, `$catalyst` does NOT abort on FMP failure — it falls back to web search (the prior behavior). Capture the result as a flag for Phase 2.

📍 **Emit before**: `📍 Phase 0.3: probing FMP API key`
✅ **Emit on success**: `✅ Phase 0.3: FMP key loaded — Phase 2a will use FMP universe endpoint`
⚠️ **Emit on miss**: `⚠️ Phase 0.3: no FMP key — Phase 2 will use web search fallback only (capped at 20)`

```bash
FMP_OK=0
if [ -f .data/config.json ]; then
  API_KEY=$(jq -r '.fmp_api_key // empty' .data/config.json)   # jq, not sed -E '\s' (BSD sed unsupported → whole-line key → rc=3 curls)
  if [ -n "$API_KEY" ] && [ "$API_KEY" != "null" ]; then
    FMP_OK=1
    echo "FMP_OK"
  fi
fi
[ "$FMP_OK" = "0" ] && echo "FMP_UNAVAILABLE — Phase 2 will use web search fallback only"
```

Record `FMP_OK` and `API_KEY` for Phase 2. The skill's primary deliverable (the calendar) is functional in either mode — FMP is a speed/precision upgrade, not a correctness gate.

## Phase 1: Load the Portfolio (Parallel Full Reads)

📍 **Emit before**: `📍 Phase 1: launching parallel read batch (<N> theses + <M> macros = <N+M> Reads in one round-trip)`
✅ **Emit after**: `✅ Phase 1: <N+M> files loaded — moving to extraction`
⚠️ **Emit if any Read fails**: `⚠️ Phase 1: <K>/<N+M> reads failed (<filenames>) — continuing with available files`

**Issue all thesis Reads AND all macro Reads in a single parallel tool-call batch** — one message with ~71 Read invocations (65 theses + 6 macros at current scale; scales with vault), not serial loops. This collapses the I/O into one round-trip while preserving full-file context: the LLM sees every thesis body in full so cross-section catalyst signal (e.g., a regulatory date mentioned in Bull Case, a product launch referenced in Business Model) isn't lost to over-aggressive section pre-filtering.

### 1.1 Parallel batch composition

- **Read** every `Theses/*.md` in full (all files — draft, active, monitoring; every thesis can carry catalysts).
- **Read** every `Macro & Technology/*.md` in full (bounded set, ~6 files — rate decisions, geopolitical deadlines, commodity contract expirations, AI bubble risk, stablecoin regulation, etc.).

All reads land in one round-trip. Do NOT serialize per-file.

### 1.2 Extract from the pulled content

Within each thesis, prioritize **Catalysts**, **Risks**, and the last 5 **Log** entries (highest-density sections for event extraction) but **maintain peripheral awareness of other sections** — a catalyst may surface in Bull/Bear Case, Summary, or Business Model when the author didn't duplicate it into the Catalysts list. Full-file context is kept intentionally; `$catalyst` favors completeness over narrow extraction.

Per thesis:
- **Catalysts** section: event description, approximate date or date range (if stated), expected impact direction (positive / negative / uncertain), magnitude estimate (major / minor).
- **Conviction Triggers** section (when present — ~half the theses): extract each `→ HIGH if` / `→ LOW if` / `→ CLOSE if` statement and pair it with any catalyst whose outcome would test it. This feeds the `Thesis test` column (Phase 4) — the calendar's falsification layer. The 000660 thesis's Catalysts table ("**Positive** if SK Hynix maintains ≥60% share") is the in-vault exemplar of the target pairing.
- **Log** entries: recently noted upcoming events (scan the last ~5 date headers; older entries typically describe past events).
- **Risks** section: risk events with timing (e.g., "regulatory decision expected Q2").
- **Elsewhere in the thesis**: flag any date-anchored event or upcoming catalyst mentioned in Bull Case, Bear Case, Summary, Industry Context, or Business Model that's absent from the Catalysts section — surface these as candidates the thesis may need to formalize.
- **Macro notes**: cross-portfolio macro events (rate decisions, geopolitical deadlines, commodity contract expirations).

## Phase 2: Enrich and Deduplicate

📍 **Emit at Phase 2 start**: `📍 Phase 2: enriching catalysts with FMP earnings dates (FMP_OK=<0|1>)`

- Where catalyst dates are vague ("Q2 2026", "H2"), convert to approximate calendar dates
- Identify catalysts that affect MULTIPLE theses (e.g., an earnings report from a major customer that affects several supplier theses)
- Flag catalysts that are stale — events that appear to have already passed based on their dates vs today's date
- **Enrich with upcoming earnings dates — FMP-first, web search fallback.**

  ### 2a. FMP universe call (when `FMP_OK=1` from Phase 0.3)

  📍 **Emit before**: `📍 Phase 2a: calling FMP universe earnings calendar (TODAY → +90d)`
  ✅ **Emit after success**: `✅ Phase 2a: FMP returned <rows> earnings rows, matched <hits>/<active+monitoring> theses`
  ⚠️ **Emit on retry**: `⚠️ Phase 2a: FMP attempt 1 failed (rc=<rc>) — retrying in 5s` then `✅ Phase 2a: FMP retry succeeded` OR `⚠️ Phase 2a: FMP retry also failed — downshifting to web search fallback (capped at 20)`

  Single curl to the universe earnings calendar over the next 90 days. One round-trip replaces what would otherwise be ~64 web searches (one per active/monitoring thesis). **Retry-once on transient failure** before downshifting to the web search fallback storm — empirically (2026-05-23 incident: two consecutive `$catalyst` runs at 14:50 and 15:12 timed out at ~9 min each because Phase 2a hit transient FMP failures and downshifted to a full 64-ticker web search storm; a 5-second retry would have salvaged both runs since FMP was healthy by 15:21).

  ```bash
  TODAY=$(date +%Y-%m-%d)
  END=$(date -v+90d +%Y-%m-%d 2>/dev/null || date -d '+90 days' +%Y-%m-%d)
  FMP_URL="https://financialmodelingprep.com/stable/earnings-calendar?from=$TODAY&to=$END&apikey=$API_KEY"

  fetch_fmp() {
    curl -sf --max-time 20 --connect-timeout 5 "$FMP_URL" > /tmp/catalyst_earnings.json
    local rc=$?
    if [ $rc -ne 0 ]; then return $rc; fi
    # Empty array is a known intermittent failure mode — treat as soft failure for retry purposes
    local rows
    rows=$(jq 'length' /tmp/catalyst_earnings.json 2>/dev/null)
    if [ "$rows" = "0" ] || [ -z "$rows" ]; then return 99; fi
    return 0
  }

  FMP_FETCH_RC=0
  if ! fetch_fmp; then
    FMP_FETCH_RC=$?
    echo "⚠️ FMP first attempt failed (rc=$FMP_FETCH_RC). Retrying after 5s..."
    sleep 5
    if ! fetch_fmp; then
      FMP_FETCH_RC=$?
      echo "⚠️ FMP retry failed (rc=$FMP_FETCH_RC). Downshifting to capped web search fallback."
      FMP_OK=0
    else
      echo "✅ FMP retry succeeded."
    fi
  fi
  ```

  **Timeout rationale**: FMP's universe earnings-calendar endpoint can TCP-establish and then stall mid-stream from networks with degraded routes (observed 2026-05-23: 500–600ms RTT, intermittent recv failures, `HTTP:000 SIZE:0` responses). Without `--max-time`, curl defaults to no transfer timeout — a stalled connection blocks `$catalyst` until the kernel TCP keepalive eventually closes the socket (5–10 min), which surfaces to the user as a skill stall with no progress signal. `--max-time 20` caps total transfer at 20s; `--connect-timeout 5` caps TCP handshake at 5s. Both well above healthy-path latency (~2s end-to-end) but tight enough to deterministically fall through to the retry / web search path below.

  **Retry rationale**: prior design said "Do NOT retry — the universe endpoint failing usually means the API key is wrong or quota is exhausted, neither of which a retry fixes." Reality: the dominant failure mode observed in production is transient (intermittent network blips, brief upstream slowness, momentary empty-array responses) — exactly the failure class a single 5-second retry fixes. Persistent failures (wrong key, exhausted quota) fail both attempts and still downshift correctly. Worst-case Phase 2a cost rises from 20s → 45s (initial 20s timeout + 5s sleep + 20s retry timeout), which is a rounding error against the 5-minute lock budget — and orders of magnitude cheaper than the 9-minute web search storm the retry prevents.

  Parse the JSON (array of `{symbol, date, epsEstimated, revenueEstimated, time}`). Build a `symbol → next_earning` map by sorting each symbol's entries ascending by `date` and taking the first row.

  For each thesis with `status: active | monitoring`, look up its ticker in the map:
  - **Hit**: record the date + EPS/revenue estimates + reporting time (BMO/AMC). Source label: `FMP`.
  - **Miss**: queue the ticker for the web search fallback (typically non-US listings — `000660.KS`, `6981.T`, `ASM.AS`, `BESI.AS`, `AIXA.DE`, `GAW.L`, `IQE.L`, `SIVE.ST`, `YAL.AX` — which FMP's universe calendar doesn't always cover; per-ticker coverage works via the transcript endpoint but the calendar endpoint is US-biased).

  **FMP call failure handling** (after retry):
  - Both attempts fail (HTTP error, curl error, or empty array) → `FMP_OK=0` set by the retry block above. Phase 2b enters capped-fallback mode. Do NOT retry a third time — by this point the failure is persistent (API key wrong, quota exhausted, or sustained upstream outage), and further retries cost time without changing outcome.

  ### 2b. web search fallback (CAPPED — hard limit 20 per run)

  📍 **Emit before**: `📍 Phase 2b: web search fallback for <queue_size> tickers (cap=20, mode=<healthy-int'l | overflow | full-fallback>)`
  ⚠️ **Emit when cap activates**: `⚠️ Phase 2b: queue (<queue_size>) exceeds cap — running top 20 by conviction+recency, surfacing <queue_size-20> dropped tickers in Notes block`
  ✅ **Emit after**: `✅ Phase 2b: <N> web searches complete, <hits> dates extracted`

  For the queued (uncovered) ticker set — or for the full thesis list if `FMP_OK=0` — send web search invocations in parallel: up to 25 invocations per message, then the next batch, never serialized.

  Query pattern: `"[Company name] next earnings date 2026"`.

  **Hard cap: 20 web searches per run, prioritized by conviction.** Empirically (2026-05-23 incident) an uncapped 64-ticker fallback storm took >9 minutes and exceeded the host kill budget, leaving Phase 4 unreached and a stale `.vault-lock` orphaned at vault root. The cap bounds worst-case Phase 2b runtime at ~3 minutes (20 calls × ~10s each, internally rate-limited by the web search backend) so total `$catalyst` runtime stays under the 5-minute lock budget even in full-fallback mode.

  **Prioritization (when queue size > 20)**:
  1. Sort by `conviction` (high → medium → low → unset)
  2. Within conviction tier, sort by frontmatter `date` descending (most recent thesis first — these are most likely to drive near-term decisions)
  3. Take the top 20
  4. Surface the dropped tickers in Phase 4's `Notes` block under the calendar: `⚠️ Earnings dates for [N] tickers not refreshed this run (FMP fallback cap): [ticker list]. Re-run $catalyst when FMP is healthy.`

  **Run modes by queue size**:
  - **Healthy FMP path** (`FMP_OK=1`, queue ≤ 20): run all web searches (typically 5–9 international tickers). No cap activation; no warning.
  - **Healthy FMP path with overflow** (`FMP_OK=1`, queue > 20): rare — would only happen if FMP universe call returns partial data missing many US listings. Cap activates, surface warning.
  - **Full fallback** (`FMP_OK=0`, queue = all 64 active/monitoring): cap activates. Run top 20 by conviction + recency. Calendar carries `⚠️ FMP unavailable — calendar reflects 20/64 active+monitoring tickers; remainder pulled from existing thesis Catalysts sections only. Re-run when FMP is healthy.` at the top of the file.

  ### 2c. Record source per ticker

  In the in-memory earnings map, tag every entry with its source (`FMP` or `web search`). Phase 4's `_catalyst.md` `Notes` column surfaces this — `FMP` entries get a `confirmed via FMP` tag, `web search` entries get `est. via news search`. Lets the user weight the calendar's confidence at a glance.

  ### 2d. Clean up

  ```bash
  rm -f /tmp/catalyst_earnings.json
  ```

## Phase 3: Analyse Catalyst Clusters

📍 **Emit before**: `📍 Phase 3: clustering catalysts (concentration, gaps, asymmetric, cross-thesis)`
✅ **Emit after**: `✅ Phase 3: <N> clusters identified, <M> no-catalyst theses, <K> cross-thesis events (3+ tickers)`

- **Concentration risk**: Are there weeks where multiple catalysts cluster? This creates portfolio-level volatility
- **Catalyst gaps**: Which theses have NO near-term catalyst? Flag as thesis drift risk — a position with no catalyst is dead capital
- **Asymmetric events**: Which catalysts have the widest range of possible outcomes? These are the highest-attention-priority events
- **Cross-thesis catalysts**: Events that simultaneously affect 3+ positions (e.g., a macro data release, a major customer's earnings)

## Phase 4: Output

📍 **Emit before**: `📍 Phase 4: writing _catalyst.md (6 tables + Notes block)`
✅ **Emit after**: `✅ Phase 4: _catalyst.md written (<word_count> words, <total_events> events across <unique_tickers> tickers)`

> **Snapshot already taken in Phase 0.2** with the mandatory hard-abort guard (§1.3 invariant). Do NOT re-snapshot here — a second `cp` without the hard-abort/non-empty check would silently overwrite Phase 0.2's protective snapshot under filesystem pressure, destroying the recovery path. The Phase 0.2 snapshot covers the pre-regenerate state for the entire run.

Save/update the catalyst calendar at `_catalyst.md` (overwrite each run — this is a regenerated utility file like `_hot.md`, not a research note):
```yaml
---
date: YYYY-MM-DD
tags: [meta, catalyst-calendar]
---
```

### Structure:
**Next 2 Weeks** (day-by-day detail)
| Date | Ticker(s) | Event | Expected Impact | Magnitude | Thesis test | Notes |
|------|-----------|-------|-----------------|-----------|-------------|-------|

**Weeks 3-4**
| Week of | Ticker(s) | Event | Expected Impact | Thesis test | Notes |
|---------|-----------|-------|-----------------|-------------|-------|

**`Thesis test` column (falsification layer — READING PROTOCOL).** Format: `[observable + threshold] → [confirms Insight #n | fires "→ LOW/HIGH/CLOSE if …" trigger of [[TICKER]] | untested-unmatched | untested-no-trigger]`. Populate from the Phase 1.2 Conviction-Triggers extraction — the thesis is already fully loaded, zero extra reads. This converts the calendar from a when-and-which-way schedule into a pre-registered hypothesis-test schedule: for each event, what outcome would CONFIRM or REFUTE which thesis.

**Split the null case — the two "untested" values mean different things and imply different fixes:**
- `untested-unmatched` — the thesis HAS `## Conviction Triggers` but none matches this event. Signal: the trigger set doesn't cover this event's risk → suggest a `$deepen TICKER "Conviction Triggers"` to add one. Actionable gap.
- `untested-no-trigger` — the thesis has NO `## Conviction Triggers` section at all. Signal: nothing defined can falsify the thesis → the event is unmoored from any pre-registered test. This is the stronger `$prune` + `$lint #60` signal; suggest creating triggers first.

A portfolio heavy in `untested-no-trigger` means the theses lack falsification machinery entirely; a portfolio heavy in `untested-unmatched` means the machinery exists but has coverage holes. Do not collapse them into one bucket — the distinction is the whole point.

**Earnings-within-14-days → `$transcript` prompt.** For any earnings event in the Next 2 Weeks table (Phase 2 enrichment supplied the date), tag its Notes cell `→ run $transcript TICKER once reported`. `$transcript` extracts management-language deltas + Q&A tone + trigger touches — the vault's highest-signal, most-underused earnings input (it has run once, ever). The catalyst calendar is the natural place to surface that a transcript will be pullable within days, so the earnings event actually gets ingested instead of passing unremarked. Collect these into the Phase 6.2 report as a `Transcript-ready this fortnight:` line.

**Month 2-3** (grouped by week)
| Approximate Date | Ticker(s) | Event | Notes |
|-----------------|-----------|-------|-------|

**No Catalyst Identified**
| Ticker | Last Catalyst Date | Days Since | Falsifiable? | Status |
|--------|-------------------|------------|--------------|--------|
[Theses with no upcoming catalyst — flag for attention. `Falsifiable?` = does the thesis have a `## Conviction Triggers` section (yes/no)? A thesis with NO catalyst AND NO triggers is doubly dead capital — nothing scheduled can move it and nothing defined can kill it: the strongest $prune candidate signal this calendar produces.]

**Stale Catalysts** (events that appear to have passed)
| Ticker | Event | Listed Date | Action Needed |
|--------|-------|-------------|---------------|
[Catalysts whose dates have passed — thesis needs updating]

**Cross-Thesis Events**
[Events affecting 3+ theses, with impact assessment for each]

## Phase 5: Update `_hot.md`

📍 **Emit before**: `📍 Phase 5: updating _hot.md (Active Research Thread + Open Questions for <K> no-catalyst tickers)`
✅ **Emit after**: `✅ Phase 5: _hot.md updated (<word_count> words, <new_open_qs> new Open Questions added)`
⚠️ **Emit if word cap pruning triggers**: `⚠️ Phase 5: _hot.md over soft cap (8,000w) — pruning <section> oldest entries until under cap`
❌ **Emit if hard cap hit**: `❌ Phase 5: _hot.md over hard cap (10,000w) after pruning — aborting _hot.md update per contract`

Read `_hot.md` then edit (do NOT touch Latest Sync or Sync Archive — those are `$sync`-owned). If `_hot.md` does not exist, create it per the AGENTS.md Rule #9 schema.

1. **Active Research Thread**: **Same-topic continuation** — if the current thread already covers catalyst-calendar work, append a dated line (`YYYY-MM-DD: refreshed catalyst calendar — [key takeaway, e.g. "2 dense weeks ahead, 3 theses with no catalyst"]`). **New topic**: compress the outgoing thread into a single `*Previous:*` entry (date + one-phrase summary). Write the new thread focused on catalyst state: `YYYY-MM-DD: refreshed catalyst calendar — next 2 weeks = [N] catalysts across [M] theses; [K] no-catalyst theses flagged for review.` Append `*Previous:*` line(s) — max 5, drop oldest.

2. **Open Questions**: For every ticker flagged under "No Catalyst Identified" in the catalyst calendar output, add a question (if not already present): `- [[TICKER]]: what catalyst in next 90 days could reignite this thesis? (flagged by $catalyst YYYY-MM-DD)`. **Dedupe by question pattern, not by ticker presence** — only suppress this entry if an existing Open Question already contains BOTH the ticker wikilink AND the substring `catalyst in next 90 days could reignite this thesis`. Other pre-existing questions about the ticker (e.g., from `$thesis`, `$stress-test`, `$surface`) must not suppress the catalyst-specific question; a thesis can legitimately have multiple open questions at once, and over-broad dedup would silently drop the catalyst gap from the user's attention surface.

3. **Recent Conviction Changes**: not touched by `$catalyst`.

4. **Portfolio Snapshot**: not touched by `$catalyst`.

**Word cap**: After edits, check total word count. If over 4,000 words (soft cap per `.agents/skills/_shared/hot-md-contract.md`), prune `## Sync Archive` entries (oldest first), then `*Previous:*` lines in Active Research Thread (oldest first), until under cap. If over 5,000 (hard cap), abort `_hot.md` update per contract.

## Phase 6: Report + lock release

📍 **Emit at Phase 6 start**: `📍 Phase 6: releasing lock and composing final report`
✅ **Emit after lock release**: `✅ Phase 6: lock released cleanly (token <token>)` — or `⚠️ Phase 6: lock token mismatch — leaving lock in place` if §6.1 found a mismatch.

**Runs in the main conversation** (no fork) — the Phase 6 report renders directly in chat. The ~71 full thesis + macro reads (~400K tokens at current vault scale) consume main-session context, so run `$catalyst` in a fresh conversation when context budget matters; `_catalyst.md` persists to disk as the authoritative calendar for later reading.

### 6.1 Lock release (MUST run before the report, even if Phases 1–5 had non-fatal errors)

Issue the lock-release shell block FIRST in Phase 6 — before composing the report. The trap-on-INT/TERM cleanup from Phase 0.1 only fires on signal-based termination; if the run is killed via SIGKILL (host timeout enforcement) or exits cleanly, the trap never runs. Explicit release here is the primary cleanup path; trap is the fallback.

```bash
# Verify token ownership before deletion (Procedure 1.5 — never delete a lock you don't own)
LOCK_FILE=".vault-lock"
EXPECTED_TOKEN="<token captured from Phase 0.1>"
if [ -f "$LOCK_FILE" ]; then
  ACTUAL_TOKEN=$(grep '^token:' "$LOCK_FILE" | sed 's/token: //')
  if [ "$ACTUAL_TOKEN" = "$EXPECTED_TOKEN" ]; then
    rm -f "$LOCK_FILE"
    echo "✅ Released vault-wide lock (token $EXPECTED_TOKEN)"
  else
    echo "⚠️ Lock token mismatch (expected $EXPECTED_TOKEN, found $ACTUAL_TOKEN). NOT releasing — another skill owns this lock now (likely because timeout_at passed and another skill broke in). Leaving in place."
  fi
else
  echo "ℹ️ Lock file already removed (trap may have fired, or skill ran past timeout_at and was reaped)."
fi
```

**Why this matters**: empirically (2026-05-23 incident) when the `$catalyst` subagent was killed at 9 min by host timeout, the trap-on-INT/TERM cleanup did not fire and `.vault-lock` was left orphaned at vault root for ~10 minutes until manually removed. While the orphaned lock's `timeout_at` had already passed (so other skills would treat it as stale via §1.3a's expiry check), it remained as clutter and a source of operator confusion. Explicit release closes the gap between "skill ran successfully" and "lock is gone".

### 6.2 Report

Report to user: next 2 weeks of catalysts, any dangerous clusters, and the list of theses with no catalyst (these need attention or pruning). Include one line summarizing the `_hot.md` update: `_hot.md: Active Research Thread refreshed; [K] no-catalyst tickers added to Open Questions.` Point the user to `[[_catalyst.md]]` for the full calendar tables (Next 2 Weeks, Weeks 3-4, Month 2-3, No Catalyst Identified, Stale Catalysts, Cross-Thesis Events).

Add a `Transcript-ready this fortnight: [TICKER (date), …] — run $transcript after each reports` line whenever any earnings event lands in the next 14 days (from the Phase 4 tagging). Omit the line entirely when none do — no noise on quiet fortnights.

If Phase 2b's web search cap activated, surface the degraded-mode warning in the report header: `⚠️ FMP unavailable this run — calendar reflects top-20-by-conviction web search results; [N] tickers carry pre-existing thesis Catalysts data only. Re-run $catalyst when FMP is healthy for full refresh.`
