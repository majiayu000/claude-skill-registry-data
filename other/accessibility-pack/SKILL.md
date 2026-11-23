---
name: accessibility-pack
description: "Accessibility pack for any finished Video Studio edit: SDH subtitles with [sound] tags and speaker IDs, broadcast-rule caption files (SRT, VTT, TTML), a clean transcript, an audio-description (AD) script written from the picture, and an AD voice track mixed into a separate described version. Use when the user says 'make it accessible', 'add SDH captions', 'subtitles for the deaf and hard of hearing', 'closed captions file', 'audio description', 'described version', 'WCAG captions', 'caption file for LMS / broadcaster', 'transcript for the video'. Runs on video-studio-core (deliver.py captions, tts.py, finish.py mix, qc.py). Works after any genre skill."
license: MIT
---

# Accessibility Pack

The same film for people who can't hear it and people who can't see it, delivered as files a broadcaster or LMS will accept.

- **Works on:** any finished edit with a plan (`W/plan.json` + `W/final.mp4`), or any video plus a words file
- **Makes:** `captions.srt/.vtt/.ttml` (SDH), `transcript.txt`, `ad_script.txt`, `ad_*.wav`, `final_ad.mp4` (described version), QC reports
- **Standards used:** Netflix/BBC caption practice (42 chars x 2 lines, <= 20 cps adults / 17 kids, 0.833-7 s), WCAG 2.2
  (1.2.2 captions, 1.2.3/1.2.5 audio description, 1.2.8 media alternative = transcript)

## Before you start

- Needs **video-studio-core** in the same skills folder (`CORE`). First run: `python CORE/scripts/check_env.py`.
- Start from a **locked** edit: captions and AD are timed to picture; any re-cut means redoing them.
- Ask: who speaks (names for speaker IDs), the language, whether the target is web (WCAG) or a broadcaster (which
  spec), whether a described version is wanted, and who will review the AD script (ideally a blind or low-vision reviewer).
- Honest limits: no SCC/CEA-608 encoder (say so if a broadcaster asks for SCC), no automatic speaker diarisation, no
  automatic sound-event detection, and finish.py does not duck the programme under AD lines. The steps below work around each.

## SDH captions (what makes them SDH, not plain subtitles)

- **Speaker IDs** when the speaker is off screen or not obvious: `PRIYA: ...` (or `[Priya]`), at the start of the cue.
- **Sound tags** in square brackets for sound that carries meaning: `[applause]`, `[upbeat music]`, `[phone buzzes]`,
  `[laughs]`, `[silence]`. Describe the sound, not your opinion of it; skip sounds that mean nothing.
- **Music:** `[upbeat music]` at the start; lyrics in the cue with ♪ if they matter to the story.
- Exact words, including meaningful hesitations; correct names and numbers; same cue length rules as broadcast.

**Make them:** the engine builds cues from a words file, so add the tags and IDs as extra "words" with times:

```bash
python - <<'EOF'
import json
p = json.load(open("W/plan.json", encoding="utf-8"))
w = [dict(x) for x in p["words"]]
w[0]["w"] = "PRIYA: " + w[0]["w"]                      # speaker ID on her first cue
sdh = [{"w": "[upbeat music]", "start": 0.0, "end": 0.9}] + w
d = p["output"]["duration"]
sdh.append({"w": "[applause]", "start": d - 0.9, "end": d - 0.1})
json.dump({"language": "en", "words": sdh}, open("W/sdh_words.json", "w", encoding="utf-8"), indent=1)
EOF
python CORE/scripts/deliver.py W/final.mp4 --to youtube --words W/sdh_words.json --out-dir W/access --burn no --no-thumbs --no-post
```

Give the **video** plus `--words`: with a plan as input, deliver.py uses the plan's own `words` and ignores `--words`.
A tag less than 0.7 s before speech joins the first spoken cue (`[upbeat music] PRIYA: Here are three`); for a cue of its
own, leave a gap of 0.8 s or more, or edit `W/access/captions.srt` by hand afterwards (it is plain text: keep the
numbering and timings, change the words). Children's content: add `--kids` (17 cps).

**Transcript (WCAG 1.2.8):** `captions.srt` text without timings, with speaker names and sound tags, plus a short
description of important visuals. Write it to `W/access/transcript.txt`.

**Burned-in (open) captions** for social feeds: `--burn yes` on the social presets; keep sidecars for YouTube/LMS.

## Audio description

1. **Find the gaps.** Read `W/plan.json` `words`: pauses of >= 1.5 s are AD slots. List what the picture shows that the
   sound doesn't say: on-screen text and slides, who appears, actions, settings, charts, the end card.
2. **Write `ad_script.txt`** in present tense, objective, short ("A slide lists three numbered mistakes."). Never
   interpret emotion the face doesn't clearly show; name people once they are introduced; read on-screen text aloud.
   One line per slot, with its start time: `14.4 | A slide lists three numbered mistakes.`
3. **Voice each line** (offline TTS; Windows SAPI is always present, kokoro is better if installed):

```bash
python CORE/scripts/tts.py --text "A slide lists three numbered mistakes." --out W/ad/ad_01.wav --backend sapi --rate 1.1
python CORE/scripts/tts.py --list-voices
```

   Check each WAV's length (`ffprobe`) fits its slot. Too long: shorten the words first, then `--rate` up to 1.2.
4. **Mix into a described copy** of the plan (same folder, so relative paths keep working):

```bash
python - <<'EOF'
import json
p = json.load(open("W/plan.json", encoding="utf-8"))
p["sfx"] = p.get("sfx", []) + [{"t": 14.4, "file": "ad/ad_01.wav", "gain": 1.0}]
p["outputFile"] = "final_ad.mp4"
json.dump(p, open("W/plan_ad.json", "w", encoding="utf-8"), indent=2)
EOF
python CORE/scripts/finish.py W/plan_ad.json --platform youtube
```

   `finish.py` re-uses `W/composite.mp4` (picture unchanged) and writes `W/final_ad.mp4`. The AD line plays on top of the
   programme without ducking it, so place lines only in real pauses. No pause long enough? Make one: add
   `"freeze": [{"at": 14.4, "dur": 3.0}]` (extended AD) to that clip in a timeline spec and rebuild, or shorten the line.
5. **Optional AD-only track** for players that take a separate AD audio stream: mix the AD WAVs onto silence with FFmpeg
   (`adelay` per line + `amix`) and deliver it next to `final_ad.mp4`.

## Broadcast caption rules (checked automatically)

`deliver.py` builds cues to Netflix/BBC practice and `qc.py` checks them: max 42 characters per line and 2 lines, <= 20 cps
(17 with `--kids`), 0.833-7 s per cue, 2-frame gaps, line breaks not after articles or between first and last name.
TTML is IMSC1 text profile. SCC (CEA-608) is not produced.

## Check before delivering

```bash
python CORE/scripts/qc.py W/access/final_youtube.mp4 --plan W/plan.json --platform youtube --out-dir W/access/qc
python CORE/scripts/qc.py W/final_ad.mp4 --plan W/plan_ad.json --platform youtube --out-dir W/access/qc_ad
python CORE/scripts/audio_chain.py measure W/final_ad.mp4 --platform youtube
```

- Read `captions.srt` start to end against the audio: names, numbers, speaker IDs, sound tags in brackets.
- Every AD line sits in a pause, never over dialogue; listen to the described version with your eyes closed.
- The described version's loudness passes (the AD lines raise the level; finish.py re-measures the whole mix).
- On-screen text that matters is either spoken by the presenter or read by AD.
- Deliver: SDH `captions.srt/.vtt/.ttml`, `transcript.txt`, `ad_script.txt`, `final_ad.mp4`, and the QC reports; say
  what you could not do (SCC, programme ducking, a human AD review).

## Example requests

- "Make SDH captions for my keynote, mark the applause and music, I'm Priya."
- "We need an audio-described version of this product video for our accessibility policy."
- "Give me caption files and a transcript the LMS will accept."
