---
name: max-chat
allowed-tools: Bash(max:*)
description: Send messages to the Max AI assistant and manage conversations from the terminal. Use when the user wants to chat with Max, send a quick question, start a new conversation, or open an interactive chat session.
---

## Prerequisites

- The `max` CLI must be installed (`npm i -g @getfrontline/cli` — provides both `frontline` and `max` binaries).
- The user must have a per-user API key saved: `max auth login <api-key>` (or `frontline auth login` on the same profile).

## Commands

### Quick message (shorthand)

```bash
max "Your question here"
max --new "Start a fresh conversation"
```

This is the fastest way to send a single message to Max. It uses the last active conversation by default, or `--new` to start a fresh one.

Calls the **Public API**: `POST /public/v1/max/conversations/message` (Bearer = user API key). Responses use `{ "ok": boolean, "data": ... }`. Default stdout is **one-line JSON**; no spinner lines.

| Flag                   | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `--new`                | Start a new conversation instead of continuing the last one |
| `--conversation <id>`  | Send to a specific conversation ID                          |
| `--no-wait`            | Do not poll for the assistant reply (fire and forget)       |
| `--timeout <seconds>`  | Max seconds to wait for assistant reply (default: 60)       |
| `--json`               | Print only the POST response JSON (no poll)                 |
| `--pretty`             | Print assistant plain text from `data` instead of JSON      |
| `--profile <name>`     | Use a specific Max CLI profile                              |
| `--base-url <url>`     | Override Public API root (…/public/v1) for this run         |
| `--api-base-url <url>` | Deprecated alias for `--base-url`                           |
| `--api-key <key>`      | Override per-user API key for this run                      |
| `--debug`              | Show HTTP request/response diagnostics                      |

**Example:**

```bash
# Quick question using last conversation
max "What agents do I have?"

# Start a new conversation
max --new "Help me set up a new workflow"

# Send to a specific conversation
max --conversation 123 "Continue from here"
```

### Send a message (explicit command)

```bash
max chat send <message...> [--new] [--conversation <id>] [--json] [--debug]
```

Same as the shorthand above but under the `chat send` subcommand. Default stdout is **one-line JSON**; **`--pretty`** for assistant plain text from `data`.

### Interactive chat (REPL)

```bash
max chat repl [--profile <name>] [--debug] [--timeout <seconds>]
max chat
```

Opens an interactive readline session for back-and-forth conversation with Max.

| REPL Command | Description                              |
| ------------ | ---------------------------------------- |
| `:help`      | Show available REPL commands             |
| `:new`       | Start a new conversation on next message |
| `:conv <id>` | Switch to a specific conversation ID     |
| `:exit`      | Exit the REPL                            |
| `Ctrl+C`     | Exit the REPL                            |

**Example:**

```bash
# Start interactive chat
max chat

# Start with a specific profile
max chat repl --profile work --debug
```

### Conversations (Public API)

```bash
max conversations list [--pinned <bool>]
max conversations get <id>
max conversations update <id> --data '{"key":"value"}'
max conversations abort <id>
max conversations pin <id>
max conversations unpin <id>
# alias: max conv list
```

See `max conversations --help` for flags (`--profile`, `--base-url`, `--api-key`, `--debug`).

## Conversation management

- Max automatically remembers the last conversation ID in your profile. Subsequent messages continue that conversation.
- Use `--new` to explicitly start a fresh conversation.
- Use `--conversation <id>` to jump to a specific conversation.
- In the REPL, use `:new` and `:conv <id>` to manage conversations interactively.

## Troubleshooting

- **"No Max API key found"**: run `max auth login <api-key>` or `frontline auth login <api-key>` on the same profile.
- **"Message cannot be empty"**: provide a non-empty message string.
- **Timeout waiting for reply**: increase `--timeout` or use `--no-wait` and check the conversation later.
- Use `--debug` to see the full HTTP request URL, headers, and response status for diagnosing issues.
- Use `--json` for machine-readable output that can be piped to `jq` or other tools.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
