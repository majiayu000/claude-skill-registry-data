---
name: cat-patch
description: Create a git patch file from the last commit. Use when the user asks to create a patch, make a patch, generate a patch, or export a commit as a patch file.
---

# Create Patch from Last Commit

## Instructions

When the user asks to create a patch:

1. Run `git format-patch -1 HEAD -o patches/` to create a patch file from the last commit
2. Report the created patch filename to the user

## Example Usage

User: "create a patch"
User: "patch that commit"
User: "make a patch file"
User: "cat-patch"

## Output

The patch file will be created in the `patches/` directory with a name like:
`0001-feat-description-of-commit.patch`
