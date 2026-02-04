---
name: network-admin
description: Manage servers on the local network (ubuntu-box and raspberrypi). Execute commands remotely via SSH, manage services, view logs, and coordinate with other skills.
---

# Network Admin Skill

This skill enables management of the two servers on the local network: ubuntu-box and raspberrypi.

## Overview

The network-admin skill provides capabilities to manage, debug, and maintain services running on two local servers. It can execute commands remotely via SSH, interact with running services, manage git repositories, and coordinate with other skills like service-monitor.

## Servers

### ubuntu-box
- **Host**: ubuntu-box.local:1222
- **SSH alias**: `ubuntu-box`
- **User**: seth
- **Access**: `ssh ubuntu-box`

### raspberrypi (pi)
- **Host**: raspberrypi.local:2222
- **SSH alias**: `pi`
- **User**: seth
- **Access**: `ssh pi`
- **Role**: Internet gateway, reverse proxy, OAuth gateway, security enforcement
- **Key Services**: Caddy, oauth2-proxy instances, fail2ban, service-monitor
- **Note**: For internet traffic and reverse proxy management, see the `reverse-proxy` skill

## SSH Configuration

Both servers are configured in `~/.ssh/config` for easy access:

```bash
# Direct SSH access
ssh ubuntu-box
ssh pi

# Execute remote commands
ssh ubuntu-box "command here"
ssh pi "command here"
```

## Claude Code on Remote Servers

Both servers have Claude Code installed with an alias `lfg` that runs Claude without permissions:

```bash
# Interactive Claude session on remote server
ssh ubuntu-box
lfg  # Alias for: claude --dangerously-skip-permissions

# Or from local machine
ssh ubuntu-box -t "cd /path/to/project && lfg"
```

**Use Case**: Delegate long-running debugging tasks or complex multi-step operations to Claude running directly on the server.

## Common Operations

### 1. Check Service Status

```bash
# Check systemd service status
ssh pi "systemctl status service-monitor"
ssh ubuntu-box "systemctl status nginx"

# List all running services
ssh pi "systemctl list-units --type=service --state=running"

# Check service logs
ssh pi "journalctl -u service-monitor -n 50 --no-pager"
ssh pi "journalctl -u service-monitor -f"  # Follow logs
```

### 2. Manage Git Repositories

```bash
# Check repository status
ssh pi "cd ~/Software/dev/claude-share && git status"

# Pull latest changes
ssh pi "cd ~/Software/dev/claude-share && git pull"

# Checkout a specific branch
ssh pi "cd ~/Software/dev/claude-share && git checkout main"

# View recent commits
ssh pi "cd ~/Software/dev/claude-share && git log --oneline -10"
```

### 3. Service Management

```bash
# Restart a service
ssh pi "sudo systemctl restart service-monitor"

# Stop a service
ssh pi "sudo systemctl stop service-monitor"

# Start a service
ssh pi "sudo systemctl start service-monitor"

# Enable service at boot
ssh pi "sudo systemctl enable service-monitor"

# Reload systemd after config changes
ssh pi "sudo systemctl daemon-reload"
```

### 4. Service Monitor Integration

The service-monitor runs on raspberrypi.local:8000. Network-admin can:

```bash
# Check service-monitor health
curl -s http://raspberrypi.local:8000/health | jq .

# View all monitored services
curl -s http://raspberrypi.local:8000/services | jq .

# Check service-monitor logs on the server
ssh pi "journalctl -u service-monitor -n 100 --no-pager"

# Restart service-monitor
ssh pi "sudo systemctl restart service-monitor && sleep 2 && curl -s http://raspberrypi.local:8000/health"
```

### 5. Process Management

```bash
# Check if a process is running
ssh pi "pgrep -f service-monitor"
ssh ubuntu-box "pgrep -f nginx"

# View process details
ssh pi "ps aux | grep service-monitor"

# Kill a process (if needed)
ssh pi "pkill -f service-monitor"
```

### 6. File System Operations

```bash
# Check disk usage
ssh pi "df -h"
ssh ubuntu-box "df -h"

# Check directory size
ssh pi "du -sh ~/Software/dev/claude-share"

# View file contents
ssh pi "cat ~/Software/dev/service-monitor/monitored_services.json"

# Check file permissions
ssh pi "ls -la ~/Software/dev/service-monitor/"
```

### 7. Network Diagnostics

```bash
# Test connectivity between servers
ssh ubuntu-box "ping -c 3 raspberrypi.local"

# Check open ports
ssh pi "sudo netstat -tulpn | grep LISTEN"
ssh pi "sudo ss -tulpn | grep LISTEN"

# Test service availability
ssh pi "curl -s http://localhost:8000/health"
```

### 8. System Information

```bash
# Check system resources
ssh pi "free -h"
ssh pi "uptime"
ssh pi "top -bn1 | head -20"

# Check OS version
ssh pi "cat /etc/os-release"

# Check Python version
ssh pi "python3 --version"
```

## Workflow Examples

### Add New Service to service-monitor

1. **Check current configuration**:
   ```bash
   curl -s http://raspberrypi.local:8000/monitored-services | jq .
   ```

2. **Add new service via API**:
   ```bash
   curl -X POST http://raspberrypi.local:8000/monitored-services \
     -H "Content-Type: application/json" \
     -d '{
       "name": "new-service",
       "health_url": "http://ubuntu-box.local:3000/health",
       "check_interval_seconds": 60,
       "enabled": true
     }'
   ```

3. **Verify on server**:
   ```bash
   ssh pi "cat ~/Software/dev/service-monitor/monitored_services.json | jq ."
   ssh pi "journalctl -u service-monitor -n 20 --no-pager"
   ```

### Update and Deploy Changes

1. **Pull latest changes on server**:
   ```bash
   ssh pi "cd ~/Software/dev/claude-share && git pull"
   ```

2. **Restart affected service**:
   ```bash
   ssh pi "sudo systemctl restart service-monitor"
   ```

3. **Verify service is healthy**:
   ```bash
   ssh pi "systemctl status service-monitor"
   curl -s http://raspberrypi.local:8000/health | jq .
   ```

### Debug Service Issues

1. **Check service status**:
   ```bash
   ssh pi "systemctl status service-monitor"
   ```

2. **View recent logs**:
   ```bash
   ssh pi "journalctl -u service-monitor -n 100 --no-pager"
   ```

3. **Check for errors**:
   ```bash
   ssh pi "journalctl -u service-monitor --since '10 minutes ago' | grep -i error"
   ```

4. **For complex debugging, delegate to remote Claude**:
   ```bash
   ssh pi -t "cd ~/Software/dev/service-monitor && lfg"
   # Then describe the issue to Claude running on the server
   ```

### Check System Health

1. **Check all systemd services**:
   ```bash
   ssh pi "systemctl list-units --type=service --state=failed"
   ssh ubuntu-box "systemctl list-units --type=service --state=failed"
   ```

2. **Check resource usage**:
   ```bash
   ssh pi "free -h && df -h"
   ssh ubuntu-box "free -h && df -h"
   ```

3. **Verify network connectivity**:
   ```bash
   ssh ubuntu-box "ping -c 3 raspberrypi.local"
   ssh pi "ping -c 3 ubuntu-box.local"
   ```

## Usage Guidelines

### When to Use network-admin

Use this skill for:
- Checking service status across servers
- Managing git repositories on remote servers
- Restarting or managing systemd services
- Viewing logs for debugging
- Quick remote command execution
- Coordinating with service-monitor
- System health checks

**Note**: For internet-facing gateway operations (Caddy reverse proxy, OAuth configuration, fail2ban security, public routing), use the `reverse-proxy` skill instead.

### When to Delegate

**Delegate to remote Claude (via `lfg`)** when:
- Task requires multiple interactive steps
- Deep debugging of application code
- Making code changes on the server
- Running complex scripts or tests
- Long-running operations that benefit from persistent context

**Escalate to chief admin (Seth)** when:
- Task is too large or complex
- System-level changes are needed (security, networking, etc.)
- Multiple servers need coordinated changes
- Uncertain about the right approach
- Task requires decisions about architecture or design

### Best Practices

1. **Check before changing**: Always check current state before making changes
2. **Use jq for JSON**: Format JSON responses with `jq` for readability
3. **View logs**: Check logs after making changes to verify success
4. **Test connectivity**: Ensure services are reachable before debugging
5. **Document commands**: Be explicit about what commands are being run
6. **Handle errors gracefully**: Check command exit codes and provide clear feedback
7. **Coordinate with skills**: Use service-monitor skill for monitoring operations

## Common Locations

### Raspberry Pi
- **claude-share**: `~/Software/dev/claude-share`
- **service-monitor**: `~/Software/dev/service-monitor`
- **squelch** (gateway configs): `~/Software/dev/squelch`
  - oauth-caddy-package/
  - squelch-package/
  - config-backup/caddy/Caddyfile
  - config-backup/oauth2-proxy/*.cfg
- **systemd units**: `/etc/systemd/system/`
- **logs**: `journalctl -u <service-name>`
- **Caddy logs**: `/var/log/caddy/access.log`

### Ubuntu Box
- **claude-share**: `~/Software/dev/claude-share`
- **systemd units**: `/etc/systemd/system/`
- **logs**: `journalctl -u <service-name>`

## Error Handling

Common issues and solutions:

### SSH Connection Failed
```bash
# Check if server is reachable
ping -c 3 raspberrypi.local
ping -c 3 ubuntu-box.local
```

### Service Won't Start
```bash
# Check service status
ssh pi "systemctl status service-monitor"

# View full logs
ssh pi "journalctl -xe -u service-monitor"

# Check for port conflicts
ssh pi "sudo netstat -tulpn | grep 8000"
```

### Git Pull Fails
```bash
# Check for uncommitted changes
ssh pi "cd ~/Software/dev/claude-share && git status"

# Stash changes if needed
ssh pi "cd ~/Software/dev/claude-share && git stash"

# Then pull
ssh pi "cd ~/Software/dev/claude-share && git pull"
```

### Permission Denied
```bash
# Use sudo for system operations
ssh pi "sudo systemctl restart service-monitor"

# Check file ownership
ssh pi "ls -la ~/Software/dev/service-monitor"
```

## Integration with Other Skills

### service-monitor
- Use network-admin to manage the service-monitor server
- Check logs, restart service, update configuration files
- Verify service-monitor health after changes

### reverse-proxy
- Use reverse-proxy skill for managing internet-facing gateway on raspberrypi
- Handles Caddy reverse proxy configuration and OAuth2 authentication
- Manages fail2ban security and traffic analysis
- Reference: squelch repository (`~/Software/dev/squelch`) is source of truth for gateway configs
- **When to use which**:
  - **network-admin**: General server management, service restarts, log viewing, git operations
  - **reverse-proxy**: Public routing, OAuth configuration, security monitoring, traffic management

### Future Skills
- Network-admin can leverage any skill in claude-share
- Skills can be used by remote Claude sessions via `lfg`
- Coordinate between local and remote Claude instances

## Examples

### Example 1: Add service and verify
```bash
# Add new service
curl -X POST http://raspberrypi.local:8000/monitored-services \
  -H "Content-Type: application/json" \
  -d '{"name": "web-app", "health_url": "http://ubuntu-box.local:3000/health", "check_interval_seconds": 60, "enabled": true}'

# Check logs on server
ssh pi "journalctl -u service-monitor -n 20 --no-pager | grep web-app"

# Verify it's being monitored
curl -s http://raspberrypi.local:8000/services/web-app | jq .
```

### Example 2: Update and deploy
```bash
# Pull changes
ssh pi "cd ~/Software/dev/service-monitor && git pull"

# Restart service
ssh pi "sudo systemctl restart service-monitor"

# Verify health
sleep 3
curl -s http://raspberrypi.local:8000/health | jq .
```

### Example 3: Debug with remote Claude
```bash
# SSH into server and start Claude
ssh pi -t "cd ~/Software/dev/service-monitor && lfg"

# In the remote Claude session:
# "The service-monitor is returning 500 errors. Can you help debug this?"
# Claude on the server will have direct access to files and logs
```
