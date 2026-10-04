---
name: declared-api-skill
description: Reads a public API using a declared token.
version: 0.1.0
author: ClawGuard
category: productivity
metadata:
  openclaw:
    requires:
      env:
        - TODOIST_API_KEY
      bins:
        - curl
      config:
        - config.json
    permissions:
      - network_access
    install:
      - kind: brew
        package: curl
---

# Declared API Skill

Use `curl` to call https://api.todoist.com with TODOIST_API_KEY.

Read `config.json` for the project ID selected by the user.
