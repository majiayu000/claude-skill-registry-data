---
name: health
description: Quick health check for ChefFlow - type check, build status, server status, and database connectivity.
user-invocable: true
---

# ChefFlow Health Check

Run these checks in order. Report results concisely.

## 1. Dev Server Status

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3100
```

Expected: 200

## 2. Production Server Status

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

Expected: 200 (if prod is running)

## 3. Type Check

```bash
npx tsc --noEmit --skipLibCheck 2>&1 | tail -20
```

Expected: exit 0, no errors

## 4. Database Connection

```bash
docker ps --filter "name=chefflow" --format "{{.Names}} {{.Status}}"
```

Expected: chefflow_postgres Up (healthy)

## 5. Git Status

```bash
git status --short
git log --oneline -5
```

Report: clean/dirty, last 5 commits

## Report Format

| Check              | Result                     |
| ------------------ | -------------------------- |
| Dev Server (3100)  | UP / DOWN                  |
| Prod Server (3000) | UP / DOWN / NOT RUNNING    |
| Type Check         | PASS / FAIL (error count)  |
| Database           | HEALTHY / UNHEALTHY        |
| Git                | CLEAN / DIRTY (file count) |

If any check fails, flag it with the exact error.
