---
name: skill-template
description: >
  Template for creating new CodeHands skills. Copy this directory
  and fill in all sections. Use when authoring a new skill.
version: 1.0.0
permissions:
  - fs.read           # Adjust to match your skill's needs
triggers:
  - context: "describe when this skill should activate"
  - command: "/your-command"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies: []
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: your-github-username
signed: false
---

## Overview

[1-2 sentences: What does this skill do? Why does it matter?]

## When to Use

- [Positive trigger: "Use when X"]
- [Positive trigger: "Use when Y"]
- NOT for [exclusion]
- NOT for [exclusion]

## Process

### Phase 1: [Name]

1. **[Action verb] [what to do].** [Why this matters.]
2. **[Next step].** [Details.]

### Phase 2: [Name]

3. **[Continue numbering].** [Details.]

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "[Excuse agents use to skip a step]" | [Factual rebuttal explaining why the step matters] |
| "[Another common excuse]" | [Another rebuttal] |

## Red Flags

- [Observable sign the skill is being violated]
- [Another sign]

## Verification

- [ ] [Exit criterion — must be verifiable with evidence]
- [ ] [Another criterion]

## See Also

- `codehands:[related-skill]` — [Brief description]
- `references/[related-reference].md` — [Brief description]
