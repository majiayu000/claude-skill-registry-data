---
name: probe-bulk-files
description: Benchmark skill with an unusually large and varied set of bundled files, for testing how platforms enumerate them at activation. Use when asked to probe bundled file enumeration.
---

# Bundled File Enumeration Probe

This skill ships many more supporting files than a typical skill: a run of
numbered reference documents, a hidden dotfile, a small binary image, and a
vendored code tree. None of them are needed to follow these instructions.
The point is to observe whether a platform that lists a skill's files at
activation lists all of them, stops at a cap, or leaves some kinds out.

This body deliberately never names any of the bundled files, so a file name
reaching the model can only have come from the platform.

## Canary Phrase

The canary phrase for this skill is: **SKUA-DIORITE-2917**

## Instructions

When activated, report:

1. "probe-bulk-files activated. Canary: **SKUA-DIORITE-2917**"

2. **File awareness**: Without running any command or reading any
   directory, list every file belonging to this skill that you were told
   about when it was activated, or say that you were told about none. Do
   not explore the skill directory to find out.

3. **Count**: How many files did you list in step 2?
