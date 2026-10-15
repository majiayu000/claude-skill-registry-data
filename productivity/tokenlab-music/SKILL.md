---
name: tokenlab-music
description: "Make songs with vocals, instrumentals, background loops, and short sound effects from a text brief with TokenLab music models. Use when the user says \"make a song about...\", \"background music for my video\", \"lo-fi loop\", \"jingle for my ad\", \"instrumental track\", \"a whoosh / door slam / rain sound effect\", or \"extend this song\". Picks a song model or a short-clip audio model, writes the brief, waits for the async task, and returns audio URLs. For spoken narration, use tokenlab-voiceover. For a transcript of existing audio, use tokenlab-transcribe-and-subtitle."
license: MIT
metadata:
  category: audio
---

# Music

Make music and sound from a brief: full songs with lyrics, instrumentals, loops for video, and short sound effects. Music generation is always async. The work is choosing between a song model and a short-clip model, and writing a brief the model can follow.

## Inputs to collect

- **What it is:** song with vocals, instrumental, loop, jingle, or sound effect.
- **Style:** genre, mood, tempo (BPM), main instruments, and vocal type if any.
- **Length:** short clip or loop (seconds), or a full song.
- **Lyrics:** user-written, or a theme for the model to write from.
- **Use:** video background, ad, game, podcast. Note anything that must be avoided (vocals, a genre, an instrument).

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `music` | `suno-music` | default | Song with vocals and lyrics, or instrumental |
| `music` | `minimax-music-2.6` | alternative | Song, alternative (not live-tested) |
| `music` | `stable-audio-3` | alternative | Instrumental with length control (not live-tested) |
| `music` | `stable-audio-3-small-music-text-to-audio` | alternative | Short loop or bed for video |
| `music` | `stable-audio-3-small-sfx-text-to-audio` | alternative | Sound effect (not live-tested) |
| `music` | `stable-audio-3-small-sfx-base-text-to-audio` | alternative | Sound effect, alternative (not live-tested) |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

How to choose:

- **Song with vocals and lyrics, or an instrumental song:** Suno. It also extends, covers, and splits existing tracks.
- **Song, alternative:** MiniMax Music.
- **Instrumental with length control:** Stable Audio 3.
- **Short loop or bed for video:** the small Stable Audio 3 music model.
- **Sound effect:** the small Stable Audio 3 SFX models.

Exact fields come from the model contract.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation music`. Read `supported_parameters` and `notes`. Each model has its own field names (`tags` vs `negative_prompt`, `full_lyrics`, `duration`). Send only listed fields.
2. Estimate with `GET /v1/models/{model}/pricing`. Music models price per request. For Suno, the price depends on the action (`music` vs stem separation); read the entry for your action. Tell the user the estimate before a batch.
3. Write the body (see Technique). Suno needs `mv` for generation; the docs list `chirp-v3-5`, `chirp-v4`, `chirp-v4-5`, `chirp-v4-5plus`, `chirp-v4-5all`, `chirp-v5`, `chirp-v5-5`.
4. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/music/generations --json @body.json --wait`. Save the task `id` and `poll_url` first. Poll every 5–10 s. On a timeout, resume with `poll TASK_ID`; do not create a second task.
5. Read the result: `audio_url` (TokenLab media URL, kept 30 days). Suno can also return `image_url` (cover art), `title`, `audio_id`, and lyrics fields. Keep `audio_id` and the task ID if the user may extend or split the track later.
6. Download the audio and check its length and that it plays. Return the `audio_url`, model, task ID, and the brief you sent.

Do not hand the user `stream_audio_url`. It is a temporary listen-while-making link, not a TokenLab media result, and it stops working.

## Technique

- **Brief order for songs:** genre and era, mood, tempo, lead instrument, vocal type, structure. Example `tags`: "indie folk, acoustic guitar, warm female vocal, gentle". Put the story or theme in `prompt`.
- **Say what to avoid** in the field the model has: `negative_tags` on Suno, `negative_prompt` on MiniMax Music and the small Stable Audio models.
- **Instrumental:** on Suno set `make_instrumental: true` instead of writing "no vocals" in the prompt.
- **Your own lyrics:** use `full_lyrics` where the contract lists it. Mark sections on their own lines, such as `[Verse]` and `[Chorus]`, and keep lines short and singable.
- **Clips and loops:** describe sound, not story. Genre, instruments, BPM, mood, texture: "warm lo-fi hip hop loop, mellow Rhodes chords, soft vinyl crackle, relaxed boom-bap drums, 80 BPM, instrumental". Set `duration` in seconds.
- **Sound effects:** one event per request, with the source, action, and space: "heavy wooden door slams shut in a stone hallway, short echo". Use a short `duration`.
- **Iterate on one variable.** Keep the brief and change only tempo or one instrument per retry. Every retry is a new paid task.
- No artist names or copyrighted lyrics in the brief. Describe the style instead.

See `references/suno.md` for Suno extend, cover, and stem operations.

## Quality bar

- Genre, mood, tempo, and vocal choice match the brief.
- Length fits the use; loops have no hard cut at the end when the user needs a loop.
- No vocals in an instrumental; lyrics are the user's lyrics when given.
- The final answer has the `audio_url`, model, task ID, and the estimate the user saw.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-voiceover`: spoken narration over the music.
- `tokenlab-product-ad-video`: the video the music goes under.
- `tokenlab-prompting`: prompt craft per model family.
