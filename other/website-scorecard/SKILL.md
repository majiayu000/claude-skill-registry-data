---
name: website-scorecard
description: >
  OPTIONAL public scorecard: publish what a site's own test gate checked, as a
  dated section on one page. `npm run scorecard` runs the whole suite and writes
  scorecard.json (checks passed per area, pages, date, tested version); a
  component renders it and tells the reader when the site was edited after the run.
  The owner can add the four Lighthouse scores of a PageSpeed run, with a re-run
  link. A red run writes nothing, so a card never shows a failed run as passed.
  Never runs unasked: publishing test results is the owner's choice. Ships an
  opt-in tests/scorecard.spec.ts. Trigger phrases: "publish our test results",
  "public scorecard", "quality report", "show the Lighthouse scores on the site",
  "proof the site is tested", "update the scorecard". Not a performance audit
  (website-qa) and not an SEO report (search-console-insights).
---

# Website scorecard

A site built with this kit carries a test gate. This skill lets the owner **show**
what it found: one section on one page, generated from a real test run, dated,
and honest about its age. It is optional and it is the owner's decision. Never add it
unasked: a public page that reports on the site's quality is a statement the owner makes.

## The offer (what to say to the owner)

Say it in the owner's language, in plain words:

> Your site comes with automatic checks: accessibility, links, search data, wording
> and more. I can add a short "Quality checks" section to one page that shows the
> results of a run, with the date and the version they were measured on. If you have
> run Google's PageSpeed test on the live site, its four scores go next to it, with a
> link so any visitor can run the same test. If the site is edited later, the section
> says so by itself until we run the checks again. Do you want that, and on which page?

Options: **Yes, on `<page>`** / **No (default)**. No answer means no.

## 0. When it runs

- Only when the owner asks, or says yes to the offer above. `new-website` copies this
  skill into every site so that day's session finds it; nothing in the pipeline runs it.
- The suite must be green first (`website-qa`). The script refuses otherwise.
- The Lighthouse scores need the **live** site, so they usually come after launch. The
  test-gate half works before that.

## 1. What it adds to the site

| File | From this skill's `templates/` | What it is |
|---|---|---|
| `scripts/scorecard.mjs` | `scorecard.mjs` | runs the suite and writes the card |
| `src/components/Scorecard.astro` | `Scorecard.astro` | renders the card; English and German built in |
| `tests/scorecard.spec.ts` | `scorecard.spec.ts` | the page shows the file's numbers; the file adds up. Needs the script: install all three, never this file alone |
| `scorecard.json` (project root) | written by the script | the card itself, committed like any other file |

The templates are in this skill's `templates/` folder, beside this SKILL.md; the bundled
copy of the skill on a handed-off repo has them too (`.claude/skills/website-scorecard/templates/`
or `.agents/skills/…`).

## 2. Install (on a branch, as a pull request: `AGENTS.md` §2)

1. Copy the three files to the places in the table above.
2. Add the command to `package.json` → `scripts`: `"scorecard": "node scripts/scorecard.mjs"`.
3. Put the component on the page the owner chose, inside that page's `<Base>`:
   ```astro
   ---
   import Scorecard from '../components/Scorecard.astro';
   ---
   <Scorecard />
   ```
   An existing page (About, or the foot of the home page) needs nothing else. A **new**
   page for it is a new page: work through `AGENTS.md` §6 (`PAGES`, `llms.txt`, share
   card, a link to it).
4. In `tests/scorecard.spec.ts` set `PAGE` to that page's address (`'/about'`).
5. Language. The section speaks the site's one language (`SITE.locale`), or on a site
   with several languages (`astro-i18n-setup`) the language of the page it is on
   (`Astro.currentLocale`); `<Scorecard lang="de" />` overrides both. English and German
   are built in. Any other language: add its texts to `TEXT` in the component, next to
   `en` and `de`. The tone rules apply to them (`tests/tone.spec.ts`).
6. Commit. The working tree has to be clean for the next step.

## 3. Generate the card

```bash
npm run scorecard        # runs the whole suite, writes scorecard.json
git add scorecard.json && git commit -m "scorecard: test run of <date>"
```

- Uncommitted changes → it stops and says so. The card describes a commit.
- Any failed or flaky test → it writes **nothing** and names the area. Fix the test, run
  it again. Do not edit `scorecard.json` by hand to get past this, ever.
- A skipped test is counted and shown as "not applicable yet" (on a new site: the
  positioning check, until terms are declared). It is not hidden.
- The card's own spec is left out of its numbers, and sits out while a new card is
  written: the card is about the site, and a wrong card must not block its own repair.
- A test file that cannot even load counts as red, and so does a stray `test.only`.

Then `npm test` once more: with the file present, `scorecard.spec.ts` now checks the
page against it.

## 4. Lighthouse scores (the owner's step)

The script does not fetch them: Google's PageSpeed API refused a request without a key
("quota exceeded") when this skill was written, and a key would be one more thing for
the owner to set up. Ask the owner, as `website-qa` §2 does:

> Please run https://pagespeed.web.dev/ on your live home page (mobile) and send me the
> four numbers at the top: Performance, Accessibility, Best Practices, SEO.

```bash
# the owner's four numbers, in this order, and the day of the run
npm run scorecard -- --lighthouse <performance>,<accessibility>,<best-practices>,<seo> --date <YYYY-MM-DD>
git add scorecard.json && git commit -m "scorecard: Lighthouse scores of <date>"
```

A desktop run: add `--strategy desktop`. The date must be a real day, not in the future.

Record what the owner measured, exactly. The section links to the same test for the
site's own address, so a visitor who re-runs it sees whether the numbers hold. Never
enter a score nobody measured (`AGENTS.md` §4: invent nothing). No scores given: leave
them out; the section works without them.

## 5. Publish

The section goes live the way every change does: pull request, green checks, merge,
and on a two-stage site `npm run ship` (`PUBLISHING.md`). Say which address shows it,
preview or live.

Then **look at the published page once.** It should say "The site has not been edited
since." If it says neither that nor "edited since", the host's build has no git and
the section cannot tell its own age there: tell the owner, so they know to refresh the
card after changes without that reminder.

## 6. Keeping it honest

- The card records the commit it tested and the git id of the paths in `TESTED`
  (`scripts/scorecard.mjs`): `src/`, `public/`, `tests/`, `functions/`, `scripts/`, the
  Astro, Playwright and TypeScript configs, the package files and `.nvmrc`. A site with
  other root files that shape the build adds them to that list. On every build the
  component compares those ids with the build's own, and counts uncommitted edits to
  those paths as edits. Same → "The site has not been edited since."
  Different → "The site has been edited since. A new test run is due." Build without
  git → it says neither. A change to a document (the README, the content guide) does
  not count.
- So an old card never claims to describe a newer site, and nothing forces a new run
  for every small edit. Re-run step 3 at launch, after a batch of changes, and whenever
  the owner wants the section to read current again.
- Lighthouse scores keep their own date. Ask for a fresh run when the old one is
  months old or the home page changed a lot.
- Removing it: delete the component's use, the three files, the `scorecard` script
  entry and `scorecard.json`.

## Boundaries (do not duplicate)

- Getting the suite green, and what the Lighthouse numbers mean: `website-qa`.
- Technical SEO and Core Web Vitals work: `seo-audit`. Search rankings and AI
  visibility over time: `search-console-insights`.
- This skill reports. It does not change what the tests check.

## Done means

The owner said yes and chose the page; `scorecard.json` is committed from a green run;
the page shows the same numbers (`scorecard.spec.ts` green with `PAGE` set); the
published page says whether the site was edited since, or the owner knows it cannot;
Lighthouse scores are either the owner's own measurement or absent; the owner knows the section
will say when it is out of date, and how to refresh it.
