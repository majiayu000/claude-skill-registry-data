---
name: platform-support-escalation
description: Build strong platform support cases for DSP and ad platform issues, with reproduction steps, entity IDs, screenshots, report exports, business impact, desired outcome, escalation path, follow-up cadence, and privacy-safe evidence. Use when a case needs Google, Amazon, StackAdapt, TTD, Meta, TikTok, Microsoft, publisher, or verification vendor support.
---

# Platform support escalation

Weak support cases waste days: "campaign not spending", "creative rejected", "report wrong".
Strong cases prove scope, reproduce the issue, quantify impact, and ask for a specific outcome.
This skill helps programmatic operators send support cases that platform teams can act on.

Use this when the issue cannot be resolved from the platform playbook, a partner has to check
their side, or the team needs a clean record of what was asked and when.

## When to use this skill

- A deal, line item, creative, report, tag, API, billing, or access issue needs platform support.
- The team needs to escalate from a basic support queue to a rep, partner manager, seller, or
  technical support path.
- A support case has stalled and needs a sharper evidence package.
- A client asks for the status of an issue that depends on a platform or vendor response.

## Support case package

Every case should include:

| Field | Requirement |
| --- | --- |
| Platform and account | Include account, advertiser, partner, seat, or manager IDs where available |
| Entity scope | Campaign, order, line item, ad group, creative, deal, pixel, report, or API request IDs |
| Symptom | What is wrong, when it started, and whether it is ongoing |
| Reproduction steps | Exact clicks, report settings, API request, or export path |
| Evidence | Screenshots, exports, logs, result files, HAR files when safe, and timestamps |
| Business impact | Dollars at risk, launch delay, delivery shortfall, conversion loss, or client deadline |
| What changed recently | Bulk upload, creative swap, tag change, budget edit, audience edit, platform release |
| Ask | The specific action requested from support |
| Deadline | When the answer is needed and why |
| Privacy check | No secrets, credentials, raw user PII, or client-confidential data beyond what is needed |

## Core process

1. **Confirm it is support-worthy.** Run the platform troubleshooting skill first. If the desk
   can fix the issue internally, fix it internally. Escalate when the cause sits with the
   platform, a seller, a vendor, an API service, an approval queue, or gated account data.
2. **Name the binding symptom.** Do not send a case with five possible theories. State the
   observed failure: "Deal ID 987 delivered normally until July 2 at 14:00 PT, then dropped to
   zero while the parent campaign and backup open-exchange line continued spending."
3. **Prove scope.** Show whether the issue affects one entity, one campaign, one advertiser,
   one region, one format, or the whole account. Scope is what tells support where to look.
4. **Attach reproducible evidence.** Include report settings, filters, dates, time zone,
   screenshots, exports, and request IDs. If the issue is API-related, include endpoint,
   request ID, response code, and the smallest safe payload that reproduces it.
5. **Quantify business impact.** Convert the issue into a risk: dollars not spent, dollars
   overspent, impressions short, conversions missing, launch delay, SLA breach, or brand risk.
6. **Ask for a specific outcome.** Examples: confirm whether the deal is paused seller-side,
   clear a creative review queue, explain a reporting discrepancy, map a conversion, raise a
   quota, or confirm a platform incident.
7. **Set follow-up cadence.** Track case ID, owner, last response, next follow-up time, and
   escalation owner in the ops control center.

## Escalation ladder

| State | Action |
| --- | --- |
| New case | Submit evidence package through the normal support path |
| No acknowledgment inside SLA | Follow up with case ID and business impact |
| No useful response | Escalate to rep, partner manager, platform account team, or vendor contact |
| Active launch, spend, or brand risk | Page the desk lead and client owner after containment |
| Repeated failure | Add to incident postmortem or platform issue log |

Use `approval-and-escalation-governance` for who owns the escalation decision and
`change-management-and-incident-response` if the issue is an active incident.

## Message template

```text
Subject: [Platform] [Advertiser] [Issue] - action needed by [date/time/time zone]

Issue:
Observed impact:
Account and entity IDs:
Started:
Current state:
Reproduction steps:
Evidence attached:
Recent changes:
Business impact:
Requested action:
Deadline:
Internal owner:
```

## Privacy and security guardrails

- Do not share credentials, refresh tokens, API secrets, or raw authentication headers.
- Redact user-level identifiers unless the platform explicitly requires a hashed or test value.
- Share the smallest export that proves the issue.
- Keep support evidence in the approved client or agency storage location, not in personal
  downloads.
- If a support case references regulated data or a legal risk, route to privacy or legal before
  sending.

## Common pitfalls

- Asking support to "look into it" without a specific outcome.
- Sending screenshots without IDs, dates, filters, or time zone.
- Hiding the business impact. A platform team cannot prioritize a case it cannot size.
- Escalating a theory instead of a symptom. Support can test a symptom; theories waste cycles.
- Letting a case stall outside the ops board. Every waiting case needs a follow-up clock.

## Related artifacts

- `templates/ops/platform-escalation-template.md`
- `programmatic-ops-control-center`
- `change-management-and-incident-response`
- `approval-and-escalation-governance`
