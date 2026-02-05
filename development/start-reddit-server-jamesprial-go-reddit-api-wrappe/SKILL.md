---
name: start-reddit-server
description: Provides simple script for safely starting the server. Use whenever you need to start ./cmd/reddit-server. Ex - "start the server..." "Debug the frontend...".
---

# start-reddit-server

## Overview

To start the server call bash(./.claude/skills/start-reddit-server/scripts/start-reddit-server.sh).
Access it localhost:8080. Use gDU5S8l8BH8sCkJ3bC6t4SMYIxlrLlYB for the API key. It's a test key. For example:
```
curl -H "Authorization: Bearer gDU5S8l8BH8sCkJ3bC6t4SMYIxlrLlYB" http://localhost:8080/api/v1/user/me
```

## Logs

find logs in /logs/reddit-server-$(date +%Y%m%d-%H%M%S).log