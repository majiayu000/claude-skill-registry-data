---
name: agent-context-binding
description: Use this skill whenever writing any AI agent API call, chat message handler, context assembly function, or code that constructs the payload sent to the Tau learning coach. This defines exactly what simulation and session context must be collected, how it is structured, and how it must be attached to every agent request. An agent call without correct context binding is a policy violation. Load this skill before writing any agent integration code.
---

This skill defines the context-binding contract for the Tau AI learning coach. The agent's value — and its safety compliance — depends entirely on it knowing exactly where the learner is, what they have tried, and what went wrong. A response composed without this context is a generic chatbot response. The platform must never produce generic chatbot responses.

---

## Context Binding Requirement

Every agent API call must include a fully-assembled `AgentContext` object. No exceptions. If any required context field is unavailable, use the fallback values specified below — do not omit the field and do not call the agent without context.

This requirement applies to all three response modes: TEXT, GUIDED_MEDIA, and LIVE_CONVERSATIONAL.

---

## AgentContext Schema

```javascript
const agentContext = {
  // Session identity
  sessionId:   '',    // current simulation/learning session UUID
  learnerId:   '',    // tenant-scoped learner identifier (never raw email)
  tenantId:    '',    // institution identifier
  demoMode:    false, // mirrors simulation session demoMode

  // Learning location
  activeModuleId:   '',    // current module ID, e.g. 'MOD-FND-TT-01'
  activeModuleTitle: '',   // human-readable, e.g. 'Lockout/Tagout Procedures'
  activeItemId:     '',    // current learning item ID
  activeItemType:   '',    // 'VIDEO' | 'QUIZ' | 'SIMULATION' | 'PRACTICAL_TASK'

  // Simulation state — populated when activeItemType is SIMULATION
  simulation: {
    active:           false,   // true only when learner is inside the simulator
    scenarioId:       '',      // e.g. 'LOTO_7STEP_v1'
    currentStep:      null,    // integer 1–7, or null if not in simulation
    currentStepLabel: '',      // e.g. 'Apply hasp to valve stem'
    stepStatus:       '',      // 'UNLOCKED' | 'IN_PROGRESS' | 'FAILED'
    attemptCount:     0,       // total attempts on currentStep in this session
    recentErrors:     [],      // last 3 FAIL events on currentStep (see schema below)
    assistModeActive: false
  },

  // Learner performance signals (session-scoped)
  performance: {
    stepsPassedThisSession:   0,
    stepsFailedThisSession:   0,
    totalResetCount:          0,
    sessionElapsedSeconds:    0,
    priorSessionAttemptCount: 0   // attempts on this scenario in previous sessions
  },

  // Agent mode being used
  agentMode: 'TEXT'   // 'TEXT' | 'GUIDED_MEDIA' | 'LIVE_CONVERSATIONAL'
};
```

### recentErrors schema

Each entry in `recentErrors` is a trimmed version of a `SimStepEvent` FAIL record:

```javascript
{
  stepId:           'LOTO_STEP_03',
  attemptNumber:    2,
  timestamp:        '2026-03-12T10:32:15.000Z',
  measuredValue:    0.045,    // what was actually measured
  requiredThreshold: 0.02,   // what was needed to pass
  thresholdOperator: 'LT'    // the operator that applies
}
```

The `recentErrors` array holds a maximum of 3 entries. If there are more than 3 FAIL events on the current step, include only the 3 most recent. The agent uses these to tailor its hint — it can see exactly how far off the learner's attempts have been without being told the pass threshold explicitly.

---

## Context Assembly Function

Build `AgentContext` from the live simulation session state before every agent call.

```javascript
function assembleAgentContext(session, moduleState, agentMode) {
  const recentStepFails = session.attemptHistory
    .filter(e => e.stepId === `LOTO_STEP_0${session.currentStep}` && e.result === 'FAIL')
    .slice(-3)  // last 3 only
    .map(e => ({
      stepId:            e.stepId,
      attemptNumber:     e.attemptNumber,
      timestamp:         e.timestamp,
      measuredValue:     e.measuredValue,
      requiredThreshold: e.requiredThreshold,
      thresholdOperator: e.thresholdOperator
    }));

  const stepsPassedCount = Object.values(session.stepStates)
    .filter(s => s.status === 'PASSED').length;

  const stepsFailedCount = session.attemptHistory
    .filter(e => e.result === 'FAIL').length;

  return {
    sessionId:         session.sessionId,
    learnerId:         session.learnerId,
    tenantId:          session.tenantId,
    demoMode:          session.demoMode,

    activeModuleId:    moduleState.moduleId,
    activeModuleTitle: moduleState.moduleTitle,
    activeItemId:      moduleState.activeItemId,
    activeItemType:    moduleState.activeItemType,

    simulation: {
      active:           true,
      scenarioId:       session.scenarioId,
      currentStep:      session.currentStep,
      currentStepLabel: getStepLabel(session.currentStep),
      stepStatus:       session.stepStates[session.currentStep].status,
      attemptCount:     session.stepStates[session.currentStep].attemptCount,
      recentErrors:     recentStepFails,
      assistModeActive: session.assistModeActive
    },

    performance: {
      stepsPassedThisSession:   stepsPassedCount,
      stepsFailedThisSession:   stepsFailedCount,
      totalResetCount:          session.resetCount,
      sessionElapsedSeconds:    getElapsedSeconds(session.startedAt),
      priorSessionAttemptCount: moduleState.priorAttemptCount || 0
    },

    agentMode
  };
}
```

### Fallback values when simulation is not active

When the learner is using the agent outside the simulator (e.g. on a module content page):

```javascript
simulation: {
  active:           false,
  scenarioId:       '',
  currentStep:      null,
  currentStepLabel: '',
  stepStatus:       '',
  attemptCount:     0,
  recentErrors:     [],
  assistModeActive: false
}
```

The `simulation.active: false` flag tells the agent it is in module-content mode and should use the `activeModuleId` and `activeItemType` as its primary context anchor.

---

## System Prompt Construction

The `AgentContext` object is serialised into the system prompt that precedes every agent API call. The system prompt must always be constructed from the live context — never cached or reused from a prior turn.

```javascript
function buildSystemPrompt(context, agentInstructions) {
  const simSection = context.simulation.active
    ? `
SIMULATION STATE:
- Scenario: ${context.simulation.scenarioId}
- Current step: Step ${context.simulation.currentStep} — ${context.simulation.currentStepLabel}
- Step status: ${context.simulation.stepStatus}
- Attempts on this step: ${context.simulation.attemptCount}
- Recent failures: ${JSON.stringify(context.simulation.recentErrors, null, 2)}
    `
    : `
SIMULATION STATE: Not currently in simulator
    `;

  return `
You are Tau, the Myelin AI learning coach. You support learners studying ${context.activeModuleTitle}.

LEARNER CONTEXT:
- Module: ${context.activeModuleId} — ${context.activeModuleTitle}
- Current item type: ${context.activeItemType}
${simSection}
PERFORMANCE SIGNALS:
- Steps passed this session: ${context.performance.stepsPassedThisSession}
- Steps failed this session: ${context.performance.stepsFailedThisSession}
- Session resets: ${context.performance.totalResetCount}
- Elapsed time: ${Math.round(context.performance.sessionElapsedSeconds / 60)} minutes

DEMO MODE: ${context.demoMode ? 'YES — use synthetic signals only' : 'NO — live learner session'}

${agentInstructions}
  `.trim();
}
```

`agentInstructions` is the policy and pedagogy layer loaded from the `agent-safety-guardrails` skill. It is always appended after the context section. Context comes first — the agent must read where the learner is before reading the policy rules.

---

## Conversation History Management

The agent has no memory between API calls. The full conversation history must be included in every request.

```javascript
function buildMessagePayload(context, conversationHistory, newUserMessage) {
  return {
    systemPrompt: buildSystemPrompt(context, loadAgentInstructions()),
    messages: [
      ...conversationHistory,
      { role: 'user', content: newUserMessage }
    ]
  };
}
```

Conversation history is stored in the client session state. It is an ordered array of `{ role: 'user' | 'assistant', content: string }` objects. Maximum history to send: 20 turns (10 exchanges). Beyond 20 turns, trim from the oldest while preserving the most recent context.

Do not include `agentContext` objects from prior turns in the history — only the text of the exchange. The current context is always reconstructed fresh from live session state and prepended as the system prompt.

---

## Context Update Triggers

The `AgentContext` must be rebuilt (not reused) whenever any of the following change:

| Event | Context fields that change |
|-------|---------------------------|
| Learner moves to a new simulation step | `simulation.currentStep`, `simulation.currentStepLabel`, `simulation.stepStatus`, `simulation.attemptCount`, `simulation.recentErrors` |
| A step attempt FAIL event fires | `simulation.recentErrors`, `simulation.attemptCount`, `performance.stepsFailedThisSession` |
| A step attempt PASS event fires | `simulation.stepStatus`, `performance.stepsPassedThisSession` |
| Learner resets the session | All `simulation.*` and `performance.*` fields |
| Learner navigates to a different module item | `activeItemId`, `activeItemType`, `simulation.active` |
| Assist mode toggled | `simulation.assistModeActive` |

Context is cheap to build. Always rebuild it. Do not cache it.

---

## Demo Mode Agent Behaviour

When `context.demoMode === true`:

- The system prompt must include `DEMO MODE: YES — use synthetic signals only`
- `context.simulation.recentErrors` is populated from the demo dataset synthetic error history, not real learner errors
- The agent narrates each step as both a learning moment and a platform capability demonstration: "In a live session, a learner who has reached this step three times would receive a hint like..."
- No real learner's attempt data, name, or institution may appear in any demo agent response

---

## What Not To Do

- Do not call the agent API without a fully assembled `AgentContext`
- Do not cache `AgentContext` from a prior turn — always rebuild from live state
- Do not include `agentContext` objects in the conversation history array — only text turns
- Do not set `recentErrors` to an empty array when errors exist — always populate with the last 3
- Do not expose the exact pass threshold value (`requiredThreshold`) in the agent's response to the learner — it is in the context for the agent's reasoning only, not for output (enforced by `agent-safety-guardrails`)
- Do not set `demoMode: false` in context when the session is a demo session
- Do not omit the `agentInstructions` (safety guardrails) from the system prompt
- Do not reuse a system prompt from a prior turn
