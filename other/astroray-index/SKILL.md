---
name: astroray-index
description: Query Astroray's built-in SQLite project index to find package ownership, dependencies, documentation, and existing scripts before broad repository searching or adding tooling.
---

# Astroray project index

Read `KNOWLEDGE.md`, then use the index for repository-routing questions:

```powershell
python scripts/project_index.py query "<topic>"
python scripts/project_index.py owns <path>
python scripts/project_index.py deps pkgNNN
python scripts/project_index.py script "<task>"
python scripts/project_index.py whatis pkgNNN
```

Treat its results as routing evidence. Inspect the returned source, package, or
documentation before changing anything. Compare package status with the live
planning sources and git state before dispatching work.
