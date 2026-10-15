---
name: tokenlab-prompting
description: "Write or fix prompts for the model families in the TokenLab catalog: FLUX, Nano Banana / Gemini image, GPT image, Seedream, Recraft, Qwen image, Ideogram, Seedance, Kling, Veo, Hailuo, Wan, PixVerse, Grok Imagine, Suno, MiniMax music, Stable Audio, and TTS voices. Use when the user says \"write a better prompt for FLUX\", \"how do I prompt Veo\", \"my video prompt ignores the camera move\", \"prompt for a Suno song\", \"keep the same face in an edit\", or \"how do I make the voice sound calm\". Each family has an official source, key levers, examples, and pitfalls. To pick a model, use tokenlab-model-picker. To run the call, use tokenlab-run."
license: MIT
metadata:
  category: foundation
---

# TokenLab Prompting

Prompt craft that matches the model family. Outcome skills point here for the wording. This skill does not call the API.

## How to use this skill

1. Find the family of the chosen model in the table below.
2. Open the reference file and read only that family section.
3. Read the model contract (`GET /v1/models/{model}`, or the `tokenlab-run` contract step). Use only the parameters the contract lists. A family tip does not prove that a parameter exists.
4. Write the prompt. Run it with `tokenlab-run`. Change one thing per retry.

## Universal structure

Put the most important facts first. Most models weight early words more.

1. **Subject:** who or what, with the few traits that matter.
2. **Action:** what happens. For video, one clear action per shot.
3. **Setting:** where and when.
4. **Light and camera:** light direction and quality, lens or shot size, angle, camera move.
5. **Style:** medium, era, film look, or art style. Use concrete words, not "epic" or "beautiful".
6. **Constraints:** what must stay the same, exact text in quotes, count of items, format or use ("poster", "square product tile").

Use full sentences or short clauses. Do not stack synonyms. Start short, then add only what changes the result.

## Image, video, music, and speech differ

| Medium | What the prompt must carry |
| --- | --- |
| Image | One frozen frame. Composition, light, materials, exact on-image text in quotes. |
| Image edit | What to change and what to keep. Name each input by number and role. |
| Video | Motion over time. Camera move, action order, sound cues. Text-to-video needs a full scene. Image-to-video needs only motion, camera, and a stability rule, because the image already shows the scene. |
| Music | Genre, instruments, mood, tempo, structure. Words to sing go in a lyrics field with section tags, not in the style text. |
| Speech | The script is the prompt. Punctuation, pauses, and tags set the delivery. Voice and speed are parameters. |

## Keep identity in edits

- State the keep list in every edit prompt: face, hair, skin tone, pose, product shape, label, camera angle. Repeat it on every retry.
- Change one target per edit. Say "change only X, keep everything else the same".
- With several inputs, name each one by number and role: "subject from image 1, style from image 2". Use the numbering the family section gives.
- For a character used many times, make one clean anchor image first and send it with every call.
- Do not re-describe what the input image already shows. It can fight the image and cause drift.

## Negative prompts

- Send `negative_prompt` (or `negative_tags` for Suno) only when the model contract lists it.
- Many models have no such field. Say the wanted result in positive words instead: "sharp focus throughout", "hands move naturally".
- Where the contract has the field, keep it short and concrete. Do not use it as the main control.

## Family map

| Family | Reference file | Key levers |
| --- | --- | --- |
| FLUX | `references/image-families.md` | Subject first, light, camera gear, hex colors, quoted text, image numbers |
| Nano Banana / Gemini image | `references/image-families.md` | Narrative scene, shot type, exact text, "change only X" edits |
| GPT image | `references/image-families.md` | Scene, subject, detail, constraints, use case, quality level, keep list |
| Seedream | `references/image-families.md` | Subject, action, setting in plain prose, quoted text, "Figure n" inputs |
| Recraft | `references/image-families.md` | Short for exploring, structured for control, vector rules, text hierarchy |
| Qwen image | `references/image-families.md` | Quoted text with role, place, font, designer-style layout |
| Ideogram | `references/image-families.md` | Exact text in quotes, layout, short lines |
| Seedance | `references/video-families.md` | Subject, action, scene, light, camera, constraints, timeline shots, numbered inputs |
| Kling | `references/video-families.md` | Scene direction, camera first, labeled shots, one speaker per line |
| Veo | `references/video-families.md` | Cinematography, subject, action, context, style, quoted dialogue, `SFX:` |
| Hailuo / MiniMax | `references/video-families.md` | Camera commands (older models), reference roles, plain camera words (H3) |
| Wan | `references/video-families.md` | Subject, scene, motion, aesthetic control, shot ranges, `Image n` inputs |
| PixVerse | `references/video-families.md` | 50 to 80 words, one camera move, no "cinematic" |
| Grok Imagine | `references/video-families.md` | Motion and camera over the first frame, audio cues |
| Suno | `references/audio-families.md` | Style text vs lyrics, section tags, few genres |
| MiniMax music | `references/audio-families.md` | Style, mood, scene text; lyrics tags |
| Stable Audio | `references/audio-families.md` | Genre, instruments, mood, BPM; SFX source, action, recording |
| TTS voices | `references/audio-families.md` | Script punctuation, tags, voice choice, speed |

## Rules

- Do not invent limits (prompt length, token counts, special syntax). Use the numbers in the reference files, and say when a number comes from the maker and not from the TokenLab contract.
- Ask for no real person's likeness without the user's right to it. Add no logos, claims, or text the user did not supply.
- If a family section says "no official guide found", treat its advice as general and test with one cheap call first.

## Related skills

- `tokenlab-model-picker`: choose the model before you write the prompt.
- `tokenlab-run`: run the call, poll, and fetch the result.
- Outcome skills that use this one for wording: `tokenlab-product-photography`, `tokenlab-cinematic-video`, `tokenlab-music`, `tokenlab-voiceover`.
