---
name: team-narrative
description: "Orchestrate narrative/content work. Game: narrative-director, writer, world-builder, and level-designer for story and lore. Product: onboarding story, docs narrative, release messaging, user education, empty-state copy, workflow explanation, and developer examples."
argument-hint: "[narrative content description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate narrative/content work. Game: narrative-director, writer, world-builder, and level-designer for story and lore. Product: onboarding story, docs narrative, release messaging, user education, empty-state copy, workflow explanation, and developer examples.
- Inputs: Command arguments: `/team-narrative [narrative content description]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before orchestrating the team:
- `design/cdd/game-concept.md` -> **[Game]** keep narrative design, worldbuilding, dialogue, pacing, story hooks, and gameplay/story integration.
- `design/cdd/product-concept.md` -> **[Product]** use this command for product narrative/content: onboarding story, docs narrative, release messaging, user education, empty-state copy, workflow explanation, and developer-facing examples.
- If unclear, ask whether the work is game narrative or product content/onboarding narrative.

Game narrative content remains intact. Product content narrative is added beside it.If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `/team-narrative [narrative content description]` — describe the story content, scene, or narrative area to work on (e.g., `boss encounter cutscene`, `faction intro dialogue`, `tutorial narrative`). Do not use `AskUserQuestion` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the narrative team through a structured pipeline.

**Decision Points:** At each phase transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **narrative-director** — Story arcs, character design, dialogue strategy, narrative vision
- **writer** — Dialogue writing, lore entries, item descriptions, in-game text
- **world-builder** — World rules, faction design, history, geography, environmental storytelling
- **art-director** — Character visual design, environmental visual storytelling, cutscene/cinematic tone
- **level-designer** — Level layouts that serve the narrative, pacing, environmental storytelling beats

## Product Content Team Composition

When the Product branch is active, use this same command for onboarding,
documentation, product messaging, release communication, examples, and workflow
education.

- **creative-director** — Product voice, promise alignment, brand narrative, user trust
- **ux-designer** — Onboarding flow, empty/error states, user education moments, comprehension and cognitive load
- **writer** — Product copy, docs narrative, onboarding text, examples, release messaging, empty states
- **lead-programmer** — Technical accuracy for API/CLI/docs examples and public contract wording
- **language specialist** — Stack-specific examples, code snippets, CLI/API usage accuracy
- **localization-lead** — i18n readiness, glossary, tone headroom, terminology consistency

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: narrative-director` — Story arcs, character design, narrative vision
- `subagent_type: writer` — Dialogue writing, lore entries, in-game text
- `subagent_type: world-builder` — World rules, faction design, history, geography
- `subagent_type: art-director` — Character visual profiles, environmental visual storytelling, cinematic tone
- `subagent_type: level-designer` — Level layouts that serve the narrative, pacing
- `subagent_type: localization-lead` — i18n validation, string key compliance, translation headroom

Always provide full context in each agent's prompt (narrative brief, lore dependencies, character profiles). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 2 agents can run simultaneously).

**Product context reads:**
- `design/cdd/product-concept.md` for Product promise, JTBD, principles, target audience, platform, and adoption blockers
- Relevant module CDDs and UX specs for the workflow being explained
- API/CLI docs, README, examples, release notes, onboarding docs, and support notes related to the requested content
- `standards/technical-preferences.md` and ADRs for stack terminology and public contract constraints
- Existing localization glossary or terminology references if present

## Pipeline

### Phase 1: Narrative Direction
Delegate to **narrative-director**:
- Define the narrative purpose of this content: what story beat does it serve?
- Identify characters involved, their motivations, and how this fits the overall arc
- Set the emotional tone and pacing targets
- Specify any lore dependencies or new lore this introduces
- Output: narrative brief with story requirements

### Phase 2: World Foundation (parallel)
Delegate in parallel — issue all three Task calls simultaneously before waiting for any result:
- **world-builder**: Create or update lore entries for factions, locations, and history relevant to this content. Cross-reference against existing lore for contradictions. Set canon level for new entries.
- **writer**: Draft character dialogue using voice profiles. Ensure all lines are under 120 characters, use named placeholders for variables, and are localization-ready.
- **art-director**: Define character visual design direction for key characters appearing in this content (silhouette, visual archetype, distinguishing features). Specify environmental visual storytelling elements for each key space (prop composition, lighting notes, spatial arrangement). Define tone palette and cinematic direction for any cutscenes or scripted sequences.

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
- **localization-lead**: Validate i18n compliance — check string key naming conventions, flag any strings with hardcoded formatting that won't survive translation, verify character limit headroom for languages that expand (German/Finnish typically +30%), confirm no cultural assumptions in text that would need locale-specific variants
- **world-builder**: Finalize canon levels for all new lore entries

## Product Pipeline

Use this pipeline instead of the game narrative pipeline when the request targets
Product onboarding, docs, examples, release messaging, user education, empty
states, workflow explanation, API/CLI guidance, or developer-facing content.

### Product Phase 1: Content Direction

Delegate to `creative-director` and `ux-designer` in parallel:
- Define the user/developer moment this content serves.
- Identify what the user already knows, what they are trying to accomplish, and what could make them abandon the workflow.
- Set voice, trust, and clarity goals from the Product Concept principles.
- Decide whether the output belongs in docs, onboarding UI, CLI help, API docs, examples, release notes, or support content.

### Product Phase 2: Technical and Copy Drafting (parallel)

Delegate in parallel:
- `writer`: draft the content with concrete user/developer language, examples, headings, and empty/error state copy.
- `lead-programmer`: verify that API/CLI/workflow claims are technically true and identify contract or implementation dependencies.
- `language specialist`: validate code snippets, command examples, SDK usage, framework terminology, and stack-specific gotchas.

### Product Phase 3: Workflow Integration

Delegate to `ux-designer`:
- Place the content in the correct user journey moment.
- Check that docs, UI, CLI, and API messages do not contradict each other.
- Confirm that the content reduces friction rather than adding repeated reading.
- Identify any missing state, screenshot, command output, or example needed for comprehension.

### Product Phase 4: Consistency and Localization

Delegate to `creative-director`, `lead-programmer`, and `localization-lead`:
- Verify alignment with Product principles and user promise.
- Verify technical terms, API names, flags, config keys, and examples.
- Check translation headroom, glossary consistency, placeholders, dates, numbers, units, and locale-sensitive wording.

### Product Phase 5: Product Content Output

Produce a summary report covering: content location, user moment, public surfaces
referenced, examples/snippets produced, technical accuracy findings,
localization readiness, and unresolved Product contradictions.

If files are written by sub-agents, route them to the appropriate existing path:
`docs/`, `docs/examples/`, `design/ux/`, `production/releases/`, or the relevant
module CDD. Do not invent a new product-only documentation tree.

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

All file writes (narrative docs, dialogue files, lore entries) are delegated to
sub-agents spawned via Task. Each sub-agent enforces the "May I write to [path]?"
protocol. This orchestrator does not write files directly.

## Output

A summary report covering: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results, and any unresolved contradictions.

Verdict: **COMPLETE** — narrative content delivered.

If the pipeline stops because a dependency is unresolved (e.g., lore contradiction or missing prerequisite not resolved by the user):

Verdict: **BLOCKED** — [reason]

## Next Steps

- Run `/design-review` on the narrative documents for consistency validation.
- Run `/localize extract` to extract new strings for translation after dialogue is finalized.
- Run `/dev-story` to implement dialogue triggers and narrative events in-engine.

**[Product] Product next steps:**
- Run `/design-review` on Product content that changes a CDD, workflow promise, onboarding flow, or public contract.
- Run `/code-review` for API/CLI/docs examples that include executable snippets.
- Run `/test-evidence-review` when docs, examples, or onboarding content claim a workflow is complete.
- Run `/localize extract` if Product UI, CLI, email, notification, or release strings are finalized.
