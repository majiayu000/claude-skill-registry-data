---
name: prune
description: Systematically evaluate weak, stale, or low-conviction theses for upgrade, monitoring, or closure. Use when user says "prune", "kill list", "clean up theses", "what should I close", or "reduce portfolio".
model: opus
effort: max
allowed-tools: Agent Read Grep Glob Edit Write WebSearch WebFetch Bash(date * find * wc * mv * cp * mkdir * rm * grep * cat * sort * printf *)
# WebSearch/WebFetch: Phase 3 CLOSE-rationale verification only (≤1 search per CLOSE candidate) — not open-ended research; the read-only analysis subagent inherits these.
---

Systematically evaluate the thesis portfolio; recommend keep / upgrade / kill. Be ruthless — cognitive overhead of tracking weak positions has a real cost.

Design rationale in `.claude/skills/prune/RATIONALE.md` (§N.M anchors).

## Execution context — split delegation (2026-07-08, MANDATORY)

`/prune` splits across the subagent boundary because it has a read-heavy analysis half (~42 full-thesis reads) and a mutation half gated by mandatory user approval. A subagent cannot obtain mid-run user confirmation, and destructive edits must stay in the main thread. So:

**ANALYSIS HALF — delegate to ONE `Agent` subagent** (`subagent_type: general-purpose`, `run_in_background: false`). The subagent runs **Phase 0.0.2 (rename-marker check) + Phase 0 (unsynced-research scan) + Phase 1–4** under a `read-only` lock (`.vault-lock.readonly` per preflight Procedure 1; it performs no writes). It reads every candidate thesis, does the two-pass triage and per-candidate assessment, and its final message returns EXACTLY:

> **Mental Models reading gate MUST cross the delegation boundary (MANDATORY — CLAUDE.md; `_shared/mental-models-section.md`).** The subagent does NOT inherit CLAUDE.md, so the agent prompt MUST embed this gate verbatim: *"Before judging any thesis for upgrade/monitor/close, read `Mental Models/Generalist - Overview.md` + the matching `Mental Models/Industry - X.md`/`Lens - X.md` for the candidates' sectors. Apply the READING PROTOCOL — a kill/keep call is a hypothesis; run the base-rate adversarially (stale ≠ wrong; a quiet thesis may still be right); read each candidate's own `## Mental Models` disconfirming check before recommending closure."*

1. A **pre-flight status**: either `PREFLIGHT-OK`, or `PREFLIGHT-BLOCKED: <rename-marker | first-run | unsynced-research>` with the details/file list the main thread needs to surface. **Override contract**: if the invoking prompt contains a line `PREFLIGHT_OVERRIDE: <unsynced-research | first-run> approved YYYY-MM-DD`, treat the corresponding Phase 0 gate as user-resolved — report the condition as a one-line warning (`⚠️ Phase 0.B: 145 unsynced files — proceeding under user override YYYY-MM-DD`) and CONTINUE to Phases 1–4 instead of returning PREFLIGHT-BLOCKED. (`rename-marker` is NEVER overridable — it is a hard-block per preflight Procedure 2.)

**Recursion guard — the agent prompt MUST also embed verbatim:** *"You are the EXECUTOR of this analysis run, not a coordinator: do NOT re-delegate any part of this work to further Agent calls. Perform all reads and analysis yourself and end your final message with the three return items."*
2. The full **Phase 4 report** (Recommendation Table + Portfolio Stats + Attention Allocation) — rendered verbatim by the main thread.
3. A compact **execution plan** the mutation half consumes without re-deriving analysis:
   - `closures:` list of `(ticker, filename, conviction_at_closure, one-line rationale)`
   - `upgrades:` list of `(ticker, filename, old→new conviction, justification, Log line)`
   - `affected_sectors:` list of `(sector_note_path, match_confidence, log_message)` from `_shared/sector-resolution.md`
   The subagent releases its read-only lock before returning.

**MUTATION HALF — main thread only.** The main thread:
- If the subagent returned `PREFLIGHT-BLOCKED`, surface the corresponding Phase 0.0.2 / Phase 0.A / Phase 0.B prompt and get user resolution. **On "proceed anyway" approval for `unsynced-research` or `first-run`**: re-invoke the analysis subagent with the SAME prompt plus the line `PREFLIGHT_OVERRIDE: <condition> approved YYYY-MM-DD` — the override crosses the delegation boundary and the fresh subagent proceeds past that gate (this closes the dead end where approval changed no vault state and the re-invoked subagent re-blocked on the same condition forever). For `rename-marker`, there is no override — the user must finish/repair the rename first, then re-invoke normally.
- Render the Phase 4 report verbatim, then run the **Phase 5 approval gate** and the entire Phase 5 Atomic Batch (Stages 1–5) **exactly as specified below — unchanged**. Acquire the `vault-wide` write lock here (Phase 0.0.1), at the start of Phase 5, not before. Re-read only the approved-for-mutation theses + affected sector notes (bounded set — never the full portfolio) before editing them, per the read-before-write rule.

**Why the lock moves**: the long read phase now runs under a read-only lock inside the subagent (narrower, non-blocking to other readers); the vault-wide write lock is held only for the short mutation window in the main thread. All Phase 5 snapshot/manifest/graph-invalidation/`_hot.md` machinery is untouched. **Why not full delegation**: the Phase 5 approval gate and destructive edits require the main thread. **Why not frontmatter `context: fork`**: that mechanism was reverted 2026-06-07 (unrendered-stdout blank panel); Agent-tool delegation returns the report as a tool result the main thread re-emits. Revert path: delete this section; the skill then runs entirely inline (report renders, ~42 reads land in main context).

## Scope Resolution

Parse `$ARGUMENTS`. Arguments can combine (e.g., `/prune semiconductors stale`):

- **Sector** (e.g., `semiconductors`): evaluate theses with matching `sector:` frontmatter only.
- **Flag filter** (pre-filters before full reads):
  - `stale` → last Log entry >60 days old
  - `low` → `conviction: low`
  - `draft` → `status: draft`
  - `monitoring` → `status: monitoring`
- **No arguments / empty**: evaluate all theses.

Pre-filtering grep on frontmatter avoids loading 39+ files when only a subset matches.

## Phase 0.0: Pre-flight

### 0.0.1: Acquire vault lock

**Under split delegation (see Execution context):** the analysis subagent holds a `read-only` lock (`.vault-lock.readonly`) for Phase 0.0.2 + Phase 0 + Phase 1–4; the **main thread** acquires the `vault-wide` write lock here at the **start of Phase 5**, immediately before the first destructive stage, and releases it in the final Phase 5 block. (Inline-fallback mode without delegation: acquire the `vault-wide` lock at the very start as the original single-lock flow.)

`vault-wide` scope per `.claude/skills/_shared/preflight.md` Procedure 1. Timeout 15 min (large portfolios are slow). Capture token, verify (Procedure 1.5) every block, release in final.

### 0.0.2: Vault-wide rename marker check (§8)

Glob `.rename_incomplete.*`. ANY marker → hard-block (all-or-nothing — §8.1):

```
❌ In-flight rename repair detected — /prune would compound split state.

Markers found:
  - .rename_incomplete.TICKER1 ([new_name from marker])
  - ...

/prune closes, upgrades, and reshapes sector notes — each operation keyed to
the CURRENT thesis filename. Any affected thesis mid-rename would leave
inbound references split across old and new names.

Complete or abandon all in-flight renames first:
  /rename TICKER "[new_name]"    # per marker
  OR
  rm .rename_incomplete.TICKER   # accept broken wikilinks
```

Wait for user resolution. Do NOT proceed.

## Phase 0: Check for Unsynced Research (§7)

Three states based on `.last_sync` and `find -newer` outcome:

### Phase 0.A: `.last_sync` absent — first-run state (B4 fix)

If `.last_sync` does not exist at vault root, the next `/sync` will treat the entire vault as first-run (epoch placeholder, every file matches `find -newer`). Proceeding with `/prune` in this state means closures/upgrades are evaluated against thesis state that may not yet reflect the most recent research notes. Hard-prompt before continuing:

```
⚠️ First-run state detected — .last_sync is absent at vault root.

The vault has either never been synced, or .last_sync was deleted (manually,
accidentally, or via `git restore` that wiped it). The next /sync (any mode)
will treat this as a first-run and re-process every file in the vault.

/prune evaluates closure candidates by reading thesis state directly, but the
thesis state in a first-run vault may not yet reflect insights from research
notes that haven't propagated yet. Running /prune now risks closing or
upgrading theses based on incomplete evidence.

Recommended: run /sync first to establish the watermark and propagate any
pending research, then re-run /prune.

Options:
  (a) Cancel — exit /prune. Run /sync, then re-invoke /prune.
  (b) Proceed anyway — accept the risk that recommendations may not reflect
      the latest research. Use only if you have already verified that no
      research notes are awaiting propagation.

Confirm (a/b):
```

**Do NOT proceed without explicit user confirmation.** Decline → exit and suggest `/sync`. Approve → continue to Phase 0.B (which will report no changed files since the watermark is missing).

### Phase 0.B: `.last_sync` present — unsynced-research scan

```bash
find Research/ Theses/ "Macro & Technology/" Sectors/ -newer .last_sync -name '*.md' 2>/dev/null
```

Changed files found → warn before proceeding:
```
⚠️ Unsynced research detected ([N] files modified since last /sync):
  [list]

Running /prune before /sync risks archiving theses before recent research insights
have been propagated. Recommended: run /sync first, then re-run /prune.

Proceed anyway? (y/n)
```

**Do NOT proceed without explicit user confirmation.** Decline → stop and suggest `/sync`.

## Phase 1: Identify Candidates (Two-Pass Triage — §6)

**If scoped**: read only matching theses in full (typically small — skip two-pass triage).

**If unscoped — Pass 1 lightweight scan (parallel full Reads)**:

**Issue all thesis Reads as a single parallel tool-call batch** — one message with ~42 Read invocations, all in full, landing in one round-trip. Do NOT serialize, and do NOT section-target at the tool level. The LLM sees every thesis body in full so subtle weakness signals outside the triage sections (e.g., a contradiction between Bull Case and recent Log entries, a Non-consensus Insight that's been quietly invalidated by newer research) aren't filtered out before the triage LLM reasons over them.

Triage focus prioritizes **frontmatter + Related Research + Catalysts + Log** (the mechanical flag inputs), but full-file context is kept intentionally — `/prune` is about spotting quietly-dead theses, which sometimes requires reading between the sections.

Apply flag criteria:

| Flag | Criteria | Source |
|------|----------|--------|
| 🟡 Low conviction | `conviction: low` | frontmatter |
| 🟡 Monitoring | `status: monitoring` | frontmatter |
| 🔴 Stale | Last Log >60 days old | Log dates |
| 🔴 Very stale | Last Log >120 days old | Log dates |
| 🟡 Thin research | <3 research notes linked | Related Research |
| 🟡 Draft limbo | `status: draft` with only 1 Log entry | frontmatter + Log count |
| 🟡 Orphaned from sector | Not in Sector Note | deferred to Pass 2 |
| 🔴 No catalyst | Catalysts empty or all dates past | Catalysts section |

Also flag: high-conviction theses with stale research (last Log >90 days despite `conviction: high`).

**Pass 2 — deep read flagged candidates**:
- Each flagged → proceed to Phase 2 (full note read).
- Each unflagged → check orphaned-from-sector by cross-referencing ticker vs Sector Note's Active Theses. If flag triggers, add to set.
- Unflagged theses passing all checks → excluded from Phase 2 entirely.

Typically reduces full reads from ~40 to 10-20.

Flag additionally during Pass 2:
- High-conviction theses whose Sector Note has been significantly updated but the thesis Log hasn't reflected it

## Phase 2: Assess Each Candidate

For each flagged thesis, read full note + supporting research. Assess:

1. **Evidence trajectory**: strengthening / weakening / going stale since creation?
2. **Thesis integrity**: does the original non-consensus insight still hold? Has the market moved toward or away?
3. **Opportunity cost**: is research time here coming at the expense of higher-conviction ideas?
4. **Catalyst horizon**: specific upcoming event that could reignite?
5. **Vault connectivity**: well-connected (wikilinks, sector, macro) or isolated bet?

## Phase 3: Recommendation

Per candidate, recommend ONE:

### ⬆️ UPGRADE
- Evidence quietly strengthened; recent research/sector developments support thesis but haven't been reflected in conviction.
- Specify: new conviction level, what justifies it, Log entry to add.

### ➡️ KEEP MONITORING
- Still valid but needs specific trigger to become actionable.
- Specify: exact trigger (falsifiable + time-bounded), review date (downgrade to CLOSE if trigger hasn't fired).

### ⬇️ CLOSE
- Evidence weakened, insight absorbed by consensus, no catalyst, or never properly developed.
- Specify: one-line rationale. Offer to move to _Archive/ with final Log entry.
- **"Absorbed by consensus" closures require an external check** — the analysis subagent runs ≤1 WebSearch per CLOSE candidate for 1–2 recent datapoints (analyst note / news item) showing the market now holds the once-non-consensus view. None found → tag the recommendation `[unverified: absorbed-by-consensus claim not externally checked]`; the tag MUST carry into the Phase 4 Rationale cell and the Phase 5 approval prompt so the user archives with eyes open. Staleness ≠ wrong: a quiet thesis is not a disproven one — do not close on absorption grounds without the datapoint or the tag.

## Phase 4: Portfolio Health Summary

### Recommendation Table

**⚡ Most urgent:** [single highest-priority action — e.g. `CLOSE TICKER — reason`, or `none this run`]

| Ticker | Company | Status | Conviction | Flag(s) | Recommendation | Model trigger | Rationale |
|---|---|---|---|---|---|---|---|
| | | | | | ⬆️/➡️/⬇️ | [G-#] / Industry # / Lens § / none | [one line] |

*Model trigger* — the mental-model trigger behind the keep/upgrade/close call, cited by stable ID (`[G-10]`, `Semis #2`, `VLM §2`) or `none`; one short ID per recommendation, binding the mandatory Mental-Models read to the deliverable. CLOSE-on-consensus → usually base-rate/outside-view `[G-10]` or a Value-Layer-Monopoly kill-criterion; KEEP MONITORING → the trigger keeping the thesis alive.

### Portfolio Stats
- Total theses: X
- Active / Draft / Monitoring: X / X / X
- Flagged for review: X
- Recommended closures: X
- Recommended upgrades: X
- Average thesis age (days since last Log): X
- Theses with no catalyst: X

### Attention Allocation Insight (§9)
- What % of theses are high-conviction? Appropriate or should more be pruned?
- Sectors with too many thin theses needing consolidation?
- Which 3 theses deserve MORE research time (conviction + evidence strength)?

## Phase 5: Execute (WITH USER APPROVAL) — Atomic Batch

**Do NOT auto-execute. Present table; wait for user confirmation.**

Atomic batch pattern (§1): all safety snapshots created BEFORE any destructive modifications. Five sequential stages — each completes fully before the next begins.

### Stage 1: Write Batch Manifest Skeleton (C2 — manifest BEFORE any snapshot/destructive op; §2)

**Why manifest-first** (C2, invariant #11): if `/prune` crashes between Stage 1 snapshots and Stage 1.5 manifest (prior order), per-thesis pre-closure snapshots exist on disk with `snapshot_trigger: prune` but no matching manifest. `/clean` Step 2d 30-day closure floor requires a matching manifest to detect — without it, snapshots fall through to "standard orphan" and can be deleted via `/clean orphans` the same day. Writing the manifest FIRST binds any subsequent snapshot to the batch ID; closure-floor protection is unbypassable from that moment.

Generate single batch ID for entire prune run:
```bash
HHMMSS=$(date +%H%M%S)
mkdir -p _Archive/Snapshots
```

`prune-YYYY-MM-DD-$HHMMSS` = `snapshot_batch` for ALL snapshots (written in Stage 1.5) and matching `batch:` field in the manifest.

**Pre-resolve affected sector notes** (read-only, destructive-safe): for each approved thesis `sector:`, resolve via `.claude/skills/_shared/sector-resolution.md`. Dedup. Collect the list of `(sector_note_path, match_confidence, log_message)` tuples. This resolution is needed for the skeleton's `## Affected Sector Notes` section and reused by Stage 1.5 snapshots + Stage 4 edits. `match_confidence: none` skipped from sector updates (Stage 4) and sector snapshots (Stage 1.5).

Write `_Archive/Snapshots/_prune-manifest (prune-YYYY-MM-DD-HHMMSS).md`:

```yaml
---
type: prune-manifest
batch: prune-YYYY-MM-DD-HHMMSS
status: in-progress
date: YYYY-MM-DD
---
```

Body:
```markdown
# Prune Batch Manifest

> **If `status: in-progress`**, `/prune` did not complete successfully.
> Recovery: `/rollback [any ticker below]` → select `(pre-prune)` → cascade (a).
> Then delete this manifest and re-run `/prune`.
>
> **If `status: completed`**, prune finished but Stage 5 cleanup didn't. Safe to delete
> manually. `/clean` and `/lint #36` also surface these.

## Intended Closures
- TICKER1 - Company1
- TICKER2 - Company2

## Intended Upgrades
- TICKER3 - Company3 (conviction low → medium)

## Affected Sector Notes
- Sector Name (closures: TICKER1, TICKER2; upgrades: TICKER3)

## Downstream Content Propagation (Stage 4.2 targets)
- Neighbor theses receiving closure-notification Log entries: *(populated at Stage 4.5 after Stage 2 neighbor scans complete — C1)*
- Macro notes referencing closed theses (reported only): *(populated at Stage 4.5 after 4.2a scan)*
```

Skeleton write failure → hard abort Stage 5 before any snapshot. Report to user; no destructive edits have run yet. `/clean`'s closure-snapshot 30-day floor is trivially unbypassable when there are no snapshots yet.

Flipped to `completed` then retained at Stage 5 (§3). Body's Downstream Content Propagation section populated at Stage 4.5 with the deduplicated neighbor list (C1 fix — prior spec left placeholders unfilled, breaking `/rollback` Step 6.2.5 Tier B surfacing).

### Stage 1.5: Snapshot ALL Affected Files (C2 — after manifest skeleton lands)

Reuse HHMMSS from Stage 1. All snapshots bound to the already-existing manifest via `snapshot_batch: prune-YYYY-MM-DD-HHMMSS` — they inherit the 30-day closure-floor protection from Stage 1's manifest even if Stage 1.5 crashes mid-snapshot (invariant #11).

**Thesis snapshots** — one per approved closure AND per approved upgrade. Issue ALL `cp` calls in ONE Bash block using background shell jobs + `wait` (mirrors `/compare` Phase 5.5a and `/rollback` Step 4 patterns — a 5-closure batch is 5 sequential `cp` rounds without this; one round-trip with it):

```bash
mkdir -p _Archive/Snapshots
# Per approved closure/upgrade, fire cp in background:
cp "Theses/TICKER1 - Name1.md" "_Archive/Snapshots/TICKER1 - Name1 (pre-prune YYYY-MM-DD-HHMMSS).md" &
cp "Theses/TICKER2 - Name2.md" "_Archive/Snapshots/TICKER2 - Name2 (pre-prune YYYY-MM-DD-HHMMSS).md" &
cp "Theses/TICKER3 - Name3.md" "_Archive/Snapshots/TICKER3 - Name3 (pre-prune YYYY-MM-DD-HHMMSS).md" &
wait
# Check exit status of all background jobs before proceeding to frontmatter Edits
```

Then issue all frontmatter-addition Edits as a **single parallel tool-call batch** (one Edit per snapshot, all in the same message):

```yaml
snapshot_of: "[[Theses/TICKER - Company Name]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: prune
snapshot_batch: prune-YYYY-MM-DD-HHMMSS
```

**Sector note snapshots** — use the `(sector_note_path, match_confidence, log_message)` tuples resolved in Stage 1. Dedup, then snapshot each unique sector note in the SAME background-jobs Bash block as the thesis snapshots above (one `wait` for all snapshots across both categories). Frontmatter (`snapshot_trigger: prune`, same batch ID).

`match_confidence: none` → skipped from snapshot and from Stage 4 sector update per Stage 1 resolution. `normalized`/`substring` → `log_message` collected for final report.

**Abort gate** (§1.3): snapshot creation fails → STOP immediately. Report `❌ Snapshot failed for [file]. Prune aborted — no downstream mutations. Fix the issue and re-run /prune.` Manifest skeleton persists with `status: in-progress`; `/lint #36` surfaces. User can `rm` the manifest manually after resolving the failure.

### Stage 2: Process ALL Thesis Closures

**Neighbor-grep batch (parallel)**: before iterating closures, issue ALL neighbor greps in ONE parallel tool-call batch — one Grep per closure, all in the same message. Each Grep uses the wikilink patterns below against `Theses/` (excluding the thesis being archived). Alternatively (fewer tool calls), issue a single Grep with alternation across all closure filenames:

```
Grep pattern='\[\[(Theses/)?(TICKER1 - Name1|TICKER2 - Name2|TICKER3 - Name3)(\.md)?(#[^\]|]+)?(\|[^\]]+)?\]\]' path='Theses/' glob='*.md' output_mode='content' -n
```

For a 5-closure batch this is 1-5 Greps in one round-trip instead of 5 sequential rounds. Partition the combined results per closure (by which filename alternation branch matched each line) in the reasoning layer.

For each approved closure:
1. Append final Log entry: `### YYYY-MM-DD\n- CLOSED: [rationale]. Archived.`
2. Change frontmatter: `status: closed`.
3. **Record neighbor list for graph invalidation** (from the parallel batch above — no additional Grep per closure). Wikilink patterns covered by the batch:
   - `[[Theses/TICKER - Name]]`, `[[Theses/TICKER - Name|...]]`, `[[Theses/TICKER - Name#...]]`, `[[Theses/TICKER - Name.md]]`
   - `[[TICKER - Name]]`, `[[TICKER - Name|...]]`, `[[TICKER - Name#...]]`
   
   Dedup per closure → that closure's neighbor set.
4. Move file:
   ```bash
   mv "Theses/TICKER - Company Name.md" "_Archive/TICKER - Company Name.md"
   ```
5. **Archive-ticker registry** (supports `/thesis` Signal C): append to `.archive_ticker_registry.md` at vault root. Create with header on first write:

   ```bash
   REGISTRY=".archive_ticker_registry.md"
   if [ ! -f "$REGISTRY" ]; then
     cat > "$REGISTRY" <<'HEADER'
   ---
   type: archive-ticker-registry
   purpose: Flat append-only log of thesis archival events. Consumed by /thesis Step 1.2 Signal C (multi-signal archive-collision check).
   ---
   
   # Archive Ticker Registry
   
   HEADER
   fi
   printf '%s|%s|%s|%s|%s\n' \
     "$TICKER" "$ARCHIVED_FILENAME" "$(date +%Y-%m-%d)" \
     "$CONVICTION_AT_CLOSURE" "$CLOSURE_RATIONALE_LINE" \
     >> "$REGISTRY"
   ```
   
   Registry append failure does not abort — log warning and continue.

Do NOT update sector notes here (batched in Stage 4). Do NOT write `.graph_invalidations` per-closure (batched in Stage 4.5 — §5.1).

**Closure mid-stage failure**: report completed/failed/pending. Pre-prune snapshots available. Manifest persists.
```
⚠️ Closure failed for [TICKER] at step [N]. Completed: [list]. Failed: [list]. Pending: [list].
All pre-prune snapshots available (batch: prune-YYYY-MM-DD-HHMMSS).
Batch manifest: [[_Archive/Snapshots/_prune-manifest (prune-YYYY-MM-DD-HHMMSS)]]
To recover: /rollback [any affected ticker] → select (pre-prune) → cascade (a) to restore all.
Sector notes have NOT been modified — no sector inconsistency from this partial failure.
After recovery, delete the batch manifest.
```

Session crash (no error): manifest persists with embedded recovery instructions. `/lint #36` surfaces.

### Stage 3: Process ALL Upgrades

For each approved upgrade:
1. Update `conviction:` in frontmatter.
2. Append Log entry (max 2 lines):
   ```
   ### YYYY-MM-DD
   - Prune upgrade [old] → [new]: [what justified] — conviction strengthened, [reason]
   ```
   Prefix `"Prune upgrade"` — `/sync` Step 2.5 skill-origin classification (registry §9).

### Stage 4: Update ALL Sector Notes

Per affected sector note (identified in Stage 1):
1. Read current sector note.
2. **Closures**: remove archived theses from Active Theses. If `## Closed/Archived` section exists, add them there.
3. **Upgrades**: if sector note displays conviction alongside thesis links, update to reflect new levels.

Do NOT rewrite wikilinks across the vault in this stage. Downstream content propagation (Stage 4.2) is append-only.

Graph update deferred: `_graph.md` owned exclusively by `/graph`. Run `/graph last` after this skill.

### Stage 4.2: Propagate Closures to Downstream Content (closures only)

Skip if Stage 2 processed zero closures. Neighbor thesis sets from Stage 2 step 3 reused here (§4.1).

#### 4.2a: Identify downstream files per closure

For each closed thesis, two target groups:
1. **Cross-referencing theses**: already collected in Stage 2 step 3.
2. **Macro notes**: grep `Macro & Technology/*.md` for same wikilink patterns used in Stage 2 step 3.

Exclude `_Archive/`, `_Archive/Snapshots/`, `_Inbox/processed/`, `.git/` from both scans.

#### 4.2b: Append closure-notification Log entry to affected theses

Per neighbor thesis from 4.2a step 1, append single dated Log entry:

```
### YYYY-MM-DD
- Cross-thesis closure: [[_Archive/CLOSED_TICKER - Company Name]] archived — [one-line rationale]. Cross-thesis and Related Research wikilinks retained; review body prose if thesis impact has changed.
```

Rules (§4.2-§4.5):
- **One Log entry per affected thesis** regardless of closure count. Multi-closure case: `Cross-thesis closures: [[_Archive/TICKER1 - ...]], [[_Archive/TICKER2 - ...]], [[_Archive/TICKER3 - ...]] archived this run — ...`
- **Max 2 lines per CLAUDE.md Writing Standards**. Collapse long lists: `... and 2 more — see /prune output`.
- **Archive-path wikilinks**: `[[_Archive/TICKER - Company Name]]` (§4.3 — Obsidian resolves natively; no broken-link display).
- **Do NOT modify body prose** — Log annotation is the notification; user reviews body at their pace.
- **Do NOT snapshot for 4.2b** — Tier B append-only (§4.2). Append failure → thesis unchanged.

Prefix `"Cross-thesis closure:"` / `"Cross-thesis closures:"` — `/sync` Step 2.5 skill-origin + Step 3e drift exclusion (registry §13).

Append failure → log + continue. Report failures in Stage 5 summary.

#### 4.2c: Macro note handling — detect and report only (§4.4)

Auto-editing narrative prose can destroy analytical coherence. For each macro note from 4.2a step 2:
- Do NOT edit the file.
- Collect `(macro note path, affected-thesis list)` pairs for Stage 5 report.
- Surface:
  ```
  ⚠️ Macro references to closed theses — review manually:
    - [[Macro & Technology/Iran conflict — Transmission Map]] references [[CLOSED_TICKER1 - ...]] (now archived)
    - [[Macro & Technology/AI capex cycle]] references [[CLOSED_TICKER1 - ...]], [[CLOSED_TICKER2 - ...]] (now archived)
  ```

User decides per macro note: (a) rewrite prose, (b) leave as historical, (c) strikethrough/annotate.

#### 4.2d: Stage report fields

Include in Stage 5 report:
- **Cross-thesis Log annotations**: `[N] neighbor theses received closure-notification entries: [list]. [M] Edit failures: [list with reason].`
- **Macro notes referencing closures**: `[N] macro notes contain wikilinks to archived theses — manual review: [list pairs].`

### Stage 4.5: Write Graph Invalidation List + Populate Manifest Neighbor List (closures only; C1 + §5.1)

Skip if Stage 2 processed zero closures. For closure runs, this stage performs two related writes:

**(1) Write `.graph_invalidations`** — merge every closure's neighbor set (from Stage 2 step 3) into one deduplicated list, append to `.graph_invalidations`:

```bash
{
  [ -f .graph_invalidations ] && cat .graph_invalidations
  # Deduplicated union of Stage 2 neighbor sets (all closures):
  printf '%s\n' "Theses/NEIGHBOR1 - ...md" "Theses/NEIGHBOR2 - ...md" ...
} | sort -u > .graph_invalidations.tmp && mv .graph_invalidations.tmp .graph_invalidations
```

Batched once per prune run — not per-closure.

Write failure → report, do NOT abort (§5.2). Closures/upgrades/sector updates already succeeded. `⚠️ .graph_invalidations write failed — run /graph (full rebuild) instead of /graph last to clean stale cross-thesis refs.`

**(2) Populate manifest body neighbor list (C1 — makes `/rollback` Step 6.2.5 Tier B surfacing work)**: Edit the Phase 1 manifest skeleton, replacing the `*(populated at Stage 4.5 ...)*` placeholders under `## Downstream Content Propagation` with the actual deduplicated values:

```markdown
## Downstream Content Propagation (Stage 4.2 targets)
- Neighbor theses receiving closure-notification Log entries:
  - [[Theses/NEIGHBOR1 - Company1]] (appended: succeeded | failed reason)
  - [[Theses/NEIGHBOR2 - Company2]] (appended: succeeded)
  - ...
- Macro notes referencing closed theses (reported only, not edited):
  - [[Macro & Technology/Example Macro Note]] — references [[_Archive/CLOSED_TICKER1 - ...]], [[_Archive/CLOSED_TICKER2 - ...]]
  - ...
```

Sources for the populated list:
- Neighbor theses: union of Stage 2 step 3 per-closure neighbor sets, paired with Stage 4.2b's per-neighbor append outcome (succeeded | failed reason).
- Macro notes: output of Stage 4.2a step 2 grep + 4.2c surface-only report (no edits applied).

Manifest body Edit failure → log warning, continue. The `.graph_invalidations` write already succeeded; the missing neighbor list only affects `/rollback` Step 6.2.5's ability to surface Tier B entries automatically — user can fall back to manual grep via the `Cross-thesis closure:` prefix. `/lint #36` will flag the placeholder survival as Nice to Have.

**Why this matters**: prior spec left the placeholder strings in the manifest body. `/rollback` Step 6.2.5 reading the manifest would surface literal text `*(populated at Stage 4.5 ...)*` to the user instead of real ticker names — breaking the documented Tier B review flow. Populating the placeholder closes that gap.

### _hot.md update

Per `.claude/skills/_shared/hot-md-contract.md` (do NOT touch Latest Sync / Sync Archive):

1. **Active Research Thread**: same-ticker continuation per contract. Write: `pruned portfolio — [N] closed, [N] upgraded, [next step]`.
2. **Recent Conviction Changes**: per-upgrade and per-closure entries. **Never compressed** per contract.
3. **Open Questions**: remove questions related to closed theses. Add new questions raised by upgrades.
4. **Portfolio Snapshot**: update conviction-level counts + sector coverage if materially changed.

Word cap: after edits, check total. Over 8,000 (soft cap per `_shared/hot-md-contract.md`) → prune `## Sync Archive` (oldest first) then `*Previous:*` lines. Abort if over 10,000 hard cap.

### Stage 5: Manifest Retention (§3 — 30-day regret window)

All stages complete. `/prune` **retains** the manifest (§3.2 — changed from prior delete-at-completion behavior):

1. **Flip manifest status**: Edit frontmatter — `status: in-progress` → `status: completed`. Add `completed_date: YYYY-MM-DD`.

2. **Verify flip landed** (Edit-return inspection — no re-read): inspect the frontmatter-flip Edit's return value. The Edit tool reports success iff the replacement landed; the returned snippet shows the post-edit frontmatter. Confirm `status: completed` present, `status: in-progress` absent from the Edit-return content.
   - **Success** → manifest stays in `_Archive/Snapshots/` with `status: completed`. `/clean` + `/lint #36` handle aging.
   - **Verification failure** (§3.4 — Edit-return indicates replacement did not produce expected frontmatter, or Edit tool returned error): do NOT attempt repair. Report:
     ```
     ❌ Manifest status flip failed: [[_Archive/Snapshots/_prune-manifest (prune-YYYY-MM-DD-HHMMSS)]] is still marked in-progress despite successful prune completion.
     
     DO NOT run /rollback — the prune closures/upgrades/sector updates/downstream propagation have all succeeded; rolling back would undo valid work.
     
     Manual fix: open the manifest and replace status: in-progress with status: completed. The manifest will then age out via /clean after 30 days. /lint #36 flagging it as Critical is a false alarm in this specific case.
     ```
     Exit.

3. **NO deletion step.** Manifest persists until `/clean` removes it (30 days after `completed_date:`) or user `rm`s manually.

### Retention policy

- **Days 0-30 after `completed_date:`**: manifest stays. `/rollback` cascade can find batch and surface Tier B Log entries for neighbor review during regret-recovery. `/lint #36` Pass.
- **Days 30+**: `/clean` (any mode) removes via Step 2a extension. `/lint #36` Nice to Have.

**User regret-recovery flow**:
```
User realizes approved /prune closure was wrong.
If `completed_date:` within 30 days:
  /rollback [any ticker from manifest's Intended Closures]
  → select (pre-prune) snapshot → cascade (a) to restore all files
  → /rollback Step 6.2.5 surfaces neighbor Tier B Log entries for strikethrough review
  → delete manifest manually after recovery: rm "_Archive/Snapshots/_prune-manifest..."
```

## Stage 5 Final Report

- **Closures completed**: [N] (list with rationales)
- **Upgrades completed**: [N] (list with old → new)
- **Sector notes updated**: [list]
- **Cross-thesis Log annotations**: `[N] neighbors received closure-notification entries: [list]. [M] Edit failures: [list with reason].`
- **Macro notes referencing closures**: `[N] macros contain wikilinks to archived theses — manual review: [list pairs].`
- **Graph invalidation**: `[N] neighbors queued in .graph_invalidations` | `no neighbors` | `write failed — recommend /graph (full)`
- **Manifest state**: `completed — retained for 30-day regret-recovery window` | `⚠️ flip verification failed — do NOT /rollback, resolve manually per warning above`
- **Graph reminder**: `→ Run /graph last to update the dependency map.` (Closure runs require this to clear stale cross-thesis refs.)
- **Sector resolution logs** (if `normalized` or `substring`): list contract's `log_message` entries.
