---
name: vps-setup
description: Set up a fresh Ubuntu VPS for web development with Node.js, Python, Nginx, PM2, SSL, and security hardening. Use when setting up a new server, configuring web hosting, deploying apps, or helping users create a development playground server.
---

# VPS Setup Skill

This skill helps set up a fresh Ubuntu VPS as a secure web development playground. It includes automated scripts and step-by-step guides for installing Node.js, Python, Nginx, PM2, Docker, SSL certificates, and security tools.

## When to Use This Skill

- Setting up a fresh VPS or cloud server
- Configuring a development/staging environment
- Helping users deploy their first web application
- Setting up reverse proxy with Nginx
- Configuring SSL certificates with Let's Encrypt
- Hardening server security

## Quick Start

For a complete automated setup, use the setup script:

```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/your-repo/vps-setup.sh | bash
```

Or guide users through the manual process using the reference documentation.

## Architecture Overview

```
Internet → UFW Firewall → Nginx (80/443) → PM2 Apps (3000+)
                        ↘ Direct port access (3000-3010)
```

## Core Components

| Component | Purpose | Default Config |
|-----------|---------|----------------|
| Node.js 20 LTS | JavaScript runtime | Via NodeSource |
| Python 3 | Python runtime | System default |
| PM2 | Process manager | Auto-restart, logging |
| Nginx | Reverse proxy | SSL termination |
| Certbot | SSL certificates | Let's Encrypt |
| UFW | Firewall | Ports 22,80,443,3000-3010 |
| fail2ban | Brute-force protection | SSH jail enabled |
| Docker | Containers | Optional, available |

## Default Port Assignments

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP (redirects to 443) |
| 443 | HTTPS |
| 3000-3010 | Development apps |
| 5000 | Internal API |

## Instructions for Claude

When helping a user set up a VPS:

### 1. Assess the Starting Point
```bash
# Check OS version
cat /etc/os-release

# Check what's already installed
which node npm python3 nginx docker pm2

# Check disk space and memory
df -h && free -h
```

### 2. Run Core Installation
Either use the automated script or guide through manual steps:
- Update system packages
- Install Node.js via NodeSource
- Install PM2 globally
- Install and configure Nginx
- Set up UFW firewall
- Install and configure fail2ban
- Install Certbot for SSL

### 3. Create Project Structure
```bash
mkdir -p /home/projects
cd /home/projects
```

### 4. Deploy First Test App
```bash
# Create hello-world test
mkdir hello-world && cd hello-world
npm init -y
# Create simple Express server
pm2 start server.js --name hello-world
```

### 5. Configure Nginx Reverse Proxy
- Create site config in /etc/nginx/sites-available/
- Enable with symlink to sites-enabled/
- Test and reload nginx

### 6. Set Up SSL (if domain available)
```bash
certbot --nginx -d yourdomain.com
```

### 7. Create Documentation
Generate CLAUDE.md, README.md, and QUICKSTART.md in /home/projects/

## Key Commands Reference

### PM2 Management
```bash
pm2 list                    # View all apps
pm2 logs [app]             # View logs
pm2 restart [app]          # Restart app
pm2 stop [app]             # Stop app
pm2 delete [app]           # Remove app
pm2 save                   # Save current apps
pm2 startup                # Enable auto-start on boot
```

### Nginx Management
```bash
nginx -t                   # Test config
systemctl reload nginx     # Apply changes
systemctl status nginx     # Check status
```

### Firewall Management
```bash
ufw status                 # View rules
ufw allow [port]/tcp       # Open port
ufw delete allow [port]    # Close port
```

### SSL Certificate Management
```bash
certbot certificates       # List certs
certbot renew --dry-run   # Test renewal
certbot --nginx -d domain  # Add new cert
```

## Security Checklist

- [ ] UFW firewall enabled with minimal ports
- [ ] fail2ban protecting SSH
- [ ] SSH key authentication (recommended)
- [ ] Regular system updates configured
- [ ] SSL certificates installed
- [ ] Non-root user for daily use (optional)

## Troubleshooting

### App not accessible
1. Check if running: `pm2 list`
2. Check logs: `pm2 logs [app]`
3. Check port: `lsof -i :[port]`
4. Check firewall: `ufw status`

### SSL certificate issues
1. Check cert status: `certbot certificates`
2. Test renewal: `certbot renew --dry-run`
3. Check nginx config: `nginx -t`

### Out of memory
1. Check usage: `free -h`
2. Check processes: `htop` or `top`
3. Consider adding swap space

## Files in This Skill

- `scripts/setup.sh` - Automated installation script
- `scripts/add-site.sh` - Add new site helper
- `templates/nginx-site.conf` - Nginx site template
- `templates/CLAUDE.md` - AI assistant guide template
- `templates/README.md` - Project README template
- `reference.md` - Detailed step-by-step guide
