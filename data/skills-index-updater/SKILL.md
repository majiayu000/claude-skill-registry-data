---
name: skills-index-updater
description: Regenerate skill indexes for IDEs without native skill support (Kiro, Gemini, etc.). ONLY use when the user EXPLICITLY asks to "update skill index", "sync agents", "regenerate index", or "update AGENTS.md". Do NOT auto-invoke after creating/modifying skills - Claude Code has native skill support and does not need this.
---

# Skill index updater

Automatically regenerate skill indexes by scanning skill directories and updating:
- **Global skills** → `~/.kiro/steering/global.md` (if Kiro installed)
- **Global skills** → `~/Documents/Cline/Rules/cline_overview.md` (if Cline installed)
- **Local skills** → `AGENTS.md` in the repo (only when NOT in home directory)

---

> **⚠️ STOP: Check before running**
>
> This skill is **ONLY for IDEs without native skill support** (Kiro, Gemini, Cursor, etc.).
>
> **Claude Code users:** You do NOT need this - Claude Code has native skill indexing built-in.
>
> Only run if the user **explicitly** asked to update skill indexes for compatibility with other tools.

---

## Quick start

```bash
# Run from any location
python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py

# Preview changes without writing
python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py --dry-run
```

## Prerequisites

- Python 3.8+
- PyYAML package (`pip install pyyaml`) - optional, falls back to regex parsing
- For Kiro: `~/.kiro/steering/global.md` must exist with `## Available Skills Index` section
- For Cline: `~/Documents/Cline/Rules/cline_overview.md` must exist with `## Available Skills Index` section

---

## How it works

The script automatically determines what to update based on your current location:

| Location | Global skills | Local skills |
|----------|---------------|--------------|
| Home directory (`~/`) | ✅ Updated in `global.md` | ⏭️ Skipped (none exist) |
| Any repo | ✅ Updated in `global.md` | ✅ Updated in `AGENTS.md` |
| Directory with AGENTS.md | ✅ Updated in `global.md` | ✅ Updated in `AGENTS.md` |
| Outside a repo (no AGENTS.md) | ✅ Updated in `global.md` | ⏭️ Skipped (use --force-local to override) |

### Skill locations

| Location | Scope | Output files |
|----------|-------|-------------|
| `~/.claude/skills/` | Global | `~/.kiro/steering/global.md` (Kiro)<br>`~/Documents/Cline/Rules/cline_overview.md` (Cline) |
| `./.claude/skills/` | Local | `AGENTS.md` in repo root |

### Available flags

| Flag | Short | Behavior |
|------|-------|----------|
| `--dry-run` | `-n` | Show changes without writing |
| `--init` | | Create AGENTS.md if missing (auto-prompted otherwise) |
| `--force-local` | | Force local skills update even without git repo |

---

## Workflow

### 1. Run the update script

```bash
python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py
```

The script will:
1. Detect your working directory and whether you're in a git repo
2. Scan global skills in `~/.claude/skills/`
3. Update `~/.kiro/steering/global.md` with global skills index (if Kiro installed)
4. Update `~/Documents/Cline/Rules/cline_overview.md` with global skills index (if Cline installed)
5. If in a repo (and not in home directory):
   - Scan local skills in `.claude/skills/`
   - Update `AGENTS.md` with local skills index

### 2. Verify output

```bash
# Check Kiro global.md update
grep -A 20 "## Available Skills Index" ~/.kiro/steering/global.md

# Check Cline overview.md update
grep -A 20 "## Available Skills Index" ~/Documents/Cline/Rules/cline_overview.md

# Check AGENTS.md update (if in a repo)
grep -A 10 "## Available Skills Index" AGENTS.md
```

---

## Example output

```
Working directory: /Users/you/projects/my-repo
Home directory: /Users/you
In home directory: False
Repository root: /Users/you/projects/my-repo

============================================================
GLOBAL SKILLS
============================================================
Scanning global skills in: /Users/you/.claude/skills
  Found 5 global skills

  Skills found:
    - skill-builder (skill-builder)
    - skills-index-updater (skills-index-updater)
    - save-context (save-context)
    - humanize (humanize)
    - docx (docx)

Updated: /Users/you/.kiro/steering/global.md
Skipping Cline: /Users/you/Documents/Cline/Rules not found (Cline not installed)

============================================================
LOCAL SKILLS
============================================================
Scanning local skills in: /Users/you/projects/my-repo/.claude/skills
  Found 2 local skills

  Skills found:
    - extract-videos (extract-videos)
    - download-transcripts (download-transcripts)

Updated: /Users/you/projects/my-repo/AGENTS.md

============================================================
SUMMARY
============================================================
Index update complete.
```

---

## Output formats

### Global skills (in global.md)

```
## Available Skills Index
*(Auto-generated - do not edit manually)*

  path: .claude/skills/skill-builder
  name: skill-builder
  description: Create, evaluate, and improve Agent skills...
---
  path: .claude/skills/humanize
  name: humanize
  description: Convert AI-written text to more human-like writing...
---
```

### Local skills (in AGENTS.md)

```markdown
## Available Skills Index
_This index is for IDEs that don't natively support skills (e.g., Gemini CLI, Kiro). Skip if your IDE reads SKILL.md directly._

- **Name:** `extract-videos`
  - **Trigger:** Extract video URLs from various sources...
  - **Path:** `.claude/skills/extract-videos/SKILL.md`

- **Name:** `download-transcripts`
  - **Trigger:** Download and process video transcripts...
  - **Path:** `.claude/skills/download-transcripts/SKILL.md`
```

---

## Quality rules

- **Descriptions come from frontmatter** - Never manually edit the index
- **Global and local are separate** - Each goes to its own file
- **Run after every skill change** - Create, delete, or modify triggers update

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "global.md not found" | Missing Kiro config | Create `~/.kiro/steering/global.md` with index section |
| "cline_overview.md not found" | Missing Cline config | Create `~/Documents/Cline/Rules/cline_overview.md` with index section |
| Skill not appearing | Missing frontmatter | Add `name:` and `description:` to SKILL.md |
| YAML parse error | Invalid frontmatter syntax | Check for tabs, missing colons |
| Index section not found | Missing marker | Add `## Available Skills Index` section |
| Local skills skipped | Working from ~/ | This is expected (no local skills in home directory) |
| IDE not updated | IDE folder doesn't exist | Script validates folder existence before updating |

---

## Additional resources

- **[TESTING.md](TESTING.md)** - Evaluation scenarios and validation commands
