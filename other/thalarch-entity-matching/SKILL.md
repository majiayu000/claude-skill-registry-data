---
name: thalarch-entity-matching
description: >
  Designs safe automatic entity-resolution and candidate-matching logic for searches such as
  title+artist to media ID, product to catalog item, album to provider entity, or similar fuzzy
  identity mapping. Use when a system must choose among near-duplicate remote search results without
  silently binding the wrong entity.
---

# Thalarch Entity Matching

Automatic identity resolution should optimize for correctness, not for always returning something.

## 1. Define the identity contract

Before scoring candidates, identify:

- the source identity fields;
- which fields are authoritative vs optional;
- which differences are harmless formatting changes;
- which differences change semantic identity;
- whether false positives or false negatives are more damaging;
- what fallback happens when no confident match exists.

For automatic playback/import/sync, a false positive is often worse than a clean miss.

## 2. Narrow server-side first

When the provider exposes a specific result class/filter/shelf, use it before local fuzzy scoring.

Examples:

- songs rather than mixed search;
- artists rather than generic web results;
- exact catalog type rather than all entities.

Do not compensate for an unnecessarily broad server query with increasingly fragile local heuristics.

## 3. Canonicalization

Reuse the project's existing normalization utilities before inventing new ones.

When needed, normalize deliberately:

- Unicode letters/numbers rather than ASCII-only `\w` assumptions;
- case;
- punctuation and spacing;
- canonical/compatibility forms where appropriate;
- diacritics only when the product's matching semantics permit it;
- common connector variants such as `&` / `and` when justified;
- artist lists and featuring syntax;
- token order when order is not identity-bearing.

Canonicalization must be idempotent and must not erase meaningful qualifiers.

## 4. Explicit qualifiers are intent

Terms such as `live`, `remix`, `acoustic`, `instrumental`, `radio edit`, `sped up`, or `remastered`
may distinguish versions.

Do not build a universal blacklist that automatically penalizes them. If a qualifier is present in
the requested identity, matching should normally preserve it. If it is absent, a candidate that adds
a materially different qualifier may deserve a lower score.

## 5. Candidate scoring

Prefer interpretable evidence over one opaque similarity number.

Score or gate independently where useful:

- title compatibility;
- primary/secondary artist compatibility;
- explicit-version qualifier compatibility;
- album/release context when available;
- duration tolerance when trustworthy;
- provider/entity type;
- exact token-set agreement vs partial overlap.

Do not let one strong field hide a contradiction in another load-bearing field.

## 6. Confidence and ambiguity

Define a confidence threshold from product risk and tests, not from a magical universal number.

A useful resolver can return:

- confident match;
- ambiguous candidates;
- no confident match.

An automatic identity resolver must be allowed to say **no confident match**.

When the top two candidates are effectively tied on load-bearing fields, prefer ambiguity/fallback
over silently choosing rank 1.

## 7. Stable retry/fallback behavior

If a retry or broader fallback is justified:

- preserve original input ordering;
- avoid duplicate matches;
- keep already-confident matches stable;
- bound concurrency and retries;
- stop retrying when rate limiting or a provider failure changes the evidence.

Do not interpret a transient provider failure as evidence that a candidate does not exist.

## 8. Test matrix

At minimum consider:

- exact title + artist;
- punctuation/case changes;
- accents/diacritics;
- non-Latin scripts;
- multiple artists / `feat.` variants;
- reordered harmless tokens;
- explicit live/remix/acoustic qualifier;
- wrong rank-1 result with correct later candidate;
- same title by different artist;
- same artist with materially different title;
- near-tie ambiguity;
- no acceptable candidate.

For normalization, property tests are valuable when tooling already exists: normalization should be
stable/idempotent and should not turn clearly distinct fixtures into the same identity unexpectedly.

## 9. Performance

Matching frequently runs on network result lists or import batches. Avoid:

- regex compilation per candidate;
- repeated Unicode normalization of the same source string;
- quadratic token work when sets/maps suffice;
- unbounded parallel provider requests.

Precompute reusable normalized source/candidate fields when the hot path warrants it and measurement
supports the optimization.

## 10. Evidence

Report what the tests prove and what they do not. A passing curated fixture set supports the known
matching contract; it does not prove provider ranking or metadata quality for every remote query.
