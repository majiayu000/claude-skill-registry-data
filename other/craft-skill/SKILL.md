---
name: craft-skill
description: How to craft an atomic skill. Includes templates and registration.
---

# Skill: Craft Skill

> "Atomic units of intelligence."

## The Principles

- **Atomicity**: One concept per file. If it does two things, split it.
- **Brevity**: Less is more. No verbose explanations.
- **Expertise**: Write *how an expert thinks*, not checklists.
- **Eighty lines, and it is ours**: front matter and all. Anthropic's published ceiling is 500, for
  performance. Eighty is stricter and answers two questions it does not. A skill is read into
  attention whole, so its length is what crowds out the next one — **and a person has to read it
  too.** Eighty is a screen. Past it, a skill is two skills.
- **Atomic examples**: one subject per file, named for it. Anthropic calls this **progressive
  disclosure**, and adds the rule that matters — **references stay one level deep from `SKILL.md`**,
  so a file it sends you to is read whole rather than chased.
- **The listing cuts at 1,536 characters**: `description` and `when_to_use` are joined, then cut
  there. Put the main use first.
- **Trigger phrases go in `when_to_use:`, and there is no `trigger:`**: Claude Code appends
  `when_to_use` to the description in the listing. It ignores a key the field list does not name,
  and claude.ai refuses that key on upload. Three skills here carried `trigger:` and nothing ever
  read a word of it.

## Choose a Template

| Template                                            | Use When            | Pattern                                |
|-----------------------------------------------------|---------------------|----------------------------------------|
| [decide](templates/decide.md)                       | X vs Y decision     | Heuristic + Quick Test + examples.md   |
| [craft](templates/craft.md)                         | How to build X      | Standard + Anti-Patterns + examples.md |
| [ground-protocol](templates/ground-protocol.md)     | Step-by-step ritual | When + Protocol + Output               |
| [ground-philosophy](templates/ground-philosophy.md) | Mindset/standards   | Standard + Check + examples.md         |

## The Structure

```
plugins/{plugin-name}/skills/{skill-name}/
├── SKILL.md        # The skill definition
├── shape.md        # One subject per file, named for it
└── traps.md        # Another subject, another file
```

**Naming**: Flat directories with prefix. `ground-vue/` not `ground/vue/`.

**Path**: Skills live at `plugins/{plugin}/skills/`, not `.claude-plugin/skills/`.

**plugin.json**: Uses `"skills": "./skills/"` (resolved relative to plugin root).

## Official Spec

The field list lives at https://code.claude.com/docs/en/skills. Fetch it rather than trusting the
numbers above. They were read there on 2026-09-29, and the ones they replaced were five weeks old
and wrong.

## Preloading

> [!IMPORTANT]
> **`skills:` is a preload list, not an allowlist.**

An agent's `skills:` frontmatter injects the **full skill content** into its context at startup.
Omitting a skill does not deny it — sub-agents can still invoke any project, user, or plugin skill
through the `Skill` tool at runtime.

So register deliberately, not defensively:

| Preload it | Leave it out |
|------------|--------------|
| The agent needs it on **every** run | The agent needs it occasionally |
| Fetching it late would change the output | A `Skill` call at the right moment is fine |
| It defines the agent's standards or vocabulary | It is reference material |

Every preloaded skill is startup context the agent pays for whether or not it uses it. A long
`skills:` list is a cost, not a safety net.

**Add to `agents/architect.md`** when the architect genuinely needs it loaded — not as a formality.
