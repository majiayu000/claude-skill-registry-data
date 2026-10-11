---
name: orchestration-flows
description: "Use when designing or reviewing Flow Orchestration for long-running, multi-user, or asynchronous business processes with stages, steps, work items, and monitoring needs. Triggers: 'flow orchestration', 'work item', 'stages and steps', 'multi-user process', 'long-running flow'. NOT for simple single-transaction record-triggered flows or lightweight approval routing that does not need orchestration."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - Reliability
  - Scalability
  - Operational Excellence
triggers:
  - "when should i use flow orchestration"
  - "flow orchestration stages and steps design"
  - "multi user business process in salesforce"
  - "work items in flow orchestration"
  - "orchestration monitoring and recovery"
tags:
  - flow-orchestration
  - work-items
  - asynchronous-process
  - stages
  - multi-user
inputs:
  - "business process timeline and handoff points"
  - "which steps are background vs human-interactive"
  - "monitoring, reassignment, and recovery expectations"
outputs:
  - "orchestration design recommendation"
  - "stage-and-step review findings"
  - "decision on orchestration vs standard flow or apex"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

Use this skill when the business process spans time, people, and system boundaries in a way that normal record-triggered or screen flows do not handle cleanly. Flow Orchestration is the right tool when a process needs explicit stage progression, work assignment, and observability across days or weeks — instead of pretending the whole journey happens in one synchronous transaction.

Orchestration is NOT "Flow with more canvas space." It adds operational overhead (stages, work items, monitoring surface) that is valuable ONLY when the business process genuinely has time gaps, multi-user handoffs, and stage-by-stage observability requirements. Using it for simple automation is like using a message queue for in-process function calls — the overhead without the payoff.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- Is the process actually long-running (hours to weeks) or multi-user, or could a standard Flow handle it more simply?
- Which parts of the process are background automation, and which parts create work items for humans?
- What must happen when a step is delayed, reassigned, fails, or needs recovery after a long wait?
- Will this process replace an existing Approval Process? (If yes, consult `automation-migration-router --source-type approval_process` first.)
- What's the expected number of concurrent in-flight instances? (Affects monitoring design and licensing — Flow Orchestration has usage limits.)

## Core Concepts

### Orchestration Is For Process Lifecycles, Not Just Automation Steps

Regular Flows are good at single execution paths. Orchestration becomes useful when the process needs explicit lifecycle management across stages, users, and time gaps. Treat it as process architecture — stages = milestones visible to operations; steps = work units that can be monitored; transitions = the contract between stages.

The litmus test: "Do I need a view of where every in-flight instance is currently stuck, who owns the next action, and what intervention is required?" If yes, Orchestration. If the answer is "we'll figure it out from the Flow Interview Log", a regular Flow is sufficient.

### Stages And Steps Need Clear Ownership

Stages should represent meaningful process milestones (not just "next page"). Steps should represent work that can be monitored, assigned, and completed. If stage boundaries are vague, monitoring and recovery become unclear — admins see "instance stuck in Stage 2" but don't know what Stage 2 actually represents to the business.

**Rule of thumb:** every stage name should be a noun phrase a business owner recognizes. "Credit Check" yes. "Stage2" no. "Processing" no. "Financial Review" yes.

### Interactive And Background Work Should Be Designed Differently

Human work items need assignment, visibility, escalation, and reassignment. Background steps need idempotency, fault handling, and service-level expectations. Orchestration only helps if those two concerns are designed deliberately — NOT if you treat all steps as "Flow steps" and ignore the difference.

| Concern | Interactive Step | Background Step |
|---|---|---|
| Completion trigger | User clicks "Complete" in the work-item UI | Underlying Flow finishes successfully |
| Failure surface | User gets an error; work item stays "In Progress" | Flow errors → Orchestration error-handling event |
| Reassignment | Manager can reassign to another user / queue | Not reassigned — either auto-retried or fails the stage |
| Monitoring | "Who has the work item" view | "Last successful execution" timestamp |
| SLA | Clock runs on human time | Clock runs on machine time |

### Monitoring Is Part Of The Design, Not an Afterthought

A long-running process is incomplete unless operations teams can see where instances are stuck, who owns the next action, and how to resume or intervene. Orchestration surfaces include:

- **Work Items tab** — all pending human work items, with filters by assignee, stage, and age.
- **Flow Orchestration Work Items List View** — customizable per-persona views of pending work.
- **Orchestration Error Email** — delivered to the Process Automation user when a stage fails.
- **Custom dashboards** — built on `FlowOrchestrationInstance` + `FlowOrchestrationWorkItem` sObjects.

If operations isn't going to look at any of these, the Orchestration was probably wrong — a standard Flow with good fault handling would have served. Design the monitoring surface BEFORE building the Orchestration, not after.

## Common Patterns

### Pattern 1: Stage-Based Onboarding Or Fulfillment

**When to use:** A business journey moves through clear milestones with a mix of automated and human tasks. Think customer onboarding, employee hiring, product fulfillment.

**Structure:**
```text
Orchestration: Customer_Onboarding
├── Stage 1: Application_Received (background)
│   ├── Step: Validate_Application (auto-launched Flow)
│   └── Step: Route_To_Underwriting (background assignment logic)
├── Stage 2: Underwriting (interactive)
│   ├── Work Item: Underwriter Review (assigned to queue)
│   └── Work Item: Senior Underwriter Approval (conditional on amount > $100k)
├── Stage 3: Contract_Generation (background)
│   ├── Step: Generate_Contract (Conga / DocuSign action)
│   └── Step: Send_To_Customer
└── Stage 4: Activation (background)
    └── Step: Provision_Services
```

**Why not the alternative:** A single standard Flow becomes brittle when it tries to model waits, approvals, and manual follow-up inside one execution path. Every `Pause` element in a non-Orchestration Flow is a hack around the lack of stage awareness.

### Pattern 2: Background Step Plus Human Review

**When to use:** System work should prepare data and then hand it to a reviewer or fulfiller.

**Structure:**
```text
Stage: Data_Prep (background)
└── Step: Fetch_External_Data (HTTP callout via External Services)
└── Step: Normalize_And_Score (auto-launched Flow calling Apex)

Stage: Human_Review (interactive)
└── Work Item: Reviewer_Decision (assigned to queue, due-date = now + 2 business days)
    └── On complete → transition to next stage
    └── On overdue → escalation auto-launched Flow
```

**Why not the alternative:** Making every step human-visible slows the process and reduces automation value. Background steps should be invisible to reviewers unless something goes wrong.

### Pattern 3: Escalation To Apex Or Another Orchestrator

**When to use:** The process needs heavy integration logic, very large data movement, or transaction behavior beyond Flow's fit.

**Signals:** Orchestration's background steps are full of `@future` / Queueable invocations; the stage boundaries are really Apex transaction boundaries; the operations team is monitoring Apex job status more than the Orchestration surface.

**Approach:** Keep Orchestration for human lifecycle management only. Move heavy system-work stages to standalone Apex (Batch, Queueable, Platform Events) that reports back to Orchestration via custom events or Flow invocations. Orchestration becomes a thin coordinator; Apex does the work.

### Pattern 4: Replace Legacy Approval Process

**When to use:** Migrating from a multi-stage Approval Process with post-approval automation.

**Structure:** Each Approval Step becomes a Stage in Orchestration; Initial Submission Actions become pre-stage background work; Final Approval Actions become post-stage background work. The migration is NOT automatic — see `automation-migration-router --source-type approval_process` for the decision tree.

Not every approval should migrate: single-step, single-assignee approvals are better left as Approval Processes (simpler, deployed as one metadata unit). Complex multi-step approvals with cross-object routing and recall semantics are where Orchestration shines.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Single save event with immediate side effects | Standard record-triggered Flow | Orchestration is unnecessary overhead |
| Long-running process with human and system work | Flow Orchestration (Pattern 1) | Stages, steps, and work items are the right abstraction |
| Process is mostly heavy integration and no human workflow | Apex or external orchestration (Pattern 3) | Flow Orchestration adds little value here |
| Monitoring, reassignment, and stuck-instance handling are important | Flow Orchestration | Operational visibility is built into the model |
| Migrating legacy Approval Process | Evaluate via `automation-migration-router --source-type approval_process` | Not every approval should migrate |
| Need SLA-tracked human work items | Flow Orchestration | Native SLA + due-date + escalation tooling |
| Process fits in < 5 minutes and 1 user | Screen Flow or record-triggered Flow | Orchestration's lifecycle machinery is wasted |

## Well-Architected Pillar Mapping

- **Reliability** — orchestration's recovery semantics (resume stuck instance, reassign work item, rerun failed stage) are core reliability affordances. Findings in this area are P0 when observability is missing.
- **Scalability** — Orchestration has per-org usage limits (in-flight instances, work items per day). Designs that assume unlimited concurrency will break at scale.
- **Operational Excellence** — the monitoring surface IS the OpsEx surface. Orchestration without custom work-item list views, dashboards, or stuck-instance alerts is an OpsEx debt.

## Review Checklist

- [ ] The use case genuinely requires long-running or multi-user process control.
- [ ] Stages represent real business milestones, not arbitrary canvas grouping.
- [ ] Human steps have clear assignment, escalation, and completion ownership.
- [ ] Background steps are idempotent and fault-aware.
- [ ] Monitoring and intervention expectations were designed before launch.
- [ ] Custom work-item list views exist for the relevant personas.
- [ ] Orchestration Error Email recipient is a monitored mailbox.
- [ ] The team considered whether standard Flow or Apex would be simpler.
- [ ] Per-org Orchestration usage limits have been checked against expected load.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, licensed features, expected load, and existing automation
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; map stages to business milestones
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **Orchestration is not a better record-triggered flow by default** — it adds operational structure, which is useful only when the process truly spans time and users.
2. **Poor stage boundaries create monitoring noise** — if stages do not map to real milestones, work-item visibility becomes hard to act on.
3. **Interactive steps are operations work, not just UI** — assignment, backlog management, and reassignment need ownership from the start.
4. **Long-running processes still need failure design** — a stuck orchestration instance is an operational incident, not a cosmetic problem.
5. **Work Item due dates are on business days, not calendar days by default** — test with your org's business-hours configuration; surprise escalation timing is a common go-live bug.
6. **Orchestration Error Email goes to the Process Automation user** — audit the mailbox annually; orchestration errors are harder to notice than Flow fault emails.
7. **In-flight instances survive a Flow version update ONLY if the new version is backward-compatible** — breaking stage/step changes require explicit migration logic. Plan deprecation windows.
8. **Per-org concurrent-orchestration limits exist** — consult Salesforce Help for current caps (they vary by edition and have changed across releases); design load-shedding if approaching limits.
9. **Work items do not auto-close on record deletion** — delete the triggering record and the work item lingers in "In Progress" forever. Build a cleanup job or set explicit completion handlers.
10. **Orchestration invoked from record-triggered Flow still fires per record** — a bulk insert triggers one Orchestration instance per record. Scale accordingly.

## Proactive Triggers

Surface these WITHOUT being asked:

- **Orchestration used for single-user, single-save automation** → Flag as High. This is overkill; convert to standard record-triggered Flow.
- **Work items with no assignee rule (all go to a default queue with no members)** → Flag as Critical. Work will pile up in the void.
- **No custom list view for pending work items** → Flag as High. Operations can't monitor what they can't see.
- **Orchestration Error Email recipient is inactive or unset** → Flag as Critical. Stage failures disappear silently.
- **Background step with no fault-handling branch** → Flag as High. Failed step = stuck instance forever.
- **Stage name that doesn't match a business-owner's vocabulary** → Flag as Medium. Naming debt; fix during design reviews.
- **Orchestration replacing a simple Approval Process (single-step, single-assignee)** → Flag as Medium. Re-evaluate; the simpler tool may fit better.
- **No plan for handling stuck in-flight instances during a Salesforce release upgrade** → Flag as High. Regression risk on release day.

## Output Artifacts

| Artifact | Description |
|---|---|
| Orchestration fit assessment | Recommendation on whether Flow Orchestration is justified vs alternatives |
| Stage-and-step model | Proposed process milestones, work items, background boundaries, transitions |
| Monitoring plan | Work-item list views, dashboards, stuck-instance alerts, error-email routing |
| Migration plan (when applicable) | Step-by-step migration from legacy Approval Process (via `automation-migration-router`) |

## Related Skills

- **flow/fault-handling** — use when error-routing and recovery are the immediate concern inside a step or subflow.
- **flow/auto-launched-flow-patterns** — the background-step flows that Orchestration invokes live here.
- **flow/subflows-and-reusability** — when Orchestration stages should factor work into reusable subflows.
- **admin/approval-processes** — use when the process is really about approval routing rather than broader orchestration.
- **apex/async-apex** — use when the system-work portions need more control than Flow should carry.
- **standards/decision-trees/automation-selection.md** — upstream decision tree routing Orchestration vs alternatives.
