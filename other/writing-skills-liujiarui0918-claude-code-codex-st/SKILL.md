---
name: writing-skills
description: Use when creating a new skill. Meta-skill with template + anti-patterns.
---

# Writing Skills

A skill is a focused, reusable piece of expertise that activates when its trigger fires. Write skills that are sharp, short, and unmistakable in scope. Vague skills never get invoked.

## Iron Law

**A skill description MUST start with "Use when..." and name a concrete trigger.** If the trigger is "use when coding," the skill is useless.

## Anatomy of a SKILL.md

```markdown
---
name: kebab-case-name
description: Use when <concrete trigger>. <One-line method or rule>.
---

# Human-Readable Title

One paragraph: what this skill is for, who needs it, what it replaces.

## Iron Law (or MUST)

The single most important rule. One sentence.

## When to use this

- Specific situation 1
- Specific situation 2

## When NOT to use this

- Adjacent skill that owns this instead → see [[that-skill]]

## The flow / checklist / phases

Step-by-step or bulleted, depending on the shape of the content.

## Red Flags

Concrete signs you're doing it wrong. Quoted phrases work well
("It should work", "I'll fix it later").

## Cross-references

- [[related-skill-1]] — why and when
- [[related-skill-2]] — why and when
```

## Description Rules

The `description` is what the skill loader matches against the user's intent. It MUST be:

- **Triggered**: starts with "Use when..." or "Use BEFORE..."
- **Specific**: names a situation, not a topic
- **Single-sentence**: one comma is fine, two is too many

| Bad | Why bad | Better |
|---|---|---|
| "For programming tasks" | Matches everything → matches nothing | "Use when diagnosing a bug. 4 phases..." |
| "Helps with git" | Topic, not trigger | "Use when starting a feature. Isolate in worktree." |
| "Code quality skill" | Vague + ambiguous | "Use BEFORE handing off. Self-review checklist." |

## Content Rules

- **100-250 lines** total. Shorter is fine. Longer means split it.
- **Concrete over abstract** — examples, commands, exact phrases.
- **Imperative voice** — "Run the test", not "tests should be run".
- **One iron law per skill** — if you have three, you have three skills.
- **Cross-reference, don't duplicate** — `[[other-skill]]` links to its home.

## Red Flags in skill design

- The description is broad enough to match any question → too general, split or sharpen.
- The skill is a tutorial / textbook on a topic → that's docs, not a skill.
- The skill has 10 sub-sections with no priority → no iron law, no teeth.
- You can't think of a "Red Flags" section → you don't have a strong enough opinion to write a skill.
- The skill references no other skill and is referenced by none → it lives alone, may be off-topic.
- You're tempted to add "..." sections → trim until the skill says one thing well.

## When a skill grows too big

Symptoms:
- Over 250 lines
- Multiple iron laws
- Sections that don't reference each other
- Description has to use "and" to cover scope

Cure:
- Split into 2-3 skills.
- One becomes the index/entry point that cross-references the others.

## When a skill is too small

Symptoms:
- Under 30 lines
- Could be a paragraph in another skill
- No real "flow" — just a rule

Cure:
- Fold into the nearest sibling skill.
- Or, merge several tiny skills into a checklist-style umbrella.

## MUST

- MUST name in `kebab-case` matching the directory name.
- MUST have a triggered "Use when..." description.
- MUST have at least one Iron Law / MUST / Red Flag section.
- MUST cross-reference any skill it relies on or depends on.

## Template starter

Copy this skeleton, fill in:

```markdown
---
name: your-skill-name
description: Use when <trigger>. <Rule>.
---

# Title

[2-sentence intro]

## Iron Law

[One sentence.]

## Red Flags

- [phrase or pattern]
- [phrase or pattern]

## Flow

1. [step]
2. [step]
3. [step]

## Cross-references

- [[related-skill]]
```
