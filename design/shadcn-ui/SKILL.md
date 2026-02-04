---
name: shadcn-ui
description: ShadCN UI component installation workflow for Wasp projects. Use when installing ShadCN components, fixing import errors, or working with UI components. Includes CRITICAL version lock (v2.3.0 ONLY) and mandatory import path fix.
triggers:
  [
    "shadcn",
    "component",
    "install component",
    "button",
    "dialog",
    "card",
    "UI component",
    "shadcn error",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Bash, Edit, Read]
---

# ShadCN UI Component Installation Skill

## Quick Reference

**When to use this skill:**

- Installing ShadCN UI components
- Fixing ShadCN import errors
- Setting up new UI components

## CRITICAL Version Lock

**ONLY USE:** ShadCN v2.3.0

**Why:** Newer versions require Tailwind v4, which is incompatible with Wasp.

## Complete Installation Workflow

### Step 1: Install Component

```bash
npx shadcn@2.3.0 add button
# Replace 'button' with desired component name
```

**CRITICAL:** Always use `@2.3.0` version lock

### Step 2: Fix Import Path (MANDATORY)

**This fix is REQUIRED for EVERY component installation!**

**File location:** `app/src/components/ui/{component}.tsx`

**Before (WRONG):**

```typescript
import { cn } from "s/lib/utils";
```

**After (CORRECT):**

```typescript
import { cn } from "../../lib/utils";
```

**Why:** ShadCN generates wrong import path. Must fix manually.

### Step 3: Use Component

```typescript
import { Button } from '@/components/ui/button'

<Button variant="default">Click me</Button>
```

## Available Components

Common components to install:

- button
- card
- dialog
- dropdown-menu
- input
- label
- textarea
- select
- checkbox
- radio-group
- switch
- accordion
- tabs
- toast
- alert
- badge
- form
- table
- sheet

## Component Location

All ShadCN components go in:

```
app/src/components/ui/
├── button.tsx
├── card.tsx
├── dialog.tsx
└── ...
```

## Common Errors & Solutions

### Error: Cannot find module 's/lib/utils'

**Cause:** Forgot to fix import path after installation

**Fix:** Change import in component file:

```diff
-import { cn } from "s/lib/utils"
+import { cn } from "../../lib/utils"
```

### Error: Component styling broken

**Cause:** Wrong import path or missing Tailwind config

**Fix:**

1. Verify import path fix was applied
2. Check `tailwind.config.js` has ShadCN config

### Error: ShadCN version mismatch

**Cause:** Used wrong version (not v2.3.0)

**Fix:** Uninstall and reinstall with correct version:

```bash
rm app/src/components/ui/{component}.tsx
npx shadcn@2.3.0 add {component}
```

## Installation Checklist

After EVERY component installation:

- [ ] Used `npx shadcn@2.3.0 add {component}`
- [ ] Fixed import path from `s/lib/utils` to `../../lib/utils`
- [ ] Verified component renders correctly
- [ ] No import errors in console

## Critical Rules

✅ DO:

- Always use @2.3.0 version lock
- Fix import path after every installation
- Verify component works before proceeding

❌ NEVER:

- Use shadcn without version lock
- Skip import path fix
- Use newer ShadCN versions (breaks with Tailwind v4)

## Examples

### Installing Button Component

```bash
# 1. Install
npx shadcn@2.3.0 add button

# 2. Fix import in app/src/components/ui/button.tsx
# Change: import { cn } from "s/lib/utils"
# To: import { cn } from "../../lib/utils"

# 3. Use
import { Button } from '@/components/ui/button'
<Button>Click me</Button>
```

### Installing Multiple Components

```bash
npx shadcn@2.3.0 add button card dialog

# Then fix import path in ALL THREE files:
# - app/src/components/ui/button.tsx
# - app/src/components/ui/card.tsx
# - app/src/components/ui/dialog.tsx
```

## Troubleshooting

If components don't work after installation:

1. Check version: `npm list shadcn-ui`
2. Verify import path fix was applied
3. Check Tailwind config includes ShadCN
4. Restart wasp: `../scripts/safe-start.sh` (multi-worktree safe)
