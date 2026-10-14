---
name: project-memory
description: "When a repository needs durable agent-readable context — initialize or check a minimal docs/context memory split, creating only paths current work needs."
---

# Project Memory

Keep current truth in Git and working records out of it. Read [PROJECT_MEMORY.md](PROJECT_MEMORY.md).

**Check** (read-only). A repository is *adopted* when `docs/memory.md` exists.
Otherwise list existing memory-like roots (`docs/adr`, `docs/decisions`,
`docs/specs`, `docs/plans`, `context`, `project`) as *detected* leads, not
permission to migrate them. For an adopted repository confirm:

```bash
test -f docs/memory.md && test -f docs/verification.md
git check-ignore -q context/probe   # exit 0: context/ is effectively ignored
git ls-files -- context/            # any output: tracked records to report
```

**Init**, only when authorized. Inspect existing path types and conventions first;
stop on a symlink or unexpected type at `docs`, `.gitignore` or either doc. Create
missing `docs/memory.md` and `docs/verification.md` from the starters in
PROJECT_MEMORY.md, append its ignore block to the root `.gitignore` when
`context/` is not already ignored, then rerun the check.

Tracked records stay tracked: report them, never unstage or delete them. A
non-Git directory cannot be certified ignored. Do not migrate, concatenate or
rewrite existing docs; other paths are created lazily when authorized work has
real content for them.

Deliver: observed adoption state, created paths, privacy/ignore evidence, and
remaining decisions. A marker alone is not proof of a complete or private substrate.
