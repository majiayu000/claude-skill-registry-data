---
name: cx-translation-workflow
description: Use to keep localised help centre content current when the source language changes, detect stale translations, and prevent silent lag between markets. Trigger for "translations are out of date", localisation workflow, source of truth language, help centre i18n, translation drift after policy update, or non-English customers seeing old policy.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Translation workflow for support content

Non-English customers routinely run **last quarter's policy** because the English
source was updated on launch day and translations were "queued." Nobody tracks the
queue. CSAT drops in one market; someone discovers the Dutch refund article still
 mentions 14 days when English says 7.

The prize: **one source of truth, explicit translation state, and no silent lag** —
markets should know they are behind, and customers should not see stale policy
presented as current.

## Source-of-truth language

Pick exactly one **authoritative source language** for each article family — usually
the language of the team that owns policy (often English, not always).

| Rule | Why |
| --- | --- |
| Source edits happen only in source language | Prevents three-way drift |
| Translations are derivatives, not co-equal originals | Ownership stays clear |
| Locale variants (en-GB vs en-US) pick one source or merge deliberately | Minor diffs become major contradictions |
| Legal/regulated text may require locale-specific source | Document exception; do not assume translate-from-English |

Agents in translated markets may add internal notes in local language — that is
internal wiki content, not a second customer-facing source.

## Translation states (make lag visible)

Every translated article needs machine-readable state, not just published/draft:

| State | Meaning |
| --- | --- |
| `current` | Translation matches source version |
| `stale` | Source changed after translation last verified |
| `in_progress` | Assigned to translator/LSP |
| `blocked` | Terminology or legal question open |
| `locale_exception` | Intentionally different in this market |

**Stale must surface in dashboards** — count of stale articles by locale, aged by
days since source change. Silent `published` on stale content is the failure mode.

Track **source version ID** (hash, updated_at, or revision number) on each
translation. Compare on every source publish.

## Workflow when source changes

1. **Source article updated and reviewed** — facts locked in source language.
2. **Auto-flag all translations stale** — immediately, on publish.
3. **Triage by impact** — usage × policy-risk priority: high-traffic + policy
   change = P0 for every locale.
4. **Translate or interim banner** — if translation lags, show banner in affected
   locales: "This page is being updated — see English" or unpublish until ready.
   **Never leave wrong policy live without warning.**
5. **Verify translation** — native reviewer for regulated topics; glossary compliance
   for product terms.
6. **Mark `current`** — only when source version ID matches.

Emergency policy correction: **all locales P0**. There is no "English only for now"
for fee or legal changes unless regulators allow it — and even then, unpublish or
banner non-compliant locales.

## Stale translation detection

Run weekly (daily during launch windows):

1. Compare translation `source_version` to live source `version`.
2. List mismatches sorted by **locale × article views × policy sensitivity**.
3. Cross-check **macro and AI corpora** in each locale — translations lag there too.
4. Sample tickets in each locale on stale topics — are agents improvising?

| Signal | Likely cause |
| --- | --- |
| One locale always stale | No owner, wrong LSP SLA, missing glossary |
| All locales stale after every release | Source edits bypass workflow |
| Stale on low-traffic only | Acceptable if bannered; not acceptable if regulated |
| Agents in locale cite English article | Translation untrusted or missing |

## Glossary and locked terms

Product names, plan names, fee currencies, and legal terms belong in a **shared
glossary** — translators do not invent equivalents. Breaking changes to glossary
trigger re-translation sweep of affected articles.

Numbers and units: **locale formatting is not translation.** Dates, currency, decimal
separators, and address formats must be localised in review, not left as copy-paste
from source.

## What not to translate literally

- Idioms and warmth — rewrite for natural local register.
- Screenshots with English UI — replace or annotate.
- Links — locale-appropriate destination if a local help path exists.
- Examples with culturally wrong scenarios — adapt in review.

Machine translation for first draft is fine; **publish requires human review** on
policy, billing, and compliance topics.

## Traps

- **Translation memory reusing old policy sentences.** TM is how "14 days" survives
  the edit to "7 days." Force re-review on policy articles.
- **Partial updates.** Source paragraph changed; translator updated half the page.
  Version ID on whole article; diff-based review.
- **English banner on local site without date.** Customers assume it is current.
  Show source update date and expected translation date.
- **Decentralised "someone in market will fix it."** Without SLA, they won't.
- **Treating macro translation as separate from KB.** Same stale problem; same queue.

## Present results to the user

1. **Source-of-truth definition** — language, owners, exceptions.
2. **Stale inventory** — by locale, ranked by usage × days stale × policy risk.
3. **Workflow spec** — states, triggers, SLAs by priority tier.
4. **Interim customer communication plan** — banner, unpublish, or English fallback.
5. **Glossary gaps** — terms blocking consistent translation.
6. **Macro/AI locale check** — non-KB content still running old translations.
