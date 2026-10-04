---
name: coc7-campaign-manager
description: "Create and maintain source-bound SagaSmith Call of Cthulhu 7e campaigns. Use for campaign settings, access, investigators/NPCs/creatures, Module and rules Packs, inventory, money, long-term development, scene progress, continuity, ActorKnowledge, branches, snapshots, restore, undo/redo, and regression audits."
---

# Call of Cthulhu 7e Campaign Manager

Use the sagasmith_coc MCP runtime. Campaign truth belongs to the server, not
workspace memory, a local CLI, prose summaries, or direct database writes.

## Start with the runtime

1. Read campaign_query and server_capabilities.
2. Open the correct campaign/principal exposure, search for the smallest
   relevant tool set, expose it, and refresh native schemas.
3. Read game_phase, current branch, campaign revision, relevant character
   revisions, active Module Pack, and pending encounter/check state.
4. Keep administrative work in Lobby. Do not force Lobby while a check, Chase,
   or Combat still requires authoritative settlement.

## Route campaign work

| Work | Search/add native tools | Read deeper |
|---|---|---|
| Create/read campaign | campaign_change, campaign_query | references/CAMPAIGN_MANAGER_DEEP_REFERENCE.md |
| Phase and access | game_phase, campaign_change | ../../references/mcp-contract.md |
| Characters | character_query, character_change | ../coc7-keeper/references/INVESTIGATOR_CREATION.md |
| Inventory and money | inventory_change, wallet_change | references/CAMPAIGN_MANAGER_DEEP_REFERENCE.md |
| Module draft/Pack | module_draft, content_pack, module_query | ../coc7-keeper/references/SCENARIO_INDEX.md; sagasmith-modulegen |
| Rules draft/Pack | rulebook_draft, content_pack, rule_query | ../../references/mcp-contract.md |
| Scene progress | module_query, module_change | ../coc7-keeper/references/SCENARIO_INDEX.md |
| Development | development_query, development_settle, long_term_change | ../coc7-keeper/references/INVESTIGATOR_CREATION.md |
| Objective continuity | memory_query, memory_change, campaign_event | ../../references/memory-ownership.md |
| Actor knowledge | actor_knowledge_query, actor_knowledge_change | ../../references/memory-ownership.md |
| Branch/snapshot/recovery | branch_query/change, snapshot_query/change, state_revision | references/CAMPAIGN_MANAGER_DEEP_REFERENCE.md |

## Campaign setup

- Create only after the user authorizes a new campaign. Record an explicit
  Classic/Pulp ruleset, era, locale, optional Spending Luck setting, and other
  campaign-approved options.
- The authenticated creator becomes the campaign owner. Grant campaign roles and
  actor control only to stable host-authenticated principals.
- Never treat player_name, chat nickname, or a prompt-supplied principal as
  authority.
- Before Play, verify at least one controlled active investigator, one active
  finalized Module Pack or an explicitly improvised Keeper situation, and a
  recoverable current branch.
- Keep two concurrent campaigns isolated by campaign id, exposure/session,
  branch, random stream, revisions, actors, knowledge, and snapshots.

## Character lifecycle

1. Read the applicable ruleset/source and gather the complete investigator,
   NPC, or creature sheet.
2. For a Pack `preset_pc`, use the import response actor_map and instantiate its
   library template into this campaign; otherwise create a reviewed sheet.
3. Present derived values and the complete draft or instantiated sheet for
   player/Keeper review.
4. Persist a new sheet only after the authorized human confirms it; never edit
   the Pack's reusable template into campaign state.
5. Reread the campaign-local character and verify identity, ruleset,
   HP/MP/SAN/Luck,
   characteristics, skills, combat values, conditions, development state, and
   actor authorization.
6. For updates, merge the complete current sheet; do not discard unknown
   campaign-approved fields.

Instantiating a Pack preset grants the Keeper control, not the intended player.
Initialize any source-required rolled field through the authoritative random
stream, then grant the actor to the authenticated player explicitly. See the
investigator lifecycle reference for the exact sequence.

Use inventory_change for stable-id add/update/remove/consume operations and
wallet_change for one campaign-defined monetary field. These are guarded actor
transactions. They do not implement a cross-actor equipment transfer; perform
separate authorized writes and record the realized exchange in continuity.

## Module Pack lifecycle

- Use module_draft only in Lobby. Start from one managed source, review exact
  evidence, apply source/content/statblock/asset/actor/package edits, and
  explicitly finalize the current revision.
- Use the sagasmith-modulegen Skill for the current coc7e schema: scenario,
  campaign, solo_adventure, or handout_pack; all six CoC play-profile sections;
  exact CoC catalogs; reachable endings where required.
- Finalized archives are immutable and remain local for commercial/private
  sources.
- content_pack import is inactive. Activate only with a fresh campaign revision.
  Review replacement progress impact and explicit scene remaps.
- Never activate the mechanical draft module or bypass evidence/finalization.

## Rules Pack lifecycle

- Use rulebook_draft in Lobby for a user-authorized local PDF/Markdown/text
  source. Inspect evidence before finalization; do not encode book-specific
  guesses in Core, system, or MCP code.
- Finalize an immutable private core_rules schema-v2 Pack, then import and
  activate it separately with fresh revisions.
- Use rule_query sources/search/expand/effective in every phase. Treat returned
  evidence and the active rule lock as authoritative source context, while the
  Keeper remains responsible for interpreting ambiguous prose.

## Development

Use development_query and development_settle in Lobby at an authorized
session/scenario improvement boundary:

- Query the current checked skills and eligibility.
- Confirm the correct actor and current campaign/character revisions.
- Settle once with a stable source description and idempotency key.
- The runtime rolls each eligible checked skill, applies increases and first
  mastery SAN where appropriate, clears all marks, and records the receipt.
- Cthulhu Mythos is not an ordinary development check.
- Use long_term_change only in Lobby for campaign-enabled Luck recovery,
  source-explicit therapy, explicit source-reviewed aging deltas, or tome/spell
  study. The Agent supplies printed values and decisions; the runtime owns the
  random stream, SAN/Mythos bounds, source catalogs, revisions, and receipt.
- Credit Rating changes still require a source-backed explicit sheet update;
  do not derive them from wallet values.

## Continuity and recovery

- Use memory for objective durable facts, events for chronology, ActorKnowledge
  for one actor's subjective state, and module progress for scoped discoveries.
- Prefer memory_change(action="commit") when one accepted outcome creates an
  event plus facts plus knowledge and an optional snapshot.
- Snapshot meaningful boundaries. Fork alternatives from an explicit parent
  snapshot and compare branches before explaining divergence.
- Restore is non-destructive history. Verify the target, use current revision
  and branch guards, restore, refresh tools, discard stale context, and reread
  all authoritative state.
- Undo/redo follows the branch revision ledger; it is not a substitute for an
  immutable snapshot.

For exact current facade actions and phases, read
../../references/mcp-contract.md. For ordered setup, Pack, restore, and
parallel-campaign procedures, read references/CAMPAIGN_MANAGER_DEEP_REFERENCE.md.
