---
name: glossary
description: Look up or update specs/glossary.md, the registry of Mathiz's first-class concepts. Use before naming a new type, table, event, API resource or UI term, and whenever a PR adds, renames, splits or removes a concept.
---

# Updating the glossary

`specs/glossary.md` exists so that each concept has **one name and one
implementation**. Look things up there before writing code; edit it when a
concept is added, renamed, split or retired.

## Is it a first-class concept?

Add an entry only if at least one is true:
- It has its own ent schema, event type, or public Go type that other
  packages use.
- It appears in an API path or response, a spec, or `docs/personas.md`.
- Parents or kids see it as a named thing in the UI.

Not glossary material: private helpers, generic programming terms, env
vars (CLAUDE.md), one-off config knobs.

## Do

- **Search first**, including synonyms and the "Homonyms & look-alikes"
  section. `grep -in "<word>" specs/glossary.md` plus a code grep for the
  idea, not just the word.
- **Reuse the existing name** in new code, API fields and specs, even if
  you'd have picked a different word.
- **Use the exact entry format** in the file: `### Term`, a 1–3 sentence
  definition (what it is plus its key invariant), `**Code:**` (1–3
  authoritative paths), `**Spec:**` link, and an optional `**Aka / don't call
  it:**` line.
- **Put it in the right domain section, alphabetically.**
- **Verify every `Code:` path exists** (`grep`/`ls`) before committing. Fix
  stale paths when you move code.
- **Update the glossary in the same PR** as the code or spec that changes the
  concept.
- **Add a Homonyms line** when your term means something else elsewhere
  (e.g. billing *plan* vs session *plan*).
- **Map kid/parent-facing copy** to its internal concept on the `Aka` line
  (e.g. "clue" → Question) instead of renaming internals to match the UI.
- **Mark draft-spec concepts** `(proposed, specs/NN)` and drop the marker
  when they ship.

## Don't

- **Don't add a near-duplicate.** If your idea is a variant of an existing
  concept, extend that entry (and the code) or explain the difference in
  both entries. Never create two entries for one idea.
- **Don't write essays.** Design rationale belongs in the spec; the glossary
  links to it.
- **Don't invent identifiers.** Every name in `Code:` must exist in the
  repo.
- **Don't delete an entry silently** when a concept is retired. Remove it
  in the PR that removes the code, and note the replacement on any entry
  that referenced it.
- **Don't rename a concept in the glossary alone.** A rename touches code,
  specs, API and docs together, or not at all.
- **Don't record volatile details** (counts, defaults, timeouts) unless
  they're an invariant. They go stale; point to the code instead.

## Checklist for a PR that adds a concept

1. The grep found no existing concept that already covers it.
2. An entry is added in the right section, alphabetically, in the house
   format.
3. The Homonyms section is updated if the word is overloaded.
4. The `Code:` paths and `Spec:` link resolve.
5. The spec and `docs/personas.md` (for a user-facing concept) use the same
   name.
