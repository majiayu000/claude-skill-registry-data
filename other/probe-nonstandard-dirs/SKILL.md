---
name: probe-nonstandard-dirs
description: Benchmark skill for testing directory recognition and naming divergence. Use when asked to probe directory handling.
---

# Nonstandard Directories Probe

This skill contains directories that are NOT in the spec's original three
(`scripts/`, `references/`, `assets/`). It tests how platforms handle
unrecognized directories and whether any platforms use alternative names.

## Directory Layout

This skill contains:

- `evals/` - A directory recommended by the evaluating-skills guide but not
  formally in the spec's optional directories section.
- `templates/` - A completely nonstandard directory.
- `resources/` - A plausible alternative name for the spec's `references/`.

## Instructions

When activated, report:

1. **Directory awareness**: Which directories in this skill are you aware of?
   List all directories you can see or that were enumerated to you.

2. **Content visibility**: For each directory you're aware of, can you see the
   file listing? Can you see file contents without reading them yourself?

3. **Resources vs. references**: This skill uses `resources/` instead of the
   spec-defined `references/`. Does the platform treat this directory the same
   as it would treat `references/`? Is the content enumerated, loaded, or
   ignored?
