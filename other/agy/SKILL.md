---
name: agy
description: Interact with Google Antigravity (agy) CLI — persistent multi-turn conversations using agy's --continue flag. Loads when user mentions agy, Antigravity, or asks to use a different local LLM.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agy, antigravity, google, local-llm, cli, interactive]
---

# Google Antigravity (agy)

Google Antigravity is a CLI-based AI assistant by Google DeepMind. It runs locally via the `agy` binary and supports persistent multi-turn conversations.

**Key binary:** `/home/chihmin/.local/bin/agy`

## Usage Pattern

The user interacts via the `/agy` prefix in conversation. This skill is loaded automatically when the user mentions "agy" or "Antigravity".

### Default: Continue Existing Session

```bash
/home/chihmin/.local/bin/agy --continue --prompt "user's message"
```

This continues the most recent conversation, preserving context. Use this by default for all follow-ups.

### Start New Session

Only when the user explicitly requests a new/fresh session:

```bash
/home/chihmin/.local/bin/agy --prompt "user's message"
```

### Command Flags Reference

| Flag | Description |
|------|-------------|
| `--prompt` / `-p` | Single non-interactive prompt, print response, exit |
| `--continue` / `-c` | Continue the most recent conversation |
| `--conversation` | Resume a specific conversation by ID |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests |
| `--print-timeout` | Timeout for print mode (default 5m) |
| `--add-dir` | Add a directory to the workspace |
| `--sandbox` | Run with terminal restrictions |
| `--log-file` | Override CLI log file path |

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `agy changelog` | Show changelog and release notes |
| `agy install` | Configure environment paths and shell settings |
| `agy plugin` | Manage plugins (install, uninstall, list, enable, disable) |
| `agy update` | Update CLI to latest version |

## Important Notes

1. **No interactive mode in non-TTY environments** — `agy --prompt-interactive` requires a controlling TTY (`/dev/tty`) and will fail with `bubbletea: could not open TTY`. Always use `--prompt` (non-interactive print mode) in this environment.

2. **Session persistence** — Sessions are stored at `~/.gemini/antigravity-cli/brain/<session-id>/`. The `--continue` flag auto-detects the most recent session.

3. **Tool permissions** — agy may request tool execution permissions (file read/write, shell commands). Use `--dangerously-skip-permissions` if the user wants to auto-approve all tool requests.

4. **Timeout** — Default print timeout is 5 minutes. For longer-running tasks, set `--print-timeout 15m`.

5. **Workspace** — Default project directory is `/home/chihmin/.gemini/antigravity-cli/scratch`. Use `--add-dir` to include additional directories.

## Workflow

When the user says something like "問 agy..." or "用 agy 跑...":

1. Extract the user's message/prompt
2. Run: `/home/chihmin/.local/bin/agy --continue --prompt "<extracted message>"`
3. Return agy's response to the user
4. For follow-up messages, continue with `--continue` until the user explicitly says "new session" or similar

## Session Management

To find all available session IDs:
```bash
ls ~/.gemini/antigravity-cli/brain/
```

To resume a specific session:
```bash
/home/chihmin/.local/bin/agy --continue --prompt "message" --conversation <session-id>
```

## Troubleshooting

### Quota Exhaustion (429 RESOURCE_EXHAUSTED)

The most common failure mode: agy calls Google Cloud APIs which have usage quotas. When exceeded:

```
RESOURCE_EXHAUSTED (code 429): Individual quota reached. Contact your administrator to enable overages. Resets in 4h5m58s.
```

**Diagnosis:** Check the log file:
```bash
cat ~/.gemini/antigravity-cli/log/cli-$(date +%Y%m%d_*.log | sort -r | head -1) | grep "RESOURCE_EXHAUSTED"
```

**Resolution:** Wait for the quota to reset. The error message includes the reset time. No action needed — it will auto-reset.

**Prevention:** Avoid rapid-fire repeated prompts. Space out requests to agy.

### Silent Exit (Empty Output)

If `agy --prompt` returns exit code 0 but no output, it may have hit an auth issue or quota. Check the latest log file for errors.

### No TTY for Interactive Mode

`agy --prompt-interactive` requires a controlling TTY and will fail with:
```
bubbletea: could not open TTY: open /dev/tty: no such device or address
```
Always use `--prompt` (non-interactive print mode) in non-TTY environments.

## Example

User: "問 agy 今天的 weather 怎麼樣"

Agent runs:
```bash
/home/chihmin/.local/bin/agy --continue --prompt "今天的 weather 怎麼樣"
```

Returns agy's response. Next message from user continues the same session automatically.
