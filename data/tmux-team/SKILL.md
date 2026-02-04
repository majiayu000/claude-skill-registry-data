---
name: tmux-team
description: Coordinate with other AI agents running in tmux panes. Use this skill when you need to delegate tasks, request reviews, or collaborate with agents like Codex, Gemini, or other Claude instances.
---

# Multi-Agent Coordination with tmux-team

You are working in a multi-agent tmux environment. Use the `tmux-team` CLI to communicate with other AI agents running in different panes.

## When to Use This Skill

- Delegating specialized tasks to other agents (e.g., "Ask Codex to review this code")
- Broadcasting messages to all agents
- Checking responses from agents you've messaged
- Coordinating parallel work across multiple agents

## Commands (use --wait for better token utilization)

```bash
# Send and wait for response (recommended)
tmux-team talk codex "your message" --wait
tmux-team talk gemini "your message" --wait --timeout 120

# Broadcast to all agents
tmux-team talk all "message for everyone" --wait

# List configured agents
tmux-team list
```

## Workflow

The `--wait` flag blocks until the agent responds, returning the response directly:

```bash
tmux-team talk codex "Review this authentication code" --wait
# Response is returned directly - no need for a separate check command
```

## Tips

- **Always use `--wait`** - it's more token-efficient than polling with `check`
- Use `--timeout 300` for complex tasks that need more time
- Use `--delay 5` to add delay between messages (rate limiting)
- Run `tmux-team learn` for a comprehensive guide
