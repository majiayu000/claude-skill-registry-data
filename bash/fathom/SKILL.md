---
name: fathom
description: >-
  Fetch meetings, transcripts, AI summaries, and action items from the Fathom
  API via the bundled Python CLI (scripts/fetch.py). Use when the user asks to
  get Fathom recordings, sync meeting transcripts, fetch recent calls, or invokes
  /fathom_*.
disable-model-invocation: true
---

### TO COPY

# fathom

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/video-conf/fathom/scripts/fetch.py --list
```

##### END TO COPY

# fathom — Fathom meeting fetcher

Fetches meeting data directly from the Fathom API: transcripts, AI summaries, action items, participant info, and (optionally) the video recording.

## When to use

Trigger phrases: "get my Fathom meetings", "sync meeting transcripts", "fetch today's calls", "download Fathom recording", `/fathom_list`, `/fathom_today`, `/fathom_since`, `/fathom_get`.

`scripts/skill_env.py` resolves `.env` via SkillCred — scripts call `ENV.read_env()` / `ENV.get_secured_env()` in-process (no `source .env` in the shell).

Library scripts: `~/.meta-skills/skills/productivity/video-conf/fathom/`.

First Python run from the **library** skill folder:

```bash
cd ~/.meta-skills/skills/productivity/video-conf/fathom
~/.meta-skills/install.sh pip init .
```

## Credentials — SkillCred `.env`

| Variable | Notes |
|----------|--------|
| `FATHOM_API_KEY` | From [Fathom Settings → API](https://fathom.ai) |
| `OUTPUT_DIR` | Optional — default output for standalone `download_video.py` |

```bash
cp ~/.meta-skills/skills/productivity/video-conf/fathom/.env.example "{SKILL_PATH}/.env"
```

## Slash commands

| Slash | CLI | Description |
|-------|-----|-------------|
| `/fathom_list` | `python scripts/fetch.py --list` | List recent meetings |
| `/fathom_today` | `python scripts/fetch.py --today` | Fetch today's meetings |
| `/fathom_since` | `python scripts/fetch.py --since YYYY-MM-DD` | Fetch since a date |
| `/fathom_get` | `python scripts/fetch.py --id RECORDING_ID` | Fetch a specific meeting |

## Examples

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"

python scripts/fetch.py --list
python scripts/fetch.py --today
python scripts/fetch.py --today --analyze
python scripts/fetch.py --since 2025-01-01
python scripts/fetch.py --id abc123def456
python scripts/fetch.py --id abc123def456 --download-video
```

## Output format

Each meeting is saved as markdown with YAML frontmatter:

```markdown
---
fathom_id: <id>
title: "Meeting Title"
date: YYYY-MM-DD
participants: [list]
duration: HH:MM
fathom_url: <url>
share_url: <url>
---

# Meeting Title

## Summary
{AI-generated summary from Fathom}

## Action Items
- [ ] Item 1 (@assignee)

## Transcript
**Speaker Name**: What they said...
```

File naming: `YYYYMMDD-meeting-title-slug.md`.

## Prerequisites

- Shared venv: `~/.meta-skills/install.sh pip init .` from the skill folder (`requests`).
- Video download (optional): `ffmpeg` / `ffprobe` on PATH.

## Integration

- **transcript-analyzer**: `--analyze` runs the analyzer on fetched transcripts (if installed at `transcript-analyzer/` under the skill dir).
- **download_video.py**: `--download-video` downloads the recording (HLS → MP4) next to the meeting markdown.

## Notes

- Never commit `.env` or `FATHOM_API_KEY`.
- API base: `https://api.fathom.ai/external/v1` (rate limited ~60/min; client self-throttles).
- Confirm with the user before destructive actions.
