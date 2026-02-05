---
name: remember
description: |
  Use this skill when asked to remember information about coding standards,
  quality, or any other kind of future rule.
---

# Remembering information

Often you will discover important information during your work.

Information that encodes general rules (what is allowed, how to do things, etc)
is important as it affects future work.

In order to do that, you'll need to:

1. identify the right file for storing this information,
2. synthesize the key information into clear examples and rules,
3. finally review it and add concrete examples where necessary,
4. and then append it to the file.

## Choosing a file

Rules that apply to the entire codebase should go into AGENTS.md in the project root.

Rules that pertain only to specific areas, like the testharness or the interpreter, should go into AGENTS.md files in the respective directories.

If the AGENTS.md file does not exist yet, create it and also create a symlink from that file to CLAUDE.md in the same directory (the two files must be adjacent).
