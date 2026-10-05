---
name: research-podcast
description: Turn papers, PDFs, reports, lecture notes, datasets, or research material into an evidence-aware AI podcast for deep dives, exam review, defense rehearsal, or multi-source briefings.
---

# Research Podcast

Create a traceable chain from research evidence to spoken dialogue.

## Paths
- `SKILL_DIR`: directory containing this file.
- `DATA_DIR`: `~/.research-podcast`.

Read `QUALITY_RULES.md` before drafting and `PROMPT.md` for dialogue style.

## Workflow
1. Read all supplied research material.
2. Build `DATA_DIR/runs/<run-id>/source_map.json` with stable source IDs, source labels, locations when known, factual summaries, and supporting evidence.
3. Use the requested mode: `deep-dive`, `exam-review`, `defense`, or `briefing`; default to `deep-dive`.
4. Follow `PROMPT.md` and save `DATA_DIR/runs/<run-id>/script.json`. Facts and interpretations require supporting `source_ids`.
5. Validate before audio:
```bash
python SKILL_DIR/scripts/validate_script.py --script DATA_DIR/runs/<run-id>/script.json --sources DATA_DIR/runs/<run-id>/source_map.json
```
6. For audio, create `DATA_DIR/venv`, install `scripts/requirements.txt`, copy `config/config.example.yaml` to `DATA_DIR/config.yaml`, set both voice IDs, and ensure `ffmpeg` is installed.
7. Generate:
```bash
DATA_DIR/venv/bin/python SKILL_DIR/scripts/speak.py --script DATA_DIR/runs/<run-id>/script.json
```
The audio tool requests the provider credential interactively and writes an MP3 under `DATA_DIR/episodes/`.

## Completion checks
Confirm the source map exists, the script validates, factual claims are traceable, and requested audio is non-empty.
