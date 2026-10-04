---
name: archive-callouts
description: Sweep addressed callouts older than a threshold (default 180 days) into the target note's ## Legacy Callouts section. Converts verbose callout blocks into plain bulleted entries sorted descending by addressed date, preserving full original text and Response. Use when user says "archive callouts", "sweep callouts", "clean old callouts", or references addressed-callout hygiene.
model: sonnet
effort: max
allowed-tools: Read Grep Glob Edit Write Bash(date * cp * mkdir * grep * rm * awk *)
---

**Follow CLAUDE.md Writing Standards strictly.** No hedge words, lead with insights/numbers, tables over prose, every sentence must earn its place.

Sweep addressed callouts older than the configured threshold from their original sections into a dedicated `## Legacy Callouts` archive section at the bottom of the target note (above `## Log`). Callout formatting is stripped — entries become plain bulleted text preserving full original body, date metadata, section provenance, and Response. The source sections become less cluttered over time; the audit trail stays co-located with the thesis.

**Tier 1 skill under CLAUDE.md Change Safety Rules** — owns the `## Legacy Callouts` section exclusively. Nothing else writes to it; this skill never writes anywhere else except the per-thesis `## Log` (append-only `Callout sweep:` entry) and thesis frontmatter (`last_callout_sweep:`).

## Arguments

`$ARGUMENTS` patterns:
- **empty** → **dry-run preview** across the whole vault using the default 180-day threshold. Never writes. Outputs the preview table and exits.
- **integer** (e.g., `180`, `90`) → execute vault-wide sweep with that day threshold.
- **`TICKER`** (e.g., `NVDA`) → scoped dry-run preview for one thesis at default 180d.
- **`TICKER [days]`** (e.g., `NVDA 90`) → scoped execute.
- **`[days] dry-run`** or **`TICKER [days] dry-run`** → explicit dry-run even with numeric threshold (belt-and-braces).

Parse order:
```
Split $ARGUMENTS by whitespace into tokens.
If any token is "dry-run" → force dry-run mode, strip it.
Classify each remaining token by CHECKING THE VAULT, not a regex:
  - If Glob "Theses/<token> - *.md" matches a file → ticker (scoped).
    Vault-check (not a charset regex) is mandatory: the vault has numeric and
    alphanumeric tickers (000660, 2383, 285A, 6857) and hyphenated ones
    (BTC-CRYPTO) that a /^[A-Z].../ pattern cannot match — misparsing "2383"
    as a 2383-day threshold silently promotes a scoped dry-run into an
    UNCONFIRMED VAULT-WIDE EXECUTE.
  - Else if token matches /^\d+$/ → integer threshold (days).
  - Else → unrecognized token. Report `❌ Unrecognized argument "<token>" — not a
    thesis ticker (no Theses/<token> - *.md) and not an integer threshold.` Abort.
    Do NOT silently fall through to vault-wide execute.
Default threshold = 180.
No numeric threshold AND no explicit execute intent → dry-run mode.
```

**When ambiguous**: a bare integer with no matching thesis (e.g., `100` — no `Theses/100 - *.md`) is a threshold. A token that matches a thesis glob (e.g., `2383` → `Theses/2383 - Elite Material.md`) is that ticker. The vault-glob check resolves the ambiguity deterministically against real files.

## Step 0: Pre-flight (MANDATORY)

### 0.1: Acquire vault lock

Per `.claude/skills/_shared/preflight.md` Procedure 1.

- **Vault-wide mode** (no ticker): `vault-wide` scope. Timeout budget: 10 minutes (may touch many theses + sector notes).
- **Scoped mode** (`TICKER`): `ticker:TICKER` scope. Timeout budget: 5 minutes.
- **Dry-run (any scope)**: still acquire the same lock (the skill reads many files and must see consistent state mid-scan). Dry-run short-circuits BEFORE any write phase, so lock-hold time is bounded by the scan.

Capture the token. Verify ownership (Procedure 1.5) at every subsequent Bash block. Release in the final reporting block.

### 0.2: Rename-marker check

Per `.claude/skills/_shared/preflight.md` Procedure 2.

- **Vault-wide**: glob `.rename_incomplete.*`. If any exist, hard-block — a sweep mid-rename could reformat a thesis whose inbound wikilinks are still split across old and new names, compounding the inconsistency.
- **Scoped**: check `.rename_incomplete.TICKER`. Hard-block if present.

### 0.3: Section existence probe — handled DIFFERENTLY from standard Procedure 4

Unlike `/deepen` (which aborts on missing sections), `/archive-callouts` **creates `## Legacy Callouts` on demand** per the Sweep Contract below. Standard Procedure 4 does NOT apply to this skill.

The skill DOES require `## Log` to exist on the target note (needed for the `Callout sweep:` append). If `## Log` is absent → skip the target with warning `ℹ️ Skipped [[target]]: no ## Log section. Sweep needs Log for audit trail. Add ## Log manually or ignore if target is free-form macro.`

Both applicable pre-flight checks must pass before proceeding to Phase 1.

## Phase 1: Scope Resolution

Resolve the list of target files.

- **Vault-wide**: `Theses/*.md` + `Sectors/*.md` + `Macro & Technology/*.md`. Research/ is excluded (Tier 2 immutable per CLAUDE.md — research notes don't carry callouts by convention).
- **Scoped (`TICKER`)**: single file `Theses/TICKER - *.md` resolved via Glob.
  - Zero matches → `❌ No thesis matching ticker "[TICKER]". Check the ticker spelling or use /thesis TICKER to create.` Abort.
  - Multiple matches (shouldn't happen with canonical naming) → list them and ask user to pick.

Report the resolved scope to the user:
```
Scope: [N] theses + [M] sectors + [K] macro notes
Threshold: [days] days from → Addressed date
Mode: [dry-run | execute]
```

## Phase 2: Per-Note Scan for Sweep Candidates

For each target file, issue ONE Read. Parse the body for callout blocks. Execute the following parallel scan pattern for efficiency:

### 2.1: Parallel batch Read

Issue a single parallel batch of Read calls for ALL resolved target files. Wait for all to land. Do not serialize.

### 2.2: Per-file callout parsing

For each file's content, identify callout blocks matching this pattern (line-anchored):

```
> [!<type>] <fresh_date>[ → Addressed <addressed_date>][ <markers>]
> <body line 1>
> <body line 2>
...
> **Response:** <response line 1>
> <response line 2>
...
```

Where:
- `<type>` is one of `question | error | tip | todo` (exactly — any other value → log `ℹ️ Skipped unrecognized callout type "[X]" in [file]` and ignore)
- `<fresh_date>` is `YYYY-MM-DD`
- `<addressed_date>` is optional. Absent → callout is **fresh** → SKIP (never sweep fresh)
- `<markers>` may include `[[pinned]]` — opt-out marker, applies to fresh OR addressed callouts → SKIP. (Note: `[[preserve]]` is **deprecated** as of 2026-04-29 — `[[pinned]]` replaces it. The skill still treats `[[preserve]]` as a skip during a transition window for safety, but `/lint #56` flags any remaining occurrences for migration.)
- `**Response:**` block must be present for a callout to qualify as addressed

**Parent section detection**: walk backward from the callout's opening line to the nearest preceding `## <section_name>` heading. This is the callout's origin section — captured for the Legacy entry. If the callout sits above all `## ` headings (shouldn't happen in theses, unusual in sector notes), label section as `<unknown>`.

**Age computation**: `age_days = today - addressed_date`. Callouts with `age_days >= threshold` AND without `[[pinned]]` (and without legacy `[[preserve]]` during the transition window) → **sweep candidates**.

**Location safety**: callouts inside `## Legacy Callouts` itself must NEVER be parsed. Callouts inside `## Log` must also be skipped (Log entries never contain callouts by convention; defensive filter). Skip the entire section bodies for these two headings during scan.

### 2.3: Type label mapping

Convert internal Obsidian callout types to human-readable labels used in the Legacy entry:

| Callout type | Legacy label |
|---|---|
| `question` | `question` |
| `error` | `warning` |
| `tip` | `tip` |
| `todo` | `todo` |

Note: `error` maps to `warning` because the template file is `user-warning.md` (user-facing vocabulary matches the hotkey label, not the Obsidian internal type). Consistent with CLAUDE.md convention.

### 2.4: Entry construction

For each sweep candidate, build the Legacy entry text:

```
- **<addressed_date>** · <legacy_label> · <parent_section> · raised <fresh_date> → <body_joined>
  - **Response:** <response_joined>
```

Where:
- `<body_joined>` = all body lines joined with a single space. Preserve inline formatting (bold, italics, wikilinks). Strip the leading `> ` quote prefix from each line.
- `<response_joined>` = Response block content joined the same way. Strip the `**Response:** ` prefix from the first line; the constructed sub-bullet re-adds `**Response:**` cleanly.
- Multi-line body / response → single-line each in the Legacy entry (callout formatting is deliberately lost per the spec).

Sub-bullet uses 2-space indent (matching CLAUDE.md markdown convention).

## Phase 3: Dry-Run Preview

ALWAYS emit the preview — both dry-run and execute modes produce this table. Execute mode then proceeds to Phase 4; dry-run stops here.

Per-file preview table:

```
### Sweep preview — threshold: [days] days

| File | Candidates | Preserved | Pinned | Fresh | Oldest addressed | Sections touched |
|------|-----------|-----------|--------|-------|------------------|-------------------|
| Theses/NVDA - Nvidia.md | 14 | 2 | 1 | 3 | 2025-08-15 | Bull Case (6), Catalysts (4), Industry Context (3), Risks (1) |
| Theses/BESI - BE Semiconductor.md | 6 | 0 | 0 | 1 | 2025-09-22 | Industry Context (4), Bull Case (2) |
| Sectors/Semiconductors.md | 3 | 1 | 0 | 0 | 2025-07-01 | Competitive dynamics (2), Macro shifts (1) |

Totals: 23 candidates across 3 files | 3 preserved | 1 pinned | 4 fresh (skipped)
```

Column semantics:
- **Candidates**: addressed callouts ≥ threshold without `[[pinned]]` marker → would be swept.
- **Pinned**: any callout (fresh or addressed) with `[[pinned]]` — skipped regardless of age. Persistent revisit slot.
- **Fresh**: unaddressed callouts without `[[pinned]]` — never eligible (not in scope for sweep).
- **Sections touched**: breakdown of candidate origins.
- *Legacy `[[preserve]]` markers* (deprecated 2026-04-29) are still honored as skips during the transition window; surfaced as a separate column when present, with a migration hint.

**If zero candidates anywhere**: `No callouts eligible for sweeping. Threshold [days]d reached zero addressed callouts across [N] files. Nothing to do.` Stop (both dry-run and execute modes exit cleanly).

**Dry-run mode terminates here** — no snapshots, no writes, no Log entries. Report: `ℹ️ Dry-run complete. Re-run without dry-run flag to execute.`

## Phase 4: Execute (skipped in dry-run)

### 4.1: Generate shared batch ID

Generate `HHMMSS` once at Phase 4 entry:

```bash
HHMMSS=$(date +%H%M%S)
TODAY=$(date +%Y-%m-%d)
BATCH_ID="callout-sweep-$TODAY-$HHMMSS"
```

Reused across all per-thesis snapshots in this run so `/rollback` can cascade.

### 4.2: Per-file snapshots (parallel batch)

For each file with ≥1 candidate, issue ONE Bash block with parallel `cp` + `wait`:

```bash
mkdir -p _Archive/Snapshots
pids=()
cp "Theses/NVDA - Nvidia.md" "_Archive/Snapshots/NVDA - Nvidia (pre-callout-sweep $TODAY-$HHMMSS).md" & pids+=($!)
cp "Theses/BESI - BE Semiconductor.md" "_Archive/Snapshots/BESI - BE Semiconductor (pre-callout-sweep $TODAY-$HHMMSS).md" & pids+=($!)
cp "Sectors/Semiconductors.md" "_Archive/Snapshots/Semiconductors (pre-callout-sweep $TODAY-$HHMMSS).md" & pids+=($!)
# Bare `wait` returns 0 even if a background cp failed — wait on each PID so a
# failed snapshot is actually detected (§4.2 hard-abort depends on this).
snap_fail=0
for pid in "${pids[@]}"; do wait "$pid" || snap_fail=1; done
[ "$snap_fail" -ne 0 ] && { echo "❌ snapshot cp failed — aborting Phase 4 (no transformations applied)"; exit 1; }
```

Then, in one parallel Edit batch, add snapshot frontmatter to each new snapshot:

```yaml
snapshot_of: "[[<original path>]]"
snapshot_date: <TODAY>
snapshot_trigger: callout-sweep
snapshot_batch: <BATCH_ID>
```

`/rollback` trigger allowlist recognizes `callout-sweep` per the updated rollback SKILL.md.

**If any `cp` fails** → hard-abort Phase 4 entirely. Do NOT proceed to 4.3 with partial snapshots. Report the failure and release the lock.

### 4.3: Per-file transformation (sequential, one file at a time)

For each file with candidates, execute the following steps atomically. If any step within a file fails, abort that file and proceed to the next; partial-file recovery uses the snapshot created in 4.2.

#### 4.3a: Remove original callout blocks

For each sweep candidate in the file, use `Edit` to delete the entire callout block from the body. The block spans from `> [!<type>]` header line through the last `> ` quoted line before the next non-`> ` line.

**Block boundary precision**: the block is ONLY the contiguous `> `-prefixed lines. The trailing blank line AFTER the block (between the callout and the next content) is NOT part of the block — do not include it in `old_string`. Obsidian renders tightly-packed callouts without intervening blanks; the surrounding blank line is surrounding text, not block structure. Including the trailing blank in the deletion collapses legitimate paragraph separators.

**Edit strategy — primary path (unique blocks)**: `old_string = <full callout block WITHOUT trailing blank line>`, `new_string = ""`. Edit each candidate one-by-one (parallel Edits on the same file are not safe).

**Edit strategy — retry path (silent failure)**: after each Edit, re-grep the file for `> [!<type>] <fresh_date>` exact header. If still present → Edit silently failed. Retry with expanded context: include 1 line before and after the block in `old_string` (and mirror in `new_string` to preserve those lines).

**Edit strategy — fallback path (byte-identical blocks)**: if retry fails AND a grep reveals ≥2 matches of the block header in the file (indicating the callout was copy-pasted and multiple byte-identical blocks exist):

1. Abort in-place Edit attempts on THIS file only (other files in the batch proceed normally).
2. Mark the file for **line-range rewrite fallback**: Read the full file into memory (single Read), compute a new body by filtering out the line ranges captured during Phase 2.2 parsing (each candidate's parsed line range is `[header_line_num, last_quoted_line_num]`).
3. Emit a single `Write` of the filtered body back to the file path. This bypasses Edit's uniqueness requirement entirely — line numbers disambiguate identical content.
4. Proceed to Phase 4.3b on this file. Phase 4.4 verification probe still runs — mismatch still triggers the failure report.

**Second failure on non-duplicate case**: if Edit retry fails AND grep shows exactly 1 match still present (genuine silent-failure mystery, not a duplicate-content issue) → abort this file, snapshot restore path available via `/rollback`. Continue to next file in batch.

**Why a file-level Write fallback is safe**: Phase 4.2 created a per-file snapshot BEFORE any 4.3 edits. A Write-based rewrite is no more destructive than the Edit-based approach — both fully control the file's final state. Snapshot-based rollback works identically either way.

#### 4.3b: Construct or update the `## Legacy Callouts` section

Read the file's current state after 4.3a. Locate `## Legacy Callouts` heading:

**Case A: Section absent**

Insert a new `## Legacy Callouts` block above `## Log`:

```
## Legacy Callouts
<!-- Auto-managed by /archive-callouts. Addressed callouts older than the sweep threshold (default 180 days) are moved here from their original sections as plain bulleted entries: `- **<addressed-date>** · <type> · <section> · raised <fresh-date> → <body>` with a `**Response:**` sub-bullet. Sorted descending (newest first). Do NOT hand-edit. To exempt a callout from sweeping, add `[[pinned]]` to its header in-place. -->

<new entries sorted descending by addressed_date>

## Log
```

Edit anchor: `old_string = "## Log\n"`, `new_string = "## Legacy Callouts\n<!-- ... -->\n\n<new entries>\n\n## Log\n"`.

**Case A fallback**: if `## Log` is absent, Phase 0.3 already skipped this file. Should not reach here.

**Case B: Section present**

Merge new entries into the existing list, maintaining **descending** sort by the leading `**YYYY-MM-DD**` date (newest first). Re-render the entire section bullet list in sorted order.

Edit anchor: find the section's bullet list (every line starting `- **YYYY-MM-DD**` and any sub-bullet indented 2 spaces). Replace the full list with the merged-and-sorted list. Preserve the section heading and comment unchanged.

**Stable tie-break**: if two entries share the same addressed date, sort by raised date descending second, then by original position third (preserve scan order).

**Malformed existing entries — preservation-in-place contract**:

When parsing existing `## Legacy Callouts` entries for sort-merge, an entry is **malformed** if ANY of the following holds:

- Lead bold date missing (no `**YYYY-MM-DD**` at bullet start)
- Date unparseable (e.g., `**2026-0i-15**`, `**26-04-15**`, non-ISO format)
- Missing type label, section reference, or `raised YYYY-MM-DD` token
- Missing `**Response:**` sub-bullet with 2-space indent
- Sub-bullet date tokens inside response body fail to parse (non-fatal — only the parent entry's lead date matters for sort)

Handling:

1. **Preserve verbatim** — malformed entries survive the merge unchanged, NOT rewritten or reformatted.
2. **Position** — all malformed entries float to the TOP of the section, ABOVE all well-formed entries (easier to spot visually; `/lint #52` will flag them).
3. **Annotate once** — if the entry does not already carry a leading `<!-- malformed — see /lint #52 -->` HTML comment on the line directly above the bullet, insert one. Do NOT modify the entry itself. Idempotent: if the comment already exists, don't duplicate.
4. **Continue the sweep** — malformed existing entries NEVER block the sweep of new candidates. Phase 4.3a / 4.3b / 4.3c / 4.3d proceed for the file regardless of how many malformed entries exist.
5. **Report** — Phase 5 per-file report line includes `⚠️ N malformed legacy entries preserved in-place; run /lint #52 for details` when applicable.

Rationale: malformed entries indicate prior hand-editing or a partial-write failure on an earlier sweep. Neither scenario justifies aborting the current sweep or silently reformatting user edits. Surface them to `/lint`, sort the clean entries, proceed.

**Edit anchor for Case B merge**:
- `old_string` = the current section's bullet list verbatim (every `- **...` line and all 2-space-indented sub-bullets, up to but not including the blank line before `## Log`)
- `new_string` = the malformed-entries block (with `<!-- malformed -->` annotations) followed by a blank line followed by the sorted clean list

If the merged output is byte-identical to the current list (no new candidates AND no malformed-annotation inserts needed), skip the Edit entirely (no-op). Log: `ℹ️ [file] Case B no-op — no merge required.`

#### 4.3c: Append Log entry

Append to the file's `## Log` section a new dated entry:

```
### <TODAY>
- Callout sweep: <N> addressed callouts ≥<days>d swept to ## Legacy Callouts. Sections touched: <breakdown>. Safety snapshot: [[_Archive/Snapshots/<filename> (pre-callout-sweep <TODAY>-<HHMMSS>)]]
```

Where `<breakdown>` matches the Phase 3 table format: `Bull Case (6), Catalysts (4), ...`.

**Edit strategy — two cases**:

Before editing, grep the file for a `### <TODAY>` header within the `## Log` section. Two outcomes determine the Edit anchor.

**Case 4.3c.A: no `### <TODAY>` header in `## Log` today** — append a new dated section.

The Log section is always the LAST section of the file (per Thesis/Sector template canonical order). Append at end-of-file is safe.

- `old_string`: the last non-empty line of the current file body (after Phase 4.3a/4.3b edits have landed). Read the file's tail to find it — typically this is the last bullet of the most recent Log entry, or the `## Log` heading itself if the section is empty.
- `new_string`: `<old_string>\n\n### <TODAY>\n- Callout sweep: ...\n`

Anchor uniqueness concern: if the file's last line happens to be text that appears multiple times elsewhere (rare but possible), expand the anchor to include 2-3 preceding lines until unique.

**Case 4.3c.B: `### <TODAY>` header already exists in `## Log` today** — append bullet under existing header.

Another skill already wrote a Log entry today. Tier 2 append-only: NEVER re-order, NEVER create a second same-day header, NEVER insert between existing bullets.

- `old_string`: find the LAST bullet line under today's date header. Walk from `### <TODAY>` downward until either (a) the next `### ` date header, (b) the next `## ` section heading, or (c) end of file. The line immediately before that boundary is the last bullet.
- `new_string`: `<old_string>\n- Callout sweep: ...`

Verification: after the Edit, re-grep the Log section for the new bullet. If absent → Edit silently failed. Retry with expanded context (include the date header + all existing same-day bullets in `old_string`). Second failure → abort this file's Log append only; the 4.3a/4.3b edits have already landed. Report: `⚠️ [file] Phase 4.3c Log append failed — body changes persist, audit trail missing. /lint #53 will flag. Manual fix: append "Callout sweep: ..." bullet to ## Log section under today's date.`

**If `## Log` is absent entirely** — Phase 0.3 already skipped this file. Should not reach here. If reached (state corruption mid-skill), hard-abort this file with snapshot-restore recommendation.

Log prefix `Callout sweep:` is registered in `_shared/log-prefixes.md` entry #17 as skill-origin (drift-exclusion, propagation-skip per `/sync` Step 2.5 and Step 3e).

#### 4.3d: Update frontmatter

Add or update `last_callout_sweep: <TODAY>` in the file's frontmatter.

Edit strategy: if field exists, Edit replaces the value. If absent, insert before the closing `---` of the YAML block.

### 4.4: Verification probes (after all 4.3 sequences complete)

For each swept file, run ONE Bash probe:

```bash
for f in [swept files]; do
  echo "=== $f ==="
  # grep -cE (extended regex): the `{4}` interval quantifier is a LITERAL in BRE
  # (plain grep -c), so the prior probe matched nothing and always printed 0 → the
  # "dropped by exactly the candidate count" check passed even when 4.3a Edits
  # silently failed. -cE fixes the quantifier; `grep -c` already prints 0 on no
  # match, so the `|| echo 0` (which double-printed) is dropped.
  echo -n "Swept callouts remaining: "
  grep -cE "^> \[!.*\] [0-9]{4}-[0-9]{2}-[0-9]{2} → Addressed [0-9]{4}-[0-9]{2}-[0-9]{2}" "$f"
  echo -n "Legacy Callouts entries: "
  awk '/^## Legacy Callouts/,/^## Log/' "$f" | grep -c "^- \*\*[0-9]"
  echo -n "Today's Callout sweep entry present: "
  grep -cE "^- Callout sweep:.*$(date +%Y-%m-%d)" "$f"
done
```

Expected: for each file, swept-callouts-remaining should have dropped by exactly the candidate count, Legacy Callouts entries should have grown by exactly the candidate count, sweep Log entry should be 1.

On any mismatch: report `⚠️ Verification failed for [file]: expected [N] swept / got [actual]. Snapshot available at [[path]]. Review and consider /rollback.` Do NOT try to self-heal — snapshot restore is the correct path.

## Phase 5: Report

### 5.1: Summary table

```
## Callout sweep complete — threshold: [days] days

Run ID: [BATCH_ID]
Files modified: [N]
Callouts swept: [total]
Preserved (opt-out): [count]
Pinned (skipped by design): [count]
Fresh (not eligible): [count]
Verification: all passed | [list failures]

| File | Swept | Sections | Snapshot |
|------|-------|----------|----------|
| Theses/NVDA - Nvidia.md | 14 | Bull Case (6), ... | [[_Archive/Snapshots/NVDA - Nvidia (pre-callout-sweep ...)]] |
```

### 5.2: Next steps

- `→ Run /graph last to refresh wikilink adjacency ([[pinned]] markers won't trigger broken-link flags — already in allowlist).`
- `→ Run /lint to verify Legacy Callouts schema (checks #50-#53).`
- `→ To undo a specific file's sweep: /rollback [ticker or note name] → select (pre-callout-sweep ...) snapshot.`
- `→ To undo the whole run: /rollback [BATCH_ID] → cascade (a) restores every file to pre-sweep state in one transaction.`

### 5.3: Release lock

Final Bash block verifies ownership and releases:

```bash
# LOCK_FILE MUST match the scope acquired at 0.1: `.vault-lock` for vault-wide,
# `.vault-lock.TICKER` for scoped. Hardcoding `.vault-lock` stranded every scoped
# run's `.vault-lock.TICKER` until its timeout (blocking follow-on ticker skills).
LOCK_FILE="<paste-lockfile-path-captured-from-Step-0.1>"   # .vault-lock OR .vault-lock.TICKER
EXPECTED_TOKEN="<paste-token-captured-from-Step-0.1>"
if [ -f "$LOCK_FILE" ] && grep -q "token: $EXPECTED_TOKEN" "$LOCK_FILE"; then
  rm -f "$LOCK_FILE" && echo "=== LOCK RELEASED ($LOCK_FILE) ==="
else
  echo "⚠️ Lock ownership check failed at release — skipping rm to avoid stealing another skill's lock."
fi
```

Runs unconditionally (same pattern as `/clean`, `/deepen`) — dry-run, execute, and abort paths all release.

## Sweep Contract — Invariants

These invariants define what `/archive-callouts` guarantees. Consumer skills (`/sync`, `/brief`, `/lint`, `/rollback`, `/graph`) depend on them; do not break without updating every consumer:

1. **`## Legacy Callouts` is owned exclusively by `/archive-callouts`.** No other skill writes to this section. Users should not hand-edit (but the skill tolerates structural damage by re-sorting and re-validating on next sweep; `/lint #52` + `#53` catch irrecoverable damage).
2. **Section position is above `## Log`** unambiguously. The skill creates it there. `/lint #53` flags out-of-position sections as Nice to Have.
3. **Sort order is descending by addressed date.** Newest sweep at top. User-decided, locked in template + skill.
4. **Entry format is load-bearing**: `- **YYYY-MM-DD** · <type> · <section> · raised YYYY-MM-DD → <body>` + `**Response:**` sub-bullet. `/lint #52` enforces.
5. **Sweep never writes outside the target file** except: (a) per-target snapshot in `_Archive/Snapshots/`, (b) `last_callout_sweep:` frontmatter, (c) `Callout sweep:` Log entry in `## Log`. No sector propagation, no macro propagation, no `_hot.md` update, no `_graph.md` update.
6. **`[[pinned]]` is the opt-out marker (replaces deprecated `[[preserve]]` 2026-04-29).** Any callout with `[[pinned]]` — fresh or addressed — NEVER sweeps regardless of age. Added by user in-place, never authored by the skill. During the deprecation transition window the skill also honors `[[preserve]]` as a skip; `/lint #56` flags any remaining occurrences for migration.
7. **Fresh callouts without `[[pinned]]` are invisible to sweep.** Only addressed callouts (with `→ Addressed YYYY-MM-DD` token) are candidates. Pinned addressed callouts skip sweep by marker; pinned fresh callouts are also exempt (and not in scope anyway because they're unaddressed).
8. **Log prefix is `Callout sweep:`.** Registered in `_shared/log-prefixes.md` §17 as skill-origin drift-exclusion. Producer drift here breaks `/sync` Step 2.5 and Step 3e silently.
9. **Snapshot trigger name is `callout-sweep`** (hyphenated). `/rollback` recognizes this in its 2.5c non-manifest cascade path. Changing the trigger name without updating rollback breaks the cascade-by-batch-id lookup.
10. **Dry-run is the safe default when intent is ambiguous.** Empty arguments → vault-wide dry-run, never silent execute.

## Failure modes and recovery

| Failure | Recovery |
|---|---|
| Snapshot `cp` fails in 4.2 | Phase 4 aborts before any file edits. Lock releases. No damage. Re-run after resolving disk/permission issue. |
| Edit fails in 4.3a (callout removal) | That file's sweep aborts mid-transform. Per-file snapshot exists at `_Archive/Snapshots/[file] (pre-callout-sweep ...)`. Restore via `/rollback`. Other files in the batch are unaffected. |
| Edit fails in 4.3b (Legacy Callouts insertion) | Same as above — per-file snapshot restores the state before 4.3a ran. |
| Edit fails in 4.3c (Log append) | Thesis has Legacy Callouts populated but no audit trail. `/lint #53` catches (Legacy entries without matching Log entries). Manual fix: append Log entry per Phase 4.3c format, or `/rollback` to pre-sweep snapshot. |
| Edit fails in 4.3d (frontmatter) | Sweep is body-complete; only hygiene metadata is stale. `/lint #50` surfaces missing `last_callout_sweep:` on next run. Low severity. |
| Verification probe mismatch in 4.4 | Reported to user. No self-heal. Snapshot restore via `/rollback`. |
| Lock ownership lost mid-run (`LOCK_STOLEN`) | Abort immediately. Report files already swept (completed 4.3 sequences) + files abandoned. User decides: keep partial progress, or `/rollback` the batch. |

## Design notes

Design rationale lives in `.claude/skills/archive-callouts/RATIONALE.md`:
- §1 — Why in-note archive, not external `_Archive/Callouts/*.md`
- §2 — Why descending sort (newest first)
- §3 — Why 180-day default threshold
- §4 — Why `warning` label for `[!error]` callout type
