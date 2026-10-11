---
name: path-and-guidance
description: "Use when setting up, customizing, or troubleshooting the Salesforce Path component on Opportunity, Lead, Case, or custom objects. Triggers: 'add guidance to stages', 'key fields on path', 'celebrate closed won', 'path not showing', 'configure path steps', 'confetti on stage change'. NOT for Sales Process configuration, validation rules that enforce required fields, or Kanban board setup."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
triggers:
  - "how do I add guidance text to each stage on the opportunity"
  - "key fields are not showing on the path component"
  - "how do I enable confetti when a deal is closed won"
  - "path is not visible on the record page"
  - "I want to show different fields at each pipeline stage"
  - "how do I activate or deactivate a path"
tags:
  - path
  - guidance
  - key-fields
  - confetti
  - picklist
  - opportunity
  - user-experience
inputs:
  - "Target object (Opportunity, Lead, Case, or custom object)"
  - "Picklist field that drives the path stages"
  - "Record type (if record-type-specific path is needed)"
  - "Stages and the key fields or guidance content for each"
  - "Whether celebration confetti is required and on which stage"
outputs:
  - "Path configuration guidance (object, record type, picklist field selection)"
  - "Stage-level key field and guidance text recommendations"
  - "Confetti enablement and troubleshooting guidance"
  - "Path activation checklist"
  - "Lightning App Builder placement notes"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

You are a Salesforce Admin expert in Path configuration and user-experience design. Your goal is to help admins configure Path so that sales reps, service agents, and other end users always know what to do next at each stage — and feel rewarded when they hit key milestones.

---

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first. Only ask for information not already covered there.

Gather if not available:

- Which object needs a Path? Standard objects (Opportunity, Lead, Case, Account, Contact, Contract, Order, Quote) and most custom objects are supported. Not every object supports Path out of the box.
- Which picklist field should drive the stages? On Opportunity the default is Stage; on Lead it is Status. Only picklist fields (not multi-select or text) qualify.
- Is there more than one Record Type on this object? Paths can be record-type-specific, or set to apply to all record types.
- What key fields (up to 5 per stage) should be surfaced at each stage?
- Is there guidance text for any stage? Guidance is rich text and can include links, bullets, or images.
- Should confetti fire on a specific stage (e.g., Closed Won)? Confetti must be explicitly enabled per stage.

---

## Core Concepts

### What Path Is

Path is a standard Lightning Experience UI component that renders as a horizontal chevron bar across the top of a record page. Each chevron corresponds to one picklist value on the chosen field. The currently selected picklist value is highlighted. Below the bar, Path optionally surfaces up to five key fields and a rich-text guidance block specific to the active stage.

Path is not a workflow enforcement tool. It does not prevent stage skipping, enforce required fields, or lock records. It is a user-experience layer that helps users know what matters at each stage. Enforcement belongs in validation rules or Flow.

Path is supported on: Opportunity, Lead, Case, Account, Contact, Contract, Order, Quote, and custom objects with a picklist field. It is not available for all standard objects — check Path Settings in Setup for the current object list.

### Path Settings and Setup Location

Path is configured at **Setup > Path Settings**. From there you:

1. Enable Path for the org (top toggle).
2. Create individual Path records — one per object + record type + picklist field combination.
3. For each path, configure stages: select picklist values, define key fields per stage, and write guidance text.
4. Activate the path when ready.

A path does not appear on a record page until both the Path org setting is enabled AND the individual path record is active AND the Path component is present on the Lightning page (via Lightning App Builder or a standard page layout that includes it).

### Key Fields Per Stage

Each stage (picklist value) can expose up to five key fields below the chevron bar. These fields are read and editable directly in the Path panel — users do not need to scroll to the full field layout.

Field restrictions:

- Formula fields, roll-up summaries, and system fields (CreatedDate, LastModifiedDate, OwnerId as a lookup) can be added as read-only key fields.
- Long text area fields and encrypted fields cannot be added as key fields.
- Lookup fields can be added but display as read-only in the key fields panel unless the full inline edit experience supports them.
- The same field can appear as a key field on multiple stages.

Key fields are stage-specific. A field that is critical at Prospecting need not appear at Closed Won.

### Guidance Text Per Stage

Each stage supports a rich-text guidance block displayed below the key fields. Guidance text supports:

- Bullet and numbered lists
- Bold, italic, underline
- Hyperlinks to external resources or Salesforce records
- Images (linked externally, not embedded as binary)

Guidance text has a character limit of approximately 1,000 characters per stage. It cannot contain Apex or JavaScript. It is static — it does not personalize based on the record values.

### Celebration Confetti

Confetti is a visual animation that fires when a user manually moves the record to a specific stage using the "Mark Stage as Complete" or "Select Closed Stage" button in the Path component. Confetti must be enabled per stage in Path Settings.

Critical behavior:

- Confetti only fires when the stage change is made **through the Path component UI**. If the stage is changed via a picklist edit on the detail page, a Flow, an API call, or a quick action, confetti does NOT fire.
- Confetti fires once per stage change session — it does not loop.
- Confetti is purely cosmetic. It has no impact on record state, automation, or workflow.
- Confetti can be enabled on any stage, not just Closed Won.

### Multiple Paths Per Object

An object can have more than one active path as long as each path is differentiated by record type or picklist field. For example, an org might have:

- An Opportunity Path for the "Enterprise" record type using the Stage field.
- An Opportunity Path for the "SMB" record type using the Stage field with different key fields and guidance.

Both can be active simultaneously. Salesforce renders the correct path based on the record's record type.

### Path and Sales Process

Path stages are derived directly from the picklist field values — specifically, the values available to the selected record type. The Sales Process (configured separately under **Setup > Sales Processes**) controls which Stage picklist values appear on an Opportunity record type. Path reads those values. Changing a Sales Process changes which stages appear in the Path.

Path does NOT configure or replace the Sales Process. Admins sometimes confuse the two. Sales Process governs available values; Path governs guidance and key fields on those values.

### Lightning App Builder and Page Placement

The Path component is a standard Lightning component available in Lightning App Builder. It must be placed on the record Lightning page to appear. Default Lightning page templates for Opportunity, Lead, and Case often include Path out of the box. Custom pages must add it manually.

Placement recommendation: Path performs best at the very top of the record page, spanning full width, above all tabs and related lists. Placing it inside a tab or a narrow column degrades the chevron rendering.

### Mobile Considerations

Path is supported in the Salesforce Mobile App (iOS and Android). Key fields and guidance text are visible on mobile. The confetti animation is also supported on mobile. However, the mobile rendering compresses the chevron bar — long stage labels truncate. Keep stage names concise (under 20 characters ideally) for mobile readability.

### Admin Permissions

To configure Path, the admin needs:
- **Customize Application** permission to access Path Settings and create paths.
- **Modify All Data** is not strictly required for Path configuration itself, but is required to edit the picklist values the path depends on.

---

## Common Patterns

### Pattern 1: Opportunity Path with Stage-Specific Key Fields

**When to use:** Sales orgs where reps need different context at each deal stage — for example, MEDDIC fields at Qualification, decision makers at Proposal, and contract details at Negotiation/Review.

**How it works:**

1. Go to Setup > Path Settings. Enable Path.
2. Create a new path: Object = Opportunity, Field = Stage, Record Type = (target record type or All).
3. For each stage, click the stage chevron and add up to 5 key fields from the available field list. Pick fields reps actually need to fill in at that stage.
4. Write guidance text per stage: link to a playbook, list the exit criteria, name the required document.
5. Enable confetti on Closed Won.
6. Activate the path.
7. Confirm the Path component is on the Lightning page via Lightning App Builder.

**Why not alternatives:** Putting all fields on the main page layout forces reps to scroll and hunt. Path surfaces exactly what matters now, reducing cognitive load.

### Pattern 2: Case Path with Guidance-Only Stages

**When to use:** Service orgs where case handlers need procedural guidance at each status but do not need inline field editing — for example, "New: assign to the right queue", "Working: link to KB article", "Escalated: contact the customer within 4 hours".

**How it works:**

1. Create a path on Case using the Status picklist.
2. For each status, add only the guidance text block. Leave key fields empty if no inline editing is needed.
3. Link guidance text to internal runbooks or external Knowledge articles where appropriate.
4. Activate. No confetti needed on a case path in most scenarios.

**Why not alternatives:** A separate training document goes stale and is not contextual. Guidance in Path is always visible in context, reducing the need for supervisors to repeat procedural instructions.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Users need to see different fields at each stage | Add key fields per stage in Path Settings | Path surfaces them inline without layout clutter |
| Users need step-by-step instructions at a stage | Write guidance text for that stage | Rich text supports links, bullets, checklists |
| You want to celebrate a milestone stage | Enable confetti on that stage in Path Settings | Cosmetic reward, no automation side effects |
| Stage changes happen via API or Flow, not UI | Do not rely on confetti | Confetti only fires through Path component UI |
| Two record types need different key fields | Create two separate active paths, one per record type | Salesforce matches path to record type at runtime |
| A field cannot be added as a key field | Check if it is a long text area, formula, or encrypted field | Those types have restrictions; use read-only display only |
| Path component is not showing on the record page | Verify org Path toggle is on, path is Active, and component is on the Lightning page | All three must be true simultaneously |
| Admin wants to enforce fields at a stage | Use validation rules or Flow, not Path | Path is a UX aid, not an enforcement mechanism |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm prerequisites** — verify Lightning Experience is enabled, the org Path toggle is on in Setup > Path Settings, and you know the target object, picklist field, and record type.
2. **Inventory stages and content** — collect the list of picklist values in play, what key fields belong at each stage (up to 5), and any guidance text or links; confirm confetti stages.
3. **Create or edit the path** — in Setup > Path Settings, create the path record for the object + record type + picklist field combination; populate key fields and guidance per stage.
4. **Enable confetti where needed** — on the stage's detail view in Path Settings, toggle the Celebration confetti option; note that it only fires through the Path component UI.
5. **Activate the path** — toggle the path to Active; inactive paths do not render.
6. **Verify Lightning page placement** — open Lightning App Builder for the target record page; confirm the Path standard component is present, spanning full width at the top.
7. **Test end-to-end** — log in as a non-admin user, open a record of the target type, step through stages using the Path component, verify key fields and guidance appear correctly, and confirm confetti fires on the designated stage.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Org-level Path Settings toggle is enabled
- [ ] Path record targets the correct object, record type, and picklist field
- [ ] Key fields per stage reviewed — no long text area, encrypted, or unsupported field types added
- [ ] Guidance text per stage is under ~1,000 characters and contains no JavaScript
- [ ] Confetti enabled only on stages where stage change will happen through the Path UI (not via automation)
- [ ] Path status is Active
- [ ] Path component is on the Lightning record page, full-width at the top
- [ ] Tested as a non-admin user to confirm rendering and inline field edit behavior
- [ ] Mobile rendering checked if mobile is in scope

---

## Salesforce-Specific Gotchas

1. **Path toggle off means nothing renders** — If the org-level "Enable Path" toggle in Setup > Path Settings is off, no paths render anywhere, even if individual paths are active. This is the first thing to check when a path disappears after a deployment or scratch org refresh.
2. **Confetti requires the Path UI — automation moves won't trigger it** — Stage changes made by Flow, Process Builder, Apex, or direct API do not trigger the confetti animation. Only stage changes made through the Path component's "Mark Stage as Complete" button fire it. This is a frequent surprise when a Stage update Flow is introduced post-launch.
3. **Long text area fields silently fail to appear as key fields** — The Path Settings UI will not let you add a long text area field. If an admin assumes all field types are supported and designs guidance around a rich-text field appearing inline, it won't work. Use short text, number, currency, date, lookup (read-only), or checkbox fields for key fields.
4. **Sales Process controls the available stages, not Path** — If a stage is missing from the Path chevron bar, it is almost certainly missing from the Sales Process assigned to that Opportunity record type, not from the Path configuration. Editing Path will not surface a stage that is not in the underlying picklist values for that record type.
5. **Path is not a validation mechanism** — Admins sometimes configure key fields thinking that making a field visible in Path will make it required. It does not. Path is display-only guidance. Required field enforcement requires a validation rule.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Path configuration guidance | Object, record type, picklist field selection with activation checklist |
| Stage content plan | Key fields and guidance text per stage, formatted for entry into Path Settings |
| Confetti enablement notes | Which stages have confetti, with caveat about UI-only trigger behavior |
| Lightning App Builder placement note | Recommendation for component position on the record page |

---

## Related Skills

- **admin/approval-processes** — Use when stage changes need to trigger a formal approval or lock the record. Path does not enforce; Approval Processes do.
- **admin/validation-rules** — Use when you need to make key fields required at a specific stage. Path surfaces fields; validation rules enforce them.
- **admin/change-management-and-training** — Use when the real problem is adoption: users know what to do but don't do it. Path + In-App Guidance together solve contextual adoption gaps.
