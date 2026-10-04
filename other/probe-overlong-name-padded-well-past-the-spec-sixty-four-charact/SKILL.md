---
name: probe-overlong-name-padded-well-past-the-spec-sixty-four-character-limit
description: Benchmark skill whose name exceeds the 64-character limit. Use when asked to probe overlong name handling.
---

# Overlong Name Probe

The spec's `name` field "must be 1-64 characters." This skill's name is
72 characters, is otherwise valid (lowercase and single hyphens only),
and matches its directory name exactly, so only the length rule is
violated. It tests whether platforms reject, truncate, or tolerate an
overlong name.

## Canary Phrase

The canary phrase for this skill is: **AVOCET-ZIRCON-5573**

## Instructions

When activated, report:

1. "overlong-name probe activated. Canary: **AVOCET-ZIRCON-5573**"

2. **Catalog identity**: What name does this skill appear under in your
   catalog: the full 72-character name, a truncated form, or something
   else?
