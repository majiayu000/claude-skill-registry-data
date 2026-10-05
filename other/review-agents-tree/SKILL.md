---
name: review-agents-tree
description: Audit the tracked `AGENTS.md` tree against best practices, write `.agents/AGENTS_TREE_REVIEW.md`, and propose cleanup, compaction, conflict resolution, or sharding when needed. May auto-apply only trivial non-semantic hygiene fixes.
---

# review-agents-tree

Manual durable-context hygiene pass.

Not a workflow gate.
Not a replacement for `distill-knowledge`.

Run this periodically to keep the tracked `AGENTS.md` tree lean, conflict-free, and aligned with current code/tests.

## Read first
- `../references/persistent-artifacts-contract.md`
- `../../references/communication-mode.md`
- root tracked `AGENTS.md`
- all tracked local `AGENTS.md` files under the repository
- tracked `AGENTS.override.md` paths only to detect misuse or drift; never treat them as canonical repo truth
- relevant code/tests only when a guidance conflict or staleness finding needs verification

## Scope
This skill owns:
- periodic best-practice audit of the tracked `AGENTS.md` tree
- writing `.agents/AGENTS_TREE_REVIEW.md`
- proposing cleanup, compaction, conflict resolution, and sharding plans
- auto-applying only trivial non-semantic hygiene fixes when they are clearly safe
- being the only non-distill skill allowed to touch tracked `AGENTS.md`, and only for those trivial non-semantic hygiene fixes

It does not own:
- writing `AGENTS.override.md`
- semantic doctrine changes without explicit human approval
- shard creation, shard moves, or meaning-changing conflict resolution without explicit human approval
- task-local packet work unless a current task explicitly asked for this audit as part of that packet

## Audit workflow
1. Discover the tracked tree.
   - Enumerate all tracked `AGENTS.md` files.
   - Note any tracked `AGENTS.override.md` files as likely hygiene smells.
   - Build the effective hierarchy from root downward.
2. Audit file shape.
   - Confirm every tracked `AGENTS.md` has `## Scope`.
   - Confirm section names stay canonical when present.
   - Flag missing, tautological, or low-value `## Scope` sections.
   - Flag `## Entrypoints` sections in deep leaf shards when they add no real wayfinding value.
   - Confirm other sections are present only when they contain real content.
   - Flag files that drift from canonical section names.
3. Audit lean-ness.
   - Treat broad overview prose, directory dumps, repeated boilerplate, and generic cookbook content as compaction smells.
   - Treat roughly 200+ lines as a review trigger for compaction or sharding, not an automatic failure.
4. Audit specificity.
   - Flag vague, non-verifiable instructions.
   - Prefer exact commands, stable owner/module names, hard constraints, and durable rationale.
   - Treat raw file-path links as a fragility smell unless they are unusually stable and clearly necessary.
5. Audit hierarchy quality.
   - Flag parent/child duplication when the child adds no meaningful specialization.
   - Flag local files that restate root doctrine instead of carrying only boundary-local guidance.
   - Flag guidance placed too high or too low relative to the stable owner boundary.
6. Audit conflicts and ambiguity.
   - Flag contradictory rules across parent/child tracked files.
   - Flag ambiguous wording that could lead different agents to make different choices.
   - Verify suspicious conflicts against code/tests before concluding.
7. Audit staleness.
   - Flag stale paths, commands, owner/module references, or other brittle anchors.
   - Flag entries that are now better encoded in code/tests and should be pruned.
8. Audit for task-state leakage.
   - Flag plan recaps, worklog residue, temporary migration notes, or current-task chatter that belongs in `.plans/*`, not tracked `AGENTS.md`.
9. Decide whether a trivial hygiene fix is safe.
   - Safe auto-fix classes:
     - section heading normalization to canonical names
     - whitespace / formatting cleanup
     - deduping exact duplicate bullets
     - removing obviously broken file references when the correct target is unambiguous
     - reordering within one section when meaning does not change
   - If any fix changes meaning, defers a judgment call, or changes topology, do not apply it automatically.
10. Write `.agents/AGENTS_TREE_REVIEW.md`.
    - Summarize current tree health.
    - Record any auto-applied hygiene fixes.
    - Emit concrete findings and approval-gated proposals.

## Findings categories
Use compact `AT#` findings.

Good finding classes:
- bloated file that should be compacted
- duplicated guidance across parent/child files
- conflict or ambiguity between tracked layers
- stale path/command/reference
- task-local residue leaking into durable context
- missing, tautological, or low-value `Scope`
- low-value leaf `Entrypoints`
- fragile raw file-path links
- file broad enough that sharding should be considered
- tracked `AGENTS.override.md` or override misuse smell

## Best-practice bar
A strong tracked `AGENTS.md` tree is:
- lean
- specific
- path-scoped by stable owner boundary
- conflict-free
- low-duplication
- explicit about commands/validation, constraints, and durable decisions only where needed
- consistently shaped, with a lean non-tautological `Scope` in every tracked file
- sparing with `Entrypoints`, mainly at root/hub levels
- resistant to path fragility

## Report shape
Default `.agents/AGENTS_TREE_REVIEW.md` should include:
- `Status:` `healthy` | `needs_cleanup` | `needs_approval_for_refactor`
- `Auto-applied hygiene fixes:`
- `AT# findings:` ordered by severity
- `Approval-gated proposals:`
- `Suggested next pass:` `no_op` | `compact_existing_files` | `apply_semantic_cleanup_after_approval` | `propose_sharding_after_approval`

## Do not
- treat `AGENTS.override.md` as canonical repo context
- auto-apply semantic changes
- auto-create new tracked shards
- auto-merge or move tracked shards
- rewrite guidance just to make it prettier
- preserve stale or redundant prose because it feels helpful

## Initiative-mode note
Initiative packets and child packets are not tracked durable memory. Review them only if a human explicitly asks how they should later distill into tracked `AGENTS.md`.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
