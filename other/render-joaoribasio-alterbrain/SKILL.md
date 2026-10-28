---
name: render
description: Makes a finished PDF or slide deck (CV, cover letter, report, memo, assignment or presentation) from the user's notes with the Quarto templates, checks the page limit and fonts, and explains any error in plain English. Use when the user asks to make, build, export, print or "turn into a PDF, CV, letter or deck".
model: sonnet
effort: medium
argument-hint: "[cv|letter|report|deck] [note, topic or folder]"
---

# Render: turn notes into a CV, letter, report or deck

Makes a good-looking, correctly sized document from text the user already has, and tells them in plain words how it went.

## When to use

- "Make my CV", "make an ATS-friendly CV", "turn this into a 6-page PDF", "make a cover letter for this job", "make slides from this note".
- `/assignment ship` and `/jobs apply` call this skill for the final file.
- Not for writing the content itself. Drafting words is `/assignment`, `/jobs` and the `ghostwriter` agent. Render only lays out words that already exist.

## Before you start

1. **Clarify first.** Use `/clarify document` (the checklist for documents) unless the request already answers it. You need five answers. Take every one you can from the files below, and ask only for what is missing, one question at a time:
   - which kind of document (see the table in step 1);
   - what the words come from (a note, an assignment folder, the user's facts);
   - who will read it and what it is for;
   - the limits: pages, font size, line spacing, margins. For an assignment these are already in `assignment.md` under `limits`;
   - the language (`en` or `nl`).
2. **Read, in this order, only what applies:**
   - `vault/10_projects/<assignment>/assignment.md` (limits, deliverables, `status`);
   - `vault/80_me/USER.md`, `vault/80_me/fact-sheet.md` and `vault/20_areas/career/career.md` (for a CV or letter);
   - the application note in `vault/20_areas/career/applications/` (for a letter);
   - the source note or `report.qmd` (for a report or deck);
   - `vault/80_me/brand/_brand.yml`, if it exists (colours and fonts: the user default when no template is set).
   - `vault/80_me/voice/<lang>/profile.md` (voice). Without one, say so once per session and suggest the voice setup; do not fall back to a neutral house style unless the user wants to go on now.
3. **Check the tools once per session.** Run `node system/quarto/tools/fonts.mjs`. For a deck, also run `node system/scripts/pages.mjs check` now: the page check in step 7 needs a PDF, so a deck that may be handed over is rendered with `--pdf`. If the PDF page renderer is missing, offer to install it once, here. If the user declines, say in the hand-over which pages you could not view.
   - If it says Quarto is missing, tell the user in one line how to install it (Windows: `winget install --id Posit.Quarto -e`, or quarto.org) and stop.
   - If fonts are missing, say which, and offer the two fixes it prints. Do not continue silently: a substitute font can change the page count.
4. Field lists for every template are in `references/templates.md`. Read it when you fill a template. Tone and voice rules: `system/deliverables/tone-and-voice.md`. Deck and document principles: `system/deliverables/principles.md`.

## Steps

1. **Pick the template** from what the user asked for.

   | Document | `--type` | Starter file |
   |---|---|---|
   | CV for a person to read | `cv` | `cv.qmd` + `cv-data.yml` |
   | CV for online forms, "ATS", "plain" | `cv-ats` | `cv-ats.qmd` + `cv-data.yml` |
   | Cover letter | `letter` | `letter.qmd` |
   | Report, case, memo, assignment | `report` | `report.qmd` + `references.bib` |
   | Slides, presentation | `deck` | `deck.qmd` |

   A CV with no preference: make both layouts from the same `cv-data.yml`, and say which is for what.

   **Resolve the template silently.** Run `node system/scripts/template.mjs resolve --kind <kind> --for <source> --json` (kind: deck, report, memo, letter, cv, essay, one-pager). Say in one line which template it chose ("Using your school's report template."). Ask only if `tie` is not empty (name the candidates, recommend the one made most recently for this course) or the user asks. The result also gives `style`, `tone`, `csl`, `max_upload_mb`, `page_limit` and `house_rules`. Pass the template folder (`template.dir`) as `--template`. Pass `--csl <resolved csl>` whenever `resolve` returns a `csl` that is a path (the programme's or the template's required style); `--reference-doc` only when the user names a file. If `csl_missing` is true or `warnings` say the required citation style has no file, tell the user in one line ("Your programme requires Chicago, but I have no style file for it, so references use the default style") and offer to add the file to the template folder. Explicit `--csl` from the user wins. Show every `warnings` line that matters to the result (an unknown course or programme link, a missing template). A built-in result with `vault/80_me/brand/_brand.yml` present keeps using that brand file. Template questions: `/template`.
2. **Choose the folder and start the files.** Use the existing source if there is one. Otherwise:
   - CV: `vault/20_areas/career/cv/`
   - letter: `vault/20_areas/career/applications/<company role>/`
   - assignment: the assignment folder (`report.qmd` already belongs there)
   - anything else: `vault/10_projects/<short-name>/`

   Then run `node system/quarto/tools/render.mjs scaffold <type> <folder>`. It never overwrites a file that is already there, so a `cv-data.yml` that another skill prepared is kept.
3. **Fill the file.** Follow the rule for the type.
   - **CV:** edit only `cv-data.yml`. Follow `references/cv-filling.md`: every line comes from `fact-sheet.md`, `USER.md` or `career/` notes. If a fact is missing, leave the line out and ask. Never guess a date, number, title or employer.
   - **Letter:** the `ghostwriter` agent drafts the text from the voice profile and the fact sheet. You place it in `letter.qmd` and fill the data block. Keep it to one page.
   - **Report:** the content is the user's. Check the structure against `references/templates.md` (sections start at `##`, `\$` for dollar signs, `*Source: ...*` notes, citations as `@key`). Add missing keys to `references.bib` only from real source notes in `vault/40_sources/`.
   - **Deck:** storyline first. Show the ghost deck (the slide titles only, each a full-sentence takeaway) and wait for a yes before writing the file (`system/deliverables/principles.md`). The style from `resolve` sets the rules: `reading-deck` slides explain themselves (an "In brief" box, sources, footnotes); `presenting-deck` slides carry minimal text and the content goes in the speaker notes (`::: {.notes}` blocks). A template or rubric structure wins over the general principles; say so in one line.
   - **Tone and voice (report, deck, memo):** write in the resolved `tone` on top of the user's own voice, with a story inside the structure, as in `system/deliverables/tone-and-voice.md`. No invented anecdotes or facts.
4. **Confirm, then write.** Give a three-line summary of what will be written and where. When the user says yes, write.
5. **Render.** Run one command from the project root:

   `node system/quarto/tools/render.mjs <source> --type <type> [--template <folder>] [--max-pages N] [--pdf] [--name "<name>"]`

   - `--max-pages N`: for assignments use `limits.pages`. With no assignment limit, use the template's `page_limit` from `resolve`. For a CV use 2 unless the user says otherwise; for a letter use 1.
   - `--pdf`: for a deck, always when it may be handed over (step 7 views the PDF pages; HTML cannot be viewed page by page) and whenever the user wants a PDF as well.
   - `--format docx` or `--format pptx`: for a Word or PowerPoint copy when the brief lists one. These have a plainer look (they use the template's reference document, else `vault/80_me/brand/reference.docx` or `reference.pptx` when present). The page count is not available for them, so say so.
   - An Obsidian note ending in `.md` works as the source. The tool converts a copy first and never changes the note.
   - Output goes next to the source in `_out/` (scratch space, replaced each time, not saved to git). For a final version add `--release`: it goes to `releases/<today>/` and every version is kept. If another skill gave you a folder or a file name, pass `--out <folder>` and `--name <name>`.
6. **Read the result.** The tool prints `Done.`, the file path, and `Info`, `Note` or `Problem` lines.
   - **Problem about length:** follow `references/page-fit.md`. At most three passes, then tell the user honestly where it stands.
   - **Any other Problem:** the lines already explain it in plain English. Try the fix they suggest once. If it is still broken, read `references/troubleshooting.md`. Do not paste technical output at the user. Summarise it in one sentence and say what you will try.
   - **Note about a font:** relay it, with the two fixes.
7. **Look at every page yourself.** Before you call anything ready: render the pages to PNG with `node system/scripts/pages.mjs pdf <file.pdf>` and open each one with the Read tool (for a `.pptx` or `.docx`, export a copy to PDF first with `pages.mjs export`, which uses PowerPoint or Word when installed). Check the cover, the edges, half-empty boxes, fallback fonts, overlaps and legibility. A helper's "viewed all" is never evidence; you look. For a deck, view the PDF made with `--pdf`. If the PDF page renderer is missing or was declined in "Before you start", do not offer again mid-task: say which pages you could not check. For a CV or letter, also re-read the filled data against the fact sheet.
8. **Hand over.** Tell the user, in plain words:
   - where the file is (full path);
   - the page count against the limit;
   - one thing to check by eye (for example "open it and check the table on page 3").

   For a file the user must approve, add a task, unless the skill that called you already adds one (`/jobs apply` and `/assignment ship` do):
   `node system/scripts/tasks.mjs add "Review <document name>" --tag render --link "<vault-relative path to the source>"`
   Nothing is ever sent or uploaded from here.

   **Final version** (the user says it is final, or `/assignment ship`, `/jobs apply`): run the delivery gate, `system/deliverables/delivery-gate.md`, before you hand over. Then offer `/critique` once (not for routine emails or messages). For a deck the user has approved, offer the rehearsal pack once (`system/deliverables/rehearsal.md`).

## Outputs

- A PDF (or, for decks, an HTML file and optionally a PDF) in `_out/`, `releases/<today>/` or the folder you were given.
- Edited or new source files in the folder you chose: `cv-data.yml`, `letter.qmd`, `report.qmd`, `deck.qmd`, `references.bib`.
- A `#ab/render` task in `vault/00_inbox/Tasks.md` when the user needs to review the result.
- No temporary files are left behind. The tool removes the copies it makes.

## Safety

- **Draft only.** This skill makes files. It never emails, uploads, submits or shares them.
- **No invented facts.** A CV or letter contains only what is in the user's own files or what they confirmed in this conversation. Label anything uncertain `[Unverified]` in the chat and leave it out of the document until the user confirms.
- **Never edit the user's note, raw sources or `vault/40_sources/raw/`.** Render works on copies.
- **Never shrink the font, margins or spacing below the brief to hit a page limit.** If the brief does not allow it, cut words and say so.
- **Coursework.** Whether AI help is allowed on an assignment is handled by `/assignment` (the notice and the user's consent). Do not repeat or record it here. If `assignment.md` shows a course with `ai_policy` of `restricted`, `banned` or `unknown` and the user has not been warned, say so once and hand back to `/assignment`.
- **No secrets, no real people in templates.** Never put anything private into `system/quarto/`. That folder is shared framework code. User data lives in the vault.
- **Do not change framework files.** `system/quarto/**` is protected. Make the user's documents in the vault.
