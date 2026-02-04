---
name: Git Workflow
description: DO NOT COMMIT unless user explicitly tells you to. Use this skill EVERY SINGLE TIME before creating a git commit. Provides mandatory commit message format, staging rules, and post-commit summary requirements for the MIRA project
---

# Git Workflow - MIRA Standards

Expert guidance for git operations in the MIRA project, emphasizing clear commit messages and proper staging practices.

## 🎯 Purpose

This skill provides git workflow standards for the MIRA project:
- Streamlined commit message format (CONTEXT → INSIGHT → APPROACH → CHANGES)
- Safe staging practices to prevent accidental commits
- Post-commit summary requirements

## 🔀 OSS Sync Workflow

### MANDATORY: Ask Before Every Commit
MIRA maintains two repositories (`origin` = private, `oss` = public OSS).

**Before EVERY commit, you MUST ask:**

> "Sync to **OSS** after this commit?"

The repos have divergent codebases, so syncing requires running makeoss.sh:
- **Yes** → After commit: `./makeoss.sh` (auto-commits to OSS with same message)
- **No** → Just push to origin as normal

## ⚙️ Git Staging Rules

### Critical Staging Protocol
- **DO NOT attempt to commit unless the user explicitly tells you to**
- **NEVER use `git add -A` or `git add .` without explicit permission**
- Always review changes before staging
- Stage specific files intentionally
- Verify what you're committing with `git status` and `git diff`

### Safe Staging Pattern
```bash
# Review what changed
git status
git diff

# Stage specific files only
git add path/to/file1.py path/to/file2.py

# Verify staged changes
git diff --cached
```

## 📝 Git Commit Format

### CRITICAL: Syntax Rules
**Use literal newlines in quotes, NEVER HEREDOC**

```bash
# ✅ CORRECT - Use literal newlines
git commit -m "prefix: summary

CONTEXT:
What triggered this work"

# ❌ WRONG - NEVER use HEREDOC (causes shell EOF errors)
git commit -m "$(cat <<'EOF'
Message here
EOF
)"
```

### Commit Template

```bash
git commit -m "prefix: summary (50 chars max)

CONTEXT:
[What situation triggered this work - symptom, user report, or need]

INSIGHT: (optional - skip if obvious)
[The key realization: root cause for bugs, design decision for features]

APPROACH:
[Why this solution over alternatives, trade-offs considered]

CHANGES:
- Specific modifications with file names

IMPACT: (only when notable - skip if none)
- Breaking/Security/Performance notes

PRESERVES: (for refactors only)
- What behavior is unchanged

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Section Guide

| Section | Required? | When to Use |
|---------|-----------|-------------|
| CONTEXT | Always | The trigger - what situation led to this commit |
| INSIGHT | Optional | The "aha" moment - root cause for bugs, key design decision for features. **Skip if obvious.** |
| APPROACH | Always | Why this solution, what alternatives considered |
| CHANGES | Always | Specific file/method modifications |
| IMPACT | Optional | Only when there's actual impact (breaking, security, perf metrics) |
| PRESERVES | Refactors | What existing behavior remains unchanged |

### Semantic Prefixes

- `feat:` - New feature or functionality
- `fix:` - Bug fix or error correction
- `refactor:` - Code restructuring without functional changes
- `perf:` - Performance improvements
- `security:` - Security-related changes
- `test:` - Adding or modifying tests
- `docs:` - Documentation updates
- `chore:` - Maintenance tasks, dependency updates
- `style:` - Code formatting, whitespace fixes
- `revert:` - Reverting previous commits

**Remember**: Commit messages are permanent documentation. Write for developers searching git history months from now.

## 📊 Post-Commit Summary (Required)

After **every commit**, provide a detailed summary:

```
✅ Commit Successfully Created

Commit Hash: abc123def
Files Changed: 3 files (+45, -12)

Key Accomplishments:
- [Specific achievement 1]
- [Specific achievement 2]
- [Specific achievement 3]

Benefits:
- [How this improves the codebase]
- [What problems this solves]

Next Steps:
- [What the human should consider next]
- [Any follow-up work needed]
```

## 🚫 Critical Anti-Patterns

### Git Commit HEREDOC (Recurring Issue)

This is a **persistent mistake** that causes shell EOF errors:

```bash
# ❌ NEVER DO THIS
git commit -m "$(cat <<'EOF'
Message here
EOF
)"

# ✅ ALWAYS DO THIS
git commit -m "Summary

Details with literal newlines"
```

**Why this matters**: HEREDOC syntax in git commits causes shell parsing errors and breaks the commit flow. Always use literal newlines within quotes.

## 🔍 Example Commits

### Bug Fix (with INSIGHT)
```bash
git commit -m "fix: preload Vault secrets at startup

CONTEXT:
Users reported Gemini/OpenRouter failing while Anthropic worked. After ~1hr
uptime, requests for uncached secrets returned 403 Forbidden.

INSIGHT:
AppRole token has 1-hour TTL. Secrets cached on first access work forever.
Keys first accessed after expiry trigger calls with dead token - Anthropic
was cached early, OpenRouter wasn't.

APPROACH:
Preload ALL secrets at startup while token is fresh. Security-equivalent
since secrets end up in memory anyway. Simpler than token refresh, no race
conditions, no failure modes.

CHANGES:
- Added preload_secrets() to vault_client.py
- Called in main.py lifespan startup

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Simple Feature (no INSIGHT needed)
```bash
git commit -m "feat: add root endpoint with service status

CONTEXT:
User curling localhost:1993 during install got 404, thought install failed.

APPROACH:
Informational endpoint confirming service is running with pointers to
/v0/api/chat and /v0/api/health. No auth - just service discovery.

CHANGES:
- Added GET / endpoint in create_app()

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Refactor (with PRESERVES)
```bash
git commit -m "refactor: split monolithic deploy.sh into modules

CONTEXT:
deploy.sh grew to 2,416 lines / 17 steps - cognitive overload, merge conflicts,
impossible to debug individual steps.

APPROACH:
Library files (shared functions) + step scripts. Used 'source' for variable
flow without temp files. ~8 logical groups over 1:1 mapping to reduce file
count while keeping clear boundaries.

CHANGES:
- Created deploy/deploy.sh thin orchestrator (~80 lines)
- Created deploy/lib/{output,services,vault}.sh
- Created step scripts: config, preflight, dependencies, python, etc.

PRESERVES:
- All 17 deployment steps execute identically
- Same interactive prompts and variable flow

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Performance (with IMPACT metrics)
```bash
git commit -m "perf: add parallel tool execution to generic provider

CONTEXT:
Generic provider executed tools sequentially - 2 tools x 1s = 2s+ total.

INSIGHT:
ThreadPoolExecutor pattern from Anthropic path directly applicable. Critical:
context propagation via invoke_with_context for RLS security.

APPROACH:
Emit all ToolExecutingEvent upfront, then concurrent execution with
as_completed(). Preserves circuit breaker recording for both paths.

CHANGES:
- Replace sequential loop with ThreadPoolExecutor (lines 697-750)
- Add invoke_with_context wrapper

IMPACT:
- 27% faster total (4.58s -> 3.36s for 2 one-second tools)

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 💡 Best Practices

1. **Before Committing**:
   - Run `git status` to see what changed
   - Run `git diff` to review actual changes
   - Stage files intentionally with specific paths
   - Run `git diff --cached` to verify staged changes

2. **Writing Messages**:
   - Start with semantic prefix
   - Keep summary under 50 characters
   - CONTEXT: the trigger, not the solution
   - INSIGHT: only when there's a non-obvious discovery (skip for simple features)
   - APPROACH: explain trade-offs, why this over alternatives
   - CHANGES: specific file/method names

3. **After Committing**:
   - Always provide post-commit summary
   - Include commit hash and file stats
   - Highlight key accomplishments
   - Note any follow-up work needed

4. **For Complex Bug Fixes**:
   - INSIGHT is critical - trace the causal chain to actual origin
   - Explain why obvious solutions don't work in APPROACH
   - Think of future developers searching git history

## 🎓 When to Use This Skill

Invoke this skill when:
- Creating any git commit
- User asks about commit message format
- Need guidance on staging files
- Uncertain about semantic prefix to use
