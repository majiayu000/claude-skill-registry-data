---
name: codex
description: >-
  This skill should be used when the user asks to "run codex", "ask GPT", "GPT
  review", "codex review", "codex exec", or needs GPT insights for complex
  tasks, code analysis, refactoring, automated editing, or code review. Also
  trigger on "second opinion", "codex resume", or when facing complex problems
  that benefit from an external AI perspective.
---
# Codex Skill Guide

Use Codex proactively for complex architectural decisions, deep code analysis, refactoring, security/performance audits, code reviews before commits/PRs, when stuck after 2+ failed attempts, or when the user explicitly requests GPT/Codex assistance.

## Models

| Role | Model |
| --- | --- |
| Primary | `gpt-5.4` |
| Fallback | `gpt-5.3-codex` |

Default to `gpt-5.4`. Fall back to `gpt-5.3-codex` if the user requests it or if `gpt-5.4` fails.

---

## Running `codex exec`

1. Ask the user (via `AskUserQuestion`) which model (`gpt-5.4` or `gpt-5.3-codex`) AND which reasoning effort (`xhigh`, `high`, `medium`, or `low`) in a **single prompt**. Default suggestion: `gpt-5.4` + `high`.

2. **Always use `-s read-only`** — codex is primarily a validator/analyzer. Only escalate sandbox if the user explicitly asks codex to edit files or needs network access:
   - User asks to edit/refactor → `-s workspace-write --full-auto` (confirm via `AskUserQuestion` first)
   - User needs network → `-s danger-full-access --full-auto` (confirm via `AskUserQuestion` first)

3. Assemble the command:
   - `-m <MODEL>` — model selection
   - `-c model_reasoning_effort="<effort>"` — reasoning effort
   - `-s read-only` — default sandbox (see step 2 for exceptions)
   - `-o /tmp/codex-last.txt` — always capture full response
   - `-C <DIR>` — working directory
   - `--skip-git-repo-check` — always include

4. Append `2>/dev/null` to suppress thinking tokens (stderr). Only show stderr if debugging.

5. Run the command, then read `/tmp/codex-last.txt` with the Read tool to get the full response (Bash output may truncate). Summarize for the user.

6. After completion: "You can resume this session at any time by saying 'codex resume'."

### Quick Reference - exec

| Use case | Command |
| --- | --- |
| Analysis/validation (default) | `codex exec --skip-git-repo-check -m MODEL -s read-only -o /tmp/codex-last.txt "prompt" 2>/dev/null` |
| Apply local edits | `codex exec --skip-git-repo-check -m MODEL -s workspace-write --full-auto -o /tmp/codex-last.txt "prompt" 2>/dev/null` |
| Network/broad access | `codex exec --skip-git-repo-check -m MODEL -s danger-full-access --full-auto -o /tmp/codex-last.txt "prompt" 2>/dev/null` |
| Different directory | `codex exec --skip-git-repo-check -C <DIR> -m MODEL -s read-only -o /tmp/codex-last.txt "prompt" 2>/dev/null` |

---

## Resuming Sessions

`resume` works both as top-level command and as `exec` subcommand:

| Mode | Command |
| --- | --- |
| Interactive resume (picker) | `codex resume` |
| Interactive resume (last) | `codex resume --last` |
| Non-interactive resume | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` |

- Don't use config flags on resume unless explicitly requested.
- For `codex exec resume`, flags go between `exec` and `resume`.

---

## Running `codex review`

No need to ask for model/reasoning — review uses sensible defaults.

1. Ask the user (via `AskUserQuestion`) what to review:
   - **Uncommitted changes** — all local modifications
   - **Against a branch** — compare to base branch (e.g., `main`)
   - **Specific commit** — review a commit SHA

2. Optionally ask for custom review focus (security, performance, conventions, etc.)

3. Run the appropriate command and summarize findings.

### Quick Reference - review

| Use case | Command |
| --- | --- |
| Uncommitted changes | `codex review --uncommitted` |
| Against main branch | `codex review --base main` |
| Against specific branch | `codex review --base feature/xyz` |
| Specific commit | `codex review --commit abc123` |
| Commit with title context | `codex review --commit abc123 --title "Add user auth"` |
| With custom focus | `codex review --uncommitted "Focus on security"` |

**Note**: `--title` requires `--commit` (not `--base`).

### Configuration Overrides

```bash
codex review --uncommitted -c model="gpt-5.3-codex"
```

---

## Decision Guide: exec vs review

| Situation | Use |
| --- | --- |
| "Review my changes" | `codex review --uncommitted` |
| "Review this PR" | `codex review --base main` |
| "Analyze this architecture" | `codex exec` |
| "Help me debug this" | `codex exec` |
| "Refactor this code" | `codex exec` with workspace-write |
| "Is this secure?" | `codex review` for diffs, `codex exec` for deep analysis |

---

## Following Up

- After every command, use `AskUserQuestion` to confirm next steps
- For `exec`: offer to resume with `codex resume --last`
- For `review`: offer to help address specific findings

## Error Handling

- Stop and report failures on non-zero exit; request direction before retrying
- Summarize warnings or partial results and ask how to adjust
