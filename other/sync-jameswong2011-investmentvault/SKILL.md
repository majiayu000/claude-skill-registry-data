---
name: sync
description: Synchronize recent research learnings across all affected theses, sector notes, and macro documents. Use after a research session or when user says "sync", "propagate", or "update everything".
model: opus
effort: max
allowed-tools: Read Grep Glob Edit Write Bash(date * find * cp * mkdir * touch * awk * sed * grep * git diff *)
---

Propagate recent research insights across all affected vault documents. **For each affected note, think through the full implications of new research on every substantive section — not just append links.**

Design rationale in `.claude/skills/sync/RATIONALE.md` (§N.M anchors).

**Shared contracts this skill consumes**:
- `.claude/skills/_shared/preflight.md` — vault locks, rename markers, name sanitization, section probes.
- `.claude/skills/_shared/wikilink-forms.md` — the 5 canonical wikilink forms every matcher must cover.
- `.claude/skills/_shared/hot-md-contract.md` — `_hot.md` compression budget and section ordering.
- `.claude/skills/_shared/log-prefixes.md` — registry of Log-entry prefixes carrying cross-skill semantics.
- `.claude/skills/_shared/sector-resolution.md` — thesis `sector:` → sector note resolution.
- `.claude/skills/_shared/mental-models-section.md` — the `## Mental Models` section schema, the MANDATORY `/Mental Models` reading gate, and the merge/idempotency write procedure.

## Step 0: Pre-flight (MANDATORY — runs before Step 1)

### 0.1: Acquire vault lock
- **`/sync` (default) and `/sync all`**: acquire `vault-wide` scope lock per preflight Procedure 1. Timeout: 15 min (`/sync all`), 5 min (default).
- **`/sync TICKER`**: acquire `ticker:TICKER` scope lock. Timeout: 5 min.

Capture the token at Step 0.1, verify ownership (Procedure 1.5) at every Bash block, release via `rm -f "$LOCK_FILE"` in the final reporting Bash block.

### 0/1 Parallel Probe Directive

Step 0.2 (rename-marker glob), Step 1.1 (`find -newer`), and Step 1.2 (Read `_graph.md`) are independent read-only probes that fire AFTER lock acquisition and BEFORE any mutation. **Issue them as a single parallel tool-call batch** — one message containing the `.rename_incomplete.*` glob, the `find -newer .last_sync` Bash, and the `_graph.md` Read. Ownership verification on subsequent Bash blocks (per preflight §1.5) still runs on every mutation block; this batch only collapses three sequential read round-trips into one. On rare lock-collision edge cases where another skill is mid-release, the wasted work is negligible (milliseconds of find + one Read).

### 0.2: Rename-marker check
- **`/sync TICKER`**: preflight Procedure 2. Hard-block if `.rename_incomplete.TICKER` exists.
- **`/sync` / `/sync all`**: glob `.rename_incomplete.*`. Hard-block if ANY marker exists — these modes propagate across the vault; a single mid-rename ticker would split inbound wikilinks across old/new names.

### 0.3: Metadata boundary
`/sync` does NOT write to `_graph.md`. Graph maintenance is owned exclusively by `/graph` (run `/graph last` after this skill). `/sync` reads `_graph.md` as an input; never writes it.

## Sync Modes

Parse `$ARGUMENTS`:
- **`/sync`** (default) — Graph-assisted targeted sync. Uses `_graph.md` if present; file-direct fallback only when graph returns empty for a given source (§2.2). Use after post-ingest propagation.
- **`/sync all`** — Full brute-force sync via graph-cached two-pass triage. Use after major research sessions or monthly maintenance.
- **`/sync TICKER`** — Ticker-scoped sync. Reads the thesis directly and reconstructs adjacency from outbound wikilinks. No graph dependency.

## Watermark

Change detection uses `.last_sync` as the timestamp watermark. Touch policy:

| Mode | `.last_sync` behavior | `.sync_all_fresh` marker |
|---|---|---|
| `/sync` (default) | Touch at end | — |
| `/sync all` | Touch at end | Write at end (triggers `/graph` full rebuild) |
| `/sync TICKER` | Do NOT touch (§6.1) | — |

**First run**: if `.last_sync` does not exist, create it with epoch timestamp: `touch -t 197001010000 .last_sync`. This applies to ALL modes (including ticker-scoped — epoch placeholder preserves baseline without advancing the watermark).

---

## Step 1: Identify Changes

### 1.1: Find changed files

If `$ARGUMENTS` specifies files, use those. Otherwise:
```bash
find Research/ Theses/ "Macro & Technology/" Sectors/ -newer .last_sync -name '*.md'
```

If no changed files AND no files specified → report "Nothing changed since last sync" and stop (skip Step 2.9 manifest — no-op runs are pure read).

### 1.2: Resolve propagation targets per changed research note

For each changed research note, the target set is the UNION of every thesis plausibly affected.

**Primary resolution — graph-assisted**: if `_graph.md` exists, look up the research note in each thesis's `research:` adjacency. Collect matches.

**File-direct fallback (T7.2 — conditional)**: run ONLY when graph-assisted returned EMPTY for this research note OR `_graph.md` is missing/unparseable. Resolves via:
- (a) Research note's `ticker:` frontmatter matching `Theses/[TICKER] - *.md`
- (b) Outbound `[[Theses/...]]` wikilinks in the research note body
- (c) `tags:` containing ticker-shaped tokens (all-uppercase, 1-5 chars) matching `Theses/[TICKER] - *.md`

When graph returned non-empty, trust the graph — see §2.2 for why. `/lint #23` catches residual reverse-index drift.

### 1.2.5: Resolve SECTOR + MACRO propagation targets per changed research note

Step 1.2 resolves research note → thesis targets. This step does the same for sector and macro targets — explicitly at Step 1 time, not lazily inside Step 4.-1 / Step 5.-1 gates. Symmetric with 1.2; prevents the cognitive shortcut where thesis-idempotent research notes cause Step 4 / Step 5 to be erroneously skipped via mental over-reach of the Step 2 source-dedup clause (see §1.11 for the 2026-04-22 failure case that motivated this step).

For each changed research note, compute two maps:

**`sector_targets_per_research_note[note]`**:
- (a) `sector:` frontmatter → resolve via `.claude/skills/_shared/sector-resolution.md` to a `Sectors/*.md` path.
- (b) Body wikilinks matching any of the 5 canonical forms from `_shared/wikilink-forms.md` against `[[Sectors/...]]` / `[[Sectors/name]]` / `[[Sectors/name.md]]` — resolved via sector-resolution contract.

Union (a) ∪ (b); dedup on resolved path.

**`macro_targets_per_research_note[note]`**:
- (a) Body wikilinks matching `[[Macro & Technology/...]]` forms (5 canonical forms).
- (b) `source_type: scenario` frontmatter OR `tags:` containing `macro` → body-scan for any `Macro & Technology/` references (treat as macro-focused note even without explicit body wikilink).
- (c) Optional `macro:` frontmatter field if the note convention uses it.

Union across (a)/(b)/(c); dedup on resolved path.

These maps are **inputs to Step 4.-1 condition (ii) and Step 5.-1 condition (ii)** as direct lookups — not re-derived at gate time. Empty set is a valid value (research note has no sector/macro relevance); the gate still fires its skip path correctly in that case.

**Authoritative-guard boundary**: Step 4.-1 / 5.-1 remain the authoritative skip gates. Step 1.2.5 only makes the gate's inputs explicit and first-class. Do not duplicate the gate logic here.

### 1.3: Resolve propagation targets per changed macro note (batched — T7.6)

**Reverse-index resolution (primary)**: Use `_graph.md`'s `Reverse Index: Macro → Theses` table for each changed macro.

**Body-grep fallback (T7.6 — one batched regex)**: ALWAYS runs to catch asymmetric adjacency (thesis wikilinks macro but macro doesn't reciprocate — §2.1). For a set of changed macro basenames `{X, Y, Z}`, issue ONE Grep:

```
Grep pattern='\[\[(Macro & Technology/)?(X|Y|Z)(\.md)?(#[^\]|]+)?(\|[^\]]+)?\]\]' path='Theses/' glob='*.md' output_mode='files_with_matches'
```

(Basenames regex-escaped; alternation built from the changed-macro set.) Output gives `file → needs Grep match re-parse to identify which macro(s)`; a second pass on the returned file subset extracts specific basename matches. Two Grep calls total, regardless of changed-macro count. Dedup against reverse-index results.

### 1.4: Resolve propagation targets per changed sector note

Graph-assisted only. Sector notes are required by template to list `## Active Theses` with every active thesis. `/lint #2` catches missing MOC entries.

### 1.5: Closed-status filter (T7.7 — single Grep)

Before detailed idempotency work, filter out theses whose status is `closed`. ONE Grep vault-wide:

```
Grep pattern='^status: closed' path='Theses/' glob='*.md' output_mode='files_with_matches'
```

For every thesis in the closed set that also appears in a target set from 1.2/1.3/1.4:
```
⚠️ Skipped [TICKER] — status: closed but file remains in Theses/ (failed archive move). Complete: mv "Theses/[file]" "_Archive/[file]" → /graph last. Or reopen: /status TICKER status closed→active [rationale].
```

### 1.6: Missing-file resilience

If a thesis listed in graph adjacency no longer exists on disk (archived since last graph rebuild):
```
⚠️ Skipped [filename] — file not found (likely archived). Run /graph last to refresh the dependency map.
```

Research notes with no resolvable target via 1.2:
```
ℹ️ [filename] — no propagation target found. Consider adding ticker: frontmatter or [[Theses/...]] wikilinks, or run /thesis [TICKER] to create the missing thesis.
```

### 1.7: Unified dedup + per-thesis idempotency (T7.1)

For each changed research note, run ONE Grep pass to find every thesis that might already reference it — using the 5 wikilink forms from `_shared/wikilink-forms.md`. This single scan serves Case 2a, Case 2b, and Check 3 simultaneously (§1.5).

**Per-research-note primary grep** (base-name escaped for regex metacharacters):
```
Grep pattern='\[\[(Research/)?<base-escaped>(\.md)?(#[^\]|]+)?(\|[^\]]+)?\]\]' path='Theses/' glob='*.md' output_mode='files_with_matches'
```

**Log-section confirmation** (semantics preservation): the primary grep matches the wikilink ANYWHERE in the thesis file, but idempotency is defined by prior Log entries, NOT by wikilinks in `## Related Research` (the user may have manually wikilinked without a Log entry, in which case /sync should still write the Log entry). Confirm in-Log presence via one Bash block across the primary match set:

```bash
# ESC_PATTERN is the same regex as the primary grep, escaped for awk.
for f in <files-returned-by-primary-grep>; do
  awk '/^## Log/{in_log=1; next}
       in_log && /^## /{exit}
       in_log && ENVIRON["ESC_PATTERN_MATCH"] ~ $0{found=1}
       END{if(found) print FILENAME}' "$f"
done
```

Alternatively (cleaner): use `grep -n` to get the line number of each primary-grep match, then intersect with the `## Log` section's line range (extractable via `grep -n '^## ' "$f"` once per file). Either approach confirms "is match line within `## Log` section" — files where the only match lies in `## Related Research` or elsewhere are NOT in the confirmed-Log set.

The result — `wikilink_match_set` — is the set of thesis files with confirmed in-Log references to this research note. These are the already-propagated targets.

This two-pass structure keeps the token-saving win of T7.1 (primary grep is O(1) per research note vs old O(N) Read per candidate) while preserving the original Log-section-only idempotency semantics.

Now classify the research note's `propagated_to:` frontmatter:

**Case 2a — Field absent**: no producer-side dedup info. For each ticker in the Step 1.2 target set:
- If that thesis is in `wikilink_match_set` → treat as already-propagated; skip. Log: `ℹ️ Log-history backfill skip: [TICKER] already has Log entry referencing [research-note]. propagated_to: absent; retry suppressed.`
- Otherwise → check Step 1.8 secondary keys; if any match → skip (rename/move case). Else → this ticker needs propagation; proceed to Step 2.
- After successful propagation completes, backfill the research note's `propagated_to:` frontmatter as a union of `wikilink_match_set` (resolved to tickers) + freshly-propagated tickers + any secondary-key-matched tickers. See `Atomicity rule` below.

**Case 2b — Field present and non-empty** (e.g., `propagated_to: [TICKER1, TICKER2]`):
- Tickers in `propagated_to:` → skip. Log: `ℹ️ Skipped [TICKER] — producer skill already propagated (in propagated_to).`
- Augmented targets (tickers in Step 1.2 target set but NOT in `propagated_to:`): for each, check `wikilink_match_set`. If present → skip (already propagated via another path). If absent → check Step 1.8 secondary keys; if any match → skip; else → propagate. Log: `➕ Augmented propagation: [TICKER] — not in propagated_to but resolved via [wikilink | tag | ticker frontmatter].`

**Case 2c — Field present and empty** (`propagated_to: []`): terminal skip for ALL targets. Log once: `ℹ️ Skipped all propagation for [research-note] — empty propagated_to: signals producer-side terminal decision.` Do NOT evaluate augmented targets. Producer must explicitly opt-out with `[]` to trigger this case (§1.6).

### 1.8: Secondary-key fallback for wikilink misses (T7.1 refinement)

When a Step 1.2 target thesis is NOT in `wikilink_match_set` but the user may have renamed the research note (wikilink drift), check stable identity keys in order. Reads candidate thesis Log section plus at most one research-note frontmatter per candidate.

**Key A — `source:` URL match**: if the current research note's `source:` is a URL (not "vault synthesis"), scan the thesis's `## Log` section for Log entries whose cited research notes share the same URL. Requires cross-read of candidate research notes' frontmatter. Match → treat as already-propagated.

**Key B — `date: + ticker:` tuple match**: for vault-synthesis notes without URLs (`/scenario`, `/stress-test`, `/compare` outputs). Scan thesis Log for entries citing Research/ notes with the same `date:` AND same `ticker:` tuple.

**Key C — `tags:` intersection + date match**: weakest. Current note's tags include ticker-shaped tokens overlapping thesis's `ticker:`, AND thesis Log has an entry citing a Research/ note whose `tags:` include the same token AND that entry's date matches current note's `date:`.

On any match: `ℹ️ Skipped duplicate propagation for [TICKER] — Log references equivalent research note ([key type]: source URL | date+ticker | tags). Current: [[Research/current-name]]. Prior match: [detail].`

Secondary keys fire rarely (only on rename/move events); their cost is bounded by the size of Step 1.2 target set minus `wikilink_match_set`.

### 1.9: Atomicity rule for `propagated_to:` updates

Update the research note's `propagated_to:` frontmatter ONLY after EVERY target thesis's Log entry has landed successfully for this research note in this run. If any Edit failed:
- Do NOT update `propagated_to:` at all for this research note.
- The next `/sync` retries the missing target via Case 2a flow.

If every append succeeded, union existing `propagated_to:` with the newly-propagated tickers AND with any tickers found via Case 2a backfill scan. This moves Case 2a retries into Case 2b on future runs, eliminating the scan cost.

Atomicity scope: ONE research note. Partial success across multiple research notes in the same run is fine — each gets its own all-or-nothing decision.

**Per-research-note append-failure reporting**: list failed targets in Step 8 under `propagated_to: update skipped`.

### 1.10: Mode-specific resolution continued

#### All mode (graph-cached two-pass — T7.3)

**Pass 1 — graph-cached triage** (no thesis file reads):
1. Read `_graph.md` ONCE. Parse the Adjacency Index with `status:` and `log_tail:` fields.
2. Read ALL macro notes in full (bounded set, ~6 files).
3. For each thesis, classify using graph data alone:
   - **High delta** (any of):
     - **Self-modified**: thesis file mtime newer than `.last_sync`. Captures manual edits with no Log entry (§3.1). Always escalates; read full thesis in Pass 2.
     - Directly referenced by a changed research note (from Step 1.2 results), OR
     - Shares sector with changed content (graph reverse index), OR
     - Has cross-thesis links to changed theses (graph adjacency), OR
     - `log_tail:` shows recent conviction/status/reaffirm prefix within last 14 days.
   - **Low delta**: same macro exposure or adjacent sector, no direct reference, not self-modified. Read **Summary + Non-consensus Insights + Outstanding Questions + Bull/Bear Case** only.
   - **No delta**: no plausible propagation path, not self-modified. Do NOT read.

**Pre-T7.3 fallback**: if `_graph.md` lacks `log_tail:` fields, extract frontmatter + Summary + last 3 Log entries per thesis in one batched Bash call as a transient in-memory substitute. Full AWK implementation in RATIONALE §10 (transitional — only fires if a pre-T7.3 `_graph.md` is restored from backup).

**Pass 2 — deep read for High-delta only (single parallel batch)**:

**Issue ALL Pass 2 reads as a single parallel tool-call batch** — one message containing every High-delta full-thesis Read, every Low-delta section-slice Bash, and every sector Read. Do NOT serialize per-thesis. A typical 15-25-file Pass 2 lands in one round-trip instead of 15-25 sequential rounds.

- For each High-delta thesis: read the full file (Step 3a may further scope per T7.5 — see Step 3).
- For each Low-delta thesis: read only the named sections via section-slice Bash. All Low-delta section-slices can be consolidated into a single Bash block that iterates the Low-delta list — one tool call regardless of Low-delta count.
- For sectors containing at least one High-delta thesis: read in full (parallel Read inside the same batch as the thesis Reads).
- Macro notes: already read in Pass 1 — do NOT re-read.

This typically reduces deep reads from ~58 files to 15-25 AND collapses those 15-25 into one round-trip. Combined with Pass 1 being a single batch, total Phase 1 cost is ~2 round-trips regardless of vault size.

#### Ticker-scoped mode

1. Locate via `Theses/TICKER - *.md` prefix glob.
   - No match, check `_Archive/`: `⚠️ [TICKER] is closed — file lives in _Archive/. To reopen: /rollback TICKER → select pre-status snapshot → /sync TICKER.`
   - Not anywhere: `⚠️ No thesis found for [TICKER]. Run /thesis [TICKER] to create it.`
   - Multiple matches: `⚠️ Multiple Theses/ files match prefix "[TICKER]" — [list]. Resolve filename collision before re-running.`
2. Read frontmatter. If `status: closed` but still in `Theses/`: `⚠️ [TICKER] has status: closed but file remains in Theses/ (failed archive move). ...`
3. Reconstruct adjacency from the thesis file (do NOT read `_graph.md` — file-direct is the only path in ticker mode):
   - Outbound `[[wikilinks]]` categorized by directory (Sectors/, Macro & Technology/, Theses/, Research/).
   - Scan `Research/` for files with `ticker: TICKER` in frontmatter.
4. Read all resolved files. Ignore `.last_sync` watermark (timestamp-independent).
5. Proceed to Step 2.

---

## Step 2: Deep Implication Analysis

**Mental Models reading gate (MANDATORY — before enumerating implications).** Complete the mental-models read per `_shared/mental-models-section.md` NOW, not at Step 3b write time: read `Mental Models/Generalist - Overview.md` (always) + the matching `Industry -` file(s) for the sectors in scope + any `Lens -` file the changed sources touch (once per run, cached). The models must inform WHAT gets propagated — implication generation is where the vault's edge (non-consensus connections, inflection-point triggers) either happens or doesn't; a write-time-only read arrives after the analytical work is done. Apply the READING PROTOCOL: implications are hypotheses to test, base-rate runs adversarially, cross-source agreement triggers a hunt for the falsifying datapoint. (Step 3b/4b then merge any fired triggers into `## Mental Models` sections per the contract — unchanged.)

**Maximum reasoning effort here.** For each source note read fully and analyse:

- **Factual deltas**: new data points, metrics, quotes, events.
- **Assumption challenges**: which existing thesis assumptions does this validate, weaken, invalidate? Name the assumption.
- **Second-order implications**: what follows that isn't explicit?
- **Competitive dynamics shifts**: does this change relative positioning within a sector?
- **Macro linkages**: does micro-level data have macro implications, or vice versa?

**Source deduplication (ANALYSIS-SCOPE ONLY)**: if a thesis appears as a changed source AND research notes referencing that thesis are also in the changed set, treat the research notes as primary sources for Step 2 reading — skip the thesis's Log entries citing those research notes during analysis (they duplicate the research note's content).

**This rule does NOT suppress Step 4 sector or Step 5 macro propagation.** Sector and macro propagation are gated separately at §4.-1 and §5.-1 against the research note's own `sector_targets_per_research_note` / `macro_targets_per_research_note` sets resolved at Step 1.2.5. Source-dedup only changes HOW YOU READ sources during analysis; it does not change WHAT YOU ACT ON downstream.

**Common mis-application** (from 2026-04-22 failure, §1.11): concluding "all thesis targets are idempotent per Step 1.7 → nothing to propagate" and skipping Step 4/5 entirely. This is wrong. Thesis idempotency (Step 1.7) and sector/macro propagation (Step 4/5) are independent propagation paths. A research note that has already been fully propagated to its thesis targets may still have pending sector or macro propagation — always evaluate Step 4.-1 and Step 5.-1 against the research note's own target maps from Step 1.2.5, regardless of thesis-target idempotency.

Propagation quality depends on this step's depth.

---

## Step 2.5: Classify Change Sources (skill-origin gate)

Gates Step 4 / Step 5 — a thesis-only change driven by a skill that already handled downstream sector/macro state should not trigger redundant `/sync` re-edits.

### Classification method (T7.3 — graph-cached)

For each changed thesis, read the most recent Log entry from `_graph.md`'s `log_tail:` field (single-line lookup, zero file reads). If `log_tail:` is missing (pre-T7.3 graph) OR the thesis isn't in the graph, fall back to one bounded Bash call:

```bash
# Batch-extract most-recent Log bullet for up to N theses.
# CONVENTION: Log entries are append-only with newest at the BOTTOM
# (CLAUDE.md Tier 2 §2: "only append new dated entries at the end").
# Track the LAST date+bullet pair seen, emit in END.
# CRITICAL: do NOT `exit` on first bullet match — that returns the OLDEST
# entry and silently misclassifies theses whose initial Log entry is a
# skill-origin prefix (e.g., "Initial thesis created") but have since had
# research-driven entries appended (the AVGO/MRVL/CRWD/PANW failure mode
# observed 2026-04-26).
for f in Theses/TICKER1 - Name.md Theses/TICKER2 - Name.md; do
  echo "=== $f ==="
  awk '/^## Log/{in_log=1; next}
       in_log && /^## /{exit}
       in_log && /^### [0-9]{4}-/{date=$2; next}
       in_log && date != "" && /^- /{last_date=date; last_bullet=$0}
       END{if(last_date) print last_date" | "last_bullet}' "$f"
done
```

### Classification rule

For each changed thesis:
- **Research-driven** (default): at least one research note in the changed-file set resolves (via Step 1.2) to this thesis, OR recent Log entries reference changed research notes. Proceed through Step 3/4/5 normally.
- **Skill-origin**: thesis is self-modified (`mtime > .last_sync`) AND most-recent Log entry matches a skill-origin prefix from `_shared/log-prefixes.md` (registry §5 `Conviction reaffirmed`, §6 `Status change: conviction`, §7 `Status change:`, §8 `CLOSED`, §9 `Prune upgrade`, §11 `Initial thesis created`, §12 `ROLLBACK to snapshot`, §13 `Cross-thesis closure:` / `Cross-thesis closures:`, §14 `Scenario REVERSED`, §15 `Renamed file:`, §16 `Comparison `, §17 `Callout sweep:`, §18 `Numbers refresh:`, §19 `Cross-thesis signal via`, §20 `Metrics synced:`) AND no research note in the changed-file set resolves to this thesis.
- **Mixed**: research-note source AND skill-origin Log prefix → treat as **research-driven**.

### Body-change override (2026-07-08 — closes the silent-skip failure mode)

The skill-origin classification keys purely on the *most-recent Log prefix*. Its known failure (CLAUDE.md Workflow Rule #6; §1.11): the user manually edits a thesis **body** (Bull Case, Risks, Industry Context…) but forgets to append a Log entry, so the most-recent prefix is still a prior skill's — the edit is misclassified skill-origin and sector/macro propagation is **silently skipped**. Previously this surfaced only as a passive Step 8 report line; now it is an **active gate**.

For each thesis about to be classified **skill-origin**, detect whether its body changed **outside `## Log`** since the last sync:

- **Primary (git)**: `git diff --unified=0 HEAD -- "Theses/TICKER - Name.md"` (the vault is a git repo). Determine whether any changed hunk falls outside the `## Log` section — parse hunk line ranges against the `## Log` start line (awk: line number of `^## Log`). Changes only within `## Log` → genuinely skill-origin (skill Log-append). Any change above `## Log` (or to a non-Log section) → **body edit**.
- **Fallback (no git / not a repo / `git` unavailable)**: diff the current body-outside-`## Log` against the most-recent prior `(pre-sync …)` snapshot for this thesis in `_Archive/Snapshots/` (awk-extract everything before `^## Log` from both, compare). No prior snapshot → cannot determine; retain skill-origin classification and rely on the Step 8 report (current behavior — no regression).

**On body-edit detection**, do NOT silently reclassify and do NOT silently skip. Surface an inline prompt:

```
⚠️ [TICKER] classified skill-origin (most-recent Log prefix "[prefix]"), but its body changed
outside ## Log since the last sync — likely a manual edit with no Log entry (Workflow Rule #6).
Propagate this thesis's changes to sector/macro notes as research-driven? [Y/n]
(Y = treat as research-driven and propagate — recommended; n = keep skill-origin, skip sector/macro)
```

Default **Y** (mirrors the Mixed → research-driven precedent). On Y, move TICKER out of `skill_origin_theses` and process it through Steps 3/4/5 normally; also recommend the user append a `Manual edit:` Log entry so future syncs classify it correctly without the prompt. On n, leave it skill-origin. Batch the prompt if multiple theses trip it (one consolidated question listing all affected tickers).

**Cost containment**: the `git diff` runs ONLY for theses that would otherwise be classified skill-origin (typically 0–few per sync), never for research-driven theses. False-positive guard: if the user hasn't committed since a prior in-session skill edit, `git diff HEAD` may include that skill's own body edits — the prompt (not silent reclassification) is what makes this safe, since the user confirms.

### Output

Maintain in-memory accumulator `skill_origin_theses: [TICKER, ...]`. Steps 4 and 5 consult this before per-sector / per-macro propagation. The Body-change override runs before this accumulator is finalized, so any prompted-Y thesis is already removed.

### Registry-driven design

The skill-origin enumeration above is a view of `_shared/log-prefixes.md`'s `skill-origin` entries. `/lint #29` verifies registry/enumeration alignment. When a new skill-origin prefix is added: update the registry first, then this enumeration.

---

## Step 2.9: Write Sync Batch Manifest — Skeleton

**Mandatory BEFORE any vault state mutation.** Runs once per non-no-op run, immediately before Step 3.

### 2.9a: Batch ID and skeleton path

Generate `HHMMSS` via `date +%H%M%S` once at the start of Step 2.9. This is THE canonical batch ID — Step 3c reuses it for all Tier A snapshots; Step 7.5 flips the same manifest.

**Batch ID format**:
- `/sync` (default) and `/sync all`: `sync-YYYY-MM-DD-HHMMSS`
- `/sync TICKER`: `sync-TICKER-YYYY-MM-DD-HHMMSS` — prevents collisions between simultaneous `/sync NVDA` and `/sync AMAT`

Skeleton path:
```
_Archive/Snapshots/_sync-manifest (sync-YYYY-MM-DD-HHMMSS).md       # default / all
_Archive/Snapshots/_sync-manifest (sync-TICKER-YYYY-MM-DD-HHMMSS).md # ticker-scoped
```

### 2.9b: Write skeleton

```yaml
---
type: sync-manifest
batch: sync-YYYY-MM-DD-HHMMSS
mode: default | all | ticker-scoped
status: in-progress
date: YYYY-MM-DD
---

# Sync Batch Manifest (in-progress)

Manifest written at Step 2.9 before any file modifications. Populated at
phase boundaries (end of Step 3, 4, 5) then flipped to status: completed
at Step 7.5.

If this file persists with status: in-progress, the sync crashed or was
interrupted. Recovery: inspect the sections below, then /rollback to
restore any Tier A snapshots listed.

## Theses with snapshots taken (Tier A)
_populated at end of Step 3_

## Theses with Log-only appends (Tier B)
_populated at end of Step 3_

## Sector notes touched
_populated at end of Step 4_

## Macro notes touched
_populated at end of Step 5_

## Source research notes processed
_populated at end of Step 3_
```

### 2.9c: Skeleton write failure — hard abort

```
❌ Sync manifest skeleton write failed: [path]
   Reason: [error]

No vault state has been modified yet. Fix the filesystem issue (disk
space, permissions, concurrent writer) and re-run /sync.
```

Exit. Do NOT proceed.

### 2.9d: Phase-boundary checkpoints (T7.4)

Manifest writes happen at 4 discrete points — NOT per event. This is the T7.4 optimization: ~4 Edits on the manifest instead of ~49 for a typical `/sync all` run. In-memory accumulators per Step 7.5d collect events during each phase; phase-end Edit flushes all accumulated entries at once.

| Checkpoint | Fires at | Writes |
|---|---|---|
| Checkpoint A | End of Step 3 (all theses done) | Populates "Theses with snapshots", "Theses with Log-only appends", "Source research notes processed" |
| Checkpoint B | End of Step 4 (all sectors done) | Populates "Sector notes touched" |
| Checkpoint C | End of Step 5 (all macros done) | Populates "Macro notes touched" |
| Step 7.5 flip | After all writes complete | Flips `status: in-progress` → `status: completed` + `completed_date:` |

See §5.3 for crash-recovery implications. The phase-boundary design accepts intra-phase granularity loss (mid-Step-3 crash means that phase's theses appear only via snapshot file glob, not via manifest). `/rollback` remains correct in both cases.

---

## Step 3: Update Thesis Notes

### 3a: Section-scoped thesis read (T7.5)

Read the thesis with scope driven by Step 3b's impact map. Procedure:

1. From Step 2's analysis, predict which thesis sections need updates (use the table in Step 3b).
2. If predicted updates touch **≥5 sections**, read the full thesis — working memory benefits from complete context.
3. If predicted updates touch **<5 sections**, read targeted sections via Bash extract:

```bash
# Example: read frontmatter + Summary + Bull Case + Risks for one thesis
awk '
  /^---$/ && !fm_done { in_fm=!in_fm; print; if(!in_fm) fm_done=1; next }
  in_fm { print; next }
  /^## Summary/,/^## /{if($0!~/^## /||$0~/^## Summary/) print}
  /^## Bull Case/,/^## /{if($0!~/^## /||$0~/^## Bull Case/) print}
  /^## Risks/,/^## /{if($0!~/^## /||$0~/^## Risks/) print}
  /^## Log/{in_log=1}
  in_log{print}
' "Theses/TICKER - Name.md"
```

Always include frontmatter (for conviction/status) and full `## Log` section (for drift detection in Step 3e). The Log is the expensive part — its tail is what drift analysis needs.

**When section-scoping is skipped** (read full):
- `/sync TICKER` mode — always read in full (ticker-scoped cost is already bounded).
- High-delta self-modified thesis in `/sync all` (body may have arbitrary user changes).

### 3b: Analyse Impact Per Section

Map Step 2's insights against each thesis section. Be selective.

| Section | Update when... |
|---|---|
| Summary | Core investment case shifted — change in thesis direction or key assumption |
| Non-consensus Insights | New evidence strengthens/weakens existing insight, OR genuinely new angle |
| Outstanding Questions | Question answered (mark resolved + date), OR new questions raised |
| Business Model | Structural change to revenue model, product mix, go-to-market, segment economics |
| Industry Context | Competitive positioning, market share, pricing power shifted |
| Bull Case | New supporting evidence, or bull scenario element validated/invalidated |
| Bear Case | New counter-evidence, or bear scenario element validated/invalidated |
| Catalysts | New catalyst identified, or existing catalyst resolved — mark outcome |
| Risks | New risk emerged, existing risk probability changed materially, or risk retired |
| Conviction Triggers | New evidence validates/invalidates a trigger, OR threshold needs updating |
| Mental Models | A new research-activated `/Mental Models` trigger fires, an existing trigger's read materially changes, or models newly agree (disconfirm check) — per `_shared/mental-models-section.md`. High selectivity: most syncs leave it untouched. |

**Do NOT update sections where the delta is trivial.** Thesis contains synthesised conclusions, not duplicated research.

**Self-contradiction check (source-thesis disconfirm — applies the Step 4b sweep discipline inward).** For each section a propagated datapoint would update, determine whether the new evidence CONTRADICTS what that section — or the thesis's Bull Case / Bear Case / Non-consensus Insights / Conviction Triggers — already asserts, not merely whether it adds to it. A propagated figure that undercuts an existing claim must SURFACE, never be smoothed into the prose silently: accumulate it and emit in the Step 8 report as `⚠️ [TICKER] §[Section]: new evidence contradicts existing claim "[…]" — reconcile, don't silently merge`. Step 4b forces this disconfirm question against every OTHER thesis in the sector; this forces it against the source thesis /sync is writing INTO — the one place the cross-thesis sweep never covers.

**Mental Models section** — before writing it, read the relevant `/Mental Models` files and apply the READING PROTOCOL per `_shared/mental-models-section.md` (MANDATORY reading gate). Merge new triggers as hypotheses-to-test; never overwrite; idempotent on model + trigger name. An unchanged section is the correct outcome for most runs.

### 3c: Pre-Edit Safety — Snapshot

Classify edits by tier:
- **Tier A — snapshot required**: editing or rewriting existing text in Summary, Non-consensus Insights, Outstanding Questions, Business Model, Industry Context, Bull Case, Bear Case, Conviction Triggers, Mental Models (rewriting or striking through existing entries).
- **Tier B — no snapshot**: appending new Catalysts, Risks, Conviction Triggers, or Mental Models trigger lines; appending to Log / Related Research; updating Key Metrics numbers.

If any Tier A edits planned, snapshot ALL Tier A theses in one Bash block using background shell jobs + `wait` (mirrors `/compare` 5.5a and `/rollback` Step 4 patterns — each `cp` is independent; sequential execution over N theses wastes N-1 round-trips):

```bash
mkdir -p _Archive/Snapshots
# For each thesis T in tier_a_thesis_snapshots (from 3g accumulator), fire cp in background:
cp "Theses/TICKER1 - Name1.md" "_Archive/Snapshots/TICKER1 - Name1 (pre-sync YYYY-MM-DD-HHMMSS).md" &
cp "Theses/TICKER2 - Name2.md" "_Archive/Snapshots/TICKER2 - Name2 (pre-sync YYYY-MM-DD-HHMMSS).md" &
cp "Theses/TICKER3 - Name3.md" "_Archive/Snapshots/TICKER3 - Name3 (pre-sync YYYY-MM-DD-HHMMSS).md" &
wait
# Check exit status of background jobs before proceeding
```

For single-thesis Tier A (`/sync TICKER` or default sync with one affected thesis), this collapses to a single foreground `cp`. The batch form only matters for multi-thesis `/sync all` runs.

Then issue all frontmatter-addition Edits as a **single parallel tool-call batch** (one Edit per snapshot, all in the same message):
```yaml
snapshot_of: "[[Theses/TICKER - Company Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: sync
snapshot_batch: sync-YYYY-MM-DD-HHMMSS
```

Batch ID reused from Step 2.9. Proceed with edits to the ORIGINAL.

### 3d: Apply Substantive Edits

- **Integrate, don't append** — weave new evidence into existing prose. No "Update (date):" blocks within sections.
- **Carry provenance tags on propagated figures** — per `_shared/provenance-tags.md`, when a quantitative claim (price, margin, yield, share, growth rate) moves from a research note's `## Evidence` into a thesis or sector body, its provenance tag travels with the number. If inline space is tight, at minimum preserve the weak-sourcing signal (`[1×: source]` / `[est.]`); never launder a single-sourced or estimated figure into a bare, authoritative-looking assertion in a thesis spine.
- **New directional claims cite or propose a trigger** — when this sync introduces a NEW Bull Case, Bear Case, or Non-consensus Insight claim (not merely strengthening one that already exists), it must either cite the existing `## Conviction Triggers` entry the claim bears on OR flag that a new trigger should be added. A new directional claim with no falsification hook is exactly what `/lint #60` and the `_shared/trigger-touch.md` contract exist to prevent — surface the missing-trigger case in the Step 8 report as a suggestion (`→ [TICKER] §[Bull|Bear|Non-consensus]: new claim "[…]" has no matching Conviction Trigger — add one via /deepen Conviction Triggers`). Never launder an unfalsifiable directional claim into the thesis spine.
- **Preserve voice and structure**.
- **Net deletions are OK** — if new evidence invalidates a prior claim, remove the claim.
- **Mark resolved Outstanding Questions**: `~~Original question~~ → Resolved YYYY-MM-DD: [answer]`.
- **Resolve absorbed open findings** — per `_shared/followups-contract.md`, when a substantive edit absorbs an existing `_followups.md` open finding into a body section (a `/surface` opportunity woven into Bull Case, a `/retro` divergence resolved by the new evidence), move the matching `## Open` entry to `## Resolved` with outcome `absorbed`. Grep `_followups.md` `## Open` for entries on the affected ticker, match by topic. Never delete — Open→Resolved only. Non-fatal: on failure keep the entry Open and report it in the Step 8 report.

### 3e: Mechanical Updates (every time)

- **Key Metrics**: update table if new numbers.
- **Related Research**: add wikilink to new research note.
- **Conviction trigger check**: if new data satisfies a predefined trigger: `⚡ Trigger hit: [quote the trigger] — [what happened]`. This is the shared `_shared/trigger-touch.md` check applied to propagated research — a touched or crossed trigger is FLAG-ONLY: surface it, never auto-execute `/status` (conviction change is Tier-3, human-gated). Distinct from drift detection below — a trigger touch is a single-datapoint event; drift is the aggregate Log-sentiment window.
- **Conviction drift detection** — see `_shared/log-prefixes.md` for authoritative prefix list. `/lint #29` verifies consistency. Scan Log backward from most recent, excluding entries that begin with (unconditional exclusions):
  - `"Stress test"` (registry §1)
  - `"Deepening"` (registry §2)
  - `"Cross-thesis closure:"` / `"Cross-thesis closures:"` (registry §13)
  - `"Scenario REVERSED"` (registry §14)
  - `"Renamed file:"` (registry §15)
  - `"Callout sweep:"` (registry §17)
  - `"Numbers refresh:"` (registry §18 — a metrics refresh is hygiene, not conviction sentiment; without exclusion each refresh consumes a drift-window slot)
  - `"Metrics synced:"` (registry §20 — a `/deepen --sync-metrics` reconciliation is hygiene, same rationale as `Numbers refresh:`; without exclusion each sync consumes a drift-window slot)
  
  **Conditionally exclude** entries beginning with `"Deepened"` or `"↳ CORRECTION: Deepened"` within 14 calendar days of a `"Stress test"` entry (registry §3-§4; `deepened_exclusion_days` in `.drift-config.md`, default 14).
  
  **Anchor handling**: if `"Conviction reaffirmed"` (registry §5) or `"Status change: conviction"` (registry §6) found, anchor the window there — only count entries after. If fewer than 3 entries after anchor, drift detection has insufficient data. If no anchor, use last 5 non-excluded entries.
  
  **Threshold (tunable via `.drift-config.md` — schema in INFRASTRUCTURE.md §2.7)**:
  - Base: 3/5 weakening (if `conviction: high`) or 3/5 strengthening (if `conviction: low`).
  - **Post-stress-test suppression**: if `"Stress test"` entry within last 30 days, raise to 4/5.
  - Missing config → defaults. Malformed → `⚠️ .drift-config.md malformed — using defaults.`
  
  - `conviction: high` + threshold weakening → `⚠️ Conviction drift — [N]/[window_size] recent updates flagged headwinds ([threshold] required, post-stress-test suppression: yes|no). Reassess. To acknowledge: /status TICKER reaffirm [rationale]`
  - `conviction: low` + threshold strengthening → `📈 Positive drift — [N]/[window_size] recent updates supportive. Reassess. To acknowledge: /status TICKER reaffirm [rationale]`

### 3f: Log Entry (last)

Append to Log:
```
### YYYY-MM-DD
- [[Research/source-note]]: [what changed] — [conviction impact: unchanged/strengthened/weakened + 1 reason]
```

Max 2 lines. Log is an audit trail; analysis lives in the updated sections above.

### 3g: Accumulate manifest entries (in-memory until Checkpoint A)

For each thesis processed in Step 3:
- Tier A edit → append `(path, snapshot_path)` to `tier_a_thesis_snapshots`.
- Tier B only (Log append without snapshot) → append `(path, log_entry_text, reason)` to `tier_b_thesis_log_appends` where reason is `cross-thesis propagation | augmented target | other`.
- For each source research note triggering this propagation → append to `source_research_notes` (dedup at checkpoint time).

**Checkpoint A fires once at end of Step 3** — one Edit populating all three manifest sections from the accumulators.

---

## Step 4: Update Sector Notes

### 4.-1: Skill-origin gate

Consult `skill_origin_theses` from Step 2.5. A sector's "affected thesis set" is every changed thesis whose `sector:` frontmatter resolves to this sector (via `_graph.md` reverse index OR `_shared/sector-resolution.md` fallback).

**Gate rule**: skip Step 4 entirely for this sector ONLY IF BOTH conditions hold:
- **(i)** EVERY thesis in the affected set is in `skill_origin_theses`, AND
- **(ii)** this sector's path does NOT appear in any entry of `sector_targets_per_research_note` (computed at Step 1.2.5).

If either condition fails, proceed to Step 4.0. Log (skip path): `ℹ️ Skipped sector update [Sector Name] — all [N] affected thesis changes are skill-origin AND no co-changed research note resolves to this sector per Step 1.2.5.`

**Condition (ii) is NOT satisfied by thesis-target idempotency** (Step 1.7 Case 2a/2b/2c). Idempotent thesis propagation and empty sector target set are independent facts. The 2026-04-22 failure case collapsed them incorrectly — see §1.11.

**Mixed set**: at least one research-driven thesis OR research note resolves to sector → proceed per §4.2.

### 4.0: Per-source idempotency check

Before snapshotting, check if this sector already received propagation for the source research note today.

1. Read the sector's `## Related Research` section. Check for the source research note's wikilink (any of 5 forms per `_shared/wikilink-forms.md`).
   - Wikilink absent → first-time propagation; proceed to 4a + 4b.
   - Wikilink present → continue to step 2.
2. Read the sector's `## Log` section. Scan for `### YYYY-MM-DD` entry where `entry_date == today` AND entry references the source research note's wikilink.
   - Today-dated entry references this source → skip 4a + 4b. Log: `ℹ️ Skipped sector update [Sector Name] — Log already contains today's entry for [research-note] (likely propagated by earlier /sync TICKER in this session).`
   - No today-dated entry → propagation may have happened earlier; proceed normally (4b's deep-analysis gates the actual edit on real delta — §1.7, §1.8).

### 4a: Pre-Edit Snapshot

If edits modify existing analytical text (competitive dynamics, value chain, sector observations, comparison narratives), snapshot ALL Tier A sectors in one Bash block using background shell jobs + `wait`:

```bash
# For each sector in tier_a_sector_snapshots, fire cp in background:
cp "Sectors/Sector A.md" "_Archive/Snapshots/Sector A (pre-sync YYYY-MM-DD-HHMMSS).md" &
cp "Sectors/Sector B.md" "_Archive/Snapshots/Sector B (pre-sync YYYY-MM-DD-HHMMSS).md" &
wait
```

Then issue all frontmatter-addition Edits as a **single parallel tool-call batch**.

Add to each snapshot's frontmatter:
```yaml
snapshot_of: "[[Sectors/Sector Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: sync
snapshot_batch: sync-YYYY-MM-DD-HHMMSS
```

Skip snapshot if only adding wikilinks.

### 4b: Apply Updates

- Add new research notes to research listing.
- Update competitive dynamics if relative positioning changed.
- Update value chain analysis if supply chain relationships shifted.
- Revise sector-level observations if cross-company patterns emerged.
- Update company comparison tables with new data points.
- **Cross-thesis contradiction sweep (not just source-ticker additive).** Propagation defaults to strengthening the SOURCE ticker; force the peer question explicitly. For each OTHER Active Thesis in this sector, ask: does this research **validate or contradict** one of its named assumptions? A datapoint that is bullish for the source is often bearish for a peer (share gain = share loss elsewhere; a moat confirmed upstream = margin risk downstream). When the answer is "contradicts," the signal must SURVIVE the run — three concrete actions: (1) **accumulate** it as a tuple `(peer_ticker, named assumption, validates|contradicts, one-line mechanism)` in a running `cross_thesis_contradictions` list; (2) **append a Tier B Log entry on the peer thesis** (no snapshot — additive Log-only): `- Cross-thesis signal via [[Research/source note]]: [assumption] contradicted by [source ticker] evidence — [mechanism]. Review §Risks/§Bear Case.` (this is the only path by which propagation can ever weaken a thesis — without it /sync is structurally bull-additive); (3) **report** the full list as a `Cross-thesis contradictions:` line in the Step 8 report. If the sector's priced-in read shifted, ALSO update the sector's **`## Investor heuristics`** (what consensus believes / where it's wrong: the vault's stated edge). Do NOT silently leave peers stale because the research arrived under the source ticker.
- Update the `## Mental Models` section when new cross-company evidence activates or retires a sector-level model trigger, or changes its read — read the relevant `/Mental Models` files first and merge per `_shared/mental-models-section.md` (high selectivity; most syncs leave it untouched).
  - **Empty-scaffold exception (CHG-14)** — selectivity governs *populated* sections. If the `## Mental Models` section is still the unpopulated template scaffold (only the three `<!-- … -->` placeholder bullets) AND the run has qualifying content — a model trigger fired this run, OR existing sector-body content that plainly activates a model (e.g. a documented named layer-monopoly fires Value Layer Monopoly §1) — then first-population is MANDATORY (Tier B, no snapshot), NOT an "empty section → trivial delta → skip". That skip is exactly what left the ABF Substrates sector note scaffold-empty through 5 consecutive `/sync` runs. Normal selectivity (do not churn already-populated sections) is unchanged. Full rule: `_shared/mental-models-section.md` Selectivity step.

### 4c: Post-Edit Verification (Edit-return inspection — no re-read)

Inspect each Edit tool call's return value (the post-edit content snippet it emits). The Edit tool reports success iff the replacement landed, and the return value shows the new content; a separate re-read adds a round-trip without adding information. Verify each edited section from the Edit-return content:

1. Ends with complete sentence (not mid-word, unmatched `**`).
2. No incomplete table rows (line starts `|` but doesn't end `|`).
3. No trailing conjunction, preposition, comma, or opening bracket.

On failure: `⚠️ Sector note may contain a partial edit in [section]. Snapshot available: [[_Archive/Snapshots/...]]. Review manually or /rollback.`

Re-reads are only required if an Edit-return is genuinely ambiguous (e.g., the replacement context was truncated in the tool's response); in that case, issue a targeted section Read — not a full-file Read.

### 4d: Accumulate manifest entries

For each sector touched:
- Tier A (4a snapshot taken + 4b analytical edit) → `(path, snapshot_path)` to `tier_a_sector_snapshots`.
- Tier B (4b wikilink-only edit) → `path` to `tier_b_sector_appends`.

**Checkpoint B fires once at end of Step 4** — one Edit populating `## Sector notes touched`.

---

## Step 5: Update Macro Notes

### 5.-1: Skill-origin gate

Consult `skill_origin_theses`. A macro's "affected thesis set" is every changed thesis that wikilinks this macro (via `_graph.md` Macro reverse index OR Step 1.3 body-grep fallback).

**Gate rule**: skip Step 5 entirely for this macro ONLY IF BOTH conditions hold:
- **(i)** EVERY thesis in the affected set is in `skill_origin_theses`, AND
- **(ii)** this macro's path does NOT appear in any entry of `macro_targets_per_research_note` (computed at Step 1.2.5).

If either condition fails, proceed to Step 5.0. Log (skip path): `ℹ️ Skipped macro update [Macro Note] — all [N] affected thesis changes are skill-origin AND no co-changed research note resolves to this macro per Step 1.2.5.`

**Condition (ii) is NOT satisfied by thesis-target idempotency**. See §1.11 for the 2026-04-22 failure case that motivated the explicit Step 1.2.5 / lookup-based gate separation.

**Mixed set**: proceed normally.

### 5.0: Per-source idempotency check

Before snapshotting:

1. **Wikilink presence** — scan macro body for the source research note's wikilink.
   - Absent → first-time propagation; proceed to 5a + 5b.
   - Present → continue to step 2.
2. **Log section check** — if macro has `## Log`, scan for `### YYYY-MM-DD` entry with `entry_date == today` referencing the source.
   - Today-dated entry → skip 5a + 5b. Log: `ℹ️ Skipped macro update [Macro Note] — Log already contains today's entry for [research-note].`
   - No today-dated entry → skip step 3; proceed to 5a + 5b.
   - No `## Log` section → fall through to step 3.
3. **Mtime fallback** (only when step 2 reported no `## Log`): if wikilink present AND `mtime > .last_sync`, skip. Log: `ℹ️ Skipped macro update [Macro Note] — wikilink present and mtime > .last_sync (no Log section to confirm); likely propagated within current sync window. Forced re-propagation: /sync all or manual edit.`

See §1.10 for mtime fallback trade-offs.

### 5a: Pre-Edit Snapshot

If edits modify existing analytical text (scenario analysis, probability weightings, trading/allocation implications), snapshot ALL Tier A macro notes in one Bash block using background shell jobs + `wait`:

```bash
# For each macro in tier_a_macro_snapshots, fire cp in background:
cp "Macro & Technology/Note A.md" "_Archive/Snapshots/Note A (pre-sync YYYY-MM-DD-HHMMSS).md" &
cp "Macro & Technology/Note B.md" "_Archive/Snapshots/Note B (pre-sync YYYY-MM-DD-HHMMSS).md" &
wait
```

Then issue all frontmatter-addition Edits as a **single parallel tool-call batch**.

Add frontmatter to each snapshot:
```yaml
snapshot_of: "[[Macro & Technology/Note Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: sync
snapshot_batch: sync-YYYY-MM-DD-HHMMSS
```

Skip snapshot if only adding wikilinks.

### 5b: Apply Updates

- Assess macro-micro linkage: does new micro-level research validate, weaken, or complicate the macro framework?
- Update scenario analysis if new data changes probability weightings.
- Add wikilinks to new research.
- Revise trading/allocation implications if macro thesis shifted.

### 5c: Accumulate manifest entries

For each macro touched:
- Tier A → `(path, snapshot_path)` to `tier_a_macro_snapshots`.
- Tier B → `path` to `tier_b_macro_appends`.

**Checkpoint C fires once at end of Step 5**.

---

## Step 6: Update _hot.md (M5 — all-or-nothing atomicity)

Follow `.claude/skills/_shared/hot-md-contract.md` for all writes — compression, per-section budgets, truncation-marker avoidance, cap handling defined there.

If `_hot.md` does not exist, create with sections: `## Active Research Thread`, `## Latest Sync`, `## Sync Archive`, `## Recent Conviction Changes`, `## Open Questions`, `## Portfolio Snapshot`. Frontmatter: `date: YYYY-MM-DD`, `tags: [meta, hot-cache]`.

### M5 atomicity rule

**All-or-nothing**: either every planned section write lands, or none of them do. Prior spec wrote sections 1-6 sequentially then checked the hard cap — so a run hitting the hard cap left `_hot.md` with sections 1-3 updated and sections 4-6 at their prior (stale) state.

The M5-compliant order is: **read → stage in memory → pre-check cap → compress if needed → pre-check again → commit writes OR abort before any write**.

### 6.0: Read `_hot.md` into memory (non-destructive)

Read current file. Parse sections. Note the current word count of each of the 6 canonical sections.

### 6.1: Stage planned deltas per section (still non-destructive)

For each planned write, compute the **projected section text** in memory (do not Edit yet):
1. Update `date:` in frontmatter and heading.
2. **Active Research Thread** — same-ticker continuation: append dated line to existing thread. New topic: compress outgoing thread into `*Previous:*` entry (date + one-phrase summary); max 5 `*Previous:*` lines; drop oldest. See hot-md-contract.md §5.
3. **Latest Sync** — replace entirely. One bullet per thesis updated, max 1 line:
   ```
   - **[TICKER]**: [what changed] — [conviction impact]
   ```
4. **Sync Archive** — compress outgoing Latest Sync into a single summary line; prepend to Sync Archive. Max 3 entries.
5. **Open Questions** — two-stage:
   - **5a.** Mark resolved Outstanding Questions: if any resolved on theses during Step 3d, stage the update. If conviction triggers or drift flagged in Step 3e, stage the reassessment question.
   - **5b.** Auto-resolve `/catalyst` no-catalyst questions (§7.1). Scan staged `## Open Questions` for the `/catalyst`-emitted pattern:
     ```
     - [[TICKER]]: what catalyst in next 90 days could reignite this thesis? (flagged by /catalyst YYYY-MM-DD)
     ```
     For each match, resolve if the linked thesis now has a forward catalyst. Method:
     1. Extract TICKER from wikilink.
     2. Read `Theses/TICKER - *.md`'s `## Catalysts` section.
     3. Parse each catalyst entry for a date token (`YYYY-MM-DD`, `Q3 2026`, `October 2026`, `next [N] weeks/months`).
     4. Resolve to absolute date (use start of period for ranges).
     5. If ANY parsed date `>= today`, thesis has a forward catalyst → stage removal (or strikethrough) of the Open Question entry.
        - Default: drop the bullet in staged text.
        - Alternative (if `_hot.md` already shows `~~strikethrough~~ → Resolved` pattern): `- ~~[[TICKER]]: what catalyst...~~ → Resolved YYYY-MM-DD: forward catalyst now exists ([summary]).`
     
     Skip safety: past-dated catalysts only → question stays. Missing/unparseable `## Catalysts` → `ℹ️ Cannot auto-resolve /catalyst question for [TICKER] — Catalysts section missing or unparseable.` (emit to Step 8 report; do NOT stage a write that can't be computed cleanly).
     
     Report resolved tickers in Step 8 under `/catalyst Open Questions auto-resolved`.
6. **Recent Conviction Changes** — if triggers hit (Step 3e ⚡) or drift flagged (Step 3e ⚠️/📈), stage the entry.

### 6.2: Pre-check projected word count (no writes yet)

Compute `projected_total = sum(staged section word counts) + frontmatter + heading overhead`.

- `projected_total ≤ soft_cap (8000)`: proceed to 6.4 direct commit.
- `soft_cap < projected_total ≤ hard_cap (10000)`: proceed to 6.3 staged compression.
- `projected_total > hard_cap (10000)`: attempt 6.3 staged compression. If still over hard cap after full compression trigger order, **ABORT all `_hot.md` writes for this run** (§6.5) before any Edit lands. `/hot.md` retains its pre-run state. Report the abort in Step 8.

### 6.3: Staged compression (applied to staged text, not to the file)

Apply compression trigger order from `_shared/hot-md-contract.md` to the staged section buffers:
1. Drop oldest Sync Archive entry from staged Sync Archive.
2. Drop oldest `*Previous:*` line from staged Active Research Thread.
3. Merge duplicate Open Questions in staged Open Questions.
4. Drop staged Open Questions cohorts older than 14 days (compress each cohort to one-line pointer to thesis `## Outstanding Questions`).
5. Roster-compress staged Recent Conviction Changes entries older than 30 days (one-liner pointing to thesis `§Log + body`).
6. Aggressive RCC fallback (only if still over hard cap after step 5): progressively roster-compress oldest RCC entries (younger than 30 days) until under hard cap OR only the 5 most-recent entries remain verbatim.

After each step, recompute `projected_total`. Stop when under soft cap. If all six exhausted and `projected_total > hard_cap`, return to 6.2's abort path.

### 6.4: Commit all section writes (single composite Edit — M5 atomicity)

Only reached when `projected_total ≤ hard_cap`. The prior six-Edits form serialized the all-or-nothing commit into six dependent tool calls, any of which could fail mid-sequence and leave partial state. Per `.claude/skills/_shared/hot-md-contract.md` §5, section ORDER inside `_hot.md` is not load-bearing (no consumer reads sections in sequence). The commit therefore compresses to **one composite Edit** that replaces the entire post-frontmatter region with the staged content — a single tool-call round-trip instead of six, and true atomicity (the Edit either lands whole or does not land at all).

**Procedure**:
1. Construct the full post-frontmatter region in memory from the Step 6.1 staged section buffers:
   - Updated `date:` and main heading.
   - All six sections in canonical order: `## Active Research Thread`, `## Latest Sync`, `## Sync Archive`, `## Recent Conviction Changes`, `## Open Questions`, `## Portfolio Snapshot` (mirrors the `_hot.md` schema from CLAUDE.md Rule #9).
2. Anchor the single Edit on the closing frontmatter delimiter `---\n` plus the current post-frontmatter content:
   - `old_string` = the closing `---\n` followed by the CURRENT post-frontmatter content (captured at Step 6.0's Read).
   - `new_string` = the closing `---\n` followed by the STAGED post-frontmatter content.
3. Inspect the Edit-return content to confirm all six sections landed and the compression-trigger-order outputs (§6.3) are reflected.

If the composite Edit fails (rare — pre-checks at 6.2 should make this the pathological case only, and anchor uniqueness is guaranteed because the closing `---\n` appears exactly once in a well-formed file), report the failure and do NOT fall back to sequential Edits. `_hot.md` retains pre-run state; primary sync propagation in Steps 3-5 is unaffected. `/lint #35` catches any post-run schema drift; `/lint #42` catches truncation markers.

**Frontmatter-only update fast path**: if `date:` is the only field that changed between the read and the staged output (body sections all byte-identical after compression), skip the composite region Edit and issue a single targeted frontmatter Edit on the `date:` line. One-line Edits are cheaper than whole-region replacements when the body didn't actually change.

### 6.5: Hard-cap abort report

If 6.2/6.3 aborted before any write:

```
⚠️ _hot.md hard cap (10000 words) exceeded after all compression triggers — no _hot.md writes committed this /sync run.
   Current: [X] words. Projected with planned writes: [Y] words. Over cap by: [Z] words.
   
   Pre-run _hot.md state preserved. Resolution options:
     (a) Run /lint #42 to surface accumulated truncation/compression markers.
     (b) Manually compress _hot.md (drop oldest Sync Archive entries, *Previous:* lines).
     (c) Accept the session-context degradation for this run; primary sync propagation already succeeded.
```

Primary sync operation (Steps 3-5) remains valid; only `_hot.md` is skipped. Preserves the contract's principle: session-context degradation is tolerable; primary operation correctness is not.

---

## Step 7: Touch Watermark + Graph-Rebuild Marker

**Runs after ALL content writes (Steps 3-6) complete, before Step 7.5.**

### Ordering invariant (C4)

`.sync_all_fresh` writes BEFORE `.last_sync` touch. If either fails, this ordering preserves correctness:
- Marker write fails, watermark not yet advanced → next `/sync` re-reads everything (safe — wasted work but no missed rebuild).
- Marker wrote, watermark touch fails → `/graph` still forces full rebuild from marker; next `/sync` re-reads (safe — doubly covered).
- Reverse order would produce the failure path where watermark advances but marker absent → `/graph last` skips full rebuild → "no delta" theses unreconciled in `_graph.md` until next `/sync all`.

### Graph-rebuild marker — `/sync all` only (writes FIRST per C4 ordering)

Skip for `/sync` (default) and `/sync TICKER`. For `/sync all`:
```bash
touch .sync_all_fresh
```

`/graph` reads this marker at Watermark Resolution and forces full rebuild regardless of mode, then deletes the marker after a successful write. See §5.4.

### Mode-conditional watermark (writes AFTER marker per C4 ordering)

- **`/sync` / `/sync all`**: touch `.last_sync`. If prior marker write failed, watermark stays unset and next run re-processes.
  ```bash
  touch .last_sync
  ```
- **`/sync TICKER`**: do NOT touch (§6.1). Report `Watermark: untouched (ticker-scoped mode preserves baseline for next default /sync)`.
  - **First-run exception**: if `.last_sync` absent, create epoch placeholder:
    ```bash
    touch -t 197001010000 .last_sync
    ```
    Report `Watermark: epoch placeholder created`.

---

## Step 7.5: Finalize Sync Batch Manifest — Flip to completed

Mandatory for every mode when Step 2.9 skeleton was written. Skip only on pure no-op.

### 7.5a: Manifest path (from Step 2.9a)

Reuse the batch ID captured at Step 2.9a. Path:
```
_Archive/Snapshots/_sync-manifest (sync-YYYY-MM-DD-HHMMSS).md
```

### 7.5b: Flip status frontmatter

Edit manifest frontmatter:
- `status: in-progress` → `status: completed`
- Add `completed_date: YYYY-MM-DD`

Expected frontmatter post-flip:
```yaml
---
type: sync-manifest
batch: sync-YYYY-MM-DD-HHMMSS
mode: default | all | ticker-scoped
status: completed
date: YYYY-MM-DD
completed_date: YYYY-MM-DD
---
```

Phase checkpoints A/B/C have already populated the body. No body Edit at this step.

### 7.5c: Verify flip landed (Edit-return inspection — no re-read)

Inspect the 7.5b Edit tool call's return value. The Edit tool reports success iff the replacement landed; the return value shows the post-edit frontmatter snippet. Confirm from the Edit-return content:
- `status: completed` present
- `status: in-progress` absent
- `completed_date:` present and equals today

**On success**: proceed to Step 8.

**On verification failure** (Edit-return indicates the replacement did not produce the expected frontmatter, or the Edit tool returned an error): do NOT retry aggressively. Report `⚠️ Sync manifest status flip failed — manifest at [path] remains status: in-progress despite successful sync completion. /lint #41 will flag this as Important until manually resolved. Manual fix: edit the manifest and replace status: in-progress with status: completed (add completed_date: today).` Continue to Step 8.

### 7.5d: Tracking accumulators (implementation reference)

Throughout Steps 3-5, maintain in-memory accumulators flushed at phase checkpoints:

| Accumulator | Populated when | Flushed at |
|---|---|---|
| `tier_a_thesis_snapshots: [(path, snapshot_path)]` | Step 3c snapshot | Checkpoint A |
| `tier_b_thesis_log_appends: [(path, log_entry_text, reason)]` | Step 3f without snapshot | Checkpoint A |
| `source_research_notes: [path]` | Step 3 starts on a research note | Checkpoint A (dedup) |
| `tier_a_sector_snapshots: [(path, snapshot_path)]` | Step 4a snapshot | Checkpoint B |
| `tier_b_sector_appends: [(path)]` | Step 4b wikilink-only | Checkpoint B |
| `tier_a_macro_snapshots: [(path, snapshot_path)]` | Step 5a snapshot | Checkpoint C |
| `tier_b_macro_appends: [(path)]` | Step 5b wikilink-only | Checkpoint C |

If the run completes with all accumulators empty (pure no-op reached Step 3 but no edits landed): skip Step 7.5 entirely. In practice this is rare since Step 1 catches the pure no-op earlier.

### 7.5e: Lifecycle

The manifest is a non-snapshot artifact (`type: sync-manifest`, no `snapshot_date:`):
- `/clean` Step 2a's non-snapshot guard skips it for snapshot-age-based cleanup.
- `/lint #41` distinguishes three states: `status: in-progress` → Important; `status: completed` → ages per 90/180 day tiers; missing → no-op.
- Persists indefinitely until manually deleted OR `/lint #41` ages it out.

---

## Step 8: Report (T7.8 — emit only non-empty lines)

Produce a compact report. **Emit only lines with non-empty data.** Do NOT include "If none, omit this line" scaffold; if the field is empty, skip the line entirely. The LLM should inspect each field before deciding to write a line, not write a template and then prune.

**Always emitted**:
- **Mode**: `default` | `all` | `ticker-scoped`
- **Files read**: [count]
- **Files updated**: [count]
- **Watermark**: `touched (default/all)` | `untouched (ticker-scoped mode preserves baseline for next default /sync)` | `epoch placeholder created`
- **Final reminder**: `→ Run /graph last to update the dependency map. Recommended after every /sync.`

**Conditionally emitted** — include only if data is non-empty:

| Field | Emit when |
|---|---|
| `Snapshots created` | at least one Tier A snapshot (theses/sectors/macros) — list paths |
| `Thesis updates` | at least one thesis touched — one bullet per thesis: `[TICKER]: [sections] — [conviction impact]. Snapshot: [[...]] or N/A` |
| `Sector note updates` | at least one sector touched — one-line summary each |
| `Cross-thesis contradictions` | at least one Step 4b sweep tuple accumulated — list each as `[peer]: [assumption] [validates\|contradicts] via [source ticker] — [mechanism]` (Tier B peer Log entries were appended for contradicts) |
| `Macro note updates` | at least one macro touched — one-line summary each |
| `Deduplication skips` | at least one Step 1.7 wikilink-presence skip |
| `Sector skill-origin skips` | at least one Step 4.-1 skip |
| `Macro skill-origin skips` | at least one Step 5.-1 skip |
| `Skill-origin classified theses` | at least one thesis classified as skill-origin in Step 2.5 — list each as `[TICKER]: most-recent Log prefix "[prefix]" (sector/macro propagation skipped)`. The Step 2.5 **Body-change override** now actively catches the manual-edit-without-Log-entry case (CLAUDE.md Workflow Rule #6): if a skill-origin thesis's body changed outside `## Log` since last sync, the user was prompted mid-run and (on Y) it was reclassified research-driven — so a thesis remaining in this skill-origin list either had only Log-section changes (correct skip) or the user chose n at the prompt (or the no-git fallback found no prior snapshot to compare). For any surprise here, append a `Manual edit: ...` Log entry and re-run /sync. Also surface `Body-change overrides prompted: [tickers, Y/n each]` when the override fired. |
| `Log-history backfill skips` | at least one Case 2a skip (Step 1.7) |
| `Sector idempotency skips` | at least one Step 4.0 skip |
| `propagated_to: skips` | at least one Case 2b skip |
| `Terminal-skip notes` | at least one Case 2c (empty `propagated_to: []`) |
| `Augmented targets` | at least one augmented ticker |
| `propagated_to: updates` | at least one research note had its frontmatter updated |
| `propagated_to: update skipped` | at least one research note had an append-failure blocking atomic update |
| `Closed-status skips` | Step 1.5 caught a `status: closed` thesis still in `Theses/` |
| `Missing-file skips` | graph-referenced thesis missing from disk |
| `Unresolved research notes` | no propagation target found for at least one note |
| `Conviction triggers hit` | Step 3e ⚡ fired on at least one thesis |
| `Conviction drift flags raised` | Step 3e ⚠️/📈 fired |
| `/catalyst Open Questions auto-resolved` | Step 6 #5b resolved at least one |
| `New connections discovered` | at least one surprising link noted during analysis |

Final line (always): `→ Run /graph last to update the dependency map. Recommended after every /sync.`
