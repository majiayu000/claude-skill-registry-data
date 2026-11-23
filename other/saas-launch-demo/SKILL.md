---
name: saas-launch-demo
description: "SaaS launch and product demo editor for Claude: turns a screen recording plus optional founder voice/face into a 60-180 s launch or demo video (outcome, problem, walkthrough, result, CTA) with readable UI, targeted zoom-ins, callouts, cursor pointers, PII blurred, and a 15 s social cut and GIF loop. Use when the user says 'edit my product demo', 'make a launch video for my app', 'Product Hunt video', 'feature announcement video', 'turn this screen recording into a demo', 'SaaS explainer', or hands over a screen capture of software. Runs on video-studio-core (transcribe, cut, motion graphics, deliver, QC)."
license: MIT
---

# SaaS Launch Demo

Get the viewer to the "aha" fast: the outcome first, then the three moves that make it happen.

- **Best for:** product launches, feature announcements, Product Hunt videos, landing-page demos, onboarding videos
- **Inputs:** screen recording(s), optional webcam/founder clip or voice-over, logo, product name and URL
- **Default skin:** `tutorial-steps` · alternatives `device-fly`, `terminal-tech`, `kinetic-launch`
- **Formats:** 16:9 hero, 9:16 and 1:1 social cuts, GIF/WebP loops
- **Durations:** hero 60-180 s (launch film 60-90 s), social 15 s, loop 6 s
- **Genre preset:** `--genre saas-launch-demo`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Record clean: demo account with fake data, notifications off, 1920x1080 or larger, large UI zoom (125-150%).
- **PII:** real emails, names, API keys or customer data on screen must be hidden. Blur them with the plan's
  `blurs` boxes (see Refine), cover them with a `shape`/`card`, or re-record with demo data.
- Ask for: product name spelling, the one outcome to promise, the three features to show, CTA and URL, pricing claims.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| outcome | 10 | the finished result on screen in the first 2 s (dashboard, report, shipped thing) |
| problem | 10 | the painful old way in one line or one shot |
| walkthrough | 60 | three features, one idea each, each ending on its result |
| result | 10 | the payoff number or screen, said and shown |
| CTA | 10 | product name, URL, offer; logo |

**Pacing.** ASL 3-6 s; a visual change every 4 s (zoom, callout, pointer, cut). Cut every wait: loading, typing,
scrolling to find something. 2x-4x speed through boring but necessary steps.

**Cut rules.**
- Cut on the click: the result appears right after the action; never watch a spinner.
- Zoom in when the UI text is below ~24 px at 1080p; zoom out to re-orient after 2-3 moves.
- Jump cuts are fine in the screen recording; in the face cam cover them with the screen.
- Never show a feature that does not exist yet as if it ships (label "coming soon").

**Transition grammar.** Cuts and zoom punches; whip only between features; dissolve only for a scene change.

**Music and sound.** Light electronic bed ~-26 dB, ducked under the voice. UI SFX low: `click` / `ui-tap` on real
clicks, `success-chime` on the result, `whoosh-short` on feature changes (about 4/min).

**Colour.** No look on the UI (`grade` none): brand colours must stay accurate. Face cam only: `cool-corporate` 0.4.

**Captions.** Two-line subtitles low, sentence case, <= 20 cps (`"preset": "clean"`); keyboard shortcuts as `chip`s.

**What the client judges.** UI readability (on a phone too) and time to "aha".

**Common mistakes.** A 15 s logo intro; tiny unreadable UI; the cursor wandering; real customer data visible;
showing every setting; a feature tour with no outcome; CTA without a URL.

## Make the edit

With voice in the recording (or a face cam with the screen recording as a clip):

```bash
python CORE/scripts/run.py demo.mp4 --style SKILLS/tutorial-steps --genre saas-launch-demo --format 16:9 --smart-cuts --retakes --title "Ship reports in 5 minutes" --cta "Try it free at acme.io" --work sd --stop-after plan
# face cam + separate screen recording: the screen becomes clip "main"
python CORE/scripts/run.py founder.mp4 --style SKILLS/device-fly --genre saas-launch-demo --format 16:9 --clip screen.mp4 --logo logo.png --work sd2 --stop-after plan
python CORE/scripts/render.py sd/plan.json --frames 1,6,15,30,50
python CORE/scripts/render.py sd/plan.json
python CORE/scripts/finish.py sd/plan.json --platform youtube
```

Silent screen recording with a written script: make the voice-over first, then use it as the speaker audio:

```bash
python CORE/scripts/tts.py --script vo.txt --out vo/voice.wav --words
python CORE/scripts/scenes.py screen.mp4 --work sd3 --threshold 0.15     # UI changes = candidate cut points
```

Then cut the screen to the voice's length (a timeline spec with `"audio": "mute"` and `"speed": 2` on waits,
built with `timeline.py build spec.json --work scr --no-transcribe`), mux the voice on with FFmpeg
(`ffmpeg -i scr/assembled.mp4 -i vo/voice.wav -map 0:v -map 1:a -c:v copy -shortest demo_vo.mp4`) and run the
first `run.py` command on `demo_vo.mp4`. Don't put a voice in `"music"`: it would be ducked and treated as a bed.

**15 s social cut:** a new work folder, `--format 9:16 --duration 15`, outcome + one feature + CTA only.

## Refine the plan

- **Hook (first 2 s):** a `text` element with the outcome ("Reports in 5 minutes, not 5 hours"); show the result screen.
- **Zoom into UI:** `"speaker": {"zooms": [{"start": 8.2, "end": 11.0, "scale": 1.6, "cx": 0.72, "cy": 0.3}]}`
  (when the screen is the speaker video; `cx`/`cy` = the button, 0-1 of the source frame, one per zoom). For a `clip` element use `keys` (`"s": [[0, 1], [0.6, 1.6, "expoOut"]]`).
- **Pointers and callouts:** `{"type": "callout", "point": [1210, 340], "x": 1500, "y": 180, "title": "One-click export", "start": 12, "end": 15}`,
  `{"type": "pointer", "x": 1210, "y": 340, "kind": "hand", "start": 12, "end": 13.5}`.
- **Steps:** `{"type": "steps", "steps": [{"label": "Connect", "at": 9}, {"label": "Build", "at": 21}, {"label": "Share", "at": 34}]}`.
- **Shortcut chips:** `{"type": "chip", "text": "Ctrl + K", "start": 18.4, "end": 20}`; code: `codeblock` with `cps`.
- **Hide PII:** `"blurs": [{"x": 640, "y": 212, "w": 380, "h": 40, "start": 0, "end": 60}]` (output pixels, top-left
  box; `"pixelate": true` for a mosaic; one box per time range when it scrolls or a zoom moves it). It blurs the
  screen under the graphics. Screen inside a `clip`/device element: blurs don't reach it, so use a solid
  `{"type": "shape", "kind": "bar", ...}` over it instead.
- **Device frame:** `{"type": "clip", "clip": "main", "device": "laptop", "motion": "flyIn"}` for the opener.
- **SFX:** `"sfx": [{"t": 12.1, "kind": "click", "gain": 0.35}, {"t": 15.0, "kind": "success-chime", "gain": 0.4}]`.
- **Colour:** leave the screen untouched (`"color": {"auto": false}`); face cam only `{"look": "cool-corporate", "intensity": 0.4}`.
- Check auto `counter`s: value and label must match what is said.

## Deliver

```bash
python CORE/scripts/deliver.py sd/plan.json --to youtube,linkedin,x,gif,webp --out-dir sd/deliver
python CORE/scripts/deliver.py sd15/plan.json --to reels,tiktok,shorts --out-dir sd15/deliver
python CORE/scripts/qc.py sd/deliver/final_youtube.mp4 --plan sd/plan.json --platform youtube --strict
```

`gif`/`webp` give a 6 s loop of the start for the landing page: make the first 6 s the outcome. Product Hunt and
landing pages autoplay muted, so burn captions in (`--burn yes`) on those uploads.

## Check before delivering

- Watch the contact sheet at phone size: every UI label readable, zooms land on the right element.
- No real personal data, keys or customer names visible in any frame (scrub the full render).
- Product name, prices and URL correct; every promised feature exists.
- `qc.py` passes; cut waits are gone; the CTA holds >= 2 s.

## Example requests

- "Turn this 6-minute screen recording into a 90-second launch video for Product Hunt."
- "Make a 15-second vertical teaser of the new export feature with captions."
- "Zoom into the buttons I click and blur the customer emails."
