---
name: tokenlab-talking-avatar
description: "Turn a portrait and a script or voice recording into a talking-head video with TokenLab avatar and video models. Use when the user says \"make this photo talk\", \"talking avatar\", \"AI presenter for my script\", \"lip-sync this face to my audio\", \"spokesperson video from a headshot\", or \"make a talking head that says ...\". Two paths: speech audio drives an avatar model, or a video model speaks a short quoted line itself. For a voice track only, use tokenlab-voiceover. For a portrait that moves without speech, use tokenlab-animate-image. For a body that copies a dance or gesture clip, use tokenlab-motion-control."
license: MIT
metadata:
  category: video
---

# Talking Avatar

Make a portrait speak. Pick the path by what the user has:

- **A voice recording, or a script plus a place to host audio:** speech audio drives an avatar model. You control the voice and the exact timing.
- **A short script only:** a video model generates the face, the voice, and the lip motion in one call. Fast, but you do not choose the voice.

TokenLab does not offer lip-sync onto an existing video. Every path starts from a still portrait.

## Inputs to collect

- **Portrait:** a public `https` URL or a TokenLab result URL. Front-facing, face clear and well lit, shoulders visible, mouth closed or neutral.
- **Speech:** a voice recording (public `https` URL), or the script text. For a script, also the voice and language.
- **Length:** the audio length sets the video length on the avatar models. Keep a first test under 10 s.
- **Format:** resolution and aspect ratio.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `image-to-video` | `omnihuman-1-5` | default | Portrait plus speech audio |
| `image-to-video` | `veed-fabric-1-0` | alternative | Portrait plus speech, alternative (not live-tested) |
| `image-to-video` | `p-video-avatar` | alternative | Low-cost portrait plus speech |
| `image-to-video` | `veo3.1-fast` | alternative | Portrait plus a short quoted line, no audio file |
| `tts` | `grok-tts` | default | Script to speech audio |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **OmniHuman 1.5 (Path A):** a portrait plus speech audio. The default avatar model.
- **Fabric 1.0 (Path A):** a portrait plus speech, as an alternative.
- **P-Video Avatar (Path A):** a low-cost portrait plus speech.
- **Veo 3.1 Fast (Path B):** a portrait plus a short quoted line, with no audio file. Audio is always on. 4, 6, or 8 s.
- **Grok TTS:** turns the script into speech audio for Path A.

The avatar models price per second of output, and the output follows the audio length. Check `GET /v1/models/{model}/pricing` for the resolution you send.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

### Path A: speech audio drives an avatar model

1. **Get the audio.** If the user has a recording, use its public `https` URL. If the user has a script, make speech:

   ```bash
   python ../tokenlab-run/scripts/tokenlab_run.py run /v1/audio/speech --json '{"model": "MODEL_ID", "input": "Hi, I am Mia. This mug keeps my coffee hot all morning.", "voice": "VOICE", "response_format": "mp3"}' --out line.mp3
   ```

   Take the TTS `MODEL_ID` from the Models list above (operation `tts`) and a voice that model lists (for example `eve` on Grok TTS).

   TTS returns audio bytes, not a URL. Put the file on storage the user controls with a public `https` URL that stays valid until the task starts (for example a public bucket or CDN path). A `data:` URL does not work for speech: `audio_url` is capped at 8192 characters, which holds well under one second of audio. `POST /v1/files` is not a general audio host.
2. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation image-to-video`. Send only listed fields.
3. Estimate: per-second price × audio seconds (`ffprobe line.mp3`). Add the TTS cost (price per character × script length). Tell the user.
4. Build the body and call:

   ```json
   {"model": "MODEL_ID", "operation": "image-to-video", "image_url": "https://...portrait.jpg", "audio_url": "https://...line.mp3", "prompt": "She speaks to the camera with natural head movement and a friendly expression.", "resolution": "720p"}
   ```

   Take an avatar `MODEL_ID` (one that takes `audio_url`) from the Models list above for `image-to-video`. Send `resolution` only when its contract lists it.

   `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @body.json --wait`. Save the task ID. Poll every 5-10 s.

### Path B: the video model speaks the line

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation image-to-video`, with the Veo 3.1 Fast model from the Models list.
2. Estimate: per-second price (audio is always on) × `duration`. Tell the user.
3. Put the line in quotes inside the prompt. Keep it short enough to say in the clip length (about 2-3 words per second):

   ```json
   {"model": "MODEL_ID", "operation": "image-to-video", "image_url": "https://...portrait.jpg", "prompt": "Close-up portrait, eye level, static camera. She looks into the lens, smiles, and says: \"Hi, I'm Mia. This mug keeps my coffee hot all morning.\" Quiet room tone, no music.", "duration": 4, "resolution": "720p", "aspect_ratio": "9:16"}
   ```

   Use the Veo 3.1 Fast `MODEL_ID` from the Models list above (`image-to-video`).

4. Call and wait as above.

### Both paths

- If a wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a duplicate task.
- Check the lips against the words. To check Path B without listening, transcribe the result's audio with `tokenlab-transcribe-and-subtitle` and compare the text with the script.
- Return the video URL, the model, the task ID, and the estimate.

## Technique

- **The portrait decides the result.** One face, front-facing or slightly turned, eyes open, mouth closed, no hands or hair over the mouth, even light.
- **Clean audio.** One speaker, no music bed, no long silences at the start or end. Trim silence first; you pay for every second.
- **Prompt the body, not the words** (Path A). The audio sets the lips. Use the prompt for expression and gestures: "calm, warm expression, small hand gestures, slight head nods".
- **Quote the exact words** (Path B). Google's Veo guide says to put speech in quotes. Describe the sound around it ("quiet room tone, no music") so music does not cover the voice.
- **Short lines per clip.** Split a long script into lines of one or two sentences. Make one clip per line and cut them together.
- **Consent.** Use only portraits and voices the user has the right to use. Do not imitate a real person without their permission.

## Quality bar

- Lip motion matches the words; the voice and mouth stay in sync to the end.
- The face keeps its identity; teeth, eyes, and hair stay stable.
- The video length matches the audio (Path A) or the requested duration (Path B).
- The script is spoken exactly (check with a transcript), and the user saw the estimate first.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-voiceover`: choose a TTS model and voice for the script.
- `tokenlab-transcribe-and-subtitle`: check the spoken words and add subtitles.
- `tokenlab-animate-image`: a portrait that moves without speech.
- `tokenlab-character-consistency`: make the presenter portrait first.
