---
name: correcting-mistakes
description: Self-corrects skill and command instructions after resolving errors. Use when Claude errors during skill/command execution and finds a solution, or when user indicates a mistake was made. Finds the relevant instruction file and applies succinct fixes.
---

# Correcting Mistakes in Skills and Commands

Trigger this skill when:
1. You error during execution of a skill or command and eventually work out a solution
2. The user indicates you made a mistake in executing a skill or command
3. Claude fails during skill or command execution due to an edge case

## Workflow

### Step 1: Locate the Instruction File

Find the relevant file that needs correction:
- Skills: `.claude/skills/{skill-name}/SKILL.md` or reference files
- Commands: `.claude/commands/{command-name}.md`

Read the file to understand the current instructions.

### Step 2: Diagnose the Root Cause

Determine: **Was this your misunderstanding, or an instruction issue?**

**Your misunderstanding** (stop here, no changes needed):
- You misread or misapplied clear instructions
- The instruction was correct but you made an execution error
- Context from the conversation led you astray, not the instruction

**Instruction issue** (proceed to Step 3):
- The instruction was ambiguous, misleading, or incomplete
- An edge case was found that the skill or command doesn't account for
- The instruction specified an incorrect approach
- The instruction omitted a critical step or detail

### Step 3: Test Before Fixing (if applicable)

**If the correction involves a script, command, or tool use:**
1. Test the correct approach in the current session
2. Verify it works as expected
3. Only proceed to Step 4 after confirmation

This prevents codifying a "fix" that doesn't actually work.

### Step 4: Apply the Correction

Edit the instruction file with these principles:

**Write for a reader with no memory of the error:**
- State the correct approach directly
- Do not reference the mistake, the error, or what was wrong before
- Do not add "Note:" or "Important:" warnings about the pitfall
- Do not explain why this is correct (unless explanation is inherently useful)

**Be succinct:**
- Change only what's necessary
- Preserve the existing style and structure
- Avoid adding defensive caveats or extra context

**Example - Good correction:**
```markdown
# Before (incorrect)
Use `synthesis.md` as the template.

# After (correct)
Use `./templates/research-synthesis.md` as the template.
```

**Example - Bad correction (too verbose, references error):**
```markdown
# After (bad - references the error)
Use `./templates/research-synthesis.md` as the template.
Note: The file is named research-synthesis.md, not synthesis.md.
```

### Step 5: Confirm

After applying the fix:
1. Re-read the corrected section to verify it reads naturally
2. Confirm the fix is self-contained (no orphaned references to removed content)
3. Inform the user what was corrected
