---
name: ci-loop
description: Run the CI fix agent — polls GitHub CI, reads failures, asks Claude to fix code, commits, and re-checks until green.
user-invocable: true
allowed-tools: Bash
---

Run the CI fix agent on the current branch:

```bash
python3 ~/.claude/agents/ci_loop.py
```

If the agent isn't installed yet, install it first:

```bash
pip install claude-agent-sdk anyio
```

Prerequisites: Python 3.10+, the `gh` CLI authenticated, and a branch with an open PR.
