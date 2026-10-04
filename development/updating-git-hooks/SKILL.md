---
name: updating-git-hooks
description: Updates existing git hook configurations for new requirements or tool changes. Use when hook requirements change, adding new quality checks, or modifying test commands.
---

# Update Git Hooks

## Purpose

This skill allows updating existing git hooks configuration without going through full interactive setup. It preserves current configuration while allowing specific changes.

## Prerequisites

Hooks must already be set up. If not, use `setting-up-git-hooks` skill instead.

```bash
# Check if hooks are configured
[ -f .wrangler/config/hooks-config.json ] && echo "Config exists" || echo "Run setting-up-git-hooks first"
```

## Activation Detection

When user runs `/wrangler:updating-git-hooks`, check if this is first activation:

1. Read `.wrangler/config/hooks-config.json`
2. Check `setupComplete` field:
   - If `false` -> First activation (was inactive)
   - If `true` or missing -> Reconfiguration (already active)

**First activation flow:**
1. Detect test framework (now that code exists)
2. Ask for test commands
3. Update hooks-config.json with `setupComplete: true`
4. Regenerate hooks with actual test commands
5. Update TESTING.md with active status
6. Message: "Git hooks activated! Tests will now run on commits."

**Reconfiguration flow:**
1. Show current configuration
2. Ask what to change
3. Update config and regenerate hooks
4. Message: "Git hooks updated with new configuration."

## Update Workflow

### Phase 1: Read Current Configuration

**Step 1: Verify Hooks Exist**

```bash
# Check configuration file
cat .wrangler/config/hooks-config.json

# Check installed hooks
ls -la .git/hooks/pre-commit .git/hooks/pre-push 2>/dev/null
```

If config doesn't exist, inform user to run `setting-up-git-hooks` first.

**Step 2: Display Current Settings**

Present current configuration to user:

```markdown
## Current Git Hooks Configuration

| Setting | Current Value |
|---------|---------------|
| Test Command | `npm test` |
| Unit Test Command | `npm run test:unit` |
| Format Command | `npm run format` |
| Lint Command | `npm run lint` |
| Protected Branches | main, master, develop |
| Skip Docs Only | true |
| Commit Msg Validation | false |
| Pattern | A (direct installation) |

**Which settings would you like to update?**
```

### Phase 2: Gather Updates

**Step 3: Ask What to Update**

Use AskUserQuestion:

```typescript
AskUserQuestion({
  questions: [{
    question: "Which settings would you like to update?",
    header: "Settings to Update",
    options: [
      { label: "Test commands", description: "Full test, unit test commands" },
      { label: "Format/lint commands", description: "Formatter and linter" },
      { label: "Protected branches", description: "Branch patterns for pre-push" },
      { label: "Commit message validation", description: "Enable/disable, pattern" },
      { label: "Docs-only skip patterns", description: "File patterns for skipping tests" },
      { label: "Multiple settings", description: "Update several settings" }
    ],
    multiSelect: true
  }]
})
```

**Step 4: Gather New Values**

For each setting being updated, ask for new value:

**Test Commands:**
```typescript
AskUserQuestion({
  questions: [{
    question: "What is your full test command?",
    header: "Test Command",
    options: [
      { label: "Keep current", description: "[current value]" },
      { label: "Custom", description: "I'll type a new command" }
    ],
    multiSelect: false
  }]
})
```

Repeat for each selected setting category.

### Phase 3: Update Configuration

**Step 5: Backup Current Config**

```bash
# Create backup
cp .wrangler/config/hooks-config.json .wrangler/config/hooks-config.json.backup

# Record timestamp
echo "Backup created at: $(date)" >> .wrangler/config/hooks-config.json.backup
```

**Step 6: Update Configuration File**

Use Edit tool to update `.wrangler/config/hooks-config.json`:

1. Read current config
2. Parse JSON
3. Update only changed fields
4. Update `updatedAt` timestamp
5. Write back to file

```json
{
  "version": "1.0.0",
  "createdAt": "[original timestamp]",
  "updatedAt": "[new timestamp]",
  "testCommand": "[updated if changed]",
  // ... other fields
}
```

### Phase 4: Regenerate Hooks

**Step 7: Regenerate Hook Files**

Read the hook templates from wrangler skills directory and regenerate with new configuration:

For Pattern A:
```bash
# Hooks are in .git/hooks/
# Regenerate each hook with new config values
```

For Pattern B:
```bash
# Hooks are in .wrangler/config/git-hooks/
# Regenerate and keep symlinks intact
```

Use same parameterization as `setting-up-git-hooks`:
- Replace `{{TEST_COMMAND}}` with new test command
- Replace `{{UNIT_TEST_COMMAND}}` with new unit test command
- etc.

**Step 8: Preserve Permissions**

```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
[ -f .git/hooks/commit-msg ] && chmod +x .git/hooks/commit-msg
```

### Phase 5: Verification

**Step 9: Verify Update**

```bash
# Show updated config
echo "=== Updated Configuration ==="
cat .wrangler/config/hooks-config.json

# Verify hooks are executable
echo ""
echo "=== Hook Status ==="
for hook in pre-commit pre-push commit-msg; do
    if [ -f .git/hooks/$hook ]; then
        if [ -x .git/hooks/$hook ]; then
            echo "[OK] $hook"
        else
            echo "[WARN] $hook not executable"
        fi
    fi
done
```

**Step 10: Summary**

```markdown
## Git Hooks Updated

### Changes Made

| Setting | Old Value | New Value |
|---------|-----------|-----------|
| Test Command | `npm test` | `npm run test:all` |
| Protected Branches | main, master | main, master, develop |

### Files Modified

- `.wrangler/config/hooks-config.json` - Updated configuration
- `.git/hooks/pre-commit` - Regenerated
- `.git/hooks/pre-push` - Regenerated

### Backup Created

Original config saved to: `.wrangler/config/hooks-config.json.backup`

### Test Your Changes

```bash
# Trigger pre-commit hook
git commit --allow-empty -m "test: verify hooks"

# Or check hook directly
./.git/hooks/pre-commit
```
```

## Edge Cases

### Adding Commit Message Validation

If enabling commit-msg validation when it wasn't before:

1. Read `commit-msg.template.sh` from templates
2. Parameterize with config values
3. Write to `.git/hooks/commit-msg`
4. Make executable

### Removing Commit Message Validation

If disabling commit-msg validation:

```bash
# Remove the hook
rm .git/hooks/commit-msg

# Keep config flag as false
```

### Switching Patterns

Switching from Pattern A to Pattern B (or vice versa) requires full re-setup:

```
This change requires full re-setup.
Run /wrangler:setting-up-git-hooks to change installation patterns.
```

### No Changes Detected

If user doesn't change anything:

```
No changes made to configuration.
Your git hooks remain as configured.
```

## Rollback

If something goes wrong:

```bash
# Restore from backup
cp .wrangler/config/hooks-config.json.backup .wrangler/config/hooks-config.json

# Regenerate hooks with original config
# Run /wrangler:updating-git-hooks to regenerate
```

## Related Skills

- **setting-up-git-hooks** - Initial hook installation
- **running-tests** - Manual test execution
- **practicing-tdd** - TDD workflow with hooks
- **verifying-before-completion** - Verification requirements

## Common Updates

### Add a Protected Branch

```bash
# Current: ["main", "master"]
# Updated: ["main", "master", "develop", "release/*"]
```

### Change Test Command

```bash
# Current: "npm test"
# Updated: "npm run test:ci"
```

### Enable Commit Message Validation

```bash
# Current in .wrangler/config/hooks-config.json: enableCommitMsgValidation: false
# Updated: enableCommitMsgValidation: true
```

### Update Docs Patterns

```bash
# Current in .wrangler/config/hooks-config.json: ["*.md", "docs/*"]
# Updated: ["*.md", "*.txt", "docs/*", "README*", "CHANGELOG*"]
```
