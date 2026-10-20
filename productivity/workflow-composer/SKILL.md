---
name: workflow-composer
description: "\"MANDATORY: Read this skill before planning or calling search, fetch, or agent when the current task needs its own research, browsing, or judgment for each of 5 or more independent, comparable items (10 or more: always fan out), or when the user asks for comprehensive coverage, parallel research, or subagents. Use `workflow/run` (the `run` tool on the `workflow` MCP server, called with the `mcp` tool using server: `workflow`, name: `run`) to compose those internal units: one dedicated agent per item, structured results aggregated back into the current task. Not for shortlists, one question with several facets, work a handful of searches can finish, or the same command over many inputs (write one script with bounded concurrency). Also use for loops, conditions, multi-stage map/reduce work, and deterministic subagent orchestration.\""
compatibility: opencode
---

# Workflow Composer

`workflow/run` in this document means the `run` tool on the `workflow` MCP server: call it with the `mcp` tool using `server: "workflow"`, `name: "run"`.

`workflow/run` executes a deterministic JavaScript orchestration script that coordinates multiple subagents. The whole workflow runs as one background job; its return value is injected into the parent conversation when it finishes.

## When to use

Required condition — every item must clear this bar:

- Each item requires non-trivial independent reasoning, research, browsing, or open-ended tool exploration. Item count alone is never sufficient. Before reaching for `workflow/run`, ask: "could this be a single script looping over the items?" — if yes, write that script and execute it directly with bounded concurrency instead.

With that condition met, use `workflow/run` when any of the following applies:

- The task contains 5 or more independent, comparable items processable concurrently. With 10 or more, fan out instead of working through them yourself.
- The user asks to research, compare, summarize, or analyze many entities with the same output structure.
- The outputs need to be collected into a table, report, ranking, dataset, or other combined deliverable.
- The orchestration needs loops, conditions, retries, staged execution, aggregation, or a large/dynamic fan-out.

Do **not** use it when there are only a few small independent tasks (direct `agent` calls are fine), when the whole task is a shortlist or recommendation, one question with several facets, or work a handful of searches can finish, when the items are answerable immediately from context, when the task is inherently sequential or tightly coupled, or when the per-item work is the same deterministic command or script with different parameters — that is a batch job for one script with bounded concurrency, not a workflow.

## MCP capability and concurrency contract

Before a workflow whose item agents depend on an MCP server, call `server.list` and obey that server description's `Subagents` and `Concurrency` contract.

- Use `sandbox: 'isolated'` when stateful tasks must proceed independently in parallel.
- Give parallel file-producing agents deterministic, distinct output paths.
- Keep operations marked parent-only in the parent agent; subagents cannot make them available by retrying through another interface.
- If a required tool is unavailable or fails, collect and report the blocker. Never fabricate completion, reuse another item's artifact, or substitute a different artifact type unless the task explicitly allows that fallback.

## Decomposition contract

For item-based fan-out:

1. Exactly one dedicated `agent()` call per independent item — never bundle several items into one subagent.
2. The parent agent must not perform item-level research before or alongside the workflow; it orchestrates.
3. Every subagent gets one clearly bounded subject and a fully self-contained prompt.
4. Comparable subagents share the same structured output fields (group `{schema}`).
5. Item agents run inside one named `parallel` group, preserving input order so outputs map back to inputs.
6. Handle individual failures without discarding successful results.

Bad: `agent('Research Nintendo, PlayStation, Xbox, Atari, Sega, …', {brief: 'Research all consoles'})`

Bad: `agent('run enrich.sh item-42')` × 230 — deterministic command fan-out belongs in a single script with bounded concurrency, not in per-item subagents.

Correct:

```javascript
const consoles = ['Nintendo NES', 'PlayStation', 'Xbox', 'Atari 2600', 'Sega Dreamcast']
const results = await parallel('Research consoles', () =>
  consoles.map(name =>
    agent(`Research ${name} and return the requested structured information.`, {brief: `Research ${name}`})
  )
)
```

## Map/reduce contract

When the final deliverable requires cross-item synthesis (comparative report, ranking, merged document, executive summary):

1. Map: one agent per item inside a `parallel` group.
2. Collect: keep successful structured results, record failures.
3. Reduce: exactly one reducer agent over the collected results.
4. Return: reducer output plus useful map results and explicit report paths. Have the parent confirm the files exist and deliver them from the shared sandbox, without re-researching the items.

Count the reducer in both `estimated_agent_calls` and `max_agent_calls`. If deterministic code can combine the results without judgment (joining strings, returning rows), skip the reducer agent.

## Discovering the item set

- Items given by the user → use that list directly.
- Item set scopable from stable domain knowledge → define a reasonable list and state the selection criteria.
- Discovery itself requires research → run one discovery agent with a JSON Schema, read the array from its structured result, then fan out one agent per discovered item. Use a conservative high-side `estimated_agent_calls` and count the discovery agent (and any reducer) in the budgets. Fan out only for work discovery did not already do; if its result already answers the task, stop there.

## Execution model

- The script runs in a sandboxed JavaScript environment with **no I/O**: no filesystem, network, timers, or `require`/`import`. Subagents use their own tools and filesystem.
- The script **must be deterministic**: `Math.random()` and the entire `Date` object (including `new Date(...)` with arguments) are unavailable. Workflows survive restarts by replaying the script against a journal of completed `agent` calls; nondeterministic control flow breaks replay. Vary prompts by stable inputs or array indexes.
- Plain JavaScript control flow (variables, loops, conditionals, array methods, async/await, string/JSON operations) is fully available; the script body may use `await` directly.
- The script's completion value (`return` or last expression) becomes the workflow result.
- Workflow completion is a barrier over every `agent()` call: even if a Promise is not explicitly awaited, the job waits for that subagent to finish. Still use `await` or `parallel()` whenever its result participates in the returned value; an unawaited result is discarded.
- `script` must contain only a syntactically valid JavaScript function body — no Markdown fences or surrounding prose.

## Primitives

- `agent(prompt, {brief, schema, input_files, sandbox, effort_level})` returns a Promise of one subagent result. `brief` is **required** (≤120 chars): a self-explanatory title of what THIS subtask does, written in the user's language and specific to the item — shown verbatim as the subtask's row title in the user-facing task board. Say what is being done to what (e.g. `Scrape ACME pricing page`); never a generic label like `agent 3` / `subtask` / `Product 3`. Prompts must be self-contained (exact item, goal, required fields, source/verification requirements, constraints, expected file paths and output format): the subagent does not see the parent conversation.
- `parallel(brief, factory, {schema}?)` concurrently runs the agent promises returned by `factory` as a named group. `brief` is **required** (≤80 chars): a descriptive group name summarizing the whole batch, shown as the group header. `factory` must be a **function** returning an array of `agent()` promises — a bare promise array is rejected. Optional `{schema}` is the group default JSON Schema: agents created inside without their own `schema` inherit it; a per-agent `schema` overrides it; nested groups use the nearest enclosing schema.
- `log(message)` publishes concise progress, visible via `job` info.

## Structured results

Give every comparable-item group a shared JSON Schema: outputs stay structurally consistent, aggregation is reliable, and the UI renders the group as a table (columns from the schema's `properties`, one row per subagent result).

A successful `value` is already JSON-decoded when the subagent returned valid JSON — **never call `JSON.parse()` on a schema-constrained result**. Results are rejected unless they are valid JSON conforming to the effective schema (own `schema`, else nearest group `{schema}`).

## Files

- Return structured data for aggregation. The current Sandbox Host does not populate durable artifact refs in a child result's `files`; do not rely on `type: "file"` or `previous.files` to deliver or transfer output files. For file-producing work, use shared mode with explicit, unique parent-sandbox paths and have the parent task verify and deliver those files through its normal file tools.
- Declare every child input file explicitly in `input_files`: `{path: '/home/ubuntu/input.csv', name: 'data'}` for an existing parent-sandbox file. ArtifactRef inputs are not supported by the current Sandbox Host. A path merely mentioned in prompt text is never transferred.
- `sandbox: 'shared'` (default) runs subagents in the parent sandbox — give each item a deterministic, collision-free output path. `sandbox: 'isolated'` gives a fresh disposable sandbox for untrusted/heavy work; declared inputs are transferred and the child receives its actual local path.

## Budget parameters

- `effort_level`: default effort for every subagent in the workflow; defaults to `lite`. Each `agent()` may override it with `lite`, `standard`, or `max`. Keep independent research, extraction, and transformation on `lite`; use `standard` for reducers or complex judgment, and reserve `max` for exceptional cases.
  `effort_level` is only supported by the workflow input and each `agent()` options object; `parallel()` group options support only `schema`.

- `max_agent_calls`: requested `agent()` budget (1–2000), not a credit limit. At creation the addon adds `max(2, floor(requested * 0.1))`, capped at 2000. The returned effective limit is persisted as the hard upper bound; restarting does not add another allowance. Report that effective limit when discussing the budget. Put the full intended fan-out in one workflow rather than splitting it into trial batches.
- `estimated_agent_calls`: conservative high-side estimate of calls actually executed (≤ `max_agent_calls`). Count everything: discovery + item/map + reducer + validation agents. Exact count for deterministic lists; realistic high-side estimate for dynamic branches — never intentionally underestimate.
- Agent registrations are paced by the worker, separately from Host execution concurrency. `parallel` expresses independence, not an immediate burst; do not split the workflow to bypass submission pacing.

## Failure policy

Default and recommended for item fan-out: `collect`. Every `agent()` resolves to `{ok: true, value, files}` or `{ok: false, error}` in input order. `error` is `{code, message}` — read the fields; do not interpolate the whole object as a string. Preserve successful results even when some items fail:

```javascript
const successful = results.filter(r => r.ok).map(r => r.value)
const failures = results
  .map((r, i) => (r.ok ? null : {item: items[i], code: r.error.code, message: r.error.message}))
  .filter(Boolean)
```

Use `fail_fast` only when later work would be invalid after any individual failure.

## Confirmation gate

The Host checks confirmation before subagents start: absent an existing auto-start authorization, an estimate or effective budget above 20 requires confirmation (for example, requested 20 becomes effective 22). A pending workflow is **already registered** — never call `workflow/run` again for the same task. Stop the turn and wait; on explicit acceptance use `job` to approve the exact job id, on explicit rejection use `job` to reject it. Never approve without a new user reply. Approval does not remove the saved effective budget.

If the effective budget is exhausted on a compatible Host, the workflow pauses instead of marking the remaining items failed. Do not submit another `workflow/run`. If the effective limit is already 2000, no increase is possible: keep the job paused, inspect retained results and in-flight subtasks with `job list`/`job info`, or use `job kill` to stop. Otherwise, use `job continue` to propose a higher absolute `max_agent_calls` (never above 2000), present that exact total, and repeat it only after a new explicit approving user reply. Never interpret refusal or unrelated input as approval. Completed results are reused. An older Host may instead report that resumable pause is unsupported; do not claim it paused successfully.

## Recommended item-research template

```javascript
const items = [
  {id: 'item-a', name: 'Item A'},
  {id: 'item-b', name: 'Item B'},
  {id: 'item-c', name: 'Item C'}
]

const itemSchema = JSON.stringify({
  type: 'object',
  properties: {
    id: {type: 'string'},
    name: {type: 'string'},
    summary: {type: 'string'},
    key_facts: {type: 'array', items: {type: 'string'}},
    report_path: {type: 'string'}
  },
  required: ['id', 'name', 'summary', 'key_facts', 'report_path']
})

const mapped = await parallel(
  'Research all items',
  () => items.map((item, index) =>
    agent(
      'Research exactly one item: ' + item.name + '.\n' +
      'Verify important facts using authoritative sources.\n' +
      'Return the requested structured fields.\n' +
      'Write the detailed report to /home/ubuntu/reports/' +
      String(index + 1).padStart(2, '0') + '-' + item.id + '.md. ' +
      'Return that exact path in report_path.',
      {brief: `Research ${item.name}`, sandbox: 'shared'}
    )
  ),
  {schema: itemSchema}
)

const successful = mapped.filter(r => r.ok).map(r => r.value)
const failures = mapped
  .map((r, i) => (r.ok ? null : {item: items[i].name, code: r.error.code, message: r.error.message}))
  .filter(Boolean)

const reduced = await agent(
  'Create the final cross-item report using these structured results:\n' +
  JSON.stringify(successful) + '\n' +
  'Include a comparison table, key differences, shared patterns, and a clear conclusion. ' +
  'Save it to /home/ubuntu/reports/final-report.md and return that path in report_path.',
  {
    brief: 'Synthesize final report',
    sandbox: 'shared',
    schema: JSON.stringify({
      type: 'object',
      properties: {report_path: {type: 'string'}, summary: {type: 'string'}},
      required: ['report_path', 'summary']
    })
  }
)

return {items: successful, failures, final: reduced.ok ? reduced.value : null}
```

Budgets for this shape: `estimated_agent_calls = items.length + 1`, `max_agent_calls = items.length + 1`, `failure_policy = collect`.

## Final checklist

Before calling `workflow/run`, verify:

- The task genuinely contains multiple independent units of work — each needing independent research or judgment, not the same deterministic command with different parameters — with one agent per item and no bundling.
- Item prompts are self-contained; comparable agents share a JSON Schema; the group has a clear user-facing brief.
- File paths are deterministic and collision-free; shared-mode outputs are verified by the parent task; inputs are declared as parent-sandbox paths in `input_files`.
- Discovery and reducer agents are counted in the budgets; `collect` failures are handled explicitly.
- The script is valid deterministic JavaScript only.
- The parent agent is orchestrating, not doing item-level work itself.
