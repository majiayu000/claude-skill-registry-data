---
name: wordpress-to-astro
version: 2.2.0
description: Migrate a WordPress (or similar CMS) site to Astro by crawling the live public domain — no WordPress admin access needed. Rebuilds the site with SEO-identical markup for a zero-SEO-impact cutover, produces content maps shaped for Payload CMS, and ends with a verified local build to review. Use when the user invokes /wordpress-to-astro <domain> [--submit-forms] [--auto] or asks to migrate, convert or move a WordPress site to Astro or a static site. Documents accessibility issues, errors and hard-coded internal links but never fixes them.
---

# WordPress to Astro migration

Migrate a site from WordPress (or similar) to Astro, with Payload as the future CMS, using only what is publicly reachable on the domain given in `$ARGUMENTS`. No WordPress admin, database or API credentials are assumed.

This file holds the non-negotiables and the map. **The detail lives in the files it links to: read each one when you reach it** (the policies once, before the first request; each stage file and each phase file in full when you start it). Do not work from memory of a step you have not just read.

The run has **five stages with a review gate at the end of each**, made of 13 phase files used as steps. If a run is already in progress (`docs/run-state.json` exists), resume it as set out in `policies/run-state.md`. If its `skillVersion` differs from this file's `version`, offer to update it as set out in `policies/updating-a-run.md` (see [CHANGELOG.md](CHANGELOG.md)).

The goal is a clean cutover with **zero SEO impact**.

1. **Rendered HTML is sacred.** Reproduce the markup of every page exactly as served: element order, attributes, classes, IDs, heading levels, whitespace-insensitive text, inline scripts, `<head>` contents and order. Do not tidy, modernise, semanticise, minify differently, or "fix" anything.
2. **Structure the source, not the output.** Astro layouts and components exist to organise the code. Their rendered output must be identical to the original page.
3. **Record, never repair.** Accessibility problems, broken links, missing images and other defects are written to `docs/` and left as they are.

If a task seems to require changing markup, stop and log it in `docs/deviations.md` instead. The permitted deviations are a short closed list, each logged there with counts:

- rewriting asset URLs from the WordPress domain to local paths, **only where serving the asset at its original path is impossible** (log each rewrite pattern)
- leaving out suspected malicious code, as set out in `policies/suspicious-code.md`
- reversing hosting-layer output, as defined in the baseline (see `policies/what-identical-means.md`)
- the additive artefacts the user approved at intake (for example the themed 404 page, or one replacement script for features that cannot run on a static host)

Anything else needs the user's explicit yes at a review gate.

## Read first

Read these before making any request, then keep to them throughout:

| File | What it covers |
|---|---|
| [policies/before-starting.md](policies/before-starting.md) | authorisation, project setup, crawl cache, resource preflight, progress updates |
| [policies/what-identical-means.md](policies/what-identical-means.md) | how "identical" is defined: origin markup, volatile tokens, the comparison contract |
| [policies/crawler-identity-and-scope.md](policies/crawler-identity-and-scope.md) | the User-Agent, host scope, subdomains, WordPress admin URLs |
| [policies/suspicious-code.md](policies/suspicious-code.md) | what to flag, how to record it, why it is never recreated |
| [policies/review-gates-and-decisions.md](policies/review-gates-and-decisions.md) | the five stages and their gates, the checkpoint template, when to stop mid-stage, recording decisions |
| [policies/auto-mode.md](policies/auto-mode.md) | `--auto`: what is assumed, what still never happens, the hard stops |
| [policies/run-state.md](policies/run-state.md) | `wordpress-to-astro.config.json`, `docs/run-state.json`, resuming a run |
| [policies/updating-a-run.md](policies/updating-a-run.md) | re-running an existing migration after the skill changes: version stamps, stale phases, hand-edit protection, crawl freshness |
| [policies/record-only.md](policies/record-only.md) | what "record, never repair" means in practice |
| [policies/plain-language.md](policies/plain-language.md) | assume no WordPress knowledge: explain every WordPress feature in plain English, ask decisions in a fixed pattern, decide whether each feature needs translating at all |
| [policies/recommended-fixes.md](policies/recommended-fixes.md) | the running list every phase appends to |
| [reference/output-layout.md](reference/output-layout.md) | every file and folder the run produces |

## The stages

Each stage ends at a review gate: **stop and wait for the user to say "continue"** (`policies/review-gates-and-decisions.md`). Read the stage file when you start it, and each phase file when you reach that step.

| Stage | File | Steps | Gate |
|---|---|---|---|
| 1 Discover | [stages/1-discover.md](stages/1-discover.md) | intake and baseline (0), crawl (1), unlinked pages (2), smoke slice | scope, baseline, smoke-slice result |
| 2 Analyse | [stages/2-analyse.md](stages/2-analyse.md) | content (3), forms (4), SEO inventory (7), accessibility (10), errors (11): read-only, parallelisable | the findings |
| 3 Build | [stages/3-build.md](stages/3-build.md) | layouts and verifier (5), CSS (6), assets (9), listings, search and 404 (8) | a verified, buildable site |
| 4 Verify and review | [stages/4-verify-and-review.md](stages/4-verify-and-review.md) | full verification, SEO and asset checks, local review, visual comparison | verification results |
| 5 Finish | [stages/5-finish.md](stages/5-finish.md) | clean build, README, index | the index |

## The steps (phase files)

| Phase | File | Produces |
|---|---|---|
| 0 Intake and baseline | [phases/00-intake-and-baseline.md](phases/00-intake-and-baseline.md) | `wordpress-to-astro.config.json`, `docs/platform-features.md`, `docs/baseline.md`, `docs/decisions.md` |
| 1 Crawl and site structure | [phases/01-crawl-and-site-structure.md](phases/01-crawl-and-site-structure.md) | `docs/site-structure.md`, `docs/url-patterns.md`, hard-coded links |
| 2 Unlinked public pages | [phases/02-unlinked-pages.md](phases/02-unlinked-pages.md) | additions to `docs/site-structure.md` |
| 3 Content, taxonomy, authors | [phases/03-content-taxonomy-authors.md](phases/03-content-taxonomy-authors.md) | `docs/content-map.md`, `docs/authors.md` |
| 4 Forms | [phases/04-forms.md](phases/04-forms.md) | `docs/forms.md` (and the submission log with `--submit-forms`) |
| 5 Structure, layouts, components | [phases/05-structure-layouts-components.md](phases/05-structure-layouts-components.md) | the Astro source, the verifier, `docs/templates-and-components.md` |
| 6 CSS | [phases/06-css.md](phases/06-css.md) | `src/styles/`, load order per template |
| 7 SEO inventory | [phases/07-seo-inventory.md](phases/07-seo-inventory.md) | `docs/seo-inventory.md`, redirects data; the check runs in stage 4 |
| 8 Search, listings, pagination | [phases/08-search-listings-pagination.md](phases/08-search-listings-pagination.md) | listing variants, rewrite rules, search index, 404 |
| 9 Images and assets | [phases/09-images-and-assets.md](phases/09-images-and-assets.md) | `public/` assets, asset manifest |
| 10 Accessibility (record only) | [phases/10-accessibility.md](phases/10-accessibility.md) | `docs/accessibility-report.md` |
| 11 Errors (record only) | [phases/11-errors.md](phases/11-errors.md) | `docs/errors.md` |
| 12 Finishing and local review | [phases/12-finishing-and-local-review.md](phases/12-finishing-and-local-review.md) | clean build, local review server, README, `docs/index-YYYY-MM-DD-HHMM.md` (sections used in stages 4 and 5) |

Also: [reference/feature-translation.md](reference/feature-translation.md) (what each common WordPress feature does, whether a static Astro site needs it, and the recommended Astro way), [reference/smoke-slice.md](reference/smoke-slice.md) (proving the chain on three pages first), [reference/tooling-contract.md](reference/tooling-contract.md) (the commands tooling should expose, so the model runs scripts rather than writing them), [reference/scale.md](reference/scale.md) (sampling and budgets for large sites), [reference/local-review.md](reference/local-review.md) (spec for `npm run review`), [reference/visual-comparison.md](reference/visual-comparison.md) (checking the local pages against the live site in a browser), [reference/interaction-checks.md](reference/interaction-checks.md) (pressing every filter, search, load-more and menu control on live and local, and building the re-fetch list from the live pages), [reference/extending.md](reference/extending.md) (how to change or extend this skill), and [reference-implementation/](reference-implementation/README.md) (working scripts from a real run, to copy and adapt).

## Tools and options

**Tools.** Assume only the default tools: web fetch, web search, the shell, file read/write/edit and the task list. Do not assume any MCP servers, connectors, SEO platforms (such as Ahrefs), or browser automation. If a step needs something that is not available, record it in the relevant `docs/` file as "not done: requires <capability>" and carry on. Never hunt for or ask the user to install extra tooling to get around it.

Helper scripts that ship in the skill's own folder (crawler, page splitter, verifier, SEO and asset checkers) count as part of the skill: use them if present. If they are absent, write the equivalent into the project's `scripts/` and keep them there so every check can be re-run.

**Options.** Read them from `$ARGUMENTS` after the domain:

- `--submit-forms` (off by default): submit each distinct form once using dummy data to capture the full form flow. See Phase 4. Without this flag, never submit a form.
- `--gates=stage|phase` (default `stage`): stop at the end of each of the five stages, or after every phase. See `policies/review-gates-and-decisions.md`.
- `--auto` (off by default): run from start to finish without stopping for user input. Assumes every recommended default and treats every gate as "continue". Safe defaults only; see `policies/auto-mode.md`.

## Introduction on invocation

As soon as the skill is invoked, before making any request to the site, give the user a short introduction covering:

1. **The stages.** The five stages (Discover, Analyse, Build, Verify and review, Finish) in order, one line each, that it pauses for review at the end of each stage and resumes when the user says "continue", and that the user can choose `--gates=phase` to be asked after every phase instead.
2. **How the crawler identifies itself.** The exact User-Agent string it will send (see `policies/crawler-identity-and-scope.md`), so the user can recognise it in the site's logs.
3. **The outcome.** What the user will have at the end: the `docs/` folder (baseline, site structure, content map, authors, forms, templates, SEO inventory, accessibility report, errors, security findings, running list of recommended fixes, decisions and a timestamped index), plus an Astro project with layouts, components, styles and assets that reproduce the site's markup exactly, the host-level data needed for cutover (redirects, rewrites, headers), and **a local build they can start with one command and review in a browser**.
4. **Options in force.** Whether `--submit-forms` is on or off (without it no form is ever submitted), the gate mode, and whether `--auto` is on (no stops, defaults assumed).

Keep it to a short screenful. End by asking the user to confirm the domain and authorisation (see `policies/before-starting.md`) and wait for the go-ahead before the first request. With `--auto`, do not ask or wait: say that auto mode is on, that passing the domain counts as the authorisation, and start (`policies/auto-mode.md`).

## Definition of done

A run is complete only when the user can clone the project, install, run **`npm run build`** and **`npm run review`**, and browse the migrated site locally, with the documentation, the verification results and the open decisions in the index. See [stages/5-finish.md](stages/5-finish.md) and [phases/12-finishing-and-local-review.md](phases/12-finishing-and-local-review.md).

## Hard rules

- Never alter HTML to improve SEO, accessibility, performance or style.
- Never drop JSON-LD or any `<head>` element.
- Never invent content, dates or authors. Mark inferences as inferences.
- Never claim pages are identical without a verifier run under the comparison contract in `docs/baseline.md`. Never normalise anything the contract does not list.
- Never submit a form unless `--submit-forms` is set, and then only as described in Phase 4, with `@example.com` addresses only.
- Never convert hard-coded internal links to relative links, or change any other markup, in the Astro source. Record them in `docs/recommended-fixes.md` instead.
- Never rely on tools beyond the defaults. Record what could not be done and continue.
- Never hit the site faster than robots.txt and reasonable load allow.
- Always send the identifying User-Agent where the tool allows it. Never disguise the crawler.
- Never request a subdomain without the user's explicit yes, and never request WordPress admin or system URLs.
- Never recreate, execute, fetch or follow code or links flagged as malicious or deceptive. Highlight them and record them in `docs/security-findings.md`.
- Never put a WordPress-specific question to the user without a plain-English explanation of what the feature does, whether the new site needs it, and a recommendation (`policies/plain-language.md`).
- Never start the next stage without the user's go-ahead (or the next phase in `--gates=phase` mode). With `--auto` the go-ahead is given in advance, but the checkpoint is still written at every gate.
- Keep `wordpress-to-astro.config.json` and `docs/run-state.json` current so a run can be resumed.
- Never run a generator that deletes hand-maintained files. Generated and hand-maintained data live apart.
- Never start a large download or build without checking free disk space first.
- Add markup only for approved artefacts, and keep each one to the minimum (one script, one 404 page). Log every one.
- When something is ambiguous, record the ambiguity in the relevant `docs/` file, add a Review entry to `docs/recommended-fixes.md`, and continue with the most faithful option.
- Never end a run without a successful `npm run build` from a clean install and a local review server that was actually started, probed and stopped (see `phases/12-finishing-and-local-review.md`).
- Never alter built files to make local review work. Localise at serve time only.
