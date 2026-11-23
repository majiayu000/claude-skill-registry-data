---
name: regional-devotional
description: "Devotional and regional-language video editor for Claude: turns bhajans, kirtans, aarti, satsang, katha, temple festivals, gurbani, qawwali and church or mosque recordings into respectful long-take films with large Indic-script lyrics or subtitles (Devanagari, Tamil, Telugu, Bengali, Gurmukhi, Gujarati, Kannada, Malayalam), plus WhatsApp-status-length verticals. Use when the user says 'edit this bhajan video', 'aarti video with lyrics', 'Hindi captions', 'Tamil subtitles', 'make WhatsApp status clips', 'temple festival video', 'satsang highlights', 'devotional song with lyrics on screen'. Runs on video-studio-core (transcribe in the regional language, lyric and caption elements, colour, deliver, QC)."
license: MIT
---

# Regional Devotional

The ritual sets the pace, the script is spelled right, and the clip fits on a WhatsApp status.

- **Best for:** bhajan, kirtan, aarti, satsang and katha, temple and festival coverage, gurbani, qawwali, hymns
- **Inputs:** the recording (one or more angles), the correct lyrics text in the regional script (from the singer,
  the temple or a printed book), optional photos of the deity or the venue
- **Default skin:** `soft-gradient` · alternatives `minimal-mono`, `dual-subs` (two scripts), `cinematic-phone`
- **Formats:** 16:9 full video, 9:16 status clips
- **Durations:** full as performed (1-60 min), status clips 15-60 s (WhatsApp status shows 60 s per part)
- **Genre preset:** `--genre regional-devotional` (see `python CORE/scripts/editor.py genre regional-devotional`)

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- Ask for: the language and script, the exact lyrics (do not rely on ASR for sacred text), the names and titles of
  the singers, saints or deities as the family or temple writes them, and what must not be cut (the full aarti,
  a mantra repeated a set number of times).
- **Rights:** a bhajan sung live is fine to film with the organisers' permission, but a recorded track from a label
  (T-Series, Saregama and others) is copyrighted. Ask who owns the audio before publishing.
- **Respect:** no comic SFX, no flashy transitions, no cropping a deity's murti or a guru's face, no cutting a mantra
  or prayer mid-line. Some temples forbid filming the garbhagriha: drop those shots if asked.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| opening darshan / title | 8 | deity or altar, the venue, title in the regional script |
| ritual / bhajan | 80 | the performance in long takes: singer, instruments, devotees, close-ups of the ritual |
| closing aarti / blessing | 12 | aarti or final prayer complete, prasad, blessing, fade out |

**Pacing.** ASL 6-20 s. Hold through each line of a song; change angle on a line or a phrase change, never mid-word.
Repetitive sections (a 108-count mantra, the pheras of a ritual) keep their rhythm: shorten with long dissolves
between complete repetitions, never by chopping inside one.

**Cut rules.**
- No autocut: the singing has natural breaths and instrumental breaks (`--no-cut`).
- Cut on the tala (beat) or on the end of a line. Devotee reactions as cutaways over the song, never over a mantra.
- Never splice lines from different verses into a new verse.

**Transition grammar.** Straight cuts and slow dissolves (1-1.5 s); a dip to black at the end. No whips, no glitch.

**Music and sound.** The performance is the audio: no added music, no SFX. Gentle dialogue chain (no heavy
compression, the harmonium and dholak need dynamics). Crowd and bells stay.

**Colour.** `golden-hour` (preset) or `portra` for warm lamp-lit interiors; `indian-wedding` keeps reds and gold rich.
Intensity 0.5-0.7. Do not push saturation on saffron and red: it clips.

**Captions.** Large lyrics, one line at a time, in the regional script (`lyric` element or `captions` with
`preset: "karaoke"`). Optional second line in English or in Latin transliteration (`dual-subs` skin). Fonts must cover
the script: Noto Sans/Serif Devanagari, Tamil, Telugu, Bengali, Gurmukhi, Gujarati, Kannada, Malayalam.

**What the client judges.** Devotional feel, correct script and spelling (matras, conjuncts), that it plays on
WhatsApp, and that elders and the guru look dignified.

**Common mistakes.** Boxes or broken conjuncts from a font without the script; ASR lyrics with spelling errors;
comic sticker effects; cutting the aarti short; status clips over 16 MB; English-only captions for a Hindi audience.

## Make the edit

```bash
python CORE/scripts/run.py bhajan.mp4 --style SKILLS/soft-gradient --genre regional-devotional --format 16:9 --no-cut --language hi --model small --prompt "Shri Ram, Hanuman, Radhe" --work bh --stop-after plan
python CORE/scripts/render.py bh/plan.json --frames 3,30,90,180
python CORE/scripts/render.py bh/plan.json
python CORE/scripts/finish.py bh/plan.json --platform youtube
```

Language codes for `--language`: `hi` Hindi, `ta` Tamil, `te` Telugu, `bn` Bengali, `pa` Punjabi, `gu` Gujarati,
`kn` Kannada, `ml` Malayalam, `mr` Marathi, `ur` Urdu, `sa` Sanskrit. Use `--model small` or larger: `base` is weak on
Indic languages. ASR is a timing guide only: replace its words with the correct lyrics (see below).

Several angles of the same performance: `python CORE/scripts/multicam.py camA.mp4 camB.mp4 --wide wide.mp4 --out bh/multicam.mp4`
(each file must start at the same moment), then use `bh/multicam.mp4` as the input above.

Status clips (9:16): pick one complete line or chorus (15-60 s) and put that range in a one-clip spec,
`bh-status/spec.json` = `{"format": "9:16", "fps": 30, "clips": [{"src": "../bhajan.mp4", "in": 120, "out": 165, "reframe": "face"}]}`:

```bash
python CORE/scripts/run.py - --timeline bh-status/spec.json --style SKILLS/soft-gradient --genre regional-devotional --format 9:16 --no-cut --model small --work bh-status --stop-after plan
```

The timeline step transcribes the clip without a language flag; set the lyrics by hand in the plan (next section).

## Refine the plan

Edit `bh/plan.json`:

- **Fonts for the script** (Devanagari example; swap the family for Tamil, Telugu...):
  `"theme": {"fontsUrl": "https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@500;700;800&display=swap",
  "vars": {"--font-display": "'Noto Sans Devanagari',sans-serif", "--font-body": "'Noto Sans Devanagari',sans-serif"}}`.
  Keep the skin's `cssFiles`. Without internet the fallback font may lack the script: check the contact sheet.
- **Correct the lyrics:** replace the `w` text in `words` with the right spelling, keeping each `start`/`end`.
  Or drive the screen from your own lines with the `lyric` element (times on the cut timeline):
  `{"type": "lyric", "lines": [{"text": "श्री राम जय राम जय जय राम", "start": 12.4, "end": 18.9}], "y": 860, "w": 1600}`.
- **Captions instead of lyric:** `{"type": "captions", "preset": "karaoke", "maxWords": 6, "uppercase": false, "y": 900}`
  (uppercase must be off for Indic scripts). Delete any skin hook/headline in English that does not fit.
- **Title:** `{"type": "titlecard", "kicker": "श्री हनुमान जयंती 2026", "title": "सुंदरकांड पाठ", "start": 0, "end": 4, "in": "fade", "out": "fade"}`.
- **Audio:** `"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "warm", "compress": false}}`; no `music`.
- **Colour:** `"color": {"look": "golden-hour", "intensity": 0.6}`, `"finish": {"grain": 0, "vignette": 0.25}`.
- **Two scripts:** run with `--style SKILLS/dual-subs` and follow that skin's notes for the second line.

## Deliver

```bash
python CORE/scripts/deliver.py bh/plan.json --to youtube --out-dir bh/deliver --burn no
python CORE/scripts/deliver.py bh-status/plan.json --to whatsapp-status,reels,shorts --out-dir bh-status/deliver
python CORE/scripts/qc.py bh/deliver/final_youtube.mp4 --plan bh/plan.json --platform youtube
python CORE/scripts/qc.py bh-status/deliver/final_whatsapp-status.mp4 --plan bh-status/plan.json --platform whatsapp-status --strict
```

`whatsapp-status` is 720x1280, max 60 s, and lowers the bitrate to fit 16 MB. The `captions.srt` sidecar keeps the
regional script (UTF-8); upload it on YouTube for search in that language. Plan already shows lyrics, so burn-in
stays off (`--burn auto` respects that).

## Check before delivering

- Contact sheet zoomed in: every matra, conjunct and nukta renders (no boxes, no dotted circles), lines not cut off.
- Lyrics match the agreed text word for word; names and honorifics (Shri, Ji, Sant, Guru) exactly as given.
- The full aarti or prayer is intact; no mid-line cuts; deity and guru never cropped.
- Status file under 16 MB and 60 s; plays on a phone; loudness -14 LUFS / -1 dBTP.
- Tell the user the audio rights question was settled (or that it still needs settling) before posting.

## Example requests

- "Edit this Hanuman Chalisa recording with the lyrics in Hindi on screen."
- "Make 30-second WhatsApp status clips of the best lines from the kirtan."
- "Temple festival video with Tamil subtitles and an English line under them."
