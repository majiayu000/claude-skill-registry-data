---
name: regl-comments
version: 1.0.0
description: Track open comment periods and draft a substantive, on-the-record comment that argues your position within the docket's rules and deadline.
author: matrixx0070
tags: [regulatory, legal, public-comment, rulemaking, deadlines, advocacy]
capabilities: []
---

## When to use

Use this when a proposed rule (NPRM) has an open comment window and you want to shape the outcome or preserve arguments for later challenge. Reach for it to track a comment clock, decide whether to file, and draft the comment itself.

**Not for:** analyzing what the rule changes (use regl-policy-diff), monitoring for new rules (use regl-reg-feed-watcher), or rewriting your own internal policy (use regl-policy-redraft). Any comment that stakes out a legal position, or that you may later cite in litigation, must be reviewed by an attorney before filing.

## Method

1. Log the deadline the instant a period opens: docket/RIN, opening date, comment-close date, and submission channel (regulations.gov docket, agency portal, mail). Set reminders at close-minus-14 and close-minus-3.
2. Decide whether to file: is there a concrete, evidenced impact worth putting on the record? A vague objection weakens the docket; a specific, data-backed one builds it.
3. Build the argument from the diff: cite the exact provision, the operational or economic burden, and a proposed alternative. Agencies must respond to substantive comments — specificity is leverage.
4. Follow docket format rules: address the RIN, respect length/attachment limits, mark any confidential business information correctly, and keep it on-topic.
5. **Decision point:** if the argument depends on a legal interpretation or preserves a challenge ground, route to attorney review before submission — comments are public and permanent.
6. Submit before the deadline, capture the confirmation/comment ID, and log it.

## Example

> NPRM RIN 3170-AB00, comment closes 2026-08-29, portal regulations.gov. Decision: file — §4 deletion-attestation timeline is unworkable for legacy systems. Argument: cite §4(b), show 90-day migration reality with cost data, propose 180-day phase-in. Attorney reviewed (preserves arbitrary-and-capricious ground). Submitted 2026-08-22, comment ID CFPB-2026-0012-0431.

## Pitfalls

- Missing the close date — there is no late lane on the record.
- Filing generic opposition an agency can dismiss without response.
- Leaking confidential business data into a public comment.
- Filing a legal-argument comment without counsel, foreclosing or weakening a later challenge.

## Output format

```
COMMENT TRACKER — <docket/RIN>
Opened: <date> | Closes: <date> | Channel: <portal/URL>
Decision to file: <yes/no — rationale>
---
COMMENT DRAFT
Re: <RIN>, <rule title>
Position: <support/oppose/modify §X>
Argument: <provision cite → burden + evidence → proposed alternative>
CBI marked: <yes/no> | Attorney reviewed: <yes/no>
Submitted: <date> | Comment ID: <id>
```

## Reference

**Rulemaking lifecycle:** comments only matter at the NPRM stage; once a final rule publishes, the window is closed and the vehicle becomes a petition or legal challenge, not a comment.

**Comment-period mechanics:** windows run ~30–60 days from Federal Register publication, occasionally extended on request; agencies must consider and respond to significant comments in the final rule, and an unaddressed substantive comment can support a later arbitrary-and-capricious challenge. Comments are public and permanent.

**Policy-diff method:** your strongest comments come straight from a regl-policy-diff delta — cite the specific provision and the concrete burden. Attorney-escalation gate: legal-theory or challenge-preserving comments require counsel sign-off before filing.
