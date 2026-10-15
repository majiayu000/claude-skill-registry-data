---
name: skill-creator
description: Use when authoring a new skill. Standardized template + quality checklist.
---

# Authoring a new Claude Code skill

Skills are reusable, discoverable instructions Claude loads when it detects the right context. A good skill is narrow, triggered by a clear pattern, and short enough to read in one pass.

## When to write a new skill

Write a new skill only when ALL of these are true:

1. You have hit the same pattern at least 3 times. One-offs belong in a prompt or memory, not a skill.
2. No existing skill covers it. Search `~/.claude/skills/` and the bundled plugin skills first.
3. The pattern is general enough to apply across projects, or it is project-specific AND lives under that project's `.claude/skills/`.
4. You can write a one-sentence `Use when ...` trigger. If you cannot, the skill is too vague.

If a memory entry, a CLAUDE.md note, or a one-shot prompt would do the job, prefer that.

## SKILL.md structure

Every skill lives at `skills/<name>/SKILL.md` (kebab-case directory). The file has a YAML front matter block followed by markdown.

```
---
name: <kebab-case-name>
description: Use when <trigger>. <One short sentence on what it does.>
---

# <Human title>

<One-paragraph summary.>

## When to trigger
- Bullet list of concrete patterns.

## Workflow
1. Steps Claude should follow.
2. Be specific. No fluff.

## Red flags
- Patterns that mean STOP and reconsider.

## References
- Pointers to other skills, docs, files.
```

Target 100-250 lines of markdown. Below 80 lines usually means the skill is too thin to deserve its own file; above 500 lines means it is doing too many things and should be split.

## Writing the `description` field

The description is what the loader sees. It decides whether your skill triggers. Treat it as the contract.

Good descriptions:

- `Use when reading/writing docx/pdf/pptx/xlsx files. Prefer programmatic libs over shelling out.`
- `Use when building a new MCP server. Covers stdio vs HTTP, tool schema, error handling.`

Bad descriptions:

- `Helpful skill for files.` (too vague, no trigger)
- `Document tools.` (no `Use when`, no scope)
- `A comprehensive guide to ...` (marketing copy, not a trigger)

Rules of thumb:

- Start with `Use when ` followed by a concrete situation.
- Name the artifacts or commands involved (e.g. `docx`, `MCP`, `settings.json`).
- Keep it under 200 characters. The loader truncates long ones in practice.

## Directory layout

```
skills/
  <skill-name>/
    SKILL.md            # required
    <helper-files>      # optional: templates, snippets, reference docs
```

Helper files are fine but do not assume Claude reads them automatically. Reference them explicitly from `SKILL.md` with absolute or skill-relative paths.

## Testing a new skill

Before considering a skill done:

1. Ask a fresh subagent to read only your `description` field and a one-line task. Does it pick the skill? If not, the description is too weak.
2. Run a realistic task end-to-end. Does the workflow section actually unblock the work, or does Claude have to re-derive the same steps?
3. Re-read the skill in a week. If you do not remember what each section is for, it is too clever.

If steps 1-2 fail, edit the skill. If step 3 fails, shorten the skill.

## Updating an existing skill

- If two skills overlap, merge them or carve out a clean boundary in their `When to trigger` sections.
- If a skill keeps misfiring, tighten the `description` first - that is usually the fix.
- If a skill grows past ~400 lines, split it into a parent skill and child skills that the parent references.

## Red flags

- The skill describes a workflow Claude could derive from first principles in 10 seconds. Delete it.
- Two skills have descriptions that could plausibly cover the same task. Disambiguate or merge.
- `description` does not start with `Use when` or an equivalent trigger phrase.
- The skill is over 500 lines. Split it.
- The skill is under 50 lines and reads like a Twitter post. Either expand with real workflow content or fold it into a memory entry.
- The skill duplicates content already in CLAUDE.md or memory. Pick one home.
- The skill prescribes specific code rather than guidelines. Skills are for judgment calls; templates are for code.

## References

- Existing skills under `~/.claude/skills/`.
- `using-memory` skill - when to use memory instead of authoring a skill.
- `lean-context` skill - keep skills short so they do not eat the context budget.
