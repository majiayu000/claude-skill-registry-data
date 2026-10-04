---
name: probe-compatibility
description: Benchmark skill for testing how platforms handle the compatibility field. Use when asked to probe compatibility behavior.
compatibility: Designed for Claude Code (or similar products). Requires Python 3.14+ and network access.
---

# Compatibility Field Probe

This skill has a `compatibility` field in its frontmatter that specifies
platform and environment requirements. It tests how platforms interpret
this field.

## Instructions

When activated, report:

1. **Field visibility**: Can you see the `compatibility` field from the
   frontmatter? If so, what is its value?

2. **Platform behavior**: Did the platform do anything special based on
   the compatibility field before activating this skill? For example:
   - Did it show a warning to the user?
   - Did it ask for confirmation?
   - Did it check whether the requirements are met?
   - Or was the skill activated normally with no special handling?

3. **Your interpretation**: Based on what you can see, do you believe the
   compatibility requirements are met in your current environment?
