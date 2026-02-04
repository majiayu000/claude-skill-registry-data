---
name: Sync Documentation
description: Use this skill at the end of a task to ensure documentation matches the code.
---

# Sync Documentation

Use this skill to prevent documentation drift after you change behavior, flows, or structure.

## Checklist

1) `architecture.md` (index)

- [ ] New module/service/folder? -> add it to the index
- [ ] Changed a main flow? -> update the relevant `docs/architecture/*` page(s)

2) `docs/architecture/` (leaf docs)

- [ ] Update the page(s) that map to the modified area (backend core/data/indicators, chart map, flows, runs/logging, etc.)
- [ ] Keep each doc short and linkable (LLM-friendly)

3) `README.md`

- [ ] New env var? -> document it
- [ ] Changed how to run/test? -> update commands

4) `ROADMAP.md`

- [ ] Completed an item? -> mark it done
- [ ] New work discovered? -> add it

## Output requirement

In the final response, explicitly list:

- `Updated: architecture.md` (if changed)
- `Updated: docs/architecture/...` (if changed)
- `Updated: README.md` / `Updated: ROADMAP.md` (if changed)

