---
name: tech-stack-doc
description: Generate a concise tech-stack decision doc (chosen stack + rejected alternatives, tabular) for a project. Use when the user asks to document/write/create a tech stack, stack decision doc, or "tech-stack.md".
---

# Tech Stack Doc

Produce a single markdown doc capturing stack choices and why alternatives were rejected. Keep every reason to one line — no essays.

## Steps

0. If a project brief or similar context doc exists or is referenced, read it first.
1. Determine the layers relevant to this project (e.g. Backend, Frontend, Data persistence, Infra, CI). Don't force layers that don't apply.
2. For each component decision, pick one choice and a one-line reason.
3. For each choice, list the alternatives seriously considered and a one-line "why not" each.
4. Note any deferred/open sub-decisions at the bottom, if any.
5. Write to `docs/tech-stack.md` (or ask for the path if the project's doc conventions differ).

## Output format

```markdown
# Tech Stack — <Project Name>

| Layer | Component | Choice | Reason |
|---|---|---|---|
| <layer> | <component> | <choice> | <one-line reason> |

## Rejected alternatives

| Component | Option | Why not |
|---|---|---|
| <component> | <option> | <one-line reason> |

## Open sub-decisions

- <anything deferred, with a pointer to where it'll be resolved>
```

## Rules

- Column names above are fixed — reuse them verbatim across projects; only the row values change.
- One row per decision, one line per reason. Full sentences not required.
- Every "Choice" needs at least one row in "Rejected alternatives" unless it was genuinely uncontested (note why, e.g. "no viable alternative found").
- Omit the "Open sub-decisions" section entirely if there are none.
