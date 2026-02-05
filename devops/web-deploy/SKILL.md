---
name: web-deploy
description: Website deployment to Caddy. Use when user mentions deploy website, create page, update site, publish, reload caddy.
---

# Web Deploy Skill

Deploy websites to Caddy static server.

## Deployment Workflow

### 1. File Location
```bash
/home/pai/merlin/workspace/site/
```

### 2. Create/Edit Files
Use `Write` or `Edit` tool.

### 3. Reload Caddy
Use MCP tool: `system_reload_caddy`

### 4. Report URL
Report using `site_url` from `../merlin-config.json`.

## Notes

- Site root: `/home/pai/merlin/workspace/site/`
- Domain and URL are configured in `../merlin-config.json`
- Caddy serves directory directly, no build needed
- File permissions are auto-fixed when reloading Caddy
