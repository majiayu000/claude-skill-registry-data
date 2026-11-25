---
name: process-root-transcripts
description: >
  Convert any *.txt transcripts at the repo root into Obsidian meeting
  transcript + summary pairs (offline, no API key required), then commit and
  push. The model authors the summary in-session from the transcript text.
  Use when asked to "process transcripts", "convert txt transcripts", "add
  meeting transcript", "ingest transcripts", or invokes /process-root-transcripts.
argument-hint: "[optional-filename.txt]"
---

# Process Root Transcripts Skill

Runs the `/process-root-transcripts` workflow for the Obsidian vault at
`/home/gbencke/git.work/331.obsidian-scripts`.

If an argument is provided, treat it as a single source filename and process
only that file. Otherwise process every `*.txt` at the repo root.

**No `ANTHROPIC_API_KEY` is used.** The model running this skill must author
the summary files in this same session — do not call any LLM-backed script.

Do not delete or move the source `.txt` files. They stay at the repo root.

---

## Step A — Discover source files

1. List candidates:
   ```bash
   ls *.txt
   ```
   at the repo root, or use the provided argument if given.
2. If the list is empty, stop and tell the user there is nothing to process.
3. For each candidate, verify it is a parseable transcript: it must contain at
   least one `HH:MM:SS` timestamp line preceded by a non-empty speaker name
   line (the format handled by `05.Scripts/convert_txt_to_meetings_offline.py`).
   Skip and report any file that doesn't match.

---

## Step B — Generate transcript .md files

Run:

```bash
python3 05.Scripts/convert_txt_to_meetings_offline.py
```

This deterministically writes
`02.Meetings/transcripts/<YYYY.MM.DD>.<Title>.Transcript.md` for each `*.txt`
at the repo root, skipping files whose transcript already exists. It uses the
per-source `OVERRIDES` table inside the script for known titles
(architecture-review, platform-sync) and falls back to `technical-refinement`
otherwise.

Capture the script's stdout and note which transcripts were `written`,
`skipped (already exists)`, or `skipped (no parseable entries)`.

If an argument was given, confirm the matching transcript was produced;
otherwise note all of them.

---

## Step C — Author summary .md files (in this session)

For **each transcript written in Step B** (skip ones that already had a
transcript on disk unless the user explicitly asked to redo them):

1. Read the freshly written transcript file in full from
   `02.Meetings/transcripts/`.
2. Read the most recent existing summary in `02.Meetings/summaries/` (sort by
   filename descending) — this is the **formatting model**. Match its
   frontmatter, heading hierarchy, and section structure exactly:
   - **Frontmatter:** `category: meeting-summary`, `description:
     "<one-paragraph summary>"`, `participants:` (same list as the transcript,
     same order), `creation` / `last_updated` (the meeting date), `tags:` with
     `meeting/summary` and `meeting/type/<slug>/summary` (same `<slug>` as the
     transcript).
   - **Body:** `#meeting #meeting/summary #meeting/type/<slug>/summary`, then
     `# <Title>`, then a friendly date/time line.
   - `## General Summary` containing one `### <Topic Name> (HH:MM - HH:MM)`
     block per discussion topic, each with bulleted notes that mention
     participants in **bold** and call out tickets, decisions, trade-offs.
   - `## Action Items` at the end, each line
     `- **<Owner>**: <action> *(HH:MM)*`.
3. Write the summary to
   `02.Meetings/summaries/<YYYY.MM.DD>.<Title>.Summary.md`. The
   `<YYYY.MM.DD>.<Title>` portion must match the transcript filename exactly
   (drop `.Transcript`, append `.Summary`).
4. Author the summary content from the transcript text in this same session.
   Do **not** invoke any external LLM script. Do not call
   `05.Scripts/convert_txt_to_meetings.py` or
   `05.Scripts/generate_summary_from_transcript.py` — those require an API key.
5. **Quality bar:** cover every distinct topic in the transcript; preserve
   ticket numbers (e.g. `NGS-2095`, `PMSC-188`); attribute opinions to the
   right speaker; keep timestamps relative to the meeting start as already used
   in the transcript body.

---

## Step D — Commit and push

For **each new (transcript + summary) pair**, publish a single commit:

```bash
python3 05.Scripts/daily_workstream_update.py git-publish "Add <YYYY-MM-DD> <Title> transcript and summary"
```

Use the dashed date form in the commit message, matching the existing history
(e.g. `Add 2026-04-24 Architecture Backlog Refinement transcript and summary`).
If multiple pairs were produced, run `git-publish` once per pair so each commit
groups its own transcript + summary.

If `git-publish` reports "nothing to commit" for any pair, say so explicitly.

---

## Final Report

Print a concise summary at the end:

- Source `.txt` files found at repo root (kept in place, not deleted)
- For each: transcript path written (or "already existed, skipped"), summary
  path written (or "already existed, skipped"), meeting type slug used, commit
  pushed (or "nothing to commit")
- Anything skipped because it wasn't a parseable transcript
- Confirmation that no `.txt` source file was modified or removed
