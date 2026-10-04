---
name: completion-gate
description: Strictly audits a defined ChefFlow scope for completion, cohesion, wiring, and proof without expanding it. Use when the user says they do not want expansion, wants completion, asks what is mandatory or absolutely crucial, asks whether a scope is fully wired or done, or needs a pass/fail gate before closeout.
---

# Completion Gate

## Mission

Evaluate a defined scope for completion only.

The job is to answer:

- Can this scope honestly be called done?
- Is it cohesive across the surfaces it already claims to touch?
- Is it wired end to end?
- Is anything mandatory, absolutely crucial, or blocking missing?
- What proof is missing?
- What must be rejected as expansion?

Do not deepen, expand, optimize, brainstorm, roadmap, or add adjacent product ideas. Close the contract of the existing scope.

## Mandatory Standard

Treat an item as mandatory only when the promised scope cannot honestly be called complete without it.

Mandatory gaps include:

- A claimed route, view, widget, action, command, rail item, lifecycle item, Remy action, CIL signal, API route, server action, database write/read, permission gate, or navigation path is missing or disconnected.
- Data appears in one required surface but cannot be acted on, traced, verified, refreshed, or recovered where the scope implies it should.
- A user can start the scoped workflow but cannot complete, cancel, recover, or confirm it.
- The feature is visually present but not operational.
- Auth, tenant scoping, route policy, role gates, or privacy boundaries are incomplete for scoped data.
- The success, empty, failed, loading, stale, partial, or permission-blocked state prevents truthful completion.
- Required proof does not exist in the running app, tests, logs, screenshots, finish-checks, or wiring audit outputs.

Not mandatory:

- Nice-to-have polish.
- New feature ideas.
- Extra dashboards, widgets, or AI helpers.
- Broader product strategy.
- Adjacent workflow improvements.
- Refactors that are not required to close the scoped contract.

If an idea would make the feature better but is not required for the existing scope, put it under `Rejected Expansion` and do not recommend it for the completion batch.

## Routing Gate

Classify the request before acting:

- **Completion audit**: User asks what is mandatory, missing, incomplete, unwired, or not cohesive. Produce a strict audit.
- **Closeout gate**: User asks whether work can be marked done. Require evidence and identify blockers.
- **Queue shaping**: User asks to queue or preserve the result. Produce queue-ready mandatory work only.
- **Direct implementation**: User explicitly says "fire the queue", "build the queue", "execute this queue item now", "direct hotfix now", "do not queue this", or clearly bypasses the queue. Inspect `git status --short`, keep edits narrow, and implement only the mandatory completion batch.
- **Scope unclear**: Ask the smallest question needed to identify the promised scope. Do not audit the whole app by default.

Respect ChefFlow Build Queue First unless the user explicitly authorizes implementation.

## Completion Frame

Inspect only what is needed to understand the scope:

- The user-stated scope, queue item, spec, recent build, route, feature, or workflow.
- Directly relevant routes, components, server actions, API routes, database logic, tests, docs, proof packs, screenshots, and wiring-audit output.
- Auth, route policy, tenant scoping, and role gates when scoped data or protected routes are involved.

Stop exploring once you can state:

- What the scope promises.
- Which users, roles, entities, and states are in scope.
- Which surfaces must be connected for the promise to be true.
- What end-to-end action or state transition proves completion.
- What evidence exists and what evidence is missing.

## Wiring Checklist

Use this as a filter, not a demand to audit every app surface.

For the scoped feature, check whether the promised workflow is connected through the relevant surfaces:

- Route/page/rendering.
- Navigation, breadcrumbs, command palette, or entry points.
- Primary and secondary actions.
- Server actions, API routes, background jobs, or automation.
- Database reads/writes, validation, tenant scope, and audit/history.
- Dashboard, rail, priority queue, commitment UI, lifecycle, ledger, communications, client intelligence, menu intelligence, PIE, Dinner Circles, Page X-Ray, Remy, Universal Rail Intelligence, CIL, and notifications when the scope claims or depends on them.
- Empty, loading, stale, partial, failed, success, permission-blocked, and recovery states.
- Runtime proof in the canonical app when UI behavior is involved.

## Cohesion Checklist

Flag cohesion gaps only when they break the defined scope:

- Same entity has conflicting labels, status, urgency, confidence, owner, or next action across scoped surfaces.
- A user sees a signal in one place but the required action, proof, or destination is missing elsewhere.
- A scoped workflow has no return path after deep work.
- Scoped state changes do not propagate to the surfaces that claim to reflect that state.
- Remy, CIL, rail, dashboard, command palette, or lifecycle surfaces describe different realities for the same scoped item.

## Evidence Standard

Do not call work complete without evidence.

Prefer evidence in this order:

1. Running app behavior at `http://localhost:3100` or the explicitly verified URL.
2. Focused tests, type checks, or smoke checks.
3. Browser console, network, and server-log checks for affected routes.
4. Screenshots, recordings, semantic snapshots, or route checks for UI work.
5. Wiring audit or finish-check output when a fired queue item is involved.
6. Code inspection only when runtime proof is not feasible; mark the residual risk.

## Output Format

Use this structure for audits and closeout checks:

```md
**Scope Contract**
What the current scope promises, and what is explicitly out of scope.

**Verdict**
complete | incomplete | visually present but not operational | wired but not cohesive | blocked | cannot prove

**Mandatory Gaps**
Only gaps that prevent the promised scope from being honestly done.

**Wiring Gaps**
Missing or broken route, nav, action, server action, API, DB, state, rail, command, Remy, CIL, lifecycle, notification, permission, or recovery connections.

**Cohesion Gaps**
Contradictions or missing propagation across scoped surfaces.

**Proof Gaps**
Evidence still needed before closeout.

**Rejected Expansion**
Useful ideas that are not mandatory for this scope and should not be part of the completion batch.

**Smallest Completion Batch**
The minimum work required to close the scope, with likely files or surfaces when known.

**Acceptance Proof**
Concrete checks that would prove completion.
```

## Implementation Rules When Authorized

1. Run `git status --short` before edits.
2. Identify unrelated dirty work and do not touch it.
3. Define the exact scope contract before changing files.
4. Edit only files needed for mandatory completion.
5. Preserve auth, tenant scoping, route policy, role gates, privacy boundaries, and existing product contracts.
6. Add focused tests when completion depends on behavior, data flow, permissions, or shared logic.
7. Verify the running route for UI work when feasible.
8. Keep non-mandatory ideas under `Rejected Expansion`.
9. Do not move fired queue work to `done` unless the finish gate and proof requirements are satisfied.

## Anti-Patterns

Do not:

- Turn completion into feature deepening.
- Suggest "one more dashboard card" unless the scoped contract requires it.
- Treat visual presence as working software.
- Treat navigation as workflow completion.
- Treat AI explanation as canonical state.
- Audit the whole app when the user gave a bounded scope.
- Recommend refactors unless they are required to close the scope.
- Hide uncertainty. If proof is missing, say `cannot prove`.
