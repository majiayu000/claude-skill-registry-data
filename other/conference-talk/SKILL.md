---
name: conference-talk
description: "Conference talk editor for Claude: turns a keynote, panel, meetup or webinar recording (speaker camera plus slides) into a clean 16:9 session video with a title card, speaker lower third, slide inserts, trimmed dead air and applause, accessible captions and chapters, plus a 60-90 s highlight and vertical quote clips. Use when the user says 'edit my talk', 'clean up this keynote recording', 'conference session video', 'add my slides to the talk', 'webinar recording edit', 'make a highlight from my speech', 'TEDx style edit'. Runs on video-studio-core (transcribe, gentle autocut, scenes, colour, deliver, QC)."
license: MIT
---

# Conference Talk

The talk as the audience should have seen it: the speaker when they matter, the slide when it matters, and nothing lost.

- **Best for:** keynotes, conference sessions, meetups, panels, webinars, lectures, TEDx-style talks
- **Inputs:** speaker camera (or the event's program feed), the slide recording or slide images, speaker name/title, event logo
- **Default skin:** `chapter-pro` · alternatives `minimal-mono`, `news-desk`, `frame-studio`
- **Formats:** 16:9 full session; 16:9 highlight; 9:16 quote clips
- **Durations:** session 10-60 min as given; highlight 60-90 s; quote clips 20-45 s
- **Genre preset:** `--genre conference-talk`

## Before you start

- Needs **video-studio-core** in the same skills folder (`CORE`); `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: exact speaker name and title, session title, event name and date, whether Q&A stays in, the slides (PDF
  exported to PNG, or a screen recording), and the event's permission to publish.
- Audience members asking questions in Q&A did not necessarily agree to be published: cut or blur them unless the event
  has consent, and keep only what the speaker repeats.
- Slides may contain third-party images or confidential numbers; ask before publishing every slide.

## How a pro cuts this

**Structure (session, % of length)**

| beat | % | what |
| --- | --- | --- |
| title card | 2 | session title, speaker, event, date (3-5 s) |
| talk | 90 | the talk in order; trim walk-on, mic fiddling, "can you hear me", long applause |
| Q&A | 6 | keep the best 1-3 questions, repeat the question as a caption if the mic missed it |
| end card | 2 | event logo, links, next event |

Highlight (60-90 s): the strongest 3-5 lines in talk order, each a complete thought, cold open on the best line.

**Pacing.** This is long-form for a patient audience: ASL 6-20 s, a visual change at least every 20 s (slide insert,
punch-in, wide). Do not tighten pauses like a reel: the speaker's timing is part of the talk. Max gap 1.2 s, fillers kept
natural (only um/uh go), no retake removal (a talk has no retakes).

**Cut rules.**
- Cut to the slide when the speaker says "as you can see", reads a number or points at the screen; hold the slide at
  least 4-6 s (people read it), longer for dense slides; go back to the speaker for stories, jokes and emotion.
- Slide + speaker picture-in-picture for long slide sections so the face stays present.
- Trim applause to 1-2 s after the opening and the ending; never cut a laugh off.
- Cover the few autocut joins with a slide insert or a punch-in (>= 1.2x) so no jump cut shows.

**Transition grammar.** Straight cuts between speaker and slide (a 0.3 s dissolve at most), dip to black between
sessions or before Q&A. Nothing else.

**Music and sound.** Music on the title and end cards only (bed -30 dB). Under the talk: none. Clean the room: light
denoise, `broadcast` EQ, de-ess; level the speaker; keep audience laughter. SFX none.

**Colour.** Accurate, not stylised: correct the white balance of stage light, `cool-corporate` or
`documentary-natural` at 0.4-0.5. Match the slide recording's brightness to the camera so cuts don't flash.

**Captions.** Accessible subtitles, sentence case, two lines, <= 15 cps (`"preset": "clean"`), plus sidecar SRT/VTT for
the platform. Speaker name as a lower third at first appearance.

**What the client judges.** Slides readable, the speaker looks good, the sound is clear, names right, and it is on
the website quickly.

**Common mistakes.** Slides too small or on screen too briefly; the speaker cut out while telling a story; reel-style
tightening; loud music under speech; missing lower third; a wrong job title; Q&A questions inaudible.

## Make the edit

```bash
# speaker camera + slide recording (available to elements as clip id "main")
python CORE/scripts/run.py talk.mp4 --style SKILLS/chapter-pro --genre conference-talk --format 16:9 --clip slides.mp4 --title "Three Mistakes" --model base --work ct --stop-after plan
# where do the slides change? (shot list of the slide recording; thumbs to look at)
python CORE/scripts/scenes.py slides.mp4 --work ct --threshold 0.15 --thumbs --out ct/slides_scenes.json
python CORE/scripts/story.py outline --work ct --genre conference-talk    # sentences s1..sN, quotable lines for the highlight
python CORE/scripts/render.py ct/plan.json --frames 1,4,8,13,16
python CORE/scripts/render.py ct/plan.json
python CORE/scripts/finish.py ct/plan.json --platform youtube
```

The genre preset keeps pauses up to 1.2 s (a speaker's timing); pass `--max-gap` only to change that.
For names and jargon add `--prompt "Priya Rao, Kubernetes"`. Long talks: `--model small` (default) is more accurate.

**Separate camera + program feed:** if you have a wide and a close-up with the same audio, `multicam.py` will not help
(it switches by loudest mic). Cut them by hand in a timeline spec, or use the program feed as the single input.

**Highlight:** pick sentences from `ct/outline.md`, then
`python CORE/scripts/story.py reorder --work ct --order "s12,s3-s4,s20" --genre conference-talk --format 16:9` and
`python CORE/scripts/run.py - --timeline ct/story_timeline.json --style SKILLS/chapter-pro --genre conference-talk --format 16:9 --model base --work ch --stop-after plan`.
Read `ct/story_flags.md`: no partial-sentence splices in a talk (it is the speaker's real words).

**Quote clips (9:16):** use clip-miner on the finished talk, or `story.py reorder ... --format 9:16` per quote.

## Refine the plan

- **Captions:** set the captions element to `{"type": "captions", "preset": "clean", "maxWords": 8}`; fix names in `words`.
- **Remove auto extras** that don't fit a talk: auto `counter` elements (check the value and label
  match what was said), `chip` "Subscribe", list `card`s built from the transcript.
- **Title card:** `{"type": "titlecard", "kicker": "VIDEO STUDIO CONF 2026", "title": "Three Mistakes", "subtitle": "Priya Rao, Founder", "start": 0, "end": 3}`.
- **Lower third:** `{"type": "lowerthird", "name": "Priya Rao", "role": "Founder, Studio Notes", "start": 3.2, "end": 8, "in": "maskUp", "out": "fade"}`.
- **Full-screen slide insert** (speaker audio continues):
  `"cutaways": [{"src": "C:/talks/slides.mp4", "start": 6.0, "end": 10.5, "srcStart": 42.0}]` with `srcStart` = the
  slide's time in the slide recording (from `slides_scenes.json`). Check the insert lands on the right slide in the `--frames` stills.
- **Picture-in-picture slide:** `{"type": "clip", "clip": "main", "clipOffset": 42.0, "start": 12, "end": 16.5, "x": 1530, "y": 640, "w": 640, "h": 360, "in": "fade", "out": "fade"}`.
  Keep it off the face (look at the sheet). Slide images instead of a recording: `{"type": "image", "image": "slide07.png", ...}`.
- **Chapters:** `"chapters": [{"start": 0, "title": "Intro"}, {"start": 95, "title": "Mistake 1"}, ...]` (first at 0, >= 3, each >= 10 s).
- **Colour and sound:** `"color": {"look": "cool-corporate", "intensity": 0.5}`, `"finish": {"sharpen": 0.3}`,
  `"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "broadcast", "deess": true}}`.
  The plan's `audio.platform` wins over `finish.py --platform`, so set the target in one place.
- Intro/outro music only: there is no per-section music in the plan. Build the title card + talk + end card as a
  timeline spec with the music on the card clips, or leave music out.
- `python CORE/scripts/editor.py review ct/plan.json --genre conference-talk` and fix its high items.

## Deliver

```bash
python CORE/scripts/deliver.py ct/plan.json --to youtube,podcast-mp3 --out-dir ct/deliver --burn no
python CORE/scripts/qc.py ct/deliver/final_youtube.mp4 --plan ct/plan.json --platform youtube --strict
python CORE/scripts/qc.py ct/deliver/final_podcast-mp3.mp3 --platform podcast
```

Upload `captions.srt`/`.vtt` as sidecars (YouTube, LMS, Vimeo) and paste `chapters.txt` into the description. For an
event site or LMS that wants -16 LUFS use `podcast-video` instead of `youtube`. Name files
`event2026_priya-rao_three-mistakes_v001_16x9.mp4`.

## Check before delivering

- Slides readable at 1080p on a phone; slide inserts held long enough to read; no slide covered by a lower third.
- Speaker name, title and session title spelled exactly as the event program.
- No jump cut visible; applause trimmed but laughs intact; the opening line is not cut.
- Captions match the audio (names, numbers, jargon); `qc.py` passes caption timing and loudness.
- Q&A voices audible or the question captioned; no audience member shown without consent.

## Example requests

- "Edit my keynote recording, put my slides in when I'm talking about them, captions on."
- "Clean up this 40-minute webinar: cut the setup, keep Q&A, add chapters."
- "Make a 90-second highlight of my talk for LinkedIn."
