---
name: obsidian-organizer
description: >
  Organize and normalize an Obsidian vault in a Zettelkasten, folder-first style.
  Use when asked to scan/analyze an Obsidian vault, generate Report.md and an executable Plan.md,
  normalize filenames (YYYYMMDD Title), merge YAML frontmatter (type/status/created/updated/tags/aliases/source),
  plan moves between top folders (00_Inbox/10_Literature/20_Permanent/30_Maps/40_Projects/90_Archive),
  fix wikilinks and markdown links after renames/moves, manage attachments in per-top-folder _assets,
  and apply changes with rollback via backups in 90_Archive/_organizer_backups.
---

# Goal & Principles

- Default to **dry-run**: generate `Report.md` + `Plan.md` without making changes.
- Never do irreversible deletes by default.
- **Single source of truth for execution**: `Plan.md` only.
- Apply is allowed even if `risk: high` exists, as long as the user confirms.
- Rollback strategy **B**: always backup before apply, rollback by restoring backups.
- Conservative Inbox: if type cannot be reliably determined, keep note in `00_Inbox` (no move).

# Vault Conventions (Zettelkasten / folder-first)

## Top folders (fixed)

- `00_Inbox/`
- `01_Daily/`
- `10_Literature/`
- `20_Permanent/`
- `30_Maps/`
- `40_Projects/`
- `90_Archive/`
- `99_Plugconfig/`

## Attachments

- Per-top-folder assets subfolder name is fixed: `_assets/`
  - `00_Inbox/_assets/`
  - `10_Literature/_assets/`
  - `20_Permanent/_assets/`
  - `40_Projects/_assets/`
  - `01_Daily/_assets/` (optional)

## Backup / rollback (strategy B)

- Backup root directory (fixed): `90_Archive/_organizer_backups/`
- Each apply creates a timestamped backup folder:
  - `90_Archive/_organizer_backups/YYYYMMDD-HHMMSS/`
- Backup all impacted notes and any assets that may change/move.
- Rollback restores backed up files to their original vault-relative paths (overwrite current).

# Naming Rules

## Note filename pattern

- `YYYYMMDD_{title}.md`

Title normalization:

- trim leading/trailing spaces
- collapse multiple spaces into one
- replace invalid filename chars `/:\\*?"<>|` with `-`
- optionally replace `:` with `：`

Conflict strategy:

- If target exists, use incremental suffix: `(2) (3) ...`

# Frontmatter Rules (merge, preserve unknown)

## Supported schema (recommended order)

```yaml
type: inbox|daily|literature|permanent|map|project|archive
status: seed|draft|evergreen|archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
aliases: []
source: ""
```

Rules:

- `mode = merge`: only fill missing keys; do not delete unknown keys.
- `created`: set only if missing.
- `updated`: set when this skill changes the note content/metadata.
- `source`: recommended for literature; if missing, report and plan patch (MED by default).

Default status by type:

- inbox: seed
- daily: seed
- literature: draft
- permanent: draft
- project: draft
- map: evergreen
- archive: archived

# Type → Folder Mapping

- inbox → `00_Inbox/`
- daily → `01_Daily/`
- literature → `10_Literature/`
- permanent → `20_Permanent/`
- map → `30_Maps/`
- project → `40_Projects/`
- archive → `90_Archive/`

# Inbox Conservative Policy (MUST)

When scanning/organizing notes under `00_Inbox/`:

- If type cannot be reliably determined:
  - do NOT generate move ops
  - allowed ops: `frontmatter`, `rename`, link fixes caused by rename
- If classification is reliable (e.g. has `source/url/doi/isbn` → literature; has `project` frontmatter → project):
  - generate `frontmatter` + `move` (cross-top => HIGH)

# Links Policy

For any rename/move:

- fix wikilinks `[[...]]`
- fix markdown links `[](...)`
  Prefer to inline link fix flags inside the rename/move op (`fixLinks`) instead of separate linkFix ops (v1).

# Non-Markdown Filetypes (.canvas / .base / .excalidraw.md)

## Goals

- Treat `.excalidraw.md` as Markdown notes (allowed to rename/move/merge frontmatter).
- Treat `.canvas` and `.base` as non-Markdown artifacts: **do not rewrite by default**.

## Rules

- `*.excalidraw.md`:
  - Allowed: frontmatter merge, rename, move.
  - Fix inbound references in other notes like normal `.md`.

- `*.canvas`:
  - Allowed: rename, move.

- `*.base`:
  - Allowed: rename, move.

## Reporting additions (Report.md)

Add these codes in Findings when applicable:

- CANVAS-BROKEN-REF (best-effort)
- BASE-BROKEN-REF (best-effort)
- EXCALIDRAW-BROKEN-REF (if detectable)
- NONMD-SKIPPED (INFO transparency)

# Outputs Overview (MUST)

This skill produces (at minimum):

- `Report.md` (v1, human-readable + machine-parseable)
- `Plan.md` (v1, executable; single source of truth for apply)

Default scan scope:

- include: all except excluded folders
- exclude by default: `90_Archive/`, `99_Plugconfig/`

High risk threshold:

- backlinks/occurrences >= 20 => HIGH impact

Orphan definition (v1):

- orphan = 0 backlinks AND not linked from any Map
- Map set = all `.md` files under `30_Maps/`

# Report.md v1 Specification (MUST)

## Header (MUST)

Report begins with an HTML comment containing YAML under root key `report:` including:

- version (1), generatedAt (ISO-8601 + timezone), timezone, vaultRoot, configPath
- scope include/exclude
- thresholds.highRiskBacklinks = 20
- definitions.orphan = { backlinks: 0, notInAnyMap: true }
- notesScanned, assetsScanned

## Summary (MUST)

Include a fixed metric summary (table preferred), including at least:

- Notes scanned
- Notes with changes suggested
- High risk items
- Missing frontmatter
- Type missing/unknown
- Status invalid/missing
- Filename nonconforming
- Duplicate title candidates
- Broken wikilinks
- Broken markdown links
- Orphan notes (0 backlinks AND not in any Map)
- Assets scanned
- Unreferenced assets
- Missing assets (referenced but not found)

## Findings (MUST): machine-parseable line format

Each finding MUST be a single line:

- [SEVERITY][CODE] <message> | path=<vault-relative-path> | refs=<n> | extra=<k=v;...>

Where:

- SEVERITY ∈ HIGH|MED|LOW|INFO
- refs = backlinks count (for note impact) OR occurrences count (for link/asset issues)
- Always include path=. Include refs= when it matters (esp for high risk).

### Severity rules (v1)

Hard rules:

- MOVE-CROSS-TOP => HIGH
- RENAME-CONFLICT => HIGH
- ASSET-MIGRATION => HIGH
- BROKEN-WIKILINK or BROKEN-MD-LINK with refs>=20 => HIGH

Default suggestions:

- missing/invalid frontmatter keys => MED
- filename nonconform => MED
- orphan => INFO

### CODE table (v1 fixed)

Frontmatter / Schema

- FRONTMATTER-MISSING
- FRONTMATTER-MISSING-KEYS
- FRONTMATTER-INVALID-VALUE
- TYPE-MISSING
- TYPE-UNKNOWN
- STATUS-MISSING
- STATUS-INVALID
- SOURCE-MISSING

Naming / Location

- FILENAME-NONCONFORM
- RENAME-CONFLICT
- WRONG-FOLDER-BY-TYPE
- MOVE-CROSS-TOP

Links

- BROKEN-WIKILINK
- BROKEN-MD-LINK
- LINK-AMBIGUOUS

Assets

- ASSET-UNREFERENCED
- ASSET-MISSING
- ASSET-MIGRATION
- CANVAS-BROKEN-REF
- BASE-BROKEN-REF
- EXCALIDRAW-BROKEN-REF
- NONMD-SKIPPED

Graph / Maps

- ORPHAN
- MAP-COVERAGE

Duplicates (heuristic)

- DUPLICATE-TITLE-CANDIDATE
- DUPLICATE-CONTENT-CANDIDATE

# Plan.md v1 Specification (MUST)

## Header (MUST)

Plan begins with an HTML comment containing YAML under root key `plan:` including:

- version (1), generatedAt, timezone, vaultRoot, configPath
- dryRun (default true)
- backup.strategy = B
- backup.dir = `90_Archive/_organizer_backups/YYYYMMDD-HHMMSS`

## Executable ops (MUST): organizer-op blocks only

Plan execution MUST only read fenced code blocks with language tag `organizer-op`.
These blocks contain YAML and are the only source for machine actions.

Each op MUST include:

- id: op_0001...
- kind: frontmatter | rename | move (v1 core)
- risk: normal | high

Op ordering (MUST):

1. frontmatter
2. rename
3. move
4. optional asset/link ops
5. optional maps update

Core op shapes:

frontmatter:

- path
- mode: merge
- set (optional)
- setIfMissing (optional)
- setAlways (optional)

rename:

- from
- to
- fixLinks: { wikilinks: true, markdownLinks: true }

move:

- from
- to
- assets (required if moving referenced assets across top folders):
  - moveReferenced: true
  - fromDir: <top>/\_assets
  - toDir: <top>/\_assets
- fixLinks: { wikilinks: true, markdownLinks: true }

# Report → Plan generation rules (v1: generate all ops)

- For every actionable issue detected in Report, generate corresponding `organizer-op` in Plan.
- HIGH risk items are still generated; they are only marked as `risk: high`.
- Conservative Inbox: no move op unless classification is reliable.

Mapping examples:

- FRONTMATTER-_/ TYPE-_ / STATUS-\* / SOURCE-MISSING => frontmatter op
- FILENAME-NONCONFORM / RENAME-CONFLICT => rename op
- WRONG-FOLDER-BY-TYPE / MOVE-CROSS-TOP => move op (cross-top => HIGH)
- BROKEN-\* => preferably handled via fixLinks inside rename/move; otherwise separate linkFix (optional)

# Apply & Rollback (v1)

Apply prerequisites (MUST):

1. Create backup dir under `90_Archive/_organizer_backups/YYYYMMDD-HHMMSS/`
2. Backup all impacted files (notes + assets). Preserve vault-relative paths in backup.
3. Validate Plan.md: all organizer-op blocks parse successfully; otherwise stop.
4. Execute ops in order; stop on first failure and report op id.

Rollback (MUST):

- Restore from backup directory by copying backed-up files back to their original vault-relative paths (overwrite).

# Trigger phrases / intents (examples)

Use this skill when the user asks to scan/organize an Obsidian vault, especially:

- “帮我整理一下 Obsidian vault / 笔记库”
- “扫描 Obsidian，输出 Report.md + 可执行 Plan.md（先别改）”
- “把文件名统一成 YYYYMMDD 标题”
- “批量补全/规范 frontmatter（type/status/created/updated/tags/aliases/source）”
- “找孤儿笔记（0入链且不在任何 Map）、断链、重复标题、未引用附件”
- “重命名/移动后修复 wikilinks / markdown links”
- “按 Zettelkasten（Inbox/Literature/Permanent/Maps/Projects）整理”
- “附件放到每个顶层文件夹的 \_assets 并修复引用”
- “生成整理计划并可回滚（90_Archive/\_organizer_backups）”

Keywords that strongly indicate this skill:

- Zettelkasten, folder-first, 00_Inbox/10_Literature/20_Permanent, \_assets, dry-run, Plan.md executable, backup rollback
