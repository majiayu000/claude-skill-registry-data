---
name: Cloudflare Workers Builds
description: This skill should be used when the user asks about "deploy status", "build failed", "build logs", "deployment history", "worker deployment", "check build", "deployment succeeded", "build error", "CI/CD", "verify deployment", or needs to monitor Cloudflare Workers builds and deployments.
version: 1.0.0
---

# Cloudflare Workers Builds

Monitor and analyze Cloudflare Workers builds using the Workers Builds MCP server.

## Available Tools

| Tool | Purpose |
|------|---------|
| `workers_builds_set_active_worker` | Set the Worker ID for subsequent operations |
| `workers_builds_list_builds` | List recent builds for the active Worker |
| `workers_builds_get_build` | Get details for a specific build (by UUID) |
| `workers_builds_get_build_logs` | Fetch logs for a specific build |

## Deployment Verification Workflow

After deploying a Worker, verify success:

1. **Set active Worker**
   ```
   workers_builds_set_active_worker with Worker ID
   ```

2. **List recent builds**
   ```
   workers_builds_list_builds
   ```
   Check the latest build status (succeeded/failed)

3. **Get build details** (if needed)
   ```
   workers_builds_get_build with build UUID
   ```
   Review build and deploy commands

4. **Check build logs** (for failures or debugging)
   ```
   workers_builds_get_build_logs with build UUID
   ```
   Analyze errors or warnings

## Post-Deployment Checklist

After verifying the build succeeded:
1. Check build logs for warnings
2. Use observability tools to monitor initial traffic
3. Verify expected behavior with test requests

## Common Use Cases

| Scenario | Tools to Use |
|----------|--------------|
| Check if deployment succeeded | `list_builds` → check status |
| Debug failed deployment | `list_builds` → `get_build_logs` |
| Review deployment history | `list_builds` |
| Compare build configurations | `get_build` for multiple UUIDs |

## Tips

- Build UUIDs are returned by `list_builds`
- Failed builds will have error details in logs
- Set the active worker once per session
- Combine with observability tools to verify runtime behavior
