---
name: tag-registry
description: Suggests and validates tags from the canonical registry (tags.md) to prevent tag sprawl and keep naming consistent. Use when creating a new post, during pitch generation, before publishing, or when the user asks about tags.
---

# Tag Registry Skill

Suggest tags from the canonical registry (`tags.md`). Prevent sprawl; keep naming consistent.

**Invoke when:** creating a new post, during pitch generation, before publishing, or when the user asks about tags.

## Responsibilities

1. Suggest 3–4 tags from `tags.md` — at least 1 Core Topic tag.
2. Warn on any proposed tag not in the registry.
3. Prevent duplicates (check aliases in `tags.md`).
4. Enforce naming standards (see `naming-standards.md`).
5. Ask the user about tag *intent*, not just topic — `Article` is for featured only; `OpenSource` requires actual code.

## Workflow

### 1. Read `tags.md`

Understand current approved tags per category.

### 2. Analyze post

Identify: primary topic → Core Topic tag; technical elements → tech/tool tags; domain; regional focus.

### 3. Suggest

```
Suggested tags:
1. [Core Topic]       — primary theme
2. [Technical/Domain] — specific area
3. [Technical/Domain] — additional context
4. [Regional]         — if applicable

All from the canonical registry.
```

If the topic *might* warrant a tag you're unsure about (`Article`, `OpenSource`, narrow ones), ask first — don't infer from topic surface.

### 4. Handle new-tag requests

```
⚠️  "[NewTag]" is not in the registry.

Similar existing tags:
- [ExistingTag1] — [description]
- [ExistingTag2] — [description]

Before creating, ask:
- Reusable across future posts?
- Specific enough to be useful, broad enough to recur?
- Does it exist under a different name?
```

Require explicit user confirmation before creating a new tag.

### 5. Validate

- ✅ 3–4 tags total
- ✅ At least 1 Core Topic tag
- ✅ Naming follows `naming-standards.md`
- ✅ No duplicate concepts
- ✅ All tags exist in registry OR user approved new tag

### 6. Add new tag to registry (only if approved)

Three atomic Edits to `tags.md`:

**a) Add under appropriate category** (Core Topics, Technical Topics, Legal Practice & Compliance, Tools & Frameworks, Regional Focus, Events & Communities, Content Type, Professional Topics).

**b) Update metadata header:**
- Bump "Last Updated" to today (YYYY-MM-DD)
- Increment "Total Tags"

**c) Append maintenance log:**

```markdown
### YYYY-MM-DD
- ✅ Added **[TagName]** tag to [Category] category
- **Justification**: [Why needed]
- **Reusability**: [Where else it will apply]
- **Total tags**: [Old] → [New]
```

## Naming quick reference

See `naming-standards.md` for full rules.

- **Multi-word:** PascalCase (`LegalTech`, `DocumentAutomation`)
- **Single words:** lowercase (`programming`, `python`)
- **Proper nouns:** proper case (`Singapore`, `ASEAN`)
- **Acronyms:** all caps (`AI`, `API`, `CLI`)
- **Never:** kebab-case, snake_case, underscores

## Integration points

- **`generate_a_pitch`** — suggest tags during pitch creation; ask intent questions first.
- **Pre-publish** — validate registry membership and naming before sending to Ghost.

## Files in this skill

- `SKILL.md` — this file
- `tags.md` — canonical registry
- `naming-standards.md` — naming conventions
- `validation-rules.md` — full validation ruleset (consult when edge cases arise)
- `README.md` — setup/operational reference (humans + Claude Code setup)

## Principles

- Default to existing tags. New tags require reusability across multiple future posts.
- Suggest, don't decide. Present options + rationale.
- Ask about intent when a tag's scope is ambiguous (Article, OpenSource).
