---
name: tool-guard
description: >-
  Allowlist/denylist for AI agent tool calls with approval gates for destructive
  operations. Define which tools the agent can use freely, which require
  confirmation, and which are blocked entirely. Combines LOCO-Agent's resource
  authorization with Flare's anomaly-aware security heuristics.
  Trigger phrases: "restrict tools", "tool permissions", "block bash",
  "approval gate", "limit what you can do", "tool whitelist", "tool blacklist".
argument-hint: "[allow|deny|gate] [tool-name]"
allowed-tools: ""
---

# Tool Guard

Control which tools the agent can use and which need approval.

## When to Use

- User wants to restrict the agent's capabilities for a sensitive task
- Working in production environments where certain operations are dangerous
- Reviewing unfamiliar code where unrestricted shell access is risky
- Pair programming where the user wants to approve every write/edit

## Commands

Parse arguments to configure tool permissions:

- `/tool-guard allow Read,Grep,Glob` — only these tools, deny everything else
- `/tool-guard deny Bash` — block Bash, allow everything else
- `/tool-guard gate Edit,Write` — allow these tools but ask before each use
- `/tool-guard gate Bash --pattern "rm|kill|drop|chmod"` — gate Bash only for matching commands
- `/tool-guard status` — show current permissions
- `/tool-guard reset` — clear all restrictions

## Permission Levels

### Allow (default for all tools)
Tool can be used freely without notification.

### Gate
Tool can be used, but the agent must explain what it's about to do and wait
for user confirmation before proceeding.

Gate prompt format:
```
🔒 Tool Guard: requesting [tool-name]
   Action: [what the tool call will do, in plain English]
   Target: [file path, command, or URL]
   Why: [how this serves the current task]
   Proceed? (y/n)
```

### Deny
Tool cannot be used. If the task requires it, explain to the user what you
need and why, and ask them to either run the command themselves or adjust
permissions.

## Preset Profiles

For convenience, support named profiles:

### `readonly`
- Allow: Read, Grep, Glob, Agent
- Gate: (none)
- Deny: Edit, Write, Bash, NotebookEdit

### `careful`
- Allow: Read, Grep, Glob
- Gate: Edit, Write, Bash, Agent
- Deny: (none)

### `untrusted-repo`
- Allow: Read, Grep, Glob
- Gate: Edit, Write
- Deny: Bash (no shell execution in untrusted code)

### `production`
- Allow: Read, Grep, Glob
- Gate: Edit, Write, Bash (every shell command needs approval)
- Deny: (none, but all mutations gated)

Usage: `/tool-guard profile readonly`

## Enforceable Team Profiles (hook-based)

The commands above are advisory — they ask the agent to self-restrict. For
deterministic enforcement that a compromised skill or prompt injection cannot
talk past, safe-agent ships a PreToolUse hook (`hooks/tool-guard.sh`) that reads
a committed policy file and decides allow / ask / deny on every tool call,
outside the agent's context.

Activate a preset by copying it to the project's policy file:

```bash
mkdir -p .safe-agent
cp profiles/careful.json .safe-agent/policy.json   # or readonly / untrusted-repo / production
git add .safe-agent/policy.json                     # commit it — the whole team gets the same enforcement
```

Wire the hook once via `hooks/settings.example.json` (PreToolUse, matcher `""`).
Because the policy lives in the repo, "what's enforced here" stops being
per-developer tribal knowledge.

**Policy format** (`profiles/*.json`):
- `tools.allow` / `tools.gate` / `tools.deny` — tool names by tier.
- `patterns.deny` / `patterns.gate` — rules `{tool?, match, reason}` where `match`
  is an extended regex tested against the command (Bash), file path (Edit/Write/
  Read), or URL (WebFetch). A rule with no `tool` applies to all tools.
- `default` — `allow` | `deny` | `ask` for tools not in any list.

**Precedence** (first match wins): tool in `deny` → deny; `patterns.deny` hit →
deny; `patterns.gate` hit → ask (so "Bash allowed, but `rm` gated" works); tool
in `gate` → ask; tool in `allow` → allow; else `default`. If no policy file
exists, the hook defers to normal permission flow (no-op).

The behavioral commands and the hook compose: use a command for a one-off
session restriction, commit a profile for durable team-wide enforcement.

## Contextual Gating

Beyond static rules, apply contextual awareness:

1. **Path-based gating**: Gate writes to sensitive paths even if Write is allowed
   - `.env*`, `*.key`, `*.pem`, `credentials*` — always gate
   - `**/config/production*` — always gate
   - `.claude/`, `.cursor/` — gate (agent config modification)

2. **Command-based gating**: When Bash is allowed, still gate commands matching:
   - Destructive patterns: `rm -rf`, `git push --force`, `DROP TABLE`
   - Network egress: `curl -X POST`, `wget --post-data`, `scp`
   - Privilege escalation: `sudo`, `chmod 777`, `chown`
   - Package publishing: `npm publish`, `pip upload`

3. **Escalation**: If the same tool is gated 3+ times in a row and the user
   approves each time, suggest: "You've approved [tool] 3 times — want me to
   allow it for the rest of this session?"

## Status Report

When the user asks `/tool-guard status`:

```
## Tool Guard Status

Profile: careful (custom modifications)

| Tool    | Permission | Notes                          |
|---------|------------|--------------------------------|
| Read    | ✓ Allow    |                                |
| Grep    | ✓ Allow    |                                |
| Glob    | ✓ Allow    |                                |
| Edit    | 🔒 Gate    | Approved 2x this session       |
| Write   | 🔒 Gate    |                                |
| Bash    | 🔒 Gate    | + deny pattern: rm|kill|drop   |
| Agent   | ✓ Allow    |                                |

Gated calls this session: 4 (3 approved, 1 skipped)
```

## Behavior

- The `/tool-guard` commands are advisory — they instruct the agent to
  self-restrict. The agent follows them because they are well-structured
  instructions, not because they are technically enforced. For deterministic
  enforcement that a compromised skill or prompt injection cannot bypass, commit
  a profile and wire the `hooks/tool-guard.sh` PreToolUse hook (see "Enforceable
  Team Profiles" above). The two layers compose.
- Always explain what you would have done with a denied tool, so the user
  can take that action themselves if needed.
- Never try to work around a denied tool by using a different tool for the
  same purpose (e.g., using Bash `cat` when Read is denied).
- Persist permissions for the duration of the session. They reset when the
  conversation ends.
