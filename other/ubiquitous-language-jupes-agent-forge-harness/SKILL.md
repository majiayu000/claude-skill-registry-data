---
name: ubiquitous-language
description: Extract a DDD-style domain glossary from conversation context, choosing canonical terms and flagging ambiguity. Use when the user asks to define domain terms, build a glossary, clarify terminology, create a ubiquitous language, or mentions domain modeling or DDD.
---

# ubiquitous-language

Extract domain terminology from the current conversation and turn it into a concise, shared glossary.

## When to use

- The user asks for a glossary, ubiquitous language, domain vocabulary, or terminology cleanup.
- A conversation uses multiple names for the same concept.
- A term appears overloaded, vague, or used differently by engineers and domain experts.
- The user mentions DDD, domain model, canonical terms, or language hardening.

## Process

1. Scan the current conversation for domain nouns, verbs, lifecycle states, roles, policies, and events.
2. Exclude generic programming terms unless they carry domain meaning in this context.
3. Identify terminology problems:
   - One word used for multiple concepts.
   - Multiple words used for the same concept.
   - Vague, overloaded, or implementation-shaped names that hide the domain idea.
4. Choose canonical terms. Be opinionated, but preserve important aliases as "aliases to avoid" or "also called" notes.
5. Group terms by natural domain area, actor, lifecycle, or process.
6. Describe relationships between canonical terms, including cardinality when it is clear.
7. Include example dialogue that shows a developer and domain expert using the terms precisely.
8. Flag remaining ambiguities with a recommendation or a question for the user.

## Persistence

Default to inline output in the conversation. Do not create a file unless the user asks for one or asks for durable repo knowledge.

When durable knowledge is requested:

- Use the explicit target file or location the user names.
- Prefer `bd remember` for durable agent knowledge when that is the intended persistence mechanism.
- Prefer existing `knowledge/` conventions for repo-level domain knowledge.
- Do not create `MEMORY.md`, task-list markdown files, or unrequested permanent documentation.

## Output format

Return a glossary in this shape:

```md
# Ubiquitous Language

## <Domain Area>

| Term | Definition | Aliases to avoid |
|------|------------|------------------|
| **Canonical Term** | One-sentence definition of what the concept is. | Old name, vague synonym |

## Relationships

- A **Canonical Term** belongs to exactly one **Related Term**.
- A **Process** may produce one or more **Events**.

## Example dialogue

> **Dev:** "When does a **Canonical Term** become a **Related Term**?"
>
> **Domain expert:** "Only after the **Policy** accepts it. Before that, it is still a **Draft Term**."

## Flagged ambiguities

- "account" was used for both **Customer** and **User**. Use **Customer** for the buyer relationship and **User** for authentication identity.
```

## Canonicalization rules

- Keep definitions tight: one sentence, focused on what the concept is.
- Prefer domain language over class, module, endpoint, or UI labels.
- Use singular nouns for entities and clear verb phrases for domain actions.
- Preserve useful synonyms only as aliases; do not let them compete with the canonical term.
- Call out unresolved ambiguity instead of silently choosing when evidence is weak.
- Avoid inventing terms that are not grounded in the conversation unless clearly labeled as proposals.

## Re-running

When invoked again in the same conversation, update the glossary rather than starting over:

1. Reuse the previous inline glossary or the explicitly requested durable target.
2. Add new terms from subsequent discussion.
3. Revise definitions when the domain understanding has changed.
4. Re-check aliases, overloaded terms, and ambiguous phrases.
5. Refresh relationships and example dialogue so they include the latest canonical terms.
