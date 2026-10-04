---
name: slop
description: Detect AI-generated design slop with concrete, locatable findings. Use when the user wants to check code for AI authorship tells, design inconsistency, or generic UI patterns. Each finding includes file, line, column, the offending snippet, why it's a problem, and a concrete fix. 12 rules covering shadow/radius variant explosion, AI-default gradients, lorem ipsum, inline styles, off-grid spacing (when a manifest exists), off-palette colors (when a manifest exists), tailwind class bloat, missing alt text, console.log leftover, emoji in headings, and transition-all defaults. Run as `node ~/.claude/skills/dragoon/skills/slop/scripts/slop.js [path]`.
version: 1.0.0
---

# /slop

The viral hook of dragoon. Detects the patterns that betray AI-generated UI: 7 different shadow values, generic violet-to-pink gradients, transition-all-duration-200 everywhere, lorem ipsum left in source, off-grid spacing, off-palette colors.

## When to use

Run /slop when:
- The user wants to check if code "looks AI-generated" or "feels off"
- Reviewing a PR or diff before merging
- After a feature lands, to catch slop before it ships
- The user says "find the slop", "scan for AI tells", "audit for design hygiene"

## How it works

12 deterministic rules. Each rule:
- Returns concrete findings with line, column, snippet, message, and fix
- Has a severity (low / medium / high)
- Is unit-tested

Two rules become **codebase-aware** when `dragoon.json` is present:
- `slop-006` spacing-off-grid uses your detected grid
- `slop-007` hardcoded-color-off-palette uses your detected palette

So /slop gives generic results without /scan, and project-specific results with it. Always run /scan first if you can.

## Run it

```
node ~/.claude/skills/dragoon/skills/slop/scripts/slop.js [path]
```

Flags:
- `--manifest <p>` use a specific dragoon.json (auto-detects ./dragoon.json otherwise)
- `--json` machine-readable
- `--severity <low|medium|high>` filter
- `--rules` list all rules and exit
- `--quiet` only show findings, no summary
- `--help` full usage

## Exit codes

- `0` no findings
- `1` findings present (good for CI gating)
- `2` bad usage

## All rules

Run `node ~/.claude/skills/dragoon/skills/slop/scripts/slop.js --rules` for the full list with descriptions.
