---
name: "ppe"
version: "1.0.0"
description: "Personal protective equipment tracker. Use when json ppe tasks, csv ppe tasks, checking ppe status."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [ppe, safety, cli, tool]
category: "safety"
---

# ppe

Personal protective equipment tracker. Use when json ppe tasks, csv ppe tasks, checking ppe status.
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
| `PPE_DIR` | Data directory (default: ~/.ppe/) |
---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
