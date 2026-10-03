---
name: "gemini"
description: "Google Gemini media generation: Nano Banana images, Imagen 4 images, Veo video, TTS, model listing. Trigger phrases: gemini image, nano banana, imagen, veo video, google veo, gemini tts."
metadata: { "includeInPrompt": true }
tagline: "Google Gemini media generation: Nano Banana images, Imagen 4 images, Veo video, TTS, model listing."
catalog_auth: "API key via the secure credential flow"
catalog_hosts: ["generativelanguage.googleapis.com"]
---

# Gemini (media generation)

## Purpose
Generate images (Nano Banana, Imagen 4), video (Veo 3.1), and speech (TTS) through Google's Gemini API with one key and one bill. Use when Michael asks for AI-generated images, video clips, thumbnails, or voiceovers via Google.

## Tooling
All commands go through `bin/gemini.py`:

```bash
bin/gemini.py auth                                                        # verify the API key (free)
bin/gemini.py models --limit 50                                           # list available models
bin/gemini.py image --prompt "a ceramic fox" --out /tmp/fox               # Nano Banana text-to-image (or edit with --image)
bin/gemini.py image --prompt "make it night" --image ./fox.png --out /tmp/fox-night
bin/gemini.py imagen --prompt "studio product shot" --count 2 --out /tmp/prod   # Imagen 4
bin/gemini.py video --prompt "a drone shot over a harbor"                 # Veo 3.1, prints an operation id
bin/gemini.py op-status --op operations/abc123                            # poll the Veo operation
bin/gemini.py tts --text "Hello there" --voice Kore --out /tmp/line       # text-to-speech
```

`image` and `imagen` save files to the `--out` prefix and are synchronous. `video` is async: it returns an operation id, poll `op-status` until `done` is true, then download the video file (files.download). `--json` merges extra fields into any request.

## Auth
- Provider id: `gemini` (credential is collected as `custom.gemini`)
- Collection: API key via the secure credential flow (`credentials.request_api_access`); created in Google AI Studio (aistudio.google.com/apikey)
- Allowed hosts: `generativelanguage.googleapis.com`
- Status check: `bin/gemini.py auth` (must return `"ok": true`). The key is sent verbatim as the `x-goog-api-key` header.

## Operating Rules
1. COST WARNING: all media generation requires a BILLING-ENABLED Google Cloud project. Free-tier media quota is 0, so calls without billing fail. This is the number one integration pitfall.
2. Every generation spends real money: Veo 3 ~$0.40/sec, Veo 3.1 Fast ~$0.10/sec, Veo 3.1 Lite ~$0.05/sec, Imagen 4 ~$0.02-0.06/image, Nano Banana ~$0.02-0.04/image. Confirm with Michael before every generation, stating the model and expected cost.
3. Veo renders take minutes. Poll `op-status` with backoff; do not hammer it.
4. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/gemini.py`). Do not print, log, or transmit the key value.

## Files
- SKILL.md
- bin/gemini.py

## Maturity
🧪 Draft: written from Google's public Gemini API docs via the research dossier; not yet live-tested end-to-end.
