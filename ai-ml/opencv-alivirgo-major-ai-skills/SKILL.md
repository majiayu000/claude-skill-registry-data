---
name: opencv
description: "Build OpenCV image and video processing workflows with transforms, contours, capture, and classical vision operations."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["opencv", "computer-vision", "image-processing", "python", "video", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# OpenCV Computer Vision AI Skill Guide

## Overview & Engine Architecture

OpenCV (`cv2`) provides image/video IO, geometric and photometric transforms, classical feature detectors, and drawing utilities. Images are NumPy arrays in BGR order by default. Agents track color-space conversions explicitly, keep resize/crop parameters reproducible, release video captures, and push deep-learning detection to `@pytorch` / `@huggingface-transformers` when classical methods plateau.

```
imread / VideoCapture
      -> BGR ndarray
          -> cvtColor / resize / filter / threshold
          -> contours / features / write
```

## When to use this skill

- Preprocessing images for ML models
- Classical detection (edges, contours, template match)
- Frame sampling and annotation from video

## Operational directives

1. Remember `cv2.imread` returns BGR - convert before RGB-only libraries.
2. Check for `None` after reads; fail fast on missing paths.
3. Use `cv2.IMREAD_COLOR` / unchanged flags intentionally for alpha/bit depth.
4. Release `VideoCapture` / writers in `finally` blocks.
5. Do not hardcode absolute machine-specific GUI paths in headless servers (`imshow` needs a display).

## Image preprocess example

```python
import cv2
from pathlib import Path

path = Path("samples/part.jpg")
bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
if bgr is None:
    raise FileNotFoundError(path)

rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
resized = cv2.resize(bgr, (640, 480), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)
cv2.imwrite("out/edges.png", edges)
```

## Contours sketch

```python
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
vis = resized.copy()
cv2.drawContours(vis, contours, -1, (0, 255, 0), 2)
```

## Video frame sample

```python
cap = cv2.VideoCapture("clips/line.mp4")
try:
    ok, frame = cap.read()
    if ok:
        cv2.imwrite("out/frame0.jpg", frame)
finally:
    cap.release()
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Wrong colors in matplotlib | BGR vs RGB | `cvtColor` |
| `imread` None | path/Unicode/cwd | resolve Path; check exists |
| GUI crash headless | `imshow` without display | write files; use notebooks |
| Slow loops | pure Python per pixel | vectorized NumPy/OpenCV ops |

## Best practices

- Keep calibration matrices and resize shapes with dataset versions.
- Normalize orientation via EXIF when feeding photos from phones.
- Use lossless PNG for intermediate masks; JPEG for previews.
- Combine with `@pytorch` for DNN modules (`cv2.dnn`) only when appropriate.

## Limitations

- Not a full video editing suite (see dedicated video skills when present).
- Patent/licensing constraints may affect some algorithms in deployments.
- GPU modules (`cuda`) depend on build flags and drivers.

## Related skills

- `@pytorch` / `@huggingface-transformers` - learned vision models
- `@jupyter` - interactive visualization of intermediates
- `@ffmpeg` - heavy video transcoding outside OpenCV
