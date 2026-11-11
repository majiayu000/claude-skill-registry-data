---
name: footage-ingest
description: "The 'card is in' step: after a recording session, finds the camera or mic card (DJI Osmo/Action/Mic, GoPro, Sony, any DCIM card), copies every clip with size verification, checks audio length == video length on every clip, transcribes them one at a time, drops clips that are not for reels, matches each take to its script and slate from the RECORD-SHEET, picks the best take of every hook, body and ending, conforms the picks (optional mirror for selfie view, constant 30 fps, TV-range BT.709), and safely ejects the card. Never writes to or deletes from the card. Use when someone says 'DJI is in', 'the card is in', 'I just recorded', 'ingest the footage', 'sort my takes'."
author: Johann (@johannships)
version: 1.0.0
---

# Footage ingest: "the card is in"

Step 3 of the pipeline: idea -> script (`reel-ideation`) -> record -> **"the card is in"** -> `edit-style` -> `trial-post` -> `reel-scorecard`.

The creator records, plugs the card (or the camera over USB) into the computer, and says "DJI is in". This skill
takes it from there and ends with a TAKE-MAP.md that hands the editor one folder per reel with the chosen clips.

## Requirements

Claude Code on the computer the card is plugged into (a chat app cannot read a card). ffmpeg + ffprobe,
Python 3.9+, a local Whisper (`use-local-whisper` skill). Check: `ffprobe -version && python3 --version`.

## Config (ask once, save to `ingest/config.json` in the creator's content folder)

| key | meaning | default |
|---|---|---|
| `dest_root` | where sessions go | `$HOME/reels` |
| `mirror_camera` | flip camera footage horizontally (selfie view). Ask the creator: many prefer how they look in a mirror | ask |
| `fps` | conform frame rate | 30 |
| `min_free_gb` | free disk needed before copying and rendering | 40 |
| `record_sheet` | the sheet the slates refer to | latest `RECORD-SHEET.md` |

## Steps

0. **Before:** if the creator is still recording, do nothing heavy (no renders, no transcription): an overloaded
   machine can drop mic audio. Start when they say the card is in.
1. **Find the card.** `python3 scripts/ingest.py find` lists every mounted folder with clips (DJI cameras write
   `DCIM/DJI_###/DJI_<YYYYMMDDHHMMSS>_<NNNN>_D.MP4`; DJI Mic transmitters mount as their own volume with WAV backups).
   Pick the folder whose clip times match the session. More than one card: ingest each.
2. **Check disk.** At least `min_free_gb` free (renders and swap need it). If not, list what could be cleared and
   ask. Never delete anything on the card, and never delete raws on the computer to make room.
3. **Copy + verify.** `python3 scripts/ingest.py copy --dest <dest_root>/record-<date> --src <card folder>`.
   It copies MP4/MOV + mic WAVs (proxies like .LRF stay on the card), size-checks every copy, re-runs safely,
   and writes `manifest.json` + `durations.tsv`. Exit 1 = a failed copy or an A/V mismatch.
4. **Audio == video, every clip.** Any `AV MISMATCH` or `NO AUDIO` line: tell the creator at once, name the
   clips, and ask for a re-take while the set is still up. If a mic WAV backup covers that clip, note it as the
   audio source instead.
5. **Eject.** Only when step 3 printed 0 failed copies: `sh scripts/eject.sh <card folder>`. From here on work
   only from the copies.
6. **Transcribe, one clip at a time.** `sh scripts/transcribe_all.sh <dest>/raw/<folder> <dest>/transcripts`.
   One heavy job at a time, `nice`, 4 threads: parallel 4K decodes plus Whisper can exhaust memory.
7. **Sort.** Read every transcript next to the RECORD-SHEET. Mark each clip:
   - which card and part it is (by the spoken slate, else by matching the words to the script): `R6 hook B`,
     `R6 body`, `R6 CTA IG`, `R6 CTA bio`;
   - `FLUB` (restart, trailing off), `RETAKE OF <clip>`;
   - `NOT FOR REELS` (other projects, tests, room tone): leave it in raw, do not edit it;
   - claims check: any spoken line that is false, outdated or overclaims ("scrape the entire internet",
     a number nobody measured) is flagged; the editor cuts it or the take is rejected.
8. **Pick the best take** of every hook, body and ending: complete, clean, the last good take of a repeated line,
   no false claims. Write the reason for every rejection. List what the sheet asked for that was NOT recorded.
9. **Conform the picks** (only the picks): `python3 scripts/conform.py <dest>/conformed <clip>... [--mirror]`.
   Mirror happens here, on the raw camera clip, before any caption, logo or screen capture is added (those are
   never mirrored). After mirroring, look at one frame per setup: text behind the creator now reads backwards
   (shirt logos, signs, screens); blur, crop or flag it. Phone screen recordings are never mirrored.
10. **Write TAKE-MAP.md** (`templates/TAKE-MAP.md`): the map table, the SHIP list (one line per reel: hook clip >
    body clips > IG ending / bio ending), REJECTED with reasons, NOT RECORDED, and open questions. Then hand each
    SHIP line to `edit-style`, at most 2 edits rendering at once on one laptop.

## Output

```
record-<date>/
  raw/<card folder>/       untouched copies (never edited, never deleted)
  manifest.json  durations.tsv
  transcripts/<clip>.words.json / .txt / .srt
  conformed/<clip>.mp4 + conform-manifest.jsonl
  TAKE-MAP.md              what ships, what was rejected and why, what is missing
  LOG.md                   written as you go (a long ingest outlives one agent)
```

## Failure handling

| problem | do |
|---|---|
| no card found | ask the creator to plug it in or connect the camera in USB storage mode; `INGEST_CARD_GLOBS` for odd mount points |
| copy size mismatch twice | do not eject; re-seat the card, run copy again (it skips good files) |
| A/V mismatch | name the clips, ask for a re-take now; check the mic backup WAV |
| disk under the limit | stop before transcribing; list space to clear, ask |
| a slate is missing | match on the words; if two scripts fit, say so in TAKE-MAP open questions |
| the agent gets cut off mid-ingest | everything is re-runnable: copy skips verified files, transcription skips done clips, LOG.md says where it stopped |
