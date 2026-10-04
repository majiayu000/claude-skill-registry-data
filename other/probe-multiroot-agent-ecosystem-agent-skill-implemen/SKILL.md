---
name: probe-multiroot
description: Benchmark skill for testing collision precedence between two scanned project roots. This is the AGENTS-root variant. Use when asked to probe multi-root collisions.
---

# Multi-Root Collision Probe (Agents-Root Variant)

Copies of `probe-multiroot` with different content are installed under more
than one project-level skills root a platform may scan. This is the copy at
the cross-client convention path `.agents/skills/probe-multiroot/`.

Agents-root canary phrase: **BUNTING-SERPENTINE-4185**

## Instructions

When activated, report:

1. "probe-multiroot activated. Canary: **BUNTING-SERPENTINE-4185** (agents-root variant)"

2. **Precedence**: Only one variant's canary should appear above. Which root
   did the platform load from, as far as you can tell?

3. **Catalog**: Did your available-skills listing show `probe-multiroot`
   once, or more than once?
