---
name: claude-code-orchestration
description: Orchestrate Claude Code (Anthropic CLI) as a subagent. Two modes — print mode (one-shot, fast) and PTY/tmux mode (interactive, multi-turn). Use when delegating a coding task to a fresh Claude Code session with restricted tools.
license: MIT
source: https://github.com/NousResearch/hermes-agent
---

# Claude Code Orchestration

Run Claude Code as a controlled subagent. Useful for isolated tasks that need their own context window, or to parallelize across multiple sessions.

**Trigger phrases:** "run claude code", "spawn claude", "delegate to claude code", "claude -p", "orchestrate claude", "claude subagent"

---

## Mode 1 — Print Mode (One-Shot)

Best for: self-contained tasks, CI-like execution.

```bash
# Basic one-shot
terminal(command="""
claude -p 'Add input validation to src/api/users.ts' \
  --allowedTools 'Read,Edit,Bash' \
  --max-turns 15 \
  --output-format text
""")

# With multi-line context
terminal(command="""
claude -p "$(cat <<'PROMPT'
Context: Fixing auth bug described in ISSUE.md.
Task: Fix JWT expiry check in src/auth/verify.ts.
Verify: Run npm test -- --testPathPattern=auth and confirm all pass.
PROMPT
)" --allowedTools 'Read,Edit,Bash' --max-turns 20
""")
```

**Key flags:**

| Flag | Use |
|------|-----|
| `--allowedTools 'Read,Edit,Bash'` | Restrict tools |
| `--max-turns 15` | Hard stop |
| `--output-format text` | Clean output |
| `--no-permission-prompts` | Auto-deny prompts (safe for subagents) |

---

## Mode 2 — PTY/tmux (Interactive Multi-Turn)

Best for: complex tasks requiring follow-up instructions.

```python
# Start session
terminal(command="tmux new-session -d -s claude-work -x 220 -y 50")
terminal(command="tmux send-keys -t claude-work 'cd /workspace && claude' Enter")
terminal(command="sleep 3 && tmux capture-pane -t claude-work -p | tail -5")

# Send task
terminal(command="tmux send-keys -t claude-work 'Refactor src/auth/ to use new JWT library.' Enter")

# Monitor
terminal(command="sleep 30 && tmux capture-pane -t claude-work -p | tail -20")

# Follow-up
terminal(command="tmux send-keys -t claude-work 'Also update db/migrations/002_auth.sql' Enter")

# Collect + clean up
terminal(command="tmux capture-pane -t claude-work -p")
terminal(command="tmux kill-session -t claude-work")
```

---

## Parallel Sessions

```python
tasks = ["Fix auth", "Add tests", "Update docs"]
for i, task in enumerate(tasks):
    terminal(command=f"tmux new-session -d -s work-{i}")
    terminal(command=f"tmux send-keys -t work-{i} 'claude' Enter")
    terminal(command=f"tmux send-keys -t work-{i} '{task}' Enter")

# Collect all results
for i in range(len(tasks)):
    terminal(command=f"tmux capture-pane -t work-{i} -p | tail -10")
    terminal(command=f"tmux kill-session -t work-{i}")
```

---

## Tool Restriction by Task Type

| Task | `--allowedTools` |
|------|----------------|
| Code review | `Read,Grep,Glob` |
| Bug fix | `Read,Edit,Bash` |
| New feature | `Read,Write,Edit,Bash` |
| Docs update | `Read,Write,Edit` |

Always exclude `WebFetch,WebSearch` unless needed.

---

## Anti-Fake-Pass

```
❌ No --max-turns → session runs forever
❌ tmux mode for simple one-shot → use print mode
❌ Not cleaning up tmux sessions → resource leak
❌ Sending next instruction before previous completes
❌ Not capturing output → can't verify what claude did
```

## See Also
- `core/skills/claude-swarm-orchestration/SKILL.md` — Python swarm with quality gate
- `core/agents/spec-executor.md` — plan execution agent
