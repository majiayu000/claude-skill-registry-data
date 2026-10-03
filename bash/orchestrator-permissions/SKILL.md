---
name: orchestrator-permissions
description: Documentation of allowed Bash commands, blocked constructs, and reliable patterns for the orchestrator workflow permission model.
user-invocable: false
---

# Orchestrator Permission Model

## Allowed commands

The orchestrator workflow only permits these Bash command prefixes:

| Prefix | Examples |
|--------|----------|
| `gh *` | `gh api ...`, `gh issue list ...`, `gh pr view ...` |
| `git *` | `git add`, `git commit`, `git push`, `git branch` |
| `jq *` | `jq '.field' file.json`, `jq -n --arg ...` |
| `mkdir *` | `mkdir -p docs/worklog/2026-02-25` |
| `ls *` | `ls tools/`, `ls -la file` |
| `date *` | `date -u '+%Y-%m-%d'` |
| `wc *` | `wc -l file` |
| `sort *` | `sort file` |
| `composer *` | `composer run test-unit` |
| `cargo *` | `cargo build --release --manifest-path tools/rust/Cargo.toml` |
| `bash *` | `bash tools/check-field-inventory-rs` |

WebFetch is allowed for `schema.org`, `developers.google.com`, `search.google.com` domains only.

## BLOCKED constructs (will cause denial and waste turns)

These shell constructs are **always blocked** by the prefix-based permission system, regardless of which commands they contain:

| Construct | Example | Why blocked |
|-----------|---------|-------------|
| `${}` substitution | `git commit -m "${VAR}"` | Sandbox blocks parameter substitution |
| Pipes | `gh api ... \| jq ...` | Prefix match only covers first command |
| Compound `&&` / `||` | `git commit -m "msg" && git push` | Not a single command |
| Heredocs `<<` | `gh api --input - <<'JSON'` | Shell construct, not a simple command |
| Command substitution `$()` | `git commit -m "$(cat ...)"` | Subprocess invocation |
| For loops | `for f in *.php; do ...; done` | Shell scripting |
| Process substitution `<()` | `gh api --input <(jq ...)` | Requires bash subprocess |
| Redirects `>` `>>` | `jq ... > file.json` | Output redirection blocked |
| Semicolons | `git add .; git commit` | Multiple commands |

### Key rule
**Each Bash tool call must be a single, simple command with no shell constructs.** If you need compound operations, use separate Bash tool calls.

## NOT allowed commands (will require user approval)

- ~~`bash`, `sh`~~ — `bash` is now ALLOWED (for invoking Rust tool wrappers). `sh` remains blocked.
- `echo`, `printf` — cannot produce text output
- `cat`, `head`, `tail` — cannot read files (use Read tool instead)
- `grep`, `rg` — cannot search (use Grep tool instead)
- `chmod` — cannot change permissions
- `env`, `printenv` — cannot inspect environment
- `curl`, `wget` — cannot make HTTP requests (use `gh api` or WebFetch)
- Any other command not in the allow list

## Reliable patterns for common operations

### Posting comments on issues

Use `gh api` with `-f body="..."` — plain text only, NO `${}` variables:

```bash
gh api "repos/EvaLok/schema-org-json-ld/issues/NUMBER/comments" -X POST -f body="Comment text here. No dollar-brace variables."
```

For multi-line or complex comments, write the body to a file first with the **Write** tool, then use `-F body=@file`:

```bash
gh api "repos/EvaLok/schema-org-json-ld/issues/NUMBER/comments" -X POST -F body=@/path/to/comment.md
```

**Never use**: `${}`, heredocs, process substitution, or pipe chains in comment commands.

### Creating issues

Write the JSON payload to a file with the **Write** tool, then use `--input`:

```bash
gh api "repos/EvaLok/schema-org-json-ld/issues" --method POST --input /path/to/issue.json
```

The JSON file should contain `title`, `body`, `labels`, `assignees`, and optionally `agent_assignment`.

### Git commit and push

Always use separate commands (not `&&`). Use simple single-line messages:

```bash
git add docs/state.json docs/worklog/
```
```bash
git commit -m "Cycle 35: description of changes"
```
```bash
git push
```

**Never use**: `$(cat <<'EOF'...)` for multi-line commit messages. If you need a multi-line message, use `-m "line 1" -m "line 2"` (multiple `-m` flags).

### Closing issues

```bash
gh api "repos/EvaLok/schema-org-json-ld/issues/NUMBER" -X PATCH -f state=closed
```

### Searching code / files

**Never use** `grep`, `find`, pipes, or `for` loops. Instead:

- **Find files**: Use the `Glob` tool with patterns like `src/**/*.php`
- **Search content**: Use the `Grep` tool with regex patterns
- **Read files**: Use the `Read` tool
- **Count items**: Use `wc -l filename` on a single file, or use the `Grep` tool with `output_mode: "count"`

### Creating directories

The `mkdir` command is on the allowed list but may be blocked by an additional sandbox security layer. If `mkdir` fails with a "may only create directories in allowed working directories" error, use the **Write** tool instead — it creates parent directories automatically when writing a file.

### Getting timestamps

```bash
date -u '+%Y-%m-%d %H:%M:%S UTC'
```

### Reading environment variables

Environment variables cannot be accessed directly (no `${}`, no `env`, no `printenv`). Use `date` for timestamps and `git` for repo info. The GitHub run ID should be captured at workflow level if needed.
