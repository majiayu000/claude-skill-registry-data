---
name: video-creator
description: Create finished local videos with Remotion, OpenFilm or HyperFrames, including animation, maps, narration and music. Automatically prepare ordinary dependencies; ask before large Qwen TTS or ACE-Step installs.
priority: P0
category: media
status: builtin-guidance
---

# Video Creator

Write the film and deliver the rendered file. Remotion 4.0.538, OpenFilm 0.2.5 and HyperFrames 0.8.193 render code on the user's computer. Read remotion-video for React scenes and Three.js cameras, hyperframes-video for HTML/SVG/GSAP motion, and openfilm-video for shot assembly. A named engine takes priority over automatic routing. Core rendering, maps and local transcription need no model API key. Device compute, storage, downloads and the calling AI's allowance still apply.

## Device and permission gates

Use an online user device with read_file, write_file and start_process, and a task folder inside its Trusted Write Locations. The requested media task authorizes preparing the ordinary dependencies below within existing device permissions. Do not ask again merely because Remotion, OpenFilm, HyperFrames, FFmpeg, Chromium, map packages/data or base Whisper are absent. Announce the source, approximate size and destination, then install and continue to the finished artifact. This does not authorize system privileges, unrelated software, cloud rendering, paid APIs, uploads or publication.

All rendering, inference, audio processing and output files stay on the selected user device. Dependency downloads contact npm, official GitHub releases and Hugging Face; never send user recordings or project assets to those services. Keep caches and tools under <workspace>/.ra-media-tools. Respect disk-space failures and OS permission prompts; do not clean unrelated user files to make room.

## Prepare and run

This package includes the pinned helper scripts/local-media.mjs.
- Arc: prepare_skill {id:"video-creator",deviceId,workspace} saves the helper and returns its directory.
- Connect: read_skill {id:"video-creator"} lists the helper SHA-256 and bytes. Read read_skill {id:"video-creator",path:"scripts/local-media.mjs",offset:0}, follow nextOffset until null, write the exact chunks on the device and check their SHA-256 against the manifest. Never reconstruct a helper from a truncated response.
- Resource-only clients can read remotearc://skills/video-creator/scripts/local-media.mjs. The skill's mere availability does not mean its engines are installed.

Use Node.js 22.2+ with npm. If absent, automatically prepare a portable official Node distribution inside .ra-media-tools/node: choose the device OS/architecture from nodejs.org/dist, verify its archive against that release's SHASUMS256.txt, extract locally and use that node/npm path for this task. Do not require a global package manager or administrator installation. If an OS prerequisite cannot be installed within existing permissions, explain the specific blocker and retain completed work.

Run, with absolute paths and quoted arguments:
    node "<helper>/scripts/local-media.mjs" ensure --workspace "<workspace>" --components openfilm
This installs only the requested engine, missing portable FFmpeg/ffprobe and Chromium; initial setup is usually hundreds of MB. For Remotion use --components remotion and read remotion-video; render with --engine remotion --entry src/index.tsx --composition <registered ID>. For HyperFrames use --components hyperframes. For a map use --components maps; it caches d3/d3-geo-projection/topojson-client and Natural Earth country geometry. For subtitles read transcribe-subtitles and use --components whisper (base model ~148 MB plus executable/build tools). Reuse the cache and package-lock on later tasks; do not reinstall everything for each job. Check the returned engine CLI paths and version. An ensure result is dependency readiness, never task completion.

OpenFilm commands must receive OPENFILM_NO_BROWSER=1 and OPENFILM_NO_UPDATE_CHECK=1. The helper does this and confines browser/download caches to the workspace. Never open Studio or preview on the user's screen merely to show progress. For direct CLI invocations, preserve the helper environment (PATH includes .ra-media-tools/bin and Node; PLAYWRIGHT_BROWSERS_PATH points to .ra-media-tools/browsers). Read the installed OpenFilm manual by running its CLI without arguments before authoring; read HyperFrames --help for exact command flags.

## Author and deliver the film

1. Infer the brief from context; use 30 s, 1920×1080 by default or 1080×1920 for Shorts/Reels. Choose language, palette and source assets. Create a new film folder within the workspace; preserve existing projects.
2. Build deterministic pages from the user's footage, photos, logo, authorized screenshots, real data or code graphics. In OpenFilm each page exposes window.film = {duration, frame(t)} and draws solely from t. No timers, random values, transitions or Date-driven animation. Put shared styles/helpers in shared.js.
3. In film.html set the viewport width/height, one section per track, upper tracks first, clips with at timestamps, static clips with #t=0,length, and audio clips only in film.html. In HyperFrames use index.html with its documented composition metadata and paused GSAP timelines; bundle fonts/scripts locally.
4. Add sound if requested. Reuse already installed native voices (macOS say or Windows speech), supplied recordings/music, or a simple local FFmpeg synth bed. Qwen/ACE installation follows the separate consent gate below. Avoid silent output when narration or music was part of the brief.
5. Render a real file:
       node "<helper>/scripts/local-media.mjs" render --workspace "<workspace>" --engine openfilm --project "<film folder>" --output "<new output>.mp4"
   HyperFrames uses --engine hyperframes. The helper installs missing ordinary tools, runs look/lint, renders, checks positive duration/video tracks, decodes the result and writes a SHA-256 artifact receipt. Run long work with start_process background:true, then inspect process_status/process_output through completion. Never treat a started process as success.
6. Inspect contact sheets/keyframes at beginning, middle and end, including title transitions and the longest text. Check legibility, clipping, collisions, blank frames, aspect ratio and audio sync. Read actual ffprobe duration/resolution/size; compare them with the brief. Check audio loudness when audio was requested. Fix observed problems and rerender to a new output.
7. Deliver the MP4 itself, its absolute local path, duration, resolution and size, together with editable project sources when useful. Keep the local file as the durable copy. create_file_resource can give a temporary download; state its expiry and regenerate on request. Upload or publish only where the user requested, using supported tools and existing permissions. Do not promise a permanent public link from a temporary bearer URL.

## Maps — local and reusable

For a finished static world map:
    node "<helper>/scripts/local-media.mjs" map --workspace "<workspace>" --output "<new map>.svg" --highlight NZL,CHN
Use ISO three-letter highlights. The helper caches Natural Earth public-domain geometry, pins its source revision and SHA-256 and writes an SVG plus artifact receipt.

For animation, copy the cached GeoJSON and local d3 distributions into the film's assets folder; load those local files in pages. Use d3.geoMercator, geoNaturalEarth1 or a suitable regional projection, and draw regions/camera motion from t. No online tile/API/CDN dependency during rendering. Country geometry is the default; fetch official Natural Earth admin-1, coastline or river datasets locally when the brief needs them, retaining source revision/hash. Do not invent province detail from country data. Check disputed boundaries and labels against the user's intended presentation.

## Voice-over, music and maps — local, no keys

**Voice-over (Qwen3-TTS, Apache-2.0).** Before installing Qwen TTS or fetching missing weights, **ask the user for explicit approval**: disclose multi-GB downloads (PyTorch plus weights), estimated expanded disk use, chosen model, destination and CPU/GPU expectations. Do not download Qwen while awaiting approval; continue independent visuals/subtitles or use an existing native voice if suitable. Requesting narration is not installation consent. An already installed compatible model or existing explicit consent within the same scope can be reused without asking again.

After approval, use a dedicated local venv and model cache under .ra-media-tools/qwen. Select PyTorch wheels for the actual device: CUDA only with supported NVIDIA hardware, MPS only where verified, CPU otherwise. Install qwen-tts and huggingface_hub with pinned versions recorded in a receipt; download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice and its tokenizer into that cache. Qwen3TTSModel.from_pretrained with the verified backend, generate_custom_voice(text, language="Chinese", speaker="Vivian"), then save the returned waveform with its actual sample rate. Check duration, intelligibility and clipping before adding it to the film. No cloud TTS fallback without authorization.

**Music bed (ACE-Step 1.5, MIT).** **Ask for explicit approval** before cloning/installing dependencies or downloading weights: disclose 10 GB+ downloads, expanded disk use, destination and hardware/runtime estimates. A generic music request does not authorize installation. Reuse an installed compatible model or existing scoped approval. While approval is pending, continue independent work or use the supplied/local synth bed if suitable.

After approval, clone https://github.com/ACE-Step/ACE-Step-1.5 at a recorded revision under .ra-media-tools/acestep, use its isolated environment and actual supported device backend, and record installed versions/model hashes. NVIDIA examples are not a promise of CPU/Intel Mac performance. If its local API is needed, start acestep-api --host 127.0.0.1 --port 8001; check that installed version's schema, submit a bounded duration, wait for completion and copy the audio into film assets. Never start a public listener. Inspect the generated audio before delivery.

**Maps & data.** Automatically prepare only the packages and datasets needed by the brief as described above. No extra installation question for ordinary local map preparation.

## Evidence of completion

Report the device, rendered file and editable project paths, verified duration/resolution/size, selected engines and remaining limitations. The helper's artifact receipt proves file/decoder checks; visual quality and speech accuracy still need review. Do not claim delivery from a plan, dependency install, sample scaffold or failed render. Paid providers, image models, Remotion licensing and publication retain their separate authorization requirements.
