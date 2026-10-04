---
name: brief
description: Generate a concise 1-page investment brief from a thesis — the elevator pitch version. Use when user says "brief", "summarise thesis", "pitch me [TICKER]", "one-pager", or "investment memo".
model: opus
effort: max
allowed-tools: Read Grep Glob Edit Write Bash(date *)
---

**Follow CLAUDE.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Distil a thesis into a sharp, 1-page investment brief. This forces clarity — if the case can't be made compellingly in one page, the thesis needs work.

## Arguments
$ARGUMENTS should be a ticker (e.g., "NVDA") or thesis name. If empty, ask the user.

**Batch mode (2026-07-08):** multiple tickers (`/brief NVDA AMD AVGO`) or a sector (`/brief [sector]` → every active thesis in that sector, resolved via `_graph.md` Sector reverse index) generates one brief per ticker in a single run — for pre-IC prep. Batch mode reads `_graph.md` ONCE up front (shared across all briefs — Phase 1.5's cluster-peer footnote data is a single read, not re-fetched per ticker) and runs each ticker through Phases 1–4. Emit each brief as its own clearly-delimited section; do not merge them. Per-ticker failures (missing thesis, rename marker) are reported and skipped, not fatal to the batch.

## Step 0: Pre-flight (MANDATORY)

### 0.1: Acquire vault lock
Acquire a `ticker:TICKER` scope lock per `.claude/skills/_shared/preflight.md` Procedure 1. Timeout budget: 3 minutes. Capture the token, verify ownership (Procedure 1.5) at every subsequent Bash block, release in the final reporting Bash block. **Batch mode**: acquire N `ticker:TICKER` locks (one per brief target, same partial-acquisition-rollback discipline as `/compare` §1.2 — release any acquired locks in reverse order if one fails); brief is read-only on theses so a `read-only` vault lock is an acceptable lighter alternative for a large batch.

### 0.2: Rename-marker pre-flight
Run `.claude/skills/_shared/preflight.md` Procedure 2. If `.rename_incomplete.TICKER` exists, hard-block per contract 2.3 — the brief's title line derives from the thesis's current filename, and any residual inbound references to the pre-rename name would not agree with the brief's title, producing inconsistent references. **Batch mode**: check the marker per target ticker; a blocked ticker is skipped-with-report, the rest of the batch proceeds.

Both checks must pass before proceeding to Phase 1.

## Phase 1: Load
1. **Duplicate check**: Grep `Research/` for existing briefs for this ticker (`source_type: brief` + matching ticker). If found, warn: `⚠️ Existing brief found: [[Research/existing-brief]]. Regenerating will create a new version. The old brief will remain in the vault.` Proceed — but note the old brief in the output so the user can delete it if desired. Additionally, surface source-thesis staleness on the same warning surface: if the thesis's last `## Log` entry date is >45 days old, warn `⚠️ source thesis last updated [N]d ago — brief may reflect stale analysis`.
2. Read the thesis note from Theses/
3. Read the 2-3 most recent or most important linked research notes (prioritise by recency and by being referenced in Log entries)
4. Read the relevant Sector Note for competitive context
5. Check Key Metrics for data freshness

### Exclusion contract — what the brief MUST NOT surface

Briefs are IC-facing pitch output. The following content categories are **working state or audit trail** and must never appear in the brief body or inform its claims beyond passive awareness:

- **All inline callouts** — `> [!question]`, `> [!error]`, `> [!tip]`, `> [!todo]` blocks in any state (fresh, addressed, pinned, preserved). Treat as invisible during Phase 2 compression.
- **`## Legacy Callouts` section entirely** — the plain-bullet archive of swept addressed callouts. Historical audit trail; no pitch relevance.
- **Provisional `Deepening` / `↳ CORRECTION: Deepened` Log entries** — transient skill-state, not analytical content.

When reading the thesis in Phase 1, mentally skip these regions. When the user asks "why isn't X in the brief" and X lives in a callout or Legacy Callouts — the answer is this exclusion contract: address the callout into the body text first, then regenerate the brief.

## Phase 1.5: Graph-primer cluster-peer context

Per `.claude/skills/_shared/graph-primer.md` Mode A.

Read `_graph.md` once. Fire the Read in parallel with Phase 1 thesis + research Reads (same tool-call batch).

For target TICKER:
- `entry = adjacency_index[TICKER]`
- `cluster` = first cluster in clusters where TICKER ∈ cluster.members (or null)
- `cluster_peers = cluster.members - {TICKER}` (empty if no cluster)
- `top_sector_peers` = up to 2 theses from `sector_reverse[s]` for s ∈ entry.sectors, ranked by most-recent `log_tail` entry date (filters for actively-maintained peers)

Extract `log_tail` for each of `cluster_peers ∪ top_sector_peers` (up to ~5 peers total, dedup).

Compose primer output for Phase 4:

```
Related Developments (cross-ticker context — graph primer footnote):
  [peer TICKER] (cluster: [name] | sector: [name]): [most-recent log_tail entry]
  [peer TICKER] (sector: [name]): [most-recent log_tail entry]
```

This section appears ONLY as a footnote-style block appended to the brief body AFTER the core 6-section structure (Pitch / Why Now / Non-Consensus Edge / Key Numbers / What Kills It / Conviction & Sizing). It is optional context for the IC reader — the brief's primary synthesis in Phase 2 must stand on its own without it.

**Orientation not filter** (contract §Anti-patterns + §Confirmation-bias mitigations): cluster peer developments are contextual only. Do NOT use peer context to soften or strengthen the target's Pitch, What Kills It, or Conviction — those must reflect the target's own thesis evidence independent of primer influence.

**Missing-graph fallback**: per `.claude/skills/_shared/graph-primer.md` §Missing-graph fallback. Brief omits Related Developments section; rest of brief unchanged.

## Phase 2: Compress
Distil the thesis into exactly this structure. Every word must earn its place.

---

**[TICKER] — [Company Name]**
*[Sector] · [Status] · Conviction: [Level] · [Date]*

### The Pitch
2-3 sentences maximum. Lead with the non-consensus angle. Why does this opportunity exist? What is the market mispricing and why?

### Why Now
The timing argument in 2-3 bullets. What catalyst, inflection point, or transition makes this relevant today rather than 6 months ago or 6 months from now?

### The Non-Consensus Edge
The single strongest variant perception — one paragraph. This is the insight that, if correct, generates the alpha. State what consensus believes, why they're wrong, and what evidence supports the contrarian view. Cite specific data points. **Name the consensus**: state in one clause the contrasting consensus / sell-side framing the edge opposes (e.g. "Street models flat take-rate; this thesis backs +300bps on the ticketing monopoly") — this mirrors the thesis `## Key Non-consensus Insights` Consensus field. **Name the falsifier**: end with the one observable that would prove the edge wrong — pull it from the thesis's `## Conviction Triggers` (the `→ LOW if` / `→ CLOSE if` condition that kills this edge). An edge with no stated falsifier is generic variant-perception prose; tying the pitch to its own kill criterion is what makes it an IC-grade claim rather than a story.

### Key Numbers
| Metric | Value |
|--------|-------|
| Market Cap | |
| EV/Revenue | |
| Revenue Growth | |
| Gross Margin | |
| FCF Yield | |

Attach below the table a data-as-of line — `Numbers as of YYYY-MM-DD` sourced from the source thesis's `key_metrics_last_refreshed` frontmatter. If the field is absent, render `as-of unknown — run /numbers`. Never present undated figures as current.

### What Kills It
The single biggest risk in 2-3 sentences. Not a laundry list — the ONE thing that, if it happens, invalidates the thesis. Be honest about probability.

### Conviction & Sizing
One line: conviction level, the quality of evidence supporting it, and what would change it (up or down).

---

## Phase 3: Quality Check
Before saving, verify:
- Does the Non-Consensus Edge name the specific consensus / sell-side framing it departs from, not merely assert it is non-consensus? A pitch that can't name the consensus it opposes is a restatement — flag it.
- Does "Why Now" contain a specific catalyst with a date, or is it vague?
- Is "What Kills It" a real risk or a softballed disclaimer?
- Are the Key Numbers current (check data age from thesis)?
- Could someone who has never read the full thesis understand the case from this brief alone?

If any check fails, strengthen that section before saving.

## Phase 4: Output

Save to `Research/YYYY-MM-DD - [TICKER] - Investment Brief.md` with:
```yaml
---
date: YYYY-MM-DD
tags: [research, brief, TICKER]
sector: [from thesis]
ticker: TICKER
source: vault synthesis
source_type: brief
propagated_to: []
---
```

> **Why `propagated_to: []`**: Briefs are derivative read-only summaries — they distill an existing thesis, not contribute new analytical evidence. Even though the brief's `ticker:` frontmatter would resolve to the thesis via `/sync`'s file-direct fallback, propagating a Log entry to that thesis would be circular ("brief written summarizing the thesis" — no new insight). The empty list is a **terminal dedup signal** to `/sync` Check 2 — the producer skill (this `/brief` run) explicitly declares "no propagation needed." See `/sync` Step 1 Check 2 for the empty-list semantics.

Do NOT modify the original thesis note (the brief is a derivative product, not a replacement).

> **Graph update deferred (accuracy note per User Guide §13)**: `/brief` creates a Research note but does NOT advance thesis mtimes or write `.graph_invalidations`. `/graph last` will NOT pick up this brief — it only processes theses changed since the last graph watermark. The new brief appears in `/graph`'s Orphan Research list only on the next **full `/graph` rebuild**, or once a thesis Edit wikilinks to it. For a brief-heavy chain where an up-to-date orphan list matters, run `/graph` (full).

Update `_hot.md` per `.claude/skills/_shared/hot-md-contract.md` (read first, then edit — do NOT touch Latest Sync or Sync Archive, owned by `/sync`):

1. **Active Research Thread**: **Same-ticker continuation** — if the current thread already covers the same primary ticker/topic, append a dated line (`YYYY-MM-DD: [update]`) to the existing thread instead of compressing. **New topic**: compress the outgoing thread into a single `*Previous:*` entry (date + one-phrase summary). Write: generated [TICKER] investment brief, and any notable gap or weakness the Phase 3 quality check identified. Append `*Previous:*` line(s) — max 5, drop oldest.
2. **Open Questions**: If the Phase 3 quality check identified weaknesses (vague catalyst, stale metrics, softballed risk), add as open questions for the ticker

**Word cap**: After all `_hot.md` edits, check total word count. If over 8,000 words (soft cap per `_shared/hot-md-contract.md`), prune `## Sync Archive` entries (oldest first), then `*Previous:*` lines in Active Research Thread (oldest first), until under cap. If over 10,000 (hard cap), abort `_hot.md` update per contract.

Present the brief directly to the user in the response — it should be immediately readable.
