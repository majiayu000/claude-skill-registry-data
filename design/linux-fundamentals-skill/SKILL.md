---
name: linux-fundamentals-skill
description: Complete Linux administration skill covering process management, filesystem, permissions, package management, users, bash scripting, and system monitoring.
sasmp_version: "1.3.0"
bonded_agent: 01-devops-fundamentals
bond_type: PRIMARY_BOND

parameters:
  - name: distro
    type: string
    required: false
    default: "ubuntu"
    validation: "^(ubuntu|debian|centos|rhel|fedora|arch)$"
  - name: operation
    type: string
    required: true
    enum: ["process", "filesystem", "permissions", "package", "user", "script", "monitor"]

retry_config:
  strategy: exponential_backoff
  initial_delay_ms: 1000
  max_retries: 3

observability:
  logging: structured
  metrics: enabled
---

# Linux Fundamentals Skill

## Overview
Master Linux system administration - the foundation of DevOps.

## Parameters
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| distro | string | No | ubuntu | Target distribution |
| operation | string | Yes | - | Operation category |

## Core Topics

### MANDATORY
- Process lifecycle and management (ps, top, kill)
- Filesystem hierarchy and operations
- File permissions (chmod, chown, ACLs)
- Package management (apt, yum, dnf)
- User and group administration
- Basic bash scripting

### OPTIONAL
- LVM and disk partitioning
- Systemd service management
- Log analysis with journalctl

### ADVANCED
- Kernel parameters and sysctl
- SELinux/AppArmor security
- Performance profiling

## Quick Reference

```bash
# Process Management
ps aux | grep [p]rocess          # Find process (avoid grep itself)
kill -15 PID                      # Graceful termination
kill -9 PID                       # Force kill (last resort)
pkill -f pattern                  # Kill by pattern
nohup command &                   # Background immune to hangup

# File Permissions
chmod 755 file                    # rwxr-xr-x
chmod u+x,g+r file               # Symbolic notation
chown -R user:group dir/         # Recursive ownership
setfacl -m u:user:rw file        # Set ACL

# Package Management (Debian/Ubuntu)
apt update && apt upgrade -y
apt install -y package
apt autoremove

# Package Management (RHEL/CentOS)
dnf update -y
dnf install package

# User Management
useradd -m -s /bin/bash user
usermod -aG sudo user
passwd user

# System Info
uname -a                          # Kernel info
cat /etc/os-release              # OS version
free -h                           # Memory usage
df -h                             # Disk usage
```

## Troubleshooting

### Common Failures
| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Permission denied | Insufficient privileges | Use sudo or check ownership |
| Command not found | Package not installed | Install with apt/dnf |
| No space left | Disk full | Clean /var/log, docker prune |
| High load | CPU/IO bottleneck | Use top, iotop |

### Debug Checklist
1. Check permissions: `id`, `ls -la`
2. Check disk: `df -h`, `du -sh /*`
3. Check memory: `free -h`
4. Check logs: `journalctl -xe`

### Recovery Procedures

#### Out of Disk Space
1. Find large files: `du -sh /* | sort -rh | head`
2. Clean cache: `apt clean`
3. Rotate logs: `journalctl --vacuum-size=100M`

## Resources
- [Linux Journey](https://linuxjourney.com)
- [TLDR Pages](https://tldr.sh)
