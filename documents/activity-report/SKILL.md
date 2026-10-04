---
name: activity-report
description: 'In one invocation, build a.md (commit messages and Markdown diffs per git working tree over a date window, default end today) without reading the full codebase, analyze it, present the topics to select, ask for a few words of context, then write or update a French report a.activity-report.<start>-<end>.md in the review artifact home (.reviews) for review. With no file it creates that conventional name, or updates it (adding only new topics) when it already exists; pass an existing report file to update it. On the user go-ahead after review, it renders the report to HTML then PDF. Use when the user asks for an activity report across one or more working trees.'
user-invocable: true
argument-hint: 'Give the start date and the working trees, for example "activity-report --start 2026-05-29 . ../my-project". End date defaults to today (--end YYYY-MM-DD). Optionally pass an existing report file to update it; with no file the conventional a.activity-report.<start>-<end>.md is created, or updated when it already exists.'
---

[Instruction](../../../instructions/activity-report.md)

Implementation is mutualized across the shared directories:

- [`../instructions/activity-report.md`](../../../instructions/activity-report.md)
  — the full end-to-end workflow.
- [`../templates/activity-elements.template.md`](../../../templates/activity-elements.template.md)
  — the structure of the generated `a.md` elements document.
- [`../templates/activity-report.french.template.md`](../../../templates/activity-report.french.template.md)
  — the structure of the French report.
- [`../scripts/activity_report.sh`](../../../scripts/activity_report.sh)
  — the git log / git diff script, run from the calling project root.

Inputs: a start date, an optional end date (default today), one or more
git working trees, and an optional existing report file to update. The
skill runs end to end: it writes `a.md` in the calling project's review
artifact home (`.reviews`, see `rules/artifact_files.md`), presents the
topics for selection, asks for a few words of context, then writes or
updates `a.activity-report.<start>-<end>.md` in the same home, creating that
conventional name, or updating it without overwriting (adding only new
topics) when it already exists, or updating the file passed in. After the
user reviews and says go ahead, it renders the report to HTML then PDF over
the same base name, using `templates/md_to_pdf.py.template`. The home's own
`*` ignore file keeps all these files out of Git.
