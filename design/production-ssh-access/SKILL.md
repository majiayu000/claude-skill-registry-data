---
name: Production SSH Access
description: Provides guidance and utilities for securely accessing the Codante Frontend production server via SSH. Use this when you need to connect to the production server, run commands, check logs, manage pm2 processes, troubleshoot issues, or verify deployments.
---

# Production SSH Access Skill

## Overview

This skill guides you through accessing and working with the Codante Frontend production server hosted on Digital Ocean.

## Server Information

- **Host**: 216.238.103.47
- **User**: robertotcestari
- **OS**: Linux (Ubuntu/Debian)
- **Web Server**: nginx
- **Application Server**: pm2 (Node.js process manager) - `codante-io-front` process
- **Runtime**: Node.js >= 20
- **Application Root**: `/var/www/codante-io-front`
- **Deployment Method**: rsync (direct, no release directories)

## Quick Access

### Connect to Production Server

```bash
ssh robertotcestari@216.238.103.47
```

### Common SSH Commands

**Check pm2 status:**

```bash
ssh robertotcestari@216.238.103.47 "pm2 status"
```

**Check nginx configuration:**

```bash
ssh robertotcestari@216.238.103.47 "sudo nginx -t"
```

**List nginx sites:**

```bash
ssh robertotcestari@216.238.103.47 "ls /etc/nginx/sites-enabled/"
```

**Check service status:**

```bash
ssh robertotcestari@216.238.103.47 "systemctl status nginx"
```

## File Transfer

WARNING: do not transfer files - this is used only for emergency debugging. To change files in the production server, use the deployment pipeline.

### Copy files from production to local:

```bash
scp robertotcestari@216.238.103.47:/path/on/server /local/path
```

### Copy files from local to production:

```bash
scp /local/path robertotcestari@216.238.103.47:/path/on/server
```

## Production Application Paths

- **Application Root**: `/var/www/codante-io-front`
- **Source Code**: `/var/www/codante-io-front/` (direct rsync, no releases/)
- **Build Output**: `/var/www/codante-io-front/dist/` (production build)
- **Node Modules**: `/var/www/codante-io-front/node_modules/`
- **pm2 Config**: `/var/www/codante-io-front/pm2.config.js` or ecosystem.config.js
- **Public**: `/var/www/codante-io-front/dist` (served by nginx)
- **.env Config**: `/var/www/codante-io-front/.env` (if used)

## Log Access in Production

### pm2 Logs

**View pm2 process logs (live):**

```bash
# Follow codante-io-front logs in real-time
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front"

# View last 100 lines
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front --lines 100"
```

**View pm2 error logs specifically:**

```bash
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front --err"
```

**View pm2 output logs specifically:**

```bash
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front --out"
```

**Get pm2 process details:**

```bash
ssh robertotcestari@216.238.103.47 "pm2 info codante-io-front"
```

### nginx Logs

**nginx access logs:**

```bash
# Real-time access logs
ssh robertotcestari@216.238.103.47 "tail -f /var/log/nginx/access.log"

# Site-specific access logs (if configured)
ssh robertotcestari@216.238.103.47 "tail -f /var/log/nginx/codante-io-front-access.log"
```

**nginx error logs:**

```bash
# Real-time error logs
ssh robertotcestari@216.238.103.47 "tail -f /var/log/nginx/error.log"

# Site-specific error logs
ssh robertotcestari@216.238.103.47 "tail -f /var/log/nginx/codante-io-front-error.log"
```

### System Logs - nginx/pm2 Services

**nginx service logs:**

```bash
ssh robertotcestari@216.238.103.47 "journalctl -u nginx -n 100 -f"
```

**pm2 service logs (if using systemd):**

```bash
# If pm2 is managed by systemd
ssh robertotcestari@216.238.103.47 "journalctl -u pm2-robertotcestari -n 100 -f"
```

### View All Logs in Directory

```bash
# List log files with sizes
ssh robertotcestari@216.238.103.47 "ls -lh /var/log/nginx/"

# Check application logs if using custom logging
ssh robertotcestari@216.238.103.47 "ls -lh /var/www/codante-io-front/logs/ 2>/dev/null || echo 'No custom logs directory'"
```

### Search and Filter Logs

**Find errors in nginx logs:**

```bash
ssh robertotcestari@216.238.103.47 "grep 'error\|ERROR\|502\|503' /var/log/nginx/error.log | head -50"
```

**Find 502/503 errors:**

```bash
ssh robertotcestari@216.238.103.47 "grep '502\|503' /var/log/nginx/access.log | tail -20"
```

**Find 4xx errors:**

```bash
ssh robertotcestari@216.238.103.47 "grep '4[0-9][0-9]' /var/log/nginx/access.log | tail -20"
```

**Monitor logs with filter:**

```bash
ssh robertotcestari@216.238.103.47 "tail -f /var/log/nginx/error.log | grep -E 'error|502|503|upstream'"
```

### Download Logs Locally

**Copy nginx access log:**

```bash
scp robertotcestari@216.238.103.47:/var/log/nginx/access.log ./nginx-access-backup.log
```

**Copy all nginx logs:**

```bash
scp -r robertotcestari@216.238.103.47:/var/log/nginx/ ./nginx-logs/
```

**Copy pm2 logs:**

```bash
# pm2 logs are stored in ~/.pm2/logs/
scp -r robertotcestari@216.238.103.47:~/.pm2/logs/ ./pm2-logs/
```

## pm2 Management

Codante Frontend uses **pm2** (Node.js process manager) running the `codante-io-front` process.

### Check pm2 Status

```bash
# View all processes
ssh robertotcestari@216.238.103.47 "pm2 status"

# Get detailed process info
ssh robertotcestari@216.238.103.47 "pm2 info codante-io-front"

# View process list with resource usage
ssh robertotcestari@216.238.103.47 "pm2 monit"
```

### View pm2 Logs

```bash
# Follow logs in real-time
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front"

# View last N lines
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front --lines 200"

# View error logs only
ssh robertotcestari@216.238.103.47 "pm2 logs codante-io-front --err"
```

### Restart pm2 Process

```bash
# Restart the codante-io-front process
ssh robertotcestari@216.238.103.47 "pm2 restart codante-io-front"

# Reload (graceful restart - used for 0-downtime reloads)
ssh robertotcestari@216.238.103.47 "pm2 reload codante-io-front"

# Stop process
ssh robertotcestari@216.238.103.47 "pm2 stop codante-io-front"

# Start process
ssh robertotcestari@216.238.103.47 "pm2 start codante-io-front"
```

### Monitor pm2 Process

```bash
# Monitor memory usage
ssh robertotcestari@216.238.103.47 "pm2 monit codante-io-front"

# Get process details including memory
ssh robertotcestari@216.238.103.47 "pm2 info codante-io-front"

# View real-time metrics
ssh robertotcestari@216.238.103.47 "watch 'pm2 status'"
```

### View pm2 Config

```bash
# View ecosystem config if exists
ssh robertotcestari@216.238.103.47 "cat /var/www/codante-io-front/ecosystem.config.js 2>/dev/null || cat /var/www/codante-io-front/pm2.config.js 2>/dev/null || echo 'No pm2 config found'"
```

## Common Production Tasks

### Check Disk Space

```bash
ssh robertotcestari@216.238.103.47 "df -h"
```

### Monitor CPU/Memory

```bash
ssh robertotcestari@216.238.103.47 "top -b -n 1 | head -20"

# Check specific process
ssh robertotcestari@216.238.103.47 "ps aux | grep 'node\|pm2'"
```

### Restart Services

```bash
# Restart pm2 process
ssh robertotcestari@216.238.103.47 "pm2 restart codante-io-front"

# Restart nginx
ssh robertotcestari@216.238.103.47 "sudo systemctl restart nginx"

# Restart both
ssh robertotcestari@216.238.103.47 "pm2 restart codante-io-front && sudo systemctl restart nginx"
```

### Check Current Deployment

```bash
# Check if app directory exists
ssh robertotcestari@216.238.103.47 "ls -la /var/www/codante-io-front/"

# Check git info
ssh robertotcestari@216.238.103.47 "cd /var/www/codante-io-front && git log -5 --oneline 2>/dev/null || echo 'Not a git repo'"

# Check if dist build exists
ssh robertotcestari@216.238.103.47 "ls -la /var/www/codante-io-front/dist/ | head -10"

# Check Node.js version
ssh robertotcestari@216.238.103.47 "node --version"
```

### Deploy New Release

When deploying via GitHub Actions + rsync:

1. Push to `main` branch
2. GitHub Actions triggers automated deployment
3. GitHub Actions handles:
   - npm install
   - Build production (npm run build)
   - rsync to server at `/var/www/codante-io-front`
   - pm2 restart (post-deploy)

Check deployment status:

```bash
ssh robertotcestari@216.238.103.47 "ls -lah /var/www/codante-io-front/ | head -20"
```

### Verify Application is Running

```bash
# Check if pm2 process is running
ssh robertotcestari@216.238.103.47 "pm2 status | grep codante-io-front"

# Check if nginx is serving requests
ssh robertotcestari@216.238.103.47 "curl -I http://localhost:3000"

# Check nginx proxy to port 3000
ssh robertotcestari@216.238.103.47 "sudo netstat -tlnp | grep -E '3000|80|443'"
```

### Clear Build Cache (if needed)

```bash
# Remove node_modules and dist
ssh robertotcestari@216.238.103.47 "cd /var/www/codante-io-front && rm -rf node_modules dist"

# Full rebuild on next deployment
ssh robertotcestari@216.238.103.47 "cd /var/www/codante-io-front && npm install && npm run build"
```

## Security Considerations

1. **SSH Keys**: Ensure your SSH key is added to `~/.ssh/authorized_keys` on the server
2. **sudo Access**: Use `sudo` for privileged commands (requires password or sudo setup)
3. **Environment Variables**: Never expose sensitive data in logs or console output
4. **Log Files**: Check logs for errors, security warnings, and performance issues
5. **Backups**: Always ensure backups exist before making changes to production
6. **Process State**: pm2 maintains process state; changes to app code require rebuild and restart
7. **nginx Proxy**: Verify nginx configuration before restarting to avoid service disruption
8. **Deployment**: Use automated GitHub Actions pipeline instead of manual rsync when possible

## Troubleshooting

### Connection Issues

If you can't connect:

1. Verify SSH key is configured: `ssh-keyscan 216.238.103.47`
2. Check your SSH config: `~/.ssh/config`
3. Test connectivity: `ping 216.238.103.47`

### Permission Denied

If you get "Permission denied":

1. Verify the username is `robertotcestari`
2. Check SSH key permissions: `chmod 600 ~/.ssh/id_rsa`
3. Ensure public key is on server: `cat ~/.ssh/id_rsa.pub`

### pm2 Process Not Running

If pm2 process is stopped:

1. Check status: `pm2 status`
2. View recent logs: `pm2 logs codante-io-front --lines 50`
3. Restart process: `pm2 restart codante-io-front`
4. Verify app directory exists: `ls /var/www/codante-io-front/`

### Build Not Found

If `npm run build` output doesn't exist:

1. Check if dist/ folder exists: `ls /var/www/codante-io-front/dist/`
2. Check package.json build script: `cat /var/www/codante-io-front/package.json | grep -A 5 '"build"'`
3. Manually trigger build: `cd /var/www/codante-io-front && npm install && npm run build`

### nginx 502 Bad Gateway

If you see 502 errors in nginx:

1. Check if pm2 process is running: `pm2 status`
2. Check if Node app is listening on port 3000: `curl http://127.0.0.1:3000`
3. Check nginx error log: `tail -f /var/log/nginx/error.log`
4. Restart pm2: `pm2 restart codante-io-front`
5. Restart nginx: `sudo systemctl restart nginx`

### High Memory Usage

If Node process is consuming too much memory:

1. Check memory: `ps aux | grep node`
2. View pm2 memory usage: `pm2 info codante-io-front`
3. Check logs for memory leaks: `pm2 logs codante-io-front`
4. Restart process: `pm2 restart codante-io-front`
5. Monitor memory: `pm2 monit`

### Slow Response Times

If application is slow:

1. Check nginx access logs: `tail -f /var/log/nginx/access.log | grep "HTTP/\|response"`
2. Check backend API availability: `curl -I http://127.0.0.1:8000`
3. Check CPU usage: `top -p $(pgrep -f 'node')`
4. Monitor pm2: `pm2 monit`
5. Check disk I/O: `iostat -x 1`

### Application Won't Start After Deployment

If app fails to start:

1. Check deployment logs: `pm2 logs codante-io-front`
2. Check if dependencies installed: `ls /var/www/codante-io-front/node_modules/`
3. Check for build errors: `cd /var/www/codante-io-front && npm run build`
4. Verify .env file exists: `test -f /var/www/codante-io-front/.env && echo 'exists' || echo 'missing'`
5. Check if API backend is reachable: `curl http://127.0.0.1:8000/health`

## When to Use This Skill

Use this skill when you need to:

- ✅ Connect to the production server
- ✅ Debug production issues
- ✅ Access and analyze production logs (pm2, nginx)
- ✅ Monitor real-time log streams
- ✅ Check server logs and metrics
- ✅ Manage pm2 processes
- ✅ Verify deployments
- ✅ Transfer files to/from production
- ✅ Run ad-hoc commands on production
- ✅ Troubleshoot deployment issues
- ✅ Monitor performance and resource usage
- ✅ Check backend API availability
- ✅ Verify nginx proxy configuration

## Related Resources

- CLAUDE.md deployment section for CI/CD information
- Server management documentation
- GitHub Actions workflow (`.github/workflows/deploy.yml`)
- pm2 documentation: https://pm2.keymetrics.io/docs/usage/quick-start/
- React Router documentation: https://reactrouter.com/
