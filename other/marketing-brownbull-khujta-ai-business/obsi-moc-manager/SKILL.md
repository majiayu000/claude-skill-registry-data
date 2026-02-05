---
name: obsi-moc-manager
description: "Standards for recursively managing Maps of Content (MOCs) across a directory tree."
---

# MOC Manager Standards

## Core Principles
**"Structure is Recursive"**
A top-level MOC (e.g., Learning MOC) is composed of smaller Topic MOCs. The Manager's job is to ensure this hierarchy remains intact and up-to-date.

## Quality Standards (Smart Refresh)

### 1. Preservation First
- **Do NOT Overwrite**: Never blindly replace an existing MOC file.
- **Preserve User Content**: Keep any manually written "Description", "Goals", or "Custom Sections".

### 2. Append Logic
- **New Topics**: If a new subfolder/cluster is found, add it to the MOC's list.
- **Uncategorized**: If a note doesn't fit existing clusters, place it in an `Uncategorized` section or clearly mark it as [NEW].

### 3. Synchronization
- **Bidirectional Integrity**: Ensure the Parent MOC links to Child MOCs, and Child MOCs link back to Parent (if applicable).

## Checklist
- [ ] **Recursion**: Did the scanning logic correctly identify all sub-folders?
- [ ] **Safety**: Did existing content remain untouched after the update?
- [ ] **Linkage**: Are all new MOCs correctly linked in the Master MOC?
