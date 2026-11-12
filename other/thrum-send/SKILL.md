---
name: thrum-send
description: Send a message to an agent
# source: claude-plugin/commands/send.md
---

# Thrum Send

Use this skill when the user explicitly wants the `send` Thrum workflow. Prefer
the umbrella `thrum` skill when the request spans multiple commands or needs
broader coordination judgment.

Send a direct message or broadcast.

If arguments are provided, use them. Otherwise ask for recipient and message
content.

```bash
thrum send --to @agent_name --stdin <<'EOF'       # Direct message (quoted heredoc body)
message here
EOF
thrum send --to @agent_a --to @agent_b --stdin <<'EOF'   # Multiple explicit recipients
message here
EOF
```

Unknown recipients are a hard error. Use `thrum team` to verify agent names
before sending.

`@everyone` was removed by design (P0 ruling); do not restore it — name every
recipient explicitly, or address a scoped agent-type group.

If the body has backticks, `$(...)`, `$VAR`, or quotes, pass it via a quoted
heredoc so the shell doesn't corrupt it:

```bash
thrum send --to @agent_name --stdin <<'EOF'
Run `make build`, then check $(git rev-parse HEAD).
EOF
```

`--body-file <path>` reads from a file; the body argument `-` is a stdin alias.
