---
name: roblox-debugging-bugfix
description: Debug and fix Roblox bugs through Studio MCP. Use for repro steps, console errors, script search/read/edit flow, broken UI, failed gameplay systems, data issues, remotes, regressions, root-cause reports, and post-fix verification.
---

# Roblox Debugging Bugfix

## Goal

Move from symptom to verified fix without guessing. For hard or intermittent bugs, follow the discipline below; skip phases only when you can justify it.

## Phase 1 — Build a repro loop first (this is the skill)

Everything else is mechanical once you have a fast, repeatable pass/fail signal for the bug. Spend disproportionate effort here. Be aggressive and creative before you touch a fix.

Ways to construct one, roughly in order:

1. **Studio playtest repro** — the exact steps in Play mode that surface the bug; watch `get_console_output`.
2. **`execute_luau` harness** — call the suspect server/module function directly with a fixture input and assert the result, instead of clicking through the whole game.
3. **Targeted scenario** — spawn the minimal instances/state that trigger the code path (one part, one remote, one player state).
4. **Replay a captured payload** — save the real remote payload / data profile that misbehaves and push it back through the code path in isolation.

Make the loop **fast, sharp, and deterministic**: narrow to the specific symptom, pin any randomness/timing, and cut unrelated setup. A 2-second deterministic check beats a 30-second flaky one.

**Intermittent bugs:** the goal is a higher reproduction rate, not a clean one-shot. Loop the trigger many times, add stress, narrow timing windows. A 50%-flake bug is debuggable; keep raising the rate until it is.

If you genuinely cannot build a loop, stop and say so — list what you tried and ask the user for the environment, a captured artifact (log dump, screen recording with timestamps, the offending data), or permission to add temporary instrumentation. Do not hypothesize without a loop.

## Phase 2 — Reproduce

Run the loop. Confirm it produces the failure the **user** described (not a nearby lookalike), that it repeats, and that you've captured the exact symptom for later verification.

## Phase 3 — Hypothesize

Generate **3–5 ranked, falsifiable hypotheses** before testing any — single-hypothesis debugging anchors on the first guess. Each states a prediction: "If X is the cause, then changing Y makes it disappear." Show the ranked list to the user before probing; they often re-rank instantly ("we just changed #3"). Proceed on your ranking if they're AFK.

## Phase 4 — Instrument

Each probe maps to one hypothesis; change one variable at a time. Prefer inspecting real values (`inspect_instance`, `execute_luau`) over log spam. **Tag every temporary log** with a unique prefix like `[DEBUG-a4f2]` so cleanup is a single `script_grep`. For performance regressions, measure first (timing/`os.clock`, MicroProfiler, instance counts) and bisect — logs are usually the wrong tool.

## Phase 5 — Fix + regression check

Make the smallest safe fix with `multi_edit`. Before declaring done, turn the repro into a durable check where a correct seam exists (an `execute_luau` assertion or a documented playtest step). If no good seam exists, that itself is a finding — note that the architecture is preventing the bug from being locked down.

## Debug Loop (mechanics)

1. Capture the user-visible symptom and expected behavior.
2. Reproduce in Play mode when possible.
3. Read `get_console_output`.
4. Search with `script_grep` and `script_search`.
5. Read relevant scripts with `script_read`.
6. Inspect relevant instances with `search_game_tree` and `inspect_instance`.
7. Make the smallest safe fix with `multi_edit`.
8. Re-run the repro and check console output again.
9. Remove all `[DEBUG-...]` instrumentation (`script_grep` the prefix).

## Common Bug Classes

- Client/server state mismatch.
- Remote payload trust issue.
- UI not updating after server state changes.
- Event connections duplicated or never disconnected.
- DataStore load/save race.
- Object path renamed or missing.
- Play mode DataModel mismatch.
- Race between character spawn, UI creation, and server initialization.

## Fix Rules

- Prefer root-cause fixes over defensive silence.
- Do not swallow errors without logging context.
- Add validation near trust boundaries.
- Keep unrelated refactors out of bug fixes.
- Verify no new console errors.

## Output

Return:

- Repro.
- Root cause (state which hypothesis proved correct).
- Files/scripts changed.
- Verification performed.
- Residual risks.
- Post-mortem: what would have prevented this bug? If the answer is architectural (no good test seam, tangled client/server boundary, hidden coupling), recommend `roblox-code-maintenance-refactor` or `roblox-luau-architecture` — after the fix is in, not before.

## Next

Verify the fix holds with `roblox-playtest-qa` (and `roblox-mobile-playtest` if it touched UI/mobile). If the post-mortem surfaced architectural debt, hand off to `roblox-luau-architecture` or `roblox-code-maintenance-refactor`. Return to `roblox-game-development-lifecycle` to resume the roadmap.

