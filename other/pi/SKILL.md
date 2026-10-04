---
name: pi
description: Raspberry Pi health check and OpenClaw status. One command to see if Pi is alive and what it did overnight.
user-invocable: true
---

# Pi / OpenClaw Status

Check Pi health and OpenClaw state. Best-effort; if Pi unreachable, say so and stop.

## 1. Connectivity + System Health

```bash
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no davidferra@10.0.0.177 "
echo '=== UPTIME ==='
uptime
echo '=== DISK ==='
df -h / | tail -1
echo '=== MEMORY ==='
free -h | head -2
echo '=== CPU TEMP ==='
vcgencmd measure_temp 2>/dev/null || echo 'N/A'
echo '=== DOCKER ==='
docker ps --format '{{.Names}} {{.Status}}' 2>/dev/null || echo 'no docker'
" 2>/dev/null || echo "PI UNREACHABLE - not on home network?"
```

## 2. OpenClaw Services

```bash
ssh -o ConnectTimeout=5 davidferra@10.0.0.177 "
echo '=== OPENCLAW SERVICES ==='
systemctl is-active openclaw-dashboard 2>/dev/null || echo 'dashboard: inactive'
systemctl is-active openclaw-scraper 2>/dev/null || echo 'scraper: inactive'
echo '=== RECENT CRON OUTPUT (last 10 lines) ==='
tail -10 /var/log/syslog 2>/dev/null | grep -i 'cron\|openclaw' || echo 'no recent cron activity'
echo '=== PRICES.DB SIZE ==='
ls -lh ~/prices.db 2>/dev/null || echo 'prices.db not found'
" 2>/dev/null
```

## 3. Report Format

```
PI STATUS - [date]

CONNECTION:  [reachable/unreachable]
UPTIME:      [X days]
DISK:        [used/total]
MEMORY:      [used/total]
CPU TEMP:    [temp]
OPENCLAW:    dashboard [active/inactive] | scraper [active/inactive]
PRICES.DB:   [size]
RECENT:      [any cron activity summary]
```

If unreachable, report that and stop. Don't retry or troubleshoot.
