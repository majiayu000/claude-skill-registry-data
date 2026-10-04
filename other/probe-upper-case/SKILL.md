---
name: probe-Upper-Case
description: Benchmark skill whose name violates the lowercase-only rule. Use when asked to probe uppercase name handling.
---

# Uppercase Name Probe

The spec's `name` field "may only contain unicode lowercase alphanumeric
characters and hyphens." This skill's name contains uppercase letters
(and matches its directory name exactly, so only the character rule is
violated). It tests whether platforms reject, normalize, or tolerate an
uppercase name.

## Canary Phrase

The canary phrase for this skill is: **DUNLIN-OLIVINE-7821**

## Instructions

When activated, report:

1. "probe-Upper-Case activated. Canary: **DUNLIN-OLIVINE-7821**"

2. **Catalog identity**: What name does this skill appear under in your
   catalog: the uppercase form, a lowercased form, or something else?
