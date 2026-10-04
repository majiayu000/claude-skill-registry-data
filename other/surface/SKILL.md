---
name: surface
description: Surface new insights, potential trades, and research opportunities from existing vault content. Use when user says "surface", "what am I missing", "find opportunities", or "what should I research next".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$surface`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Perform deep insight discovery across the vault. This is the highest-value operation — finding connections and opportunities the user hasn't seen yet.

## Execution context — Codex subagent delegation (MANDATORY)

The MAIN THREAD resolves scope first, then spawns ONE Codex subagent with the available delegation tool. Prefer the project `vault_worker` agent when selectable. Pass this skill's full instructions plus the resolved scope. The subagent performs Step 0 through Phase 4, including reads, analysis, lock handling, and the specified Research-note and `_hot.md` writes. Wait for completion and render its complete user-facing report **verbatim**.

**Mental Models gate:** Do not rely on inherited project context. Embed this text in the delegated prompt: *"Before ranking any opportunity, read `Mental Models/Generalist - Overview.md` (always) + the matching `Mental Models/Industry - X.md` for sectors in scope + any relevant `Mental Models/Lens - X.md`. Apply the READING PROTOCOL — models are lenses/questions held as hypotheses, never verdicts; run the base-rate/outside view adversarially; treat agreement across models as a trigger to disconfirm, not to commit."*

**Recursion guard:** Also embed: *"You are the EXECUTOR of this skill run, not a coordinator. Do not delegate any part of this work to another subagent. Perform all reads, analysis, and writes yourself, and end your final message with the complete user-facing report."*

Delegation keeps the large read set out of the main context. If delegation is unavailable, run inline. `all` mode still requires the user's explicit request and cost acceptance.

## Step 0: Pre-flight (MANDATORY — delegated run; scope already resolved)

### 0.1: Acquire vault lock
- **Unscoped `$surface`** (full vault): acquire a `vault-wide` scope lock per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout budget: 10 minutes.
- **Scoped `$surface TICKER`**: acquire a `ticker:TICKER` scope lock. Timeout budget: 5 minutes.
- **Scoped `$surface [sector]`**: acquire a `vault-wide` scope lock (the sector set spans multiple tickers; concurrent ticker-scoped writers would race on sector note edits). Timeout budget: 10 minutes.

Capture the token emitted at Step 0.1, verify ownership (Procedure 1.5) at every subsequent shell block, release in the final reporting shell block via `rm -f "$LOCK_FILE"`.

### 0.2: Rename-marker pre-flight (ticker-scoped mode only)
For `$surface TICKER`, run `.agents/skills/_shared/preflight.md` Procedure 2. If `.rename_incomplete.TICKER` exists, hard-block per contract 2.3. For unscoped and sector-scoped modes, check `.rename_incomplete.*` at vault root; if any marker exists, emit a warning but DO NOT abort (surface is read-mostly for these modes — it writes a research note but does not edit thesis wikilinks). Warning text: `⚠️ In-flight rename repair(s) detected: [list markers]. Surface scan will proceed but its research note's wikilinks to the affected ticker(s) use current filenames. Complete rename repair before running downstream $sync.`

## Scope Resolution

Parse `SKILL_ARGS` to determine scope:

- **`all`** (literal keyword): Full vault, **full-read mode** (comprehensive, legacy pre-2026-04-21 behavior). Reads every thesis, sector, and macro note in full. Use when doing a once-off deep review and willing to pay the larger context cost for maximum signal.
- **Ticker** (e.g., `NVDA`): Read `_graph.md` and resolve the ticker's adjacency set — its thesis, sector note(s), macro note(s), cross-thesis references, and all linked research. Also include theses that share a sector (one ring outward) for competitive context. **Adjacency-miss branch (thesis newer than the graph):** if the ticker has no adjacency entry in `_graph.md` BUT `Theses/TICKER - *.md` exists on disk (e.g. `$surface CBRS` when CBRS was created after the last `$graph` run), do NOT treat it as unknown — warn `ℹ️ [TICKER] not yet in _graph.md (created since last $graph run) — resolving from disk; run $graph last for full adjacency.` then resolve the scope set from the thesis file directly: its `sector:` frontmatter (→ sector note via the resolution procedure below) + its `## Related Research` wikilinks + Log-mentioned macro notes. This is the mirror of the existing archived-thesis validation (graph lists a file that's gone); here disk has a file the graph lacks.
- **Sector** (e.g., `semiconductors`): Resolve the argument to a sector note via `.agents/skills/_shared/sector-resolution.md` (the canonical procedure — case/whitespace/punctuation tolerant), NOT a raw case-sensitive `_graph.md` key lookup. Then use the `_graph.md` Sector → Theses reverse index (keyed on the RESOLVED sector-note name) to gather all theses in that sector, plus the sector note, related macro notes, and their linked research.
- **No arguments / empty**: Full vault, **section-targeted mode** (default). Reads bounded per-thesis sections only — fast, lean, suitable for weekly/monthly cadence.

Argument disambiguation: `all` is a reserved keyword (matches `$sync all` precedent). Never a ticker — no archived or live thesis with that filename pattern. Never a sector — no sector note named `all`. `all` is accepted in any case (`all`, `ALL`, `All`).

**Sector matching is case-INSENSITIVE via `.agents/skills/_shared/sector-resolution.md`.** The prior "case-sensitive for ticker/sector match" rule made the skill's OWN documented example `$surface semiconductors` (and User Guide's) resolve to zero matches, because the graph key is `Semiconductors & AI Infrastructure`, not `semiconductors`. Route every sector argument through the resolution procedure; the ticker match stays exact (tickers are canonical uppercase/numeric filenames).

**No-match behavior (both scoped modes).** If the argument resolves to neither a ticker (no `Theses/ARG - *.md` on disk AND no graph adjacency) NOR a sector (`sector-resolution.md` returns `match_confidence: none`), STOP with: `⚠️ $surface [ARG] — "[ARG]" matched no thesis (Theses/[ARG] - *.md) and no sector note (via sector-resolution). Check the ticker/sector name, or run $surface (no args) for a vault-wide scan. No research note written.` Do NOT silently fall back to a vault-wide scan (that would write a note the user didn't scope for).

If a non-`all` scope is requested but `_graph.md` does not exist, warn: `⚠️ Graph missing — cannot scope. Run $graph first, or run $surface (default, section-targeted) or $surface all (full-read) without arguments.` Then stop. (Exception: the adjacency-miss branch above still resolves a ticker from disk when the graph merely lacks that one new thesis — a missing graph FILE is different from a graph that is present but stale for one ticker.)

### Scope-set existence validation (ticker-scoped and sector-scoped modes only)

After resolving the scope set from `_graph.md` and before reading any thesis files, validate that every resolved thesis's file still exists on disk. `_graph.md`'s reverse indexes and adjacency entries reflect the last `$graph` run's filesystem state; closures via `$status active→closed` or `$prune` between that run and now mv files to `_Archive/` without touching `_graph.md`. Scoped `$surface` would otherwise resolve archived theses into the scope set and fail when reading them — producing silently incomplete analysis.

Validation rule:

1. Collect `resolved_theses: [Theses/TICKER - Name.md, ...]` from Scope Resolution output.
2. For each path, test existence:
   ```bash
   for path in resolved_theses:
       [ -f "$path" ] || record_as_missing "$path"
   ```
3. If `missing: [ ]` is empty → proceed to Phase 1 normally.

4. If `missing: [ ]` is non-empty:

   **Sector-scoped mode**: stop the skill immediately. Do NOT proceed with a partial scope — scoped portfolio-level output (research velocity ranking, attention allocation, decay alerts) depends on complete coverage; a partial scope silently under-reports these metrics without flagging the gap. Report:
   ```
   ⚠️ Scope resolution via _graph.md found [N] thesis(es) still listed in the Sector → Theses reverse index but no longer present in Theses/:
     - [missing path 1]
     - [missing path 2]
     ...

   _graph.md is stale relative to filesystem state — likely a $status active→closed or $prune closure since the last $graph run.

   Resolution: run $graph last (consumes .graph_invalidations, rebuilds reverse indexes from current filesystem state, excludes archived theses). Then re-run $surface [sector].

   No surface-scan research note was written for this run.
   ```

   **Ticker-scoped mode**: if the scoped ticker itself is in `missing:`, report:
   ```
   ⚠️ $surface [TICKER] — thesis file not found at Theses/[TICKER] - *.md. Likely archived since the last $graph run.

   Options:
     (a) Run $rollback [TICKER] to reopen the archived thesis (then $sync TICKER → $graph last → re-run $surface [TICKER]).
     (b) Run $surface without arguments for a vault-wide scan that will correctly exclude the archived ticker.
     (c) Run $graph last to rebuild indexes from current filesystem state, then re-run $surface [TICKER] — but expect the same error if the thesis is archived.

   No surface-scan research note was written for this run.
   ```
   Stop the skill in either ticker-scoped sub-case.

### Why stop rather than best-effort continue

Design rationale in `.agents/skills/surface/references/rationale.md` §1.

### Why not auto-run `$graph last`

Design rationale in `.agents/skills/surface/references/rationale.md` §2.

## Phase 1: Portfolio Scan (mode-dependent read strategy)

Read strategy branches by scope. The two full-vault modes trade completeness against main-session context budget:

| Mode | Thesis reads | Sector reads | Expected read budget | Use when |
|---|---|---|---|---|
| `$surface` (default) | Section-targeted (frontmatter + 4 sections + last 5 Log) | Section-targeted (4 sections + last 5 Log, all ~50) | ~150-200K words | Weekly / monthly cadence; part of a maintenance chain |
| `$surface all` | Full read (entire file per thesis) | Full read (all ~50) | ~960K words — **exceeds a single subagent context; run only on explicit `all` with the user accepting the cost** | Once-off deep review; maximum signal |
| `$surface TICKER` | Full read of scope set | Full read of the ticker's sector note(s) only | ~20-40K words | Ticker-focused insight discovery |
| `$surface [sector]` | Full read (≤6 theses) or section-targeted (>6 theses) | Full read of the one resolved sector note | ~20-80K words | Sector-level review |

### Unscoped default mode — section-targeted reads

1. For each thesis file in `Theses/*.md` (every file — draft, active, monitoring; not just active):
   - Read **only**: frontmatter + `## Summary` + `## Key Non-consensus Insights` + `## Risks` + `## Catalysts` + **last 5 Log entries**
   - Skip: Business Model & Product Description, Industry Context, Key Metrics, Bull Case, Bear Case, Outstanding Questions, Related Research, older Log entries
   - Target: ~800-1,500 words per thesis instead of ~4,000-6,000 — reduces total thesis read from ~175K words to ~35-50K words
   - Extract via the shared helper (2026-07-08 — replaces the prior brittle inline awk range-patterns, which silently mis-extracted on any heading drift that `$lint #14` flags; the script is heading-case/whitespace/prefix tolerant and reports missing sections):

```bash
python3 .agents/skills/_shared/scripts/extract_sections.py Theses/*.md \
  --sections "Summary,Key Non-consensus Insights,Risks,Catalysts" --log-tail 5
```

   One call handles every thesis; output is grouped per file (`===== FILE: ... =====`) with a `--- missing sections: ... ---` line whenever a thesis lacks a requested heading (surface that as a template-drift signal, don't silently drop it). Exit 3 = a file was unreadable (self-validation); investigate rather than proceeding on partial output.

2. **Sector Notes are section-targeted too, NOT read in full.** There are **~50 sector notes ≈ 445K words** (the old "~13 files, read in full" count was stale by ~4× and, read in full, alone exceeds the delegated subagent's entire context — the run would silently truncate on exactly the sections the edge lives in). Extract only the highest-signal sector sections via the same helper:

```bash
python3 .agents/skills/_shared/scripts/extract_sections.py Sectors/*.md \
  --sections "Key industry questions,Competitive dynamics,Investor heuristics,Mental Models" --log-tail 5
```

This cuts ~445K → ~110-130K words while keeping the non-consensus surface (Investor heuristics = what's priced in / where consensus is wrong; Competitive dynamics = pricing-power trajectory). Full-read a sector note ONLY if a specific opportunity thread requires its Product-level or Industry-history detail — targeted, not blanket.

3. **Issue steps 3-4 as a single parallel tool-call batch** (after the Step 1 + Step 2 extractor blocks land): all Macro Note Reads (~8-9, full) + all heavily-cited research note Reads (~10-20) in ONE message. Do NOT serialize.
4. Read all **Macro Notes** in full (bounded set, ~8-9 files). Scenario frameworks require complete context.
5. For heavily cited research notes (appearing in ≥3 theses' Related Research via `_graph.md` orphan+adjacency lookup): read in full. All other research notes: trust the thesis Log citations as summaries.

**Expected read budget**: ~150-200K words total (thesis-targeted ~35-50K + sector-targeted ~110-130K + macro ~15K + cited research). The prior "~50-80K" line assumed the stale 13-sector count; at 50 sectors even the targeted budget is larger, but it stays within a delegated subagent's context — a full-read of all 50 sectors (~445K words + ~127K thesis + macro > 600K words) would not. The `all` mode's true cost is ~960K words and MUST run full-read only when the user explicitly accepts it.

### `$surface all` mode — full-read comprehensive scan

Use when the user wants maximum analytical depth for a once-off deep review. Reads every thesis file in full — accepts the larger main-session context cost for richer cross-thesis connection detection (particularly valuable for Business Model and Industry Context cross-referencing that section-targeted mode misses).

**Issue ALL reads in steps 1-3 as a single parallel tool-call batch** — one message with every thesis Read (~76), every Sector Read (~50), and every Macro Read (~8-9) firing in parallel. Do NOT serialize. Step 4's heavily-cited research reads join the same parallel batch when `_graph.md` adjacency is already loaded; otherwise they land in a second parallel batch after the Step 1-3 batch returns.

1. Read every `Theses/*.md` in full (all 15 thesis sections). No extraction.
2. Read all Sector Notes in full (~50).
3. Read all Macro Notes in full (~8-9).
4. For heavily cited research notes (≥3 theses in `_graph.md` adjacency): read in full — include in the parallel batch with steps 1-3 (one round-trip). For others: read on-demand when Phase 2 analysis surfaces a specific question about them.

**Expected read budget**: ~960K words total (76 theses ~127K + 50 sectors ~445K + macro ~15K + cited research + growth since pre-R2) — this **exceeds a single delegated subagent's context window**. Run `all` mode only when the user explicitly requests it AND accepts that the subagent may need to chunk the read across multiple passes or that coverage of the lowest-signal sections may be partial; log any section dropped. Default section-targeted `$surface` (~150-200K subagent words) remains the lean routine-cadence choice and the safe default; reserve `all` for deliberate deep reviews where the user has accepted the cost.

**Output differentiation**: `$surface all` research notes carry `source_type: synthesis` with `scope: all` in a `scope:` frontmatter field, so downstream review can distinguish deep-scan outputs from routine `$surface` scans. Filename: `Research/YYYY-MM-DD - Insight Surface Scan (all).md`.

**When to prefer `$surface` over `$surface all`**: unless you're explicitly doing a quarterly/annual portfolio deep-review, default mode is strictly better — same insight signal at 25% the read cost. `$surface all` is the escape hatch for cases where section-targeting empirically misses a cross-section pattern.

### Scoped mode — reads bounded by scope resolution

**Ticker-scoped `$surface TICKER`**: read the resolved ticker + adjacencies (thesis, sector, macros, cross-thesis, linked research, sector peers). Set is small (1 focal thesis + 2-6 peers); section-targeting not needed — read all files in full for full competitive context.

**Sector-scoped `$surface [sector]`**: read the sector note + all theses in that sector + linked macros + their research. Typical set is 3-8 theses; apply section-targeting (as in default mode above) only if the sector has >6 theses.

Skip vault-wide checks that require full portfolio coverage (Attention Allocation ranking, Research Velocity ranking across all theses — these need the full set to be meaningful).

## Phase 2: Connection Analysis

**Portfolio Blind Spots**
- Identify sectors or sub-sectors the vault's theses imply are important but have NO coverage. (e.g., if you hold BESI + LITE + NVDA, you're implicitly betting on advanced packaging — do you cover the substrate suppliers? The test equipment vendors? The materials companies?)
- Flag value chain nodes that appear in multiple theses' Risk sections but have no dedicated research — these are unmonitored dependencies
- Check for "implied but unwritten" theses — tickers mentioned in 3+ research notes that still have no Thesis note. These are ideas the vault has been circling without committing to
- Identify adjacent companies that vault research strongly implies should be covered based on competitive dynamics in Sector Notes

**Supply Chain Mapping**
- Which thesis companies are suppliers, customers, or competitors of each other?
- Are there hidden portfolio correlations? (e.g., multiple bets on the same underlying trend)
- Would a single event break multiple theses simultaneously?

**Macro Exposure Audit**
- Map each thesis against current macro scenarios (Iran conflict, AI bubble risk, rate expectations)
- Flag theses with unacknowledged macro sensitivity
- Identify natural hedges within the portfolio

**Catalyst Calendar**
- What upcoming events could move multiple positions?
- Are there clustered earnings dates that create portfolio risk?
- Any regulatory, geopolitical, or technology milestones approaching?

**Contrarian Signal Detection** — *delegated to `$retro` (2026-07-08 de-overlap).*
- The vault-vs-market gap (where vault conviction diverges from market pricing) is `$retro`'s flagship: it computes the narrative-price delta rigorously against *actual* price moves + newsflow polarity, not an ad-hoc web guess. `$surface` no longer re-derives it (doing so duplicated ~per-ticker web queries with no shared query plan and produced a weaker, price-blind version of the same signal).
- `$surface`'s job here is only to **flag** which positions look most worth a market-reaction check, then defer: `→ Run $retro [window]` (or `$retro [window] TICKER` for a single name) to quantify the gap and rank trade ideas. Do not issue price/consensus web searches from `$surface`.

**Research Freshness Audit** (forward attention only — no market overlay)
- From vault data alone: which theses have the oldest last-Research/-note date? Rank them. This is a *what-to-research-next* signal (surface's forward domain).
- Do NOT web-search for "recent developments" here — that market-overlay work belongs to `$retro` (backward) and `$catalyst` (forward events). Surface flags the staleness; retro/catalyst supply the external delta.

**Thesis Velocity & Attention Allocation**
- **Research velocity ranking**: Which theses received the most research activity recently (new Research/ notes, Log entries, edits)? Which received zero? Rank all active theses by volume of recent activity.
- **Attention vs conviction alignment**: Compare where research time was spent against conviction levels. Flag any mismatch — disproportionate time on low-conviction ideas while high-conviction theses go unattended is a resource allocation error.
- **Decay alert**: List any active thesis that hasn't been touched (no Log entry, no new linked research) in 30+ days. These are candidates for `$deepen` or `$prune`.

## Phase 2.5: Story-log drift mining (unscoped and `all` modes only — 2026-07-20)

The n8n Workflow 3 news sweep writes one machine-readable story log per run to `.data/news_stories/*.json` (schema: `{date, stats, stories: [{title, cluster, score, sum, members}]}`). This corpus records *what actually scored high against current coverage* — the empirical check on whether the watcher registry is drifting behind reality.

1. **Read** (skip silently if the folder is absent or empty — the sweep may not be live): `ls .data/news_stories/*.json` → parse the last `track_window_d` days of files (registry Tuning row, default 30). Budget guard: read at most 60 files.
2. **Aggregate** stories with `score ≥ track_min_score` (registry Tuning row, default 8). Group by recurring subject (same company/technology/theme appearing across ≥3 distinct days). **Sentiment trajectory**: for any ticker/theme with ≥3 days of coverage, also read each story's `sig`/markers (the 𝕏 bullish/bearish/quiet and catalyst-proximity tags Assemble stamped) across the window — a directional shift (e.g. 𝕏 flips bearish→bullish, or scores trend up) is a tracked sentiment change worth surfacing alongside the drift signals. The logs are the substrate; this read is the 30-day sentiment view the user asked for.
3. **Compare against the registry**: read `_watchers.md § News & Thematic`. Two drift signals:
   - **Missing watcher**: a recurring high-score subject with NO matching registry row → the sweep is catching it only incidentally (via outlet feeds or ticker queries); a dedicated thematic row with a proper `thesis` anchor would track it deliberately. Propose the row (id, query, thesis link, expires) in the report.
   - **Dead watcher**: an `active` registry row whose query subject produced ZERO stories (any score) across the window → the theme has gone quiet or the query is mistuned. Propose `paused` or a query rewrite.
4. **Output**: add a `### Registry drift` section to the Phase 4 report listing proposed row additions/retirements — proposals only, the user edits `_watchers.md` (or asks Claude to). Registry drift findings do NOT go to `_followups.md` (they are config hygiene, not research opportunities) — EXCEPT when a missing-watcher subject also generates a Phase 3 opportunity, in which case the opportunity entry carries it.

This phase feeds Phase 3: a recurring high-score subject with no thesis anchor anywhere in the vault is itself a candidate opportunity (new-thesis or macro-note gap).

## Phase 3: Opportunity Generation

Generate 3-5 specific, actionable research prompts ranked by potential conviction impact:

For each opportunity:
- **Topic**: What to research
- **Why now**: What triggered this being relevant
- **Vault connection**: cite **≥2 specific cross-note datapoints** (name the notes) that, connected, produce the insight — a single-note observation is a summary, not a surfaced connection. The vault's edge is correlating optically-insignificant datapoints across notes (AGENTS.md); an opportunity that rests on one datapoint or a generic theme fails this bar.
- **Model trigger**: the mental-model trigger the opportunity rests on, cited by stable ID (`[G-#]` / `Industry #` / `Lens §`) or `none`. Binds the mandated Mental-Models read to each idea (per-opportunity, not one global gate check); when ≥2 sources point the same way, treat the agreement as a trigger to disconfirm (READING PROTOCOL), not to commit.
- **Falsifier**: the single observable that would prove this opportunity ISN'T real (READING PROTOCOL — every surfaced idea is a hypothesis; name what kills it). An opportunity with no falsifier is a narrative, not a testable idea.
- **Priced-in check**: whether the market already prices this — `already consensus / partially priced / genuinely non-consensus — [what the market currently assumes]`. Source it from the relevant sector note's `Investor heuristics` section (already in the Phase 1 read set). An opportunity the market already prices has no edge even if true; this field makes that explicit per idea.
- **Expected impact**: High/Medium/Low potential to change a conviction level
- **Suggested approach**: Specific research steps

**Targeted deep read before saving (default section-targeted mode).** Default mode skips each thesis's Business Model & Product Description and Industry Context (Phase 1) — the likeliest home of the cross-company linkage an opportunity rests on. Once an opportunity is generated, do a TARGETED read of those two sections for ONLY the tickers it implicates (not the whole portfolio) to pressure-test the connection before saving. Keep it targeted — implicated tickers only; a portfolio-wide back-fill would defeat the mode's read budget.

## Phase 4: Output

Save findings to:
- **Unscoped default**: `Research/YYYY-MM-DD - Insight Surface Scan.md`
- **Unscoped `all`**: `Research/YYYY-MM-DD - Insight Surface Scan (all).md`
- **Ticker-scoped**: `Research/YYYY-MM-DD - [TICKER] - Surface Scan.md`
- **Sector-scoped**: `Research/YYYY-MM-DD - [Sector] - Surface Scan.md`

If the file already exists, append a counter (`...2.md`, `...3.md`). Save with:
```yaml
---
date: YYYY-MM-DD
tags: [research, meta, surface-scan]
status: active
source: vault synthesis
source_type: synthesis
scope: default | all | ticker:TICKER | sector:[Sector]
propagated_to: []
---
```

The `scope:` frontmatter field records which mode produced the note — lets downstream review (and `$lint`) distinguish a routine section-targeted scan from a deep `all` scan or a scoped run.

> **Why `propagated_to: []`**: Surface scans are exploratory portfolio-level metadata, not per-thesis evidence. Their body wikilinks reference many theses for context, NOT to claim each one needs a Log entry. The empty list is a **terminal dedup signal** to `$sync` Check 2 — the producer skill (this `$surface` run) explicitly declares "no propagation needed." Without this, the next `$sync` would treat each body wikilink as a propagation target and spam Log entries across 10+ theses with shallow scan-derived insights. See `$sync` Step 1 Check 2 for the empty-list semantics.

> **Graph update deferred**: `_graph.md` is now owned exclusively by `$graph`. After this skill, run `$graph last` to register the surface scan research note, new cross-thesis connections, and any implied-but-unwritten thesis candidates in the dependency map.

Update `_hot.md` (read first, then edit — do NOT touch Latest Sync or Sync Archive, owned by `$sync`):

1. **Active Research Thread**: **Same-ticker continuation** — if the current thread already covers the same primary ticker/topic, append a dated line (`YYYY-MM-DD: [update]`) to the existing thread instead of compressing. **New topic**: compress the outgoing thread into a single `*Previous:*` entry (date + one-phrase summary). Write: surface scan completed [scoped/unscoped], top insight found, and the logical next research step. Append `*Previous:*` line(s) — max 5, drop oldest.
2. **Open Questions**: Add any critical blind spots or research gaps the scan exposed

**Word cap**: After all `_hot.md` edits, check total word count. If over 8,000 words (soft cap per `.agents/skills/_shared/hot-md-contract.md`), prune `## Sync Archive` entries (oldest first), then `*Previous:*` lines in Active Research Thread (oldest first), until under cap. If over 10,000 (hard cap), abort `_hot.md` update per contract.

**Note body carries every Phase 3 field per opportunity — the Falsifier is mandatory in the saved note, not just the chat report.** If opportunities are rendered as a table, `Falsifier` is a required column; if as prose blocks, each opportunity ends with its `Falsifier:` line. A surfaced idea whose falsifier survives only in chat is unfalsifiable by the time anyone re-reads the note.

**Trigger-utilization rollup (report section).** Add a short section to the report summarizing which mental-model lenses fired across this run's opportunities (from the Phase 3 `Model trigger` fields). A lens that NEVER fires across any opportunity is a **blind spot** — the vault isn't looking through it; a lens that fires on EVERYTHING is **decoration** — it isn't discriminating between ideas. This is a meta-signal on the reading gate itself: the utilization pattern audits whether the Mental-Models read is doing analytical work or just being ritually cited.

**Write actionable opportunities to the open-findings register** (`_followups.md` at vault root — durable ledger, `.agents/skills/_shared/followups-contract.md`). Read the file first (auto-created by the first writer if absent). For each Phase 3 opportunity ranked worth a concrete next skill (`$thesis`, `$deepen`, `$ingest`, `$stress-test`), append ONE entry to `## Open` (prepend under the heading — newest first):

`- [ ] YYYY-MM-DD · surface · [[Theses/TICKER - Name]] · <opportunity one-liner>, <suggested skill> → user acts or dismisses · src [[Research/YYYY-MM-DD - Insight Surface Scan …]]`

Use `portfolio` in place of the thesis wikilink for cross-ticker opportunities (blind spots, supply-chain correlations). Only genuinely actionable opportunities — never routine scan output.

- **Dedup (mandatory)**: grep `## Open` for a `surface ·` entry on the same thesis/opportunity; if present, update its date instead of stacking a duplicate.
- **Soft cap**: if `## Open` exceeds 50 entries, surface `⚠️ _followups.md over 50 open entries — review/resolve backlog` in the report; never auto-drop open entries.
- Resolvers `$status` and `$sync` close entries later; surface only appends.
- **Non-fatal**: on register write failure, report and continue — the Research note and `_hot.md` update are unaffected.

Also report a concise summary to the user highlighting the top 3 most actionable insights.
