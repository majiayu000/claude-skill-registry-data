---
name: import-refactor
description: Update all import statements, module references, string paths, and config references after moving or renaming files and modules. Handles Python, TypeScript, and JavaScript imports. Use when moving files, renaming modules, restructuring directories, or consolidating code.
---

# Import and Reference Updater

This guide is for updating all module references after moving or renaming files, including import statements, string paths, and configuration references.

**Core workflow**:
1. Map old paths → new paths
2. Find ALL references (imports, strings, configs, docs)
3. Update systematically by type
4. Verify paths exist and imports resolve
5. Report changes made

**Reference types updated**:
- Import statements (Python/TS/JS)
- String-based paths
- Configuration files
- Documentation examples

## Quick example

```
Moving utilities to /utils:
1. Find old utility imports
2. Update to /utils imports
3. Update string references
4. Update docs
→ Report: 23 files, 45 imports updated
```

**Best practices**:
- Verify paths exist before updating
- Preserve import style (absolute vs relative)
- Process in batches for large refactorings
- Test after major changes
