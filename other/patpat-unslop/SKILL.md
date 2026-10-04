---
name: patpat-unslop
description: Cut AI tells, superficial patterns, and fluff from text or diffs.
disable-model-invocation: true
---

# Patpat Unslop

Scan text, documentation, and diffs to remove artificial writing artifacts and fluff.

## Process

1. Scan text against the pattern catalog below.
2. Report concrete rewrite recommendations that preserve exact technical meaning with natural, concise phrasing.
3. Replace vague hand-waving with concrete references, code symbols, or numbers.

## Pattern Catalog

### Content and Substance

1. **Superficial participial clauses.** Eliminate ungrounded `-ing` trailing clauses such as *"highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering..."*. Replace with active statements or concrete causal evidence.
2. **Vague attributions.** Eliminate *"Industry standards suggest"*, *"Experts believe"*, *"Many developers prefer"*. Name the concrete specification, RFC, or team constraint, or delete the phrase.
3. **Empty summary filler.** Remove introductory or concluding cheerleading phrases like *"In summary, this change enhances stability"* or *"It is worth noting that..."*. State the technical fact directly.

### Language and Vocabulary

4. **Banned AI tropes.** Replace these inflated words with plain engineering terms:
   - *additionally* -> *also* or merge sentences
   - *crucial / pivotal* -> *required* or *necessary*
   - *delve* -> *inspect* or *investigate*
   - *enhance* -> *improve* or name the concrete modification
   - *foster* -> *allow* or *enable*
   - *intricate* -> *complex* or specify the architecture
   - *landscape* -> *context* or specify the system
   - *tapestry* -> delete
   - *testament* -> delete or cite the test/metric
   - *underscore* -> *show* or *confirm*
   - *vibrant* -> delete
5. **Fancy copulas.** Replace *"serves as"*, *"stands as"*, *"boasts"*, *"features"* with simple *"is"* or *"has"*.
6. **False contrasts.** Eliminate *"Not only X, but also Y"* structures. State both facts plainly.
7. **Rule-of-three bias.** Do not force lists or arguments into groups of three. Use the natural, accurate count.
8. **Synonym cycling.** Avoid rotating synonyms for the same entity (*"the caller, the invoker, the consumer"*). Pick the canonical domain term and stick with it.
9. **Fake ranges.** Eliminate *"from X to Y"* when X and Y are not points on a continuous scalar spectrum. Use an exact list.

### Style and Punctuation

10. **Em dash overuse.** Do not use em dashes (`—`). Use periods or commas only.
11. **Excessive bullet nesting.** Prefer flat, compact bullet points or code blocks over multi-nested outlines.
12. **Apologetic or sycophantic tone.** Never use *"Certainly!"*, *"I would be happy to..."*, or *"You are absolutely right!"*. State technical findings and decisions neutrally.
13. **Narrative code commentary.** Strip conversational commentary from code changes. Code should communicate via types, names, and explicit structure.
14. **Unproven claims.** Never state that a fix works or tests pass without attaching fresh, observable command receipts.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
