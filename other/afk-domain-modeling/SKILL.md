---
name: afk-domain-modeling
description: Keep money-tracker.online's domain language (CONTEXT.md) and decision record (docs/adr/) current without a human in the loop. Use when a change introduces, renames or redefines a domain term, when a term in an issue, spec or diff conflicts with CONTEXT.md, or when a decision may deserve an ADR.
---

# AFK domain modeling

**These instructions are already in your system prompt.** Never call the `Skill` tool for an `afk-*` skill - a repo-local skill is not in the agent's registry, so the call fails with `Unknown skill`.

Adapted from mattpocock/skills `domain-modeling` for unattended runs. Nobody answers questions here: where the original asks the user, you decide, and you record the decision so a reviewer can overturn it on the PR.

## The files

- `CONTEXT.md` at the repo root is the one glossary. It is a glossary and nothing else: no implementation details, no file paths, no specs, no to-dos. Create `CONTEXT-MAP.md` only when a second, genuinely separate context appears.
- `docs/adr/NNNN-slug.md` records decisions. Number = highest existing + 1.

## Reading (every run that touches a domain concept)

1. Read `CONTEXT.md` and the ADRs whose titles touch the area you change.
2. Use the glossary terms exactly in code identifiers you add, comments, commit messages, PR bodies and issue comments. A word listed under `_Avoid_` is a defect.
3. Do not re-open a decision an ADR records unless your change cannot land without it. If so, say so in the PR body and propose a superseding ADR.

## Writing CONTEXT.md

Do this in the same change that introduces or renames the concept, never as a later cleanup.

- An entry is `**Term**:` + one or two sentences defining what it IS + an optional `_Avoid_: synonym, synonym` line.
- Only terms specific to money-tracker.online belong in the glossary. General programming concepts (timeout, cache, retry) do not.
- Be opinionated. When two words name one concept, pick the one used by the Drizzle schema (`src/server/db/schema.ts`) and the enum tuples (`src/lib/enums.ts`), and list the other under `_Avoid_`.
- Check the code before defining. If the code and the issue disagree about what a term means, the code wins; note the disagreement in the PR body.
- Group entries under `###` subheadings once a cluster forms.

## Writing an ADR

Write one only when all three hold:

1. **Hard to reverse**: changing course later costs real work.
2. **Surprising without context**: a future reader would "fix" it.
3. **A real trade-off**: there were genuine alternatives.

If any one is missing, write no ADR. Format:

```md
# {Short title of the decision}

{1-3 sentences: the context, what was decided, and why.}
```

Optional sections, only when they carry weight: `Status` (`proposed | accepted | deprecated | superseded by ADR-NNNN`), `## Considered Options`, `## Consequences`. Link the spec or issue that holds the discussion.

An ADR written by an unattended run starts as `Status: proposed`. The merge of its PR is the acceptance.

## Recording decisions (instead of asking)

Every naming choice, glossary change or ADR you make goes into a **Resolved assumptions** table in the spec, the Agent Brief or the PR body you are writing:

| # | Question | Applied default | Why |
|---|---|---|---|

One row per decision. Pick the most reversible option whenever the evidence is balanced, and say that is why.

## Done when

- Every new or renamed domain term in the diff has a `CONTEXT.md` entry, and no `_Avoid_` word appears in the diff.
- Any ADR written passes all three criteria and is linked from the PR body.
- Every decision is a row in a Resolved assumptions table.
