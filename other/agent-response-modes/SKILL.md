---
name: agent-response-modes
description: Use this skill whenever writing the agent response handler, mode switching logic, guided media reference system, live conversational video integration, QTB response formatting, or any code that determines how Tau delivers a response to the learner. This defines the three response modes, their switching rules, the QTB pedagogy contract, and the approved content registry pattern. Load this skill before writing any agent response or delivery code.
---

This skill defines how the Tau AI learning coach delivers responses to learners. The what-to-say rules live in `agent-safety-guardrails`. The how-to-say-it rules live here. Both must be loaded when writing agent response code.

---

## Three Response Modes

Tau supports three response modes. The active mode is stored in the session state and determines both how the response is rendered and what the API request shape looks like.

| Mode | ID | v1 Status | Description |
|------|----|-----------|-------------|
| Text | `TEXT` | Always on | Standard conversational text response, markdown-aware |
| Guided media | `GUIDED_MEDIA` | Feature-flagged per tenant | Text response with embedded references to approved video/document content |
| Live conversational | `LIVE_CONVERSATIONAL` | Feature-flagged, Operational/National tier only; not pilot-launch blocking | Voice + avatar/video surface; real-time interaction after readiness sign-off |

Mode availability is gated by tenant feature flags. The UI must check `tenant.featureFlags.aiAgentGuidedMedia` and `tenant.featureFlags.aiAgentLiveConversational` before rendering mode toggle controls.

---

## Mode Switching Rules

The learner may switch modes mid-session. Switching modes does not reset conversation history.

```javascript
function switchAgentMode(currentSession, newMode) {
  const allowed = getAvailableModes(currentSession.tenant);

  if (!allowed.includes(newMode)) {
    throw new FeatureGateError(`AGENT_MODE_NOT_AVAILABLE: ${newMode}`);
  }

  return {
    ...currentSession,
    agentMode: newMode
  };
}

function getAvailableModes(tenant) {
  const modes = ['TEXT']; // always available
  if (tenant.featureFlags.aiAgentGuidedMedia)       modes.push('GUIDED_MEDIA');
  if (tenant.featureFlags.aiAgentLiveConversational) modes.push('LIVE_CONVERSATIONAL');
  return modes;
}
```

When the learner is inside the simulator, mode switching is available but must not interrupt the simulation. The mode toggle is a HUD control — it changes the coach panel's rendering mode without affecting the 3D scene or session state machine.

---

## Mode 1 — TEXT

Standard text response. Markdown is supported for structure (headings, lists, code blocks when relevant to technical concepts). Responses must be concise — the learner is mid-task.

Response length targets:
- Hint during simulation step: 2–4 sentences maximum
- Conceptual explanation between steps: 4–8 sentences or a short list
- Safety redirect message: 2–3 sentences
- Distress acknowledgement: 3–4 sentences before escalation handoff

All text responses must follow the QTB pattern (defined below) unless the response is a safety redirect, distress acknowledgement, or out-of-scope redirect.

```javascript
function buildTextResponse(agentOutput) {
  return {
    mode: 'TEXT',
    content: agentOutput.text,
    citations: agentOutput.citations || [],   // approved source URLs referenced
    policyFlag: agentOutput.policyFlag || null
  };
}
```

---

## Mode 2 — GUIDED_MEDIA

Text response with embedded references to approved content. The agent may surface a relevant video clip, document section, or diagram from the approved content registry.

The agent must never hallucinate content references. It may only reference items that exist in the `approvedContentRegistry` for the learner's active tenant and module.

```javascript
function buildGuidedMediaResponse(agentOutput, contentRegistry) {
  const references = (agentOutput.contentReferenceIds || [])
    .map(id => contentRegistry.find(item => item.contentId === id))
    .filter(Boolean);   // silently drop any unresolvable reference

  return {
    mode: 'GUIDED_MEDIA',
    content: agentOutput.text,
    mediaReferences: references.map(ref => ({
      contentId:    ref.contentId,
      title:        ref.title,
      contentType:  ref.contentType,   // 'VIDEO' | 'DOCUMENT' | 'DIAGRAM'
      url:          ref.approvedUrl,
      startSeconds: ref.startSeconds || null,   // for video deep-links
      durationSeconds: ref.durationSeconds || null
    })),
    citations: agentOutput.citations || [],
    policyFlag: agentOutput.policyFlag || null
  };
}
```

### Approved content registry entry schema

```javascript
{
  contentId:       'LOTO-VID-003',
  tenantId:        '',              // tenant-specific or '*' for platform-wide
  moduleId:        'MOD-FND-TT-01',
  title:           'Step 3: Applying the hasp — demonstration',
  contentType:     'VIDEO',
  approvedUrl:     'https://content.myelin.io/loto/step3-hasp-demo.mp4',
  startSeconds:    42,              // optional deep-link start time
  durationSeconds: 90,
  standards:       ['FND-TT-01'],
  lastApprovedAt:  '2026-02-01',
  approvedBy:      'content-review-team'
}
```

The registry is tenant-scoped. When a content item's `tenantId` is `'*'`, it is available to all tenants. A tenant-specific content item is only available to that tenant.

Do not allow the agent to reference a URL that is not in the registry. If the agent output contains a URL not in the registry, strip it before sending the response to the client.

---

## Mode 3 — LIVE_CONVERSATIONAL

Voice-enabled interaction with an avatar/video surface. This mode is a controlled v1 feature — not pilot-launch blocking and not available at Pilot tier by default.

v1 implementation requirements for live conversational mode:
- Use a supported real-time voice API (STT → LLM → TTS pipeline, or a unified API)
- Require explicit user gesture to activate the microphone (`getUserMedia` must not be called without a button press)
- Display a clear visual indicator while the microphone is active
- Preserve the same safety guardrails as TEXT mode — voice input does not bypass policy checks
- Transcript of the voice exchange must be logged to `agent_transcripts` with `agentMode: 'LIVE_CONVERSATIONAL'`
- The QTB pedagogy pattern applies to voice responses — the agent thinks aloud through Question, Think, Bridge even in spoken form

Voice response length target: 15–30 seconds of spoken content per turn (approximately 60–120 words). Voice responses must be more conversational and less structured than text — avoid bullet points in TTS output.

---

## QTB Pedagogy Pattern — Mandatory for Instructional Responses

QTB (Question-Think-Bridge) is the required response structure for any agent response to a learning-related question. It applies across all three modes.

### Structure

**Question** — open the response by activating what the learner already knows. Phrase as a genuine question, not rhetorical. Aim to make the learner recall a relevant prior concept before you explain anything.

**Think** — guide the learner toward the concept with a reasoning prompt. Do not state the conclusion. Lead the learner to reach it. Use: "Think about what happens when...", "Consider the relationship between...", "What would change if..."

**Bridge** — connect their reasoning path to the concept or next action. The bridge must reference their reasoning, not just state the answer. It completes the thought they were led toward in the Think step.

### QTB example — Step 3 hasp alignment failure

```
Q: What do you think the hasp needs to do to the valve stem in order to work as a lockout device?

T: Think about what happens to the valve if the hasp isn't fully seated — could someone still turn it? What does that tell you about where the hasp needs to be?

B: Exactly — the hasp has to fully encircle the stem so the valve can't move. Getting it close but not fully aligned leaves a gap that defeats the whole purpose of lockout. Try bringing it in from directly above the stem rather than at an angle.
```

### QTB constraints

- The Bridge step must never state the exact numeric pass threshold (e.g. "you need to be within 2 centimetres"). The agent knows the threshold from the context — it uses it to shape the guidance, not to quote it.
- If the learner has failed the same step 3 or more times, the hint in the Bridge may be more direct and specific — but still must not reveal the threshold value.
- The QTB structure may be compressed for short hints but must not be abandoned. Even a 2-sentence hint should open with a micro-question and close with a guiding bridge.

### When QTB does not apply

Do not use QTB structure for:
- Safety redirect responses (direct, firm, no leading questions)
- Distress acknowledgement (empathic, direct, no pedagogical framing)
- Out-of-scope redirect (brief, neutral, no leading questions)
- Simple factual answers to non-assessed questions (e.g. "What does LOTO stand for?")

---

## Response Classification

Before composing any response, the agent must classify the incoming message into one of these categories. The classification determines which response pattern applies.

```javascript
const RESPONSE_CLASSES = {
  INSTRUCTIONAL:    'QTB pattern required',
  HINT_REQUEST:     'QTB pattern, compressed, step-specific',
  SAFETY_REDIRECT:  'No QTB — direct refusal and redirect',
  ASSESSMENT_BLOCK: 'No QTB — polite refusal, redirect to try',
  DISTRESS:         'No QTB — empathic acknowledgement + escalation',
  OUT_OF_SCOPE:     'No QTB — brief scope explanation + module redirect',
  FACTUAL_SIMPLE:   'No QTB — direct answer permitted'
};
```

Classification logic belongs in the system prompt instructions. The agent self-classifies based on the message content and the `recentErrors` context. The classification is not exposed to the learner — it is a reasoning step.

---

## Citation and Source Reference Format

When the agent refers to a standard, procedure, or approved content in any mode, it must use this format in its text output:

```
[Standard reference]  → e.g. "as required by ISO 14118 Section 4.2"
[Content reference]   → e.g. "See the hasp alignment demonstration (Module 1, Video 3)"
```

The agent must never invent a standard reference. If it cannot cite a specific standard from the approved corpus, it must not cite one at all.

---

## Response Delivery Timing

Response latency targets:
- TEXT mode p95: <= 2.5 seconds from message send to first token rendered
- GUIDED_MEDIA mode p95: <= 3.5 seconds (additional content registry lookup)
- LIVE_CONVERSATIONAL mode end-to-end: <= 1.5 seconds STT-to-first-audio-token

If response latency exceeds these targets in production, surface a visual thinking indicator ("Tau is thinking...") immediately on message send. Do not leave the input in a blank/unresponsive state while waiting for the response.

---

## Response Logging

Every agent response must produce a transcript entry before it is shown to the learner. The response must not be rendered if the transcript write fails — this is an audit integrity requirement.

```javascript
async function deliverAgentResponse(response, context) {
  // Write transcript first
  await writeTranscriptEntry({
    role:             'agent',
    content:          response.content,
    agentMode:        response.mode,
    simulationContext: {
      activeModuleId: context.activeModuleId,
      activeStepId:   context.simulation.currentStep
        ? `LOTO_STEP_0${context.simulation.currentStep}`
        : null,
      attemptCount:   context.simulation.attemptCount
    },
    citedSources:    response.citations,
    policyFlag:      response.policyFlag,
    demoMode:        context.demoMode
  });

  // Render to learner only after transcript is committed
  renderResponseToUI(response);
}
```

See `agent-transcript-logging` skill for the full transcript schema.

---

## What Not To Do

- Do not render a mode toggle for a mode that is not enabled in the tenant feature flags
- Do not call `getUserMedia` for LIVE_CONVERSATIONAL mode without an explicit user gesture
- Do not hallucinate content references — only use items from the approved content registry
- Do not strip or skip the QTB structure for instructional responses to make responses shorter
- Do not quote exact numeric pass thresholds in the Bridge step of a QTB response
- Do not render the agent response to the learner before the transcript entry is committed
- Do not reuse the system prompt from a prior turn — rebuild it from live context every call
- Do not allow voice mode to bypass safety policy checks
- Do not use QTB structure for safety redirects, distress responses, or out-of-scope redirects
