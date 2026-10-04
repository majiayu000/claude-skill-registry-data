---
name: clinic-status
version: 1.0.0
description: Produce a concise matter status update for the supervising attorney or case rounds, separating settled facts from open questions.
author: matrixx0070
tags: [status, clinic, case-rounds, deadlines, blockers, supervision]
capabilities: []
---

## When to use
Use this to give your supervising attorney or case rounds a fast, accurate read on a matter: what happened since last update, what is pending, what is blocking you, upcoming deadlines, and any decision you need from the attorney. Keep it tight enough to scan in under a minute.

**Not for:** launching research on a new issue (use clinic-research-start), transferring a matter to the next cohort (use clinic-semester-handoff), or assembling finished drafts for sign-off (use clinic-supervisor-review-queue). A status update is internal reporting — it is not advice to the client, and any decision that changes the matter's direction or reaches the client must come from or be approved by the supervising attorney (Model Rule 5.5); you report and recommend, you do not decide independently.

## Method
1. State the matter and the reporting window in one line.
2. Summarize what happened since the last update — actions taken, filings, client contact.
3. List what is pending and who owns each item.
4. Name blockers explicitly, including anything waiting on the attorney.
   **Decision point:** clearly separate confirmed facts from open questions; if a fact rests on unverified GenAI output or an unread citation, list it under open questions, not facts (ABA Op. 512 candor).
5. Surface upcoming deadlines with dates and the decisions you need from the supervising attorney.
6. Keep client-identifying detail to what the internal audience needs; never route the update through external or GenAI tools that expose client data (Rule 1.6).

## Example
> Matter C-07 (wage claim), week of Feb 10. Filed demand letter Feb 11; client confirmed receipt. Pending: employer response (due Feb 25). Blocker: need your call on whether to add a retaliation count. Open question: whether the 3-year or 4-year limitations period applies — case on point not yet read.

## Pitfalls
- Blending unverified assumptions into the facts section instead of the open-questions section.
- Burying a deadline or a decision the attorney must make inside prose.
- Reporting activity ("worked on the brief") instead of status and outcomes.
- Sending the update through a channel or GenAI tool that exposes client identifiers (Rule 1.6).

## Output format
```
MATTER: <id / short name>     WINDOW: <dates>
SINCE LAST UPDATE (facts): <confirmed actions/outcomes>
PENDING: <item | owner>
BLOCKERS: <item | waiting on>
OPEN QUESTIONS: <unconfirmed items needing verification>
UPCOMING DEADLINES: <date | event>
DECISIONS NEEDED FROM SUPERVISOR: <list>
```

## Reference
- ABA Formal Opinion 512: treat unverified GenAI output as an open question, never a fact (candor).
- Model Rules 1.4 (communication), 1.6 (confidentiality), 5.5 (supervision/UPL).
- Clinic norm: direction-setting and client-facing decisions require supervising-attorney approval.
