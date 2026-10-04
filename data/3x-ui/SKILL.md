---
name: 3x-ui
description: 3x-ui (MHSanaei/3x-ui) panel administration — a VLESS/Xray web management UI. Install, configure, manage nodes, reset password, and troubleshoot. Installed at /usr/local/x-ui on this VPS.
version: 1.0.0
metadata:
  hermes:
    tags: [xray, vless, proxy, panel, vpn, networking]
---

# 3x-ui Administration

3x-ui is a web panel for managing Xray/VLESS, Shadowsocks, Trojan, and other proxy protocols.

## Quick Status Check

```bash
# Service status
sudo systemctl status x-ui

# Port check
sudo lsof -i :49004

# Binary version
/usr/local/x-ui/x-ui 2>&1 | head -3

# Running process
ps aux | grep x-ui | grep -v grep
```

## Current State (This VPS)

| Item | Value |
|------|-------|
| Version | 2.9.3 |
| Status | ✅ Running (PID 968) |
| Port | 49004 |
| Web Panel | `http://<VPS_IP>:49004` |
| Database | SQLite at `/etc/x-ui/x-ui.db` |
| Backend | xray-linux-amd64 (PID 1382) |

## Access

Open in browser: `http://43.155.135.188:49004`

**Default credentials:** `admin` / `admin`

## Common Operations

```bash
# Restart service
sudo systemctl restart x-ui

# Stop / Start
sudo systemctl stop x-ui
sudo systemctl start x-ui

# View logs
sudo journalctl -u x-ui -n 50 --no-pager

# Reset password
/usr/local/x-ui/x-ui setting -username admin -password admin
```

## Password Reset

If you forgot the admin password:

```bash
/usr/local/x-ui/x-ui setting -username admin -password admin
sudo systemctl restart x-ui
```

## Reinstall (if needed)

```bash
# Stop service
sudo systemctl stop x-ui

# Download installer
bash < <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/main/install.sh)

# Or manual install
cd /usr/local
wget https://github.com/MHSanaei/3x-ui/releases/latest/download/3x-ui-linux-amd64.tar.gz
tar -xzf 3x-ui-linux-amd64.tar.gz
rm 3x-ui-linux-amd64.tar.gz
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Port 49004 not responding | Service down or firewall | Check `systemctl status x-ui`, `sudo ufw allow 49004` |
| Port works locally but nginx proxy to public IP fails | 3x-ui binds only to 127.0.0.1, not 0.0.0.0 | Use `proxy_pass http://127.0.0.1:49004` — see `references/reverse-proxy-8443.md` |
| "400 The plain HTTP request was sent to HTTPS port" | Upstream 49004 is HTTPS, nginx used HTTP | Use `proxy_pass http://127.0.0.1:49004` (nginx terminates SSL, 3x-ui speaks HTTPS locally) |
| "address already in use" | Another process on port | `sudo lsof -i :49004` to find conflicting process |
| Can't login | Wrong password | Reset with `x-ui setting -username admin -password admin` |
| xray backend not running | Config issue | Check `/usr/local/x-ui/bin/config.json`, `journalctl -u x-ui` |
| Permission denied on log file | Log dir missing | `sudo mkdir -p /var/log/x-ui && sudo chown x-ui:x-ui /var/log/x-ui` |

- Nginx 反代理配置（绕过 Cloudflare 端口限制）: `references/reverse-proxy-8443.md`

## Related

- GitHub: https://github.com/MHSanaei/3x-ui
- 3x-ui vs X-UI (original): This is the updated fork by MHSanaei with more features