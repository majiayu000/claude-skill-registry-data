---
name: switch
description: Move this conversation to another Claude account (the previous one, or one by name), or set up, add, remove, rename and list accounts.
argument-hint: "[account name] | setup [name] | add <name> | remove <name> [--delete-dir] | rename <old> <new> | list | theme <name> [theme]"
disable-model-invocation: true
allowed-tools:
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" request:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" setup:*)
  - Bash(python "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" setup:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" add:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" remove:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" rename:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" list:*)
  - Bash("${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" theme:*)
---

Pick the branch by the first word of `$ARGUMENTS` and run only its commands with the Bash tool, exactly as written, no text before the first one.

**`setup [name]`** (first-time setup; `name` is the account you're on, default `main`): two steps, never one.

1. Show the changes, then ask "Write these changes? (yes/no)" and stop until the user answers:

   ```
   "${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --dry-run
   ```

   If it says Python was not found or `python3: command not found` (on Windows `python3` is often a Microsoft Store stub), run this instead, and use `python` in step 2 too:

   ```
   python "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --dry-run
   ```

   `everything is up to date` or a refusal (a bad name, a name or dir already taken) ends it here: show the output as is.
2. Only on the user's explicit yes in their next message, run the same command with `--yes` in place of `--dry-run`:

   ```
   "${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --yes
   ```

   Then tell the user: open a new terminal and start Claude with `claude` (or `claude-<name>`); `/switch` works in sessions started that way. Anything but yes: say nothing was changed and stop.

**`add <name> [--dir DIR]`**:

```
"${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --session "${CLAUDE_SESSION_ID}"
```

Show its output as is. `switching to '<name>'` means the launcher ends this session and reopens it on the new account, which asks for a login; add nothing.

**`rename <old> <new>`**, **`list`** or **`theme <name> [theme]`**:

```
"${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS
```

Show its output as is.

**`remove <name> [--delete-dir]`**: two steps, never one.

1. Show the plan, then ask "Remove as above? (yes/no)" and stop until the user answers:

   ```
   "${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --dry-run
   ```

   A refusal (the account you're on, the last or first account, an overlapping dir) ends it here.
2. Only on the user's explicit yes in their next message:

   ```
   "${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" $ARGUMENTS --yes
   ```

   Anything but yes: say nothing was changed and stop.

**Anything else** (empty or an account name): run this and show its output as is.

```
"${CLAUDE_SWITCH_PYTHON:-python3}" "${CLAUDE_SKILL_DIR}/scripts/claude_switch.py" request $ARGUMENTS --session "${CLAUDE_SESSION_ID}"
```

- Ends with `switching to '<name>'` → the launcher ends this session and resumes it on that account. Add nothing.
- Anything else (unknown name with the account list, already on that account, not started by the launcher with setup steps, python not found) → nothing was switched; show the output as is. Python not found means the session wasn't started by the launcher: suggest `/switch setup`.
