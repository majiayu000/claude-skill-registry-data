---
name: saas-ux-review
description: "Validate a UX spec, App Shell design or pattern library — accessibility, PRD alignment, readiness. APPROVED / NOT ASSESSED / NEEDS REVISION / MAJOR REVISION NEEDED."
argument-hint: "[file-path or 'all' or 'app-shell' or 'patterns']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash(bash "*/.claude/skills/saas-ux-review/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,workflow`

Resolved above — use as-is. No block → defaults in
`.claude/docs/config-resolution.md`.

# UX Review

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

## Overview

Validates UX design documents before they enter the implementation pipeline.
Acts as the quality gate between UX Design and Visual Design/Implementation in
the `/saas-team-ui` pipeline.

**Run this skill:**
- After completing a UX spec with `/saas-ux-design`
- Before handing off to `frontend-engineer` or `design-system-director`
- Before the Pre-Production to Production gate check (which requires key screens
  to have reviewed UX specs)
- After major revisions to a UX spec

**Verdict levels:**
- **APPROVED** — spec is complete, consistent, and implementation-ready
- **NOT ASSESSED** — one or more review dimensions had no criterion to check
  against, or the spec could not be read; name which
- **NEEDS REVISION** — specific gaps found; fix before handoff but not a full redesign
- **MAJOR REVISION NEEDED** — fundamental issues with scope, user need, or
  completeness; needs significant rework

**`NOT ASSESSED` ranks above APPROVED and below the two revision verdicts.** A
review that could not evaluate a dimension has not shown the spec is
implementation-ready; but a gap somebody found is more actionable than one nobody
could look for, so it must not displace them. Emit it when the spec file cannot
be read, when a checklist dimension has no source of truth to compare against, or
when the accessibility tier is uncommitted (below).

---

## Phase 1: Parse Arguments

- **Specific file path** (e.g., `/saas-ux-review design/ux/workspace-catalog.md`): validate
  that one document
- **`all`**: find all files in `design/ux/` and validate each
- **`app-shell`**: validate `design/ux/app-shell.md` specifically
- **`patterns`**: validate `design/ux/interaction-patterns.md` specifically
- **No argument**: ask the user which spec to validate

For `all`, output a summary table first (file | verdict | primary issue) then
full detail for each.

**Which checklist a file gets** (a file path, or each file under `all`): its
`> **Template**:` header line, which `/saas-ux-design` writes — `UX Spec` → Phase 3A,
`App Shell & Global Navigation Spec` → 3B, `Interaction Pattern Library` → 3C. A file without that line
is classified by name — `app-shell.md` → 3B, `interaction-patterns.md` → 3C, anything
else → 3A — and the report says which checklist it assumed, and why.

---

## Phase 2: Load Cross-Reference Context

Before validating any spec, load:

1. **Input & Platform config**: Read the `platform` block from `project.yaml`
   (`platform.targets`, `platform.primary_input`, `platform.touch/mobile_support`,
   `platform.touch_support`); if `project.yaml` has no `platform` block, fall
   back to the `## Input & Platform` section of
   `.claude/docs/technical-preferences.md`. For the set of supported input
   methods: when reading from `project.yaml`, derive it — keyboard/mouse if
   `PC` or `Web` is in `targets`; touch/mobile if `touch/mobile_support` is Full or
   Partial; touch if `touch_support` is Full or Partial; plus `primary_input`.
   When falling back to `technical-preferences.md`, use its explicit Input
   Methods field instead. This is the authoritative source for the Input Method
   Coverage checks in Phase 3A — not the spec's own header. If neither source is
   configured, fall back to the spec header.
2. The accessibility tier committed to in `design/accessibility-requirements.md`
   (if it exists)
3. The interaction pattern library at `design/ux/interaction-patterns.md` (if
   it exists)
4. The PRDs referenced in the spec's header (read their UI Requirements sections:
   check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings: if `.basinfy/` exists, use `basinfy_search` and `basinfy_read`; otherwise use the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit)
5. The customer journey map at `design/customer-journey-map.md` (if it exists) for
   context-arrival validation

---

## Phase 3A: UX Spec Validation Checklist

Run all checks against a `ux-spec.md`-based document.

### Completeness (required sections)

- [ ] Document header present with Status, Author, Platform Target
- [ ] Purpose & User Need — has a user-perspective need statement (not
  developer-perspective)
- [ ] User Context on Arrival — describes user's state and prior activity
- [ ] Navigation Position — shows where screen sits in hierarchy
- [ ] Entry & Exit Points — all entry sources and exit destinations documented
- [ ] Layout Specification — zones defined, component catalog table present
- [ ] States & Variants — at minimum: loading, empty/populated, and error states
  documented
- [ ] Interaction Map — covers all target input methods (check platform target
  in header)
- [ ] Data Requirements — every displayed data element has a source system and owner
- [ ] Events Fired — every user action has a corresponding event or null
  explanation
- [ ] Transitions & Animations — at least enter/exit transitions specified
- [ ] Input Method Completeness Checklist — a block for each input method in
  the Platform Target line; any unticked item is listed under Open Questions
- [ ] Accessibility Requirements — screen-level requirements present
- [ ] Localization Considerations — max character counts for text elements
- [ ] Acceptance Criteria — at least 5 specific testable criteria

### Quality Checks

**User Need Clarity**
- [ ] Purpose is written from user perspective, not system/developer perspective
- [ ] User goal on arrival is unambiguous ("The user arrives wanting to ___")
- [ ] The user context on arrival is specific (not just "they navigated to the
  settings modal")

**Completeness of States**
- [ ] Error state is documented (not just happy path)
- [ ] Empty state is documented (no data scenario)
- [ ] Loading state is documented if the screen fetches async data
- [ ] Any state with a timer or auto-dismiss is documented with duration

**Input Method Coverage**
- [ ] If platform includes PC: keyboard-only navigation is fully specified
- [ ] If platform includes mobile/touch: tap targets >= 44x44px and bottom sheet navigation
  mapping documented
- [ ] No interaction requires mouse-like precision on touch/mobile
- [ ] Focus order is defined (Tab order for keyboard, logical visual order for mobile)

**Data Architecture**
- [ ] No data element has "UI" listed as the owner (UI must not own application state)
- [ ] Update frequency is specified for all real-time data (not just "realtime" —
  what triggers update?)
- [ ] Null handling is specified for all data elements (what shows when data is
  unavailable?)

**Accessibility**
- [ ] Accessibility tier from `accessibility-requirements.md` is matched or exceeded
- [ ] If Basic tier: no color-only information indicators
- [ ] If Standard tier+: focus order documented, text contrast ratios specified
- [ ] If Comprehensive tier+: screen reader announcements for key state changes
- [ ] Colorblind check: any color-coded elements have non-color alternatives

**PRD Alignment**
- [ ] Every PRD UI Requirement referenced in the header is addressed in this spec
- [ ] No UI element displays or modifies application state without a corresponding PRD
  requirement
- [ ] No PRD UI Requirement is missing from this spec (cross-check the referenced
  PRD sections)

**Pattern Library Consistency**
- [ ] All interactive components reference the pattern library (or note they are
  new patterns)
- [ ] No pattern behavior is re-specified from scratch if it already exists in
  the pattern library
- [ ] Any new patterns invented in this spec are flagged for addition to the
  pattern library

**Localization**
- [ ] Character limit warnings present for all text-heavy elements
- [ ] Any layout-critical text has been flagged for 40% expansion accommodation

**Acceptance Criteria Quality**
- [ ] Criteria are specific enough for a QA tester who hasn't seen the design docs
- [ ] Performance criterion present (screen opens within Xms)
- [ ] Resolution criterion present
- [ ] No criterion requires reading another document to evaluate

---

## Phase 3B: App Shell & Global Navigation Validation Checklist

Run all checks against a `app-shell-navigation-spec.md`-based document.

### Completeness

- [ ] Navigation Philosophy defined
- [ ] Information Architecture table covers ALL systems with UI Requirements in PRDs
- [ ] Layout Zones defined with safe zone margins for all target platforms
- [ ] Every App Shell element has a full specification (zone, visibility trigger, data
  source, priority)
- [ ] App Shell States by Application Context covers at minimum: standard route, focus mode,
  modal dialog / drawer, offline / reconnecting state
- [ ] Information Hierarchy gives every App Shell element a priority tier (MUST KEEP /
  SHOULD KEEP / CAN HIDE / ALWAYS HIDE)
- [ ] Visual Budget defined (max simultaneous elements, max screen %)
- [ ] Platform Adaptation covers all target platforms
- [ ] User Preferences & Settings present for user-adjustable elements
- [ ] Acceptance Criteria — at least 5 specific testable criteria

### Quality Checks

- [ ] No App Shell element obstructs the main viewport without a visibility rule to
  hide it
- [ ] Every information item that exists in any PRD is either in the App Shell or
  explicitly categorized as "hidden/demand"
- [ ] All color-coded App Shell elements have colorblind variants
- [ ] App Shell elements in the Feedback & Notification section have queue/priority
  behavior defined
- [ ] Visual Budget compliance: total simultaneous elements is within budget

### PRD Alignment

- [ ] All systems in `design/prd/features-modules-index.md` with UI category have
  representation in App Shell (or justified absence)

---

## Phase 3C: Pattern Library Validation Checklist

- [ ] Pattern catalog index is current (matches actual patterns in document)
- [ ] All standard control patterns are specified: button variants, toggle,
  slider, dropdown, list, grid, modal, dialog, toast, tooltip, progress bar,
  input field, tab bar, scroll
- [ ] All application-specific patterns needed by current UX specs are present
- [ ] Each pattern has: When to Use, When NOT to Use, full state specification,
  accessibility spec, implementation notes
- [ ] Animation Standards table present
- [ ] Sound Standards table present
- [ ] No conflicting behaviors between patterns (e.g., "Back" behavior consistent
  across all navigation patterns)

---

## Phase 4: Output the Verdict

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Checklist**: [3A / 3B / 3C — from its Template line, or assumed from the file name]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & User Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### PRD Alignment: [ALIGNED / GAPS FOUND]
- PRD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered PRD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT / NOT ASSESSED]
- Target tier: [tier]
- [list specific accessibility findings]

> **If `design/accessibility-requirements.md` is absent there is no committed
> tier, so this dimension has no criterion.** Report
> `Accessibility: NOT ASSESSED — no committed tier (design/accessibility-requirements.md absent)`
> and do NOT report it as COMPLIANT — a gate compared against an absent standard
> passes the way an assertion that can never fail passes. The same rule lives in
> `/saas-team-ui` Phase 4 and is mirrored here so the two cannot drift. If the spec's own
> header states a tier, carry it forward as an **assumption** and say plainly that
> it was assumed rather than committed. Recommend `/saas-ux-design accessibility` to
> establish the tier.

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND / N/A]
- [findings]

> **For an App Shell design there is no Pattern Library checklist to run it against (Phase 3B has none), so Pattern Library is N/A, excluded from the dimension count.**
> Report `Pattern Library: N/A — no pattern library checklist for this document
> type`.
>
> For a UX spec, this dimension does have a checklist — it is checked against
> `design/ux/interaction-patterns.md`. If that file is absent: N/A only where
> the workflow tier does not require the library (`minimal`) — report
> `Pattern Library: N/A — interaction pattern library not required at this
> tier`. At any tier that requires or recommends it (`standard`, `full`), report
> `Pattern Library: NOT ASSESSED — design/ux/interaction-patterns.md not found`
> instead: the library is missing, not out of scope, and NOT ASSESSED counts it
> against the verdict as the unresolved item it is.

### Verdict: APPROVED / NOT ASSESSED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking
**Dimensions not assessed**: [N] — [name each, and what would make it checkable]

[For APPROVED]: This spec is ready for handoff to `/saas-team-ui` Phase 2
(Visual Design).

[For NOT ASSESSED]: [N] of the four review dimensions could not be evaluated:
[name them]. The spec may well be sound — this review cannot say either way for
those dimensions. [For each: the one input that would make it checkable.]
Handoff to `/saas-team-ui` is not recommended on this result.

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run
`/saas-ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas].
Recommend returning to `/saas-ux-design` to rework [sections].
```

---

## Phase 5: Collaborative Protocol

This skill is READ-ONLY — it never edits or writes files. It reports findings only.

After delivering the verdict:
- For **APPROVED**: suggest running `/saas-team-ui` to begin implementation coordination
- For **NOT ASSESSED**: name the missing input per dimension and offer to help
  produce it (`/saas-ux-design accessibility` for an uncommitted tier, the PRD path
  for absent UI requirements). Do not re-run the review against the same missing
  inputs and report a different verdict — only new inputs change this one
- For **NEEDS REVISION**: offer to help fix specific gaps ("Would you like me to
  help draft the missing error state?") — but do not auto-fix; wait for user
  instruction
- For **MAJOR REVISION NEEDED**: suggest returning to `/saas-ux-design` with the
  specific sections to rework

Never block the user from proceeding — the verdict is advisory. Document risks,
present findings, let the user decide whether to proceed despite concerns. A user
who chooses to proceed with a NEEDS REVISION spec takes on the documented risk.
