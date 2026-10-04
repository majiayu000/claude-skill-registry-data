---
name: system-report
description: Generate a comprehensive MacBook system health report. Use when Rick asks about system status, performance, or space.
disable-model-invocation: true
allowed-tools: Bash
---

# MacBook System Report

Run these commands and format the output:

```bash
echo "==============================================="
echo "MACBOOK SYSTEM REPORT"
echo "$(date)"
echo "==============================================="

echo ""
echo "DISK USAGE"
df -h / | tail -1 | awk '{print "   Total: "$2, "Used: "$3, "("$5")", "Free: "$4}'

echo ""
echo "MEMORY"
vm_stat | head -5

echo ""
echo "TOP CPU PROCESSES"
ps aux --sort=-%cpu | head -6

echo ""
echo "TOP MEMORY PROCESSES"
ps aux --sort=-%mem | head -6

echo ""
echo "CLEANABLE SPACE"
echo "   Browser Caches: $(du -sh ~/Library/Caches/Google 2>/dev/null | cut -f1 || echo 'N/A')"
echo "   System Caches: $(du -sh ~/Library/Caches 2>/dev/null | cut -f1)"
echo "   Logs: $(du -sh ~/Library/Logs 2>/dev/null | cut -f1)"
echo "   Downloads (30d+): $(find ~/Downloads -type f -mtime +30 2>/dev/null | wc -l | tr -d ' ') files"
echo "   Trash: $(du -sh ~/.Trash 2>/dev/null | cut -f1)"

echo ""
echo "BATTERY"
system_profiler SPPowerDataType 2>/dev/null | grep -A 3 "Health Information"

echo ""
echo "SECURITY"
echo "   Firewall: $(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)"
echo "   FileVault: $(fdesetup status 2>/dev/null)"
echo "   Updates: $(softwareupdate -l 2>&1 | head -3)"
echo "==============================================="
```

Present the results in a clean, formatted report with recommendations.
