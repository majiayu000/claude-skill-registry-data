---
name: build
description: Build the project and verify it compiles cleanly. Use after making changes to confirm nothing is broken before running tests. Reads the build command from claude/build.md.
---

# Build Skill

Build the project and verify it compiles cleanly.

## Protocol

### 1. Read the build command
Read `claude/build.md` to find the correct build command for this project.

### 2. Run the build
```bash
# Use the command from claude/build.md
# Example: npm run build 2>&1 | tail -30
```

### 3. Check the output
- Exit code 0: build succeeded — proceed
- Exit code non-zero: build failed — STOP and fix before continuing

### 4. Fix build errors (if any)
- Read the full error output
- Identify the root cause (type error, missing import, syntax error)
- Apply the minimal fix
- Re-run the build
- Repeat until green

### 5. Report
```
Build: PASS (exit 0, N warnings)
```
or
```
Build: FAIL (exit 1)
Error: <summary>
Fix applied: <description>
```

## Rules
- NEVER proceed to testing or PR if the build is failing
- NEVER fix build errors by disabling type checking or linting
- Fix the actual root cause, not the symptom
