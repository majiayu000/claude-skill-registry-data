---
name: evi-secret-guard
description: Use when secret files and destructive commands must be refused mechanically, before the model can be talked into them — a PreToolUse deny layer.
---

# Secret guard

A `PreToolUse` hook that denies any tool call touching secrets (`.env`,
`.credentials/`) or running a destructive command (`rm -rf` on root/home/wildcard,
`git push --force`, `git reset --hard origin`). It does not ask the model — a
model under adversarial prompting or context pressure can be convinced to read a
secret; a hook cannot be convinced of anything.

## What it guarantees

Secret files cannot be read or written, and a small set of irreversible commands
cannot run, regardless of what the conversation talked the model into. The
decision is made before the tool executes. `.env.example` is explicitly allowed
(it is a template, not a secret).

## How it works

The hook reads the tool call from stdin and pattern-matches:

- **Bash**: the command string is checked against deny regexes (`.env` access,
  `.credentials/`, `rm -rf` on root/home/`/*`, force-push, hard-reset-to-origin).
  `.env.example` is neutralized before matching so it is never caught.
- **Write / Edit / Read**: the `file_path` is checked for `/.env` (not
  `.env.example`) and `/.credentials/`.

On a match it returns
`{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":...}}`;
otherwise `allow`.

## Implement in your project

Reference implementation: [`../../scripts/hooks/pre-tool-guard.sh`](../../scripts/hooks/pre-tool-guard.sh)

Wire it on `PreToolUse` (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"PreToolUse": [
  {
    "matcher": "",
    "hooks": [
      { "type": "command", "command": "bash $CLAUDE_PROJECT_DIR/scripts/hooks/pre-tool-guard.sh" }
    ]
  }
]
```

No environment variables required.

## Adaptation points

- **More secret paths:** add entries to `DENY_BASH` and the Write/Edit/Read
  checks (e.g. `id_rsa`, `*.pem`, a cloud-credentials dir).
- **Stricter destructive set:** add patterns (e.g. `dropdb`, `kubectl delete`,
  `terraform destroy`) following the existing `(regex, reason)` shape.
- **Allowlist exceptions:** the `.env.example` neutralization shows the pattern
  for carving out a safe lookalike; replicate it for any template path.

## Verify

1. `bash -n scripts/hooks/pre-tool-guard.sh` exits 0.
2. `echo '{"tool_name":"Bash","tool_input":{"command":"cat .env"}}' | bash scripts/hooks/pre-tool-guard.sh`
   returns `"permissionDecision":"deny"`.
3. `echo '{"tool_name":"Bash","tool_input":{"command":"cat .env.example"}}' | bash scripts/hooks/pre-tool-guard.sh`
   returns `"permissionDecision":"allow"`.

## Rollback

Remove the `PreToolUse` entry from `.claude/settings.json`.
