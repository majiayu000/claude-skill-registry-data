---
name: windows-file-management
description: Use this skill when working on Windows environments, particularly when you need to create folders, manipulate files, or execute shell commands. It explains how to avoid Unix-specific commands (like mkdir -p or rm -rf) and use Windows-compatible PowerShell commands or native Python alternatives.
---

# Windows File Management Best Practices

When operating as an autonomous agent or writing code that executes in a Windows shell (like PowerShell), you MUST follow these rules to avoid syntax errors and failed executions.

## 1. Avoid Unix-specific Shell Commands
Do NOT use Unix-specific syntax in bash/shell commands:
- ❌ `mkdir -p folder/subfolder` -> PowerShell does not support `-p`.
- ❌ `rm -rf folder` -> PowerShell does not support `-rf`.
- ❌ `touch file.txt` -> PowerShell does not have `touch`.
- ❌ `cmd1 && cmd2` -> PowerShell older versions do not support `&&`. Use `;` instead.

## 2. Use PowerShell Equivalents
When executing shell commands on Windows:
- ✅ **Create Directory**: `New-Item -ItemType Directory -Force -Path "folder/subfolder"` (or simply `mkdir folder/subfolder` which natively creates parents in PowerShell).
- ✅ **Remove Directory**: `Remove-Item -Recurse -Force "folder"`
- ✅ **Create Empty File**: `New-Item -ItemType File -Force -Path "file.txt"`
- ✅ **Chain Commands**: `cmd1 ; cmd2`

## 3. Prefer Python (os / pathlib)
Whenever possible, instead of executing shell commands, write a Python script using standard libraries. It is inherently cross-platform.
- **Create folders**:
  ```python
  import os
  os.makedirs("folder/subfolder", exist_ok=True)
  ```
- **Write files**:
  ```python
  from pathlib import Path
  Path("folder/file.txt").write_text("content", encoding="utf-8")
  ```

*Note: If you are running inside a restricted CodeAgent sandbox, ensure that "os" and "pathlib" are included in the `additional_authorized_imports` list.*
