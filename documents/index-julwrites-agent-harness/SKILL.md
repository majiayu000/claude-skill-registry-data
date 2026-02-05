---
name: index
description: Manage and query the documentation dependency index. Use this to identify which documents need to be updated when code changes.
---

# Documentation Index Skill

This skill allows you to track relationships between code and documentation, enabling "Impact Analysis".
Before making changes to code, you should check which documents describe that code.
After making changes, you should update the relevant documents and the index itself.

## Commands

### Check Impact
Find out which documents are affected by a change to a specific file.
Command: `./scripts/index impact <filepath> [--format json]`
**Use this before editing any code.**

### List Index
View all indexed relationships.
Command: `./scripts/index list [--format json]`

### Add/Update Entry
Register a relationship between a document and code files, or between documents.
Command: `./scripts/index add <doc_path> [--related "src/file1.py,src/file2.py"] [--depends "docs/other.md"] [--force]`
*   `doc_path`: The documentation file (e.g., `docs/architecture/auth.md`).
*   `--related`: Comma-separated list of files (code or other) that `doc_path` describes.
*   `--depends`: Comma-separated list of other documents that `doc_path` depends on.

### Remove Entry
Remove a document from the index or specific items from it.
Command: `./scripts/index remove <doc_path> [--item "src/file1.py"] [--section related|depends_on]`

### Check Integrity
Verify that all paths in the index actually exist.
Command: `./scripts/index check [--format json]`

### Visualize
Generate a Mermaid graph of the documentation topology.
Command: `./scripts/index graph`

## Workflow

1.  **Before Coding**: Run `./scripts/index impact src/target_file.py` to see what docs need attention.
2.  **After Coding**:
    *   Update the identified docs.
    *   If you created new files, add them to the index using `./scripts/index add`.
    *   If you deprecated files, remove them using `./scripts/index remove`.
3.  **Validation**: Run `./scripts/index check` to ensure the index is healthy.
