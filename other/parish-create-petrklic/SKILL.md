---
name: parish-create-petrklic
description: Add a new issue of the Petrklíč parish newsletter to the new farakurim.cz site from its PDF - confirm the issue number with the user, stage the PDF for upload, render the cover and viewer pages, add the issue, then publish. Use whenever the user brings a new Petrklíč, zpravodaj or newsletter PDF.
---

# Create a Petrklíč issue

`pnpm stage petrklic` stages the issue's PDF and images for upload and adds the issue. The newest issue is the
current one (aktuální číslo): the Petrklíč page shows its pages in the viewer and the homepage card shows its cover.

## 1. Read the PDF

The user gives at least a file name; without a folder, look in `~/Downloads/`. Read page 1 with the `Read` tool
(`pages: "1"`) for the year and the number within the year: the cover usually says them ("1/2026", "Velikonoce
2026"). If the cover does not give both, ask the user for them before going on; never guess them.

## 2. Confirm with the user

Check the issue from step 1 and get the page count:

```sh
pnpm stage petrklic "<source>" --year <year> --number <number> --check
```

It prints the folder it would stage (named by the id), the page count and where the issue would go, and refuses an
issue already in the file.

The issue is taken as a regular one: tell the user that a special issue needs them to say so, which sets the note
(`"mimořádné"` for an extra issue, `"1. část"` or `"2. část"` for an issue in two parts). The note changes the id, so
when they name one, run `--check` again with `--note "<note>"`. A refused issue may be a special one (a
`"mimořádné"` issue shares its number with a regular one): say so when you report the refusal.

Then show:

- **year** and **number** within the year, from step 1.
- **note**, only for special issues.
- **id**, as `--check` printed it: computed from the year, number and note (`2026-2`, `2026-3-mimoradne`,
  `2026-1-2-cast`). It names the PDF and the images.
- **pageCount**, as `--check` printed it.

Wait for the user's yes or corrections to these before staging anything.

## 3. Stage the PDF and render the images

```sh
pnpm stage petrklic "<source>" --year <year> --number <number> [--note "<note>"]
```

It stages the PDF, renders the cover and every page, adds the issue and runs the Petrklíč test. It says whether the
issue is now the current one: an older issue goes lower in the list.

## 4. Publish

Follow **`parish-publish-content`**.

## Common mistakes

- Staging (without `--check`) before the user confirms: an abandoned issue would go out with the next release.
