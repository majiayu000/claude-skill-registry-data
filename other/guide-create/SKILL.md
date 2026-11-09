---
name: guide-create
description: "Use when a project needs a guide of its own: a rule for how a kind of code is shaped while written, scoped to the files it governs. Produces the project's `guide-<name>` skill at `<repo>/.claude/skills/guide-<name>/SKILL.md`. Not for a repository-wide convention (write-conventions) and not for a skill that does work (write-skills)."
---

# Create a guide

A guide is a skill that loads on the files it governs and shapes code while it is written.

1. Settle with the person: what code it governs, the shaping step, what ok at merge means.
2. Write `<repo>/.claude/skills/guide-<name>/SKILL.md` in this shape:
   - frontmatter: `name: guide-<name>`; `description` the trigger only (what activates it, what it produces, what it excludes); `paths` a list of globs, **required**, the code files it governs, never docs (a guide for all code: `["**/*.{ts,tsx,js,py,go,…}"]`).
   - `**Applies**`: the code it covers, in one line.
   - `## Shaping step`: 3–5 numbered steps, done before the code; a skill it hands to, by name alone.
   - `## Ok at merge`: checkable lines a reviewer ticks.
3. Name no file, module or name a glob does not need; a guide outlives the code that prompted it.
4. Show the person the file; done on their yes.
