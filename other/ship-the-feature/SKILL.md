---
name: ship-the-feature
description: Take game work all the way to done in one session, from what is left to built, seen working, pushed and shown with screenshots. Use in a game project, in any engine, when the user says "finish the game work", "finish this game feature" or "ship-the-feature". For apps that are not games, use ship-it.
---

# Finish game features

You do the work, in this session, start to finish. Only slow side jobs (fetching or buying assets, long downloads) go to a separate session or person (see `game-director`).

Load these first: `game-calls`, `fix-it-for-real`, `art-director`, `prove-it`, `boot-game`, `devlog`.

1. **State.** Read `git log`, the project's design doc and roadmap (look for DESIGN.md, GAME_DESIGN.md, a roadmap, a TODO or the issue tracker), any asset or status reports in the repo, and everything the user asked for this session. List what is left. Never redo done work.
2. **Order the work.** One list, top to bottom: what blocks other work first, then what the user can see. Keep the user's exact words and the look bar (`art-director` rule 1) in front of you.
3. **Build and prove each item.** A compile or script check, a call to the game's debug hooks or a render (`prove-it`). Look at every render against `art-director`. Fix a gap before you move on.
4. **Commit and push** each item once it is proven (`devlog`).
5. **Review page.** Every finished item goes on the review page as a new version with a note from the agent. Anything still wrong gets a mark on the shot (`show-me`). Before a release, run one `fix-it-everywhere` turn (`devlog` rule 3). No review page tool? Write a local HTML or markdown page with the shots and notes.
6. **Report.** A short status with screenshots: done, in progress, left (with rough times), and what needs the user's hands (a store or asset-site login, a licence to accept, a model or service to start, a permission to grant).
