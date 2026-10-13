---
name: ux-review
description: "Validates a UX spec, HUD design, or interaction pattern library for completeness, accessibility compliance, CDD alignment, and implementation readiness. Supports both game projects (player need, HUD, input methods) and product projects (user goal, workflow, API/CLI affordance)."
argument-hint: "[file-path or 'all' or 'hud' or 'api' or 'cli' or 'patterns']"
user-invocable: true
allowed-tools: Read, Glob, Grep
agent: ux-designer
---

## User Guide

- When to use: Validates a UX spec, HUD design, or interaction pattern library for completeness, accessibility compliance, CDD alignment, and implementation readiness. Supports both game projects (player need, HUD, input methods) and product projects (user goal, workflow, API/CLI affordance).
- Inputs: Command arguments: `/ux-review [file-path or 'all' or 'hud' or 'api' or 'cli' or 'patterns']`; actual project artifacts and review scope referenced below.
- Outputs: Conversation findings and an advisory verdict. This skill does not write files; later persistent saves belong to a separately authorized write-capable workflow.
- Memory-bank writes: None in this read-only workflow. A later authorized save workflow may own `memory_bank/t3_archive/reviews/review-index.md` as described below.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

Resolve the actual project domain and interface from substantive existing concept documents in `design/cdd/` and the configured domain and surface in standards/technical-preferences.md; a filename alone does not establish the domain:
- `design/cdd/game-concept.md` -> use `[Game]` paths only when its substantive content and the actual configuration establish Game scope.
- `design/cdd/product-concept.md` -> use `[Product]` paths only when its substantive content and the actual configuration establish Product scope.
- Missing or conflicting domain/configuration -> keep the domain Unknown and clarify the actual domain, interface, and review scope with the configured project lead or user before selecting domain-specific inputs. Do not default to Game. The hud mode is Game-only; api and cli modes are Product-only. Clarify an incompatible selected mode before reading its domain-specific inputs; neutral conversational findings do not establish domain readiness.

---

## Overview

Validates UX design documents before they enter the implementation pipeline.
Acts as the quality gate between UX Design and Visual Design/Implementation.

**Run this skill:**
- After completing a UX spec with `/ux-design`
- **[Game]** Before handing off to `ui-programmer` or `art-director`
- **[Product]** Before handing off to `lead-programmer` or `ui-programmer`
- Before the Pre-Production / Pre-Implementation gate check (which requires reviewed UX specs)
- After major revisions to a UX spec

**Verdict levels:**
- **APPROVED** — spec is complete, consistent, and implementation-ready
- **NEEDS REVISION** — specific gaps found; fix before handoff but not a full redesign
- **MAJOR REVISION NEEDED** — fundamental issues with scope, user need, or
  completeness; needs significant rework

---

## Phase 1: Parse Arguments

- **Specific file path** (e.g., `/ux-review design/ux/inventory.md`): validate
  that one document
- **`all`**: find all files in `design/ux/` and validate each
- **[Game] `hud`**: validate `design/ux/hud.md` specifically
- **[Product] `api`**: validate `design/ux/api-consumer-journey.md` specifically
- **[Product] `cli`**: validate `design/ux/cli-interaction.md` specifically
- **`patterns`**: validate `design/ux/interaction-patterns.md` specifically
- **No argument**: ask the user which spec to validate

For `all`, output a summary table first (file | verdict | primary issue) then
full detail for each.

---

## Phase 2: Load Cross-Reference Context

Before validating any spec, load:

### [Game] Game Context

1. **Input & Platform config**: Read `standards/technical-preferences.md` and
   extract `## Input & Platform`. This is the authoritative source for which input
   methods the game supports — use it to drive the Input Method Coverage checks in
   Phase 3A, not the spec's own header. If unconfigured, fall back to the spec header.
2. The accessibility tier committed to in `design/accessibility-requirements.md`
   (if it exists)
3. The interaction pattern library at `design/ux/interaction-patterns.md` (if
   it exists)
4. The CDDs referenced in the spec's header (read their UI Requirements sections)
5. The player journey map at `design/player-journey.md` (if it exists) for
   context-arrival validation

### [Product] Product Context

1. **Technology stack and surfaces**: Read `standards/technical-preferences.md`,
   actual configured fields and the owning CDD/spec surface profile. Resolve
   Product Stack or valid populated legacy Language & Framework, Platform &
   Deployment, Agent Routing and Testing sections. Apply API/CLI/Web checks to
   the actual surfaces; placeholders do not establish a capability.
2. The accessibility tier committed to in `design/accessibility-requirements.md`
   (if it exists)
3. The interaction pattern library at `design/ux/interaction-patterns.md` (if
   it exists)
4. The CDDs referenced in the spec's header (read their UI Requirements or Data Model sections)
5. The product concept doc at `design/cdd/product-concept.md` for user goal and workflow validation
6. For API specs: read the OpenAPI/Swagger spec if it exists
7. For CLI specs: read `--help` output or man page draft if available

---

## Phase 3A: UX Spec Validation Checklist

Run all applicable checks against a `ux-spec.md`-based document. Use the
checklist that matches the detected domain and actual surface from Phase 0.
For API-only or CLI-only scope, graphic controls, visual layout, animation,
audio and browser focus checks apply only if those capabilities actually exist.
Record each N/A with its substantive CDD/spec/configuration reason and named
owner; unresolved applicability remains Unknown and prevents affected approval.
Absence of graphical UI never waives required API/CLI interaction, accessibility,
auth, error, recovery or contract checks.

### [Game] Game UX Spec — Completeness (required sections)

- [ ] Document header present with Status, Author, Platform Target
- [ ] Purpose & Player Need — has a player-perspective need statement (not
  developer-perspective)
- [ ] Player Context on Arrival — describes player's state and prior activity
- [ ] Navigation Position — shows where screen sits in hierarchy
- [ ] Entry & Exit Points — all entry sources and exit destinations documented
- [ ] Layout Specification — zones defined, component inventory table present
- [ ] States & Variants — at minimum: loading, empty/populated, and error states
  documented
- [ ] Interaction Map — covers all target input methods (check platform target
  in header)
- [ ] Data Requirements — every displayed data element has a source system and owner
- [ ] Events Fired — every player action has a corresponding event or null
  explanation
- [ ] Transitions & Animations — at least enter/exit transitions specified
- [ ] Accessibility Requirements — screen-level requirements present
- [ ] Localization Considerations — max character counts for text elements
- [ ] Acceptance Criteria — at least 5 specific testable criteria

### [Product] Product UX Spec — Completeness (required sections)

- [ ] Document header present with Status, Author, Technology Target
- [ ] Purpose & User Need — has a user-perspective need statement (not developer-perspective)
- [ ] User Context on Arrival — describes user's task state and prior activity in workflow
- [ ] Workflow Position — shows where interaction sits (CLI command tree / API path tree / web breadcrumb)
- [ ] Entry & Exit Points — all entry sources and exit destinations documented
- [ ] Layout / Output Specification — for web: zones + component inventory; for API: response envelope + endpoint contract; for CLI: output format + flag inventory
- [ ] States & Variants — at minimum: loading, empty, error, AND: rate-limited, auth-expired, offline, maintenance mode (as applicable)
- [ ] Interaction Map — for API: HTTP methods, params, auth; for CLI: flags, positional args, exit codes; for Web: keyboard, pointer, focus order
- [ ] Data Requirements — every displayed/returned data element has a source system and owner
- [ ] Events Fired — every user action has a corresponding analytics event, state change, or null explanation
- [ ] Transitions — for API: request lifecycle states; for CLI: progress indicators and signal handling; for Web: route transitions and loading states
- [ ] Accessibility Requirements — requirements for the actual surface: configured WCAG/ARIA/keyboard behavior for visual UI, readable and scriptable CLI output/errors, and clear API error contracts/docs for consumers
- [ ] Localization Considerations — max character counts for text elements; RTL readiness for web; locale-aware formatting
- [ ] Acceptance Criteria — at least 5 specific testable criteria with product-appropriate examples (response time, exit codes, breakpoint verification)

### [Game] Game Quality Checks

**Player Need Clarity**
- [ ] Purpose is written from player perspective, not system/developer perspective
- [ ] Player goal on arrival is unambiguous ("The player arrives wanting to ___")
- [ ] The player context on arrival is specific (not just "they opened the
  inventory")

**Completeness of States**
- [ ] Error state is documented (not just happy path)
- [ ] Empty state is documented (no data scenario)
- [ ] Loading state is documented if the screen fetches async data
- [ ] Any state with a timer or auto-dismiss is documented with duration

**Input Method Coverage**
- [ ] If platform includes PC: keyboard-only navigation is fully specified
- [ ] If platform includes console/gamepad: d-pad navigation and face button
  mapping documented
- [ ] No interaction requires mouse-like precision on gamepad
- [ ] Focus order is defined (Tab order for keyboard, d-pad order for gamepad)

**Data Architecture**
- [ ] No data element has "UI" listed as the owner (UI must not own game state)
- [ ] Update frequency is specified for all real-time data (not just "realtime" —
  what triggers update?)
- [ ] Null handling is specified for all data elements (what shows when data is
  unavailable?)

### [Product] Product Quality Checks

**User Need Clarity**
- [ ] Purpose is written from user perspective, not system/developer perspective
- [ ] User goal on arrival is unambiguous ("The user interacts with this to ___")
- [ ] The user context on arrival is specific to the workflow (not just "they opened
  the page" / "they ran the command")

**Completeness of States**
- [ ] Error state is documented (not just happy path)
- [ ] Empty state is documented (no data / 0 results scenario)
- [ ] Loading/processing state is documented if the interaction is async
- [ ] Rate-limited state is documented (if public API)
- [ ] Auth-expired state is documented (if session-based)
- [ ] Offline/connectivity-loss state is documented (if applicable)

**Input / Interaction Coverage**
- [ ] For API: all HTTP methods used are specified with URL, params, auth, and response schema
- [ ] For API: error response format is consistent and documented (400/401/403/404/422/429/500)
- [ ] For CLI: all flags and positional args are specified with types and defaults
- [ ] For CLI: exit codes are defined and consistent (0=success, non-zero=error types)
- [ ] For Web: keyboard-only navigation is fully specified (Tab/Enter/Escape)
- [ ] For Web: focus order is defined for all interactive elements
- [ ] For Web: responsive breakpoints are specified (mobile/tablet/desktop)

**Data Architecture**
- [ ] No data element has "UI" / "presentation" listed as the owner
- [ ] Update frequency is specified for all time-sensitive data
- [ ] Null/empty handling is specified for all data elements
- [ ] Staleness tolerance is documented (how old can data be before refresh?)

**[通用场景] Shared Quality Checks**

**Accessibility**
- [ ] Accessibility tier from `accessibility-requirements.md` is matched or exceeded
- [ ] If Basic tier: no color-only information indicators on any actual visual or CLI output
- [ ] If Standard tier+ and visual UI exists: focus order documented, text contrast ratios specified
- [ ] If Comprehensive tier+ and visual UI exists: screen reader announcements for key state changes
- [ ] Colorblind check: any actual color-coded elements/output have non-color alternatives
- [ ] API/CLI consumers have the applicable error, output and recovery guidance; absent graphical capabilities use the owner/reason N/A rule above

**CDD Alignment**
- [ ] Every CDD requirement referenced in the header is addressed in this spec
- [ ] No UI element displays or modifies state without a corresponding CDD requirement
- [ ] No CDD requirement is missing from this spec (cross-check the referenced CDD sections)

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
- [ ] [Product] RTL language readiness assessed (web)
- [ ] [Product] Date/time/currency locale-aware formatting verified

**Acceptance Criteria Quality**
- [ ] Criteria are specific enough for a QA tester who hasn't seen the design docs
- [ ] Performance criterion present (screen opens within Xms / endpoint responds within Xms / command completes within Xs)
- [ ] Resolution/progressive enhancement criterion present (if applicable)
- [ ] No criterion requires reading another document to evaluate

---

## Phase 3B: HUD Validation Checklist `[Game]`

Run all checks against a `hud-design.md`-based document. This phase is game-only.

### Completeness

- [ ] HUD Philosophy defined
- [ ] Information Architecture table covers ALL systems with UI Requirements in CDDs
- [ ] Layout Zones defined with safe zone margins for all target platforms
- [ ] Every HUD element has a full specification (zone, visibility trigger, data
  source, priority)
- [ ] HUD States by Gameplay Context covers at minimum: exploration, combat,
  dialogue/cutscene, paused
- [ ] Visual Budget defined (max simultaneous elements, max screen %)
- [ ] Platform Adaptation covers all target platforms
- [ ] Tuning Knobs present for player-adjustable elements

### Quality Checks

- [ ] No HUD element covers the center play area without a visibility rule to
  hide it
- [ ] Every information item that exists in any CDD is either in the HUD or
  explicitly categorized as "hidden/demand"
- [ ] All color-coded HUD elements have colorblind variants
- [ ] HUD elements in the Feedback & Notification section have queue/priority
  behavior defined
- [ ] Visual Budget compliance: total simultaneous elements is within budget

### CDD Alignment

- [ ] All systems in `design/cdd/module-index.md` with UI category have
  representation in HUD (or justified absence)

---

## Phase 3C: Pattern Library Validation Checklist

Resolve the library's actual Game/UI/API/CLI scope from its owning specs, CDDs
and configuration. Apply every required surface below; a mixed library must
cover each actual surface. Absent capabilities need a recorded N/A reason and
named owner. Unknown scope or missing required patterns prevents approval.

- [ ] Pattern catalog index is current (matches actual patterns in document)
- [ ] Each pattern has: When to Use, When NOT to Use, full state specification,
  accessibility spec, implementation notes
- [ ] No conflicting behaviors between patterns (e.g., navigation "Back", API
  error contracts or CLI exit-code/output behavior remain consistent)

**Game and graphical UI patterns**

- [ ] For Game or actual graphical UI, all required standard control patterns
  are specified: button variants, toggle, slider, dropdown, list, grid, modal,
  dialog, toast, tooltip, progress bar, input field, tab bar, scroll
- [ ] All game-specific patterns needed by current Game UX specs are present
- [ ] Game Animation Standards and Sound Standards tables are present; actual
  Product UI animation/audio requirements apply where those capabilities exist
- [ ] Graphical UI patterns meet configured input, focus, accessibility and
  localization requirements; absent Product animation/audio uses justified N/A

**API consumer patterns (when present)**

- [ ] Request/response envelopes, methods/parameters, status and error schemas,
  auth/permission states and consumer recovery are specified for actual contracts
- [ ] Rate-limit, retry and idempotency patterns are specified where applicable
- [ ] Docs/examples and accessibility of consumer guidance match those contracts

**CLI patterns (when present)**

- [ ] Commands, flags/defaults, help/examples, stdin/stdout/stderr, machine-readable
  output and exit codes are specified for actual command contracts
- [ ] Invalid input/configuration, permission errors, progress/cancellation and
  recovery behavior are specified where applicable
- [ ] Required destructive-action confirmation/dry-run behavior is retained;
  readable output and diagnostics do not rely on color alone

API-only or CLI-only libraries need no invented graphical controls, animations
or sounds. This applicability rule waives no required contract or safety check.

---

## Phase 4: Output the Verdict

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Domain**: [Game / Product]
**Platform / Technology Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & [Player/User] Need
- [ ] States & Variants — MISSING: [error state / rate-limited state / etc.]

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### CDD Alignment: [ALIGNED / GAPS FOUND]
- CDD [name] Requirements — [X/Y requirements covered]
- Missing: [list any uncovered CDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

[For APPROVED]: This spec is ready for handoff. [Game]: to `/team-ui` Phase 2 (Visual Design). [Product]: to lead-programmer for implementation.

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run `/ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas]. Recommend returning to `/ux-design` to rework [sections].
```

---

## Phase 5: Collaborative Protocol

This skill is READ-ONLY — it never edits or writes files. It reports findings only.

A later write-capable workflow may save the review only within its named
path/effect authority. That workflow may also update
`memory_bank/t3_archive/reviews/review-index.md` when `memory_bank/` exists and the
index update itself is covered by existing scoped authority or an approved named
changeset. Approval for the report alone does not authorize the index.
Use Review Type `ux-review`, the verified saved artifact path as `Source Artifact`,
and dedupe on `Source Artifact`. `/ux-review` does not invoke that write workflow
or create `memory_bank/`; deliver findings in conversation until those effects
are separately authorized.

After delivering the verdict:
- For **APPROVED**: suggest next steps — **[Game]** `/team-ui` for implementation coordination; **[Product]** hand off to lead-programmer
- For **NEEDS REVISION**: offer to help fix specific gaps ("Would you like me to
  help draft the missing error state?") — but do not auto-fix; wait for user
  instruction
- For **MAJOR REVISION NEEDED**: suggest returning to `/ux-design` with the
  specific sections to rework

Never block the user from proceeding — the verdict is advisory. Document risks,
present findings, let the user decide whether to proceed despite concerns. A user
who chooses to proceed with a NEEDS REVISION spec takes on the documented risk.
