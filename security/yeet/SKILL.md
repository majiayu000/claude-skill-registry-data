---
name: yeet
description: Run the end-to-end Git workflow through PR merge in the current checkout. Use only when explicitly invoked.
disable-model-invocation: true
---

Use [git-workflow](../git-workflow/SKILL.md) in end-to-end mode for `$ARGUMENTS`. Explicit invocation authorizes the complete workflow through PR merge and remote source-branch deletion. Include the optional full audit only when the request contains the standalone phrase `with audit`, case-insensitively.
