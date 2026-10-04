---
name: simulation-state-machine
description: Use this skill whenever writing the simulator runtime, step gating logic, session state object, restart/reset controls, wrong-order interaction handling, completion transitions, or any code that reads or writes the simulation's current state. This is the authoritative runtime contract for the simulator. Load this skill before writing any simulator state, session, or progression logic. Use alongside loto-interaction-mechanics for step-specific physics and tolerances.
---

This skill defines the runtime architecture and state machine for the Myelin simulator. It is the contract between the simulation physics layer (see `loto-interaction-mechanics`), the telemetry layer (see `simulation-telemetry-schema`), and the UI shell. Every state transition must go through this machine. No simulation state may be mutated directly from interaction handlers.

---

## Session State Object

The canonical shape of the simulation session at runtime. This object is the single source of truth for all simulation state. No component reads state from anywhere else.

```javascript
const simulationSession = {
  sessionId: '',           // UUID v4, generated at session init
  learnerId: '',           // tenant-scoped learner identifier
  tenantId: '',            // institution identifier
  scenarioId: 'LOTO_7STEP_v1',
  scenarioVersion: '',     // semver of the active scenario definition
  scoringRulesVersion: '', // semver of the scoring rules applied
  demoMode: false,         // set at init, immutable for session lifetime

  currentStep: 1,          // 1–7, the step the learner is currently on
  maxUnlockedStep: 1,       // highest step the learner may attempt
  status: 'IDLE',          // IDLE | IN_PROGRESS | PAUSED | COMPLETE | FAILED

  stepStates: {
    1: { status: 'UNLOCKED', attemptCount: 0, passedAt: null },
    2: { status: 'LOCKED',   attemptCount: 0, passedAt: null },
    3: { status: 'LOCKED',   attemptCount: 0, passedAt: null },
    4: { status: 'LOCKED',   attemptCount: 0, passedAt: null },
    5: { status: 'LOCKED',   attemptCount: 0, passedAt: null },
    6: { status: 'LOCKED',   attemptCount: 0, passedAt: null },
    7: { status: 'LOCKED',   attemptCount: 0, passedAt: null }
  },

  attemptHistory: [],      // ordered array of SimStepEvent records for this session
  resetCount: 0,           // number of full session resets
  assistModeActive: false, // whether AI-guided instruction mode is on
  inputMode: 'POINTER',    // POINTER | KEYBOARD | GAMEPAD | HAND_TRACKING
  startedAt: null,         // ISO 8601, set when first step interaction begins
  completedAt: null,       // ISO 8601, set on COMPLETE transition
  lastInteractionAt: null  // ISO 8601, updated on every interaction event
};
```

Step status values:
- `LOCKED` — step is not yet accessible; prior step has not passed
- `UNLOCKED` — step is accessible but not yet attempted
- `IN_PROGRESS` — step interaction is currently active
- `PASSED` — step has passed validation; gate opens for next step
- `FAILED` — most recent attempt on this step failed; retry is available

---

## State Machine Transitions

All state transitions are handled through a single dispatch function. Interaction handlers call `dispatch()` — they never mutate the session state object directly.

```javascript
function dispatch(action, session) {
  switch (action.type) {
    case 'SESSION_START':
      return handleSessionStart(action, session);
    case 'STEP_ATTEMPT':
      return handleStepAttempt(action, session);
    case 'STEP_PASS':
      return handleStepPass(action, session);
    case 'STEP_FAIL':
      return handleStepFail(action, session);
    case 'WRONG_ORDER_INTERACTION':
      return handleWrongOrder(action, session);
    case 'SESSION_RESET':
      return handleSessionReset(action, session);
    case 'SESSION_COMPLETE':
      return handleSessionComplete(action, session);
    case 'ASSIST_TOGGLE':
      return handleAssistToggle(action, session);
    case 'INPUT_MODE_CHANGE':
      return handleInputModeChange(action, session);
    default:
      return session;
  }
}
```

### SESSION_START

```javascript
function handleSessionStart(action, session) {
  return {
    ...session,
    sessionId: generateUUID(),
    learnerId: action.learnerId,
    tenantId: action.tenantId,
    demoMode: action.demoMode,
    status: 'IDLE',
    startedAt: null,
    stepStates: resetStepStates()
  };
}
```

`demoMode` is set here and must never be changed by any subsequent action.

### STEP_ATTEMPT

Called when a learner begins interacting with a step's primary object.

```javascript
function handleStepAttempt(action, session) {
  const { stepId } = action;
  if (session.stepStates[stepId].status === 'LOCKED') {
    // Attempting a locked step is a WRONG_ORDER_INTERACTION — do not advance
    return dispatch({ type: 'WRONG_ORDER_INTERACTION', stepId }, session);
  }
  return {
    ...session,
    status: 'IN_PROGRESS',
    currentStep: stepId,
    startedAt: session.startedAt || new Date().toISOString(),
    lastInteractionAt: new Date().toISOString(),
    stepStates: {
      ...session.stepStates,
      [stepId]: {
        ...session.stepStates[stepId],
        status: 'IN_PROGRESS',
        attemptCount: session.stepStates[stepId].attemptCount + 1
      }
    }
  };
}
```

### STEP_PASS

Called by the physics/validation layer when a step's acceptance criteria are met. Never called from the UI layer directly.

```javascript
function handleStepPass(action, session) {
  const { stepId, measuredValue, timestamp } = action;
  const nextStep = stepId < 7 ? stepId + 1 : null;

  const updatedStepStates = {
    ...session.stepStates,
    [stepId]: {
      ...session.stepStates[stepId],
      status: 'PASSED',
      passedAt: timestamp
    }
  };

  if (nextStep) {
    updatedStepStates[nextStep] = {
      ...session.stepStates[nextStep],
      status: 'UNLOCKED'
    };
  }

  const newSession = {
    ...session,
    stepStates: updatedStepStates,
    maxUnlockedStep: Math.max(session.maxUnlockedStep, nextStep || stepId),
    lastInteractionAt: timestamp
  };

  // Check for overall completion
  if (stepId === 7) {
    return dispatch({ type: 'SESSION_COMPLETE', timestamp }, newSession);
  }

  return newSession;
}
```

### STEP_FAIL

Called by the physics/validation layer when a step attempt does not meet acceptance criteria.

```javascript
function handleStepFail(action, session) {
  const { stepId, measuredValue, requiredThreshold, timestamp } = action;
  return {
    ...session,
    lastInteractionAt: timestamp,
    stepStates: {
      ...session.stepStates,
      [stepId]: {
        ...session.stepStates[stepId],
        status: 'FAILED'
      }
    }
  };
}
```

On STEP_FAIL: display corrective feedback identifying the specific tolerance not met. Do not reset the step's attempt count. Do not unlock or lock any other step. The learner retries from where they are.

### WRONG_ORDER_INTERACTION

Called when the learner attempts to interact with an object belonging to a locked step.

```javascript
function handleWrongOrder(action, session) {
  // No state change — purely triggers feedback
  showWrongOrderFeedback(action.stepId, session.currentStep);
  return session; // state is unchanged
}
```

Wrong-order interactions produce immediate corrective feedback — "Complete step [N] first" — without changing any step state or advancing the session. They do not increment the attempt count on the target step.

### SESSION_RESET

```javascript
function handleSessionReset(action, session) {
  return {
    ...session,
    currentStep: 1,
    maxUnlockedStep: 1,
    status: 'IDLE',
    stepStates: resetStepStates(),
    attemptHistory: [],
    resetCount: session.resetCount + 1,
    startedAt: null,
    completedAt: null,
    lastInteractionAt: null
    // demoMode, sessionId, learnerId, tenantId are preserved
  };
}
```

Full reset restores all steps to their initial locked/unlocked states. It preserves `sessionId`, `learnerId`, `tenantId`, and `demoMode`. The `resetCount` is incremented and must be included in the session completion telemetry.

### SESSION_COMPLETE

```javascript
function handleSessionComplete(action, session) {
  // Guard: all steps 1–7 must have status PASSED
  const allPassed = Object.values(session.stepStates).every(s => s.status === 'PASSED');
  if (!allPassed) {
    console.error('SESSION_COMPLETE dispatched without all steps passing — guard rejected');
    return session;
  }
  return {
    ...session,
    status: 'COMPLETE',
    completedAt: action.timestamp
  };
}
```

The completion guard is non-negotiable. If `SESSION_COMPLETE` is dispatched without all seven steps passing, the transition is rejected and the session state is unchanged. This is the last line of defence before the `SIM_COMPLETE` telemetry event fires and the post-simulation UI unlocks.

---

## Feedback Requirements by State Transition

| Transition | Required feedback |
|---|---|
| STEP_PASS | Visual snap/confirmation, audio cue for step (see `loto-interaction-mechanics`), step indicator updates to green |
| STEP_FAIL | Visual indicator on the failed interaction point, plain-language message stating which tolerance was not met, no audio completion cue |
| WRONG_ORDER_INTERACTION | Corrective message "Complete step [N] first", highlight the current active step indicator, no audio completion cue |
| SESSION_COMPLETE | Full completion animation, summary panel with step trace, `SIM_COMPLETE` event emitted |
| SESSION_RESET | Scene returns to initial position, all step indicators reset, reset counter visible to learner |

All feedback must be readable under both bright and low-contrast scene conditions.

---

## Camera Reset Control

The simulator must expose a camera reset control at all times during a simulation session. Camera reset:
- Returns the camera to the default scene position
- Does not affect any step state or session state
- Does not count as a step interaction or reset
- Is accessible via keyboard shortcut (default: `R`)

---

## AI-Guided Instruction Mode

The `assistModeActive` flag controls whether the AI learning coach panel is visible alongside the simulation. It is toggleable during a session via the assist mode button (SIM-006).

Toggling assist mode:
- Does not pause the simulation
- Does not affect step state
- Does not affect scoring

When assist mode is active, the AI agent receives `activeStepId` and `recentErrors` from the current session state on every message. See `agent-context-binding` skill for the full context-binding contract.

---

## Performance Integration

The simulation state machine operates on the CPU thread. Physics and rendering run on the GPU/render loop. The state machine must not block the render loop.

Rules:
- Step validation results are passed to the state machine via a callback, not inline in the render loop
- State machine dispatch must complete in under 2 ms
- If dispatch takes longer than 2 ms in profiling, the state update is too complex — simplify

---

## Startup Sequence

1. Initialize `simulationSession` with `SESSION_START` action
2. Load scenario geometry and PBR assets (non-blocking, show loading state)
3. Initialize physics engine with baseline settings (see `physics-baseline` skill)
4. Register interaction handlers on scene objects
5. Set `stepStates[1].status = 'UNLOCKED'`, all others `LOCKED`
6. Render scene and await first learner interaction
7. First interaction on Step 1 dispatches `STEP_ATTEMPT`

Scene first interaction must be achievable within 5 seconds on standard broadband (SIM startup target from PRD Section 10.2).

---

## Known Prototype Bug — Fix Required

The existing prototype has a broken navigation target after simulator completion — it points to a non-existent `assignments` view. The `SESSION_COMPLETE` handler must route to the e-Portfolio submission view (`view-portfolio` / `/submissions/new`), not `assignments`. This is the correct post-completion destination per the learner journey (step 4: submit practical evidence).

---

## What Not To Do

- Do not mutate `simulationSession` directly from interaction handlers — always use `dispatch()`
- Do not call `SESSION_COMPLETE` without the all-steps-passed guard
- Do not allow `WRONG_ORDER_INTERACTION` to change any step state
- Do not change `demoMode` after `SESSION_START`
- Do not allow step `maxUnlockedStep` to decrease during a session (forward-only progression)
- Do not block the render loop with synchronous state dispatch
- Do not route post-completion to the `assignments` view — route to `/submissions/new`
