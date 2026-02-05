---
name: File Validation
description: Strict detection and removal of unrelated files before PR creation
---

# File Validation Skill

> Be strict, not permissive. Unrelated files MUST be removed, not suggested.

**Core Principle**: STRICT MODE - Unrelated files are removed immediately, not flagged for later cleanup.

---

## Overview

File validation ensures PRs contain only relevant changes. This prevents:
- Local dev artifacts (redis-cluster, .env.local, tmp/)
- Debug files (console.log, dump.rdb)
- OS/IDE artifacts (.DS_Store, .vscode/)
- Unintentional changes from other work

**Policy**: When unrelated files are detected, remove them. Don't suggest cleanup - do it.

---

## When to Use

**Trigger automatically** during:
- `/commit-commands:commit-push-pr`
- `/commit-commands:commit`
- Any PR creation workflow

**Trigger manually** with:
- `/v-file-validation:check`

---

## Commands

| Command | Purpose |
|---------|---------|
| `/v-file-validation:check` | Run detection and prompt for removal |

---

## Detection Patterns

### By File Path

Flag files containing these path segments:

| Pattern | Category | Example |
|---------|----------|---------|
| `local` | Local config | `config/local.json` |
| `test-data` | Test fixtures | `test-data/users.json` |
| `tmp` | Temporary | `tmp/debug.log` |
| `debug` | Debug files | `debug/output.txt` |
| `dump` | Data dumps | `dump/database.sql` |
| `cache` | Cache files | `.cache/` |
| `redis-cluster` | Local Redis | `redis-cluster/dump.rdb` |
| `docker-compose.override` | Local Docker | `docker-compose.override.yml` |

### By File Extension

Flag files with these extensions:

| Extension | Category | Example |
|-----------|----------|---------|
| `.log` | Log files | `app.log` |
| `.pid` | Process IDs | `server.pid` |
| `.rdb` | Redis dumps | `dump.rdb` |
| `.dump` | Data dumps | `postgres.dump` |
| `.swp` | Vim swap | `.file.swp` |
| `.pyc` | Python compiled | `__pycache__/*.pyc` |

### By File Name

Flag files matching these names:

| Name | Category |
|------|----------|
| `.DS_Store` | macOS artifact |
| `Thumbs.db` | Windows artifact |
| `desktop.ini` | Windows artifact |
| `.env.local` | Local env config |
| `.env.development.local` | Local env config |
| `.env.test.local` | Local env config |

### Common Categories

| Category | Examples | Why Unrelated |
|----------|----------|---------------|
| **Local dev artifacts** | `redis-cluster/`, `dump.rdb`, `.env.local` | Only exist in local environment |
| **Debug files** | `debug.log`, `tmp/`, `console-output.txt` | Temporary debugging |
| **OS artifacts** | `.DS_Store`, `Thumbs.db`, `desktop.ini` | OS-specific, should be in .gitignore |
| **IDE files** | `.vscode/`, `.idea/`, `*.swp` | IDE-specific, should be in .gitignore |
| **Build artifacts** | `node_modules/`, `dist/`, `build/`, `*.pyc` | Generated, should be in .gitignore |
| **Test data** | `test-data/`, `fixtures/local/` | Local testing only |
| **Config overrides** | `docker-compose.override.yml`, `local.settings.json` | Local dev config |

---

## Detection Logic

```python
def is_unrelated(file_path, pr_scope):
    # 1. Path-based detection
    unrelated_patterns = [
        'local', 'test-data', 'tmp', 'debug', 'dump',
        'cache', '.DS_Store', '*.log', '*.pid',
        'redis-cluster', 'docker-compose.override'
    ]

    if any(pattern in file_path for pattern in unrelated_patterns):
        return True

    # 2. Extension-based detection
    unrelated_extensions = ['.log', '.pid', '.rdb', '.dump', '.swp', '.pyc']
    if any(file_path.endswith(ext) for ext in unrelated_extensions):
        return True

    # 3. Scope-based detection
    # Read PR description + Linear issue
    # Check if file is mentioned or relates to scope
    if not file_mentioned_in_scope(file_path, pr_scope):
        return True

    return False
```

---

## Strict Mode Policy

### Wrong Approach (Too Permissive)

```
❌ "These files shouldn't affect the PR, but you may want to clean them up later"
```

### Right Approach (Strict)

```
✅ "These files are unrelated to this PR and must be removed:
- redis-cluster/dump.rdb (local dev artifact)
- .env.local (local config)
- tmp/debug.log (debug file)

Removing them now."
```

Then execute the removal.

---

## Handling User Override

**Rare case**: User insists files ARE related.

**Response**:
```
Okay, keeping the files. Please add justification to PR description:

## Unusual Files Included

This PR includes files that may appear unrelated:
- redis-cluster/: [Explain why needed]
- .env.local: [Explain why needed]

Justification: [User's explanation]
```

This documents the decision for reviewers.

---

## Integration Points

### With commit-commands Plugin

When `/commit-commands:commit-push-pr` runs:
1. List all changed files
2. Invoke `/v-file-validation:check`
3. If unrelated files found → Prompt for removal
4. After cleanup → Continue with commit

### With Tech Lead

Before tech lead approval:
1. Run file validation
2. If unrelated files found → Block until cleaned

---

## Reference Files

| File | Purpose |
|------|---------|
| `violet-brain/patterns/pr-quality.md` | PR quality standards and file validation criteria |
| `violet-brain/patterns/multi-agent-git.md` | Multi-agent git safety (never use `git add -A`) |

---

*Skill Version: 1.0.0*
