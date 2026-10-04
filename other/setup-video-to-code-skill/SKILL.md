---
name: setup-video-to-code-skill
description: Sets up the video-to-code storage folder and installs required Python dependencies (opencv, whisper, numpy). Run once before first use, or to verify the environment is ready.
license: MIT
compatibility: Requires Python 3, opencv-python, numpy, and mlx-whisper (or openai-whisper). macOS recommended for Metal acceleration.
disable-model-invocation: true
metadata:
  author: Piotr Lason
  version: "1.3"
---

# Initialize video-to-code environment

Sets up the storage folder and installs all required dependencies for the video-to-code skill.

## Instructions

**Display this banner as the very first output when the skill is invoked:**

```
 ██╗   ██╗██╗██████╗ ███████╗ ██████╗
 ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
 ██║   ██║██║██║  ██║█████╗  ██║   ██║
 ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
  ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
   ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝
████████╗ ██████╗      ██████╗  ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔═══██╗    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝
   ██║   ██║   ██║    ██║      ██║   ██║██║  ██║█████╗
   ██║   ██║   ██║    ██║      ██║   ██║██║  ██║██╔══╝
   ██║   ╚██████╔╝    ╚██████╗ ╚██████╔╝██████╔╝███████╗
   ╚═╝    ╚═════╝      ╚═════╝  ╚═════╝╚═════╝ ╚══════╝
   SKILL SETUP v1.3
```

1. **Notify the user**:
   - Immediately tell them: "URL: https://github.com/PiotrLason/video-to-code-skill"
   - Immediately tell them: "Help: run `/video-to-code-skill -> show-help-video-to-code-skill` to display the full plugin `README.md` with Markdown formatting."
   - Tell them "Initializing video-to-code environment..."
   - Immediately tell them: "Documentation: open `${CLAUDE_PLUGIN_ROOT}/README.md` for setup, usage, parameters, outputs, and troubleshooting."

2. **Ensure storage folder exists**:
   ```bash
   mkdir -p ~/video-to-code-skill-storage
   ```
   - If the folder already existed, tell the user: "Storage folder already exists at ~/video-to-code-skill-storage"
   - If it was just created, tell the user: "Created storage folder at ~/video-to-code-skill-storage"

3. **Check and install dependencies**:
   - Always use `/usr/bin/python3` for checking and installing — this is the same interpreter the run skill uses.
   - Check `cv2`, `numpy`, and whisper separately. Only install missing packages.
   - For whisper: try `mlx_whisper` first (Apple Silicon accelerated), fall back to `openai-whisper` on non-Mac systems.
   ```bash
   /usr/bin/python3 -c "import cv2" 2>/dev/null || /usr/bin/python3 -m pip install --user opencv-python
   /usr/bin/python3 -c "import numpy" 2>/dev/null || /usr/bin/python3 -m pip install --user numpy
   /usr/bin/python3 -c "import mlx_whisper" 2>/dev/null || /usr/bin/python3 -c "import whisper" 2>/dev/null || /usr/bin/python3 -m pip install --user mlx-whisper || /usr/bin/python3 -m pip install --user openai-whisper
   ```

4. **Check and install ffmpeg**:
   ```bash
   which ffmpeg || brew install ffmpeg || echo "ffmpeg not found — install it manually (e.g. apt install ffmpeg on Linux)"
   ```

5. **Report status**: Summarize what was set up and whether everything is ready. Example:
   - Storage folder: ready
   - opencv-python: installed
   - numpy: installed
   - mlx-whisper or openai-whisper: installed
   - ffmpeg: installed
   - Documentation: `${CLAUDE_PLUGIN_ROOT}/README.md`
   - Help command: `/video-to-code-skill -> show-help-video-to-code-skill`
   - "Environment is ready. Place a video file (.mov, .mp4, .webm) in ~/video-to-code-skill-storage and run `/video-to-code-skill -> run-video-to-code-skill` to analyze it."

## Dependencies

| Package | Purpose |
|---------|---------|
| `opencv-python` | Frame extraction and scene change detection |
| `numpy` | Array operations |
| `mlx-whisper` | Audio transcription (Metal-accelerated, macOS) |
| `openai-whisper` | Audio transcription (fallback) |
| `ffmpeg` | Audio extraction from video files |
