---
name: system-updates
description: This skill should be used when the user asks to "update my system", "run system updates", "update everything", "update brew yadm pass", or mentions running comprehensive system updates including Homebrew, yadm, and pass.
---

You are an expert at managing system updates across multiple tools simultaneously. When invoked, you will coordinate updates for Homebrew, yadm dotfiles, and the pass password manager in a single operation.

## Update Workflow

When the user requests system updates, execute the following operations in sequence:

### 1. Update yadm (Dotfiles)

Pull the latest dotfiles from the remote repository:

```bash
yadm pull
```

**Expected behavior:**
- If already up-to-date: Shows "Already up to date."
- If changes pulled: Shows files updated and any merge messages
- If conflicts: Report conflicts to user for manual resolution

### 2. Update pass (Password Store)

Pull the latest password store changes:

```bash
pass git pull
```

**Expected behavior:**
- If already up-to-date: Shows "Already up to date."
- If changes pulled: Shows Git pull output with updated refs
- If conflicts: Report conflicts to user for manual resolution

### 3. Update Homebrew

Update Homebrew itself and upgrade all installed packages:

```bash
brew update && brew upgrade
```

**Expected behavior:**
- `brew update`: Updates Homebrew formulae and cask definitions
- `brew upgrade`: Upgrades all outdated packages
- Shows list of packages being upgraded
- May take several minutes depending on outdated packages

## Execution Strategy

**Run all updates in sequence with proper error handling:**

```bash
echo "==> Updating yadm dotfiles..."
yadm pull

echo "==> Updating pass password store..."
pass git pull

echo "==> Updating Homebrew..."
brew update && brew upgrade
```

## Success Criteria

A successful update completes when:

1. **yadm pull** completes without conflicts
2. **pass git pull** completes without conflicts
3. **brew update** refreshes formulae
4. **brew upgrade** upgrades all outdated packages

## Error Handling

### yadm Conflicts

If yadm pull reports merge conflicts:

```bash
# Show conflicted files
yadm status

# User must resolve manually:
# 1. Edit conflicted files
# 2. yadm add <resolved-files>
# 3. yadm commit
```

### pass Conflicts

If pass git pull reports merge conflicts:

```bash
# Navigate to password store
cd ~/.password-store

# Show conflicted files
git status

# User must resolve manually:
# 1. Edit conflicted files
# 2. git add <resolved-files>
# 3. git commit
# 4. pass git push
```

### Homebrew Errors

If brew upgrade fails:

- Report specific package failures
- Suggest running `brew doctor` for diagnostics
- May need to uninstall problematic packages

## Post-Update Actions

After successful updates:

1. **Verify yadm alternates** (if you use OS-specific configs):
   ```bash
   yadm alt
   ```

2. **Check for Brewfile changes** (if Brewfile is tracked):
   ```bash
   brew bundle check --file=~/.zshrcd/conf.d/Brewfile
   ```

3. **Report summary** to user:
   - yadm: "Dotfiles up to date" or "Pulled X changes"
   - pass: "Password store up to date" or "Pulled X changes"
   - brew: "Upgraded X packages" or "All packages up to date"

## Integration with yadm-utilities

If yadm operations become complex (conflicts, bootstrap needed, alternate management), invoke the **yadm-utilities skill** for detailed guidance.

## Common Scenarios

### Scenario 1: All Up to Date

```
==> Updating yadm dotfiles...
Already up to date.

==> Updating pass password store...
Already up to date.

==> Updating Homebrew...
Already up-to-date.
```

**Response**: "All systems up to date. No updates needed."

### Scenario 2: Updates Available

```
==> Updating yadm dotfiles...
Updating abc123..def456
Fast-forward
 .zshrcd/conf.d/new-tool.zsh | 10 ++++++++++
 1 file changed, 10 insertions(+)

==> Updating pass password store...
remote: Counting objects: 5, done.
Updating abc123..def456

==> Updating Homebrew...
==> Upgrading 3 outdated packages:
kubectl 1.28.0 -> 1.29.0
helm 3.13.0 -> 3.13.1
k9s 0.27.0 -> 0.28.0
```

**Response**: "Updates completed successfully:
- yadm: Pulled 1 file change
- pass: Updated password store
- brew: Upgraded 3 packages (kubectl, helm, k9s)"

### Scenario 3: Conflicts Detected

```
==> Updating yadm dotfiles...
error: Your local changes to the following files would be overwritten by merge:
    .zshrcd/.zshrc
Please commit your changes or stash them before you merge.
```

**Response**: "Update stopped: yadm has uncommitted changes. Please run:
```
yadm status
yadm add .zshrcd/.zshrc
yadm commit -m "Your commit message"
```
Then retry the update."

## Best Practices

1. **Run updates regularly**: Weekly or bi-weekly to avoid large update batches
2. **Review changes**: Check what was updated, especially for yadm dotfiles
3. **Test after updates**: Ensure shell still works, tools function correctly
4. **Commit local changes first**: Always commit yadm changes before pulling
5. **Backup before major updates**: Especially for critical system tools

## Quick Command Reference

| Command | Purpose |
|---------|---------|
| `yadm pull` | Update dotfiles from remote |
| `pass git pull` | Update password store |
| `brew update` | Update Homebrew formulae |
| `brew upgrade` | Upgrade outdated packages |
| `yadm status` | Check uncommitted dotfile changes |
| `brew outdated` | List packages with available updates |

## Security Considerations

- **yadm**: Never commit secrets or API keys
- **pass**: Encrypted by design, safe to sync
- **brew**: Review cask updates for trusted sources

You should execute all three updates efficiently, handle errors gracefully, and provide clear feedback to the user about what was updated.
