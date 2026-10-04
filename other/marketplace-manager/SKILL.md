---
name: marketplace-manager
description: Manage flight505-marketplace plugin synchronization and validation. Sync plugin versions from submodules to marketplace.json, validate manifests, and maintain marketplace versioning. Use when syncing plugins, validating marketplace manifests, or updating marketplace.json.
---

# Marketplace Manager

Specialized skill for managing the flight505-marketplace Claude Code plugin marketplace. Handles synchronizing plugin versions from git submodules to marketplace.json, validating plugin manifests, and maintaining marketplace versioning.

## When to Use

Use this skill when working in the flight505-marketplace repository to:

- Sync a plugin's version after bumping it in the submodule
- Sync all changed submodules at once
- Validate plugin manifests manually
- Check marketplace synchronization status

**Important:** This skill only works from the marketplace root directory. It will error if run elsewhere.

## Commands

### /marketplace:sync <plugin-name>

Sync one plugin's version from its submodule to marketplace.json.

**Usage:**

```bash
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace
claon
# In Claude Code:
/marketplace:sync sdk-bridge
```

**Flow:**

1. Verify in marketplace root (check for `.claude-plugin/marketplace.json`)
2. Verify plugin submodule exists (sdk-bridge, storybook-assistant, nano-banana, claude-project-planner)
3. Read version from `<plugin-name>/.claude-plugin/plugin.json`
4. Update `marketplace.json` plugins[] array with new version
5. Bump marketplace patch version (e.g., 1.2.28 → 1.2.29)
6. Git commit and push
7. Output: `✓ Synced sdk-bridge v4.0.1 to marketplace v1.2.29`

**Example:**

```bash
# After bumping sdk-bridge in its submodule
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace
/marketplace:sync sdk-bridge

# Output:
# ✓ Read sdk-bridge version: 4.0.1
# ✓ Updated marketplace.json
# ✓ Bumped marketplace version: 1.2.28 → 1.2.29
# ✓ Committed and pushed
#
# Synced sdk-bridge v4.0.1 to marketplace v1.2.29
```

---

### /marketplace:sync-all

Sync ALL submodules that have uncommitted pointer changes.

**Usage:**

```bash
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace
/marketplace:sync-all
```

**Flow:**

1. Run: `git diff --submodule` to detect changed submodules
2. For each changed submodule → read its version from plugin.json
3. Update marketplace.json for all changed plugins
4. Bump marketplace patch version once
5. Create one commit for all changes
6. Push to origin
7. Output: `✓ Synced 2 plugins: sdk-bridge v4.0.1, nano-banana v1.2.0`

**Example:**

```bash
# After updating multiple submodule pointers
/marketplace:sync-all

# Output:
# Detected changed submodules: sdk-bridge, nano-banana
# ✓ Read sdk-bridge version: 4.0.1
# ✓ Read nano-banana version: 1.2.0
# ✓ Updated marketplace.json
# ✓ Bumped marketplace version: 1.2.28 → 1.2.29
# ✓ Committed and pushed
#
# Synced 2 plugins: sdk-bridge v4.0.1, nano-banana v1.2.0 to marketplace v1.2.29
```

---

### /marketplace:validate

Run all marketplace validators manually.

**Usage:**

```bash
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace
/marketplace:validate
```

**Flow:**

1. Execute `.claude/hooks/validators/*.py` scripts:
   - `plugin-manifest-validator.py`
   - `marketplace-sync-validator.py`
2. Show results in readable format
3. Block on errors, warn on issues

**Example:**

```bash
/marketplace:validate

# Output:
# Running marketplace validators...
#
# ✓ plugin-manifest-validator.py
#   - All 4 plugin manifests valid
#   - Required fields present
#   - Versions in valid format
#
# ✓ marketplace-sync-validator.py
#   - marketplace.json versions match submodules
#   - All plugins synchronized
#
# All validations passed!
```

If validators fail:

```bash
/marketplace:validate

# Output:
# Running marketplace validators...
#
# ✗ plugin-manifest-validator.py
#   - sdk-bridge: Missing 'description' field
#   - nano-banana: Invalid version format: 'v1.2.0' (should be '1.2.0')
#
# ✗ marketplace-sync-validator.py
#   - sdk-bridge version mismatch:
#     - Submodule: 4.0.1
#     - Marketplace: 4.0.0
#
# Validation failed! Fix errors above.
```

## Supported Plugins

The skill works with these plugins in flight505-marketplace:

- **sdk-bridge** - Interactive autonomous development assistant
- **storybook-assistant** - Storybook component development
- **claude-project-planner** - Project planning and management
- **nano-banana** - Lightweight utility plugin

## Location Detection

marketplace-manager verifies it's running in the correct location:

**Detection method:**

```bash
# Check for marketplace.json
if [ -f ".claude-plugin/marketplace.json" ]; then
  # In marketplace root ✓
else
  # Not in marketplace root ✗
  echo "Error: Must be run from marketplace root"
fi
```

**Error if wrong location:**

```
Error: marketplace-manager can only run from marketplace root
Expected: .claude-plugin/marketplace.json
Current directory: /Users/jesper/some/other/project

Did you mean to run this from ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace?
```

## Marketplace Version Bumping

marketplace-manager always bumps the marketplace **patch** version when syncing plugins:

**Bump logic:**

- Read current marketplace version from `marketplace.json`
- Parse semantic version: `X.Y.Z`
- Increment patch: `X.Y.(Z+1)`
- Update marketplace version
- Commit with descriptive message

**Example:**

```
Current: 1.2.28
After sync: 1.2.29

Commit message:
"chore: sync sdk-bridge to v4.0.1, bump marketplace to v1.2.29"
```

**When to manually bump major/minor:**

- Major (X.0.0): Breaking changes to marketplace structure
- Minor (X.Y.0): New features in marketplace itself
- Patch (X.Y.Z): Plugin version updates (automatic via this skill)

## Integration with version-manager

These skills work together in the typical workflow:

**Step 1: Work in plugin submodule**

```bash
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace/sdk-bridge
git checkout main
# Make changes
git commit -m "feat: new generative UI"

# → version-manager Stop hook triggers
# → Analyzes commits: sees "feat:" → recommends minor
# → Prompts: "Bump version? (Minor 4.1.0 - Recommended)"
# → User selects "Minor"
# → Updates plugin.json, README badge, commits, tags, pushes
```

**Step 2: Sync to marketplace**

```bash
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace
claon

# In Claude Code:
/marketplace:sync sdk-bridge

# → Reads sdk-bridge/.claude-plugin/plugin.json (v4.1.0)
# → Updates marketplace.json
# → Bumps marketplace to 1.2.29
# → Commits and pushes
```

## Git Submodule Workflow

Understanding how submodules work helps with this skill:

**Submodule basics:**

- Each plugin is a separate git repository
- Marketplace repository stores a "pointer" to a specific commit in each submodule
- When you commit in a submodule, the marketplace parent doesn't automatically update

**Typical flow:**

```bash
# 1. Work in submodule
cd sdk-bridge
git commit -m "feat: new feature"
# → version-manager bumps version to 4.1.0
# → Pushes to sdk-bridge repo

# 2. Submodule pointer is now "dirty" in marketplace
cd ..
git status
# Output: modified: sdk-bridge (new commits)

# 3. Sync to marketplace
/marketplace:sync sdk-bridge
# → Updates marketplace.json with v4.1.0
# → Adds and commits the submodule pointer update
# → Pushes to marketplace repo
```

## Validation Integration

marketplace-manager integrates with existing validators:

**PostToolUse validators** (automatic, real-time):

- `.claude/hooks/validators/plugin-manifest-validator.py`
  - Runs after Edit/Write on plugin.json files
  - Validates manifest structure
  - Checks required fields
- `.claude/hooks/validators/marketplace-sync-validator.py`
  - Runs after Edit/Write on marketplace.json
  - Ensures versions match submodules
  - Catches sync drift

**Manual validation** (via command):

- `/marketplace:validate`
  - Runs all validators on demand
  - Shows detailed results
  - Useful before committing

## Files in This Skill

- `SKILL.md` (this file) - Skill instructions
- `commands/sync.md` - `/marketplace:sync` command details
- `commands/sync-all.md` - `/marketplace:sync-all` command details
- `commands/validate.md` - `/marketplace:validate` command details
- `scripts/sync-marketplace.py` - Marketplace.json updater script

## Installation

Install as a project-local skill via symlink:

```bash
ln -sfn "$TOOLKIT_DIR/marketplace-manager" "$WORKSPACE_ROOT/.claude/skills/marketplace-manager"
```

Once installed, the slash commands are available when working in marketplace root.

## Auto-Update Implications

When you sync plugins to marketplace, understand the user impact:

**Patch/Minor bumps → Auto-update users**

- Users with auto-update enabled pull immediately
- Your changes reach users as soon as you sync
- Test thoroughly before syncing to marketplace

**Major bumps → Manual update**

- Users must explicitly update
- Use for breaking changes only

**Best practices:**

1. Test plugins in feature branches before merging to main
2. Only bump versions on main branch (version-manager ensures this)
3. Sync to marketplace after version bump is confirmed working
4. Monitor GitHub issues after syncing for user reports

## Troubleshooting

**Issue: "Not in marketplace root" error**

- Solution: `cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace`
- Verify: `ls .claude-plugin/marketplace.json`

**Issue: Plugin not found**

- Solution: Check plugin name spelling (sdk-bridge, not sdk_bridge)
- Verify: `ls sdk-bridge/.claude-plugin/plugin.json`

**Issue: Version mismatch after sync**

- Cause: Submodule pointer not updated
- Solution: `cd .. && git add sdk-bridge && git commit`

**Issue: Git push fails**

- Cause: Uncommitted changes or conflicts
- Solution: Resolve conflicts, ensure clean working tree

**Issue: Validators failing**

- Cause: Plugin manifest issues or sync drift
- Solution: Run `/marketplace:validate` to see details, fix errors

## Integration with Existing Scripts

marketplace-manager **replaces** parts of the manual workflow:

**Deprecated:**

- Manual marketplace.json editing
- Manual marketplace version bumping
- Running bash scripts to sync versions

**Still used:**

- `scripts/validate-plugin-manifests.sh` (called by `/marketplace:validate`)
- `scripts/bump-plugin-version.sh` (kept as reference/backup)

**Workflow comparison:**

**Old workflow (manual):**

```bash
# 1. Bump plugin version manually
./scripts/bump-plugin-version.sh sdk-bridge 4.1.0
# 2. Script does everything (submodule + marketplace)
```

**New workflow (hook-based):**

```bash
# 1. Commit in submodule
cd sdk-bridge
git commit -m "feat: new feature"
# → version-manager bumps automatically

# 2. Sync to marketplace
cd ..
/marketplace:sync sdk-bridge
# → marketplace-manager syncs automatically
```

## Examples

### Example 1: Single Plugin Update

```bash
# Start in marketplace root
cd ~/Projects/Dev_projects/Claude_SDK/flight505-marketplace

# Work on plugin
cd sdk-bridge
# ... make changes ...
git commit -m "fix: correct validation logic"
# → version-manager: "Bump version? (Patch 4.0.1 - Recommended)"
# → User selects "Patch"
# → plugin.json updated to 4.0.1, README badge updated, tagged, pushed

# Sync to marketplace
cd ..
claon
/marketplace:sync sdk-bridge
# → Reads sdk-bridge version: 4.0.1
# → Updates marketplace.json
# → Bumps marketplace: 1.2.28 → 1.2.29
# → Commits and pushes
```

### Example 2: Multiple Plugin Updates

```bash
# Update sdk-bridge and nano-banana
cd sdk-bridge
git commit -m "feat: new feature"
# → Bumped to 4.1.0

cd ../nano-banana
git commit -m "fix: bug fix"
# → Bumped to 1.2.1

# Sync all at once
cd ..
/marketplace:sync-all
# → Detects: sdk-bridge and nano-banana changed
# → Syncs both to marketplace
# → One marketplace commit: 1.2.29 → 1.2.30
```

### Example 3: Validation Before Sync

```bash
# Check everything is valid before syncing
/marketplace:validate
# → All validators pass

/marketplace:sync sdk-bridge
# → Syncs successfully
```

## Best Practices

1. **Always validate before syncing** - Run `/marketplace:validate` first
2. **Sync immediately after version bump** - Don't let submodule pointers drift
3. **Use sync-all for multiple updates** - One commit is cleaner than many
4. **Test plugins before syncing** - Marketplace users get updates immediately
5. **Monitor after sync** - Watch for user issues on GitHub

## Future Enhancements

- GitHub release creation for marketplace versions
- Changelog generation from plugin updates
- Slack/Discord notifications on marketplace updates
- Automatic webhook triggering after sync
- Marketplace version validation (ensure all plugins compatible)
