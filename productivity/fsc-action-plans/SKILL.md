---
name: fsc-action-plans
description: "Use this skill when designing, building, or troubleshooting FSC Action Plan templates for client-facing task sequences such as client onboarding, account opening, annual review preparation, and compliance tasks. Trigger keywords: Action Plan template, ActionPlanTemplate, ActionPlan object, FSC task sequence, onboarding checklist, review prep tasks. NOT for standard Salesforce Tasks, Flow automation, or general task management outside of FSC Action Plan objects."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
  - Security
triggers:
  - "how do I create a reusable onboarding checklist for new FSC clients using Action Plan templates"
  - "my FSC action plan template is published and I need to update the task list without breaking in-progress plans"
  - "action plan tasks are not showing the correct due dates after the plan is launched from a financial account"
  - "how do I attach an action plan to a FinancialAccount or InsurancePolicy record in Financial Services Cloud"
  - "what FSC objects support Action Plan templates and how do I configure the template for compliance review tasks"
tags:
  - fsc-action-plans
  - financial-services-cloud
  - action-plan-template
  - client-onboarding
  - compliance-tasks
  - task-sequence
inputs:
  - FSC org with Action Plans feature enabled (Financial Services Cloud license required)
  - List of task names, responsible roles, and deadline offsets (calendar or working days)
  - Target object type (FinancialAccount, FinancialGoal, InsurancePolicy, ResidentialLoanApplication, PersonLifeEvent, BusinessMilestone, or standard objects like Account/Contact/Opportunity/Lead/Contract/Case/Campaign)
  - Whether deadlines should be computed from plan start date using calendar days or working days
  - Compliance or regulatory context driving task sequence design
outputs:
  - Published ActionPlanTemplate with versioned task sequence
  - Configuration guidance for launching Action Plans from FSC object records
  - Deadline offset configuration for each ActionPlanTemplateItem
  - Clone-and-republish versioning strategy for template updates
  - Validation checklist for plan launches and task assignment
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# FSC Action Plans

This skill activates when a practitioner needs to design or maintain versioned reusable task sequences in Financial Services Cloud using Action Plan templates — for use cases such as client onboarding, account opening, annual review preparation, compliance documentation, or milestone-driven task coordination. It does NOT cover standard Salesforce Tasks, Flow-based task creation, or task management outside of the ActionPlanTemplate/ActionPlan object model.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the org has Financial Services Cloud enabled and the Action Plans feature is active. Action Plans require FSC and are available via the ActionPlanTemplate and ActionPlan standard objects introduced in API v44.0 (Winter '19).
- Identify the target object type. FSC extends Action Plan support beyond standard objects (Account, Contact, Opportunity, Lead, Contract, Case, Campaign) to FSC-specific objects: FinancialAccount, FinancialGoal, InsurancePolicy, ResidentialLoanApplication, PersonLifeEvent, and BusinessMilestone.
- Determine the deadline calculation mode. Each ActionPlanTemplateItem has a `DaysFromStart` field; the template itself has a `TaskDeadlineType` that controls whether deadlines count calendar days or working days from the plan start date.
- The most common wrong assumption: admins assume they can edit a published template in place and have changes propagate to in-flight plans. Published templates are immutable — changes require a clone-and-republish workflow, and existing plan instances are unaffected by the new version.
- Platform limit to be aware of: an Action Plan can contain up to 75 task items. This is a hard platform limit, not a soft warning.

---

## Core Concepts

### ActionPlanTemplate and ActionPlanTemplateItem Objects

An `ActionPlanTemplate` is the master blueprint for a reusable task sequence. It holds metadata such as the name, description, the target object type (`TargetEntityType`), and the deadline calculation mode (`TaskDeadlineType`: `Calendar` or `BusinessDays`). Each individual task within the template is an `ActionPlanTemplateItem` record linked to the template. The item stores the task subject, assigned-to rule, `DaysFromStart` offset, priority, and whether the task is required.

When an admin or automated process launches an Action Plan from a record, Salesforce creates an `ActionPlan` instance linked to that record and generates `ActionPlanItem` records for each task, computing absolute due dates from the plan's `StartDate` plus the `DaysFromStart` offset.

### Template Publishing and Immutability

Templates have a `Status` picklist: `Draft` and `Active`. Only `Active` (published) templates can be used to launch plans. Once a template is published (`Status = Active`), Salesforce treats it as immutable — the template record and its items cannot be directly edited via the UI or API without cloning. The correct versioning workflow is: clone the active template (creates a new Draft), modify the clone, then publish the clone. The original template remains active and continues to back any in-flight plans. In-progress plans launched from the old template version are never retroactively updated.

### FSC-Specific Object Support

Standard Salesforce Action Plans only support Account, Contact, Opportunity, Lead, Contract, Case, and Campaign as target objects. FSC extends this to include: FinancialAccount, FinancialGoal, InsurancePolicy, ResidentialLoanApplication, PersonLifeEvent, and BusinessMilestone. When configuring a template for an FSC object, the `TargetEntityType` field on ActionPlanTemplate must be set to the correct API name. Templates configured for one object type cannot be launched against a different object type.

### Deadline Calculation

`TaskDeadlineType` on the template controls deadline math. `Calendar` counts all days including weekends and holidays from the plan start date. `BusinessDays` skips weekends (Saturday and Sunday) but does not automatically skip org-configured holidays. If the use case involves regulatory deadlines that must account for business days, use `BusinessDays`. If the deadline is calendar-based (e.g., 30-day annual review window), use `Calendar`. `DaysFromStart` on each item can be zero (same day as plan start) or positive. Negative values are not supported.

---

## Common Patterns

### Client Onboarding Template for FinancialAccount

**When to use:** A new financial account has been opened and a standard set of onboarding tasks must be assigned to a relationship manager and compliance officer with deadlines staggered across the first 30 days.

**How it works:**
1. Create an ActionPlanTemplate with `TargetEntityType = FinancialAccount`, `TaskDeadlineType = BusinessDays`, Status = `Draft`.
2. Add ActionPlanTemplateItem records for each task (e.g., "Send welcome packet" at DaysFromStart=1, "Verify KYC documentation" at DaysFromStart=3, "Schedule introductory call" at DaysFromStart=2, "Confirm beneficiary designations" at DaysFromStart=10, "Submit account to compliance review" at DaysFromStart=15).
3. Set `AssignedTo` on each item to the appropriate queue, role, or user. For dynamic assignment, use a named queue so the plan launcher can override at launch time.
4. Publish the template by setting Status = `Active`.
5. From any FinancialAccount record, use the Action Plans related list or the "New Action Plan" button to launch a plan instance, select the published template, and set the plan start date.

**Why not the alternative:** Using Flow to create Tasks independently loses the grouped visibility of an Action Plan, has no deadline-offset calculation built in, and cannot be versioned as a template unit.

### Compliance Annual Review Template for Existing Clients

**When to use:** Regulatory requirement mandates an annual review checklist to be completed on every client account before a specified date, with tasks assigned across advisor, compliance, and operations teams.

**How it works:**
1. Create an ActionPlanTemplate targeting the Account or FinancialAccount object with `TaskDeadlineType = Calendar`.
2. Add items representing each compliance step: "Pull account statement", "Review suitability questionnaire", "Document risk tolerance update", "Advisor sign-off", "Compliance officer sign-off", "File regulatory report". Set DaysFromStart to stagger tasks so downstream tasks have realistic lead time.
3. Use a Required flag on critical items (e.g., compliance sign-off) so the plan cannot be marked complete without those tasks being closed.
4. Clone and publish an updated version at the start of each review cycle if the task list changes year-over-year.
5. Use a report or list view on ActionPlan filtered by TemplateId and Status to monitor completion rates across all clients.

**Why not the alternative:** Manually creating tasks per client per review cycle is error-prone, non-auditable, and lacks the grouped tracking that Action Plans provide.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to update a task in a published template | Clone template, edit clone, publish clone | Published templates are immutable; editing in place is blocked by the platform |
| Existing in-flight plans after template update | Leave them against the old version | In-flight plans are bound to the version at launch time; no retroactive update |
| Deadline must skip weekends | Set TaskDeadlineType = BusinessDays | Calendar mode counts all 7 days; BusinessDays skips Sat/Sun |
| Target object is InsurancePolicy | Set TargetEntityType = InsurancePolicy | FSC extends standard object support; verify FSC feature is enabled |
| Task count approaches 75 | Split into two sequential templates | 75 is a hard limit per plan; launching a second plan from a process is the correct workaround |
| Need to assign tasks to a team not known at template design time | Use a queue as AssignedTo on the template item | Queues allow launchers to re-assign at plan-launch time without modifying the template |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm prerequisites** — Verify the org has FSC enabled and the Action Plans feature is active. Check that the target object type is supported (FSC or standard). Confirm the requester has the "Manage Action Plans" or system administrator permission.
2. **Design the task sequence** — Gather the full list of task names, assigned roles or queues, relative deadlines (DaysFromStart), priority, and required vs. optional flags. Confirm whether deadline calculation should be Calendar or BusinessDays.
3. **Create the template in Draft status** — In Setup or declaratively via the ActionPlanTemplate API, create the template with the correct TargetEntityType and TaskDeadlineType. Add all ActionPlanTemplateItem records with correct DaysFromStart offsets.
4. **Review and publish** — Have a second admin or compliance stakeholder review the draft template. Publish by setting Status = Active. Document the template Id and version in your release notes.
5. **Test with a plan launch** — Launch a plan instance from a test record of the target object type. Verify all tasks appear with correct due dates, correct assignments, and correct required flags.
6. **Establish a versioning convention** — Adopt a naming convention such as `[Use Case] v[N]` (e.g., "Client Onboarding v2") so teams can identify the active version. When updates are needed, clone, modify, and publish under the next version name; do not delete the prior version until all in-flight plans on it are closed.
7. **Monitor plan completion** — Create a report on ActionPlan filtered by template and status to track incomplete plans across the book of business.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] TargetEntityType on ActionPlanTemplate matches the intended FSC or standard object
- [ ] TaskDeadlineType is set correctly (Calendar vs. BusinessDays) for the regulatory context
- [ ] All ActionPlanTemplateItem records have a non-negative DaysFromStart and a valid AssignedTo
- [ ] Template Status is Active before attempting to launch any plan
- [ ] Test plan launched from a real target object record with correct due-date computation verified
- [ ] Versioning convention documented; prior template not deleted if in-flight plans exist
- [ ] Task count is under the 75-item platform limit

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Published templates cannot be edited** — Once an ActionPlanTemplate Status is set to Active, the record and all its ActionPlanTemplateItem children are locked. Attempting to edit via UI or API returns an error. The only path forward is to clone the active template, edit the clone (which starts in Draft), and publish the clone. This is the canonical FSC versioning pattern.
2. **In-flight plans do not inherit template updates** — Existing ActionPlan instances are bound to the version of the template at launch time. Publishing a new template version (via clone-and-publish) does not retroactively update in-progress plans or recalculate task due dates on open plans.
3. **FSC object support requires FSC feature** — TargetEntityType values like FinancialAccount, InsurancePolicy, or ResidentialLoanApplication are only available if the Financial Services Cloud managed package or core FSC license is active. In an org without FSC, these values are absent from the picklist.
4. **BusinessDays does not skip holidays** — The BusinessDays deadline mode skips Saturday and Sunday only. It does not automatically skip org-configured holidays. Teams expecting holiday-aware deadlines must account for this manually or build post-launch correction logic.
5. **75-task hard limit per plan** — Each ActionPlan can contain a maximum of 75 ActionPlanItem records. Exceeding this at template design time causes the plan launch to fail. For complex onboarding workflows exceeding 75 steps, the correct pattern is to split into two sequenced templates (e.g., Phase 1 and Phase 2), launching the second plan upon completion of the first.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Published ActionPlanTemplate | The active versioned template backing one or more plan launches |
| ActionPlanTemplateItem list | Per-task configuration with DaysFromStart, AssignedTo, and Required flag |
| ActionPlan report | Report on ActionPlan object filtered by template and status for monitoring |
| Clone-and-republish runbook | Step-by-step procedure for safely updating a published template |

---

## Related Skills

- admin/financial-account-setup — Covers the FinancialAccount object data model and configuration; use alongside this skill when action plans target FinancialAccount records and field-level setup is also required.
- admin/compliance-documentation-requirements — Covers regulatory documentation requirements; use to determine which tasks must appear in compliance-driven Action Plan templates.
- admin/client-onboarding-design — Covers the broader FSC onboarding process design; Action Plan templates are the task-execution layer within that broader workflow.
