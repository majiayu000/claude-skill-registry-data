---
name: skill-design
description: "Author Agent Skills with progressive disclosure: thin SKILL.md, details in references, scripts for execution. Use when creating or reviewing any skill in this repo."
---

# skill-design

Match specificity to risk: thin entrypoint, conditional detail in references, determinism in scripts.

## Activate when

- Creating, reviewing, or refactoring a skill (any domain).

## Do NOT activate for

- Using a skill to do its task (activate that skill instead).

## Procedure

1. Scope: one verifiable job per skill; write the trigger (when) and non-trigger (when NOT) first.
2. Entry: keep SKILL.md short — purpose, procedure, decision criteria, verification. Move conditionals, tables, and long checklists to `references/`.
3. Scripts: put repeatable verification or generation in `scripts/`; document required tools and fallbacks.
4. Evaluate: draft → test prompts → variance analysis across runs → tighten the description until routing is stable.
5. Validate: frontmatter `name` (lowercase-hyphen) + `description` (what + when), relative links resolve, scripts execute.
6. Never fabricate APIs/flags/behavior; mark unverified claims explicitly.

## References
- Progressive disclosure: thin entrypoint, conditional detail in references, determinism in scripts — the same doctrine behind this repo's own layout.
