---
name: food-fetch
description: "Lawfully acquire the full text of academic articles so the research and review skills can read papers, not just abstracts. Routes each article through legal open access (Unpaywall/OpenAlex/PMC/arXiv), the user's own reference-manager library (EndNote/Zotero/Mendeley PDFs), and — only with the user's own logged-in institutional browser session — their library's entitled full text, then extracts the text and writes a manifest of what was and was not obtained. Open-access articles are always downloaded and read, never left at abstract-level. Never bypasses paywalls, DRM, or logins. Use to fetch PDFs for a reference list or DOIs, get full text behind a subscription the user is entitled to, or build a full-text corpus. Triggers: download these papers, get the full text, fetch the PDFs for these DOIs, retrieve full text for my reference list, access the article through my library, build a full-text corpus."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  subagents: [fetch_coordinator, access_router, oa_fetcher, library_fetcher, institutional_fetcher, content_reader]
  related_skills: [food-research, food-deep-research, food-review, food-paper, agri-research, agri-review]
  references:
    - references/access-routing.md
    - references/institution-profiles.md
    - references/institutional-access.md
    - references/format-reading.md
    - references/manifest-and-status.md
    - references/boundaries.md
---

# Food-Fetch — Lawful Full-Text Acquisition

Turn a list of references or DOIs into **read full text**, so `food-research`,
`food-deep-research`, and `food-review` build their knowledge base from the actual
papers rather than abstracts. Original work; the routing/manifest architecture is
informed by the open-source `nature-downloader` skill (see the repo README
Acknowledgements). Legal-access-only, and **it never fabricates** — a paper that was
not obtained is recorded as not obtained, never summarized as if read.

## First-run setup — ask once, remember, remind if skipped
On the **first** run that needs full text, help the user set up access — this is what
decides whether the review reads real papers. Check
`python3 scripts/food_fetch_setup.py status` (exit 3 = not set up):

- If **not set up**, surface a **highlighted request** offering the choices, then save
  the answer so it isn't asked again:
  > 📚 **Set up full-text access (one-time).** To read papers, not just abstracts,
  > pick one:
  > 1. **Reference-manager library** — send the path to your **EndNote `.Data`
  >    folder** (or Zotero `storage/` / Mendeley). Best coverage for cited work.
  > 2. **Institutional access** — I'll reach entitled full text through **your own
  >    logged-in library session** in the browser when needed.
  > 3. **Open access only** — no setup, but see the warning below.
  >
  > ⚠️ **Without access to non-open-access articles, the accuracy of the results is
  > substantially limited** — most published papers are paywalled, so the knowledge
  > base and every claim's grounding would rest on abstracts + the ~half of literature
  > that is open access.

  Save the choice: `food_fetch_setup.py set --library <path>` / `--institutional` /
  `--open-access-only`.
- If **already set up** (exit 0), use the saved mode silently — **do not re-ask**.
- If the saved mode is **`open_access_only`**, **remind** at the start of each
  full-text run — briefly, once — that non-OA access is not configured and that this
  **substantially limits accuracy**, and offer to switch (options 1–2). Don't block;
  proceed at open-access + abstract level.

The store holds only a folder path and a mode — **never** a password, cookie, or token.

## Access ladder (each article, in order) — see `references/access-routing.md`
1. **Open access** — resolve a legal free PDF (Unpaywall → OpenAlex; PMC/Europe PMC
   full text; arXiv/preprints) and **download it**. `oa_fetcher` runs
   `scripts/fetch_oa.py`. **Open-access full text is always fetched and read — never
   left at abstract-level.**
2. **The user's reference-manager library** — `library_fetcher` reads the PDFs the
   user already downloaded in **EndNote** (`<Library>.Data/PDF/`), **Zotero**
   (`storage/`), or **Mendeley**, mapping each reference by DOI/title. Read-only.
3. **The user's entitled institutional access** — `institutional_fetcher` reuses the
   user's **own logged-in library session in the browser** (Claude-in-Chrome) to open
   the article through their library resolver / EZproxy / Shibboleth-CARSI / WebVPN
   and save the entitled PDF. **User-driven login only.** See
   `references/institutional-access.md`.
4. **User-supplied PDFs** — anything the user drops in the project folder.

If none reaches it, the article is `oa_not_found` / `library_no_permission` — the
user is told plainly, and the source stays unread (not summarized).

## Subagents (dispatch via the Agent tool)
1. **`fetch_coordinator`** — takes the reference list / DOIs, confirms the **Supporting Information** choice once, runs the batch, and returns the manifest + a plain summary of read vs unread.
2. **`access_router`** — per article, normalize the DOI/title, detect open-access vs paywalled and publisher, and choose the ladder step (`references/access-routing.md`).
3. **`oa_fetcher`** — download every open-access PDF via `scripts/fetch_oa.py`; verify each is a real PDF (`%PDF`); record source + SHA-256.
4. **`library_fetcher`** — match references to PDFs in the user's reference-manager library folder and read them (read-only).
5. **`institutional_fetcher`** — with the user's own browser session, reach the library-entitled full text and save the PDF; hand off to the user for any login/CAPTCHA/2FA (`references/institutional-access.md`).
6. **`content_reader`** — normalize each obtained article (XML/HTML/PDF) into clean sectioned full text, **preferring structured JATS XML over scraped PDF** (`references/format-reading.md`); never treat an abstract or a login page as the paper.

## Deliverable — a coverage manifest (`references/manifest-and-status.md`)
Always return one manifest listing **every** requested reference with a typed status
(`open_access_downloaded` · `library_pdf_read` · `institutional_downloaded` ·
`oa_not_found` · `library_no_permission` · `pdf_fetch_failed` · `not_a_pdf`), its
access route, and file/SHA-256 where downloaded — plus a one-line count of how many
were read in full vs not. This is what makes the review's grounding honest and
auditable. Run `scripts/privacy_scan.py` on anything delivered.

## Boundaries (non-negotiable) — `references/boundaries.md`
Lawful access only: legal OA, the user's own library files, and the user's own
authorized institutional session. **Never** bypass a paywall, DRM, or 2FA; never read,
type, export, or ask for passwords / cookies / OTP codes / session tokens; never
scrape against a site's terms; no bulk/indiscriminate downloading — only the confirmed
list. For a login or verification challenge, hand the browser to the user.

## Called by
`food-research` (`screener_appraiser`/`data_extractor`), `food-deep-research`
(`investigator`/`source_verifier`), and `food-review` (`knowledge_builder`) call
food-fetch to obtain full text before extracting; the `agri-*` skills via delegation.
