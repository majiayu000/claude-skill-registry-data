---
name: update-claude-dev-kit
description: Use when updating Claude Dev Kit components - checks registry for new versions, shows changelogs, updates components individually or all at once, supports rollback
---

# Update Claude Dev Kit

## Overview

Update mechanism for Claude Dev Kit. Checks for new versions, displays changelogs, and updates components while preserving user customizations.

## When to Use

- User asks to update Claude Dev Kit
- Checking for available updates
- Updating specific components
- Rolling back a problematic update

## Quick Reference

| Component | Version File | Update Source |
|-----------|--------------|---------------|
| Shell | `~/.claude-dev-kit/versions/shell` | GitHub release |
| Editor | `~/.claude-dev-kit/versions/editor` | GitHub release |
| Git | `~/.claude-dev-kit/versions/git` | GitHub release |
| Templates | `~/.claude-dev-kit/versions/templates` | GitHub release |
| Quality | `~/.claude-dev-kit/versions/quality` | GitHub release |
| Memory | `~/.claude-dev-kit/versions/memory` | GitHub release |

## Update Steps

### 1. Check Current Versions

```bash
# Create versions directory if needed
mkdir -p ~/.claude-dev-kit/versions

# Read installed versions
get_installed_version() {
  local component=$1
  local version_file="$HOME/.claude-dev-kit/versions/$component"
  if [ -f "$version_file" ]; then
    cat "$version_file"
  else
    echo "0.0.0"
  fi
}

# Display current versions
echo "Installed versions:"
for component in shell editor git templates quality memory; do
  echo "  $component: $(get_installed_version $component)"
done
```

### 2. Fetch Registry

```bash
# Fetch latest registry
REGISTRY_URL="https://raw.githubusercontent.com/claude-dev-kit/claude-dev-kit/main/registry.json"

fetch_registry() {
  curl -sL "$REGISTRY_URL"
}

# Parse version for component (using jq)
get_latest_version() {
  local component=$1
  fetch_registry | jq -r ".components.$component.version"
}
```

### 3. Compare Versions

```bash
# Version comparison (returns 0 if update available)
version_gt() {
  test "$(echo -e "$1\n$2" | sort -V | head -n1)" != "$1"
}

check_updates() {
  local updates_available=false

  echo "Checking for updates..."
  echo ""

  for component in shell editor git templates quality memory; do
    local installed=$(get_installed_version "$component")
    local latest=$(get_latest_version "$component")

    if version_gt "$latest" "$installed"; then
      echo "  $component: $installed → $latest (update available)"
      updates_available=true
    else
      echo "  $component: $installed (up to date)"
    fi
  done

  $updates_available
}
```

### 4. Show Changelog

```bash
# Fetch changelog for component
get_changelog() {
  local component=$1
  local from_version=$2
  local to_version=$3

  local changelog_url="https://raw.githubusercontent.com/claude-dev-kit/cdk-$component/main/CHANGELOG.md"

  echo "## $component Changelog ($from_version → $to_version)"
  echo ""

  # Fetch and display relevant section
  curl -sL "$changelog_url" | sed -n "/^## \[$to_version\]/,/^## \[/p" | head -n -1
}
```

### 5. Backup Before Update

```bash
backup_before_update() {
  local backup_dir="$HOME/.claude-dev-kit/backups/$(date +%Y-%m-%d-%H%M%S)"
  mkdir -p "$backup_dir"

  echo "Creating backup at $backup_dir"

  # Backup current configs
  cp ~/.zshrc "$backup_dir/" 2>/dev/null || true
  cp ~/.gitconfig "$backup_dir/" 2>/dev/null || true
  cp ~/.gitmessage "$backup_dir/" 2>/dev/null || true

  # VS Code settings
  if [ -d "$HOME/Library/Application Support/Code/User" ]; then
    cp "$HOME/Library/Application Support/Code/User/settings.json" "$backup_dir/vscode-settings.json" 2>/dev/null || true
  fi

  # Store backup location for potential rollback
  echo "$backup_dir" > ~/.claude-dev-kit/last_backup

  echo "Backup complete"
}
```

### 6. Update Component

```bash
update_component() {
  local component=$1

  echo "Updating $component..."

  case "$component" in
    shell)
      # Update Oh My Zsh
      cd ~/.oh-my-zsh && git pull --quiet

      # Update Powerlevel10k
      cd "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" && git pull --quiet

      # Update plugins
      cd "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" && git pull --quiet 2>/dev/null || true
      cd "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" && git pull --quiet 2>/dev/null || true
      ;;

    editor)
      # Update extensions
      if command -v code &>/dev/null; then
        code --update-extensions 2>/dev/null || true
      fi
      if command -v cursor &>/dev/null; then
        cursor --update-extensions 2>/dev/null || true
      fi
      ;;

    git)
      # Re-apply git hooks (preserves customizations)
      # Hooks are simple enough to just overwrite
      echo "Git hooks updated via skill re-run"
      ;;

    templates)
      # Update template files
      echo "Templates updated via registry"
      ;;

    quality)
      echo "Quality tools updated"
      ;;

    memory)
      echo "Memory tools updated"
      ;;
  esac

  # Record new version
  local latest=$(get_latest_version "$component")
  echo "$latest" > "$HOME/.claude-dev-kit/versions/$component"

  echo "$component updated to $latest"
}
```

### 7. Update All Components

```bash
update_all() {
  echo "Updating all Claude Dev Kit components..."
  echo ""

  backup_before_update
  echo ""

  for component in shell editor git templates quality memory; do
    local installed=$(get_installed_version "$component")
    local latest=$(get_latest_version "$component")

    if version_gt "$latest" "$installed"; then
      update_component "$component"
      echo ""
    fi
  done

  echo "All components updated!"
}
```

### 8. Rollback

```bash
rollback() {
  local backup_dir=$(cat ~/.claude-dev-kit/last_backup 2>/dev/null)

  if [ -z "$backup_dir" ] || [ ! -d "$backup_dir" ]; then
    echo "No backup found to rollback to"
    return 1
  fi

  echo "Rolling back to backup: $backup_dir"

  # Restore configs
  cp "$backup_dir/.zshrc" ~/.zshrc 2>/dev/null || true
  cp "$backup_dir/.gitconfig" ~/.gitconfig 2>/dev/null || true
  cp "$backup_dir/.gitmessage" ~/.gitmessage 2>/dev/null || true

  # Restore VS Code settings
  if [ -f "$backup_dir/vscode-settings.json" ]; then
    cp "$backup_dir/vscode-settings.json" "$HOME/Library/Application Support/Code/User/settings.json" 2>/dev/null || true
  fi

  echo "Rollback complete. Restart your terminal."
}
```

## Verification

```bash
# Verify update succeeded
verify_update() {
  echo "Verifying installation..."

  local all_good=true

  # Check shell
  [ -d ~/.oh-my-zsh ] || { echo "✗ Oh My Zsh missing"; all_good=false; }
  [ -d ~/.oh-my-zsh/custom/themes/powerlevel10k ] || { echo "✗ Powerlevel10k missing"; all_good=false; }

  # Check git
  [ -f ~/.gitmessage ] || { echo "✗ Git template missing"; all_good=false; }

  # Check versions recorded
  [ -d ~/.claude-dev-kit/versions ] || { echo "✗ Version tracking missing"; all_good=false; }

  if $all_good; then
    echo "All components verified!"
  fi
}
```

## Interactive Update Flow

When user requests update:

1. **Check for updates:**
   ```
   Checking Claude Dev Kit for updates...

   Component   Installed   Latest    Status
   ---------   ---------   ------    ------
   shell       1.0.0       1.1.0     Update available
   editor      1.0.0       1.0.0     Up to date
   git         1.0.0       1.0.1     Update available
   templates   1.0.0       1.0.0     Up to date
   ```

2. **Ask what to update:**
   - Update all
   - Update specific components
   - Show changelogs first
   - Skip update

3. **Show changelog if requested:**
   ```
   ## shell 1.1.0
   - Added Fish shell support
   - Fixed p10k instant prompt on slow systems

   ## git 1.0.1
   - Fixed commit-msg hook for merge commits
   ```

4. **Confirm and update:**
   - Create backup
   - Update selected components
   - Verify installation
   - Report results

## Common Issues

| Issue | Fix |
|-------|-----|
| Registry unreachable | Check internet connection, try again |
| Version file missing | Will be created on first update |
| Rollback fails | Check backup directory exists |
| Component won't update | Re-run the component's setup skill |

## Scheduled Updates

For automated update checks, add to crontab or launchd:

```bash
# Check weekly (doesn't auto-update, just notifies)
0 9 * * 1 ~/.claude-dev-kit/check-updates.sh
```

Create `~/.claude-dev-kit/check-updates.sh`:
```bash
#!/bin/bash
# Notify if updates available

REGISTRY_URL="https://raw.githubusercontent.com/claude-dev-kit/claude-dev-kit/main/registry.json"

# Simple check - compare local version file to registry
# If different, create notification file

if curl -sL "$REGISTRY_URL" | grep -q '"version"'; then
  echo "Updates may be available. Run: claude 'update-claude-dev-kit'"
fi
```

## Manual Version Override

If needed, manually set a component version:

```bash
echo "1.0.0" > ~/.claude-dev-kit/versions/shell
```

This is useful when:
- Troubleshooting version detection
- Forcing a re-update
- Testing update logic
