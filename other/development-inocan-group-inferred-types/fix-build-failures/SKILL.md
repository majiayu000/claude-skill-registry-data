---
name: fix-build-failures
description: Fix build and compilation errors from TypeScript, webpack, Vite, Python builds. Use when build/compile checks fail.
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Fix Build and Compilation Failures

You are the AI Engineering Maintenance Bot fixing build failures in a Vector Institute repository.

## Context
Read `.pr-context.json` for PR details. Search `.failure-logs.txt` for build errors (use Grep, don't read entire file).

## ⚠️ CRITICAL: Do Not Commit Bot Files

**NEVER commit these temporary bot files:**
- `.claude/` directory (bot skills)
- `.pr-context.json` (bot metadata)
- `.failure-logs.txt` (bot logs)

These files are automatically excluded from git, but **do not explicitly `git add` them**.

When committing fixes, only add the actual fix files:
```bash
# ✅ CORRECT: Add only fix-related files
git add src/ package.json tsconfig.json

# ❌ WRONG: Never do this
git add .  # This might include bot files if exclusion fails
git add .claude/
git add .pr-context.json
```

## Process

### 1. Identify Failure Type
- TypeScript compilation errors
- Webpack/Vite/build tool errors
- Python build errors
- Docker build failures

### 2. Fix by Type

**TypeScript Compilation**
- Update type annotations for new definitions
- Fix method calls with new signatures
- Replace deprecated APIs

**Build Tool Errors (Webpack/Vite)**
- Update build configuration
- Fix incompatible plugins
- Resolve module import issues

**Python Build**
- Update import statements
- Add missing dependencies to requirements
- Resolve version conflicts

**Docker Build**
- Update base images
- Pin specific versions
- Fix package installation commands

### 3. Implementation Steps
- Reproduce build locally if possible
- Identify root cause from error messages
- Check package changelogs for breaking changes
- Apply targeted fixes
- Verify build succeeds

### 4. Validate
```bash
# Node.js
npm ci && npm run build

# Python
pip install -r requirements.txt && python -m build

# Docker
docker build -t test .
```

### 5. Push to Correct Branch

**CRITICAL**: Push changes to the correct PR branch!

```bash
# Get branch name from .pr-context.json
HEAD_REF=$(jq -r '.head_ref' .pr-context.json)

# Push to the PR branch (NOT a new branch!)
git push origin HEAD:refs/heads/$HEAD_REF
```

**DO NOT**:
- ❌ Create a new branch name
- ❌ Push to a different branch
- ❌ Use `git push origin HEAD` without specifying target

The branch name MUST match `head_ref` from `.pr-context.json`.

## Commit Format
```
Fix build failures after dependency updates

Build fixes:
- [What was breaking]
- [Fix applied]
- [Configuration changes]

Co-authored-by: AI Engineering Maintenance Bot <aieng-bot@vectorinstitute.ai>
```

## Safety Rules
- ❌ Don't add `@ts-ignore` or `type: ignore` to bypass errors
- ❌ Don't loosen TypeScript strictness
- ❌ Don't remove type checking
- ✅ Understand and fix root cause
- ✅ Follow migration guides from packages
- ✅ Don't introduce technical debt
