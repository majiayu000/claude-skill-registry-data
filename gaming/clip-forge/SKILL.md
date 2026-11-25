---
name: clip-forge
description: Turn a long YouTube video, podcast, gameplay recording, match or tutorial into ready-to-post, fully edited vertical Shorts / Reels / TikToks. Finds the most viral moments (from the transcript for talk, from action, sound and scoreboard or kill-feed changes for gameplay and sport), shows a scored table for approval, then renders 1080x1920 clips with a real edit - colour grade, punch-in zooms, slow motion, sound effects, speaker tracking, an animated headline and word-by-word captions (English and Malayalam). Use whenever the user gives a YouTube link or a video file and wants shorts, reels, clips, highlights, "viral parts", "best moments", "cut this into short videos" or "edit this clip", even if they do not name this skill. Also use when a message starts with /clip-gameplay, /clip-podcast, /clip-sports, /clip-tutorial, /clip-video or /clip-edit.
---

# ClipForge

Long video in, a handful of finished vertical clips out. ClipForge is built
by lowdevco.

The bar is a clip that looks like an experienced editor made it: the picture
fills the frame, the colour has punch, the picture and sound react on the
moments that matter, and the headline and captions are designed and timed.
A plain cut with a label on top is not the goal.

## At a glance

| Step | You do | Output | Stop for the user? |
|---|---|---|---|
| 0. Mode | Settle the kind of video, read its reference | `references/<mode>.md` in mind | Only if the mode is unclear |
| 1. Check | `check_setup.py` | `mode`, `todo`, `speech_to_text` | Before installing anything on their PC |
| 2. Get | `fetch.py`, the .bat route, or a file already here | `<workdir>/<video>.mp4` (+ subtitles) | Videos over ~90 min: whole or a section? |
| 3. Find | Tools from the mode reference | Candidate moments | No |
| 4. Score | Score, table, ask | Approved clip numbers | **Always.** Never render before the answer |
| 5. Edit | Plan → render → quality check | `<workdir>/shorts/*.mp4` | No |
| 6. Post copy | Title, caption, hashtags | `<workdir>/shorts/posts.md` | No |
| 7. Hand over | Deliver files, list clips, offer changes | The reply | It ends the turn |

Working conventions:

- All scripts live in `scripts/` next to this file. Call them with the
  absolute path to that folder.
- One work folder per video (`<workdir>`); finished clips go in
  `<workdir>/shorts`.
- Anything that takes more than a minute or two (speech-to-text, scouting,
  rendering) runs in the background, and you tell the user roughly how long.

## Ground rules

1. **Rights.** Only work on videos the user owns or may reuse. If they are
   clipping someone else's channel, say once that re-uploading needs the
   owner's permission, then carry on.
2. **Approval before rendering.** Rendering is the slow part and their taste
   decides. Show the scored table and wait.
3. **Never invent.** Hooks, callouts, kill counts, scores and quotes come from
   what you saw in frames or read in the transcript. Never make up a channel
   handle; ask for it once.
4. **Honest scores.** Three good moments get three high scores, not twelve
   85s. Say when you judged from still frames only.
5. **Check your own work.** Look at frames of every rendered clip before
   showing it (step 5c).
6. **Restraint.** Three well-placed beats in 30 s feel edited; ten feel like
   a filter.

## 0. Mode

The kind of video decides how moments are found, framed and captioned. Read
the one reference file for the mode before step 3, and follow it.

| Command | Mode | Reference | Use for |
|---|---|---|---|
| `/clip-gameplay <link>` | gameplay | `references/gameplay.md` | Game recordings and streams, with or without a facecam |
| `/clip-podcast <link>` | podcast | `references/podcast.md` | Podcasts, interviews, talking head: the moment is in the words |
| `/clip-sports <link>` | sports | `references/sports.md` | Matches and broadcasts: goals, wickets, points, finishes |
| `/clip-tutorial <link>` | tutorial | `references/tutorial.md` | How-to, lessons, coding, screen recordings: one complete idea per clip |
| `/clip-video <link>` | video | `references/video.md` | Everything else: vlogs, reviews, events, travel, reactions |
| `/clip-edit <file or link>` | edit | `references/edit.md` | The user already has the clip or the times and wants only the edit; replaces steps 3 and 4 |

- A command at the start of the message (or the kind of video named in
  words) settles the mode. Do not second-guess it.
- With no command, decide from the title, channel and a contact sheet
  (`peek.py --at` with five times spread over the video). Still unclear: ask
  in one line.
- Anything after the link is a request to honour, for example
  `/clip-gameplay <link> top 3, neon captions, watermark @myname`.

## 1. Check the machine

```
python scripts/check_setup.py
```

Read `mode`, `todo` and `speech_to_text`. Install what `todo` lists (they are
copy-paste commands; ask before installing on the user's own PC).

| Result | Meaning |
|---|---|
| `mode: local` | YouTube is reachable (Claude Code on the user's own PC). The whole pipeline runs from just a link |
| `mode: cloud` | YouTube is blocked (Claude chat / cloud sessions). The download happens on the user's computer; everything after runs here. Do not retry through other tools or mirrors: the block is at the network level |
| `speech_to_text: false` | No transcript can be made here unless the video has subtitles. Podcast mode needs one; say so before starting |

## 2. Get the video

**A. Local mode, link given**

```
python scripts/fetch.py "<url>" --out <workdir>
```

It prints the video path and any subtitle files. For videos over ~90 minutes
ask whether they want the whole thing or a section (`--section 600-3000`).

**B. Cloud mode, link given**

Say plainly, in one or two sentences, that this chat cannot download from
YouTube itself and the download takes one step on their PC. Then:

1. Send them `assets/pc/get_video.bat` (once; they keep it in a folder of
   their choice, e.g. a project folder connected to the chat).
2. They double-click it and paste the link. It saves the video, subtitles
   and info file into an `inbox` folder next to the .bat. Default is 720p to
   keep the file small; `get_video.bat <url> 1080` gives sharper crops.
3. If computer-folder tools are available (names containing
   `remote-devices`), list the `inbox` folder, copy the `.mp4` and every
   `.json3` / `.vtt` beside it into the workspace, and continue. Those tools
   usually cap one file at about 400 MB: if the video is bigger, ask them to
   re-run the .bat at 480, or to say which part of the video matters.
4. With no such tools, ask them to attach the video and subtitle file (small
   files only), or to run this skill in Claude Code on the PC where route A
   works end to end.

**C. A video file is already here** (attached, or in a connected folder):
use it directly. A subtitle file with the same name beside it is picked up
automatically.

## 3. Find the moments

Follow the reference file for the mode. The tools it draws on:

| Tool | What it gives |
|---|---|
| `transcribe.py <video> --out <workdir> [--lang en\|ml\|auto] [--model small]` | Word-timed transcript: subtitle file → faster-whisper → sherpa-onnx. Exit code 3 = no transcript possible |
| `scout.py <video> --out <workdir> [--top 12] [--len 30] [--kind sports] [--roi x,y,w,h]` | The stretches with the most sound and motion, ranked, each with an 8-frame filmstrip in `<workdir>/scout/`, plus `end.jpg` for the last 45 s. `--roi` is the kill-feed or scoreboard box: every change there is counted and timed |
| `track.py <video> --clips <workdir>/clips.json --write` | Who is on screen and who is talking in each clip; writes a suggested layout, face positions and a speaker-following crop path into `clips.json` |
| `analyze_audio.py <video> --out <workdir>` | Single loud instants (a laugh, a shout) with their lift in dB |
| `peek.py <video> --at 754,760 --out x.jpg` | Frames at exact times |
| `peek.py <video> --range 998-1032 --n 8 --out x.jpg` | A filmstrip of one stretch, start to finish |
| `peek.py <video> --at 600 --grid --out x.jpg` | One frame with a pixel grid, for reading the box of a facecam, kill feed or scoreboard |
| `peek.py <video> --at 600,640 --crop x,y,w,h --out x.jpg` | One region enlarged, for reading a score or other small on-screen text |

Transcripts:

- `exact_word_timing: false` means word timings are estimated inside each
  line. Captions still work; the highlight is a little less tight.
- Speech-to-text is roughly real time with `small` on 2 CPUs. Run it in the
  background and tell the user. Do not go below `small` for Malayalam, and
  say Malayalam captions will need a read-through.
- When it finishes, read `<workdir>/transcript.txt` in full (compact
  `[mm:ss] text`; the JSON is for the renderer).

Scouting: `scout.py` takes about two minutes for a 17-minute 1080p video. Its
`action` number is a rank inside that one video: it says where to look first,
not how good the moment is. Open the filmstrips and judge with your own eyes.

## 4. Score and get approval

Aim for 8–12 candidates on a long video (fewer if it is short), each 20–60 s;
action moments can be as short as 12 s. No overlaps.

Score each out of 100:

| Part | Points | What earns them |
|---|---|---|
| Hook | 30 | First 3 seconds make a stranger stop: a claim, a question, or action already under way |
| Payoff | 25 | It delivers: the answer, the punchline, the kill, the fail |
| Stands alone | 20 | Makes sense without the rest of the video |
| Emotion | 15 | Surprise, laughter, tension, awe, or strong disagreement |
| Pace | 10 | No dead stretch; the length fits the content |

Show the table, best first:

| # | Time | Len | Score | Hook line (on screen) | Why it works |
|---|---|---|---|---|---|
| 1 | 12:34–13:10 | 36s | 88 | He quit a ₹40 lakh job for this | Bold claim up front, clean ending |

Then, in the same message, ask:

- which numbers to render (offer "top 5");
- the channel handle for the watermark, if not known;
- whether they want a different look from the mode's default edit.

**Stop here until they answer.**

The hook line is the 3–8 word headline shown for the first 3.5 seconds. Put
`*stars*` around the one or two words that carry it; they take the accent
colour. Create curiosity without lying about the clip. Use the speaker's
language (Malayalam hook for a Malayalam clip).

## 5. Edit

Read `references/editing.md` now. It is the editing standard; this section
is the short version.

### 5a. Plan each clip

For every approved clip decide five things, then write `<workdir>/clips.json`:

| Decide | Key | Rule of thumb |
|---|---|---|
| Framing | `layout` | Fill the screen: `center` or `speaker` first, `blur` last |
| Treatment | `edit` | From the mode reference, unless the user named a look |
| Headline | `hook` | 3–8 words, one or two `*starred*` words, true to the clip |
| Beats | `beats` | The 2–3 moments the picture reacts to; exact times beat `auto` |
| Ending | `end`, `outro` | End on the payoff, never in an end card or menu |

```json
{"clips": [
  {"id": 1, "start": 754.2, "end": 790.6, "hook": "He quit a *₹40 lakh* job",
   "slug": "quit-job", "layout": "auto", "edit": "story", "tighten": true},
  {"id": 4, "start": 2210, "end": 2236, "hook": "1 HP. *Four enemies.*",
   "layout": "center", "edit": "hype", "captions": false,
   "beats": ["auto", {"t": 2229.4, "fx": ["punch", "flash"], "text": "Clutch"},
             {"t": 2231.0, "fx": "slowmo", "len": 1.2}]}
]}
```

**Edits**

| Edit | Best for | What it does |
|---|---|---|
| `hype` | Gameplay, sports, anything fast | Vivid grade, slow push-in, punch + shake + flash with a bass thump on each beat, condensed all-caps headline, progress bar |
| `premium` | General video (default) | Punchy grade, slow push-in, punch-in with a soft thump on each beat, bold headline |
| `story` | Podcasts, interviews, talking head | Soft grade, zoom cuts on sentence changes, animated captions |
| `clean` | Business, tutorials, serious topics | Soft grade and animated text only |
| `raw` | When the user wants it untouched | Plain cut, boxed headline, static captions |

**Beats** are the moments the picture reacts to. Leave `"beats"` out to have
them found from the sound, or list your own: `t` in source seconds, `fx` of
`punch`, `shake`, `flash`, `slowmo`, optional `text` for a one-to-three word
callout. Slow motion at most once per clip, on the payoff.

**Layouts**

| Layout | Result |
|---|---|
| `speaker` | 9:16 crop centred on the detected face; follows `"focus_path"` from `track.py` when present |
| `auto` | `speaker` if a clear face is found, otherwise `blur` |
| `center` | 9:16 crop that fills the screen; `"focus_x": 0–1` slides it, `"focus_path"` moves it over time |
| `stack` | Two speakers, one above the other; face positions come from `track.py` or `"faces"` |
| `split` | Facecam on top, game below; needs `"facecam": [x, y, w, h]` |
| `blur` | Whole width kept in the middle, blurred copy above and below; `"zoom": 1.0–2.5` enlarges the sharp picture. Last resort: it leaves the picture small |

**Looks**, for every clip on the command line or per clip in `clips.json`:

| Option | Per-clip key | What it does |
|---|---|---|
| `--edit hype\|premium\|story\|clean\|raw` | `"edit"` | The editing treatment |
| `--style bold\|clean\|neon\|fire` | `"style"` | Caption look and accent colour. `bold`: white capitals, yellow accent (default). `clean`: smaller sentence case, pale blue. `neon`: green accent, purple outline. `fire`: largest, orange accent |
| `--outro "Follow for more"` | `"outro"` | Tag that pops over the last 1.6 s |
| `--watermark "@name"` | `"watermark"` | Small see-through channel tag for the whole clip |
| `--progress` | `"progress"` | Thin bar along the top that fills as the clip plays |

### 5b. Render

```
python scripts/render.py <video> --clips <workdir>/clips.json --out <workdir>/shorts [--edit hype] [--style fire] [--outro "Follow for more"] [--watermark "@name"]
```

- It prints one JSON line per clip: `ok`, `file`, `layout`, `edit`,
  `seconds`, and `beats` with the times the effects landed.
- A full render takes about 1.5× the clip's length per clip on an ordinary
  PC. Say how long, and run it in the background.
- When framing or a beat time is a guess, run `--preview` first: small fast
  drafts (`*_preview.mp4`) to check before the full render.
- Re-render one clip with `--only <id>`.

### 5c. Quality check

Pull frames from each clip and look at them before showing anything:

```
ffmpeg -y -loglevel error -ss 2 -i <clip.mp4> -frames:v 1 <workdir>/check_01.jpg
```

Check the headline (2 s), one beat, and the last second. Every clip must pass:

| Check | Fix if it fails |
|---|---|
| The subject is in frame, nothing important cropped off | `layout`, `focus_x`, `zoom` or `facecam` |
| The frame is full, not a small picture floating in blur | `center` / `speaker`, or `blur` with `"zoom": 1.6`+ and `"hook_hold": true` |
| The hook is readable and true to the clip | Rewrite `hook` |
| Captions do not sit on a face or on the part of the game that matters | `layout` or `"captions": false` for voiceless gameplay |
| Beats land on the actual moment, not near it | Exact `t` in `beats` |
| The clip ends on the payoff, not in an end card or menu | Move `end`; check with `peek.py --range` |
| Caption words are right (names, terms) | Fix `transcript.json`, re-render |

Re-render just the failing clip with `--only <id>`.

## 6. Post copy

For each rendered clip, in the clip's language:

- **Title**: under 60 characters, the hook rephrased, no clickbait the clip
  does not pay off.
- **Caption**: 1–2 lines plus a question or call to action.
- **Hashtags**: 3–5, one broad, the rest specific to the topic or game.

Save them as `<workdir>/shorts/posts.md` and show them in the reply.

## 7. Hand over

- **Local mode**: say where the `shorts` folder is.
- **Cloud mode**: send each `.mp4` and `posts.md` as files. If the video came
  from a connected folder on their computer, also save the clips into a
  `shorts` folder beside the `inbox`.

Finish with one line per clip (number, length, hook) and offer changes: a
different start or end, another layout or caption style, a new hook line, or
more clips from the remaining candidates.

## Things that go wrong

| Symptom | Cause and fix |
|---|---|
| Download fails in local mode with a sign-in or bot message | Update yt-dlp (`python -m pip install -U yt-dlp`) and retry once. Still failing: ask the user to download it another way and use route C |
| `transcribe.py` exits 3 with "could not find module ... dll" | The speech engine is installed but cannot load. `check_setup.py` prints the fix (on Windows, the Visual C++ runtime). A machine problem, not a silent video: say so |
| Captions are wrong words | The transcript is wrong, not the renderer. Fix the words in `transcript.json` for that range and re-render, or re-run `transcribe.py` with a bigger `--model` |
| Face crop follows the wrong person | `track.py` guesses the speaker from mouth movement. Switch that clip to `stack`, or `center` with a `focus_x` |
| The edit feels like too much | Drop to `premium` or `clean`, or give a short explicit `beats` list instead of `auto` |
| `ass` filter missing | ffmpeg was built without libass; `check_setup` says how to install a full build |
