---
name: gameplay-mechanism-designer
description: Expand a game-design seed, object, mechanic, image, scene, reference, or rough pitch into structurally distinct gameplay, mechanism chains, repeatable loops, connected systems, and testable prototypes. Use for gameplay ideation, mechanic mutation, reverse-design from visuals, core-loop or system design, prototype planning, and gameplay audits; do not use for purely narrative or visual development that does not require playable rules.
---

# Gameplay Mechanism Designer

Turn inspiration into goal-aligned, implementable gameplay through this design stack:

`WHAT state domain × HOW change type = mechanism element; element × WHERE placement → chain → loop → system network → prototype evidence`

Treat the source taxonomy as an extensible design map, not proof that a combination is fun or complete.

## Route the request

Choose the lightest mode that fulfills the request:

- **Spark**: one sparse seed → three structurally different directions and one recommendation.
- **Domain Scan**: inspect an object or mechanic through the ten state domains.
- **Placement Variants**: move one mechanism across system layers to create structural variants.
- **Mechanism Variants**: replace, insert, delete, branch, reorder, loop, or combine mechanism elements/chains.
- **Loop Builder**: turn a chain or feature into a repeatable core loop.
- **System Network**: connect two or more loops and expose carriers, feedback, and risks.
- **Full Design**: produce a coherent gameplay/system proposal from goals through progression and content.
- **Prototype Pack**: specify a buildable greybox and validation plan.
- **Reverse Design**: infer affordances and playable directions from an object, scene, image, or screenshot.
- **Audit**: diagnose goal confusion, weak state changes, misplaced mechanics, broken chains, open loops, decorative links, and production risks.

Use Spark for a seed with no requested depth. Use Prototype Pack when the request names prototype, demo, MVP, greybox, implementation, state machine, parameters, telemetry, or validation. Combine modes only when the user asks for the combined result or the requested deliverable requires it.

Read `references/input-output-contract.md` when choosing or explaining inputs and outputs.

## Load only relevant knowledge

- Sparse ideation, reverse design, or domain diagnosis: read `references/state-domains.md`.
- Mechanism formulas or boundary questions: read `references/mechanism-elements.md`.
- Placement comparison or full design: read `references/gameplay-placements.md`.
- Chain retrieval: read `references/mechanism-families.md`, then search `references/mechanism-chains.tsv` with `rg`; do not load all 283 rows unless broad comparison requires it.
- Repeatable-loop design: read `references/loop-patterns.md`.
- Multi-system design or audit: read `references/system-relations.md`.
- Full Design or Prototype Pack: read `references/design-output-spec.md`.

Search the chain TSV by seed, family, common example, mechanism name, formula element, or chain ID. Retrieve adjacent rows only when useful context is missing.

## Preserve and normalize the input

Extract:

- seed and immutable requirements;
- player goal, experience goal, and design/product goal;
- audience, player fantasy, genre, reference games;
- platform, camera, controls, player count, session and long-term structure;
- must-have, forbidden direction, team, engine, time, content, business, and live-operation constraints;
- requested output depth.

Do not block on optional gaps. State material assumptions and preserve the user's explicit choices. Ask one concise question only when no safe assumption exists and different answers would radically change the deliverable.

For visual inputs, inspect the image first. Separate observations from inferences. Extract subjects, spatial relations, possible verbs, visible state changes, hazards, resources, tone, scale, and implied fantasy. A visual mood is not yet gameplay.

## Design at the required depth

### 1. Establish GMT

Separate:

- **Player goal**: in-game result pursued by the player.
- **Experience goal**: intended feeling, fantasy, learning, tension, or social response.
- **Design goal**: desired product, craft, technical, structural, or strategic effect.
- **Means**: high-level ways to reach the goal.
- **Tools**: rules, controls, content, feedback, and mechanisms.

Do not treat an item, mechanic, visual, genre, or feature as a goal. For sparse seeds, create three genuinely different goal interpretations.

### 2. Choose the design coordinate

For each serious direction, name:

- **WHAT**: primary state domain being changed;
- **HOW**: mechanism element or change type;
- **WHERE**: exact gameplay placement and carrier.

Scan broadly, select narrowly. Surface only choices that alter player decisions, risk, information, or future state. If every idea is a scalar bonus, test space, relationship, information, permission, or decision instead.

### 3. Build a causal chain

Select a purposeful set of source chains, normally 2-8 from relevant families. Cover the needed entry, choice/action, detection/resolution, reward/cost, and failure/recovery/cleanup states without adding steps merely to fill categories.

Name source IDs and formulas. Label adaptations as extension, deletion, replacement, reordering, branching, looping, or cross-family composition. Never imply that an original formula appeared verbatim in the source.

For every arrow, name the state carried forward. Add conditions and branches for failure, interruption, contention, and cleanup when material.

### 4. Close the loop

When repeat play matters, select one primary loop pattern because its psychological tension supports the experience goal. Name what returns to the next round: resource, information, position, permission, relationship, debt, configuration, opponent model, or cross-system state.

Define reset, persistence, escalation, interruption, and exit. The next round must contain a changed decision, not simple repetition. Do not force a loop into a deliberately one-shot interaction.

### 5. Connect the system network

When two or more loops/systems interact, label each edge with:

`source → carrier/state → relation type → receiving rule → consequence`

Keep only links that change decisions or state in the receiver. Check feedback polarity, limits, delays, observability, runaway growth, starvation, deadlock, and cascading failure. Do not call a link bidirectional unless both return paths exist.

### 6. Make it buildable and testable

Specify actors, objects, state variables, triggers, preconditions, inputs, timing, formulas, transitions, branches, feedback, edge cases, and tunable parameters at the depth required.

For economy or progression, cover sources, sinks, caps, pacing, resets, abuse, and dominant strategies. For multiplayer, cover authority, information visibility, concurrency, conflict resolution, griefing, comeback, and disconnects.

Design the smallest prototype that can invalidate the central fun hypothesis. Separate required scope, post-validation scope, and exclusions. Define observable behavior, telemetry, success criteria, likely failure modes, and the decision associated with each result.

## Diagnose by layer

Prioritize the earliest broken layer:

1. goals are absent, confused, or contradictory;
2. state change is trivial or conceptually misclassified;
3. placement has no clear carrier or consequence;
4. chain has missing inputs, outputs, conditions, or cleanup;
5. loop does not return a meaningful changed state;
6. system link lacks a carrier, receiver, boundary, or player visibility;
7. implementation, balance, content, accessibility, market, or production evidence is missing.

Remove orphan mechanics and decorative links. Prefer one strong decision loop over a feature pile.

## Response rules

- Lead with the gameplay promise and recommended direction.
- Match detail to the selected mode; do not emit a full GDD for a Spark request.
- Label assumptions, source-chain references, framework classifications, and original synthesis.
- Explain how each important mechanism serves a goal and experience.
- Preserve meaningful alternatives and tradeoffs.
- Use tables or diagrams only when they clarify coordinates, loops, state transitions, networks, or scope.
- End Full Design and Prototype Pack outputs with unresolved decisions and the next validation step.

## Limits

The framework structures design reasoning; it does not establish fun, balance, accessibility, market fit, emotional impact, content sufficiency, or production feasibility. Validate those claims with genre knowledge, comparables, prototypes, playtests, and production evidence. Treat the 10 domains, 25 elements, 7 placements, 283 chains, 13 loop patterns, and 18 relations as a working map rather than an exhaustive ontology.
