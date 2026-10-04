---
name: agent-foundry-proactive
description: "Design product-agnostic proactive systems for AgentFoundry AI-native products and write an ADR before implementation. Use when any product type, such as travel, health, running, commerce, education, finance, support, or operations, needs event watchers, reactions, ProactiveState, ProactiveWatchers, ProactiveSignals, ProactiveTasks, ProactiveApprovals, notifications, and native UX on top of durable artifacts. The skill asks the user one question at a time, researches useful proactivity for the product vertical, ranks candidate watcher/reaction features with RICE/RISE, asks the user which to implement, and creates an ADR. This skill does not implement code directly."
---

# AgentFoundry Proactive

## Purpose

Use this skill to design a reusable proactive system for any AgentFoundry product before implementation.

This skill is not travel-specific. TravelPlanner2 is the reference implementation and ADR 0001 is the product precedent, but the skill must generalize the model to any vertical:

```text
Durable artifact / user goal
-> ProactiveState
-> ProactiveWatchers observe events over time
-> ProactiveSignals explain what changed or matters now
-> ProactiveTasks propose or perform useful work
-> ProactiveApprovals gate risky or external actions
-> Native UX shows Now, Proactive Feed, cards, approvals, task status, and notifications
```

Examples of source artifacts:

- Travel: `travel_plan`
- Health: `care_plan`, `habit_tracker`, `health_day`
- Running/weekend: `activity_plan`, `training_plan`
- Commerce: `cart`, `watchlist`, `order_plan`
- Education: `learning_plan`, `lesson_progress`
- Operations/legal/support: `case_status`, `work_order`, `approval_packet`

## Required References

Load only what is needed:

- Read `references/proactive-architecture.md` before designing schemas, backend state machines, workers, provider adapters, ADR runtime sections, or implementation tasks.
- Read `references/product-research-and-task-selection.md` before recommending domain-specific event watchers, reactions, or ProactiveTask types.
- Read `references/native-ux-patterns.md` before designing ADR UX sections, iOS proactive surfaces, task cards, approvals, or notification routing.

When using TravelPlanner2 as precedent, read its current implementation and ADR if available:

- `docs/adr/0001-travel-proactive-companion.md`
- `functions/src/schemas.ts`
- `functions/src/index.ts`
- SwiftUI surfaces that render ProactiveState/Watchers/Signals/Tasks/Approvals/Notifications

The current TravelPlanner2 code is more current than ADR 0001. Prefer code for implemented DTO/runtime details and ADR 0001 for product taxonomy, RICE/RISE scoring, result-type separation, and production scanner direction.

## Relationship To Other AgentFoundry Skills

- `agent-foundry-proof` creates the base iOS/Firebase/backend-agent proof.
- `agent-foundry-artifact-ui` creates durable typed artifacts and native artifact UI.
- `agent-foundry-design` owns native iOS target, Liquid Glass design, visual QA, clickability, shadow/clipping, and interaction quality.
- `agent-foundry-proactive` creates the proactive ADR and reusable runtime decision record on top of durable artifacts.

When proposing typed artifact/card changes, load `../agent-foundry-artifact-ui/SKILL.md`.
When proposing or implementing iOS UI, load `../agent-foundry-design/SKILL.md`.

## Product Stance

- Proactivity is event architecture, not a list of travel features.
- A proactive feature is `event source -> ProactiveWatcher -> ProactiveSignal -> reaction/result -> optional ProactiveTask -> optional ProactiveApproval -> notification/native UX`.
- A ProactiveWatcher observes reality. A reaction is what the app does after the event matters. Do not blur watcher names with result names.
- A ProactiveSignal is an observation or recommendation. A ProactiveTask is actionable work with lifecycle. A ProactiveApproval gates side effects.
- External, costly, irreversible, provider-visible, regulated, or user-visible-outside-app work must require ProactiveApproval.
- The user must be asked what event watchers and reactions they want, one question at a time, before the skill performs research.
- The agent must still perform product research for the specific product and user segment, then infer which proactive moments users actually need. User ideation is input, not the whole taxonomy.
- Default architecture target is production-scale: millions of users, many artifacts per user, many watchers per artifact, shared provider facts, and bounded notification volume.
- A prototype-only scanner is allowed only when the ADR explicitly labels it as temporary, states the expected user/watchers ceiling, and includes the migration trigger to the production due-index runtime.
- The output of this skill is an ADR. Do not implement code unless the user separately asks to implement an already approved ADR.

## Universal Naming

Use the `proactive` prefix in schemas, storage paths, DTOs, UI names, and ADR text:

- `ProactiveState`
- `ProactiveWatcher`
- `ProactiveSignal`
- `ProactiveTask`
- `ProactiveApproval`
- `proactiveWatchers`
- `proactiveSignals`
- `proactiveTasks`
- `proactiveApprovals`
- `proactiveNotifications`

Do not introduce new `Companion*` names or `companion*` collections. If studying TravelPlanner2, translate existing `Companion*` code concepts into `Proactive*` terminology in the ADR.

## Hard Gates

Do not claim proactive design work is complete unless all are true:

- A source-of-truth durable artifact or user goal is identified.
- `ProactiveState`, `ProactiveWatcher`, `ProactiveSignal`, `ProactiveTask`, and `ProactiveApproval` are defined or explicitly scoped out with a reason.
- The user was asked, one question at a time, which event watchers and reactions they imagine for the product.
- Product research was performed or explicitly marked unavailable/forbidden before choosing domain event/reaction types. Research must identify what proactive help users actually need in the stated product, not only which providers or facts are technically available.
- A researched candidate event/reaction table was produced and sorted by RICE or RISE.
- The user explicitly selected which events and reactions the ADR should include.
- An ADR was created or updated for the proactive feature.
- The ADR states the scale target: `prototype`, `production_mvp`, or `million_user_production`.
- For `production_mvp` and `million_user_production`, the ADR defines due indexing, sharding, leasing, idempotency, dedupe, provider snapshot caching, provider fanout, retry/backoff, and notification budgets.
- If the ADR chooses `prototype`, it must include a hard migration trigger, such as watcher count, due work per minute, provider call volume, or active-user threshold.
- Watchers have trigger sources, cadence, expiration, quiet hours/notification rules, dedupe, and rate limits.
- ProactiveTasks are typed, versioned, persisted, and restorable after app relaunch.
- Task status transitions are explicit and validated.
- External side effects require explicit ProactiveApproval: calls, bookings, purchases, messages, payments, publishing, sharing, regulated advice, provider-visible actions, or third-party data transfer.
- No fake success states. Unknown, estimated, pending, failed, stale, and unavailable states are visible.
- The backend owns scheduled checks, provider calls, task execution, and secrets. iOS only displays, approves, and routes.
- Native UX exists for current status, proactive feed, signal/task cards, approval review, task detail, stale/failed state, and notification deep links.
- Privacy boundaries are explicit: what data is used, what is sent to providers, what is logged, and what can be deleted.
- Verification covers ADR review, schema decoding, state transitions, approval/rejection, worker output, restoration, unknown-version fallback, and notification/deep-link routing where possible.

If any gate fails, stop with the smallest concrete next action. Do not implement code as a substitute for the missing ADR decision.

## Workflow

### 1. Establish The Source Artifact And User's Intended Events

Identify the durable object the proactive system watches and improves. Ask questions one at a time and wait for the user's answer after each question.

Ask these questions in order, skipping only answers already present in an approved product spec:

1. What product/domain and target user is this for?
2. What durable artifact or goal state should the proactive system watch?
3. Which event watchers does the user already want? Phrase as: "when X changes or becomes true".
4. Which reactions does the user want? Phrase as: "then the app should Y".
5. Which actions may notify, mutate app state, contact third parties, spend money, share data, publish/send messages, or provide regulated advice?
6. Which providers, internal data sources, user permissions, constraints, and forbidden data are known?
7. What scale target is required for the first implementation: prototype, production MVP, or million-user production?

Do not ask the user to design the full task taxonomy. The user supplies intent; the skill supplies researched options and prioritization.

### 2. Product Research: What Proactivity Users Actually Need

Always combine:

- User's requested event watchers and reactions.
- Independent product research for the stated product, target user, and vertical.
- Local product analysis when code, docs, existing user flows, or artifacts are available.
- Feasibility and safety judgment.

Use web research when user behavior, market patterns, APIs, providers, regulations, prices, health/commerce/travel/running/education trends, or external service capabilities may be current. If browsing is unavailable or forbidden, proceed from local context and label assumptions.

Before recommending domain tasks, load `references/product-research-and-task-selection.md`.

Product research must answer:

- Who the target user is and what job they hire this product to do.
- Where the user's current workflow breaks, stalls, creates anxiety, or forces repeated manual checking.
- What the user would want the product to notice before they notice it themselves.
- Which proactive moments would make the product feel meaningfully more useful, not just more noisy.
- What users manually check today.
- Which real-world facts change and can break the artifact/goal.
- Which moments are time-sensitive.
- Which events create anxiety, missed opportunity, safety risk, cost, delay, or cognitive load.
- Which reactions are safe suggestions versus external side effects.
- Which providers or internal data sources can verify reality.
- Which proactive surfaces are understandable without rereading chat.

Synthesize the research into 5-10 user-need statements before scoring features. Format:

```text
User need: <target user> needs the product to notice <event/change> because <consequence if missed>.
Proactive value: <brief/check/alert/proposal/handoff/approval>.
Evidence: <user answer, local product context, or external research source>.
```

Only then convert user needs into event watcher / reaction candidates.

### 3. Build The Candidate Event/Reaction Table

Generate a table of candidate proactive features. Each row is one event watcher and its reaction.

Columns:

```text
Rank
Priority
Event watcher
Observed event
Algorithm / importance rule
Data source / provider
Reaction / result type
Approval required
Reach
Impact
Confidence
Effort
Ease
RICE
RISE
Why this score
Ship / later / avoid
```

Scoring:

```text
Reach: 1-10
Impact: 1-5
Confidence: 0.5-1.0
Effort: 1-5
Ease = 6 - Effort
RICE = Reach * Impact * Confidence / Effort
RISE = Reach * Impact * Confidence * Ease
```

Use RICE as the default sort order unless the user asks for RISE. RISE is allowed when the user wants easy/high-value wins emphasized.

Use universal result types unless the product needs a documented product-specific result type:

- `health_finding`: missing, stale, weak, unverifiable, or blocked data.
- `notification_card`: verified fact matters, no mutation needed.
- `time_sensitive_push`: user must act soon.
- `approval_handoff`: user must approve external/costly/sensitive work.
- `artifact_change_proposal`: verified fact should change the durable artifact, but only after approval.
- `daily_brief`: low-risk current-state summary.
- `document_handoff`: exact document/pass/code/form surfaced at the useful moment.

### 4. Ask The User To Select Events And Reactions

Show the ranked table and ask the user to choose which events/reactions to include in the ADR.

Ask one decision question and stop until the user answers. The choice should be concrete:

- MVP only: top 3-5 low-risk/high-RICE rows.
- Balanced release: top 5-7 rows including one approval-gated handoff.
- Ambitious release: broader set, but mark provider-heavy or risky rows as phased.
- Custom: user names exact rows.

If the user chooses custom, confirm the final row list before writing the ADR.

### 5. Write The Proactive ADR

Create or update an ADR in the target repo, normally:

```text
Docs/ADR/NNNN-<product>-proactive.md
```

If the repo uses lowercase `docs/adr`, follow the repo convention. If no ADR directory exists, create `Docs/ADR`.

ADR template:

```markdown
# ADR NNNN: <Product> Proactive System

Status: Proposed
Date: <YYYY-MM-DD>
Owners: <product/backend/iOS or user-specified>
Source artifact: `<artifact_type>`

## Context
<Product/domain, target user, durable artifact, user-stated events/reactions, current manual/status quo behavior.>

## Decision
<Selected event watchers and reactions. Separate observed events from reactions/results.>

## Universal Runtime Model
<ProactiveState, ProactiveWatcher, ProactiveSignal, ProactiveTask, ProactiveApproval, notification/deep-link policy.>

## Result Types
<Result type table and approval rules.>

## Feature Matrix
<Selected rows from the RICE/RISE table plus deferred rows.>

## User Experience
<Now/current-state surface, Proactive Feed, ProactiveSignal card, ProactiveTask card, ProactiveApproval sheet, ProactiveTask detail, notification routing.>

## Backend Runtime
<Artifact creation/update, watcher materialization, due index/scanner, leases, provider snapshots/fanout, idempotency, dedupe, counters.>

## Privacy, Safety, And Approvals
<Data used, provider data sent, logs, deletion, user controls, external side-effect gates.>

## Rollout And Verification
<MVP slice, tests, smoke scenarios, provider mocks, iOS decode/fallback, notification/deep-link checks.>

## Consequences
<What gets easier, what complexity is introduced, what remains deferred.>
```

Do not write a generic plan instead of an ADR. The ADR is the output of this skill.

### 6. Define The Generic Proactive Runtime For The ADR

Before writing runtime sections, load `references/proactive-architecture.md`.

Define:

- `ProactiveState`: per artifact/session current proactive state and settings.
- `ProactiveWatcher`: scheduled or event-driven observer.
- `ProactiveSignal`: timely observation, risk, opportunity, reminder, or recommendation.
- `ProactiveTask`: typed actionable unit with lifecycle.
- `ProactiveApproval`: explicit user gate for side effects and sensitive actions.
- Provider adapters: tools/APIs/human fallback used by tasks.
- Notification policy: permissions, quiet hours, dedupe, priority, deep links.

### 7. Backend Runtime Requirements For Downstream Implementation

Recommended backend path:

```text
artifact created/updated
-> create/update ProactiveState
-> create/update ProactiveWatchers
-> workers evaluate ProactiveWatchers
-> workers persist ProactiveSignals and ProactiveTasks
-> approval-required tasks wait
-> approved tasks call provider adapters
-> task results update ProactiveState and source artifact
-> notifications deep-link to exact task/signal/artifact context
```

Use backend-owned scheduled jobs, task queues, Firestore triggers, or equivalent durable workers. Do not rely on the iOS app staying open.

For prototypes, a collection-group scan over enabled watchers is acceptable if called out as prototype-only. For production, require a due index or equivalent:

```text
proactiveDueIndex/{shard}/{dueEntryId}
providerSnapshots/{providerKey}
providerFanout/{providerKey}/subscribers/{watcherRef}
```

Production scanner requirements:

- Query due work by `nextRunAt <= now`, `status == enabled`, and shard.
- Order by due time and paginate.
- Acquire a transactional lease with `leaseOwner`, `leaseUntil`, and `attempt`.
- Dispatch work through durable queues or scheduled workers with bounded concurrency.
- Retry with backoff and dead-letter handling for provider failures.
- Use idempotency key = watcher id + input snapshot hash + due window.
- Use dedupe key = user/artifact/event/affected object/provider fact.
- Avoid provider calls per user when many users depend on the same fact; cache provider snapshots and fan out.
- Enforce per-user, per-artifact, per-provider, and global notification/provider-call budgets.
- Track lag, due queue depth, lease failures, provider error rate, notification suppression, and task conversion metrics.

### 8. Native UX Requirements For The ADR

Before iOS UI work, load `references/native-ux-patterns.md` and `../agent-foundry-design/SKILL.md`.

Recommended surfaces:

- Now / Today / Current State surface.
- Proactive Feed.
- Inline task/signal cards in chat or artifact UI.
- ProactiveApproval sheet.
- ProactiveTask detail/status timeline.
- Notification deep links.

The UX must make external actions feel deliberate and reviewable.

### 9. Verify

Run or specify:

- ADR review for event/reaction separation, scoring rationale, and approval gates.
- Backend schema/state-machine tests.
- Worker smoke tests for at least one ProactiveWatcher.
- Provider adapter tests or mocked contract tests.
- iOS decoding tests for ProactiveSignal/ProactiveTask/ProactiveApproval payloads.
- Unknown type/version fallback.
- Approval accept/reject/change path.
- Close/reopen restoration.
- Notification/deep-link smoke where tools permit.

## Output Shape

For ADR/design:

- Source artifact and journey moments.
- User's requested event watchers and reactions.
- Research summary and sources when browsing was used.
- User-need statements explaining which proactive moments users actually need and why.
- Candidate event/reaction table sorted by RICE or RISE.
- User-selected events/reactions.
- Generic runtime architecture: ProactiveState, ProactiveWatchers, ProactiveSignals, ProactiveTasks, ProactiveApprovals.
- Product-specific first-release event taxonomy.
- Deferred task types and reasons.
- Backend implementation plan.
- Native UX plan.
- Approval, safety, privacy, and notification policy.
- Verification plan.
- ADR file path and status.

For implementation:

- Files changed, only after an ADR exists or the user explicitly asks to implement an already approved ADR.
- Schemas and state transitions added.
- Watchers/workers/provider adapters added.
- Native surfaces/cards added.
- Tests/commands run.
- Remaining provider setup or manual approval steps.
