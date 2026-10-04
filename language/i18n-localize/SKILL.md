---
name: i18n-localize
version: 1.0.0
description: Adapt content for a specific locale — units, dates, currency, idioms, and cultural fit — beyond literal translation.
author: matrixx0070
tags: [localization, i18n, locale, culture]
capabilities: []
---

## When to use

Use this when content must feel native to a specific locale, not just be readable in the language. Localization covers formatting (dates, numbers, currency, units), culturally appropriate idioms and examples, legal/regulatory phrasing, imagery references, and etiquette. Reach for it before shipping a product, campaign, or document into a new market.

**Not for:** straight meaning-preserving translation with no cultural reshaping (use `i18n-translate`), extracting a term list (use `i18n-glossary`), formality tuning alone (use `i18n-tone-adapt`), or captions (use `i18n-subtitle`).

## Method

1. Pin the exact locale (language + region, e.g. `pt-BR` not just Portuguese). This drives every formatting choice.
2. Localize formats: dates (`MM/DD` vs `DD/MM` vs ISO), decimal/thousands separators, currency symbol and position, 12h/24h time, measurement units, phone/address formats.
3. Convert quantities where the audience thinks in different units. Decision point: convert values (miles→km) OR keep and annotate — choose based on whether precision is legally sensitive.
4. Replace culturally-bound references: idioms, holidays, sports metaphors, name/example placeholders, and imagery that won't land.
5. Check sensitivities: color/symbol meanings, honorifics, taboo topics, regulatory disclaimers required in-market.
6. Decision point: if a source concept has no local equivalent (e.g. "Thanksgiving sale"), substitute an equivalent local occasion rather than transliterate.

## Example

Source (en-US): "Get 20% off this Labor Day — orders over $50 ship free. Sale ends 9/7 at 5pm."

Localized (en-GB): "Get 20% off this August bank holiday — orders over £40 ship free. Sale ends 07/09 at 17:00."

Notes: swapped US holiday → UK bank holiday; `$`→`£` with a market-appropriate threshold; date reordered to `DD/MM`; time to 24h.

## Pitfalls

- **Translating but not converting.** Leaving "70°F" or "5 miles" in a metric locale breaks immersion and usability.
- **Ambiguous dates.** `03/04` is March 4 or April 3 depending on locale — always disambiguate or use ISO.
- **Transliterated culture.** Keeping source-only holidays, sports, or slang that mean nothing locally.
- **Ignoring legal in-market copy.** Missing required disclaimers, tax-inclusive pricing, or consumer-rights phrasing.

## Output format

```
Target locale: <lang-REGION>
Locale conventions applied: date=<fmt> currency=<sym/pos> units=<system> time=<12/24h>

--- Localized content ---
<content>

--- Adaptation log ---
- <element>: <source> → <localized> (<reason>)
```
