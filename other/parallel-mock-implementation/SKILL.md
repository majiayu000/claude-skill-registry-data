---
name: parallel-mock-implementation
description: Pattern for parallelizing emule mock authorship via the Workflow tool. Spawn one sub-agent per file in isolation; the orchestrator handles centralized finalization (wiring, build, test, promote). Invoked from `/implement-mock` (Strategy A batching) and `/compute-llk-bringup` (shim sweeps).
---

# Parallel mock implementation

This is a **building block**, not a standalone bring-up workflow.
Invoke it as part of `/implement-mock` or `/compute-llk-bringup` when
the work-list is large enough to amortize the dispatch overhead.

## When to use

- ≥4 similar files to author (e.g. a batch of SFPU shims, a sweep of
  missing NOC overloads, a fanout of fabric primitives).
- Each output is **independent** — one file per worker, no shared
  edits, no read dependencies between workers.

Don't use it for:
- Single-file work — call the worker prompt directly inline.
- Cross-cutting wiring that touches a shared file (e.g. one
  `sfpu_split_includes.h`, one `.claude/references/structure.yaml`). The orchestrator
  handles those centrally after workers return.

## Worker prompt skeleton

Each worker writes exactly one file. Customize the constraints for
your scope; the structure below stays the same.

```
You are implementing an emule mock for tt-emule. Write exactly ONE file.

TARGET FILE: <relative path under include/jit_hw/ or src/>
UPSTREAM REFERENCE (read-only): <path to the silicon API definition>
ADDITIONAL REFERENCE (read-only, optional): <e.g. LLK impl, RTL spec>
REFERENCE EMULE FILES (read for boilerplate):
  <path to an existing similar mock — keep this list short>

REQUIRED SIGNATURES (mirror upstream — if upstream differs, follow upstream):
<list>

SEMANTICS:
<formula / contract>

HARD CONSTRAINTS:
- Do NOT modify any file other than the TARGET FILE.
- Do NOT touch shared wiring files (the orchestrator handles those).
- Do NOT run pytest, build, or commit.
- Read at most 3 files: upstream, optional second reference, one
  existing mock as boilerplate.
- (Add scope-specific exclusions — e.g. for compute shims:
  "Do NOT read tt_metal/llrt/, tt_metal/impl/dispatch/,
  tt_metal/soc_descriptors/".)

OUTPUT: write the file, return status=DONE with file=<relative path>
and lines=<count>.
If signature is ambiguous or upstream missing, return status=STUCK with
a one-sentence reason.
Do NOT invent signatures.
```

## Result schema

```js
const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: ['DONE', 'STUCK'] },
    file:   { type: 'string' },
    lines:  { type: 'integer' },
    reason: { type: 'string' },
  },
  required: ['status', 'file'],
  additionalProperties: false,
}
```

## Orchestration

```js
phase('Write mocks')
const results = await parallel(ITEMS.map(it => () =>
  agent(makePrompt(it), {
    label: `mock:${it.name}`,
    phase: 'Write mocks',
    schema: RESULT_SCHEMA,
  }).then(r => ({ item: it.name, ...(r || {status: 'NULL'}) }))
))
const done  = results.filter(r => r.status === 'DONE')
const stuck = results.filter(r => r.status !== 'DONE')
log(`${done.length}/${ITEMS.length} DONE; ${stuck.length} STUCK`)
return { done, stuck }
```

## Orchestrator finalization

After the workers return, the orchestrator (you) handles centrally:

1. Visual diff each new file.
2. Wire any shared aggregator/registration file (e.g. for compute LLK
   shims: `SFPU_OP_*_INCLUDE` branches in `sfpu_split_includes.h`).
3. Update `.claude/references/structure.yaml` with one line per new file (per `CLAUDE.md`
   project rule).
4. Build.
5. Run targeted tests for each new mock — this loop can itself
   parallelize via one pytest call per item.
6. Promote 100%-pass entries into the regression script (e.g.
   `scripts/run_ttnn_pytests.sh` for compute LLK shims).
7. For partial passes, decide per-item: pytest `-k` filter, or defer
   with a written note.

## Anti-patterns

1. **Don't have parallel workers touch shared files.** Each worker
   owns a unique target path; the orchestrator centralizes wiring
   after the batch returns. Without this, you get racing writes that
   silently lose changes.
2. **Don't skip the `STUCK` branch.** When a worker hits ambiguity it
   must report STUCK with a reason; the orchestrator decides how to
   resolve (e.g. surface to the user, drop the item, hand-write it).
   Workers that "guess" produce subtle bugs that surface much later.
3. **Don't bypass the schema.** Free-text worker output is unparseable
   at scale. Even a STUCK item needs structured `{status: STUCK,
   file: <intended path>, reason: <one sentence>}`.
4. **Concurrency cap is automatic.** The Workflow runtime limits
   concurrent `agent()` calls (typically ≤16); excess queue up. Don't
   manually batch in chunks unless you have a reason — `parallel()`
   over the full work-list is fine.
