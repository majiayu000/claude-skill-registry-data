---
name: team-narrative
description: "Use when story content, world lore, writing, and level narrative need coordinated development."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Narrative

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$team-narrative [narrative content] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `narrative-director`
- `writer`
- `world-builder`
- `level-designer`

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

### Phase 1: Narrative Direction
Delegate to **narrative-director**:
- Define the narrative purpose of this content: what story beat does it serve?
- Identify characters involved, their motivations, and how this fits the overall arc
- Set the emotional tone and pacing targets
- Specify any lore dependencies or new lore this introduces
- Output: narrative brief with story requirements

### Phase 2: World Foundation (parallel)
Delegate the three independent, bounded briefs concurrently and collect every result before parent synthesis:
- **world-builder**: Create or update lore entries for factions, locations, and history relevant to this content. Cross-reference against existing lore for contradictions. Set canon level for new entries.
- **writer**: Draft character dialogue using voice profiles. Ensure all lines are under 120 characters, use named placeholders for variables, and are localization-ready.
- **world-builder**: Define character visual design direction for key characters appearing in this content (silhouette, visual archetype, distinguishing features). Specify environmental visual storytelling elements for each key space (prop composition, lighting notes, spatial arrangement). Define tone palette and cinematic direction for any cutscenes or scripted sequences.

### Phase 3: Level Narrative Integration
Delegate to **level-designer**:
- Review the narrative brief and lore foundation
- Design environmental storytelling elements in the level
- Place narrative triggers, dialogue zones, and discovery points
- Ensure pacing serves both gameplay and story

### Phase 4: Review and Consistency
Delegate to **narrative-director**:
- Review all dialogue against character voice profiles
- Verify lore consistency across new and existing entries
- Confirm narrative pacing aligns with level design
- Check that all mysteries have documented "true answers"

### Phase 5: Polish (parallel)
Delegate in parallel:
- **writer**: Final self-review — verify no line exceeds dialogue box constraints, all text uses string keys (not raw strings), placeholder variable names are consistent
- **writer**: Validate i18n compliance — check string key naming conventions, flag any strings with hardcoded formatting that won't survive translation, verify character limit headroom for languages that expand (German/Finnish typically +30%), confirm no cultural assumptions in text that would need locale-specific variants
- **world-builder**: Finalize canon levels for all new lore entries

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

## Changeset Gate

Delegated agents return drafts or read-only evidence to the parent. The parent synthesizes every proposed edit, lists all affected paths and material changes, and requests one complete changeset approval. After approval, implementation stays within that boundary; any expansion pauses for a revised approval.
## Output

A summary report covering: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results, and any unresolved contradictions.

Verdict: **COMPLETE** — narrative content delivered.

If the pipeline stops because a dependency is unresolved (e.g., lore contradiction or missing prerequisite not resolved by the user):

Verdict: **BLOCKED** — [reason]

## Next Steps

- Run `$design-review` on the narrative documents for consistency validation.
- Run `$localize extract` to extract new strings for translation after dialogue is finalized.
- Run `$dev-story` to implement dialogue triggers and narrative events in-engine.
