---
name: fix-it-for-real
description: Fix bugs at the system level instead of patching symptoms, by reproducing each bug with a failing probe, finding who already solved the general problem, and committing small checked changes safely even when several agents share one checkout. Use when fixing a bug, especially one that came back, or when the user says "no hack fixes", "fix it properly", "this keeps breaking", "fix the root cause" or "fix-it-for-real".
---

# Fix the real problem

This works for any codebase. The examples come from games, where symptoms are easy to see and easy to patch badly, but the method is the same for apps, services and tools.

Before you start, find the project's own rules: the agent instructions file (CLAUDE.md, AGENTS.md, .cursorrules or similar), the contributing guide, the architecture doc, the linter and formatter config, and any rules-check script. Where this skill names a file such as "the architecture doc", use the project's equivalent.

## If the user says "no test runs"

Sometimes the user wants the code finished with no time spent on side runs. When they say so, until they say otherwise:
- Write code in the main tree and commit it. Find causes by reading the code and the logs, frames and reports that already exist.
- Run nothing beyond compile and static checks: no probes, no autoplay, no test harness, no private copy of the services, no headless game.
- The allowed checks only read files: the compiler or type checker on what you touched (for example `node --check`, `tsc --noEmit`, `godot --headless --check-only`, a C# or C++ build) and the project's rules-check script. A file that doesn't load is never left in the tree.
- A probe the fix needs may be written but not run by you. Commit small and often, and name the probe in the commit so someone can run it later.
- Testing is grouped and run by whoever owns it (see `build-while-you-sleep`).

## Change the real tree, never a copy

Make every edit in the project's own files, the ones that run. No working copy in a scratch folder to edit and copy back, and no "after" tree built beside it. A scratch copy is allowed only to run a probe's before-run against the untouched code at HEAD (read only, deleted after). Keep the tree working while you edit: make each edit whole, run its load or compile check at once, and land it. A file that doesn't load is never left in the tree.

## No hack fixes: reproduce it, then fix the system

A bug seen on screen (a cart driving through a well, a horse spinning on the spot, a button that does nothing once) is a symptom. Before any code:
1. **Reproduce it with a probe first.** Prefer a headless one that needs no GPU: a small script or test that sets the situation up and asserts the rule (nobody spins on the spot, no path crosses a building, everyone arrives). It must fail now.
2. **Name the general problem and the block that solves it** (see the gate below). When a shared system changes, write 3 to 5 lines of design in the commit or the docs before code: which block, and what hand-written code it replaces.
3. **Fix the system, not the instance.** The probe passes. It stays as a guard and runs on every later change.

No fix lands without its probe. If you patch the same area twice, the first fix was a hack: stop and redesign.

## Before any change: who already solved this?

Every change, even a one-line fix, passes this gate first. A fix that places, times or decides something by hand is a sign you are rebuilding a solved problem.

1. **Name the problem in general terms**: "a horse pulling a cart along a road", "characters choosing what to do next", "UI that fits any window size", "show the player where an event is", "retry a failed network call". Not "the horse is 0.16 off".
2. **Find how it is solved, and look wide.** You are rarely the first.
   - **Your engine or framework and its ecosystem:** its own built-in nodes, components and services, its asset or package store, and what users of other engines reach for (Godot, Unity, Unreal, Bevy, web frameworks), including free content and open-source ports of a technique.
   - **Open-source games and apps in your genre:** for strategy and sims, for example 0 A.D., OpenRA, Widelands, Freeciv, Mindustry, OpenTTD, OpenRCT2, Battle for Wesnoth. Read how their code solves it.
   - **Game AI and design craft:** GDC talks and postmortems, *Game AI Pro* (free online), utility AI, GOAP, behaviour trees, Celia Hodent's work on game UX, the Game Accessibility Guidelines.
   - **Asset commons:** Mixamo, Quaternius, KayKit, Kenney, Poly Haven, ambientCG, OpenGameArt, Freesound.
   - **Outside your field:** film and animation craft (Disney's twelve principles, cinematography), theme-park and crowd design, theatre staging, board-game design, platform interface guidelines (Apple, Material), and research papers.
   - **Shipped products' answers:** the well-known games or apps in your genre, and what their players, modders and users say worked.
3. **Use that.** Your code only configures and connects it.
4. **None exists?** Say so in the commit and in the project's review or decision log, and keep the hand-written part small. For anything big, the user decides first.
5. **Patching a hand-built part again?** Stop and replace it with the proven block.

## Architecture: SSOT, SRP, DRY, SOLID

Every change follows these. A plan that breaks one isn't approved.

- **SSOT: one owner per fact.**
  - Map each kind of state to exactly one owner (for example: the simulation owns units and terrain, the server owns accounts and saves, the view keeps one read-only mirror).
  - The view or client keeps one mirror, filled from one source. No other script parses that source or caches its own copy; they read the mirror.
  - Every plan names the owner of each new piece of state, and says nothing else holds a copy. Keep the owner list in the docs.
- **SRP: one decider per behaviour.**
  - Each agent's or feature's "what next" runs in one place (a behaviour tree, a state machine, a reducer). Movement code only moves; rendering code only draws.
  - A file or function doing two jobs gets split by job, not grown.
- **DRY: one place per rule.** A threshold, colour, time span, mood rule, animation pool or event shape is defined once and imported. Two copies of a rule is a bug waiting to drift.
- **SOLID.**
  - New behaviour arrives as a new tree, task, handler or data row, not as another branch in a growing switch on type strings.
  - Depend on interfaces, signals and events, not on another module's internals or on raw data shapes from a server.
- **Consolidating is expected; no fallbacks.** Rewrites toward these principles are welcome. The new code replaces the old in the same change: no switch back to the old path, no two systems doing one job. Carry every behaviour over (nothing lost) and delete the old code. These rewrites are exempt from "additive" below.
- **One interface per behaviour.** For example, everything that moves goes through one mover that asks the navigation system for the route; nothing else tweens or sets a position to travel. Scenes, moods and reactions are data rows, never new hand-written functions.
- **Check the rules.** If the project has a rules-check script or lint rules for these principles, run it before committing. A breach is fixed, not added to the known-breach list (that list only shrinks). If there is none, suggest one.
- **Proof includes behaviour.** Compiling isn't working. Every change to AI, characters or other behaviour passes a behaviour probe (for example: distinct activities, no repeats, no over-long holds, pools not empty) before it is committed. See `prove-it` for games and `bug-trap` for apps.

## Working rules

1. **Write like the code around it.** Same naming, comments, density and idiom. Doc comments say what a thing is in the product's own words. Don't add dependencies where the code avoids them.
2. **Additive.** No unrelated refactors. Ask the user before a new abstraction. Before launch, a change to a save or data format needs no migration or compatibility shim unless the user says so; after launch, it does.
3. **Glue, not engines.** Your code connects proven parts. A new system needs a reason no existing block covers it.
4. **Check every edit.** Run the compiler, type checker or engine script check on each file you touch. In typed scripting languages, give explicit types to values from untyped sources, or the check may fail.
5. **Reload what you changed.** Restart the service you changed and re-import changed assets, using the project's own commands.
6. **Never freeze the frame.** Big builds or loads (a town, a level, a long list) go through a per-frame budget, a coroutine or a background worker. Never a multi-second loop on the main thread.
7. **Small commits.** One change each, by subsystem, staged by name. Never skip hooks (`--no-verify`).
8. **Third-party assets stay out of git** unless their licence allows it. Track only import settings and licence files. Own art, code and docs go in. Follow `.gitignore`.
9. **Never wait.** Builds, renders, imports and long calls run in the background; carry on and resume when they finish.
10. **Cached builds get a version.** If the project caches generated content (baked levels, merged models, generated terrain), keep a version number for it and bump it in the same commit as any change to how that content is built or looks. Otherwise players keep the old one. Don't bake things into the cache that must stay live (for example particle systems).
11. **Local AI models, if the project uses one:** keep prompts short, use real conversation turns and plain-text replies, and ask for JSON only for simple choices.

## Sessions that share one checkout and one git index

If several agent sessions commit to the same branch from the same folder, the shared git index is a trap. Never `git add` and leave files staged: another session's commit will take them. Commit only your own changes, in one step.

A path commit takes the whole file. If `git diff <file>` shows lines that aren't yours (another session is editing it too), commit your hunks from a private index, so nobody else's staged or unstaged work rides along:

```
git diff HEAD -- <file> > "$TMPDIR/mine.patch"   # trim it to your hunks
export GIT_INDEX_FILE=$(mktemp -u); git read-tree HEAD
git apply --cached "$TMPDIR/mine.patch" && git commit -m "..."; unset GIT_INDEX_FILE
git reset -q -- <your paths>   # refresh the shared index to the new HEAD for those paths only
```

- Build the private index from HEAD **at commit time**: run `read-tree HEAD` right before `apply`, in the same command, never earlier. An index read before another session's commit landed will put the old code back in their files.
- Make your patch with `git diff HEAD -- <file>` at that moment.
- The last line matters. Without it the shared index still holds the old file, so every other session sees a staged revert of your change and its next commit undoes it. It touches the index only, never the files.
- Before pushing, read `git show --stat HEAD`. Every file listed must be one you meant to change, with your line counts.
- If the file is yours alone: `git commit --only -m "..." -- <paths>` (new files: `git add <paths> && git commit --only -m "..." -- <paths>` in the same command). Never a bare `git commit` in a shared folder.
- Then `git push`. If it is rejected because another session just pushed: `git pull --rebase -q && git push`.
- Check the compile output is clean before committing, never after.

If only one session works in the folder, normal small commits are fine. Using one git worktree per session avoids the problem altogether.

## Production grade

The bar is a shippable product. Nothing debug reaches the player or the log: no animation lists, test pickers, key-help strips, internal names, stray print traces or frame probes in committed code. Keep test aids behind an explicit flag (for example `--probe`) that is off in normal play. The player sees the world and the choices that matter; the product makes the rest of the calls. Read the log of every run you do, and fix any recurring error or warning instead of ignoring it.
