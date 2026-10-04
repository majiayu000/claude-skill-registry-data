---
name: document
description: Auto-update living docs (USER_MANUAL.md, app-complete-audit.md) after code changes. Keeps docs in sync with reality.
user-invocable: true
---

# Document Sync

After code changes, update the living docs that track what the app does. Run this after building, before shipping.

## 1. Detect What Changed

```bash
git diff --name-only
```

```bash
git diff --cached --name-only
```

Categorize changes:

- **UI changes** (app/, components/) -> update both docs
- **Backend only** (lib/, scripts/) -> update USER_MANUAL.md only if behavior changed
- **Docs only** -> skip, already handled

## 2. Update USER_MANUAL.md

Read `docs/USER_MANUAL.md`. For each UI/behavior change:

- Find the relevant section
- Edit in-place (don't append)
- If new feature, add section in logical position
- If removed feature, delete the section
- Keep the manual's existing voice and structure

## 3. Update app-complete-audit.md

Read `docs/app-complete-audit.md`. For each UI change:

- New page/route -> add entry
- New button/form/modal -> add under correct page
- Removed element -> delete entry
- Renamed element -> update entry

## 4. Report

```
DOCS UPDATED

USER_MANUAL:  [sections added/edited/removed, or "no changes needed"]
AUDIT:        [entries added/edited/removed, or "no changes needed"]
```

Only touch sections relevant to the code changes. Don't rewrite unrelated sections.
