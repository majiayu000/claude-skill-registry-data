---
name: julien-infra-hostinger-web
description: Web infrastructure for Hostinger VPS - Nginx reverse proxy, SSL/Let's Encrypt, configuration audit, and application deployment (INCLUZ'HACT). Use for site configuration, SSL setup, 502/504 errors, or deployments.
license: Apache-2.0
triggers:
  - nginx
  - reverse proxy
  - ssl certificate
  - certbot
  - deploy hostinger
  - deploy incluzact
  - 502 error
  - 504 error
---

# Hostinger Web Infrastructure

Nginx, SSL, and deployment management for srv759970.hstgr.cloud.

## Server Info

| Property | Value |
|----------|-------|
| **Host** | automation@69.62.108.82 |
| **Nginx config** | /etc/nginx/sites-available/ |
| **Sites enabled** | /etc/nginx/sites-enabled/ |
| **Logs** | /var/log/nginx/ |

---

## 1. Nginx Management

### Add New Site

```bash
ssh srv759970
sudo nano /etc/nginx/sites-available/mysite
```

Template (CRITICAL: include IPv6):
```nginx
server {
    listen 80;
    listen [::]:80;  # IPv6 REQUIRED
    server_name mysite.srv759970.hstgr.cloud;

    location / {
        proxy_pass http://localhost:PORT;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo nginx -t
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
sudo certbot --nginx -d mysite.srv759970.hstgr.cloud
sudo certbot certificates  # Check status
sudo certbot renew --dry-run  # Test renewal
```

### Common Commands

```bash
sudo nginx -t                  # Test config
sudo systemctl reload nginx    # Reload (preferred)
sudo tail -f /var/log/nginx/error.log  # View errors
ls /etc/nginx/sites-enabled/   # List sites
```

---

## 2. Troubleshooting

### 502 Bad Gateway

```bash
# Check backend
docker ps | grep service-name
curl localhost:PORT
docker restart container-name
docker logs container-name --tail 50
```

### 504 Gateway Timeout

Add to nginx config:
```nginx
proxy_read_timeout 300;
proxy_connect_timeout 300;
```

### SSL Certificate Mismatch (IPv6 issue)

**Cause**: Missing IPv6 listeners

**Fix**:
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;  # ADD THIS
    # ...
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -6 https://mysite.srv759970.hstgr.cloud  # Test IPv6
```

---

## 3. Nginx Audit

### Check All Sites for IPv6

```bash
ssh srv759970 << 'EOF'
for site in /etc/nginx/sites-enabled/*; do
    if ! grep -q "listen \[::\]:443" "$site" 2>/dev/null; then
        echo "MISSING IPv6: $(basename $site)"
    fi
done
EOF
```

### Quick Security Check

```bash
curl -sI https://site.srv759970.hstgr.cloud | grep -iE "x-frame|x-content|strict-transport"
```

---

## 4. INCLUZ'HACT Deployment

### Environments

| Env | Branch | URL | Port | PM2 |
|-----|--------|-----|------|-----|
| Production | main | https://incluzhact.fr | 5173 | incluzhact |
| Preview | staging | https://preview.incluzhact.fr | 5174 | incluzhact-preview |

### Quick Deploy

```bash
ssh automation@69.62.108.82 << 'EOF'
cd /var/www/incluzhact
git checkout staging  # or main
git pull origin staging
npm install
npm run build
pm2 reload incluzhact-preview  # or incluzhact
EOF
```

### Verify Deployment

```bash
pm2 status incluzhact
curl -I https://incluzhact.fr
pm2 logs incluzhact --lines 50
```

### Rollback

```bash
ssh srv759970 << 'EOF'
cd /var/www/incluzhact
git reset --hard HEAD^
npm run build
pm2 restart incluzhact
EOF
```

---

## 5. Nginx Templates

### Basic Reverse Proxy

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name app.srv759970.hstgr.cloud;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### WordPress

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name wp.srv759970.hstgr.cloud;
    client_max_body_size 100M;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Quick Reference

```bash
# Test nginx
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# SSL certificate
sudo certbot --nginx -d domain.com

# Check SSL
sudo certbot certificates

# Deploy INCLUZ'HACT
ssh srv759970 'cd /var/www/incluzhact && git pull && npm install && npm run build && pm2 reload incluzhact'

# Check IPv6
sudo nginx -T | grep -E "listen.*\[::\]"
```
