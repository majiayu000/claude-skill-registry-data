---
name: tokenlab-product-ad-video
description: "Make a short product ad or promo clip from a product photo or a written brief with TokenLab video models. Use when the user says \"make an ad video for this product\", \"turn my product photo into a video\", \"promo clip for the launch\", \"product reveal\", \"9:16 video for TikTok / Reels / Shorts\", or \"e-commerce video\". Usually a short pipeline: get a clean product still, animate it with a slow camera move, and add sound or a spoken line. For a still product image only, use tokenlab-product-photography. For general camera-led storytelling with no product focus, use tokenlab-cinematic-video. For a presenter who talks about the product, use tokenlab-talking-avatar."
license: MIT
metadata:
  category: video
---

# Product Ad Video

Turn a product into a short ad clip that keeps the product exact. Start from a good still, move the camera around it, and add sound. One call makes one shot; cut shots together in an editor.

## Inputs to collect

- **Product image:** a public `https` URL or a TokenLab result URL. If the user has no clean shot, make one first with `tokenlab-product-photography`. Several angles help reference-to-video models.
- **Brief:** the one thing the viewer should notice (texture, size, the lid opening, steam, a pour).
- **Format:** aspect ratio per channel (9:16 Reels/Shorts/TikTok, 1:1 or 4:5 feed, 16:9 web) and length per shot.
- **Sound:** none, ambient sound and effects, or a short spoken line.
- **Hard rules:** product shape, color, logo, and on-pack text must not change. Add no claims, prices, or badges the user did not supply.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `image-to-video` | `veo3.1-fast` | default | Animate one product still |
| `image-to-video` | `veo3.1` | alternative | Higher tier (not live-tested) |
| `image-to-video` | `kling-v3.0` | alternative | Alternative; sound on or off (not live-tested) |
| `image-to-video` | `grok-imagine-video` | alternative | Low-cost draft |
| `reference-to-video` | `seedance-2.0` | default | Keep the product from several photos |
| `reference-to-video` | `veo3.1-fast` | alternative | References, alternative (not live-tested) |
| `reference-to-video` | `grok-imagine-video` | alternative | Low-cost references |
| `text-to-video` | `veo3.1-fast` | default | Brief only, no photo |
| `text-to-video` | `seedance-2.0` | alternative | Brief only, alternative (not live-tested) |
| `text-to-video` | `grok-imagine-video` | alternative | Low-cost draft |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **One product still (`image-to-video`):** Veo 3.1 Fast is the default, with sound, 4, 6, or 8 s at 720p or 1080p. Veo 3.1 is the higher tier. Kling 3.0 is an alternative with sound on or off. Grok Imagine video makes a low-cost draft.
- **Several product photos (`reference-to-video`):** Seedance 2.0 keeps the product from several photos. Veo 3.1 Fast is an alternative; it takes 8 s only for this operation. Grok Imagine video makes low-cost reference drafts (1-10 s).
- **Brief only, no photo (`text-to-video`):** Veo 3.1 Fast, then Seedance 2.0 as an alternative. Grok Imagine video makes a low-cost draft.
- **Sound:** Veo always adds audio. For silent shots, pick a model whose contract lists `output_audio`.

All video calls use `POST /v1/videos/generations` with an explicit `operation`. Send `output_audio` only when the operation lists it.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. **Get a clean still.** Use the user's photo if it is sharp and well lit. Otherwise run `tokenlab-product-photography` first and keep its result URL as the anchor.
2. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation image-to-video` (or `reference-to-video`, `text-to-video`). Use only listed fields and values.
3. Estimate the cost: `python ../tokenlab-run/scripts/tokenlab_run.py price MODEL`, then per-second price × `duration` for each shot. Some models charge more with audio on or at a higher resolution. Use the Official price as the upper bound. Tell the user the total for all shots before you start.
4. Build one body per shot:

   ```json
   {"model": "MODEL_ID", "operation": "image-to-video", "image_url": "https://...", "prompt": "Slow push-in on the white ceramic mug on a walnut table. Soft morning light moves across the glaze. Coffee steam rises. Quiet room tone, a soft clink. The mug shape, color, and logo stay exactly the same.", "duration": 6, "resolution": "720p", "aspect_ratio": "9:16"}
   ```

   Take `MODEL_ID` from the Models list above for the shot's operation. Set `duration` and `resolution` to values its contract lists.

5. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @shot1.json --wait`. Save each task ID. Poll every 5-10 s.
6. If a wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a duplicate task.
7. Check each shot against the Quality bar. Re-run only the weak shot, after you tell the user the cost.
8. Return each video URL with its model, task ID, aspect ratio, and estimate.

## Technique

- **Restage, then animate.** Fix the product still first. A video model copies the flaws of its first frame.
- **Slow, simple camera moves sell products.** Use one move per shot: slow push-in, slow orbit, low-angle tilt up, top-down reveal. Fast moves blur labels.
- **Light is the motion.** "A light sweep moves across the glass", "sunlight shifts across the table" add life without changing the product.
- **Protect the product in words.** End the prompt with what must stay: "the bottle shape, label, and cap stay exactly as in the image."
- **One action per shot.** Pour, open, rotate, or steam. Make a second shot for the next action.
- **No generated text.** Do not ask the model to write slogans or prices on screen. Add text, logo cards, and prices in an editor.
- **Sound.** Veo models always add audio. Describe it: "soft clink of the cup, quiet morning room tone". Put a spoken line in quotes. For silent shots, pick a model that lists `output_audio` and send `false`.
- **Multi-angle consistency.** For a hero product shown from several angles, use `reference-to-video` with 2-4 clean product photos instead of separate image-to-video calls.
- **One aspect ratio per call.** Make 9:16 and 16:9 as separate calls. For image-to-video, crop the still to the target shape first, because some models follow the input image shape.

## Quality bar

- The product matches the input: shape, proportions, color, logo, and label.
- No warped text, extra parts, or floating products. Shadows follow the light.
- Each shot has one clear action and a steady camera.
- Aspect ratio and length match each channel. No invented claims, prices, or badges.
- The user saw the total estimate before the jobs, and the answer lists every shot's model and task ID.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-product-photography`: make the clean product still first.
- `tokenlab-animate-image`: generic image-to-video with no product rules.
- `tokenlab-cinematic-video`: camera language for brand mood shots.
- `tokenlab-talking-avatar`: a presenter who talks about the product.
- `tokenlab-voiceover`: a separate voice track for the edit.
