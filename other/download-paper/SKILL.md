---
name: download-paper
description: Download the PDF of an academic paper (by DOI, publisher/doi.org URL, arXiv id, Anna's Archive md5, or title) with `paper-fetch`, the single paper-acquisition tool, including its browser fallback for challenge-protected hosts. Use whenever the user wants a paper, article, preprint or its PDF obtained, fetched, downloaded, saved or attached, even if they only paste a DOI or link, mention Anna's Archive, Sci-Hub, LibGen, PhilPapers or Unpaywall, or ask why a paper download failed. Not for books by ISBN or for creating bibliography entries alone (use add-bib-entry, which calls this for attachments).
---

# Download Paper

## Core rule

`paper-fetch` is the only implementation for obtaining a paper PDF. Do not write
a new downloader, call Anna's Archive or LibGen directly, or reach for
`annas-mcp`, `download-missing-pdfs.py --article-doi`, or Playwright. Every route
that works from a shell is already inside the tool, in the right order, with
identity verification; the skill's job is to run it, and to drive the one step it
cannot do itself: a real browser session for hosts that only answer a real
browser. Shared logic: `~/My Drive/dotfiles/lib/python/paper_fetch.py`.

## Procedure

1. Run the tool with a staging directory outside Drive. Use the citekey as
   `--name` when the paper is going into the bibliography.

   ```bash
   paper-fetch get "IDENT" --out "STAGING-DIR" [--name CITEKEY] [--author SURNAME]
   ```

   `IDENT` may be a DOI, a doi.org or publisher URL, an arXiv id, a 32-hex Anna's
   Archive md5, or a title (add `--author` to disambiguate a title). The tool
   resolves metadata through Crossref/OpenAlex, then tries open access (Unpaywall,
   OpenAlex, arXiv, publisher page), then LibGen -> Anna's Archive member fast
   download, then Anna's SciDB. It reads the Anna's Archive key itself; never pass
   or print a key or a signed download URL.

   Anna's Archive's only API is that member fast-download endpoint, which takes
   an md5; it has no search API, and the key does not unlock search. Going from a
   title or ISBN to an Anna's md5 therefore needs either LibGen (inside the tool)
   or Anna's `/search` in the browser. For books, that browser step is
   `paper-fetch book-candidates`'s `annas_browser_search` handoff
   (`docs/book-acquisition.md`, "Anna's Archive search").

2. Read `status` and act on it:

   | status | meaning | next step |
   |---|---|---|
   | `ok` (exit 0) | file staged and its text matched the requested title or DOI | use `file`; hand to `add-bib-entry` for attachment when wanted |
   | `needs-browser` (2) | the only remaining copies sit behind a bot challenge (PhilPapers, PhilArchive, Anna's HTML) | run the browser job below, then `paper-fetch collect JOB` |
   | `not-member` (3) | Anna's Archive answered "Not a member": the paid membership lapsed | tell Pablo; only he can renew. The md5 is in the message, so rerun with `--md5` after renewal |
   | `unavailable` (4) | every route failed | read `attempts`; a failed route is not proof the work is unavailable everywhere. Try `--author`, a DOI instead of a title, or a version (preprint vs published) |
   | `error` (1) | configuration problem (invalid key, quota, missing curl_cffi) | fix the cause named in `message` |

   A `verification.verdict` of `unverified-no-text` means a scanned PDF without a
   text layer: inspect the first page yourself before trusting it. `mismatch`
   files are deleted by the tool, never staged.

3. Browser job (`needs-browser`). The tool wrote `browser_job.path` (JSON) and one
   JavaScript snippet per origin. Use the session's Chrome control (Claude:
   `claude-in-chrome`; Codex: the Chrome plugin per `service-access.md`), in a tab
   you create, and follow this order for each origin — it matters:

   1. Navigate the tab to the *first item URL* of that origin (the PDF itself).
      The challenge page ("Just a moment…", "DDoS-Guard") clears on its own within
      about ten seconds; wait until the tab title changes. Opening the origin's
      home page is not enough: PhilPapers challenges `/archive/` separately.
   2. Navigate to the origin root (an HTML page, e.g. `https://philpapers.org/`).
      The snippet must run on an HTML document; Chrome's PDF viewer swallows
      anchor downloads.
   3. Read the snippet file and evaluate it in that tab (wrap it as
      `await (async () => { ... })()` if the tool needs a returned promise). It
      fetches each item with the cleared cookies and saves it through a normal
      Chrome download under the job's file name. It returns one small record per
      item: `saved` + `bytes`, or an HTTP `status`, or `md5_groups` for a SciDB
      page (eight-character hex groups of the record's md5; join them and rerun
      `paper-fetch get IDENT --md5 MD5` to download through the API instead).
   4. `paper-fetch collect "JOB.json" --out STAGING-DIR [--name CITEKEY]`. It
      finds the job's files in `~/Downloads`, verifies identity, installs the
      first verified file, and leaves anything else in place.

   If the snippet reports `saved` but `collect` says `no-downloads`, Chrome blocked
   the download: it allows one automatic download per site and then requires the
   "Automatic downloads" permission. Ask Pablo to allow it once for that origin
   (the blocked-download icon in the address bar, or
   `chrome://settings/content/automaticDownloads`), then rerun steps 3–4. This is
   a per-site, one-time browser permission; nothing else can substitute for it —
   bytes cannot be passed back through the tool result (encoded blobs are
   redacted) or posted to localhost (Private Network Access blocks it).

   If the snippet reports `403` for an item, the challenge was not cleared or has
   expired (clearance lasts roughly half an hour): repeat step 1 for that item.

   **Anna's Archive SciDB items** (`kind: scidb` or a DOI the API could not serve):
   open `https://<annas-host>/scidb/DOI/` in the tab and, once the page has
   loaded, click its **Download** link (`[...document.querySelectorAll('a')].find(a
   => a.textContent.trim() === 'Download').click()`). That is a plain navigation
   download from the partner server and works whenever the viewer would show the
   PDF. Two failure shapes are known and are not worth retrying: the page redirects
   to `/search` (no SciDB record), and the partner answers `404` for DOIs whose
   suffix contains `/` or `:` (`10.1093/mind/fzv208`, `10.1023/a:…`) because the
   partner path double-encodes the separator. For those, use the page's **Sci-Hub**
   link instead: on `sci-hub.ru/DOI` the PDF is the `object`/`embed`/`iframe`
   source; fetch it in-page and save through an anchor when it is same-origin, and
   when it lives on another Sci-Hub host (`sci-hub.red`, `sci-net.xyz`) navigate the
   tab to it and fetch from there. Sci-Hub shows an "Are you a robot? → No" gate
   once per session; that click is Pablo's, not the agent's. The extension refuses
   site-level permission for Sci-Hub hosts, so budget one approval per paper and
   do the whole fetch-and-save in a single JavaScript action per DOI.

   Chrome's automatic-download gate applies per site: the first download from
   `sci-hub.ru`, `sci-hub.red`, `sci-net.xyz` or an Anna's host lands, later ones
   are dropped silently until that site is allowed. Confirm each save in
   `~/Downloads` before moving on rather than trusting the snippet's `saved`.

4. Hand-off. A staged PDF is a file, not a bibliography attachment. When the paper
   belongs in the bibliography, continue with `add-bib-entry`, which imports the
   metadata and attaches the staged file through Ebib with the same operation.

## Batches

Run one identifier per `paper-fetch get`, in order; the tool is serial by design so
that Anna's Archive quota and challenge state stay legible. Group browser items by
origin: one cleared tab serves every item of that origin. Record per-paper
outcomes (status, route, file) so a rerun can skip successes.

## Failure reporting

Report the tool's `status` and `attempts` verbatim rather than a paraphrase.
"Every route failed" is the accurate summary of `unavailable`; "the paper is not
available" is not. Never present a `mismatch` or unverified file as the requested
work, and never substitute a related paper from a SciDB results page.

## Verification before finishing

- `status: ok` and `verification.verdict: verified` (or a manually inspected
  `unverified-no-text` scan), and the staged path exists and is non-empty.
- The first page's text names the requested title or DOI.
- Browser tabs you created are closed; nothing left in `~/Downloads` except files
  `collect` deliberately kept.
