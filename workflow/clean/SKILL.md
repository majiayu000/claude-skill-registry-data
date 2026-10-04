---
name: clean
description: Delete old snapshots from _Archive/Snapshots/. Accepts a day threshold (default 180). Also `daily-intel [days]` mode — prune auto-generated n8n scanning surfaces (news briefs, X dashboards) from Daily Intel/ older than 90 days. Use when user says "clean", "clean snapshots", "delete old snapshots", "clean daily intel", or when $lint flags stale snapshots.
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$clean`, or infer them from the user's request when this skill is invoked implicitly.

Delete snapshots older than a given threshold from `_Archive/Snapshots/`.

## Arguments (6.9 — orphan handling)

`SKILL_ARGS` patterns:
- **Number of days** (e.g., `90`, `30`): age-based cleanup. Default: **180** if no argument provided. Orphan snapshots (source file missing) are **PROTECTED by default** — reported but not deleted. See Step 2c.
- **`orphans`** (literal word): delete only orphan snapshots, regardless of age. Skips age-based cleanup entirely.
- **Number of days + `--include-orphans`** (e.g., `180 --include-orphans`): standard age-based cleanup PLUS delete orphans. Explicit opt-in.
- **`inbox`** (literal word): delete files in `_Inbox/processed/` older than 180 days (the default). Skips snapshot cleanup entirely. The source URL/path is preserved in the corresponding `Research/*.md`'s `source:` frontmatter, so processed inbox files are recoverable in principle. Per-file safety net: skip if no corresponding Research note exists (means the original `$ingest` did not complete cleanly — the source is still authoritative). See Step 2e.
- **`inbox [days]`** (e.g., `inbox 90`, `inbox 30`): same as `inbox` mode with custom age threshold.
- **`daily-intel [days]`** (e.g., `daily-intel`, `daily-intel 60`) — 2026-07-20: delete auto-generated scanning surfaces in `Daily Intel/` (n8n news briefs + X dashboards) older than the threshold (default **90**). Skips snapshot cleanup entirely. These files are regenerable machine output (n8n Workflows 3 + 5), never hand-edited, and never referenced by `propagated_to:` chains — deletion is safe by construction. Safety nets: (a) filename must match the n8n output patterns (`* - Daily intel - n8n.md`, `* - News digest - n8n.md`, `* - X Dashboard.md`) — anything else in the folder is user-created and PROTECTED (report, never delete); (b) `.data/news_stories/*.json` is NEVER touched by this mode — it is the `$retro` backtest corpus, not a scanning surface. Execution: enumerate matching files with date-prefix older than threshold → report the list + count + protected non-matching files → delete on the standard report-before-delete flow (Step 3's pattern) → release lock.

**Universal closure-snapshot floor** (applies to ALL modes including `orphans` and `--include-orphans`): pre-closure thesis snapshots from `$prune` Stage 1 or `$status active→closed` Step 3.1 whose matching manifest's `completed_date:` is within 30 days are PROTECTED. No `$clean` argument override — the only path to delete is to wait for the floor to expire OR `rm` the snapshot manually with full awareness of the consequence (closure becomes unrecoverable via `$rollback`). See Step 2d for detection and Step 3 for reporting.

Parse patterns in this order:
```
if SKILL_ARGS first token == "inbox" → inbox-cleanup mode; second token (optional integer) overrides 180-day default; skip Steps 1-4 entirely (snapshots untouched), execute Step 2e + Step 3.5 + Step 4.5 instead
elif SKILL_ARGS first token == "daily-intel" → daily-intel mode; second token (optional integer) overrides 90-day default; skip Steps 1-4 entirely (snapshots untouched), execute per the daily-intel argument spec above
elif SKILL_ARGS == "orphans" → orphans-only mode
elif SKILL_ARGS ends with "--include-orphans" → age + orphans mode; strip flag to get days
elif SKILL_ARGS is integer → age-only mode (default orphans PROTECTED)
else → default age-only mode (180 days; orphans PROTECTED)
```

## Step 0: Pre-flight

Acquire a `vault-wide` scope lock per `.agents/skills/_shared/preflight.md` Procedure 1. Timeout budget: 5 minutes. Capture the token emitted at Step 0.1, verify ownership (Procedure 1.5) at every subsequent shell block, release explicitly in the final reporting shell block.

## Step 1: Inventory Snapshots

List all files in `_Archive/Snapshots/`:
```bash
find _Archive/Snapshots/ -name '*.md' -type f | sort
```

If no files found, report "No snapshots exist — nothing to clean." and stop.

## Step 2: Parse Ages and Safety Net Check

### 2.0: Single-Bash frontmatter extraction (replaces per-file Reads)

Run ONE shell block that extracts every snapshot's frontmatter fields into a single pipe-delimited table. This collapses what was N serial Reads into 1 tool call regardless of snapshot count (hundreds of snapshots → same cost as one).

```bash
# Verify lock ownership first (preflight §1.5), then extract everything in one pass.
for f in _Archive/Snapshots/*.md; do
  [ -f "$f" ] || continue
  # head -40 bounds I/O; every skill writes frontmatter in the first ~30 lines
  head -40 "$f" | awk -v path="$f" '
    BEGIN {
      in_fm=0; type=""; sd=""; so=""; sb=""; status=""; cd=""
      batch=""; new_value=""; ticker=""
    }
    NR==1 && /^---$/ { in_fm=1; next }
    in_fm && /^---$/ { in_fm=0; exit }
    in_fm && /^type:/            { type=$2 }
    in_fm && /^snapshot_date:/   { sd=$2 }
    in_fm && /^snapshot_of:/     { so=$2; for(i=3;i<=NF;i++) so=so" "$i }
    in_fm && /^snapshot_batch:/  { sb=$2 }
    in_fm && /^status:/          { status=$2 }
    in_fm && /^completed_date:/  { cd=$2 }
    in_fm && /^batch:/           { batch=$2 }
    in_fm && /^new_value:/       { new_value=$2; for(i=3;i<=NF;i++) new_value=new_value" "$i }
    in_fm && /^ticker:/          { ticker=$2 }
    END {
      print path "|" type "|" sd "|" so "|" sb "|" status "|" cd "|" batch "|" new_value "|" ticker
    }
  '
done
```

This one block emits everything Steps 2a-2d need. Downstream classification consumes the table in-memory — no additional file reads for frontmatter. If source-file mtime comparison is needed (Safety Net Check), that uses `stat` in a second bounded shell block, not per-file Reads.

For each file in `_Archive/Snapshots/`, classify using the extracted data (`type:`, `snapshot_date:`, `snapshot_of:`, etc.):

### 2a: Non-snapshot artifact guard (must run first)

Some files in `_Archive/Snapshots/` are NOT snapshots — they are operational artifacts that other skills store there to survive across sessions:

- **`_prune-manifest`** files — written by `$prune` Stage 1.5 as a crash-recovery breadcrumb. Frontmatter has `type: prune-manifest` and carries no `snapshot_date:`. While a prune is in progress (or the prune crashed mid-run), this file is the user's only pointer to the batch that needs cascade-rollback.
- **`_sync-manifest`** files — written by `$sync` Step 2.9 (skeleton) then flipped by Step 7.5. Frontmatter has `type: sync-manifest` and carries no `snapshot_date:` (it carries `date:` and `completed_date:` instead). Consumed by `$rollback` Step 2.5b cascade detection. Aged by `$lint #41`.
- **`_compare-manifest`** files — written by `$compare` Phase 5.5c as a cross-sector atomicity record. Frontmatter has `type: compare-manifest`. Aged by `$lint #45`.
- **`_stress-test-manifest`** files (T3.1) — written by `$stress-test` Phase 4.6 to enable `$rollback` cascade-detection for append-only Log entries. Frontmatter has `type: stress-test-manifest`. Aged by `$lint #47`.
- **`_status-manifest`** files (T2.2) — written by `$status` Step 3.0.5 (skeleton) then flipped by Step 7.9. Frontmatter has `type: status-manifest`. Aged by `$lint #48`.
- **`_thesis-manifest`** files (H1) — written by `$thesis` Step 3.5 (skeleton) then flipped by Step 7.5. Frontmatter has `type: thesis-manifest`. Aged by `$lint #49`.
- **Future artifact types** — any file whose `type:` frontmatter is set to anything other than a snapshot flavor.

Detection rule: if the file's frontmatter has a `type:` field AND that value is not empty AND is not a snapshot-producer identifier (`snapshot`, or absent), treat the file as a non-snapshot artifact. Also treat any file missing `snapshot_date:` as non-snapshot (defensive — `$clean` cannot date-age what isn't dated).

Handling:
- **Skip the file entirely** for prune manifests with `status: in-progress` and for any other non-snapshot type.
- **For `type: prune-manifest` with `status: in-progress`**: add a line to the Step 3 report under a new category `🛑 Prune manifest (in-progress)` — the user should resolve the in-flight prune (via `$rollback` cascade) before letting `$clean` proceed, though `$clean` itself takes no action on this file.
- **For `type: prune-manifest` with `status: completed`** (5.2 retention fix): compute age from `completed_date:` frontmatter (not `date:`, which is the start of prune — `completed_date:` anchors retention).
  - **Age ≤ 30 days**: add to Step 3 report under `🔒 Completed prune manifest — in 30-day regret-recovery window` — do NOT delete regardless of `$clean` threshold. The manifest supports `$rollback` cascade-detection for neighbor Tier B Log entries if the user needs recovery.
  - **Age > 30 days**: eligible for deletion. Include in the Step 3 "Snapshots to delete" report under the regular age-based cleanup bucket. The 30-day floor is absolute — a user running `$clean 10` does NOT delete 15-day-old completed prune manifests (they are still in regret-window regardless of the user-supplied age threshold). A user running `$clean 180` DOES delete 40-day-old completed prune manifests (both windows satisfied).
  - **Missing `completed_date:`** (legacy manifests or flip-verification-failure manifests that flipped status without adding the timestamp): treat as age > 30 days for cleanup safety — these are stuck manifests whose prune unambiguously succeeded; cleanup is correct. Log `ℹ️ Legacy completed prune manifest (no completed_date:) — eligible for deletion.`
- **For any other non-snapshot type**: log `ℹ️ Skipped non-snapshot artifact: [path] (type: [value], no snapshot_date)`.

### 2b: Classify actual snapshots

For each file that passed the 2a guard (has `snapshot_date:`, no conflicting `type:`), calculate age in days from today's date.

Classify each snapshot:
- **Retained**: age <= threshold (kept)
- **Expired**: age > threshold — but check safety net status before marking for deletion (see below)

### Safety Net Check (expired snapshots only)

For each snapshot classified as Expired:
1. Extract `snapshot_of:` to identify the source file path
2. Check if the source file still exists at its original path
3. If source exists: check whether it was modified after `snapshot_date:` (compare file mtime against snapshot_date)
   - Modified after snapshot → reclassify as **🛡️ Active safety net** — this snapshot captures a pre-modification state that cannot be recovered otherwise. Exclude from deletion.
   - Not modified after snapshot → keep as **Expired** — snapshot is redundant (source unchanged since snapshot was taken)
4. If source file no longer exists (archived/deleted) → reclassify as **👻 Orphan** (6.9 fix). Handling depends on mode:
   - **Default age mode** (no `orphans` keyword, no `--include-orphans`): PROTECT — do NOT delete. List in Step 3 report under "Orphan snapshots (source file missing)" so the user can review. The snapshot may be the only recovery path if the source file was mistakenly deleted. **This is a deliberate fail-safe reversal from the legacy behavior where orphans were treated as "Expired" alongside stale-but-redundant snapshots.**
   - **`orphans` mode**: mark for deletion. This is the explicit opt-in.
   - **`--include-orphans` mode**: mark for deletion as part of age-based batch.

### 2c: Orphan enumeration (6.9 — explicit pass)

Orphans are identified by `snapshot_of:` pointing to a path that does NOT exist. Resolve the path:
- Wikilink form `"[[Theses/TICKER - Name]]"` → check `Theses/TICKER - Name.md`
- Wikilink form `"[[_Archive/TICKER - Name]]"` → check `_Archive/TICKER - Name.md`
- Plain path form `"Theses/TICKER - Name.md"` → check as-is

If the resolved path does not exist, the snapshot is an orphan.

**Why default-protect orphans**: the legacy "delete orphans as part of expired batch" behavior created an unrecoverable loss path for scenarios where a thesis was deleted manually (violating AGENTS.md "archive don't delete") — the snapshots were the user's only lingering audit trail, and `$clean` silently erased them along with genuinely-stale redundant snapshots. Default-protect surfaces orphans for review; the user can explicitly opt in via `orphans` or `--include-orphans` once they've inspected the reported list.

### 2d: Closure-snapshot 30-day regret-recovery floor (universal — applies to age, orphans, and --include-orphans modes)

The pre-closure thesis snapshots created by `$status active→closed` (Step 3.1) and `$prune` Stage 1 become orphans the moment the source thesis file moves to `_Archive/` (the snapshot's `snapshot_of: "[[Theses/TICKER - Name]]"` target is now missing). Without protection, `$clean orphans` and `$clean N --include-orphans` silently destroy the recovery path for any recent closure within seconds of the closure landing. `$lint` cannot retroactively recreate deleted snapshots; `git restore` only helps if the snapshot was committed before deletion. This 30-day floor universally protects closure snapshots regardless of `$clean` mode.

**Detection procedure** — runs for every snapshot classified as 👻 Orphan in 2c:

1. Read snapshot's `snapshot_batch:` frontmatter. Skip protection check if absent (legacy snapshot).
2. Search `_Archive/Snapshots/` for a manifest whose `batch:` matches the snapshot's `snapshot_batch:`:
   - **Status manifest match** (`type: status-manifest`): closure detection requires the manifest's `new_value:` to contain the literal token `closed` (covers `new_value: closed`, `new_value: "closed"`, and compound forms like `"monitoring → closed"`). Match → it's a `$status active→closed` (or `monitoring→closed`) snapshot.
   - **Prune manifest match** (`type: prune-manifest`): every `$prune` Stage 1 snapshot for an Intended Closure target is a closure snapshot by construction. Match → confirmed closure snapshot.
3. If matched manifest found AND manifest's `status: completed` AND `completed_date:` is within 30 days of today → **PROTECT** under closure-floor regardless of `$clean` mode (age, `orphans`, `--include-orphans`).
4. If manifest's `status: in-progress` → also PROTECT (the closure transaction is unresolved; deleting recovery snapshots compounds the failure state). Surface separately under Step 3 reporting.
5. If manifest matched but `completed_date:` is missing (legacy or flip-verification miss) → treat as completed-30-days-ago for cleanup (no protection). Log: `ℹ️ Closure manifest [batch] missing completed_date: — treating snapshot as past regret window. Verify manually if you need the snapshot.`
6. If no matching manifest → snapshot's closure status cannot be confirmed. Treat as standard orphan (default-protected; deletable via `$clean orphans` per 2c).

**Reporting**: protected closure snapshots appear under a dedicated Step 3 section (see below) so users see exactly which closures they cannot yet aggressively prune from. The protection cannot be overridden by `$clean` flags by design — the user's only path to delete a 30-day-floored closure snapshot is to wait for the floor to expire OR to manually `rm` the snapshot (with full awareness of the consequence).

**Why universal across modes**: the prior $prune-manifest 30-day floor (2a) only protected the *manifest* file. It did NOT protect the per-thesis snapshots that the manifest references. `$clean orphans` could delete a 5-day-old prune's per-thesis snapshots while preserving the manifest — leaving the user with a manifest body listing closures they could no longer restore. This 2d floor closes that gap and extends symmetric protection to `$status` closures (which have no manifest-floor analog).

### 2e: Inbox processed-file enumeration (inbox mode only)

**Only runs when `SKILL_ARGS` first token == `inbox`.** Skips Steps 1, 2.0, 2a–2d entirely (snapshots untouched in inbox mode).

`_Inbox/processed/` accumulates source files moved by `$ingest` Mode C after a successful research-note write. The source URL/path remains the canonical provenance record on the matching `Research/*.md` (`source:` frontmatter), so processed files become redundant once the corresponding research note is durable. `$clean inbox` enumerates candidates with a per-file safety net keyed to research-note existence.

**Threshold**: second `SKILL_ARGS` token if integer; otherwise default 180. (Same default as snapshot age.)

**Per-file enumeration** — single shell block:

```bash
THRESHOLD_DAYS=${THRESHOLD_DAYS:-180}
TODAY_EPOCH=$(date +%s)
for f in _Inbox/processed/*; do
  [ -f "$f" ] || continue
  MTIME_EPOCH=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null)
  AGE_DAYS=$(( (TODAY_EPOCH - MTIME_EPOCH) / 86400 ))
  echo "$f|$AGE_DAYS"
done
```

**Per-file research-note existence probe** (safety net):

For each candidate, the LLM derives the most plausible research-note name from the inbox filename and confirms via `Glob`:
1. Strip the inbox filename's extension. Strip leading date prefix if present (`YYYY-MM-DD - ...`).
2. `Glob Research/*<keyword>*.md` against tokens from the stripped name (use 2-3 of the most distinctive tokens, dedup whitespace).
3. If at least one candidate Research note exists AND its `source:` frontmatter resolves to (a) the absolute inbox file path, (b) the original URL the file was downloaded from (visible in the research note `source:` line), or (c) a partial-name match flagged advisory — mark as `safe_to_delete`.
4. If no Research note matches → mark as `unsafe (no Research note found)`. The original `$ingest` may have been interrupted between writing the inbox file and creating the Research note; deleting now would lose the source. **Do NOT mark for deletion.**
5. If multiple Research notes match ambiguously → mark as `ambiguous`; surface to user under a separate report bucket.

**Classification**:
- **Inbox to delete**: `age_days >= threshold` AND `safe_to_delete`.
- **Inbox protected (under threshold)**: `age_days < threshold`.
- **Inbox unsafe (no matching Research note)**: any age. PROTECTED — listed for user review.
- **Inbox ambiguous (multiple matches)**: any age. PROTECTED — listed for user review.

## Step 3: Report Before Deletion

Present a summary table. **Do NOT delete anything yet.**

### Snapshots to delete (older than N days)
| File | Snapshot Date | Age (days) | Source Note |
|------|--------------|------------|------------|
| `filename.md` | YYYY-MM-DD | X | `snapshot_of` value |

### 🛡️ Active safety nets (excluded from deletion)
| File | Snapshot Date | Age (days) | Source Note | Source Modified |
|------|--------------|------------|------------|----------------|
| `filename.md` | YYYY-MM-DD | X | `snapshot_of` value | YYYY-MM-DD |

These snapshots exceed the age threshold but their source files were modified after the snapshot was taken. Deleting them removes the only recovery path to the pre-modification state. To override, re-run `$clean` targeting specific filenames.

### Snapshots retained (within threshold)
| File | Snapshot Date | Age (days) |
|------|--------------|------------|

### 🛑 Prune manifest (in-progress) — do NOT clean
| File | Batch ID | Status |
|------|---------|--------|

These represent in-flight `$prune` operations. Resolve the batch first (`$rollback` cascade via any ticker in the batch, then delete the manifest) before running `$clean` again.

### 🔒 Completed prune manifests — in 30-day regret-recovery window (PROTECTED)
| File | Batch ID | Completed Date | Days remaining |
|------|---------|---------------|---------------|

These manifests are within 30 days of `completed_date:` and are retained to support `$rollback` cascade-detection if the user decides to undo an approved closure. `$clean` does NOT delete these regardless of age threshold.

### 🧹 Completed prune manifests — eligible for deletion (>30 days old)
| File | Batch ID | Completed Date | Age (days) |
|------|---------|---------------|------------|

These manifests have exceeded the 30-day regret-recovery window. `$clean` deletes these alongside regular age-based cleanup (if snapshot threshold is also satisfied). Manifests with missing `completed_date:` (legacy or flip-verification failures) are also included here — those are stuck completed manifests whose prune unambiguously succeeded.

### 👻 Orphan snapshots (source file missing)
| File | Snapshot Date | Age (days) | `snapshot_of` (missing) |
|------|--------------|------------|--------------------------|

These snapshots reference source files that no longer exist in the vault. Possible causes: (a) source was manually deleted (violates AGENTS.md archive-don't-delete rule — investigate), (b) source was archived and the archive was later renamed (snapshots track original path), (c) legacy snapshot from a pre-6.9 vault where the convention drifted.

- **Default age mode**: orphans are PROTECTED and listed here only. Not deleted.
- **To delete orphans**: run `$clean orphans` (orphans only, any age) or `$clean [days] --include-orphans` (age + orphans).

### 🛟 Closure snapshots — in 30-day regret-recovery window (PROTECTED across all modes — 2d)

| File | Closure Type | Batch ID | Closure Completed | Days remaining |
|------|-------------|----------|-------------------|---------------|

Pre-closure thesis snapshots from `$prune` Stage 1 or `$status active→closed` Step 3.1, where the matching manifest's `completed_date:` is within 30 days of today. These snapshots are the only recovery path for `$rollback TICKER` if the user regrets the closure. **Protected universally** — `$clean orphans` and `$clean [days] --include-orphans` cannot delete these. Becomes eligible for deletion automatically once 30 days have elapsed since `completed_date:`.

If you need to delete one of these urgently (e.g., disk pressure + already verified backup elsewhere), `rm` the snapshot manually with full awareness that the closure becomes unrecoverable.

### 🛟 Closure snapshots — manifest in-progress (PROTECTED — 2d)

| File | Manifest Path | Manifest Batch ID |
|------|--------------|-------------------|

Snapshots whose matching `_status-manifest` or `_prune-manifest` is still `status: in-progress`. The closure transaction did not complete cleanly — the snapshot is the sole rollback path. Resolve the in-progress manifest first (run `$rollback` cascade per the manifest's recovery guidance, OR manually flip the manifest after spot-checking that work landed) before re-running `$clean`.

### Non-snapshot artifacts (skipped)
| File | Type |
|------|------|

**Total**: X to delete, Y active safety nets (protected), Z retained, V orphans (protected by default | slated for deletion), P prune manifests in regret-window (protected), Q prune manifests eligible for deletion, R closure snapshots in regret-window (PROTECTED across all modes — 2d), S closure snapshots with in-progress manifests (PROTECTED — 2d), W non-snapshot artifacts (skipped).

### 📥 Inbox files to delete (inbox mode only — older than threshold AND matching Research note exists)

| File | Age (days) | Matched Research note |
|------|-----------|------------------------|

These files are processed sources whose corresponding `Research/*.md` exists and carries the source provenance in its `source:` frontmatter. Deleting the inbox copy is safe — the research note (and the original URL within it) preserves traceability.

### 📥 Inbox files protected (under threshold)

| File | Age (days) |
|------|-----------|

### ⚠️ Inbox files unsafe — no matching Research note (PROTECTED, manual review)

| File | Age (days) | Reason |
|------|-----------|--------|

These processed-inbox files have no obvious matching Research note. Likely cause: the original `$ingest` was interrupted between moving the source and writing the Research note. Do NOT delete — the inbox file may be the only intact copy of the source. Inspect manually: either re-run `$ingest [path]` (which will short-circuit on URL-dedup if the matching Research note exists under a different name) OR delete after manual confirmation.

### 📥 Inbox files ambiguous — multiple Research-note matches (PROTECTED, manual review)

| File | Age (days) | Candidate matches |
|------|-----------|-------------------|

Multiple Research notes plausibly cite this inbox file. PROTECTED until disambiguated.

## Step 4: Confirm and Execute

**Wait for user confirmation before deleting.**

**Snapshot modes (default age, `orphans`, `--include-orphans`)** — if confirmed, delete each expired snapshot:
```bash
rm "_Archive/Snapshots/[filename]"
```
Report: "Deleted X snapshots. Y remain."

**Inbox mode** — if confirmed, delete each safe inbox file:
```bash
rm "_Inbox/processed/[filename]"
```
Report: "Deleted X inbox files. Y unsafe (no Research note) preserved. Z ambiguous (multi-match) preserved. W under threshold."

Inbox mode never touches `_Archive/Snapshots/`. Snapshot modes never touch `_Inbox/processed/`. The two modes are mutually exclusive at parse time.

## Step 5: Release lock

After Step 4's deletion and report, release the vault lock per `.agents/skills/_shared/preflight.md` §1.7 as the skill's FINAL shell block. Runs unconditionally — whether deletions proceeded, user declined confirmation, or there was nothing to delete.

```bash
# Lock release — verify ownership before rm (preflight §1.5)
LOCK_FILE=".vault-lock"
EXPECTED_TOKEN="<paste-token-captured-from-Step-0.1>"
if [ -f "$LOCK_FILE" ] && grep -q "token: $EXPECTED_TOKEN" "$LOCK_FILE"; then
  rm -f "$LOCK_FILE" && echo "=== LOCK RELEASED ==="
else
  echo "⚠️ Lock ownership check failed at release — skipping rm to avoid stealing another skill's lock."
fi
```
