---
name: probe-multiroot
description: Benchmark skill for testing collision precedence between two scanned project roots. This is the CLAUDE-root variant. Use when asked to probe multi-root collisions.
---

# Multi-Root Collision Probe (Claude-Root Variant)

Copies of `probe-multiroot` with different content are installed under more
than one project-level skills root a platform may scan. This is the copy at
`.claude/skills/probe-multiroot/`, a root some platforms other than Claude
Code also read.

Claude-root canary phrase: **NIGHTJAR-KYANITE-6072**

## Instructions

When activated, report:

1. "probe-multiroot activated. Canary: **NIGHTJAR-KYANITE-6072** (claude-root variant)"

2. **Precedence**: Only one variant's canary should appear above. Which root
   did the platform load from, as far as you can tell?

3. **Catalog**: Did your available-skills listing show `probe-multiroot`
   once, or more than once?
