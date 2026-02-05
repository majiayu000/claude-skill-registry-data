---
name: skills-sync
description: Sync Claude Code skills from the ChillSkills GitHub repository
---

# Skills Sync - Manage Your Claude Code Skills

## Purpose

This skill helps you sync your Claude Code skills with the ChillSkills GitHub repository. Think of it as "version control for your AI assistant's skills."

## Two Modes of Operation

### Mode 1: **"Sync skills"** - Pull from GitHub
When user says things like:
- "Sync skills"
- "Update skills from GitHub"
- "Pull latest skills"
- "Refresh my skills"

**What to do:** Pull latest skills from ChillSkills GitHub repo and update local skills directory.

### Mode 2: **"Push skill changes"** - Push to GitHub
When user says things like:
- "Push skill changes"
- "Commit this skill update"
- "Save this skill to GitHub"
- "Push skills to the repo"

**What to do:** Push local skill changes back to ChillSkills GitHub repo.

---

## Configuration

- **GitHub Repo:** `ChinchillaEnterprises/ChillSkills`
- **GitHub Token:** Stored in AWS Secrets Manager as `github-token`
- **Local Path:** `~/.claude/skills/`
- **Important:** The local skills directory IS a git repository

---

## Mode 1: Sync Skills (Pull from GitHub)

### When to Use
User wants to pull the latest skills from the ChillSkills repo to update their local skills.

### Strategy
Since `~/.claude/skills/` is already a git repository, we can use standard git operations:

```bash
# Navigate to skills directory
cd ~/.claude/skills

# Check current status
git status

# Pull latest from GitHub
git pull origin main

echo "✅ Skills synced from ChillSkills repo!"
```

### Success Message
```
✅ Skills synced from ChillSkills!
   - Pulled latest from: https://github.com/ChinchillaEnterprises/ChillSkills
   - Updated skills directory: ~/.claude/skills/
   - You now have the latest versions of all skills
```

### Handling Conflicts
If there are local changes that conflict with remote:
```bash
# Show what files have conflicts
git status

# Ask user what to do:
# 1. Stash local changes and pull
# 2. Commit local changes first, then pull
# 3. Force overwrite with remote version
```

---

## Mode 2: Push Skill Changes (Push to GitHub)

### When to Use
User has created or updated skills locally and wants to push them to the ChillSkills repo.

### Strategy
Since `~/.claude/skills/` is already a git repository, we use standard git operations:

```bash
# Navigate to skills directory
cd ~/.claude/skills

# Check what files changed
git status

# Show the diff to user
git diff

# Ask user which files to commit (or commit all changed files)
# For example, if handbook/SKILL.md was updated:

# Stage the changes
git add handbook/SKILL.md
# Or stage all: git add .

# Commit with message
# Ask user for commit message or generate one
COMMIT_MESSAGE="feat: Update handbook skill with GitHub API sync"
git commit -m "$COMMIT_MESSAGE"

# Push to GitHub
git push origin main

echo "✅ Skill changes pushed to ChillSkills repo!"
```

### Commit Message Guidelines
Follow conventional commits format:
- `feat: Add new skill for X`
- `fix: Fix bug in Y skill`
- `docs: Update skill documentation`
- `refactor: Improve Z skill structure`

### Success Message
```
✅ Skill changes pushed to ChillSkills!
   - Files changed: handbook/SKILL.md
   - Commit: "feat: Update handbook skill with GitHub API sync"
   - Pushed to: https://github.com/ChinchillaEnterprises/ChillSkills
   - View commit: [commit URL]
```

---

## Common Workflows

### Workflow 1: Pull Latest Skills
```
User: "Sync my skills"

You:
1. cd ~/.claude/skills
2. git pull origin main
3. Show summary of what was updated
4. Done! ✅
```

### Workflow 2: Push Single Skill Update
```
User: "I just updated the handbook skill. Push it to GitHub."

You:
1. cd ~/.claude/skills
2. git status (show what changed)
3. git diff handbook/SKILL.md (show the changes)
4. Ask: "Commit message?" or suggest: "feat: Update handbook skill"
5. git add handbook/SKILL.md
6. git commit -m "feat: Update handbook skill with sync functionality"
7. git push origin main
8. Done! ✅
```

### Workflow 3: Push Multiple Skill Updates
```
User: "Push all my skill changes"

You:
1. cd ~/.claude/skills
2. git status (list all changed files)
3. Ask: "Commit all changes?" or ask for specific files
4. git add .
5. Ask for commit message or generate comprehensive one
6. git commit -m "feat: Update multiple skills with new features"
7. git push origin main
8. Done! ✅
```

### Workflow 4: Create New Skill and Push
```
User: "I created a new skill called 'code-review'. Push it to the repo."

You:
1. cd ~/.claude/skills
2. git status (should show new directory: code-review/)
3. git add code-review/
4. git commit -m "feat: Add code-review skill"
5. git push origin main
6. Done! ✅
```

---

## Checking Skill Status

### See What's Changed Locally
```bash
cd ~/.claude/skills
git status
```

### See What Would Be Pulled
```bash
cd ~/.claude/skills
git fetch origin
git log HEAD..origin/main --oneline
```

### See Remote Commits Not Yet Pulled
```bash
cd ~/.claude/skills
git log --oneline --graph --all --decorate
```

---

## Important Notes

### This is a Git Repo
Unlike the handbook sync (which uses GitHub API), the skills directory is already a full git repository. This means:
- ✅ Use normal git commands (pull, push, commit, etc.)
- ✅ Full git history is available
- ✅ Can create branches if needed
- ✅ Can see diffs and logs

### Authentication
Git should already be configured with credentials. If push fails due to authentication:
```bash
# Check if remote is configured
git remote -v

# If using HTTPS, may need to set up credentials
# If using SSH, may need to set up SSH keys
```

### File Management
The skills directory structure:
```
~/.claude/skills/
├── .git/                    ← Git repository
├── .gitignore
├── README.md
├── handbook/                ← Individual skills
│   └── SKILL.md
├── handbook-updater/
│   └── SKILL.md
├── skills-sync/             ← This skill!
│   └── SKILL.md
└── [other skills]/
```

---

## What This Prevents

❌ Skills going out of sync across machines
❌ Losing skill improvements when switching computers
❌ No version history of skill changes
❌ Manual copy-paste of skill files
❌ Forgetting what changed in a skill

✅ Version-controlled skills
✅ Easy skill sharing across machines
✅ Full history of skill improvements
✅ Collaborative skill development
✅ Easy rollback if something breaks

---

## Example Scenarios

### Scenario 1: Starting Work on New Machine
```
User: "Sync my skills"

You:
1. cd ~/.claude/skills
2. git pull origin main
3. Show: "Updated 3 skills: handbook, handbook-updater, skills-sync"
4. Done! All skills are now up to date ✅
```

### Scenario 2: After Improving a Skill
```
User: "I just added GitHub API sync to the handbook skill. Push it."

You:
1. cd ~/.claude/skills
2. git status → Shows: modified: handbook/SKILL.md
3. git add handbook/SKILL.md
4. git commit -m "feat: Add GitHub API sync to handbook skill"
5. git push origin main
6. Done! Improvement is now saved and shared ✅
```

### Scenario 3: Creating a New Skill
```
User: "I created a new skill called 'test-runner'. Commit it."

You:
1. cd ~/.claude/skills
2. git status → Shows: Untracked: test-runner/
3. git add test-runner/
4. git commit -m "feat: Add test-runner skill for automated testing"
5. git push origin main
6. Done! New skill is now in the repo ✅
```

---

## Remember

**Skills are your AI assistant's capabilities.**

Think of this skill as your skill manager:
- **Sync** to get latest skills
- **Push** to share your skill improvements
- **Version control** keeps everything safe

Every time you improve a skill, push it so you don't lose it!
