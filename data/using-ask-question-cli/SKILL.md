---
name: Using ask-question CLI
description: Send prompts to ChatGPT via browser automation. Use this when you need to query ChatGPT from the command line or integrate with the /ask-question slash command.
allowed-tools: [Bash, Read]
---

# Using ask-question CLI

Send prompts to ChatGPT via Playwright browser automation with headless operation.

## Architecture

```
ask-question CLI ──► HTTP POST /ask ──► ask-question-server (daemon)
                                              │
                                              ▼
                                        Chromium (headless)
                                        + storageState session
                                              │
                                              ▼
                                        ChatGPT response
```

## Prerequisites

1. **Node.js** installed
2. **Playwright** with Chromium (`npm install` downloads it)
3. **npm link** run in the chatgpt-relay directory

## Setup (One-Time)

```bash
cd ~/Code/chatgpt-relay
npm install
npm link
ask-question-login  # Opens browser, log into ChatGPT
```

## Starting the Daemon

```bash
cd ~/Code/chatgpt-relay
npm run server:log
```

Keep this running in a dedicated terminal or tmux pane. It runs headless (no visible browser).

**Why `tee` to a log file?** This allows Claude Code to check logs via `tail ~/.local/state/chatgpt-relay/daemon.log` even when the daemon runs in a separate terminal.

**Expected output:**
```
[ask-question-server] Starting headless browser...
[ask-question-server] Using session: ~/.chatgpt-relay/storage-state.json
[ask-question-server] ChatGPT page opened.
[ask-question-server] Login verified.
[ask-question-server] HTTP server listening on http://127.0.0.1:3033
```

## Usage

### Direct prompt

```bash
ask-question "What is the capital of France?"
```

### From file

```bash
ask-question -f question.md -o answer.md
```

### Pipe input

```bash
echo "Explain async/await in JavaScript" | ask-question
```

### Options

| Option | Description |
|--------|-------------|
| `-f, --file <path>` | Read prompt from file |
| `-o, --output <path>` | Write response to file |
| `-t, --timeout <ms>` | Response timeout (default: 1200000 / 20 min) |
| `--continue` | Continue existing chat (default: start new chat) |
| `-h, --help` | Show help |

## Integration with /ask-question Slash Command

The `/ask-question` slash command in Claude Code uses this CLI:

1. Claude drafts a Stack Exchange-formatted question
2. Claude invokes: `ask-question -f question.md -o answer.md`
3. CLI blocks while ChatGPT responds (typically 1-10 minutes)
4. Claude reads the answer file and discusses

Use `/ask-question draft topic` to skip automation and just draft the question.

## Troubleshooting

### "Server not running or not responding"

Start the daemon:
```bash
ask-question-server
```

### "No session found"

Run login helper:
```bash
ask-question-login
```

### Session expired

ChatGPT sessions expire after a while. Re-run login:
```bash
ask-question-login
```

### Response timeout

Default is 20 minutes. Adjust if needed:
```bash
# Shorter timeout for quick questions
ask-question -t 120000 "What is 2+2?"

# Longer timeout for complex responses
ask-question -t 1800000 "Write a comprehensive analysis..."
```

## Debugging

### Request ID Tracing

Each request gets a unique ID (e.g., `[a1b2c3d4]`) logged on both CLI and server sides:

```
[ask-question] [a1b2c3d4] Attempt 1/2...
[ask-question-server] [a1b2c3d4] Received (500 chars)
[ask-question-server] [a1b2c3d4] Processing...
[ask-question-server] [a1b2c3d4] Sending response (1200 chars)
[ask-question] [a1b2c3d4] Success
```

Use this to correlate CLI errors with server logs.

### Connection Failures

The CLI automatically retries once on connection errors (fetch failed, ECONNREFUSED, etc.). If you see:
```
[ask-question] [a1b2c3d4] Error: fetch failed
[ask-question] [a1b2c3d4] Cause: ...
[ask-question] [a1b2c3d4] Cause code: UND_ERR_HEADERS_TIMEOUT
```

This indicates Undici's internal timeout fired. The CLI will retry automatically.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ASK_QUESTION_SERVER_URL` | `http://127.0.0.1:3033` | Server URL |
| `ASK_QUESTION_PORT` | `3033` | Server port |
| `ASK_QUESTION_STORAGE_STATE_FILE` | `~/.chatgpt-relay/storage-state.json` | Session file |

## Files

| Path | Purpose |
|------|---------|
| `~/.chatgpt-relay/storage-state.json` | Saved ChatGPT session (cookies/localStorage) |

## Architecture Deep Dive

### Components

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Claude Code                                                            │
│      │                                                                  │
│      ▼                                                                  │
│  /ask-question (slash command)                                          │
│      │                                                                  │
│      ▼                                                                  │
│  CLI (ask-question) ─► HTTP POST /ask ─► ask-question-server (daemon)   │
│                                               │                         │
│                                               ▼                         │
│                                         Chromium (headless)             │
│                                         + storageState session          │
│                                               │                         │
│                                               ▼                         │
│                                         ChatGPT tab                     │
│                                         (DOM automation)                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Design Decisions

**HTTP Daemon over WebSocket Connect**
- `launchServer()` doesn't support persistent sessions
- HTTP is curl-debuggable and simpler
- Request queue handles serialization naturally
- Browser runs headless (no focus-stealing)

**Headless with StorageState**
- `ask-question-login`: One-time headed browser for manual login, saves cookies
- `ask-question-server`: Headless browser loads saved session
- Session persists across server restarts

### Reliability Features

| Feature | Description |
|---------|-------------|
| Request ID Tracing | 8-char ID correlates CLI and server logs |
| Automatic Retry | CLI retries once on connection failures |
| Network Failure Detection | Tracks streaming response via `response.finished()` |
| Hard Reset on Errors | Closes and recreates page on failure |
| Login Verification | Server verifies login state at startup |

### Fragile Components (Maintenance Required)

These rely on ChatGPT's DOM structure and may break when ChatGPT updates their UI:

- Composer selectors (`div[contenteditable]`, `#prompt-textarea`)
- Send button selectors (`button[data-testid="send-button"]`)
- Message extraction (copy button, innerText fallback)
- Login detection (chat history panel visibility)
- Stop button lifecycle (generation progress)

**Mitigation:** Multiple selector fallbacks, semantic selectors where possible, clear error messages.
