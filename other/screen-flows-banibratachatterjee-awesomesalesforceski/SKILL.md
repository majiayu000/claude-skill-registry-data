---
name: screen-flows
description: "Use when designing or reviewing interactive Flow screen experiences, including navigation, validation, screen component choice, custom LWC screen components, and user-safe commit timing. Triggers: 'screen flow validation', 'back button behavior in flow', 'custom flow screen component', 'screen flow UX'. NOT for Experience Cloud guest exposure or custom property editor design-time tooling."
category: flow
salesforce-version: "Spring '25+'"
well-architected-pillars:
  - User Experience
  - Reliability
  - Operational Excellence
tags:
  - screen-flows
  - flow-ux
  - screen-components
  - flow-validation
  - navigation
triggers:
  - "how should i design a screen flow"
  - "screen flow validation is confusing"
  - "back button behavior in flow"
  - "custom lwc screen component in flow"
  - "when should screen flow save data"
inputs:
  - "how many screens the interview needs and where data should be committed"
  - "which standard or custom screen components are required"
  - "how validation, back navigation, cancel, and mobile usage should work"
outputs:
  - "screen-flow UX recommendation for navigation, validation, and commit timing"
  - "review findings for weak screen design or risky save placement"
  - "guidance for using standard components versus custom LWC screen components"
dependencies: []
version: 2.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

Use this skill when the Flow is interactive and the quality of the user journey matters as much as the automation logic. Screen flows succeed when they guide the user through a deliberate sequence, validate at the right moments, and commit data only where the consequences are clear. They become fragile when navigation, validation, and side effects are all mixed together casually.

The three most common screen-flow design failures: (1) DML happens on screen 2 of 6, so clicking Back from screen 5 leaves half-committed data, (2) custom LWC screen component's validation doesn't integrate with the Flow runtime, so users hit Next through invalid inputs, (3) screen count grows from 3 to 11 over iterative "just one more screen" additions until the flow is unusable on mobile. This skill exists to prevent those.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first.

Gather if not available:
- How many decision points and data-entry steps are truly necessary for the user to complete the task?
- Which fields can rely on standard screen components, and which require a custom LWC because the runtime UX truly differs?
- At what point should the flow create or update data, and what should happen if the user clicks Back, Cancel, or Next with invalid inputs?
- Who is the target user (internal employee on desktop, field agent on mobile, Experience Cloud customer)?
- Will this flow be embedded as a Quick Action, Lightning Record Page component, utility bar flow, or standalone URL?

## Core Concepts

Screen flows are interviews, not pages. That means the experience is stateful, sequential, and sensitive to where the design commits work. A strong screen flow keeps the user focused on entering or confirming information. A weak one starts performing irreversible actions too early or makes validation unpredictable between screens.

### Commit Timing Is A UX Decision

If the flow creates or updates records before the user reaches a natural confirmation point, Back and Cancel become much harder to reason about. In many cases, the best pattern is to gather inputs first, show a summary or final confirmation, and only then perform the final DML.

| Commit placement | When correct | When wrong |
|---|---|---|
| Very early (screen 2 of 6) | Side effects are idempotent AND user can't navigate back | User expects Back/Cancel to undo; partial commits confuse |
| In the middle (screen 4 of 6) | Staged commits are business-meaningful (e.g., "Reserve" then "Confirm") | Staging isn't part of the business model; users confused by half-state |
| At the end (after review screen) | Most cases — the canonical pattern | Business needs true in-progress state persistence across sessions |
| Never (ephemeral flow) | Wizards that only display data or produce a PDF | Data actually needs to persist |

### Standard Components Are Usually Better Defaults

Flow screen components cover many common needs without custom code. Reach for a custom LWC screen component only when the interaction model, validation behavior, or rendering requirement truly exceeds what standard screen elements provide.

Standard screen components handle:
- Text, Number, Date, DateTime, Email, URL, Phone inputs
- Picklist, Multi-select Picklist, Radio Buttons, Checkbox, Checkbox Group
- Lookup (single- and multi-select)
- Dependent Picklists (controlling/dependent relationships)
- Rich Text display
- File Upload
- Data Table (including editable)
- Address compound input

A custom LWC screen component is warranted when you need: cascading reactive UI between multiple fields on the same screen, real-time external-system validation, a rendering that truly isn't expressible with standard components (drag-and-drop, inline image annotation, etc.), or when a reusable LWC you already own must be surfaced.

### Custom Screen Components Need A Validation Contract

A custom LWC used in Flow has to cooperate with Flow runtime validation intentionally. That means implementing the right methods and making sure internal validation, externally supplied error messages, and displayed errors stay consistent with how the user moves between screens.

Required contract for Flow-compatible LWCs:
- `@api validate()` method returning `{ isValid: boolean, errorMessage?: string }`.
- `@api`-exposed properties aligning with Flow variable types.
- `FlowAttributeChangeEvent` dispatched when internal state changes affect Flow variables.
- `FlowNavigationNextEvent` (optional) when the component wants to force advancement.

Missing any of these creates the "Next clicks past invalid data" class of bugs.

### Navigation Should Feel Predictable

The number of screens, presence of a Back path, and clarity of button labels all shape the experience. If a flow has too many screens or too much hidden branching, users stop understanding where they are in the process.

**Heuristic:** < 4 screens feels like a form; 4–7 screens feels like a wizard; > 7 screens feels like a maze. If the flow needs more than 7 screens, reconsider: is this one task or two? Can some screens be combined? Does a custom LWC display replace a multi-screen sequence?

## Common Patterns

### Pattern 1: Gather, Review, Then Commit

**When to use:** Any flow where the user enters meaningful data or confirms a business transaction.

**Structure:**
```text
Screen 1: Collect inputs (required fields, defaults where safe)
Screen 2: Collect additional inputs (conditional on Screen 1's answers)
Screen 3: Review screen — read-only display of ALL values the user entered + "Confirm" button
[On Confirm click → Create Records / Update Records / Invoke Apex action]
Screen 4: Confirmation — "Done. Record created: <link>"
```

**Why not the alternative:** Early record mutation makes cancellation and back-navigation behavior harder to trust; the user reasonably expects Back and Cancel to undo their changes.

### Pattern 2: Standard Components First, Custom Component Only For Real Gaps

**When to use:** Most inputs are standard, but one part of the experience needs custom UX or validation.

**Structure:**
```text
Screen 1: Standard components (Name, Status, Date)
Screen 2: STANDARD fields + ONE custom LWC component for the exceptional interaction
          (e.g., a reactive product configurator that depends on Screen-1's selections)
Screen 3: Review + commit (Pattern 1 from here)
```

**Why not the alternative:** Rebuilding entire screens as custom LWCs raises maintenance cost, bypasses Flow Builder's accessibility features, and makes the flow harder for admins to adjust.

### Pattern 3: Bounded Screen Count With Clear Branching

**When to use:** A process needs several decisions but should still feel guided.

**Structure:** Every Decision element leads to at most 2 "branch endings" (screens specific to that path). Avoid branches that loop back to common screens — causes confusing Back behavior. Use `Is First Screen` / `Is Last Screen` pattern via dynamic component visibility to signal progress.

### Pattern 4: Modal Flow (Quick Action) vs Full-Page Flow

Screen flows behave differently by surface:

- **Quick Action modal** — appears as a dialog; Cancel = close without committing; tight screen-count budget (3–4 max); limited width. Use for focused tasks.
- **Lightning Record Page component** — embedded in the record view; persistent while user navigates; stateful across record refreshes. Use for ongoing data entry.
- **Standalone URL** — full-page flow; Cancel navigates away; widest width; good for wizards. Use for one-off journeys.
- **Utility bar flow** — persistent access; shared state across records. Use for tools.

The commit-timing rules change per surface: modal Cancel is a strong "undo" signal; full-page Cancel is a "leave the page" signal. Align UX to surface.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Guided user input with standard fields | Standard Flow screen components | Fastest path to clear, supported UX |
| One input needs specialized rendering or validation | Custom LWC screen component (Pattern 2) | Contains custom complexity to one boundary |
| Data changes are significant or hard to undo | Commit near the end after review (Pattern 1) | Makes user intent and rollback expectations clearer |
| Many screens needed for one task | Reassess info architecture OR split into multiple flows | Flow is too fragmented or task is too broad |
| Public or external-site embedding | Use `flow/flow-for-experience-cloud` | Guest-user semantics add security concerns |
| Flow must share state across multiple record views | LWC-backed state persistence or full-page flow | Quick Action modal loses state on close |

## Well-Architected Pillar Mapping

- **User Experience** — commit timing, screen count, validation clarity, Back/Cancel behavior. UX findings dominate this skill.
- **Reliability** — custom LWC validation contract gaps; flows that commit partially and cannot undo on Cancel; fault-handling on the DML at commit step (see `flow/fault-handling`).
- **Operational Excellence** — the custom-LWC maintenance burden over time; the risk of "one admin built it, nobody else understands it."

## Review Checklist

- [ ] Each screen has one clear purpose and does not overload the user.
- [ ] Validation timing is predictable for both standard and custom components.
- [ ] Data commit points are intentional and not placed too early.
- [ ] Back, Next, Cancel, and Finish behavior all make sense to a real user.
- [ ] Custom screen components implement the `@api validate()` contract.
- [ ] Mobile or smaller-screen behavior was considered when layout matters.
- [ ] Screen count is within the "form / wizard / maze" heuristic range.
- [ ] Fault handling exists on the commit step (Pattern A from `flow/fault-handling`).


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Common Patterns above; choose the surface deliberately
4. Validate — run the skill's checker script and verify against the Review Checklist above
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

1. **A screen flow is not automatically reversible** — once DML has happened, Back and Cancel cannot behave like true undo.
2. **Custom screen components need to cooperate with Flow validation** — they do not get correct validation behavior for free; missing `@api validate()` lets users click Next past errors.
3. **Too many screens feel like poor information architecture, not better guidance** — sequence alone does not improve UX.
4. **Standard components are easier to support than fully custom screen UIs** — custom screens should be the exception.
5. **Finish button does NOT always go where admin expects** — screen flows finish at an implicit redirect; use `{!$Flow.CurrentRecord}` or explicit redirect to control.
6. **Mobile behavior differs from desktop** — custom LWCs may render differently; some standard components (Data Table edit mode) have reduced mobile support.
7. **Quick Action modal has a narrower width than standalone** — layouts that work in full-page break in the modal.
8. **Back-button is disabled by default on some screen types** — explicitly enable if the UX needs it; don't rely on browser back.
9. **Screen flows in Experience Cloud inherit the site's profile, not the invoking user's** — sharing implications differ (see `flow/flow-for-experience-cloud`).
10. **Lookup component defaults to the first match on typeahead** — users sometimes pick the wrong record; include a disambiguator (e.g. show Account Name next to Contact Name).

## Proactive Triggers

Surface these WITHOUT being asked:

- **DML on screen 2 of 6 without a staging-model justification** → Flag as High. Almost always wrong; move commit to post-review.
- **Custom LWC screen component with no `@api validate()` method** → Flag as Critical. Users can Next past invalid data.
- **Screen flow with > 7 screens** → Flag as Medium. Reassess info architecture.
- **Quick Action modal flow with > 4 screens** → Flag as High. Modal is the wrong surface for that many screens.
- **Full-page flow with Cancel behavior not explicitly specified** → Flag as Medium. Users guess — ambiguity invites support tickets.
- **Custom LWC used where standard components would suffice** → Flag as Low. Maintenance-cost observation, not a bug.
- **Back button disabled on a wizard-style flow** → Flag as Medium. Users want to go back; disabling surprises them.
- **Screen flow embedded in Experience Cloud without guest-access review** → Flag as Critical. Route to `flow/flow-for-experience-cloud`.

## Output Artifacts

| Artifact | Description |
|---|---|
| Screen-flow UX design | Recommendation for screens, navigation, and commit timing |
| Validation contract | Guidance for standard vs custom component validation behavior |
| Review findings | Risks in screen count, save placement, navigation flow |
| Surface recommendation | Quick Action / LRP embed / full-page / utility bar choice with rationale |

## Related Skills

- **flow/flow-for-experience-cloud** — use when the screen flow is being embedded for external users or guest audiences.
- **flow/fault-handling** — use when the harder problem is failure behavior after the user submits.
- **flow/record-triggered-flow-patterns** — when the screen flow's commit triggers a record-triggered flow downstream.
- **lwc/custom-property-editor-for-flow** — when the question is about Flow Builder design-time configuration rather than runtime screen UX.
- **lwc/lwc-in-flow-screens** — companion LWC-side skill for building the custom components.
