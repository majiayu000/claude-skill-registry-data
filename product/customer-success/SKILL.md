---
name: customer-success
description: Use when setting up or reviewing post-sale support (ticket triage, priorities, SLAs, escalation) or account health (churn signals, renewal risk). Picks up where business/sales-support stops.
---

# customer-success

Business layer (`business/README.md`). `business/sales-support` covers the path to a closed deal; this
block covers what happens to the customer after — support tickets and account health — where the two
recurring engineering-adjacent failures are treating every ticket as equally urgent, and discovering
churn risk only when the customer already has one foot out the door.

## When
Setting up or reviewing a support/ticketing process (priority levels, SLAs, escalation), or an ongoing
customer-health/renewal-risk process (health scores, QBRs, proactive outreach).

## Steps

### 1. Ticket triage: not every ticket is equally urgent
1. **Every ticket gets a priority level on arrival**, not "whoever picks it up next decides." A small,
   fixed set of levels (e.g. critical/high/medium/low) each tied to real criteria — is production down
   for the customer, is there a workaround, how many users affected — beats an ad hoc judgement call
   made fresh every time.
2. **Each priority level carries a stated response and resolution target**, known to both the team and
   the customer. A critical ticket with no faster commitment than a low-priority one isn't actually
   being prioritised, whatever the label says.
3. **Escalation is automatic on breach, not manual on notice.** A ticket that crosses its SLA clock
   (unassigned past its target, or unresolved past it) escalates to a named owner or team by rule,
   rather than depending on someone happening to notice the queue is backing up.
4. **Route by who's asking, not only by what's asked**: a ticket from an account already flagged at
   risk (see §2) deserves faster handling than the priority label alone would give it, because a slow
   response on an at-risk account compounds the risk it's already carrying.

### 2. Reduce ticket volume before triaging it better
1. **The cheapest ticket is the one that never gets filed.** A self-serve knowledge base covering the
   handful of issues that generate the most tickets reduces inbound volume more reliably than triaging
   the same recurring issue faster every time it arrives.
2. **A ticket resolved three times this month for the same root cause is a signal to fix the product or
   the documentation, not to keep resolving it well.** Recurring tickets are a backlog input, not just
   support workload — feed them back to whoever owns the product/docs.

### 3. Account health: don't wait for the renewal conversation
1. **A health score is a combination signal, not one number picked because it's easy to query**: product
   usage/adoption, support ticket volume and CSAT, responsiveness to outreach and QBR attendance,
   payment/renewal proximity. An account that's technically "using the product" but has stopped
   responding to any human contact is a churn risk a pure usage metric alone will miss.
2. **Low feature adoption and low seat utilisation are early-warning signs, not neutral facts.** An
   account only using a sliver of what it's paying for is at measurably higher churn risk — worth a
   proactive check-in, not a wait-and-see.
3. **A quarterly business review that's the *first* time low adoption gets raised is too late.** Health
   score thresholds should trigger proactive outreach continuously, so the QBR is a scheduled checkpoint
   on an already-tracked relationship, not the moment risk gets discovered.
4. **"Gone dark" (no response to outreach, no-shows on scheduled calls) is itself a churn signal**,
   independent of any usage number — silence is data, not a null result to ignore.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: a stated priority
scheme with response/resolution targets per level, escalation that fires automatically on SLA breach, a
combined health-score signal tracked continuously rather than reconstructed at renewal time, and
recurring tickets fed back to product/docs rather than just being resolved again.

## Guardrails
- Never let a critical-priority label exist with no faster commitment behind it than a low-priority one
  — an unbacked priority scheme is worse than none, because it creates a false expectation.
- Never treat "the account is still logging in" as proof an account is healthy — check adoption depth
  and responsiveness, not just presence.
- Never wait for the renewal conversation to have the first conversation about risk.
- This block has no dedicated in-house support/customer-success expertise behind it yet: a solid set of
  structural defaults, not proven doctrine, to be confronted with a real support/CS operation.

## Origin
Assembled from public sources, written without internal customer-success expertise. Ticket triage,
priority levels and SLA-driven automatic escalation: published help-desk/ticket-triage practice.
Self-serve knowledge base as volume reduction, and recurring-ticket-as-product-signal: the same public
practice, generalised. Customer health scores (multi-signal composition, adoption/seat-utilisation as
early churn signals, proactive-outreach-before-QBR, "gone dark" as its own signal): published
SaaS-customer-success guidance on health scoring and churn prediction. Stamped 2026-08-11.
