---
name: rtf
description: Give it a YouTube URL and it returns a word level timestamped transcript (an RTF) plus the moments in the video where a graphic would actually earn its place — each with in and out timecodes, the words underneath, why it was picked, and what to put there. Also reads the picture to say where the speaker sits and which part of the frame stays free. Trigger on "/rtf", "RTF this video", "transcript with timestamps", "word level transcript", "where should I add graphics", "find the moments in this video", "timestamp this video", or any YouTube URL handed over with a request for a transcript or for insert points.
---

# /rtf — a YouTube URL in, a timestamped transcript and the moments out

    python3 scripts/run.py "https://youtu.be/VIDEO_ID"

That is the whole thing. It takes about ten seconds for a ten minute video.

## What comes out

In the output folder:

    report.html    everything in one self contained file you can send to anyone
    rtf.json       every word with its timestamp, plus sentences
    words.tsv      seconds<TAB>word, one row per word
    moments.json   the ranked moments with their scores and their reasons
    picture.json   where the speaker sits, and how still the screen is second by second

**RTF means every word is mapped to the second it is spoken.** Not a caption block, not a
line, the word. That is what makes the rest possible: you can place something on screen
against the exact word it belongs to instead of guessing from a paragraph.

## Options

    --out <folder>    where to write (default: ./rtf-<video title>)
    --top <n>         how many moments to return (default 8)
    --min-gap <secs>  spacing between moments (default: scaled to the video length)
    --no-video        transcript only. Much faster, no screen check, weaker moments.

## How a moment gets picked

Two questions, and both have to go the right way.

**Is he saying something a picture explains better than words?** A figure, a list, a
comparison, a mechanism, a definition, a point in time. Those are the things an audience
cannot hold in their head from audio alone. Each fires a signal with its own weight, and
the strongest signal decides what the suggested visual should be.

**Is the screen free?** A graphic dropped over a moment that already shows the thing is
wasted, and one dropped over a busy demo fights it. The video is sampled twice a second, so
stillness is measured rather than assumed.

There is also a negative signal, and it matters as much as the positive ones. "As you can
see here", "look at this", and — the sneaky one — "I'm going to come over here and click
this" all mean the screen is already doing the explaining. Those windows lose points however
good the sentence reads in a transcript.

Windows are aligned to sentence boundaries so no clip starts mid word, they run 6 to 20
seconds, and once one is chosen nothing else is allowed within the gap. That last rule is
deliberate: eight graphics inside the first ninety seconds is a worse answer than eight
spread across the video, even when the raw scores prefer the cluster.

Anything scoring below the floor is dropped rather than padded, so a thin video honestly
returns four moments instead of eight weak ones.

## How the picture read works

The video is shrunk to a 32x18 grid, each cell covering a 60x60 block of a 1080p frame, and
every cell is watched across the whole video.

A cell showing a person changes a little in almost every single sample. A cell showing a
parked slide or a still editor barely changes at all, with occasional spikes when something
is clicked. The **median** change per cell separates those two cleanly, with no fixed
brightness threshold to tune per video.

The report gives you two boxes:

- **The busiest region.** On a screen recording with a webcam this is the person, and the
  box lands within about one grid cell of the real inset. On a fully animated video it is
  whatever the video is animating, so it is labelled as that rather than called a speaker.
  A small always moving box against the edge of the frame is called a camera inset; the same
  box floating in the middle is not.
- **The clear zone.** The largest rectangle that stays still for most of the video. Put a
  graphic there and it will not cover anything that matters.

## After it runs

Summarise the moments in chat as a table — number, in, out, length, and one line on why —
and point at the report. Open `report.html` if the person wants to read the transcript;
searching it is faster than scrubbing the video.

If they want graphics built from the moments, hand over `moments.json`. Every entry carries
the exact words underneath it, so whatever builds the visual can sync to the word rather
than to the clip.

## Honest limits

- **It reads the transcript, not the screen.** The signals are language patterns. Before
  committing to a moment, pull the frame and look — the thumbnail on each card in the report
  is there for exactly that. A moment where the screen already shows the thing is dead, and
  this is the single most common way a pick goes wrong.
- **Captions come from YouTube, so timings follow the published cut**, not your edit
  timeline. If you own the video and have a word level export from your editor, that is
  better and should be used instead.
- **Some channels get captions with no punctuation at all.** Sentences then fall back to
  pauses, which is fine for finding moments and makes the transcript harder to read.
- **No captions, no analysis.** If a video has neither automatic captions nor uploaded
  subtitles there is nothing to work from.

## Requirements

`python3`, `yt-dlp`, and `ffmpeg` on PATH. No Python packages at all — standard library
only, so there is nothing to install and nothing to keep up to date.

    brew install yt-dlp ffmpeg          # macOS
    pip install yt-dlp                  # anywhere

`ffmpeg` is only needed for the picture pass. Without it, `--no-video` still works.
