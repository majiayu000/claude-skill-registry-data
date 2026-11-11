---
name: smoke-test-game
description: Run Vỉa Hè Online end to end and prove it works, from server tests to the Unity client reaching the login screen with a clean console. Use this skill before saying a client or server change works, after a large merge, and when the user says "chạy thử game", "test game", "game có chạy không", "vào game xem", "kiểm tra Unity". Compiling is not proof, and a Play Mode screenshot can show a frozen frame, so follow the order below.
---

# Smoke test the game

Stop at the first failed step and report it with the output. Do not retry in a loop.

## 1. Server and protocol

From the repository root:

```bash
node .agents/skills/verify-protocol/scripts/check-protocol.mjs
```

Then, in `server/`:

```bash
npm test
npm run test:garden
npm run test:world
```

## 2. Start the server

Check whether port 2567 already answers. If not, start `npm start` in `server/` in the background.
Confirm `http://localhost:2567/` replies. Stop the server afterwards only if you started it.

## 3. Unity prerequisites

This needs the Unity CLI (`unity --version`) and the `com.unity.pipeline` package in `client/`
(`unity pipeline install --project-path client`). If either is missing, tell the user. Installing
the CLI changes their machine, so it needs their approval.

## 4. Play Mode

Commands come from the Pipeline package and can change between versions. If one fails, list the
current ones with `unity command`. Run them from the repository root, and add
`--project-path client` before any `--` on each `unity command` line. On Windows the CLI may not be
on PATH in an agent shell; it is at `%LOCALAPPDATA%\Unity\bin\unity.exe`.

After `unity pipeline install`, an open Editor loads the package only when its window has focus, so
ask the user to click it if `unity status` reports `STATUS_PIPELINE_LOAD_PENDING`.

```bash
unity status --format json
unity command editor status
```

If the Editor is already playing or paused, that session belongs to the user. Read it, change
nothing, and tell them. Also ask before entering Play Mode if the open scene has unsaved work.

```bash
unity command editor set_auto_tick
unity command editor.playmode set_run_in_background
unity command editor.playmode start
```

Entering Play Mode reloads the domain, so the next command can fail with "No Pipeline instance
found". Wait a few seconds and run it once more.

```bash
unity command job wait -- --condition '{"member":"UnityEngine.Time.frameCount","op":"changed"}' --timeout 10
unity command capture game_view -- --source screen --output-path Screenshots/smoke-test.png
unity command console get -- --tail 50 --level error
```

## 5. What passes

- Frames are advancing: the `job wait` step succeeded.
- The screenshot shows the login screen. `Game.Boot` builds the scene and UI in code, so no scene
  file needs to be open.
- The console has no errors. The Input Manager deprecation warning is known and harmless. Missing sprites appear as `Missing sprite ...`; use `export-sprites`.

## 6. Clean up

```bash
unity command editor.playmode stop
unity command editor.playmode set_run_in_background -- --enabled false
```

Turn auto tick off with `unity command editor set_auto_tick -- --enable false` only if it was off
before you started.

`client/Screenshots/` is ignored by git. Report what you saw, and say which steps did not run.

## 7. First sale flow

Use this after step 5 to test login through the first banana sale. It takes about 5 minutes because
the first crop really ripens in 3. Run it on a throwaway server so `server/data/game.db` stays clean:

```bash
cd server && PORT=2568 DATA_DIR=<temp folder> npx tsx src/index.ts
```

Enter Play Mode and call `unity command editor.playmode set_run_in_background` again, because the
setting does not survive a stop. Then run each script in `scripts/` with
`unity command script eval --project-path client -- --file <absolute path>` (a relative path resolves against `client/`, and a wrong path prints no `result:` line):

1. `login.cs`: backs up the `deviceId`, `name` and `serverAddress` PlayerPrefs, then logs in a new test device on port 2568.
2. `create.cs`, `plant.cs`, `water.cs`: tutorial reaches 2. `lot.cs` prints the seconds left.
3. `harvest.cs` once ripe, then `sell.cs`: tutorial reaches 4.
4. `invite.cs` every 5 seconds until a customer wants banana and `money` rises: tutorial reaches 5.
5. `state.cs`: the HUD must show the new money and the leader's next line.
6. Stop Play Mode, stop the test server, then run `restore.cs`. Never skip this: until then the Editor plays as the test device.

The scripts call `Game` methods and button handlers directly, so they do not prove that taps hit
the right place on screen.

A capture can be old. If `editor status` shows `playerLoopTicking: false` or `runInBackground: false`,
trust `state.cs` over the picture.

## Not covered yet

Real taps, the second crop, buildings, the bus trip and anything after tutorial step 5.
