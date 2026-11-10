---
name: grill-piece
description: "Grill the developer on a writing Piece: read its Supporting Material first, ask grilling.md's questions in rounds with drafted answers, then end with the calibration paragraph and an Outline for approval. /piece-spec files the result."
disable-model-invocation: true
---

Grill the developer on one Piece by the questions in [`docs/pieces/grilling.md`](../../../docs/pieces/grilling.md); read it in full first. The Piece words (Piece, Deliverable, Section, Outline, Supporting Material, Reference) are the writing [`GLOSSARY.md`](../../../docs/pieces/GLOSSARY.md)'s.

## 1. Opening round

Ask for two things, in one message:

- **The Deliverable**: the Google Doc's title and Doc ID.
- **The Supporting Material**: Drive file IDs, a Drive folder to search, or web page URLs.

An ID is always asked for, never guessed. For a folder, list it with the gworkspace tools and read the files found back to the developer, who strikes any that don't belong. Done when both are answered, each web page is saved to Drive and the file list is confirmed; section 2 can still send a saved page down the paste path.

**Every source is a Drive file**, read by its ID here and in every Workflow stage after the grill; a web page is saved to Drive in this round, and no later stage reads it live.

### Saving a web page

Fetch the page's own bytes with `curl`, the URL written out in the command so the sandbox sees its host ([the Bash sandbox](../../../docs/claude-code-guardrails.md#the-bash-sandbox)). Never use `WebFetch`: it returns a small model's answer about the page, not its text. Files go in `/tmp/claude/`, the one folder the gworkspace server reads local files from (`ALLOWED_FILE_DIRS` in [`scripts/setup-agent-account-mcp.sh`](../../../scripts/setup-agent-account-mcp.sh)).

1. **Fetch**: `curl -sSL --create-dirs -o /tmp/claude/<name>.page -w "%{http_code} %{content_type}\n" "<url>"`.
2. **A PDF**, whose first bytes `head -c 4 /tmp/claude/<name>.page` prints as `%PDF` whatever content type the site sent, is saved as that PDF, so it keeps its pages: `create_drive_file` with `fileUrl` `file:///tmp/claude/<name>.page` and `mime_type` `application/pdf`.
3. **An HTML page** becomes a Google Doc whose first line is the URL and the date fetched. Write `<p><url>, fetched <YYYY-MM-DD></p>` to `/tmp/claude/<name>-head.html`, join the two with `cat /tmp/claude/<name>-head.html /tmp/claude/<name>.page > /tmp/claude/<name>.html`, and import that with `import_to_google_doc`, `file_path` set to it and `source_format` `html`. Drive's conversion keeps the article's text word for word and some of its headings, which serve as locators; the page's menus and footer come too.
4. **The paste path**, when `curl`'s status isn't 200 or [section 2](#2-read-the-files)'s report finds the Doc holds little real text (a page built by scripts, a login wall, a paywall's teaser): say so, trash the Doc if one was made, and hand the developer the URL. They open it in a browser's Reader view, paste its text into a new Doc whose first line is the URL and the date, and give its ID.

Name each file for the page's title, and put it in the Supporting Material folder when the developer named one. Once a page is saved, `rm` its `/tmp/claude/` files. Its new ID joins the file list.

## 2. Read the files

**Short** is under about 10 pages. A Google Doc is sized by its Drive metadata: under about 30 KB is short. A PDF is downloaded and its pages counted, by [`docs/pdf-pages.md`](../../../docs/pdf-pages.md); one that can't be counted is long.

- **The short files go to one sub-agent together**, which reads each in full and returns, per file by title: what it is, every fact bearing on grilling.md's questions, and any of the developer's own text, quoted verbatim with where it lives.
- **Each long file gets its own sub-agent**, which reads only its table of contents and front matter and returns its chapters and sections with page ranges. A long PDF's sub-agent gets its local path and `docs/pdf-pages.md`, reads the first 20 PDF pages and more only while the contents run on, and gives each range as PDF pages with the printed pages beside them. One that finds the file short after all reads it whole and returns what a short-file sub-agent would.

A web page's Doc also gets a line saying whether it holds the article or little real text, which sends it down the paste path.

Dispatch them all at once, reads only, each told the file IDs and to cite by title and page. Done when every file has its report: its facts and own text, or its chapter list, and each pasted Doc that replaced a page has its own.

## 3. Ask in rounds

Call the Skill tool with "grilling" for its round format; the rounds rule here and this skill's done criterion win over that skill's. **Rounds rule**: every question whose answer doesn't wait on another goes in one round, and each voice question is asked alone, one at a time, so its answer stays in the developer's words; Temperature and Reach share one round. Ask the Long reads question against step 2's chapter lists: "which of these matter?"

**Before drafting, read the root's `docs/writing-voice.md` and `docs/writing-craft.md` with a Read that has no offset or limit, or a whole-file `cat`**, and for an Academic Piece `docs/academic-writing-style.md`, per [`docs/pieces/rules.md`'s Implementing a piece spec section](../../../docs/pieces/rules.md#implementing-a-piece-spec). Every draft in the grill, the calibration paragraph included, follows them.

Every question carries a recommendation:

- **A factual question's** is drafted from the files and cites the file it came from.
- **A voice question's**, one grilling.md names, quotes the developer's own text from Drive when one exists, cited. Otherwise it is a first draft labelled _draft, reword it_, given with the question, never on request. The developer rewords it or keeps it as drafted; either makes it their answer.

**Write a term settled in the grill into the writing glossary, `docs/pieces/GLOSSARY.md`, at once**, in its existing entry shape; that is the only file written before `/piece-spec`.

## 4. End

1. **The calibration paragraph.** Once the questions before it are answered, draft one paragraph in chat and have the developer rewrite it. Name each difference, then ask whether it holds for this Piece alone, which makes it a style override for the Style field, or for every Piece, which makes it a `/to-writing-style` candidate. In #1, one rewrite would have surfaced the name-not-pronoun, verdict-first and serial-comma habits before the full draft.
2. **The Outline.** Read [`docs/pieces/outlining.md`](../../../docs/pieces/outlining.md), then draft it from the settled facts for the developer's approval.
3. **Research, Final pass and Split**: ask grilling.md's three questions that wait on the Outline in one round once it is approved, so all ten [`/piece-spec`](../piece-spec/SKILL.md#1-fill-the-ten-fields) fields are settled.
4. **The `/to-writing-style` candidates**: list each difference that holds for every Piece in chat, unwritten, for that skill's approval.

5. **Delete the PDFs step 2 downloaded**, by the paths it got back; each later stage downloads the ranges it reads.

Done when every grilling.md question has an answer (the developer's words, or a draft they kept) or the developer's waiver, the calibration paragraph is rewritten, the Outline is approved, the candidates are listed and the downloads are gone. End by recommending `/piece-spec <repo>`, `<repo>` being the one that files the spec.
