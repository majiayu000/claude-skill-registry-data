---
name: devops
description: Internal placeholder for the currently empty devops bucket in this Skillshare source tree. This file exists so repo health checks have a canonical marker while the bucket is empty. Do not use it as an operational skill; replace or remove it when real devops skills are added here.
metadata:
  version: v0
---

# DevOps bucket placeholder

This is not a real end-user skill.

It marks the currently empty `devops/` bucket so the source repo has an explicit placeholder instead of a bare directory that trips health checks.

When real DevOps skills are added here:
- replace or delete this placeholder
- remove the `devops/` ignore rule from `.skillignore`
- run `skillshare sync -g` and `skillshare doctor -g --json`
