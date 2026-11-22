---
name: release-cross-check
description: "Release-time six-point cross-check for EISS: the roadmap, sitemap, translations, repo docs, Anthology abstract-coverage and team-announcement surfaces (the For the team note, the dashboard release card, the EISS release notes email, the news item) to verify before cutting a minor or major release, plus milestone hygiene. Use when cutting a release, running scripts/release.sh, or asked what to check before a release. Skip for patch releases."
---

# 5. Release-time six-point cross-check (minor / major only)

Every **minor (`X.Y.0` where `Y > prev`) or major (`X.0.0`)
release** should trigger a deliberate check across six surfaces
before `scripts/release.sh` runs. Skip the cross-check on **patch
releases** (`X.Y.Z` where `Z > 0`); they're scoped to small fixes
and the overhead isn't justified. The release script's
*self-policing tier* mirrors this: patches ship the index only.

For each surface, the question is the same: *"Did anything in this
release change what this surface documents?"* If yes, edit in the
same release. If yes but too big to fit, open a tracking issue
(rule §3) and reference it from the surface itself.

### 1. Roadmap (`/roadmap.html` + FR + DE + `docs/roadmap-2026.md`)

- Is the next planned release on the *At a glance* timeline still
  accurate? Do the version milestones and their due dates match it?
- On the public `/roadmap.html` (+ FR + DE), flip the card for the
  release just cut from *Planned* / *In progress* to *Shipped*: set
  its date, add the release-notes link, and drop the `data-milestone`
  attribute so it no longer renders a progress bar. The next planned
  card is auto-promoted to *In progress* by `roadmap-progress.js`.

  **`scripts/release.sh` now offers to do this**, showing the diff and
  applying it only on an explicit `y` (#280). To do it outside a
  release, or to check what it would change:

  ```bash
  node scripts/flip-roadmap-card.mjs v2.27.0            # dry run
  node scripts/flip-roadmap-card.mjs v2.27.0 --write
  ```

  It edits `src/_data/roadmap.js`, which the three locale pages render
  from, so one command covers EN, FR and DE. The dates come from the
  same `Intl` formatter the news surface uses, so a flipped card reads
  identically to a hand-written one. Still eyeball the rendered page:
  the script guarantees the data is right, not that the prose around
  it still is.
- Anything in the *Under watch* section ready to promote to a dated
  release row (and its own milestone)?
- The autostamp on `docs/roadmap-2026.md` (rule §11) keeps the
  `[Unreleased]` bullet count fresh automatically. The prose timeline
  rows and the public cards stay maintainer-edited.

### 2. Sitemap (`src/sitemap.xml.njk` + `src/sitemap.njk` + FR + DE)

- New pages added in this release? Confirm they show up in
  `src/sitemap.xml.njk` (the XML index for search engines) and in
  the visual `src/sitemap.njk` inventory + its FR / DE siblings.
- The visual sitemap is hand-edited; confirm new pages land in the
  correct branch (*About* / *Programmes* / *Conferences* / etc.).

### 3. Translations (FR + DE variants)

- Run `python3 scripts/check-i18n-drift.py` locally. CI catches drift
  on HTML-touching PRs, but a release moment is the right place to
  confirm zero drift before stamping a version.
- Did any EN copy change in this release? FR / DE need updating
  (machine translation is fine, and merging the PR approves it, per rule §1).
- The `status: beta` ribbon on `*.fr.njk` / `*.de.njk` says the English
  version is authoritative. It is not a review flag. Dropping it from a
  page is a maintainer decision.

### 4. Repo docs

- Maintainer-facing markdown docs under `docs/`
  (`board-bios-setup.md`, `i18n.md`, `indico-api-token.md`,
  `indico-programme-integration.md`, `new-conference.md`,
  `roadmap-2026.md`): does anything in this release contradict what's
  documented?
- `BRAND.md` and the brand SVGs under `src/assets/images/brand/`:
  refresh if the visual identity changes.
- The documentation pack (`docs/pdf/EISS-website-documentation.pdf`,
  source `docs/pdf/documentation.html`, built by `docs/pdf/build.sh`).
  Minor / major releases only, patches skip it. Same two-tier cadence as
  NetSec's pack:
  - **Cover bump** on every minor / major: update the website version and
    the pack version on the cover, and add an Appendix C entry. Deferring
    the section-level catch-up is fine if that entry says so.
  - **Section-level catch-up** every two or three minor releases: refresh
    the page graph, feature inventory and pipeline tables, and re-capture
    the screenshots with `./docs/pdf/build.sh --shots`.
  - After any rebuild, check the contents page numbers against the PDF:
    they are typed by hand. Figures stay JPEG at device scale 1 (the NetSec
    pack reached 24.6 MB on full-resolution PNGs).

### 5. Abstract coverage (Anthology)

- Run `node scripts/check-abstract-coverage.mjs`. It lists every paper
  abstract that fails to attach to an Anthology paper, by year, with the
  closest programme title and a similarity score. A high score is title
  drift; a low score means the paper is absent from the programme (or is a
  panel-level abstract, which correctly matches nothing). Informational, not
  a gate. The `abstract-coverage.yml` workflow also runs it every four months
  and files a tracking issue if it finds likely drift, so this is a backstop
  more than a chore.
- Reconcile drift one of two ways. If the **programme** title is the one to
  keep (correct British spelling, or a clean version of a garbled Indico
  title), add the synced→programme mapping to
  `src/_data/paperAbstractAliases.json`. If the **programme** has the typo,
  fix it in `src/_data/archiveProgrammes.js`.
- Abstracts the sync can't pull live in `src/_data/paperAbstractsManual.json`,
  never in `paperAbstracts.json` (the sync overwrites the latter wholesale, so
  anything hand-added there is silently dropped on the next run). Two cases:
  pre-Indico editions (2022 and earlier), and **subcontribution-level
  abstracts** — papers run as subcontributions of a panel. Indico's export API
  does not expose subcontribution descriptions at any detail level or auth
  (confirmed by `scripts/probe-indico-subcontribs.py`), so those paper
  abstracts must be hand-added here from the organisers' files.

### 6. Announcements (the "For the team" note and where it goes)

The release notes reach people beyond GitHub. Four places read them,
and the first three need nothing done by hand once the release exists:

- **The release card on `/internal.html`**, built by
  `src/_data/latestReleases.js` from the newest released section of
  `CHANGELOG.md`. It shows for 14 days after a minor or major release,
  or a patch whose notes have `### For the team`. It shows that section,
  or the lede when there is none, at most three paragraphs, with links
  reduced to their text.
- **The release email**, sent by the "EISS release notes" Apps Script
  project (`workspace-ops/release-notes`, admin@, daily early-morning
  trigger). It reads `releases.atom`, so it goes out the morning after
  the GitHub Release is published, from "EISS releases" with no reply
  address. Subject: `EISS website vX.Y.Z: <title>`. A minor or major
  goes to staff@, internship@ and board@, a patch with "For the team" to
  staff@ and internship@, a patch without it to nobody. A release more
  than 14 days old is never sent, and each release is sent once. Its run
  stamps "Release notes" in the "EISS system status" Sheet.
- **The NetSec card** on the same dashboard, from NetSec's latest GitHub
  Release. A NetSec release follows the same rule and the same email.
- **A news item**, by hand. After a minor, `release.sh` asks whether the
  release brings a feature visitors can see. If it does, file the News
  item form with Newsletter ticked (`docs/news-publishing.md`): it goes
  to the site, the feed, LinkedIn and Bluesky after the `social`
  approval, and the next newsletter. The What's New banner is a separate
  decision (the `whats-new-banner` skill).

Before running `release.sh`, check:

- `[Unreleased]` has `### For the team` after the lede, with its heading
  spelt exactly that way, in English. Both readers match the heading
  text.
- The note reads on its own under the release title, as the email and
  the card show nothing else. Whatever the title names should appear in
  the note. Write it for staff, the board and volunteers, who are not
  developers: plain sentences, no file paths, no issue numbers. Two to
  four sentences in one paragraph.
- The note says nothing that board@ should not read, since a minor goes
  to the board.
- The title is final. It is the card's heading, the email subject and
  the GitHub Release name, and none of them changes after the email has
  gone.

To preview both, promote a copy of `CHANGELOG.md` the way `release.sh`
does, then feed it to `card()` in `latestReleases.js` and the rendered
section to `noteOf_()` and `message_()` in `release-notes/Code.gs`.
`node test.mjs` in that folder covers the parser.

After the release, check the next morning that the email arrived and
that "Release notes" in the status Sheet is green. The card appears on
`/internal.html` with the deploy of the release commit.

### 7. Milestone hygiene (gate, not a surface)

- Every issue closed by this release carries the matching milestone.
- Every issue still open and tagged with a milestone that just shipped
  has either been ticked off in the release notes or moved to the
  next milestone with a one-line reason in the issue thread.
- The release should not ship with its own milestone holding open work.
  Publishing the release closes its milestone (`close-milestone.yml`).
  If work is still open the run fails and the failure alarm files an issue.
  See rule §10.

This is a deliberate friction-point: cutting a minor release here is
**slightly more work than running release.sh**, by design. The
release script's confirmation prompt is the last moment to bail if
the cross-check surfaces something that needs to land in the same
release.
