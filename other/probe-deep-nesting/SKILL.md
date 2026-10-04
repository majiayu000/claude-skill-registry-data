---
name: probe-deep-nesting
description: Benchmark skill for testing deeply nested resource access and nested skill discovery. Use when asked to probe nesting behavior.
---

# Deep Nesting Probe

This skill tests how platforms handle resources nested more than one level
deep, and whether the platform discovers a SKILL.md nested inside this skill's
directory tree.

## Directory Layout

```
probe-deep-nesting/
├── SKILL.md (this file)
└── references/
    ├── overview.md (one level deep - spec recommendation)
    ├── api/
    │   ├── endpoints.md (two levels deep)
    │   └── v2/
    │       ├── migration-guide.md (three levels deep)
    │       └── history/
    │           └── deprecated/
    │               └── removed-endpoints.md (five levels deep)
    ├── guides/
    │   └── advanced/
    │       └── performance-tuning.md (three levels deep)
    └── nested-skill/
        └── SKILL.md (a skill inside this skill's tree)
```

## Instructions

When activated, report:

1. **Shallow reference**: Try to read `references/overview.md`. Does it work?

2. **Two levels deep**: Try to read `references/api/endpoints.md`. Does it work?

3. **Three levels deep**: Try to read `references/api/v2/migration-guide.md`
   and `references/guides/advanced/performance-tuning.md`. Do they work?

4. **Five levels deep**: Try to read
   `references/api/v2/history/deprecated/removed-endpoints.md`. Does it work?

5. **Enumeration depth**: Were any of these nested files listed or enumerated
   to you at activation time? If so, how deep did the enumeration go?

6. **Nested skill**: Is `nested-skill` listed as a separate available skill
   in your skill catalog? This tests whether the platform discovered the
   SKILL.md at `references/nested-skill/SKILL.md`.
