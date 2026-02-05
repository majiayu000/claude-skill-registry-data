---
name: tailscale-manager
description: Manage Tailscale funnels across different ct project instances. Start/stop funnels and route traffic to different docker containers.
---

# Tailscale Funnel Manager

## Purpose

This skill manages Tailscale funnels to expose local docker containers to the internet via Tailscale. Each `ct*` project runs on a different port, and we use Tailscale funnels to route HTTPS traffic to these local ports.

## Port Mapping Pattern

Each ct project uses a specific port pattern:

| Project | API Port | Database Port | Redis Port |
|---------|----------|---------------|------------|
| ct1     | 8081     | 5431          | 6371       |
| ct2     | 8082     | 5432          | 6372       |
| ct3     | 8083     | 5433          | 6373       |
| ct4     | 8084     | 5434          | 6374       |
| ct5     | 8085     | 5435          | 6375       |
| ct6     | 8086     | 5436          | 6376       |
| ct7     | 8087     | 5437          | 6377       |
| ct8     | 8088     | 5438          | 6378       |

**Pattern:**
- API: `808X` where X is the ct number
- Database: `543X` where X is the ct number
- Redis: `637X` where X is the ct number

## ⚠️ CRITICAL: Only ONE Funnel at a Time

**Only one funnel can run on port 443 at a time.** You MUST stop the existing funnel before starting a new one.

## Foreground vs Background Mode

Tailscale funnels can run in two modes:

### Foreground Mode (Default)
```bash
sudo tailscale funnel --https=443 8082
```

**Characteristics:**
- Runs ONLY while the command is active (ephemeral)
- Automatically closes when you press Ctrl+C or terminal session ends
- **Does NOT show in `tailscale funnel status`** (this is expected!)
- Must be restarted after reboot or terminal disconnect
- Good for temporary testing only
- Provides real-time feedback and logging

**⚠️ IMPORTANT**: `tailscale funnel status` will show **"No serve config"** even though the funnel IS working. This is because foreground funnels are ephemeral and don't write persistent configuration. Use `ps aux | grep funnel` to verify foreground funnels.

**⚠️ WARNING**: Foreground mode will stop if your terminal session ends. For persistent funnels, use background mode.

### Background Mode (Persistent)
```bash
sudo tailscale funnel --bg 8082
```

**Characteristics:**
- Runs persistently until explicitly stopped
- **Shows in `tailscale funnel status`** ✅
- Survives reboots and Tailscale restarts
- Must be stopped with `sudo tailscale funnel --https=443 off`
- Good for long-running production use

**When to use background mode:**
- Long-running services
- When you need `tailscale funnel status` to show configuration
- Production deployments
- When you want funnel to survive reboots

## Managing Funnels

### ALWAYS Check Current Status First

```bash
sudo tailscale funnel status
```

**Expected output for BACKGROUND mode funnel:**
```
# Funnel on:
#     - https://wakeup.tail<hash>.ts.net
#
https://wakeup.tail<hash>.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:8084
```

**Expected output when no background funnel OR foreground funnel running:**
```
# Funnel on:
No serve config
```

⚠️ **"No serve config" does NOT mean no funnel is running!** Foreground funnels don't show here. Check processes:

### Check Running Funnel Processes

**This is the ONLY reliable way to check if a foreground funnel is running:**

```bash
ps aux | grep -E "tailscale.*funnel" | grep -v grep
```

### Start a Funnel

#### Option 1: Foreground Mode (Temporary/Testing)

**For ct2 (port 8082):**
```bash
sudo tailscale funnel --https=443 8082
# OR shorter form:
sudo tailscale funnel 8082
```

**For ct4 (port 8084):**
```bash
sudo tailscale funnel --https=443 8084
# OR shorter form:
sudo tailscale funnel 8084
```

**For any ct project:**
```bash
# Replace X with the ct number (2, 3, 4, etc.)
sudo tailscale funnel 808X
```

#### Option 2: Background Mode (Persistent/Production)

**For ct2 (port 8082):**
```bash
sudo tailscale funnel --bg 8082
```

**For ct4 (port 8084):**
```bash
sudo tailscale funnel --bg 8084
```

**For any ct project:**
```bash
# Replace X with the ct number (2, 3, 4, etc.)
sudo tailscale funnel --bg 808X
```

### Stop a Running Funnel

#### Stopping Background Mode Funnels

**Method 1: Clean shutdown (ALWAYS USE THIS FOR BACKGROUND MODE)**
```bash
sudo tailscale funnel --https=443 off
```

This properly removes the persistent configuration and stops the background funnel.

#### Stopping Foreground Mode Funnels

**Method 1: Keyboard interrupt (PREFERRED)**
Press `Ctrl+C` in the terminal where the funnel is running.

**Method 2: Kill the process**
```bash
# Find the funnel process
ps aux | grep "tailscale funnel" | grep -v grep

# Kill it (replace PID with actual number)
sudo kill <PID>
```

#### Last Resort: Kill Stuck Processes

**Only use if the above methods don't work:**
```bash
# Find stuck funnel processes
ps aux | grep "tailscale funnel" | grep -v grep

# Force kill (replace PIDs with actual numbers)
sudo kill -9 <PID>
```

**⚠️ WARNING**: Only kill `tailscale funnel` processes. NEVER kill the main `tailscaled` daemon or `tailscaled be-child ssh` processes.

### Switch to a Different Port

**MANDATORY WORKFLOW:**

1. **Check current status:**
   ```bash
   sudo tailscale funnel status
   ```

2. **Stop existing funnel:**
   ```bash
   sudo tailscale funnel --https=443 off
   ```

3. **Verify it stopped:**
   ```bash
   sudo tailscale funnel status  # Should show "No serve config"
   ```

4. **Start new funnel:**
   ```bash
   sudo tailscale funnel --https=443 8082  # Switch to ct2
   ```

5. **Verify it started:**
   ```bash
   sudo tailscale funnel status
   ```

## Workflow

### Recommended: Background Mode (Simplest)

1. **Check current status:**
   ```bash
   sudo tailscale funnel status
   ```

2. **Stop any existing funnel:**
   ```bash
   sudo tailscale funnel --https=443 off
   ```

3. **Start background funnel:**
   ```bash
   sudo tailscale funnel --bg 8082  # For ct2
   ```

4. **Verify it's running:**
   ```bash
   sudo tailscale funnel status  # Should show configuration
   ```

### Alternative: Foreground Mode (For Testing/Debugging)

**⚠️ NOT RECOMMENDED**: Foreground funnels stop when terminal disconnects. Use background mode instead.

1. **Check what's currently running:**
   ```bash
   ps aux | grep "tailscale funnel"
   ```

2. **Stop any existing funnel:**
   - Background: `sudo tailscale funnel --https=443 off`
   - Foreground: Press `Ctrl+C` or `sudo kill <PID>`

3. **Start a new foreground funnel:**
   ```bash
   sudo tailscale funnel 8082  # For ct2
   ```

4. **Verify it's running:**
   ```bash
   ps aux | grep "tailscale funnel"  # Should show process
   ```

**Note**: Keep your terminal open - closing it will stop the funnel.

## Common Commands Reference

```bash
# List all docker containers with their ports
docker ps --format 'table {{.Names}}\t{{.Ports}}'

# Filter for specific ct project
docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep ct2

# Check tailscale device status
tailscale status

# Get the public URL for your machine
tailscale status | grep $(hostname)
```

## Troubleshooting

### "No serve config" But Funnel IS Running

**Cause**: You're running a foreground funnel, which doesn't show in `tailscale funnel status`

**This is NORMAL and EXPECTED behavior!** Foreground funnels are ephemeral and don't write persistent configuration.

**How to verify the funnel is actually working:**
1. Check processes: `ps aux | grep "tailscale funnel" | grep -v grep`
2. Test locally: `curl http://localhost:8082/` (or your port)
3. Test externally: `curl https://wakeup.tail3b4b7f.ts.net/`

**Solution**: If you want the funnel to show in status, use background mode: `sudo tailscale funnel --bg 8082`

### Error: "foreground already exists under this port"

**Cause**: Another funnel is already running or stuck

**Fix**:
1. Check status: `sudo tailscale funnel status` (for background funnels)
2. Check processes: `ps aux | grep "tailscale funnel" | grep -v grep` (for all funnels)
3. Stop background funnel: `sudo tailscale funnel --https=443 off`
4. Stop foreground funnel: `Ctrl+C` or `sudo kill <PID>`
5. Start your new funnel

### Funnel Stops When Terminal Closes

**Cause**: You're using foreground mode, which stops when the terminal session ends

**Fix**: Use background mode for persistent funnels:
```bash
sudo tailscale funnel --bg 8082
```

### Funnel Not Accessible

1. Check if the docker container is running:
   ```bash
   docker ps | grep ct2-api
   ```

2. Check if the port is exposed:
   ```bash
   docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep ct2
   ```

3. Test local connectivity:
   ```bash
   curl http://localhost:8082/health
   ```

4. Check tailscale funnel status:
   ```bash
   tailscale funnel status
   ```

## Integration with Docker Compose

Each ct project has a `compose.override.yaml` file that defines its port mappings:

**ct2/compose.override.yaml:**
```yaml
services:
  api:
    ports:
      - "8082:80"
```

**ct4/compose.override.yaml:**
```yaml
services:
  api:
    ports:
      - "8084:80"
```

## Health Check

Run these commands to diagnose issues:

```bash
# 1. Check funnel status
sudo tailscale funnel status

# 2. Check for orphaned processes
ps aux | grep "tailscale funnel" | grep -v grep

# 3. Check if local services are running
docker ps --format 'table {{.Names}}\t{{.Ports}}'

# 4. Test local connectivity
curl http://localhost:8084/health

# 5. Check tailscale connection
tailscale status | grep wakeup
```

## Quick Reference

```bash
# Check background funnel status
sudo tailscale funnel status

# Check ALL funnels (including foreground)
ps aux | grep "tailscale funnel" | grep -v grep

# Start BACKGROUND funnel (RECOMMENDED - persistent, shows in status)
sudo tailscale funnel --bg 8082  # ct2
sudo tailscale funnel --bg 8083  # ct3
sudo tailscale funnel --bg 8084  # ct4

# Start FOREGROUND funnel (NOT RECOMMENDED - stops when terminal closes)
sudo tailscale funnel 8082  # ct2
sudo tailscale funnel 8083  # ct3
sudo tailscale funnel 8084  # ct4

# Stop background funnel (REQUIRED for background mode)
sudo tailscale funnel --https=443 off

# Stop foreground funnel (Ctrl+C or kill process)
# Find PID: ps aux | grep "tailscale funnel" | grep -v grep
sudo kill <PID>
```

## Critical Safety Rules

1. **Only ONE funnel at a time** on port 443 - stop the old one first
2. **Always use clean shutdown** - `sudo tailscale funnel --https=443 off` before starting new
3. **Run in zellij/tmux** - foreground process, needs persistent session
4. **Never kill main daemon** - only kill `tailscale funnel` processes, not `tailscaled` or `tailscaled be-child`
5. **Check before starting** - always run `sudo tailscale funnel status` first

## Process Safety

When viewing processes (`ps aux | grep tailscale`), you'll see:
- **Main daemon**: `/usr/sbin/tailscaled --state=...` (NEVER KILL)
- **SSH children**: `/usr/sbin/tailscaled be-child ssh ...` (NEVER KILL)
- **Funnel processes**: `sudo tailscale funnel --https=443 <port>` (OK to kill if stuck)

Only manage the funnel-specific processes.

## When to Restart Tailscaled

Only as **last resort**:
```bash
sudo systemctl restart tailscaled
```

Most issues are resolved by properly managing funnel processes.

## Notes

- Funnels must be run with `sudo` to bind to port 443 (HTTPS)
- The `--https=443` flag configures the funnel to accept HTTPS traffic on port 443 and route it to the local port
- **Two modes available:**
  - **Foreground** (default): Temporary, doesn't show in status, stops when terminal closes
  - **Background** (`--bg`): Persistent, shows in status, survives terminal disconnects and reboots
- **RECOMMENDATION**: Always use background mode (`--bg`) for persistent funnels
- The public URL follows the pattern: `https://[machine-name].[tailnet].ts.net`
- **"No serve config" is NORMAL for foreground funnels** - use `ps aux` to verify them
