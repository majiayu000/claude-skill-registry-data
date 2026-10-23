---
name: post-mortem-author
description: "Build-an-X workflow that produces a blameless post-mortem from an incident - captures the timeline (chronological event sequence with sources), root cause analysis (what + why, not who), impact (users / revenue / SLO debt), action items (with owners + due dates + measurable success criteria), and \"what went well\" (intentional). Per Google SRE: \"Blameless postmortems are a tenet of SRE culture.\" Use after every user-visible incident, not just severe ones."
---

# post-mortem-author

## Overview

Per [google-sre-postmortem][gsp]:

[gsp]: https://sre.google/sre-book/postmortem-culture/

> "A postmortem is **'a written record of an incident, its impact,
> the actions taken to mitigate or resolve it, the root cause(s),
> and the follow-up actions to prevent the incident from
> recurring.'**"

> "Blameless postmortems are a tenet of SRE culture."
> ([google-sre-postmortem][gsp])

> "Writing a postmortem is not punishment - it is a learning
> opportunity for the entire company." ([google-sre-postmortem][gsp])

The blameless framing is load-bearing. Per
[google-sre-postmortem][gsp], the document must "focus on
identifying the contributing causes of the incident without
indicting any individual or team for bad or inappropriate
behavior" - assuming "everyone involved in an incident had good
intentions and did the right thing with the information they
had."

## When to use

Per [google-sre-postmortem][gsp], common triggers include:

> "user-visible downtime, data loss, on-call interventions,
> extended resolution times, and monitoring failures."

Author a post-mortem after every such incident - not just sev-1.
Lower-severity incidents accumulate context that prevents the
sev-1.

## Step 1 - Author the document

Copy the full section skeleton from
[references/post-mortem-document-template.md](references/post-mortem-document-template.md)
and fill every section. The required sections, in order:

1. **Header** - status, severity, authors, dates, reviewers.
2. **Summary** - 2-3 sentences: what, who, how long, what was done.
3. **Impact** - users affected, revenue (deferred vs lost), SLO debt, reputational.
4. **Timeline** - chronological events with UTC timestamps and a source per row.
5. **Root cause** - what happened in detail, with the system as the subject, never a person.
6. **Contributing factors** - every condition that allowed the incident; list all, since incidents rarely have one cause.
7. **What went well** - the positives; per [google-sre-postmortem][gsp], post-mortems should call these out too.
8. **Action items** - the load-bearing section (Step 3).
9. **Lessons learned** and **Postmortem trigger** - what is known now, and which trigger criteria the incident met.

The worked example below fills this skeleton for a real SEV-2.

## Step 2 - Blameless review

Per [google-sre-postmortem][gsp]: "Postmortems are not punishment."

Reviewers should:

- **Reject blame language.** "Bob deployed without testing" → "The
  pre-deploy testing didn't cover the null-metadata case."
- **Focus on systems, not individuals.** "Why did Bob fix this
  fast?" → "What enabled fast diagnosis? (Sentry stack trace +
  the team's incident-response training.)"
- **Surface contributing factors openly.** Multiple factors usually
  contribute; document all.

## Step 3 - Action item discipline

Action items must have:

- **Owner** (one named person; not "the team").
- **Due date** (concrete; not "next sprint when we have time").
- **Priority** (P0/P1/P2/P3; ties to the action's importance).
- **Success criterion** (measurable; "X done" not "we'll think about X").

The action items are the post-mortem's value. Without them, the
document is paperwork.

## Step 4 - Approval + closure

The post-mortem isn't "done" until:

1. Reviewers (eng manager, SRE lead, Product) sign off.
2. Action items are added to the team's tracker (Jira / Linear /
   GitHub issues).
3. P1/P2 action items have a target completion before the next
   release.

The post-mortem is "closed" when all action items ship - typically
2-4 weeks. A 6-month-old open post-mortem is a process failure.

## Step 5 - Storage

```
docs/postmortems/
├── INC-1234-stripe-webhook-2026-05-04.md
├── INC-1235-cache-invalidation-2026-05-12.md
├── INC-summary-2026-Q2.md       ← rollup
└── README.md
```

Markdown + git. Quarterly rollup identifies patterns:

```markdown
## Q2 2026 incident summary

**Total incidents:** 12
**SEV-1:** 1
**SEV-2:** 6
**SEV-3:** 5

**Patterns:**
- 4 of 12 (33%) were "test gap" - the failing condition wasn't
  in the test suite. Action: invest in
  test-coverage-targeter
  + property-based testing.
- 3 of 12 (25%) involved canary metrics; 2 of those proceeded
  through canary gate. Action: review thresholds (per AI-2 from
  INC-1234).
- ...
```

## Worked example - INC-1234 Stripe webhook failure (SEV-2)

The skeleton from Step 1, filled for a real incident.

**Summary.** A v1.4.5 deploy introduced a null-metadata crash in the Stripe
webhook handler; ~12,400 customers (4.3% of MAU) hit failed checkout
completions for 23 minutes until rollback.

**Impact.** ~$140,000 in delayed (not lost) orders; 32% of the monthly
availability budget burned; 47 support tickets.

**Timeline (excerpt).**

| Time (UTC) | Event | Source |
|------------|-------|--------|
| 14:00 | Deploy of v1.4.5 to canary (5% traffic) | CD pipeline log |
| 14:23 | First Sentry alert: NullPointerException at WebhookHandler:42 | Sentry |
| 14:30 | Canary window ends within thresholds; promoted to 100% | CD pipeline |
| 14:42 | PagerDuty SLO burn-rate alert; incident declared SEV-2 | PagerDuty |
| 14:58 | Rollback complete; error rate returning to baseline | Datadog |

**Root cause (what, not who).** The v1.4.5 handler added a path for Stripe's
`payment_intent.partially_funded` event that called
`payment.metadata.get("internal_id")`; for ~3% of events `metadata` was null,
the exception was uncaught, the handler returned 500, and Stripe stopped
retrying, so fulfillment never triggered. The canary stage saw the error rate
rise (0.4% vs 0.3% baseline) but stayed under the 1.5x rollback threshold, so
`prod-canary-validator` returned PROCEED with WARNING and the gate was acked.

**Contributing factors.** (1) test gap - no unit test for the null-metadata
case; (2) canary threshold too lenient for a low baseline; (3) staging carries
almost no Stripe webhook traffic, so the new event type was never exercised
pre-deploy.

**Action items.**

| ID | Action | Owner | Priority | Due | Success criterion |
|----|--------|-------|----------|-----|-------------------|
| AI-1 | Unit test for `partially_funded` with null metadata | Bob | P1 | 2 days | Test in `WebhookHandlerTest.kt` fails against the bug, passes after |
| AI-2 | Tighten canary error-rate threshold 1.5x -> 1.3x | SRE | P2 | 1 sprint | `canary-thresholds.yml` updated; one normal canary passes |
| AI-3 | Staging fixture covering all Stripe event types | Bob | P2 | 1 sprint | Staging "events by type" metric shows all types > 0 |

**What went well.** Sentry caught the regression at 14:23, well before the
PagerDuty page; rollback finished in 7 minutes, inside RTO. Diagnosis came from
the Sentry stack trace alone, with no production debugging.

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Blame language                                                         | Defeats the blameless principle; team stops authoring post-mortems honestly. | Per Google SRE: focus on contributing causes, not individuals (Step 2). |
| Action items without owner / due date                                  | Nobody acts; same incident recurs.                                       | All four fields required (Step 3). |
| Skipping post-mortems for "small" incidents                            | Lower-severity context that prevents big incidents is missed.            | Author per [google-sre-postmortem][gsp] trigger criteria (Step 1). |
| Post-mortem stored in private docs                                     | Org learning capped at the team.                                         | Public to org (per Google SRE pattern). |
| One-shot post-mortem with no follow-up                                  | "Closed" but action items stale; recurrence likely.                      | Track action items in tracker (Step 4); post-mortem closed only when all done. |
| Post-mortem authored 2+ weeks after incident                           | Memory faded; details lost.                                              | Author within 5 business days. |

## Limitations

- **Honesty depends on culture.** A team that fears blame will
  produce sanitized post-mortems. Leadership must reinforce
  blamelessness in word and action.
- **Post-mortems don't prevent the next incident.** They prevent
  the same class of incident. Pair with proactive practices
  (chaos testing, threat modeling).
- **Time investment.** A SEV-2 post-mortem typically takes 4-8
  hours to author + 2-4 hours of review. Budget accordingly.

## References

- [gsp][gsp] - Google SRE blameless post-mortem definition,
  triggers, blamelessness principle, learning-opportunity framing.
- `prod-canary-validator` - sibling: canary verdict; post-mortems often surface threshold
  tuning needs.
