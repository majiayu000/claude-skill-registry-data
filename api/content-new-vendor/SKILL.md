---
name: content-new-vendor
description: Add a CMS vendor to @joinery/content — a ContentProvider subclass, its options type, configProblems(), one registry line and a spec. Use when adding or changing a content vendor such as Contentful, Sanity, Strapi or another WordPress-like API.
---

# Adding a content vendor

The steps are in the [Vendors section](../../../packages/content/README.md#vendors) of the package README. Follow
them; this file is what the prose can't enforce. Read
[`wordpress/`](../../../packages/content/src/core/adapters/providers/wordpress) first — it is the only vendor, so it
*is* the pattern, including the split into a provider, its constants, its mapping helpers and its
response types.

## The five things that go wrong

1. **One `<Name>`, four places.** `contentful` → `contentful/` → `ContentfulProvider.ts` →
   `class ContentfulProvider` → `contentful:` in the registry. The registry key is what appears in
   `nuxt.config.ts`, so a mismatch is a config that can't be typed.

2. **The provider is a default export.** `createProvider` reads `module.default`, and the
   `options` type is read off the instance (`ProviderOf<N>["options"]`). That derivation is what
   makes `options` **required** in config for a vendor that has them and **forbidden** for one that
   doesn't:

   ```ts
   export interface ContentfulProviderOptions {
       accessToken: string;
   }

   class ContentfulProvider extends ContentProvider<ContentfulProviderOptions> { … }

   export default ContentfulProvider;
   ```

   `baseURL` is on the base class for every vendor; don't re-declare it. **`options` is credentials
   only**, because it is left out of the cache key: anything that picks the document (a space, an
   environment, a dataset) goes in `baseURL` as the path or host segment the vendor's API already
   uses (`https://cdn.contentful.com/spaces/<space>/environments/<env>`). An identity field in
   `options` makes two spaces share cache entries. The shape is `@joinery/i18n`'s too, so change
   both packages or neither.

3. **`configProblems()` covers `options` only, and is optional.** `baseURL` is already checked in
   the base for every vendor, so a vendor with no options overrides nothing. It runs from the base
   constructor, so an override may only read `this.options` — the subclass's own field initialisers
   have not run yet, so a `private readonly apiPath = …` referenced from it is `undefined`.
   `core/ports/ContentProvider.spec.ts` pins this; meet it there rather than in production. Return
   *every* problem as a string, never throw: one `MisconfiguredVendorError` listing all of them
   beats one restart per missing env var.

4. **Only override `getEntry`/`getTerm` for a native single-document endpoint.** The inherited
   implementation is a one-item list and already handles the 404. Overriding it "for symmetry" adds
   two methods that can drift from the list path.

5. **The registry import stays lazy.** One line, `() => import(…)`. A static import ships every
   vendor to every deployment.

## The domain is not negotiable

A vendor's shapes never leave its adapter. Map to `Entry`, `Term` and `Page` in the provider; ids
are strings even when the vendor numbers them. If the vendor cannot serve a query axis, refuse it
with a 400 naming the vendor and the parameter — never silently drop it, because the result gets
cached under the value that was asked for. There is no error class for that yet, since every axis
in `Query` is one WordPress serves; write one beside the axis that needs it. A transport failure
surfaces as `UpstreamError` and nothing else; anything
other than a 400 or 404 becomes a 502, since an upstream 401 means *our* credentials are wrong.

URLs are **relative**: the consumer builds the client with `ofetch.create({ baseURL })`, so a
provider passes the path its API defines (`/wp-json/wp/v2/posts`). All I/O goes through the
injected `HttpClient`; a provider that imports `ofetch` directly has bound itself to a transport.

If the vendor needs a resource family the domain doesn't have, that is a change to
`core/domain/content.ts` and a conversation about `Resource` being two closed unions; raise it with
the user before opening it up.

## No service layer

Callers talk to the port directly. A class forwarding one call to one collaborator is a name and a
file with no behaviour.

## Finish

A `<Name>Provider.spec.ts` beside it, covering the URL contract, the mapping, and a
misconfigured construction. Then:

```sh
pnpm exec nx run-many -t lint typecheck test --projects @joinery/content
```

Nothing else. Config typing, lazy loading and the Nuxt routes follow from the registry line.
