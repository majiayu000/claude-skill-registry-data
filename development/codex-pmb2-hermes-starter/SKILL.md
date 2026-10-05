---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    triggers: [codex, openai-codex, codex-cli, coding-agent, ai-coding]
    related_skills: [claude-code, hermes-agent, opencode]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## When to escalate to Codex

If you (Hermes) have attempted 3+ distinct fixes for a coding/technical problem and are still stuck, delegate to Codex instead of continuing to thrash. the operator's rule: "If you continue to struggle, connect with Codex." This applies to:
- Debugging sessions where fixes aren't sticking
- Feature implementations hitting a wall
- Any task where you're past the third attempt without resolution

### the operator's Preferred Pattern: Scope Document → Delegate

When escalating a complex multi-fix debugging session that has uncovered several issues:

1. **Compile a comprehensive scope document** first — enumerate everything:
   - What works vs. what's broken (in priority order)
   - All fixes tried so far and their outcomes
   - All file paths and relevant code sections
   - Environment details (OS, Python version, GPU, dependency versions)
   - The ideal end state (what "done" looks like)
   - Any diagnostic scripts or test results already produced

2. **Delegate to Codex via `delegate_task`** with full context, not a bare `terminal(codex)` call. Use:
   ```python
   delegate_task(
       goal="Fix [specific problem — NOT a research task]",
       context="""Full scope document as described above.
   Use: codex -m gpt-5.4 -c model_reasoning_effort="high" exec "<prompt>"
   Work in /path/to/git/repo""",
       toolsets=['terminal', 'file']
   )
   ```

3. **Verify and patch after Codex finishes** — Codex may introduce new issues (log spam, race conditions, missing imports). Always review the diff and run a quick smoke test. Patch any post-Codex issues yourself — don't re-delegate for cleanups.

Delegate the full context — error messages, file paths, what was tried — so Codex can pick up where you left off. Use `delegate_task` with `toolsets=['terminal', 'file']` for isolated investigation.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- **Must run inside a git repository** — Codex refuses to run outside one
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

### Check Current Configuration

Before running, inspect `~/.codex/config.toml` to know the active model, reasoning effort, sandbox mode, and marketplace sources:

```bash
cat ~/.codex/config.toml 2>/dev/null | grep -E '^(model|model_reasoning_effort|approvals_reviewer)' || echo "no codex config"
```

This reveals what model Codex is currently using and whether `reasoning_effort` is set to `"high"`. Override at runtime with the flags below.

### Model & Reasoning Selection

Codex uses a model configured in `~/.codex/config.toml`. Override per-run:

- **`-m <model>`** — Select model (e.g., `-m gpt-5.5`, `-m o3`, `-m gpt-5.4`)
- **`-c model_reasoning_effort="high"`** — Set reasoning effort (high/medium/low)

Example — override both in one shot:

```bash
codex -m gpt-5.5 -c model_reasoning_effort="high" exec "Add dark mode toggle"
```

For complex tasks requiring lengthy prompts with multiple instructions, pass the prompt via `-C <workdir>` and write a self-contained multi-line prompt:

```bash
codex -m gpt-5.5 -c model_reasoning_effort="high" -C /path/to/repo exec "
Fix these bugs in src/transport.py:

1. Add grace period to prevent immediate disconnect after voice join
2. Reduce audio logging to once per user burst instead of every frame
3. Cancel orphan tasks on disconnect

Work in /path/to/repo.
"
```

The `-C/--cd <DIR>` flag sets the working directory inside Codex's sandbox.

## Delegating to Codex via delegate_task

For complex coding tasks, delegate to a subagent that runs Codex directly. This keeps the Codex interaction isolated and avoids PTY issues with the main terminal:

```
delegate_task(
    goal="Fix voice agent transport bugs",
    context="""The voice agent at /path/to/voice-agent has these bugs:
1. Bot leaves voice channel immediately on join
2. Audio logging floods console every 20ms frame

Use: codex -m gpt-5.5 -c model_reasoning_effort="high" exec "<detailed instructions>"
Work in the voice-agent git repo directory.
""",
    toolsets=['terminal', 'file']
)
```

This pattern is preferred when:
- The fix needs 3+ targeted edits across a file
- Codex needs to read the full file context and apply patches
- You want isolated terminal state without risk of PTY conflicts

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |
| `-m <model>` | Model selection (e.g., `gpt-5.5`, `o3`) |
| `-c key=value` | Override any config.toml value (e.g., `model_reasoning_effort="high"`) |
| `-C/--cd <DIR>` | Working directory inside sandbox |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Common Pitfalls

1. **`pty=true` is required for interactive mode** — Codex is a TUI and hangs without a PTY. `opencode run` does NOT need pty, but interactive sessions do.
2. **Git repo required everywhere** — Codex refuses to run outside a git directory. For scratch work, use `mktemp -d && git init`.
3. **Always use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly. Without `exec`, Codex starts in interactive mode.
4. **`--full-auto` vs `--yolo` distinction** — `--full-auto` auto-approves changes within the isolated sandbox. `--yolo` removes the sandbox entirely — use only for throwaway scratch work on isolated branches.
5. **Don't trust Codex self-report as verification** — Codex may report success when changes are partial or broken. Always inspect the diff (`git diff`) and run tests independently.
6. **Session state is per-directory** — `--continue` resumes the most recent session in the current working directory. If you change directories, you lose the session link.
7. **Background sessions persist** — Always clean up with `process(action="kill")` when done. Orphan sessions consume resources.
8. **Enter may need pressing twice in `process(action="submit")`** — In pty mode, the first Enter finalizes text input, the second submits the prompt.
9. **Codex runs slow on first invocation** — Model loading and sandbox initialization can take 10-30 seconds. Set generous timeouts (60s+).
10. **`codex` binary resolution varies** — npm vs brew installations put the binary in different paths. Use `which -a codex` to check.

## Verification Checklist

- [ ] `codex --version` returns expected version number
- [ ] `codex exec 'echo OK'` works (basic smoke test)
- [ ] For code changes: `git diff --stat` shows only expected files changed
- [ ] Canonical tests pass after Codex edits (run from Hermes, not just Codex self-report)
- [ ] No secrets, credentials, or generated artifacts included in the diff
- [ ] `--allowedTools` / `--full-auto` flags match the task's safety requirements
- [ ] Background sessions cleaned up: `process(action="kill")` for any orphan sessions
- [ ] For PRs: run `codex review --base origin/main` or equivalent

## Rules
