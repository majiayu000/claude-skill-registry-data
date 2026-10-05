---
name: commit
description: Create repository-adaptive checkpoint commits for coherent work, including requests to split changes into commits and push; publication remains separately authorized
when_to_use: "commit, checkpoint, save work, 提交, preserve progress, done with a coherent slice — NOT release aggregation (use /ship)"
argument-hint: '[--publish] [--candidate] [--dry-run]'
user_invocable: true
---

# Commit

Create one or more truthful checkpoint commits on an owned delivery branch.
Discover repository message, signing, DCO, hook, and verification policy before
committing. A commit preserves work; it does not automatically authorize push,
PR publication, merge, or branch deletion.

This skill is the BUILD/checkpoint operation of `$delivery`. Run the shared
delivery context probe and use its active record rather than assuming
`origin/main`, GitHub, branch ownership, or a writable attached checkout.
