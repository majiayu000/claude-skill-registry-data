---
name: phxstack-document
description: Maintain docs/overview.md, architecture.md, and reference.md from the code as it actually is. Use when docs are missing or stale.
---

# phxstack-document

Maintain only these files:

```text
docs/overview.md
docs/architecture.md
docs/reference.md
```

Read the code first: structure, entry points, important modules, data,
configuration, runtime, and actual development and test commands. Document
the system that exists.

When the files exist, update only what changed and preserve valid human-written
material. Every command must come from the repository. If a boundary has no
clear rationale, say that it is unclear rather than inventing one.
