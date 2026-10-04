---
name: planning-visual-tasks
description: v1.2 LLM-driven planner. Turns a natural-language instruction into a structured Plan envelope (`contracts/agent/plan.schema.json`) of typed sub-goals (workflow_search → model_resolve → comfyui_execute → llm_transform → evaluate → mcp_tool → checkpoint → wait_user). Use whenever a user instruction needs routing through the host orchestrator. The legacy v1 keyword router is preserved as a deterministic fallback when no LLM provider is configured.
---

# planning-visual-tasks

**v1.2 — the brain of the agent loop.** Inputs: a user instruction +
optional `task_state` + the discovered tool / model / template
inventory. Output: a `Plan` envelope (matching
`contracts/agent/plan.schema.json`) that the host
`Orchestrator` consumes via `Executor.run(sub_goal, task_state)`.

The v1 keyword router (`scripts/decompose.py` + `scripts/emit_dag.py`)
is **preserved** as a deterministic, no-LLM fallback. The host
`POST /api/chat/invoke` route picks v1.2 when an LLM provider is
configured (`host.llm.provider.resolve_credentials()` returns a key)
and falls through to the v1 router otherwise. See
`host/api/chat_invoke.py::_llm_available` and `_invoke_stream_v12`.

## When this Skill applies

- Any natural-language image / video generation, edit, or
  composition request that the host has routed through
  `POST /api/chat/invoke`.
- Single-goal instructions still go through this Skill — the LLM
  planner is responsible for the "do not over-decompose" decision
  and emits a 1-step Plan in that case.
- Multi-step "generate then adjust the light" / "and then make it
  dance" instructions become a multi-subgoal DAG with explicit
  `state://`, `template://`, and `model://` refs across steps.
- Cross-turn "and then" continuations consume the prior turn's
  `TaskState.named_outputs` so an earlier image can be referenced
  by name in the next turn.

Do **not** invoke when the caller already has a fully-specified
`comfyui_execute` sub-goal — instantiate the `Executor` and call
its `comfyui_execute` handler directly.

## Scripts

- `scripts/propose_plan.py` — v1.2 LLM-driven planner. Stdin:
  `{instruction, task_state, available_tools}`. Stdout: a Plan
  envelope. Wraps `host.agent.planner.Planner.propose`.
- `scripts/discover_tools.py` — stdin `{}`, stdout
  `{tools, models, templates, mcp_tools}`. Lists every executor
  `kind` plus stubs from any installed Stream M / W / X surfaces.
- `scripts/validate_plan.py` — stdin Plan, stdout `{ok, errors}`.
  Checks schema, DAG acyclicity, ref resolution.
- `scripts/legacy/decompose.py` — v1 keyword router (no-LLM
  fallback). Heuristic clause-to-skill mapping. Still callable
  from the legacy code path for users without an LLM key.
- `scripts/legacy/emit_dag.py` — v1 DAG emitter for the legacy
  router output.
- `scripts/decompose.py` and `scripts/emit_dag.py` — copies of
  the legacy scripts kept in place so v1.1 callers (the existing
  `host.api.chat_invoke.plan_instruction`) keep working without
  modification. Removing these breaks the v1.1 fallback path.

## Output contract — v1.2

The Plan envelope shape is canonical
(`contracts/agent/plan.schema.json`): `{plan_id, task_id,
user_instruction, execution_order, subgoals[]}`. Sub-goal `kind`
values are limited to: `workflow_search, model_resolve,
model_download, comfyui_execute, llm_transform, evaluate,
mcp_tool, checkpoint, wait_user`. Cross-step refs use
`scheme://sgN/<name>` format only (`state`, `template`, `model`,
`artifact` schemes); the legacy `$sgN.field` form is rejected
by the executor's `resolve_inputs` unless `allow_legacy_refs=True`
is set explicitly.

The legacy v1 router emits a different shape (`{steps,
execution_order, created_at}` keyed by skill+intent) — that
shape is consumed by `host.runner.runner.Runner.run_dag` and is
ONLY used on the no-LLM fallback path.

## When this Skill applies

- The user issues an instruction that is not a trivial pass-through to one
  capability Skill (e.g. "generate a cyberpunk portrait, then replace the
  background with a neon street, then preserve the face across a style
  transfer"). Any instruction with ≥2 visual goals must go through the planner.
- Single-goal instructions still go through the planner — it is responsible
  for the "do not over-decompose" decision and emits a 1-step DAG in that
  case.
- Unusual requests that aren't covered by any bundled capability Skill route
  through `searching-comfyui-solutions` first; the planner consumes the
  ranked search results as candidates.

Do **not** invoke when the caller already has a fully-specified Visual Intent
Object for a single Skill — call the capability Skill directly.

## Pipeline

1. Parse the instruction: extract `goals[]`, optional `constraints`, optional
   `inputs.image_refs[]`.
2. If any clause has no matching keyword and the caller supplies
   `search_candidates` on stdin, the planner emits a search-grounded step
   for it. **The planner itself does not shell out to `search_local.py` or
   `search_web.py`** — the caller (host runner) is responsible for invoking
   the `searching-comfyui-solutions` Skill scripts and passing the ranked
   hits in. Each candidate **must** carry `skill` and `goal` fields
   declaring the target capability Skill; candidates without them are
   rejected (the planner fails loudly instead of guessing). See
   `scripts/decompose.py` `VALID_SKILLS` / `VALID_GOALS`.
3. Run `scripts/decompose.py` — heuristics map (goals + constraints +
   search candidates) → ordered list of `{skill, intent, depends_on,
   evaluators, provenance}`. Any clause that cannot be resolved (no
   keyword match and no usable candidate) causes the script to exit 2
   with a `no_match` error; partial plans are rejected.
4. Run `scripts/emit_dag.py` — validates the decomposition, attaches
   provenance, returns the DAG JSON on stdout.
5. Caller (host) renders the DAG, gets user approval, then executes step by
   step through each capability Skill's `compile.py` and then
   `comfyui-execution/submit_prompt.py`.

Every step carries:

- `provenance.source` — `"bundled"` | `"search:<url>"` | `"user-supplied"`
- `provenance.retrieved_at` — ISO 8601 UTC timestamp (or `null` for bundled)
- `provenance.trust_tier` — one of `bundled` / `web_trusted` /
  `web_unverified` per
  `../searching-comfyui-solutions/reference/trust-tiers.md`

## One-step vs multi-step decision

See `reference/strategies.md`. Hard rule: if the instruction contains a
**single atomic visual action** (`generate`, `inpaint`, `replace bg`,
`transfer style`, `preserve face`) and no compositional connective
("then", "and after", "while keeping"), emit a 1-step DAG.

## Reference files

- `reference/intent-schema.md` — Visual Intent Object fields
- `reference/strategies.md` — decomposition heuristics
- `reference/dag-examples.md` — four worked examples including the v1
  acceptance test

## Scripts

- `scripts/decompose.py` — pure Python; stdlib only; keyword + pattern match;
  no LLM. Input: `{instruction, project_state?, search_candidates?}`.
- `scripts/emit_dag.py` — validates and attaches provenance.

## Error handling

Both scripts emit `{"error": "...", "code": "..."}` on bad input with exit
code 2. Never raise to caller.

## References

- `knowledge/plans/v1/plan_v1.md` §1, §7, §8.4
- `knowledge/plans/v1/todo.md` §6 (Stage 3)
