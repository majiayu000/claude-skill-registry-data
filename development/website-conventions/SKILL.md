---
name: website-conventions
description: "Rules every website follows: light and dark mode, own imprint and privacy pages with fixed routes and locale redirects, a footer on every page, and nothing built that the shared web library provides. Use when building, extending or reviewing a website, a landing page or its legal pages."
---

# Website conventions

One rule set for every website, so each site is built and reviewed the same way.

## When to use

- Building a website or a landing page.
- Adding or changing an imprint, privacy or terms page.
- Reviewing a website against the baseline.
- A site needs a feature the shared web library might already offer.

## Rules

### Shared web library

- A site implements nothing the shared web library provides or will provide.
- A missing piece is an issue in the shared web library first. The site waits or uses the
  released version. It never keeps a private copy.
- The redirect set comes from the shared web library, not from the site.
- The library never ships legal texts.

### Theme

- Every site offers light and dark mode with the shared theme and the theme switch.

### Legal pages

- Every site has its own imprint and privacy statement, and its own terms when it sells
  something.
- The texts are written for that site's features and live in its repository.
- The texts are never shared between sites and never shipped by the library.
- The owner reviews every text before it goes live. The texts are not legal advice.
- The pages exist in German and English.
- The page texts are site content in both languages. The repository language rule covers code
  and documentation only.
- The terms page exists only for a site that sells something. Otherwise `/terms` and `/agb`
  are both left out.
- The imprint has no dispute resolution section. No arbitration statement, no online dispute
  platform link.

### Routes

- English names: `/imprint`, `/privacy`, `/terms`.
- German aliases: `/impressum` for the imprint, `/datenschutz` and `/datenschutzerklaerung` for
  privacy, `/agb` for the terms.
- Every unprefixed path and every alias redirects server side to the page of the negotiated
  locale, `/de/...` or `/en/...`.
- Example: `/impressum` goes to `/de/imprint` for a German visitor and to `/en/imprint` for an
  English one.
- The locale comes from the visitor's choice, then the `Accept-Language` header, then the site
  default.

### Footer

- A footer on every page links the imprint, the privacy page and, where present, the terms.

## Steps

### Build a site

1. Find the web library the site depends on, from its dependency file. Check that its released
   version supports the routes, the redirects, the theme and the theme switch.
2. File an issue in the library for every gap, see `issue`. Wait or use the released version.
3. Register the routes once.
4. Wire the theme and the theme switch.
5. Add the footer links on every page.
6. Read the site's real features and config values: cookies, analytics, forms, hosting,
   payments.
7. Write the imprint and privacy text from those facts, in German and English.
8. Write the terms only if the site sells something.
9. Check the redirects: request each path without JavaScript and expect a 3xx status.
10. Run the repository's verify command, see `repo-conventions` Config `verify`.
11. List for the owner every text to review and every fact the site could not supply.

### Review a site

Report findings through `review` or `work-review`.

1. Light and dark mode work with the shared theme and the switch.
2. Request each path without JavaScript. Expect a 3xx status and a `Location` header to the
   page of the right locale. A site that sells nothing has no `/terms` and no `/agb`.
3. The locale order is visitor choice, header, site default.
4. German and English pages exist.
5. The footer links the pages on every page.
6. The imprint has no dispute resolution section.
7. The texts are the site's own and match what the site really does.
8. No code copies a feature of the shared web library.

## Guardrails

- Never copy a legal text from another site or from the library.
- Never call a text legal advice.
- Never mark a text final before the owner reviewed it.
- Never invent a provider detail, a VAT ID or a retention period. Ask the owner.
- Never keep a private copy of a library feature to avoid waiting.
- Never add a dispute resolution section to an imprint.

## References

- `repo-conventions` for the repository layout and the verify command.
- `issue` for the library issue.
- `review` and `work-review` for reporting findings.
