---
name: prove-it
description: Prove a game change works by seeing it work, with debug calls, compile checks, renders and clips, even when the game has no unit tests. Use before claiming any game change works, or when the user says "prove it works", "show me it works", "did you test it", "verify this change" or "prove-it".
---

# Prove game changes

Many games have no unit test suite. Proof is what you can see: a debug reply, a render, a log line. If the project does have tests, run them too, but they never replace seeing it.

First find the project's proof tools (see `boot-game`): how to compile or check scripts, how to take a screenshot or clip from the command line, any debug server, console or API, and the log file.

1. **Behaviour, seen.** A change is done when it is seen working: a debug reply, a render, a log line. A compile pass is not proof.
2. **Debug API first.** If the game has a local server, console or debug API, hit it (for example with `curl`). Send harmless input first (a bad id), then a real one. Check game state through the game's own read calls, not by opening save files.
3. **Seed through the product.** Make test state the way the game does: start a new game, edit a character, take an action through the game or its debug API. Never hand-edit save files.
4. **Renders for anything visible.** Use the engine's command-line screenshot or capture (see `boot-game`). Look at every image yourself before you call it done.
5. **Probe, don't guess.** When something is wrong, add a temporary print marked with a tag you can grep (for example `DEBUG-PROBE`), measure, fix the cause, then remove every probe.
6. **Throwaway saves for risky tests.** Make a test save or profile, run the risky test there, then go back to the user's save and delete the test one. Never risk the user's own save.
7. **Batch, then test together.** Make all the related changes. Compile or check every touched script with the engine's own checker (Godot: `godot --headless --check-only --script <file>`; Unity: a batch-mode compile; Unreal: build the editor target; web: the type checker and linter). Then do one launch or render that films all of them, and judge it frame by frame. Fix, run again. If the shell has no `timeout` command, bound long runs another way (for example `perl -e 'alarm shift; exec @ARGV' 180 <cmd>`).
8. **A failure is a finding.** Fix the cause. Never hide it with a longer wait or a looser check.
9. **Check motion one character at a time, and let the game check itself.** Before any clip goes to the user: crop close on the action, read frame strips at 4 or more frames per second, and follow single characters to the end (a fallen character stays down, an attack plays out, nobody glides). Add runtime checks for what the game can catch itself (for example a log line tagged `CHECK` when a dead character is asked to move). Grep the run's log for them and fix every one before you show the clip.
10. **The dev run isn't the shipped build.** A check that passed in the editor or a screenshot run does not pass for the exported game. Before a release, check the exported build itself.
11. **Results go on the review page.** What a test shows goes on the page as a new version (a clip for anything that moves), with a note on what changed and a mark on anything still wrong (`show-me` sections 5 and 6). No review page tool? Put the shots and notes in a local HTML or markdown page.
