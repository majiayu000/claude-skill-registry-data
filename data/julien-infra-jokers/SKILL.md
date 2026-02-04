---
name: julien-infra-jokers
description: Complete management for Jokers Hockey website - deployment, build checks, database migrations (Drizzle ORM), and PM2 process management. Use for any Jokers site operation.
license: Apache-2.0
triggers:
  - deploy jokers
  - jokers hockey
  - push to production
  - check jokers logs
  - restart jokers
  - jokers database
  - jokers build
  - jokers pm2
---

# Jokers Hockey - Infrastructure Management

Complete infrastructure management for the Jokers Hockey website.

## Quick Reference

| Component | Details |
|-----------|---------|
| **Server** | srv759970.hstgr.cloud (69.62.108.82) |
| **User** | automation |
| **Path** | /var/www/jokers |
| **PM2 Process** | jokers-hockey |
| **Port** | 5020 |
| **URL** | https://jokers.srv759970.hstgr.cloud |
| **Database** | PostgreSQL (localhost:5432/jokers_prod) |
| **ORM** | Drizzle |

---

## 1. Deployment

### Quick Deploy (Git)

```bash
ssh automation@69.62.108.82
cd /var/www/jokers
git pull origin main
npm install
npm run db:push
npm run build
pm2 restart jokers-hockey
```

### Pre-Deployment Checks

```bash
# Local: verify build works
npm run check
npm run build
ls -la dist/
```

### Verify Deployment

```bash
pm2 status jokers-hockey
pm2 logs jokers-hockey --lines 50
curl -I https://jokers.srv759970.hstgr.cloud
```

### Rollback

```bash
git log --oneline -5
git checkout <previous-commit>
npm install && npm run build
pm2 restart jokers-hockey
```

---

## 2. Build Verification

### Full Build Check

```bash
# TypeScript compilation
npm run check

# Clean build
rm -rf dist/ && npm run build

# Verify output
ls -la dist/
ls -la dist/public/assets/
```

### Expected Structure

```
dist/
├── index.js        (server ~5KB)
└── public/
    ├── index.html
    └── assets/
        ├── index-[hash].css  (~70KB)
        └── index-[hash].js   (~350KB)
```

### Quality Checks

```bash
# No debug code
grep -r "console.log\|debugger" client/src/ || echo "Clean"

# Security audit
npm audit --production

# Bundle sizes (should be < 500KB JS, < 100KB CSS)
du -sh dist/public/assets/*.js
du -sh dist/public/assets/*.css
```

---

## 3. Database (Drizzle ORM)

### Schema Location

- **Schema**: `shared/schema.ts`
- **Config**: `drizzle.config.ts`

### Push Schema Changes

```bash
# Development (direct apply)
npm run db:push

# Production
ssh automation@69.62.108.82
cd /var/www/jokers
git pull origin main
npm run db:push
pm2 restart jokers-hockey
```

### Schema Example

```typescript
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const news = pgTable("news", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content").notNull(),
  publishedAt: timestamp("published_at").defaultNow(),
});
```

### Backup Before Changes

```bash
docker exec postgresql-shared pg_dump -U postgres jokers_prod > backup_$(date +%Y%m%d).sql
```

### Verify Database

```bash
ssh automation@69.62.108.82
docker exec -it postgresql-shared psql -U postgres -d jokers_prod
\dt  # list tables
\d table_name  # describe table
\q
```

---

## 4. PM2 Management

### Status & Monitoring

```bash
ssh automation@69.62.108.82
pm2 status jokers-hockey
pm2 show jokers-hockey
pm2 monit  # live dashboard
```

### Logs

```bash
pm2 logs jokers-hockey --lines 100
pm2 logs jokers-hockey --err  # errors only
pm2 flush jokers-hockey  # clear logs
```

### Process Control

```bash
pm2 restart jokers-hockey
pm2 stop jokers-hockey
pm2 start jokers-hockey
pm2 reload jokers-hockey  # zero-downtime
```

### PM2 Config

File: `/var/www/jokers/ecosystem.config.cjs`

```javascript
module.exports = {
  apps: [{
    name: 'jokers-hockey',
    script: './dist/index.js',
    instances: 1,
    env: { NODE_ENV: 'production', PORT: 5020 },
    max_memory_restart: '500M',
  }]
}
```

### Save Configuration

```bash
pm2 save  # after any changes
```

---

## 5. Troubleshooting

### Site Down

```bash
pm2 status jokers-hockey
pm2 logs jokers-hockey --lines 100
pm2 restart jokers-hockey
curl -I https://jokers.srv759970.hstgr.cloud
```

### Build Fails

```bash
npm run check  # TypeScript errors
rm -rf node_modules/.vite && npm install
npm run build
```

### Database Connection

```bash
echo $DATABASE_URL
docker exec postgresql-shared psql -U postgres -d jokers_prod -c "SELECT version();"
```

### Port Conflict

```bash
netstat -tulpn | grep :5020
```

### 502 Bad Gateway

```bash
pm2 restart jokers-hockey
sudo nginx -t
sudo tail -f /var/log/nginx/jokers_ssl_error.log
```

---

## 6. Health Check Script

```bash
#!/bin/bash
echo "=== Jokers Health Check ==="
pm2 status jokers-hockey | grep online && echo "PM2: OK"
curl -sI https://jokers.srv759970.hstgr.cloud | grep "200\|301" && echo "HTTP: OK"
netstat -tulpn | grep :5020 && echo "Port: OK"
docker exec postgresql-shared psql -U postgres -d jokers_prod -c "SELECT 1;" && echo "DB: OK"
```

---

## Security Notes

- Never commit .env files
- DATABASE_URL stored server-side only
- SSL auto-renews via Let's Encrypt
- Always test locally before deploying
