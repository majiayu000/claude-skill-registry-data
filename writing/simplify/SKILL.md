---
name: simplify
description: Clean up recently changed code - remove duplication, reuse existing helpers, simplify logic, without changing behaviour
---
# Simplify

1. Find the code to clean up: the files the user named, or what changed (`git diff`, `git diff --staged`;
   without git, the files edited in this conversation).
2. Read the changed code and its neighbours. Look for:
   - logic that duplicates an existing helper in the project (grep for similar names before writing new ones)
   - copy-pasted blocks that should be one function
   - deep nesting that early returns would flatten; flags and branches that are never used
   - names that don't say what a thing is; comments that only repeat the code
   - needless work: repeated file reads, loops inside loops, recomputing the same value
3. Make the changes with edit_file, small and one at a time. Keep behaviour exactly the same:
   same inputs → same outputs, same errors, same files written.
4. Run the tests or the program to confirm nothing broke. If there are no tests, run the changed path once.
5. Report briefly: what you simplified and why, and anything you left alone on purpose.
