---
name: dcg
description: Destructive Command Guard. Installs a pre-tool-use hook that blocks unrecoverable shell commands (rm -rf /, git reset --hard, git clean -fd, rm of .env / credentials, force-pushing to main, fork bombs, shred / dd, etc.) before the agent executes them. Use when the user says "install dcg", "destructive command guard", "guard rails for destructive commands", or invokes /dcg.
---

# DCG — Destructive Command Guard

A pre-tool-use hook that intercepts every shell command the agent is about to run. If the command matches a known destructive pattern, the hook returns a non-zero exit and a `stopReason` payload, blocking execution.

## What it blocks

- `rm -rf /` — at root
- `sudo ... rm -rf /` — same with sudo
- `git reset --hard` — irreversible discard of local work
- `git clean -fd` — force-delete untracked files (commonly nukes `.env`, generated configs)
- `git push --force` to `main` / `master` — overwriting upstream history on protected branches
- `rm` of `.env` / credentials / `.pem` / SSH keys
- `shred` / `dd` — disk destruction
- `:(){ :|:& };:` — fork bomb
- `chmod 777` on `$HOME` — permission disaster
- `find $HOME -delete` — bulk deletion in home

The full pattern list is in `hooks/dcg.sh`. New patterns can be added by appending to the `patterns` array.

## What it does NOT block

By design DCG is a *floor*, not a *ceiling*:

- `rm -rf <project>/build` — project-local cleanup is allowed
- `git reset HEAD~1` — non-`--hard` resets are recoverable
- `rm .DS_Store` — junk-file removal is allowed
- Anything outside the agent's shell tool

This is intentional. Over-blocking causes alert fatigue; agents start either circumventing or losing trust. DCG focuses on the truly unrecoverable cases.

## How install wires it up

`jutsu install dcg` registers a `pre-tool-use` hook with matcher `Bash` for every active agent:

| Agent | Settings file | Native event |
|---|---|---|
| Claude Code | `~/.claude/settings.json` | `PreToolUse` |
| OpenAI Codex CLI | `~/.codex/config.toml` | `PreToolUse` |
| Google Gemini CLI | `~/.gemini/settings.json` | `BeforeTool` |

Each entry is tagged with `_kaijutsu: skill:dcg:hook:block-destructive-shell` so `jutsu remove dcg` can clean up exactly what we added without disturbing user-authored hooks.

The script at `hooks/dcg.sh` is platform-agnostic POSIX bash — it reads the hook JSON from stdin, extracts the `command` field via `jq` (with a regex fallback if `jq` is absent), and matches against the pattern list.

## How agents experience a block

When DCG fires:

```json
{
  "continue": false,
  "stopReason": "dcg blocked: rm -rf /",
  "matched_command": "rm -rf /"
}
```

Plus a non-zero exit. Each agent's hook framework propagates this differently:

- **Claude Code**: surfaces `stopReason` to the model so the assistant knows why and can react (apologize, propose a safer alternative).
- **Codex**: returns the `"blocked"` status to the model.
- **Gemini**: similar — the `BeforeTool` interception aborts the call.

In every case the destructive shell never runs.

## Customization

Edit `hooks/dcg.sh` to add or remove patterns:

```bash
patterns+=(
  "rm of database backups:rm.*\\.sql\\.bak"
)
```

The format is `"<label>:<regex>"`. The script `grep -E`s each regex against the proposed command.

## Testing locally

After install, in any project where DCG is registered:

```sh
# In any agent session, ask:
> please run `rm -rf /tmp/foo`

# DCG should let it through (limited to /tmp/foo, not /).

> please run `rm -rf /`

# DCG should block. The agent will report "dcg blocked: rm -rf /".
```

## Hard rules

- **Never bypass DCG by editing settings.json directly while an agent is running.** Restart the agent after disabling.
- **DCG is not a security boundary against malicious skills**. A malicious skill could ship its own hooks that disable DCG. Treat DCG as a guardrail against agent mistakes, not against adversaries with skill-install access.
- **The hook script timeout is 5 seconds**. If `jq` is slow or stdin is malformed, the hook exits and the action proceeds (fail-open). v0.4 may switch to fail-closed.
- **DCG patterns are not exhaustive**. Use it alongside, not instead of, repository-level safeguards (commit signing, branch protection, CI checks).

## v0 limitations

- Patterns only match shell strings — agents that use direct file-edit tools (Claude's Edit tool, Codex's apply_patch) bypass DCG. Future v0.4: extend matchers to `Edit` / `Write` tools with sensitive-path patterns (`.env`, `credentials`, `id_rsa`).
- No per-project pattern overrides yet. v0.4 will read `<project>/.kaijutsu/dcg-patterns.txt` as an addendum.
- jq dependency is best-effort. If `jq` isn't installed, the script greps over the full JSON payload — works but slightly less precise.
