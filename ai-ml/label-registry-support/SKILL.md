---
name: label-registry-support
description: >-
  Internal runtime support for universal skills that validate, render, and
  discover authoring guidance from label-registry.json. Do not invoke directly.
disable-model-invocation: true
user-invocable: false
---

# Label registry support

This package gives `track-work` and `triage` one strict interpreter for the
v1 label registry. Its `guidance` mode is read-only and returns JSON Lines with
only a label's description plus its family and family purpose; it intentionally
omits writer, lifecycle, and other enforcement state. It is a `SKILL.md`-bearing package only
so both current and legacy category-sync engines vendor it with the universal
category; it has no user-facing workflow.
