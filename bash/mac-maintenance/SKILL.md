---
name: mac-maintenance
description: >-
  Runs macOS upkeep: Homebrew update and upgrade, pulling clean git repositories, and emptying the
  Trash. Use when asked for Mac cleanup, maintenance, or a refresh of packages and repos.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# Mac Maintenance

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use when asked for Mac cleanup, maintenance, or package/repo refresh.

## Run

### 1. Homebrew update

```bash
brew update && brew upgrade
```

### 2. Pull repos

```bash
for repo in ~/Projects/*/.git; do
  dir=${repo:h}
  git -C "$dir" status --short --branch
  git -C "$dir" pull --ff-only
done
```

Skip dirty repos unless explicitly asked to handle them. Report skipped paths.

### 3. Empty Trash (macOS)

```bash
osascript -e 'tell application "Finder" to empty trash'
```

## Summary

Finish with terse counts:
- brew: `N packages upgraded` / `already current`
- repos: `N pulled` / `N skipped (dirty)` / `N failed`
- trash: `emptied` / `failed`
