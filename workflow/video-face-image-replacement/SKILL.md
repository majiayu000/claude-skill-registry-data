---
name: video-face-image-replacement
description: Use when replacing or covering one or more detected video faces with supplied or generated image assets, including single-avatar overlays and multi-person animal masks such as panda, red panda, horse, cow, and giraffe, using accurate detection, identity tracking, background removal, alpha compositing, and ffmpeg audio-preserving output.
triggers:
  - replace face in video
  - cover face with image
  - panda face video
  - multi person animal masks
  - different animal per person
  - panda red panda horse cow giraffe
  - identity animal mapping
  - face identity tracking video
  - keyframe rgb mask propagation
  - aginti mask grid
  - feature matching identity propagation
  - face overlay video
  - face mask compositing
  - swap face with avatar
  - remove image background for overlay
  - InsightFace SCRFD face detection
---

# Video Face Image Replacement

Use this skill when video faces should be fully covered or replaced with supplied or generated image assets. This is the right workflow for non-human masks such as panda, red panda, horse, cow, giraffe, cat, robot, or avatar heads. Human identity swap models are a different workflow and should only be used with consent.

For multi-person animal masking, see `references/multi-person-animal-masks.md` for the deeper tracking design, source links, and MVP plan.

## Core Rules

- Use one source image when the user asks for one generated/reused asset. Do not call image generation again unless explicitly requested.
- For multiple visible people, assign stable distinct animals by identity. Default order: `panda`, `red_panda`, `horse`, `cow`, `giraffe`; if more than five people appear, repeat with visible variants such as scarf/color/style.
- Prefer image-overlay replacement for non-human faces. Human face-swap models such as `inswapper_128`, Roop, or FaceFusion assume human-to-human identity transfer and are usually wrong for a panda/avatar mask.
- Preserve the original video and audio. Write a new output file; never overwrite the source.
- Remove green, white, or other simple generated backgrounds locally and composite with alpha. Key only the background connected to the image border; do not globally remove all white pixels, because that can punch holes through a panda/animal/avatar face.
- Use accurate face detection first, then tracking or detection reuse for speed. For multiple people, persist identity-to-animal assignments in `identity_map.json` and reuse that file for rerenders and section clips.
- For difficult multi-person videos, use keyframe RGB identity masks as a bootstrap: color each person consistently on selected keyframes, parse the masks, then propagate IDs with video object segmentation, optical flow, feature matching, face embeddings, or person tracking.
- Use user-provided or source-provided girl/boy labels only as style direction. If no label is provided, default to neutral styling or store automatic analysis only as a private `style_hint` with confidence; do not publish it as a factual gender claim.
- Validate with sample frames before processing the full video. For multiple people, create a contact sheet showing representative crops, `track_id`, animal, and style before the final render.
- For private videos, keep raw source media uncommitted and publish only intentional derived clips.

## Detection Choice

Use the best available detector in this order:

- **InsightFace/SCRFD**: strong default for accurate face boxes, landmarks, and embeddings in local Python pipelines.
- **RetinaFace**: accurate alternative when already installed or when landmark quality matters.
- **MediaPipe Face Detector/BlazeFace**: fast, lightweight, good for real-time or mobile-like workflows.
- **OpenCV Haar cascades**: emergency fallback only; fast but less reliable.

For full replacement, enlarge the detected face box enough to cover hairline, ears, chin, and motion jitter. Start with `scale=1.8-2.2` around the face box and tune from sample frames. If the user asks for "2x bigger" after a `scale=2.0` result, use `scale=4.0` and save it as a new output variant.

For multiple people, match detections to tracks by combining face-embedding cosine similarity, bounding-box IoU, and center-distance motion. Keep lost tracks alive for short occlusions. Add ByteTrack or DeepSORT only if face-only tracking shows identity switches in validation.

If the user proposes AgInTi-generated keyframe masks, use that as an annotation/bootstrap layer, not as a per-frame renderer. The local `aginti image` CLI may only expose text-to-image generation; for masks from actual frames, use an image-edit/chat surface that can see the uploaded keyframe grid, then validate the returned mask mechanically.

## Workflow

1. Copy or reference the video:

```bash
mkdir -p video artifacts/face_replace/{assets,frames,output}
cp -n "/path/to/source.mp4" "video/source.mp4"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height,r_frame_rate -of json "video/source.mp4"
```

2. Prepare the replacement image:

- If generated, request a centered mask on a flat chroma-key background.
- If supplied, inspect it first.
- Remove a flat green or white background locally into `replacement_alpha.png`.
- Use edge-connected background removal: detect the likely background color from border pixels, flood-fill or connected-component the keyed border region, and make only that border-connected region transparent. This preserves interior white/light subject regions such as a panda's face.

Example asset preparation command when the local script supports it:

```bash
python face_overlay.py prepare-asset \
  --input artifacts/face_replace/assets/replacement_generated.png \
  --output artifacts/face_replace/assets/replacement_alpha.png
```

3. Extract representative frames and run detection:

```bash
ffmpeg -y -ss 00:00:03 -i video/source.mp4 -frames:v 1 artifacts/face_replace/frames/frame_0003.jpg
ffmpeg -y -ss 00:02:00 -i video/source.mp4 -frames:v 1 artifacts/face_replace/frames/frame_0120.jpg
```

Use InsightFace/SCRFD or another available detector to confirm face count, box coordinates, and confidence on these frames.

4. Render a short sample before the full run:

```bash
python face_overlay.py process \
  --input video/source.mp4 \
  --replacement artifacts/face_replace/assets/replacement_alpha.png \
  --output artifacts/face_replace/output/sample.mp4 \
  --det-size 320 \
  --detect-every 5 \
  --scale 2.0 \
  --limit-frames 150
```

5. Inspect sample frames:

```bash
ffmpeg -y -ss 00:00:03 -i artifacts/face_replace/output/sample.mp4 -frames:v 1 artifacts/face_replace/output/sample_check.jpg
```

Check that the original face is fully covered, the overlay is not too small, and it does not drift off the head.

6. Render the full output:

```bash
python face_overlay.py process \
  --input video/source.mp4 \
  --replacement artifacts/face_replace/assets/replacement_alpha.png \
  --output artifacts/face_replace/output/source_replaced.mp4 \
  --det-size 320 \
  --detect-every 5 \
  --scale 2.0
```

Mux original audio back with `ffmpeg` if the processing script does not preserve it.

For a larger variant, never overwrite the first output:

```bash
python face_overlay.py process \
  --input video/source.mp4 \
  --replacement artifacts/face_replace/assets/replacement_alpha.png \
  --output artifacts/face_replace/output/v2_large/source_replaced_2x.mp4 \
  --det-size 320 \
  --detect-every 5 \
  --scale 4.0
```

7. For multiple people, generate or prepare one alpha PNG per animal/style and process through an identity map:

```bash
python animal_face_overlay.py process \
  --input video/source.mp4 \
  --assets-config artifacts/animal_face_swap/assets.json \
  --identity-map artifacts/animal_face_swap/identity_map.json \
  --output artifacts/animal_face_swap/output/source_animals.mp4 \
  --det-size 320 \
  --detect-every 3 \
  --scale 2.2 \
  --track-identities \
  --write-contact-sheet artifacts/animal_face_swap/identity_review.jpg
```

`identity_map.json` should persist mappings such as:

```json
{
  "animal_order": ["panda", "red_panda", "horse", "cow", "giraffe"],
  "tracks": {
    "1": {"animal": "panda", "style": "neutral"},
    "2": {"animal": "red_panda", "style": "neutral"}
  }
}
```

For keyframe RGB mask bootstrapping, create a grid of selected frames and a layout JSON, ask AgInTi or another image-edit model for a same-size PNG mask with black background plus person colors, then split and threshold it:

```text
person_1: #ff0000 -> panda
person_2: #00ff00 -> red_panda
person_3: #0000ff -> horse
background: #000000
```

Use the colored masks to attach face detections and embeddings to stable person IDs. For intermediate frames, continue using face/head boxes for animal placement; use propagated person masks only to preserve identity through crossings, occlusion, or missed face detections.

## Practical Notes

- For a static talking-head video, detecting every 5-15 frames and reusing the most recent box is usually accurate and much faster than per-frame detection.
- For fast head movement, use a smaller `detect_every`, optical-flow tracking, or detector correction on every frame.
- If there are multiple people, process all faces by default with distinct animals. Choose a single target only when the user asks for it, using area, position, or a reference face embedding.
- For repeated rerenders, larger variants, and transcript-derived section splits, reuse the same `identity_map.json` so one person never changes animals between outputs.
- If automatic face-attribute analysis is used for styling, keep it private and reviewable. Prefer manual labels such as "left person is girl style, right person is boy style" over model inference.
- If the asset has hair/fur, chroma-key removal may leave fringing. Use despill and a slight alpha feather.
- If the subject itself contains white or background-like colors, do not use global thresholding. Use border-connected keying from the original opaque generated image, or regenerate on green screen.
- If the overlay must match head angle, generate or prepare a small view set instead of one image; one asset cannot fully match large yaw/pitch changes.

## Validation Checklist

- Source video copied or referenced without overwriting.
- Replacement asset has alpha and no visible keyed background.
- Detector finds the intended face on sample frames.
- For multiple people, contact sheet confirms no duplicate tracks, no identity switches, and correct animal/style assignments.
- Sample clip shows complete face coverage.
- Full output preserves audio and expected duration.
- Spot checks from early, middle, and late sections show the overlay remains aligned.
- Raw media and private generation metadata are not committed unless explicitly requested.
