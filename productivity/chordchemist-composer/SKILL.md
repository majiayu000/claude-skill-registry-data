---
name: chordchemist-composer
description: Use when ChordChemist songwriting, harmony, melody generation, reharmonization, vocal adaptation, key detection, Melody Canvas edits, deterministic WAV/SVG previews, Copilot workbench validation, or CLI-backed music-theory answers are needed. Do not use for generic frontend work or music advice that does not need ChordChemist's deterministic CLI/app surfaces.
---

# ChordChemist Composer

## Core Rule

Use ChordChemist's CLI as the source of truth for music-theory operations. Do not invent chord spellings, melody analysis, key-distance claims, vocal adaptation rankings, or Melody Canvas fields when `npm run --silent cc -- ...` can answer deterministically.

## Scope

Use this skill for:

- Deterministic theory answers about keys, modes, scale degrees, harmonic function, circle-of-fifths distance, and transposition.
- Chord progression rendering or next-chord suggestions in ChordChemist's model.
- Melody generation, Melody Canvas analysis, scoped melody edits, SVG piano-rolls, and local WAV previews.
- Vocal range adaptation and key detection from pitch-class evidence.
- Copilot Workbench operation at `/_codex/copilot-workbench` for agent-native songwriting UX validation, direct tool calls, tool logs, app-state inspection, and Melody Audition controls.
- Workbench CLI bridge calls with `npm run --silent cc:workbench -- <tool> '<json args>'` when Codex needs to control the app state open in the browser.

Do not use this skill for:

- Generic browser debugging, microphone permissions, or Realtime WebRTC internals unless the user specifically asks to validate Copilot Workbench behavior.
- Editing frontend code unless the code change is specifically to the CLI/music engine this skill invokes.
- Freeform music critique when no deterministic ChordChemist command can ground the answer.

## Workflow

1. Confirm the working directory is the ChordChemist repo, or locate it before running commands.
2. Run `npm run --silent cc -- help` to inspect the available command surface if uncertain.
3. Pass explicit `--tonic`, `--mode`, `--degrees`, `--seed`, and vocal range flags. Avoid hidden state unless the user gave a state file.
4. Treat the CLI JSON response as ground truth. Read `ok`, `result`, `warnings`, and `nextSuggestedCommands`.
5. For melody work, generate first, analyze into Melody Canvas, then request edits by scope. If the user provides an existing state file, start from that instead of regenerating.
6. Use `audio render` for deterministic offline WAV previews when the user needs to hear CLI output. Microphone capture, browser playback debugging, and real device permission work still belong in the app UI/browser.
7. For Copilot UX validation or app-native tool inspection, use the local Workbench workflow below instead of inventing state from memory.
8. For iterative composition, ask for user feedback at musical decision points. When `request_user_input` is callable in the active tools, call it instead of writing a plain-text option list. Use 1-3 short, mutually exclusive choices. If the tool is not callable, ask one concise free-text question and continue only after the user answers or explicitly delegates the choice.

## Copilot Workbench

Use the Workbench when the task is to test or operate ChordChemist as an agent-native songwriting surface.

1. Start the app with `npm run dev` if no dev server is running.
2. Open the printed local URL with `/_codex/copilot-workbench` in the Codex browser.
3. Use the Chat panel for real Text Copilot behavior through `/api/agent`.
4. Use Direct Tool Call for deterministic tool debugging, with JSON args.
5. Inspect `Inspectable State`, `Melody Canvas`, `Audition Controls`, and `Tool Log` before reporting results.
6. Prefer stable `data-testid` targets in the Workbench when using browser automation.
7. Validate UX claims against visible state/tool results. Do not say a Copilot action worked unless the Tool Log or app state confirms it.

## Workbench CLI Bridge

Use the bridge when you need programmatic control of the browser app state from Codex without hand-clicking the UI.

1. Start the app with `npm run dev`.
2. Open the printed local URL with `/_codex/copilot-workbench` in the Codex browser and keep that tab open.
3. Run commands from the repo:

```bash
npm run --silent cc:workbench -- get_app_state
npm run --silent cc:workbench -- set_key '{"tonic":"D","mode":"lydian"}'
npm run --silent cc:workbench -- set_progression '{"degrees":[1,3,6,2,4,3,2,1]}'
npm run --silent cc:workbench -- suggest_melody '{"bars":8,"density":"medium","autoplay":false}'
npm run --silent cc:workbench -- create_melody_sketch '{"authoringMode":"assisted","notes":[{"note":"C4","bar":1,"beat":1},{"note":"C#4","bar":1,"beat":2}]}'
```

The CLI queues the command through `/api/codex-bridge`; the Workbench executes it with `executeToolCall()` in the browser and returns JSON. If the CLI times out, check that the Workbench tab is open on the same dev server URL.

Good Workbench smoke scenarios:

- `compare` should call `compare_melody_versions` and explain differences without autoplay.
- `play before` and `play after` should use `play_melody_audition` one side at a time.
- `delete C3` should create a `delete_melody_notes` audition, not retune the note.
- `extend bars 6-8` should use `identify_melody_gaps` then `extend_melody`.
- `stitch source version` without `versionId` should fail clearly instead of falling back to audition material.
- `create_melody_sketch` should accept chromatic/out-of-scale notes as a pending audition and report analysis overlays instead of rejecting the sketch.

## Decision Points

- If the user asks for a factual music-theory answer, run the smallest CLI command that answers it and cite the resulting chord/key data.
- If the user asks to create music, produce one deterministic first artifact before asking aesthetic questions.
- If the user asks for a variation, reuse the latest state file or user-provided state and change only the requested musical dimension.
- If the user asks to hear something, render a WAV with `audio render`; if they ask to inspect it, render an SVG with `visual piano-roll`.
- If a command suggests `nextSuggestedCommands`, use them as hints, not obligations. Choose the next command only when it advances the user's request.

## Feedback Checkpoints

Ask for feedback after audible artifacts, not abstract plans. Prefer checkpoints like:

- After the first rendered sketch: keep motif A, motif B, or regenerate.
- After a melody edit: accept, revert, or push the same direction further.
- Before expanding to a full song: choose section role such as verse, hook, bridge, or outro.
- When metrics reveal a tradeoff: more space vs. more motion, more resolved vs. more suspended, more singable vs. more instrumental.

Good feedback prompts are short and musically actionable:

```text
Which direction should I develop: the opening leap motif, the lower staccato answer, or a smoother hook?
```

For `request_user_input`, keep the first option as the recommended default and make each option explain the musical consequence, not the implementation detail.

Do not ask for feedback after every command. Ask when the next choice changes musical identity, arrangement structure, or the direction of a multi-minute composition.

## Command Families

Use the CLI directly:

```bash
npm run --silent cc -- theory key --tonic D --mode minor
npm run --silent cc -- progression render --tonic D --mode minor --degrees 1,6,3,7
npm run --silent cc -- melody generate --tonic D --mode minor --degrees 1,6,3,7 --bars 4 --seed 42
npm run --silent cc -- melody analyze --state song.json
npm run --silent cc -- melody edit --state song.json --scope phrase:phrase-2 --operation resolve-tensions
npm run --silent cc -- visual piano-roll --state song.json --out output/piano-roll.svg
npm run --silent cc -- audio render --state song.json --out output/demo.wav
npm run --silent cc -- vocal adapt --state song.json --range-low 57 --range-high 76
npm run --silent cc -- key detect --pitch-classes C:900,E:700,G:850,A:450
```

For the full command contract, read `references/cli-contract.md`.

For Melody Canvas fields and edit scopes, read `references/melody-canvas.md`.

## Output Discipline

- Prefer `--compact` when command output will be pasted into a response or another prompt.
- When saving intermediate state, redirect JSON to a temp file and reuse it with `--state`.
- If a command returns `ok:false`, fix inputs or explain the limitation instead of continuing from a guessed result.
- When the CLI returns `changed:false` for `melody edit`, explain that the selected scope already satisfied the requested transform or did not match editable notes.

## Verification

Before claiming the task is done:

- Confirm every reported chord, key, melody metric, SVG, WAV, or adaptation ranking came from a successful CLI result.
- For generated files, verify the output path exists and the CLI reported `ok:true`.
- For multi-step melody work, keep the state handoff explicit: generated state, analyzed canvas, edited state, rendered artifact.
- For Workbench tasks, confirm the route loads, the relevant `data-testid` surface is visible, and the Tool Log/state reflects the expected behavior.
- For skill maintenance, run the Codex skill validator and at least one wrapper command from outside the repo.

## Wrapper

The bundled `scripts/cc` wrapper can run the repo CLI from any current directory. It resolves `CHORDCHEMIST_REPO`, then walks up from the current directory:

```bash
./scripts/cc theory key --tonic C --mode major --compact
```
