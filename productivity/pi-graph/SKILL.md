---
name: pi-graph
description: Build, run, and iterate on Pi agent graphs (pi-graph) — explicit-state multi-agent workflows with isolated/thread/shared context modes, schema-validated node handoffs, conditional routing, fan-out/barrier, durable checkpoints, and human approval gates. Use when the user wants to design a multi-agent workflow, set up a pi-graph, orchestrate specialized agents (researcher/writer/reviewer loops, parallel fan-out, idea tournaments, human-in-the-loop approval), define reliable structured outputs between nodes, author a graph JSON, or validate/run/resume/visualize a graph. Reach for this only when the task genuinely needs specialization, parallelism, independent review, or persistent role memory — otherwise prefer a single agent loop.
---

# Pi Graph

`pi-graph` orchestrates multi-agent workflows as **explicit state graphs**: nodes, schema-validated handoffs, static and conditional edges, reducers, supersteps, durable checkpoints, and interrupts. It is a Pi extension modeled on LangGraph's low-level orchestration.

**Loop first.** A graph is overhead. Use one only when the task genuinely needs it (see below). For ordinary work, stay in a normal Pi agent loop — a single-node graph even emits a compile warning.

## Decide: graph or loop?

Reach for a graph only if **at least one** is true:

- **Distinct specialties** — two or more roles that should not share one context (e.g. a researcher vs. a skeptical reviewer).
- **Parallelism** — fan-out (run N branches at once) or barrier fan-in (wait for N sources).
- **Independent reviewer with teeth** — a node that can reject work and route it back for revision.
- **Persistent role memory** across iterations (`thread`), or an **auditable shared transcript** (`shared`).
- **Different models / tools / budgets per step.**
- **Typed handoffs** — downstream edges or nodes depend on required fields and JSON types, so malformed model output must fail before state commit.
- **Human-in-the-loop** approval, choice, or input gates.
- **Failure isolation** between steps (retry, continue, or route on error without losing graph state).

If none apply, do not build a graph.

## Install & discover

Install the published package:

```bash
pi install npm:@shying/pi-graph
```

For source development, run one of these from the repository root:

```bash
pi install .
pi --no-extensions -e ./extensions/pi-graph.ts
```

Graphs are discovered from:

- User: `~/.pi/agent/graphs/*.json`
- Project (trusted projects only): `<project>/.pi/graphs/*.json`

Project graphs override same-named user graphs. **Tools and commands accept only discovered graph names — never raw file paths.**

## The three context modes (most important decision)

Every `agent` node declares a `context.mode`. Pick deliberately by role semantics.

| Mode | When to use | Memory |
|---|---|---|
| `isolated` | Independent judgment, parallel branches, one-shot experts, **reviewers**. | None private — passes via graph state / files only. |
| `thread` | **Default** since 0.1.0. Same role revisits across loops (implement → fix → implement). | Reopens one private Pi JSONL history per `threadKey` in a new `AgentSession`. |
| `shared` | Several nodes share an auditable conversation (ReAct-style handoff). | Role-tagged messages appended to graph state. |

How to choose:

```
Role needs working memory preserved across loops   → thread (default)
Several nodes must share an auditable conversation → shared
Node must judge independently or run in parallel   → isolated
Plain deterministic transform (no model)           → set
Needs human approval / choice / input              → human
```

Hard rules (the compiler warns/violates on these):

- A `purpose: "reviewer"` node should be `isolated` **and** `readOnly`.
- Nodes sharing a `threadKey` must share the same `cwd` and never run concurrently in one superstep.
- `thread` retry creates a new `AgentSession` and re-appends to the same JSONL history → set `maxAttempts: 1` on thread nodes; let the graph loop do revisions.
- A lost `thread` session fails recovery closed — the runner never silently resets role memory.

## Authoring workflow

1. **Name** the graph and pick the `entry` node(s) (array = parallel start).
2. **List roles.** For each `agent` node decide: context mode, `output` path, `readOnly`, model/tools/budget.
3. **Define handoff contracts.** Add `response.schema` whenever downstream logic depends on a fixed JSON shape. Use plain `response.format: "json"` only when syntax is enough.
4. **Draw control flow.** Put every connection in `edges`: use top-level `to` for static edges or `cases`/`default` for conditional edges. Mark fan-out (`to: [...]`) and barrier fan-in (`from: [...]`).
5. **Reducers and lifecycle.** Any path written by parallel nodes needs a reducer. Use `collect` for current-round fan-in, `append` only for intentional history, and `overwrite`/`unset` set assignments to clear stale working state.
6. **State hygiene.** Keep full reports/transcripts in `response.storage: "artifact"`; keep summaries and artifact references in state. Never put the same large path in both a template and `reads`.
7. **Result projection.** Set top-level `result.paths` and `includeState: false` so the parent Pi does not receive the entire internal state. **Do not add `limits` by default** — omitting them means nodes run to natural completion, exactly like a normal Pi session. A premature `maxTurns`/`timeoutMs` cap kills legitimate long tasks mid-run and the work is lost. Add a cap only for a concrete reason (cost control, untrusted model, user-requested budget).
8. **Validate → run → iterate.** Don't skip validate.

### Minimal skeleton (adapt this)

```json
{
  "schemaVersion": 2,
  "name": "research-review",
  "entry": "researcher",
  "nodes": {
    "researcher": {
      "type": "agent",
      "prompt": "Research {{input.task}}",
      "readOnly": true,
      "context": { "mode": "isolated" },
      "output": "notes"
    },
    "writer": {
      "type": "agent",
      "prompt": "Write from {{notes}}. Prior review: {{review}}",
      "readOnly": true,
      "context": { "mode": "thread", "threadKey": "writer" },
      "output": "draft"
    },
    "reviewer": {
      "type": "agent",
      "purpose": "reviewer",
      "prompt": "Review {{draft}} and return {\"approved\": boolean, \"issues\": string[]}",
      "readOnly": true,
      "context": { "mode": "isolated" },
      "output": "review",
      "response": {
        "schema": {
          "type": "object",
          "properties": {
            "approved": { "type": "boolean" },
            "issues": { "type": "array", "items": { "type": "string" }, "maxItems": 20 }
          },
          "required": ["approved", "issues"],
          "additionalProperties": false
        }
      }
    }
  },
  "edges": [
    { "from": "researcher", "to": "writer" },
    { "from": "writer", "to": "reviewer" },
    {
      "from": "reviewer",
      "cases": [
        { "when": { "path": "review.approved", "op": "eq", "value": true }, "to": "__end__" }
      ],
      "default": "writer"
    }
  ],
  "policy": { "allowNonInteractive": true }
}
```

No `limits` block: agent nodes then run uncapped like normal Pi. Add one only when you specifically need a guardrail.

**Full schema:** `../../docs/SCHEMA.md`. **Worked examples** (copy and adapt): `../../examples/` — `research-review` (parallel research + thread writer + isolated reviewer), `coding-review` (thread coder + reviewer + human approval), `shared-handoff` (shared channel), `idea-tournament` (3-way fan-out + barrier judge), `science-research` (planner → parallel branches → evidence review → integrate → report).

## Structured node handoffs

Use `response.schema` on an `agent` node when a downstream node, conditional edge, reducer, or result projection relies on a stable JSON shape:

```json
{
  "type": "agent",
  "prompt": "Classify {{input.ticket}}",
  "readOnly": true,
  "tools": [],
  "output": "classification",
  "response": {
    "schema": {
      "type": "object",
      "properties": {
        "priority": { "type": "string", "enum": ["low", "medium", "high"] },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "maxItems": 10,
          "uniqueItems": true
        }
      },
      "required": ["priority", "confidence", "tags"],
      "additionalProperties": false
    },
    "maxBytes": 8192
  }
}
```

Choose the response mode deliberately:

| Configuration | Guarantee | Use when |
|---|---|---|
| no `response` / `format: "text"` | text only | prose, code, Markdown |
| `format: "json"` | parseable JSON syntax | the JSON shape is intentionally open |
| `schema: {...}` | JSON plus field/type/value constraints | downstream logic depends on the shape |

`schema` implies JSON. Never combine it with `format: "text"`; the compiler rejects that combination. `format: "json"` may be omitted when `schema` is present.

Runtime enforcement follows the structured-output pattern:

1. Graph compilation rejects malformed, keyword-less, or ineffective schemas before any model starts.
2. `InProcessPiAgentRuntime` injects an invocation-local `pi_graph_node_output` custom tool, even when the node declares `tools: []`.
3. The schema is included in the node prompt and tool description. The model must submit its final value through the tool rather than plain assistant text.
4. A hook steers the model up to two times if it omits the tool or its call fails validation.
5. Tool execution validates the value, and the parent executor validates it again immediately before writing graph state.
6. Missing or invalid structured output is a retryable node failure. No output write or shared-message capture is committed, so downstream nodes never observe the malformed value.

Schema authoring rules:

- Declare every field downstream logic reads in `properties`, and put mandatory fields in `required`.
- Prefer `additionalProperties: false` for control decisions, reviewer verdicts, and router inputs.
- Bound collections and strings with `maxItems` / `maxLength`; `response.maxBytes` still limits the serialized whole value.
- Use `enum`, numeric bounds, and nested schemas instead of encoding constraints only in the prompt.
- Local `$ref`, `$defs`, boolean schemas, and common object/array/composition keywords are supported.
- Do not use `{}` or an object without validation keywords as a schema; compile rejects accept-all shapes. Although `true` is legal, avoid it when the goal is a meaningful contract.

Interactions:

- `retry.maxAttempts` applies after the two in-session steering attempts. If the node can perform external side effects before submitting output, retries still require `idempotent: true` and a real idempotency design.
- Each assistant response caused by an in-session steer counts toward `limits.maxTurns`; it is a real model call with token and cost usage. Budget a schema node for its normal task turns plus up to two recovery turns.
- With `response.storage: "state"` (default), the validated JSON value is written to `output` and is what downstream nodes read.
- With `response.storage: "artifact"`, the validated JSON body is stored in the artifact while state receives an `ArtifactReference`; JSON is the default media type.
- Shared `compact` capture references the committed output path. Validation happens before both the output and shared-message writes.
- `response.schema` validates an agent's response payload only. It is not a graph-wide schema for `initialState`, `set`/`human` outputs, arbitrary state paths, or artifact references.

## Edges and reducers

```jsonc
// plain
{ "from": "a", "to": "b" }
// fan-out
{ "from": "a", "to": ["b", "c"] }
// barrier fan-in (join waits for all sources)
{ "from": ["b", "c"], "to": "join" }
// conditional edge
{
  "from": "reviewer",
  "cases": [
    { "when": { "path": "review.approved", "op": "eq", "value": true }, "to": "__end__" }
  ],
  "default": "writer"
}
```

Condition DSL (no `eval`): `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `exists`, `truthy`, `includes`, `matches`, combinators `all` / `any` / `not`.

Reducers for write conflicts: `replace`, `append`, `collect`, `concat`, `merge`, `sum`, `min`, `max`. `collect` discards the previous round and keeps only the current superstep batch; use it for refinement loops. Two parallel nodes writing the same path without a reducer → run fails. A parent and child path written in the same superstep is also rejected.

## State and token hygiene

Use a three-tier convention:

```text
working  current-round data; unset before refinement
memory   compact summaries retained across rounds
result   final summary and artifact references
```

- `append` is historical accumulation; it is wrong for a fixed set of branch results across refinement rounds. Use `collect`. Treat `ACCUMULATING_REDUCER_IN_CYCLE` as a design defect unless the history is intentionally bounded elsewhere.
- Default shared capture is `compact`, which stores a state reference rather than a duplicate body. Set `maxStoredMessages` for durable retention. Use `assistant-only` + `storeOutput: false` when the channel should be the canonical copy. Avoid `full` unless a transcript is an explicit requirement.
- Store full Markdown/JSON/text with `response.storage: "artifact"`.
- Use `response.schema` for structured agent handoffs. It implies JSON output and prevents malformed data from reaching downstream nodes; see **Structured node handoffs** above. Use plain `response.format: "json"` only when JSON syntax without a fixed shape is sufficient.
- Use top-level `result.paths` and leave `includeState: false` so the parent Pi does not receive the entire internal state.
- Prompt preflight fails before creating the Pi `AgentSession` when rendered bytes exceed graph/node `maxPromptBytes`.

## Limits & policy

**Every `limits` field is optional — omitting it disables that cap entirely.** The default way to author a graph is with no `limits` at all: nodes run until the task completes, matching normal Pi behavior. Only add the specific cap you actually need:

- Graph `limits` (optional): `maxSteps`, `maxNodeRuns`, `maxConcurrency`, `maxCostUsd`, `timeoutMs`, `maxStateBytes`, `maxPromptBytes`.
- Node `limits` (optional): `maxCostUsd`, `timeoutMs`, `maxTurns`, `maxPromptBytes`. `response.maxBytes` bounds agent output; `statePolicy.paths` sets exact-path byte budgets.

A task that outgrows a cap fails with its work discarded (state is committed only after node success), so size any cap to the real task or leave it unset.

`policy`:

- Non-interactive runs require `allowNonInteractive: true`.
- Non-interactive **mutations** additionally require `allowNonInteractiveMutations: true`.
- Graphs using `bash`/`edit`/`write` or unknown tools require confirmation by default.

## Validate, run, resume

```text
/pig list
/pig validate research-review        # always validate first
/pig run research-review <task text or JSON object>
/pig resume <runId> <value or JSON>  # after a human interrupt
/pig inspect [runId] [--inventory|--full|state.path]
/pig delete <runId>                 # confirms, then removes all run data
```

Or via tools (the model calls these; the three tools are excluded from every node `AgentSession` to prevent hidden recursion):

- `pi_graph_run` — `{ graph, task, checkpoint }`; input lands at `state.input`.
- `pi_graph_resume` — `{ runId, value | valueJson }` to satisfy a human node.
- `pi_graph_inspect` — summary-first checkpoint inspection, state inventory/path views, or explicit full records.

The checkpoint store lives at `~/.pi/agent/pi-graph/runs/`. Its authoritative record is the immutable journal under `.journal/<runId>/`; `<runId>.json` is only a best-effort human-readable mirror. Recovery re-runs only unresolved nodes. Resuming after the graph **definition** changed is refused by default; set `forceGraphVersion: true` only after checking state compatibility and side-effect idempotency.

Graph persistence is independent of agent process boundaries: GraphEngine checkpoints scheduling, durable node resolutions, committed state/control, interrupts, and terminal status while skipping redundant boundary writes. `PiNodeExecutor` uses the `NodeAgentRuntime` seam; its default `InProcessPiAgentRuntime` calls `createAgentSession` once per invocation. Isolated/shared sessions are in memory, while thread invocations reopen the private JSONL history in a new `AgentSession`.

## Human nodes

```json
{ "type": "human", "kind": "confirm", "prompt": "Approve this plan: {{draft}}", "output": "approved" }
```

A human node pauses the run and returns an `interrupt` + `runId`. Resume with the user's answer. Use for approvals, choices, or requesting missing input.

In the TUI, an interrupted `input`/`confirm`/`select` node is auto-captured: the extension holds the live board and the user's next chat message is routed directly as the resume value (`/` commands pass through; `/pig skip` releases capture).

## Failures & retries

```json
"onError": { "strategy": "fail" }                         // default: stop, keep checkpoint
"onError": { "strategy": "continue", "output": "errors.x" }
"onError": { "strategy": "route", "to": "fallback", "output": "errors.x" }
"retry": { "maxAttempts": 3, "backoffMs": 500, "backoffMultiplier": 2 },
"idempotent": true
```

`idempotent: true` is a **design declaration** — it does not make external side effects idempotent. State is committed only after a node succeeds, so failed/interrupted nodes never write half-finished output.

For schema nodes, distinguish two retry layers: the structured-output hook first steers up to two times inside one Pi invocation; if no valid tool result is produced, normal node retry / `onError` handling begins. Route schema failures to a repair/fallback node when graceful degradation matters.

## Visualize

```text
/pig visualize research-review
```

Renders the graph as a Mermaid `flowchart LR` in the TUI. Shapes: `agent` → stadium `([id])`, `set` → `[[id]]`, `human` → hexagon `{id}`, `__end__` → circle `((end))`. Solid arrows = static edges; dashed labeled arrows = conditional edges (`else` = default branch). Entry nodes get a green border. Use this to sanity-check topology before running.

## Inspect & debug

- `/pig inspect <runId>` — compact status, usage, pending work, state bytes, and largest paths.
- `/pig inspect <runId> --inventory` — state path/type/size inventory.
- `/pig inspect <runId> working.reviewed_evidence` — one state path.
- `/pig inspect <runId> --full` — complete checkpoint, explicitly requested and byte capped.
- `/pig delete <runId>` — confirm and remove the checkpoint, private thread history, and artifacts; active runs are rejected.
- Stuck after a definition edit? You hit the graph-hash guard — review state compatibility, then `forceGraphVersion`.
- `thread` run won't resume? The private session file may be missing — recovery fails closed by design.
- Cost overshoot near its limit is expected; enforcement relies on provider usage events and a single in-flight response can slightly exceed before termination.

## Boundaries to respect

- `shared` is an explicit transcript projection into a fresh in-memory `AgentSession` — not a hidden shared session, and not provider-native message-array injection.
- `thread` continuity is real, but the graph checkpoint and the Pi JSONL session are **two non-atomic** persistence objects; back up / migrate both and never treat either as an atomic copy of the other.
- Checkpoints are **at-least-once**; external side effects are not guaranteed exactly-once.
- GraphEngine enforces graph and node deadlines for every `NodeExecutor` through `NodeExecutionContext.signal`; executors must stop promptly. The Pi runtime maps that signal to `session.abort()`. Cancellation remains cooperative, with no child-process `SIGKILL` fallback, so a provider or tool may finish after the nominal deadline if it delays cancellation.
- `readOnly` is a tool allowlist, **not** an OS sandbox. For high-risk execution use a container.
- Read-only nodes default to `read`, `grep`, `find`, and `ls`. They may explicitly request `web_search`, `fetch_content`, or `get_search_content` when `loadExtensions: true`; other extension tools remain rejected.
- Treat every `loadExtensions: true` graph as potentially mutating for authorization, even when its active tool list is read-only: Pi executes all configured extension initialization code. Headless runs therefore also need `policy.allowNonInteractiveMutations: true`.
- `response.schema` protects one agent output boundary, not every value already present in graph state.
- Graph format is `schemaVersion: 2`; other schema versions are rejected.
