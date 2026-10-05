---
name: flow-detector
description: Analyzes a task description plus the surrounding codebase and produces a list of candidate end-to-end flows. Activates when a developer describes a task using vague verbs (send, notify, sync, handle, process, integrate) without specifying entity, trigger, or recipient. Returns 1 candidate when the flow is unambiguous, 2+ when multiple plausible interpretations exist. Each candidate is a complete proposed execution context, never a question.
---

# Flow Detector

Detect end-to-end flows for a vague task. Output is structured candidates, not questions.

## Activation Triggers

This skill activates when:
- The user runs `/clarify "<task>"` or invokes `@clarifier`.
- The user describes a task using vague verbs: **send, notify, sync, handle, process, integrate, support, fire, dispatch, push, alert, log**.
- The user mentions a ticket reference and the description doesn't fully pin down the implementation surface.

## Core Principle

**Every candidate flow is a complete answer**, not a piece of one. The user picks between whole flows, not between individual dimensions. Do not emit candidates that differ only in trivial parameters (timeout values, log level, retry count) — those are defaults inside one flow.

## Process

### 1. Read the task description

Extract:
- The verb (what is being done)
- Any explicit entity mention (User, Tenant, Order, etc.)
- Any explicit trigger mention (on signup, after payment, etc.)
- Any explicit recipient mention (to the user, to the team, etc.)

### 2. Ground in the codebase

Before generating candidates, scan the repo for evidence:

- **Entities**: search for likely model files — `User`, `Tenant`, `Org`, `Account`, `Workspace`, `Team`, `Member`. Note which exist.
- **Auth surfaces**: search for `sign-in`, `signin`, `login`, `signup`, `register`, `authenticate`, `auth/`, `/api/auth`. Note routes/handlers.
- **Notification channels**: search for email senders (`sendgrid`, `ses`, `resend`, `mailer`), push (`fcm`, `apns`, `expo`), in-app (`notifications` table/service), SMS (`twilio`).
- **Async infrastructure**: queues (`bullmq`, `celery`, `sidekiq`), background jobs, event buses.
- **Failure infrastructure**: retry libs, dead-letter queues, error reporters (`sentry`, `bugsnag`).

Anchor every candidate in symbols you found. A candidate that mentions infrastructure the repo doesn't have is a defect — either reframe the candidate as "build new X" or drop it.

### 3. Generate candidates

A candidate flow is a record:

```json
{
  "id": "kebab-case-id",
  "title": "Short human-readable name",
  "one_line_diff": "What makes this candidate different from the others",
  "full_context": {
    "entity": "...",
    "trigger": { "event": "...", "timing": "before|after|on", "preconditions": ["..."] },
    "action": { "verb": "...", "channel": "...", "recipient": "..." },
    "flow": { "services": ["..."], "mode": "sync|async", "transport": "..." | null },
    "failure_handling": { "strategy": "retry|silent|block|escalate", "details": "..." },
    "out_of_scope": ["..."]
  }
}
```

Rules:

- **Differentiate at the top level**: candidates must differ in entity, trigger, or recipient. If two candidates differ only in retry strategy, merge them into one with the more conservative default.
- **Cap at 4 candidates**: if more than 4 are plausible, group similar ones or pick the top 4 by repo-evidence strength (which entities/services actually exist).
- **Order by evidence strength**: the most-supported candidate is `id: 1`. If a single candidate dominates (no close runner-up), emit just that one.
- **No fictional infrastructure**: if a candidate would require a service the repo lacks, either reframe ("Build minimal in-app notification service, then dispatch") or drop it.

### 4. Decide single vs multiple

You return a list. The caller branches on `length`:

- `length === 1` → caller proceeds straight to artifact generation. Skill must be confident; do not pad to 2 candidates just to ask a question.
- `length >= 2` → caller invokes `flow-selector`.

When in doubt, return more candidates rather than fewer. The user picking between two clear options is cheap; building the wrong thing is expensive.

## Examples

### Example 1 — Single candidate

Task: `"Add a 'Forgot password' link to the login form"`
Repo: Has `app/(auth)/login/page.tsx`, an existing `auth/forgot-password/route.ts` handler, one auth surface.

Output: 1 candidate.
```
[
  {
    "id": "forgot-password-link-existing-flow",
    "title": "Add Forgot password link wiring to existing /forgot-password handler",
    "one_line_diff": "Single auth surface, handler already exists",
    "full_context": { entity: "User", trigger: { event: "click", timing: "on", preconditions: ["on /login page"] }, … }
  }
]
```

### Example 2 — Multiple candidates

Task: `"Send message on sign-in"`
Repo: Has User and Tenant models, an in-app `notifications` table, an email sender, a sign-in route.

Output: 2 candidates.
```
[
  {
    "id": "user-post-auth-notify",
    "title": "User sign-in flow — in-app message to the signing-in user",
    "one_line_diff": "Recipient is the user who signed in; channel is in-app",
    "full_context": { entity: "User", trigger: { event: "post-auth", timing: "after", preconditions: ["successful login"] }, action: { verb: "send", channel: "in-app", recipient: "signing-in user" }, … }
  },
  {
    "id": "tenant-owner-audit-email",
    "title": "Tenant audit flow — email to the tenant owner when a member signs in",
    "one_line_diff": "Recipient is the tenant owner; channel is email",
    "full_context": { entity: "Tenant", trigger: { event: "member-sign-in", timing: "after", preconditions: ["member belongs to tenant"] }, action: { verb: "send", channel: "email", recipient: "tenant.owner" }, … }
  }
]
```

### Example 3 — Repo has no infrastructure

Task: `"Send SMS confirmation on order placed"`
Repo: Has Orders, no SMS provider, no async queue.

Output: 1 candidate, framed as build-new.
```
[
  {
    "id": "build-sms-then-dispatch-on-order",
    "title": "Build SMS infrastructure, then dispatch on order creation",
    "one_line_diff": "No SMS provider in repo; candidate includes provisioning Twilio + queue",
    "full_context": { entity: "Order", trigger: { event: "order.created", timing: "after", preconditions: ["payment captured"] }, … out_of_scope: ["replacing existing email confirmation"] }
  }
]
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Emit 4 candidates that differ only in retry count | Emit 1 candidate with a sensible retry default |
| Emit a candidate using a service that doesn't exist in the repo | Reframe as "build new X" or drop |
| Pad to 2 candidates so the caller asks a question | Trust the single-candidate path; it's the desired UX |
| Ask the user to fill in the entity / trigger | Infer from the task + repo. Each candidate already includes them |
| Phrase candidates as questions ("Should we…") | Phrase as completed proposals ("User sign-in → in-app message to user") |

## Success Criteria

- [ ] Output is an ordered list of 1–4 candidates.
- [ ] Every candidate has a unique top-level differentiator (entity, trigger, or recipient).
- [ ] Every candidate is grounded in symbols actually found in the repo.
- [ ] No candidate is phrased as a question.
- [ ] When the task is unambiguous, exactly one candidate is returned.
