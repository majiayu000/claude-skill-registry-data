---
name: parish-correct-service-sheet
description: Correct a week's service sheet (the "pořad bohoslužeb" or "ohlášky") already on the new farakurim.cz site - fix its sheet through a corrected record, or stage a corrected PDF (or the corrected week of the parish's DOCX) with --corrected, then publish. Use whenever the user brings a corrected or replaced service sheet ("pořad bohoslužeb", "ohlášky") DOCX or PDF, or says a service, intention or announcement of a published week is wrong. A new week is added with parish-create-service-sheet.
---

# Correct a service sheet

Never edit a sheet in `src/content/service-sheets.json` by hand: a correction reruns `pnpm stage sheet` with a corrected
record, which replaces the sheet of the same week. A released file is never replaced, so once the week is
released its PDF's name is taken and the rerun takes `--corrected`.

## 1. Find the week

Take the sheet of the week the user names, or the corrected source's heading shows ("od … do …", its `validFrom`), from
`src/content/service-sheets.json`. A week no longer in the file (the script removes the sheets before the current one)
cannot be corrected.

## 2. Write the corrected record

Write `record.json` in the session's scratchpad (never in the repo) from the sheet: its `days` and `announcements`
only, without `validFrom`, `validTo` and `rev` (the script sets them). Change only what is wrong:

- a corrected PDF: compare it with the sheet, the way **`parish-create-service-sheet`** step 1 reads a PDF, and
  take over every difference;
- a corrected DOCX: draft the week (`pnpm stage sheet "<docx>" --from <validFrom> --to <validTo> --corrected
--draft <scratchpad>/draft.json`), compare the draft with the sheet and take over only the differences in the
  text, keeping the sheet's fixes (`<strong>`, categories, `newsId`);
- a correction the user describes: change those rows or announcements.

The fields follow **`parish-create-service-sheet`** step 2 (rows, `mass` and `service`, privacy, announcements).
A cancelled or moved service changes the week's `rows` only.

## 3. Confirm with the user

```sh
pnpm stage sheet "<source>" --record <scratchpad>/record.json [--corrected] --check
```

`<source>` is the corrected PDF or DOCX, which always takes `--corrected` (with a DOCX, also `--from` and `--to`
when the week is not its newest). When only the record changes, it is the week's
staged PDF in `uploads/porady_bohosluzeb/` (`pnpm pull-uploads` fetches the released files): `--corrected` only once
the week is released, as the check refuses the taken name otherwise. Show the user what changes
(day by day, the rows and announcements that differ).

Wait for the user's yes or corrections to these before staging anything.

Unattended: write this into the report instead, see "Unattended run" below.

## 4. Stage

```sh
pnpm stage sheet "<source>" --record <scratchpad>/record.json [--corrected]
```

It replaces the sheet of the same week, formats the file and runs the service sheet test. Before the release it
replaces the staged PDF; once the week is released, `--corrected` stages `…-porad-bohosluzeb-r2.pdf` (then `-r3`, …) and
stores the sheet's `rev`.

## 5. Publish

Follow **`parish-publish-content`**. Remind
the user to mirror changed or cancelled services in the "Bohoslužby" Google Calendar, which the Kalendář reads.

## Unattended run

Only when the prompt says the run is **unattended**; a local run follows steps 1 to 5 as written. The parish's
e-mailed DOCX never comes here: `parish-create-service-sheet` handles its newest week, corrections included. This
section is for a correction the prompt gives in words (a PR comment, the workflow's second phase): step 2's "a
correction the user describes" applies. Follow the rules of **`parish-create-service-sheet`** "Unattended run" except
its newest-week bullet (never asks, blocking questions and notes, report first, then stage, no
`parish-publish-content`, no commit, no release), with the scratchpad, the previous report and the report file the
prompt gives, in the same format. Here the commit line is a `fix(content): correct the service sheet for …` message,
the week's outcome is `corrected`, and the summary is what differs from the published sheet.

## Common mistakes

- Editing a sheet in `service-sheets.json` by hand instead of rerunning the command with a corrected record.
- Rewriting the whole record from the PDF and losing earlier fixes (a category, a `newsId`): start
  from the sheet.
- Leaving out `--corrected` after the release: the PDF's name is taken.
- Putting `validFrom`, `validTo` or `rev` into `record.json`: the script reads the dates from the heading and sets
  `rev`.
