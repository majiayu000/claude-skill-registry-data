---
name: add-human-approval
description: >-
  Load this skill when an AG-UI agent must stop for the user's decision before an irreversible or
  costly step (a delete, a payment, a send), using AG-UI 1.0 interrupts and resume. Trigger on "ask
  the user before", "human in the loop", "approval step".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs the canvas's toolchain (Bun or Node.js 20+, @ag-ui/client 1.x) and, for the mock agent,
  uv with Python 3.11+ and ag-ui-protocol 1.x, which carries the interrupt outcome and resume.
license: Apache-2.0
---

# Add a human approval step

An approval is a **pause the protocol knows about**, not a chat message asking "are you sure?". The
agent ends the run with an interrupt. The canvas shows a card whose look it controls. The user's
decision comes back as a `resume` entry on the next run, and the agent acts only on that.
The work is done when the five checks in step 3 pass.

## Procedure

### 1. Agent side

Keep a server-side record of what each pending interrupt guards. **Act only on a resume entry whose
id is in that record**, then remove it, so each approval can be used once. Never act on an id the
server did not issue, and never on an expired one.

Mock-agent handlers (`agent/main.py`; import `Interrupt` and `RunFinishedInterruptOutcome` from
`ag_ui.core`). `respond` checks `run.resume` first, and triggers `ask_approval` when the text
mentions "delete":

```python
PENDING: dict[str, str] = {}  # interrupt id -> the action it guards


def ask_approval(run: RunAgentInput, action: str) -> list[BaseEvent]:
    interrupt = Interrupt(
        id=str(uuid.uuid4()),
        reason="confirmation",
        message=f"Allow the agent to {action}?",
        response_schema={
            "type": "object",
            "properties": {"approved": {"type": "boolean"}},
            "required": ["approved"],
        },
    )
    PENDING[interrupt.id] = action
    outcome = RunFinishedInterruptOutcome(interrupts=[interrupt])
    return [
        RunFinishedEvent(thread_id=run.thread_id, run_id=run.run_id, outcome=outcome)
    ]


def resumed(run: RunAgentInput) -> list[BaseEvent]:
    events: list[BaseEvent] = []
    for entry in run.resume or []:
        action = PENDING.pop(entry.interrupt_id, None)
        if action is None:
            events += say("That request is no longer waiting for approval.")
        elif (
            entry.status == "resolved" and (entry.payload or {}).get("approved") is True
        ):
            events += say(f"Done: {action}.")
        else:
            events += say(f"Not done: {action}.")
    return events
```

The template mock sends `RUN_FINISHED` itself unless a handler's last event is already one. That
lets `ask_approval` end the run with the interrupt outcome.

With a real model (the `ceh-ag-ui:build-ag-ui-agent` server), mark the sensitive **backend tools**
as needing approval. When the model calls one, do not execute it. Store the call under a new
interrupt id and end the run with the interrupt outcome, leaving the `tool_use` unanswered. On
resume, execute it (approved) or return an `is_error` tool result saying the user declined
(rejected or cancelled). That result goes in the same user turn as any other results for that
model turn, and the loop then continues as usual.

### 2. Canvas side

In `useAgent.ts`, add the interrupt handling to the existing `drive` loop and `send`:

```ts
import { isInterruptExpired, type Interrupt } from "@ag-ui/client";

const [interrupts, setInterrupts] = useState<Interrupt[]>([]);
const [decisions, setDecisions] = useState<Record<string, boolean>>({});

// in drive(), right after `params = {};`:
if (agent.pendingInterrupts.length > 0) break; // waiting on the user: don't re-run
// in drive()'s finally:
setInterrupts([...agent.pendingInterrupts]);

// Every open interrupt must be answered in one resume, so decisions are collected first.
async function decide(id: string, approved: boolean) {
  const next = { ...decisions, [id]: approved };
  if (agent.pendingInterrupts.some((i) => !(i.id in next)))
    return setDecisions(next);
  setDecisions({});
  await drive({
    resume: agent.pendingInterrupts.map((i) =>
      isInterruptExpired(i)
        ? { interruptId: i.id, status: "cancelled" as const }
        : {
            interruptId: i.id,
            status: "resolved" as const,
            payload: { approved: next[i.id] },
          },
    ),
  });
}

// at the top of send(): typing instead of answering cancels what was pending,
// then the new message goes out as its own run.
if (agent.pendingInterrupts.length > 0) {
  setDecisions({});
  await drive({
    resume: agent.pendingInterrupts.map((i) => ({
      interruptId: i.id,
      status: "cancelled" as const,
    })),
  });
}
// return interrupts, decisions and decide from the hook
```

The approval card is a **fixed component**, not a catalogue entry. The agent supplies only the
question, and the card renders it as text:

```tsx
// src/ApprovalCard.tsx
export function ApprovalCard({
  interrupt,
  decided,
  onDecide,
}: {
  interrupt: Interrupt;
  decided?: boolean;
  onDecide: (approved: boolean) => void;
}) {
  const labelId = `approval-${interrupt.id}`;
  return (
    <section
      className="card has-edge is-active"
      role="group"
      aria-labelledby={labelId}
    >
      <p className="eyebrow">Approval needed</p>
      <p id={labelId}>{interrupt.message ?? interrupt.reason}</p>
      {decided === undefined ? (
        <div className="approval-actions">
          <button
            type="button"
            className="btn btn-primary btn-sm"
            onClick={() => onDecide(true)}
          >
            Approve
          </button>
          <button
            type="button"
            className="btn btn-outline btn-sm"
            onClick={() => onDecide(false)}
          >
            Reject
          </button>
        </div>
      ) : (
        <p className="muted">
          {decided ? "Approved" : "Rejected"}, waiting for the others.
        </p>
      )}
    </section>
  );
}
```

Render the cards in the chat panel between the messages and the input, where the user is already
looking:
`{interrupts.map((i) => <ApprovalCard key={i.id} interrupt={i} decided={decisions[i.id]} onDecide={(ok) => void decide(i.id, ok)} />)}`.
In `app.css`, add `.approval-actions { display: flex; gap: var(--space-2); }` and
`.chat .card { margin: 0 var(--space-4) var(--space-2); }`.

### 3. Verify against the mock

1. "delete old records" shows one card with Approve and Reject, and nothing else runs.
2. Approve: the chat says "Done: …" and the card disappears.
3. Reject: "Not done: …".
4. Ask again, then type a message instead of answering. The chat says "Not done: …" (cancelled),
   the new message gets its normal reply, and no client error appears.
5. Server check: resending an already used interrupt id is refused ("no longer waiting").

## Rules

### The contract (AG-UI 1.0)

```
run 1  →  … RUN_FINISHED { outcome: { type: "interrupt", interrupts: [ { id, reason, message, responseSchema?, expiresAt? } ] } }
          client: agent.pendingInterrupts = [...]   (the canvas shows one card per interrupt)
run 2  ←  RunAgentInput.resume = [ { interruptId, status: "resolved", payload: { approved } } | { interruptId, status: "cancelled" } ]
```

- **Every open interrupt must be answered in the next run's `resume`.** `@ag-ui/client` throws
  "Thread has N pending interrupt(s) not addressed by resume" otherwise. Collect a decision for
  every card, then resume once.
- **Use `resolved` + `{ approved: false }` for an explicit Reject, and `cancelled` when the user
  never answered**: they typed something else, or the interrupt expired. Send `cancelled`, never
  `resolved`, for an interrupt past its `expiresAt` (check with `isInterruptExpired`).
- **One interrupt = one decision.** Do not bundle "delete 3 records and email the owner" into one
  approval if the user could want only one of them.

### The approval card

- **Keep the look fixed.** `.has-edge.is-active` is the theme's "this needs you" signal. Its colour
  comes from the theme, never from the interrupt. If the agent needs a severity, make it a semantic
  field that the card maps to a class, as `tone` does in the catalogue.
- **The buttons say what they do.** Approve is the single primary button. Put the consequence in
  `message` ("delete 3 archived records"), because a vague "Proceed?" gets approved without being
  read.
- **Use `role="group"` with `aria-labelledby`**, so a screen reader announces the question with the
  buttons. Use `role="alert"` only when the run truly cannot continue without it.

## Hands off to

- Live progress instead of a decision: `ceh-ag-ui:add-live-state-panel`.
- Placing a component: `ceh-ag-ui:add-canvas-component`.
- No canvas exists yet: `ceh-ag-ui:build-ag-ui`.
