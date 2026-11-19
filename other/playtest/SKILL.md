---
name: playtest
description: Check the whole game scene by scene with renders and debug calls, and get a pass or fail report with a picture for each check plus a fun score. Use when the user says "playtest", "check everything", "verify the game", "test every scene" or "playtest".
---

# Playtest every scene

Load `boot-game`, `prove-it` and `art-director`. Then, in this session:

1. **Checklist.** Write one list: do this, then you should see this. Cover every screen and scene the game has. Find them from the scene or level folder, the main menu flow and the design doc. A typical list: title and new-game screens, the main map or level, a close view of busy areas (are people or units spread out, do their actions fit the place), character screens and editing, every menu and dialogue, taking direct control (move, talk, doors), each combat or challenge type, each interior or sub-level, each special event, the end of a run and what follows it.
2. **One render at a time**, on the native build of the engine for this machine, each timed to the event it shows. Look at every image yourself.
3. **Debug checks** for what renders can't show: dialogue replies, rule outcomes, save and log entries, a death or game over and what happens next. Use the game's debug API, console, test hooks or log (see `boot-game`).
4. **Report each check:** pass with its screenshot, fail with what you saw, or not run and why. Each check's shot or clip goes on the review page as a version. Each fail gets a mark on the shot (`show-me` section 6). No review page tool? Write a local HTML or markdown report with the images.
5. **Score the fun bar.** If the design doc has a fun bar or playtest metrics, play one real session (about 15 minutes) and run every test in it. If it has none, propose a few with the user, such as decisions per minute, share of time with nothing to do, repeated events or names, and time from the player's input to a visible change. Count from the game's own log. Report each score next to the last run's.
6. **A failure is a bug.** Fix "now" items (broken, frozen, unreadable) here and check again. Log the rest on the project's roadmap or issue tracker.
