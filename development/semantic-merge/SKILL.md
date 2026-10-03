---
name: semantic-merge
description: Semantic branch integration. Use before git merge, rebase, or cherry-pick, or when syncing branches where conflicts or overlapping intent must be resolved deliberately.
---

# Semantic Merge

Integrate branches by intent, not by lines: understand what each side was achieving, synthesize where both changes are valid, escalate decisions that change what the branch means to the user, leave a trail later agents can follow.

**Treat conflicts as intent conflicts first, line conflicts second.** Intent-changing conflicts always go to the user; implement their decisions, never override them.

## Choose a Mode

Load exactly the mode reference matching the call path:

- **Workflow sync author:** `references/workflow-sync-author.md` when `superintegrate` dispatches an agent to bring the current branch onto a confirmed base.
- **Workflow sync reviewer:** `references/workflow-sync-reviewer.md` when `superintegrate` dispatches a separate reviewer before maturation begins.
- **Standalone merge:** `references/standalone-merge.md` when this skill is invoked directly for a merge, rebase, cherry-pick, or branch sync outside the full integration workflow.

All modes walk §Semantic Coherence Checklist below.

## Shared Steps

### 1. Ground in repository state

Inspect before changing anything:

- Current branch, worktree status, and any ongoing merge / rebase / cherry-pick state.
- Merge base, incoming commit range, and the set of touched files.
- For workflow mode: the dispatched `BASE_REF`, `PRE_SYNC_BASE_SHA`, `BASE_HEAD_SHA`, and incoming range.

Dirty worktree with unrelated changes: stash them under a name before any sync operation and report the stash in the status return. Stop and clarify only when the repository is already mid-operation (unresolved merge, in-flight rebase, detached HEAD) in a way that makes intent ambiguous.

### Scope the merge first

Size the work from Step 1's conflict status, touched-file set, and incoming range before investigating intent in depth. A merge is **trivial** when all three hold:

- it applies with no conflicts,
- the incoming range touches no file the current branch also changed since the merge base, and
- nothing incoming renames, moves, or redefines an identifier, path, schema, or output that current-branch code references.

Trivial merge: land it and run the stale-reference sweep (Step 6) bounded to that near-empty reach — the sweep confirms the third condition held. Skip intent synthesis, the resolution plan, and escalation; they have no overlapping cluster to act on. Record a clean sync. Any condition failing — a conflict, an overlapping file, a rename reaching current-branch code — takes the merge at full depth. Unsure whether overlap or a rename reaches current-branch code: treat it as non-trivial.

### 2. Investigate intent on both sides

Read commit messages, diffs, and any task tree or docs for each side. Current-branch intent: the `superRA/` task tree in workflow mode, the branch name, commits, and diffs in standalone mode. Incoming intent: the commit range on the other side of the merge base.

**Classify each cluster of changes by role.** The role drives its resolution:

- **Behavior or API** — what the program does or how it is called. Synthesize when both sides extend behavior compatibly; escalate when they contradict.
- **Data or schema** — column names, file formats, key definitions, sample filters. Escalate before choosing — the user owns these calls.
- **Docs or narrative** — prose explaining intent. Prefer synthesis; rewrite stale claims from either side.
- **Generated outputs** — figures, tables, compiled artifacts, fixtures. **Regenerate** from merged sources rather than hand-edit either side's copy.
- **Tests** — including drift tests. Preserve both sides' assertions unless a meaningful result change justifies re-expecting; escalate result changes rather than silently updating.
- **Config or build** — dependencies, pipeline wiring, environment. Synthesize when additive; escalate when directions diverge.

Classify and execute within each role; intent-changing calls — data contracts, test expectations, outputs — go to the user.

### 3. Build a resolution plan

For each overlapping area, pick one of:

- keep incoming,
- keep current-branch,
- **synthesize** both (preferred when both are valid and compatible),
- **regenerate** derived artifacts from merged sources,
- escalate to the user.

Prefer synthesis over picking sides, regeneration over hand-editing generated files.

### 4. Escalate intent-changing choices

Ask the user before resolving — with intent and consequences, not raw diff chunks — when:

- both sides imply different valid intents,
- a conflict changes data contracts, inputs, test expectations, program outputs, or the meaning of a published result,
- task structure would change (routed through `superplan §User Feedback and Changing the Task Tree`),
- drift-test or result-level expectations would move because outputs meaningfully changed.

Fold every answer into the relevant task objective — rewritten self-sufficient with the new context — before committing the resolution. No task tree: record the decision in the sync commit body.

### 5. Resolve and land

Run the sync operation only after intent investigation. Resolve by the plan from Step 3. Preserve base-current deletions and relocations by default; restore branch-side content only when current-branch intent, an approved task objective, or a logged user decision justifies it.

**Land one merge commit plus N propagation commits as needed to reach semantic coherence.** Every commit leaves the tree passing the automated protection selected before Sync, or existing tests and drift tests when standalone. Per-commit protection-pass is the lower bound; the whole-mode stopping rule is §Semantic Coherence Checklist §Scope boundary.

Include the conflict resolution, resolved docs, and the mode-specific sync record with the commits producing them — commit messages plus task-local `## Sync Impact` sections in workflow mode, the commit body in standalone mode. Broader **codebase-coherence** work belongs to `refactor-and-integrate`. The sync record may capture context explaining the post-sync diff for later codebase review; it never carries unresolved semantic-merge work into Integrate.

### 6. Detect and resolve stale references

A "no conflict markers" check is not enough. Before returning, sweep the merge's semantic reach for stale references and resolve them:

- labels, identifiers, or variable names renamed on one side but still used on the other,
- paths or module locations moved on one side,
- docs and comments that reference the old shape,
- generated outputs that should have been regenerated,
- cross-file imports, registry entries, or config keys.

Run targeted checks for touched subsystems where cheap. Fix stale references following directly from the merge; defer broader codebase-fit work to `refactor-and-integrate`. Confirm the tree matches the integrated intent, not just a conflict-free state.

## Semantic Coherence Checklist

Semantic-merge is done when the merge's meaning is fully represented in the tree. The implementer walks this as a pre-handoff self-check; the reviewer walks what its focus covers. A merge scoped trivial per §Scope the merge first satisfies the intent-preservation and resolution items by construction — confirm the verification items and move on. `[BLOCKING]` items must be satisfied for the sync to be accepted; `[ADVISORY]` items are recorded and do not block.

**Intent preservation:**

- `[BLOCKING]` Incoming intent understood from commits, diffs, docs, and caller context.
- `[BLOCKING]` Governing baseline and direction identified before conflict resolution.
- `[BLOCKING]` Each overlapping cluster classified by role (behavior/API, data/schema, docs/narrative, generated outputs, tests, config/build) before resolution.
- `[BLOCKING]` No silent losses from either side; dropped hunks have a documented rationale.
- `[BLOCKING]` No silent restorations of base-current deletions or relocations in workflow Sync.

**Scope boundary (semantic coherence stopping rule):**

- `[BLOCKING]` Stale references within the merge's semantic reach are resolved (per Step 6).
- `[BLOCKING]` Generated outputs made stale by the merged sources are regenerated, or escalated per Step 4 and recorded when regeneration would change a meaningful result.
- `[BLOCKING]` Docs and comments that describe the merged code are updated to match.
- `[BLOCKING]` Existing protection passes on every commit landed by this skill (per Step 5).
- `[BLOCKING]` Broader **codebase-coherence** work is left to `refactor-and-integrate`; the sync record defines no unresolved semantic-sync targets.

**Intent integrity:**

- `[BLOCKING]` Intent-changing choices were escalated, folded into the relevant task objective, and implemented as stated.
- `[BLOCKING]` Data-discipline artifacts and drift tests were preserved.
- `[BLOCKING]` Meaningful result changes were not silently accepted or re-expected.

**Sync record:**

- `[BLOCKING]` Task files remain coherent after the sync when present.
- `[BLOCKING]` Task-structure changes were routed through `superplan §User Feedback and Changing the Task Tree` before adaptation proceeded.
- `[BLOCKING]` Affected tasks carry a `## Sync Impact` section (per `references/workflow-sync-author.md`) when workflow Sync leaves task-specific context needed to understand the post-sync diff.

**Verification:**

- `[BLOCKING]` Stale-reference sweep covered labels, paths, docs, and generated outputs — not just the absence of conflict markers.
- `[BLOCKING]` Targeted checks were run, or the sync record says why none applied.
- `[BLOCKING]` Dirty-state stash (when used) was reported in the status return so the user can restore it.

## Exception

Orchestrator-managed parallel worktrees bypass this skill. Branches matching `<current-branch>-agent/parallel/<slug>` merge with plain `git merge --no-ff`; the merge-guard hook exempts `*/parallel/*` source refs.
