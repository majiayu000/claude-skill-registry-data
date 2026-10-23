---
name: explainer-video-create
description: Create a narrated 3Blue1Brown-style animated explainer video about how an existing project feature works, using manim with ElevenLabs or local text-to-speech. Use when the user asks for an explainer, walkthrough, or teaching video about code, architecture, or system behavior; not for promotional clips or slide decks.
---

# Explainer Video Creation

Produce one narrated MP4 that teaches how a feature works. Every narrated claim must come from investigated evidence.

## Workflow

### 1. Set the scope

Extract the project, feature, focus, audience, narration language, and output path from the request. Default to engineers who know the domain, English narration, a 3 to 5 minute length, and `~/Desktop/<feature>-explainer.mp4`, or the scratch directory when `~/Desktop` does not exist. Ask only when the feature or project cannot be identified.

### 2. Investigate the feature

Run `system-investigate` on the feature in read-only mode. Record a short fact sheet in the scratch directory:

- each mechanism, state change, rule, and failure path the video will show, with a `file:line` reference;
- one concrete example from repository history, such as a real commit, PR, or log line, when one exists;
- facts that the evidence does not settle.

Narrate only facts from the sheet. Leave out inconclusive facts or present them as open questions.

### 3. Choose the voice

Select the first available provider:

1. `elevenlabs`: `ELEVENLABS_API_KEY` is in the environment, or in a `.env` file that the user named or that exists in the working directory or project root. Validate it with `narrate.py --provider elevenlabs --language <ISO 639-1 code> --check-key`, adding `--env-file <path>` when the key is in a file, before you write narration that depends on it. The check also fails when the script's model does not support the narration language.
2. `say` on macOS, or `espeak` when `espeak-ng` is installed.
3. `silent`, which only sets the timing.

The default voices speak English. For any other narration language, choose a voice for that language and pass it as `--voice`: an ElevenLabs voice ID, a voice from `say -v '?'`, or a voice from `espeak-ng --voices`.

If no key is found, or the key fails validation, ask the user once. Offer three choices: give a key, use the best local voice, or make a silent video. Continue with the local voice only if the user agrees. Never print, log, or copy a key. ElevenLabs receives the narration text, so keep secrets, customer data, and internal hostnames out of the narration.

The default ElevenLabs voice is Jack John (`7EzWGsX10sAS4c9m9cPf`), a voice from the ElevenLabs voice library. If the account cannot use it, pass another voice from `narrate.py --provider elevenlabs --list-voices`, or ask the user to add Jack John from the voice library; do not change the account yourself. When the user names an ElevenLabs voice, find its id with `--list-voices` and pass it as `--voice`. The script uses Eleven v4 at stability 1.0 and style 0. Lower values make the voice over-act explanatory text. Keep the voice's own pace. Pass `--speed` only when the user asks for a faster or slower voice. Eleven v4 ignores the speed voice setting, so the script changes the tempo of each clip after synthesis.

### 4. Prepare tools

Require `ffmpeg` and `ffprobe`. Create an isolated environment in the scratch directory, with Python 3.12 for manim wheel support. Prefer `uv venv --python 3.12` followed by `uv pip install manim`. Ask before you make any system-wide installation. Use `Text` objects so that LaTeX is not needed.

### 5. Write the storyboard and narration

Plan 5 to 8 scenes. Give each scene one idea and split it into beats of 1 to 3 spoken sentences. A beat is the unit of audio-to-picture sync. A typical arc:

1. Problem: show the failure that the feature prevents.
2. Core rule: state the key invariant in one sentence.
3. One scene for each mechanism.
4. Failure and recovery paths.
5. Recap: the invariant again, now earned.

Follow 3Blue1Brown style. Use a dark background and one visual metaphor for each idea. Build the picture step by step and use motion to show change. Give each color one meaning for the whole video. Keep text to short labels. Leave file paths and long hashes on screen only.

Write narration as plain speech in the narration language for text-to-speech:

- Replace terms that the voice says wrong with plain words. Do not use phonetic spellings; the voice reads them inconsistently.
- Use no commas, colons, semicolons, or dashes inside a sentence, because the voice pauses at each one. End each clause with a full stop instead.
- Add no delivery tag by default. When the user wants a different tone, start the first beat of each scene with one tag, such as `[serious]`. ElevenLabs reads each scene in one take, so the tag sets the tone for the whole scene.
- Compare the words per second that `narrate.py` prints for each scene. A long take often reads faster than the rest. Start that scene's first beat with `[speaking slowly and clearly]` and generate it again. Never change the tempo to fix the pace.
- Use `[short pause]` where a break helps, such as before a value read aloud. Do not add emotion tags such as `[concerned]` or `[excited]` to single lines; they make explanatory narration sound acted.

Save the narration as `narration.json` in scene order: `{"S1Problem": ["beat", ...], ...}`.

### 6. Generate the audio

Copy `scripts/scenekit.py` from this skill's directory into the scratch directory. Run `scripts/narrate.py narration.json --provider <provider> --language <code>` there, with `--voice` when step 3 requires it. It writes one clip per beat and `audio/durations.json`. ElevenLabs reads each scene in one take with a `[long pause]` between beats, and the script cuts the take inside those pauses, so the pace stays even across a scene. End every beat with a full stop or a question mark, and do not write `[long pause]` in a beat yourself. An edited beat regenerates only its own scene.

### 7. Write the scenes

Write `scenes.py` with `from manim import *` and `from scenekit import *`. Give each scene class the same name as its `narration.json` key, subclass `Narrated`, and wrap the animations for beat `i` in `with self.beat(i):`. Keep the animations in each beat shorter than the clip, because the beat waits until the clip ends. Call `self.clear_all()` between visual sections. Draw arrows with `arrow()` and animate them with `grow_arrow()`, because manim's `Arrow` and `GrowArrow` scale the tip and the line width with the arrow's length.

When a scene must show the real product interface, record it instead of animating it. Give that scene one beat for each recorded step.

1. Run the product locally with its API stubbed at the boundary, so the recording creates nothing in a shared environment. Use realistic data without customer or colleague details.
2. Script the steps with browser automation. Inject `../bug-report-reproduce/scripts/cursor.js` into every page, move the pointer in small steps before each click, and write the end time of each step in seconds to `step-ends.json`.
3. Open the first page and wait until it renders before the capture starts, because the browser shows a blank white page during navigation. Capture with a `page.screenshot` loop at device scale factor 1.5 on a 1280 by 720 viewport, then join the frames at their timestamps into a 30 fps MP4. Built-in video recording and the CDP screencast capture CSS pixels, so the text is not sharp. CSS `zoom` breaks the position of popovers and tooltips.
4. Run `scripts/screencast.py <scene> <recording> step-ends.json audio media/videos/scenes/1080p30/<scene>.mp4`. It holds each step's last frame until its clip ends, so a new voice does not need a new recording. Never change the audio tempo or cut narration to fit a recording. Make the picture wait for the voice.

### 8. Render a draft and inspect it

Render with `manim -ql --disable_caching scenes.py <scene names>`, and write each recorded scene to the `480p15` directory with `screencast.py`. Then run `scripts/assemble.py sheets narration.json media/videos/scenes/480p15 sheets` and view every sheet. Fix text cut off at the frame edge, overlapping labels, unreadable sizes, and objects that remain from an earlier beat. Render again only the scenes you changed.

### 9. Render the final video

Render with `manim -qh --fps 30 --disable_caching`. Then run `scripts/assemble.py concat narration.json media/videos/scenes/1080p30 <output>`. The script converts every scene to the first scene's format and pads its audio before it joins the scenes, and it fails when the audio and video lengths differ.

## Result

Report the output path, the length, the voice provider, the scenes and the claims each one makes with its `file:line` evidence, the facts left out, and the scratch path of `narration.json` and `scenes.py` for later edits. Do not publish or upload the video unless the user asks.
