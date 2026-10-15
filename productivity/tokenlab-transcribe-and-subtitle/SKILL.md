---
name: tokenlab-transcribe-and-subtitle
description: "Turn audio or video into a transcript, SRT or VTT subtitles, and translated subtitles with TokenLab speech-to-text and text translation models. Use when the user says \"transcribe this recording\", \"make subtitles for my video\", \"I need an SRT file\", \"caption this podcast\", \"what does this audio say\", or \"translate these subtitles into Spanish\". Gets timed segments, builds SRT/VTT, and translates cue by cue so timings stay. To turn a script into speech, use tokenlab-voiceover. For a talking video from a script, use tokenlab-talking-avatar."
license: MIT
metadata:
  category: audio
---

# Transcribe and Subtitle

Turn speech into text you can ship: a clean transcript, timed SRT or VTT subtitles, and the same subtitles in other languages. Transcription and text translation are two different endpoints and two different models.

## Inputs to collect

- **Audio or video file:** flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm. Max 25 MB per request.
- **Spoken language,** if known (ISO-639-1, for example `en`, `zh`, `ja`).
- **Output:** plain transcript, SRT, VTT, or word timings.
- **Subtitle rules:** max characters per line (42 is a common default), and target languages.
- **Terms to spell right:** names, brands, and jargon.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `stt` | `whisper-large-v3-turbo` | default | Timed transcript for subtitles |
| `stt` | `whisper-large-v3` | alternative | Timed transcript, alternative (not live-tested) |
| `stt` | `qwen3-asr-flash` | alternative | Plain transcript |
| `stt` | `fun-asr` | alternative | Plain transcript, alternative (not live-tested) |
| `translation` | `doubao-seed-translation` | default | Translate transcript or cue text |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **Timed transcript for subtitles:** Whisper. The turbo tier is the default; large v3 is the alternative. `verbose_json` returns `segments`, and word timings when you ask for them.
- **Plain transcript:** Qwen ASR, or Fun ASR as the alternative. Qwen ASR takes `prompt` for spelling. Check for timings before you build subtitles from it.
- **Translate transcript or cue text:** Doubao Seed Translation, through `/v1/translations`.

Exact fields come from the model contract.

Do not use `/v1/audio/translations` for this skill. Translate the text with `/v1/translations` instead.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contracts: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL_ID --operation stt` for the speech-to-text model and `contract MODEL_ID --operation translation` for the translation model. Take `MODEL_ID` from the Models list above.
2. Check the file. If it is over 25 MB, cut it into parts at silences, or extract a mono audio track from the video (for example `ffmpeg -i in.mp4 -vn -ac 1 -b:a 64k out.mp3`). Keep each part's start offset.
3. Estimate. Speech-to-text prices per second of audio; some models bill a minimum length per request (read `minimumUnitCount` in `GET /v1/models/{model}/pricing`). Example: a 5.5 s clip on a 10 s minimum is billed as 10 s × (price per second). Translation prices per token.
4. Transcribe with timings. Multipart upload:
   `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/audio/transcriptions --form model=MODEL_ID --form response_format=verbose_json --form 'timestamp_granularities[]=word' --form language=en --file file=@clip.mp3 --wait > transcript.json`
   The response can be the transcript or a task (`status` + `poll_url`); `--wait` polls a task for you.
5. Build subtitles from the timings with this skill's own helper, `scripts/subtitles.py` (relative to this skill's folder; standard library only, no API calls, and it reads the helper's output directly): `python scripts/subtitles.py transcript.json --format srt --max-chars 42 > clip.en.srt` (or `--format vtt`). This works even when a model cannot return SRT or VTT itself. Add each part's start offset if you split the file.
6. Translate cue by cue, so each cue keeps its time:
   - `python scripts/subtitles.py transcript.json --max-chars 42 --text-only > cues.en.txt`
   - Send the lines as `text` to `/v1/translations` with `target_language`. Write the returned `text` to `cues.es.txt`.
   - `python scripts/subtitles.py transcript.json --max-chars 42 --texts cues.es.txt > clip.es.srt`
   If the line count does not match, translate in smaller batches or one cue per request.
7. Return the transcript text, the subtitle files, the models, and the request IDs.

## Technique

- **Ask for `verbose_json`.** It returns `segments` with `start` and `end`, and word timings when you ask for them. Build SRT/VTT from that. Direct `response_format=srt` or `vtt` is documented for Whisper, but if it fails, the `verbose_json` path still works.
- **Whisper fields.** The Whisper model contracts list only `file` and `language`, but the transcription API reference documents `response_format` and `timestamp_granularities` for Whisper, and both work today. If a call returns `400 unsupported_parameter`, drop them and fall back to plain `json` text.
- **Send `language` when you know it.** It avoids a wrong-language guess on short or noisy clips.
- **Use `prompt` for spelling** on models that list it (Qwen ASR): put names and terms in it, for example "TokenLab, Kubernetes, Dr. Okafor".
- **Not every `verbose_json` has timings.** Some models return only `text`, `language`, and `duration`. Use a Whisper model when you need segments.
- **Cue length:** about 42 characters per line and one or two lines per cue reads well. `--max-chars` splits long segments on word timings.
- **Translate text, not files.** Send cue lines, not the SRT with timestamps; the translator can merge or drop lines. Keep the line count equal to the cue count.
- **Clean audio wins.** Mono, normal level, and little music under the voice give better text than any setting.

## Quality bar

- The transcript matches the audio; names and terms are spelled right.
- Subtitle times line up with speech, with no overlaps and no cue longer than the line limit.
- Translated subtitles have the same cue count and times as the source.
- The final answer lists files, models, request IDs, and any parts you split.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-voiceover`: speech audio from a script.
- `tokenlab-talking-avatar`: a speaking video from a portrait and audio.
- `tokenlab-api-integration`: put this flow into application code.
