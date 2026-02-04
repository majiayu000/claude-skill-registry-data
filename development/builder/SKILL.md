---
name: builder
description: Build applications that require compilation. Use this skill before testing or running apps that need a build phase (e.g., C++ desktop app).
---

# Builder

Compile applications before testing or deployment.

## Reference Documentation

| Reference | When to Read |
|-----------|--------------|
| `references/desktop-build.md` | Building desktop C++ app |

## When to Build

Build is required when:
- Source code has changed
- Dependencies have been updated
- First time setting up the project
- After pulling new changes from git

## Workflow

### STEP 1: IDENTIFY APP

Determine which app needs building:

| App | Build Required | Reference |
|-----|----------------|-----------|
| `desktop/` | Yes (C++) | `references/desktop-build.md` |
| `backend/` | No (Python) | Just `uv sync` for deps |

### STEP 2: CHECK PREREQUISITES

Before building, verify:
- Required tools are installed
- Environment is configured
- Dependencies are available

See app-specific reference for prerequisites.

### STEP 3: CONFIGURE (if needed)

Run configuration step on:
- First build
- After changing build configuration
- After updating dependencies

### STEP 4: BUILD

Execute build command. Handle common issues:
- Kill running processes (file locks)
- Clean build if needed
- Check for errors

### STEP 5: VERIFY

Confirm build succeeded:
- Check for executable/output
- Run basic health check
- Note any warnings

## Quick Reference

### Desktop App

```powershell
cd D:\projects\buddy\desktop

# First time or after config changes
.\configure.ps1

# Build (kills running process automatically)
.\build.ps1

# Verify
.\build\Debug\BuddyDesktop.exe --version
```

### Backend (no build needed)

```bash
cd backend
uv sync                          # Install/update dependencies
uv run uvicorn backend.main:app  # Run directly
```

## Build Errors

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| File in use | App still running | Kill process, retry |
| Missing tool | Not installed | Install prerequisite |
| Linker errors | ABI mismatch | Clean build, reconfigure |
| Dependency fail | Package issue | Check vcpkg/npm logs |

### When to Clean Build

```powershell
# Desktop - remove build directory
Remove-Item -Recurse -Force desktop/build
.\configure.ps1
.\build.ps1
```

Clean build when:
- Switching branches with major changes
- Updating build configuration
- Unexplained linker errors
- Dependency version conflicts

## Integration with Testing

Always build before running tests:

```powershell
# Desktop workflow
.\desktop\build.ps1                             # Build first
.\desktop\build\Debug\BuddyDesktop.exe --debug  # Run in debug mode
python desktop/tests/T00022/T00022-01.py        # Then test
```

## Critical Rules

1. **Build before test** - Always compile latest code
2. **Check for errors** - Don't ignore warnings
3. **Kill running processes** - Prevents file lock issues
4. **Clean when stuck** - Fresh build solves many issues
5. **Document build issues** - In `5-progress-and-issues.md`
