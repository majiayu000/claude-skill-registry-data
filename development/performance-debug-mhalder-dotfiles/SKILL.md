---
name: performance-debug
description: Diagnose system performance issues including CPU, memory, disk, and network. Use when the user says "server is slow", "high CPU", "out of memory", "disk full", "performance issues", or asks to debug system performance.
allowed-tools: Bash, Read, Grep
---

# Performance Debug

Diagnose CPU, memory, disk, and network performance bottlenecks.

## Instructions

1. Get system overview: `top`, `htop`, or `vmstat`
2. Identify the bottleneck type (CPU, memory, disk, network)
3. Drill down with specific tools
4. Identify the root cause process/resource
5. Recommend solutions

## Quick overview

```bash
# System summary
uptime
free -h
df -h
top -bn1 | head -20

# All-in-one view
htop  # or top
```

## CPU analysis

```bash
# High-level CPU usage
mpstat 1 5
top -bn1 -o %CPU | head -15

# Per-process CPU
pidstat 1 5
ps aux --sort=-%cpu | head -10

# Find CPU-intensive process
top -bn1 | grep -A10 "PID USER"
```

## Memory analysis

```bash
# Memory overview
free -h
vmstat 1 5

# Per-process memory
ps aux --sort=-%mem | head -10
pidstat -r 1 5

# Memory details
cat /proc/meminfo
smem -tk  # if available

# Find memory leaks (growth over time)
watch -n 5 'ps aux --sort=-%mem | head -10'
```

## Disk analysis

```bash
# Disk space
df -h
du -sh /* 2>/dev/null | sort -hr | head -10

# Disk I/O
iostat -x 1 5
iotop -b -n 5  # requires root

# Find large files
find / -type f -size +100M 2>/dev/null

# Find disk-heavy processes
pidstat -d 1 5
```

## Network analysis

```bash
# Connections and bandwidth
ss -tuln
ss -tunap | grep ESTAB
nethogs  # per-process bandwidth

# Network statistics
netstat -i
ip -s link

# Check for connection issues
ping -c 4 8.8.8.8
mtr --report google.com
```

## Common bottlenecks

| Symptom              | Indicator  | Solution                                  |
| -------------------- | ---------- | ----------------------------------------- |
| Load > cores         | CPU-bound  | Identify hot process, scale horizontally  |
| High %wa in top      | I/O wait   | Check disk, move to SSD, optimize queries |
| Low free + high swap | Memory     | Find leak, increase RAM, tune OOM         |
| High %si/%hi         | Interrupts | NIC issue, driver problem                 |

## Rules

- MUST check all four resources (CPU, memory, disk, network)
- MUST identify specific processes causing issues
- MUST provide actionable recommendations
- Never kill processes without user approval
- Always check if symptoms correlate with specific times (cron, traffic)
