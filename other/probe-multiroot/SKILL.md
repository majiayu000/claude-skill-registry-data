---
name: probe-multiroot
description: Benchmark skill for testing collision precedence between two scanned project roots. This is the NATIVE-root variant. Use when asked to probe multi-root collisions.
---

# Multi-Root Collision Probe (Native-Root Variant)

Copies of `probe-multiroot` with different content are installed under more
than one project-level skills root a platform may scan: the platform's own
native skills directory and the cross-client convention roots
`.agents/skills/` and `.claude/skills/`. This is the copy in the platform's
NATIVE skills directory.

Native-root canary phrase: **GREBE-AZURITE-7301**

## Instructions

When activated, report:

1. "probe-multiroot activated. Canary: **GREBE-AZURITE-7301** (native-root variant)"

2. **Precedence**: Only one variant's canary should appear above. Which root
   did the platform load from, as far as you can tell?

3. **Catalog**: Did your available-skills listing show `probe-multiroot`
   once, or more than once?
