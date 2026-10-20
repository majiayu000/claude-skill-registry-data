---
name: spec-sync
owner: baseline
description: Bootstrap the central system spec at `docs/system/` for a repository that has never had one. Scans the governed surface, proposes a concept map clustered by directory, and materializes elements + shards ONLY after a human confirms that map. Use when adopting the baseline on an existing project, or when the corpus needs re-deriving from scratch. Re-runnable. Requires `memory.architecture_map.enabled` and a declared `governed_surface`.
disable-model-invocation: true
---

# spec-sync — derive the central system spec, then have a human curate it

A project adopting the baseline has no spec archive to migrate from. Measured on this
repository, **68% of governed files appear in no spec at all** — and a project that
never ran the spec phase has none. So the corpus is rebuilt from code, not imported.

What the machine does and what the human does is the whole design:

| Step | Owner |
|---|---|
| Scan the governed surface, cluster by directory, propose a concept map | machine |
| **Confirm or edit that map** | **human, always** |
| Materialize elements, derive edges, stamp digests, report coverage gaps | machine |

## Prereq

`project.json → memory.architecture_map.enabled` is `true` and
`memory.architecture_map.governed_surface` declares this project's roots. An absent
surface is a named error, never a default — a fallback would model the consumer's
`.claude/` and report total coverage over a surface that is not theirs.

## Steps

1. **Check the flag.**

   ```
   node .claude/skills/workspace/cli.mjs flags   # gates on memory.architecture_map.enabled — read the `architecture_map:` line
   ```

   `false` → stop and tell the user to enable it (and declare a governed surface) first.

2. **Propose the map.**

   ```
   node .claude/skills/workspace/cli.mjs sync --json   # wraps workspace/sync.mjs -> proposeMap (propose half only; runSync is not exposed)
   ```

   The proposal is a starting point, not an inference to trust. Directory clustering
   is deliberately plain because a human edits it next.

3. **Have the human confirm it — always.** Present the proposed concepts via
   `AskUserQuestion`: which clusters are real concepts, which should merge, which
   should split, what each is called. Concept membership is **authored**; this step
   has no skip and no `--yes`. An unattended run that inferred membership would undo
   the rule every prior decision in this lineage protects.

4. **Materialize what was confirmed.** `runSync` writes the confirmed concepts, derives
   one element per anchor, stamps digests, and returns coverage gaps. It refuses
   outright when no confirmation callback is supplied, and writes nothing before
   confirmation returns — a refused sync leaves the corpus byte-identical.

5. **Report the gaps.** Every governed file should resolve to at least one element.
   Surface what did not, and let the human decide whether to widen an anchor or accept
   the gap. Do not close a gap by inventing a concept.

## Constraints

- **Never infer concept membership.** Step 3 is unconditional.
- **Element ids are derived here**, because no human authored them — that is what
  `identity.deriveId` exists for. Ids stay authored wherever a concept file declares
  one.
- **Re-runnable.** Running again re-proposes from the current tree; materialization is
  idempotent.
- Writes only under `docs/system/`. It never writes memory, never touches a consent
  path, and never commits.
