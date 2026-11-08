---
name: mema
description: Mema's personal brain - SQLite metadata index for documents and Redis short-term context buffer. Use for organizing workspace knowledge paths and managing ephemeral session state.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["REDIS_HOST","REDIS_PORT"]},"install":[{"id":"pip-deps","kind":"exec","command":"pip install -r requirements.txt"}]}}
---
# Mema Brain (Centralized Memory)

Standardized memory system providing a Metadata Index (SQLite) and Short-Term Context (Redis).

## Core Components

### 1. Document Index (SQLite)
- **Primary Path:** `~/.openclaw/memory/main.sqlite`
- **Capability:** Stores file paths, titles, and tags. 
- **Note:** This is a **Metadata Index only**. It does not ingest or provide full-text search of file contents.

### 2. Short-Term Memory (Redis)
- **Key Prefix:** `mema:mental:*`
- **Purpose:** Ephemeral state management and cross-session context passing.
- **TTL:** Default 6 hours (21600 seconds).

## Core Workflows

### Indexing Knowledge
Record a file's location and tags in the local database.
- **Usage**: `python3 $WORKSPACE/skills/mema/scripts/mema.py index <path> [--tag <tag>]`

### Searching Index
List indexed paths filtered by tag or recency.
- **Usage**: `python3 $WORKSPACE/skills/mema/scripts/mema.py list [--tag <tag>]`

### Mental State (Redis)
Manage key-value pairs in the `mema:mental` namespace.
- **Set**: `python3 $WORKSPACE/skills/mema/scripts/mema.py mental set <key> <value> [--ttl N]`
- **Get**: `python3 $WORKSPACE/skills/mema/scripts/mema.py mental get <key>`

## Setup
1. Copy `env.example.txt` to `.env`.
2. Configure `REDIS_HOST` and `REDIS_PORT` (defaults: localhost:6379).
3. Initialize the SQLite schema:
   `python3 $WORKSPACE/skills/mema/scripts/mema.py init`

## Reliability & Security
- **Data Privacy**: All data is stored locally.
- **Network Safety**: Only point `REDIS_HOST` to trusted instances.
- **Path Isolation**: Database operations are confined to the `~/.openclaw/memory` directory.
