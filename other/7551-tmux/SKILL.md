---
name: tmux
description: >
  Control tmux sessions for testing and verification.
  Use when launching Claude Code test sessions, verifying plugins/skills/hooks in fresh sessions,
  sending commands to interactive terminal applications, or reading output from background processes.
  Triggers on: "launch a test session", "verify in a fresh session", "check tmux", "send to tmux",
  "create a tmux session", "read tmux output", "clean up sessions".
---

# Tmux Session Control

Control tmux sessions for launching test/verification Claude Code sessions, sending commands, and reading output. Multi-agent safe.

## Hard Rules

1. **Own sessions only.** Only interact with sessions YOU created this conversation. Never touch other `agent-*` sessions.
2. **User sessions are hands-off.** Sessions like `claude`, `claude-1`, `shell` belong to the user. Do not create, kill, send input, or modify them unless the user explicitly names one and gives permission.
3. **Registry every session.** Every session you create MUST be registered. Every session you kill MUST be marked closed.
4. **Clean up before "done".** Before reporting any task as complete, run the Cleanup recipe for every session you created.
5. **Sleeps are not optional.** Always wait between send-keys and capture-pane. Race conditions are silent and hard to debug.

## Recipe 1: Create a Session

```bash
# 1. Generate unique name (max 40 chars)
SESSION="agent-<context>-$(openssl rand -hex 2)"

# 2. Ensure registry directory exists
mkdir -p ~/.local/share/tmux-skill

# 3. Create detached session with initial command
#    Always pass command as argument — avoids shell-ready race
tmux new-session -d -s "$SESSION" -c "<workdir>" "<command>"

# 4. Verify it was created
tmux list-sessions -F '#{session_name}' | grep -qx "$SESSION"
# If this fails: regenerate UUID suffix and retry ONCE

# 5. Register (flock prevents concurrent write corruption)
flock ~/.local/share/tmux-skill/sessions.jsonl -c \
  "echo '{\"session\":\"$SESSION\",\"created\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"creator\":\"$$\",\"bead\":\"<bead-id-or-none>\",\"purpose\":\"<why>\",\"workdir\":\"<workdir>\",\"status\":\"active\"}' >> ~/.local/share/tmux-skill/sessions.jsonl"
```

**Session naming:** `agent-<context>-<4-char-hex>`
- `<context>`: bead ID, task name, or purpose (e.g., `4p8`, `verify-hooks`)
- Only `[a-zA-Z0-9_-]` characters. No dots, colons, spaces.
- Examples: `agent-4p8-a3f2`, `agent-verify-hooks-b7e1`

## Recipe 2: Send Input to a Session

```bash
# 1. Escape copy-mode (safe even if not in copy-mode)
tmux send-keys -t "$SESSION" -X cancel 2>/dev/null || true

# 2. Send text in literal mode (prevents tmux key interpretation)
tmux send-keys -t "$SESSION" -l -- "your text here"

# 3. Wait for text to be processed
sleep 0.2

# 4. Send Enter separately
tmux send-keys -t "$SESSION" Enter
```

**For multiline or long text (>400 chars):**

```bash
# Write content to unique temp file
cat > "/tmp/agent-${SESSION}-input.txt" << 'CONTENT'
your multiline
content here
CONTENT

# Load into tmux buffer and paste
tmux load-buffer -b agent-buf "/tmp/agent-${SESSION}-input.txt"
tmux paste-buffer -p -d -b agent-buf -t "$SESSION"
sleep 0.2
tmux send-keys -t "$SESSION" Enter

# Clean up
rm -f "/tmp/agent-${SESSION}-input.txt"
```

**For complex shell commands (quotes, pipes, variables):**

```bash
# Write command to temp script
cat > "/tmp/agent-${SESSION}-cmd.sh" << 'CMD'
echo "complex command with $VARS and | pipes"
CMD

# Send the script path (simple, no escaping needed)
tmux send-keys -t "$SESSION" -l -- "bash /tmp/agent-${SESSION}-cmd.sh"
sleep 0.2
tmux send-keys -t "$SESSION" Enter

# Clean up after output is captured
```

**Special keys (no -l flag):** `C-c`, `C-d`, `Escape`, `Enter`

```bash
tmux send-keys -t "$SESSION" C-c      # Ctrl+C
tmux send-keys -t "$SESSION" Escape    # Escape key
```

## Recipe 3: Read Output from a Session

```bash
# Quick check — last 20 lines
tmux capture-pane -t "$SESSION" -p | tail -20

# Deeper analysis — last 500 lines
tmux capture-pane -t "$SESSION" -p -S -500

# Full scrollback (use sparingly — can be huge)
tmux capture-pane -t "$SESSION" -p -S -

# Join wrapped lines (better for programmatic parsing)
tmux capture-pane -t "$SESSION" -p -J -S -500
```

**IMPORTANT:** After sending input, always `sleep 0.3` before capturing. Output needs time to flush.

## Recipe 4: Launch a Claude Code Test Session

```bash
# 1. Create session running Claude with auto-accept permissions
#    ONLY for throwaway test sessions — never for real data or shared repos
SESSION="agent-<context>-$(openssl rand -hex 2)"
mkdir -p ~/.local/share/tmux-skill
tmux new-session -d -s "$SESSION" -c "<workdir>" "claude --dangerously-skip-permissions"

# 2. Verify + register (see Recipe 1, steps 4-5)

# 3. Wait for Claude to boot
sleep 8

# 4. Check if Claude is ready
tmux capture-pane -t "$SESSION" -p | tail -10

# 5. Send a test prompt (use Recipe 2)
tmux send-keys -t "$SESSION" -l -- "Your test prompt here"
sleep 0.2
tmux send-keys -t "$SESSION" Enter

# 6. Wait for response, then read
sleep 10  # adjust based on expected response time
tmux capture-pane -t "$SESSION" -p -S -500

# 7. Exit Claude when done
tmux send-keys -t "$SESSION" -l -- "/exit"
sleep 0.2
tmux send-keys -t "$SESSION" Enter
```

**For non-interactive verification (preferred when possible):**

```bash
# No tmux needed — run Claude directly
CLAUDECODE= claude --print --output-format text "your verification prompt"
```

## Recipe 5: Clean Up (MANDATORY Before "Done")

```bash
# For EACH session you created this conversation:

# 1. Kill the session
tmux kill-session -t "$SESSION" 2>/dev/null || true

# 2. Mark closed in registry
flock ~/.local/share/tmux-skill/sessions.jsonl -c \
  "echo '{\"session\":\"$SESSION\",\"status\":\"closed\",\"closed\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}' >> ~/.local/share/tmux-skill/sessions.jsonl"

# 3. Clean up temp files
rm -f /tmp/agent-${SESSION}-*.sh /tmp/agent-${SESSION}-*.txt
```

## Recipe 6: Check for Orphaned Sessions (Housekeeping)

Run at the start of a conversation if tmux hygiene is relevant.

```bash
# 1. List all active agent sessions from registry
grep '"status":"active"' ~/.local/share/tmux-skill/sessions.jsonl 2>/dev/null | while IFS= read -r line; do
  SESSION=$(echo "$line" | grep -o '"session":"[^"]*"' | cut -d'"' -f4)

  # 2. Check if session still exists in tmux
  if ! tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -qx "$SESSION"; then
    # 3. Mark as orphaned
    flock ~/.local/share/tmux-skill/sessions.jsonl -c \
      "echo '{\"session\":\"$SESSION\",\"status\":\"orphaned\",\"detected\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}' >> ~/.local/share/tmux-skill/sessions.jsonl"
  fi
done
```

Sessions active for more than 4 hours are candidates for cleanup. Registry entries older than 7 days can be purged.

## Listing Sessions

```bash
# All tmux sessions (safe — read-only)
tmux list-sessions

# Just agent-managed sessions
tmux list-sessions -F '#{session_name}' | grep '^agent-'

# Check if a specific session exists (exact match)
tmux list-sessions -F '#{session_name}' | grep -qx "$SESSION"

# DO NOT use tmux has-session — it prefix-matches and hits wrong sessions
```

## Quick Reference: Defensive Patterns

| Situation | Do This |
|-----------|---------|
| Creating a session | Pass command as arg to `new-session` (not send-keys after) |
| Sending text | Always `-l` flag, always separate Enter, always `sleep 0.2` between |
| Reading output | Always `sleep 0.3` after send-keys before capture-pane |
| Multiline text | `load-buffer` + `paste-buffer`, NOT send-keys |
| Complex shell commands | Write to temp file, send `bash /tmp/file.sh` |
| Before any send-keys | Cancel copy-mode: `send-keys -X cancel 2>/dev/null \|\| true` |
| Session names | `agent-<context>-<4hex>`, max 40 chars, `[a-zA-Z0-9_-]` only |
| Name collision | Regenerate UUID suffix, retry once |
| Checking existence | `list-sessions` + `grep -qx`, never `has-session` |
| Registry writes | Always `flock` the JSONL file |
| Before claiming "done" | Kill all your sessions + update registry + delete temp files |
