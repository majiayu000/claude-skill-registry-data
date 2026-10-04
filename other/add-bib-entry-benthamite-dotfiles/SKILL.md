---
name: add-bib-entry
description: Use when adding works to Pablo's bibliography, creating BibTeX/BibLaTeX entries, adding DOI/ISBN/URL references, resolving missing citekeys, replicating zotra-extras-add-entry followed by ebib-extras-process-entry, or preparing notes that cite works not yet in the configured bibliography files.
---

# Add Bib Entry

## Core Rule

Use Pablo's Emacs bibliography workflow, not ad hoc BibTeX, whenever a work has a DOI, ISBN, URL, or other identifier. The canonical sequence is `zotra-extras-add-entry`, then `ebib-extras-process-entry`. Manual use selects the imported entry; agent use passes the entry key and database explicitly. The agent should carry out both steps, including downloading and attaching the paper; do not stop after metadata import. The desired end state is a clean BibLaTeX entry plus obtainable associated files: PDF/HTML for written works and subtitles for videos. Import success alone does not establish correct metadata or attachment completion.

Read [the shared bibliography policy](../../../agents/bibliography-policy.md)
before selecting a work/edition, reviewing fields or accepting an attachment.
That document owns these decisions; this skill owns how to apply them through
Emacs. For whole-note source cleanup, use `clean-citations`.

Use `/Users/pablostafforini/My Drive/dotfiles/bin/emacs-eval` for ad-hoc live
expressions. It bounds results before Emacs prints them and reports truncation;
it does not make expensive computation safe or cancel server work after a
client timeout. Export complete selected-entry data to a private file. When
writing native `json-serialize` output into a multibyte buffer, decode its UTF-8
bytes first; use UTF-8 for the file. Do not change global coding settings.

## Workflow

1. Establish the intended work and first edition under the shared policy, then check whether it is already present.
   - Prefer `search_bibliography` if available.
   - Otherwise search active bibliography files with `rg -n -F -- "IDENTIFIER" BIBFILE...`, then check title/author and alternate identifier forms. Reuse a matching work's existing key; distinguish editions/versions before creating a duplicate.
   - Get active paths from Emacs rather than guessing:
     ```bash
     "/Users/pablostafforini/My Drive/dotfiles/bin/emacs-eval" '(progn (require '\''paths nil t) (mapcar (lambda (symbol) (cons symbol (and (boundp symbol) (symbol-value symbol)))) '\''(paths-file-personal-bibliography-new paths-file-personal-bibliography-old paths-files-bibliography-all citar-bibliography)))'
     ```

2. Choose the target BibTeX file.
   - For Pablo's personal notes, default to `paths-file-personal-bibliography-new`, normally `/Users/pablostafforini/My Drive/bibliography/new.bib`.
   - Do not add new personal references to `old.bib` or Babel/Tlön bibliography files unless the user or project context explicitly calls for that.
   - Resolve the actual target and active databases before writes. If Emacs is unavailable or paths are unset, diagnose that gap; the usual path is not evidence of the current configuration. Do not restart/signal Emacs or silently switch workflows.
   - Check for unsaved changes in the target's visiting buffers and loaded Ebib database before importing or reloading. Reconcile them without discarding or saving unrelated user edits; stop this addition if that cannot be done safely.

3. Add and process the entry through Zotra/Ebib.
   - If you need to inspect or reload an Elpaca package involved in this workflow, resolve it with `"/Users/pablostafforini/My Drive/dotfiles/bin/elpaca-package-path" PACKAGE`. For Anna's Archive source append `annas-archive annas-archive.el` to that quoted executable. Do not use `locate-library`, `symbol-file`, or `~/.emacs.d/elpaca/...` as the source authority.
   - Manual/full workflow: run `zotra-extras-add-entry` in Emacs. It imports metadata via Zotra/Zotero translators, prompts for the target bibfile, opens the entry in Ebib, and then runs the Ebib processing path.
   - Headless/agent workflow: import metadata with `gptel-extras-add-bib-entry` (the `add_bib_entry` tool), after `gptel-extras--bib-import-preflight` on the explicit target. Load that key with `gptel-extras--open-bib-entry-for-processing` and review all imported fields under the shared policy before attachment. For DOI articles and books use the staged-download sequence below; for webpage/video routes process the SAME existing key with `gptel-extras--process-bib-entry-headless`. Never reimport merely to invoke `add_bib_entry_and_process`. The combined helper remains available for already-reviewed straightforward identifiers; it does not replace final field review. Retain the explicit DB and operation across callbacks and do not start competing downloads.
   - Metadata-import template (transport identifiers/paths as escaped Lisp strings through an argument vector, not shell interpolation):
     ```bash
     "/Users/pablostafforini/My Drive/dotfiles/bin/emacs-eval" --timeout 60 '(progn (require '\''gptel-extras) (require '\''zotra-extras) (require '\''ebib-extras) (gptel-extras--bib-import-preflight "RESOLVED-BIBFILE") (gptel-extras-add-bib-entry "IDENTIFIER" "RESOLVED-BIBFILE"))'
     ```
   - Programmatic Emacs calls must not select an Ebib entry, launch a viewer/browser or prompt. Use explicit entry/database and noninteractive operation policy. Inspect extracted text and rendered page images with agent tools; this does not require opening the user's PDF viewer. Browser acquisition, when needed, uses the mapped browser workflow. Manual commands retain their interactive behavior.
   - The headless helper calls the actual `ebib-extras-process-entry` without rebinding global input functions. It preserves an existing abstract and reports missing language, ambiguous choices, destination collisions or conflicting edits as blocked results instead of prompting. Inspect the document and candidate metadata to resolve ordinary choices yourself; ask Pablo only when his preference is needed. Preserve unrelated user edits.
   - Process one addition at a time. Poll `(ebib-extras-operation-status-for-id "OPERATION-ID")` while its `:pending` count is positive, including after the initial wait expires. A timeout, an existing file or an unrelated process finishing does not establish completion. `:status complete` with zero pending tasks is the operation's completion state; `blocked` includes the reason in `:errors` and can still have callbacks draining. After those callbacks finish and the cause is resolved, retry the SAME existing entry with a NEW operation through `(gptel-extras--process-bib-entry-headless TIMEOUT KEY DB)`. Do not reimport or reuse the failed operation. Re-read the final database and verify its attachments.
   - `add_bib_entry` is metadata-only: it deliberately passes `DO-NOT-OPEN` to `zotra-extras-add-entry`, so it does not run Ebib post-processing or attach files. Use it as the first phase for metadata review and staged PDF acquisition below, and carry the remaining attachment and processing phases through. Otherwise use it only when the limited outcome was requested, or as a clearly labeled, justified and approved fallback.

4. Complete post-processing.
   - The full manual path calls `zotra-extras-open-in-ebib`, which confirms the entry type/key and invokes `ebib-extras-process-entry`.
   - `ebib-extras-process-entry` regenerates/validates the key, sets language, calls `ebib-extras-attach-files`, and checks crossrefs.
   - `ebib-extras-attach-files` chooses attachments from DOI, ISBN/book type, video URL, or online/article URL:
     - DOI: searches/downloads through Anna's Archive. This is the configured paper-download route; Sci-Hub is not a second implemented backend. Do not claim to have used it.
     - ISBN/book-like entries: the legacy Emacs route searches Anna's Archive but does not enforce the shared book policy. Agent additions use the staged book route below before running this function.
     - Video URLs: obtains subtitle files, not a paper PDF.
     - Online/article URLs: generates PDF and HTML files with `eww-extras-url-to-file`.
   - Manual Anna's Archive downloads may use the external browser. The noninteractive route reports a blocked result when it cannot complete unattended. If the returned file list is empty or incomplete, inspect the `file` field and this operation's status. Match a candidate in Downloads/library by work identity and job evidence, never merely by recency. An existing but stale `file` field can prevent normal attachment; diagnose it rather than repeatedly importing the work.
   - Read `/Users/pablostafforini/My Drive/dotfiles/claude/context/service-access.md` before direct service access; its mapped paper route is `paper-fetch`. Read `/Users/pablostafforini/My Drive/dotfiles/claude/context/secrets.md` before any credential-backed action. Do not print credentials or signed download URLs.
   - For article PDF downloads, use `paper-fetch` (dotfiles `bin/`; shared logic in `lib/python/paper_fetch.py`) with a fresh staging directory outside Drive. The `download-paper` skill documents its routes, statuses and browser fallback. Keep Zotra/Ebib responsible for metadata and attachment; diagnose an unavailable Emacs session before changing bibliography state:
     ```bash
     paper-fetch get "DOI-OR-URL" --out "STAGING-DIRECTORY" --name "CITEKEY"
     ```
     It downloads files only: it does not import metadata or update `new.bib`. It reads the Anna's Archive key itself; never pass a key on the command line. `status: ok` means the file exists and its text matched the requested title or DOI; `needs-browser` means only challenge-protected hosts hold a copy (follow `download-paper`); `not-member` means the Anna's Archive membership lapsed; `unavailable` means every route failed, which is not proof that the work is unavailable everywhere. Diagnostics omit credentials and signed URLs; do not reconstruct or print them while investigating errors.
   - For books, read [book acquisition](references/books.md). It uses `paper-fetch` candidate search, explicit staging and hash-bound reviews, then the same Ebib attachment operation below. Do not use the website script's BibTeX writer or accept the legacy Emacs single-candidate choice as an editorial review.
   - For a PDF obtained through `paper-fetch`, a publisher/author source, or another authorized route, inspect its title, authors, DOI, version and language before attaching it. Load and validate the intended entry/database in the background with `(gptel-extras--open-bib-entry-for-processing bibfile key)`, set `langid` to the verified document language, and save those owned metadata changes before creating the operation. Do not assume every paper is English. Capture that DB once and pass the SAME operation through attachment and processing:
     ```elisp
     (let ((operation (ebib-extras-make-operation key db t)))
       (condition-case nil
           (progn
             (ebib-extras-attach-file staged-pdf key t db operation)
             (gptel-extras--process-bib-entry-headless 45 key db operation))
         ((error quit)
          (ebib-extras-operation-status-for-id
           (ebib-extras-operation-id operation)))))
     ```
     Do not reopen/reload the database between these calls: delayed work retains the original entry object. Follow the returned operation until all attachment, abstract and OCR tasks finish. Save and verify through Ebib; do not hand-edit `new.bib` or select the most recent download as a substitute for attachment.
     Attachment errors are recorded and re-signaled; the handler above retains the operation ID even when callbacks remain pending. For retries, inspect which phases finished. If installation failed, retry the staged attachment with a new shared operation; successful installation moves the staged file, so check its path before reuse. If post-processing failed after installation, resume that unfinished phase on the attached PDF. Processing an entry alone does not reinstall a staged file or rerun OCR.
   - Re-read the generated entry and do targeted metadata cleanup only for fields the programmatic path missed:
     - For ordinary text fields, use `ebib-set-field-value` with explicit key/DB and normal bracing, then mark the DB modified and save through `ebib-extras--save-database`. The lower-level `ebib-db-set-field-value` stores raw BibTeX syntax and does not add braces. Preserve the dirty-state checks above and verify the saved entry parses back to the same field values.
     - Apply the shared policy to all fields, including previously nonempty abstracts. `ebib-extras-process-entry` assumes most metadata correct, and its abstract path preserves nonempty content; operation completion is not field acceptance. Correct wrong values through Ebib. If removing an invalid abstract, obtain a valid source/document-grounded replacement when feasible and review what callbacks finally saved.
     - Export only the selected entry as JSON `{"entrytype":"book","key":"ActualKey","fields":{...}}` with parsed field values. Run `bin/bib-entry-check ENTRY.json --parents PARENTS.json` (omit parents when absent), using the absolute dotfiles tool path. Run `--check-files` for structural attachment checks. Supply each explicitly resolved parent entry; do not infer it from a cache hit.
     - Resolve structural errors and separately record the policy's semantic review. Re-run on the saved entry after callbacks finish. `--describe` exposes the machine rules; a zero exit certifies only structure, never edition choice, abstract quality or attachment identity.

5. Use the returned/generated citekey in notes.
   - Cite as `[cite:@Key]`.
   - After editing notes, verify every citekey resolves in the active bibliography files.

## Fallbacks

- If Zotra cannot import the work, inspect the relevant implementation before hand-writing BibTeX:
  - `/Users/pablostafforini/My Drive/dotfiles/emacs/extras/zotra-extras.el`
  - `/Users/pablostafforini/My Drive/dotfiles/emacs/extras/ebib-extras.el`
  - Anna's Archive download behavior: run `"/Users/pablostafforini/My Drive/dotfiles/bin/elpaca-package-path" annas-archive annas-archive.el` and inspect the returned file.
  - package docs in `/Users/pablostafforini/My Drive/dotfiles/emacs/extras/doc/zotra-extras.org` and `ebib-extras.org`
- Manual BibTeX is acceptable only for genuinely unsupported cases, after the Zotra/Ebib path and relevant implementation have been inspected and the labeled fallback is justified and approved. Preserve the shared policy, structural validation, valid key style and citation resolution.
- Exhaust available in-scope agent paths before declaring an attachment blocked. If a credential, unavailable live session or genuinely ambiguous candidate still prevents completion, preserve the entry and report the exact missing piece. Do not substitute a different work or claim the attachment is complete.

## Verification

Before finishing:

- Re-read the added BibTeX entry and cited note lines. Require structural validation plus explicit semantic review against the shared policy.
- Confirm the citekey appears in one active bibliography file.
- Confirm every expected `file` field resolves to the intended nonempty PDF/HTML/subtitle file, and inspect content identity rather than trusting its name or extension. Reconcile unfinished attachment callbacks before reporting completion.
- Check both disk and the active Ebib/visiting buffer after any approved external edit; do not overwrite unsaved edits to force them into agreement.
- Keep unrelated user changes in bibliography files unstaged/uncommitted unless explicitly asked.
- If committing, commit bibliography and note changes separately when they live in different repos.
