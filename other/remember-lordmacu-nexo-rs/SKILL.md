---
name: Remember
description: Memory hygiene workflow to classify, deduplicate, and promote durable knowledge across local memory layers.
requires:
  bins: []
  env: []
---

# Remember

Review memory-like artifacts and propose what should be kept, promoted, merged,
or removed. This keeps guidance accurate as the project evolves.

## Use when

- Memory instructions are drifting or conflicting.
- Team wants to clean stale guidance from old sessions.
- You need to promote stable patterns into durable docs.

## Do not use when

- There is no meaningful memory/context to review.
- User only needs a one-off answer (no memory maintenance).
- You are asked to auto-edit memory layers without confirmation.

## Input contract

- `review_scope` (optional): `workspace_docs`, `session_logs`, `both` (default `both`).
- `apply_changes` (optional): default `false` (proposal mode first).
- `priority` (optional): `conflicts`, `duplicates`, `promotions`, `all` (default `all`).
- `target_files` (optional): explicit files to inspect first.

## Parsing rules (priority order)

1. Use explicit structured args when provided.
2. Else infer from user phrasing:
   - "clean memory", "dedupe instructions" -> `priority=duplicates,conflicts`
   - "promote stable conventions" -> `priority=promotions`
   - "just review, don't edit" -> `apply_changes=false`
3. Defaults:
   - `review_scope=both`
   - `apply_changes=false`
   - `priority=all`

## Canonical workflow

1. **Collect sources**
   - Workspace memory docs (for example: `IDENTITY.md`, `SOUL.md`, `MEMORY.md`,
     `USER.md`, `AGENTS.md`) and session evidence when available.
2. **Classify entries**
   - durable convention, temporary note, duplicate, outdated, conflicting, ambiguous.
3. **Generate proposals**
   - promotions (move to durable location), cleanup (remove/merge duplicates),
     conflict resolution (which version wins + rationale).
4. **Present grouped report**
   - `Promotions`, `Cleanup`, `Conflicts`, `Ambiguous`, `No action`.
5. **Apply only with approval**
   - If `apply_changes=true`, execute approved changes and re-validate consistency.

## Guardrails

- Default to proposal mode; do not mutate without explicit approval.
- Never delete content that has unresolved ambiguity.
- Prefer reversible edits and clear provenance notes.
- Keep sensitive values out of memory docs; redact before proposing promotion.
- State uncertainty explicitly when evidence is insufficient.

## Output format

Always return:

- `status`: `proposed` | `applied` | `needs_user_input`
- `review_scope`: effective scope
- `promotions`: list with destination + rationale
- `cleanup`: duplicates/outdated removals or merges
- `conflicts`: contradiction list + recommended resolution
- `ambiguous`: items requiring user decision
- `next_action`: required unless `status=applied`

## Example

- `review_scope="both" priority="all" apply_changes=false`
