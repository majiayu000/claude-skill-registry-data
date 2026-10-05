---
name: case-data-material-planner
description: >-
  Prepares executable case preconditions and case-executable.md from a
  requirement or written cases. Internal case-material engine; enter
  through codexqa-testdata-generator so SKILL_DIR and adapters resolve.
license: Apache-2.0
---

# case-data-material-planner

One-stop material engine between case authoring and case execution.

- Build an optional business-context graph from requirements
- Parse entities and actions from each case
- Construct data and bind commands through adapters
- Emit `case-executable.md`

## How the work is divided

`scripts/pipeline.ts` owns orchestration. You supply judgment at three points
only — `parse-case`, `knowledge-build`, and `select-tool` — and the script does
construction, binding, linting, and writeback. This split exists because those
three stages need reading comprehension while the rest must be reproducible: a
case re-run tomorrow has to yield the same manifest, which is impossible if a
model re-derives each step. So when the runner exits asking for one of the three,
launch that Agent, merge its patch, and `--resume`; do not take over a stage the
script already implements (`invoke_entity.ts`, `bind_action.ts`,
`slot_render.ts`), and with 2+ cases go through the dispatcher so each case gets
its own `pipeline.ts` process.

## Hard constraints

These are the ones that silently corrupt output rather than failing loudly,
which is why they are worth stating:

- **Do not invent business IDs, amounts, or config values.** A plausible-looking
  ID makes a case that fails at execution time with no trace of where the value
  came from. When unsure, record `failReason` and let the gate surface it.
- **Parse before constructing.** Data needs come from the case's preconditions
  and steps; skipping parse means constructing something the case never asked
  for.
- **Keep `case-executable.md` business-only.** No `node` / `python` / `bash`
  invoke lines, no `skillRoot`, cwd, host, or mock-server ports — those live in
  `manifest.json` (`invokeCmd` / `filledCmd`). The case document is read by
  people and replayed in other environments, where local paths and ports are
  wrong or meaningless.
- **Persist every non-envelope business field**, not just the primary ID. A
  downstream step usually needs the attributes that came back with it, and
  re-fetching them is not always possible.
- **Respect the gates.** C3 stays blocking when lint-gate is abnormal, and the
  lint-gate loop runs at most 3 rounds before it must hand the decision to the
  user — an unbounded loop burns the run without converging.
- **During knowledge-build, describe the business, not a shopping list.** The
  graph answers "what does this domain look like"; deciding what data to prepare
  is the parse stage's job and doing it early biases the parse.

---

## Entry routes

After receiving the request, classify the input:

### Path A: requirement / design doc (+ cases)

1. Read `planner.md` and run `scripts/pipeline.ts`
2. Exit 12 → knowledge-build Agent, merge, `--resume`
3. Then parse (exit 11) or continue if cases were already parsed

### Path B: cases only (no requirement doc)

1. Read `planner.md` and run `scripts/pipeline.ts --case-id … --source …`
2. Reuse `./testdata/case-materials/business-context.json` via `--context` when it exists
3. Otherwise knowledge-build is skipped by the runner
4. Handle exit 11 (parse-case) then `--resume`. Construction, binding, and
   writeback stay inside `pipeline.ts` — do not take those stages over.

### Path C: batch (2+ cases)

When the user supplies **2 or more cases**:

1. Read `case-dispatcher.md` and follow it
2. One `pipeline.ts` process per case (parallel). Shared knowledge-build once
3. The user talks to the dispatcher, not a per-case Planner Agent

**Rule:**

- case count ≥ 2 → Path C
- case count == 1 → Path A or B

### Input sources (highest first)

| Priority | Source | How | Notes |
|---|---|---|---|
| 0 | Caller-supplied `sources[]` | Passed in the Task / delegate prompt | Each item is `{caseId, sourceType, sourcePath}`; skip interactive collection |
| 1 | Document URL | `doc_source.get(<ref>)` | Requirement / design / knowledge-base page |
| 2 | `planId` | `workspace_context.get_plan(<id>)` + `api_catalog.search_plan_changes(<id>)` | Plan detail and change APIs |
| 3 | Local file path | Read the file | |
| 4 | Pasted text | Use as-is | |

Priority 0 is an optional fast path. `sourceType` values:
`remote-case | local-file | planId | paste`.
They map to the four legal `caseSource.type` values.
Callers that omit `sources[]` still use priorities 1–4 interactively.

## Material gate (case source)

The prerequisite material is **the case pack**, not executor fields.

- **No case source** → ask for a file, paste, `planId`, or document URL. Do not invent case text. Do not start parse or construct.
- **Path A without cases** → finish knowledge-build, then **wait** for cases. Do not jump to invoke.
- **Path B** → at least one case is mandatory. `knowledge-build` may be skipped; parse may not.
- **Batch (2+)** → every listed case needs a resolvable source. Do not silently drop a case.
- After the user supplies cases, `--resume` `pipeline.ts`. Do not skip parse, invoke, or writeback.
- Executor / tool params inside pipelines follow the original fill rules (defaults for optional fields; do not invent core IDs). C3 / lint-gate stay blocking.

---

## Constraints

- Execution logic lives in `scripts/pipeline.ts`; `planner.md` is the host protocol
- LLM Agents allowed: `parse-case`, `knowledge-build`, `select-tool` only
- Do not skip C3; the happy path has zero human gates
- Lint-gate loop is at most 3 rounds
- Entities and actions are equal tracks; an empty track short-circuits
- `targetLocation` is the only bind to the original case text
- Action params: `paramsFromEntities` / `paramsFromGenerators` / `paramsFromPriorActions`
- Tool verify uses `tool_registry.query_input_list` (see `references/param-source-spec.md`)
- `businessContext = null` is a valid degraded mode
- Entities follow `constructionStrategy`: `tool-build` → `invoke_entity.ts`,
  `config` → `generate_config_commands.ts`, `static-value` → filled at parse,
  `runtime` → deferred to execution
- New scenes: drop a slot under pack `slots/` or `workspace.slot_roots`.
  `select_tool.ts` binds from `slot.yaml` (or inferred executors). Do not edit the selector

## Path roots

Two roots, and mixing them up is the most common failure here:

| Variable | Points at | Owns |
|---|---|---|
| `SUBSKILL_DIR` | directory of this file (`$SKILL_DIR/references/case-data-material-planner/`) | `scripts/`, `agents/`, `templates/`, `references/` — every relative path in this sub-skill |
| `SKILL_DIR` | the parent skill root that contains the top-level `SKILL.md` | `scripts/adapters/`, `scripts/search_data_build.ts`, `slots/` |

There is no `adapters/` folder under `SUBSKILL_DIR/scripts/`. Adapter calls go to
`$SKILL_DIR/scripts/adapters/cli.ts`.

## File layout

```
SKILL.md                    entry routing (this file)
planner.md                  host protocol for pipeline.ts
case-dispatcher.md          multi-case: one pipeline.ts per case
agents/                     LLM specs (parse / knowledge-build / select-tool)
  knowledge-build.md
  parse-case.md
  select-tool.md
  writeback.md              slot_render render rules, applied by the script
scripts/                    pipeline.ts + construct/writeback scripts
templates/                  manifest / cache / context templates
references/                 thresholds and contracts
```

## Outputs

- `./testdata/case-materials/business-context.json`
- `./testdata/case-materials/tool-binding-cache.json`
- `./testdata/case-materials/{case-id}/manifest.json`
- `./testdata/case-materials/{case-id}/case-executable.md`

## Dependencies

No private CLIs. All I/O goes through the parent skill's adapters
(`$SKILL_DIR/scripts/adapters/cli.ts`):

| Need | Adapter |
|---|---|
| Discover / install domain skills | `skill_marketplace` |
| Query / execute / publish tools | `tool_registry` |
| Discover HTTP APIs | `api_catalog` |
| Proven methods | `experience_store` |
| Documents | `doc_source` |
| Test-plan context | `workspace_context` |
| Case writeback | `case_writeback` |
| Config and SQL | `config_store`, `data_store` |

## Collaboration

This sub-skill is hosted by `codexqa-testdata-generator`. `select_tool.ts` reuses
`scripts/parallel_search.ts`, which calls the same adapters. Enterprise tools
are added through those adapters or a new slot under `slots/` /
`workspace.slot_roots` — `invoke_entity.ts` only dispatches on `toolType`.
