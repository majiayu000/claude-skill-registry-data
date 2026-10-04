---
name: writing-skills
description: >
  Guide for authoring new CodeHands skills. Use when creating a new
  skill, improving an existing skill, or contributing to the CodeHands
  framework. Covers skill anatomy, writing principles, testing, and
  the contribution process.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
triggers:
  - context: "creating a new skill"
  - context: "contributing to CodeHands"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

Skills are behavioral shaping code — they change how agents act, not just what agents know. Writing a good skill requires the discipline of writing good code: clear structure, testable outputs, and defense against misuse.

## When to Use

- When creating a new skill for CodeHands
- When improving an existing skill
- When reviewing skill contributions
- NOT for skill usage (see `codehands:using-codehands`)

## Process

### 1. Start from the Template

Copy `skills/_template/SKILL.md` and fill in all sections. Never write a skill from scratch — the template ensures you don't miss required sections.

### 2. Write the Description First

The description in YAML frontmatter is the most important text in the skill. Agents decide whether to activate a skill based on this text. Rules:
- Start with what the skill does (third person)
- Include trigger conditions: "Use when [X]"
- Maximum 1024 characters
- Do NOT summarize the process — agents may follow the summary instead of the full skill

### 3. Design the Process

The Process section is the heart of the skill. Each step must be:
- **Actionable** — "Run `npm test`" not "make sure tests work"
- **Verifiable** — Each step produces evidence of completion
- **Sequential** — Steps build on each other with clear gates

### 4. Write Anti-Rationalizations

For EVERY step an agent might want to skip, add an entry:

1. Think: "What would a lazy agent say to skip this step?"
2. Write the excuse in the Rationalization column
3. Write a factual rebuttal in the Reality column

This is the MOST IMPORTANT section. Skills without anti-rationalizations are requests, not rules.

### 5. Add Model Variants

Different models respond to different enforcement styles:
- **Claude**: Collaborative framing ("your human partner")
- **Gemini**: Structured checklists with clear gates
- **GPT**: Direct imperatives with MUST/SHALL language

Add `model_variants` to frontmatter with appropriate phrasing.

### 6. Test the Skill

Validate your skill:
```bash
bash tests/skill-format.test.sh skills/your-skill/
bash tests/frontmatter.test.sh skills/your-skill/SKILL.md
```

### 7. Keep Token Budget

- SKILL.md body < 2,000 tokens
- If a section exceeds 100 lines, move it to a supporting file
- Every section must justify its inclusion — if removing it wouldn't change agent behavior, remove it

## Writing Principles

1. **Process over knowledge.** Steps, not facts.
2. **Specific over general.** Commands, not advice.
3. **Evidence over assumption.** Every gate requires proof.
4. **Anti-rationalization as first-class.** Every skip-worthy step needs a counter.
5. **Progressive disclosure.** Entry point first, details on demand.
6. **Token-conscious.** Justify every section's inclusion.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "My skill doesn't need anti-rationalizations" | Every skill has skip-worthy steps. If you can't think of any, you haven't thought hard enough. Ask: "What would a time-pressured agent skip?" |
| "The process is obvious, I don't need detailed steps" | What's obvious to you is ambiguous to an agent. "Write good tests" is useless. "Run `npm test` and verify 0 failures" is actionable. |
| "Model variants are overkill" | Models are your users. Different users respond to different communication styles. 3 extra lines of YAML is not overkill. |

## Red Flags

- Skills without Common Rationalizations table
- Skills with vague process steps ("ensure quality")
- Skills that exceed 2,000 tokens without supporting files
- Description that summarizes the process (agents won't read the full skill)
- No Verification section

## Verification

- [ ] All required sections present (Overview, When to Use, Process, Rationalizations, Red Flags, Verification)
- [ ] YAML frontmatter valid with all required fields
- [ ] Description < 1024 chars, starts with what (not how)
- [ ] Every process step is actionable and verifiable
- [ ] Anti-rationalization table has 3+ entries
- [ ] Model variants specified
- [ ] SKILL.md < 2,000 tokens
- [ ] Cross-references use `codehands:` namespace
- [ ] Format tests pass

## See Also

- `docs/skill-anatomy.md` — Canonical specification
- `skills/_template/SKILL.md` — Starter template
- `codehands:using-codehands` — Framework overview
