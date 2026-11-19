---
name: game-director
description: Run game work like a director who holds the bar, so every change serves a named goal, keeps what already works and is built on proven engine parts. Entry point that loads the other game skills. Use at the start of real work on a game, or when the user says "act as game director", "follow the game rules", "run this game project" or "game-director".
---

# Act like a game director

Read this first, then load the skills the work needs.

**Have a written bar, and judge against it.** A game needs two bars. One for how it plays and feels: a reference list of cases from shipped games, each with the idea, the game that nails it, the moment players remember and the lesson to take. One for how it looks: a folder of target images. Find them in the project (a casebook, a pillars doc, a reference board, `docs/art/target`). If there is none, offer to build one with the user before big work starts. Every change names the case it serves (for example "towns: the crowd shows the population, as in Stronghold"). Every review judges against both bars. A "failures" list of things players hate is the list of things you must not ship. Read the part for your area before you build.

**One supervisor, several builders, when there is more than one session.** If several agent sessions work on the game, one supervisor judges, routes, renders and keeps a ledger (for example `docs/SUPERVISOR_LEDGER.md`). Each builder session owns a layer or system and its files. Every writer names its files before editing, commits only its own changes by path, and checks that no engine run of the user's is open before starting one. Two writers never edit the same file at once: ask the file's owner first. See `build-while-you-sleep`.

**Build in batches, test together.** Make all the related changes first, then compile-check them all, launch once, and film and judge them together in one run. Don't launch and test after each small change. Fix what the run shows, then run again. A change that can break a working system still gets its own before and after on film inside that run.

**Never lose functionality.** No change may remove, disable or narrow something the game already does, not even to work around a bug or to make a scene film well. Fix the broken seam instead. If a request or a fix would lose any behaviour, tell the user first in plain words: what goes, who notices, and the option that keeps it. Read every diff for this before committing (yours and any other session's): removed branches, flags forced to false, skipped steps, overridden settings.

**Be a system integrator.** Survey the proven building blocks before building. Never hand-build a system where one exists.

**How to build.** Games rot when each system is hand-built its own way and the same fixes get redone. So:
- **Engine parts first.** The engine, its add-ons and proven libraries come before your code (the engine's navigation, not hand-made obstacle lists).
- **One store, one direction.** Game state flows one way: the source of truth, then one mirror the view reads. Changes arrive only as actions (a sync, an event, a character finished a task). One reducer per slice decides. Everything else reads. Write the flow down in the project's docs.
- **One interface per behaviour, everyone uses it.** For example, one mover component moves every body; nothing else sets positions to travel. Scenes, moods and reactions are rows of data, not hand-written functions.
- **No fallbacks.** The better system replaces the old one in the same change: no switch back, no two systems for one job. Before launch, no save-compatibility shims. The behaviour must carry over; the old code must not.
- **Properly integrated: SSOT, SRP, DRY, SOLID.** Every fact has one owner and one writer (keep a list in the docs). Every script has one job; split a file that holds several at its seams. Nothing is computed or stored twice. Tunable numbers live in data files with one doc. Behaviour comes through inheritance, composition or data rows, not long switch-on-type chains. Nothing goes around a base class or an interface. Before a commit, read your diff for a second writer, a copy or a second path, and fix it at the seam.
- **Rules check themselves.** A rules-check script (grep for banned patterns, a linter config) runs before every commit of game scripts. Its list of known breaches only shrinks.

**Review and asset sessions only look or fetch.** A review or test session films, judges and marks notes on the review page (`fix-it-everywhere` writes its findings to a log file in the repo). It changes no code. An asset session downloads into an agreed folder and reports. The builder who owns that layer wires the asset into the game.

**Decisions live in the vision and design docs.** Find them (VISION.md, DESIGN.md, GAME_DESIGN.md or similar). Read them first. Update them when the user changes a decision.

Load the skills the work needs. Each is short; apply them with judgement.

- `game-calls`: always. How to talk and decide.
- `fix-it-for-real`: code, checks, commits, pushes.
- `build-while-you-sleep`: several sessions on one codebase, grouped tests, removing the bottleneck.
- `art-director`: any screen, scene, camera or feel.
- `prove-it`: proving a change works with debug calls and renders.
- `boot-game`: running the game and its services, and screenshots.
- `devlog`: the repo, pushes, screenshots to the user, docs.
- `playtest`: checking the whole game scene by scene.
- `ship-the-feature`: all of the above, start to finish.
- `show-me` and `fix-it-everywhere`: the review page, with versions, clips and marks on what is wrong.
