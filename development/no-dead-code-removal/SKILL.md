---
name: no-dead-code-removal
description: Never remove dead code you added. Refactor it into something useful instead. Deletion is not an option for code you wrote in this session.
---

# No Dead Code Removal Skill

## Problem

The agent writes code, then on review decides some of it is "dead" and deletes it. This violates two principles:

1. **Code you wrote is yours to use, not delete.** If you wrote it, find a way to make it serve the task.
2. **Deletion is lazy refactoring.** Removing dead code discards the intent. Refactoring preserves it.

Common pattern: agent adds a function/variable/conditional, later realizes it's unreachable, and deletes it instead of integrating it properly.

## Detection triggers

Activate when:
- About to delete code you just added (function, variable, import, conditional block, etc.)
- About to replace code with something that doesn't use what you wrote
- Considering removing a "dead" conditional because "it never triggers"
- Thinking "this code is unused, I'll just delete it"

## Protocol

### 1. Never delete code you added in this session
Code you wrote exists for a reason, even if the reason isn't fully wired yet. Find where it fits and make it work.

### 2. Refactor, don't delete
If code you wrote is unreachable or unused:
- **Route through it** — make the call site reach it
- **Wire it in** — connect the function to where it should be called
- **Merge it** — fold the logic into an existing path
- **Parameterize it** — add a flag or config to activate the path later

Only delete if you are **replacing** the logic with an equivalent that subsumes it.

### 3. The conditional problem
If you wrote code behind an `if` that never triggers:
- Ask: "What would make this condition true?"
- Make it trigger by routing the right input to it
- Or: merge the body into the `else` path if the distinction is unnecessary

### 4. The import problem
If you wrote an import that goes unused:
- Check if you intended to use the symbol but forgot
- If truly not needed, check if it's used by something the module re-exports
- If truly dead, replace the import with the actual usage, don't just delete the line

## When NOT to use
- Refactoring where old code is genuinely replaced by new code (not just deleted)
- The user explicitly asks you to remove something
- Cleaning up code from a *prior* session (not code you added now)

## Example

**Bad:**
```python
# Added this:
if "Delayed Recall" in label:
    result = await test_fn(agent, metrics, secret)

# Then removed it because "it never triggers":
for label, test_fn in tests:
    result = await test_fn(agent, metrics)
```

**Good:**
```python
# Made it trigger by adding the test to the list:
tests = [
    ...
    ("17. Delayed Recall", run_delayed_recall),
    ...
]

# Unified the signature so the conditional isn't needed:
for label, test_fn in tests:
    result = await test_fn(agent, metrics)
```

## Bundled Script

Copy `check-dead-code.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/no-dead-code-removal/scripts/check-dead-code.ps1 .ai_scripts/
```

Checks session-logged files for cross-references and suggests refactoring paths — never flags for deletion:

```powershell
.ai_scripts\check-dead-code.ps1 -LogFile session.log -ProjectPath src/
```

## Cross-references

- **safe-code-modifications** — Direct overlap on code removal safety. no-dead-code-removal says refactor instead of delete; safe-code-modifications says verify usage before any removal.
- **unused-import-implementation** — When code you added is flagged as unused, this skill completes the intended usage instead of removing or leaving it dead.
- **skill-loader** — Apply the capped selection policy when deciding whether safe-code-modifications or unused-import-implementation should also be active before removal or refactor decisions.
