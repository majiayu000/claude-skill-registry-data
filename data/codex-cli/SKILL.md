---
name: codex-cli
description: OpenAI Codex CLI fundamentals for code analysis, review, and validation. Use when (1) executing codex commands for code review/analysis, (2) configuring models (gpt-5.2-codex/gpt-5.2/gpt-5.1-codex-max/codex-mini), sandbox modes (read-only/workspace-write), or reasoning effort (low/medium/high/xhigh), (3) managing Codex sessions with resume, (4) integrating Codex into automation scripts. Do NOT use for orchestration patterns (use codex-claude-loop instead).
---

# Codex CLI Skill

## ⚠️ Environment Notice

| Environment | Git Repo | Command Format |
|-------------|----------|----------------|
| Interactive terminal | Any | `codex "prompt"` |
| **Claude Code / CI** | ✅ Yes | `codex exec -s read-only "prompt"` |
| **Claude Code / CI** | ❌ No | `codex exec --skip-git-repo-check -s read-only "prompt"` |

**Non-TTY environments** (Claude Code, CI pipelines, scripts) require `codex exec`.

### Git Repository Detection
Before executing Codex commands, check if the working directory is a Git repository:
```bash
# Check Git repository status
git rev-parse --git-dir 2>/dev/null && echo "Git repo: YES" || echo "Git repo: NO"
```

- **Git repo exists**: Use standard commands
- **No Git repo**: Add `--skip-git-repo-check` flag (requires user awareness of security implications)

## Quick Start

### In Git Repository (Standard)
```bash
# Basic code review (terminal)
codex "Review this code for bugs"

# Non-interactive mode (Claude Code/CI)
codex exec -s read-only "Review this code for bugs"

# With specific model and reasoning effort
codex exec -s read-only -m gpt-5.2-codex -c model_reasoning_effort=high "Deep analysis"

# With image input
codex exec -s read-only -i screenshot.png "What's shown here?"
```

### Outside Git Repository
```bash
# IMPORTANT: --skip-git-repo-check required for non-Git directories
# Ask user permission before using this flag

codex exec --skip-git-repo-check -s read-only "Review this code for bugs"

# With options
codex exec --skip-git-repo-check -s read-only -m gpt-5.2-codex "Deep analysis"
```

### Session Resume (Special Syntax)
```bash
# IMPORTANT: Options must come BEFORE 'resume' subcommand
# SESSION_ID is from previous command output (e.g., 019ae3a3-f1cf-7dc1-8eee-8f424ae7a6f0)

# In Git repository
codex exec -s read-only resume [SESSION_ID] "Continue the analysis"

# Outside Git repository
codex exec --skip-git-repo-check -s read-only resume [SESSION_ID] "Continue the analysis"
```

## Reference Documentation

- **[Commands Reference](references/commands.md)** - `codex`, `resume`, `apply`, input/output patterns
- **[Options Reference](references/options.md)** - Models, sandbox, reasoning effort, approval modes
- **[Examples](references/examples.md)** - Code review, security analysis, automation scripts

## Available Models

> **Full model details**: See [Options Reference](references/options.md#model-selection--m---model)

| Model | Best For |
|-------|----------|
| `gpt-5.2-codex` | Complex analysis, critical systems (recommended) |
| `gpt-5.2` | General AI tasks, multi-domain |
| `gpt-5.1-codex-max` | Security audits, architecture review |
| `gpt-5.1-codex-mini` | Quick checks, batch operations |

## Reasoning Effort

> **Usage examples**: See [Options Reference](references/options.md#reasoning-effort)

| Level | Use Case |
|-------|----------|
| `low` | Simple checks, syntax review |
| `medium` | Standard code review (default) |
| `high` | Security audits, complex logic |
| `xhigh` | Critical systems, exhaustive analysis |

## Sandbox Modes

| Mode | Description |
|------|-------------|
| `read-only` | Cannot modify files (safest, recommended) |
| `workspace-write` | Can modify workspace files |
| `danger-full-access` | Full system access (use sparingly) |

## Key Options

> **Full options list**: See [Options Reference](references/options.md#quick-reference)

## Common Patterns

> **Full examples**: See [Examples](references/examples.md) for detailed patterns

### Essential Patterns
```bash
# Code review (Claude Code/CI)
codex exec -s read-only "Review: $(cat src/auth.js)"

# Maximum depth analysis
codex exec -m gpt-5.2-codex -c model_reasoning_effort=xhigh -s read-only "Security audit"

# Session continuity
codex exec -s read-only resume [SESSION_ID] "Continue analysis"

# Cross-directory
codex exec -C ./backend --add-dir ./frontend -s read-only "Review API"

# Non-Git directory (ask user first)
codex exec --skip-git-repo-check -s read-only "Analyze code"
```

## Platform-Specific Notes

### Windows Limitations
| Issue | Description | Workaround |
|-------|-------------|------------|
| `-C` with absolute paths | `cwd is not absolute` error with Windows paths like `C:\path` | Use relative paths (`./subdir`) or run from target directory |
| Path separators | Backslashes may cause issues | Use forward slashes (`/`) in paths |

```bash
# AVOID on Windows:
codex exec -C C:\Projects\myapp -s read-only "analyze"

# USE instead:
cd C:\Projects\myapp && codex exec -s read-only "analyze"
# OR use relative paths:
codex exec -C ./myapp -s read-only "analyze"
```

## Error Handling

> **Error recovery patterns**: See [Examples](references/examples.md#automation)

| Error | Cause | Solution |
|-------|-------|----------|
| `stdin is not a terminal` | Using `codex` in non-TTY | Use `codex exec` |
| `Not inside a trusted directory` | Not in Git repo | Ask user, then use `--skip-git-repo-check` |
| `invalid value for '--ask-for-approval'` | Invalid approval value | Use: `untrusted`, `on-failure`, `on-request`, `never` |
| `unexpected argument` after `resume` | Options after `resume` | Place options BEFORE `resume` subcommand |
| `cwd is not absolute` | Windows absolute path | Use relative paths or `cd` first |
| `No prompt provided via stdin` | Empty prompt | Ensure prompt string is not empty |

## Timeout Configuration

| Task Type | Recommended Timeout | Claude Code Tool |
|-----------|---------------------|------------------|
| Quick checks | 2 minutes | `timeout: 120000` |
| Standard review | 5 minutes | `timeout: 300000` |
| Deep analysis | **10 minutes** | `timeout: 600000` |

**Recommendation**: Use `timeout: 600000` for all Codex exec commands (model_reasoning_effort=high/xhigh can take 3-7 minutes).

## Best Practices

1. **Use `codex exec`** in Claude Code and CI environments (non-TTY)
2. **Default to `-s read-only`** for all review tasks
3. **Match model + reasoning effort** to task complexity
4. **Use `resume`** to maintain session context
5. **Use `--add-dir`** for cross-project context
6. **Use `--full-auto`** only in controlled environments
7. **Ask user before `--skip-git-repo-check`** - explain implications
8. **Check valid approval values** - only use `untrusted`/`on-failure`/`on-request`/`never`
9. **Set 10-minute timeout** for all Codex exec commands (`timeout: 600000`)
