---
name: ftb-quest-authoring
description: Design, implement, balance, validate, and release FTB Quests chapters for any Minecraft modpack. Use when an agent must turn a modlist, player goals, progression state, economy, or art assets into playable quests; edit or generate FTB Quests SNBT and localization; audit quest graphs, layouts, reward economies, or image paths; run static and in-game checks; or prepare a Packwiz/Git release. Treat the installed pack as the source of truth and avoid custom KubeJS by default.
---

# FTB Quest Authoring

Build quests that give a server a reason to play together without letting a grinder, a lucky drop, or a reward loop decide who wins. Keep the method pack-agnostic: discover IDs, recipes, currencies, task syntax, and art conventions from the supplied pack instead of carrying assumptions from another pack.

**Rule precedence:** economy and balance safety outrank every other rule in this skill. When guidance conflicts, resolve in favor of the stricter economic reading; breaking the economy breaks the world. Prose quality, art, pacing, and completeness all yield to it, and the resolution is noted in authoring notes.

## 1. Establish the brief

Always discover or establish a persistent server-specific configuration/rules doc (e.g., `SERVER_RULES.md` in the project root or docs) before authoring or modifying chapters. This document records server-specific boundaries: active factions, allowed/forbidden chapters, opt-out rules, PvP/pranking consent boundaries, and chapter quotas. Refer to it on every quest edit.

Collect only the missing decisions that could change the design. Record:

- audience, active headcount, expected absences, and veteran/new-player mix;
- current progression (tools, armor, machines, bosses, Pokemon/creatures, magic tiers, and known outliers);
- preferred activities and activities the group avoids;
- social shape: solo, teams, server-wide cooperation, or optional competition;
- cadence: one-session events, a linked week, or a longer chapter; typical session length;
- challenge and gating: casual, meaningful, or expert; optional, guiding, or mandatory;
- reward currency, existing sinks, and rewards that would damage the economy;
- desired art/lore polish and the acceptance test (local parse, server smoke test, or live playtest).

Do not repeat answers already present in the request. If a high-impact value is unknown, state a reasonable assumption and make it easy to revise.

For standard multi-faction campaigns, organize starting progression into foundational chapters: (1) Introduction & Rules (minimal closed-loop onboarding), (2) Choosing a Faction (symmetrical presentation of core faction paths + protected neutral opt-out path), followed by dedicated chapters for each primary faction. Never create unprompted third/splinter faction progression chapters, and never create joint/cooperative cross-faction progression chapters unless explicitly requested in the server brief. Structure each faction chapter using the **Core Parity Spine + Specialized Branches** architecture:
- **Core Parity Spine (Themed/Reskinned for flavor, structurally mirrored for balance):** Mirrored milestone tiers (Tier 1: Foundation/Settlement -> Tier 2: Workstations & Infrastructure -> Tier 3: Logistics & Power -> Tier 4: Faction Capstone) that maintain identical progression depth, pacing, and economic reward tiers so no faction gains an unfair server advantage.
- **Specialized Mod Branches (Exclusive gameplay loops):** Off-shooting branches attached to the core nodes that engage exclusively with the specific mods in the pack assigned to that faction's identity (unique mod mechanics, exclusive workstations, mod-specific abilities, distinct palette builds, and tailored challenges). These ensure factions do not feel like cookie-cutter clones and provide unique gameplay experiences.

Determine whether the world is persistent, seasonal, or event-based before framing the campaign. Do not imply a wipe, finale, or disposable "season" when the intended experience is a long-lived SMP; use civic milestones, evolving roles, maintenance, and future hooks instead.

## 2. Inspect the actual pack before writing

Use the repository and installed artifacts as the authority.

1. Check git status and preserve unrelated work.
2. Locate the modlist/version files (pack.toml, index.toml, launcher manifests, or equivalent) and list the installed mods. Prefer the pack's existing helper scripts and packwiz list; run packwiz refresh after edits when Packwiz is present.
3. Identify the authoritative authoring representation before writing: live SNBT/localization, a generator, or another source model. Compare generated output with live files. Never run a whole-campaign generator over richer authored files merely because the generator exists; update it, generate into a scratch directory for review, or protect it behind an explicit overwrite flag.
4. Read several existing FTB Quests chapters, reward tables, translations, and resource-pack definitions. Copy their SNBT shape, ID conventions, layout, and version-specific fields rather than inventing a new dialect.
5. Resolve every proposed item, block, entity, advancement, statistic, recipe, currency, and reward from actual JARs, data packs, configs, recipe viewers, or authoritative mod docs. Never guess an ID because its display name looks plausible.
6. Verify survival obtainability for every item and reward. Never assign internal, backend, or creative-only items (such as blank scrolls or debug items) in tasks or rewards.
7. Keep domain-specific utility items in their intended mechanic lanes (for example, Create super glue belongs to Create/aerowork quests, not generic building or faction rewards).
8. Inspect kubejs/ only to understand available behavior. Do not add custom KubeJS for quest logic unless the user explicitly changes that requirement.
9. Inventory image references and the JAR/resource-pack paths that can satisfy them. Keep resource paths POSIX-style (/) even when working on Windows.
10. Map the station-and-consumable loop before designing a mod's progression line: survey its recipe tree and item registry to identify the core crafting station / apparatus (primary interaction block), base catalysts / reagents (raw consumable inputs), and peak operational outputs (highest-tier consumables, longest-duration draughts, or advanced ammunition types). Mapping this loop beforehand prevents disconnected tasks and ensures rewards feel genuinely impactful.

If the pack has no existing quest examples, use the FTB Quests version shipped by the pack and validate a tiny throwaway chapter before building the full one.

## 3. Design the chapter around the server

Translate the brief into a compact loop:

1. Hook/session opener - a short, completable first quest that explains the fiction and gives a useful but non-snowballing nudge.
2. Choice routes - usually three to five routes across the group's preferred activities. Make routes roughly equivalent in time and power, not identical in materials.
3. Shared or capstone moment - a co-op build, raid, expedition, showcase, or other event that creates a story without forcing every player to grind the same item.
4. Utility sink - a repeatable, clearly priced exchange using the pack's real currency. Give player choice among convenience, infrastructure, cosmetic/status, and modest combat/collection help.

Use dependencies and "complete any N of M" patterns to reward breadth without making attendance a prerequisite. Separate personal progression from server-wide milestones. Use honor-system checkmarks for social/build/showcase verification when no standard task detector exists.

### Graph-truth rules

- For a true any-N-of-M gate, attach all M alternatives to the same intended predecessor, make the capstone depend on all M, and set its minimum to N. Simulate the shortest path: a hidden shared prerequisite must not turn “any three” into “this mandatory quest plus three.”
- Mark non-gating side quests with the installed schema's explicit optional flag when available. Being absent from the main capstone dependencies makes a quest mechanically optional, but may not communicate that in the UI.
- Keep world-building, equipment/workstations, and mod progression as visibly separate lanes when they serve different player motivations. Do not disguise a build as an item tutorial.
- Re-check reachability, dependency direction, minimum counts, and layout after every graph edit; a parseable acyclic graph can still express the wrong progression.
- Use closed-loop topology for mandatory rules, safety policy, or required onboarding: every required clause must feed the final acknowledgement, and later chapters must depend on that terminal gate when the brief calls for a strict lock.
- Use open branches for genuine choices such as factions or specialties, arrange equivalent choices symmetrically, and reconverge them through an explicit breadth gate rather than an arbitrary subjective review.
- Focus faction progression strictly on the pack's primary factions; discourage and never invent splinter factions or unprompted third-faction progression lines. Never create joint-faction or forced co-op chapters unless explicitly instructed. Provide an explicit Neutral / Civic opt-out path for players who wish to opt out of conflict, giving practical survival jump-starts (full iron armor/tools, bed, food, currency) and completing onboarding, but **never author a dedicated progression chapter or questline for the neutral opt-out path**.
- Keep playful sabotage and conflict quests strictly claim-safe under FTB Chunks / FTB Teams protections. Replace untrackable griefing, mock duels, or territory invasions with tangible, survival-friendly mechanics (such as photography recon/propaganda via Exposure camera and film, harmless throwables, or craftable prank tools).

Balance against the slowest regular player and the server's current state, not its most advanced outlier. Let questing make life meaningfully easier while preserving the value of ordinary play.

### Anti-runaway rules

- Avoid currency-positive loops, buy/sell arbitrage, duplication routes, and rewards that generate their own input.
- Do not skip an entire progression tier, hand out early armor/rare drops, or make one route strictly best.
- Cap repeatable value by cooldown, price, stock, or a weekly/server milestone; choose the least disruptive limiter supported by the installed schema.
- Prefer player choice over a single optimal reward and keep team rewards intentional. Decide whether progress and rewards are individual or team-scoped for every quest.
- Give catch-up utility (tools, ingredients, transport, information) rather than a permanent power lead.
- Budget the worst-case reward if every active player completes every repeatable quest.
- Keep separate ledgers for one-time personal issuance, one-time team issuance, the minimum intended route, completionism, repeatable income, and paid sinks. Model team fragmentation as well as one shared team.
- Treat a native choice claim as the number of entries the installed implementation actually grants. Do not multiply currency exposure by unrelated table metadata such as display/loot size without verifying the semantics.
- When the pack has a central server-issued currency and real server sinks, make currency the default reward for substantive progress and combine it with useful thematic items. Currency without desirable sinks has no durable value.
- **Stage Relevance and Milestone Scaling:** Evaluate the intended game stage and requirements for a quest when deciding on the reward. Later quests and quests with harder requirements must have proportionally better, higher-tier rewards. Rewards should always be strictly relevant and immediately useful to the intended game stage (e.g., survival basics for starter tiers, infrastructure/automation for mid tier, advanced alloys/capstones/high currency for late tier).
- Scale currency rewards dynamically with quest tree depth and milestone weight. Do not award flat starter pocket change (1-2 low coins) on late or deep milestone quests; increase coin volume or step up coin denominations (e.g., Bevel -> Sprocket -> Cog -> Crown) as progression deepens.
- Set rewards near the most generous value justified by the verified challenge and current progression band. Pair currency with a useful thematic bundle on substantive quests unless the bundle would create a tier skip, duplication route, or faction advantage. The bundle is always intended; omit it only when every candidate bundle is unsafe, and record that omission in authoring notes.
- Follow the full-set threshold rule: when awarding specialized crafting materials (such as armor runes, portal obsidian, or weapon ingots), award enough to complete a full functional craft (e.g., 4 runes for a 4-piece armor set, 16 obsidian for a nether portal with corners, complete ingots/blocks for a weapon) rather than unusable single fragments.
- Align rewards to stage utility: early rewards should solve immediate survival friction (armor, weapons, food, bedding, basic tools) rather than dormant high-tier materials. Mid-game quests should supply infrastructure solutions (such as leads, fences, and gates alongside blood altar/animal penning quests; brewing stands and potion ingredients for alchemy).
- Provide meaningful consumable batches: avoid token scraps (such as 2 common ink, 1 stake, 4 emeralds). Award useful batches (such as 16 rare + 4 epic ink) and balanced early/mid utility or combat spells that exist in the pack.
- Measure item rewards against recipe and gameplay thresholds. A loose component that cannot enable a craft, service, or meaningful next step is inventory clutter; award a usable bundle or currency/player-choice utility instead.
- Keep adjacent item rewards distinct. Scale late-game rewards beyond repeated starter lighting, scaffolding, or token raw materials while still avoiding tier skips and faction imbalance. Consumable items (food, fuel, ammunition, bottles, film) are an exception to the uniqueness rule when the repeat appears in a different chapter.
- Never reward an item that is later used as a task condition in any descendant quest, and never use a rewarded item as a later condition. Either the reward changes or the condition does — check every reward against all downstream tasks, not just the next quest.

### Player-facing writing contract

- **Gameplay-Driven Progression Over Lore Bloat:** Treat quests as gameplay and progression tools first. Focus on clear mechanical objectives, workstations, recipes, and survival unlocks. Avoid author-invented lore chapters, extensive backstories, or narrative fluff unless the user explicitly requests a lore-heavy campaign.
- Quest text is for players. Keep guarantees, balance claims, implementation notes, admin policy, and validator language out of titles, subtitles, and bodies.
- Treat the quest book as scaffolding for a player-driven sandbox. Prefer world consequences, player roles, and reusable places over an elaborate author-invented cast or fixed history unless the user explicitly wants authored lore.
- Make each quest answer three questions in one coherent body: why do this, what does it enable or change, and what follows from doing it. If the body needs several sections or a long bullet list, split it into multiple quests.
- Keep graph titles short—normally two to four words—and move lane/type labels and suitability into subtitles. Preserve a visible price or consent warning when hiding it would mislead players.
- **Never use unescaped `& ` (ampersand followed by whitespace) in titles, subtitles, group names, or descriptions.** FTB Quests uses `&` as a formatting code prefix; unescaped whitespace after `&` breaks text rendering with `Invalid formatting! You must escape whitespace after & with \&!`. Use the word `and` or properly escape formatting symbols.

Read [references/player-facing-campaign-design.md](references/player-facing-campaign-design.md) whenever writing or revising quest prose, mandatory onboarding, persistent-world pacing, verification rules, reward bundles, or faction visibility.

## 4. Implement with native FTB Quests features

Copy a nearby working SNBT object and change the smallest possible surface area. Keep IDs unique, stable, and easy to trace. Use only task/reward types supported by the installed FTB Quests build.

- Use item/block/entity tasks for observable inventory or world state.
- Use advancement tasks for mod progression; include the schema-required criterion field (an empty criterion commonly means the whole advancement, but verify against the installed version).
- Detect faction joining using native mod items and advancements (e.g., obtaining `vampirism:vampire_fang` + advancement `vampirism:vampire/become_vampire`; crafting/using `vampirism:injection_garlic` + advancement `vampirism:hunter/become_hunter`). Do not invent ungrounded lore rituals.
- Use stat tasks only with a real statistic ID and text that matches its trigger (for example, a battle-start statistic should say "enter/start a battle," not "win").
- Use checkmark tasks for trust-based completion, social verification, or a human-reviewed build rather than introducing a script.
- Give substantive non-explanatory quests a hard, native criterion wherever the installed pack can verify one. A checkmark-only quest should usually be optional or explanatory; otherwise require meaningful prerequisites and keep its payout modest. Do not make server currency its primary reward by default.
- Do not write custom code (KubeJS, integration glue, custom task types) unless a dev clears it and no native path achieves the result. Do not attempt faction/class state integration without native support unless expressly requested and then validated; do not add custom checks unless the dev really wants them.
- Never require untrackable in-world construction, multiblock structures, or complex fluid piping setups.
- Use the **Palette Quest pattern** for building incentives: require gathering a curated, accessible starter palette of thematic building blocks (favoring accessible items like normal lanterns/fences over tedious items like tinted glass/soul lanterns). Reward with abundant matching building blocks (2x-3x stock, stonecutters) plus substantial crafting materials (diamonds, iron, obsidian, andesite alloy). This enforces a coherent aesthetic theme, equips players with materials to build, and provides high-value completion incentives without untrackable block placement.
- For multiblocks and progression stations (such as altars, inscription tables, hunter tables, and blood containers), base tasks strictly on acquiring/crafting the core item components and storage tanks in inventory, not on world assembly.
- For a human-reviewed build, do not also consume a duplicate material bundle unless the quest is intentionally a donation. Placed blocks already cost resources; an extra consumed task can charge players twice. Use a non-consuming item preview, a checkmark, or a deliberate public-stock contribution.
- For an any-of-many branch, set the installed schema's minimum dependency count and test the actual shortest and maximum paths.
- Set an explicit optional quest flag for side stories when supported; do not rely only on the absence of downstream dependencies.
- For a repeatable currency exchange, make the input an item task that consumes exactly the displayed price, set a deliberate cooldown, and set team_reward deliberately on every reward. A team-scoped task can let one payer unlock rewards for others if this is left implicit.
- Use existing reward tables or native item/command/reputation rewards. Resolve every item component, count, and namespace before committing. Issue central currency directly as a guaranteed fixed reward; never place it as an entry in a random or choice reward table.
- **Choice Rewards & Registry Isolation:** Use interactive Choice Rewards for branching archetypes (e.g., choosing between distinct weapons, staffs, or utility foci) to provide player agency without doubling the player's power budget or cluttering inventories.
- **FTB Quests Reward Table ID Partitioning:** FTB Quests stores chapters, quests, tasks, reward items, and reward tables in a single shared internal registry (`questObjectMap`). Allocate reward tables an isolated, non-overlapping ID space (such as a dedicated prefix or offset) distinct from quests, tasks, and item rewards. If a reward table shares an ID with any quest, task, or item reward, the engine's `readID()` deserializer detects a collision and reassigns the table a random runtime ID, breaking the quest's choice interface.
- **Choice Reward SNBT LongTag Serialization:** Choice reward `table_id` fields must always serialize as typed 64-bit longs (e.g., `table_id: 8796029108802813953L`). Serializing `table_id` as a string causes `tag.getLong("table_id")` to evaluate to `0L`, resulting in a null table lookup and an unresponsive choice reward.
- **Strict Data Component / Codec Schemas (1.20.5+ / 1.21+):** When specifying item components (e.g. Iron's Spells scrolls, potion containers, complex modded items), ensure the SNBT matches the exact Java `RecordCodecBuilder` structure. Missing mandatory codec fields (such as `maxSpells: 1`, `mustEquip: false`, `spellWheel: false`, or slot `index: 0` in `irons_spellbooks:spell_container`) causes item deserialization failures and marks chapters with a red exclamation mark (`!`).
- State whether an item task is an inventory inspection, consumed hand-in, or world-placement requirement. Never ship a placeholder task or an unresponsive social action as though it were functional.
- Do not reward an item immediately before a task that merely detects possession of that same item; test the actual mechanic or a later consequence so the quest does not auto-complete from its own prerequisite reward.
- If a quest has a faction/class anti-condition, hide it from currently ineligible players using verified native visibility support. If the shipped version cannot express that safely, redesign the condition or provide an accessible alternative instead of showing an impossible quest.

When multiple agents author in parallel, assign exclusive chapter/file ownership and reserve non-overlapping quest, task, and reward ID ranges. Keep localization, manifests, indexes, and shared reward tables under one integration owner. Subtasks should not regenerate the campaign, commit, push, or revert another worker's edits unless explicitly assigned.

Read references/ftb-quests-patterns.md for portable templates and an audit checklist. Treat examples there as patterns, not as pack-specific IDs.

## 5. Add art without creating fragile assets

Reuse the pack's existing resource-pack namespace, dimensions, typography, and naming. Add custom art only when it improves orientation or the emotional beat of a quest.

- Keep image namespace:path references exact and use forward slashes.
- Put files at the path the client actually loads; check case and extension.
- Validate pack.mcmeta for the target Minecraft version and update hosted asset metadata/digests whenever a .pw.toml points to a new release.
- Search every quest image reference across the JARs and resource-pack ZIPs; a visually polished chapter with one missing texture is not complete.
- Distinguish an unresolved custom-resource reference from an unresolved built-in mod/Minecraft texture. A renderer given only a custom resource ZIP cannot prove native textures are missing; validate each namespace against the resource source that owns it.
- Do not commit generated binaries that the pack's distribution rules exclude; publish large assets through the project's established release mechanism.

## 6. Validate before calling it done

Run the narrowest useful checks, then expand them in proportion to risk:

1. Repository/Packwiz: inspect the diff, run packwiz refresh and packwiz list when available, then run refresh a second time and confirm the index hash is stable. Confirm only intended files changed.
2. SNBT/schema: parse the edited files with the pack's parser or a supported FTB Quests loader. Check unique IDs, valid task/reward types, required fields, resolvable namespaces, survival obtainability (no backend/creative items), complete item component codec fields, dependency acyclicity, reachable quests, translation keys, and absence of unescaped `& ` formatting sequences.
3. Graph/layout: verify the advertised any-N-of-M minimum by simulation, not hand-counting. Render each edited chapter, detect node overlap and dependency-line crossings, and inspect the central spine, side-lane direction, labels, background contrast, and long text. A source render is review evidence, not an in-client screenshot.
4. Economy: calculate minimum-route and completionist one-time issuance separately for personal and team rewards. Calculate worst-case repeatable issuance, fragmented-team issuance, and the cost of the complete sink board. Test that no reward can reproduce its input, self-fund the board, or dominate normal play. Count choice rewards using verified claim semantics. Verify each material bundle reaches a useful recipe/service threshold, specialized items meet full-set crafting thresholds, currency scales with quest depth, and adjacent quests do not repeat filler rewards.
5. Task verifiability & safety: verify that building quests use palette gathering rather than untrackable multiblock placement, multiblock stations check component acquisition, and conflict/prank tasks respect claim boundaries.
6. Assets: resolve all icons and images against actual client resources, check ZIP entry separators, verify Packwiz hashes, and confirm no stale URL/digest remains.
7. Source synchronization: regenerate or synchronize derived manifests/localization/indexes from the chosen authority, run a check-only/idempotency pass, and prevent a stale generator from clobbering live content.
8. KubeJS boundary: confirm no custom quest logic was added. If existing scripts are involved, test them as-is and document the dependency.
9. Small playtest: load a disposable world/server, open the chapter, claim the opener, complete one task from each task family used, trigger advancement/stat tasks, complete the minimum dependency path, run one repeatable exchange, and inspect the result as both a payer and a teammate. Check logs for parser, missing-ID, reward errors, or item component deserialization warnings.
10. Eligibility evidence: static analysis is acceptable proof that every visible quest is completable by at least one intended player; add a runtime check at the end of the project when reasonable.
11. Failure evidence: record commands, exit codes, screenshots/log excerpts, and the one remaining manual check. Do not report a playtest as successful when only static text inspection happened. State separately whether static parsing, server loading, client visual inspection, and two-account reward testing passed or remain pending.

Also audit prose and completion clarity: no designer-facing claims in player text, no placeholder objectives, short graph titles, one coherent action per quest, hard criteria coverage for substantive progression, explicit consume/inspect/place semantics, and no currently visible quest that its audience cannot complete.

## 7. Ship safely

Update translations, changelog/version metadata, Packwiz indexes, and hosted asset references only when the change requires them. Stage only the quest/art/release files in scope. Fetch the target branch before committing or pushing; if it advanced, inspect and integrate it without discarding unrelated work, then refresh Packwiz metadata again. Commit with a focused message, push the requested branch, and use a draft pull request unless the user explicitly asks for a merge. Preserve existing tags and unrelated user changes.

## 8. VvH project preferences

When working on the VvH campaign in this repository, load and respect
`docs/vvh/HUMAN_QUEST_PREFERENCES.md` alongside this skill, with its
structured companion `docs/vvh/HUMAN_QUEST_PREFERENCES.json`. It records
scoped human design corrections (Market hidden lines and two-wing layout,
short purchase cooldowns, the shared paid-entitlement exception to the
personal default, raw-Stone masonry, stack-safe rewards, stable IDs, and
verified-only modded IDs) with hard requirements enforced by the campaign
validator where static checks are possible. Treat it as a maintained artifact
and extend it when new human edits set precedent; do not universalize these
VvH decisions into generic authoring defaults.

## 9. Hand off clearly

Report:

- the chapter's player-facing loop and intended audience/progression band;
- files changed and any new asset URLs/digests;
- validation and playtest results, including what was not run;
- economy guardrails, currency scaling, and team-scope decisions;
- the branch/commit/PR or release link and the next safe playtest step.
