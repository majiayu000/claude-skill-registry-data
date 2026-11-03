---
name: release-notes
description: >
  Write or update developer-facing release notes for the current application. Derives what shipped
  from the actual code changes since the last release section, verifies every claim against the
  code, and writes scannable versioned notes a developer can read to understand what features were
  built. Use whenever the user says "release notes", "changelog", "write up this release",
  "update RELEASE_NOTES", or asks to document what shipped in a version.
---

# Release Notes

You write release notes for **developers** — someone who wants to know what features were built
and how the system behaves now, without reading commits or code. Notes describe **behavior**, not
implementation.

## Step 1 — Locate the file

Look for an existing release notes file (`RELEASE_NOTES.md`, `CHANGELOG.md`, or similar) at the
repo root first, then one level down (e.g. a Laravel app in a subfolder).

- Found one → use it. Match its existing version numbering.
- None found → ask the user where to put it, offering the **root of the application's git repo,
  as `RELEASE_NOTES.md`** as the default. Do not silently pick a location.

## Step 2 — Determine scope

Find what changed since the last release section:

- Last version section in the file → diff/log since the commit that added it.
- No file yet → since the last tag; no tag → ask the user where this release starts.

Commit messages are only a map. For every change you intend to mention, **read the code or tests
behind it** and describe what the system actually does. Never copy a commit message into a bullet.
A claim you cannot verify in the code does not go in the notes.

## Step 3 — Write the section

### Structure

- New section at the **top**: `## X.Y — Since X.(Y-1) — YYYY-MM-DD`. Newest first, never rewrite
  history below (see Corrections).
- One-line summary directly under the header naming the headline changes, so the reader decides
  in two seconds whether to read on.
- Group bullets under bold area labels (module, screen, or subsystem). Keep the **same area order
  in every version** — pipeline/data-flow order if the app has one, otherwise alphabetical.

### Bullets

- Every bullet starts with a **bold micro-lead**, then one sentence *what changed*, at most one
  sentence *why*. A scanner reading only the bold text should get the whole release.
- Deep rationale, mechanics, or edge cases → fold into the parent bullet as a clause, or one
  sub-bullet. Never a paragraph disguised as a bullet.
- **No commit hashes. No class or method names.** Config keys, env vars, artisan/CLI commands,
  and URLs are allowed when the developer needs the knob.
- **Name trade-offs outright.** If a change accepts a risk or removes a safeguard, say so in the
  bullet ("Note the trade: …"). Honest notes are the point.
- Behavioral numbers (limits, defaults, windows, thresholds) go in exactly as configured, with the
  setting that controls them.

### Example bullet

> **Long subjects no longer block auto-approve.** Nearly every subject exceeds the 50-char limit
> by design, so overflow was noise, not a defect. Still shown as a badge; all other review flags
> unchanged. Note the trade: a draft whose only fault is a long subject can send unread.

## Corrections — never rewrite history silently

If a past section turns out to be wrong:

- Add a one-line **"Correction to X.Y:"** bullet in the new section stating the true behavior.
- Annotate the old bullet in place with *(Corrected in X.Z: …)* — keep it short, keep both
  directions linked. Never delete or reword the old claim as if it was always right.

## Carry-forward checklist

If the file has a **"Before shipping"** (or similar open-decisions) list, carry every still-open
item into the new section verbatim, noting it is still open. Drop only items actually resolved,
and say what resolved them.

## Step 4 — Verify before finishing

Re-read the drafted section once against the code: every number, every default, every claim.
Then show the user the new section and where it was written.
