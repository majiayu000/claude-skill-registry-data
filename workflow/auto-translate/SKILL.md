---
name: auto-translate
description: >
  Translate a designed loop (from auto-design) or a workflow (from
  auto-author-workflow) into an execution tree — ordered parallel waves sized from
  the workflow's depends_on DAG and the active fan-out cap, fan-out do_step children
  nested under their producer parent, and a substrate routing decision
  (native subagent-tree = executable, workflow-script = an inert label deferred to
  the parked RFC). Use when the user says "translate this loop", "what's the
  execution tree / wave order", "how will this workflow parallelize", "size the
  fan-out", or when a designed loop needs its runnable shape shown before /auto
  drives it. This skill COMPOSES auto-design/auto-author-workflow (it consumes their
  output; it does not replace them) and reuses the existing dependency engine.
---

# auto-translate (loop/workflow → execution tree)

An **execution tree** is the runnable shape of a workflow: which steps run in
parallel, in what wave order, which fan-out `do_step` children nest under which
parent, and which substrate the loop targets. This skill derives that tree from a
workflow and shows it — it does NOT invent a new artifact and it does NOT dispatch.
It calls one pure helper (`lib/execution_tree.py::derive_execution_tree`) and
reports the result. (R9, R10, R11.)

It sits DOWNSTREAM of loop design: hand it a workflow that `auto-design` /
`auto-author-workflow` already wrote (or a built-in like `a2` / `a4`). It composes
with the dependency engine (`lib/dispatcher.py::ready_steps` / `dispatch_batch`)
and the two-handoff `do_step` split rather than replacing them — the same readiness
frontier drives both the preview here and the real run.

## What stays true throughout

- **Parallelism is implicit in the DAG — no wave field.** Steps sharing a phase
  with independent `depends_on` run concurrently; a multi-dep step is a fan-in.
  The derivation reuses `dispatcher._is_ready` / `_dependency_satisfied` to walk
  waves — it never invents a second parallelism model. (KTD6.)
- **The fan-out `cap` bounds each wave.** A wave wider than `cap` spills its excess
  to the next wave, exactly as `dispatch_batch` leaves over-cap steps pending for a
  later call. Pass the active work-loop cap.
- **Native subagent-tree is the only executable target this run.** `workflow-script`
  is a **routing label + a topology preview**, an inert annotation — NOT a runnable
  compiled script. The parked workflow-substrate RFC's `pipeline()`/`parallel()`
  compiler is unbuilt and its re-entry gates are unmet, so executable
  workflow-script compilation is deferred. R10's "target either substrate" is
  satisfied by the routing DECISION, with native as the sole executable output.
  (KTD6b.)
- **Both routings are supervised from outside.** The wedge-timeout watchdog (U1)
  lives external to the substrate, so the routing label changes the compile target,
  never how the run is supervised.

## The flow

### 1. Get the workflow

Take the workflow the design step produced. If you have a workflow **name** (a
built-in or a workspace-tier variant), resolve + validate it first:

```
python3 -c "import sys; sys.path.insert(0,'lib'); from _bootstrap import load_lib_module; \
r,_=load_lib_module('workflows').load_and_validate('<name>', '.'); import json; print(json.dumps(r))"
```

If `auto-design` handed you a draft workflow dict directly, use it as-is (it already
passed the authoring gate). Never hand-derive parallelism — pass the workflow to the
helper.

### 2. Derive the execution tree

Call the one pure helper with the workflow dict and the active fan-out cap:

```
python3 -c "import sys, json; sys.path.insert(0,'lib'); from _bootstrap import load_lib_module; \
xt=load_lib_module('execution_tree'); \
r=json.load(open('workflows/<name>.json')); \
res=xt.derive_execution_tree(r, 16); \
print(res['preview']); \
print('substrate:', res['substrate']); \
print('waves:', res['waves'])"
```

`derive_execution_tree(workflow, cap)` returns `{workflow, cap, waves, nesting,
substrate, emitted, preview}` — pure and deterministic. It:

- **expands producer-produced steps first** — workflows like `a4` declare their paired
  builders in `expected_emit_outputs` (materialized at runtime by a phase-boundary
  producer, NOT in `steps[]`), so the derivation synthesizes placeholder nodes for
  them before the frontier walk. `a2`'s parallel steps are static — no expansion.
- **walks ordered waves** from the expanded `depends_on` DAG, bounding each to `cap`.
- **nests fan-out `do_step` children** under their producer parent.
- **routes a substrate** (step 4).

### 3. Show the topology preview

Print `res['preview']` — a deterministic ASCII card of the derived tree: each wave
as a numbered parallel row, fan-out children indented under their parent, and the
substrate footer. Show it and point at the wave order and any fan-out. This is the
`topology-render`-family card (same visual family the picker/authoring skill use),
rendered over the DERIVED waves rather than the raw workflow.

### 4. State the substrate routing

Report the routing decision and what it means:

- **`subagent-tree`** — the default and the **only executable** target this run
  (`lib/dispatcher.py::dispatch_batch`). A loop with per-step ce-work/`review`
  dispatch or long-lived verdicts routes here.
- **`workflow-script`** — an **inert routing label** for a self-contained bounded
  parallel-fan-in loop (single-phase, no `do_step`/`review` op, an engine-enforced
  `iteration.bound`). Say plainly that it is **not runnable this run** — it is a
  preview + annotation, deferred to the parked workflow-substrate RFC's re-entry.
  Do not imply a compiled script exists.

The predicate is concrete (single-phase + no ce-work/review backend op + bounded →
`workflow-script`; else `subagent-tree`) — see the module docstring for the exact
rule. `a2` and `a4` both carry a `review` op (a4 also `do_step`), so both route to
`subagent-tree`.

### 5. Report

State the wave order, the fan-out nesting, the substrate routing (and that
workflow-script is inert if that's the decision), and how to run it: `/auto <plan>
--workflow <name>`. If the substrate is `workflow-script`, note the run still
executes on the native subagent-tree — the label is a forward-looking annotation.

## What this skill does NOT do

- It does not build a `pipeline()`/`parallel()` compiler or any runnable
  workflow-script — that target is inert this run (KTD6b).
- It does not dispatch, mutate the run-record, or touch a run. Derivation is pure; the
  real run goes through `/auto` and `dispatch_batch`.
- It does not replace `auto-design` / `auto-author-workflow` (it consumes their
  output) or the dependency engine (it reuses `ready_steps` / `_is_ready`). (R11.)
- It does not invent a new workflow field or a wave annotation — parallelism stays
  implicit in `depends_on` (KTD6, no workflow-format change).

## Invariants

- **Reuse the frontier, don't re-derive it.** Waves come from
  `dispatcher._is_ready`, bounded by `cap` — never a second parallelism model.
- **Expand producer-produced steps before the walk**, or a workflow whose builders
  live in `expected_emit_outputs` (a4) yields only `{plan}` and its dependents
  never become ready.
- **Native is the only executable target.** `workflow-script` is a routing label +
  preview, deferred to the RFC. (KTD6b, R10.)
- **Compose, don't consolidate.** This skill calls the derivation and the existing
  engine; it writes no artifact and replaces no skill. (R11.)
