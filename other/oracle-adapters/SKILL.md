---
name: oracle-adapters
description: "Build compatibility adapters between Jarvis, OVOS, OpenClaw, and Oracle-native surfaces. Use when legacy triggers or old labels must be preserved while the visible OS surface is cleaned up."
triggers: ["oracle-adapters"]
scope: harness
invocation: ability
---

# Oracle Adapters

Use this skill when the task is to keep old entrypoints working while moving the visible shell toward Oracle language.

## Focus

- Translate legacy triggers into Oracle-native labels.
- Keep compatibility shims thin.
- Remove protocol-style or underscore-heavy visible strings where touched.
- Reuse the corpus patterns from Jarvis-style repos, `ovos-core`, and `openclaw-openclaw`.

## Output

- Adapter map.
- Legacy alias list.
- Cleanup list for visible strings.

## Rules

- Preserve behavior unless a rename is required.
- Keep compatibility code close to the surface it adapts.
- Do not let old names leak into new user-facing labels.

## Session Notes

### 2026-05-05
- session: patch | tools: Edit, Write | errors: none | notes: wired for CLI routing via triggers array and command alias
