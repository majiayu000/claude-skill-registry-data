---
name: test-review
description: Audit the tests of a Go package for truth and coverage quality. Trigger for test review, coverage checks, mocks, fakes, edge cases, vacuous assertions, or cross-package integration test gaps.
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

This skill is defined in `.agents/skills/test-review/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
