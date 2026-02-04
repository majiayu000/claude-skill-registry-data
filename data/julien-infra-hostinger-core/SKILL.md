---
name: julien-infra-hostinger-core
description: Core server management for Hostinger VPS srv759970 - SSH access, system status, maintenance tasks, and disk space reclamation. Use for any server operation, connection issues, or maintenance tasks.
license: Apache-2.0
triggers:
  - ssh hostinger
  - connect server
  - disk space
  - server maintenance
  - cleanup vps
  - free space
  - system status
---

# Hostinger VPS Core Management

Core infrastructure management for srv759970.hstgr.cloud.

## Server Info

| Property | Value |
|----------|-------|
| **Host** | 69.62.108.82 |
| **User** | automation (sudo, no reboot) |
| **Alias** | srv759970 |
| **OS** | Ubuntu 24.04 LTS |
| **Disk** | 193 GB total |
| **RAM** | 16 GB |

---

## 1. SSH Connection

### Quick Connect

```bash
ssh automation@69.62.108.82
# Or with alias
ssh srv759970
```

### SSH Config (~/.ssh/config)

```
Host srv759970
    HostName 69.62.108.82
    User automation
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
```

### Fix Permission Denied (Windows)

```powershell
$keyPath = "$env:USERPROFILE\.ssh\id_ed25519"
$acl = Get-Acl $keyPath
$acl.SetAccessRuleProtection($true, $false)
$acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) | Out-Null }
$user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($user, "FullControl", "Allow")
$acl.AddAccessRule($rule)
Set-Acl $keyPath $acl
```

---

## 2. System Status

### Quick Status Check

```bash
ssh srv759970 'free -h && df -h && uptime'
```

### Disk Space

```bash
ssh srv759970 'df -h | grep -E "Filesystem|/dev/"'
ssh srv759970 'du -sh /opt/* 2>/dev/null | sort -rh | head -10'
```

**Thresholds**: < 20 GB = Warning, < 10 GB = Critical

### Memory Usage

```bash
ssh srv759970 'free -h'
ssh srv759970 'docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" | head -15'
```

### Services Status

```bash
ssh srv759970 'docker ps --format "table {{.Names}}\t{{.Status}}"'
ssh srv759970 'systemctl status nginx docker'
ssh srv759970 'pm2 list'
```

---

## 3. Weekly Maintenance

### Docker Cleanup (Safe)

```bash
ssh srv759970 << 'EOF'
echo "=== Docker Cleanup ==="
docker system df
docker image prune -f
docker volume prune -f
docker system df
EOF
```

**Never run** `docker system prune -a` (breaks auto-start)

### System Health Check

```bash
ssh srv759970 << 'EOF'
echo "=== Health Check ==="
df -h /
free -h
docker ps -a --filter "status=exited" --format '{{.Names}}'
sudo certbot certificates | grep -E "Certificate Name|Expiry Date"
EOF
```

---

## 4. Space Reclamation

### Phase 1: Safe Cleanup (No approval needed)

```bash
ssh srv759970 << 'EOF'
# Dangling images (~1GB)
docker image prune -f

# Journal logs (~400MB)
sudo journalctl --vacuum-size=100M

# Safe log cleanup
sudo truncate -s 0 /var/log/rclone-music.log
sudo truncate -s 0 /var/log/nginx-auto-docker.log
EOF
```

### Phase 2: Moderate Cleanup (Ask user first)

```bash
# Old Docker images (>30 days)
docker image prune -a --filter 'until=720h'

# Unused volumes
docker volume prune -f
```

### Emergency Cleanup (< 5 GB available)

```bash
ssh srv759970 << 'EOF'
# Find large files
find /opt -type f -size +100M -exec ls -lh {} \; 2>/dev/null | head -20

# Large container logs
find /var/lib/docker/containers -name "*-json.log" -exec ls -lh {} \; | sort -k5 -hr | head -10

# Aggressive cleanup
docker system prune -f
sudo apt clean
EOF
```

---

## 5. Troubleshooting

### SSH Connection Issues

| Problem | Solution |
|---------|----------|
| Permission denied | Fix key permissions (see above) |
| Connection timeout | Check `ping 69.62.108.82` |
| Host key changed | `ssh-keygen -R 69.62.108.82` |

### View Logs

```bash
ssh srv759970 'sudo journalctl -n 100 --no-pager'
ssh srv759970 'sudo journalctl -u nginx -n 50'
```

---

## Automation User Restrictions

**CAN**: Docker, Nginx, services, SSL, packages, file permissions
**CANNOT**: Reboot, shutdown, modify sudo config

---

## Quick Reference

```bash
# Connect
ssh automation@69.62.108.82

# Status
ssh srv759970 'free -h && df -h && uptime'

# Docker
ssh srv759970 'docker ps && docker system df'

# Cleanup
ssh srv759970 'docker image prune -f && sudo journalctl --vacuum-size=100M'

# Logs
ssh srv759970 'sudo journalctl -n 100'
```
