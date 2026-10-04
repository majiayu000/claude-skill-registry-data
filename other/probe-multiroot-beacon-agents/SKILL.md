---
name: probe-multiroot-beacon-agents
description: Control beacon for the multi-root collision check, installed only under the AGENTS-root beacon path with no colliding name. Use when asked to probe the agents-root beacon.
---

# Multi-Root Beacon (Agents Root)

This skill lives at `.agents/skills/probe-multiroot-beacon-agents/` and
nowhere else, and no other skill shares its name. If it appears in the
catalog, the platform scanned `.agents/skills/`, so a missing
`probe-multiroot` variant from the same root was dropped by name, not
by the scan.

Beacon canary phrase: **DIPPER-LIMONITE-9106**

## Instructions

When activated, report: "probe-multiroot-beacon-agents activated. Canary: **DIPPER-LIMONITE-9106**"
