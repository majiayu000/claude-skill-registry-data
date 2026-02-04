---
name: local-dev-server
description: PM2-based local development server management for Empathy Ledger. Handles port conflicts and auto-restart.
---

# Local Dev Server

PM2-based server management for reliable local development.

## When to Use
- Starting/stopping dev server
- "Address already in use" errors
- Server crashes and needs restart
- Testing API endpoints

## Quick Commands
```bash
# Start server (port 3030)
pm2 start npm --name "empathy-ledger" -- run dev

# Restart after code changes
pm2 restart empathy-ledger

# View logs
pm2 logs empathy-ledger

# Stop server
pm2 stop empathy-ledger
```

## Fix Port Conflicts
```bash
# Kill process on port and restart
lsof -ti :3030 | xargs kill -9
pm2 start npm --name "empathy-ledger" -- run dev
```

## ACT Ecosystem
```bash
# Start all projects
/Users/benknight/act-global-infrastructure/deployment/scripts/deploy-act-ecosystem.sh start

# Restart all
/Users/benknight/act-global-infrastructure/deployment/scripts/deploy-act-ecosystem.sh restart

# Stop all
/Users/benknight/act-global-infrastructure/deployment/scripts/deploy-act-ecosystem.sh stop
```

## PM2 vs npm run dev
- **Use PM2**: Auto-restart, centralized logs, multi-project
- **Use npm run dev**: Quick testing, active debugging

## Reference Files
| Topic | File |
|-------|------|
| Full PM2 reference | `refs/pm2-commands.md` |

## Related Skills
- `deployment-workflow` - Production deployment
- `supabase-connection` - Database setup
