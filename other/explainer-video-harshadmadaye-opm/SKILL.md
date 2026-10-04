---
name: explainer-video
description: Turns a spec or document into a narrated explainer video. Produces a 1920x1080 MP4 of illustrated still slides with a neural voice-over and a sidecar .srt; it is a narrated slideshow with fades, not animation. Slides come from a script-rendered layout kit so the run is cheap and repeatable on macOS, Linux and Windows. Use when the developer runs /opm:explainer-video <path>, asks for an explainer or walkthrough video of a spec, brew-idea result, milestone summary or other document, or wants to rebuild such a video after an edit.
argument-hint: <path to spec or document>
disable-model-invocation: true
---

# Story-video

One document in, a narrated explainer out. The developer is involved at three
points: the length, the storyboard with audio consent, and the finished video.
Everything between is scripts.

**Announce at start:** "Using opm:explainer-video; this makes a narrated slideshow, not animation."

Invocation text is in `$ARGUMENTS`. Scripts live next to this file in
`${CLAUDE_PLUGIN_ROOT}/skills/explainer-video/scripts/` (written `S/` below). Every
script takes the story directory as its one argument. Layout slots and
pictogram names: `templates/layouts.md`. A complete example:
`templates/storyboard.example.json`.

## Gates

| Gate | Passes only when |
|---|---|
| G1 Source | The path exists, is readable text, and can support about 270 words of narration (a 2 minute video) |
| G2 Storyboard and audio | `validate-storyboard.js` prints `ok:` AND the developer chose a build option on the latest storyboard |
| G3 Video | The developer chose "Approve" on the latest build, not an earlier one |

Never skip a gate. Silence or "sounds good" does not pass one.

## Phase 0: parse and check tools

1. The source path is all of `$ARGUMENTS`. Resolve it to an absolute path. It may contain spaces, even a trailing space in a directory name; always pass paths as separate arguments.
2. `slug`: the source file name without a leading date and without its extension, in kebab-case. Story directory: `docs/story/<slug>/` in the current project.
3. Run `node S/setup.js --check`. `browser: null` stops the run: name the browsers looked for (Chrome, Chromium, Edge, Brave) and the `CHROME_PATH` override. `python: null` means only the local voice can be offered at G2; say so now.

## Phase 1: read and size

Read the source. Propose a length and ask once with AskUserQuestion: 2, 4 or 6
minutes, default 4. The measured pace is 134 words per minute including pauses.

| Target | Narration words | Scenes |
|---|---|---|
| 2 min | about 270 | about 5 |
| 4 min | about 540 | about 9 |
| 6 min | about 800 | about 14 |

If the source cannot support 270 words without padding, stop at G1 and say how
much it could support.

## Phase 2: storyboard

Write `docs/story/<slug>/storyboard.json` yourself, in the main thread, in the
shape of `templates/storyboard.example.json`. Then run
`node S/validate-storyboard.js <storyDir>` and fix every error.

Rules for the author:
- Every fact in narration, headings and slots comes from the source. Each scene's `source` names the section. Invent nothing.
- Anything the source describes as not built yet gets `planned: true`.
- Narration is never repeated on the slide. The voice carries the words; the slide carries the picture.
- Write "AI", not "A.I.".
- Declare one `protagonist` at the top level and use that name in every scene that
  shows a person. Never use a real person's name, even a colleague's first name,
  and never carry a name across from the source document. Use a placeholder such
  as Alice, Bob or Asha, or ask the developer which name to use. A video outlives
  the conversation it came from and the person in it did not agree to appear.
- Pick a kit layout for every scene you can. Use `custom` only when no layout can carry the point, and say why in `visual`.
- `voice` and `rate` are optional. Suggest a voice that fits the source's language and locale; write the narration in that language. Do not translate the source.

## Phase 3: approve the storyboard, consent to audio (G2)

Show: the title, each scene's id, layout and heading, the narration word count
and estimated length from the validator, which scenes are `planned`, and every
person's name that appears in the storyboard. If a named person is real, say
so, and make sure `note` does not describe them as made up.

Ask one question with AskUserQuestion:

- **Build with the neural voice.** The narration text is sent to Microsoft's speech service through edge-tts, an unofficial route with no licence or uptime guarantee. Fine for internal use. For client-facing or public videos the licensed route is Azure AI Speech, which this skill does not implement.
- **Build with the local OS voice.** Nothing leaves the machine. It sounds noticeably robotic.
- **Change the storyboard.** Free text. Revise, re-validate, ask again.

Ask once per run. Rebuilds after G3 feedback reuse the answer. Offer the
neural option only when Python was found in Phase 0.

## Phase 4: build

Run in order. Every step is incremental: unchanged scenes are skipped.

1. `node S/setup.js` installs ffmpeg, ffprobe and edge-tts into the tools folder. First run takes about a minute.
2. `node S/render-slides.js <storyDir>` writes `slides/`. It ends with `custom scenes to draw: <ids>`. Above that it prints `orphan slides, not in the storyboard: <ids>` when slide files are left over from scenes that have since been deleted; it never removes one. Delete those files yourself before Phase 6, which commits `slides/` wholesale.
3. If that list is not `none`, dispatch one agent for all of them:

```
Agent (subagent_type: general-purpose, model: opus)
description: "Draw custom explainer-video slides"
prompt: |
  Draw slides for scenes <ids> of <abs storyDir>/storyboard.json. For each,
  write <abs storyDir>/slides/scene-<id>.html. Copy the whole document from
  <abs storyDir>/slides/scene-<a kit scene id>.html and change only the
  heading, sub line, chip, counter and the contents of the
  <svg viewBox="0 0 1740 530"> stage. Draw what the scene's `visual` field
  describes. Rules: nothing on the stage under 30px; stay inside the 1740x530
  stage; do not put the narration on the slide; draw the protagonist the same
  way the kit's `person` pictogram does; use only the colours in slides.css.
  Do not edit slides.css, do not take screenshots, do not dispatch subagents.
  Report: files written.
```

4. `node S/render-frames.js <storyDir>` writes one 1920x1080 PNG per slide.
5. `node S/build-video.js contact-sheet <storyDir>` writes `.build/contact-sheet.png`. Read that one image. Open a full frame from `frames/` only when a tile looks wrong. Fix the storyboard slot or the custom slide, then rerun from step 2.
6. `node S/narrate.js <storyDir> --engine neural` or `--engine local`, as chosen at G2.
7. `node S/build-video.js build <storyDir>` measures every scene's narration, refuses silent or truncated audio, then writes `<slug>.mp4` and `<slug>.srt` and confirms the MP4 has an audio track. Its last line ends `narration checked`.

## Phase 5: approve the video (G3)

Open the MP4: `open` on macOS, `xdg-open` on Linux, `start ""` on Windows.
Report its length, size and scene count. Ask: "Approve" or "Request changes"
(free text). On changes: edit the storyboard or a custom slide, re-validate,
and rerun Phase 4 from step 2. Do not work out what changed; the scripts do.
Every rebuild gets its own approval question.

## Phase 6: finish

Commit `storyboard.json`, `slides/`, `<slug>.srt`, `<slug>.mp4` and `.gitignore`
as `docs(story): <slug> explainer video`. Frames, audio and segments are
ignored by the `.gitignore` the skill wrote. Report the MP4 path, length, size,
the voice used, and that an edit is rebuilt by rerunning Phase 4.

## Errors

| Situation | Do |
|---|---|
| Source missing, not text, or too thin | Stop at G1 and say which |
| No Chromium-family browser | Stop; name the browsers looked for and `CHROME_PATH` |
| No Python 3 | Continue; offer only the local voice at G2 and say why |
| `setup.js` fails (offline, npm or pip error) | Stop; show the failing command's last lines |
| Validator errors | Fix them all before G2; never build around one |
| `narrate.js` fails after 3 attempts on a scene | Finished scenes are kept. Offer a retry or the local voice |
| No local voice (`espeak-ng` missing on Linux) | Say so; do not install it |
| A frame is not 1920x1080 or never appears | Stop naming the scene; the slide file stays for inspection |
| Build says a scene's narration is silent or too short | Delete that `audio/scene-<id>.mp3`, rerun `narrate.js`. If it is silent again with the local voice, say so and offer the neural voice |
| Missing frame or audio at build | `build-video.js` names the scene before encoding; rerun the step that makes it |
| Custom-slide agent fails | Kit scenes are still built. Offer a retry or switch that scene to a kit layout |

## Red flags

| Thought | Reality |
|---|---|
| "I'll draw every slide myself, the kit looks generic" | That cost 190k tokens once. Use a layout; `custom` is for the scene that truly needs it. |
| "I'll look at every frame to be safe" | Read the contact sheet once. Open a frame only when a tile looks wrong. |
| "This fact makes the story better" | If it is not in the source, it is not in the video. |
| "It's planned but basically decided" | Planned is labelled planned. |
| "They agreed to the neural voice last time" | Consent is per run. Ask at G2. |
| "The name is obviously fictional" | List the names and let the developer say. Keep `note` truthful. |
| "I'll reuse the name from the source document" | That is usually a real colleague. Use a placeholder or ask. |
| "Narration failed, I'll drop in silent audio so the build finishes" | A video without its voice is the bug users report. Fix the narration or stop and say so. |
| "ffmpeg is missing, I'll install it with the system package manager" | Tools go in the tools folder through `setup.js`. Never touch the system. |
| "I'll put the narration on the slide so it's clear" | The validator rejects it, and it reads badly on video. |
| "Small edit, I'll work out which files to rebuild" | Rerun the same commands. The manifest rebuilds only what changed. |

## Safety

- Narration text leaves the machine only after consent at G2, and only to Microsoft's speech endpoint.
- Nothing is installed outside `~/.opm/explainer-video-tools/` (`OPM_EXPLAINER_TOOLS` overrides; an older `~/.opm/story-video-tools/` is reused if present). No PATH changes, no global packages. Deleting that folder is a full uninstall.
- In the project, the skill writes only under `docs/story/<slug>/`, and commits only at Phase 6. Outside it, only the tools folder above and a temporary browser profile under the system temp directory, removed after each frame; when the removal keeps failing the script warns, leaves the profile behind and carries on, so a stuck profile never fails a render.
- Real people are surfaced at G2. `note` must not describe a real person as made up.
