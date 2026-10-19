---
name: ovstorage-contributor-verify-before-merge
description: Use before opening or merging an ovstorage PR to run the project verification gate and inspect risky diffs.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, ci, verification]
tools: [Read, Bash]
compatibility: Requires an ovstorage checkout and local toolchains needed by make verify and make test.
---

# Verify Before Merge

## Goal

Run the same checks CI uses and catch common mistakes before review.

## Recipe

1. Run `git status --short` and make sure only intended files changed.
2. Run `make verify`.
3. Run `make test`.
4. If skills changed, run `make validate-skills`.
5. Confirm no vendored services files changed with
   `git diff --name-only -- ovstorage-services/`.
6. If generated headers changed, verify they were regenerated with
   `make verify-headers-clean`.

## References

- [`docs/public/agent/README.md`](../../docs/public/agent/README.md) for the agent skill
  surface.
