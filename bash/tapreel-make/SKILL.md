---
name: tapreel-make
description: Make a narrated how-to video of a web app with Tapreel. Use when the user wants a video guide, tutorial or walkthrough of an app they own or manage. Covers script, scenes, consent, narration, recording and the finished film.
---

# Make a how-to video with Tapreel

Run the `tapreel` CLI (`node <plugin>/bin/tapreel.mjs`, called `tapreel` below) from the root of the app's repo.
First run the `tapreel-setup` skill so every tool is present.

## Permissions come first (never skip, never self-approve)
Tapreel drives the real app in a browser. Before any recording:
1. Ask the user which URL, which **demo account** (never a real person's), whether the walkthrough changes data, and whether the window should be hidden.
2. Put those answers in `tapreel/tapreel.config.json` under `access` (`baseUrl`, `allowedOrigins` incl. any API origin the app calls, `accountIsDemo: true`, `dataChanges`).
3. The account's name and password come from environment variables only (`TAPREEL_USER`, `TAPREEL_PASS`). Never write them to a file, the chat or the repo.
4. The owner runs `tapreel consent` and approves. **You must not run `tapreel consent --yes` for them.** Consent is tied to the settings: changing the target or data policy needs it again.
5. If `dataChanges` is `restored-by-hooks`, write `tapreel/hooks.mjs` (`before` snapshots, `after` restores) and show it to the user.
The recorder blocks every site not in `allowedOrigins`. Entries are sites, not pages (`https://app.example.com`, or `https://*.example.com` for subdomains too). After a recording, tell the user which blocked hosts it reported and ask before adding any.

## Steps
1. `tapreel init`, then edit the config (name, colours, URL, chips, voice). `tapreel doctor` must pass.
2. Write `tapreel/script.json`: scenes with short spoken lines (one sentence each, 6 to 14 words, friendly, no jargon). Use the `say` field for how a word should sound ("S M F D"). Aim for 5 to 8 scenes, 4 to 8 minutes. `hold` adds a pause for on-screen action.
3. `tapreel plan` (a first timeline from estimates), `tapreel narrate`, `tapreel plan --freeze` (locks each sentence's length so later edits never move recorded footage), then `tapreel plan` again.
4. Write one `tapreel/scenes/<scene id>.mjs` per scene (see `templates/scene.mjs`). Time every action to the narration with `S.at(S.cue('line start') + offset)`. Wrap steps in `ui.safe` so one missing element does not stop the scene.
5. `tapreel record` (or `--scenes 2,3`), read the "late" notes, fix timing, re-record only those scenes.
6. `tapreel narrate --mix-only`, `tapreel build`, then `tapreel check`.
7. Follow the `tapreel-qa` rules. Tell the user which timestamps to listen to; you cannot hear the audio.

## Limits (v0.1)
Web apps and PWAs in Chromium with a phone-shaped layout. Not yet: desktop-window layout, Electron, native Windows apps. Say so rather than faking it.
