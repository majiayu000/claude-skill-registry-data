---
name: uefn-quests
description: Builds custom quests with the Verse Progression API (quest, objective, rewards, collection, participant) that UEFN 43.00 lets you publish. Use when the owner asks for a quest, mission, objective chain, collect-N task, tracked goal, or a reward for finishing something.
kind: discipline
last_reviewed: 2026-11-03
sources: [Verse digests of UEFN 43.00 read in the editor, a minimal quest compiled in the lab]
---

# Custom quests in UEFN 43.00

The Progression API left experimental in 43.00: a custom quest can be published. There is no editor tool for it; a quest is Verse. The facts below were read from the project's own digests and a minimal quest was **compiled** in the lab (compile only: it has not been run in a session, and publishing one has not been tried).

## When to use
- "Collect 10 coins", "talk to three NPCs", "finish the course": a goal with progress and an end.
- A reward or a notification when something is completed, tracked per player.

**When not to use:** a plain score or timer (use a device and a variable), an ordered chain of steps without tracking (use the `ordered objectives` recipe), saving progress between sessions (use `verse-patterns`, persistable data).

## The pieces (all in the digests)
- `objective`: has a state (Inactive, Active, Complete) and a progress text. `progress_objective` counts up to `RequiredProgress`.
- `quest`: an objective that players join and abandon; has join, abandon and complete events. `basic_quest` is "do X, get Y": it completes by itself when its objective completes and grants its rewards once.
- `quest_collection`: groups quests (use `fort_quest_collection`). `quest_category` sorts them for the player.
- `quest_participant`: who plays. For a player use `agent_quest_participant{Agent := Player}`; `quest_participant_info` tells whether they contribute, observe or receive.
- `quest_reward`: what the quest grants (`entitlement_quest_reward` for an entitlement). Leave the rewards empty for a quest without one.
- Devices that show progress to the player: `objective_device`, `timed_objective_device`, `tracker_device`, `progress_based_mesh_device`.

## Workflow
1. Say the quest in one line: who, what, how many, what reward. Ask only what is missing.
2. Subclass `basic_quest`, make a `progress_objective` with `RequiredProgress`, put the quest in a collection, join the player, activate, advance with `SetProgress`. Start from `references/quest-minimal.verse.txt`.
3. Bind every result: `Join` and `Activate` return a result, and `_ :=` does not compile.
4. Subscribe to the quest's complete event for the reward moment and the feedback (see `game-feel-uefn`).
5. Build, then playtest one player: progress text and the complete event must both print.

## Rules (symptom, cause, remedy)
- Error 3600 on `progress_objective{}`: `RequiredProgress` must be set in the archetype; a later `SetRequiredProgress` is too late.
- Error 3512 on a `case` over `objective_state`: the enum is open; add a default clause.
- Errors 3514/3532 on `_ := ...`: give the result a name.
- Quest never completes: the objective was not activated, or progress was set on another objective than the quest's.
- Several players: one participant per player; progress is per participant, not shared, unless the design says so.
- Experimental: nothing in these classes is marked experimental in the Verse digest, and the compiler printed no warning. The UnrealEngine digest was not scanned for it: read it before promising a publish.

Class list with signatures: `references/quest-minimal.verse.txt` compiles against them; the full digest lines are in the editor's `Verse.digest.verse` and `UnrealEngine.digest.verse`.
