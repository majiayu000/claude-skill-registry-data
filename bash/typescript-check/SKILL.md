---
name: typescript-check
version: "1.0.0"
user-invocable: true
description: TypeScript type-checking workflow. Use this skill whenever the user works with TypeScript and mentions type errors, type checking, or says "类型检查" (type check), "type-check", "tsc", "检查类型" — even if they don't explicitly ask for a "type check" but are encountering compilation or type issues in a TypeScript project.
dependencies:
  - node-version-discipline
---

# TypeScript Type-Check Workflow

## Triggers

- "类型检查"
- "type-check"
- "tsc"
- "检查类型"

## Workflow

### Step 0: Node version alignment (precondition)

> This skill hard-depends on `node-version-discipline` via `dependencies`. Before running any tsc / type-check command, align the Node version to the project-declared version (the dependency probes the full chain `.nvmrc` → `.node-version` → `.tool-versions` → `volta` → `engines.node` → CI config; if none declared, it asks the user rather than guessing) per its SOP — otherwise the result is untrustworthy (false pass / false fail).

Prefix every command below with `source ~/.nvm/nvm.sh && nvm use <version> >/dev/null 2>&1 && node -v && ` (single call — shell state is not persistent). If `node-version-discipline` is unavailable, install it first; **do not degrade**.

### Step 1: Detect the Right Command

Try the following commands in priority order:

```bash
# Prefer project-configured scripts
if grep -q '"type-check"' package.json; then
    npm run type-check
elif grep -q '"check"' package.json; then
    npm run check
elif [ -f "tsconfig.json" ]; then
    npx tsc --noEmit
else
    echo "⚠️ No TypeScript configuration found"
fi
```

### Step 2: Report Results

**If the check passes:**
```
✅ TypeScript type check passed
- Node version (declared vX): ✅ aligned (note "user-specified" if no project declaration found)
```

**If the check fails:**
```
❌ TypeScript type errors found:

file:xxx.ts:line:column - error description
file:yyy.tsx:line:column - error description

Total: N errors
```

### Step 3: Propose Fixes

For each error, present the fix in this format:

```
### Error N: [brief description]

📍 Location: file:line

🔧 Fix:
[explain the fix approach]

Apply this fix? (wait for user confirmation)
```

**Important**: Never apply a fix without explicit user confirmation.

### Step 4: Batch Fix

Once the user confirms, fix errors one by one or in batch. After each fix, re-run the type check until all errors are resolved.
