---
name: x-extractor
description: Turn X/Twitter links into a folder with post text, article, images, video and transcript by running python_skills/confirmed/x_pipeline/x_link.py. Use when the user gives X or twitter.com status links to capture.
---

# x-extractor (pure Python skill, Claude Code only)

All the work is done by `python_skills/confirmed/x_pipeline/x_link.py`. There is no LLM step.

## Run

From the repo root, after `pip install -r python_skills/confirmed/x_pipeline/requirements.txt`:

```
python python_skills/confirmed/x_pipeline/x_link.py LINK1 LINK2 --out x_inbox
python python_skills/confirmed/x_pipeline/x_link.py --links-file links.txt
```

Options: `--model small|medium` (whisper), `--no-transcribe`, `--no-download`, `--no-articles`, `--cookies-browser chrome` (protected posts).

## Mode

Check mode until the user says this skill is established: read the script's output and `x_inbox/SUMMARY.md` and report anything missing.
Once the user says it is established: run the script and do not read its source.

## Output

`x_inbox/notes/<id>.md`, `images/`, `videos/`, `SUMMARY.md`, `failed_*.txt`.
Exit code 0 = all captured, 1 = a link failed, 2 = no valid links.

## Report back

Per link: captured or missing (text, article, images, video, transcript). Transcripts are machine-generated (faster-whisper), so names and numbers can be wrong; say so.
Never paste keys or cookies into chat or the repo.
