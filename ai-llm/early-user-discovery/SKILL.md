---
name: early-user-discovery
type: Skill
title: Early user discovery and founder feedback trials
description: "Early-user discovery and feedback trials. Use when reviewing unfamiliar AI Matrx accounts, classifying owner relationships, recommending trial plans, or running approved outreach and reply checks."
tags: [users, feedback, outreach, administration]
timestamp: 2026-09-30
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/early-user-discovery/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Early user discovery

**Human activity and an external relationship are separate facts.** OAuth, a plausible name,
nonzero spend, no admin flag and a solo organization never establish that someone is outside
Arman's circle. Tahir was misclassified because the analyst skipped organization connections.

## Resolve relationships before ranking

1. Read the owner's confirmed category, notes, contact history and restrictions first.
   Owner-confirmed employee, former employee, friend/family, test or real-user facts override guesses.
2. Check **all organization memberships**, roles, inviter and invitation history. Compare by org
   ID against the owner's organizations, not just company email domains or org names. Do not
   narrow this check to the currently selected organization.
3. Resolve the existing `crm.party` through `claimed_by`, then check CRM employment/affiliations
   and available HR links. Former membership or employment still explains a known connection.
4. Record the evidence and its source. Shared organization means **connected / needs review**,
   not automatically employee. An unread or empty relationship source means **unknown**;
   do not equate a failed lookup with no relationship. Never merge accounts from names alone.
5. Keep known people eligible for usage analysis while excluding them from automatic **external**
   discovery and unsolicited trial invitations. No bulk outreach from inferred categories.

## Date and usage window

**This program starts 2026-06-01T00:00:00Z**, by Arman's September 30 instruction.
Ignore earlier activity for selection, growth and offers. An old signup can qualify through
later activity; an old signup or pre-June conversation alone cannot qualify. Preserve old
relationship facts for exclusion. Label every request and cost window. Never call account
counts people counts; deduplicate only from verified identity evidence.

Use the last seven days and the preceding seven days for changes, recent signups for discovery,
and at least two separate active days for a sustained-use signal. Human requests, child-agent
requests and workflow executions are different counts. Acquisition and page visits are evidence
only when actually captured; do not invent them from a conversation title.

## Recommend an allowance

Read live `billing.plan` and `billing.plan_limit`, not marketing constants. Compare usage
inside actual billing periods, including AI points, storage and resource limits. All-time
cost alone cannot prove a monthly tier. Distinguish measured plan fit from a provisional offer.
A three-month **paid-tier trial** is not three months of an already free plan. Do not promise
unlimited spend, guaranteed custom work, or silently grant entitlements. Owner approval names
recipient, plan, duration and script.

## Approved personal outreach only

- Read current owner notes and prior contact first. Preserve blocks and contact holds.
  Owner-reported contact is not permission to infer delivery IDs or contact channel.
- Draft email and DM separately. Begin in Arman's requested voice when appropriate:
  “Hi [first name]. This is Arman, not one of the agents. lol. I'm the founder of AI Matrx
  and the lead engineer.” Attribute it to him only through his approved sending identity.
- Personalize from coarse **verified feature/page activity**: “I noticed you tried our workspace.”
  Never quote private prompts, file contents, conversation titles, emails, personal topics or
  precise tracking timestamps. If page evidence is absent, use a general welcome.
- **Approval binds exact recipient, channel, sender, offer and final text.** Any edit revokes
  it. A template approval alone is not approval for every future recipient or personalization.
- Use existing Gmail and DM paths only after verifying the sending identity and replay guarantees. Respect canonical suppression,
  restrictions and stop requests. Store provider message/thread IDs and stable replay keys.
  After an ambiguous send, reconcile sent records before retrying; do not send blindly.
- No invitation to blocked, opted-out or known-internal accounts. A reply stops follow-ups.
  Do not schedule a reminder merely because the send returned successfully.
- Read only relevant reply threads, preserve inbound cursors and report new replies with
  their source link, brief meaning and next action. Do not change the approved offer yourself.

## Daily run

Use one cheap execution model. Claim the day once, load owner facts, reconcile relationships,
collect bounded new-signup/usage evidence and draft only new candidates. Saved drafts reserve
the account; they are not approvals. Read replies only from verified existing outreach threads.
Sending remains a separate approved action through the existing app, with a recorded receipt.
Do not treat draft JSON as an executable queue or claim an unattended sender is implemented. Keep
quiet when nothing actionable changes. Report new qualified candidates, replies, failed sends
and uncertain delivery. Never claim a scheduled task is active until the scheduler confirms it.
Schedule activation needs the owner's approval of the script and proposed time.

Proof scenarios and outcomes: [evals.md](evals.md).
