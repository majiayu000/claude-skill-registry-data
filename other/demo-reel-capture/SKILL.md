---
name: demo-reel-capture
description: Produce a short-form reel that demos a live web product. Claude drives Chrome with Playwright in macOS fullscreen and records the screen itself, so there is no extension overlay, no AI cursor, no Dock, no tabs and no address bar. Plans beats from the script first, records only those, pulls full-resolution assets out of the page, and assembles the screen footage with a talking head without breaking lip sync. Use when someone wants a product demo reel, a sponsored or brand video that shows a web app working, or clean screen footage of a website. Usage - /demo-reel-capture <product name or URL>
argument-hint: <product name or URL>
---

# Demo Reel Capture

Production pipeline for a reel where a web product has to be **shown working**, not described.

**Input**: $ARGUMENTS

This skill covers **capture and assembly**. Once you have a synced master, hand off to your caption,
SFX and overlay pass (for example the `edit-reel` skill in this plugin).

## Requirements

- **macOS** (fullscreen is driven by AppleScript and the screen is recorded through ffmpeg's
  `avfoundation` input)
- Google Chrome installed (Playwright uses the `chrome` channel)
- Python 3.9+ with Playwright: `pip3 install playwright` (the installed Chrome is used, so
  `playwright install chromium` is only needed if you switch the channel to bundled Chromium)
- `ffmpeg` and `ffprobe` on PATH
- The terminal app running Claude Code needs **Screen Recording** and **Accessibility** permission
  (System Settings > Privacy & Security)
- For assembly and word anchoring: `openai-whisper` (`pip3 install openai-whisper`)

Bundled scripts live in `${CLAUDE_SKILL_DIR}/lib/`.

---

## The rule that governs everything

**Record only what you will use.**

A recorded "walkthrough" easily runs 5+ minutes for a reel that needs about 30 seconds of screen
footage. That surplus costs a full session of scrubbing and breeds mistakes: a beat where the prompt
box is still empty, a "3D you can spin" beat where the model sits static, a crop that cuts the
screen edges.

**Hard cap the walkthrough recording at 1:30.** If the flow genuinely cannot be shown in 90 seconds,
record it in two takes rather than one long one.

The way to hit that: **write the script first, list the beats, then record only those beats.** Never
record a full exploratory session and hope the moments are in there.

---

## Phase 0: plan the beats before anything records

From the approved script, write a beat list: one line per voiceover line that needs screen, and what
must be visibly true on screen at that moment.

```
L04 "Describe what you want"     -> prompt text VISIBLE in the box, not empty
L09 "3D designs you can spin"    -> model actually ROTATING, not a static front view
L10 "Technical drawings"         -> annotated flat sketches on screen
L12 "sends it to a manufacturer" -> the quote screen, all the way through
```

That "must be visibly true" column is the whole point. The most common revision note on a demo reel
is a beat where the screen does not show what the voiceover claims.

---

## Phase 1: Claude drives AND records, fullscreen

Do NOT use the Claude-in-Chrome extension for footage that will be published. It draws an outline
around the page and a large glowing cursor, both deliberate "an AI is driving this" indicators with
no off switch, and they look wrong in a published reel.

Instead, drive Chrome with Playwright and record it yourself. No extension means no overlay, and
fullscreen means no Dock, no macOS menu bar, no tabs and no address bar.

```bash
cp ${CLAUDE_SKILL_DIR}/lib/beats_example.py ./<product>_beats.py     # edit the beats
python3 ${CLAUDE_SKILL_DIR}/lib/capture.py ./<product>_beats.py
```

Output lands in `./demo_captures/<NAME>.mp4` (override with `REEL_CAPTURE_DIR`), already cropped to
the page content. Each beat is a function taking the `Stage` helper; its docstring is the VO line and
a comment says what must be visibly true. See `beats_example.py`.

### The three things that make it clean

All three are needed. Any one missing and something ugly is in frame.

1. `ignore_default_args=["--enable-automation"]` removes the "Chrome is being controlled by
   automated test software" infobar.
2. `--test-type` removes the yellow "You are using an unsupported command-line flag" bar that
   appears once you remove the first one.
3. `browser.show_fullscreen_toolbar = false` in the recording profile's Preferences. This is the one
   that actually hides the tabs and address bar. **Fullscreen alone does not do it**, Chrome pins
   the toolbar by default.

`--kiosk` does NOT work here, Playwright overrides it. Real macOS fullscreen driven by AppleScript
(`Cmd+Ctrl+F`) is what removes the Dock and menu bar.

### Recording profile

A dedicated profile at `~/Library/Application Support/ReelRecordingProfile` (override with
`REEL_PROFILE_DIR`) keeps personal bookmarks, tabs and logged-in accounts out of frame. Log into the
product once in that profile and it persists. The script also neutralises the auto-assigned profile
theme, which otherwise tints the browser frame.

### Pacing

The driver types character by character (65ms) and glides the mouse over 30 steps. Instant text
reads as a paste and teleporting cursors read as a bot. Call `st.hold()` on every beat so each end
state is long enough to cut on.

### Before a real shoot

- **Allowlist Chrome in Screen Time** (or any app limiter). A usage limit can kill the run mid-take
  with a "You've reached your limit" dialog.
- **Check the product tolerates automation.** Sites behind bot protection (e.g. a Cloudflare
  "Performing security verification" challenge) will block the scripted browser. Dry-run before
  committing to a shoot. If it blocks, record the flow by hand and use `playback-capture` instead.
- **There is no address bar in fullscreen**, so a "type the URL" beat is not possible. Load the start
  URL before recording, and open on the product itself.
- **Multiple displays**: set `REEL_SCREEN` to the screen number Chrome goes fullscreen on.

## Phase 2: pull the real assets out of the page

Do not screenshot product imagery. Screenshots are viewport-resolution and look soft as overlays.
Extract the source URLs from the DOM and download them at full size:

```javascript
[...document.querySelectorAll('img')].map(i => i.currentSrc || i.src)
  .filter(s => s.includes('<the product CDN or storage host>'))
```

Then `curl` them down. Product renders and generated images usually exist at far higher resolution
than they are displayed, sharp enough to use as full-screen cards.

Store them under `assets/<product>/`, verify each file is a real image (a 2KB file is an error page,
not a PNG) and eyeball a contact sheet before using them.

---

## Phase 3: talking head

**Rear camera, not front.** The front camera mirrors, which flips any text in frame and reads as off.

Film the whole script in one sitting with multiple takes per line. Do not intercut a different
location or outfit with an earlier batch. To pick takes from raw footage, use `trim-raw-video`.

---

## Phase 4: phone over the screen (optional, and usually skip it)

Filming a phone pointed at the laptop while the walkthrough plays gives handheld texture. **The
fullscreen capture in Phase 1 replaces this.** It is sharper, has no moire, no glare, no reframing
drift, and needs no sync work at all.

Only reach for the phone pass when the brief specifically wants a physical, in-the-room feel. If you
do, use `playback-capture` to build the video to film, keep the laptop screen filling most of the
frame and lit so it is not blown out, then follow the offset and crop notes in Phase 5.

## Phase 5: sync and assemble

If you used the Phase 1 digital capture, there is no offset to find and no screen crop to choose.
Skip straight to "Cut talking-head segments as ONE unit", which still applies and is still the thing
most likely to break.

The two subsections below apply ONLY to the optional phone-filmed path.

### Find the offset once, verify at both ends

The phone footage starts before the playback does. Find the constant offset:

```
screen_source_time = walkthrough_time + OFFSET
```

**Verify it at the start and again at the end of the recording.** If it drifts, the playback and the
phone camera are running at different effective rates and you need to re-derive it per beat.

### Crop for the whole screen, not a punch-in

Use a crop that keeps the **entire laptop screen** in frame. An aggressive punch reads as sloppy
because it slices the screen edges.

```
crop=2060:3662:50:178     # whole screen, from 2160x3840 phone footage
crop=1542:2742:309:625    # REJECTED 1.4x punch, cut the edges off
```

Check a dense page (a spec sheet, a settings table) at the chosen crop before committing. If the
dense page reads, everything reads.

### Cut talking-head segments as ONE unit

**This is the part that breaks lip sync if you get it wrong.**

Do not build a video track and map audio over it separately. Cut each talking-head segment with
**both streams from the same source window**, so lip sync is native and cannot drift:

```python
subprocess.run(["ffmpeg","-y","-ss",str(a),"-to",str(b),
                "-i", TALKING_HEAD,          # ONE input, both streams
                "-vf", VF, "-af","aresample=async=1:first_pts=0",
                *COMMON, seg_path])
```

For b-roll segments, pair the screen video with that line's voiceover:

```python
subprocess.run(["ffmpeg","-y",
                "-ss",str(screen_in),"-t",str(D),"-i", SCREEN,
                "-ss",str(vo_in),   "-t",str(D),"-i", TALKING_HEAD,
                "-map","0:v","-map","1:a", ...])
```

Then concat segments with audio intact. Rounding resets at each cut instead of accumulating.

**The failure mode this prevents:** concatenating a dozen re-encoded video pieces and mapping a
separately built audio track over the result. Video and audio durations diverge and the last
talking-head beat ends up visibly out of sync. Verify with:

```bash
ffprobe -select_streams v:0 -show_entries stream=duration ...
ffprobe -select_streams a:0 -show_entries stream=duration ...
# must match within ~10ms
```

### Silence padding

`PAD = (0.06, 0.08)` seconds before and after each line. Tighter than it sounds like it should be.
`(0.10, 0.14)` leaves the cut feeling slack.

---

## Phase 6: anchor everything to words, then hand off

Re-transcribe the assembled master (Whisper, in the language of the video, e.g. `en` or `el`) and
anchor captions, SFX and overlays to **word indices**, never hardcoded seconds, so a re-cut re-times
itself.

**The pitfall that will bite you:** if you merge tokens (gluing a leading-`.` token like `.com.` onto
the previous word), every index after that point shifts down by one. Recalculate anchors against the
**merged** list, and print each resolved anchor before rendering:

```
W_LINK -> [95] 'Link' @ 34.02
```

A wrong anchor is an `IndexError` if you are lucky and a silently misplaced caption if you are not.

Then hand off to the caption, SFX and overlay pass.

---

## Verify before delivering

1. Frame grid across the whole video, actually look at it. Every screen beat must show what the VO
   says at that moment.
2. Video and audio stream durations match.
3. Audio peak below 0 dBFS.
4. Largest gap with nothing happening under ~2s.
5. Re-transcribe the final and diff against the approved script.

---

## Notes for sponsored work

- Get the product and hook **signed off in writing** before filming. A change of product after script
  approval is a new production, not a revision.
- Log which revision round you are on. Contracts typically grant one.
