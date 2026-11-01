---
name: yacy
description: "Control and manage a local YaCy search engine instance. Use when the user needs yacy functionality."
metadata: {"minis":{"originalSource":"https://clawskills.sh/skills/qsmtco-yacy","convertedAt":"2026-10-31T22:15:12.523Z","license":"Unknown"}}
---

# YaCy Skill

Control and manage a local YaCy search engine instance.

## Description

This skill provides an interface to interact with YaCy, the open-source distributed search engine, running on localhost. It allows you to start/stop the service, check status, and integrate search capabilities into your OpenClaw workflows.

## Prerequisites

- Docker installed and running
- Ports 8090 and 8443 available on localhost

## Installation

The YaCy container runs with persistent data stored in a Docker volume (`yacy_search_server_data`). To install:

```bash
docker run -d --name yacy_search_server -p 8090:8090 -p 8443:8443 -v yacy_search_server_data:/opt/yacy_search_server/DATA --restart unless-stopped --log-opt max-size=200m --log-opt max-file=2 yacy/yacy_search_server:latest
```

Access the web interface at: http://localhost:8090

Default credentials: admin / yacy (change after first login)

## Capabilities

- [x] Start YaCy container/daemon
- [x] Stop YaCy container/daemon
- [x] Check YaCy status
- [x] Perform web searches (RSS API)
- [ ] Manage indexing (future)

## Tools

This skill provides:
- `yacy_start` - Start the YaCy service
- `yacy_stop` - Stop the YaCy service
- `yacy_status` - Check if YaCy is running and view logs
- `yacy_search` - Perform a search query (replaces Brave search when configured as default)

## Configuration

Set in OpenClaw config or via environment:
- `yacy_dir` - Path to YaCy installation (default: `/home/q/.openclaw/workspace/yacy_search_server`)
- `port` - HTTP port (default: `8090`)

## Replacing Brave Search

To make YaCy your default web search:
1. Install and start YaCy
2. Set OpenClaw config: `tools.defaultSearch = "yacy_search"`
3. Remove `BRAVE_API_KEY` environment variable if set

Now all "search for X" requests will use your local YaCy instance instead of Brave.

## Notes

YaCy runs completely locally and can be used as a privacy-focused search solution. It also participates in the global YaCy peer-to-peer network by default, but this can be disabled in settings.

## License

GPL 2.0+ (same as YaCy)

---
Created: 2026-02-11
Skill version: 0.1.0
Target OpenClaw: 2026.2.9+
