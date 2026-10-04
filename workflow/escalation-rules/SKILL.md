---
name: escalation-rules
description: "Configure and troubleshoot Salesforce Case Escalation Rules: time-based escalation entries, business hours configuration, escalation actions (email alerts and reassignment), and diagnosing why cases are not escalating. Covers the EscalationRules metadata shape, businessHoursSource and escalationStartTime semantics, staged escalationAction thresholds, deploy-inactive parallel-run cutover, and monitoring escalated cases. Trigger keywords: escalation rule, case not escalating, SLA breach notification, escalate after X hours, reassign case automatically, IsEscalated. NOT for SLA milestone timers — use admin/entitlements-and-milestones. NOT for case routing on creation — use admin/assignment-rules. NOT for the calendar itself — use admin/business-hours-and-holidays."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
triggers:
  - "case is not escalating to a manager after the required time has passed"
  - "how do I set up automatic case escalation after X hours"
  - "escalation rule is not firing or not sending email notifications"
  - "how to configure business hours so escalation only counts working hours"
  - "cases are being escalated even on weekends or outside business hours"
  - "how to reassign a case automatically when it is not resolved in time"
  - "wave of cases escalated all at once after we reactivated the escalation rule"
  - "escalation clock keeps resetting because a flow updates the case"
  - "deploy an escalation rule from sandbox without switching off the live one"
  - "find every case where IsEscalated is true and nobody followed up"
tags:
  - escalation-rules
  - case-management
  - business-hours
  - service-cloud
  - time-based-automation
inputs:
  - "The objects involved (always Case)"
  - "SLA requirements: how many hours before escalation fires"
  - "Whether escalation time should respect business hours or run 24/7"
  - "Escalation actions required: email notification targets, reassignment target (user, queue, or manager)"
  - "Case criteria for each escalation tier (priority, type, origin, etc.)"
  - "The name of the currently active escalation rule in the target org, and its owner"
outputs:
  - "Deployable escalationRules/Case.escalationRules-meta.xml with entries and staged actions"
  - "Business hours setup recommendation"
  - "Escalation configuration review checklist"
  - "Troubleshooting diagnosis for non-firing escalations"
  - "Cutover plan: deploy inactive, activate one rule, compare against the incumbent"
  - "Monitoring query and report definition for escalated cases"
dependencies: []
version: 1.1.2
author: Pranav Nagrecha
updated: 2026-09-12
---

# Escalation Rules

This skill activates when you need to configure, review, or troubleshoot Salesforce Case Escalation Rules — the declarative mechanism that automatically notifies stakeholders or reassigns cases when they are not resolved within a specified time window.

It owns the **design and operation** of the rule: entry criteria, staged action thresholds, engine behaviour, the cutover, and the monitoring that proves it still works. The calendar the entry points at belongs to `admin/business-hours-and-holidays`; the routing that put the case somewhere in the first place belongs to `admin/assignment-rules`.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Active rule limit:** Plan for one active escalation rule per org. If multiple rule configs exist, only the one marked Active fires. Confirm whether an active rule already exists before creating a new one. UNVERIFIED (2026-09-04): the Metadata API guide describes `escalationRule` as a repeating element "processed in the order they appear in the EscalationRules container" and gives each rule its own `active` flag; it does not state the one-active-rule ceiling, and help.salesforce.com cannot be fetched. Verify in the target org's Setup > Escalation Rules list before relying on it.
- **Processing cadence:** The time-based engine that drives escalation is not real time. A case that hits its threshold at 2:05 PM may not escalate until the next engine pass — plan SLA commitments accordingly. UNVERIFIED (2026-09-04): the widely-quoted "approximately every hour" cadence appears in no fetchable official source; treat the interval as "batched, not immediate" and measure it in your own org before promising a number.
- **Business hours dependency:** The Object Reference states it directly for the `BusinessHours` object — "Escalation rules are run only during these hours" — and adds that holidays attached to a calendar suspend both the hours and the escalation rules that use them. If no calendar is restricted, the org default is 24/7.
- **Who else writes `OwnerId`:** an escalation action that reassigns changes the case owner, which re-fires every record-triggered automation watching ownership. Inventory those before staging a reassign action.

---

## Questions to Ask Before Configuring

Ask these before opening Setup. Each one maps to a failure documented in `references/gotchas.md`, and an LLM that skips them produces a rule that deploys cleanly and escalates the wrong cases at the wrong time.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "Does the clock start at case creation, or restart every time anyone edits the case?" | `escalationStartTime` is `CaseCreation` or `CaseLastModified`; `disableEscalationWhenModified` is a separate lever that stops escalation on edit | The per-tier choice of both fields, and a list of the automations that count as an "edit" |
| "Which calendar does each tier follow, and is there a tier that must run 24/7?" | `businessHoursSource` is `None`, `Case`, or `Static` per entry — a per-Case calendar design is defeated by an entry left on `None` | One `businessHoursSource` value per entry, with the Sev-1 exception written down as a decision |
| "Which escalation rule is active in production today, and who owns it?" | Activating a new rule is a cutover, not an addition | The incumbent rule's name, its entries, and a named owner to sign off the swap |
| "When the timer expires, do we notify, change the owner, or both?" | Reassignment writes `OwnerId` and re-fires record automation; notify-only does not | A per-threshold action table, and the automation blast radius for any reassign action |
| "What is the SLA in minutes, and has anyone signed off on the engine's batching latency?" | `minutesToEscalation` is stored in minutes while Setup shows hours, and the engine fires in batches | An agreed minutes value with headroom, not an hours value transcribed as minutes |
| "How will we know next month that the rule still fires?" | `IsEscalated` is a plain writable boolean, not an engine-owned lock — nothing reports on a rule that quietly stopped | A saved report or query on escalated, still-open cases, with an owner and a cadence |
| "How do we cut over without a wave of instant escalations?" | Cases already past their threshold escalate on the first pass after activation | A deploy-inactive-then-activate plan with a defined comparison window |

What a proper configuration adds over just doing it: the timer measures the working time the SLA actually promised, the cutover is a comparison rather than a surprise, and someone is still looking at escalated cases a quarter later.

---

## Core Concepts

### How Escalation Rules Differ from Assignment Rules

Assignment rules route cases to users or queues **when a case is created or re-opened**. They fire once on creation.

Escalation rules operate on a **timer**: they fire when a case that matches defined criteria has been open for longer than a configured threshold. If a case is not resolved within X hours, escalation rules send notifications or reassign the case.

The two rules are complementary. Assignment routes the case on arrival; escalation follows up when response time is exceeded.

### Rule Structure: One Rule, Many Entries

A single active escalation rule contains multiple **rule entries**. In metadata each `ruleEntry` carries:

| Field | Type | What it controls |
|---|---|---|
| `criteriaItems` | FilterItem[] | Which cases the entry applies to (`field`, `operation`, `value`) |
| `formula` | string | Alternative to `criteriaItems` — "Specify either formula or criteriaItems, but not both fields" |
| `booleanFilter` | string | Advanced filter logic across the numbered `criteriaItems` |
| `businessHoursSource` | enum | `None`, `Case`, or `Static` |
| `businessHours` | string | The named calendar — "Specify only if businessHoursSource is set to Static" |
| `escalationStartTime` | enum | `CaseCreation` or `CaseLastModified` |
| `disableEscalationWhenModified` | boolean | Escalation is disabled when the record is modified |
| `escalationAction` | EscalationAction[] | The staged actions to perform when the criteria are met |

Entries are evaluated in order. The **first matching entry** wins — subsequent entries are skipped, just like assignment rule evaluation. Rules themselves are "processed in the order they appear in the EscalationRules container".

### Escalation Actions Are Staged Inside One Entry

Multi-tier escalation is built from several `escalationAction` elements inside a **single** entry, each with its own `minutesToEscalation`. It is not built from several entries — a case only ever matches one entry.

| Field | Meaning |
|---|---|
| `minutesToEscalation` | int, **minutes** — the guide's own sample uses `1440` for 24 hours |
| `notifyTo` | The user to notify |
| `notifyToTemplate` | Template for the notification email |
| `notifyEmail` | A free-form email address to notify |
| `notifyCaseOwner` | Boolean — notify the current owner |
| `assignedTo` | The user or queue the case is reassigned to (omit for notify-only) |
| `assignedToType` | `User` or `Queue` — meaningless without `assignedTo` |
| `assignedToTemplate` | Template for the email sent to the new owner; a Classic template, because "Lightning email templates aren't packageable" |

An action with no `assignedTo` is notification-only and is a legitimate first stage. An action with `assignedTo` writes `OwnerId`.

UNVERIFIED (2026-09-04): the commonly-cited ceiling of **5 escalation actions per entry** is not in the Metadata API guide's `EscalationAction` table and does not appear in the Salesforce App Limits cheat sheet (`grep -i escalation` returns nothing). `escalationAction` is typed as an unbounded array. Confirm the Setup-UI ceiling in your org before designing a fifth stage; `scripts/check_escalation_rules.py` reports the count as INFO rather than failing on it.

### Business Hours and the Escalation Clock

`businessHoursSource` decides per entry which clock runs:

| Value | Clock used |
|---|---|
| `None` | No calendar — wall-clock time, 24/7. Correct for Sev-1. |
| `Case` | The calendar on `Case.BusinessHoursId` (a writable reference field) |
| `Static` | The calendar named in `businessHours` on the entry, whatever the case says |

Two facts from the Object Reference's `BusinessHours` entry govern the result: escalation rules run only during the calendar's hours, and holidays associated with the calendar suspend those hours **and the escalation rules that use them**. Restricting the calendar is what makes off-hours pausing real — a calendar left at the shipped 24/7 default makes `Static` and `None` behave identically. Calendar design itself lives in `admin/business-hours-and-holidays`.

---

## Common Patterns

### Pattern: Tiered Escalation by Case Priority

**When to use:** Different SLA windows for different priorities. P1 cases escalate in 1 hour; P3 cases escalate in 8 hours.

**How it works:**
1. Create rule entries in priority order: P1 entry first, P2 next, P3 last.
2. Each entry uses field criteria `Priority = "P1"` (or P2, P3).
3. Set `minutesToEscalation` per stage: P1 = 60, P2 = 240, P3 = 480.
4. Add staged actions per tier: P1 notifies the manager at stage 1 and reassigns at stage 2.

**Catch:** Rule entries are evaluated top to bottom. Put P1 first, otherwise a P1 case might match a lower-tier entry if that entry has looser criteria.

### Pattern: Mixed Clocks in One Rule

**When to use:** Sev-1 must escalate at 3 AM Sunday; everything else must wait for the next working morning.

**How it works:** Give the Sev-1 entry `businessHoursSource` = `None` and the standard entries `businessHoursSource` = `Case` (or `Static` with a named calendar). The choice is per entry, so one rule carries both clocks. The full XML is in `references/metadata-examples.md`.

**Why not two rules:** a second rule is a cutover, not an addition — see the deploy-inactive pattern below.

### Pattern: Notify and Reassign at Different Thresholds

**When to use:** You want to warn the case owner at hour 2, then escalate to a queue at hour 4 if still unresolved.

**How it works:** Within a single rule entry, add two `escalationAction` elements:
- Action 1: `minutesToEscalation` 120 → `notifyCaseOwner` true, `notifyTo` the manager. No `assignedTo`.
- Action 2: `minutesToEscalation` 240 → `assignedTo` the escalation queue, `assignedToType` `Queue`, plus `notifyEmail`.

Both actions are attached to the same entry (same criteria). They fire as their thresholds are crossed.

### Pattern: Deploy Inactive, Then Cut Over

**When to use:** Replacing or materially changing the live rule in production.

**How it works:**
1. Deploy the new rule with `<active>false</active>` alongside the incumbent. Nothing changes in production.
2. Compare the two rules' entry criteria against a sample of live cases before switching.
3. Activate the new rule in a separate, small deploy, in a window where a wave of instant escalations is survivable.
4. Watch escalated-case volume for one full SLA period before deleting the old rule.

The step-by-step with XML and CLI is in `references/metadata-examples.md`.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Route case to agent on creation | Assignment Rule | Escalation only activates after time passes — it is not a routing tool for new cases |
| Fire when SLA time is exceeded | Escalation Rule | Purpose-built for time-based case follow-up |
| Clock should pause on weekends | `businessHoursSource` `Case` or `Static`, pointed at a restricted calendar | Escalation runs only during the calendar's hours |
| Sev-1 must ignore the calendar | `businessHoursSource` `None` on that entry | The choice is per entry, so it coexists with business-hours entries |
| Reset clock when agent responds | `escalationStartTime` `CaseLastModified` | The clock restarts on each update — including automation updates |
| Stop escalating once someone touches the case | `disableEscalationWhenModified` true | Disables escalation on modification instead of restarting the timer |
| Keep original owner but notify manager | Action with `notifyTo`/`notifyCaseOwner` and no `assignedTo` | Notification-only actions are valid |
| Multiple SLA tiers by priority | Multiple rule entries, ordered P1 first | First matching entry wins; put most specific criteria at top |
| Progressive escalation within one tier | Multiple `escalationAction` elements on one entry | A case matches one entry only; stages live inside it |
| Sub-hourly, guaranteed-precision SLA | Scheduled Flow or Apex Schedulable | The declarative engine is batched, not real time |
| Replacing the live rule | Deploy inactive, activate separately | Activation is a cutover with a possible escalation wave |

---

## Recommended Workflow

1. **Inventory the incumbent** — retrieve the org's current rules (`sf project retrieve start --metadata EscalationRules:Case`) and record which rule is active, its entries, and its owner. Answer the table in `## Questions to Ask Before Configuring` before designing anything.
2. **Design the tiers** — one entry per distinct clock-and-criteria combination, staged actions inside each entry; capture the design in `templates/escalation-rules-template.md` so the minutes, the calendar source, and the action targets are agreed before they are typed.
3. **Confirm the calendar** — check each entry's `businessHoursSource` against the calendar design in `admin/business-hours-and-holidays`; a `Case` source needs `Case.BusinessHoursId` populated at creation.
4. **Build as metadata** — shape `escalationRules/Case.escalationRules-meta.xml` from `references/metadata-examples.md`, with the new rule `<active>false</active>` for now.
5. **Lint** — run `python3 skills/admin/escalation-rules/scripts/check_escalation_rules.py --manifest-dir force-app/main/default`; it flags two active rules, a `Static` entry with no calendar, non-positive `minutesToEscalation`, `assignedTo` without `assignedToType`, a notified-but-templateless action (`notifyCaseOwner` or `notifyTo` with no `notifyToTemplate`), and catch-all entries.
6. **Test the clock** — reuse the after-hours clock test in `admin/business-hours-and-holidays` `references/examples.md` (Example 4) against a real case, then verify with the monitoring query in `references/metadata-examples.md`.
7. **Cut over and watch** — activate in its own deploy, then run the escalated-case monitoring query for one full SLA period; if nothing fired, work `references/gotchas.md` in order.

---

## Review Checklist

Run through these before marking escalation rule work complete:

- [ ] Exactly one rule in the file has `<active>true</active>`, and it is the one you intend
- [ ] Rule entries are ordered correctly — most specific criteria appear first
- [ ] Every `minutesToEscalation` is a positive integer expressed in **minutes**, cross-checked against the SLA in hours
- [ ] Each entry's `businessHoursSource` (`None` / `Case` / `Static`) is the intended one, and `businessHours` is present exactly when the source is `Static`
- [ ] `escalationStartTime` and `disableEscalationWhenModified` were chosen deliberately per entry, not left at defaults
- [ ] No entry sets both `criteriaItems` and `formula`
- [ ] Every action with `assignedTo` also sets `assignedToType`, and the target user or queue exists in the target org
- [ ] Every action with `notifyCaseOwner` true or a populated `notifyTo` also sets `notifyToTemplate` — the org rejects the deploy without it even though the guide does not mark it Required
- [ ] Email templates referenced by `notifyToTemplate` / `assignedToTemplate` exist, are Classic templates, and are named folder-qualified (`<folder>/<name>`)
- [ ] The record automation that watches `OwnerId` has been reviewed for any reassigning action
- [ ] A test case has been aged past the threshold and escalation fired as expected
- [ ] Entry criteria values match the actual field values used in the org
- [ ] The cutover was a deploy-inactive-then-activate, and escalated-case volume was watched afterwards
- [ ] A monitoring report or query on escalated, still-open cases exists and has an owner

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems. Full treatment in `references/gotchas.md`.

1. **The engine batches; it does not fire on the minute.** Do not sell minute-level SLA precision on a declarative escalation rule.
2. **Reactivating a rule can produce a wave.** Cases already past their threshold escalate on the first pass after activation.
3. **A 24/7 calendar makes the business-hours setting a no-op.** Restricting the calendar is the work; selecting it is not.
4. **`minutesToEscalation` is minutes; Setup shows hours.** A "4 hour" tier written as `4` escalates after four minutes.
5. **Reassignment writes `OwnerId`.** Every record-triggered automation on ownership fires again, hours after the case was created.
6. **Holidays on the calendar suspend the escalation rules that use it.** An unmaintained holiday list silently changes SLA behaviour a year later.
7. **`IsEscalated` is a plain writable boolean.** Anything with update access — a data load, a flow, an integration — can set or clear it.
8. **`notifyToTemplate` is required whenever the case owner or a named user is notified, but the guide never says so.** An action with `notifyCaseOwner` true and no `notifyToTemplate` deploys as valid XML and fails only at org validation.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `escalationRules/Case.escalationRules-meta.xml` | The deployable rule with ordered entries and staged actions |
| Business hours decision | Which `businessHoursSource` each entry uses, and why any entry is `None` |
| Cutover plan | Deploy-inactive, activate, compare, retire — with the watch window named |
| Escalation configuration review | Checklist confirming rule order, thresholds, action targets, and calendar wiring |
| Monitoring query / report | Escalated, still-open cases by owner and age, with a review cadence |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing or reviewing the deployable XML, package.xml, CLI, cutover, or monitoring query |
| `references/gotchas.md` | The escalation fired late, early, twice, or not at all |
| `references/examples.md` | You want two worked scenarios end to end, plus the multiple-active-rules anti-pattern |
| `references/well-architected.md` | Choosing declarative escalation over Flow/Apex, and the official sources behind the claims here |
| `references/llm-anti-patterns.md` | Self-checking generated escalation guidance before returning it |

---

## Related Skills

- admin/assignment-rules — initial routing; its `references/metadata-examples.md` holds the base EscalationRules shape and its `references/troubleshooting.md` step 5 covers ownership overwrites
- admin/business-hours-and-holidays — the calendar an entry consumes through `businessHoursSource`, and the after-hours clock test
- admin/case-management-setup — case intake, where `Case.BusinessHoursId` gets populated
- admin/entitlements-and-milestones — milestone timers, the other SLA clock; not the same engine
- architect/sla-design-and-escalation-matrix — the tier table and escalation matrix that decide what these entries should say
- admin/approval-processes — time-based routing for human decisions, not SLA escalation
