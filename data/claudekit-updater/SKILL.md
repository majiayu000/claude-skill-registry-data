---
name: claudekit-updater
description: Update ClaudeKit Engineer projects to the latest version. Capabilities include update single projects (safe mode with test branches), batch update multiple projects, find all ClaudeKit projects in home directory, verify updates with automated checks, preserve user settings and code, create timestamped backups, handle git workflows (branch, commit, merge), and rollback if needed. Use when user wants to update ClaudeKit framework, upgrade to latest version, apply new features/skills/commands, or maintain multiple ClaudeKit projects.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# ClaudeKit Updater Skill

Safely update ClaudeKit Engineer projects to the latest version with automated backup, testing, and verification.

## Core Capabilities

### Single Project Update
- Update one project with test branch
- Automatic backup creation
- Preserve user settings (settings.local.json)
- Full verification checks
- Easy rollback if needed

### Batch Updates
- Update multiple projects sequentially
- Pause between projects for testing
- Consolidated status reporting
- Skip non-ClaudeKit projects

### Discovery
- Find all ClaudeKit projects in home directory
- Verify project structure
- Check for uncommitted changes
- Detect git repository status

### Safety Features
- Timestamped backups (.claude.backup-YYYYMMDD-HHMMSS)
- Git test branches (safe mode)
- Never modifies user code
- Preserves custom settings
- Verification checks (6-9 checks)

## When to Use This Skill

Use this skill when:
- User wants to update ClaudeKit to latest version
- New features/skills/commands are available
- Maintaining multiple ClaudeKit projects
- Applying framework updates
- User says "update ClaudeKit" or "upgrade ClaudeKit"

## Update Process

### Safe Mode (Default)
1. Create timestamped backup
2. Create git test branch
3. Update framework files (agents, commands, workflows, skills, hooks)
4. Preserve settings.local.json
5. Run verification checks
6. Report results with next steps

### Quick Mode
1. Create timestamped backup
2. Update directly (no test branch)
3. Preserve settings
4. Verify
5. Report results

## What Gets Updated

**Modified (54 files):**
- `.claude/agents/` - All 14 agent definitions
- `.claude/commands/` - All 36 command files
- `.claude/workflows/` - All 4 workflow files

**Added (516 files):**
- `.claude/skills/` - 19 new skills
- `.claude/hooks/` - Security and notification hooks
- Configuration files (.env.example, metadata.json, etc.)

**Preserved:**
- All user project code (everything outside .claude/)
- `.claude/settings.local.json`
- Git history
- Custom commands/agents

## Usage Examples

### Example 1: Update Single Project

```bash
# User request: "Update my Lex-Stream project to latest ClaudeKit"

# Step 1: Read project location
cd ~/Lex-Stream

# Step 2: Run update script
/Users/sam/claudekit-engineer/update-claudekit-project.sh ~/Lex-Stream

# Step 3: Verify output shows:
# ✓ Backup created
# ✓ Test branch created
# ✓ Framework updated
# ✓ Settings preserved
# ✓ Verification: X/X checks passed
# ✓ Update complete

# Step 4: Report results to user
```

### Example 2: Update Multiple Projects

```bash
# User request: "Update all my ClaudeKit projects"

# Step 1: Find projects
find ~ -type d -name ".claude" -maxdepth 3 2>/dev/null | sed 's|/.claude||'

# Step 2: Run batch script
/Users/sam/claudekit-engineer/batch-update-example.sh

# Or update one by one:
/Users/sam/claudekit-engineer/update-claudekit-project.sh ~/Lex-Stream
/Users/sam/claudekit-engineer/update-claudekit-project.sh ~/Lex-stream-2
```

### Example 3: Quick Mode Update

```bash
# User request: "Quickly update my project"

/Users/sam/claudekit-engineer/update-claudekit-project.sh ~/my-project --quick
```

### Example 4: Find ClaudeKit Projects

```bash
# User request: "What ClaudeKit projects do I have?"

find ~ -type d -name ".claude" -maxdepth 3 2>/dev/null | sed 's|/.claude||'

# Example output:
# /Users/sam/Lex-Stream
# /Users/sam/Lex-stream-2
```

## Verification Steps

After running update, verify:

```bash
cd ~/project-path

# Check new files exist
ls .claude/skills/ai-multimodal/SKILL.md
ls .claude/commands/code.md
ls .claude/commands/use-mcp.md
ls .claude/skills/backend-development/SKILL.md

# Check git status
git branch
# Should show: update-claudekit-YYYYMMDD-HHMMSS

# Check file count
find .claude -type f | wc -l
# Should show ~570+ files (was ~60)

# Check backup exists
ls -la | grep .claude.backup
```

## Post-Update: Test & Merge

### Testing
```bash
cd ~/project-path
claude

# Try new commands:
/ask "what's new in v1.14?"
/code
/use-mcp
/review:codebase
```

### Merge (if tests pass)
```bash
git add .
git commit -m "chore: update ClaudeKit Engineer to v1.14.0"
git checkout main
git merge update-claudekit-YYYYMMDD-HHMMSS
git branch -d update-claudekit-YYYYMMDD-HHMMSS
```

### Rollback (if tests fail)
```bash
git checkout main
git branch -D update-claudekit-YYYYMMDD-HHMMSS
# Main branch unchanged - easy rollback!
```

## Troubleshooting

### Uncommitted Changes Error
```bash
# Error: "You have uncommitted changes"
cd ~/project-path
git add .
git commit -m "chore: commit before ClaudeKit update"
# Then run update again
```

### Template Not Found
```bash
# Verify template exists
ls /Users/sam/claudekit-engineer/.claude/
# Should show: agents, commands, workflows, skills, hooks
```

### Verification Checks Failed
```bash
# Check which files are missing
ls .claude/skills/ai-multimodal/
ls .claude/commands/code.md

# If missing, run update again
```

### Script Not Executable
```bash
chmod +x /Users/sam/claudekit-engineer/update-claudekit-project.sh
```

## What's New in Latest Version

**v1.14.0 Features:**
- 19 new skills (ai-multimodal, backend-dev, mobile-dev, databases, devops, etc.)
- 9 new commands (/code, /use-mcp, /review:codebase, /fix, etc.)
- 2 new agents (mcp-manager, scout-external)
- Better token efficiency (uses Haiku where appropriate)
- Security hooks (scout-block prevents .env exposure)
- Notification hooks (Discord, Telegram)
- Performance improvements

## Success Criteria

✅ **Update Successful When:**
- Script completes without errors
- Backup created with timestamp
- Test branch created (safe mode)
- Verification shows X/X checks passed
- New files visible in .claude/skills/
- settings.local.json preserved
- User code untouched

## Important Notes

- **Only .claude/ directory is modified** - User code is 100% safe
- **Always creates backup** - Easy rollback available
- **Safe mode creates test branch** - Main branch never touched
- **Settings preserved** - settings.local.json is restored
- **Quick mode available** - Use --quick flag for faster updates

## File Locations

**Update Script:**
```
/Users/sam/claudekit-engineer/update-claudekit-project.sh
```

**Batch Script:**
```
/Users/sam/claudekit-engineer/batch-update-example.sh
```

**Documentation:**
```
/Users/sam/claudekit-engineer/UPDATE-PROJECTS.md
/Users/sam/claudekit-engineer/CLAUDE-UPDATE-INSTRUCTIONS.md
/Users/sam/claudekit-engineer/HOW-TO-USE-WITH-FRESH-CLAUDE.md
```

**Desktop References:**
```
~/Desktop/claudekit-update-cheatsheet.txt
~/Desktop/FRESH-CLAUDE-PROMPT.txt
```

## Skill Activation Examples

**Example prompts that should activate this skill:**

- "Update my ClaudeKit project"
- "Upgrade Lex-Stream to latest ClaudeKit"
- "Update all my ClaudeKit Engineer projects"
- "What ClaudeKit projects can I update?"
- "Apply the latest ClaudeKit framework updates"
- "Update to ClaudeKit v1.14"
- "Upgrade my ClaudeKit to get the new skills"

## Response Template

When user requests update:

```
I'll update your ClaudeKit project(s) to the latest version (v1.14.0).

[Run update script and show progress]

Update Results:
✓ Backup created: .claude.backup-YYYYMMDD-HHMMSS
✓ Test branch: update-claudekit-YYYYMMDD-HHMMSS
✓ Framework updated: 54 files modified, 516 files added
✓ Settings preserved: settings.local.json ✓
✓ Verification: X/X checks passed

What's New:
• 19 new skills (ai-multimodal, backend-dev, mobile-dev, etc.)
• 9 new commands (/code, /use-mcp, /review:codebase)
• Better token efficiency
• Security hooks

Next Steps:
1. Test: cd ~/project && claude
2. If good, merge: git checkout main && git merge update-claudekit-*
3. If issues, rollback: git checkout main && git branch -D update-claudekit-*
```

## Common User Requests

| Request | Action |
|---------|--------|
| "Update Lex-Stream" | Run script on ~/Lex-Stream |
| "Update all projects" | Use batch script or iterate |
| "What's new?" | Show changelog from v1.14.0 |
| "Quick update" | Add --quick flag |
| "Find my projects" | Use find command for .claude dirs |
| "Rollback update" | Checkout main, delete test branch |
| "Merge update" | Commit, checkout main, merge |

## References

- **Changelog:** `/Users/sam/claudekit-engineer/CHANGELOG.md`
- **Template:** `/Users/sam/claudekit-engineer/.claude/`
- **Comparison:** `temp-update-files/claudekit-update-comparison.md`
- **GitHub:** https://github.com/claudekit/claudekit-engineer
- **Docs:** https://docs.claudekit.cc

---

**This skill enables safe, automated ClaudeKit project updates with full backup and rollback capabilities.**
