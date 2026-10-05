---
name: qruiq-update
description: |
  Update all qruiq skills to the latest version from GitHub.
  Use when asked to "update qruiq skills", "upgrade qruiq", or "pull latest skills".
allowed-tools:
  - Bash
---

# qruiq-update

Pull the latest qruiq skills from GitHub and re-run setup to refresh symlinks.

## Steps

1. Run: `cd ~/.qruiq/skills && git pull`
2. Run: `~/.qruiq/skills/setup`
3. Report which skills were linked
