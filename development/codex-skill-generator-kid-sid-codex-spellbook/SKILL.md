---
name: codex-skill-generator
description: Create or update Codex skills that follow the repository skill format, trigger cleanly, and stay concise. Use when adding a new skill, refining an existing SKILL.md, or converting domain guidance into an installable Codex skill package.
---

# Codex Skill Generator

Create focused Codex skills that trigger reliably, stay small, and encode reusable judgment instead of generic prose.

## When to Activate

- Create a new skill for this repo
- Refactor a large guidance document into a skill
- Tighten a weak `description` so the skill triggers correctly
- Convert AGENTS-style guidance into `skills/<name>/SKILL.md`
- Review an existing skill for format drift
- Add examples, tables, or a checklist to a thin skill
- Update the README inventory after adding a skill

## Build Order

| Step | Do |
| --- | --- |
| 1 | Pick one narrow domain with clear activation triggers |
| 2 | Write a dense `description` that says what the skill does, when to use it, AND when NOT to use it |
| 3 | Add 6-8 verb-led items under `## When to Activate` |
| 4 | Organize the body around decisions, examples, and checklists |
| 5 | End with a shipping-oriented checklist |
| 6 | Update the repo inventory and validation surface |

## Required Format

```markdown
---
name: kebab-case-name
description: Dense sentence that says what the skill does, when to use it, AND when NOT to use it (scope boundary). Codex uses this for implicit activation matching.
---

# Title

One-sentence summary.

## When to Activate
- Verb-led trigger

## Content Sections

## Checklist
- [ ] Shipping check
```

Rules:

- Folder name must match `name`.
- Frontmatter must contain only `name` and `description`.
- Put activation hints AND scope boundaries in `description`; that is what Codex matches against for implicit invocation.
- Include at least one decision or comparison table.
- Include at least one `BAD` / `GOOD` pair.
- Keep the body terse and directly operational.
- Optionally add `agents/openai.yaml` to the skill folder to set `interface` metadata, `policy.allow_implicit_invocation`, and `dependencies.tools` (e.g. required MCP servers).

## What Good Skills Contain

| Include | Why |
| --- | --- |
| Trigger language in `description` | Helps the skill load at the right time |
| Decision tables | Compress tradeoffs without bloating prose |
| Realistic code or command examples | Makes the guidance executable |
| A checklist | Gives Codex a final pass before finishing |

| Avoid | Why |
| --- | --- |
| Meta-commentary like "this skill covers..." | Wastes tokens and weakens the signal |
| Broad multi-domain sprawl | Makes triggering and usage fuzzy |
| Long essays | Consumes context without improving execution |
| Placeholder examples with no domain meaning | Low signal; hard to apply |

## BAD / GOOD Examples

BAD

```markdown
---
name: auth
description: This skill covers authentication.
---

# Auth Skill

This skill covers authentication patterns and best practices.
```

GOOD

```markdown
---
name: jwt-auth
description: JWT authentication patterns for token issuance, validation, refresh rotation, and authorization checks. Use when building or reviewing bearer-token auth flows in APIs or services. Do NOT use for session-cookie auth, OAuth provider integration, or mTLS.
---

# JWT Auth

Implement bearer-token auth flows with explicit validation and rotation rules.
```

BAD

```markdown
## When to Activate
- Coding
- APIs
```

GOOD

```markdown
## When to Activate
- Build a JWT login or refresh flow
- Review token validation or claim handling
- Add authorization middleware to an API
```

## Editing Workflow For This Repo

| Task | Action |
| --- | --- |
| Add a skill | Create `skills/<name>/SKILL.md` |
| Keep counts accurate | Update `README.md` |
| Keep CI aligned | Ensure `scripts/validate_skills.py` still matches format expectations |
| Match house style | Read `skills/api-design/SKILL.md` and `skills/coding-standards/SKILL.md` first |

## Checklist

- [ ] Skill name is kebab-case and matches the folder
- [ ] Description says what the skill does, when to use it, AND when NOT to use it
- [ ] `## When to Activate` has concrete verb-led triggers
- [ ] At least one decision or comparison table is present
- [ ] At least one `BAD` / `GOOD` example pair is present
- [ ] The body is concise and code-forward
- [ ] The checklist is written from a "before you ship" perspective
- [ ] README inventory is updated after adding the skill
