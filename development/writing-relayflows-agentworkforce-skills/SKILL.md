---
name: writing-relayflows
description: Use when authoring a Relayflows flow (@relayflows/surface / @relayflows/sdk, the journal-based v2 engine — the CLI is `flows`, package versions 2.0.x) in TypeScript or YAML/JSON. Covers the run/llm/agent ladder, direct child flows with use/dispatch, verification gates, cli/model selection, flows.json, parallel agents, Cloud dashboard mirroring, and `flows check`/`run`/`deploy`/`schedule` refusal shapes. Do not use the older, unrelated `@relayflows/core` WorkflowBuilder engine for new work.
---

# Writing Relayflows

## Overview

Relayflows turns a coding-agent task into steps a journal can inspect, verify, and resume. A flow is data (YAML/JSON) or code (TypeScript) that compiles to the same journal-backed kernel spec. Every effect is journaled before it's treated as real — a journal write that fails fails the step, with no silent fallback.

**Name collision warning.** An older, unrelated engine is also casually called "Relayflow" (singular): `@relayflows/core`'s `WorkflowBuilder`, a chained builder (`workflow('name').pattern('dag').agent(...).step(...).run()`). This skill is the **v2** engine: `@relayflows/surface`'s `flow()` function and the YAML/JSON dialect compiled by `@relayflows/sdk`. If you see `.pattern(`, `.agent(` as a chained builder call, or `ctx.workflow.run()`, you are looking at legacy code. Do not use that syntax for new work; keep v2 guidance inside this skill.

## When to use this skill

- Writing a new `.flow.ts` or `.flow.yaml`/`.flow.json` for the `flows` CLI (package `@relayflows/sdk`, binary name `flows`).
- Deciding whether a step needs `run` (shell), `llm` (bare model call), or `agent` (harnessed coding agent in a workspace).
- Choosing a verification gate that will actually run — a wrong choice here compiles fine and fails at `flows run` time, not authoring time.
- Wiring up `cli`/`model` for an `agent` or `llm` step, in either language.
- Debugging a `REFUSED [...]` message from `flows check` or `flows run`.
- Deciding between running a flow locally, deploying it to listen for tickets, or scheduling it on a cron.

## The ladder

Three step verbs, one per rung (`@relayflows/sdk`'s `StepType = 'deterministic' | 'llm' | 'agent'`):

1. **`run` / `deterministic`** — a shell command. No model. Implicit gate is `exit_code == 0`.
2. **`llm` / `llm`** — a bare model call. Prompt in, verified output out. No workspace, no tool use.
3. **`agent` / `agent`** — a harnessed coding agent in a workspace. Returns `{ summary, artifacts }`, not raw text.

Plus resident verbs that aren't ladder rungs: `human` (durable approval), `dispatch` (a direct child flow declared in `use`), and `done` (typed finish). `dispatch` executes in `2.0.35` and newer; see **Human approval and direct child flows**. The generated **helper** namespace (`f.slack`, `f.github`, `f.linear`, `f.notion`, `f.jira`, and 30+ others — see **Helpers**) and YAML `on`/triggers are separate surfaces.

Most flows only need `run` and `llm`. Climb to `agent` once a step needs hands on a real workspace.

## Two ways to author the same thing

**YAML/JSON** is data: `flows check` or CI can validate it without running anything. **TypeScript** calls the same primitives imperatively as ordinary async code. Both compile to the same journal.

### TypeScript

```ts
import { flow } from '@relayflows/surface';

export default flow('hello', { budget: { wallclock: '10m' } }, async (f) => {
  const greeting = await f.run('echo "Hello from Relayflows"');
  console.log(greeting.trim());

  const answer = await f.agent('greeter', {
    task: 'Reply with one short hello sentence. Do not use tools or modify files.',
    cli: 'claude',
    model: 'claude-sonnet-4-6',
  });
  console.log(answer.summary);

  f.done('success');
});
```

### YAML

```yaml
version: '0.1.0'
name: hello
steps:
  - id: greeting
    type: deterministic
    command: 'echo "Hello from Relayflows"'
  - id: greeter
    type: agent
    dependsOn: [greeting]
    instruction: 'Reply with one short hello sentence. Do not use tools or modify files.'
    cli: claude
    model: claude-sonnet-4-6
```

**Version note.** The contracts below were checked against the published `@relayflows/surface@2.0.35` / `@relayflows/sdk@2.0.35` declarations. Direct `use`/`f.dispatch` composition requires `2.0.35` or newer. `AgentOptions.permissions` landed in `2.0.17`; predicate `.gate()` and `artifact_exists` landed with [flows#449](https://github.com/AgentWorkforce/flows/pull/449); `f.human` was already executable in `2.0.22`.

## The real `Ctx` contract (TypeScript)

From the shipped `@relayflows/surface@2.0.35` `.d.ts` files (`dist/context.d.ts`, `dist/step.d.ts`, `dist/flow.d.ts`, `dist/completion.d.ts`):

```ts
export interface AgentResult {
  summary: string;
  artifacts: string[];
}

export interface PermissionsSpec {     // exported from the package root
  fileGlobs?: string[];
  networkAllowlist?: string[];
  accessPreset?: 'readonly' | 'readwrite';
}

export interface AgentOptions {
  task: string;
  workspace?: string;
  permissions?: PermissionsSpec;         // since 2.0.17 — declared and journaled, NOT enforced
  cli?: string;
  model?: string;
  cwd?: string;                          // working dir for the CLI subprocess; defaults to the flow-runner's cwd
  transport?: 'direct' | 'relay';        // see Agent-relay transport, below
}

export interface LlmOptions {
  output: Record<string, unknown>;       // JSON Schema, checked before the journal accepts the result
  cli?: string;
  model?: string;
}

export interface DispatchResult {
  name: string;
  completionReason: 'success';
  completionDetail?: string;
}

export interface Ctx extends Helpers {   // Helpers = f.slack, f.github, f.linear, f.notion, ... — see Helpers
  readonly mcp: Readonly<Record<string, Readonly<Record<string, (args: unknown) => Step<unknown>>>>>;
  run(command: string, options?: { timeout?: string | number }): Step<string>;
  llm(strings: TemplateStringsArray, ...values: unknown[]): Step<string>;
  llm(prompt: string, options: LlmOptions): Step<unknown>;
  agent(name: string, options: AgentOptions): Step<AgentResult>;
  human(question: string, options: { to: string }): Step<boolean>;
  dispatch(flow: string, input: unknown): Step<DispatchResult>;
  done(reason: FlowCompletionReason): void;
  cloud: CloudHelper;
  memory: MemoryHelper;
}
```

Do not add fields to `AgentOptions`/`Ctx` that aren't in this list — they don't exist in the shipped SDK. In particular: **no flow-level named-agent selector on `f.agent`, no `recoveryMode`/`surfaces`/`output`** on the TypeScript call site. Those stay YAML/JSON step fields. `FlowHeader` (`dist/flow.d.ts`) allows `use`, `identity`, `memory`, `budget`, `tools`, `workspace` — no bare `agents` map key (TypeScript composes reusable flows via `use: string[]` instead — see **Named agents and flow composition**). An unknown *header* field throws a `TypeError` at authoring time, before anything is journaled; an unknown `AgentOptions` field is caught by `tsc`, not at runtime.

**`permissions` is a real TypeScript option and it does not sandbox anything.** Since `2.0.17` it is on `AgentOptions`, validated by the SDK, lowered to `file_globs`/`network_allowlist`/`access_preset` and journaled with the step — and nothing reads it to gate a file or a network call. `flows check` warns `permissions_unenforced` on any declaration, including `{}`. Enforcement is [flows#442](https://github.com/AgentWorkforce/flows/issues/442). Declare it to record intent; do not rely on it to contain an agent.

`run()`'s second argument is a real, current option: `{ timeout?: string | number }` — a duration string (`"15m"`) or milliseconds. Every real cookbook example that runs something slower than a few seconds sets this explicitly.

### `f.done()`'s closed set is six values, not four

```ts
export const FLOW_COMPLETION_REASONS = ['success', 'step_failed', 'canceled', 'budget_exceeded', 'needs_human', 'declined'] as const;
```

An authored body can meaningfully call `f.done('success')`, `f.done('step_failed')`, `f.done('needs_human')` (parks the run — it's not a kernel cancellation), or `f.done('declined')` (a deliberate decision not to act — also not a cancellation). `'canceled'` and `'budget_exceeded'` exist in the same closed set but are the **kernel's** to record; a body calling them itself is calling the wrong verdict for what actually happened. The verdict for a human declining a durable approval is `f.done('declined')`, not `f.done('canceled')` — a human declining is a decision, not the kernel calling off the run.

`Step<T>` (`dist/step.d.ts`) is a `PromiseLike<T>` with one extra method, `.gate(...)` — see **Verification gates**. Every awaited step must actually be awaited — an unawaited or manually-`.then()`-chained step is refused (`unawaited_step` / a manual `.then()` is not an await), not silently dropped.

## Verification gates

Verification is control flow, not decoration — a gate decides whether a step actually completed, not just whether the process exited cleanly.

### YAML/JSON (`@relayflows/sdk`'s `VerificationSpec`)

```ts
export type VerificationSpec = ExitCodeGate | OutputContainsGate | JsonSchemaGate | NamedDataGate;
// NamedDataGate = ReferencesInputGate | SubprocessGate | WordCountBoundsGate | RegexMatchGate
//              | ArtifactExistsGate
```

- `exit_code` — implicit default for `deterministic` steps. Not configurable; writing it explicitly is allowed and compiles to the same thing as omitting it.
- `output_contains` — step output (stdout tail, or the LLM value stringified) contains `value`.
- `json_schema` — step output validates against a JSON Schema (`boolean | Record<string, unknown>`). Used for structured LLM/agent output; `output?: JsonOutputSchema` on an `llm`/`agent` step is sugar that compiles to this.
- `subprocess_gate` — runs `command` under `/bin/sh`, judged on its exit code. The gate that actually works for "check a file the agent wrote": `{ type: 'subprocess_gate', command: 'test -s review.md' }`. If you also need to inspect the step's own output (via `from_output`), the SDK's generated wrapper reads its internal `FLOWS_INPUT` env var, extracts the value, and passes it to *your* command as `$INPUT` — `FLOWS_INPUT` itself is never visible to the author's command, only `$INPUT` is: `{ type: 'subprocess_gate', command: 'echo "$INPUT" | grep -q PASSED', from_output: ['summary'] }`.
- `regex_match` — the step's output (or a value at `in_output_at`) matches `pattern`, evaluated by a non-backtracking RE2 engine (only `i`, `m`, `s` flags).
- `artifact_exists` — passes when the step's journaled `artifacts` list contains `path` (working-directory-relative POSIX). It reads the journal, not the disk, so it sees exactly what the worker measured at `step.completed`; a path the worker never journaled reads as missing even when the file is there.
- `word_count_bounds`, `references_input` — narrower named gates; see `packages/sdk/src/named-gates.ts` in the flows repo for the exact contract.

```yaml
- id: classify
  type: llm
  prompt: 'Classify this ticket as bug, feature, or question: "the export button does nothing"'
  cli: claude
  model: claude-sonnet-4-6
  verification:
    type: output_contains
    value: bug
```

### TypeScript (`Step<T>.gate(...)`) — read this before you write one

`Step<T>` has **two** overloads, and **one `.gate()` per step** — a second throws `unsupported_gate`:

```ts
gate(config: NamedGate): Step<T>;
// NamedGate = ReferencesInputNamedGate | SubprocessNamedGate | WordCountBoundsNamedGate
//           | RegexMatchNamedGate | ArtifactExistsNamedGate
// — the surface-visible subset of NamedDataGate above. Data, not code: `flows check` can prove it.

gate(predicate: (value: T) => boolean, because?: string): Step<T>;
// Runs since flows#449. The executor calls the closure once, on the journaled value, and
// journals the VERDICT as a lowered `<step>.gate` step — so resume and replay read the
// recorded verdict and never re-run the function. A false verdict fails the run as
// `gate_failed`, carrying `because`.
```

The predicate form was refused with `unsupported_gate` through `2.0.16`; on `2.0.22` it runs. **Prefer the config-object form anyway** — `flows check` cannot prove a predicate (docs/SURFACE.md §6), so a named gate is the only kind a preflight can tell you about before you spend a run:

```ts
const outdated = await f.run('npm outdated --json 2>/dev/null || true')
  .gate({ type: 'subprocess_gate', command: 'test -n "$INPUT"' });   // provable by `flows check`

const review = await f.agent('review', { task: '…', cli: 'claude' })
  .gate({ type: 'subprocess_gate', command: 'test -s review.md' });  // checks a file the agent wrote, ignores $INPUT
```

(Verified for real: `.gate({ type: 'subprocess_gate', command: 'test -n "$INPUT" && echo "$INPUT" | grep -q pkg' })` against a step outputting `{"pkg":"left-pad"}` passes — `$INPUT`, not `$FLOWS_INPUT`, is what the author's command sees. `FLOWS_INPUT` is an env var the SDK's own generated wrapper reads internally to extract the value before invoking your command; it is never visible to `command` itself.)

An agent step rarely fails by crashing; it fails by returning something plausible and wrong, which a plain retry-on-error never catches. Validate every `agent`/`llm` result, either directly with a supported gate or in a following deterministic verifier.

**Where to put that check depends on what you want a red result to do.** A config-object or predicate gate directly on the agent/LLM step ends the run when it fails; use it when that failure should be terminal. For repairable failures, the following deterministic verifier must explicitly read the preceding output or workspace, produce its own verification result, and record it for repair. Output-dependent gates inspect the step they guard: moving the same gate unchanged would inspect the verifier's output, not the agent's. Use the record/repair/re-record/assert pattern in `relay-80-100-workflow`, gating the final verification result after repair.

## Helpers: journaled effects, not just Slack

`Ctx extends Helpers`, and `Helpers` is generated from 40+ provider adapters shipped in `@relayflows/surface` — `slack`, `github`, `linear`, `jira`, `notion`, `salesforce`, `postgres`, `s3`, `redis`, `daytona`, `gmail`, `google-calendar`, `hubspot`, and more (`dist/helpers/index.d.ts` lists them all). A helper call — `f.slack.post(channel, text)`, `f.github.comment(...)` — compiles to a journaled effect: the receipt the helper returns *is* the journal record, so a retried step that already posted doesn't double-post; the second attempt is deduped by `(step_id, idempotency_key, surface_path)`.

Two things every helper call needs:

- **A relayfile mount for that provider**, locally — `flows check` refuses `helper_slack.credential_missing` (or the equivalent for another provider) without one. Cloud provides a mount for every connected provider automatically.
- **A declared intent** on the flow header: `tools: { slack: true }` in TypeScript, or the equivalent in YAML. Forgetting this is a separate, earlier failure than the mount check.

For local development without standing up a real provider mount, prefix the run with the provider's mock env var — `RELAYFLOWS_SLACK_MOCK=1 flows run ... --local-agent` records the effect (a real file under the daemon's data dir) instead of sending it. This does not exercise live delivery, and should be called out as such wherever you cite it as verification.

**`tools` means two different things depending on where you write it — do not confuse them:**

- `FlowHeader.tools` (TypeScript) / `FlowSpec` top-level `tools` you're declaring intent on: `Partial<Record<keyof Helpers, boolean>> & { relayfile?: string[]; mcp?: string[] }` — e.g. `{ slack: true }`. This is "which helpers this flow uses."
- `FlowSpec.tools` in the compiled YAML/JSON spec is instead `{ fs?: string | string[] }` — path-scoped **filesystem** grants, mirroring `workspace` for shell/deterministic steps. Not the same field, despite the identical name.
- `flows.json` (the project config file) has **no** `tools` field at all — see **`flows.json`**, below. Putting a `tools` key there is refused as `config_invalid`; this is an easy, first-try mistake (made once, personally, writing this refresh).

## `cli` / `model`: what a step actually runs on

Both YAML and TypeScript agent/llm steps can set `cli` and `model` directly. Resolution order for `cli`, identical regardless of authoring language because both compile to the same `StepSpec`:

1. **step** — `step.cli` (or TS's `options.cli`)
2. **named** — the flow's `agents[step.agent]` entry, if the step selects one via `agent: <name>` (YAML/JSON only — TypeScript composes reusable flows via `use:` instead, not a per-step named-agent selector; see **Named agents and flow composition**)
3. **flow** — `FlowSpec.cli` (YAML) — there is no equivalent flow-level `cli` field on the TypeScript `FlowHeader`
4. **project** — nearest `flows.json`'s `cli`, found by walking up from the flow file's directory

No resolution found at any level → `REFUSED [cli_unresolved]`, before anything is journaled, e.g.:

```
$ flows check hello.flow.yaml   # agent step, no cli anywhere
REFUSED [cli_unresolved] Step "greeter" has no CLI at step, flow, or project level. No flows.json was found from "..." to the filesystem root.
```

`model` has **no** flow or project default — only step or named-agent. Omitting it just runs whatever model the resolved CLI defaults to.

### `flows.json`

Nearest-wins project config, walking from the flow file's directory to the filesystem root. The shipped SDK type (`@relayflows/sdk`'s `FlowsJson`) is exactly:

```ts
interface FlowsJson {
  cli?: string;
  executors?: string[];
  models?: string[];
  mcp?: Record<string, McpServerConfig>;
  deploy?: { bucket: string };
}
```

- `cli` — the project-wide CLI default (resolution rung 4 above).
- `executors` — trigger executors this project has registered. A trigger whose `executor` isn't in this list is `no_executor`; a flow that declares `.on(...)` triggers but is invoked directly (not via a webhook) still needs its provider named here — e.g. `{ "executors": ["github"] }` for a flow with `.on(github.pull_request(...))` handlers, even when you never hit that code path.
- `models` — **an allowlist, not a default.** Any model declared on any step or named agent anywhere in the flow must appear here, or `flows check`/`flows run` refuses `model_unknown` / `llm_cli_unresolved`. Setting `models` does not select a model for anything.
- `mcp` — project-owned MCP server connections.
- `deploy` — a file-bucket target for `flows deploy <flow>@sha256:<digest> --to <bucket-uri>`.

**Verified for real:**

```
$ flows run hello.flow.ts --local-agent --input '{}'   # step declares model "claude-opus-5", flows.json has no models[]
REFUSED [invalid_spec] llm_cli_unresolved: Step "llm-1" declares model "claude-opus-5" for CLI "claude",
but it is not listed in project model registry "…/flows.json"; add the exact model only after verifying
that project is allowed to use it.

$ flows run pr-reviewer.flow.ts --local-agent --input '{...}'   # flow declares .on(github....) handlers, no executors[]
REFUSED [no_executor] webhook trigger "github" is not registered in flows.json
```

Any other top-level key — `tools`, `budget`, `identity`, `agents` — is refused as `config_invalid`. Those are `FlowHeader`/`FlowSpec` fields on the *flow itself*, not on the project config.

## Named agents and flow composition

**YAML/JSON**: a named-agent map declares each `{ cli, model }` pair once; a step's `agent:` selector resolves to it at compile time, and `flows check` flags a named agent nobody selects, or one a step overrides without using.

```yaml
agents:
  planner: { cli: claude, model: claude-opus-5 }
  implementer: { cli: codex, model: gpt-5.6-codex }
steps:
  - id: plan
    type: agent
    agent: planner
    instruction: '…'
```

**TypeScript** has no equivalent `agents:` map key on `FlowHeader` — the closest idiom is a plain object spread reused across calls:

```ts
const planner = { cli: 'claude', model: 'claude-opus-5' };
await f.agent('plan', { ...planner, task: '…' });
```

What TypeScript *does* have is `FlowHeader.use?: string[]`: relative `.flow.ts` paths to direct child flows the body may call with `f.dispatch`. This is composition of complete flows, not a named-agent map. It executes in `2.0.35` and newer; see **Human approval and direct child flows**.

## Parallel agents

Running several agent (or any) steps concurrently is first-class, documented authoring — not a workaround:

> "…`Promise.resolve`, `Promise.all`, `Promise.allSettled`, `Promise.any` and `Promise.race` over authored steps" are "ordinary, supported authoring." — `docs/SURFACE.md`, the authored operation lifecycle

```ts
const LENSES = ['security', 'correctness', 'performance'] as const;

await Promise.all(
  LENSES.map((lens) =>
    f.agent(`${lens}-reviewer`, {
      task: `Review this diff for ${lens} issues ONLY. Write findings to review/${lens}.json.`,
      cli: 'claude',
    }).gate({ type: 'subprocess_gate', command: `test -s review/${lens}.json` }),
  ),
);

const consensus = await f.agent('consensus', {
  task: 'Read review/*.json. Resolve disagreement between lenses. Write review/consensus.json.',
  cli: 'claude', // TypeScript has no flow-level cli; without it (or a flows.json default), flows run refuses with REFUSED [invalid_spec] and the unresolved CLI in the message
}).gate({ type: 'subprocess_gate', command: 'test -s review/consensus.json' });
```

This is the exact shape `examples/pr-review-pipeline` in `AgentWorkforce/flows` (and the cookbook's would-be equivalent) uses: fan out, each lane writes its own file, a reconciliation step reads them all. **Disclosure worth knowing before you rely on it**: the flows package replaces the global `Promise.all` intrinsic, process-wide, for the lifetime of any authored flow execution, so the kernel can prove every concurrent step was actually awaited (rather than inferring group membership from callback identity). It delegates to the real intrinsic and restores it when the last concurrent flow closes — but any other code sharing that process sees the replacement during that window.

## Agent-relay transport: dispatch, not live chat

`AgentOptions.transport?: 'direct' | 'relay'` (default `'direct'`, a local subprocess). Setting `transport: 'relay'` dispatches the step to Agent Relay's own task infrastructure instead — per the shipped type's own doc comment: *"posts to agent-relay so the agent registers as a first-class workspace participant that DMs can steer."*

What this actually is, per `docs/AGENT-RELAY-TRANSPORT.md`: the step calls `POST /v1/actions/task.run/invoke` against relaycast, then waits for a durable final receipt — spawn readiness and invocation acceptance do **not** complete the step, only a terminal receipt does. It needs a pre-provisioned `RELAY_AGENT_TOKEN` (a workspace API key cannot substitute) and the Relay provider running with `AGENT_RELAY_TASK_PROVIDER=1`. The dispatched worker submits its result via an injected `agent_result` tool.

Don't describe this as "agents talking to each other" — there's no documented pattern in this skill's scope for two flow steps to hold a live back-and-forth over Relay channels while both are running. What's real: the step's agent becomes a genuine Agent Relay workspace participant while it runs (so a human, or another agent with the right access, can DM it and potentially steer it — per the type's own wording), and the flow still only sees a request-and-durable-receipt shape, not an open channel. Multi-agent *coordination* inside a flow today means sequential handoff (one step's return value feeds the next) or parallel fan-out (**Parallel agents**, above) — not live messaging.

## Human approval and direct child flows

`f.human` parks a root run on a durable approval. `f.dispatch` executes a statically declared direct child in the same durable tree on `2.0.35` and newer. Both must be awaited.

`f.human` parks the run durably on a kernel `wait.human`, keyed `human-<n>` in the order the body asked. A person answers, and `flows resume` continues the body from that line:

```ts
const ok = await f.human(`Ship this?\n${plan.summary}`, { to: 'khaliq' });
if (!ok) return f.done('declined');   // a person's "no" is declined, never canceled
```

```
$ flows answer <run-id> human-1 yes --by khaliq --note 'reviewed the diff'
$ flows resume <run-id>
```

`to` names who is asked and is recorded with the question — **it is not a delivery address**; nothing notifies that person for you. The kernel closes a wait once, so the first answer wins, and it records `attribution: "client_asserted"` because the daemon socket, not the kernel, authenticated whoever `--by` names. The answer step takes a `.gate(config)` like any other step. One caveat: `f.human` needs a durable root run to park in — under a runner that has none it refuses with `unsupported_verb`, so run it with `flows run`.

For a composed local run, declare each direct child in the parent's static `use` header, then dispatch by the child's declared `flow(...)` name—not by its file path:

```ts
// release.flow.ts
import { flow } from '@relayflows/surface';

export default flow('release', { use: ['./implement.flow.ts'] }, async (f) => {
  await f.run("printf '%s' prepare");
  const child = await f.dispatch('implement', { issue: 123 });
  await f.run("printf '%s' publish");
  f.done(child.completionReason);
});
```

```ts
// implement.flow.ts
import { flow } from '@relayflows/surface';

export default flow('implement', async (f, input: { issue: number }) => {
  // The type is not a runtime check: dispatch input is JSON, so validate it
  // before it reaches a shell command.
  if (!Number.isSafeInteger(input.issue) || input.issue < 1) throw new Error('issue must be a positive safe integer');
  await f.run(`printf '%s' ${input.issue}`);
  f.done('success');
});
```

Interpolating step input into `f.run` is shell code: validate it (or quote it) first, because the TypeScript type of `input` is not checked at runtime.

`use` resolves relative `.flow.ts` files before a body runs. Missing or repeated files, duplicate direct-child names, cycles, and undeclared or transitive-only dispatch targets are refused. The child's steps receive qualified IDs such as `dispatch-2--run-1`; the dispatch receipt joins child leaves back to the parent's next step. Parent and child share one root budget and worker-capacity pool, and resume reuses journaled identities rather than repeating completed effects. A successful dispatch returns `{ name, completionReason: 'success', completionDetail? }`; any other child verdict fails the dispatch.

Authority narrows: a child cannot declare a second budget, require a helper/MCP capability its parent did not grant, or call `f.human`. Static cycles are refused and runtime child depth is capped at three. This is direct authored composition, not arbitrary public-flow invocation.

To put the **whole local tree** on one Cloud dashboard page, run `flows run --cloud-mirror release.flow.ts --input '{}'` (or affirmatively set `FLOWS_CLOUD_MIRROR=1`). The root, qualified child steps, dispatch receipts, dependency edges, transcripts, source, and output are projected into one connected graph; the local journal remains authoritative. Mirroring uploads that data and is opt-in. A mirror failure cannot fail the local run. The default observer link is separate and does not add the run to Cloud history.

Do not confuse this with **hosted execution**. `flows run --cloud [--sync-code] release.flow.ts --input '{}'` still rejects `use` dependencies with `unsupported_source`: Cloud accepts one self-contained `.flow.ts` source. Use `--cloud-mirror` for the connected child-flow dashboard today; do not promise that Cloud can itself execute a multi-file `use` tree.

**The same "types accept it, the executor doesn't" trap applies to `workspace` on an agent step under `--local-agent`.** Neither an annotated (`'acme/api: readonly'`) nor a bare (`'acme/api'`) value works — both fail identically:

```
REFUSED [invalid_spec] unsupported_workspace_permission: The local agent worker accepts
stream-only steps. Remove workspace or attach a worker that holds its revision pins.
```

It isn't the `: readonly`/`: readwrite` annotation syntax that's rejected — it's that the local-agent worker doesn't hold workspace revision pins at all. Omit `workspace` entirely for a step you intend to run with `--local-agent`; it's a real, working field only against a worker that supports it (Cloud's). Against a worker that does hold pins, the suffix is separately refused, and the remedy the SDK's own message names is `f.agent`'s `permissions` option — which records the scope and does not enforce it.

## Running it: `flows check` / `run` / `deploy` / `schedule`

```
flows check [--json] [--watch] <flow.ts|flow.yaml|spec.json>
flows run [--json] [--no-spawn] [--no-observer-link] [--cloud-mirror] [--data-dir <dir>] [--local-agent] <flow.yaml|spec.json>
flows run [--json] [--no-spawn] [--no-observer-link] [--cloud-mirror] [--data-dir <dir>] [--local-agent] <flow.ts> --input <inline-json-or-file>
flows resume [--allow-human-influenced] [--json] [--no-spawn] [--no-observer-link] [--cloud-mirror] [--data-dir <dir>] [--local-agent] <run-id>
flows deploy <flow.ts> --repo <owner/name> --on <provider>[:key=value,...] [--on ...] --approver <handle> [--agents claude[,codex]] [--name <name>] [--draft] [--json]
flows deployments [--json]
flows undeploy [--json] <deployment-id>
flows schedule <flow.ts> --cron "<expr>" --tz <tz> --input <inline-json-or-file>
```

`check` is a pure compile-and-preflight — no daemon, no socket, no data dir. It's the fast, safe way to validate a flow before ever running it, and it does accept `.flow.ts` despite older `--help` text implying only YAML/JSON.

**`--local-agent` is not optional decoration.** Without it, `agent`/`llm` steps have no worker to dispatch to and the run parks indefinitely rather than executing. Every local run in this skill's examples, and every real run in [`AgentWorkforce/flows-cookbook`](https://github.com/AgentWorkforce/flows-cookbook), passes it.

A `.flow.ts` run via `flows run` requires `--input <inline-json-or-file>` even when the flow body ignores its input argument.

**`--data-dir` gotcha, learned the hard way.** If a flow does its own git hygiene on the directory you invoke it from — `pr-reviewer`'s and similar examples' `git clean -fdq -e .workforce` when there's nothing to push — that cleanup deletes *anything else untracked in that directory*, including the daemon's own default `.relayflowd/` state if you didn't move it. The symptom is a bizarre `SQLite journal failed: unable to open database file` on the *next* run in the same checkout, because the previous run's own cleanup step deleted the very journal directory the daemon needed. Fix: put the daemon's data outside the checkout:

```bash
flows run pr-reviewer.flow.ts --local-agent --data-dir /somewhere/outside/the/repo --input '{...}'
```

**Before `flows deploy` will do anything, two things have to already be true — a correct command still fails without them:**

1. **You (or whoever's driving this) are logged in.** `agent-relay cloud login` once; check with `agent-relay cloud whoami`. There's no separate `flows`-specific login — it shares the `agent-relay` Cloud session.
2. **The workspace has a GitHub App installation covering `--repo`, and the `--on` provider is actually a connected integration** — not just declared in the command. `flows deploy` looks up the workspace's GitHub installation before it will activate a listener; with none, it refuses `flow_repository_not_connected` rather than deploying a broken one (`prepare-flow-deploy.ts` in `AgentWorkforce/cloud`). Check what's connected with `agent-relay cloud integration connections --workspace <id>` — a provider showing `degraded` instead of `ready` is not deploy-safe, even though the CLI won't tell you that until you try. This is a separate concern from your own local git push access (a personal git/`gh` credential thing, needed only for testing a flow's own `git push`/`gh pr create` steps locally) — don't conflate the two when debugging a refusal.

**`flows deploy`** creates a persistent listener: each matching ticket (`--on github:labels=agent`, `linear:team=ENG`, `jira:project=OPS`, `shortcut:workspace=…`, `slack:channel=#eng`) launches one Cloud run. `flows deployments` lists what's listening; `flows undeploy <id>` stops it — verified for real this session (deployed `software-factory` against a real repo with `--on linear:team=…`, got back `{"status":"listening", ...}`, then cleanly undeployed).

**`flows schedule`** puts a flow on a cron instead of a ticket trigger — newer (shipped after the `2.0.16` release line) and not yet reflected everywhere in older examples that instead show `flows run --cloud` for the same use case.

**Now fixed, was broken through `2.0.16`** ([flows#461](https://github.com/AgentWorkforce/flows/issues/461), closed): the one-shot `flows run --cloud [--sync-code] <flow.ts> --input <json>` form used to misroute authored TypeScript flows into the declarative-spec loader (`invalid_input: Cannot read or compile the declarative flow`) or refuse with a bare `http_error: HTTP 400`. Root cause: Cloud pinned an older `@relayflows/surface` than the CLI authored against, and refused the version mismatch with those opaque errors instead of naming it. Fixed in `2.0.17` (CLI side) — verified for real: `flows run --cloud --wait <flow.ts> --input '{}'` now submits successfully and returns a real run ID instead of refusing immediately. If you still hit a bare `HTTP 400`/`invalid_input` on this path, you're likely on a CLI older than `2.0.17` — update first before assuming something else is wrong. (Cloud-side reporting of the exact version mismatch, when one still exists, was tracked as a separate follow-up PR at the time of writing — the CLI's own refusal is fixed either way.)

### Watching a local run: observer link vs `--cloud-mirror`

New in **`2.0.32`**. A local run has two ways to be watched, and they are not the same thing:

- **The observer link is the default.** Every `flows run` mints a read-only `ot_live_` link scoped to that run's own `wf-<runId>` channel and prints `Observer: <url>`. It is free, needs only a workspace key, and carries a step projection. `--no-observer-link` suppresses it.
- **`--cloud-mirror` additionally puts the run on the Cloud dashboard** — the richer hosted view: the flow source, **every agent step's transcript**, the run graph, the run's own log, and the run sitting in the same history as your hosted ones. `FLOWS_CLOUD_MIRROR=1` turns it on for a whole shell.

```bash
flows run review.flow.ts --local-agent --input '{}'                  # observer link only
flows run --cloud-mirror review.flow.ts --local-agent --input '{}'   # ...and the dashboard
```

The run prints both, and the dashboard line names Cloud's run id as well as the page:

```
Observer:  https://agentrelay.com/observer?key=ot_live_...
Dashboard: https://.../dashboard/workflow/<cloud-run-id>/runner  ·  flows status --cloud --watch <cloud-run-id>
```

**That second id matters and is easy to get wrong.** The report's own `runId` is the *journal's* ULID (`01M3B9...`), while the two hosted verbs that take an id — `flows status --cloud <run-id>` and `flows logs <run-id>` — want Cloud's UUID. Do not pass a journal id to either. Under `--json` both ride in the report as `cloudRunId` and `dashboardUrl`, beside `observerUrl`.

`flows runs` is the odd one out and the way *out* of this problem: it takes no id at all (`flows runs [--limit <n>] [--json]`) and lists the runs the credential can see, newest first, with each one's Cloud UUID — so it is how you find the id the other two want when you no longer have the terminal that printed it.

**Why it is opt-in, not on by default.** Because it is the richer view, it is also the one that *stores* all of that: source, step metadata, agent transcripts, and the CLI's own stderr. Transcripts are whatever the agent printed, including file contents and command output. Everything goes through the same redactor `flows status` uses — but redaction is pattern matching, and pattern matching has a false-negative rate. So the trigger is an explicit request and never the mere presence of a Cloud login. Only an affirmative counts for the env var (`1`/`true`/`on`/`yes`); `0`, empty, and anything nobody meant as a switch all leave the run local.

**What it buys you, concretely:** the three read verbs start answering for *local* runs, which until `2.0.32` only worked for runs Cloud had launched.

```
$ flows status --cloud <cloud-run-id>
RUN 27ab5702-...  local-mirror-agent-confirmation  completed  spend 13,088 in / 61 out / $0.01836
  ✓ ask-claude  agent  1 attempt  3.3s  claude-haiku-4-5-20251001 · 1 turn · $0.01836
  ✓ ask-codex   agent  1 attempt  7.9s
$ flows logs <cloud-run-id> --step ask-claude    # that step's transcript, out of Cloud storage
```

Three behaviours worth knowing before you rely on it:

- **It cannot fail a run.** Every push collapses to a boolean; each poll and the whole finish are bounded. A Cloud outage costs the run its dashboard page and nothing else. If the mirror is refused you get one line naming which switch asked for it, and the run's exit code is untouched.
- **The dashboard says the run was local.** The row is `dispatchType: "local"`, and the run page shows **Ran on: Your machine** instead of a sandbox tile. Cancel is refused for it — Cloud mirrors a local run, it does not control it, so stop it where it is running.
- **A `--cloud-mirror` resume is a second dashboard row, linked to the first.** Cloud refuses to move a terminal run back to `running` (its own hosted resume mints a fresh id too), so the resumed attempt carries `resumedFromRunId` and the run page links the two — the parked "Needs review" row shows what continued it. The mapping lives in `<data-dir>/cloud-runs/`: the Cloud run id and the deployment, no credential, mode 0600, ageing out at 30 days.

**Requires a Cloud login** (`agent-relay cloud login`, or `FLOWS_CLOUD_TOKEN`) — the same credential every other hosted verb uses. Without one, `--cloud-mirror` prints one line saying the run stays local and the run proceeds normally. A local run that joins no workspace is not a defect (RFC-0001 settled decision 7: the journal is the record, the workspace is one view onto it).

### Exit codes and refusal shapes

Every refusal before a journal write is exit **2**, printed as `REFUSED [<kind>] <message>`. The `<kind>` differs by *how* the flow was checked, not just *what* was wrong:

- `flows check` on a YAML/JSON spec, or the declarative-compiler path in general → the preflight's own kind directly: `cli_unresolved`, `model_unknown`, `cli_missing`, `cli_unauthenticated`, `no_executor`, `config_invalid`, etc.
- `flows run` on a **TypeScript** `.flow.ts` whose authored `f.agent`/`f.llm` call can't resolve a CLI or model at runtime → wrapped and printed as `REFUSED [invalid_spec] <message>` with the specific reason (`llm_cli_unresolved`, etc.) inside the message text, not as the printed `[kind]` itself.

Both are real, both are exit 2 — the same underlying problem can print a different `[kind]` depending on whether you hit it via `flows check` on YAML or `flows run` on TypeScript.

## Common mistakes

- **Forgetting `version` in a YAML/JSON `FlowSpec`.** Required, not optional.
- **Attaching two `.gate()` calls to one step.** `unsupported_gate`: a step takes one. Also note a predicate gate is invisible to `flows check` — prefer a config object when preflight should be able to prove it.
- **Putting `tools`, `budget`, or any other `FlowHeader` field into `flows.json`.** `flows.json` only accepts `cli`, `executors`, `models`, `mcp`, `deploy` — anything else is `config_invalid`.
- **Assuming `flows.json`'s `models` sets a default model.** It only validates models already declared elsewhere; it never selects one.
- **Declaring `.on(...)` trigger handlers without registering the provider in `flows.json`'s `executors`.** Even a flow you only ever run directly (never via a real webhook) needs this, or it's refused `no_executor` before your input is even read.
- **Calling `f.done('canceled')` for a human's "no."** That's `f.done('declined')` — `canceled` is the kernel's verdict, not an authored body's.
- **Running an agent/llm-bearing flow without `--local-agent`.** The run parks with nothing attached to do the work.
- **Letting a git-hygiene flow's cleanup step delete your daemon's own data dir.** Pass `--data-dir` outside the checkout for any flow that runs `git clean`/`git checkout --force` on its own working tree.
- **Not awaiting a step, or manually `.then()`-chaining one.** Refused (`unawaited_step`) rather than silently ignored.
- **Running a `.flow.ts` without `--input`.** Required even for flows that don't use their input argument.
- **Assuming `flows run --cloud` for a one-shot TypeScript flow run is still broken.** It was through `2.0.16` ([flows#461](https://github.com/AgentWorkforce/flows/issues/461), now closed) — fixed in `2.0.17`. If you're on an older CLI, update rather than reach for a workaround; `flows deploy` remains the right choice for a persistent listener regardless.

## What this skill does NOT cover

- **Triggers/webhooks** (`.on(github.pull_request(...), ...)`), **memory retrieval**, and the full **helper** catalog's per-provider quirks (`f.mcp`, provider-specific settings) — each is its own surface; see the [Relayflows product docs](https://agentrelay.com/docs/relayflows) and the [flows-cookbook](https://github.com/AgentWorkforce/flows-cookbook) for real, run-verified examples of each.
- **Named-agent map equivalent in TypeScript beyond `use:`** — `use` composes complete child flows, not named agent configurations.
- **YAML-only agent step fields with no TypeScript equivalent**: `recoveryMode`, `surfaces`, `output`, the `agent:` named-agent selector, and enforced `workspace` (TypeScript's `workspace` string is accepted by the type but rejected by the local-agent worker — see **Human approval and direct child flows**). `permissions` is **not** on this list — it is a TypeScript option too (see **The real `Ctx` contract**).
- **Hosted multi-file child-flow execution** — `flows run --cloud` refuses `use` dependencies even with `--sync-code`; `--cloud-mirror` is the supported route for a local child-flow tree on the Cloud dashboard.
- The **older `@relayflows/core` `WorkflowBuilder`** engine. Do not use it for new work; this skill intentionally provides no legacy authoring route.

## Quick reference

| Verb / field | Language | Notes |
|---|---|---|
| `f.run(command, {timeout?})` / `type: deterministic` | both | shell command, implicit `exit_code` gate |
| `f.llm(...)` / `type: llm` | both | bare model call, no workspace |
| `f.agent(name, opts)` / `type: agent` | both | harnessed coding agent, returns `{summary, artifacts}` |
| `f.human(question, {to})` | TS only | parks the run on a durable `wait.human`; `flows answer <run> human-<n> yes\|no` then `flows resume` |
| `use: ['./child.flow.ts']` / `f.dispatch(name, input)` | TS only | `2.0.35`+ direct child in one durable tree; dispatch by declared name |
| `f.done(reason)` | TS / kernel | one of `success \| step_failed \| needs_human \| declined` from an authored body; `canceled \| budget_exceeded` are kernel-only |
| `.gate(config)` / `.gate(predicate, because)` | TS | one per step; both run since flows#449, but only a config object is provable by `flows check` |
| `options.transport: 'relay'` | TS/YAML `agent` step | dispatch to Agent Relay's task infra; request+receipt, not live chat |
| `Promise.all([...steps])` | TS | first-class supported concurrent fan-out |
| `flows.json`: `cli, executors, models, mcp, deploy` | project config | exact accepted key set — nothing else |
| `flows check <file>` | CLI | pure validate + preflight, no daemon |
| `flows run <file> --local-agent [--input ...]` | CLI | actually executes; `.flow.ts` needs `--input`, agent/llm steps need `--local-agent` |
| `flows deploy <flow.ts> --repo ... --on ...` | CLI | persistent trigger-based listener; needs `agent-relay cloud login` plus a connected GitHub App + `--on` provider first, or `flow_repository_not_connected` |
| `flows run --cloud <flow.ts> --input ...` | CLI | fixed in `2.0.17` ([flows#461](https://github.com/AgentWorkforce/flows/issues/461)); update if you still see `http_error`/`invalid_input` |
| `flows run --cloud-mirror <file> --local-agent` | CLI | `2.0.32`+; local run also on the Cloud dashboard, transcripts included. Opt-in; `FLOWS_CLOUD_MIRROR=1` for a shell. `--json` gains `cloudRunId`/`dashboardUrl` |
| `flows run --cloud` with `use` | CLI | unsupported: one self-contained `.flow.ts` source only, even with `--sync-code` |
| `flows status --cloud <run-id>` / `flows logs <run-id>` | CLI | take Cloud's **UUID**, not the journal ULID. Answer for mirrored local runs since `2.0.32` |
| `flows runs [--limit <n>]` | CLI | takes **no id** — lists runs newest-first, which is how you find the UUID the two above want |
| `flows schedule <flow.ts> --cron ...` | CLI | cron-based cloud run |

## Verified against

**The `Ctx` and child-flow contracts were checked against the published `@relayflows/surface@2.0.35` / `@relayflows/sdk@2.0.35` declarations.** Earlier gate, helper, and agent-option findings below were established on `2.0.22`; the original `--cloud-mirror` verification was on `2.0.32`.

A three-level root → child → grandchild fixture was run locally from published `2.0.35` packages, then mirrored to the production Cloud dashboard. The [mirrored run](https://agentrelay.com/cloud/dashboard/workflow/0d502725-e4c2-4cfd-aed2-ed0dd49bd6ac/runner) completed with `completionReason: success`; its Cloud graph contained seven succeeded work/dispatch nodes, seven runtime dependency edges, both child labels, and no warnings. A separate `flows run --cloud --sync-code` attempt refused the same tree before admission with `unsupported_source`, which is why this skill does not promise hosted child-flow execution. This checks the graph API used by the dashboard, not an authenticated browser screenshot.

**The `--cloud-mirror` section was verified on `2.0.32`, against production, with the published artifact.** `relayflows@2.0.32` was installed from npm into a scratch project — not run from a source tree — and two real local runs were mirrored to `agentrelay.com`:

- a two-step deterministic flow, read back with `flows status --cloud`, `flows logs` (the `runner.log` round-trip) and `flows runs` (the run appearing in history beside hosted ones);
- a two-agent flow, one `cli: claude` step and one `cli: codex` step, spending a real `$0.01836` — whose **per-step transcripts were fetched back out of Cloud storage** and rendered in each provider's own frame vocabulary. That is the claim worth having evidence for: an echo-only flow exercises none of the transcript path.

Two things that verification established and that are easy to assume otherwise. **Flows drives exactly two agent CLIs**: `adapters/index.ts` registers `claude` and `codex`, and anything else resolves to `relayflows-wrapper-v1`, which requires the executable to answer `--relayflows-adapter-v1` with a flows-specific token. A real `devin` CLI on `PATH` rejects that flag outright (`error: unexpected argument`), so it cannot be used as a `cli:` for an agent step no matter what is installed — adding one is a new `adapters/<name>.ts` plus a registry entry. And the **observer projection has no retry**: `run-projection.ts` sets `failed = true` on the first error and every later publish is a no-op, so a transient `429 workspace_busy` — observed for real during this verification, while another run was launching in the same workspace — permanently loses the observer view for that run. The dashboard mirror survived the same window because it classifies `429` as transient and retries on its next poll. If an observer link opens an empty channel, that asymmetry is the first thing to check.

The earlier `2.0.22` refresh settled several contradictions against the published package: `AgentOptions.permissions` exists on the TypeScript call site (added in `2.0.17`, validated and journaled, not enforced — preflight warns `permissions_unenforced`); `run(command, options?)` takes a second `{timeout}` argument; `f.done` takes six `FLOW_COMPLETION_REASONS`; there is no `budget.maxWallclockMs`; predicate `.gate()` and `artifact_exists` ship; and `f.human` executes. Its then-true finding that `f.dispatch` was unsupported was superseded by `2.0.35`. Older real-run recipes are in [`AgentWorkforce/flows-cookbook`](https://github.com/AgentWorkforce/flows-cookbook); check their dates when comparing behavior.

The `flows.json` schema refusal, the `--data-dir` git-hygiene interaction, and the `flows run --cloud` bug were reproduced while building that cookbook past `v2.0.16` (2026-09-17). The `2.0.22` refresh also checked the `workspace: readonly` annotation and the `subprocess_gate` env var name against the real CLI. Child-flow claims above instead rest on the published `2.0.35` run and its production Cloud graph.
