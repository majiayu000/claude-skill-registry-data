---
name: agent-skills
description: Use when creating a new skill under .agents/skills/, editing an existing one, or deciding whether a technique deserves to become a skill at all - covers SKILL.md structure, the description field, and how to keep a skill discoverable and token-efficient.
---

# Agent Skills — Writing and Maintaining Skills

A skill is a reusable reference: a technique, pattern, or tool that a future agent session should be able to find and apply without re-deriving it from scratch. This skill is about authoring *other* skills in `.agents/skills/`.

## When to Create a Skill

**Create one when:**
- The technique wasn't obvious and took real effort to work out
- It will plausibly be needed again, in this repo or elsewhere
- It applies broadly, not to one specific file or one-off situation
- Other contributors (human or agent) would benefit from finding it

**Don't create one for:**
- A one-off fix specific to a single bug
- Something already well documented upstream (framework docs, official guides)
- A project convention that's mechanically enforceable — put that in ESLint config or a CI check, not prose
- A narrative about how a problem was solved once — skills are reusable guides, not incident reports

## Anatomy

```
.agents/skills/
  skill-name/
    SKILL.md              # required — the whole skill, if it fits
    reference.md           # optional — only for heavy reference material
    scripts/                # optional — only for reusable executable tooling
```

Flat, searchable namespace. Most skills in this repo need only `SKILL.md` — reach for a separate file only when something genuinely doesn't belong inline (a 300-line API reference, a script meant to be run rather than read).

## SKILL.md Structure

**Frontmatter — exactly two required fields:**

```yaml
---
name: skill-name-with-hyphens
description: Use when <specific triggering conditions>.
---
```

- `name`: letters, numbers, hyphens only
- `description`: third person, states **only when to use it** — not what it does or how. This is what an agent scans to decide whether to open the file at all.

**Why "when," never "how," in the description:** if the description summarizes the workflow, an agent can act on the summary and skip reading the actual skill — including the parts of the process the summary left out. Keep the description to triggering conditions; put the process in the body where it will actually get read before being followed.

```yaml
# Bad — summarizes the process, invites skipping the body
description: Use for code review - dispatch a reviewer, read findings, fix critical issues

# Good — only the trigger
description: Use when completing a task or before merging, to catch issues before they ship
```

**Body**, roughly in this shape:

```markdown
# Skill Name

## Overview
What is this, in 1-2 sentences. The core principle.

## When to Use
Concrete symptoms/situations that signal this applies (and, if non-obvious, when NOT to).

## Core Pattern / Process
The actual technique. Inline code for short patterns; a linked file for heavy reference.

## Common Mistakes
What goes wrong and the fix, ideally as a table.
```

## Discovery: Make It Findable

A skill nobody finds isn't a skill, it's dead prose.

- **Keywords matter.** Use the words an agent would actually search for: real error messages, symptom names, tool/command names — not just abstract category words.
- **Name by what it does or its core insight**, verb-first or gerund where natural: `systematic-debugging`, not `debugging-techniques`; `writing-plans`, not `plan-creation`.
- **Keep it lean.** SKILL.md content loads into context whenever the skill is used — every unnecessary paragraph is a tax on every future invocation. Cut narrative, cut redundant examples, keep one excellent example instead of three mediocre ones.
- **Cross-reference by name, not by force-loading.** Point at another skill in this repo by its path/name ("see the `verification-before-completion` skill under `superpowers/`") rather than inlining its whole content — that keeps each skill focused and avoids drift when the referenced skill changes.

## Writing Style

- Imperative voice for instructions ("Run the test", not "You should run the test")
- Explain *why* a rule exists, not just that it exists — a rule with a reason survives edge cases better than a bare "MUST"
- One complete, realistic, copy-adaptable example beats three generic templates
- Prefer tables for anything scannable (common mistakes, quick reference); prose for anything sequential

## Before Calling a New Skill Done

- [ ] `name` and `description` are both present and `description` states only *when*, not *how*
- [ ] The body would make sense to someone who has never seen this repo before
- [ ] No dangling references to files that don't actually exist in this skill's directory
- [ ] It's short enough that loading it doesn't dominate the conversation it's used in
- [ ] It was tried once for real, on a real task, before being trusted

## Updating an Existing Skill

Same bar as writing a new one. If a skill turns out to have a gap (an agent following it still got something wrong), that's a signal to tighten the skill itself — add the missing case, don't just fix it in code and leave the skill stale for the next session.
