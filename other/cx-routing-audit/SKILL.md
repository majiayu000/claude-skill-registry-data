---
name: cx-routing-audit
description: Use to find where support routing is failing — misrouted contacts, reassignment chains, unassigned work, and queues nobody owns. Trigger for "why do tickets bounce between teams", "are we routing correctly", "tickets sitting unassigned", "how many tickets get reassigned", ticket ping-pong, or reviewing routing rules and queue design.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Routing audit

Routing failures are invisible in every headline CX metric and they are expensive in
all of them. A misrouted contact adds handle time to two people, adds wait time for the
customer, and usually adds a repeat contact — but it shows up as slightly worse
averages everywhere rather than as a routing problem anywhere.

The audit makes it visible and, importantly, separates the failures that are worth
fixing from the ones that are normal.

## Reassignment is not automatically a failure

Distinguish these before counting anything, because lumping them together produces a
scary number that nobody can act on:

- **Designed escalation** — tier 1 to tier 2, or to a specialist queue. Working as
  intended. Expected volume, and if it is *lower* than expected that is its own finding.
- **Load balancing** — moved because someone was unavailable. Neutral.
- **Misroute** — arrived somewhere that could never have handled it. A failure of the
  routing rule.
- **Ping-pong** — three or more hops, or a return to a queue that already had it. Always
  a failure, and the customer experience is far worse than the hop count suggests.

The metric worth tracking is **misroute rate** and **ping-pong rate**, not raw
reassignment rate.

## What to measure

**Hop count distribution.** Most contacts should be zero or one hop. Report the share at
0, 1, 2, and 3+. The 3+ tail is small and carries a wildly disproportionate share of
complaints — check it against complaint and escalation records and quantify the link.

**Time lost per hop.** Wall-clock between arrival at a queue and reassignment out of it.
This is dead time from the customer's point of view, and totalling it across the window
converts a routing problem into a number leadership acts on.

**Misroute origin.** For misroutes, where did they come from? Almost always one of:

- a routing rule matching on the wrong signal
- an intake form whose categories do not match the queues
- a customer-facing menu whose labels do not mean what customers think
- a channel with no routing at all, defaulting everything to one queue

Group misroutes by first queue and by contact driver; the clusters name the broken rule.

**Unassigned open work.** Contacts sitting in a queue with no owner. Cluster them by
queue, tag, time of day and channel. This is usually a rule gap rather than a people
problem — a category with no assignment rule, or a queue whose only member left.

**Queues nobody owns.** Enumerate queues and check each has a current owner, current
members, and recent activity. Dormant queues that still receive traffic are a reliable
source of abandoned contacts, and they are invisible until someone lists them.

**First-time-right rate**, per contact driver: the share handled entirely by the queue
that first received it. More useful than a global routing accuracy figure because it
points at the specific rules to change.

## The signal people miss: routing that looks fine because it never fires

A queue with zero misroutes may have perfect rules, or may be receiving nothing because
an upstream rule is swallowing its traffic. Check queue volumes against expectation:

- A queue whose volume dropped sharply is usually an upstream rule change, not a demand
  change.
- A catch-all queue growing steadily means specific rules are decaying.
- **Catch-all volume as a share of total is the single best health metric for a routing
  configuration**, and it is rarely tracked. Rising catch-all share means the rules are
  falling behind the product.

## Traps

- **Reassignment data quality varies enormously.** Some helpdesks record every
  assignment change, some only the current assignee, some record automation as a
  reassignment. Establish what the event log actually contains before computing hop
  counts — a system that only stores the current assignee cannot support this analysis
  at all, and saying so is the correct output.
- **Automated reassignments** by rules or schedulers inflate hop counts and are not
  human failures. Separate them.
- **Team reorganisations** inside the window make queue-level trends meaningless.
  Check for renames and merges first.
- **A transfer with a good handoff note is a different experience** from a silent one.
  Where notes exist, measure the share of transfers that carry context; a transfer
  chain with no handoff notes is why the customer repeats themselves four times.
- **Do not attribute misroutes to the agent who transferred.** They usually did the
  right thing with a contact that should never have reached them. The finding belongs to
  whoever owns the rule.

## Present results to the user

1. **What the data supports** — whether the assignment event history is complete enough
   for hop analysis, stated first.
2. **Hop distribution**, with the 3+ tail called out and its link to complaints.
3. **Misroute and ping-pong rates**, separated from designed escalation and load
   balancing.
4. **Time lost to routing**, totalled across the window.
5. **Misroute clusters** by origin queue and contact driver, each mapped to the rule,
   form or menu that produced it.
6. **Unassigned work and unowned queues**, as a specific list with owners to assign.
7. **Catch-all share** and its trend.
8. **Ranked fixes**, by time recovered, each naming the rule or form to change — not
   the people.
