---
name: maintain-glossary
description: >-
  Load this skill when a project's words need pinning down: a term with two senses, two words for
  one thing, or a new concept to name, settled in a committed GLOSSARY.md. Trigger on "what do we
  call X", "define our terms", "add this to the glossary", "these two words mean the same thing".
argument-hint: "[term ...]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Maintain the glossary

Keep one committed `GLOSSARY.md` in which each domain concept has exactly one word and one
definition. Done means every term in scope is either settled in the file or listed as open, and
the code or text that still uses a rejected alias is reported.

## Procedure

1. **Pick the terms**: the ones named, otherwise the terms that caused confusion in the
   conversation. Asked to start a glossary from scratch, list the domain nouns that recur in the
   docs, file names, and identifiers, and take the twenty used most.
2. **Gather the usages.** Grep each term and its likely aliases across the repo, code and prose
   alike. Read enough hits to see every sense in which it is used.
3. **Challenge the term.** Look for three faults: one word used in two senses, two words used for
   one sense, and a word whose everyday meaning misleads ("user" for a paying organisation). For
   each fault, propose one word and one definition, and ask the user to settle it when the choice
   changes meaning. A choice that is purely spelling or casing is yours.
4. **Write the entry** in `GLOSSARY.md` at the repo root, or under `docs/` when the repo keeps its
   docs there, in alphabetical order and the format under Output.
5. **Report the stragglers**: each file still using a rejected alias, as `path:line`. Rename
   nothing yourself. Renaming identifiers or rewriting prose is a separate change the user decides
   on.

## Rules

- Define in domain words, not implementation words: what the thing is to someone who never read
  the code. "An Order is a customer's request to buy one or more products", not "the `orders`
  table".
- One concept, one word. Every other word for it goes under _Avoid_.
- Leave out general terms any reader knows (API, database, commit). The glossary holds what is
  particular to this project.
- A term's definition changes only with the user's agreement, because code and documents were
  written against the old one.
- The reason a term was chosen, when it was a real trade-off, belongs in the Key Decisions log of
  ceh-codebase-explanation:document-architecture, not in the entry.

## Output

```markdown
# Glossary

**<Term>** — <one or two sentences: what it is, in domain words>.
_Avoid:_ <alias>, <alias>. _Not to be confused with:_ **<Other term>**.
```
