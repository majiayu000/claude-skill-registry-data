---
name: sol-luna-max-orchestrator
description: Keep GPT-5.6 Sol as the single user-facing commander while a local blocking controller runs fresh GPT-5.6 Luna Max implementation, independent review, correction, and re-review cycles. Never wake Sol for heartbeat or worker-to-worker routing; return to Sol only after independent PASS, a verified user-only blocker, bounded cycle exhaustion, or a transport failure.
---

# Sol + Luna Max Codex Orchestrator

Use this skill when one Codex conversation should remain the user-facing commander while GPT-5.6 Luna at `max` performs the expensive repository work.

## Fixed architecture

```text
USER
  ↓
GPT-5.6 SOL
commander: goal + constraints + acceptance criteria
  ↓ one blocking controller call
LOCAL NON-LLM CONTROLLER
  ↓
fresh GPT-5.6 LUNA MAX executor
  ↓ process waits locally
fresh DIFFERENT GPT-5.6 LUNA MAX reviewer
  ↓ process waits locally
  ├─ PASS → return compact proof to Sol
  ├─ FAIL/UNKNOWN → fresh Luna fixer → fresh Luna reviewer → repeat
  └─ BLOCKED → return verified blocker to Sol
  ↓
GPT-5.6 SOL
cheap final sanity gate / user-facing result
```

The user interacts only with Sol. Worker lifecycle is internal.

## Hard invariants

### 1. User never orchestrates workers

Never require the user to say or do:

```text
check Luna
resume Luna
open another Luna
copy this to Sol
review what Luna did
start a reviewer
start the fixer
start the next worker
```

One user request must be enough until final proof or a genuine user-only decision is required.

### 2. Sol never wakes between Luna stages

There is **no root-model routing wake fallback**.

After Sol creates the initial bounded packet, use `scripts/run_luna_cycle.py` or an equivalent truly blocking local controller. The controller owns all mechanical transitions:

```text
executor → reviewer → fixer → reviewer → ...
```

Sol must not resume merely because:

- an executor reached terminal state;
- a reviewer needs to start;
- a correction worker needs to start;
- a worker is still running;
- a watcher observed a progress event.

The controller returns to Sol only when one terminal orchestration state exists:

```text
PASS
BLOCKED
EXHAUSTED
TRANSPORT_ERROR
```

`EXHAUSTED` is a bounded-cost stop after the configured correction-cycle limit; it is not success.

### 3. No heartbeat polling by any LLM

Never use recurring `wait_thread`, `wait_agent`, status prompts, or model turns merely to ask whether Luna is done.

Waiting must be ordinary process work:

1. a blocking `codex exec` process;
2. or an exact-session local watcher when another Luna-capable transport is used.

A local process may wait or poll deterministic process/session state. It must not invoke Sol or another model for status checks.

### 4. Executor and reviewer are different fresh Luna contexts

Sol and every Luna worker are distinct execution contexts.

For every material implementation/correction phase:

- implementation worker = fresh GPT-5.6 Luna at `max`;
- mandatory reviewer = another fresh GPT-5.6 Luna at `max`;
- correction worker after failed review = another fresh GPT-5.6 Luna at `max`;
- re-review = another fresh GPT-5.6 Luna at `max`.

Never let the executor certify its own work.
Never let the fixer certify its own correction.

### 5. Luna is the required worker model

The required model is `gpt-5.6-luna` with reasoning effort `max`.

Do not silently substitute Sol, Terra, or another model.
Do not retry a transport that explicitly rejects Luna.

The bundled zero-wake controller uses fresh non-interactive `codex exec` runs and explicitly sets:

```text
model = gpt-5.6-luna
model_reasoning_effort = max
agents.enabled = false
```

Disabling descendant agents keeps worker fan-out and cost under the controller's ownership.

If `codex exec` is unavailable in the active host, another Luna-capable **blocking** transport may be used only if it can preserve this exact zero-wake lifecycle. A transport that requires Sol to resume between executor and reviewer does not satisfy this skill.

### 6. Exact workspace affinity

Every Luna executor, reviewer, and fixer must operate on the exact authorized repository/workspace/folder and relevant project instructions.

Fresh context means a fresh model execution context, not a different repository.

Do not rediscover or invent project identity when the authoritative workspace is already known.

### 7. Executor completion is only a claim

Any of the following from the implementation worker is **not final proof**:

```text
task_complete
exit code 0
"tests passed"
"done"
"fixed"
"deployed"
```

Sol must never announce success from the executor report alone.

### 8. Mandatory independent review gate

A different fresh Luna reviewer must independently inspect the resulting workspace/state and verify every material acceptance criterion.

The reviewer must not trust the executor summary as proof.

Reviewer verdict is exactly one of:

```text
PASS
FAIL
BLOCKED
UNKNOWN
```

A `PASS` is valid only when:

- every acceptance criterion is present exactly;
- every criterion status is `PASS`;
- every criterion has concrete evidence;
- no unresolved high/critical finding exists.

The local controller must downgrade an internally inconsistent `PASS` to `UNKNOWN` instead of forwarding false success.

### 9. Sol cannot celebrate early

Sol may tell the user the work is complete/fixed/deployed/correct/verified only after the controller returns `PASS` from an independent reviewer.

For `BLOCKED`, `EXHAUSTED`, or `TRANSPORT_ERROR`, report the exact state and evidence. Never convert them into success.

## Required zero-wake controller

Default implementation:

```text
scripts/run_luna_cycle.py
```

Sol should create one compact JSON packet and invoke the controller once.

Packet shape:

```json
{
  "goal": "one concrete end-state",
  "acceptance_criteria": [
    "criterion 1",
    "criterion 2"
  ],
  "constraints": [
    "non-negotiable constraint"
  ],
  "context": "only essential context; optional"
}
```

Typical invocation:

```powershell
python scripts/run_luna_cycle.py `
  --packet <packet.json> `
  --workspace <authorized-repository-root>
```

Do not use the controller against an unrelated checkout merely because the orchestrator repository contains the script. `--workspace` is the user's actual authorized target repository.

The controller:

1. launches a fresh Luna Max implementation worker with workspace write permission;
2. blocks locally until that worker exits;
3. launches a fresh independent Luna Max reviewer;
4. blocks locally until review exits;
5. if `FAIL` or `UNKNOWN`, launches a fresh correction worker automatically;
6. launches another fresh reviewer automatically;
7. repeats within a bounded cycle limit;
8. prints one compact terminal JSON result and exits.

No Sol turn occurs at steps 2–7.

## Independent reviewer contract

The reviewer receives:

```text
OVERALL GOAL
PHASE ACCEPTANCE CRITERIA
WORKSPACE IDENTITY
NON-NEGOTIABLE CONSTRAINTS
EXECUTOR-DECLARED SCOPE (context only, never proof)
```

It must:

- inspect the workspace/state independently;
- copy each acceptance criterion exactly;
- provide evidence for each criterion;
- run safe deterministic verification when available;
- remain non-editing during review;
- return `UNKNOWN` when proof is insufficient;
- return `BLOCKED` only for a real prerequisite that prevents verification;
- return `FAIL` for incorrect/incomplete implementation.

Default reviewer sandbox is `read-only`. If a specific project requires test tooling that writes build/cache artifacts, a broader reviewer sandbox may be selected only when the existing authorization permits it; reviewer instructions still prohibit implementation edits.

## Automatic correction loop

For `FAIL` or technically resolvable `UNKNOWN`, the local controller automatically sends the failed criteria/findings to a fresh Luna correction worker.

Then it launches another fresh independent reviewer.

```text
FAIL/UNKNOWN
→ fresh fixer
→ fresh reviewer
→ PASS / FAIL / UNKNOWN / BLOCKED
```

The user is never asked to manage that loop.
Sol is never awakened to route that loop.

A bounded default cycle limit prevents an infinite token-spend loop. Reaching the limit returns `EXHAUSTED` with the last reviewer evidence so Sol can report the unresolved issue instead of silently spending forever.

## Compact handoffs

Do not replay whole transcripts into fresh workers.

Executor/fixer packets contain only:

```text
GOAL
ACCEPTANCE CRITERIA
NON-NEGOTIABLE CONSTRAINTS
ESSENTIAL CONTEXT
FAILED REVIEW EVIDENCE (correction cycles only)
```

Reviewer packets contain only:

```text
GOAL
ACCEPTANCE CRITERIA
NON-NEGOTIABLE CONSTRAINTS
EXECUTOR-DECLARED CHANGED SCOPE (context only)
```

Each Luna worker gathers repository context directly from the authorized workspace.

## Sol final sanity gate

After the controller returns `PASS`, Sol performs only a cheap commander-level sanity gate on the compact terminal result:

1. terminal state is `PASS`;
2. review evidence covers every material acceptance criterion;
3. no unresolved blocker/high-severity finding is present;
4. controller did not report transport/cycle exhaustion.

Sol should not reread the whole diff or duplicate the deep Luna review merely to spend premium tokens again.

If the compact result is malformed or logically inconsistent, do not claim success. Treat it as orchestration failure.

## Transport errors

If Luna cannot launch, the controller returns `TRANSPORT_ERROR` with the exact transport failure.

Do not:

- retry the same rejected Luna route repeatedly;
- fall back to Terra/Sol;
- ask the user to manually open a Luna chat;
- announce partial execution as success.

## Side effects and permissions

Preserve existing production, security, approval, tenant, trust, provider, and financial boundaries.

Ask the user only when the next action requires genuinely new authority, for example:

- a new credential;
- financial spend;
- irreversible/destructive production action;
- a business/product decision not implied by the original request.

Do not use the orchestration loop to bypass an approval boundary.

## External canaries

When a task contains live external canaries, read `references/trace-first-canary.md` and preserve the trace-first pattern:

```text
ONE live canary
→ correlate and characterize
→ defect ledger
→ bounded repair
→ deterministic component proof
→ ONE new end-to-end proof canary when authorized
```

Do not create uncontrolled external retries merely because the Luna correction loop is automatic.

## Cost-efficiency policy

The cost controls are architectural:

- one Sol dispatch instead of Sol heartbeat turns;
- zero Sol worker-routing wakes;
- Luna Max for implementation and deep review;
- fresh contexts instead of transcript bloat;
- compact structured handoffs;
- descendant Luna subagents disabled by the bundled controller;
- bounded correction cycles;
- one cheap Sol sanity gate only after independent proof.

## User experience

The intended experience is exactly:

```text
user tells Sol what to do once
→ Sol dispatches once
→ Luna works
→ different Luna reviews
→ if needed Luna fixes + different Luna reviews again
→ Sol returns only after terminal proof/blocker
```

The user never manages the worker sessions.

## Project identity

Independent community repository:

https://github.com/twillio-ai/sol-luna-max-codex-orchestrator

This is not an official OpenAI skill. OpenAI Codex and model capabilities may change, so transport compatibility must fail closed rather than silently changing the required worker model.
