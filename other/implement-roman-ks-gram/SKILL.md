---
name: implement
description: Implement a spec from docs/changes/open/ following the project workflow
---

# Implement Spec

Implement a spec file from `docs/changes/open/` following the standard project workflow.

## Usage

```
/implement <spec-filename>
```

Examples:
```
/implement 0004-replace-fooditem-dropdowns.md
/implement 0005-chrome-installable-webapp.md
```

## Workflow

When you invoke this skill, follow these steps:

1. **Read the request** — Read the spec file from `docs/changes/open/` and review relevant code/DESIGN sections
2. **Implement** — Implement against the acceptance criteria; tick each box as you complete them
3. **Record decisions** — Document any decisions/tradeoffs under **Notes / decisions** in the spec
4. **Update status** — Change the header from `Status: open` to `Status: **done** · Shipped: YYYY-MM-DD` (use today's date)
5. **Move file** — Move the spec file from `docs/changes/open/` to `docs/changes/done/`
6. **Update CHANGELOG.md** — Add one line describing the change
7. **Update DESIGN.md** — If an architectural decision was made, log it in DESIGN.md §11

## Tips

- Use the **Read** tool to fetch the spec and any relevant code/design docs
- Use **Edit** to modify files and update the spec status before moving it
- Use **Bash** to move the file: `mv docs/changes/open/FILENAME docs/changes/done/FILENAME`
- Tick the acceptance criteria boxes in the spec as proof of completion
- Keep CHANGELOG.md entries concise (one line per change)
- CHANGELOG.md is located in docs/changes/CHANGELOG.md

