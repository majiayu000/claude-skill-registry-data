---
name: system-monitoring
description: System resource monitoring including CPU, memory, disk, and network statistics. Use when checking system health, diagnosing performance issues, or monitoring resources.
allowed-tools: Bash, Read
mcp_tools:
  - "resource_cpu"
  - "resource_memory"
  - "resource_disk"
  - "resource_network"
  - "resource_overview"
  - "resource_battery"
  - "resource_os"
  - "resource_processes"
  - "resource_graphics"
  - "resource_usb"
---

# System Monitoring Skill

**Version**: 1.0.0
**Purpose**: System resource monitoring and health checks

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Overview | "system status", "health check", "システム状態" |
| CPU | "CPU usage", "check CPU", "CPU確認" |
| Memory | "memory usage", "RAM check", "メモリ確認" |
| Disk | "disk space", "storage", "ディスク容量" |
| Network | "network stats", "ネットワーク状態" |

---

## Integrated MCP Tools

| Tool | Purpose |
|------|---------|
| `resource_cpu` | CPU cores, usage, temperature |
| `resource_memory` | RAM usage, swap, available |
| `resource_disk` | Disk partitions, usage, I/O |
| `resource_network` | Interfaces, bandwidth, connections |
| `resource_overview` | Combined system overview |
| `resource_battery` | Battery status (laptops) |
| `resource_os` | OS information, uptime |
| `resource_processes` | Top processes by resource usage |
| `resource_graphics` | GPU information |
| `resource_usb` | Connected USB devices |

---

## Workflow: Health Check

### Phase 1: Quick Overview

#### Step 1.1: System Overview
```
Use resource_overview to get:
- OS information
- Uptime
- Load averages
- Quick resource summary
```

### Phase 2: Detailed Analysis

#### Step 2.1: CPU Analysis
```
Use resource_cpu to check:
- Core count
- Usage percentage
- Temperature
- Processes per core
```

#### Step 2.2: Memory Analysis
```
Use resource_memory to check:
- Total/used/free RAM
- Swap usage
- Memory pressure
```

#### Step 2.3: Disk Analysis
```
Use resource_disk to check:
- Partition usage
- Available space
- I/O statistics
```

#### Step 2.4: Network Analysis
```
Use resource_network to check:
- Interface status
- Bandwidth usage
- Active connections
```

### Phase 3: Process Investigation

#### Step 3.1: Top Processes
```
Use resource_processes to identify:
- CPU-heavy processes
- Memory-heavy processes
- Zombie processes
```

---

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU Usage | >70% | >90% |
| Memory Usage | >80% | >95% |
| Disk Usage | >80% | >95% |
| Load Average | >cores | >cores×2 |

---

## Diagnostic Commands

### Quick Health Check
```bash
# CPU load
uptime

# Memory
free -h

# Disk
df -h

# Top processes
top -bn1 | head -20
```

---

## Best Practices

✅ GOOD:
- Regular monitoring
- Set up alerts
- Track trends over time
- Document baseline metrics

❌ BAD:
- Ignore warnings
- No monitoring in production
- React only to outages
- No capacity planning

---

## Checklist

- [ ] CPU usage normal (<70%)
- [ ] Memory available (>20% free)
- [ ] Disk space sufficient (>20% free)
- [ ] Network interfaces up
- [ ] No zombie processes
- [ ] Load average acceptable
