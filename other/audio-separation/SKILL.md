---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: audio-separation
description: >
  Separate audio with fal.ai: split a song into vocals and instrumental (Demucs),
  or isolate any described sound like a voice, dog bark or siren (Meta SAM Audio).
  Use when the user wants vocal removal, acapella, karaoke track, stems, isolate
  voice or speech, remove background noise or music, or extract a sound from audio
  or a video soundtrack.
---

# Audio separation

Two bun scripts in `~/.config/opencode/skills/audio-separation/`. Both take a
local file or a URL, upload local files to fal storage, and save the results
next to the input (or in `--out`). They print a JSON map of saved paths to
stdout and progress to stderr.

```bash
S=~/.config/opencode/skills/audio-separation
bun $S/demucs.ts song.mp3                          # song.vocals.wav + song.instrumental.wav
bun $S/sam.ts interview.mp3 --prompt 'man speaking' # interview.target.wav + interview.residual.wav
```

## Which script

| goal | script | model | price (3 min audio) |
|---|---|---|---|
| song vocals vs instrumental, karaoke, acapella | `demucs.ts` | `fal-ai/demucs` `htdemucs_ft` | ~$0.13 |
| drums, bass, other stems | `demucs.ts --stems` | same | ~$0.13 |
| guitar and piano stems too | `demucs.ts --model htdemucs_6s --stems` | `htdemucs_6s` | ~$0.13 |
| speech over noise, dialogue from video, any sound by text | `sam.ts --prompt '...'` | `fal-ai/sam-audio/separate` | ~$0.30 |
| a sound you can locate in time | `sam.ts --span 6-10` | `fal-ai/sam-audio/span-separate` | ~$0.30 |

Default to `demucs.ts` for music. It is cheaper and trained on music stems.
Use `sam.ts` when the target is not a standard music stem, or when Demucs
leaves too much bleed and the user accepts the higher price.

## API key

`FAL_KEY` lives in `.env` next to the scripts (gitignored). The scripts read it
themselves; an exported `FAL_KEY` wins. If it is empty the script exits with
an error: ask the user to fill it from https://fal.ai/dashboard/keys. Never
print the key.

## demucs.ts

```bash
bun $S/demucs.ts <file-or-url> [--out dir] [--model htdemucs_ft] [--format wav|mp3] [--stems] [--shifts 1-10]
```

- **instrumental** is the sum of the non-vocal stems, mixed locally with ffmpeg.
- `--stems` keeps the separate drums/bass/other files.
- `--shifts` above 1 improves quality a little but runs longer.

## sam.ts

```bash
bun $S/sam.ts <file-or-url> --prompt 'what to isolate' [--predict-spans] [--candidates 1-7]
  [--acceleration fast|balanced|quality] [--span 6-10 ...] [--exclude-span 20-22 ...] [--trim]
  [--format wav|mp3] [--out dir]
```

- **target** is the prompted sound, **residual** is everything else.
- Write short concrete prompts: `man speaking`, `female singing voice`, `dog barking`.
- `--candidates 3` reranks multiple outputs. Better quality, +50% cost per extra candidate.
- `--span` / `--exclude-span` switch to the span endpoint. `--trim` cuts output to the spans.
- fal documents WAV, MP3 and FLAC input. For video, extract audio first:
  `ffmpeg -i in.mp4 -vn -b:a 192k in.mp3`.

## Discord

After a run, upload the outputs with
`kimaki upload-to-discord --session <current-session> <files...>`.
Convert to mp3 first if wav files exceed Discord upload limits
(`ffmpeg -i x.wav -b:a 192k x.mp3`).
