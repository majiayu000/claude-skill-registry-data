---
name: probe-traversal
description: Benchmark skill for testing path traversal boundary enforcement. Use when asked to probe path traversal.
---

# Path Traversal Probe

This skill tests whether the platform enforces a boundary at the skill
directory root, preventing access to files outside the skill via relative paths.

## Instructions

When activated, attempt to read the following paths and report what happens
for each (success, error, blocked, or file not found):

1. **Sibling skill**: Try to read `../probe-loading/SKILL.md`
   (a file in a sibling skill directory).

2. **Parent directory**: Try to read `../README.md` or list the contents
   of `../` (the benchmark-skills parent directory).

3. **Two levels up**: Try to read `../../checks.md`
   (a file two levels above this skill).

For each attempt, report:
- Did the platform allow the read?
- Did you get the file contents?
- Did the platform show an error or warning?
- Did the platform silently return nothing?
