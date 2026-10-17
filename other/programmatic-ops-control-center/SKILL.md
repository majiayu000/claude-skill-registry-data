---
name: programmatic-ops-control-center
description: Run the daily programmatic operations desk across campaigns, platforms, tickets, launches, incidents, creative review, access, billing flags, and client deadlines. Use when the user asks for an ops command center, daily queue, status board, launch readiness view, desk handoff, or a single operating rhythm for programmatic operations.
---

# Programmatic ops control center

Programmatic operations is not one task. It is a desk that must keep launches, live delivery,
creative, tracking, approvals, tickets, access, incidents, and billing evidence moving at the
same time. This skill gives the assistant a command-center routine for that work.

Use it to help operators see the whole desk without pretending the assistant owns the account.
The assistant reads, organizes, drafts, and recommends. A programmatic operator approves live
changes, client messages, and spend-affecting decisions.

## When to use this skill

- The user asks for a daily programmatic ops queue, command center, launch board, or status board.
- Multiple campaigns, platforms, or client requests are active and need prioritization.
- A launch, creative, tracking, or support issue is blocked and needs an owner and next action.
- A client or account lead asks "what is at risk today".
- A handoff is needed between traders, ad ops, measurement, analytics, and account leads.

## Quick reference

| Lane | What to check | Output |
| --- | --- | --- |
| Launches | Every campaign due to go live, gate status, missing evidence | Go, no-go, or blocked |
| Live delivery | Pacing, spend spikes, non-delivery, deal health | Owner and one proposed action |
| Measurement | Tag firing, key events, Floodlight, consent, pipeline freshness | Verified, degraded, or blocked |
| Creative | Assets in review, rejected assets, expiring assets, swaps | Queue status and blocker |
| Tickets | New asks, overdue asks, unclear asks, priority changes | Triaged queue |
| Approvals | Budget, bid, safety, taxonomy, access, client copy | Approver and due time |
| Incidents | Active Sev 1 or Sev 2, containment, comms, postmortem | Incident state |
| Close | Reconciliation, make-good, billing evidence, accruals | Month-end risk list |

## Core process

1. **Build the desk board.** Create one row per item that can block launch, delivery,
   reporting, billing, or the client deadline. Do not hide work in prose. Every row needs
   platform, advertiser, campaign or ticket ID, owner, due date, current state, blocker, next
   action, and evidence link.
2. **Classify each row.** Use four states only: `Green`, `Yellow`, `Red`, and `Waiting`.
   Green means on track with evidence. Yellow means at risk but still recoverable inside the
   SLA. Red means blocked, late, live-risking, or missing a required approval. Waiting means
   the next action sits with a named outside party.
3. **Prioritize by risk, not noise.** Handle live spend risk first, then launch blockers,
   then client deadlines, then tracking and data quality, then routine queue cleanup. A loud
   ticket does not outrank a spend spike or a launch without conversion verification.
4. **Assign one next action.** Each non-green row gets exactly one owner and one next action
   with a due time. If two teams are involved, name the current owner and the receiving owner.
5. **Route to the right skill.** Use `cross-platform-launch-qa` for launch blockers,
   `bulk-change-governance-and-rollback` for batch edits, `ops-ticket-intake-and-triage` for
   unclear asks, `creative-review-and-approval-queue` for asset issues,
   `platform-support-escalation` for platform cases, and `programmatic-month-end-close` for
   billing and reconciliation risk.
6. **Close the loop.** At the end of the desk sweep, produce three lists: launch decisions,
   live-risk decisions, and items waiting on someone else. Anything red needs a named owner,
   a time, and a decision path through `approval-and-escalation-governance`.

## Decision rules

- Red beats yellow. A small live risk with dollars moving outranks a large future nice-to-have.
- Do not optimize a campaign whose measurement is broken. Route it to measurement first.
- Do not launch a campaign with a missing conversion, tag, creative, consent, budget, or brand
  safety gate. A delayed launch is cheaper than a broken launch.
- Do not call a support case "blocked" without an evidence package and a specific ask.
- Do not mark a row green because someone promised to fix it. Green requires evidence.
- Every red row has one current owner. Shared ownership is how work gets missed.

## Status board template

```text
Programmatic ops control center
Date:
Desk owner:

| Status | Platform | Advertiser | Campaign/Ticket | Lane | Owner | Due | Blocker | Next action | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Red | DV360 | Example | LI 123 | Launch | trader | Today 2 PM | Floodlight not firing | Measurement engineer to retest purchase tag | link |
| Yellow | TTD | Example | Case 456 | Support | ops lead | Today EOD | Deal underdelivering | Send floor, bid, win rate, request seller check | link |
```

## Handoffs

- To `programmatic-ops-lead`: the full board and the red/yellow decision list.
- To `qa-scrutinizer`: any launch or client-facing artifact that needs independent hold power.
- To `measurement-and-tagging-engineer`: any conversion, tag, consent, or pipeline blocker.
- To `account-operations-specialist`: taxonomy, access, bulk edit, or platform setup work.
- To `client-communications-lead`: client-facing status once the facts are verified.

## Common pitfalls

- Treating the board as a status report instead of an operating tool. It must drive owners and
  next actions.
- Leaving `Waiting` rows without a follow-up time. Waiting still needs a clock.
- Marking launches green before the post-launch check. A launch is not complete until early
  delivery, spend, tags, and reporting are verified.
- Mixing client language with internal risk language. Keep the internal board direct, then hand
  verified client copy to the communications lead.

## Related skills and loops

- `ops-ticket-intake-and-triage`
- `cross-platform-launch-qa`
- `bulk-change-governance-and-rollback`
- `platform-support-escalation`
- `creative-review-and-approval-queue`
- `programmatic-month-end-close`
- `approval-and-escalation-governance`
- `ops-command-center-daily` loop
