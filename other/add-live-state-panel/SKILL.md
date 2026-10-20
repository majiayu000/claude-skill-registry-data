---
name: add-live-state-panel
description: >-
  Load this skill when adding a live panel to an AG-UI canvas: one fixed area the agent keeps
  updating while it works, wired from STATE_SNAPSHOT and STATE_DELTA. Trigger on "show the agent's
  progress live", "shared state", "sync state with the agent".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs the canvas's toolchain (Bun or Node.js 20+, @ag-ui/client 1.x, zod 4) and, for the mock
  agent, uv with Python 3.11+ and ag-ui-protocol 1.x.
license: Apache-2.0
---

# Add a live state panel to the canvas

Catalogue components are **snapshots**: once placed, a component never changes. Shared state is for
the opposite case, a **value that changes while the user watches**. A progress tracker ticks, a
plan gets rewritten, a counter climbs. The agent owns the value and streams its changes, and one
fixed panel on the canvas renders it. The work is done when the three checks in step 5 pass.

## Procedure

### 1. Decide before wiring

- **Does the value change after it is shown?** If not, it is a catalogue component, not state.
- **Who writes each top-level key?** Give every key exactly one writer: the agent (`progress`,
  `plan`) or the UI (`filters`, `selection`). Two writers on the same key race, because each run
  sends the UI's copy and the agent answers with its own.
- **Keep the state small and serialisable.** It travels in full on every run (`RunAgentInput.state`),
  and the agent may snapshot it at any time.

### 2. Agent side: snapshot, then deltas

- **`STATE_SNAPSHOT { snapshot }`** replaces the whole state. Send one when a value first appears,
  and whenever you are unsure what the client holds (a new run, a reconnect).
- **`STATE_DELTA { delta }`** is an RFC 6902 JSON Patch applied to the client's current state. Paths
  must exist, except for `add`. A patch against a path the client never received fails on the
  client, so when in doubt, snapshot.

Mock-agent handler (`agent/main.py`; import `StateSnapshotEvent` and `StateDeltaEvent` from
`ag_ui.core`, and call it from `respond` when the text mentions "progress"):

```python
def progress() -> list[BaseEvent]:
    steps = ["Collect data", "Analyse", "Write summary"]
    snapshot = {"progress": {"title": "Preparing report", "steps": steps, "done": 0}}
    deltas = [
        [{"op": "replace", "path": "/progress/done", "value": i}]
        for i in range(1, len(steps) + 1)
    ]
    return [
        StateSnapshotEvent(snapshot=snapshot),
        *(StateDeltaEvent(delta=d) for d in deltas),
        *say("Report ready."),
    ]
```

With a real model (the `ceh-ag-ui:build-ag-ui-agent` server), give the model a **backend tool**
such as `update_progress` whose handler validates the input and updates the thread's state. The
loop then yields a `STATE_DELTA` for the change before continuing, and the model never writes the
patch itself. To make the loop yield state events from a handler, have handlers return the events
to emit alongside the tool result. Keep the thread's state next to its transcript and send a
`STATE_SNAPSHOT` at the start of each run.

### 3. Canvas side

In `useAgent.ts`, mirror the client's state. The client applies snapshots and patches itself:

```ts
const [state, setState] = useState<Record<string, unknown>>({});
// inside the existing agent.subscribe({...}):
onStateChanged: ({ state }) => setState({ ...state }),
// and return `state` from the hook
```

Render each agent-owned key with **one fixed panel**, validated like tool arguments. State is agent
output, so the styling lock applies in the same way:

```tsx
// src/state/progress.tsx
const progressSchema = z.object({
  title: z.string(),
  steps: z.array(z.string()).min(1),
  done: z.number().int().nonnegative(),
});

export function ProgressPanel({ value }: { value: unknown }) {
  const parsed = progressSchema.safeParse(value);
  if (!parsed.success) return null;
  const { title, steps, done } = parsed.data;
  return (
    <section className="card" aria-label={title}>
      <p className="eyebrow">In progress</p>
      <h2>{title}</h2>
      <div
        className="bar-track"
        role="progressbar"
        aria-label={title}
        aria-valuemin={0}
        aria-valuemax={steps.length}
        aria-valuenow={done}
      >
        <div
          className="bar-fill is-1"
          style={{
            width: `${(Math.min(done, steps.length) / steps.length) * 100}%`,
          }}
        />
      </div>
      <ol>
        {steps.map((step, i) => (
          <li key={step} className={i < done ? "muted" : undefined}>
            {step}
            {i < done && <span className="visually-hidden"> (done)</span>}
          </li>
        ))}
      </ol>
    </section>
  );
}
```

In `App.tsx`, pin the panel above the placed components, and keep the empty state only while there
is neither:

```tsx
{state.progress !== undefined && <ProgressPanel value={state.progress} />}
{blocks.length === 0 && state.progress === undefined ? (/* empty state */) : (/* blocks */)}
```

### 4. UI-owned keys (UI to agent)

For keys the UI writes, call `agent.setState({ ...agent.state, filters })` before the next
`runAgent`. The state goes out in `RunAgentInput.state`. On the server, read it from `run.state`
and pass the relevant part to the model as text in the new user turn. Do not put it in the system
prompt: rewriting the prompt on every run breaks the prompt cache and the append-only transcript.

### 5. Verify against the mock

1. "show progress" draws the panel. `aria-valuenow` ends at the step count, and the chat says
   "Report ready."
2. A malformed snapshot, such as `done` as a string, renders no panel and does not crash.
3. The panel still looks right with the other theme's `brand.css`.

## Rules

- **Treat state as data only.** No key carries a class name, colour or size. The panel decides how
  things look from the theme, and derives any geometry, such as the bar width, from validated
  numbers.
- **Never copy state into a second store.** Render from the hook's `state`. A copy goes stale on
  the next delta.
- **Announce progress without flooding screen readers.** `role="progressbar"` with `aria-valuenow`
  reports the value when asked. Keep a fast-changing panel outside any `aria-live` region.

## Hands off to

- A value that never changes once shown is a catalogue component: `ceh-ag-ui:add-canvas-component`.
- The agent must wait for the user's decision: `ceh-ag-ui:add-human-approval`.
- No canvas exists yet: `ceh-ag-ui:build-ag-ui`.
