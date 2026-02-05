---
name: vercel-debug
description: Investigate Vercel deployment errors using Vercel CLI. Use when user shares a Vercel deployment error, build failure, or deployment URL that needs debugging.
---

# Vercel Deployment Debugging

## Workflow

### 1. Check authentication

```bash
vercel whoami
```

If error "No credentials found", prompt user to run `vercel login` in their terminal (interactive).

### 2. List recent deployments

```bash
vercel list <project-name> --scope <team-name>
```

Find the failing deployment URL (status: `Error` or `Building`).

### 3. Get build logs

```bash
vercel inspect <deployment-url> --logs --scope <team-name>
```

Add `--wait` to wait for in-progress builds:
```bash
vercel inspect <deployment-url> --logs --scope <team-name> --wait
```

### 4. Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Mixed Routing Properties | `routes` and `rewrites` mixed in vercel.json | Use only `rewrites` (new format) |
| Cannot find module | Package not built before dependent | Add to build command or use turbo |
| Build Command > 256 chars | Command too long | Use `pnpm build` with turbo/nx |

### 5. Get deployment info (without logs)

```bash
vercel inspect <deployment-url> --scope <team-name>
```
