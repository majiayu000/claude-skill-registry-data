---
name: "agv"
version: "1.0.0"
description: "Automated guided vehicle route planner. Use when json agv tasks, csv agv tasks, checking agv status."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [agv, industrial, cli, tool]
category: "industrial"
---

# agv

Automated guided vehicle route planner. Use when json agv tasks, csv agv tasks, checking agv status.
## Commands

### `status`

```bash
scripts/script.sh status
```

Show current status

### `add`

```bash
scripts/script.sh add
```

Add new entry

### `list`

```bash
scripts/script.sh list
```

List all entries

### `search`

```bash
scripts/script.sh search
```

Search entries

### `remove`

```bash
scripts/script.sh remove
```

Remove entry by number

### `export`

```bash
scripts/script.sh export
```

Export data to file

### `stats`

```bash
scripts/script.sh stats
```

Show statistics

### `config`

```bash
scripts/script.sh config
```

View or set config

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Configuration

Use `scripts/script.sh config <key> <value>` to set preferences.

| Variable | Description |
|----------|-------------|
| `AGV_DIR` | Data directory (default: ~/.agv/) |
---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
