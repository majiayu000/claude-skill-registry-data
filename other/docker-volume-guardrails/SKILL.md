---
name: docker-volume-guardrails
description: Set up a Claude Code hook to unconditionally block Docker commands that permanently delete a volume (docker volume rm/prune, docker rm -v, docker system prune --volumes, docker compose down -v). Use when setting up guardrails against destructive volume deletion, or after "never delete volumes without confirmation" has been violated or nearly violated.
---

# Docker Volume Guardrails

Sets up a PreToolUse hook that unconditionally blocks any Docker command
that permanently deletes one or more volumes.

## Why unconditional, with no override

This repo's own global instructions already say: "never delete volumes
without explicit human confirmation." A hook only ever sees the raw command
string handed to it - it has no way to observe whether a human actually
confirmed *this specific* deletion earlier in the conversation. The only
mechanical enforcement that is actually faithful to that rule is to never
let the agent run this class of command at all - exactly matching
`git-guardrails-claude-code`'s own precedent for force-push and
`reset --hard`. If a human has genuinely decided to delete a volume, they
run that command themselves, outside the agent.

Companion to `docker-db-guardrails`, which handles a different class of
mistake (a schema/data-wipe command run against the wrong database because
its real target was never resolved and verified). This skill's class of
mistake needs no such resolution step - volume deletion is destructive
regardless of which volume it targets, so the rule is simply "never," full
stop.

## What Gets Blocked

- `docker volume rm` / `docker volume remove`
- `docker volume prune`
- `docker rm -v` / `docker rm --volumes` (removes anonymous volumes attached
  to a container)
- `docker system prune --volumes` (with or without `-a`)
- `docker compose ... down -v` / `--volumes`, and the legacy `docker-compose
  down -v`/`--volumes` binary

Ordinary volume **mounting** (`docker run -v /host:/container ...`,
`docker compose up`) is untouched - the hook only matches `-v`/`--volumes`
on the specific subcommands where that flag means "delete" (`rm`, `down`),
never on `run`/`create`/`up`, where the identical flag means "mount."

As with `docker-db-guardrails`, prose that merely *mentions* these commands
(a commit message or issue body discussing this very hook, for example) is
not blocked - the hook tokenizes with `shlex` and excludes the values of
text-carrying flags (`-m`/`--message`/`--body`/`--title`/`--comment`) from
the scan.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or
**all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at:
[scripts/block-volume-deletion.py](scripts/block-volume-deletion.py)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-volume-deletion.py`
- **Global**: `~/.claude/hooks/block-volume-deletion.py`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file, merging into any existing
`hooks.PreToolUse` array's `"Bash"` matcher entry — don't overwrite other
hooks already registered there (`git-guardrails-claude-code`,
`docker-db-guardrails`, etc.):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-volume-deletion.py"
          }
        ]
      }
    ]
  }
}
```

(Project scope: use
`"\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-volume-deletion.py"` instead.)

### 4. Verify

Test both directions before trusting the hook in a new environment:

```bash
SCRIPT=~/.claude/hooks/block-volume-deletion.py

# Should exit 2 (BLOCKED):
echo '{"tool_input":{"command":"docker volume rm my-app-data"}}' | "$SCRIPT"
echo '{"tool_input":{"command":"docker compose down -v"}}' | "$SCRIPT"

# Should exit 0 (allowed) — mounting a volume, and prose that merely mentions these words:
echo '{"tool_input":{"command":"docker run -v my-app-data:/data --rm image"}}' | "$SCRIPT"
echo '{"tool_input":{"command":"gh issue create --body \"should we ever allow docker volume prune?\""}}' | "$SCRIPT"
```

Then prove it fires live in-session: run an actual `docker volume rm
<some-real-volume-name>` in the Bash tool and confirm the hook intercepts it
with a `PreToolUse:Bash hook error` before it executes.

## Known limitations

- No override mechanism exists by design (see above) - if this blocks a
  deletion the user has genuinely authorized, the answer is the user runs
  it themselves, not a flag or environment variable that lets the agent
  bypass it. Adding a bypass would let an agent self-authorize the exact
  thing this hook exists to prevent.
- Does not resolve command substitution or shell variables in volume names
  or subcommands - the threat model is an honest agent's mistake, not
  adversarial evasion (same scoping rationale as `docker-db-guardrails`).
