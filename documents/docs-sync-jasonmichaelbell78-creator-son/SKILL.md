---
name: docs-sync
description: Document Sync Check
---

# Document Sync Check

Run the automated document template-instance synchronization validator.

## What This Does

Executes `npm run docs:sync-check` to validate that:

1. Template-derived documents are properly synchronized
2. No placeholder content remains (7 patterns detected):
   - `[e.g., ...]` - example placeholders (CRITICAL)
   - `[X]` - value placeholders (CRITICAL)
   - `[Project Name]`, `[GITHUB_REPO_URL]`, `[Repository]`, `[Framework]`,
     `[TODO]` - generic placeholders (MAJOR)
3. All relative links point to existing files
4. Sync dates are recent (<90 days)

## How It Works

The script reads `docs/DOCUMENT_DEPENDENCIES.md` to identify template-instance
pairs, then validates each instance for common sync issues.

## Output

- **Exit 0**: All documents synced ✅
- **Exit 1**: Sync issues found ⚠️
- **Exit 2**: Error during check ❌

**Flags:**

- `--verbose` - Show detailed line numbers (use
  `npm run docs:sync-check -- --verbose`)
- `--json` - Output as JSON (use `npm run docs:sync-check -- --json`)

**Note:** When using npm scripts, pass flags after `--` separator.

## When to Use

- Before executing multi-AI audits (ensure audit plans are synced)
- After updating templates (verify instances were updated)
- Quarterly validation (catch drift early)
- When creating new instances from templates

## Example Output

```
🔍 Document Template-Instance Sync Check

Checked 6 template-instance pair(s)

✅ All documents are in sync
   No placeholders, broken links, or stale sync dates found
```

---

**Execute the check:**

```bash
npm run docs:sync-check
```

If issues found, see `docs/DOCUMENT_DEPENDENCIES.md` for sync protocols.
