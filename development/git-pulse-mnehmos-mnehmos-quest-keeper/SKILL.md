---
name: git-pulse
description: Version control discipline for Quest Keeper AI development. Enforces the "commit early, commit often" pattern.
---

# Git Pulse Protocol

## Core Rule
> Your work is volatile until captured.

**After successful test pass, IMMEDIATE LOCAL COMMIT.**

## Quick Commands
```powershell
git status
git add . && git commit -m "type(scope): message"
```

## Commit Types
- `fix` - Bug fixes
- `feat` - New features  
- `test` - Test additions
- `refactor` - Code cleanup
- `docs` - Documentation
- `style` - Formatting
- `chore` - Build/config