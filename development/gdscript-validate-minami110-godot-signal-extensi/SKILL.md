---
name: GDScript Validate
description: Validate GDScript changes by refreshing Godot cache and checking diagnostics. Use after creating or editing GDScript files.
---

# GDScript Validate

Validate GDScript file changes by refreshing Godot's language server cache and checking for errors/warnings.

## When to Use

After creating or editing GDScript files (`.gd`):
- **Multiple files**: Run once after editing all files
- **Single file**: Run immediately after editing

## Validation Steps

### Step 1: Refresh Godot Cache

```bash
<this skill dir>/scripts/refresh_godot_lsp.sh
```

- Updates Godot's language server cache to recognize GDScript changes.
- **Important**: When processing multiple files, run this once after editing all files (not per file).

### Step 2: Check Diagnostics

**For specific file:**
```bash
mcp__ide__getDiagnostics --uri file:///absolute/path/to/file.gd
```

**For entire project:**
```bash
mcp__ide__getDiagnostics
```

**Note**: Only available when IDE MCP server is connected. Skip if unavailable.

### Step 3: Review Results

Check the diagnostic output for:
- **Errors**: Blocking issues that must be fixed
- **Warnings**: Code quality issues that should be addressed

**Note on diagnostic errors:**
- Real errors (UNUSED_PARAMETER, TYPE_MISMATCH, etc.): Fix your code
- False positives: If code is correct but error shows "wrong argument count" after changing signatures, ignore it (VSCode LSP cache issue, resolves on restart)
- DO NOT EDIT "./godot/" directory
