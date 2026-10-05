---
name: adverse-action-prep
description: |
  Use this skill when the user asks about FCRA adverse action procedures — what to do when a background check (MVR, criminal, drug test) returns information that may lead to denying employment or terminating a CDL driver. Covers the 5-business-day pre-adverse-action notice, FCRA Summary of Rights, final adverse action notice, state-specific add-ons (CA, NY, etc.), and how to handle disputes. Cite 15 USC § 1681 (FCRA) and 49 CFR 391.
---

# FCRA Adverse Action — 15 USC § 1681b(b)(3)

When a consumer report (MVR, criminal background, drug test verified result, PSP, Clearinghouse) returns information that may cause an adverse action (refusal to hire, termination, suspension), federal law requires a specific 2-step notice + waiting period process.

## What counts as "adverse action"

- Refusal to hire
- Termination
- Suspension from CMV duty
- Failure to renew
- Demotion to non-driving role
- Any other "denial of employment" based on the report

If the action is based ON the consumer report (even partially), FCRA applies.

## Step 1: Pre-adverse action notice (BEFORE you take action)

Send the driver:

1. **A copy of the consumer report**
2. **The FCRA Summary of Rights** (the standard CFPB-published form)
3. **A clear statement** that you may take adverse action based on the report
4. **Your contact information** for disputes

**Wait at least 5 business days** before taking adverse action. (Some states require longer — see state additions below.)

This 5-day window gives the driver time to:
- Review the report
- Dispute inaccuracies directly with the CRA (Checkr, etc.)
- Provide context (e.g., "that DUI was 20 years ago and I was rehabilitated")
- Provide updated documentation

## Step 2: Final adverse action notice (after the wait period)

If you decide to proceed:

1. **Notify the driver in writing** of the adverse action
2. Include:
   - Name, address, phone of the CRA that provided the report
   - Statement that the CRA didn't make the decision (you did)
   - Statement of the driver's right to a free copy of their report within 60 days
   - Statement of the driver's right to dispute the report's accuracy with the CRA
3. **Document everything** in your DQF + termination file

## What goes in your records

For each adverse action, retain:

- Copy of the report that triggered the action
- Pre-adverse-action notice with date sent
- Driver's response (if any)
- Final adverse-action notice with date sent
- Proof of delivery (email read receipt, certified mail, etc.)
- Internal decision memo explaining how you reached the decision

Retention: at least 2 years (FCRA recommends 5). Treat as part of the driver's terminated employment file.

## State-specific add-ons

| State | Additional requirement |
|---|---|
| **California** (Investigative Consumer Reporting Agencies Act) | Detailed notices + driver's right to receive copies; specific format required |
| **New York** (Article 23-A) | Special procedures for criminal record-based adverse actions; consider rehabilitation |
| **Massachusetts** | "Ban the Box" — limits on when criminal records can be considered |
| **Illinois** (Job Opportunities for Qualified Applicants Act) | Restricts consideration of criminal history pre-offer |
| **Washington** | Sealed/expunged convictions can't be considered |
| **Maryland** | Disclosure requirements at offer stage |
| **Connecticut** | Time limits on consideration of criminal records |
| **Many cities** (Seattle, NYC, San Francisco, etc.) | Local "Fair Chance" / ban-the-box rules |

Always check your state + local rules. A federal-compliant adverse-action process can still violate state law.

## What if the driver disputes?

A driver who reads the pre-adverse notice and disputes can:

1. Contact the CRA (e.g., Checkr) directly
2. The CRA must reinvestigate within 30 days (typically faster)
3. If the CRA confirms the report is wrong, they issue a corrected report
4. The driver should re-share the corrected report with you
5. You re-evaluate based on the corrected report

You should pause adverse action pending dispute resolution if the dispute appears credible. Talk to your attorney if the dispute is substantive.

## Drug test specifics (49 CFR 40 Subpart G + R)

For drug test results specifically:

- The MRO (Medical Review Officer) talks to the driver before issuing a verified positive
- Driver has 72 hours to request a split-specimen test (Bottle B from the same sample)
- The MRO's verified result is what triggers consequences, NOT the lab's raw result

A verified positive is NOT subject to the standard FCRA adverse-action process — it's covered by DOT's separate D&A regulations. The driver is "prohibited" via Clearinghouse and cannot operate until SAP + RTD complete.

## Common adverse-action mistakes

1. **Acting immediately on a "consider" result without pre-adverse notice.** That's a $1,500+ statutory damages per claim under FCRA.
2. **Not sending the Summary of Rights** with the pre-adverse notice.
3. **Sending pre-adverse + final the same day.** The 5-day wait is mandatory.
4. **Mixing FCRA process with state-specific add-ons.** California, NY, etc. have additional requirements.
5. **Not preserving the original report** the driver received.

## Practical timeline (with X3 + Checkr)

```
Day 0  - Checkr "consider" status received via vendor-result-webhook
Day 0  - send-compliance-notification fires with severity=warning
Day 1  - Safety manager reviews report in app.x3fleetsafety.com/background-checks.html
Day 1  - Decision: pre-adverse action notice sent (using adverseActionPrepEmail template)
Day 2-7 - Driver can dispute via Checkr's portal
Day 8  - If no dispute resolution OR confirmed adverse → Final adverse-action notice
Day 8+  - Driver removed from active fleet
```

## Where this fits in X3

X3's `vendor-result-webhook` flags `report.completed` events with status=consider as `bg_check_consider` event. The `send-compliance-notification` Edge Function fires the `adverseActionPrepEmail` template to the safety manager with the FCRA timeline. The notification_routing helper resolves this event to email (it's a 5-day workflow, not 1-day urgent).

The `_shared/email_templates.ts` `adverseActionPrepEmail` template includes:
- The 5-day timeline reminder
- Link to the driver's record
- A note that X3 has Summary of Rights + sample pre-adverse-action letter templates
- Joshua's contact info for ad-hoc questions


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=adverse-action-prep

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
