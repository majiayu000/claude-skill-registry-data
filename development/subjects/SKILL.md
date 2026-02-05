---
name: subjects
description: Explore denmark statistics subject hierarchy for all fact tables
---

# subjects CLI

This CLI lets you explore denmark statistics subject hierarchy. The subject hierarchy creates a hierarchical grouping of all the fact tables.

```bash
python scripts/subjects.py  
```

## Browsing subjects

```bash
python scripts/subjects.py           # children of the root subject (DST)
python scripts/subjects.py "Borgere" # children of subject "Borgere" ("Borgere" is a child of root subject)
```

### Slash paths

Use slash-separated names to jump multiple levels in one command:

```bash
python scripts/subjects.py "Borgere/Befolkning/Befolkningstal"
```

Each segment matches the description, label, or raw node id of a child under the previous segment.

### Depth control

`--depth` controls how many layers of descendants to show. `-1` means “all descendants”.

```bash
python scripts/subjects.py "Borgere" --depth 2
python scripts/subjects.py "Borgere/Befolkning" --depth -1
```

Indented children are subject nodes; when a leaf is reached, its subjects print with descriptions.

### Breadcrumbs

`--parents` (or `--no-parents` to suppress) prints the resolved path from the root before the listing:

```bash
python scripts/subjects.py "Befolkningstal" --parents
```