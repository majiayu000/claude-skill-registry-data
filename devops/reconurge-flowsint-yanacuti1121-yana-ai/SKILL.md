---
name: reconurge--flowsint
description: "OSINT graph investigation platform — visual, flexible, extensible. Dùng khi cần map relationships, investigate entities, trace connections giữa người/tổ chức/domains."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Flowsint là open-source OSINT graph exploration tool cho security analysts và investigators.

## Quick start

```bash
# Requires: Docker + Make
git clone https://github.com/reconurge/flowsint
cd flowsint
make install
make start
# UI: http://localhost:3000
```

## Use cases

- Map relationships giữa entities (people, orgs, IPs, domains)
- Visualize investigation graphs
- Cybersecurity threat intelligence
- OSINT research với visual node graph

## Key features

- Graph-based visual investigation
- Extensible node types
- Export investigation graphs
- TypeScript, self-hosted

## Source

https://github.com/reconurge/flowsint
