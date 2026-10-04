---
name: probe-stray
description: Benchmark skill placed OUTSIDE any recognized skills directory, in the project tree. Use when asked to probe stray skill discovery.
---

# Stray Skill Probe

This is a valid, spec-compliant skill — but it is installed outside every
recognized skills root (e.g. at `<project>/probe-stray/` instead of
`<project>/.claude/skills/probe-stray/`). It tests whether platforms
discover SKILL.md files anywhere in the project tree, or only under their
designated skills directories.

## Canary Phrase

The canary phrase for this skill is: **MERLIN-GYPSUM-8852**

## Instructions

When activated, report:

1. "probe-stray activated. Canary: **MERLIN-GYPSUM-8852**"

2. **Discovery**: If you can execute these instructions via normal skill
   activation, the platform discovered a SKILL.md outside its skills root.
