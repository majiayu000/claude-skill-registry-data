---

name: video-edit

description: |

  Edit any video into a captioned showcase — transcribe (any language, defaults to large-v3), present a transcript_review.txt for user approval BEFORE rendering, then build a HyperFrames composition with liquid-glass caption pills, liquid blob background, liquid morph wipes, and optional behind-subject text. Use when editing, captioning, or adding subtitles to video files. Supports English, Hebrew, and any Whisper-supported language. Renders both 16:9 and 9:16 from the SAME 16:9 source — vertical mode uses a centered footage strip with a blurred backdrop + liquid blobs and a vertical-tuned caption pill. THE PIPELINE PAUSES FOR USER APPROVAL on the transcript before final render. Pairs with hyperframes, hyperframes-cli, hyperframes-registry, and yuv-design-system skills.



---



# Video Edit — Captioned Showcase Pipeline



End-to-end captioned video editor on top of HyperFrames. The user gives you a video; you orchestrate transcribe → review → render and ALWAYS pause for transcript approval before the long render.



## Where this skill sits in the YUV.AI pyramid



`video-edit` is in the **middle tier** of the YUV.AI skills pyramid alongside `yuv-design-system`, `yuv-decks`, `yuv-viral-video`, `parallax-landing-page`, and `video-to-landing-page`. The top-tier orchestrator `yuv-pilot` routes here whenever the user wants a captioned showcase, tutorial, or talking-head edit with subtitles.



This is the more general video sibling to `yuv-viral-video`. The split:

- `yuv-viral-video` — opinionated YUV.AI viral-short pipeline (MrBeast pacing, signature editorial style)

- `video-edit` — general captioned editor with transcript-review-before-render (Hebrew + English + any Whisper language)



For YUV.AI-branded captioned video, pair this skill with `yuv-design-system` (Neon mode for type/palette decisions). For generic / third-party captioned video, this skill works standalone.



## When to invoke



- A path to a video file (mp4/mov/mkv) + a request to "edit", "caption", "add subtitles", "make a reel/promo", "do the same"

- "Fix the captions / Hebrew misspells" — re-enter at the review step on an existing project

- Any captioned tutorial / talking-head / promo build



## Save location



**Default:** `~/Documents/yuv-projects/videos/<slug>/` — always save captioned video projects here so renders are findable. The `<slug>` is short, derived from the topic or source filename.



```bash

mkdir -p ~/Documents/yuv-projects/videos

cd ~/Documents/yuv-projects/videos

# Initialize the project here.

```



Final render lands at `~/Documents/yuv-projects/videos/<slug>/renders/<name>_FINAL.mp4`. Tell the user where the video lives at the end of the render.



---



## Workflow (12 steps)



1. **Probe the source** — `ffprobe` for dimensions, fps, duration, audio.

2. **Scaffold** — `cd ~/Documents/yuv-projects/videos && npx hyperframes init <slug> --video <path> --non-interactive`. Rename the copied video to `source.mp4`.

3. **Extract audio** — `ffmpeg -i source.mp4 -vn -ac 1 -ar 16000 audio.wav`.

4. **Transcribe** — copy `references/transcribe.py` into the project. Default model `large-v3` (best Hebrew). CUDA usually fails on Windows (missing cuDNN); the script falls back to CPU int8. Force `language="he"` for Hebrew, `language="en"` for English; otherwise auto-detect.

5. **Apply known corrections** — copy `references/corrections-hebrew.md` content into a `corrections.json` at the project root (keys = wrong token, values = correct token).

6. 🛑 **STOP — start the review server and let the user approve in a webapp.**

   First apply known corrections: copy `references/make_review.py` into the project and run

   `python make_review.py`. It applies `corrections.json` to `transcript.json`.



   Then spawn the review server **as a background task** (it blocks until the user clicks

   "Approve & Render" in the browser):

   ```bash

   python "$HOME/.claude/skills/video-edit/references/serve_review.py" .

   # On Windows: python "C:\Users\<you>\.claude\skills\video-edit\references\serve_review.py" .

   ```

   The server prints a line like `REVIEW_URL=http://localhost:PORT/`. Grab that URL from

   the background-task output (or read stdout) and send the user:



   > 👉 Review your transcript here: **http://localhost:PORT/**

   > When you click **Approve & Render**, I'll continue automatically.



   The agent **does not need a "continue" message** — when the user clicks the button, the

   server writes `transcript_review.txt` to the project dir AND exits with code 0. The

   agent's background-task notification fires, and the pipeline resumes from step 8.



   **Fallback if no browser / no server**: open the editor as a static file

   (`start "" "$HOME/.claude/skills/video-edit/transcript-editor/index.html"`),

   ask the user to pick the project folder, edit, save `transcript_review.txt` back into

   the project, and reply "continue". The editor supports both modes.



7. **(Optional) Background removal** — see step 7 below; can run in parallel with the user's

   review.



8. After approval, run `python references/apply_review.py`. It re-tokenises edited lines and

   redistributes word timings back into `transcript.json` so caption sync still works.

7. **(Optional) Background removal** — if any talking-head segment needs behind-subject text, extract the segment as `outro.mp4` (or `intro.mp4`) and run `npx hyperframes remove-background <clip>.mp4 -o <name>_subject.webm --quality best`. CPU only on most setups (~3–8 min for a ~15s 1440p clip).

8. **Re-encode source with dense keyframes** — multi-worker render seeks freeze on sparse keyframes. Always run:

   ```bash

   ffmpeg -y -i source.mp4 -c:v libx264 -preset medium -crf 18 -r 30 -g 30 -keyint_min 30 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -c:a copy footage.mp4

   ```

9. **Re-load the (edited) transcript** and generate the body sub-composition via `references/gen_body.py`. The generator emits the full `compositions/components/caption-body.html` with editorial + matrix alternating in liquid-glass pills, anchored lower-left-of-centre (clears bottom-right webcam PiPs).

10. **Wire the host `index.html`** from `references/host-template.html`. Layer order (z-index, NOT track-index):

    - z0: footage `.cam-bg`

    - z1: liquid blob background (`compositions/liquid-blobs.html`, `mix-blend-mode: screen`, full duration)

    - z2: parallax behind-subject caption (intro and/or outro, when bg-removal used)

    - z3: subject cut-out `.cam-out` / `.cam-sub` (with matching `data-media-start`)

    - z6: body captions

    - z46: progress bar + flash + liquid morph wipe

11. **Lint** — `npx hyperframes lint`. Must be 0 errors. Common fixes: GSAP/CSS transform conflict on the wipe element (use `xPercent/yPercent` or remove the CSS transform); overlapping tweens on the same property (add `overwrite: "auto"`).

12. **Render** — `npx hyperframes render --quality standard --fps 30 --output renders/<name>_FINAL.mp4`. Standard is the right delivery target — `high` roughly doubles render time. Verify with 6–8 spot-check frames from across the timeline before reporting done.



### Vertical (9:16) output for TikTok / Reels / Shorts



When the user asks for vertical / portrait / TikTok / Reels / 9:16 output (from a 16:9 source):



1. Clone the project to a sibling folder: `cp -r project/ project-vertical/`.

2. Replace its `index.html` with `references/host-template-vertical.html` (1080×1920 canvas, blurred-bg backdrop with liquid blobs, the 16:9 footage as a centered horizontal strip, captions below).

3. Replace its `gen_body.py` with `references/gen_body_vertical.py` (centered pill, larger fonts, narrower max-width), then re-run it to emit `compositions/components/caption-body.html`.

4. Drop the behind-subject cut-out + parallax sub-compositions (the cutout is aligned for 16:9; not worth re-aligning for v1). The vertical comp uses the blurred-source backdrop + blobs for atmosphere instead.

5. Update `data-duration` to the actual video duration. Update the brand-chip text in `index.html` (`YUV.AI` by default).

6. Lint + render — same commands. Output is `1080×1920`. Drop straight onto TikTok / IG Reels / YT Shorts.



To deliver **both** 16:9 and 9:16 in one go, run two render commands (in parallel projects). The transcript_review.txt approval applies to both — same captions, two compositions.



## Critical rules



- **Never render the final without explicit transcript approval.** The review step is the whole point.

- For Hebrew: `large-v3` + `language="he"` + `direction: rtl` + Rubik (700 + 900 for editorial dual-weight emphasis).

- Caption pills always need an opaque dark backing — bare light text vanishes on white app UI.

- Centre caption pills horizontally but shift the centre x-coord left (e.g. `left: 720px`) when the footage has a bottom-right webcam PiP.

- The behind-subject cut-out clip MUST carry `data-media-start` matching its `data-start` (or matching the offset from the source if the clip was extracted), or the cut-out plays from frame 0 and desyncs.

- The `remove-background` webm keeps the original RGB and writes only the alpha mask — `ffprobe` reports `yuv420p`, which looks like "no alpha". Confirm via `TAG:ALPHA_MODE=1` or composite over a solid colour.

- Outro/end cards with burned-in text — do NOT caption over them; they collide.



## File references



| File | Purpose |

| --- | --- |

| `transcript-editor/index.html` | **Interactive browser editor** — video preview, RTL editing, dictionary apply, optional WebLLM AI suggestions, saves `transcript_review.txt` |

| `references/setup.md` | Prerequisites + install commands for Node / Python / FFmpeg / faster-whisper |

| `references/transcribe.py` | faster-whisper transcribe with CPU fallback + word timestamps |

| `references/serve_review.py` | **Local review server** — auto-loads editor, blocks until user clicks Approve & Render, then writes `transcript_review.txt` and exits (signals the agent) |

| `references/make_review.py` | Apply corrections + emit `transcript_review.txt` (file-mode fallback) |

| `references/apply_review.py` | Parse edited review file, redistribute word timings, update `transcript.json` |

| `references/gen_body.py` | Caption-body generator (editorial + matrix in liquid-glass pills) |

| `references/host-template.html` | **16:9** host composition with liquid effects + transition wipe |

| `references/host-template-vertical.html` | **9:16** host (1080×1920) — TikTok / Reels / Shorts layout: blurred bg, centered 16:9 footage strip, captions below, brand chip top-right |

| `references/gen_body_vertical.py` | Caption-body generator tuned for vertical (centered pill, larger fonts, narrower max-width) |

| `references/liquid-blobs.html` | Full-duration drifting blob layer |

| `references/caption-parallax-outro.html` | Behind-subject caption template (English; clone for other languages) |

| `references/palettes-neon.md` | YUV.AI Neon styling details |

| `references/lessons-learned.md` | Hardened design and layout patterns |

| `references/corrections-hebrew.md` | Known Hebrew Whisper mishears |

| `references/transcript-review-workflow.md` | The pause/approve step in detail |



## References & Loading Triggers



**MANDATORY - LOADING TRIGGERS**:

- Before starting the CUDA transcription CPU fallbacks in Step 4, you **MUST** read `references/setup.md` fully.

- Before wiring the layout transition layers in Step 10, you **MUST** read `references/host-template.html` and `references/host-template-vertical.html`.

- **Do NOT load** design patterns or lessons learned files during the initial ffmpeg probes and scaffolds.



### Background Task Termination & Disk Space Constraints

1. **Dangling process cleanup**: If the user cancels the session early or requests a rollback, immediately terminate any background `serve_review.py` processes.

2. **Disk volume validation**: Re-encoding raw clips and creating vertical folder clones can consume multiple gigabytes of disk space. Check available disk storage before copying projects.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
