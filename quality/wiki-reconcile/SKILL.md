---
name: wiki-reconcile
description: Search, compare, and reconcile pending Yarbrain memory candidates with canonical semantic notes through reviewable patches. Use when processing inbox/memory candidates, resolving conflicting evidence, or applying an explicitly approved knowledge patch; do not capture sessions or promote procedures.
---

# Reconcile Wiki Knowledge

Maintain current understanding without erasing evidence. A candidate is a claim
to evaluate, not a fact to append.

## Search Before Write

Do not create a file under notes/ until all of these steps succeed:

1. Resolve ../../scripts/yarbrain.py relative to this SKILL.md.
2. Search by proposed title, entities, aliases, project, and distinctive phrases.
   Repeat searches and raise the result limit when five results cannot cover
   every plausible overlap.
3. Read every plausible overlap with the helper's read command.
4. Compare scope, dates, confidence, volatility, status, and provenance.

If search is unavailable or ambiguous, stop without changing canonical notes.

## Reconcile

Choose exactly one operation:

- NOOP when the current note already represents the candidate accurately.
- MERGE when the candidate adds compatible evidence or detail.
- SUPERSEDE when newer evidence replaces a time-sensitive claim.
- SPLIT when different projects, environments, users, or versions explain an
  apparent contradiction.
- CONFLICT when credible evidence disagrees and cannot yet be resolved.
- CREATE only when no existing note represents the concept.

Draft a focused patch before editing canonical knowledge. Hash the UTF-8 string
<candidate-id><newline><operation> with SHA-256 and use
proposal-<first-16-lowercase-hex-characters> as its ID and Markdown filename.
Digest the UTF-8 proposal body, excluding its digest field, with SHA-256, then
store it beside its candidate under inbox/memory/. Show the operation, every
target, search evidence, source episodes, changed current understanding,
history effect, and rollback steps. Store unresolved conflicts under
inbox/conflicts/. If the current request does not authorize a vault write, show
the draft without storing it.

Apply a patch only after explicit approval, including a request that clearly
names the reviewed proposal ID and digest. Any proposal change invalidates that
approval. For a multi-file change, require a working rollback mechanism and
restore the pre-edit state after partial failure. Preserve old provenance and
record corrected or superseded claims in History. A canonical note must contain
id, kind, scope, status, created, updated, verified_at, volatility, aliases, and
sources frontmatter plus Current understanding, Why, Edge cases, Evidence, and
History sections when those sections have content.

After an approved edit, read every target back and run lint. Restore the
pre-edit state when the patch introduced a lint failure; report unrelated
pre-existing issues separately. Mark the candidate reconciled with the applied
proposal ID and then rebuild INDEX.md. An index failure does not invalidate a
correct canonical edit because the index is derived; report it as stale and
leave the approved note intact.

If the canonical edit succeeds but the candidate status write fails, keep the
canonical edit, report incomplete finalization, and retry only the status write
after verifying the applied proposal. Do not apply the canonical patch again.

Never silently resolve a conflict, remove the only evidence copy, rewrite an
episode, or edit installed plugin skills.
