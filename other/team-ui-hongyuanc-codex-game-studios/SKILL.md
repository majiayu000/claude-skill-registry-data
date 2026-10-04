---
name: team-ui
description: "Use when a UI feature needs coordinated UX, art, implementation, accessibility, and QA work."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Ui

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$team-ui [UI feature] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `ux-designer`
- `art-director`
- `ui-programmer`
- `accessibility-specialist`
- `qa-tester`

## Delegation Plan

- Delegate only tasks that are independent and bounded.
- Name the Codex custom-agent role and the exact artifact or evidence it must return.
- Team members must not spawn additional agents (`agents.max_depth = 1`).
- The parent agent synthesizes all results, resolves overlap, and communicates with the user.
- No subagent commits, publishes, or expands scope.
- Parallel delegation is read-only or draft-only until the parent presents a consolidated result.
- Any multi-file implementation requires one complete changeset approval before work begins.
- If a delegated task blocks, surface the evidence and stop dependent work while preserving independent results.

## Pipeline

Every phase before `## Parent Changeset Gate` is read-only or draft-only. Phase 1 returns context, UX, and review drafts; no agent writes specs, assets, source, tests, or pattern files.

### Phase 1a: Context Gathering

Before designing anything, read and synthesize:
- `design/gdd/game-concept.md` — platform targets and intended audience
- `design/player-journey.md` — player's state and context when they reach this screen
- All GDD UI Requirements sections relevant to this feature
- `design/ux/interaction-patterns.md` — existing patterns to reuse (not reinvent)
- `design/accessibility-requirements.md` — committed accessibility tier (e.g., Basic, Enhanced, Full)

**If `design/ux/interaction-patterns.md` does not exist**, surface the gap immediately:
> "interaction-patterns.md does not exist — no existing patterns to reuse."

Then use `request_user_input` with options:
- (a) Have `ux-designer` return a read-only in-memory pattern-library draft intended for `design/ux/interaction-patterns.md`
- (b) Stop here and establish the pattern library in a separately approved workflow

Do NOT invent or assume patterns from the feature name or GDD alone. If the user chooses (a), the draft is not written and its exact path/content must enter the parent changeset gate. If the user chooses (b), stop without invoking another skill.

Summarize the context in a brief for the ux-designer: what the player is doing, what they need, what constraints apply, and which existing patterns are relevant.

### Phase 1b: UX Spec Authoring

Delegate only to `ux-designer` for a read-only in-memory UX artifact draft. Do not invoke a write-capable skill. The delegate reads these references without modifying them:

- `../../../.codex/docs/templates/ux-spec.md` for screens and flows
- `../../../.codex/docs/templates/hud-design.md` for HUD work
- `../../../.codex/docs/templates/interaction-pattern-library.md` when a pattern-library draft is required

The `ux-designer` returns the complete draft, its exact intended path such as `design/ux/[feature-name].md`, the template used, and any unresolved decisions. It writes no file and does not expand scope.

### Phase 1c: Draft Readiness Check

Have `ux-designer` compare the in-memory artifact against the selected template and return a section-completeness checklist. Keep the artifact and checklist in memory for parent synthesis; no skill or agent writes pre-gate.

### Phase 2: Visual Design

Delegate to **art-director**:
- Review the full UX spec (flows, wireframes, interaction patterns, accessibility notes) — not just the wireframe images
- Apply visual treatment from the art bible: colors, typography, spacing, animation style
- Check that visual design preserves accessibility compliance: verify color contrast ratios, and confirm color is never the only indicator of state (shape, text, or icon must reinforce it)
- Specify all asset requirements needed from the art pipeline: icons at specified sizes, background textures, fonts, decorative elements — with precise dimensions and format requirements
- Ensure consistency with existing implemented UI screens
- Output: visual design-spec draft with style notes and asset manifest

## Parent Changeset Gate

The parent synthesizes the UX, visual, engine, implementation, and pattern-library proposals before any mutation. Present one complete proposal containing exact file paths, exact diffs, tests and evidence, and all session-state, report, and milestone writes (use `None` where no such write exists). Obtain approval for the whole changeset; a new path or material change requires a revised proposal.

## Approved Execution

Only after approval may the parent execute or delegate the exact approved changes. No subagent commits, publishes, or expands scope. Every delegate receives only its approved paths, diffs, tests, and acceptance criteria.

First, the parent writes the approved UX artifact and any approved pattern-library artifact to their exact paths. Then run the read-only `$ux-review` on the saved UX path. If review requires material revision, stop and return the revised exact diff to `## Parent Changeset Gate`; do not continue implementation under stale approval.

### Phase 3: Implementation

Before implementation begins, have `ui-programmer` read the Engine Specialists → UI Specialist guidance in `.codex/docs/technical-preferences.md` and return engine-specific implementation notes with the draft:
- Which engine UI framework should be used for this screen? (e.g., UI Toolkit vs UGUI in Unity, Control nodes vs CanvasLayer in Godot, UMG vs CommonUI in Unreal)
- Any engine-specific gotchas for the proposed layout or interaction patterns?
- Recommended widget/node structure for the engine?
- Output: engine UI implementation notes to hand off to ui-programmer before they begin

If no engine is configured, mark the engine-specific notes N/A.

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
- **Confirm all HUD elements respect the visual budget** defined in `design/ux/hud.md` (element count, screen region allocations, maximum opacity values)

## Quick Reference — When to Use Which Skill

- `$ux-design` — Author a new UX spec for a screen, flow, or HUD from scratch
- `$ux-review` — Validate a completed UX spec before implementation
- `$team-ui [feature]` — Full pipeline that drafts, approves, and uses an approved UX spec before implementation and polish
- `$quick-design` — Small UI changes that don't need a full new UX spec

## Error Recovery Protocol

If any delegated agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via request_user_input with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## Output

A summary report covering: UX spec status, UX review verdict, visual design status, implementation status, accessibility compliance, input method support, interaction pattern library update status, and any outstanding issues.

Verdict: **COMPLETE** — UI feature delivered through full pipeline (UX spec → visual → implementation → review → polish).
Verdict: **BLOCKED** — pipeline halted; surface the blocker and its phase before stopping.

## Next Steps

- Run `$ux-review` on the final spec if not yet approved.
- Run `$code-review` on the UI implementation before closing stories.
- Run `$team-polish` if visual or audio polish pass is needed.
