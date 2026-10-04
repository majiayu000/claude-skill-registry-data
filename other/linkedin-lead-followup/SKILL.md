---
name: linkedin-lead-followup
description: >-
  Use when reviewing warm LinkedIn prospects and interactions, deciding the next
  relationship action, drafting grounded replies/DMs, and moving genuine
  commercial opportunities through the shared pipeline. Not for cold bulk
  outreach, generic prospect scraping, or publishing posts. Uses `copywriting`
  then `humanizer` to clarify and naturalize an already-grounded message.
  Require a verified Sheet interaction before sending; local state is for
  review and drafting only.
license: MIT
---

# LinkedIn lead follow-up

Develop warm professional relationships created through content, comments,
connections, referrals, or inbound messages. The goal is to identify genuine
commercial fit without converting every interaction into a sales pitch.

## Inputs

Prefer the shared `Prospects`, `Interactions`, and `Pipeline` tabs defined by
`linkedin-workspace`, plus the live LinkedIn thread/profile when an external
action is being considered.

When a shared Sheet is selected, persist the exact follow-up draft in an
`Interactions` row with `Status=pending_approval` and re-read it before asking
for approval. If that write fails or is ambiguous, do not ask for approval or
send the message; retain the local draft for reconciliation by stable IDs.
Use local/session state for read-only review and drafting when no authorized
Sheet is available, but never send a follow-up message without a verified
Interaction row in the selected workspace.

Read:

- [references/qualification.md](references/qualification.md)
- [references/messaging-rules.md](references/messaging-rules.md)

## Boundaries

- This is a **warm follow-up** skill. Do not use it for automated cold DM blasts.
- Do not infer budget, urgency, authority, company problems, or buying intent from
  a job title alone.
- Do not invent familiarity, prior conversations, referrals, client work,
  availability, outcomes, or technical claims.
- Do not draft or send an initial connection request here. Connection requests
  are outside warm follow-up unless the user selects a separate approved
  workflow.
- Do not send a message without approval for that exact action.
- Do not repeatedly follow up with someone who has not responded unless the user
  explicitly asks and the follow-up remains professionally reasonable.

## Relationship workflow

1. Find prospects with a concrete unresolved `Next Action`, recent inbound reply,
   connection acceptance, or meaningful interaction.
2. Inspect the actual recent interaction/thread before recommending action.
3. Update factual relationship state only from observed evidence.
4. Choose the least-salesy useful next action:
   - public reply;
   - no action / continue observing;
   - DM when the relationship/context supports it;
   - qualification question when a real problem/project is already being discussed;
   - meeting/call handoff when the prospect indicates appropriate intent.
5. Explain the reason for the suggested action in concrete terms; do not use an
   arbitrary lead score.
6. Draft the exact message/reply from the real context.
7. Use `copywriting` for specificity, structure, and a low-pressure next step,
   then use `humanizer` for a bounded voice audit. If either skill cannot be
   loaded, apply the equivalent checks locally and report the fallback; never
   claim that a separate skill ran. Neither may add facts, experience,
   confidence, or relationship claims.
8. Create or update the `Interaction` row before asking for approval with the
   Prospect ID, date/time, topic, correct interaction type, relevant thread or
   post URL, factual context, exact `Our Text`, `Status=pending_approval`, and
   the proposed next action. Re-read the row and verify the exact draft.
9. Show the exact persisted message and Interaction ID, then ask for approval.
   If declined, update the Interaction to `declined` or `skipped` and do not
   send it.
10. If approved, re-check the live thread/profile and persisted draft
    immediately before sending, submit through the visible UI, and verify the
    result. Update the Interaction and Prospect only after the result is known,
    including `External Action URL` when available.
    If the result is ambiguous, mark the Interaction `pending_verification` and
    do not retry automatically. If the final Sheet update fails, report the
    verified UI result and unsynchronized state for stable-ID reconciliation.
11. Re-evaluate lead stage only when new commercial evidence exists.

## Qualification

A warm professional contact becomes a `lead` only when there is a plausible
commercial connection to a problem/service. Move to `qualified` when there is
specific evidence such as an active project/problem, relevant need, decision or
influence context, and a credible next step. Not every factor must be known, but
unknowns must remain unknown.

Use evidence text, not numeric scoring.

Examples of useful signals:

- the prospect explicitly describes an AI/software implementation problem;
- they are evaluating vendors/contractors/implementation help;
- they ask about the user's relevant experience or approach;
- they describe a project, deadline, integration, reliability, cost, data, or
  workflow problem where the user's service could reasonably fit;
- they invite a deeper discussion or meeting.

Likes, profile views, generic replies, and connection acceptance alone are not
qualification.

## Pipeline handoff

Create/update a `Pipeline` row only when a genuine commercial opportunity exists.
Record:

- the problem in the prospect's terms;
- service fit;
- concrete qualification evidence;
- current stage;
- next step/date;
- value only when grounded in an actual discussion.

Do not create fake deal value to make the dashboard look complete.

## Completion report

Report prospects reviewed, actions recommended, messages approved/verified,
relationship-stage changes, leads created/qualified, pipeline changes, and cases
where no action was the correct action.
