---
name: vault-cleanup-studio
description: Find vault hygiene issues — stub notes, oversized notes, duplicates, stale attachments — and fix them ONLY after explicit permission per change. Use when the user says "clean up the vault", "find junk notes", "vault health check", or "what's bloating the vault". NOT for link/orphan repair (use vault-link-index) or structural drift like empty dirs and sync-conflict copies (run scripts/check_vault_structure.py).
---

# Cleanup Studio

Vault hygiene analysis tool. **Read-only by design** — always asks user permission before any action.

## Golden Rules

**NEVER auto-fix. ALWAYS ask permission.**

When reporting issues, Claude Code must:
1. Show the issue
2. Explain options
3. Ask "Would you like me to [action]?"
4. Wait for explicit confirmation

**Before deleting files, ALWAYS check recoverability:**
1. Is the file tracked by git? (`git ls-files <path>`)
2. Is the file in the daily backup? (Backup excludes `.mp4`, `.wav`, `.mov` — see `backup-vault.bat`)
3. If **neither git nor backup** → warn the user: "These files are NOT recoverable if deleted."
4. For batch deletions (>5 files), list the count and total size, and get explicit "yes delete" confirmation.

## Files

- **Script**: `80_Code/scripts/cleanup-studio.py` — content hygiene (this skill's detector)
- **Sibling scanner**: `D:/emptyos/scripts/check_vault_structure.py` — structural drift (NOT this skill)

## Division of labour — don't re-derive what a scanner already decides

Two scanners cover different axes. Run the structural one **first**; it settles the
mechanical cases deterministically so the triage below only handles judgment.

| Class | Owner | Why |
|---|---|---|
| Empty dirs, byte-identical sync-conflict copies (`name 2.md`), `.tmp`, aged zero-byte files | `check_vault_structure.py` | Content-lossless, classified `safe`, auto-purgeable |
| Undeclared top-level folders, divergent duplicate copies, non-empty `Untitled*.md` | `check_vault_structure.py` (`review` class) | It reports; a human decides. Never auto-touched |
| Oversized notes (raw size threshold) | `check_vault_structure.py` (`advisory`) | Mechanical size check |
| **Stub categorization** (old-journal vs dictionary vs truly-empty) | **this skill** | Needs domain judgment |
| **Huge-note expected-vs-actionable** classification | **this skill** | Needs to know what an OCR'd standard is |
| **Duplicate-name rename convention** + wikilink updates | **this skill** | Needs naming taste + link surgery |
| **Stale-attachment keep/delete** calls | **this skill** | Needs recoverability + intent |

```bash
# Structural pass first (report-only; --purge is a human-run act, never automatic)
python D:/emptyos/scripts/check_vault_structure.py
```

Exit code = number of `review` findings. If it flags a duplicate as byte-identical,
**don't** re-triage it below — it's already settled. Only bring pairs it calls
*divergent* into the Duplicates workflow.

## Commands

Run from vault root with `PYTHONIOENCODING=utf-8` on Windows:

```bash
# Quick summary
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py"

# Individual checks
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py" --stubs
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py" --huge
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py" --duplicates
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py" --stale

# Full lists (no truncation)
PYTHONIOENCODING=utf-8 python "80_Code/scripts/cleanup-studio.py" --stubs --all
```

## Smart Filtering (What the Script Already Handles)

The script automatically excludes false positives. Do NOT flag these as issues:

### Excluded from all scans
Folders: `.obsidian`, `.git`, `.claude`, `_claude`, `.claude_backup`, `node_modules`, `.pytest_cache`, `venv`, `venv_mac`, `__pycache__`, `.semantic_index`, `.smart-connections`, `.makemd`, `.space`, `.trash`, `temp-backup`

### Excluded from stubs
These are intentionally short notes, not real stubs:
- `$`-prefix notes (finance tracking)
- `#subscription` tagged notes
- Credential/API key notes (passwords, tokens, GitHub/Groq/OpenAI keys)
- Finance keywords in filename or body (税号, 信用卡, 银行, etc.)
- Pure-number bodies (account numbers, IDs)
- Attachment-only notes (just `![[...]]` embeds)
- Completed-task-only notes (only `- [x]` items)
- Social media account lists

### Excluded from duplicates
- Structural convention names: `_tracker` (DB Folder plugin index)

## Triage Workflow

### Stubs
After running `--stubs`, categorize results before acting:

| Category | Typical action |
|----------|---------------|
| Old journal entries (2015 etc.) | Keep — historical, just short days |
| Dictionary entries | Keep — valid vocab notes |
| Recipes | Keep — short recipes are fine |
| Archived notes | Keep — cold storage reference |
| Work notes with just headings | Expand or keep as placeholder |
| Truly empty / meaningless | Delete after confirming |

### Huge Notes
The `--huge` output groups notes by category and shows a breakdown. Most huge notes are **expected to be large**:

| Category | Expected? | Action |
|----------|-----------|--------|
| Cable rating references (OCR'd standards) | Yes | Keep — splitting loses context |
| HV sheath voltage papers (OCR'd) | Yes | Keep |
| University notes | Yes | Keep — completed coursework |
| English/PTE study banks | Yes | Keep — inherently large (机经) |
| Excalidraw drawings | Yes | Keep — binary-ish format |
| Book notes / Readwise | Yes | Keep — long-form content |
| Archived notes | Yes | Keep — already in archive |
| CBT/therapy logs | Yes | Keep — personal journals |
| **Notification log** | **No** | **Trim** — `_claude-notifications.md` grows unbounded |
| **Other** | **Check** | These are the actionable ones shown in detail |

Only the "Actionable" section of the output needs review.

### Duplicates
After running `--duplicates`, investigate each pair. **Skip any pair
`check_vault_structure.py` already classified as a byte-identical copy** — that's
`safe`-class structural litter, not a naming decision.

1. **Read both files** — are they identical or different?
2. If identical → keep canonical copy, replace other with a link
3. If different content, same name → rename with suffix/prefix:
   - Standard sections: `{standard}--{section}.md` (e.g., `tb880--01-introduction.md`)
   - Project-scoped: `{name}-{project}.md` (e.g., `README-atp-emtp.md`)
   - YouTube publishing vs creative: add `-yt` suffix
   - Job applications: add `-{company}` suffix
4. If different purpose, same name by convention → add to `STRUCTURAL_DUPLICATE_NAMES` in script
5. After renaming: **always search for and update wikilinks** (`Grep` + `Edit`)

### Stale Attachments
- Large files (>100KB): confirm with user before deleting
- Small files: can batch-review
- When in doubt, keep — storage is cheap

### Temp Backups
The `temp-backup/` folder is excluded from all scans. These are safety nets for file modifications. **Do not clean them up** — the verification cost (reading + diffing each pair) far exceeds the storage cost (~750 KB).

## Example Interaction

```
User: Clean up my vault

Claude: I'll scan for issues first.

[Runs --summary]

CLEANUP SUMMARY
  Stub notes:      31
  Huge notes:     166
  Duplicate names:  1
  Stale attachments: 125 (45 MB)

Which would you like to address first?
1. Review stub notes (31 — after smart filtering)
2. Review huge notes (166 — mostly expected, I'll show category breakdown)
3. Review duplicate names (1)
4. Review stale attachments (125, ~45 MB)

User: 1

Claude: [Runs --stubs, categorizes results, asks about each group]
```

## Proactive Behavior

Claude Code should:
- Offer cleanup analysis during weekly reviews
- Warn about duplicate names when creating new notes
- **But NEVER delete/modify without asking**

## Obsidian CLI (Quick Health Checks) — with Fallbacks

Try CLI for instant vault health metrics before running the full Python scan.

```bash
OBS="bash 80_Code/scripts/obs.sh"

# Quick health snapshot
$OBS vault                         # total files, folders, size
$OBS orphans total                 # notes with no incoming links
$OBS deadends total                # notes with no outgoing links
$OBS unresolved total              # broken links count

# Find what links to a stub before deciding to delete
$OBS backlinks file="Stub Note Name"
$OBS backlinks file="Stub Note Name" total
```

**Fallbacks** (if Obsidian not running):
- Vault stats → `Glob **/*.md` + count
- Orphans → `python "80_Code/scripts/generate-link-index.py" --orphans`
- Broken links → `python "80_Code/scripts/generate-link-index.py" --broken`
- Backlinks for one note → `Grep` for `\[\[Note Name` across vault

**Workflow**: CLI health check first → Python script for detailed analysis → triage.

## Integration with Other Skills

- Use CLI `backlinks` (or Grep fallback) to check links before deleting stubs
- After cleanup, regenerate `link-index.json`
