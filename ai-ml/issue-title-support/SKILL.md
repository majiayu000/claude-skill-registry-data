---
name: issue-title-support
description: >-
  Internal runtime support for universal skills that validate canonical scoped
  issue titles. Do not invoke directly.
disable-model-invocation: true
user-invocable: false
---

# Issue title support

This package gives `track-work` and `triage` one mechanical predicate for the
canonical scoped issue-title contract. It is a `SKILL.md`-bearing package only
so current and legacy category-sync engines vendor it with the universal
category; it has no user-facing workflow.
