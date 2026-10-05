---
name: cx-queue-design
description: Use to design support queues and the skill taxonomy routing rules depend on — not as an org chart mirror, but as staffable combinations of skill, priority and channel. Trigger for "how should we structure our queues", "too many queues", "queue design", "routing taxonomy", "catch-all queue growing", overflow rules, or redesigning queue structure before changing routing rules.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Queue design

The most common queue design mistake is mirroring the org chart: a queue per team,
per region, per product line, per manager's span. It feels logical and it produces
routing that nobody can staff.

**Queues are not teams.** A queue is a promise: *if a contact arrives here, someone
with these skills will handle it within this service expectation.* Design queues around
what you can actually promise and staff, not around who exists in the directory.

## The right unit: skill + priority + channel

Every queue should be definable as a combination you can answer three questions about:

1. **What skills does the handler need?** Product knowledge, language, regulatory
   authority, technical depth — the minimum set, not the ideal résumé.
2. **What priority class applies?** Urgent, standard, low — tied to a service target, not
   to a feeling.
3. **What channel constraints apply?** Real-time voice and chat need different staffing
   maths than async email; mixing them in one queue hides the constraint.

A queue that cannot be described this way is probably a team label wearing a queue name.

| Design signal | Healthy | Unhealthy |
| --- | --- | --- |
| Queue count vs headcount | Few enough that every queue has a named owner and a minimum staffing plan | More queues than people who could ever be in them at once |
| Volume per queue | Most queues see enough traffic to learn from weekly | Long tail of queues with single-digit contacts per month |
| Skill overlap | Agents credentialed for 2–4 queues, not 15 | Every agent "in" every queue; routing becomes random |
| Catch-all share | Stable and shrinking as rules improve | Growing; specific rules decaying |

## Few queues vs many: the trade-off

**Few queues** simplify staffing and reduce misroutes from over-specific rules. Cost:
longer handle time as generalists research, higher training burden per agent, and
priority dilution — urgent contacts wait behind routine ones in the same pipe.

**Many queues** shorten handle time when skills genuinely differ and let you protect
priority lanes. Cost: fragmentation, empty queues at off-peak, agents spread too thin,
and routing rules that must be perfect or work goes nowhere.

Neither extreme wins. The decision rule:

- **Split a queue when** handle time, quality or compliance differ materially by segment
  *and* you can staff the split queue at its minimum viable level across the week.
- **Merge queues when** the same people handle both with the same tools and targets,
  or when one queue is chronically under-staffed because demand is too thin to forecast.

Document the split/merge rationale. Future reorganisations will otherwise recreate the
org-chart pattern by default.

## Skill taxonomy: what routing actually matches on

Routing rules match contacts to queues. The taxonomy is the vocabulary those rules use.
Build it before the queues, not after.

Principles:

- **Skills are capabilities, not team names.** "Billing disputes" is a skill; "Team
  Phoenix" is not.
- **One primary skill per contact type** in the taxonomy. Secondary skills are overflow
  credentials, not parallel routing targets.
- **Align taxonomy labels with customer-facing language** where customers self-select.
  Mismatch between what the customer clicks and what the rule expects is the leading
  cause of catch-all growth.
- **Version the taxonomy.** When product or policy changes, stale skill tags silently
  misroute until someone notices catch-all volume rising.

The taxonomy and the queue list should be mappable to each other in a table anyone can
read. If the mapping requires a ten-page appendix, the design is too complex to operate.

## Overflow and backup

Every queue needs a defined overflow path before go-live, not improvised at peak:

- **Skill-based overflow** — if primary queue is saturated, route to the nearest
  credentialed queue with capacity. Document which skills are acceptable substitutes
  and which are not (compliance, language, authority limits).
- **Priority overflow** — urgent contacts may jump queue order within a queue or move
  to a dedicated priority queue. Define whether overflow preserves priority or downgrades
  it.
- **Time-based overflow** — after a wait threshold, escalate to a supervisor queue or
  offer callback. The threshold must match what you can actually deliver, not an aspirational
  SLA printed on a slide.

Overflow without a rule is either abandonment or catch-all poisoning.

## Catch-all poison

The catch-all queue — "General", "Other", "Unassigned" — is necessary as a safety valve
and lethal as a design default.

Failure modes:

- **Catch-all as lazy routing.** Rules that match too broadly dump work here. Volume
  rises; nobody owns the quality of resolution because the queue has no skill definition.
- **Catch-all as staffing plan.** Teams staff specialists and leave catch-all as
  whoever is free. It becomes the highest-volume queue and the lowest-quality one.
- **Invisible demand signal.** Product and policy gaps show up in catch-all first. If
  catch-all is not tagged and reviewed, you lose the earliest warning of taxonomy decay.

Treat catch-all share as a health metric: rising share means rules or taxonomy are
falling behind reality. Target is not zero — some contacts genuinely do not fit — but
a stable or falling trend with a named owner reviewing weekly outliers.

## Operating the design

Once queues exist:

- **Named owner per queue** — accountable for rules, staffing plan, and outlier review.
- **Minimum staffing floor** — the smallest headcount that keeps the queue from being
  permanently in breach at expected volume. If you cannot staff the floor, merge the queue.
- **Join/leave rules for agents** — who can be in which queue, how credentials are
  granted and revoked, and what happens when someone leaves the team.
- **Review cadence** — monthly volume by queue, catch-all share, and queues with zero
  activity that still receive traffic (dormant poison).

Queue design is not a one-off project. It rots when the product ships, when teams
reorganise, and when nobody updates the taxonomy.

## Traps

- **Geographic or regional queues** when language and regulation do not require them.
  They duplicate staffing and confuse routing for customers who do not know your org.
- **Product-line queues** that share the same handlers and tools. Split on skill
  difference, not on P&L ownership.
- **Priority as a tag instead of a queue** when real-time channels need protected lanes.
  Tags sort within a pipe; they do not create capacity.
- **Designing queues in the routing tool** without a written taxonomy. The tool becomes
  the documentation and nobody can see the whole picture.
- **Assuming AI or bot deflection removes the need for queue design.** Deflected
  contacts still need a path when the bot fails; that path is a queue.

## Present results to the user

1. **Current queue inventory** — name, owner, channel, stated skill, priority class,
   and weekly volume. Flag queues with no owner or near-zero activity.
2. **Taxonomy map** — contact types / skills mapped to queues, with gaps and overlaps
   called out.
3. **Catch-all diagnosis** — share, trend, and top drivers landing there; each mapped to
   a rule or taxonomy fix.
4. **Split/merge recommendations** — each with the staffing implication stated (can you
   staff the floor?).
5. **Overflow paths** — documented per queue, or explicit gaps where overflow is
   improvised today.
6. **Proposed target structure** — the minimum queue set that covers skill + priority +
   channel without mirroring the org chart.
7. **Implementation sequence** — taxonomy first, then rules, then agent credentials;
   not the reverse.
