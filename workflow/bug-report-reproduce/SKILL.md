---
name: bug-report-reproduce
description: Reproduce a user, customer, or support-reported problem with synthetic data, prove the cause with a temporary test, record a narrated click-through walkthrough of the symptom, and report what was and was not proven. Use when the user links a bug report, support thread, or ticket and asks to reproduce it, find the cause, or show a recording or walkthrough video; not for read-only questions without a report, which belong to system-investigate, or for planned feature work.
---

# Bug Report Reproduction

Turn one reported problem into a reproduction, a proven cause, and visual evidence that a teammate can review. Leave the repository as it was unless the user asks for a fix.

## Workflow

### 1. Read the report

Read the report and its attachments through the available connector. If you cannot read the report, ask the user to paste it. Record:

- the symptom in the reporter's words and in observable terms;
- exact messages, errors, outputs, and screenshots;
- the affected area, environment, input shape, and plan already agreed in the report.

Do not write to the report's source. Draft any reply for the user to send.

Record `git status --short` before you change anything. Cleanup in step 8 restores this state.

### 2. Trace the symptom to the code

Start from the most specific observable detail in the report and follow the code that produces it, across process and service boundaries, to the decision that causes it. Record each step with `file:line`.

State the working hypothesis and the strongest alternative. Keep the observed symptom separate from its cause; the place where a problem shows is often not where it starts.

### 3. Build synthetic input

Never copy customer data, files, or identifiers into the repository, tests, recordings, or reports. Create a synthetic input with the same structure, format, and size class as the reported one, and keep it in the scratch directory.

### 4. Choose the environment

Ask which environment to use only when the report and repository do not settle it. Respect organization policy and tool blocks: when tools or access are blocked for an environment, do not work around the block. Fall back to the closest local harness and record the gap as a limit.

### 5. Prove the behavior with a focused test

Before any recording, write one temporary test at the narrowest unit that owns the behavior. Control inputs, timing, and external replies at the system boundary. Assert the observed sequence of states, including repeated paths. A passing test that shows the reported sequence proves the symptom; the recording only shows it.

To prove the cause, change only the suspected cause, for example one input condition or a temporary one-line patch, and show that the symptom goes away. Revert the change. If the symptom stays, the hypothesis is wrong: test the alternative from step 2.

### 6. Reproduce the symptom

Reproduce in the repository's existing isolated harness or fixtures, with external replies stubbed at the boundary. Run the real feature, not a copy. Exaggerate the trigger only enough to make it visible. Use `ui-control` for graphical surfaces and `cli-control` for terminal surfaces.

### 7. Record a narrated walkthrough

Produce one MP4 that clicks through the reproduction while a voice explains each step. Require `ffmpeg` and `ffprobe`. Keep working files in the scratch directory, and write the final video to `~/Desktop/<symptom>-walkthrough.mp4` unless the user names a path. When `~/Desktop` does not exist, use the scratch directory.

When the symptom has no browser surface, or the repository has no browser automation that can record video, skip the recording. Say so, and give the test output and a terminal transcript as the evidence.

1. **Choose the voice.** Use `../explainer-video-create/scripts/narrate.py` from this skill's directory. Narrate in the user's language; `<code>` below is its ISO 639-1 code, such as `en`. Select the first available provider: `elevenlabs` when `narrate.py --provider elevenlabs --check-key --language <code>` passes, adding `--env-file <path>` when the key is in a `.env` file instead of the environment; then `say` on macOS or `espeak` with `espeak-ng`; then `silent`. If no key works, ask the user once whether to give a key, use the local voice, or make a silent video. Never print or copy a key.
2. **Write the beats.** Save `narration.json` as `{"Walkthrough": ["beat", ...]}`. Give each beat one user action or one visible state change, in 1 or 2 spoken sentences. A typical order: what the reporter sees, the action that triggers the problem, the symptom while it lasts, the resolution, and the cause from step 2 in plain words. Narrate only facts from the trace and the test. Keep file paths, hostnames, customer data, and identifiers that are hard to say out of the narration, because a text-to-speech service may receive it.
3. **Generate the audio first.** Run `narrate.py narration.json --provider <provider>` in the scratch directory. For `elevenlabs`, add `--language <code>` and any `--env-file` from step 1. It writes one clip per beat and `audio/durations.json`, which sets how long the recording holds each beat.
4. **Script the recording.** Write a temporary script with the repository's own browser automation that can record video. Open the reproduction so that the video shows only the affected feature. In the script:
   - record at the viewport size, so the video is not scaled;
   - inject `scripts/cursor.js` from this skill into every page, because headless recordings show no pointer;
   - take the start time when video recording starts;
   - for each beat, log its start in seconds, perform the action, wait for the beat's observable state, take a screenshot, then wait until the beat's clip ends plus a short pause;
   - move the pointer in small steps before each click, so the viewer can follow it;
   - hold the final state for about 1.5 seconds, write the beat starts to `beat-starts.json`, and close the browser context to save the video.
5. **Join audio and video.** Run `scripts/walkthrough.py mux <recording> audio beat-starts.json <output.mp4>`. It places each clip at its beat start and trims the video to the narrated span. It fails when beats overlap, the recording ends before the narration, or the audio and video lengths differ. Fix the script timing and record again when it fails.
6. **Inspect the result.** Run `scripts/walkthrough.py sheet <output.mp4> sheet.png` and view the sheet and the beat screenshots. Confirm that each beat's state appears in order, and that the video shows the pointer, no blank frames, no harness loading screens, no cut-off panels, and no customer data. Edit only the beats or timing that fail, and record again.

### 8. Clean up

Copy the recording script to the scratch directory, then delete the temporary test, harness entries, recording script, fixtures, and synthetic files from the repository. Stop servers and browsers that this workflow started. Confirm `git status` matches its state before the session.

### 9. Fix only on request

When the user asks for a fix, work in a separate git worktree. Use `behavior-implement` with a regression test that fails on the default branch and passes with the fix, and run the repository's lint, type, and affected test suites. Use `pr-draft` to open a pull request only when the user also authorizes the commit, push, and pull request.

## Result

Report:

- the reproduction result and the evidence paths: walkthrough video, contact sheet, beat screenshots, and test output, plus the scratch paths of `narration.json` and the recording script for later edits;
- the cause with `file:line` references, and how it produces the reported symptom;
- what the reproduction proves and what it does not, such as synthetic data instead of the real environment, or paths shown in the test but not in the video;
- the evidence that would settle each open question;
- a draft reply to the report, not posted.

Do not upload or share evidence unless the user asks.
