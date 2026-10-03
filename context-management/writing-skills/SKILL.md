---
name: writing-skills
description: Author or improve any .claude asset — skills, agents, hooks, CLAUDE.md sections — following Anthropic's authoring rules and the modern prompt-engineering lexicon. Use proactively whenever creating or editing files under .claude/, or when the user says "new skill", "improve this skill", "write an agent", or "add a hook".
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Writing Skills (meta-skill)

Keeps every future `.claude` asset consistent with the system that exists. Read `learnings.md` beside this file first.

## Governing Principle

> **The context window is a public good, and the model is already smart.** Every line must justify its token cost. Write at the right altitude: specific enough to steer, free enough that intelligence dominates.

## Procedure

1. **Read the deep rules first** — `references/skill-authoring-rules.md` (frontmatter constraints, description patterns, progressive disclosure, degrees of freedom, hook semantics, agent fields). Non-negotiable before writing.
2. **Compress with the field's vocabulary** — `references/prompt-engineering-lexicon.md`. Standard terms (plan-then-execute, verifier/generator split, rubric-based evaluation, chain-of-verification) carry shared meaning; use them instead of paragraphs. Gloss any loose term in five words.
3. **Evaluation-driven**: before writing a skill, name 3 concrete scenarios it must improve. If you can't, the skill documents an imagined problem — don't write it.
4. **Structure**: lean SKILL.md (router + procedure + constraints, well under 500 lines) → depth in `references/` (one level deep, TOC if >100 lines) → determinism in scripts. Add a `learnings.md` and wire it ("read before starting, append after surprises").
5. **Calibrate degrees of freedom**: review/design skills = high freedom (principles, rubrics); auth/migrations/format = low freedom (exact commands, "do not modify").
6. **Test with fresh eyes**: after writing, re-read as a cold model — does the description alone tell you when to fire? Does the body assume context that won't exist?

## Constraints

- Descriptions: third person, "pushy" (explicit trigger nouns/verbs — models under-trigger), state what it does AND when to use it, ≤1024 chars.
- Names: lowercase-hyphen, gerund-friendly, no reserved words.
- Never bake in time-sensitive facts (model IDs, versions) without marking where to re-verify them.
- One term per concept everywhere (semantic anchoring — consistent naming so the model binds one meaning).

## Handoffs

- New reviewer dimension → also update `/full-review`'s dispatch list. New hook → verify settings.json wiring and exit-code semantics against the rules reference.
