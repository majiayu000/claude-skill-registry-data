---
name: run-video-to-code-skill
description: Analyzes video feedback by extracting key frames and audio transcription. Use when the user mentions video feedback, screen recordings, user recordings, or wants to analyze a video file from ~/video-to-code-skill-storage folder.
license: MIT
compatibility: Requires Python 3, opencv-python, numpy, and mlx-whisper (or openai-whisper). macOS recommended for Metal acceleration.
disable-model-invocation: true
metadata:
  author: Piotr Lason
  version: "1.3"
---

# Your video recording will be added as a multimodal data bundle to the context window and tokenised as a part of your prompt

Analyze video feedback from `~/video-to-code-skill-storage` folder by extracting key frames and generating audio transcription.

## When to Use

This skill runs only when explicitly invoked by the user.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-vd`, `-visual_details` | Visual detail level (1-10). 1 = 10% — fewest keyframes, 10 = 100% — most keyframes captured. | `10` |
| `-sd`, `-summary_details` | Detail level for the "Detailed Walkthrough" section in `summary.md` (1-10). 1 = brief overview, 10 = exhaustive long-form. | `5` |
| `YYYY-MM-DD_HH-MM-SS` | Timestamp of an archived video to load directly from the archive. | — |

Examples:
- `/video-to-code-skill -> run-video-to-code-skill -vd 8`
- `/video-to-code-skill -> run-video-to-code-skill -sd 8`
- `/video-to-code-skill -> run-video-to-code-skill 2026-03-19_10-12-51`

### Strict parameter parsing rules

**Arguments come ONLY from the `<command-message>` tag** in the conversation. The `<command-message>` tag contains the exact text the user typed after the slash command name. Parse parameters exclusively from that string.

- If `<command-message>` is just `run` (no extra text), there are **zero** parameters.
- If `<command-message>` is `run -vd 8`, the visual detail level is `8`.
- If `<command-message>` is `run -sd 8`, the summary detail level is `8`.
- If `<command-message>` is `run -vd 8 -sd 3`, both parameters are set.
- If `<command-message>` is `run 2026-03-19_10-12-51`, the timestamp is `2026-03-19_10-12-51`.

**Everything else is NOT a parameter** — including IDE context, additional working directories, open file paths, environment metadata.

## Instructions

Important: You can only modify files in `~/video-to-code-skill-storage` folder. If other files are to be modified outside of this folder, always ask the user for permission.

**Display this ASCII art banner as the very first output when the skill is invoked:**

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
   SKILL RUN v1.3
```

`-vd <1-10>` visual detail — 1 = fewest keyframes, 10 = most (default: 10) · `-sd <1-10>` summary detail — 1 = brief, 10 = exhaustive (default: 5)

1. **Notify the user**:
   - Immediately tell them: "URL: https://github.com/PiotrLason/video-to-code-skill"
   - Immediately tell them: "Help: run `/video-to-code-skill -> show-help-video-to-code-skill` to display the full plugin `README.md` with Markdown formatting."
   - Tell them "Analyzing user feedback video from ~/video-to-code-skill-storage - extracting key frames and narration transcript..."
   - Immediately tell them: "Documentation: open `${CLAUDE_PLUGIN_ROOT}/README.md` for setup, usage, parameters, outputs, and troubleshooting."

2. **If a timestamp argument is provided** (matches `YYYY-MM-DD_HH-MM-SS` and follows "Strict parameter parsing rules"), look for a matching archive folder:
   ```bash
   ls -d ~/video-to-code-skill-storage/archive/<timestamp>*/ 2>/dev/null | head -1
   ```
   - If no matching folder is found, tell the user: **"No archived video found for timestamp `<timestamp>`"** and skip to step 3.
   - Tell the user which archived video is being loaded (show the archive folder name).
   - If a matching folder exists, read its `analysis/*/analysis.json` and keyframe images, as well as `summary.md` and `narration.md` (if present) — skip to step 8.

3. **Sanitize filenames** — replace invisible Unicode whitespace variants (e.g. macOS narrow no-break space `U+202F` before AM/PM) with regular spaces:
   ```bash
   python3 -c "
   import os, re, glob
   for f in glob.glob(os.path.expanduser('~/video-to-code-skill-storage/*')):
       fixed = re.sub(r'[\u00a0\u202f\u2007\u2009\u200b]', ' ', f)
       if fixed != f: os.rename(f, fixed)
   "
   ```

4. **Find the latest video file** (by modification time):
   ```bash
   find ~/video-to-code-skill-storage -maxdepth 1 -type f \( -name "*.mov" -o -name "*.mp4" -o -name "*.webm" \) -exec ls -t {} + | head -1
   ```
   - **If a video file IS found** → proceed to step 6 (run the analysis script). Do NOT fall back to archive.
   - **If NO video file is found** → go to step 5 (archive fallback).

5. **Archive fallback** (ONLY if step 4 found no video file). Load the most recent archived video:
   ```bash
   ls -dt ~/video-to-code-skill-storage/archive/*/ 2>/dev/null | head -1
   ```
   - If an archived folder exists, read its `analysis/*/analysis.json` and keyframe images, as well as `summary.md` and `narration.md` (if present) — skip to step 8.
   - Tell the user which archived video is being loaded (show the archive folder name).
   - If no archived analysis exists either, tell the user: **"No current or archived videos to input into the context"** and stop.

6. **Run the analysis script** (use the `-vd` or `-visual_details` parameter value if provided, otherwise default to `10`). Prefer `/usr/bin/python3` if available:
   ```bash
   /usr/bin/python3 "${CLAUDE_PLUGIN_ROOT}/scripts/video-to-code-skill-processor.py" <video_path> -o ~/video-to-code-skill-storage/analysis/<video_name> -vd <visual_detail>
   ```

7. **Read the results**:
   - Read `~/video-to-code-skill-storage/analysis/<video_name>/analysis.json`
   - Read each keyframe image listed in the analysis
   - Count how many keyframe images were created or found
   - Determine the size in KB of `summary.md` and, if present, `narration.md`

8. **Summarize** what the user is demonstrating or reporting — write a detailed content summary describing what is shown and said in the video with as much detail as possible. Present this summary to the user.

9. **Archive** the analyzed video (skip if using archived analysis from step 2 or 5):
   - Create timestamp folder: `~/video-to-code-skill-storage/archive/YYYY-MM-DD_HH-MM-SS_<video_filename>/` where `YYYY-MM-DD_HH-MM-SS` is the **current date/time when the analysis is performed** (NOT the video file's creation or modification time), and `<video_filename>` is the original video filename without extension; separate the timestamp and filename with a space where the OS allows (e.g. `2026-03-18_12-45-00 login flow dropdown bug/`), falling back to an underscore otherwise
   - Move video file and analysis folder to archive
   - Save the detailed video analysis summary as `summary.md` in the archive folder, using this structure:
     - Start with a short, high-level overview (up to 10 paragraphs) of what the video covers, grouped by chapters and topics using bullet lists when needed and short paragraphs.
     - Add a **"Key Moments"** section that contains a Markdown table with at least these columns: `Timestamp`, `What's happening`. Each important event from the video should have its own row.
     - Add **Questions, Requests and Issues** mentioned in the recording
     - Include the **total analysis processing time** (sum of keyframe extraction and transcription) in a clearly labeled line, formatted as `HH:MM:SS` (hours:minutes:seconds), e.g. `Total analysis time: 00:07:35`.
     - End with a final section (for example **"Detailed Walkthrough"**). The length and depth of this section is controlled by the `-sd` parameter (default: 5). Treat the value as a percentage scale: `-sd 1` means 10% of maximum detail (a short paragraph or two), `-sd 5` means 50% (a balanced walkthrough covering key points), `-sd 10` means 100% (an exhaustive long-form essay for a detail-oriented, technically savvy reader, covering every flow, context, and reasoning step).
   - If the video contains human narration/speech, save it as `narration.md` in the archive folder in screenplay-ready format with matching timestamp ranges. Each timestamp block must contain multiple sentences — combine short consecutive transcript segments into longer blocks rather than having one sentence per timestamp. Example:
     ```
     # Narration Transcript

     **[00:00 – 00:12]**
     So here I'm opening the settings panel and you can see the bug right away. The sidebar loads but the icons are missing. I've seen this happen on every refresh since the last deploy.

     **[00:12 – 00:25]**
     When I click on the dropdown it doesn't close properly, it just stays open. If I click elsewhere on the page it still doesn't dismiss. The only way to close it is to click the toggle again.
     ```

10. **Ask the user** what they would like help with based on the feedback

## Output Format

After analyzing, provide:

- **Video**: filename and duration
- **Analysis time**: Total processing time (keyframe extraction + transcription) formatted as `HH:MM:SS`
- **Keyframes**: Total number of keyframes created or found
- **Artifacts**: `summary.md` size in KB, and `narration.md` size in KB if it exists
- **Summary**: Detailed content summary — describe what is shown, demonstrated, and said in as much detail as possible
- **Key moments**: Important timestamps with what's happening
- **User's intent**: What they seem to want help with
- **Questions and requests in the recording**: List all questions and requests from the presenter in the recording. Try to answer the questions.
- **Documentation**: `${CLAUDE_PLUGIN_ROOT}/README.md`
- **Help command**: `/video-to-code-skill -> show-help-video-to-code-skill`

### Archived artifacts
Saved alongside the video and analysis in the archive folder:
- `summary.md` — the detailed video analysis summary
- `narration.md` — (if human speech is present) full narration in screenplay-ready format with timestamp ranges

Then ask: "What would you like me to help you with based on this feedback?"

## Script Reference

The `${CLAUDE_PLUGIN_ROOT}/scripts/video-to-code-skill-processor.py` script accepts these arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `<video_path>` | Path to video file | Required |
| `-o, --output-dir` | Output directory | `./video_analysis` |
| `-vd, --visual-details` | Visual detail level (1-10) | `10` |
| `-m, --model` | Whisper model (tiny, base, small, medium, large) | `base` or `large-v3-turbo` |

## Dependencies

| Package | Purpose |
|---------|---------|
| `opencv-python` | Frame extraction and scene change detection |
| `numpy` | Array operations |
| `mlx-whisper` | Audio transcription (Metal-accelerated, macOS) |
| `openai-whisper` | Audio transcription (fallback) |
