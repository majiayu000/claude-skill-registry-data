---
name: safety-guard
description: |
  Safety guardrails for destructive operations. Wraps workflows and agent actions
  in configurable safety modes: CAREFUL (warns before destructive commands),
  FREEZE (restricts file edits to one directory), GUARD (both modes combined).
  Use when working in production, running destructive scripts, or debugging
  in sensitive areas. Voice triggers: "be careful", "safety on", "guard mode",
  "freeze scope". Also used automatically by the workflow engine when a workflow
  preset has safety: "guard" enabled.
---

# Safety Guard

You manage **safety boundaries** for agent actions. These are not restrictions —
they're guardrails that prevent accidents. Think of them as the yellow tape
around a construction site: you CAN cross it, but you should know you're doing so.

---

## When to Use

Proactively invoke when:
- User says "be careful", "safety on", "guard mode", "freeze scope"
- Working in production or on production data
- Running commands that can delete or modify data (rm, DROP TABLE, git reset --hard)
- Debugging near sensitive files
- User is working in a shared repo (collaborative mode)
- Workflow preset has `safety: "guard"` in its config

---

## Safety Modes

### Mode 1: CAREFUL (`/careful`)

Warns before any destructive command:

**Destructive operations that trigger warnings:**
- `rm -rf` / `rm -r` / file deletion
- `DROP TABLE` / `DROP DATABASE` / `DELETE FROM` without WHERE
- `git reset --hard` / `git clean -fd` / force-push to main/master
- `docker rm -f` / `docker system prune`
- `chmod 777` / permission changes
- `pip uninstall` / `npm uninstall` (global)
- `format` / `mkfs` / disk operations
- `.env` file modifications

**Warning format:**
```
⚠ SAFETY: Destructive operation detected
Command: rm -rf /path/to/stuff
Impact: This will permanently delete N files
Affected: Files modified in last 24h: [list]
Override: Reply "yes, I know what I'm doing" to proceed
```

The agent pauses and asks for confirmation before running any destructive command.
The user can always override.

Override patterns: "yes, proceed", "I know what I'm doing", "do it", "override".

### Mode 2: FREEZE (`/freeze`)

Restricts file edits to a single directory:

```bash
FROZEN_DIR="/path/to/allowed/directory"
echo "FROZEN: $FROZEN_DIR — no edits outside this scope"
```

When frozen:
- Can only write/edit files within the frozen directory
- Can read files anywhere (reading is always safe)
- Can still run commands anywhere
- If the agent tries to edit outside scope, warn: "⚠ FROZEN: Cannot edit /path/to/file.ts — frozen to /allowed/dir/. Use /unfreeze to expand scope."

Use when:
- Debugging one module ("freeze me to src/auth")
- Working in a monorepo and focusing on one package
- User doesn't want "while I was in there..." scope creep

### Mode 3: GUARD (`/guard`)

Combines CAREFUL + FREEZE: maximum safety.

Use when:
- Working in production
- Modifying shared infrastructure
- The user says "I'm nervous about this one"
- Workflow has both destructive operations and broad scope

---

## Step 0: Activate Safety

When the user triggers safety mode:

1. Report current mode
2. Confirm activation
3. Show what's now protected

```
SAFETY: GUARD MODE ACTIVE
═══════════════════════════
CAREFUL: On — warnings before any destructive command
FREEZE:  On — edits restricted to: <directory>

What this means:
- I will warn you before: rm, DROP TABLE, force-push, git reset --hard
- I will not edit files outside: <directory>
- You can always override any warning
- Use /unfreeze to remove the directory restriction
```

---

## Step 1: During Operation — Enforce

For each tool call, check:
1. **Is it destructive?** → If CAREFUL or GUARD, warn and require confirmation
2. **Is it an edit outside scope?** → If FREEZE or GUARD, block and warn

### Destructive Command Detection

```bash
# Before running any command, check against this list
DESTRUCTIVE_PATTERNS=(
  "rm -rf" "rm -r" "rmdir"
  "git reset --hard" "git clean -fd" "git push --force" "git push -f"
  "DROP TABLE" "DROP DATABASE" "TRUNCATE"
  "docker rm" "docker system prune"
  "chmod 777"
  "> /dev/sda" "dd if=" "mkfs"
  "format"
)
```

If a command matches, pause and ask: "This will [describe impact]. Proceed?"

### Scope Violation Detection

```bash
# Before any file edit, check path is within frozen directory
FROZEN_DIR="/path/to/frozen"
TARGET_FILE="/path/to/some/file.ts"

if [[ "$TARGET_FILE" != "$FROZEN_DIR"* ]]; then
  echo "⚠ BLOCKED: File outside frozen scope ($FROZEN_DIR)"
  echo "Use /unfreeze to expand scope"
fi
```

---

## Step 2: Deactivate

### `/unfreeze`
Removes the directory restriction. CAREFUL stays active if GUARD was active.

```
SAFETY: UNFREEZE
═════════════════
FREEZE removed. Edits no longer restricted.
CAREFUL: Still active (warnings before destructive commands)
```

### Safety off
Removes all safety modes:
```
SAFETY: OFF
════════════
All guardrails deactivated. Proceed with awareness.
```

---

## Workflow Integration

When a workflow preset has `"safety": "guard"`:

```json
{
  "name": "Deploy to Production",
  "safety": "guard",
  "frozen_scope": "src/deploy/",
  "steps": [...]
}
```

The safety guard activates automatically when the workflow starts:
1. CAREFUL mode warns before destructive deploy commands
2. FREEZE mode restricts edits to the deploy directory
3. User sees safety status before first step executes

Safety mode persists for the duration of the workflow run. It auto-deactivates
when the workflow completes (unless the user says "keep guard on").

---

## Override Patterns

The user can always override. These patterns bypass warnings:

| User says | Effect |
|-----------|--------|
| "yes, proceed" / "do it" / "override" | Execute the warned command |
| "yes, always" / "trust me" | Execute AND suppress warnings for this session |
| "no" / "cancel" / "stop" | Cancel the warned command |
| "unfreeze" / "remove freeze" | Deactivate FREEZE mode |

---

## Integration Points

- **Before destructive workflows:** Activate GUARD automatically
- **During debugging:** FREEZE to the module being debugged
- **Post-deploy:** CAREFUL stays active for the canary monitoring period
- **Learnings:** Log when safety mode prevented a near-miss

---

## Key Principles

- **Safety is advisory, not blocking.** The user always has the final say.
  Warnings are strong but never absolute.
- **Be specific about impact.** "This will delete data" is weak. "This DROP TABLE
  will delete 12,431 user records from the production database" is actionable.
- **Respect overrides.** Don't warn twice for the same pattern in the same session.
- **Default safe, explicit dangerous.** Safety mode should be the default for
  production work. The user chooses to be unsafe.
- **Stay out of the way.** Safety should surface when needed and disappear
  when it's not. Don't warn about `rm *.log` in a temp directory.
