---
name: gog-gemini-meeting-import
description: 'Import Gemini meeting Google Doc URLs using `gog` to export the doc, extract the Transcript section, write a transcript Markdown file, and generate structured meeting notes (summary/decisions/action items) using the bundled meeting-notes prompt. Use when given a "Notes by Gemini" Google Doc link and asked to save the transcript and produce meeting notes.'
disable-model-invocation: true
---

# Import Gemini meeting notes

Use this skill when asked to save a Gemini meeting Google Doc as a transcript and structured notes. It uses `gog` for Google Docs access and writes files to `/Users/prateek/code/github.com/prateek/personal-notes/21-openai-meetings` by default.

## Requirements

`gog` must be installed and authenticated for Google Docs access.

## Import one document

Pass either the Google Doc URL or its doc ID to the importer:

```bash
python3 scripts/import_gemini_meeting.py "<google_doc_url_or_doc_id>"
```

To choose another destination, pass `--out-dir`:

```bash
python3 scripts/import_gemini_meeting.py "<url>" --out-dir "/path/to/notes/dir"
```

The importer exports the document, extracts its Transcript section, writes the transcript, and prints the transcript and suggested notes paths. It does not generate the notes for a single-document import. Read `references/meeting-notes.md` and the transcript, then write the requested structured notes to the suggested notes path, following that prompt.

The filenames use `YYYY-MM-DD-meeting-transcript-<participants>.md` and `YYYY-MM-DD-meeting-notes-<participants>.md`. The importer infers the date and participant names from the transcript, then the document title; if it cannot infer them, it uses `unknown-date` or `unknown-attendees`. It can append a short doc ID to both names to avoid collisions when the importer is invoked with `--include-doc-id`.

The importer refuses to overwrite an existing transcript by default. Its `--overwrite` option replaces that file. Its `--allow-existing` option permits an existing transcript and returns the suggested paths without replacing it; use this when a workflow needs to reuse an existing transcript.

## Sync recent documents

Use the sync helper to discover Gemini meeting docs through Drive and Calendar. Preview discovery first:

```bash
python3 scripts/sync_gemini_meetings.py --dry-run --days 7
```

Import discovered documents and generate transcript and notes files with Codex:

```bash
python3 scripts/sync_gemini_meetings.py --days 90
```

The sync helper records completed doc IDs in `.gemini-sync/processed-docids.txt` under the output directory. It writes discovery and debug artifacts to the OS temporary directory and prints its location as `Run dir`. By default, it uses the same personal-notes meetings folder as the single-document importer. Pass `--out-dir` to select another destination.

## Transcript extraction

The importer starts at the `📖 Transcript` marker when present. It also accepts a plain `Transcript` marker and can fall back to a Transcript line followed by timecodes. It takes everything from that marker to the end of the document.

If extraction fails, preserve the source document and report that no transcript marker was found; do not invent transcript content. If the importer warns that the date or participants could not be inferred, keep its `unknown-date` or `unknown-attendees` filename unless the source provides reliable metadata to correct it.
