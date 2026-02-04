---
name: johnny-decimal
description: >
  Helps organize files in a Johnny Decimal system at ~/Documents. Use this
  skill when filing documents, finding files, creating folders, taking notes
  about JD items, or understanding where something belongs in the system.
---

# Johnny Decimal File Organization

**Skill base directory:** `{baseDir}`

This skill helps you work with the Johnny Decimal (JD) file system located at
`~/Documents` (or `$XDG_DOCUMENTS_DIR`).

## Quick Reference

The system has 10 areas:

| Area | Purpose |
|------|---------|
| 00-09 System | Meta-management (inbox, templates, scripts, archive) |
| 10-19 Personal | People (Self, Spouse, Kids, Parents, Friends, Pets) |
| 20-29 Finances | Banks, investments, credit, taxes, insurance |
| 30-39 Home and Property | Homes, vehicles, major assets |
| 40-49 Career and Education | Education, research, employers |
| 50-59 Health and Wellness | General health resources (not personal records) |
| 60-69 Hobbies and Recreation | Games, computing, creative works, travel |
| 70-79 Legal and Records | Legal documents and archival records |
| 80-89 Household and Services | Services, products, utilities, meals |
| 90-99 Reference | Library, research, manuals, datasets |

## Structure Format

```
XX-XX Area Name/           # Area (decade range)
└── XX Category Name/      # Category (two digits)
    └── XX.YY Subcategory/ # Subcategory (ID)
```

Example path:
```
~/Documents/20-29 Finances/21 Banks/21.10 Example Bank/
```

## Key Principles

1. **One place for everything** - Each item has exactly one correct location
2. **Person-first for personal records** - A spouse's health records go in
   `12 Spouse`, not `50 Health`
3. **Purpose determines area** - A bill goes in `27 Bills`, not with the service
   provider
4. **JDex is the brain** - Notes and decisions live in `00.00 JDex for System`

## Finding Where Things Go

Before filing, consult:
- **Flowchart**: `00-09 System/00 System/00.00 JDex for System/flowchart.md`
- **Full structure**: `00-09 System/00 System/00.00 JDex for System/overview.md`

Or use your judgment with the filing hierarchy:
1. Is it about a specific person? → `10-19 Personal` under their folder
2. Is it about yourself specifically? → `11 Self`
3. Otherwise, match by purpose → Areas 20-99

## Notes System

Notes about JD items live as markdown files in the JDex:
```
00-09 System/00 System/00.00 JDex for System/
├── overview.md      # System structure documentation
├── flowchart.md     # Filing decision tree
├── 31.14.md         # Notes about current home
├── 21.10.md         # Notes about a bank account
└── ...
```

Use `jd-note` to add timestamped entries to these files.

## Naming Conventions

**Folders:**
- Areas: `XX-XX Name` (e.g., `20-29 Finances`)
- Categories: `XX Name` (e.g., `21 Banks`)
- Subcategories: `XX.YY Name` (e.g., `21.10 Example Bank`)

**Files:**
- Date-prefixed for transient items: `2024-12-27_statement.pdf`
- Descriptive for permanent items: `policy_declaration.pdf`
- Statements: `statements/YYYY/MM.pdf` or `cc_MM.pdf` for credit cards

## Available Scripts

Scripts are located in `{baseDir}/scripts/`. Use the full path when invoking:

| Script | Purpose |
|--------|---------|
| `{baseDir}/scripts/jd-list.sh [ID]` | List contents of an area, category, or ID |
| `{baseDir}/scripts/jd-tree.sh [-L depth] [ID]` | Show directory structure using tree |
| `{baseDir}/scripts/jd-validate.sh <filename>` | Check if filename follows conventions |
| `{baseDir}/scripts/jd-mkdir.sh <category> <name>` | Create a new subcategory folder (auto-numbers) |
| `{baseDir}/scripts/jd-move.sh <file> <ID>` | Move a file to a JD location (with validation) |
| `{baseDir}/scripts/jd-note.sh [ID] [text]` | Add a timestamped note (browse if no ID given) |
| `{baseDir}/scripts/jd-read.sh [ID] [--edit]` | Display notes for an ID (browse if no ID given) |

Also available: `jd <query>` for navigation (in `~/bin/`).

### Interactive Features

When run by a human (not an agent), these commands have interactive modes:

- `jd-note` (no args) - Hierarchical browse (Area → Category → ID), then opens editor
- `jd-note <ID>` (without text) - Opens editor to write a note
- `jd-read` (no args) - Hierarchical browse (Area → Category → ID), then displays notes
- `jd-read --edit` (no args) - Hierarchical browse, then opens editor
- `jd-read <ID> --edit` - Opens the note file for editing

All properly handle TTY redirection for compatibility with any editor.

## Agent Usage (--porcelain)

All scripts support a `--porcelain` flag for machine-readable output:

```bash
{baseDir}/scripts/jd-list.sh 21 --porcelain                # Full paths, no colors
{baseDir}/scripts/jd-tree.sh -L3 --porcelain               # Full structure, no colors
{baseDir}/scripts/jd-mkdir.sh 21 "Name" --porcelain        # Outputs created path
{baseDir}/scripts/jd-move.sh file.pdf 21.10 --porcelain    # Outputs destination path
{baseDir}/scripts/jd-note.sh 21.10 "text" --porcelain      # Adds note (text required)
{baseDir}/scripts/jd-read.sh 21.10 --porcelain             # Outputs note file path
{baseDir}/scripts/jd-validate.sh file.pdf --porcelain      # Machine-readable validation
```

When using these scripts as an agent:
- **Always use `--porcelain`** for reliable parsing
- Paths are absolute and suitable for further operations
- Errors go to stderr with exit code 1
- `jd-note` **requires text argument** in agent mode (no editor)
- `jd-read --edit` is **not available** in agent mode (requires TTY)
- All scripts auto-detect agent mode when stdout/stdin are not TTYs

## Safety Rules

- Scripts will **refuse to overwrite** existing files
- Scripts **validate paths** before operations
- Always **confirm destructive operations** with the user
- When uncertain about filing location, **ask** rather than guess

## When to Explore

If you need current structure details not covered here, read:
1. `overview.md` in the JDex for full category breakdown
2. `flowchart.md` in the JDex for filing decisions
3. Use `{baseDir}/scripts/jd-list.sh` to see what exists in a location

## References

For more detailed guidance, use the Read tool to load:
- `{baseDir}/references/FILING-GUIDE.md` - Detailed filing decisions and examples
- `{baseDir}/references/NAMING.md` - File and folder naming conventions
