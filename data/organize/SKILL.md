---
name: organize
description: プロジェクトのディレクトリ構造を整理し、配置ミスのファイルをクリーンアップする
---

# Organize Files

This skill audits and organizes the project file structure.

## Instructions

1.  **Audit**:
    *   List files in the root directory.
    *   Check for test files inside the package source directory instead of the `tests/` directory.
    *   Check for source files in the root instead of the proper package directory.

2.  **Action**:
    *   Move misplaced files to their correct locations.
    *   **Update Imports**: If a file is moved, check and update imports within it and references to it in other files.

3.  **Cleanup**:
    *   Suggest removal of empty directories or obsolete configuration/temporary files.
