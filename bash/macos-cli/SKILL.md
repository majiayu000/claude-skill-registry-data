---
name: macos-cli
description: >
  Navigate, script, and manage macOS terminal environments, accounting for BSD
  toolchain differences from GNU/Linux. Use when writing cross-platform shell
  scripts, diagnosing BSD sed/date/stat/find incompatibilities, managing Homebrew
  packages and services, configuring launchd agents, or inspecting macOS developer tools.
compatibility: >
  Agent Skills-compatible coding agents operating in macOS (Darwin) terminal environments.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "macos, bsd, homebrew, terminal, launchd, cross-platform, zsh"
  topics: "operating-systems, devtools"
---

# macOS CLI & BSD Incompatibilities

macOS is a certified UNIX system (Darwin) utilizing a **BSD-derived userland** and `zsh` as its default shell. Many Linux/GNU command-line idioms (e.g. GNU `sed -i`, `date -d`, `grep -P`, `find -printf`) fail or produce completely different results on macOS. Linux instructions must never be assumed to work on macOS without verification.

## Core Rules

1. **Never assume GNU CLI syntax works on macOS**: Commands like `sed`, `date`, `stat`, `find`, and `xargs` behave differently in BSD userland.
2. **Handle in-place editing safely**: BSD `sed -i` requires an explicit extension argument (`sed -i '' 's/.../.../'`); GNU `sed -i` does not.
3. **Use Homebrew non-interactively in automation**: Always set `NONINTERACTIVE=1` when running `brew install` in scripts.
4. **Use `launchd` instead of `systemd`**: macOS does not have systemd; background services are managed via `launchctl` and LaunchAgent/LaunchDaemon plists.
5. **Inspect file quarantine flags**: Files downloaded from the internet may have the `com.apple.quarantine` extended attribute, blocking CLI execution.

---

## 1. Critical BSD vs GNU CLI Differences

### 1. `sed -i` (In-Place Substitution)
- **Linux (GNU sed)**: `sed -i 's/foo/bar/g' file.txt`
- **macOS (BSD sed)**: Requires an empty string argument for no backup:
  ```bash
  sed -i '' 's/foo/bar/g' file.txt
  ```
- **Cross-platform portable idiom**:
  ```bash
  sed 's/foo/bar/g' file.txt > file.txt.tmp && mv file.txt.tmp file.txt
  ```

### 2. `date` (Formatting & Arithmetic)
- **Linux (GNU date)**: `date -d "yesterday" +%Y-%m-%d`
- **macOS (BSD date)**: Uses `-v` flag:
  ```bash
  date -v-1d +%Y-%m-%d
  ```

### 3. `stat` (File Metadata)
- **Linux (GNU stat)**: `stat -c %s file.txt` (file size in bytes)
- **macOS (BSD stat)**: Uses `-f` flag:
  ```bash
  stat -f %z file.txt
  ```

### 4. `find` and `xargs`
- GNU `find . -printf` is **not supported** in BSD find.
- BSD `xargs` does not support `-r` / `--no-run-if-empty` (which is default behavior in BSD).
- Always use null termination for safe handling of paths with spaces:
  ```bash
  find . -type f -name "*.log" -print0 | xargs -0 rm -f
  ```

---

## 2. Package & Service Management with Homebrew

Homebrew installs software in `/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel x86_64).

```bash
# Verify installation architecture and path
brew --prefix
# Apple Silicon: /opt/homebrew
# Intel: /usr/local

# Non-interactive package installation
NONINTERACTIVE=1 brew install ripgrep jq uv

# Manage user-space background services (wrapper around launchd)
brew services start postgresql@16
brew services list
brew services stop postgresql@16
```

---

## 3. macOS Background Services: `launchd`

macOS services are configured as XML Property List (`.plist`) files placed in:
- `~/Library/LaunchAgents/` (user-specific services run when user logs in).
- `/Library/LaunchDaemons/` (system-wide daemons run as root at system boot).

### Example LaunchAgent Plist (`~/Library/LaunchAgents/com.user.task.plist`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.task</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/username/scripts/sync.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/task.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/task.err</string>
</dict>
</plist>
```

Managing with `launchctl`:
```bash
# Load and start the agent
launchctl load ~/Library/LaunchAgents/com.user.task.plist

# Check if agent is loaded
launchctl list | grep "com.user.task"

# Unload agent
launchctl unload ~/Library/LaunchAgents/com.user.task.plist
```

---

## 4. macOS Security: Gatekeeper, Codesign, and Quarantine

When binaries or scripts fail with "Killed: 9" or permission prompts:

```bash
# Check extended attributes on a downloaded binary
xattr -l ./my-binary

# Remove macOS quarantine attribute from trusted tools
xattr -d com.apple.quarantine ./my-binary

# Verify code signature
codesign -dv --verbose=4 ./my-binary
```

---

## 5. Writing Cross-Platform Shell Scripts

Detect the host operating system at runtime:

```bash
case "$(uname -s)" in
  Darwin*)
    OS="macos"
    SED_INPLACE=(-i '')
    ;;
  Linux*)
    OS="linux"
    SED_INPLACE=(-i)
    ;;
  *)
    echo "Unsupported operating system" >&2
    exit 1
    ;;
esac

# Execute sed portably:
sed "${SED_INPLACE[@]}" 's/old/new/g' config.txt
```

---

## 6. Verification Checklist

- [ ] Script does not invoke GNU-specific flags (`sed -i` without extension, `date -d`, `grep -P`).
- [ ] Homebrew commands account for Apple Silicon (`/opt/homebrew`) path differences.
- [ ] Executable scripts and binaries have quarantine attributes cleared if necessary.
- [ ] Services are configured via `launchd` / `brew services`, not `systemctl`.
