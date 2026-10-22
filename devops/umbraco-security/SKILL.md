---
name: umbraco-security
description: >-
  What Umbraco provides for keeping a package secure, on the server and in the backoffice:
  Management API authorization and policies, settings that hold secrets, endpoints outside
  the Management API, sanitizeHTML and escapeHTML, DOMPurify rules for
  custom elements, and umbHttpClient instead of handling tokens in the browser. Use when
  writing or reviewing a Management API controller, a secret setting, a custom endpoint, a
  backoffice template that uses unsafeHTML, or frontend code that calls an API.
---

# Security in Umbraco packages

General security (injection, XSS, CSRF, secrets in bundles, supply chain) isn't repeated
here. This skill covers what Umbraco provides for it and where Umbraco's defaults stop, so a
package uses those instead of hand-rolling its own.

Check type names and exports against the CMS source at the target release
(`umbraco-cms-source`). Everything below was checked at `release-17.6.1`.

## Management API controllers

- **The base class is the authentication.** `ManagementApiControllerBase` carries
  `[Authorize(Policy = AuthorizationPolicies.BackOfficeAccess)]`. The
  `/umbraco/management/api/` route alone protects nothing, so a controller on that route
  that inherits plain `ControllerBase` is open to anyone.
- **Backoffice access isn't enough for a sensitive action.** Add a stricter policy to
  deletes, secret access, and settings that affect other users. `AuthorizationPolicies` has
  built-in section and tree policies (`SectionAccessSettings`, `RequireAdminAccess`, and
  others); a package-specific one is registered in a composer with `AddAuthorization`
  (example in `umbraco-extensibility`'s `references/api-and-infrastructure.md`).
- **Every policy name must be registered.** An unknown name throws
  `InvalidOperationException` ("The AuthorizationPolicy named: '...' was not found") on
  every request to that endpoint. It fails closed, but only shows up when someone calls it.
- **Check each action, not just the class.** An action's `[AllowAnonymous]` overrides the
  class-level policy.

## Secrets and sensitive configuration

- **A masked field is write-only in the API.** A field shown as a password in the editor
  must not come back in any response, not even to redraw the mask. Return whether a value
  is set; treat an empty or masked value on save as "keep the existing one".
- **Prefer a configuration reference to the secret itself.** A setting can store a
  configuration key (`MyPackage:Providers:CoolVendor:ApiKey`) resolved from `IConfiguration`
  at the point of use. Each environment then supplies its own value, and the reference is
  safe to move between environments (`umbraco-env-sync`). Restrict the reference to the
  package's own configuration sections, or it can be pointed at a connection string or
  another package's secret and read back through your API.
- **Keep secrets out of Deploy and uSync exports**: `umbraco-env-sync`.

## Endpoints outside the Management API

A minimal API route, a surface controller, or a webhook receiver doesn't inherit the
Management API's authentication or anything else from the backoffice, even in the same
project. Decide each one explicitly: a member endpoint called with the login cookie needs
antiforgery or an origin check, and a public webhook needs its own authentication
(a signature or shared secret).

## Backoffice: sanitizing and escaping

Lit escapes interpolated values; the risk is in `unsafeHTML()`/`unsafeSVG()`.
`@umbraco-cms/backoffice/utils` exports two helpers:

- **`sanitizeHTML(html)`** runs DOMPurify with its default config. Use it on any HTML that
  must render as markup and isn't a constant: rich text, AI output, external API content,
  editor-written help text.
- **`escapeHTML(value)`** escapes one value for insertion into HTML you then render with
  `unsafeHTML`.

```typescript
import { html, unsafeHTML } from '@umbraco-cms/backoffice/external/lit';
import { sanitizeHTML } from '@umbraco-cms/backoffice/utils';

// WRONG: renders unsanitized markup
html`<div>${unsafeHTML(this._summary)}</div>`;

// RIGHT
html`<div>${unsafeHTML(sanitizeHTML(this._summary))}</div>`;
```

Import DOMPurify itself from `@umbraco-cms/backoffice/external/dompurify` if you need a custom
config, so the package doesn't bundle a second copy.

## Backoffice: custom elements in sanitized HTML

Allowing your own elements through DOMPurify (`CUSTOM_ELEMENT_HANDLING`) needs an
`attributeNameCheck` that excludes event handlers. `/.+/` lets `onclick` and `onload` through
on every allowed tag. Umbraco's own UFM sanitizer had this bug (GHSA-vrqc-59mw-qqg7) and now
uses `/^(?!on)/`. Match it, or list the allowed attributes:

```typescript
CUSTOM_ELEMENT_HANDLING: {
  tagNameCheck: /^my-pkg-/,
  attributeNameCheck: /^(?!on)/,
  allowCustomizedBuiltInElements: false,
}
```

## Backoffice: credentials stay on the server

- **Backoffice auth.** From 17.0 the backoffice's access token lives in an httpOnly cookie
  that scripts can't read. Call your package's Management API through `umbHttpClient`
  (`@umbraco-cms/backoffice/http-client`), and pass it as the `client` option to calls from
  a generated client so they reuse its cookie setup (generating one is in
  `umbraco-backoffice-conventions`). Never read, copy, or store a token in
  `localStorage`/`sessionStorage`.
- **Third-party keys.** A key in `import.meta.env.VITE_*` is public once built. Put the call
  to the third-party service behind your own Management API endpoint, which reads the key
  from server-side settings ("Secrets and sensitive configuration").

## *In a review*

Each of these is an injection, an authorization gap, or a secret exposure, which the
`reviewer` agent treats as `Critical`:

- a Management API controller without `ManagementApiControllerBase` or an explicit
  backoffice policy, or a policy name nothing registers
- a sensitive action guarded only by backoffice access
- a masked setting returned in a response, or a configuration reference with no section
  restriction
- a cookie-authenticated endpoint outside the Management API with no antiforgery or origin
  check
- an unsanitized `unsafeHTML`/`unsafeSVG` render of non-constant content
- a DOMPurify config that lets `on*` attributes through
- a secret reaching the client bundle
