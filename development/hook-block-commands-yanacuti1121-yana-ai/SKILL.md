---
name: "hook-block-commands"
description: "Pattern guide for writing PreToolUse hooks that block dangerous shell commands. Use when: building or auditing a guard-destructive hook, adding new blocked patterns, reviewing what the current hook covers. Covers 3 safety levels (critical/high/strict) and 58+ regex patterns. Inspired by: karanb192/claude-code-hooks block-dangerous-commands pattern (MIT)."
---

# Hook Block Commands Pattern

## When to trigger

- "what does guard-destructive block?"
- "add pattern to hook", "block this command"
- "review hook coverage", "hook pattern"
- Auditing `core/hooks/guard-destructive.sh`

## Safety levels

| Level | Scope |
|---|---|
| `critical` | Catastrophic only: rm -rf ~, dd to disk, fork bombs |
| `high` (default) | + force push main, git reset --hard, git clean -f, chmod 777, curl\|sh, secret file ops |
| `strict` | + any force push, sudo rm, docker prune, crontab -r |

## Core pattern categories (58+ patterns)

### Filesystem destruction
- `rm -rf /`, `rm -rf ~`, `rm -rf $HOME`
- `mkfs.*`, `dd if=.* of=/dev/`
- `shred`, `wipe`

### Git destructive
- `git push.*--force.*main`, `git push.*-f.*main`
- `git reset --hard`, `git clean -fdx`, `git filter-branch`
- `git reflog expire`

### System/process
- `:(){:|:&};:` (fork bomb)
- `chmod -R 777`, `chmod 777 /`
- `sudo rm`, `sudo chmod`

### Secret exposure
- `cat ~/.aws/credentials`, `cat .env`
- `echo $.*TOKEN`, `env | grep.*KEY`
- Piping secrets to curl/netcat

### Exfiltration
- `curl.*upload`, `scp.*`, `rsync.*remote`
- `nc.*<IP>`, `netcat.*`

## Hook exit codes

```bash
exit 0  → allow (no output)
exit 2  → block (JSON reason on stdout)
```

## Blocking response format

```json
{
  "decision": "block",
  "reason": "🚫 Blocked: rm -rf on home directory. Safety level: high."
}
```

## Adding new patterns to guard-destructive.sh

1. Identify the pattern category (filesystem / git / system / secret / exfiltration)
2. Write a regex that matches the dangerous form but not safe variants
3. Add to the correct safety level block
4. Add a test case to `core/tests/hooks/run-hook-tests.sh`
5. Update hook `# Last Reviewed:` date

## Reference

YAMTAM hook: `core/hooks/guard-destructive.sh`
Tests: `core/tests/hooks/run-hook-tests.sh`
