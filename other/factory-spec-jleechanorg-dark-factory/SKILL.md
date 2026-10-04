---
name: factory-spec
description: "Dark Factory two-phase spec workflow (/factory-spec, /fs): create a main spec (spec.md) AND an attractor spec (attractor_spec.md) via the spec_gen pipeline, review an existing spec of either kind, or display the pipeline node graphs — spec-review pipelines, factory gates, node types, edge conditions, handler mappings. Create mode runs dark-factory --pipeline slim/spec_gen.dot; both the main and attractor specs must be codex-cold-reviewed and pass before exit. Review and show modes are in-session only."
---

# /factory-spec — Dark Factory Spec Workflow & Node Graph Reference

## Install vs source

Dark Factory runs via the **`dark-factory` binary**, not `python -m runner` from
a raw checkout:

```bash
~/projects/dark-factory/install.sh
export DARK_FACTORY_HOME=~/projects/dark-factory
export PATH="$HOME/.local/bin:$PATH"
```

- **`/fs` / `/factory-spec`** — spec creation (via pipeline), review, or graph reference.
- **`/f` / `/factory`** — run feature/implementation pipelines via `dark-factory`.

Pipelines and prompts resolve from `$DARK_FACTORY_HOME`; implementation work
happens in the caller's cwd (`--workdir` defaults to cwd).

This block is the **canonical install/setup copy** — the command files
(`factory-spec.md`, `fs.md`) point here; do not maintain divergent copies.

## Modes — what `/fs` / `/factory-spec` execute

### Create mode (default: `/fs <spec description>`)

**Two-phase spec generation.** By default, `/fs` produces BOTH a **main
spec** (`spec.md`) AND an **attractor spec** (`attractor_spec.md`). The
main spec describes the implementation path (acceptance criteria, test
command, non-goals, lane-independence matrix). The attractor spec
describes the convergence goal (stable end state the system must reach,
plus the anti-attractor states it must NOT converge to). A cold
adversarial codex reviewer signs off on **both** before exit. Pass
`--skip-attractor` to produce only the main spec.

1. Run **Step 0** (below): classify greenfield vs brownfield. Mandatory.
   The classification output feeds the goal/context string passed to the pipeline.
2. For brownfield tasks, encode rules 1–6 (delete-first, executor node for
   deletion, net-LOC ≤ 0 guard, dead-code gate, same-call-site replace,
   post-deletion proof) directly in the goal string.
3. Report the proposed `--goal` string (classification + description) and ask
   the user to confirm or modify **before** running.
4. Run the spec-generation pipeline from the target project's cwd:

   ```bash
   export DARK_FACTORY_HOME=~/projects/dark-factory
   export PATH="$HOME/.local/bin:$PATH"
   dark-factory --pipeline slim/spec_gen.dot --goal "<Step-0 context + description>"
   ```

   The pipeline runs:

   ```
   start → explore_in → explore_fanout → {explore_concept, explore_auth,
          explore_reuse, explore_risks} → explore_join → explore_stitch →
          explore_out
        → plan_main        [plan.md → spec.md]
        → review_main      [codex cold review of spec.md]              ─┐
        → plan_attractor   [plan_attractor.md → attractor_spec.md]     │ if main review fails → fix_main → review_main
        → review_attractor [codex cold review of attractor_spec.md]    ─┐
        → exit                                                            │ if attractor review fails → fix_attractor → review_attractor
   ```

   The attractor spec is generated **after** the main spec passes review
   (sequential, not parallel), so the attractor spec can reference the
   codex-signed-off `spec.md` for the consistency check. Both phases
   must sign off before exit. The pipeline produces a reviewed `spec.md`
   AND a reviewed `attractor_spec.md` without running any implement
   node. Pass `--skip-attractor` to short-circuit the attractor phase.

### Review mode (`/fs --review [spec_path]`)

1. `spec_path` defaults to `spec/feature.md` relative to the caller's cwd.
2. Read the spec and check, line-by-line: testable acceptance criteria;
   greenfield/brownfield classification stated; brownfield rules 1–6 present
   when applicable; pipeline named; goal stated as an observable output
   (a PR, a passing named test, a deleted path — not "improve X").
3. Report findings with line references and a verdict: `ready` or
   `needs-changes` with the specific gaps. Do **not** run a pipeline.

### Show mode (`/fs --show`)

Display the pipeline graphs below. Read-only; no classification, no spec
writes, no run.

## Proof block (create mode, binary-backed)

The default graph must preserve these nodes or their generated equivalents:
main spec plan, independent cold review, bounded main-spec fix loop,
attractor-spec plan, independent cold review, bounded attractor fix loop,
and exit. An in-Claude prose-only workflow that claims a spec run without a
logged binary invocation is not a valid run.

End every `/fs` create-mode response with this proof block. Missing any
required line means the run is unproven:

```bash
# Literal command run:
cd /Users/jleechan/projects/<target-repo>
DARK_FACTORY_HOME=~/projects/dark-factory \
DARK_FACTORY_HOLDOUTS=~/projects/dark-factory-holdouts \
PATH="$HOME/.local/bin:$PATH" \
dark-factory \
  --pipeline pipelines/slim/spec_gen.dot \
  --goal "<echo of $ARGUMENTS>" \
  --backend <backend> \
  --feature <feature> \
  --cxdb ~/.dark-factory/cxdb.sqlite
# Run ID: <id>
# CXDB SHA: <sha>
# Final outcome: <success|failure|exhausted|error>
# Exit code: <integer>
# Wall-clock: <duration>
# Logs: <path>
# Evidence envelope: <path>
```

Honesty rules:
- Quote the **actual** `dark-factory` command run — no paraphrasing.
- If the binary run fails, surface the trace and stop; don't assume "we can
  fix the spec later" without feeding the full review output into the next
  fix loop.
- If `--backend echo` was used, label the run as a wiring smoke — echo-mode
  review verdicts are not real LLM verdicts.
- Do not claim an in-Claude workflow or `Skill()` result is a factory run.
  The only valid proof is an actual `dark-factory` binary invocation plus
  this proof block.
- Reference/review/show modes (`--review`, `--review-attractor`, `--show`)
  are in-session helpers, not binary runs — they do not emit this proof
  block and must not be reported as a factory run.

**Why binary-first is the default**: the user's 2026-06-27 clarification
requires default binary invocation. Claude/workflow logic may build a
dynamic DOT graph behind the binary, but the durable proof remains the DOT
graph, CXDB, logs, and evidence envelope — same reasoning as `/f`.

## Pipeline selection (mandatory before `/f` or `/factory`)

When `--pipeline` is omitted, `/f` and `/factory` default to `two_node` (`pipelines/slim/two_node.dot`). To opt into a non-default pipeline, pass explicit `--pipeline <name>`.

| Task | Pipeline |
|------|----------|
| **Default `/f` / `/factory` invocation** | `pipelines/slim/two_node.dot` (generic worker + controller cold reviewer) |
| **Create a reviewed spec (main + attractor)** | `pipelines/slim/spec_gen.dot` ← `/fs` create mode (default) |
| **Create only the main spec** | `pipelines/slim/spec_gen.dot` ← `/fs --skip-attractor` |
| Smoke / wiring | `pipelines/factory/hello.dot` |
| New feature (full loop) | `pipelines/slim/minimal_feature.dot` |
| PR iteration (research + holdout) | `pipelines/slim/minimal_pr.dot` |
| Validate diff + holdout | `pipelines/factory/gates.dot` |
| PR gates only | `pipelines/factory/pr_gates.dot` |
| Spec review slim (legacy attractor) | `benchmarks/attractor-spec-review/pipelines/review_slim.dot` |
| Spec review full (legacy attractor) | `benchmarks/attractor-spec-review/pipelines/review_full.dot` |
| Brownfield replace/delete | custom goal + delete-first rules; often `minimal_feature.dot` or custom `.dot` |

Short names for `--pipeline`: `two_node`, `spec_gen`, `gates`, `hello`, `pr_gates`,
`minimal_pr`, `minimal_feature`, `review_slim`, `review_full`.

**Repo-specific pipelines (target-repo subdir convention):** graphs that
hardcode the target repo's own slash commands or repo-specific review
lanes belong at `<target_repo>/dark-factory/pipelines/<name>.dot`, not
in `~/projects/dark-factory/pipelines/`. The runner resolves bare
filenames against `<workdir>/dark-factory/pipelines/` **before** falling
through to `$DARK_FACTORY_HOME/pipelines/`, so an operator in the target
repo can pass `--pipeline my_repo_lane.dot` and the runner finds it
locally.

**When `--pipeline` is omitted (auto-select path),** `/f` and `/factory`
list the contents of `<workdir>/dark-factory/pipelines/` **before**
falling back to the built-in decision table, so repo-specific graphs
surface in the auto-select output. The convention is therefore
discoverable, not just documentable.

Execution command (from target repo cwd):

```bash
export PATH="$HOME/.local/bin:$PATH"
dark-factory --pipeline pipelines/slim/minimal_pr.dot --goal "..." --backend claude
```

## Purpose

Show the factory pipeline graph structure at a glance — node types, edges,
conditions, and handler mappings — without running a pipeline. Use this when
you need to remember what nodes exist, what the wiring looks like, or which
pipeline to pick for a given goal.

## Step 0 (MANDATORY): classify the task — Brownfield vs Greenfield

Before picking a pipeline or writing the spec/goal, decide which kind of change this is.
**Getting this wrong is the #1 cause of a factory run that reaches `exit`/success while
certifying the wrong thing.** (Real failure 2026-05-30: a *replace-the-backend-override*
task was run with a greenfield additive pipeline → the override was never deleted, a parallel
mechanism was bolted on top, net LOC was +2507/−54, and an unwired Pydantic model passed
`test_e2e` as dead code.)

### Greenfield — new behavior from scratch (net-additive)
Use the standard pipelines (`hello.dot`, `minimal_feature.dot`, `review_*.dot`):
`plan → implement → test → review → holdout → gates`. Net-positive LOC is expected.

### Brownfield — refactor / replace / **delete** existing behavior
The task removes or replaces a code path that already runs in production. A greenfield
pipeline is **wrong** here. Encode these rules in the spec, the `--goal`, and the DAG:

1. **DELETE-FIRST ordering (not delete-last).** The `implement` node must *remove or replace
   the old path as part of the build*, and the behavior/`test_llm` node then proves the new
   path works **with the old one already gone**. Never "add new alongside old → prove → delete
   later": the deletion gets **orphaned** (no node executes it) and the proof is **confounded**
   (the old path's fallback/passthrough can mask a weak new path, so green proves nothing).
2. **Deletion needs an executor node — never a conditional.** Do NOT write "(N) only AFTER the
   proof, delete X" in a goal: nothing in the DAG runs a post-proof deletion, and resume
   pipelines (test-onward) have no `implement` node at all. Make the deletion part of
   `implement`/`fix`, or add an explicit node.
3. **Net-LOC ≤ 0 guard.** For replace/delete milestones, add a gate/acceptance check that
   FAILS if net production LOC > 0 (the new code must displace at least as much as it adds).
   See `deletion-milestone` skill.
4. **Dead-code gate.** Add a check that FAILS if a newly-added module/symbol is *defined but
   unreferenced in runtime* (non-test). Otherwise a passing unit test makes `test_e2e` green
   while the code is dead (e.g. a model class only instantiated in its own test).
5. **Replace at the same call site.** The new mechanism must be wired into the *same* call
   site the old one used, and the old one removed in the same change — not added at a new
   site while the old site still runs.
6. **Prove against the post-deletion tree.** The real-LLM / behavior test must execute with the
   old path already deleted, so a green verdict cannot be produced by the old fallback.

**Quick test:** "If this milestone succeeds, should `git diff` show deletions of production
code?" If yes → brownfield → apply rules 1–6. If the planned diff is all additions for a
replace/delete goal, the pipeline is mis-shaped — STOP and re-architect delete-first.

## Spec-Review Pipelines (Primary)

These are the Attractor-style spec-validation pipelines under
`benchmarks/attractor-spec-review/pipelines/`. The key innovation: an
**independent cold reviewer** (`codex exec --yolo`) that numbers every spec
line and returns strict JSON line-by-line findings.

### 1. `review_slim.dot` — Line-Aware Spec Review (Slim)

```
start ──▶ plan ──▶ implement ──▶ acceptance ──(success)──▶ review ──(success)──▶ exit
                                    │                       │
                                    └──(fail)──▶ fix ◀──────┘ (max 3 visits)
                                                      │
                                                      └──▶ implement (loop)
```

| Node | Type | Command / Prompt | What it does |
|------|------|-----------------|-------------|
| `start` | built-in | — | Entry point |
| `plan` | `codergen` | `@benchmarks/attractor-spec-review/prompts/plan.md` | Plan from spec |
| `implement` | `codergen` | `@benchmarks/attractor-spec-review/prompts/implement.md` | Write code |
| `acceptance` | `tool` | `python scripts/validate_spec.py --spec spec/feature.md --report spec_review/validation_report.json` | Line-numbered spec validation |
| `review` | `tool` | `benchmarks/attractor-spec-review/scripts/review_with_codex.sh . spec/feature.md spec_review/independent_reviewer.json` | Independent cold reviewer via `codex exec --yolo`; returns JSON verdict |
| `fix` | `codergen` | `@benchmarks/attractor-spec-review/prompts/fix.md`, `max_visits=3` | Fix failures, loops back to implement |
| `exit` | built-in | — | Terminal node |

**Use when:** validating a spec implementation against line-numbered acceptance
+ independent reviewer, without full-stack smoke.

### 2. `review_full.dot` — Line-Aware Spec Review (Full)

```
start ──▶ plan ──▶ implement ──▶ acceptance ──(success)──▶ stack_smoke ──(success)──▶ review ──(success)──▶ exit
                                    │                       │                       │
                                    └──(fail)──▶ fix ◀──────┘                       └──(fail)──▶ fix
                                                      │
                                                      └──▶ implement (loop)
```

Same as slim, plus a `stack_smoke` node between acceptance and review:

| Node | Type | Command | What it does |
|------|------|---------|-------------|
| `stack_smoke` | `tool` | `bash scripts/fullstack_smoke.sh` | Full-stack smoke test before reviewer |

**Use when:** you need end-to-end runtime verification before the independent
reviewer checks spec conformance.

### Key node: Independent Reviewer

The `review` node runs `review_with_codex.sh` which:

1. Numbers every spec line (`0001: ...`, `0002: ...`)
2. Shells out to `codex exec --yolo` — **separate process, cold reviewer**
3. Returns strict JSON: line-by-line findings + verdict (`pass`/`fail`)
4. `goal_gate=true` + `retry_target="fix"` — failure routes to fix loop

This is the Attractor guarantee: the reviewer has never seen the implementation
prompt, only the spec and the code diff.

## Factory Pipelines (Validation Gates)

### 3. `gates.dot` — 4-Gate Validation

```
start ──▶ holdout_eval ──(success)──▶ gate_es ──(success)──▶ gate_er ──(success)──▶ gate_cs ──▶ exit
                 │                      │                      │
                 └──(fail)──▶ exit      └──(fail)──▶ exit     └──(fail)──▶ exit
```

| Node | Type | Handler | What it does |
|------|------|---------|-------------|
| `holdout` | `holdout_eval` | Sealed evaluator at `$DARK_FACTORY_HOLDOUTS/evaluator/run.py` | Runs hidden test scenarios against the diff |
| `gate_es` | `gate_es` | `claude --print /es` | Evidence standards check |
| `gate_er` | `gate_er` | `claude --print /er` | Evidence review check |
| `gate_cs` | `gate_code_standards` | `claude --print /code_standards` | ZFC + leveling + root-cause-first |

**Use when:** already-implemented diff needs Attractor-style 4-gate validation (requires holdout).

### 3.5 `pr_gates.dot` — 3-Gate PR Validation (No Holdout)

```
start ──▶ gate_es ──(success)──▶ gate_er ──(success)──▶ gate_cs ──▶ exit
             │                      │
             └──(fail)──▶ exit      └──(fail)──▶ exit
```

| Node | Type | Handler | What it does |
|------|------|---------|-------------|
| `gate_es` | `gate_es` | `claude --print /es` | Evidence standards check |
| `gate_er` | `gate_er` | `claude --print /er` | Evidence review check |
| `gate_cs` | `gate_code_standards` | `claude --print /code_standards` | ZFC + leveling + root-cause-first |

**Use when:** validating an in-flight PR diff (like gates.dot; the actual `.dot` runs holdout as the first node per the Holdout-always policy, so pass `--feature <name>`).

### 4. `hello.dot` — Plan/Implement/Fix Loop

```
start ──▶ plan ──▶ implement ──▶ holdout_eval ──(success)──▶ exit
                                      │
                                      └──(fail)──▶ fix ──▶ holdout_eval (loop, max 3 visits)
```

**Use when:** adding a new feature from scratch with a holdout scenario.

### 5. `minimal_feature.dot` — Full Feature Factory (Slim)

```
start ──▶ plan ──▶ implement ──▶ test ──(success)──▶ review ──(success)──▶ holdout ──(success)──▶ gate_es ──(success)──▶ gate_er ──(success)──▶ exit
                                    │                  │                  │                  │
                                    └──(fail)──▶ fix ◀─┘                  │                  │
                                                          └──(fail)──▶ fix ┘                  │
                                                                               └──(fail)──▶ fix ┘

fix ──▶ test (loop)
```

**Use when:** full production pipeline from scratch: test → review → holdout → evidence gates.

### 6. `minimal_pr.dot` — Slim PR Iteration Factory (No Holdout)

```
start ──▶ explore ──▶ research ──▶ plan ──▶ implement ──▶ test ──(success)──▶ review ──(success)──▶ holdout ──(success)──▶ gate_es ──(success)──▶ gate_er ──(success)──▶ exit
                                                            │                  │                       │                      │                      │
                                                            └──(fail)──▶ fix ◀─┴───────────────────────┴──────────────────────┴──────────────────────┘

fix ──▶ test (loop)
```

**Use when:** in-flight PR iteration loop with parameterized test commands (`--state slim.test_command="..."`) and evidence checks. Holdout-always policy: this lane runs the sealed behavioral holdouts (requires `$DARK_FACTORY_HOLDOUTS`), and a classless `research` node (coder tier) digests explore findings before plan.

## Handler type registry

| Node `type` attr | Handler function | Behavior |
|-------------------|-----------------|----------|
| `codergen` | `_codergen` | Render prompt template, dispatch to backend (claude/codex/ao/agy) |
| `tool` | `_tool` | Shell out to `command="..."` attribute |
| `holdout_eval` | `_holdout_eval` | Run sealed evaluator from `$DARK_FACTORY_HOLDOUTS` |
| `gate_es` | `_gate_es` | Shell out to `claude --print /es` |
| `gate_er` | `_gate_er` | Shell out to `claude --print /er` |
| `gate_code_standards` | `_gate_code_standards` | Shell out to `claude --print /code_standards` |
| `human_gate` | `_human_gate` | Block on stdin or use `ctx.state["<node>.outcome"]` |
| `conditional` | `_conditional` | Hexagon decision node; outcome from `ctx.state[decision_key]` |

## Shape-based handler fallback

| DOT shape | Handler |
|-----------|---------|
| `Mdiamond` | `start` |
| `Msquare` | `exit` |
| `hexagon` | `conditional` |

## Edge condition syntax

- `condition="key=value"` — matches `ctx.state[key] == value`
- `condition="key!=value"` — matches `ctx.state[key] != value`
- No condition — unconditional (fallback)
- Conditional edges tried **before** unconditional ones

## Backend routing

| `--backend` flag | Per-node `backend` attr | CLI invoked |
|------------------|------------------------|-------------|
| `echo` | — | Deterministic mock, no LLM |
| `claude` | `claude` | `claude --print --dangerously-skip-permissions` |
| `codex` | `codex` | `codex exec --yolo` |
| `ao` | `ao` | Agent Orchestrator `ao spawn` |
| `agy` | `agy` | `agy --print --dangerously-skip-permissions` |

## Source files

- Spec-review pipelines: `benchmarks/attractor-spec-review/pipelines/`
- Spec-review scripts: `benchmarks/attractor-spec-review/scripts/`
- Factory pipelines: `pipelines/factory/` and `pipelines/slim/`
- Handlers: `runner/handlers.py`
- Engine: `runner/engine.py`
- Parser: `runner/parser.py`
