---
name: skills-local-setup
description: Set up AI tool symlinks in a repository for multi-agent compatibility. Use when the user wants to set up skills for Gemini, Claude, or other AI tools, or when they mention "setup skills", "configure agents", or "link AGENTS.md".
---

# Local Skills Setup

Create symlinks so multiple AI tools can use the same skill definitions from `.claude/`.

**Why?** Different AI tools look for config in different places (`.claude/`, `.agent/`, `GEMINI.md`). This skill creates symlinks so you maintain ONE source of truth in `.claude/` and `AGENTS.md`.

## Quick Start

```bash
# Run from any repo root (script is in the global skill location)
~/.claude/skills/skills-local-setup/scripts/skills-local-setup.sh [agent|opencode|gemini|all]
```

---

## Directory Structure

```
.claude/skills/   <- SOURCE (tracked in git)
.agent/skills/    -> symlink to .claude/skills/ (gitignored)
.opencode/skill/  -> symlink to .claude/skills/ (gitignored, singular!)
GEMINI.md         <- directive file (gitignored)
```

## Supported Tools

| Tool | Command | What It Does |
|------|---------|--------------|
| Agent | `agent` | Creates `.agent/skills/` symlink to `.claude/skills/` (backward compat) |
| OpenCode | `opencode` | Creates `.opencode/skill/` symlink to `.claude/skills/` (singular!) |
| Gemini | `gemini` | Creates `GEMINI.md` with directive to load `AGENTS.md` |
| All | `all` | Sets up all compatibility layers (agent + opencode + gemini) |

> [!NOTE]
> `.claude/skills/` is the source of truth and should be tracked in git. Only the compatibility symlinks/files are gitignored.


---

## Workflow

### 1. Run the Setup Script

```bash
# From repo root — script lives in the global skills directory
~/.claude/skills/skills-local-setup/scripts/skills-local-setup.sh [agent|opencode|gemini|all]
```

The script automatically:
- Validates prerequisites (git repo)
- Creates `.claude/skills/` directory if needed (source of truth, tracked in git)
- Creates compatibility symlinks with relative paths
- Adds symlinks/directive files to `.gitignore`
- Asks for Y/N confirmation before overwriting existing files
- Migrates existing `.agent/settings.json` to `.claude/settings.json` if found

> [!TIP]
> If `AGENTS.md` doesn't exist when setting up Gemini, the script will instruct you to run the `skills-index-updater` skill first to create it.


---

### 2. Verify Setup

```bash
# Check directories and symlinks
ls -la .claude/ .agent/ .opencode/ GEMINI.md 2>/dev/null

# Check .gitignore (should NOT include .claude/)
grep -E "GEMINI|\.agent|\.opencode" .gitignore

# Check git status (symlinks should be ignored)
git status
```

---

## Quality Rules

- **`.claude/` is the source of truth** — Never edit symlinked files directly
- **Symlinks must be in .gitignore** — Keep repo clean, only track actual content
- **Use relative paths** — Symlinks should work regardless of absolute path
- **Confirm before overwriting** — Script shows existing content and asks for Y/N confirmation before removing

### Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use absolute paths in symlinks | Breaks when repo moves or on other machines | Use relative paths (`../`) |
| Commit symlinks to git | Creates merge conflicts, breaks for others | Add to `.gitignore` |
| Edit `.agent/` directly | Changes won't persist (it's a symlink) | Edit `.claude/` instead |
| Run outside repo root | Symlinks will be created in wrong location | `cd` to repo root first |

### Validation Checklist

Before considering setup complete:
- [ ] `ls -la` shows symlinks pointing to correct targets
- [ ] `git status` shows no untracked symlinks
- [ ] `.gitignore` contains entries for all symlinks

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "File exists" error | Target already exists | Check if it's a symlink first, backup if needed |
| Symlink broken after clone | Absolute path used | Recreate with relative path |
| Changes not syncing | Editing symlink, not source | Edit `.claude/` directly |
| Git tracking symlink | Missing .gitignore entry | Add entry to .gitignore |
| AGENTS.md not found | Missing AGENTS.md file | Run `/skills-index-updater` skill first |
