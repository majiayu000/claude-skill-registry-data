---
name: git-guardrails-claude-code
description: Set up Claude Code hooks to block dangerous git commands (force-push, direct push to protected branches, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
---

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks a fixed list of destructive git commands before Claude executes them.

Source: adapted from [mattpocock/skills — misc/git-guardrails-claude-code](https://github.com/mattpocock/skills/blob/main/skills/misc/git-guardrails-claude-code/SKILL.md), imported 2026-08-26. Upstream blocks **every** invocation of `git push`, including plain feature-branch pushes. This adaptation narrows that to force-push and direct pushes to protected branches only, because `system-level/core.md`'s git workflow requires routine feature-branch pushes for the standard worktree → branch → push → PR flow — blocking all pushes would make this repo's own workflow unusable. The rest of upstream's blocked-command list (reset --hard, clean -f/-fd, branch -D, bare checkout/restore) is unchanged.

## What Gets Blocked

- `git push` with `--force` / `--force-with-lease` / `-f`
- `git push` directly to `main`, `master`, or `staging`
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .` (bare, discards uncommitted changes)

Routine `git push origin <feature-branch>` is **not** blocked.

When blocked, Claude sees a message telling it that it does not have authority to run the command.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file, merging into any existing `hooks.PreToolUse` array — don't overwrite other settings:

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

(Project scope: use `"\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"` instead.)

### 4. Ask about customization

Ask if the user wants to add or remove any protected branch names or command rules. Edit the copied script's `PROTECTED_BRANCHES` array for branch names and `is_dangerous_git_command` for command rules.

### 5. Verify

The hook tokenizes each shell command segment, recognizes `git` and absolute paths to the Git executable, consumes Git global options, and then checks the subcommand arguments. This avoids matching quoted prose that merely mentions Git operations. Test both directions before trusting the hook in a new environment:

```bash
# Should exit 2 (BLOCKED) — real dangerous commands, one per pipe-test:
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
echo '{"tool_input":{"command":"git -C /tmp/example reset --hard origin/main"}}' | <path-to-script>

# Should exit 0 (allowed) — routine push and prose that merely mentions these words:
echo '{"tool_input":{"command":"git push origin feature/my-branch"}}' | <path-to-script>
echo '{"tool_input":{"command":"gh issue create --body \"discusses git push and main\""}}' | <path-to-script>
```

Then prove it fires live in-session: run a real (but harmless-context) `git push --force` or similar in the Bash tool and confirm the hook intercepts it with a `PreToolUse:Bash hook error`, per this repo's own `update-config`-style hook-construction discipline (pipe-test → `jq -e` schema check → live fire proof).
