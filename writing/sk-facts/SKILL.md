---
name: sk-facts
description: Researches, verifies and records the factual claims of a short in the fact ledger (docs/facts/facts.json and sources.json), including the licence of every image, clip and dataset. Use when the user says "check this fact", "is this true", "find a source for", "research the topic", "add to the ledger", "where does this number come from", "can I use this photo", or when lint reports a missing or unverified fact. Step 2 of sk-pipeline, and the step to return to whenever a number changes.
---

# sk-facts: source, verify, record

**Announce:** "Using sk-facts for <topic>."

Rules: §9 (`docs/soul/07-facts.md`); schema in `docs/facts/README.md`. Read the
schema before writing the first record. The § wins over this file.

**Core principle: research that exists only in prose cannot be re-checked.** The
output of this skill is records in two files, not a paragraph in a brief:

- `docs/facts/facts.json`: one record per claim:
  `{ "id": "f-0001", "claim", "value", "status": "verified|contested|unverified", "sources": ["s-0001"], "caveat", "checkedAt": "YYYY-MM-DD" }`
- `docs/facts/sources.json`: one record per source:
  `{ "id": "s-0001", "title", "url", "publisher", "licence", "accessed": "YYYY-MM-DD" }`

## Steps

1. **Search the ledger before researching.** `grep -i "<keyword>" docs/facts/facts.json`.
   Re-researching a claim already recorded wastes a session; re-using a claim
   already found wrong is worse.
2. **Split the claim from the number.** Write it as subject, measure, where, when
   ("river X, width, at point Y, dry season"). A claim that cannot be pinned to a
   place and a time is not checkable: pin it or cut it.
3. **Source in tiers.**
   1. Primary or institutional: the original paper, agency, statistics office,
      official record, the document itself.
   2. Encyclopaedic: follow through to *its* citation and read that.
   3. Popular articles and listicles: use them only to find candidates. Two
      tier-3 sources agreeing is still tier 3.
   Follow laundered claims to the end. Ten blogs copying each other are one
   source; if the chain ends at nothing, drop the claim.
4. **Read the original wording yourself.** Summarisers and extraction tools keep
   the number and drop the hedge: "probably reduced" becomes "reduced". That turns
   a model estimate into a measurement, and nothing downstream catches it because
   the number is still right. `claim` and `caveat` are written from text you read.
5. **Flag hypotheses as hypotheses.** Superlatives ("largest", "only", "first")
   almost always have a competing definition: state it or drop the superlative.
   "Recently discovered" and anniversaries: check the year.
6. **Write the record, whatever the answer.**
   | status | meaning | on screen |
   |---|---|---|
   | `verified` | you read it in the original | yes |
   | `contested` | real but sources disagree, or common phrasing is wrong | only with a `caveat`, and say it in the caption (`sk-handoff`) |
   | `unverified` | not checked yet | no; lint blocks it |
   A claim you proved wrong is still worth a record with a `caveat` saying so: a
   popular belief that is false is often the best hook, and the record stops
   someone re-researching it later.
7. **Record every image, clip, font and music track as a source** with its exact
   `licence` string (e.g. "CC BY 4.0", "public domain", "CC0", "licensed: <terms>").
   Take attribution text verbatim from the provider; it often carries a year or
   author that is part of the requirement. Prefer public domain and CC0; CC BY
   needs a credit line (on screen or in the pinned comment). Never use imagery
   whose terms you have not read, including map tiles and stock sites' previews.
8. **Link narration lines to facts.** Each line that states a fact carries
   `"fact": "f-xxxx"` in `src/videos/<id>/narration.json`.
9. **Validate.**
   ```bash
   bun run facts        # ledger schema, ids, source references
   bun run lint <id>    # every referenced fact exists and is verified (contested needs caveat)
   ```

## Verify

- [ ] ledger searched before researching
- [ ] every on-screen or spoken number has a `verified` record (or `contested` + caveat)
- [ ] no claim rests only on a tier-3 source
- [ ] every `url` in sources.json was actually opened this session
- [ ] every image and audio asset has a source record with a licence
- [ ] `bun run facts` exits clean, with no new warnings
- [ ] anything that could not be verified was cut, not softened into vagueness

Next: back to `sk-brief` (or `sk-narration` if the brief exists).
