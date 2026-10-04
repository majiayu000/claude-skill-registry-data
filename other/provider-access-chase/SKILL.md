---
name: provider-access-chase
description: "Follow-up sweep for pending third-party provider access campaigns. Use when the recurring 30-minute Provider Access Launch dispatcher wakes, or for a manual status check of due email threads, developer portals, support cases, or review deadlines."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/provider-access-chase/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Chase Provider Access

This skill is the follow-through loop. A recurring runner may wake every 30 minutes, but it acts only
on due campaigns and stays quiet only when nothing changed **and nothing actionable remains**.

## Durable scheduled prompt

```text
Use $provider-access-chase on the AI Matrx Provider Access Launch project. Select only planned or
active campaigns whose next-check/due time has arrived. Check their recorded email thread,
developer portal, or support case using existing authenticated access. Record consequential changes
in the task and CRM, set the next phase/action/check, and verify any approval through the canonical
integration path. Arman's 2026-08-29 standing authorization covers free, reversible,
least-privilege accounts, ordinary signup terms, development apps, keys, service accounts,
DCR/OAuth/MCP grants, Vault custody, secret rotation, service restarts, and safe proofs. Execute
those actions directly through `$provider-access-submit`; never ask him to reply yes again. Alert
Arman only for approval, rejection, deadline, material scope change, or an uncovered consequential
boundary: paid commitment, negotiated contract, regulated/compliance or legal-identity attestation,
customer data, production DNS/traffic, external communication, public publication, destructive
operation, or provider-enforced human ceremony. If nothing changed and no action is open, report only
a compact no-change receipt and do not notify repeatedly. If any earlier provider request or other
action remains unresolved, every run must lead with `OPEN ACTION — waiting on AI Matrx:` and restate
the exact deliverable, owner, blocker, and next move. “No new provider event” is only a delta and must
never be translated into “no action required,” “waiting on the provider,” or completion.
```

Use this prompt for the initial Codex scheduled task. Any later in-product scheduler must invoke a
declared Mandate by `mandate_key`; it may not take a hardcoded agent UUID or silently fall back.

## Selection and idempotency

1. Read `common-docs/systems/integrations/provider-access/FEATURE.md` when available.
2. Open the live `Provider Access Launch` Project.
3. Select only planned/active tasks in a pending phase with a due `Next check` or due date. Never check the
   whole catalog simply because the dispatcher woke.
4. Set a selected task `active` only while checking it; return it to `planned` when it is waiting on
   a provider or owner with a future due check.
5. Build a check identity from `campaign_key + source identity + newest provider event/message ID`.
   Do not write a duplicate CRM interaction or repeat an alert for the same event.
6. Use the exact recorded email thread, portal application/case ID, or support ticket. Do not search
   a whole inbox and infer campaign state from an unrelated message.
7. Establish the full current state before describing the newest delta. Carry every unresolved action
   forward from the task, CRM, and last provider event until completion is verified. A newer no-change
   check never clears an older Action Required event.

## Check order

1. Existing provider email thread or labelled provider mailbox state.
2. Developer/reviewer portal status.
3. Support ticket or escalation route when the promised window has elapsed.
4. Canonical AI Matrx connection state when an approval may have landed.

Exhaust authenticated browser sessions, provider CLI/API access, Vault credentials, and service
identities before asking Arman to log in. A provider-enforced challenge is an owner blocker; a stale
agent login that can be repaired through the normal account flow is not.

## On a new event

- Record the exact provider event, timestamp, source identity, case/thread/message ID, and links.
- Create/update the consequential `crm.interaction`; keep secrets out of the body.
- Update task `Phase`, exact next action, and next check in the same pass.
- Approval: verify the real product connection/operation before marking complete.
- Request for evidence/clarification: prepare the smallest factual response and required assets.
- Rejection: preserve the reason, compare it with submitted scopes/assets, and prepare a repair plan.
- Deadline: escalate immediately with the exact action and deadline.
- Material new scope/legal/compliance request: set `blocked_owner`; do not accept or attest.

Routine free/reversible setup proceeds under the standing authorization and must not wait for a new
confirmation. A draft response is not a sent response, and representational communication or any
other action outside the standing authorization still requires the recorded owner decision.

## Cadence

Set the next check from the provider's stated timing and current conversation intensity:

- active same-day reviewer exchange: 1 hour unless the provider states otherwise;
- ordinary pending review: daily during business days;
- stated review window: at the end of that window, then use the documented escalation route;
- owner blocker: immediately after the owner action, plus a reasonable reminder;
- completed/cancelled/dismissed: no further check.

The 30-minute runner is a dispatcher, not a mandate to poll every provider twice an hour.

## Output receipt

Always leave a compact run receipt. Its first line must be the terminal current state:

- unresolved provider/agent/owner action: `OPEN ACTION — waiting on <owner>: <exact action>`;
- genuinely provider-pending with no action owed by AI Matrx or Arman: `WAITING ON PROVIDER`;
- complete and verified: `COMPLETE`.

Never emit `NO ACTION REQUIRED`, `UNCHANGED`, or a quiet/no-notify result while an unresolved action
exists. “No new provider event” belongs only in the delta field below the current-state line.

```text
Current state:
Run time:
Due campaigns checked:
New provider events:
Unresolved actions carried forward:
Tasks changed:
CRM interactions added/updated:
Approvals verified:
Owner alerts:
Next scheduled check:
No-change event identities suppressed:
```

## Example requests

- “Use `$provider-access-chase` for every campaign due now.”
- “Use `$provider-access-chase` on the Google verification thread and portal.”
- “Use `$provider-access-chase` to run a no-change/idempotency test without sending anything.”
