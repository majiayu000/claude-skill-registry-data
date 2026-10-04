---
name: rename
description: Rename a thesis file when company name changes. Atomically updates filename, all inbound wikilinks across the vault, graph adjacency entry header, sector note Active Theses entry, snapshot snapshot_of references, and _hot.md mentions. Use when company changes name (FB → META, Square → Block, etc.), or when correcting a typo in a thesis filename.
model: sonnet
effort: max
allowed-tools: Read Grep Glob Edit Write Bash(date * mv * cp * mkdir * find * grep *)
---

Rename a thesis file when the company name portion changes. **TICKER does NOT change** — only the segment after ` - `. Example: `Theses/META - Meta.md` → `Theses/META - Meta Platforms.md`.

Without `/rename`, manual file renames break: (a) every inbound wikilink across the vault, (b) `_graph.md`'s adjacency header, (c) sector note Active Theses entries, (d) `snapshot_of:` fields in `_Archive/Snapshots/` (breaking `/rollback`), (e) `_hot.md` free-text mentions. `/lint #3` catches broken wikilinks only after the fact without auto-fix.

Design rationale in `.claude/skills/rename/RATIONALE.md` (§N.M anchors).

## Arguments

`$ARGUMENTS` = `TICKER "New Company Name"`. Examples:
- `/rename META "Meta Platforms"`
- `/rename SHOP "Shopify Inc"`
- `/rename SQ "Block"` (after Square → Block rebrand)

Missing quoted name, no ticker, or extra args → ask user to clarify.

## Step 0: Pre-flight

### 0.1: Acquire vault lock

`ticker:TICKER` scope per `.claude/skills/_shared/preflight.md` Procedure 1. Timeout 5 min. Capture token, verify (Procedure 1.5) every subsequent block, release in final reporting block.

### 0.2: Name sanitization (C6.1 — §7)

Run `.claude/skills/_shared/preflight.md` Procedure 3 against proposed `new_name` from $ARGUMENTS:
1. NFC-normalize input.
2. Trim leading/trailing whitespace. Empty → reject.
3. Length ≤ 100 bytes → reject if exceeded.
4. Character whitelist: `[a-zA-Z0-9 \-_.,'&()]`. Any other character → reject (specific flag for `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`).
5. No leading dot → reject.
6. First whitespace-token not reserved (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`, case-insensitive) → reject.

On rejection, emit contract's standard rejection message + suggested clean variant. Do NOT proceed.

## Step 1: Validate

1. **Find current thesis** via ticker-prefix glob: `Theses/TICKER - *.md`.
   - Zero matches: stop. `⚠️ No thesis found for [TICKER] in Theses/. Run /thesis [TICKER] to create.`
   - Multiple: stop. `⚠️ Multiple Theses/ files match prefix "[TICKER]" — [list]. Resolve filename collision before re-running.`
   - One match: extract `[old_name]` from `Theses/TICKER - [old_name].md`.

2. **Compute new filename**: `Theses/TICKER - [new_name].md`.

3. **Validate new name**:
   - No path-illegal characters (double-checked post-sanitization).
   - Must not match existing file at new path in `Theses/`. Collision → stop: `⚠️ Target file already exists: Theses/TICKER - [new_name].md. Choose a different name or remove the existing file first.`
     - **Exception — incomplete-rename repair** (§2.2): if `.rename_incomplete.TICKER` exists AND its `new_name:` equals proposed new name, this is a repair re-run. The collision is expected (filename move from prior failed run already produced `Theses/TICKER - [new_name].md`). Skip abort, log `ℹ️ Repair re-run detected — .rename_incomplete.TICKER exists for [TICKER] → [new_name]. Skipping mv (already done), proceeding to retry failed wikilink rewrites from Step 5.`, jump from Step 1 directly to Step 5 (skip Steps 2/3/3.5/4).
   - **Archive collision check** (§6): glob `_Archive/TICKER - [new_name].md` (non-recursive — ignore `_Archive/Snapshots/`). Match → warn, require explicit confirmation:
     ```
     ⚠️ Archive collision: _Archive/TICKER - [new_name].md already exists from a prior closure of this ticker. If you later close the renamed thesis, /status Step 7.5 would mv the new thesis to the same archive path and silently overwrite the old archive copy.
     
     Options:
       (a) Proceed anyway (accept future overwrite risk).
       (b) Rename the old archive first: mv "_Archive/TICKER - [new_name].md" "_Archive/TICKER - [new_name] (closed YYYY-MM-DD).md" — then re-run /rename.
       (c) Cancel.
     ```
     Wait for user selection. Do NOT proceed silently.

4. **Check no-op**: `[old_name] == [new_name]` (case-sensitive after trim) → stop. `⚠️ Old and new names match. Nothing to rename.`
   - **Exception — incomplete-rename repair**: same bypass as Step 1.3 when `.rename_incomplete.TICKER` matches proposed new name.

### Step 1.4.5: Incomplete-rename cross-name guard (§2.3)

If `.rename_incomplete.TICKER` exists, read its frontmatter and compare `new_name:` to proposed new name:

- **`marker.new_name == proposed_new_name`** → repair re-run (already handled by Steps 1.3/1.4 exceptions). Jump to Step 5.
- **`marker.new_name != proposed_new_name`** → STOP with explicit guard. Proceeding would orphan repair targets.

   ```
   ❌ In-flight rename conflict for TICKER:
     Existing marker: .rename_incomplete.TICKER
       prior new_name:     [marker.new_name]
       failed_files:       [N entries — these need OldName → marker.new_name rewrites]
       batch:              [marker.batch]
   
     Proposed rename:
       new new_name:       [proposed_new_name]
   
   These conflict. The marker's failed wikilink rewrites were collected for
   "[marker.new_name]" — proceeding with "[proposed_new_name]" would orphan those
   repair targets (their wikilinks would still reference an obsolete OldName,
   never NewName2, with no marker to track them).
   
   Resolve before re-running /rename. Options:
     (a) Finish the prior rename first:
         /rename TICKER "[marker.new_name]"
         (re-runs Step 5 wikilink rewrites for the still-failing files;
         when all succeed, marker auto-deletes)
     (b) Manually resolve the failed files listed in the marker, then
         delete the marker (rm ".rename_incomplete.TICKER"), then re-run
         this rename.
     (c) Accept loss of in-flight repair state. BEFORE running rm:
         (1) READ the marker's "Failed files" list. Print with explicit warning:
             "These N file(s) currently contain wikilinks to [[Theses/TICKER -
              [TRULY_ORIGINAL_NAME]]] (the name BEFORE the prior failed rename).
              After deleting the marker and re-running with the new name, those
              wikilinks will remain broken — Step 5's grep/replace targets the
              CURRENT filename ([marker.new_name]), not the truly-original name.
              The new rename's Step 5 will NOT fix these. /lint #3 will flag them
              eventually.
              Resolution before option (c): manually grep-replace
              [TRULY_ORIGINAL_NAME] → [proposed_new_name] in each listed file
              FIRST, then proceed."
         (2) Wait for explicit user confirmation of manual remediation OR explicit
             acceptance of broken-wikilink outcome.
         (3) Only then rm ".rename_incomplete.TICKER" and re-run /rename.
   ```

   Do NOT proceed silently. Wait for user action, then re-invoke.

5. **Survey inbound references** (read-only — for confirmation prompt). **Issue the five probes below as a single parallel tool-call batch** — all probes are read-only against vault state that is stable under the ticker lock acquired in Step 0.1. One message, five independent tool invocations, lands in one round-trip instead of five serial rounds:

   | # | Probe | Tool | Purpose |
   |---|---|---|---|
   | 1 | Grep vault | `Grep` (multi-path) across `Theses/ Sectors/ Macro & Technology/ Research/ _Archive/ _Archive/Sectors/ _Archive/Research/ _Archive/Snapshots/`, excluding `.git/` and `_Inbox/processed/` | Count Step 5 wikilink pattern matches; partition results by category during parsing — live files (Theses/, Sectors/, Macro & Technology/, Research/), archived theses (`_Archive/*.md` root), archived sectors (`_Archive/Sectors/`), archived research (`_Archive/Research/`), snapshot bodies (`_Archive/Snapshots/`) — for the Step 2 survey breakdown |
   | 2 | Grep snapshot frontmatter | `Grep` for `snapshot_of:` references to old path in `_Archive/Snapshots/` | Frontmatter count (separate from body matches — handled by Step 8) |
   | 3 | Read `_graph.md` | `Read` | Locate `### TICKER - [old_name]` in Adjacency Index; note presence |
   | 4 | Resolve sector note | `Read` candidate sector note (inferred from thesis `sector:` frontmatter read earlier in Step 1) | Scan Active Theses for old wikilink (sector-resolution contract applied in reasoning layer after read) |
   | 5 | Read `_hot.md` | `Read` | Count free-text mentions of `TICKER - [old_name]` (outside wikilink syntax) |

   After the batch returns, parse results in the reasoning layer to build the survey summary for Step 2's confirmation prompt. Sector-resolution `match_confidence` is determined from the already-read sector candidate content; no additional tool call needed. If the sector-resolution fallback chain requires reading multiple candidate sector files, the LLM may issue a secondary parallel Read batch — still bounded.

## Step 2: Confirm (Tier 3 — Mandatory)

Present proposed rename + survey. **Wait for explicit user confirmation.**

```
Proposed rename:
  Old: [[Theses/TICKER - old_name]]
  New: [[Theses/TICKER - new_name]]

Side effects (will be updated):
  - Inbound wikilinks in live files (Theses/, Sectors/, Macro & Technology/, Research/, _hot.md): [count] across [N] files — [list paths]
  - Inbound wikilinks in archived theses (_Archive/*.md root): [count] across [P] files — [list paths]
  - Inbound wikilinks in archived sectors (_Archive/Sectors/): [count] across [Q] files — [list paths]
  - Inbound wikilinks in archived research (_Archive/Research/): [count] across [R] files — [list paths]
  - Inbound wikilinks in snapshot bodies: [count] across [M] snapshots (excludes the pre-rename snapshot from Step 3)
  - Graph adjacency entry header: ### TICKER - [old_name] → ### TICKER - [new_name]
  - Sector note Active Theses entry: [present/absent — sector resolved as [sector_name] via [confidence]]
  - Snapshot snapshot_of fields: [count] snapshots in _Archive/Snapshots/
  - _hot.md free-text mentions: [count] occurrences

Pre-rename safety snapshot will be created.

Confirm? (y/n)
```

**Do NOT proceed without explicit user confirmation.**

## Step 3: Pre-Rename Snapshot

```bash
mkdir -p _Archive/Snapshots
HHMMSS=$(date +%H%M%S)
cp "Theses/TICKER - [old_name].md" "_Archive/Snapshots/TICKER - [old_name] (pre-rename YYYY-MM-DD-HHMMSS).md"
```

Read snapshot, add frontmatter:
```yaml
snapshot_of: "[[Theses/TICKER - [old_name]]]"
snapshot_date: YYYY-MM-DD
snapshot_trigger: rename
snapshot_batch: rename-YYYY-MM-DD-HHMMSS
rename_target: "[[Theses/TICKER - [new_name]]]"
```

Batch ID uses HHMMSS (6 digits) to prevent same-minute collisions. `rename_target:` field tells `/rollback` that a cascade matching this batch is reversing a rename.

## Step 3.5: Pre-flight Read/Write Check (§1)

Step 5's rewrite will touch every file in the inbound-reference set. Catch unreachable files BEFORE the mv — §1.1 explains why.

For each file in the inbound-reference set (live files in `Theses/`, `Sectors/`, `Macro & Technology/`, `Research/`, `_hot.md`, plus `_Archive/Snapshots/*.md` with body matches and `snapshot_of:` matches):

1. **Read check**: attempt to read file's first 10 bytes. Fail → record in `unreachable_files: [list]`.
2. **Write probe**: `[ -w "path" ]`. Not writable → record in `unreachable_files`.

**`unreachable_files` non-empty → STOP.** Vault in original state (no mv, no edits).

```
❌ Pre-flight check failed: [N] file(s) cannot be edited. Rename aborted — vault unchanged.

Unreachable files:
  - [path 1] (reason: [permission denied | file locked | not found])
  - [path 2] (reason: ...)

Resolve access issue (close file in another editor, fix permissions, restore deleted file) and re-run /rename. Pre-rename snapshot retained: [[_Archive/Snapshots/...]].
```

## Step 4: Move the File

```bash
mv "Theses/TICKER - [old_name].md" "Theses/TICKER - [new_name].md"
```

Verification:
```bash
ls "Theses/TICKER - [new_name].md"
ls "Theses/TICKER - [old_name].md" 2>/dev/null  # should produce no output
```

`mv` fails → stop. `❌ Rename failed at mv step — vault unchanged. Snapshot retained: [[_Archive/Snapshots/...]]. Investigate filesystem permissions.` Wikilinks not modified; vault safe.

## Step 5: Update Inbound Wikilinks (§3, §5)

Grep vault (excluding `.git/` and `_Inbox/processed/`), Edit each file. **`_Archive/` (root archived theses), `_Archive/Sectors/`, `_Archive/Research/`, and `_Archive/Snapshots/` are NOT excluded** — every one of these locations holds notes that may carry `[[Theses/TICKER - old_name]]` wikilinks. Stale wikilinks in archived sector or research notes break Obsidian rendering on browse and break `/rollback` integrity if those archives are ever restored. Stale wikilinks in snapshot bodies break `/rollback` content fidelity (§3.1).

**Prefix-rewrite rule (§5 — supersedes the old 7-pattern enumeration).** Rewrite by the wikilink STEM, not by enumerating suffix combinations. Every inbound link to the thesis begins with one of two stems:

- `[[Theses/TICKER - old_name`  → `[[Theses/TICKER - new_name`
- `[[TICKER - old_name`         → `[[TICKER - new_name` (folder-less form)

…and the stem is followed **immediately** by exactly one character from the **boundary set `{ ] . # | }`**:

| Boundary char after `old_name` | Link form | Example |
|---|---|---|
| `]` | bare | `[[Theses/TICKER - old_name]]` |
| `.` | `.md` suffix (± anchor/alias) | `[[Theses/TICKER - old_name.md]]`, `[[Theses/TICKER - old_name.md#Outstanding Questions]]`, `[[Theses/TICKER - old_name.md\|alias]]` |
| `#` | anchor | `[[Theses/TICKER - old_name#Bull Case]]` |
| `\|` | alias | `[[Theses/TICKER - old_name\|Company]]` |

Rewriting the STEM automatically preserves every suffix — `.md`, `#anchor`, `\|alias`, AND their combinations (`.md#anchor`, `.md\|alias`) — because only the `old_name` portion changes and everything after the boundary char is untouched. The old table enumerated 7 forms and **missed `.md#anchor`, `.md\|alias`, and the three folder-less `.md` variants**, silently breaking those links on rename (real vault exposure: `[[Theses/SOI - Soitec.md#Outstanding Questions]]` + 18 escaped-pipe `[[Theses/… \| alias]]` links).

**Boundary-set guard (do NOT over-match):** only rewrite when the next char is in `{ ] . # | }`. This prevents a rename of `Meta` from clobbering `[[Theses/META - Meta Platforms]]` (next char after `Meta` is a space, not a boundary char). When old_name is a strict prefix of another thesis name, the boundary guard is what keeps them distinct.

**Edit-per-file approach**: per file with matches, one `Edit` with `replace_all: true` for the `[[Theses/TICKER - old_name` stem and one for the `[[TICKER - old_name` stem. Since Edit does literal-substring replacement, replacing the stem string (which ends at `old_name`, before the boundary char) is inherently boundary-safe — a longer name like `old_name Plus` contains the stem but the replacement correctly rewrites only the `old_name` portion, leaving ` Plus` intact; verify post-Edit that no unintended thesis was touched (Step 5 tracking). Atomic; bounded failure blast-radius.

**Self-references in renamed thesis**: covered by same rewrite (e.g., template scaffolding wikilinks back to the thesis itself).

**Snapshot body rewrite exception** (§3.3): skip the just-created pre-rename snapshot from Step 3. Identify via `snapshot_trigger: rename` frontmatter + matching HHMMSS. That snapshot IS the pre-rename state — must stay untouched so `/rollback` recovers original content. All OTHER snapshots are eligible for body wikilink rewrites.

**Forward-drift trade-off** (§3.2): rewriting snapshot bodies means snapshots no longer faithfully reproduce vault state at snapshot time. Alternative (not rewriting) re-injects broken wikilinks on rollback. Forward-drift is lesser evil — a snapshot that can't cleanly restore is a dead snapshot.

**Track**: list of files modified (split by live vs snapshot for Step 11 report), total wikilink count, `failed_edits: [list]` for any Edit that errors.

**Failure handling**: Edit fails for a file → do NOT abort loop. Continue with remaining. Append failed path + reason to `failed_edits`. End of Step 5, if `failed_edits` non-empty → write incomplete-rename marker (Step 5.5).

**Cross-step failure accumulator initialization (H3 fix)**: at the start of Step 5, also initialize an empty `all_failed_ops: []` list in working memory. Steps 6 through 10 append to this list on any Edit / validation / Bash failure. Step 10.5 consolidates into the marker. Section `## Failed operations (Steps 6-10)` of the marker captures everything beyond Step 5's wikilink failures.

### Step 5.5: Write `.rename_incomplete.TICKER` Marker (if any Edit failed)

If `failed_edits` empty → skip Step 5.5 write; Step 10.5 will still write the marker later if `all_failed_ops` accumulates.

If non-empty → write `.rename_incomplete.TICKER` at vault root. Per-ticker filename (§2.1 — multiple in-flight repairs coexist). The marker created here includes an empty `## Failed operations (Steps 6-10)` section that Step 10.5 populates on demand.

```markdown
---
type: rename-incomplete
ticker: TICKER
old_name: [old_name]
new_name: [new_name]
batch: rename-YYYY-MM-DD-HHMMSS
date: YYYY-MM-DD
---

# Incomplete Rename

`/rename TICKER "[new_name]"` completed the move but left [N] file(s) with
stale wikilinks and/or [M] follow-up operation(s) in a partial state. These
must be repaired before downstream ticker-scoped skills operate on TICKER.

## Failed files (Step 5 — wikilink rewrites)

*(empty if all Step 5 wikilink rewrites succeeded; populated by Step 5.5)*

- `Theses/SOMEOTHER - Foo.md` — reason: [Edit error: file lock | permission denied | concurrent modification]
- `_Archive/Snapshots/X.md` — reason: ...

## Failed operations (Steps 6–10)

*(empty if Steps 6-10 succeeded; populated or updated by Step 10.5 — H3 fix)*

- Step 6 (graph adjacency header): _graph.md — adjacency entry `### [TICKER] - [old_name]` not found (graph stale)
  - Recovery: run `/graph` (full rebuild) after the marker is cleared — re-derives header from current filename
- Step 7 (sector note Active Theses): Sectors/[Sector Name].md — [specific failure — e.g., sector-resolution substring confidence declined, Edit lock]
  - Recovery: manually replace `[[Theses/[TICKER] - [old_name]]]` → `[[Theses/[TICKER] - [new_name]]]` in the sector's Active Theses section, then remove this bullet from the marker
- Step 8 (snapshot `snapshot_of:` field): _Archive/Snapshots/[Snapshot Name].md — Edit failed
  - Recovery: manually edit the snapshot's frontmatter `snapshot_of: "[[Theses/[TICKER] - [old_name]]]"` → `"[[Theses/[TICKER] - [new_name]]]"`
- Step 8.5 (archive registry row rewrite): .archive_ticker_registry.md — [awk/mv error]
  - Recovery: manually replace `[TICKER] - [old_name]` → `[TICKER] - [new_name]` in the `archived_filename` column (second pipe-delimited field) of every row whose first field is `[TICKER]`
- Step 9 (_hot.md free-text mentions): _hot.md — Edit failed ([N] mentions unresolved)
  - Recovery: manually replace `[TICKER] - [old_name]` → `[TICKER] - [new_name]` in free-text mentions (Active Research Thread narrative, Recent Conviction Changes bullets, etc.)
- Step 10 (thesis Log append): Theses/[TICKER] - [new_name].md — Edit failed
  - Recovery: manually append the `Renamed file:` Log entry per the format in `rename/SKILL.md` Step 10

## Recovery

Re-run:

  /rename TICKER "[new_name]"

/rename's repair detection (Step 1.3/1.4 exceptions) skips the filename move
(already done) and retries:
  - All "Failed files" wikilink rewrites (Step 5)
  - All "Failed operations" bullets above (Steps 6–10 — H3 fix)

Successful retries remove their entries from the respective list. When both
lists are empty, this marker is auto-deleted.

/lint #37 surfaces this marker until every listed repair succeeds.

DO NOT delete this marker manually unless you have verified every failed file
and operation has been repaired externally.
```

**Append-only on re-runs** (§2.4): if `.rename_incomplete.TICKER` already exists AND `new_name:` matches current run, READ first. Merge new `failed_edits` into existing "Failed files" list (dedupe by file path) and merge new `all_failed_ops` into existing "Failed operations" list (dedupe by `(step, target)` tuple), update `batch:` to latest run's batch, rewrite. Don't overwrite — accumulating across repair attempts surfaces persistent problem files and ops.

**Cross-new_name conflict**: handled by Step 1.4.5 guard. Never runs here.

## Step 6: Update Graph Adjacency Entry Header (§4)

Edit `_graph.md`:
- Find: `### TICKER - [old_name]` in `## Thesis Adjacency Index` section.
- Replace with: `### TICKER - [new_name]`.

Missing heading (graph stale) → warn + append to `all_failed_ops` (H3 fix):
```
- Step 6 (graph adjacency header): _graph.md — adjacency entry for [TICKER] not found (graph stale)
  - Recovery: run /graph (full) after marker clears — rebuilds adjacency index from current filenames
```

Emit user-visible warning: `⚠️ Graph adjacency entry for [TICKER] not found — graph is stale. Run /graph after rename to rebuild.` Continue skill — do not fail.

Scan `## Cross-Thesis Clusters` table for cells containing old name format. Replace. (Most cluster references use `[[Theses/...]]` wikilinks — Step 5 handled. This catches free-text.)

**Do NOT update `_graph.md` frontmatter `date:` or `last_graph_write:`** (§4.1). Watermark ownership is `/graph`'s. Advancing would silently mask pending changes from next `/graph last`. Next `/graph last` correctly re-extracts this thesis (mtime advanced by rename).

**Graph validation**: re-read `_graph.md`. Verify:
1. YAML frontmatter parses.
2. New heading `### TICKER - [new_name]` exists in adjacency index.
3. Old heading `### TICKER - [old_name]` does not exist anywhere.
4. Adjacency entry count matches `theses:` frontmatter (±2).

Any fail: emit `⚠️ Graph may be corrupted by rename — [specific failure]. Run /graph to rebuild.` AND append to `all_failed_ops`:
```
- Step 6 (graph validation): _graph.md — [specific failure: YAML parse | duplicate heading | old heading remains | count mismatch]
  - Recovery: run /graph (full rebuild) to regenerate graph from current filenames
```

## Step 7: Update Sector Note

If thesis is `status: active` or `status: monitoring`, sector note (resolved Step 1.5) likely contains thesis in Active Theses.

Read sector note. If contains `[[Theses/TICKER - old_name]]` or `[[TICKER - old_name]]`:
- Already rewritten in Step 5 if grep covered sector note. Verify via re-read.
- If missed (unusual format), apply targeted Edit here.

Skip if `status: draft` (drafts aren't in sector notes per `/thesis` Step 5).

**Failure handling (H3 fix)**: if sector-resolution returned `substring` confidence and user declined, OR if the targeted Edit here fails, append to `all_failed_ops`:
```
- Step 7 (sector note Active Theses): Sectors/[Sector Name].md — [substring-confidence declined | Edit error: specific reason]
  - Recovery: manually replace [[Theses/[TICKER] - [old_name]]] → [[Theses/[TICKER] - [new_name]]] in the sector's Active Theses section
```
If sector-resolution returned `none` (no matching sector note), this is NOT a failure — log `ℹ️ Sector note skipped — no matching Sectors/*.md for frontmatter [sector]. Skipping Step 7.` and continue; the thesis's sector frontmatter is the authoritative signal and `/thesis` Signal C handles orphans.

## Step 8: Update Snapshot `snapshot_of:` Fields (§3.4)

For each `_Archive/Snapshots/*.md` with `snapshot_of: "[[Theses/TICKER - [old_name]]]"`:
1. Read frontmatter.
2. Targeted `Edit`: `snapshot_of: "[[Theses/TICKER - [old_name]]]"` → `snapshot_of: "[[Theses/TICKER - [new_name]]]"`.

Preserves `/rollback` functionality. Without this, `/rollback` would read `snapshot_of:`, look for old path, fail to find original (or recreate at old path causing filename split).

**Exception** (§3.3): skip snapshots whose `snapshot_trigger: rename` AND `rename_target:` matches the new path — these are this skill's own snapshots (Step 3); must retain old `snapshot_of:` reference for accurate rollback semantics.

**Failure handling (H3 fix)**: for each snapshot whose Edit fails, append to `all_failed_ops` (one entry per failed snapshot):
```
- Step 8 (snapshot `snapshot_of:` field): _Archive/Snapshots/[Snapshot Name].md — [Edit error: specific reason]
  - Recovery: manually edit the snapshot's frontmatter `snapshot_of: "[[Theses/[TICKER] - [old_name]]]"` → `"[[Theses/[TICKER] - [new_name]]]"`
```
Do NOT abort the loop — continue with remaining snapshots.

## Step 8.5: Update `.archive_ticker_registry.md` Historical Rows (H4 fix)

`.archive_ticker_registry.md` carries `TICKER|archived_filename|YYYY-MM-DD|conviction|rationale` rows. If TICKER was previously closed (under `[old_name]`), then resurrected via `/rollback` (which ideally cleared the row via its Step 6.2a), then renamed live — or if resurrection happened via manual mv that bypassed `/rollback` — the registry may still carry rows referencing the pre-rename `archived_filename`.

Rewrite the `archived_filename` column for every row matching this TICKER so future `/thesis TICKER` Signal C lookups resolve consistently:

```bash
if [ -f .archive_ticker_registry.md ]; then
  # Replace the second pipe-delimited field for rows whose first field == TICKER.
  # Preserve rows for OTHER tickers untouched. Preserve header/comment lines.
  awk -F'|' -v OFS='|' -v t="$TICKER" -v oldn="$OLD_NAME" -v newn="$NEW_NAME" '
    NR==1 || /^#/ || NF<2 { print; next }
    $1==t && $2==t " - " oldn ".md" { $2 = t " - " newn ".md"; print; next }
    $1==t && $2==t " - " oldn      { $2 = t " - " newn;      print; next }
    { print }
  ' .archive_ticker_registry.md > .archive_ticker_registry.md.tmp
  mv .archive_ticker_registry.md.tmp .archive_ticker_registry.md
fi
```

**Track**: count of rewritten rows (0 if no prior closures on record, typically 0–1 in practice). Report in Step 11.

**Failure handling** (H3 — see §Step 10.5): if awk or mv fails, append to `all_failed_ops` accumulator with recovery instructions:
```
- Step 8.5 (archive registry row rewrite): .archive_ticker_registry.md — [awk/mv error]
  - Recovery: manually replace "[TICKER] - [old_name]" → "[TICKER] - [new_name]" in the `archived_filename` column of every row whose first field is "[TICKER]"
```

**No-op on missing file**: if `.archive_ticker_registry.md` doesn't exist (clean vault or all prior rows already cleared), skip silently — no error.

**Why this is safe against double-rewrite**: the awk match is exact (`$2==t " - " oldn` — not substring). A row already rewritten to `[new_name]` doesn't match, so re-running `/rename` with the same args is idempotent.

## Step 9: Update _hot.md Free-Text Mentions

Most `_hot.md` references use `[[Theses/...]]` — handled by Step 5. This step catches free-text:
- `Recent Conviction Changes`: bullets may say `**TICKER - old_name**: ...` → replace.
- `Active Research Thread`: narrative prose mentions.
- `Latest Sync` / `Sync Archive`: descriptions.

Use `Edit` with `replace_all: true` for literal `TICKER - [old_name]` (not in wikilink syntax). Word-boundary care — don't match substring inside longer words.

**Word cap**: after edits, check `_hot.md` total. Over 8,000 (soft cap per `_shared/hot-md-contract.md`; unlikely from rename) → prune `## Sync Archive` oldest first. Abort if over 10,000 hard cap.

**Failure handling (H3 fix)**: if the free-text Edit fails (rare — `_hot.md` rarely has file locks), append to `all_failed_ops`:
```
- Step 9 (_hot.md free-text mentions): _hot.md — [Edit error: specific reason] ([N] mentions unresolved)
  - Recovery: manually replace `[TICKER] - [old_name]` → `[TICKER] - [new_name]` in `_hot.md` (outside wikilink syntax — Active Research Thread narrative, Recent Conviction Changes bullets)
```

## Step 10: Append Log Entry to Renamed Thesis

Append to renamed thesis's `## Log`:

```
### YYYY-MM-DD
- Renamed file: "TICKER - [old_name]" → "TICKER - [new_name]". [N] inbound wikilinks rewritten across [M] files. Snapshot: [[_Archive/Snapshots/TICKER - [old_name] (pre-rename YYYY-MM-DD-HHMMSS)]]
```

Prefix `"Renamed file:"` — `/sync` Step 2.5 skill-origin classification + Step 3e drift exclusion (registry §15).

**Failure handling (H3 fix)**: if the Log append Edit fails, append to `all_failed_ops`:
```
- Step 10 (thesis Log append): Theses/[TICKER] - [new_name].md — [Edit error: specific reason]
  - Recovery: manually append the "Renamed file:" Log entry per the format above; required for audit trail and /sync Step 2.5 classification
```

## Step 10.5: Consolidate failure accumulator into marker (H3 fix)

**Purpose**: Steps 5.5 (failed_edits) and 10.5 (all_failed_ops) jointly own the `.rename_incomplete.TICKER` marker. Step 5.5 writes the marker on Step 5 wikilink failures. This step writes or updates the marker to include any Step 6–10 operation failures accumulated in `all_failed_ops`.

**Skip condition**: if `failed_edits` empty AND `all_failed_ops` empty → skip. No marker action.

**Otherwise**:
1. Determine marker state (new or existing from Step 5.5 / prior run):
   - Marker does NOT exist → write from scratch using the template in Step 5.5, populating both `## Failed files (Step 5 — wikilink rewrites)` and `## Failed operations (Steps 6–10)` sections from the two accumulators.
   - Marker EXISTS (Step 5.5 wrote it this run, or prior-run marker being repaired):
     - Read marker, parse existing `## Failed files` and `## Failed operations` sections.
     - **Failed files merge**: current `failed_edits` replaces existing list entries whose file path matches (repair retries remove resolved entries; new failures add). Dedupe by file path.
     - **Failed operations merge**: current `all_failed_ops` replaces existing bullets whose `(step, target)` tuple matches (repair retries remove resolved entries; new failures add). Dedupe by `(step, target)`.
     - Update `batch:` frontmatter to current run's batch ID (tracks latest repair attempt).
     - Rewrite marker with merged sections.
2. **Auto-cleanup after merge**: if both merged lists are EMPTY (every prior failure resolved, no new failures accumulated), delete the marker:
   ```bash
   rm -f ".rename_incomplete.TICKER"
   ```
   The auto-cleanup contract (§Marker auto-cleanup contract below) is now owned by Step 10.5, not scattered across Step 5.5. Marker persists until every file and every op succeeds.

**Repair re-run semantics**: when `/rename TICKER "[same new_name]"` runs with an existing marker, Step 1.3/1.4 exceptions skip the mv. Steps 5, 6, 7, 8, 8.5, 9, 10 all re-run and re-accumulate their failures. Step 10.5 merges: resolved entries drop, persistent entries remain, new failures add. Monotonic shrink until empty, then marker disappears.

## Step 11: Report

- **Renamed**: `Theses/TICKER - [old_name].md` → `Theses/TICKER - [new_name].md` | `Repair re-run — mv skipped (already done)`
- **Pre-flight check**: `passed ([N] files reachable)` | `aborted ([M] unreachable — no changes made)`
- **Wikilinks rewritten (live files)**: [count] across [live file paths in Theses/, Sectors/, Macro & Technology/, Research/, _hot.md]
- **Wikilinks rewritten (snapshot bodies)**: [count] across [`_Archive/Snapshots/*.md` paths]. Excludes pre-rename snapshot from Step 3.
- **Wikilink update failures** (Step 5, if any): [list files]
- **Follow-up operation failures** (Steps 6–10 — H3 fix, if any): [list `(step, target, reason)`]
- **`.rename_incomplete.TICKER` marker**: `created (with Failed files and/or Failed operations sections)` | `updated (merged new failures)` | `cleared (all prior failures resolved — file deleted)` | `n/a`
- **Repair status** (if marker processed this run):
  - **Failed files resolved this run**: [paths retried successfully and removed from marker]
  - **Failed files still failing**: [paths still in marker]
  - **Failed operations resolved this run**: [`(step, target)` tuples retried successfully and removed from marker]
  - **Failed operations still failing**: [`(step, target)` tuples still in marker]
  - **Marker state**: `cleared (both sections empty — file deleted)` | `retained ([N] files + [M] ops still need repair)`
- **Graph adjacency entry**: header updated | `⚠️ stale graph — entry not found, run /graph` (recorded in marker via Step 6)
- **Sector note**: updated as `[sector_name]` (resolution `[exact|normalized|substring]`) | `skipped (draft status)` | `skipped (no matching sector note)` | `⚠️ failed — see marker Step 7 entry`
- **Snapshots updated**: [count] `snapshot_of:` fields adjusted (of [total]); [failed_count] recorded in marker Step 8
- **Archive registry rows rewritten** (Step 8.5 — H4 fix): [count] rows in `.archive_ticker_registry.md` updated | `0 (no prior closures on record)` | `⚠️ failed — see marker Step 8.5 entry`
- **_hot.md**: [count] free-text mentions replaced | `⚠️ failed — see marker Step 9 entry`
- **Pre-rename snapshot**: `[[_Archive/Snapshots/TICKER - [old_name] (pre-rename YYYY-MM-DD-HHMMSS)]]`
- **Batch ID**: `rename-YYYY-MM-DD-HHMMSS`

**To undo this rename**: run `/rename TICKER "[old_name]"` (symmetric inverse). Pre-rename snapshot also available via `/rollback TICKER` → select `(pre-rename)` snapshot, but rollback alone restores content only; filename revert + inbound wikilink revert require running this skill in reverse.

### Marker auto-cleanup contract (H3 refactor — now owned by Step 10.5)

The `.rename_incomplete.TICKER` marker is jointly owned by two write points:
1. **Step 5.5**: writes marker if `failed_edits` (Step 5 wikilink failures) is non-empty. Includes an empty `## Failed operations (Steps 6–10)` section that Step 10.5 may populate.
2. **Step 10.5 (H3 fix)**: consolidates `all_failed_ops` from Steps 6–10 into the marker. Creates the marker if Step 5.5 didn't (Step 5 succeeded but a later step failed). Deletes the marker if both sections are empty after merge.

Both write points dedupe across re-runs: Step 5.5 dedupes by file path, Step 10.5 dedupes by `(step, target)` tuple. Monotonic shrink across repair re-runs until both lists empty, then marker auto-deletes.

`/lint #37` surfaces any marker with non-empty `## Failed files` OR non-empty `## Failed operations`.

## Edge cases (§8 — all out-of-scope)

- **Rename across ticker change** (`FB - Facebook` → `META - Meta`): TICKER must be stable. Manual workaround: `/thesis META` + copy content + `/status FB active→closed`.
- **Renaming archived theses**: `/rename` operates on active/monitoring/draft in `Theses/`. Manual mv + registry edit for archived.
- **Old name with regex special chars**: glob/grep assume literal string matching. Unusual symbols (parens, braces, `$`) prompt explicit escaping confirmation.
