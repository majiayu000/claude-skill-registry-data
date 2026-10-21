---
name: website-review
description: >
  The Double-Knuth review for a site — a two-pass correctness + cross-file
  consistency audit run at the END of a build (pre-launch) and after ADDING or
  substantially editing a page.
  Pass 1 = bugs/correctness (delegates the diff to /code-review);
  Pass 2 = completeness + route/URL/SEO/config/email/docs consistency against
  the site contract. Read-only: returns a ranked BUG/RISK/NIT list with
  file:line + fixes. Prerequisite: website-qa green. Also owns the "review
  depth" decision for website work — when this free default suffices vs. an
  owner-approved single external reviewer for genuinely higher-stakes changes
  (its "Review depth" section has the rule). Trigger phrases: "double-knuth",
  "double knuth the site", "review the site", "site review", "final review
  before launch", "review this page", "did adding the page break anything",
  "consistency check the site", "audit the site code", "how much review does
  this need", "do I need a second opinion on this", "should I use
  independent-review for this".
---

# Website review — Double-Knuth (correctness + consistency)

A two-pass audit of a site's code/config/content, modelled on the
`portfolio-code-reviewer` Double-Knuth. It sits **on top of `website-qa`**: the
tests are the floor (must be green first); this is the human-grade review that
catches what a test suite can't — cross-file drift and half-done work.

## When to run
- **End of a build, before launch** (pipeline step 8).
- **After adding or substantially editing a page** — a new route touches `PAGES`,
  nav, the sitemap, internal links and canonical, so consistency can silently break.
- It is **read-only**: produce a ranked list, then fix BUGs before launch. Don't
  fix-and-forget — surface first (Rule 12: never hide a skipped or broken thing).
- For just "is the offer clear to a stranger" on a site that's already built —
  faster and narrower than this full audit — use `website-positioning-check`.

## Review depth — the owner chooses, every time

A website is lower-stakes than application code: a subtle bug in a landing
page's copy costs a bad reading experience, not a broken payment or a data
leak. This skill (Double-Knuth, below) is free, runs entirely in the current
session, and is **the default, sufficient review for the large majority of
website changes** — new pages, copy edits, layout tweaks, small SEO
adjustments, content updates. An external AI reviewer on top of it is an
*optional* extra, never a requirement, and never more than one at a time.

**Default — no setup, no cost, use this unless there's a specific reason not to:**
- **This skill, both passes** — Pass 1 delegates to `/code-review`
  (correctness bugs), Pass 2 is the cross-file/consistency sweep below.
- **`/code-review` alone** — just Pass 1, for a small, self-contained diff
  where cross-file consistency clearly isn't at risk (a one-page copy fix, a
  single component tweak). Faster than the full two-pass audit when that's
  all the change touches.

**Optional escalation — one external reviewer, only when it's genuinely worth it:**
A handful of website changes carry enough risk that a second, independent
model is worth the extra step: a **site-wide SEO repositioning** (the
`seo-reposition` skill's plan/diff gates), a **payment or checkout flow**, a
form collecting **sensitive personal data**, or a **major structural
redesign** where the author reviewing their own architecture risks sharing
its blind spots. Even for these, use **one** external reviewer, not the
`independent-review` skill's own default of two — that default is calibrated
for production application code (Rails migrations, auth changes), not
website content/structure work:
```bash
# from this repo's skills root, or the equivalent path in a site that has
# independent-review vendored in:
skills/independent-review/scripts/independent_review.sh <file> --plan --first-success   # or --diff
```
`--first-success` stops at the first reviewer that answers (Codex CLI,
falling back to ollama-cloud) instead of running both — independent-review
honors this override for plans, it doesn't force the pair. Setup: if
`independent-review` isn't already working in this repo, its own SKILL.md
has a guided onboarding wizard for getting Codex or ollama-cloud running
(free, no payment) — walk through that first rather than assuming it's ready.
In a scaffolded site the skill isn't shipped at all: check that the
`independent-review` folder actually exists before offering this escalation
as ready-to-run. If it doesn't, either vendor it first (copy
`skills/independent-review/` from the Croftweaver suite — the same kit
this skill was copied from — into the site's `.claude/skills/`) or frame the
offer honestly as "available after a one-time setup step".

**Explain the choice, then ask — don't decide silently.** Before reaching for
anything beyond this skill's own two passes, say plainly what the options
are and what's actually at stake: *"I can review this with the built-in
check — free, runs now — or also send it to an outside AI for a second
opinion, which costs nothing either but takes a few extra minutes. For
[this kind of change] I'd lean toward
[recommendation] because [reason] — want that, or would you rather [the
other option]?"* The owner decides; this skill's job is to make an informed
recommendation, never to pick unasked.

## Pass 1 — correctness / bugs
- Run **`/code-review`** on the branch/diff (correctness bugs + reuse/simplification).
  `/code-review` is Claude Code-only — under another host, review the diff by
  hand against this pass's checklist, or vendor the generic `double-knuth`
  skill from the Croftweaver suite.
- `npm run build` is clean — no errors **or warnings**; TS strict passes.
- `npm test` green (a11y/seo/navigation/anchors/orphans/images/tone/positioning/placeholders/email/links/llms-coverage/middleware) — nothing skipped or loosened. (A site scaffolded before a spec existed: copy it in from the starter rather than reviewing without it. `placeholders.spec.ts` goes in with its `UNFILLED_UNTIL_LAUNCH` as shipped, on a launched site too: the first run names each entry to delete, and its check for lower-case slots, which runs on listed pages only, finds the one older starters carried on the privacy page.)
- `astro preview` the new/edited pages — **no console errors**; interactions work.
- Nothing half-done: no TODO/placeholder/lorem and no leftover `[BRACKET]` slots in shipped
  pages OR `public/` assets. `placeholders.spec.ts` enforces this on the rendered pages and
  the manifest; read for what it cannot see: pages outside `PAGES` (the 404 page, noindex
  pages), other `public/` files (`llms.txt` and its own slots included), PDFs, text inside
  images, the starter's example values, and an entry still sitting in its
  `UNFILLED_UNTIL_LAUNCH` at launch (it only warns there).
- **Freshness date matches the edit:** if the page's visible content changed and it carries a
  last-modified signal (a `dateModified`/"Updated" byline, an Article/BlogPosting JSON-LD date),
  that date is bumped to today. It silently drifts otherwise — stale in the visible byline, the
  `<time datetime>` attribute, and the schema's `dateModified` (an SEO/AI-answer-engine freshness
  signal) all at once, and no test catches it because nothing can know a date is "wrong" without
  knowing the edit happened.
- Nothing silently unshipped (two-stage sites): `git log origin/production..origin/main` empty,
  or the gap is a conscious decision — and the last `npm run ship` ended "✓ LIVE — verified".
  Any deploy you run or announce follows the site's `PUBLISHING.md` § "For AI assistants —
  deploy-time guardrails" (preview-vs-live announcements + the cached-404 rule).

## Pass 2 — completeness + cross-file/skill consistency
- **Routes:** every `src/pages/**` route is in `tests/_helpers.ts` `PAGES` (and vice-versa;
  seo.spec.ts's sitemap drift alarm enforces it); nav + every internal link points to a real
  route; every route is reachable via at least one inbound internal link (no orphan pages —
  the privacy page included).
- **URLs:** the no-trailing-slash convention holds everywhere (`/about`, not `/about/`);
  `canonical == og:url == SITE.url + path`.
- **Single source of truth:** address, email, phone, nav come **only** from `src/config.ts` —
  no hardcoded copies drifting inside pages.
- **Recurring section patterns carry consistent headings:** if a component pattern (e.g. a
  `grid grid-2`/`grid-3` card block) has its own `<h2>` directly above it everywhere else it
  appears on the site, a new or edited instance should too. A local heading step (h2 → h3) will
  not trip axe's heading-order rule, so this only surfaces by checking this page's heading
  structure against how the same pattern is used on other pages, not by trusting the a11y suite.
- **SEO (`website-seo-geo`):** title ≤60, description 120–160, og/twitter mirror, exactly one
  `<h1>`, JSON-LD valid, sitemap covers every page, `llms.txt` current.
- **Images (`website-design-system`):** WebP/AVIF, explicit `width`/`height`, `alt`; the LCP
  image eager (`fetchpriority="high"`), below-fold lazy; no oversized files.
- **Email:** every address rendered via `<EmailLink>`; `email.spec.ts` green.
- **Headers/redirects:** `_headers` CSP present; legacy URLs 301 in `_redirects`; the
  `*.pages.dev` middleware in place (previews noindexed); on a launched site,
  the project's own `pages.dev` address (as Cloudflare shows it; not always the project's
  name) answers 301 to the live domain — if it answers 200, see
  the causes listed in `new-website/references/CLOUDFLARE_FIRST_DEPLOY.md`, "After
  go-live", step 3 (variable not under Production or rejected, no redeploy since, or a
  middleware that predates the redirect).
- **Secrets:** no `.env`/token committed; `.gitignore` covers them.
- **Docs match code:** README test list + "how to add a page / run tests / deploy" current;
  `CONTENT_GUIDE.md` + `BRAND.md` filled (+ `STORY.md`, consistent with `POSITIONING.md`,
  if the site opted into `website-story`); decision-interview answers recorded; the handoff
  skill set present in `.claude/skills/`.
- **Language/i18n (non-English or multi-locale sites):** every page's CONTENT language
  matches its `<html lang>` (the tone gate's density check covers German; eyeball other
  languages); `og:locale` present and matching on every page; chrome (skip link, footer)
  in the site's language; German-market sites carry the filled Impressum and the German
  privacy page at the right URL (`/datenschutz` single-locale, `/de/privacy` multilingual);
  multi-locale sites: hreflang sets complete + reciprocal (`tests/i18n.spec.ts` green, or
  the twin-page seo.spec test for the light path), every `/locale` route in PAGES, the
  language switcher on every multi-locale page, llms.txt entries in each page's language.

## Output / done means
A ranked **BUG / RISK / NIT** list, each with `file:line` and a concrete fix (same shape as
the portfolio Double-Knuth). Fix BUGs before launch; RISK/NIT by judgment. Re-run `website-qa`
after fixes. **Done = both passes clean**, or the remaining items explicitly listed — never hidden.
