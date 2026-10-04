---
name: path-and-guidance
description: "Use when setting up, customizing, or troubleshooting the Salesforce Path component on Opportunity, Lead, Case, or custom objects. Triggers: 'add guidance to stages', 'key fields on path', 'celebrate closed won', 'path not showing', 'configure path steps', 'confetti on stage change'. NOT for creating the stage picklist — use admin/opportunity-management. NOT for in-app prompts — use admin/in-app-guidance-and-walkthroughs. Metadata: PathAssistant, PathAssistantStep, PathAssistantSettings, pathAssistantEnabled, canOverrideAutoPathCollapseWithUserPref, runtime_sales_pathassistant:pathAssistant, picklistValueName, recordTypeName, BusinessProcess."
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
  - "path deployed to production but does not render anywhere"
  - "deploy pathassistant metadata to another org"
  - "path shows collapsed by default and users never see the guidance"
  - "path chevron missing a stage that exists in the picklist"
  - "confetti setting disappeared after deployment"
  - "can I have two paths on the same object"
  - "change the record type or driver field on an existing path"
  - "path renders in sandbox but not in the scratch org"
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
version: 1.1.2
author: Pranav Nagrecha
updated: 2026-09-19
---

You are a Salesforce Admin expert in Path configuration and user-experience design. Your goal is to help admins configure Path so that sales reps, service agents, and other end users always know what to do next at each stage — and feel rewarded when they hit key milestones.

---

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first. Only ask for information not already covered there.

Gather if not available:

- Which object needs a Path? Standard objects (Opportunity, Lead, Case, Account, Contact, Contract, Order, Quote) and most custom objects are supported. Not every object supports Path out of the box.
- Which picklist field should drive the stages? On Opportunity the default is Stage; on Lead it is Status. Only picklist fields (not multi-select or text) qualify.
- How many Record Types does this object have? Exactly one path exists per record type per object — the UI's "All Record Types" is the `Master` record type and occupies that object's single Master slot (api_meta.txt L94496). Count the record types; that is the number of path files.
- What key fields should be surfaced at each stage, and do they all exist on this object? `fieldNames` names fields on `entityName` only — no cross-object dotted references (api_meta.txt L94545). The commonly cited cap is five per stage; see the marked note under Key Fields Per Stage.
- Is there guidance text for any stage? Guidance is rich text and can include links, bullets, or images.
- Should confetti fire on a specific stage (e.g., Closed Won)? Confetti is enabled per stage in Setup and is not represented in `PathAssistant` metadata, so plan the manual re-enable step for every org it is promoted to.

---

## Questions to Ask Before Configuring

Ask these before opening Path Settings. Each one maps to a failure mode in `references/gotchas.md`; skipping them produces a path that deploys green and renders nothing, or renders and teaches the wrong thing.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "How many record types does this object have, and does each one need different guidance?" | Exactly one path can exist per record type per object, including `__Master__` (api_meta.txt L94496) — record type is the only differentiator available | The file count: one `.pathAssistant-meta.xml` per record type, each with an owner |
| "Is the driver picklist final, or are stage values still moving?" | `fieldName` and `recordTypeName` are not updateable (api_meta.txt L94515, L94521, L94529); re-pointing a path is delete-and-recreate | Whether to build now or wait for `admin/opportunity-management` to settle the stage model first |
| "Which edition is every target org, including scratch orgs?" | `pathAssistantEnabled` defaults to `true` only in Enterprise Edition (api_meta.txt L124222–124224), and a path deploys fine into an org where Path is off | `settings/PathAssistant.settings-meta.xml` in the package instead of a manual Setup step per org |
| "Does anyone need to see the guidance without clicking?" | The path loads collapsed unless `canOverrideAutoPathCollapseWithUserPref` is true — default false for all editions (api_meta.txt L124216–124221) | A decision on the org-wide expand preference before adoption is measured |
| "Who advances the stage — a person in the UI, or automation?" | Celebration is a UI interaction reward, and it has no element in `PathAssistant` at all, so it never travels with a deploy | Either a celebration stage a human actually clicks through, or an honest "no celebration" and a Flow-based congratulation instead |
| "Which of these key fields must be filled, versus merely visible?" | Path displays; it does not enforce. The must-fill list is a validation-rule backlog, not a Path backlog | A hand-off list for `admin/validation-rules` written at the same time as the guidance |
| "Which Lightning record page will render this, and what template is it built on?" | The component is `runtime_sales_pathassistant:pathAssistant` in the `subheader` region (api_meta.txt L67766–67779, L67993–67996); a template without that region has nowhere to put it | The `FlexiPage` that must ship in the same package, named before the deploy is built |

What a proper configuration adds over just creating a path in Setup: the path, its record type, its stage values, the org preference, and the Lightning page all travel as one reviewable package, so the guidance a rep sees in production is the guidance that was written and approved — not whatever survived a partial deploy.

---

## Core Concepts

### What Path Is

Path is a standard Lightning Experience UI component that renders as a horizontal chevron bar across the top of a record page. Each chevron corresponds to one picklist value on the chosen field. The currently selected picklist value is highlighted. Below the bar, Path optionally surfaces up to five key fields and a rich-text guidance block specific to the active stage.

Path is not a workflow enforcement tool. It does not prevent stage skipping, enforce required fields, or lock records. It is a user-experience layer that helps users know what matters at each stage. Enforcement belongs in validation rules or Flow.

Path is supported on: Opportunity, Lead, Case, Account, Contact, Contract, Order, Quote, and custom objects with a picklist field. It is not available for all standard objects — check Path Settings in Setup for the current object list. UNVERIFIED (2026-09-05): the Metadata API guide names only Opportunity, Lead, and Quote as objects where `entityName` and `fieldName` are hard coded, plus custom objects where both must be specified (api_meta.txt L94513–94521). That is a statement about the metadata field, not an exhaustive support list, and the extracted guides do not enumerate the rest — confirm the object picker in Setup > Path Settings before designing for Account, Contact, Contract, or Order.

### Path Settings and Setup Location

Path is configured at **Setup > Path Settings**. From there you:

1. Enable Path for the org (top toggle).
2. Create individual Path records — one per object + record type + picklist field combination.
3. For each path, configure stages: select picklist values, define key fields per stage, and write guidance text.
4. Activate the path when ready.

A path does not appear on a record page until both the Path org setting is enabled AND the individual path record is active AND the Path component is present on the Lightning page (via Lightning App Builder or a standard page layout that includes it).

### Key Fields Per Stage

Each stage (picklist value) can expose up to five key fields below the chevron bar. UNVERIFIED (2026-09-05): the five-field cap is not stated in the Metadata API guide — `fieldNames` is documented only as "All the fields in entityName that will display in this step" (api_meta.txt L94545) — and the Developer Limits and Allocations Quick Reference contains no Path entry at all. `scripts/check_path_and_guidance.py` reports counts above five as a NOTE, not an error. These fields are read and editable directly in the Path panel — users do not need to scroll to the full field layout.

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

Guidance text is the `info` element of a `PathAssistantStep`, described in the guide only as "The guidance information displayed in this step" (api_meta.txt L94547). It cannot contain Apex or JavaScript. It is static — it does not personalize based on the record values. UNVERIFIED (2026-09-05): no character limit for `info` appears in the Metadata API guide, the Object Reference, or the limits cheat sheet. Prior SfSkills content has carried ~1,000 characters and `agents/path-designer/AGENT.md` states ~5,000; neither figure is grounded, and they contradict each other. Treat the practical ceiling as a readability judgement (a scannable list, not prose) until it is confirmed in an org.

Rich text guidance carries one documented deployment constraint: it "cannot be retrieved or deployed from or to translation workbench" (api_meta.txt L94497). Multilingual orgs cannot translate guidance through the usual route.

### Celebration Confetti

Confetti is a visual animation that fires when a user manually moves the record to a specific stage using the "Mark Stage as Complete" or "Select Closed Stage" button in the Path component. Confetti must be enabled per stage in Path Settings.

Critical behavior:

- Confetti only fires when the stage change is made **through the Path component UI**. If the stage is changed via a picklist edit on the detail page, a Flow, an API call, or a quick action, confetti does NOT fire.
- Confetti fires once per stage change session — it does not loop.
- Confetti is purely cosmetic. It has no impact on record state, automation, or workflow.
- Confetti can be enabled on any stage, not just Closed Won.
- Celebration has **no element in the `PathAssistant` metadata type**. The field tables are exactly `active`, `entityName`, `fieldName`, `masterLabel`, `pathAssistantSteps`, `recordTypeName`, and per step `fieldNames`, `info`, `picklistValueName` (api_meta.txt L94510–94529, L94545–94549). Celebration therefore does not travel with a deploy and must be re-enabled by hand in every org — see `references/gotchas.md` Gotcha 8.

UNVERIFIED (2026-09-05): the UI-only firing behaviour above is not stated in any of the extracted guides — it is retained from prior skill content. The only `enableConfettiEffect` field in the Metadata API belongs to `TrailheadSettings` and governs Guidance Center milestones, an unrelated feature (api_meta.txt L127903–127906); do not reach for it.

### One Path Per Record Type — Record Type Is the Only Differentiator

The guide states the constraint directly: "Only one path can be created per record type for each object, including `__Master__` record type" (api_meta.txt L94496). So an org can have:

- An Opportunity path for the `Enterprise` record type.
- A second Opportunity path for the `SMB` record type, with different key fields and guidance.

Both are active simultaneously and Salesforce renders the one matching the record's record type. What is **not** available: two paths on the same object and record type differentiated by driver picklist field, by profile, or by permission set. The pair `(entityName, recordTypeName)` is the unique key, and `fieldName` is not part of it. `scripts/check_path_and_guidance.py` fails a manifest that ships two paths against the same pair.

### Path and Sales Process

Path stages are derived directly from the picklist field values — specifically, the values available to the selected record type. The Sales Process (configured separately under **Setup > Sales Processes**) controls which Stage picklist values appear on an Opportunity record type. Path reads those values. Changing a Sales Process changes which stages appear in the Path.

Path does NOT configure or replace the Sales Process. Admins sometimes confuse the two. Sales Process governs available values; Path governs guidance and key fields on those values.

In metadata the Sales Process is the `BusinessProcess` type, defined inside the object definition rather than as a standalone file (api_meta.txt L42969), and bound by `RecordType.businessProcess` using the bare process name — never the object-qualified form (api_meta.txt L45006–45012). `RecordType.businessProcess` is required for lead, opportunity, solution, and case record types. `references/metadata-examples.md` § 1 shows the object file with both the business process and the record type's `picklistValues` block, which is the pairing a Path step's `picklistValueName` is validated against.

### Lightning App Builder and Page Placement

The Path component is a standard Lightning component available in Lightning App Builder. It must be placed on the record Lightning page to appear. Default Lightning page templates for Opportunity, Lead, and Case often include Path out of the box. Custom pages must add it manually.

Placement recommendation: Path performs best at the very top of the record page, spanning full width, above all tabs and related lists. Placing it inside a tab or a narrow column degrades the chevron rendering.

In `FlexiPage` metadata the component is `runtime_sales_pathassistant:pathAssistant`, placed in the region named `subheader` on a page built from the `flexipage:recordHomeWithSubheaderTemplateDesktop` template, with properties `hideUpdateButton` and `variant` (api_meta.txt L67766–67779, L67993–67996). Grep a retrieved `.flexipage-meta.xml` for that component name — its absence, not the path configuration, is the usual reason a correctly built path shows nothing.

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
| Two audiences on the *same* record type need different guidance | Add a record type, or move the audience-specific content to In-App Guidance | Only one path per record type per object (api_meta.txt L94496); profile is not a Path dimension |
| The driver field or record type must change on a live path | Delete the path and create a new one | `entityName`, `fieldName`, `recordTypeName` are not updateable (api_meta.txt L94515, L94521, L94529) |
| Promoting a configured path to another org | Ship path + object file + `Settings:PathAssistant` + `FlexiPage` together, then re-enable celebration by hand | The preference need not be on to deploy the path (api_meta.txt L94498), and celebration has no metadata element |
| Users say the guidance is never visible | Check `canOverrideAutoPathCollapseWithUserPref`, then `User.UserPreferencesPathAssistantCollapsed` | Collapsed-on-load is the default for all editions (api_meta.txt L124216–124221), and the per-user override is a queryable field |

---

## Recommended Workflow

1. **Establish the value universe before the guidance.** Retrieve the object's record types, business process, and value set — `sf project retrieve start --metadata "RecordType:<Object>.<RT>" --metadata "BusinessProcess:<Object>.<Process>" --metadata "StandardValueSet:OpportunityStage"` — and list what the record type actually exposes with `SELECT ApiName, MasterLabel, IsActive, SortOrder FROM OpportunityStage ORDER BY SortOrder`. Every step you are about to write must name one of those strings exactly. `references/metadata-examples.md` § 1 and § 7 show both.
2. **Fill in `templates/path-and-guidance-template.md`.** One row per stage: key fields, guidance summary, celebration flag, owner. Answer the Questions to Ask table above into the Context Gathered block — particularly the record-type count, which decides how many path files you are writing.
3. **Inventory what already exists before adding.** `sf project retrieve start --metadata "PathAssistant:*"` — `PathAssistant` supports the wildcard (api_meta.txt L94614–94615). If a path already binds this object and record type, you are editing it, not adding one (Gotcha 9). If it binds a different driver field than you want, that is a delete-and-recreate (Gotcha 7).
4. **Write the four files, not one.** The `.pathAssistant-meta.xml`, the object file carrying the business process and record type `picklistValues`, `settings/PathAssistant.settings-meta.xml` with `pathAssistantEnabled` and `canOverrideAutoPathCollapseWithUserPref` both explicitly `true`, and the `FlexiPage` containing `runtime_sales_pathassistant:pathAssistant`. Copy the shapes from `references/metadata-examples.md`.
5. **Run the checker against the manifest before deploying:** `python3 scripts/check_path_and_guidance.py --manifest-dir force-app/main/default`. It resolves every `picklistValueName` against the record type, business process, or value set in the same tree, verifies custom `fieldNames` exist on `entityName`, and fails a manifest with two paths on one object + record type pair. Fix every ISSUE; read every NOTE.
6. **Validate, then deploy in dependency order** — value set, fields, object file, path, settings and FlexiPage last (`references/metadata-examples.md` § 6). `sf project deploy validate` first; a green validate still tells you nothing about whether the path will *render*, which is why step 7 exists.
7. **Verify as a non-admin, then verify the three queries.** Open a record of the target type: chevrons present, key fields editable, guidance expanded on load. Then run the `OpportunityStage`, `RecordType.BusinessProcessId`, and `User.UserPreferencesPathAssistantCollapsed` checks in `references/metadata-examples.md` § 7 — those three cover the failures that look identical from the UI. Re-enable celebration by hand and record it in the template's Deviations section, because it did not deploy.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] `settings/PathAssistant.settings-meta.xml` is in the package with `pathAssistantEnabled` explicitly `true` — not left to the edition default
- [ ] `canOverrideAutoPathCollapseWithUserPref` is `true`, or the collapsed-on-load behaviour is a deliberate decision
- [ ] `entityName`, `fieldName`, and `recordTypeName` match the intended binding — they cannot be changed later
- [ ] Exactly one path exists per object + record type pair across the whole package
- [ ] Every `picklistValueName` matches a value the record type exposes, checked against `SELECT ApiName, IsActive FROM OpportunityStage`
- [ ] Every custom `fieldNames` entry exists on `entityName`; no long text area, encrypted, or unsupported field types added
- [ ] Guidance text per stage is scannable and contains no JavaScript; no translation-workbench dependency assumed
- [ ] Confetti enabled only on stages where the change happens through the Path UI — and on the manual post-deploy checklist, because it does not deploy
- [ ] `active` is `true` and every configured step carries either key fields or guidance
- [ ] The target `FlexiPage` contains `runtime_sales_pathassistant:pathAssistant`, and the page is in the same package
- [ ] `python3 scripts/check_path_and_guidance.py --manifest-dir <dir>` reports no ISSUE lines
- [ ] Tested as a non-admin user to confirm rendering and inline field edit behavior
- [ ] Mobile rendering checked if mobile is in scope

---

## Salesforce-Specific Gotchas

1. **Path toggle off means nothing renders** — If the org-level "Enable Path" toggle in Setup > Path Settings is off, no paths render anywhere, even if individual paths are active. This is the first thing to check when a path disappears after a deployment or scratch org refresh.
2. **Confetti requires the Path UI — automation moves won't trigger it** — Stage changes made by Flow, Process Builder, Apex, or direct API do not trigger the confetti animation. Only stage changes made through the Path component's "Mark Stage as Complete" button fire it. This is a frequent surprise when a Stage update Flow is introduced post-launch.
3. **Long text area fields silently fail to appear as key fields** — The Path Settings UI will not let you add a long text area field. If an admin assumes all field types are supported and designs guidance around a rich-text field appearing inline, it won't work. Use short text, number, currency, date, lookup (read-only), or checkbox fields for key fields.
4. **Sales Process controls the available stages, not Path** — If a stage is missing from the Path chevron bar, it is almost certainly missing from the Sales Process assigned to that Opportunity record type, not from the Path configuration. Editing Path will not surface a stage that is not in the underlying picklist values for that record type.
5. **Path is not a validation mechanism** — Admins sometimes configure key fields thinking that making a field visible in Path will make it required. It does not. Path is display-only guidance. Required field enforcement requires a validation rule.
6. **A deploy into a non-Enterprise org lands silently off** — `pathAssistantEnabled` defaults to `false` outside Enterprise Edition (api_meta.txt L124222–124224), and the guide notes the preference "does not need to be on to retrieve or deploy PathAssistant" (api_meta.txt L94498). Ship `Settings:PathAssistant` in the package rather than inheriting the default.
7. **Celebration never travels with the metadata** — there is no celebration element in `PathAssistant` or `PathAssistantStep`. Every promotion needs a manual re-enable step.
8. **A step you delete from the XML is not a stage you removed** — "a missing step in the .xml file means it has not been configured, not that it doesn't exist" (api_meta.txt L94525–94526). The chevron stays; only the guidance goes.
9. **`entityName`, `fieldName`, and `recordTypeName` cannot be updated** (api_meta.txt L94515, L94521, L94529). Changing any of them is a destructive change plus a new path.
10. **The path loads collapsed by default in every edition** — `canOverrideAutoPathCollapseWithUserPref` defaults to `false` (api_meta.txt L124216–124221), so the guidance is one click away on every record until you ship it as `true`.

Full detail, with the failure mode and the avoidance for each, is in `references/gotchas.md` (13 gotchas).

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Path configuration guidance | Object, record type, picklist field selection with activation checklist |
| Stage content plan | Key fields and guidance text per stage, formatted for entry into Path Settings |
| Confetti enablement notes | Which stages have confetti, with caveat about UI-only trigger behavior |
| Lightning App Builder placement note | Recommendation for component position on the record page |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/metadata-examples.md` | Writing deployable `PathAssistant`, `BusinessProcess` + `RecordType`, `StandardValueSet`, `PathAssistantSettings` and `FlexiPage` XML — plus the package.xml, the split-deploy order, and the three post-deploy SOQL verifications |
| `references/gotchas.md` | The path deployed cleanly and shows nothing, shows collapsed, lost its celebration, has holes in the chevron bar, or refuses to be re-pointed at a different record type |
| `references/examples.md` | Designing stage content before any XML exists — a MEDDIC Opportunity path and a Case status path, end to end, plus the two anti-patterns that produce them wrongly |
| `references/well-architected.md` | Justifying the tradeoff between richer guidance and maintenance load, or locating the official source behind a claim in this skill |
| `references/llm-anti-patterns.md` | Reviewing Path advice an AI assistant produced — especially "add it as a key field so it becomes required" and any claim that celebration deploys |
| `templates/path-and-guidance-template.md` | Running workflow step 2 — the stage content plan and the context gathering that precedes it |
| `scripts/check_path_and_guidance.py` | Workflow step 5, before every deploy that touches a path |

---

## Related Skills

- **admin/approval-processes** — Use when stage changes need to trigger a formal approval or lock the record. Path does not enforce; Approval Processes do.
- **admin/validation-rules** — Use when you need to make key fields required at a specific stage. Path surfaces fields; validation rules enforce them.
- **admin/change-management-and-training** — Use when the real problem is adoption: users know what to do but don't do it. Path + In-App Guidance together solve contextual adoption gaps.
- **admin/record-types-and-page-layouts** — Use before building the path. Record type is the only thing Path can differentiate on, and the record type's `picklistValues` block decides which chevrons exist.
- **admin/picklist-and-value-sets** — Use when a stage is missing from the bar. The value set and the record type's selected values, not the path file, control which steps render.
- **admin/opportunity-management** — Use when the stage model itself is the problem. Redesigning guidance on top of fragile stages fails; settle the business process first.
- **admin/lightning-record-page-configuration** — Use when the path is correct and still invisible. The `FlexiPage` must carry `runtime_sales_pathassistant:pathAssistant` in a `subheader` region.
- **admin/in-app-guidance-and-walkthroughs** — Use when guidance must vary by profile. Path cannot target profiles; In-App Guidance can.
