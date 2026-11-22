---
name: debug
description: Find and fix the real cause of a bug, error or crash - reproduce, narrow down, fix, prove it
---
# Debug

1. Reproduce first. Run the failing command or test and capture the exact error. If you can't make it
   fail, ask the user for the steps or input — don't fix blind.
2. Read the stack trace from the bottom up to the first line in this project's code. Read that code and
   what calls it.
3. Form one hypothesis at a time and test it cheaply: print/log the values, run a smaller input, check
   the git history of the lines (`git log -L` or `git blame`) to see what changed recently.
4. Fix the cause, not the symptom. Avoid try/except that hides the error, sleeps that hide timing bugs,
   or special cases for one input.
5. Prove it: rerun the reproduction (now passes), then the related tests. Where it fits, add a test
   that would have caught the bug.
6. Report: the cause in one or two sentences, the fix, and how you verified it.
