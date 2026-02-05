---
name: fossil-ui
description: Git to Fossil export
---

# Fossil UI

Export current git repository to Fossil database and launch web UI for browsing.

## Workflow

### 1. Verify Prerequisites

```bash
which fossil && fossil version
```

If fossil not installed:
```bash
# macOS
brew install fossil

# Ubuntu/Debian
sudo apt-get install fossil
```

### 2. Generate Database Path

Store in temp directory with project-based naming:

```
/tmp/fossil-ui/<project-dirname>.fossil
```

Example: `/Users/choi/.claude` -> `/tmp/fossil-ui/claude.fossil`

```bash
mkdir -p /tmp/fossil-ui
```

### 3. Clean Existing Database

Remove existing database before creating new one (ephemeral usage):

```bash
rm -f /tmp/fossil-ui/<name>.fossil
```

### 4. Export and Import

```bash
git fast-export --all | fossil import --git /tmp/fossil-ui/<name>.fossil
```

### 5. Launch Fossil UI

```bash
fossil ui --page timeline /tmp/fossil-ui/<name>.fossil
```

If port 8080 is in use:
```bash
fossil ui --page timeline -P 8081 /tmp/fossil-ui/<name>.fossil
```

Browser opens automatically to timeline view. Press `Ctrl+C` to stop the server.

## Notes

- Fossil admin password is displayed during import (save for UI admin access)
- Database is self-contained single file
- Verify import: `fossil info -R /tmp/fossil-ui/<name>.fossil`
- Temp files are cleaned on system reboot
