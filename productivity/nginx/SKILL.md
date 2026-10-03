---
name: nginx
description: "Configure, manage, and troubleshoot nginx web server. Use for: (1) Creating and editing site configurations, (2) Setting up reverse proxies and load balancers, (3) SSL/TLS certificate configuration, (4) Security hardening, (5) Performance optimization, (6) Troubleshooting nginx issues, (7) Managing virtual hosts and server blocks."
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["nginx"]},"install":[{"id":"apt","kind":"apt","package":"nginx","bins":["nginx"],"label":"Install nginx (apt)"},{"id":"yum","kind":"yum","package":"nginx","bins":["nginx"],"label":"Install nginx (yum)"},{"id":"dnf","kind":"dnf","package":"nginx","bins":["nginx"],"label":"Install nginx (dnf)"}]}}
---

# Nginx

## Overview

Nginx is a high-performance web server, reverse proxy, and load balancer. This skill provides workflows for common nginx tasks including site configuration, SSL setup, reverse proxying, and security hardening.

## Quick Commands

### Test Configuration
Always test before reloading:
```bash
nginx -t
```

### Reload Nginx
Apply changes without dropping connections:
```bash
systemctl reload nginx
# or
nginx -s reload
```

### Check Status
```bash
systemctl status nginx
nginx -v
```

## Site Configuration

### Default Paths
- **Main config:** `/etc/nginx/nginx.conf`
- **Sites available:** `/etc/nginx/sites-available/`
- **Sites enabled:** `/etc/nginx/sites-enabled/`
- **HTML root:** `/var/www/html/` or `/usr/share/nginx/html/`

### Create a New Site

1. Create configuration in `sites-available/`:
```bash
nano /etc/nginx/sites-available/example.com
```

2. Basic static site template:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

3. Enable the site:
```bash
ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

## Reverse Proxy

### Basic Reverse Proxy
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### WebSocket Support
```nginx
location /ws {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## SSL/TLS with Let's Encrypt

### Using Certbot
```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Obtain and configure certificate
certbot --nginx -d example.com -d www.example.com

# Auto-renewal test
certbot renew --dry-run
```

### Manual SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # SSL optimization
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
```

## Load Balancing

### Upstream Configuration
```nginx
upstream backend {
    least_conn;  # or ip_hash, least_time
    server 192.168.1.10:3000 weight=5;
    server 192.168.1.11:3000 weight=5;
    server 192.168.1.12:3000 backup;
    keepalive 32;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Load Balancing Methods
- **round_robin** (default): Requests distributed evenly
- **least_conn:** Sends to server with fewest active connections
- **ip_hash:** Client IP determines server (session persistence)
- **least_time:** Sends to server with lowest response time (NGINX Plus)

## Security Hardening

### Hide Nginx Version
```nginx
# In http block of nginx.conf
server_tokens off;
```

### Rate Limiting
```nginx
# In http block
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

# In server/location block
limit_req zone=one burst=5 nodelay;
limit_conn addr 10;
```

### Block Bad User Agents
```nginx
if ($http_user_agent ~* (bot|crawler|spider|scraper)) {
    return 403;
}
```

### Restrict Access
```nginx
location /admin {
    allow 192.168.1.0/24;
    deny all;
    # or
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

## Performance Optimization

### Gzip Compression
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;
```

### Static File Caching
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Buffer Settings
```nginx
client_body_buffer_size 10K;
client_header_buffer_size 1k;
client_max_body_size 8m;
large_client_header_buffers 2 1k;
```

## Troubleshooting

### Check Configuration Syntax
```bash
nginx -t
nginx -T  # Full config dump
```

### View Error Logs
```bash
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Common Issues

**"nginx: [emerg] bind() to 0.0.0.0:80 failed"**
Port 80 already in use:
```bash
ss -tlnp | grep :80
systemctl stop apache2  # If Apache running
```

**Permission Denied on Static Files**
```bash
chmod -R 755 /var/www/site
chown -R www-data:www-data /var/www/site
```

**502 Bad Gateway**
- Check upstream service is running
- Verify firewall allows connection
- Check SELinux/AppArmor policies

## Scripts

Use bundled scripts for common operations:

```bash
# Create new site configuration
scripts/create-site.sh example.com /var/www/example.com

# Enable/disable sites
scripts/site-enable.sh example.com
scripts/site-disable.sh example.com

# Test and reload with backup check
scripts/safe-reload.sh
```

## Resources

- **Full configuration reference:** See [references/nginx-directives.md](references/nginx-directives.md)
- **Common snippets:** See [references/snippets.md](references/snippets.md) for copy-paste templates
