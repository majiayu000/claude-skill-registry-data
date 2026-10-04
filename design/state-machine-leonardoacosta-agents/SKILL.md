---
name: state-machine
description: "Models any UI, workflow, or agent behavior as an explicit state machine. Use whenever the user describes a component or process with multiple interacting modes — loading, empty, error, editing, submitting, authenticated, paused, disconnected, or any combination of flags and derived states. Covers when to use a state machine vs useState/useReducer, how to discover hidden states, guard composition, and routing to the right implementation platform (XState v5 for React, AWS Step Functions for cloud workflows, Godot HSM for game AI). Also use when the user has boolean-flag explosion, defensive state-guard coding, timing coordination across states, or interdependent state updates. Don't reach for this for simple toggles, single-form validation, or server-state caching (React Query handles those)."
---

# State Machine — Decision Router & Modeling Mentor

You model any UI, workflow, or agent behavior as explicit finite state machines. Your job is threefold: (1) help discover the real states hiding in scattered flags, (2) model them cleanly with guards and transitions, (3) route to the right implementation platform.

## Step 1: Discover the real states

Before writing any code, interrogate the problem. Boolean flags are almost never independent — they combine into a finite set of real modes:

| User says | Real states hiding |
|-----------|-------------------|
| "I have isLoading, isError, isSuccess" | `idle → loading → success | error` |
| "Sometimes the button should be disabled" | Discover WHEN: during submission? When form invalid? When unauthorized? Each is a state. |
| "If the user logs out while uploading…" | You have concurrent concerns — the auth state machine and the upload state machine need to be modeled separately (parallel states). |
| "After 3 retries we give up" | `loading → retrying` is a distinct state from initial loading. It has different UI, different timeout, and a `retries >= 3` guard to `error`. |
| "The modal should close on escape, but not during the save animation" | The modal has a `closing` sub-state during the animation. Escape key is only handled in `open`, not `closing`. |

**Heuristic: if you're writing `if (a && !b && c)` to determine what to show, you have implicit states. Name them.**

## Step 2: Choose the right tool

This is NOT a one-size-fits-all decision. Route to the correct implementation:

| Scenario | Implementation | Load |
|----------|---------------|------|
| React component with async flows, forms, auth, wizards | XState v5 + `@xstate/react` | `/react-state-machine` |
| Cloud workflow orchestration (sagas, retries, human approval, parallel branches) | AWS Step Functions (ASL/JSONata) | `/aws-step-functions` |
| Game AI, character behavior, combat/pushdown states | Godot HSM / pushdown automata | `/godot-state-machine-advanced` |
| Simple toggle (`isOpen`, `isActive`) with no guards or async | `useState` is fine — do NOT use a state machine |
| Single form field validation | `useReducer` or Zod — do NOT use a state machine |
| Server cache invalidation, refetching | React Query / TanStack Query — do NOT use a state machine |
| Any other platform (Vue, Svelte, Angular, SwiftUI, Flutter, vanilla JS) | Model the machine using the Step 3 template below, then implement manually with the platform's native tools. No domain skill exists yet — use the modeling patterns in this skill and the platform's own documentation. |

**Load the matching skill immediately after this modeling step.** Don't model and then leave the implementation hanging. The domain skill has the concrete API patterns, anti-patterns, and code examples you need.

## Step 3: Model before you code

Always model the machine before writing it. Use this structure:

```
States: [list each distinct mode]
Events: [what triggers transitions — user actions, API responses, timers]
Transitions: [on EVENT in STATE → NEW_STATE]
Guards: [conditions that block transitions — "only if valid", "only if authorized"]
Actions: [side effects during transitions — show toast, log, navigate]
```

Then ask:
- **Are there impossible states?** If you can be `loading` AND `error` simultaneously, split them into distinct states.
- **Does every state have a way out?** No dead ends — even `error` needs a retry or dismiss path.
- **Are there concurrent concerns?** Auth state + upload state = two independent machines. Use parallel states.
- **What happens on re-entry?** If the user goes loading→error→loading→success, does that differ from the first loading→success? It often does (cached data, different animation).

## Key anti-patterns (learned the hard way)

- **NEVER model derived data as states** — "hasResults", "hasManyResults", "hasNoResults" are not states; they're data in context. The state is `success`; the count lives in `context.count`.
- **NEVER use a timer without a cleanup transition** — if a state has a timeout, it MUST have a `TIMEOUT` event that transitions somewhere. Aborted renders don't clean up timers; your state machine must.
- **NEVER represent "not yet attempted" as the same state as "failed"** — `idle` and `error` are different states. One shows nothing, the other shows an error message and a retry button.
- **NEVER let a guard have side effects** — guards are predicates. If checking "hasPermission" calls an API, that's an invoked actor, not a guard. A guard reads existing context; it doesn't fetch.
- **NEVER send events from inside action handlers** — actions are fire-and-forget. If you need to chain transitions, use the `raise` action (internal event) instead of `send`.

## How to think about state machine sizing

A machine is the right size when:
- You can name every state in one sentence ("this component is either idle, loading, editing, saving, or in an error state")
- Transitions feel obvious once states are named
- You're not creating states for data variations ("loading-5-results" — no, that's context)

Split into sub-machines when:
- One concern doesn't care about another ("the auth state doesn't need to know about the upload progress")
- A state's internal behavior is complex enough to be its own machine ("the form wizard has 5 steps, each with validation")

Compose via invoked actors when:
- One machine needs to spawn and manage another ("the checkout machine invokes a payment machine and waits for its result")

## When you're stuck

If the modeling feels wrong, you might not actually have a state machine problem. Consider:
- **Is this just data flow?** A sequence of API calls with no branching UI might just be an async function with await.
- **Is this just conditional rendering?** "Show admin panel if user.isAdmin" is not a state machine — it's a single guard on a single render.
- **Is this a behavior tree?** If states need to run concurrently with priority-based interruption (game AI often), a behavior tree may fit better than a flat FSM.