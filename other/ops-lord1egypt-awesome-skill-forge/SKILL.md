---
name: Ops
description: A comprehensive AI agent skill for running operations effectively across engineering, business, and organizational contexts. Manages runbooks, incident coordination, deployment processes, team rituals, cross-functional workflows, vendor relationships, and the operational infrastructure that keeps organizations functioning smoothly when nobody is paying attention to it.
---

# Ops

## The Work That Makes Everything Else Possible

There is a category of work that never appears in a product roadmap, never gets celebrated at an all-hands, and never shows up in the metrics that investors look at. It is not glamorous. It does not generate the kind of visible output that makes careers. It is the work of keeping things running.

The weekly sync that surfaces blockers before they become crises. The vendor contract renewal that gets handled before the service lapses. The incident postmortem that actually changes the process instead of sitting in a folder nobody opens. The deployment checklist that prevents the mistake that would have taken down production on a Friday afternoon. The onboarding process that means a new hire is productive in two weeks instead of two months.

Operations is the discipline of making these things happen consistently, not heroically. Not through the extraordinary effort of exceptional people working exceptional hours, but through systems, processes, and habits that produce reliable outcomes regardless of who is doing them and what else is happening.

When operations is working well, it is invisible. The organization runs smoothly. Decisions happen at the right level with the right information. Problems surface before they become emergencies. The team can move fast because the operational foundation is solid enough to support speed without creating chaos.

When operations is failing, it is very visible. Everything requires more effort than it should. The same problems recur because nothing was done to address the root cause. Information lives in people's heads instead of in systems, which means when those people are unavailable, the organization loses access to it. Coordination happens through heroism instead of process.

Ops is the skill that builds the invisible foundation.

---

## Incident Management

Incidents have a lifecycle that most organizations manage reactively rather than systematically. Something breaks. The people who notice it start trying to fix it. Other people get looped in or not depending on who happens to be available. Communication to affected stakeholders happens inconsistently. The fix is implemented. Everyone moves on. The same incident happens again three months later because nothing was done to prevent it.

Systematic incident management looks different at every stage.

**Detection and triage** determines whether what just happened is a minor anomaly, a significant incident, or a critical outage requiring immediate all-hands response. The classification matters because the response is different. Treating every alert as a critical incident creates alert fatigue and burns out the people responding. Treating a critical incident as a minor anomaly allows it to compound. The skill helps you build triage criteria that produce the right classification consistently.

**Coordination** during an active incident is where most of the lost time happens. Who is the incident commander? Who is working on diagnosis versus working on the fix versus communicating with stakeholders? What is the current hypothesis about root cause? What has been tried and eliminated? Without clear coordination, multiple people work on the same thing, important information does not reach the people who need it, and the incident drags on because nobody has the full picture.

The skill maintains the incident coordination structure. It tracks the current status, the hypotheses being tested, the actions in progress and their owners, and the communication that needs to go out to stakeholders. It ensures that the person coordinating the incident can focus on coordination rather than trying to simultaneously work on the technical problem.

**Stakeholder communication** during incidents requires a specific skill that most technical people find uncomfortable: conveying accurate uncertainty in plain language under time pressure. Not overpromising a resolution time that turns out to be wrong. Not being so vague that stakeholders lose confidence. Not using technical language that means nothing to the people receiving the update. The skill drafts stakeholder communications at each stage of the incident that are honest, clear, and calibrated to what is actually known.

**Postmortems** that prevent recurrence are structured differently from postmortems that document what happened. The skill facilitates postmortems focused on systemic causes rather than individual failures, that produce specific, actionable, owned improvements rather than general observations, and that are actually completed rather than scheduled and then deprioritized when the next urgent thing arrives.

---

## Deployment Operations

Every deployment is a change to a system that real people depend on. The discipline of deployment operations is the set of practices that make those changes reliable — that reduce the probability of a deployment causing an incident, and reduce the impact and duration of incidents when they happen anyway.

**Deployment checklists** are the operational artifact that most teams either do not have or do not follow consistently. The checklist is not bureaucracy. It is the accumulated learning of every deployment that went wrong, encoded into a sequence of checks that prevents those failures from recurring. The skill helps you build deployment checklists that cover the checks that actually matter for your specific systems, and maintains them as your systems evolve.

**Rollback procedures** are the thing nobody thinks about until they need them urgently, at which point the absence of a clear, tested procedure adds significant time to an already bad situation. The skill documents rollback procedures for every deployment type and ensures they are tested periodically so that when they are needed, they work.

**Change management** for operational changes — infrastructure updates, configuration changes, database migrations — requires a level of rigor proportional to the risk of the change. Low-risk changes can move quickly. High-risk changes require review, testing, staged rollout, and clear rollback criteria. The skill helps you apply the right level of rigor to each change rather than either applying maximum rigor to everything (which slows everything down) or minimum rigor to everything (which produces preventable incidents).

---

## Team Operations

**Meeting design** is one of the highest-leverage operational interventions available to any team. The meeting that takes sixty minutes but could accomplish the same outcome in thirty, run every week for a year, costs the organization twenty-six hours of collective attention per participant. Across a team of ten, that is two hundred and sixty hours per year for a single recurring meeting.

The skill helps you design meetings that accomplish their purpose efficiently. Not by eliminating meetings — some coordination genuinely requires synchronous discussion — but by ensuring that the synchronous time is used for the decisions and discussions that require it, and that the information sharing that does not require synchronous discussion happens asynchronously instead.

**Operational rituals** — the weekly review, the monthly retrospective, the quarterly planning — are the rhythms that keep teams aligned and surfacing problems before they become crises. Most teams have these rituals in some form. Few have them designed to consistently produce the outcomes they are meant to produce. The skill designs operational rituals with clear purposes, clear ownership, and clear outputs, and helps you run them consistently rather than letting them drift into box-checking.

**Cross-functional coordination** is where most operational friction in organizations actually lives. Not within teams, which usually have enough daily interaction to stay coordinated, but between teams that are working on interdependent problems and need a reliable mechanism to surface dependencies, share status, and make decisions that cross organizational boundaries.

The skill designs the coordination mechanisms — the right meeting cadence, the right documentation, the right decision-making process — for the specific cross-functional dependencies in your organization.

---

## Vendor and Contract Operations

Vendor relationships have an operational lifecycle that most organizations manage poorly: due diligence at the beginning, then benign neglect until renewal, then rushed renegotiation when the renewal date is discovered at the last minute.

Good vendor operations look different. Contracts are tracked with renewal dates and notification windows that give you time to evaluate alternatives and negotiate from a position of knowledge rather than urgency. Vendor performance is reviewed periodically against the commitments made at the time of the contract. Concentration risk — the degree to which your operations depend on a single vendor — is monitored and managed.

The skill maintains your vendor registry, tracks renewal dates and contract terms, surfaces renewal conversations at the right time, and helps you prepare for vendor reviews and negotiations with the information you need to negotiate effectively.

---

## Operational Documentation

Operations runs on documentation: runbooks, processes, checklists, decision frameworks, vendor contacts, escalation paths. Documentation that is out of date is operationally dangerous — it gives people false confidence that they know what to do, and then fails them at the moment they need it most.

The skill helps you maintain operational documentation that reflects how operations actually works rather than how it worked eighteen months ago. It identifies documentation that is likely to be stale based on known changes to the systems or processes it covers. It builds documentation review into the operational calendar rather than treating documentation maintenance as a separate project that never gets prioritized.

---

## The Operations Mindset

The underlying discipline of operations is this: every problem that happens more than once is a process problem, not a people problem. The incident that recurs because the runbook was not updated. The deadline that was missed because nobody owned the reminder. The vendor contract that auto-renewed at unfavorable terms because the renewal date was not tracked.

These are not failures of individual attention or effort. They are failures of operational systems that should have prevented the problem from recurring after the first time.

Operations is the practice of building those systems — not perfectly, not all at once, but incrementally, with each recurrence of a preventable problem treated as information about where the next system needs to be built.

The organizations that scale without operational chaos are not the ones with the most talented people working the hardest. They are the ones that have built operational systems good enough that talented people do not have to work heroically to compensate for the absence of process.

That is what this skill is for.
