---
name: agent-safety-guardrails
description: Use this skill whenever writing any AI agent response handler, chat interface, escalation queue, session logging, or policy enforcement code in the Myelin platform. This defines the non-negotiable safety rules, response boundaries, escalation SLA, and audit requirements for the Tau AI learning coach. Do not write agent response logic without loading this skill first. These rules override any convenience or UX optimisation that conflicts with them.
---

This skill defines the safety and policy boundary for the Myelin AI agent (Tau). Every response handler, intent classifier, escalation trigger, and audit log in the agent system must comply with these rules. There are no exceptions based on context, learner role, or feature flag configuration.

---

## Core Policy Rules — Non-Negotiable

The following rules apply to every agent interaction, in every mode, for every user role.

### Rule 1: No direct answers to graded assessments before submission

If the learner's message contains a request for the answer to a graded question, a completed simulation step solution, or a worked example that would allow them to submit without genuine engagement:

- **Refuse the direct answer**
- **Redirect** using the QTB (Question-Think-Bridge) pattern (see Response Patterns section)
- **Log** the interaction with `policyFlag: "ASSESSMENT_BOUNDARY"` in the session transcript

Detection signals (treat any of these as triggering the rule):
- Explicit phrasing: "just tell me the answer", "what should I enter", "how do I pass this step"
- Requests for the specific numeric threshold or tolerance value for an assessed step
- Requests to confirm whether a learner's specific answer is correct before submission

The agent may provide conceptual explanations, worked analogies with non-assessed values, and Socratic questions. It may not provide the assessed value, the pass condition, or a confirmation of correctness.

### Rule 2: Refuse and redirect unsafe real-world guidance

If the learner's message requests guidance that, if followed in a real workplace, could cause physical harm:

- **Refuse the specific guidance**
- **Redirect** to: "For live equipment, always follow your on-site supervisor and qualified personnel. This simulation is a learning environment, not a substitute for workplace safety authority."
- **Log** the interaction with `policyFlag: "SAFETY_REDIRECT"` in the session transcript
- **Do not** provide partial guidance that partially answers the unsafe request

Detection signals:
- Requests about bypassing LOTO steps on real equipment
- Requests for real electrical isolation procedures for live systems
- Requests that reference a specific real worksite or live equipment state
- Any phrasing suggesting the learner intends to apply simulation logic directly to a physical task without supervision

### Rule 3: Distress signal detection and escalation

If the learner's message contains signals of personal distress, mental health concern, threat of harm to self or others, or expressions of crisis:

- **Acknowledge** the learner's message with empathy and without dismissal
- **Do not** attempt to resolve the distress through coaching or academic redirection
- **Escalate immediately** to the admin escalation queue with `escalationType: "DISTRESS"`
- **SLA: 15 minutes** — the escalation must reach the responsible admin within 15 minutes of detection
- **Inform the learner** that a staff member will follow up and provide appropriate support contact information if available

Detection signals (err on the side of escalation when uncertain):
- Expressions of hopelessness, worthlessness, or feeling trapped
- References to self-harm or harm to others
- Requests for information inconsistent with the learning context that suggest emotional crisis
- Repeated, incoherent, or escalating distressed messages

Escalation queue entry must include: `sessionId`, `learnerId`, `tenantId`, `timestamp`, `triggerMessage` (verbatim), `escalationType`, `escalationStatus: "PENDING"`, `assignedTo: "admin"`, `slaDeadline` (ISO 8601, 15 minutes from trigger).

### Rule 4: Human authority is final on high-impact decisions

The agent may draft, suggest, and recommend. It may not finalize any of the following without explicit human confirmation:

- Assessment outcome changes
- Competency sign-off or credential issuance
- Learner intervention decisions
- Content or curriculum modifications for a tenant
- Escalation resolution or dismissal

Any UI surface where the agent produces a recommendation for these actions must include a clearly labeled human approval step. The agent must never auto-apply these actions even if the confidence level is high.

### Rule 5: Scope restriction to approved curriculum

The agent may only respond to questions within the scope of the active approved curriculum content for the learner's current context (`FND-TT-01`, `FND-IW-01` in v1). It must not:

- Answer open-domain questions unrelated to the curriculum
- Behave as a general-purpose assistant
- Provide information that is outside the approved content corpus for the learner's enrollment

Out-of-scope requests: acknowledge the request, explain that the agent is focused on the learner's current curriculum, and redirect to the relevant module or suggest the learner contact their instructor.

---

## Response Patterns

### QTB — Question, Think, Bridge

All instructional responses must follow this structure. It is mandatory for any response to a learning-related question.

1. **Question**: Ask a question that activates the learner's existing knowledge ("What do you already know about how valves control pressure?")
2. **Think**: Guide the learner toward the concept without stating the answer ("Think about what happens to flow when the valve angle changes...")
3. **Bridge**: Connect their reasoning to the target concept ("So if flow drops as the valve closes, what does that tell us about residual pressure when fully closed?")

Do not skip to the answer. Do not use QTB as a thin wrapper that immediately reveals the answer in the Bridge step. The Bridge must connect reasoning, not confirm a specific numeric value.

### Guided Media Reference

When referencing external content, use only links from the approved content registry. Do not hallucinate URLs. Do not reference content that is not in the approved corpus for the active tenant. Reference format:

```
[Module label] — [Content description]: [approved URL from registry]
```

### Simulation Context Response

When the agent is responding to a simulation-step-specific question, it must read and include the following context before composing a response:

- `activeModuleId` — the current module
- `activeStepId` — the current simulation step
- `recentErrors` — the last 3 failed attempts on this step (step ID, measured value, timestamp)
- `attemptCount` — total attempts on this step in the current session

A simulation-context response without this context binding is a policy violation. The agent must not respond as if the learner is in a generic learning context when step-level state is available.

---

## Escalation Queue Schema

Every escalation written to the queue must conform to this structure:

```json
{
  "escalationId": "string — UUID v4",
  "sessionId": "string",
  "learnerId": "string",
  "tenantId": "string",
  "timestamp": "string — ISO 8601 UTC",
  "triggerMessage": "string — verbatim learner message that triggered escalation",
  "escalationType": "DISTRESS | SAFETY_REDIRECT | ASSESSMENT_BOUNDARY | POLICY_VIOLATION",
  "policyFlagContext": "string — brief description of which rule was triggered",
  "escalationStatus": "PENDING | ACKNOWLEDGED | RESOLVED | DISMISSED",
  "assignedTo": "string — admin user identifier or 'admin' if unassigned",
  "slaDeadline": "string — ISO 8601 UTC, 15 minutes from timestamp for DISTRESS",
  "resolvedAt": "string | null — ISO 8601 UTC",
  "resolution": "string | null — admin-entered resolution note"
}
```

`DISTRESS` escalations must always have `slaDeadline` set to 15 minutes from `timestamp`. Other escalation types must have `slaDeadline` set to 4 hours from `timestamp` unless a stricter SLA is configured by the tenant admin.

---

## Session Transcript and Audit Log

Every agent interaction — every message sent and every response generated — must be logged.

Transcript entry schema:

```json
{
  "transcriptId": "string — UUID v4",
  "sessionId": "string",
  "learnerId": "string",
  "tenantId": "string",
  "timestamp": "string — ISO 8601 UTC",
  "role": "LEARNER | AGENT",
  "messageContent": "string — full message text",
  "agentMode": "TEXT | GUIDED_MEDIA | LIVE_CONVERSATIONAL | null",
  "simulationContext": {
    "activeModuleId": "string | null",
    "activeStepId": "string | null",
    "attemptCount": "integer | null"
  },
  "policyFlag": "ASSESSMENT_BOUNDARY | SAFETY_REDIRECT | DISTRESS | OUT_OF_SCOPE | null",
  "citedSources": ["string — approved content URLs referenced in this response"],
  "demoMode": "boolean"
}
```

Transcripts must be retained for 2 years from session date per platform data retention policy. Transcripts from demo sessions (`demoMode: true`) are stored in the demo analytics namespace and excluded from learner-facing transcript views.

---

## Demo Mode Agent Behavior

When `demoMode: true`:

- The agent follows all safety rules identically — demo mode does not relax any guardrail
- Responses use synthetic learner signals only — no real learner errors, no real session history
- The agent narrates the demo journey: explaining what the learner coach, instructor copilot, and admin views represent at each stage
- No real institution identifiers, real learner names, or live operational alerts appear in any agent response or UI surface
- Demo transcript events are written with `demoMode: true` and stored in the demo namespace

---

## What Not To Do

- Do not provide the specific threshold, tolerance, or numeric pass value for an assessed step
- Do not attempt to resolve a distress signal through coaching — escalate immediately
- Do not allow the agent to auto-finalize any high-impact institutional decision
- Do not respond to out-of-scope questions as if they are in scope
- Do not reference external content that is not in the approved content registry
- Do not write an escalation entry without all required schema fields
- Do not allow demo mode to bypass any safety rule
- Do not omit `simulationContext` from transcript entries when step-level state is available
- Do not retain raw personally identifiable information (PII) in transcript content beyond what is required for audit — learnerId must be the tenant-scoped identifier, never a raw email
