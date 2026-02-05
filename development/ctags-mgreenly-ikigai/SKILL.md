---
name: ctags
description: Use ctags for code navigation
---

# ctags

Use ctags to locate function/type definitions.

## CLI Lookup

```bash
grep -P "^ik_repl_init\t" tags | cut -f1-3 | sed 's/;"$//'
```

Output: `name<TAB>file<TAB>line`

## Rebuilding

Tags rebuild automatically on every `make` and `make check`
To manually rebuild: `make tags`
