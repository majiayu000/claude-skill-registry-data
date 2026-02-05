---
name: deployment
description: Deploy web applications to Cloudflare Pages/Workers or DigitalOcean VPS. Use when configuring deployment, setting up production environments, or managing releases.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Deployment Skill

Deploy static sites and Node.js applications to Cloudflare and DigitalOcean.

## Deployment Targets

| Target | Best For | Output |
|--------|----------|--------|
| Cloudflare Pages | Static sites, SSG | HTML/CSS/JS files |
| Cloudflare Workers | Edge functions, SSR | JavaScript workers |
| DigitalOcean App Platform | Managed containers | Docker/Buildpacks |
| DigitalOcean Droplet | Full control VPS | Any stack |

## Cloudflare Pages (Static Sites)

### Project Structure

```
project/
├── dist/                 # Build output (or _site, build, etc.)
├── public/               # Static assets (copied as-is)
├── _redirects            # Redirect rules
├── _headers              # Custom headers
└── wrangler.toml         # Optional: Wrangler config
```

### Deployment Methods

**Git Integration (Recommended):**
1. Connect repository in Cloudflare dashboard
2. Configure build settings:
   - Build command: `npm run build`
   - Output directory: `dist`
3. Automatic deploys on push

**Wrangler CLI:**
```bash
# Install Wrangler
npm install -D wrangler

# Login
npx wrangler login

# Deploy
npx wrangler pages deploy dist --project-name=my-project
```

### Redirects (_redirects)

```
# Simple redirect
/old-page /new-page 301

# Wildcard redirect
/blog/* /articles/:splat 301

# Proxy (hide origin)
/api/* https://api.example.com/:splat 200

# Country-based redirect
/ /en 302 Country=us,ca,uk
/ /es 302 Country=mx,es
```

### Headers (_headers)

```
# All pages
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# Cache static assets
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# Security headers for HTML
/*.html
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
```

### Environment Variables

Set in Cloudflare dashboard or wrangler.toml:

```toml
# wrangler.toml
name = "my-project"
compatibility_date = "2024-01-01"

[vars]
API_URL = "https://api.example.com"

# Secrets (set via CLI, not in file)
# npx wrangler secret put API_KEY
```

Access in Workers/Functions:
```javascript
export default {
  async fetch(request, env) {
    const apiUrl = env.API_URL;
    const apiKey = env.API_KEY; // From secrets
  }
}
```

## Cloudflare Workers (SSR/Edge)

### Astro with Cloudflare Adapter

```javascript
// astro.config.mjs
import cloudflare from '@astrojs/cloudflare';

export default {
  output: 'server',
  adapter: cloudflare({
    mode: 'directory', // or 'advanced'
  }),
};
```

```toml
# wrangler.toml
name = "my-astro-site"
compatibility_date = "2024-01-01"
pages_build_output_dir = "dist"
```

### Deploy Worker

```bash
npx wrangler deploy
```

## DigitalOcean App Platform

### App Specification (.do/app.yaml)

**Static Site:**
```yaml
name: my-static-site
region: nyc
static_sites:
  - name: web
    source_dir: /
    github:
      repo: username/repo
      branch: main
    build_command: npm run build
    output_dir: dist
    routes:
      - path: /
    environment_slug: node-js
    envs:
      - key: NODE_ENV
        value: production
```

**Node.js Service:**
```yaml
name: my-node-app
region: nyc
services:
  - name: api
    source_dir: /
    github:
      repo: username/repo
      branch: main
    build_command: npm ci && npm run build
    run_command: node dist/server.js
    http_port: 3000
    instance_size_slug: basic-xxs
    instance_count: 1
    routes:
      - path: /api
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        type: SECRET
      - key: NODE_ENV
        value: production
```

### Deploy via CLI

```bash
# Install doctl
brew install doctl

# Authenticate
doctl auth init

# Create app from spec
doctl apps create --spec .do/app.yaml

# Update existing app
doctl apps update <app-id> --spec .do/app.yaml
```

## DigitalOcean Droplet (VPS)

### Initial Server Setup

```bash
# SSH into droplet
ssh root@your-droplet-ip

# Create non-root user
adduser deploy
usermod -aG sudo deploy

# Setup SSH key for deploy user
mkdir -p /home/deploy/.ssh
cp ~/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install Nginx
sudo apt-get install -y nginx
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/my-app
server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Static files
    location /assets/ {
        alias /var/www/my-app/dist/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Node.js app
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

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/my-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

### PM2 Process Management

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: 'dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    env_file: '.env.production'
  }]
};
```

```bash
# Start application
pm2 start ecosystem.config.js

# Save process list
pm2 save

# Setup startup script
pm2 startup

# View logs
pm2 logs my-app

# Monitor
pm2 monit
```

### Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

APP_DIR=/var/www/my-app
REPO_URL=git@github.com:username/repo.git

# Pull latest code
cd $APP_DIR
git pull origin main

# Install dependencies
npm ci --only=production

# Build
npm run build

# Restart application
pm2 reload ecosystem.config.js

echo "Deployment complete!"
```

## Zero-Downtime Deployment

### Rolling Restart (PM2)

```bash
# Graceful reload (zero-downtime)
pm2 reload my-app

# Hard restart (brief downtime)
pm2 restart my-app
```

### Health Check Endpoint

```javascript
// src/api/health.js
export function healthCheck(req, res) {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
}
```

## Rollback Procedures

### Git-based Rollback

```bash
# List recent deployments
git log --oneline -10

# Rollback to specific commit
git checkout <commit-hash>
npm ci
npm run build
pm2 reload my-app

# Or revert and push
git revert HEAD
git push origin main
```

### Cloudflare Rollback

```bash
# List deployments
npx wrangler pages deployment list --project-name=my-project

# Rollback to previous deployment (via dashboard)
# Or redeploy previous commit
git checkout <commit-hash>
npx wrangler pages deploy dist
```

## Checklist

Before deploying:

- [ ] Environment variables configured (not in code)
- [ ] Build succeeds locally
- [ ] SSL certificate configured
- [ ] Security headers in place
- [ ] Health check endpoint works
- [ ] Rollback procedure documented
- [ ] Monitoring/logging configured

## Related Skills

- **env-config** - Environment variable management
- **ci-cd** - Automated deployment pipelines
- **security** - Production security headers
- **performance** - Caching and optimization
- **astro** / **eleventy** - SSG deployment specifics
