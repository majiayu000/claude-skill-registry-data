---
name: website-launch-check
description: >-
  Launch readiness check for a site built with this toolkit: runs the site's own build and
  tests first, then checks only what they cannot (legal pages, E-E-A-T and local signals,
  content the site's settings call for, testimonial consent, what only a deployed site shows),
  asks only where the owner's intent decides, and writes a dated report with a verdict to
  docs/launch/ as Markdown plus a self-contained HTML page. When the site replaces an older
  one, also a current-vs-new comparison with a redirect map for every old address. Runs three
  times in new-website (baseline after the scaffold, the verdict before launch, an optional
  live re-check) and on its own. Trigger phrases: "launch check", "ready to launch", "what's
  missing before launch", "pre-launch", "go live", "launch audit", "relaunch", "compare the old
  and the new site", "post-launch gap analysis".
---

# Website launch check

A conversation, not a static report: settings first, then the site's own tests, then the
checks the tests cannot do, a question only where the owner's intent decides, an offer to fix
each gap, and a dated report. The skill's text is English; everything the owner sees is in the
owner's language (§1).

When it runs:

| Run | When | Report |
|---|---|---|
| **baseline** | `new-website` step 5a: after the scaffold is green (and after the brand-kit intake, where there is one) | `launch-check-<date>-baseline.md`, verdict "Baseline, not a launch verdict" |
| **pre-launch** | `new-website` step 10c: after steps 7 to 10b, before §4's deploy | `launch-check-<date>-prelaunch.md`, verdict 🟢 / 🟡 / 🔴; §4 starts after 🟢, or a 🟡 the owner accepts |
| **live** | `new-website` step 12a, optional: once the production build is Active on the live domain | `launch-check-<date>-live.md` |

It also runs on its own, on any site built with this toolkit, whenever the owner asks.

## 0. Settings: `docs/launch/config.json`

Read `docs/launch/config.json`. If the site has an older `.launch-check-config.json` in its
root, move it there first: `git mv` when git tracks it, `mv` when not, and say so. If both
exist, move nothing and ask which to keep. Make the folder first (`mkdir -p docs/launch`). Older reports in `docs/` stay where they are. The
old file's keys `storybrand` and `contact_forms` become `story_layer` and `contact_form`; fill a
missing key as below. A moved file counts as saved settings (the last paragraph of this section).

Without a settings file, fill one from what the site already says, and ask only what is
still open:

| Setting | From |
|---|---|
| `business_in_germany` (where the business is based decides the legal checks, not the site's language) | ask; the interview does not ask it |
| `site_languages` | `SITE.locale` in `src/config.ts`, the README's interview answers (Q4) |
| `story_layer` | the README's record of the §2a story offer, `STORY.md`; never ask again |
| `blog`, `contact_form` | the README's interview answers (Q1, Q2), the pages |
| `testimonials` | `src/data/testimonials.ts` (from `website-testimonials`); ask if the site has none |
| `analytics` | `USE_ANALYTICS` and the README (Q5) |
| `report_language` | the owner's language (§1) |
| `replaces` | ask once: does this site replace one that is live now? Its address, or `null` |

```json
{
  "business_in_germany": true,
  "site_languages": ["de"],
  "story_layer": false,
  "blog": false,
  "testimonials": true,
  "contact_form": true,
  "analytics": "plausible",
  "report_language": "de",
  "replaces": "https://www.example.com"
}
```

On later runs, name the saved settings in one line and ask once whether any changed.

## 1. Language

Questions, findings, reports, todos and the HTML are in the language the owner writes in;
`report_language` is the default on a re-run, and the owner's message overrides it. A German
owner gets everything in German, headings included. This file stays English.

## 2. The site's tests first

Run, in the site's folder, `npm run build`, then the whole suite with
`npx playwright test --forbid-only`, keeping the whole output. Use it, not `npm test`, so a
narrowed `test` script cannot hide a failure, and `--forbid-only` so a `test.only` left in a spec
fails the run instead of narrowing it; if `package.json`'s `test` script is anything but `playwright test`, that is
a 🟡 finding. Then follow `references/test-coverage.md`:

- A failing test is a 🔴 blocker that names the test and quotes its message. No look by eye
  stands in for a test.
- Every `⚠ placeholders:` line is a blocker (a page still listed in `UNFILLED_UNTIL_LAUNCH`,
  or a `[MISSING: …]` placeholder, which only warns outside CI). `⚠ positioning coverage:` is a
  🟡 finding. A skipped test is a 🟡 finding.
- A category the mapping gives to a test is left to that test, **per page**, only where the
  output shows that page's test passed. The report lists those under "Left to the site's tests,
  as they stand in this site, for the pages in `PAGES`", and the check does not look at them
  again on those pages. Every other page, and every built page that `PAGES` lacks, is the
  check's.

## 3. What the launch check checks

Only what the tests cannot. Skip what the settings rule out, and list it under "Skipped by the
settings".

**Always:**
- Titles and descriptions: no two pages share one, and each says what its page is (🟡).
- What no test reads (🔴, since a visitor would read it): the starter's example values (the name
  `Example`, `hello@example.com`) on the home page and the legal pages (the imprint where the
  site has one, the privacy or Datenschutz page), `public/llms.txt`'s own
  `[bracket]` slots, the 404 page's text.
- Console errors on the local preview (`npm run preview`), read with the site's own Playwright (a
  short script that opens each built page and collects console errors). Run it after the tests,
  and stop it when done: the tests start a preview of their own, and Astro refuses it while
  another one runs. Errors that come from
  the `_headers` rules, HTTPS and the 404 status show only on a deployed site: at the
  baseline and pre-launch runs they read "not checked yet: not deployed", and the live run
  checks them.

**Business in Germany:**
- **Impressum** per § 5 DDG (the Digitale-Dienste-Gesetz replaced the TMG in May 2024): name,
  address, a fast electronic contact, register entry, VAT ID if any; for a regulated
  profession (architects, lawyers, doctors, and a trade that must register with a chamber such
  as the Handwerkskammer) also the chamber, the professional title and the state that granted it.
- **Datenschutz:** hosting, analytics, forms, any embeds, the contact for data questions.
  Whether the text fits what the site really does; the slots and the analytics settings are
  `new-website` §4's own item.
- **Consent banner:** needed only if the site stores or reads non-essential data on the
  visitor's device (§ 25 TDDDG, formerly TTDSG), such as Google Analytics, YouTube or Google
  Maps embeds. Analytics that store and read nothing on the device need no § 25 consent (the
  privacy page still names their legal basis, which is the owner's to settle), but check it on
  the deployed site (the browser's storage panel after a page view) rather than
  assume it from the product's name. If anything is stored or read, or you cannot tell, report
  the banner question as open for the owner, not as passed. A banner the site does not need
  is itself a finding.

**Business elsewhere:** a privacy policy (GDPR-ready where the site serves people in the EU),
and terms where the site sells or takes bookings.

**Story layer:** the home page against `STORY.md` (from `website-story`), not against a
generic list.

**Blog:** an index page, at least one post (or drafts ready), a feed, a named author.

**Testimonials** (`src/data/testimonials.ts`): real names and roles where the owner chose names, and **consent on file for
each named person**: at each pre-launch run, ask the owner, quote by quote. "Yes" goes in the report as "owner confirmed
consent on file, <date>". "No" or "don't know" for a quote is a blocker that points at
`website-testimonials`' consent rule (keep it off the live site until consent lands). Keep no
consent record and no contact details.

**Contact form:** it shows its confirmation; a privacy note beside it links the privacy page;
spam protection where it sends to a server. Ask before sending a test message: on a live site
it reaches a real inbox.

**E-E-A-T and local signals** (an assessment, not a measurement): rate Experience, Expertise,
Authority, Trust and Local from what the site shows, 1 to 5 with one line why. **Authority
needs outside data** (links from other sites, press, awards, a Business Profile): without it,
the row reads "not checked: no outside data", with no stars, and the overall line names the
rows it averaged. If `analytics/eeat.md` exists (`search-console-insights`), read its newest
section and say what changed. Local: Google Business Profile, the same name, address and phone
everywhere, `LocalBusiness` markup, the city or region in titles and headings, `hreflang`
where `site_languages` has several, a map or directions link. `website-seo-geo`'s "GEO" is
generative engine optimization, not local SEO.

## 4. Questions and findings

Ask only where the owner's intent decides; everything else is a finding with an offer to fix.

- Ask: "Your settings say testimonials. The site has none. Still planned, or skip?" Intent
  decides.
- Do not ask: a page with two H1s, a missing description, an unfilled imprint line. Those are
  findings: "Found: … Want me to fix it?"

Offer to fix each gap on the spot (draft a description, describe an image, fill an Impressum
line from what the owner tells you), and run the tests again after a fix.

## 5. The report

Write `docs/launch/launch-check-<YYYY-MM-DD>-<baseline|prelaunch|live>.md` from
`references/report-template.md`, in the owner's language, without the template's comment. Each
run starts from the template and this run's findings, never from an earlier report.
A second report of the same kind on one day gets `-2` (then `-3`), and so does a second
comparison: never overwrite a report.

- **Verdict:** 🔴 when any blocker is open; 🟡 when only soon-after items are; 🟢 when nothing
  is. The baseline's verdict line is "Baseline, not a launch verdict".
- Every row says what was seen and where. A row with no evidence reads "not checked" with the
  reason; never a guessed score or number.

Then make the HTML page and keep every page current. The name in braces stands for the folder
this SKILL.md is in: Claude Code fills it in; with another assistant, put that folder's path in
its place. Run the commands in the site's folder (Claude Code asks before each, since the
site's permission list does not include `python3`):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/report_html.py" docs/launch/<report>.md --lang <report language>
python3 "${CLAUDE_SKILL_DIR}/scripts/report_html.py" --rebuild docs/launch
```

The first writes `<report>.html` beside the Markdown; the second rebuilds every HTML page in
`docs/launch/` that has its Markdown beside it, so a report someone edited since shows the edit
(a Markdown with no page yet needs the first command). The
Markdown is the source; never edit the HTML by hand. The page opens from disk in any browser
and loads nothing.

## 6. Todos (when the owner wants them)

Ask: "Want to assign these?" If yes, write `docs/launch/launch-todos-<YYYY-MM-DD>.md` from
`references/todos-template.md` (Markdown only: people tick its boxes), with the names or roles
the owner gives. Anything assigned to the assistant: offer to do it now. If the project uses a
task tracker, offer to create the tickets there too.

## 7. Relaunch: the current site against the new one

When the settings name `replaces`, the pre-launch run also writes
`docs/launch/launch-comparison-<YYYY-MM-DD>.md` and its HTML, following `references/relaunch.md`
and `references/comparison-template.md`: a verdict, before-launch items, speed old and new,
E-E-A-T for both, open questions, a redirect map for every old address, a side by side, what
the old site gets wrong, what the new one adds and what it does not have yet.

## 8. The live re-check (12a)

Only once the new site's production build is Active on the live domain: never request a page
of the new site on the live domain before that (`PUBLISHING.md`, "Never request a page on the
live domain before its build is Active": a first request caches a 404). Reading the old site's
existing addresses before the switch is fine. Then check HTTPS, the 404 status, console errors
on the live pages and the consent question, measure the live domain's speed as `website-qa` §2
does (the assistant runs Lighthouse; its fallbacks are PageSpeed Insights, then the owner), and
fill the comparison's new-site row. For a WordPress move,
point at `wordpress-inspector`'s `scripts/check_move.py --moves` where that skill is installed;
a site's bundled skills do not include it, so otherwise say it comes from Croftweaver.

## 9. Committing

The reports are the site's records: commit them the way the site's `AGENTS.md` says (a branch
and a pull request, unless it says otherwise). Both the Markdown and the HTML go in. In a
**public** site repository, ask before committing a comparison (it lists the old site's
addresses) or todos that name people.

## Related skills

- `website-qa`: the site's test suite, which this check runs first, and the speed measurement
  (§2).
- `website-review`: the two-pass review at the end of a build.
- `website-testimonials`: the consent rule for named quotes.
- `wordpress-inspector`: the inventory, the redirects and the move check for a WordPress
  relaunch.
- `outgoing-link-audit` and `internal-link-audit`: link liveness and orphan pages.
- `seo-audit` and `website-seo-geo`: deeper SEO and the AI-search contract.
- `search-console-insights`: the `analytics/` folder, including `eeat.md`.
