---
name: session-recovery
description: Troubleshoot Claude Code session issues. Use when encountering "No conversations found" errors, missing sessions, or session file corruption problems.
allowed-tools: Read, Bash
---

# Claude Code Session Recovery Skill

## Quick Reference

**When to use this skill:**

- "No conversations found to resume" when running `claude -r`
- New conversations not creating session files
- Sessions appearing in wrong locations (`/tmp/` instead of `~/.claude/projects/`)
- Session history missing after environment changes
- IDE/terminal settings affecting session creation
- Need to migrate or recover 600+ legacy sessions

## Official Session Storage

**Standard Location:** `~/.claude/projects/`

**Structure:**

```
~/.claude/projects/
├── -home-username-my-project/     # Encoded absolute path
│   └── 364695f1-13e7-4cbb-ad4b-0eb416feb95d.jsonl
└── -tmp-another-project/
    └── a8e39846-ceca-421d-b4bd-3ba0eb1b3145.jsonl
```

**Format:** One JSON event per line (JSONL), UUID-based filenames

## Critical Pitfall: HOME Variable

### Problem

Claude Code uses `$HOME` environment variable to determine session storage location. If `$HOME` is incorrect, sessions go to wrong directory or disappear.

### Symptoms

- `claude -r` shows "No conversations found to resume"
- New conversations work but files don't appear in expected location
- Sessions found in `/tmp/` or other unexpected paths
- Works on one machine but not another

### Diagnosis

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
# Step 1: Check current HOME
echo "Current HOME: $HOME"

# Step 2: Check system expectation
echo "Expected HOME: $(getent passwd $(whoami) | cut -d: -f6)"

# Step 3: Find where Claude is actually writing
find /tmp -name "*.jsonl" -path "*/.claude/projects/*" 2>/dev/null
PREFLIGHT_EOF
```

---

## Reference Documentation

For detailed diagnostic steps and solutions, see:

- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Detailed diagnostic procedures and fixes
