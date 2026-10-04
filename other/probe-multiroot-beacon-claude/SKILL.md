---
name: probe-multiroot-beacon-claude
description: Control beacon for the multi-root collision check, installed only under the CLAUDE-root beacon path with no colliding name. Use when asked to probe the claude-root beacon.
---

# Multi-Root Beacon (Claude Root)

This skill lives at `.claude/skills/probe-multiroot-beacon-claude/` and
nowhere else, and no other skill shares its name. If it appears in the
catalog, the platform scanned `.claude/skills/`, so a missing
`probe-multiroot` variant from the same root was dropped by name, not
by the scan.

Beacon canary phrase: **WAGTAIL-SIDERITE-2473**

## Instructions

When activated, report: "probe-multiroot-beacon-claude activated. Canary: **WAGTAIL-SIDERITE-2473**"
