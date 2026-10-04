---
name: heal-skill
description: Self-repair a skill that failed or produced bad results. Analyze what went wrong and update the skill definition.
user-invocable: true
---

# Heal Skill

When a skill produces bad output or fails, this skill diagnoses and patches it.

## Input

User says which skill failed and what went wrong (or reference the failure in conversation history).

## Process

1. **Read the skill file:** `.claude/skills/[name]/SKILL.md` or `.claude/skills/[name]/skill.md`
2. **Identify the failure:**
   - Did a command fail? (wrong path, missing tool, bad syntax)
   - Did the output format not match expectations?
   - Did it do too much or too little?
   - Did it miss context it should have had?
3. **Diagnose root cause:** Check if the issue is in the skill definition, the underlying script, or a changed environment
4. **Patch the skill file** with the fix
5. **Report what changed and why**

## Rules

- Only modify the skill file the user identified (or the one that clearly failed)
- Don't rewrite the whole skill; patch the specific broken part
- If the underlying script is broken (not the skill definition), fix the script instead
- Add a comment in the skill file noting what was healed and when, if the fix was non-obvious

## Output

```
HEALED: /[skill-name]

FAILURE:  [what went wrong]
CAUSE:    [why]
FIX:      [what was changed in the skill definition]
TEST:     [how to verify the fix works]
```
