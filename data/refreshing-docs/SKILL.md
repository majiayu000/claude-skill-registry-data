---
name: refreshing-docs
description: Refreshes README.md documentation tables including the packages table and core namespace index. Reads from package.json files and core module JSDoc.
---

# Refreshing Docs

Update auto-generated documentation tables in README.md.

## Steps

1. Run the script at `.claude/skills/refreshing-docs/scripts/docs-refresh.ts`

## Reference

The script updates two sections in README.md:

1. **Packages table** - Lists all packages from `packages/*/package.json`
2. **Core namespace index** - Lists modules from `core/src/*/_.ts` with JSDoc descriptions

Sections are marked with HTML comments:

```markdown
<!-- PACKAGES_TABLE_START -->
| Package | Description |
| ------- | ----------- |
| [`@kitz/core`](./packages/core) | Core utilities |
...
<!-- PACKAGES_TABLE_END -->

<!-- CORE_NAMESPACE_INDEX_START -->
| Module | Description |
| ------ | ----------- |
| `Arr` | Array utilities |
...
<!-- CORE_NAMESPACE_INDEX_END -->
```

## Notes

- Run after adding/removing packages or modifying package descriptions
- Run after adding/modifying core modules or their JSDoc
- The markers must exist in README.md for the script to work
