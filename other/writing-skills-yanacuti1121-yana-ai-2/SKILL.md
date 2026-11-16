---
name: writing-skills
description: "Use when creating a new YAMTAM skill. Triggers on: 'add a skill', 'create a skill', 'write a skill', 'new skill for X', 'make a skill that'. Enforces frontmatter shape, trigger-phrase quality, and lockfile registration."
---

# Writing Skills Skill

A YAMTAM skill is a reusable behaviour rule. Writing a bad skill wastes everyone's time.
This skill enforces the standard that makes skills discoverable and triggerable.

## Anatomy of a skill file

Every skill lives at: `core/skills/<skill-name>/SKILL.md`

### Required frontmatter

```yaml
---
name: skill-name          # kebab-case, matches directory name
description: "..."        # trigger phrase description — see quality rules below
---
```

### Required sections in body

```markdown
# [Title] Skill

[One sentence: what problem this skill solves and why it exists]

## When to use this skill
[Bullet list of triggers — be specific]

## [Main workflow / steps / rules]
[The actual content]

## What NOT to do
[Anti-patterns and common failure modes]
```

## Trigger phrase quality rules

The `description:` field is the most important part.
Claude uses it to decide WHEN to load this skill.

Good description:
```
"Use when user asks to review a diff or PR. Triggers on: 'review this',
'check my changes', 'code review'. Focuses on bugs and security."
```

Bad description:
```
"A skill for reviewing code."
```

Rules:
1. Start with "Use when..." — specify the situation
2. Include at least 3 trigger phrases in "Triggers on: ..."
3. Name what the skill does, not what it is
4. Under 2 sentences

## After writing the skill

1. Register it in `core/config/skills-lock.json` — add an entry manually
2. Run `bash core/scripts/update-skills-lock.sh` to compute and write the hash
3. Update `MANIFEST.json` skills count and `actual_present` list
4. Add trigger phrase tests to `core/tests/skills/test-skill-triggering.sh`
5. Run `bash core/tests/skills/test-skill-triggering.sh` — all tests must pass

## Checklist before done

- [ ] File at `core/skills/<name>/SKILL.md`
- [ ] `name:` matches directory name (kebab-case)
- [ ] `description:` has "Use when" + 3+ trigger phrases
- [ ] Body has "When to use" and "What NOT to do" sections
- [ ] skills-lock.json entry added
- [ ] `update-skills-lock.sh` run and hash updated
- [ ] MANIFEST.json count updated
- [ ] Trigger test added and passing
