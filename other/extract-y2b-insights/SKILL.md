---
name: extract-y2b-insights
description: Extract the most controversial or genuinely-novel insights from a YouTube video and output them both as a .txt file and printed in the terminal. Use when the user provides a YouTube URL and wants the key ideas, hot takes, or original thinking — NOT video clips. Optionally cross-checks ideas against the web to judge novelty.
allowed-tools: Bash,Read,Write,Glob,WebSearch,WebFetch
---

# Extract YouTube Insights

Pull the highest-signal **ideas** out of a YouTube video — specifically the most
**controversial** takes and the ones that read as **genuinely new** (ideas you would
NOT easily find already discussed across the web). Output them two ways:

1. A clean **`.txt` report** saved to disk
2. The same content **printed in the terminal**

This is the text-only cousin of `get-y2b-clips`: it reuses that skill's transcript
download + VTT parsing, but produces **no video clips and no subtitles** — just
distilled insights.

## When to Use This Skill

Activate when the user:
- Provides a YouTube URL and wants "insights", "key ideas", "hot takes", "takeaways"
- Wants the "most controversial" points, or "ideas that don't already exist" / "novel ideas"
- Wants a written summary of the *thinking* in a video, not clips of it

If the user wants **video clips** → use `get-y2b-clips`.
If the user wants **subtitles burned into a video** → use `add-subtitles`.

## Dependencies Check

```bash
command -v yt-dlp || echo "MISSING: yt-dlp"
```

`yt-dlp` is the only hard dependency (used to fetch the transcript). Install:
```bash
# macOS
brew install yt-dlp
# Linux / universal
pip3 install yt-dlp
```

`ffmpeg` is NOT required for this skill (no media is produced).

## Input Requirements

- **Required**: YouTube URL
- **Optional**:
  - Number of insights (default: 5–8, scaled to video length)
  - Focus: lean more "controversial" vs more "novel" (default: both)
  - Whether to web-check novelty (default: yes, when WebSearch is available)
  - Output path (default: `./insights/<date>_<slug>/insights.txt`)

## Workflow

### Phase 1: Setup

```bash
VIDEO_URL="USER_PROVIDED_URL"
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL")
CHANNEL=$(yt-dlp --print "%(channel)s" "$VIDEO_URL")
DURATION=$(yt-dlp --print "%(duration)s" "$VIDEO_URL")

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SLUG=$(echo "$VIDEO_TITLE" | tr '/:?*"<>|\\' '-' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | cut -c1-50)
OUT_DIR="./insights/${TIMESTAMP}_${SLUG}"
mkdir -p "$OUT_DIR"
echo "Video: $VIDEO_TITLE ($((DURATION / 60)) min)"
echo "Output: $OUT_DIR"
```

### Phase 2: Get the Transcript

**Priority: manual subtitles → auto-generated subtitles.**

```bash
cd "$OUT_DIR"

if yt-dlp --write-sub --sub-langs "en" --skip-download -o "transcript" "$VIDEO_URL" 2>/dev/null; then
    echo "Manual subtitles downloaded"
elif yt-dlp --write-auto-sub --sub-langs "en" --skip-download -o "transcript" "$VIDEO_URL" 2>/dev/null; then
    echo "Auto-generated subtitles downloaded"
else
    echo "No subtitles available"
    # Tell the user; without a transcript this skill can't extract insights.
fi

# Parse VTT -> segments.json + full_transcript.txt (timestamps preserved)
python3 .claude/skills/extract-y2b-insights/parse_vtt.py transcript.en.vtt
```

### Phase 3: Analyze for Controversial & Novel Insights

Read `full_transcript.txt` and select the standout **ideas**. Score each candidate
on two axes (0–10):

**Controversy (does it cut against consensus / provoke disagreement?)**
- Direct disagreement with named people, institutions, or "everyone"
- Contrarian framing: "everyone thinks X, but actually…", "unpopular opinion"
- Strong stance language: "never", "always", "completely wrong"
- Predictions that defy the current narrative

**Novelty (would you struggle to find this idea already discussed online?)**
- A specific mechanism, framework, or causal claim that isn't the standard talking point
- A non-obvious connection between two domains
- A concrete prediction or number that isn't the consensus figure
- Reframing of a familiar problem in a way that isn't widely circulated

Select an insight if it scores **high on at least one axis** (≈7+). Prefer ideas that
are *specific and falsifiable* over vague platitudes. Skip generic advice, well-worn
truisms, and anything that's just a summary of common knowledge.

Capture the **exact timestamp** from `segments.json` for each insight so the user can
jump to it (`<URL>&t=<seconds>s`).

### Phase 4: Web-Check Novelty (optional but recommended)

For each candidate flagged as "novel", do a quick WebSearch to test whether the idea
is genuinely uncommon:

- Search the core claim in a few words.
- If results show the idea is widely repeated → lower its novelty score (or drop it).
- If results show only the *opposite/conventional* view, or little on the specific
  framing → keep it and fill in `web_contrast` (what the common online view is, and
  how this differs).

Only do this when WebSearch is available and the user hasn't opted out. Keep it light
(1 quick search per candidate) — this is a sanity check, not exhaustive research.

### Phase 5: Write insights.json

Create `$OUT_DIR/insights.json` following this schema:

```json
{
  "source": {
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "title": "Video Title",
    "channel": "Channel Name",
    "duration_minutes": 92
  },
  "insights": [
    {
      "title": "Short headline for the idea",
      "claim": "1-3 sentence statement of the insight as the speaker frames it.",
      "timestamp": "00:14:05",
      "type": "controversial",
      "controversy_score": 9,
      "novelty_score": 6,
      "why": "Why this is controversial and/or appears to be a genuinely new idea.",
      "web_contrast": "What the conventional / commonly-found-online view is, and how this differs.",
      "quote": "Optional short verbatim quote from the transcript."
    }
  ]
}
```

- `type`: `"controversial"`, `"novel"`, or `"both"`.
- Order insights strongest-first (highest combined controversy + novelty).
- `web_contrast` is optional; include it whenever a web-check was done.

### Phase 6: Render to .txt AND terminal

```bash
python3 .claude/skills/extract-y2b-insights/render_insights.py \
    --insights "$OUT_DIR/insights.json" \
    --output "$OUT_DIR/insights.txt"
```

This writes a clean `insights.txt` and prints the same report (colorized) to the
terminal. Use `--no-print` to only write the file.

### Phase 7: Summary

Tell the user:
- How many insights were extracted and the path to `insights.txt`
- A one-line teaser of the top 1–2 insights
- That timestamps are included so they can jump to each moment in the video

## Console Progress Reporting

```
[SETUP] Fetching video info...
  ✓ Video: "Title Here" (92 min) — Channel Name

[TRANSCRIPT] Downloading subtitles...
  ✓ Auto-generated English subtitles found
  ✓ Parsed 1,204 segments

[ANALYSIS] Scoring controversial & novel ideas...
  ✓ 7 insights selected (web-checked 4 for novelty)

[OUTPUT]
  ✓ insights.json written
  ✓ insights.txt written + printed below
```

## Error Handling

| Issue | Solution |
|-------|----------|
| `MISSING: yt-dlp` | Provide install command, then retry |
| No subtitles available | Inform user — without a transcript, insights can't be extracted. Offer to fall back to `get-y2b-clips`' Whisper path if they want audio transcription |
| Private/unavailable video | Inform user, cannot proceed |
| Very short video | Extract fewer insights (1–3) |
| WebSearch unavailable | Skip Phase 4; still extract based on transcript, note novelty is un-verified |

## Output Files

```
insights/
  YYYY-MM-DD_HH-MM-SS_<slug>/
    transcript.en.vtt      # raw subtitles
    segments.json          # timestamped segments
    full_transcript.txt    # readable transcript w/ timestamps
    insights.json          # structured insights (source of truth)
    insights.txt           # final human-readable report (also printed to terminal)
```

## Example Session

**User**: Pull the most controversial / original ideas from
https://www.youtube.com/watch?v=abc123 and save them to a txt.

**Claude**:
1. Checks `yt-dlp`
2. Fetches video info + downloads the transcript, parses to `segments.json`
3. Scores ideas for controversy + novelty; web-checks the novel ones
4. Writes `insights.json`, then runs `render_insights.py` → `insights.txt` + terminal print
5. Summarizes the top insights and the file path
