---
name: premortem-bind
description: Run a 5-phase agentized pre-mortem (Klein 1989) on a plan or design. Each surfaced failure mode is bound to a NAMED OWNER and a REGRESSION TEST hook before the plan exits — prevents "decorative" pre-mortems where risks are named but never tracked. Use before exiting plan mode on high-risk changes (auth, payments, migrations, multi-step rollouts) or after a prior incident in the area.
---

# Premortem-bind

A pre-mortem only matters if the surfaced failures *bind* to commitments. Naming "we could lose data" and moving on is decoration. This skill enforces binding: no risk leaves the room without an owner, a regression hook, and a renegotiation clause.

## The 5 phases

### 1. Framing

State the assumption being stress-tested in **one sentence**. Format:

> *"This plan will succeed at <outcome> under <conditions>."*

If you cannot phrase it in one sentence, the plan is not focused enough; go back to planning.

### 2. Free generation

Generate **≥8 failure modes**. No filtering, no probability-weighing yet. Group as you go:

- Data / edge cases / encoding / time zones
- Security / auth / multi-tenant / privilege escalation
- Perf / scale / cold-start / N+1 / fan-out
- Ops / observability / rollback / on-call burden
- UX / accessibility / i18n / offline
- Concurrency / consistency / partial failure / retry storms
- Dependencies / supply chain / version skew

If you cannot list eight, you have not stressed enough. Spawn the `grill-me` skill or a fresh-context adversarial sub-agent to push further.

### 3. Behavioral attractor test

For each failure mode, ask:

> *"If I remove this top-1 failure and re-derive, does the same shape come back?"*

- **Yes** → it is a **structural attractor** (architectural, will recur). Treat as a design constraint, not a discrete bug. May require re-planning, not just adding a test.
- **No** → it is a **discrete risk** to mitigate with a specific guard.

### 4. Probability × impact ranking

Sort all failures by P × I (each 1-5). Keep the top 5. Drop or defer the rest with a one-line reason each.

### 5. Commitment binding (mandatory — no skipping)

For each top-5 failure, produce **three** fields. If you cannot fill all three, the failure was decoration, not a risk — drop it or re-stress.

- **Named owner** — a concrete test file path, a sub-agent name, or a monitoring rule. Not "the team", not "ops". Examples:
  - `tests/auth/session-fixation.test.ts`
  - `code-reviewer subagent on every auth-touching PR`
  - `Datadog monitor: payment_intent.failed rate > 1% over 5m`
- **Regression test hook** — the concrete artifact (test file + assertion description) that fails when this failure mode occurs. If the test does not exist, write it now or schedule it as **phase 1** of the plan.
- **Renegotiation clause** — what triggers revisiting this commitment?
  - "If P99 latency > 300ms for > 5m on the checkout path"
  - "If we add multi-region — the assumption changes"
  - "Never — this is a permanent constraint"

## Output format (exact structure)

```
## Pre-mortem on: <one-sentence framing>

### Top failure modes (ranked)
1. <description>  P:<1-5>  I:<1-5>  type: <discrete | attractor>
2. ...
5. ...

### Bindings
| # | Failure                | Owner                       | Regression test               | Renegotiation                       |
|---|------------------------|-----------------------------|-------------------------------|-------------------------------------|
| 1 | Session fixation       | tests/auth/session.test.ts  | "old session ID invalidated"  | Permanent                           |
| 2 | ...                    | ...                         | ...                           | ...                                 |

### Re-plan signals (attractors)
- <attractor 1>: <what this implies for the plan — re-shape needed?>

### Deferred (with reason)
- <failure>: <why it's safe to defer>
```

## Anti-patterns

- ❌ Generating <8 failure modes → you didn't stress enough.
- ❌ "The team will watch for this" — not an owner.
- ❌ A binding without a concrete test file path → the test doesn't exist, you haven't bound.
- ❌ Skipping the attractor test → you might patch the symptom of an architectural problem.
- ❌ Running a pre-mortem *after* coding → that's a retrospective, different purpose, different ritual.
- ❌ A pre-mortem with no top-1 failure (all "low P, low I") → either the plan is trivial (skip the skill) or you're not actually stressing.

## Integration with other skills

- After `slice-check` accepts the plan → run `premortem-bind` on the highest-risk slice.
- If the pre-mortem surfaces an attractor → re-plan; do not patch.
- The bindings produced here feed directly into `to-issues` as test-writing tasks.

$ARGUMENTS
