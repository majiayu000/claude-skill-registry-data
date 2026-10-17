---
name: showme
description: Drive a headed browser to a specific state in a web app (a feature, flow, screen, or bug repro) and leave the window open for the user to explore. Use when the user says "show me X", "take me to that screen", "set up the repro", or wants to try an app state firsthand.
allowed-tools: Bash(playwright-cli:*)
---

# showme

Drive a headed browser to the state the user described, then hand them the live window. You do the setup, they do the exploring.

This skill only adds the headed, leave-open, hand-over wrapper. For the actual driving (navigate, snapshot, click, fill, log in), load the `playwright-cli` skill and follow it.

## Steps

1. **Preflight.** Run `${CLAUDE_PLUGIN_ROOT}/skills/playwright-cli/check.sh`. If it fails, relay its message to the user and stop. Do not fall back to another automation tool.

2. **Work out the target.** From context, find the URL (production, staging, or `localhost:PORT`), the preconditions that define the state, and the point of interest. If the app is this repo's and its dev server is not running, start it first. Ask one short question only when the target is genuinely ambiguous.

3. **Open a headed, named session.** Every later command carries the same `-s=showme`.

   ```bash
   playwright-cli -s=showme open --headed <url>
   ```

   If no window appears, a `showme` session is already running headless. Close it with `playwright-cli -s=showme close` and reopen. `playwright-cli list` shows every session and whether it is headed.

4. **Drive to the state** with the snapshot-and-ref loop from `playwright-cli`, stopping just before the point of interest.

5. **Verify before handing over.** When the state is a claim to confirm (a bug, a regression, "X happens when you do Y"), trigger the key action yourself and check the outcome, as long as it is non-destructive. Never hand over a window that "should" show something you have not seen it show.
   - It reproduced: reset to just before the action (reload or undo) so the user can trigger it themselves, then hand over and say you confirmed it.
   - It did not reproduce: stop and tell the user the claim did not hold, with what you did and what happened instead of the expected result. Catching this here saves the user a dead-end click-through.
   - The action is destructive, or the state is open-ended exploration: leave the action to the user and hand over.

6. **Hand over. Do not close.** The session daemon keeps the window alive. Tell the user in a few lines:
   - It is open: session `showme`, on which page.
   - You are here: the current state, what you set up, and whether you confirmed the action works.
   - Try this: the exact action, for example "click the blue Save button".
   - You will see: what should happen, so they know what to look for.

   Mention `playwright-cli -s=showme close` for when they are done.

## Notes

- The open window is the deliverable. Never close it on your own.
- To keep login state across runs, open with `--persistent` (profile managed by playwright-cli) or `--profile=$HOME/.showme-profile` for a directory you choose. The in-memory default forgets everything on close.
