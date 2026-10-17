---
name: rails-i18n
description: "Use when designing, implementing, reviewing, testing, or operating Rails internationalization/localization across locale selection, translation keys, pluralization, interpolation, dates/numbers, localized views/routes, model errors, mailers, APIs, jobs, caching, and translation backends."
license: MIT
---

# Rails I18n & Localization Engineering

## Purpose

Treat localization as a cross-layer application contract, not as a collection of translated strings.

Rails I18n provides a public API for translation and localization, locale configuration, permitted locales, default locale, translation load paths, and backend selection. Rails also integrates I18n with views, Active Model/validation errors, Active Record naming, Action Mailer subjects, and date/time formatting.

Core flow:

```text
define supported locale contract
-> resolve locale from a trusted source
-> establish request/job context
-> use stable translation keys
-> provide interpolation/pluralization/formats
-> render localized output
-> preserve locale across async/dependency boundaries
-> test fallback and isolation
-> observe missing/invalid translations
```

## Activate when

- adding or changing I18n.t, I18n.translate, I18n.l, or localize;
- adding locales or changing I18n.available_locales;
- changing I18n.default_locale or enforce_available_locales;
- selecting locale from URL, domain, subdomain, header, cookie, or user preference;
- localizing routes or URL generation;
- adding/changing translation files in config/locales;
- adding pluralized or interpolated translations;
- changing date, time, number, currency, or format localization;
- translating validation/model errors;
- localizing Action Mailer subjects/content;
- propagating locale through Active Job/background work;
- localizing API responses;
- deciding whether locale belongs in cache keys;
- adding custom I18n backends or database-backed translations;
- diagnosing missing translations, wrong locale, locale leakage, or inconsistent formatting;
- adding translation tests or translation linting.

Do not activate merely because a page contains one hard-coded string. Use the smallest relevant Rails view/controller skill for a trivial change when no localization contract is introduced.

## Repository inspection

Inspect before changing localization:

1. Ruby/Rails and I18n versions;
2. I18n.load_path, locale directory structure, and translation file conventions;
3. I18n.available_locales, default_locale, and enforce_available_locales;
4. existing locale-resolution code in controllers/middleware;
5. routes and URL generation conventions;
6. user/account locale preference storage and authorization;
7. request/job locale propagation;
8. Active Job serialization and locale behavior;
9. views/helpers/components using translation keys;
10. model validation/error translation conventions;
11. Action Mailer locale handling;
12. API serialization/error contracts;
13. cache keys and locale-sensitive cached representations;
14. fallback configuration and missing-translation handling;
15. custom backends or external translation stores;
16. tests, fixtures, translation linting, and CI checks;
17. source-control organization and translation ownership.

Do not introduce a second locale-resolution mechanism when the repository already has one.

## Decision rules

1. Classify the change: locale contract and resolution, locale propagation across requests/threads/jobs, translation keys and interpolation, localized formatting, localized views/routes/mail/API, caching, translation storage and fallbacks, or security/performance/testing.
2. Load the matching reference below before changing behavior; locale resolution and propagation changes usually need both the resolution and the propagation reference.
3. Scope every locale change with I18n.with_locale (or the repository's equivalent) so it cannot leak across requests, threads, fibers, or jobs.

## Critical invariants

- A locale is presentation context, not authorization.
- Do not use locale as a substitute for timezone.
- Do not make frontend logic depend on exact translated English text.
- Do not let arbitrary request input become a locale merely because a translation file happens to exist.
- Locale is part of the cache identity whenever the rendered or computed result changes by locale.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters supported locales, how a locale is chosen, or Accept-Language negotiation | [references/locale-resolution.md](references/locale-resolution.md) | Locale contract; Locale resolution; Locale negotiation | `i18n-locale-resolution` |
| locale state crosses requests, threads, fibers, or background jobs | [references/locale-propagation.md](references/locale-propagation.md) | Request locale isolation; Thread, fiber, and concurrency boundaries; Background jobs and locale propagation | `i18n-context-propagation` |
| a change adds or alters translation keys, interpolation, pluralization, or _html translations | [references/translation-keys.md](references/translation-keys.md) | Translation key contract; Interpolation; Pluralization; Safe HTML translations | `i18n-translation-key-contract`, `i18n-pluralization-formatting` |
| a change localizes dates/numbers/currency, templates, routes, model/validation messages, API responses, or mail | [references/localized-surfaces.md](references/localized-surfaces.md) | Date, time, number, and currency localization; Localized views and templates; Localized routes and URLs; Model and validation translations; API localization; Action Mailer localization | `i18n-pluralization-formatting`, `i18n-localized-routing` |
| a change alters localized caching, translation file layout, missing-translation handling, fallbacks, backends, or translation administration | [references/translation-storage-and-fallbacks.md](references/translation-storage-and-fallbacks.md) | Caching and locale; Translation file organization; Missing translations; Fallback behavior; Custom backends; Translation administration | `i18n-cache-identity` |
| a change has I18n performance, security/privacy, or test-strategy impact | [references/performance-security-testing.md](references/performance-security-testing.md) | Performance; Security and privacy; Testing | `i18n-security-boundary`, `i18n-testing` |

## Reference example

All user-visible strings through I18n with lazy-lookup keys, plus locale-aware formatting for numbers and dates.

```ruby
class InvoicesController < ApplicationController
  def create
    if @invoice.save
      redirect_to @invoice, notice: t(".created", reference: @invoice.reference)
    else
      flash.now[:alert] = t(".rejected")
      render :new, status: :unprocessable_entity
    end
  end
end

# config/locales/en.yml:
#   en:
#     invoices:
#       create:
#         created: "Invoice %{reference} issued."
#         rejected: "We could not issue this invoice."
#
# Locale-aware presentation:
#   l(invoice.due_on)                 # -> "2026-09-30" per locale format
#   number_to_currency(cents / 100.0) # -> "19,99 EUR" per locale
```

## Agent review checklist

- [ ] supported locales explicit
- [ ] locale precedence explicit
- [ ] untrusted locale input validated
- [ ] request locale scoped with restoration
- [ ] concurrency boundaries reviewed
- [ ] job locale behavior explicit
- [ ] translation keys semantic/stable
- [ ] interpolation contract explicit
- [ ] pluralization delegated to I18n
- [ ] date/time/number presentation localized
- [ ] localized routes/URLs reviewed
- [ ] model errors/API error contract reviewed
- [ ] mailer locale behavior reviewed
- [ ] locale-sensitive caches reviewed
- [ ] missing/fallback behavior explicit
- [ ] custom backend justified when used
- [ ] translation administration secured when present
- [ ] translation tests deterministic
- [ ] sensitive interpolation/logging reviewed

## Anti-patterns / failure modes

- mutating I18n.locale globally without restoration;
- trusting arbitrary request locale input;
- treating locale as authorization;
- concatenating translated fragments into sentences;
- manually implementing pluralization;
- using translated messages as machine-readable API identifiers;
- storing localized presentation values as canonical domain data;
- using locale to infer timezone;
- caching localized output without locale identity;
- caching locale-independent values with unnecessary locale dimensions;
- translating security/business state by parsing human-readable strings;
- exposing privileged translation administration to untrusted users;
- allowing user HTML through trusted translation-safe paths;
- hiding missing translations in all environments;
- database-backed translation lookup without availability/capacity analysis;
- assuming locale context automatically crosses background/concurrent boundaries.

## Verification

For a localization feature:

```text
supported locale contract
-> trusted locale resolution
-> scoped execution context
-> translation/formats contract
-> cross-boundary propagation
-> fallback/missing-key behavior
-> focused locale tests
-> security/cache/API review
-> regression suite
```

For localization incidents distinguish:

```text
locale resolution
-> locale availability
-> translation lookup
-> interpolation/pluralization
-> formatting
-> route/rendering
-> cache
-> job/mail/dependency propagation
```

Never claim complete localization coverage merely because every visible English string has a translation file entry. Verify execution paths, fallback behavior, formatting, and cross-boundary locale propagation.

## Source foundation

Primary Rails source:

- https://guides.rubyonrails.org/i18n.html

Current guide evidence used by this skill includes locale configuration/availability, request-scoped I18n.with_locale, localized routes/URLs, translation keys, pluralization, model errors, Action Mailer subjects, locale files, and custom backends.

Composed repository skills:

- `rails-action-view` skill
- `rails-routing` skill
- `rails-validations` skill
- `rails-api-integration` skill
- `rails-action-mailer` skill
- `rails-active-job` skill
- `rails-caching` skill
- `rails-security` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill
- `ruby-concurrency` skill

## Rails I18n changes

For I18n/localization changes:
- inspect supported locales, default locale, locale resolution, translation file organization, route conventions, user/account locale preferences, jobs, mailers, APIs, caches, tests, and custom backends before implementation;
- define supported locales and precedence explicitly; normalize/reject untrusted locale input before entering the scoped locale context;
- use request-scoped I18n.with_locale rather than leaking mutable I18n.locale across requests or execution units;
- keep locale separate from authentication/authorization and timezone; locale is presentation context, not authorization.
- use semantic translation keys with explicit interpolation contracts; do not use human-readable translated text as machine-readable identifiers;
- delegate pluralization and locale-aware date/number/currency formatting to I18n rather than hand-building grammar or presentation strings;
- review localized routes/default_url_options and bound locale dimensions when locale participates in URLs;
- explicitly decide whether background work captures or re-reads locale and validate locale again at execution;
- include locale in cache identity only when the cached representation actually varies by locale;
- treat translated HTML, interpolation data, translation administration, and localized caches as security boundaries;
- keep canonical domain data locale-independent and translate at presentation/wire boundaries;
- define missing-translation and fallback behavior for development, test, and production;
- use deterministic locale-sensitive tests and restore locale state between examples;
- never claim localization coverage solely from translation-file presence; verify execution paths, formatting, fallback, and cross-boundary propagation.
