---
name: handbook-sync
description: Sync central handbook from ~/.claude/AmplifyHandbook/ to current project's resources/handbook/
---

# Handbook Sync - Update Project Handbook

## Purpose

Syncs the central handbook from `~/.claude/AmplifyHandbook/` to the current project's `resources/handbook/` folder.

This ensures your project has the latest Amplify Gen 2 documentation, patterns, and best practices.

---

## When to Use

User says:
- "Sync the handbook"
- "Update the handbook"
- "Pull latest handbook"
- "Refresh handbook docs"
- "Get latest handbook"

---

## Workflow

### Step 1: Verify Central Handbook Exists

Check that `~/.claude/AmplifyHandbook/` directory exists and has content:

```bash
ls ~/.claude/AmplifyHandbook/README.md
```

If it doesn't exist, tell the user:
```
❌ Central handbook not found at ~/.claude/AmplifyHandbook/

Please clone the AmplifyHandbook repo:
  git clone https://github.com/ChinchillaEnterprises/AmplifyHandbook.git ~/.claude/AmplifyHandbook
```

### Step 2: Create Project Handbook Directory

```bash
mkdir -p resources/handbook
```

### Step 3: Sync Everything

Copy everything from central handbook to project:

```bash
cp -r ~/.claude/AmplifyHandbook/* ./resources/handbook/
```

**Important:** This overwrites everything in the project's handbook with the latest from the central source.

**What gets copied:**
- All markdown documentation files
- All code examples
- Complete folder structure (auth/, data/, functions/, webhooks/, frontend/, troubleshooting/)
- README.md and navigation files

**Note:** AmplifyHandbook repo contains only documentation (no SKILL.md)

### Step 4: Verify Success

```bash
ls -la resources/handbook/README.md
```

### Step 5: Confirm to User

Tell the user:
```
✅ Handbook synced successfully!
   - Source: ~/.claude/AmplifyHandbook/
   - Destination: ./resources/handbook/
   - All documentation is now up to date
```

---

## What This Does

**ONE-WAY sync:** Central → Project

```
~/.claude/AmplifyHandbook/  (central, source of truth)
         ↓
         ↓  cp -r command
         ↓
./resources/handbook/              (project, local copy)
```

This is NOT a two-way sync. Changes in the project's `resources/handbook/` are NOT pushed back to central.

---

## Important Notes

### To Get Latest Central Handbook

Before syncing to a project, ensure your central handbook is up to date:

```bash
cd ~/.claude/AmplifyHandbook/
git pull
```

This gets the latest handbook updates from the AmplifyHandbook repo.

### To Contribute New Patterns

If you want to add new patterns to the central handbook, use the `handbook-updater` skill instead. It will:
1. Update files in `~/.claude/AmplifyHandbook/`
2. Commit and push to GitHub
3. Make updates available to the whole team

---

## Complete Example

**User:** "Sync the handbook"

**Claude:**
```bash
# Step 1: Verify central handbook exists
ls ~/.claude/AmplifyHandbook/README.md

# Step 2: Create project directory
mkdir -p resources/handbook

# Step 3: Copy everything
cp -r ~/.claude/AmplifyHandbook/* ./resources/handbook/

# Step 4: Verify
ls -la resources/handbook/README.md
```

**Output:**
```
✅ Handbook synced successfully!
   - Source: ~/.claude/AmplifyHandbook/
   - Destination: ./resources/handbook/
   - All documentation is now up to date
```

---

## Troubleshooting

### "No such file or directory" for central handbook

**Problem:** `~/.claude/AmplifyHandbook/` doesn't exist

**Solution:**
```bash
git clone https://github.com/ChinchillaEnterprises/AmplifyHandbook.git ~/.claude/AmplifyHandbook
```

If it exists but is out of date:
```bash
cd ~/.claude/AmplifyHandbook/
git pull
```

### "Permission denied"

**Problem:** Can't write to `resources/handbook/`

**Solution:** Check you're in a project directory where you have write permissions.

---

## Remember

- This skill does a **full overwrite** of `resources/handbook/`
- Always pulls from `~/.claude/AmplifyHandbook/` (central)
- To update central handbook, use `handbook-updater` skill
- To read handbook, use `handbook` skill
