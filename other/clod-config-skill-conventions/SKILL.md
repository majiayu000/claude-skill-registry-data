---
name: "Config: Skill Conventions"
description: "Jason's placement, invocation and metadata conventions for creating or editing skills"
when_to_use: "Before creating or editing a skill: where it should live, who invokes it and how its model and metadata are set."
# No model/effort override: reference content that loads inline, where an
# override would downgrade the very session that's editing skills
disable-model-invocation: false # Claude must be able to load the conventions at the moment it's creating or editing a skill; read-only guidance needs no gate
metadata:
  family: clod-config
---

# Skill creation conventions

- All skills live in `~/.claude/skills/` as `SKILL.md` files.
- Command skills (invoked explicitly) get `disable-model-invocation: true`; knowledge skills (always available for reference, never directly invoked) get `user-invocable: false`.
- Exception: a command skill may set `disable-model-invocation: false` when its `when_to_use` describes a moment Claude recognises before the user does (stale PR description, post-merge status drift, "add this to the roadmap" phrasing) **and** the skill contains its own approval gate before anything irreversible. The gate is the safety net; without one, keep it `true`.

## Where to create a skill

1. Always create in the project-local `.claude/skills/` directory unless explicitly told to create it globally.
2. Check for naming conflicts with personal-level skills (`~/.claude/skills/`); personal scope shadows project scope.
3. Use the new frontmatter convention below when creating or editing skills; recognise the old convention when reading existing skills.

## Metadata convention (current)

Model and taxonomy live in real frontmatter, never in the `description` text:

```yaml
model: opus          # explicit on every command skill; omit on knowledge skills (inherit)
effort: high         # explicit on every command skill; omit on knowledge skills (inherit)
metadata:
  glyph: ᛟ           # mirrors the model: field; omit when model is omitted
  family: pr         # the skill's family prefix (pr, roadmap, doc, clod-lens, …)
```

| Glyph | Rune | Model |
|---|---|---|
| `ᚺ` | hagalaz | haiku |
| `ᛊ` | sowilo | sonnet |
| `ᛟ` | othala | opus |
| `ᚠ` | fehu | fable |

Knowledge skills (`user-invocable: false`) set neither `model` nor `effort`: both fields override the session absolutely while the skill is active, so an inline reference skill would hijack the very turn that triggered it.

## Model-tag conventions (old: recognise, don't write)

Retired forms that tagged the model inside `description` as `"{{ X }} …"`: Greek triples (`𝚫𝚫𝚫` haiku, `ƔƔƔ` sonnet, `𝛀𝛀𝛀` opus) and before that runic pairs (`ᚻᛕ` haiku, `ᛇᚤ` sonnet, `ᛜᚹ` opus, `ᚨᛔ` fable). On sight, migrate the skill to the metadata convention above.
