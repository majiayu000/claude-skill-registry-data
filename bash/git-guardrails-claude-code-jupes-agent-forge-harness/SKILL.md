---
name: git-guardrails-claude-code
description: Set up Claude Code git safety guardrails that block dangerous git commands before execution. Use when the user asks to prevent git push, hard reset, git clean, destructive checkout/restore, or branch deletion from Claude Code hooks.
---

# git-guardrails-claude-code

Guide a user through installing a Claude Code `PreToolUse` hook that blocks dangerous git commands before they execute.

This Agent Forge port is guidance-first: do not install hooks, edit `.claude/settings.json`, edit `~/.claude/settings.json`, or create executable hook files unless the user explicitly asks for installation in the current task.

## What gets blocked

The reference hook blocks commands matching these patterns:

- `git push`, including force-push variants
- `git reset --hard`
- `git clean -f` and `git clean -fd`
- `git branch -D`
- `git checkout .`
- `git restore .`
- Short forms that still contain `push --force` or `reset --hard`

When a command is blocked, the hook exits with code `2` and prints a message explaining which dangerous pattern matched.

## Workflow

### 1. Confirm scope

Ask the user where they want the guardrail installed:

- **Project only**: `.claude/settings.json` with the hook script under `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/settings.json` with the hook script under `~/.claude/hooks/block-dangerous-git.sh`

If the user only asks for advice or review, provide the guidance and stop before editing files.

### 2. Review the reference hook

Use the bundled reference as the source for the script content:

[references/block-dangerous-git.sh.md](references/block-dangerous-git.sh.md)

Keep it as documentation unless installation is explicitly requested. If installing, copy the shell script content from the reference into the selected hook path and make that copied file executable.

```bash
chmod +x .claude/hooks/block-dangerous-git.sh
```

For global installs, use the global hook path instead:

```bash
chmod +x ~/.claude/hooks/block-dangerous-git.sh
```

### 3. Merge hook settings

Add a `PreToolUse` hook for the Bash tool. If the settings file already exists, merge into the existing JSON and preserve all unrelated settings and hooks.

Project-scoped hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

Global hook:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

Do not replace an existing `hooks.PreToolUse` array. Append the new command hook only if an equivalent command is not already present.

### 4. Customize intentionally

Ask whether the user wants to add or remove blocked patterns before installation. Keep the defaults unless the user chooses a different policy.

Common customizations:

- Allow ordinary `git push` but keep blocking `git push --force`.
- Add `git checkout -- .` or repo-specific destructive commands.
- Add explanatory text that matches the team's git policy.

Document any customization in the response so future agents understand the local policy.

### 5. Verify with sample JSON

Test the installed or candidate script by piping Claude Code hook JSON into it:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | .claude/hooks/block-dangerous-git.sh
```

Expected result:

- Exit code: `2`
- Stderr includes `BLOCKED`
- Message includes the matched pattern, such as `git push`

Also test an allowed command:

```bash
echo '{"tool_input":{"command":"git status --short"}}' | .claude/hooks/block-dangerous-git.sh
```

Expected result:

- Exit code: `0`
- No block message

## Agent Forge safety notes

- Preserve non-interactive shell behavior; never run commands that wait for input.
- Do not run a real dangerous git command to test the hook.
- Do not install this hook as part of a porting or documentation task.
- Do not overwrite settings files. Parse and merge JSON when installation is requested.
- Keep project-specific installs in the target project, not in this harness, unless the user explicitly chooses this repository as the target.

