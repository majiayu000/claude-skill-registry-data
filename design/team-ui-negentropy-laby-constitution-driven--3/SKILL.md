---
name: team-ui
description: "Orchestrate the UI team through the full UX pipeline: from UX spec authoring through visual design, implementation, review, and polish. Integrates with /ux-design, /ux-review, and studio UX templates."
argument-hint: "[UI feature description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate the UI team through the full UX pipeline: from UX spec authoring through visual design, implementation, review, and polish. Integrates with /ux-design, /ux-review, and studio UX templates.
- Inputs: Command arguments: `/team-ui [UI feature description]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Read `standards/technical-preferences.md`, existing scoped domain decisions,
and the substantive bodies of any `design/cdd/game-concept.md` and
`design/cdd/product-concept.md` before selecting a branch. Filenames, placeholder
or copied concept text and shared extensions do not establish a domain. Read
actual configured values in `Product Stack` or the populated legacy
`Language & Framework`, `Platform & Deployment`, and `Agent Routing` /
`File Extension Routing`
sections in their owning domain context; missing new sections or a concept do
not erase configured legacy Product facts. A placeholder Game concept does not
override a configured Product.

Resolve Game from consistent substantive Game concept/decision or actual
configured engine/domain and Game behavior evidence; resolve Product from
consistent substantive Product concept/decision or actual Product configuration.
Two substantive concepts, conflicting concept/configuration values or mixed scope
leave the affected branch **Unknown** until a scoped decision resolves the conflict.
With no consistent substantive concept/scoped decision or sufficient actual
configuration evidence, the domain is also Unknown; a valid concept alone can
establish the domain before stack configuration.
Record the supporting sections and values. For Unknown, use an existing matching
scoped decision or clarify with the user/configured project lead before
domain-specific delegation or writes; resolved configured facts need no new vote.
Independent neutral reads may continue. Domain selection does not waive required
branch inputs: read their actual originals and leave missing inputs Incomplete.
Never silently default to Game.

- **[Game]** keep game UI/HUD orchestration: player journey, HUD, engine UI specialist, visual design, accessibility, localization, and UI programmer handoff.
- **[Product]** coordinate product interaction work: web UI, admin screens, CLI interaction, API consumer journey, component patterns, accessibility, localization, implementation handoff, and QA evidence.

Game UI workflow remains intact. Product interaction orchestration is added beside it. When this skill is invoked, orchestrate the UI team through a structured pipeline.

**Decision Points:** At each phase transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **ux-designer** — User flows, wireframes, accessibility, input handling
- **ui-programmer** — UI framework, screens, widgets, data binding, implementation
- **art-director** — Visual style, layout polish, consistency with art bible
- **engine UI specialist** — Validates UI implementation patterns against engine-specific best practices (read from `standards/technical-preferences.md` Engine Specialists → UI Specialist)
- **accessibility-specialist** — Audits accessibility compliance at Phase 4

## Product Interaction Team Composition

When the Product branch is active, use this same command for web UI, admin
screens, CLI interaction, API consumer journeys, onboarding flows, docs examples,
and workflow states.

- **ux-designer** — User journey, screen/flow/CLI/API interaction model, accessibility, information architecture
- **ui-programmer** — Product UI components, state binding, forms, tables, dashboards, admin screens, web/native UI implementation where applicable
- **lead-programmer** — API/CLI contract, data/state ownership, integration boundary, implementation handoff
- **language specialist** — Stack-specific UI/API/CLI implementation notes from `standards/technical-preferences.md`
- **accessibility-specialist** — WCAG, keyboard navigation, screen reader, reduced motion, CLI readability, error-state accessibility
- **qa-tester** — Workflow, contract, accessibility, and docs/example evidence

**Templates used by this pipeline:**
- `ux-spec.md` — Standard screen/flow UX specification
- `hud-design.md` — HUD-specific UX specification
- `interaction-pattern-library.md` — Reusable interaction patterns
- `accessibility-requirements.md` — Committed accessibility tier and requirements

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: ux-designer` — User flows, wireframes, accessibility, input handling
- `subagent_type: ui-programmer` — UI framework, screens, widgets, data binding
- `subagent_type: art-director` — Visual style, layout polish, art bible consistency
- `subagent_type: [UI engine specialist]` — Engine-specific UI pattern validation (e.g., unity-ui-specialist, ue-umg-specialist, godot-specialist)
- `subagent_type: accessibility-specialist` — Accessibility compliance audit

Always provide full context in each agent's prompt (feature requirements, existing UI patterns, platform targets). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 4 review agents can run simultaneously).

**Product context reads:**
- `design/cdd/product-concept.md` for user promise, JTBD, target users, platform, and Product principles
- Relevant module CDDs, API/CLI contracts, and UX specs in `design/cdd/` and `design/ux/`
- `standards/technical-preferences.md` for language/framework, UI stack, routing, testing, and deployment conventions
- `docs/architecture/` ADRs for state ownership, API boundaries, auth, permissions, migrations, and observability
- Existing docs/examples/config/release notes for the public surface being changed

## Pipeline

### Phase 1a: Context Gathering

Before designing anything, read and synthesize:
- `design/cdd/game-concept.md` — platform targets and intended audience
- `design/player-journey.md` — player's state and context when they reach this screen
- All CDD UI Requirements sections relevant to this feature
- `design/ux/interaction-patterns.md` — existing patterns to reuse (not reinvent)
- `design/accessibility-requirements.md` — committed accessibility tier (e.g., Basic, Enhanced, Full)

**If `design/ux/interaction-patterns.md` does not exist**, surface the gap immediately:
> "interaction-patterns.md does not exist — no existing patterns to reuse."

Then use `AskUserQuestion` with options:
- (a) Run `/ux-design patterns` first to establish the pattern library, then continue
- (b) Proceed without the pattern library — ui-programmer will treat all patterns created as new and add each to a new `design/ux/interaction-patterns.md` at completion

Do NOT invent or assume patterns from the feature name or CDD alone. If the user chooses (b), explicitly instruct ui-programmer in Phase 3 to treat all patterns as new and document them in `design/ux/interaction-patterns.md` when implementation is complete. Note the pattern library status (created / absent / updated) in the final summary report.

Summarize the context in a brief for the ux-designer: what the player is doing, what they need, what constraints apply, and which existing patterns are relevant.

### Phase 1b: UX Spec Authoring

Invoke `/ux-design [feature name]` skill OR delegate directly to ux-designer to produce `design/ux/[feature-name].md` following the `ux-spec.md` template.

If designing the HUD, use the `hud-design.md` template instead of `ux-spec.md`.

> **Notes on special cases:**
> - For HUD design specifically, invoke `/ux-design` with `argument: hud` (e.g., `/ux-design hud`).
> - For the interaction pattern library, run `/ux-design patterns` once at project start and update it whenever new patterns are introduced during later phases.

Output: `design/ux/[feature-name].md` with all required spec sections filled.

### Phase 1c: UX Review

After the spec is complete, invoke `/ux-review design/ux/[feature-name].md`.

**Gate**: Do not proceed to Phase 2 until the verdict is APPROVED. If the verdict is NEEDS REVISION, the ux-designer must address the flagged issues and re-run the review. The user may explicitly accept a NEEDS REVISION risk and proceed, but this must be a conscious decision — present the specific concerns via `AskUserQuestion` before asking whether to proceed.

### Phase 2: Visual Design

Delegate to **art-director**:
- Review the full UX spec (flows, wireframes, interaction patterns, accessibility notes) — not just the wireframe images
- Apply visual treatment from the art bible: colors, typography, spacing, animation style
- Check that visual design preserves accessibility compliance: verify color contrast ratios, and confirm color is never the only indicator of state (shape, text, or icon must reinforce it)
- Specify all asset requirements needed from the art pipeline: icons at specified sizes, background textures, fonts, decorative elements — with precise dimensions and format requirements
- Ensure consistency with existing implemented UI screens
- Output: visual design spec with style notes and asset manifest

### Phase 3: Implementation

Before implementation begins, spawn the **engine UI specialist** (from `standards/technical-preferences.md` Engine Specialists → UI Specialist) to review the UX spec and visual design spec for engine-specific implementation guidance:
- Which engine UI framework should be used for this screen? (e.g., UI Toolkit vs UGUI in Unity, Control nodes vs CanvasLayer in Godot, UMG vs CommonUI in Unreal)
- Any engine-specific gotchas for the proposed layout or interaction patterns?
- Recommended widget/node structure for the engine?
- Output: engine UI implementation notes to hand off to ui-programmer before they begin

If no engine is configured, skip this step.

When implementation uses an established library, read the actual interaction patterns, including option (a) after its separately approved creation. Explicit option (b) proceeds with new patterns. Keep the initial absent-library warning and user choice visible, do not invent existing patterns, and retain new-pattern documentation plus the final actual library check. Unresolved choice stays Unknown.

Delegate to **ui-programmer**:
- Implement the UI following the UX spec and visual design spec
- **Use patterns from `design/ux/interaction-patterns.md`** — do not reinvent patterns that are already specified. If a pattern almost fits but needs modification, note the deviation and flag it for ux-designer review.
- **UI NEVER owns or modifies game state** — display only; emit events for all player actions
- All text through the localization system — no hardcoded player-facing strings
- Support both input methods (keyboard/mouse AND gamepad)
- Implement accessibility features per the committed tier in `design/accessibility-requirements.md`
- Wire up data binding to game state
- **If any new interaction pattern is created during implementation** (i.e., something not already in the pattern library), add it to `design/ux/interaction-patterns.md` before marking implementation complete
- Output: implemented UI feature

### Phase 4: Review (parallel)

Delegate in parallel:
- **ux-designer**: Verify implementation matches wireframes and interaction spec. Test keyboard-only and gamepad-only navigation. Check accessibility features function correctly.
- **art-director**: Verify visual consistency with art bible. Check at minimum and maximum supported resolutions.
- **accessibility-specialist**: Verify compliance against the committed accessibility tier documented in `design/accessibility-requirements.md`. Flag any violations as blockers.

All three review streams must report before proceeding to Phase 5.

### Phase 5: Polish

- Address all review feedback
- Verify animations are skippable and respect the player's motion reduction preferences
- Confirm UI sounds trigger through the audio event system (no direct audio calls)
- Test at all supported resolutions and aspect ratios
- **Verify `design/ux/interaction-patterns.md` is up to date** — if any new patterns were introduced during this feature's implementation, confirm they have been added to the library

Apply HUD budget checks when the actual agreed feature scope includes HUD elements. A confirmed non-HUD surface has no HUD branch; unresolved scope stays Unknown. Actual HUD budget checks and required current visual inputs remain unchanged.

- **Confirm all HUD elements respect the visual budget** defined in `design/ux/hud.md` (element count, screen region allocations, maximum opacity values)

## Product Interaction Pipeline

Use this pipeline instead of the game UI/HUD pipeline when the target is a
Product web screen, admin flow, CLI interaction, API consumer journey, docs
example, onboarding flow, or workflow state.

### Product Phase 1: Context Gathering

Before designing anything, read and synthesize:
- `design/cdd/product-concept.md` -- user promise, JTBD, target user, platform, Product principles, and adoption blockers
- Relevant module CDDs -- user promise, API/CLI/UI/data requirements, acceptance criteria, permissions, configuration, and integration constraints
- Existing `design/ux/*.md` specs and interaction patterns
- API/CLI docs, schema files, config examples, release notes, and support docs
- Accessibility requirements and any Product design system document

Summarize: who the user is, what workflow they are trying to complete, what
surface is involved (web/admin/CLI/API/docs), what data/state is read or
changed, and which public contracts must not break.

### Product Phase 2: Product UX Spec Authoring

Invoke `/ux-design [feature name]` or delegate to `ux-designer` to produce a
Product UX spec:
- For web/admin/mobile: screens, forms, tables, navigation, error/empty/loading states, keyboard and screen-reader behavior
- For CLI: command shape, flags, stdin/stdout/stderr, exit codes, examples, scripting behavior, error recovery
- For API consumer journeys: request/response flow, auth/permission states, error bodies, docs examples, SDK snippets, rate-limit and retry behavior

Output: `design/ux/[feature-name].md` or the relevant module CDD UX/API/CLI section.

### Product Phase 3: Contract and Implementation Handoff

Spawn `lead-programmer` and the relevant language specialist in parallel:
- Validate API/CLI/UI state ownership and public contract boundaries.
- Identify stack-specific implementation patterns and migration/config impact.
- Confirm observability, logging, and test evidence required for the workflow.

Then delegate implementation to the appropriate programmer:
- Product UI reads data through approved API/state boundaries.
- CLI emits scriptable output and documented exit codes.
- API consumer journeys do not hide contract changes behind UI-only behavior.
- All user/developer-facing strings go through the localization/content path where the project requires it.

### Product Phase 4: Review (parallel)

Delegate in parallel:
- `ux-designer`: Verify workflow clarity, information architecture, empty/error states, and Product principle alignment.
- `lead-programmer` or language specialist: Verify API/CLI/UI contract, data/state ownership, config/migration impact, and implementation feasibility.
- `accessibility-specialist`: Verify keyboard, screen reader, reduced motion, color/contrast, CLI readability, and error-state accessibility.
- `qa-tester`: Verify Product evidence plan for contract, integration, workflow, docs/examples, and accessibility.

All review streams must report before proceeding to Product Phase 5.

### Product Phase 5: Product Polish

- Address all review feedback.
- Confirm errors are actionable and do not expose internal details.
- Confirm docs/examples match the implemented API/CLI/UI workflow.
- Confirm loading, retry, permission denied, invalid config, migration/deploy failure, and rollback/recovery states are covered when applicable.
- Confirm evidence is written or queued under `production/qa/evidence/`.

## Quick Reference — When to Use Which Skill

- `/ux-design` — Author a new UX spec for a screen, flow, or HUD from scratch
- `/ux-review` — Validate a completed UX spec before implementation
- `/team-ui [feature]` — Full pipeline from concept through polish (calls `/ux-design` and `/ux-review` internally)
- `/quick-design` — Small UI changes that don't need a full new UX spec

## Error Recovery Protocol

If any spawned agent (via Task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via AskUserQuestion with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, CDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (UX specs, interaction pattern library updates, implementation files) are
delegated to sub-agents and sub-skills (`/ux-design`, `ui-programmer`). Each enforces the
"May I write to [path]?" protocol. This orchestrator does not write files directly.

## Output

A summary report covering: UX spec status, UX review verdict, visual design status, implementation status, accessibility compliance, input method support, interaction pattern library update status, and any outstanding issues.

For Product projects, the summary must also cover: public surface type
(web/admin/CLI/API/docs), contract impact, implementation handoff owner,
docs/examples impact, QA evidence required, accessibility status, and any
compatibility or migration risk.

Verdict: **COMPLETE** — UI feature delivered through full pipeline (UX spec → visual → implementation → review → polish).
Verdict: **BLOCKED** — pipeline halted; surface the blocker and its phase before stopping.

## Next Steps

- Run `/ux-review` on the final spec if not yet approved.
- Run `/code-review` on the UI implementation before closing stories.
- Run `/team-polish` if visual or audio polish pass is needed.

**[Product] Product next steps:**
- Run `/code-review` on API/CLI/UI implementation before closing stories.
- Run `/test-evidence-review` on Product workflow, contract, docs/example, and accessibility evidence.
- Run `/release-checklist` if the interaction changes deployment, migration, package, docs, or public compatibility behavior.
