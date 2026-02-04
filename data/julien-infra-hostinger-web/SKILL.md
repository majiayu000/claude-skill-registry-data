---
name: julien-infra-hostinger-web
description: Web infrastructure for Hostinger VPS - Nginx, SSL/Let's Encrypt, static site deployment (Slidev/Astro/Vite), reverse proxy, and 502/504 troubleshooting.
license: Apache-2.0
triggers:
  # Core
  - nginx
  - reverse proxy
  - ssl certificate
  - certbot
  - 502 error
  - 504 error
  # Hostinger deploy
  - deploy hostinger
  - deploy incluzact
  - deploy sur le vps
  - deployer sur hostinger
  - mettre en ligne hostinger
  - upload hostinger
  # Static site deploy
  - deploy static site
  - deploy slidev
  - deploy astro
  - deploy vite
  - site statique
  - déployer site statique
  - héberger site
  - mettre en ligne slides
  - servir fichiers statiques
  - nginx static files
  # IPv6 / SSL issues
  - ipv6 nginx
  - certbot unauthorized
  - certbot 401
  - ssl ipv6
---

# Hostinger Web Infrastructure

Nginx, SSL, and deployment management for srv759970.hstgr.cloud.

## Server Info

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-infra-hostinger-web" activated
```

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

## 6. Static Site Deployment (Slidev, Astro, Vite, etc.)

### Workflow Complet

```bash
# 1. Build localement
cd /path/to/project
npm run build  # ou pnpm build

# 2. Créer le dossier sur le serveur
ssh srv759970 "sudo mkdir -p /opt/PROJET_NAME && sudo chown automation:automation /opt/PROJET_NAME"

# 3. Uploader les fichiers
scp -r dist/* srv759970:/opt/PROJET_NAME/

# 4. Créer la config Nginx
ssh srv759970 "sudo tee /etc/nginx/sites-available/PROJET_NAME << 'EOF'
server {
    listen 80;
    listen [::]:80;  # IPv6 REQUIS pour certbot!
    server_name PROJET_NAME.srv759970.hstgr.cloud;
    root /opt/PROJET_NAME;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Cache pour assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control \"public, immutable\";
    }
}
EOF"

# 5. Activer le site
ssh srv759970 "sudo ln -sf /etc/nginx/sites-available/PROJET_NAME /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx"

# 6. Obtenir SSL
ssh srv759970 "sudo certbot --nginx -d PROJET_NAME.srv759970.hstgr.cloud --non-interactive --agree-tos --email julien@geneste.dev"
```

### One-Liners par Framework

**Slidev**:
```bash
npm run build && scp -r dist/* srv759970:/opt/slides/
```

**Astro**:
```bash
npm run build && scp -r dist/* srv759970:/opt/astro-site/
```

**Vite/React/Vue**:
```bash
npm run build && scp -r dist/* srv759970:/opt/app-name/
```

### Template Nginx pour Site Statique

```nginx
server {
    listen 80;
    listen [::]:80;  # CRITIQUE: IPv6 requis pour certbot
    server_name PROJET.srv759970.hstgr.cloud;
    root /opt/PROJET;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;  # SPA fallback
    }

    # Compression gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Cache assets statiques
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Dépannage Certbot

**Erreur "unauthorized" / 401**:
```bash
# Vérifier que IPv6 retourne 200 (pas 301 redirect)
ssh srv759970 "curl -6 -I http://PROJET.srv759970.hstgr.cloud"

# Si 301 → Ajouter listen [::]:80 à la config
ssh srv759970 "sudo sed -i 's/listen 80;/listen 80;\n    listen [::]:80;/' /etc/nginx/sites-available/PROJET"
ssh srv759970 "sudo nginx -t && sudo systemctl reload nginx"

# Relancer certbot
ssh srv759970 "sudo certbot --nginx -d PROJET.srv759970.hstgr.cloud"
```

**Vérification DNS**:
```bash
# Le wildcard DNS *.srv759970.hstgr.cloud existe
dig +short monsite.srv759970.hstgr.cloud  # Doit retourner 69.62.108.82
```

### Script Automatisé

```bash
# deploy-static.sh <nom-projet> <dossier-local>
PROJECT_NAME=$1
LOCAL_DIR=${2:-dist}

# Upload
scp -r "$LOCAL_DIR"/* srv759970:/opt/"$PROJECT_NAME"/

# Config + SSL si nouveau site
ssh srv759970 "[ ! -f /etc/nginx/sites-available/$PROJECT_NAME ] && {
    sudo tee /etc/nginx/sites-available/$PROJECT_NAME << EOF
server {
    listen 80;
    listen [::]:80;
    server_name $PROJECT_NAME.srv759970.hstgr.cloud;
    root /opt/$PROJECT_NAME;
    index index.html;
    location / { try_files \\\$uri \\\$uri/ /index.html; }
}
EOF
    sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx
    sudo certbot --nginx -d $PROJECT_NAME.srv759970.hstgr.cloud --non-interactive --agree-tos --email julien@geneste.dev
}"

echo "✅ Déployé: https://$PROJECT_NAME.srv759970.hstgr.cloud"
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
