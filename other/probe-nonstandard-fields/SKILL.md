---
name: probe-nonstandard-fields
description: Benchmark skill for testing how platforms handle nonstandard frontmatter fields. Use when asked to probe nonstandard fields.
requires: probe-loading
depends-on:
  - probe-shadow-alpha
  - probe-shadow-beta
priority: high
---

# Nonstandard Fields Probe

This skill uses frontmatter fields that are NOT in the Agent Skills
specification: `requires`, `depends-on`, and `priority`. It tests whether
any platform recognizes and acts on these fields.

## Instructions

When activated, report:

1. **Field visibility**: Can you see the nonstandard frontmatter fields
   (`requires`, `depends-on`, `priority`)? If so, list their values.

2. **Platform behavior**: Did the platform do anything with these fields?
   For example:
   - Did it attempt to load `probe-loading` based on the `requires` field?
   - Did it attempt to load `probe-shadow-alpha` and `probe-shadow-beta`
     based on the `depends-on` field?
   - Did it order skills or change behavior based on `priority`?
   - Or were the fields silently ignored?

3. **Validation**: Did the platform warn about unrecognized frontmatter
   fields, or accept them silently?
