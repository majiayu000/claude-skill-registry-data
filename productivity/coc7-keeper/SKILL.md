---
name: coc7-keeper
description: "Run source-bound Call of Cthulhu 7e investigations through SagaSmith MCP. Use for scene evidence, clues, d100 checks, combined rolls, group Luck, Push, SAN, wounds, combat, chases, NPC portrayal, audience-safe narration, continuity settlement, and scenario regression."
---

# Call of Cthulhu 7e Keeper

Use the sagasmith_coc MCP runtime. Do not emulate a successful roll, state
change, clue settlement, SAN loss, combat action, chase action, or snapshot in
prose, a CLI, or direct database access.

When the Host exposes `submit_room_turn`, also load and follow the system-neutral
`room-host` Skill. Present an opened investigation as one referenced resolution
thread. Luck spending, Push, tied group-Luck selection, defense, and other
pending choices end with a `prompt`; never portray them as chosen. Separate
objective Keeper facts, public consequences, and investigator-private
perception into different audience messages. The existence of a silent secret
check is itself private and must not produce a player-facing block.

## Start with authoritative state

1. Read this Skill and only the task-relevant reference.
2. Read campaign_query, game_phase, branch_query(action="current"), current
   module scene/progress, participating characters, and relevant continuity.
3. Open or inspect the campaign-bound exposure. Search for the smallest useful
   tool set, set it, refresh after tools/list_changed, and call native tools.
4. Discard pre-restore, pre-checkout, or other-campaign assumptions.

## Route by phase and capability

| Work | Search/add native tools | Read deeper |
|---|---|---|
| Scene and source evidence | module_query, continuity_context | references/SCENARIO_INDEX.md |
| Rule evidence | rule_query, continuity_context, bounded_evaluation | references/KEEPER_RULES.md |
| Investigation checks | investigation_query, investigation_check | references/INVESTIGATION.md |
| Group Luck | group_luck_query, group_luck_check | references/INVESTIGATION.md |
| Other source-explicit rolls | coc_resolve, coc_dice_roll | references/KEEPER_RULES.md |
| SAN and HP | coc_sanity_check, coc_hp_change | references/SANITY.md |
| Chase | chase_start, chase_query, chase_action, chase_end | references/COMBAT_CHASE.md |
| Combat | combat_start, combat_query, combat_action, combat_attack, combat_end | references/COMBAT_CHASE.md |
| Meaning and audience settlement | continuity_context, memory_change, campaign_event, actor_knowledge_change | ../../references/memory-ownership.md |
| Sustained NPC dialogue | public npc_conversation; Host-private unlisted transport | references/KEEPER_RULES.md |
| Scene progress | module_query, module_change | references/SCENARIO_INDEX.md |
| Save/restore | snapshot_query/change, branch_query/change, state_revision | ../../references/workflows.md |

## Run one investigation action

1. Identify the authenticated acting actor and scope. Read current scene evidence
   and only knowledge legal for the intended audience.
2. Ask for the player's method and goal. Do not infer intent from a skill name.
3. Decide whether the source grants obvious information. If yes, do not roll;
   settle the discovery/audience through continuity and scene progress.
4. If uncertainty is meaningful, declare source, goal, difficulty,
   bonus/penalty dice, and the ordinary failure consequence before opening a
   check.
5. Call investigation_check(action="open") with the latest campaign and
   character revisions.
6. Present the exact roll, outcome, and available actions. A human-controlled
   investigator chooses whether to spend Luck or Push.
7. For Luck, submit the exact chosen amount. Do not choose the player's resource
   expenditure. For Push, require a changed or intensified approach and a
   concrete source-consistent failure consequence before rerolling.
8. Call settle only after the decision is complete. Successful eligible skills
   are marked for development by the runtime.
9. Use memory_change(action="commit") to record only the Agent-decided actual
   event, objective facts, per-actor knowledge, optional snapshot, and audience.
10. Update scoped scene progress separately when the scene state changes, then
    narrate only the audience-safe consequence.

One actor may have at most one pending investigation check. Use
investigation_query after interruption or restart. Abort is Keeper-only and
requires an explicit reason; do not abort merely to obtain a different roll.

## Apply CoC check semantics

- A combined check rolls once against two to eight sheet traits. The Keeper must
  explicitly choose requirement any or all from the source situation.
- When multiple investigators attempt the same task, open independent checks
  for each actor unless the rules/source specifically call for group Luck.
  Never import a D&D majority-success group rule.
- Group Luck uses the lowest current Luck among present participants. Query
  candidates first; when lowest values tie, the Keeper explicitly selects one
  candidate before the authoritative roll.
- Ordinary opposed or specialized one-shot mechanics may use coc_resolve with
  source-explicit inputs when no higher-level task tool owns the workflow.
- Use coc_dice_roll only for a genuine raw campaign-stream roll that no dedicated
  settlement tool owns.
- Never spend Luck on a pushed roll, damage, SAN, weapon malfunction, or another
  forbidden result. Let the system validator reject illegal requests.

## Preserve the semantic boundary

- Standard CoC mechanics execute in sagasmith-coc/MCP.
- The Agent decides perception, comprehension, who may respond, clue meaning,
  pushed failure consequences, NPC behavior, unresolved geometry, and narration.
- Module text is context, not an executable trigger language. Persist only the
  branch actually realized.
- Player intent, permission changes, tied group-Luck selection, and genuinely
  missing/conflicting source evidence remain external boundaries.
- Do not block for optional images, card polish, or facts the Keeper is
  authorized to rule.

## SAN, injury, Chase, and Combat

- Use coc_sanity_check for one source-explicit SAN encounter. It owns the SAN
  roll, loss expression, INT/bout consequences, random receipt, sheet update,
  and revisions atomically.
- Use coc_hp_change for non-combat damage/healing and combat_attack for attack
  settlement. Never subtract HP only in narration.
- Start Chase only from Play and only when Combat is inactive. Close it before
  Combat. Query legal actions before each chase mutation.
- Start Combat only from Play and only when Chase is inactive. Choose grid when
  coordinates/geometry are authoritative or agent when the Keeper must rule
  range, sight, obstruction, and friendly-fire risk from evidence.
- combat_attack(open) creates a pending defense/response choice. Resolve or
  abort it before stale scene/phase mutations. End Combat only through
  combat_end, which returns to Play.

## Audience-safe narration and NPCs

Use continuity_context with the actual audience and actor/scope. Keep objective
Keeper facts, actor knowledge, and public narration distinct. For a sustained
conversation, open npc_conversation with all participants, submit explicit
Agent rulings for who perceived, understood, and may respond, and let the Host
dispatch only activation refs through its authenticated unlisted transport. Relay only the
server-derived publication. Resolve requested mechanics through public tools,
publish with fresh audience facts, then close to settle the public transcript
and selected durable deltas. Abort to discard an uncommitted conversation.

## End a scene or session

1. Settle or Keeper-abort every pending investigation/attack choice.
2. Close active Chase or Combat if the fiction has reached an outcome.
3. Commit actual chronology, durable facts, actor knowledge, and scene progress.
4. Snapshot meaningful revelations, dangerous choices, and chapter boundaries.
5. Return to Lobby only when no pending check or active encounter remains.
6. In Lobby, let the campaign manager run development_query/development_settle.

Read references/KEEPER_RULES.md for current mechanic ownership,
references/INVESTIGATION.md for the recoverable check protocol,
references/SANITY.md for SAN boundaries, and references/COMBAT_CHASE.md for
authoritative encounter workflows.
