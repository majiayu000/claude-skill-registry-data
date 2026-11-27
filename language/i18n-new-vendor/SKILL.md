---
name: i18n-new-vendor
description: Add a TMS vendor to @joinery/i18n — a TranslationProvider subclass, its options type, configProblems() and one registry line. Use when adding or changing a translations vendor such as Phrase, Crowdin, Lokalise or another Tolgee-like API.
---

# Adding a translations vendor

The steps are in the [Vendors section](../../../packages/i18n/README.md#vendors) of the package README. Follow
them; this file is what the prose can't enforce.
[`TolgeeProvider.ts`](../../../packages/i18n/src/core/adapters/providers/TolgeeProvider.ts) is the example with
options, [`InternalProvider.ts`](../../../packages/i18n/src/core/adapters/providers/InternalProvider.ts) the one
without.

## The four things that go wrong

1. **One `<Name>`, three places.** `phrase` → `PhraseProvider.ts` → `class PhraseProvider` →
   `phrase:` in the registry. The registry key is what appears in `nuxt.config.ts`.

2. **The provider is a default export**, and the `options` type is read off the instance
   (`ProviderOf<N>["options"]`). That derivation is what makes `options` **required** in config for
   a vendor that has them and **forbidden** for one that doesn't:

   ```ts
   export interface PhraseProviderOptions {
       token: string
   }

   class PhraseProvider extends TranslationProvider<PhraseProviderOptions> {
       protected override configProblems(): string[] { … }

       override async getTranslations(locale: Locale): Promise<TranslationMap> { … }
   }

   export default PhraseProvider;
   ```

   `baseURL` and `project` are on the base class for every vendor, and only `options` is per-vendor.
   Don't re-declare them. **`options` is credentials only**, because it is left out of the cache key:
   anything that picks the document (a branch, an export profile) belongs on `Vendor`. The shape is
   `@joinery/content`'s too, so change both packages or neither. Overrides carry the `override`
   keyword.

3. **`configProblems()` covers `options` only, and is optional.** `project` non-empty and `baseURL`
   absolute are already checked in the base for every vendor, so a vendor with no options overrides
   nothing. It is called from the
   base constructor via `assertConfigured()`, so an override may only read `this.options`; the
   subclass's own field initialisers have not run. Return every problem as a string, never throw: one
   `MisconfiguredVendorError` listing all of them beats one restart per missing env var.

4. **The registry import stays lazy.** One line, `() => import(…)`. A static import ships every
   vendor to every deployment.

## Boundaries

`getTranslations` returns a `TranslationMap` — the vendor's response shape never leaves the
adapter. All I/O goes through the injected `HttpClient`; a provider that imports `ofetch` directly
has bound itself to a transport.

A failed request arrives as an `UpstreamError` already, reporting 502 whatever the vendor answered —
the locale was checked against the declared list before the request, so nothing upstream reports is
the caller's fault. Read its `upstreamStatus` if a vendor needs to tell one failure from another, but
do not relay it as a status. (`@joinery/content` does relay 400 and 404; its slug is caller input.)

The URLs are **relative**: the consumer builds the client with `ofetch.create({ baseURL })`, so a
provider passes a path. `http.get` resolves `{ data, headers }`; read the body off `data`.

No service layer over the port: a class forwarding one call to one collaborator adds a name and a
file without adding behaviour. Locale fallback or merging local overrides would be the day that
changes.

## Finish

A `<Name>Provider.spec.ts` beside it, covering the URL contract, the mapping, and a misconfigured
construction. Then:

```sh
pnpm exec nx run-many -t lint typecheck test --projects @joinery/i18n
```

Nothing else. Config typing, lazy loading and the Nuxt route follow from the registry line.
