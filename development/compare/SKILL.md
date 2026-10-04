---
name: compare
description: Side-by-side competitive comparison of two or more companies. Use when user says "compare", "X vs Y", "which is better", or asks about competitive dynamics between specific companies.
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$compare`, or infer them from the user's request when this skill is invoked implicitly.

Build a rigorous side-by-side comparison focused on competitive dynamics and investment merit.

Design rationale in `.agents/skills/compare/references/rationale.md` (§N.M anchors).

## Arguments

`SKILL_ARGS` = 2+ tickers or company names (e.g., "BESI vs AMAT", "PANW NET CRWD"). Only one ticker provided → identify closest competitors from Sector Note, ask user to confirm before proceeding. **Any competitor added by this expansion that has a thesis and will receive a Phase 5 Log append MUST be locked + rename-checked (Step 0.-1.3) before Phase 5 — the initial acquisition only covered the supplied ticker.**

## Phase 0.-1: Pre-flight

### 0.-1.1: Acquire per-ticker locks (C4 — §1)

Parse tickers from `SKILL_ARGS`. Acquire one lock per ticker (`.vault-lock.A`, `.vault-lock.B`, `.vault-lock.C`) per `.agents/skills/_shared/preflight.md` Procedure 1.3c — **per-ticker individual locks, NOT a joint `+`-delimited lock** (§1.1 — breaks on hyphen-containing tickers like `BRK-B`).

Timeout 10 min. Verify ownership every subsequent shell block via token match (Procedure 1.5). Release all N locks in final reporting block.

**Rollback-on-partial-acquisition** (§1.2): if any per-ticker lock is held by another skill, release all previously-acquired locks in this run and abort. Prevents holding a proper subset while concurrent skill holds the rest.

### 0.-1.2: Rename-marker pre-flight for EACH ticker

For each ticker in `SKILL_ARGS`, run Procedure 2. ANY `.rename_incomplete.TICKER_N` → hard-block per contract 2.3. Split-name state on any one ticker would corrupt the cross-thesis comparison research note's wikilinks.

### 0.-1.3: Lock + rename-check competitors added by single-ticker expansion

If `SKILL_ARGS` was a single ticker (§Arguments) and the user confirmed a competitor set from the Sector Note, the initial 0.-1.1/0.-1.2 covered ONLY the supplied ticker. Before Phase 5, for every confirmed competitor **that has a thesis** (web-only competitors get no vault writes, so no lock): acquire its `.vault-lock.TICKER` (Procedure 1.3c, appended to the run's lock set — same token) and run Procedure 2. Partial-acquisition rollback (§0.-1.1) applies to the expanded set. Skipping this lets Phase 5.2 append to a thesis Log with no lock held and no rename-marker guard.

## Phase 0: Thesis Existence Check

Verify which tickers have existing thesis notes in `Theses/`.

**All tickers have theses** → proceed to Phase 1 (full comparison mode).

**Some tickers lack theses** → report and offer options (§2.2):
```
⚠️ No thesis found for [TICKER(S)]. Options:
  (a) Proceed — use web research for [TICKER(S)] (lighter comparison, no vault updates for missing tickers)
  (b) Stop — run $thesis [TICKER] first for a full-depth comparison
```
Wait for user selection.
- **(a) Web-supplemented mode**: proceed. Missing tickers use web research in Phase 1. Phase 5 vault updates apply ONLY to tickers with existing theses. Report appends: `💡 Consider $thesis [TICKER] to formalize coverage.`
- **(b) Stop**: report missing tickers, stop.

**No tickers have theses** → stop (§2.1). At least one thesis is required as analytical anchor.

## Phase 1: Gather Context

**Two-round parallel-batch pattern.** For N tickers the research-note wikilinks can only be enumerated after the thesis is read, so the thesis reads fire first (Round 1), then all downstream reads fire in one parallel batch (Round 2).

### Round 1 — parallel batch (single message)
Issue ALL of these in ONE message:
- **Read** each thesis note — one Read per ticker with a thesis. Do NOT loop serially; send all N Reads in one tool-call batch.
- **Grep** once across `Research/ Macro & Technology/` for any of the tickers with `glob='*.md'` (use an alternation pattern `TICKER1|TICKER2|TICKER3`, scoped to markdown). One multi-ticker Grep replaces N per-ticker Greps.

Wait for Round 1 to land. Enumerate, per ticker: Related Research wikilinks, sector note paths (from `sector:` frontmatter), referenced Macro notes.

**Mental Models reading gate (MANDATORY — AGENTS.md; `.agents/skills/_shared/mental-models-section.md`).** Include in the Round 2 batch: `[[Mental Models/Generalist - Overview]]` (always) + the `[[Mental Models/Industry - X]]` for the compared tickers' sector(s) + any `[[Mental Models/Lens - X]]` in play (Value Layer Monopoly is especially load-bearing for competitive comparison — which player owns the layer everything else must traverse). Apply the READING PROTOCOL: the comparison verdict is a hypothesis; run the base-rate adversarially; where the models rank the same winner the bull consensus already sees, hunt the datapoint that would flip it. Read each ticker's own `## Mental Models` section to compare their recorded triggers head-to-head.

### Round 2 — parallel batch (single message, may be large)
Issue ALL of these in ONE message:
- **Read** every research note linked from every thesis (union across N tickers — deduped).
- **Read** every distinct Sector Note (N tickers may share sectors — read each sector note once).
- **Read** any Macro notes referenced by any of the theses.
- **Read** `[[Mental Models/Generalist - Overview]]` + the in-scope Industry/Lens files (reading gate above).

**Scaling note**: `$compare A vs B` issues ~10-20 Reads in Round 2. `$compare A vs B vs C` issues ~15-30. All land in one round-trip. Do not serialize per-ticker.

**Web-supplemented tickers** (Phase 0 option a): skip Rounds 1-2 for that ticker. Issue web search for business model overview, latest financials (revenue, margins, growth), competitive position, key products **in parallel with Round 2's vault reads** (different tool surfaces — web search and Read parallelize freely). Search vault (`Research/`, `Sectors/`, `Macro & Technology/`) for existing mentions. Flag sections without vault-depth data with `[web only]`.

## Phase 1.5: Graph-primer shared adjacency

Per `.agents/skills/_shared/graph-primer.md` Mode B.

Read `_graph.md` once. Fire the Read in parallel with Round 2 reads above (same tool-call batch — different tool surface from the thesis/sector/research Reads, parallelizes freely). Parse `adjacency_index` and `clusters`.

For targets A, B (and C, D, … if 3+ tickers):
- `entry_a = adjacency_index[A]`, `entry_b = adjacency_index[B]`, …
- `shared_sectors = entry_a.sectors ∩ entry_b.sectors`
- `shared_macros = entry_a.macros ∩ entry_b.macros`
- `shared_research = entry_a.research ∩ entry_b.research`
- `cross_thesis_link = (B ∈ entry_a.cross-thesis, A ∈ entry_b.cross-thesis)` — surface as `both`, `A→B`, `B→A`, or `none`
- `cluster_co_member = ∃ c ∈ clusters where {A, B} ⊆ c.members`

**N>2 tickers**: compute pairwise for all pairs. Surface `common_sectors = intersection across all entries` and `common_macros = intersection across all entries` for the aggregate view; individual pairs retain their shared sets.

Inject as primer context for Phase 2 + Phase 3:

```
Shared adjacency baseline (graph primer):
  Shared sectors:       [list]
  Shared macros:        [list]
  Shared research:      [list]
  Cross-thesis link:    [both | A→B | B→A | none]
  Cluster co-membership: [cluster name or "none"]
```

Phase 2 framing: "Shared adjacency establishes the comparison baseline. Differences below are sharper against this baseline — a divergence despite shared sector is structurally more interesting than a divergence between unrelated names."

**Orientation not filter** (contract §Anti-patterns): cluster co-membership does NOT imply substitutability. Ticker-specific content reads from Phase 1 remain primary.

**Missing-graph fallback**: per `.agents/skills/_shared/graph-primer.md` §Missing-graph fallback. Phase 2 proceeds without shared-adjacency context; comparison quality matches pre-retrofit behavior.

## Phase 2: Structural Comparison

### Business Model Comparison

| Dimension | [TICKER A] | [TICKER B] | Edge |
|-----------|-----------|-----------|------|
| Core revenue model | | | |
| Gross margin structure | | | |
| Customer concentration | | | |
| Recurring vs one-time revenue | | | |
| Geographic mix | | | |
| Capital intensity | | | |
| R&D as % of revenue | | | |

### Competitive Position

| Factor | [TICKER A] | [TICKER B] | Edge |
|--------|-----------|-----------|------|
| Market share (current) | | | |
| Market share trend (direction) | | | |
| Pricing power trajectory | | | |
| Technology moat depth | | | |
| Switching costs | | | |
| Scale / network advantages | | | |
| Management quality / track record | | | |
| Insider alignment | | | |

### Financial Comparison

| Metric | [TICKER A] | [TICKER B] | Notes |
|--------|-----------|-----------|-------|
| Market Cap | | | |
| EV/Revenue | | | |
| Revenue Growth (latest) | | | |
| Revenue CAGR (3yr) | | | |
| Gross Margin | | | |
| Operating Margin | | | |
| FCF Yield | | | |
| Net Cash / Net Debt | | | |

Use data from vault Key Metrics tables, supplement with web where gaps exist.

**Metrics-freshness check.** Read each compared thesis's `key_metrics_last_refreshed` frontmatter. Annotate each ticker column with its as-of date (`[TICKER A] (as of YYYY-MM-DD)`). Flag when the tickers' metrics are not comparably fresh — any two differ by >45 days OR any is >90d old:
```
⚠️ comparing metrics of different vintages — [TICKER_A] as of [date] vs [TICKER_B] as of [date]; run $numbers to align before trusting the financial comparison
```
A side-by-side of stale-vs-fresh numbers silently misleads the verdict.

## Phase 3: Dynamic Analysis (§8 — where insight lives)

Go beyond static snapshots:

1. **Market share trajectory** — where is share shifting and why? Use vault research notes for evidence. Structural or cyclical?
2. **Pricing power divergence** — whose pricing power is strengthening vs weakening? What drives divergence (technology, regulation, lock-in, commoditisation)?
3. **Technology trajectory** — who is on the right side of the next platform shift? Who is investing in the right areas? Who risks disruption?
4. **Logical tension** — what does each company need to be true that the other's success disproves? (If BESI wins on hybrid bonding, does that mean AMAT's approach fails, or can both win?)
5. **Scenario divergence** — under what macro or industry scenario does the current underdog win? How likely per vault macro notes?
6. **Customer and supplier overlap** — do they share customers? Who has more pricing power in that relationship? Shared suppliers (correlated supply risk)?

## Phase 3.5: External-evidence check (parallel batch — MANDATORY-unless-waived when any compared ticker is high conviction)

The verdict turns on the decisive axis surfaced in Phase 3 (market-share trajectory, pricing-power divergence, the platform-shift call). An internal-only verdict draws that axis from the same vault notes that built both theses — recent analyst actions, PT changes, and third-party market-share reads are the external check the vault does not carry. **If any web search / web fetch/open calls are issued, batch them in parallel** — one message, up to 25 invocations, mirroring `$stress-test` Phase 2.5 and `$thesis` Step 3. Do NOT serialize independent external lookups.

**Conviction-gated requirement (2026-07-14):**
- **Any compared ticker is `conviction: high`** → this phase is **mandatory**. Issue at least one parallel batch on the comparison's decisive axis: recent analyst downgrades / PT changes on each name, competitive / market-share datapoints, and a fresh third-party take (≤90 days) on which name is winning. The Phase 4 verdict MUST cite ≥1 datapoint the vault did not author. Rationale: both theses were likely written by the same analyst applying the same mental models, so the verdict inherits that shared prior — the winner the vault already favours — unless an outside datapoint breaks the tie (READING PROTOCOL: agreement across models is a disconfirm trigger, not a confirmation). The user may waive ONLY with an explicit "vault-only" instruction.
- **All compared theses `conviction: medium | low` or `status: draft`** → external evidence is optional; skip freely when the vault already carries sufficient competitive evidence. Its absence must then be stated in the Phase 4 verdict (`external evidence: none — vault-only comparison`).

## Phase 4: Investment Verdict

- **Risk-adjusted asymmetry**: not "which is cheaper" but which offers better upside/downside skew given the evidence
- **Consensus tag**: tag the stated preference `[consensus]` or `[non-consensus]` — is the preferred name already the Street's pick (little edge; the market prices it) or a genuine variant view? When `[non-consensus]`, name the contrasting consensus in one clause (e.g., "Street prefers AMAT on scale; this backs BESI on hybrid-bonding share gain"). A `[consensus]` verdict adds no edge even when correct.
- **Portfolio role**: substitutes or complements? Can you own both, or one-or-the-other? Does owning both create hidden concentration?
- **Preference trigger**: specific, observable event that would flip preference. Make it falsifiable.
- **Conviction gap**: if one has a thesis and the other doesn't, should it? If both have theses, is the conviction spread justified by the evidence?

## Phase 5: Output

### 5.0: Write manifest skeleton (M2 — skeleton before destructive edits)

Generate `HHMMSS` once for the entire Phase 5 run. All downstream per-file writes (research note, sector snapshots, manifest) reuse it.

```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
```

Before any destructive mutation (5.1 research-note write, 5.2 Log appends, 5.5b sector edits), write a manifest skeleton at `_Archive/Snapshots/_compare-manifest (compare-YYYY-MM-DD-HHMMSS).md` with `status: in-progress` (§3 invariant: skeleton → populate → flip):

```yaml
---
type: compare-manifest
batch: compare-YYYY-MM-DD-HHMMSS
status: in-progress
date: YYYY-MM-DD
---

# Compare Batch Manifest

> **If `status: in-progress`**, `$compare` crashed between Phase 5.0 (skeleton)
> and Phase 5.5c (flip). Check the vault for partial state:
>   - Research note at `Research/YYYY-MM-DD - [tickers] - Competitive Comparison.md` may or may not exist.
>   - Thesis Logs may have partial appends (filter by today's date + comparison wikilink).
>   - Sector notes may have been edited (Phase 5.5b rolls back on failure, but crash mid-5.5b leaves partial edits).
> Recovery: `$rollback compare-YYYY-MM-DD-HHMMSS` → cascade through each affected sector snapshot in Phase 5.5a.
>
> **If `status: completed`**, Phase 5 finished with all sector writes succeeding atomically.
> **If `status: rolled-back`**, Phase 5.5b atomicity fired — sectors restored from 5.5a snapshots; research note and thesis Logs preserved.

## Tickers compared
- *(filled in Phase 5.5c flip)*

## Sector writes attempted
- *(filled in Phase 5.5c flip with per-sector outcomes)*

## Sector writes rolled back (if any)
- *(filled in Phase 5.5c flip — empty if status: completed)*

## Thesis Log appends
- *(filled in Phase 5.5c flip with per-ticker outcomes)*

## Research note
- *(filled in Phase 5.5c flip with path and propagated_to status)*
```

Skeleton write failure → hard abort Phase 5 before any destructive edit. Locks remain held until the final reporting block; report to user and release.

### 5.1: Write comparison research note (without `propagated_to:` — §3.1)

Save to `Research/YYYY-MM-DD - [TICKER A] vs [TICKER B] - Competitive Comparison.md`:
```yaml
---
date: YYYY-MM-DD
tags: [research, comparison, SECTOR, TICKER_A, TICKER_B]
sector: [shared sector]
source: vault synthesis
source_type: comparison
# propagated_to: omitted intentionally — set in Phase 5.4 only after every Log append succeeds
---
```

**Omitted at write time**: mirrors `$scenario` Phase 6.1 + 6.3 atomicity (§3). If any Phase 5.2 Log append fails, pre-writing `propagated_to:` would falsely claim every ticker received its Log entry → permanent audit gap.

### 5.2: Per-thesis Log append (track per-ticker outcomes)

**Vault updates** — ONLY for tickers with existing thesis notes. Skip web-supplemented tickers (§2.3).

For each thesis with existing note, attempt Log append (max 2 lines). Prefix `"Comparison "` (trailing space significant — registry §16 in `.agents/skills/_shared/log-prefixes.md`) marks this as skill-origin for `$sync` Step 2.5 and pairs with the sector-side idempotency markers in Phase 5.5 to prevent `$sync` Step 4 from silently overwriting the sector analytical edits this skill just applied:
```
### YYYY-MM-DD
- Comparison [[Research/YYYY-MM-DD - A vs B - Competitive Comparison]]: [key competitive insight] — conviction [unchanged/strengthened/weakened + reason]
```

**Track per-ticker outcomes**: `succeeded: [tickers]` and `failed: [tickers, reason]`. Failure = Log append Edit failed (file locked, missing `## Log`, malformed frontmatter). Do NOT abort loop on single failure.

### 5.3: Add to Related Research (independent of Log outcome — §3.3)

For each compared thesis with existing note, add comparison to `## Related Research` (if not already present):
```
- [[Research/YYYY-MM-DD - A vs B - Competitive Comparison]]
```

Wikilink registration, not propagation claim — runs regardless of 5.2 outcome.

### 5.4: Atomicity rule for `propagated_to:` (§3.2)

Update research note's `propagated_to:` **only after EVERY thesis-with-existing-note Log append has landed**.

- **All succeeded** (`failed:` empty): edit frontmatter to add `propagated_to: [TICKER1, TICKER2, ...]` (all tickers with existing theses). Insertion: immediately before closing `---`. `$sync` Case 2b skips as already-propagated.
- **One or more failed** (`failed:` non-empty): do NOT write `propagated_to:` at all. Next `$sync` detects each via file-direct fallback (research note `tags:` + body wikilinks list each ticker), per-thesis idempotency check re-attempts failed; succeeded targets skipped via per-thesis idempotency.

**Per-failure reporting**: list every failed ticker in Phase 6 report under `Per-thesis Log appends — failed: [TICKER1 (reason), TICKER2 (reason)]`.

### 5.5: Cross-sector atomic sector-note updates (6.5 — §4)

Cross-sector ALL-OR-NOTHING semantics. Any sector note's edit failure mid-transaction → roll back all preceding successful sector edits using per-sector snapshots.

**Resolve target sector set**: for each compared thesis with existing note, resolve sector via `.agents/skills/_shared/sector-resolution.md`. Dedup. Yields `target_sectors: [(thesis_list, sector_note_path, match_confidence), ...]`.

**Confidence handling per resolved sector** (§4.3):
- `match_confidence: none`: emit no-match warning. Remove sector from atomic transaction set. Comparison still completes for resolved sectors.
- `match_confidence: substring`: emit `log_message` AND pause for explicit user confirmation before modifying analytical text. Declined → remove from transaction set.
- `match_confidence: normalized | exact`: proceed silently (normalized logs in final report, no prompt).

### 5.5a: Pre-snapshot ALL target sectors FIRST (§4.2)

Before any sector note write, snapshot every target sector. Any snapshot fails → abort immediately (no destructive modifications yet).

**Issue all `cp` calls in ONE shell block using background shell jobs + `wait`** — for a 3+ sector span, this is one Bash round-trip instead of 3+ sequential Bash calls:

```bash
mkdir -p _Archive/Snapshots
HHMMSS=$(date +%H%M%S)
# For each (thesis_list, sector_note_path, _) in target_sectors, fire cp in background:
pids=()
cp "Sectors/Sector A.md" "_Archive/Snapshots/Sector A (pre-compare YYYY-MM-DD-$HHMMSS).md" & pids+=($!)
cp "Sectors/Sector B.md" "_Archive/Snapshots/Sector B (pre-compare YYYY-MM-DD-$HHMMSS).md" & pids+=($!)
cp "Sectors/Sector C.md" "_Archive/Snapshots/Sector C (pre-compare YYYY-MM-DD-$HHMMSS).md" & pids+=($!)
# Wait per-PID: bare `wait` returns 0 even if a background cp failed, so the
# "any snapshot fails → abort" rule (§4.2) could never detect the failure and
# 5.5b destructive edits would proceed with no rollback anchor.
snap_fail=0
for pid in "${pids[@]}"; do wait "$pid" || snap_fail=1; done
[ "$snap_fail" -ne 0 ] && { echo "❌ sector snapshot failed — aborting before any sector edit"; exit 1; }
```

Then issue all frontmatter-addition Edits as a single parallel tool-call batch (one Edit per snapshot, all in the same message).

Add frontmatter to each snapshot with per-sector batch ID (§5.1 — distinct per sector). The `-[sector-slug]` goes at the END so the manifest batch `compare-YYYY-MM-DD-HHMMSS` (§5.0) is a PREFIX of every sector snapshot batch — otherwise `$rollback compare-YYYY-MM-DD-HHMMSS` (2.5a prefix lookup) matches zero sector snapshots and the cascade silently restores nothing:
```yaml
snapshot_of: "[[Sectors/Sector Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: compare
snapshot_batch: compare-YYYY-MM-DD-HHMMSS-[sector-slug]
```

Store `snapshot_map: {sector_note_path → snapshot_path}` for potential rollback in 5.5b.

### 5.5b: Apply sector edits; on failure, roll back all prior successes (§4.2)

```
attempted_and_succeeded: []
attempted_and_failed: []

for sector_note_path, thesis_list, confidence in target_sectors:
    try:
        apply_sector_edit(sector_note_path, thesis_list, comparison_insight)
        attempted_and_succeeded.append(sector_note_path)
    except EditFailure as e:
        # Roll back ALL prior succeeded sector edits
        for prior_sector in attempted_and_succeeded:
            copy_from(snapshot_map[prior_sector], prior_sector)  # restore from snapshot
        
        attempted_and_failed.append((sector_note_path, str(e)))
        abort_transaction(
            reason=f"Sector note write failed: {sector_note_path} ({e}). "
                   f"Rolled back: {attempted_and_succeeded}. "
                   f"Research note and thesis Logs preserved. "
                   f"Re-run $compare after resolving the sector write issue.")
```

**`apply_sector_edit`**: targeted `Edit` operations on sector note. Covers FOUR edit surfaces in a fixed order — each atomic, single Edit failure triggers outer abort + rollback:

1. **Competitive dynamics** — revise relative-positioning prose where A vs B comparison changes the sector narrative.
2. **Value chain / comparison tables** — update tables that list A and B side-by-side.
3. **`## Related Research` — append research-note wikilink** (idempotency marker, §4.5 — pairs with `$sync` Step 4.0 sub-step 1):
   ```
   - [[Research/YYYY-MM-DD - A vs B - Competitive Comparison]]
   ```
   Skip if already present (idempotent on repair re-runs).
4. **`## Log` — append dated entry referencing the research note** (idempotency marker, §4.5 — pairs with `$sync` Step 4.0 sub-step 2):
   ```
   ### YYYY-MM-DD
   - Comparison [[Research/YYYY-MM-DD - A vs B - Competitive Comparison]]: [one-line sector-level takeaway — e.g., "competitive dynamics revised: A's moat widens vs B"]
   ```
   Same `Comparison ` prefix as thesis Log entries (registry §16). If sector note has no `## Log` section, graceful-skip this sub-step per `.agents/skills/_shared/preflight.md` Procedure 4 and log `ℹ️ Sector [name] has no ## Log — Related Research wikilink alone serves as idempotency marker.`

**Why sub-steps 3 and 4 are load-bearing** (§4.5 — C1 fix): without them, `$sync` Step 4.0 idempotency check fails to detect that `$compare` already propagated the research note to this sector. `$sync` Step 4a/4b then re-edits the same competitive-dynamics / value-chain sections from scratch, silently overwriting `$compare`'s nuanced analysis.

**How the two sub-steps combine with `$sync` Step 4.0**:
- **Sub-step 3** (`## Related Research` wikilink) satisfies Step 4.0 sub-step 1 — without a wikilink match there, Step 4.0 classifies as "first-time propagation" and proceeds straight to 4a/4b (full re-edit). Sub-step 3 is therefore the **minimum required** marker: it stops "first-time" misclassification.
- **Sub-step 4** (today-dated sector `## Log` entry) additionally satisfies Step 4.0 sub-step 2 — wikilink present alone only advances Step 4.0 to its Log-entry probe; it does NOT by itself fire the skip. With both markers present, Step 4.0 returns `skip 4a + 4b` cleanly.
- **Sector without `## Log`** (sub-step 4 graceful-skips): Step 4.0 sub-step 2 reads the absent Log, finds no today-dated entry, and falls through to its "proceed normally" branch (which then relies on Step 4b's deep-analysis to decide whether any real delta exists). This is strictly weaker than the two-marker case — Step 4b may still issue redundant edits, though its deep-analysis is designed to gate on genuine delta. Treat the sector-without-Log case as a known soft spot and ensure sub-step 3 at minimum lands.

**`abort_transaction` surfaces** (§4.4):
- Sectors successfully edited (now rolled back to pre-compare state): list
- Sector that failed: path + reason
- Research note status: preserved (5.1 already wrote it)
- Thesis Logs status: preserved (5.2 already wrote them)
- `propagated_to:` status: depends on 5.4 — set (if all 5.2 succeeded) or omitted (atomicity fired)

### 5.5c: Populate + flip compare manifest (M2 — skeleton → populate → flip)

Manifest skeleton was written at Phase 5.0 with `status: in-progress`. Phase 5.5c populates the body placeholders with actual outcomes from 5.1-5.5b and flips status.

**Populate body** (Edit the Phase 5.0 skeleton, replacing `*(filled in Phase 5.5c flip)*` placeholders):

```markdown
## Tickers compared
- TICKER_A, TICKER_B, TICKER_C

## Sector writes attempted
- Sectors/X.md — succeeded (snapshot: [[_Archive/Snapshots/X (pre-compare ...)]])
- Sectors/Y.md — succeeded (snapshot: [[_Archive/Snapshots/Y (pre-compare ...)]])

## Sector writes rolled back (if any)
- (none if status: completed)

## Thesis Log appends
- TICKER_A: succeeded
- TICKER_B: succeeded
- TICKER_C: failed (reason) — will be retried by next $sync via file-direct fallback

## Research note
- [[Research/YYYY-MM-DD - TICKER_A vs TICKER_B vs TICKER_C - Competitive Comparison]]
- propagated_to: set | omitted (atomicity — Log append failed for at least one ticker)
```

**Flip frontmatter**:
- All sector writes succeeded: `status: in-progress` → `status: completed`. Add `completed_date: YYYY-MM-DD`.
- Phase 5.5b rollback fired: `status: in-progress` → `status: rolled-back`. Add `completed_date: YYYY-MM-DD`.

**Verify flip landed** (targeted live-file verification): run a targeted frontmatter read against the live file after applying the patch. Do not rely only on the patch operation's success status. Confirm `status:` is no longer `in-progress` from the targeted verification output. On verification failure: report `⚠️ Compare manifest status flip failed — manifest remains status: in-progress despite completion. $lint #45 will flag this as Critical. Manual fix: edit manifest frontmatter to the correct terminal status.` This is the FINAL step — sector edits (5.5) already ran; proceed only to the `_hot.md` update and the Phase 6 report.

`status: rolled-back` indicates clean abort (Phase 5.5b rollback fired). `status: completed` indicates atomic success. `status: in-progress` surfaced as Critical by `$lint #45` (§6.2).

### Sector edits — targeted `Edit` operations

Modify original sector notes using targeted `Edit` (atomic string replacement per section), NOT full-file `Write`. Each `Edit` call succeeds atomically or leaves the section unchanged — blast radius of mid-edit failure is zero. Apply one `Edit` per modified section (e.g., one for competitive dynamics, one for value chain).

**Post-edit verification** (targeted live-file verification): run a targeted read of each edited sector section in the live file. Per edited section, verify from the targeted verification output:
- Ends with complete sentence (no mid-word, mid-sentence, unclosed formatting)
- No incomplete table rows (line starts `|` but doesn't end `|`)

Any fail: `⚠️ Sector note may contain a partial edit in [section]. Snapshot available: [[_Archive/Snapshots/...]]. Review manually or $rollback.`

### Graph update deferred

`_graph.md` owned exclusively by `$graph`. Run `$graph last` after this skill to register comparison research note and new cross-thesis connections.

### _hot.md update

Per `.agents/skills/_shared/hot-md-contract.md` (do NOT touch Latest Sync / Sync Archive):

1. **Active Research Thread**: same-ticker continuation per contract. Write: compared [TICKER A] vs [TICKER B], key competitive insight, logical next research step.
2. **Recent Conviction Changes**: add entry per ticker where conviction was strengthened or weakened.
3. **Open Questions**: add unresolved competitive questions comparison surfaced.

Word cap: after edits, over 8,000 (soft cap per `.agents/skills/_shared/hot-md-contract.md`) → prune `## Sync Archive` (oldest first) then `*Previous:*` lines. Abort if over 10,000 hard cap.

## Phase 6: Report

1. **Single most important competitive insight** and whether it changes conviction on either name — lead with the decisive-axis divergence and the Phase 4 verdict (`[consensus]`/`[non-consensus]`), not the research-note link.
2. **Comparison research note**: `[[Research/YYYY-MM-DD - A vs B - Competitive Comparison]]`
3. **Per-thesis Log appends** (5.2 outcome):
   - `Theses with existing notes propagated: [N] of [M]` (succeeded list)
   - `propagated_to: frontmatter` — `set ([TICKER1, TICKER2, ...])` (all succeeded) | `omitted (one or more appends failed — next $sync will retry)`
   - **Failed appends** (if any): `[TICKER1 (reason), TICKER2 (reason)]`
4. **Web-supplemented tickers** (if any from Phase 0 option a): `[TICKER1, TICKER2] — used web research, no vault updates. Consider $thesis [TICKER] to formalize coverage.`
5. **Sector notes updated**: per-sector list with snapshot path, or "no snapshot (link addition only)".
6. **Transaction state**: `completed` | `rolled-back: [sectors rolled back, reason]`
7. **Follow-up**: `→ Run $sync to propagate sector note changes and retry failed Log appends. Then $graph last.`
