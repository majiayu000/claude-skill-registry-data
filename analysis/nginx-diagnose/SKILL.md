---
name: nginx-diagnose
description: Analyze Nginx configuration and check for issues
activation_keywords: [nginx, config, configuration, web server, reverse proxy]
execution_mode: client
---

# Nginx Diagnose Skill

Provides read-only Nginx analysis:
- Test nginx configuration syntax
- Show active nginx configuration
- List enabled sites/vhosts
- Check nginx process status

Use `builtin_nginx_diagnose` tool with fields:
- `operation`: one of "test_config", "show_config", "list_sites", "status"

Note: All operations are read-only.
