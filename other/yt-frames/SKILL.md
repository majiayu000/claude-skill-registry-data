---
name: yt-frames
description: Inspect existing video frames for first-frame brightness, approximate shot cuts, motion per shot and visible face detections. Use for visual clip analysis, including narrated or silent footage.
---

Run `python frames.py video.mp4 --sample-fps 4`. This optional helper requires
OpenCV 4.x and numpy; install the optional pinned `requirements.txt` into this folder's `vendor/` directory. Core text tools
remain dependency-free. Use available visual
inspection if dependencies are unavailable; report unavailable measurements explicitly.

Read brightness, motion, cuts and face detections alongside actual representative frames.
Low brightness is not automatically bad. Motion includes camera movement and lighting.
Cuts have sampling uncertainty and can miss similar-looking transitions. Frontal face
detection can miss stylized, angled or small faces. Detection is not identity recognition.
Do not interpret no detection as proof there is no face. Transcripts describe speech only;
inspect the footage itself for narrated stories such as a Reaper episode.
