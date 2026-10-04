---
name: clean-mac
description: Clean caches, temp files, logs, and junk from MacBook to free up space. Use when Rick says clean, free space, or optimize Mac.
disable-model-invocation: true
allowed-tools: Bash
---

# Clean MacBook

Run each step, report space freed:

```bash
echo "Starting MacBook cleanup..."
BEFORE=$(df -k / | tail -1 | awk '{print $4}')

# Browser caches
rm -rf ~/Library/Caches/Google/Chrome/Default/Cache/* 2>/dev/null
rm -rf ~/Library/Caches/com.apple.Safari/Cache.db 2>/dev/null

# System caches (user level)
rm -rf ~/Library/Caches/* 2>/dev/null

# Logs
rm -rf ~/Library/Logs/* 2>/dev/null

# DNS cache
sudo dscacheutil -flushcache 2>/dev/null
sudo killall -HUP mDNSResponder 2>/dev/null

# npm/pnpm caches
pnpm store prune 2>/dev/null
npm cache clean --force 2>/dev/null

# Homebrew cleanup
brew cleanup --prune=all 2>/dev/null
brew autoremove 2>/dev/null

# Docker cleanup (if running)
docker system prune -af --volumes 2>/dev/null

# Old downloads (30+ days)
find ~/Downloads -type f -mtime +30 -exec rm -f {} \; 2>/dev/null

# Trash
rm -rf ~/.Trash/* 2>/dev/null

# Xcode derived data (if exists)
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null

AFTER=$(df -k / | tail -1 | awk '{print $4}')
FREED=$(( (AFTER - BEFORE) / 1024 ))
echo "Cleanup complete! Freed approximately ${FREED}MB"
```

Report total space freed and current disk status.
