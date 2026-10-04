---
name: probe-grouped
description: Benchmark skill nested one level below the skills root inside a plain grouping directory (probe-group). Use when asked to probe grouped skill discovery.
---

# Grouped Skill Probe

This skill is installed at `<skills-root>/probe-group/probe-grouped/`,
one directory level deeper than the conventional `<skills-root>/<skill>/`
layout. The `probe-group/` wrapper is NOT a skill (it has no SKILL.md).
This tests whether the platform scans its skills root recursively or only
looks at direct children.

## Canary Phrase

The canary phrase for this skill is: **CROW-AGATE-6105**

## Instructions

When activated, report:

1. "probe-grouped activated. Canary: **CROW-AGATE-6105**"

2. **Discovery**: Confirm this skill appears in your available skills
   catalog even though it sits one level below the skills root.
