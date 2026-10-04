---
name: evo-dubbing-mux-report
description: Muxes normalized TTS audio segments into the original video at precise time offsets using FFmpeg, and generates the JSON report with timing, drift, and loudness metadata.
---

# evo-dubbing-mux-report

Muxes dubbed audio into video and generates JSON report.

## Key Functions

- `get_video_duration(path)` - Get video duration using ffprobe
- `build_ffmpeg_mux_command(video, segments, output)` - Build FFmpeg command
- `mux_dubbed_video(video, segments, output)` - Execute muxing
- `calculate_drift(placed_start, tts_duration, window_end)` - Calculate timing drift
- `generate_report_json(data, output_path)` - Write JSON report

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-dubbing-mux-report/scripts')
from utils import mux_dubbed_video, generate_report_json, get_video_duration
```
