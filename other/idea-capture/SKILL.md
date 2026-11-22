---
name: idea-capture
description: Capture a raw idea the moment it arrives and keep it in a durable store, so it survives between sessions. Use whenever an idea comes up mid-work, in passing, or outside a calibration session — before it is lost — and when you need to find, promote, or drop a stored idea. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Python 3.11+.
---

# IDEA-CAPTURE — a fleeting idea that is not captured is lost

An idea that arrives mid-work and is not written down is gone by the next session. This skill is the store for raw ideas: one Markdown file per idea, in the project's `ideas/` directory, written verbatim and never edited. Calibration is a separate step (`idea-calibrate`); this skill only makes sure the idea is still there when you are ready for it.

## Rules

- Capture first, calibrate later. When a raw idea arrives, write it down before doing anything else with it — before answering, before coding, before the next message.
- Verbatim, always — with one exception: capture refuses text that
  looks like it contains a secret (a key-shaped value) unless
  `--allow-secret` is given; with the override the text is still
  stored verbatim, but the id's slug is built from the redacted form,
  so no secret fragment lands in the filename. The raw text is the
  idea as spoken, with the date and who said it. Never edit, improve,
  or interpret it after capture.
- The store lives in the project (`ideas/`), committed with it. A store in `/tmp` is lost on the next restart; a store in the project survives.
- A dropped idea is never deleted. Dropping only changes the status and records the reason. The file, the raw text, and the reason stay.
- Statuses move one way: `raw` → `calibrated` → `scoped`, or any → `dropped`. A dropped idea never comes back as raw; if it returns, capture it again as a new idea.

## Steps, in order

### 1. Capture

Run the script (`scripts/capture.py`, Python 3.11+, standard library only):

```
capture.py capture --store <project>/ideas --text "<the idea, verbatim>" --source "<who said it>"
```

It prints the idea id (`YYYYMMDD-HHMMSS-slug`). The slug is ASCII only (a-z, 0-9, hyphen): the raw text may be any language — a Persian-only idea gets the slug `idea` (with a `-2` suffix if two collide in the same second) — while the raw text itself is stored verbatim. An empty idea is refused (exit 1, no file created). A secret-shaped value is the other refusal: capture exits 1 with no file created when the text matches a high-confidence secret pattern (a key-shaped value such as an `sk-…` token), unless `--allow-secret` is given — and the slug is always derived from the redacted form, so even an allowed capture never leaks a secret fragment into the id or filename. The refusal names the pattern, never the value. If two ideas arrive in the same second, the second gets a `-2` suffix — the id is always unique. The raw text is stored exactly as given; only the emptiness check strips whitespace, and CRLF line endings are normalised to LF. The frontmatter carries `raw_length` (the length of the raw text), so an idea that itself contains a line reading `## History` is not truncated. The source must be a single line (a newline would inject a frontmatter field). The id is strictly validated (only the generated shape is accepted) and the resolved path must stay inside the store, so an id can never escape it — even through a symlink. Listing and searching resolve every file and require it to stay inside the store, and a file whose frontmatter id does not match its filename is reported as malformed. A status change takes a lock file (created with O_EXCL; the holder's PID is written into it, so a lock left by a dead process is recognised as stale and removed with a note, while a lock with no readable PID is never stolen and a lock is never removed for age) for the whole read-modify-write, then writes atomically (temp file + replace), so two concurrent changes cannot lose a History entry and an interruption cannot leave a half-written file. A capture creates its file exclusively, so two concurrent captures cannot overwrite each other. A file that cannot be parsed is reported to stderr, never silently skipped — and a `list` or `search` that skipped one exits 2 (partial), so a machine caller never treats an incomplete result as complete. A status change edits only the frontmatter's `status:` line, never a `status:` line inside the raw text, and a file with no status recorded fails cleanly instead of assuming one.

### 2. Find it later

- `capture.py list --store <project>/ideas` — every idea, with status and date.
- `capture.py list --store <project>/ideas --status raw` — only the unprocessed ones.
- `capture.py search --store <project>/ideas <keyword>` — ideas whose raw text contains the keyword (case-insensitive; works in Persian and English). Search matches only the raw idea text, not the frontmatter or the History, so searching for "raw" or "dropped" does not return everything.
- `capture.py show --store <project>/ideas <id>` — the whole file.

### 3. Move it forward

When the idea is calibrated with `idea-calibrate`, record it:

```
capture.py promote --store <project>/ideas <id> calibrated --note "<what it became>"
```

When the calibrated brief is scoped into v1, promote it to `scoped`. When the idea is not going ahead, drop it — with a reason, always:

```
capture.py drop --store <project>/ideas <id> --reason "<why not>"
```

Every move appends one line to the file's History. The raw text is never touched.

## Report

Return the report in this form:

- Captured (id, date, source).
- Store (path, number of ideas by status).
- Moved (every status change, with the reason).
- Verdict: PASS (the idea is on disk verbatim, findable by search, and every move is recorded) or FAIL (an idea was lost, edited, or deleted, or a move was not recorded).

## Scope

This skill is the store only. It does not sharpen, validate, or scope an idea — that is `idea-calibrate`. It does not decide what to build — that is the user, at the Idea → Code gate. The store is plain Markdown files; there is no database, no server, and no sync — the project's own git history is the backup.

## Sources

Written from scratch. No ready skill answers this need: the research found capture-in-session (idea-calibrate, step 1) but no persistent store for fleeting ideas between sessions.
