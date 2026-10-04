---
name: godot-quest-designer
description: "Design and audit reactive quests for Godot games. Use for quest premises, emotional arcs, objectives, branching story graphs, dialogue and gameplay beats, world facts, conditions, consequences, rewards, quest data contracts, journals, save/load continuity, and narrative path testing; use level designer for space and Godot engineer for code-heavy implementation."
---

# Godot Quest Designer

Turn story and emotion into playable, state-safe quests that respect player agency and remain testable in a Godot project.

## Core Rules

1. Inspect the story context, current quest and dialogue data, gameplay verbs, world-state owner, save format, scene transitions, level hooks, UI/journal contract, and Godot version before designing a quest system or branch.
2. Start with the intended player experience: premise, role-playing question, emotional movement, stakes, and world or character change. Do not confuse a lore summary with a playable quest.
3. Express every quest beat through an available player verb, observation, decision, challenge, or consequence. Add new mechanics only when the experience justifies their production and test cost.
4. Make choices legible at the moment of commitment and consequences attributable when they arrive, without spoiling every result.
5. Budget branches by impact. Spend bespoke content where a choice changes a relationship, location, mechanic, or ending; reuse content where variation would be forgettable.
6. Design for out-of-order play, early NPC death, skipped dialogue, alternate solutions, failure, scene unload, save/reload, and revisit. Never assume the player follows the preferred sequence.
7. Separate immutable authored definitions from mutable runtime and saved state. Use stable IDs and explicit condition/effect contracts; never persist node references or rely on display text as identity.
8. Treat CD PROJEKT RED and Larian examples as public design and QA evidence, not formulas, branded prose, or IP to imitate.
9. Combine automated graph/state checks with scripted scenario paths and human narrative playtests. Automation can prove consistency, not emotional impact or fun.

## Workflow

1. Classify the work: quest pitch, objective/branch graph, companion arc, investigation, systemic quest, quest-data contract, journal/UX flow, implementation brief, bug diagnosis, or narrative QA.
2. Record the player promise, story and character prerequisites, available verbs, locations, cast, desired emotion, choice budget, fail policy, rewards, target platform, and acceptance condition.
3. Trace existing quest definitions, facts or tags, condition/effect handlers, signal flow, world actors, dialogue/cinematic hooks, journal UI, persistence, debug tools, and tests before proposing new state.
4. Write the quest spine: hook, player goal, escalation, reversal or discovery, commitment point, climax, resolution, aftermath, and the changed world state.
5. Convert the spine into a graph of explicit states, objectives, conditions, effects, branches, convergence points, failure/recovery paths, terminal outcomes, and delayed callbacks.
6. Create a fact and contract ledger. Give every quest, objective, actor, item, location, outcome, and durable choice a stable identifier, owner, type, default, writer, reader, persistence rule, and invalid-state behavior.
7. Walk the graph as a hostile player: do steps early, late, simultaneously, silently, lethally, non-lethally, with missing items or actors, after scene changes, and across save/reload boundaries.
8. Prototype the riskiest playable beat with placeholder content before commissioning the full asset, cinematic, VO, localization, level, or engineering scope.
9. Hand implementation to `godot-game-creation-engineer` with the quest graph, data schema, condition/effect registry, signal contracts, save migration, debug surface, and scenario tests.
10. Verify functional playability, narrative continuity, consequence readability, pacing, emotional intent, accessibility, localization expansion, and exported-build behavior.

## Verification Loop

1. Run static checks for duplicate IDs, missing references, unreachable states, non-terminal dead ends, invalid cycles, impossible conditions, ambiguous ownership, and unhandled effects.
2. Unit-test condition evaluation, effect application, idempotency, reward delivery, transition legality, and save migration with controlled time and randomness.
3. Run scripted paths for the golden path, every material branch, failure/recovery, completionist, speedrun, and off-sequence cases. Reload at commitment and terminal boundaries.
4. Exercise the quest in the real level with combat, inventory, interaction, party, UI, audio, cinematics, checkpoints, scene transitions, and save/load enabled.
5. Conduct human narrative QA for motivation, pacing, character continuity, agency, emotional impact, and whether consequences feel connected to player action.
6. Before reporting done, load [references/quest-design-workflow.md](references/quest-design-workflow.md) and apply its graph, Godot contract, and path-testing checklists.

## Routing

- Use `godot-level-designer` for spatial flow, grayboxing, traversal, encounter layout, landmarks, and environmental story placement.
- Use `gameplay-consultant` for mechanics, balance, progression, difficulty, economy, and broad player-experience experiments.
- Use `godot-game-creation-engineer` for production scripts, resources, UI, save migrations, tools, debugging, performance, and exports after the quest contract is clear.
- Use `writing-assistant` when the primary task is dialogue or prose craft rather than interactive quest structure.
- Use `testing-engineer` when test framework or suite architecture is the main task rather than narrative path coverage.

## Reference Map

Load [references/quest-design-workflow.md](references/quest-design-workflow.md) for quest and fact templates, branch budgeting, Godot data boundaries, CDPR/Larian public design anchors, content validation, and narrative path testing.

## Tool Output

Use RTK when available for noisy, non-destructive content validation, scripted quest paths, test output, save inspection, or exported-build logs. Inspect raw output before making an exact branch-coverage, persistence, or completion claim.

## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.

## Output Shape

For a quest proposal or audit:

1. player promise, emotional arc, and evidence inspected
2. playable spine and branch graph
3. facts, conditions, effects, and system contracts
4. level, asset, UI, save, and implementation handoffs
5. path matrix and narrative QA evidence
6. branch budget, unresolved states, and next owner
