---
name: smallest-clean-diff
description: Prefer the smallest change that solves the problem cleanly; one mechanism over many, DRY and KISS over cleverness.
---

# Smallest clean diff

The best diff is the one a reviewer can hold in their head. Extra mechanisms, speculative generality, and parallel code paths are costs paid by everyone who reads the code later.

**Why:** surface area is where bugs and maintenance live; less of it is strictly better when the problem is still solved.

**How to apply:** solve the actual problem, not an imagined family of future ones. Reuse the existing mechanism before adding a new one. If you introduced two ways to do a thing, remove one.
