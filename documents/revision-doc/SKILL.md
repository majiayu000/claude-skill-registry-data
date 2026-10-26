---
name: revision-doc
description: Build a before and after revision report as a Word document for a batch of UI or product changes. Captures a before screenshot of every screen before the code changes and an after screenshot of the same screen at the same size, draws red boxes on what changed, and writes a landscape .docx with one page per change holding the problem behind each request, what changed and how it was checked, with the before and after shots side by side. The document is authored by the person signed in to the computer, not python-docx, and carries a real preview thumbnail so File Explorer and Finder show the first change instead of a blank white page.
when_to_use: Use when the user asks for a before and after document, a revision report, a revision doc, a change report with screenshots, before after shots for each change or feature, a docx of what changed, or says "like the revision of <date>" for a batch of fixes. Also use when an existing revision .docx shows python-docx as its author or a blank white thumbnail. Do not use for release notes without screenshots, changelogs, or single screenshots.
argument-hint: '[folder] | build <folder> | check <file.docx>'
allowed-tools: Bash(bash "${CLAUDE_SKILL_DIR}/scripts/*) Bash(powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/*) Bash(pwsh -NoProfile -File "${CLAUDE_SKILL_DIR}/scripts/*) Read Write Edit Glob Grep
---

# Revision Doc

You turn a batch of changes into a revision report that a client or teammate can read without opening the code. Every change gets its own page: what was asked, what changed, how it was checked, and the same screen before and after with red boxes on the difference.

Arguments: `$ARGUMENTS`

The skill directory is `${CLAUDE_SKILL_DIR}`. Reference files write it as `<skill-dir>`, and relative links in this file resolve from it.

## Terse Chat

Chat replies are terse by default to save tokens. Lead with the result. Drop filler, pleasantries, hedging, tool narration and closing recaps. Fragments are fine. Keep every fact, number, path, command and error string exact.

Terse covers chat only. The report itself is written in full sentences under its own rules below.

Turn it off when the user says `verbose`, "normal mode", "full sentences" or "stop caveman", or their CLAUDE.md asks for verbose replies. Turn it back on with `terse`. Never announce or name the style.

## Pick the Mode

| Arguments or request | Mode | What to do |
|----------------------|------|------------|
| empty, a folder, or "make a before after doc for these changes" | Report | Follow Report below |
| `build <folder>` | Build | Run the build script on an existing revision folder, then Check |
| `check <file.docx>` | Check | Run the check script and fix what it reports by rebuilding |

## Report

1. **Plan the folder.** One dated folder per batch next to the project, named like the user's earlier ones (for example `21 okt revision`). Create it with `bash "${CLAUDE_SKILL_DIR}/scripts/revision-doc.sh" init "<folder>" --title "<title>" --lang <id|en>` or `powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/revision-doc.ps1" init "<folder>" -Title "<title>" -Lang <id|en>`. Pick the language the user writes in. Reuse an existing folder instead of making a second one for the same batch.
2. **Capture before shots first.** Before editing any code, take a screenshot of every screen a change will touch, following [references/capture.md](references/capture.md). Save them under `before/<role>/NN-name.png`. If the code was already changed, take them from an untouched copy of the last commit, never from `git stash` in a shared tree. If a before shot cannot exist (a new screen, a backend only fix), leave `before` out and write a `before_note` that says why.
3. **Make the change and test it.** Run the project's tests and check the change in a real browser like a user would.
4. **Capture after shots** of the same screens at the same size, language, account and scroll position. Save them under `after/` with the same file names.
5. **Mark the changes.** Write `before/boxes.json` and `after/boxes.json` with one red box per changed area, in CSS pixels of the capture viewport. View a few boxed crops to confirm each box sits on the change.
6. **Write `items.json`** in the format in [references/items-format.md](references/items-format.md). One item per visible change, in the order the user asked for them.
7. **Build** with `bash "${CLAUDE_SKILL_DIR}/scripts/revision-doc.sh" build "<folder>" --copy-to "<downloads>"` (PowerShell: `build "<folder>" -CopyTo "<downloads>"`). Copy to the user's Downloads folder unless they keep reports somewhere else.
8. **Check** with `check "<folder>/<output>.docx"`. It must report the user's name as AUTHOR and `THUMBNAIL: embedded`, with no PROBLEM lines.
9. **Report** in chat: the path of the docx, the number of items, and any item that has no before or after shot and why.

## Writing Rules

- **Asked** states the problem, not the prompt. Turn each request into a plain statement of what was wrong: what happened, where, and what it cost the user. Drop chat words like please, can you, "dong" or "ya", questions and first person. Every request in the batch is covered by at least one item.
  - Prompt: "Pas gw tambahin step skill test lagi jadinya error. Kalau bug perbaiki dong."
  - Problem: "Tahap Tes keahlian baru di lowongan yang sudah Dibuka tidak bisa disimpan. Sistem minta tes ditautkan dulu, tapi tes baru bisa ditautkan setelah tahap disimpan."
  - Prompt: "Buat requirements dan benefits dibikin stacking aja, jangan kanan kiri."
  - Problem: "Kolom Persyaratan dan Tunjangan berdampingan kiri kanan, jadi ruangnya sempit dan toolbar editornya terlipat dua baris."
- When the user asked for a new feature rather than a fix, describe the gap it fills: "Dari halaman Tahap rekrutmen tidak ada jalan ke pengaturan templat alur, jadi HR tidak tahu di mana templat bisa diubah."
- **Changed** says what is different for the user first, then the cause when it was a bug, then the technical change in plain words.
- **Checked** names real evidence: the number of tests that passed and what was done in the browser with which account and data. Never write a check that was not run.
- A change with no visible difference still gets a page, with a note in place of the missing shot.
- Write in the user's language. No semicolons and no em dashes. No marketing words.
- Say plainly when something was not fixed or was left for later.

## Before You Send

- [ ] Every change has a page, and every user request of the batch is covered by a problem statement under Asked, written as a problem, not as the prompt
- [ ] Before and after shots of each page show the same screen at the same size
- [ ] Every red box sits on the changed area
- [ ] `check` shows the user's name as AUTHOR, `THUMBNAIL: embedded`, and no PROBLEM
- [ ] The docx was copied where the user keeps reports

## Gotchas

- The python-docx default template ships a blank white `docProps/thumbnail.jpeg`, which is why File Explorer shows a white page. The build script replaces it with a preview of the title and the first before and after pair. Explorer may keep the old preview until the file changes or the view refreshes.
- The author comes from the display name of the signed in account (Windows `GetUserNameExW`, the passwd full name on macOS and Linux), falling back to the login name. Set `REVISION_DOC_AUTHOR` to override it.
- The build needs Python 3.8 or newer with `python-docx` and `pillow`. Exit code 3 means one is missing. Install with `pip install python-docx pillow`.
- Boxes are in CSS pixels of `viewport` (default 1440). Screenshots taken at a device scale factor of 2 still line up because the script scales by image width.
