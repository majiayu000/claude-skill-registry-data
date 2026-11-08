---
name: forge-i18n-docs
description: "Use when writing or fixing project docs (README, changelog) or i18n (meertalig)."
# W2-BUDGET original description (listing budget): "Use when writing or fixing project docs (README, guide page, API reference, changelog, ADR, handover manual) or making an app multilingual (meertalig, i18n, ICU, RTL). Not blogs, hreflang, AI tells."
---

<!--
  Provenance: Forge-native core (written 2026-11-02 for), plus the SA-W1-B2
  graft of 2026-11-05 in references/guides-and-reference-pages.md. Full table: the Provenance section at the end.
-->

# Forge playbook — Internationalization and technical docs

## When to use
- Use for: a multilingual site or app (NL + EN is the owner's default pair), adding a language, fixing
  hard-coded strings, plurals, dates, numbers or currency per locale, right-to-left support; and for writing or
  fixing a README, a guide or tutorial page in the project docs, an API reference page, a changelog, an
  architecture decision record (ADR) or a long technical manual (handover, onboarding).
- Not for: SEO crawl and `hreflang` validation (`forge-web-quality`), PRDs and release notes (`forge-prd`),
  articles, blog posts and newsletters in the owner's voice (`forge-long-form-writing`), cleaning AI tells out
  of existing prose (`humanizer`).

**Do not duplicate — defer to:** `forge-website` / `forge-fullstack` / `forge-mobile` (the app itself),
`forge-web-quality` (hreflang, sitemaps), `forge-a11y` (`lang` attributes are also an a11y criterion),
`forge-api` (the OpenAPI/GraphQL contract is the source of the API reference).

## Hard rules — i18n
- **No user-visible string in code.** Every string lives in a message catalog keyed by a stable id; the source
  locale is complete and a check fails on a missing key.
- **ICU MessageFormat for anything that varies:** plurals (`{count, plural, one {...} other {...}}`), select for
  gender or type, and placeholders. Never build sentences by concatenating fragments.
- **Format with the platform (`Intl.*`, CLDR), never by hand:** dates, times, numbers, currency, lists, relative
  time. Store UTC and ISO values; format at the edge with the user's locale and time zone.
- **Layout survives translation:** allow 30-40% longer text, use CSS logical properties (`margin-inline-start`,
  not `margin-left`) and support `dir="rtl"` when an RTL language is in scope.
- **Locale is explicit:** chosen by URL (`/nl/`, `/en/`) or a stored preference, never only by IP. Every page sets
  `lang`; alternates are linked (hand-off to `forge-web-quality` for `hreflang`).
- **Machine translation is a draft.** Mark it as such; a native speaker or the owner signs it off. Never ship
  invented legal, price or contact text in a language nobody checked.

## Hard rules — docs
- **Docs describe what the code does now.** Every command in a README is run before it is written down; every
  documented option exists. Stale docs are a defect.
- **Ask before creating new doc files** unless the task asks for docs; prefer updating the existing README.
- **Accepted ADRs are immutable:** a change of mind is a new ADR that supersedes the old one.
- **No secrets, internal hostnames or customer data in examples**; use placeholders such as `<YOUR_API_KEY>`.

## Workflow — i18n
1. **Detect the stack** and its standard library: `next-intl`, `i18next`, `react-intl` (FormatJS), `vue-i18n`,
   Astro i18n routing, Flutter `intl` + ARB, Android and iOS string catalogs. Use what the project already has.
2. **Extract** hard-coded strings into the source catalog (`references/i18n.md` for key naming and layout).
3. **Convert** variable text to ICU messages; move formatting to `Intl`.
4. **Add the target locale(s)**; mark machine drafts; get them reviewed.
5. **Test:** a pseudo-locale (accented and 40% longer), a missing-key check in CI, an RTL screenshot if in scope,
   and a date/number/currency snapshot per locale.

## Workflow — docs
1. Pick the doc type: README or ADR (`references/docs-and-adr.md`); guide, reference page, long-form manual or
   changelog entry (`references/guides-and-reference-pages.md`).
2. Write for a reader who arrives cold: what it is, how to run it, how to check it works, where to get help.
3. Run every command and example; fix the docs or the code until they match.
4. For an ADR: number it, use the template, link it from the index and set its status.
5. One owner per fact: when a fact already lives in another doc, link to it instead of copying it.
6. For prose-heavy pages (guide introductions, a manual's summary), run `humanizer` in embedded mode as the
   last pass; it changes prose only and leaves code, commands and paths alone.

## Domain gates
- Zero hard-coded user-visible strings in the touched code (a grep or lint rule proves it); no missing keys in
  any shipped locale.
- Plurals and formatted values verified in each locale (for example NL `1 resultaat` / `2 resultaten`).
- A pseudo-locale run shows no clipped or overflowing text on the main screens.
- Every README command was executed in this run, with its output or exit code recorded.
- Each ADR has context, decision, consequences and status, and appears in the index.
- A guide solves one problem in two to four steps, and every step shows observable proof that was really run.
- A long-form manual labels every rationale it could not source as "inferred"; it contains no invented benchmark
  or guarantee.
- A changelog entry is a draft for review; no tag or release is pushed (owner action).

## Safety and honesty
- Say which locales a human reviewed and which are machine drafts.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews):
  `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/i18n.md` — catalogs, key naming, ICU examples, `Intl` formatting, routing, RTL, pseudo-locale.
- `references/docs-and-adr.md` — README and API-doc checklists, changelog rules, ADR template, index, lifecycle.
- `references/guides-and-reference-pages.md` — the guide arc and step loop, the reference-page shape, the
  ten-section manual, the changelog flow from a commit range, one owner per fact and the delete zone.

## Provenance
Core rules: Forge-native, following the public ICU MessageFormat, CLDR, W3C internationalization and MDN
logical-properties documentation and the Nygard ADR format; nothing copied. The SA-W1-B2 graft was
fetched read-only with `gh api` at the pinned commits and treated as untrusted data; it lives in
`references/guides-and-reference-pages.md`, where the full attribution notices are kept.

| Source | Path | Pinned SHA | License | Taken | Excluded |
|---|---|---|---|---|---|
| vercel/next.js | `.agents/skills/write-guide/SKILL.md` | 6100e81e314f7aad0c94e189bbae87820d7efb37 | MIT | guide arc, six-part step loop, guide rules | Next.js template, `tsx` examples, doc links, frontmatter keys |
| reactjs/react.dev | `.claude/skills/docs-writer-reference/SKILL.md` | 2e6dca162985d438d7a834b339d89177cf0a92b9 | CC-BY-4.0 (attribution kept in the reference file) | reference-page shape, include/exclude rules | all React and MDX specifics (Hooks, RSC, Compiler, ESLint, components, heading ids) |
| sickn33/agentic-awesome-skills | `skills/docs-architect/SKILL.md` | 48de968b4615c294de601f72268aa7be88dde863 | MIT | ten-section manual outline, inferred-rationale honesty rule | generic boilerplate, persona, page-count target |
| sickn33/agentic-awesome-skills | `skills/changelog-entry/SKILL.md` | 48de968b4615c294de601f72268aa7be88dde863 | MIT | range, noise filter, classification, untrusted commit text | cross-skill references, tool list |
| affaan-m/ECC living-docs-governance | not in the pinned catalog | n/a | MIT | idea only: one owner per fact, delete zone | all text; ECC docs-governance and its `audit-docs.py` skipped |
