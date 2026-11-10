---
name: dotkernel-evolution-pattern
description: >
  Use whenever a change would break something a client already depends on in a Dotkernel
  project — renaming or removing a field, parameter, route or template variable; changing a
  type, status code or response shape; making an optional field required; deprecating or
  deleting an endpoint — or when someone proposes a /v2, a version prefix, a version header, or
  "versioning the API". Also use when working with ResourceDeprecation, Sunset and Link headers,
  or the deprecation middleware.
---

# Evolution pattern, not versioning

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
             - Dotkernel Frontend
             - Dotkernel Light
  Packages:  - none
```

Dotkernel prefers evolving one codebase over maintaining parallel versions. Breaking changes are
announced ahead of time and removed on a published date. Full rewrites and `/v2/` prefixes are a
last resort reserved for architectural change.

**Default answer to "should we add /v2?": no.** Propose an evolution path first. Escalate to
versioning only for genuinely architectural change (a different protocol or response paradigm),
and say explicitly that you are recommending an exception.

Scope note: the mechanics below (Sunset headers) are an API concern. In a templated project the same
*thinking* applies to route URLs, query parameters and anything a bookmark, integration or email
link depends on — but the announcement channel is a redirect and a changelog entry, not a header.

## Decision table

| Change | Approach |
| --- | --- |
| Fix a typo in a parameter name | Accept both for a period, deprecate the old. Versioning is overkill. |
| Add a response field | Just add it — additive changes are non-breaking. |
| Add a request parameter | Make it **optional** with a safe default. |
| Richer behaviour for richer input | Branch on the payload: old shape → old behaviour, new shape → enhanced. |
| Remove a field, change a type, tighten validation | Breaking. Deprecate with a sunset date, keep the old path until then. |
| Remove an endpoint or route | Deprecate with a sunset date; afterwards it answers 410 Gone (API) or permanently redirects (templated), and 404s once removed. |
| Move a page to a new URL (templated) | Serve it at the new URL and permanently redirect the old one straight away — the redirect is what keeps bookmarks and email links working. |
| Rework one endpoint fundamentally | A `v2` for **that endpoint only**, never the whole project. |
| A different response paradigm entirely | Genuine versioning. |

Old and new coexist for a reasonable window. The sunset date is a promise — do not shorten it
silently.

## Marking a deprecation (API-style projects)

Class-level attribute on the handler:

```php
#[ResourceDeprecation(
    sunset: '2099-01-01', // placeholder — use the real, future date agreed for this window
    link: 'https://docs.dotkernel.org/…/api-evolution/',
    deprecationReason: 'Replaced by GET /book/{id}/detail.',
    rel: 'sunset',
    type: 'text/html',
)]
class GetBookResourceHandler extends AbstractHandler
```

Mechanics:

- The deprecation middleware reflects the handler after dispatch and adds `Sunset:` and `Link:`
  response headers.
- Once the sunset date has passed, the middleware throws `ExpiredException` before the handler
  runs, and the endpoint answers `410 Gone` as problem details.
- `sunset` must be a valid date or the attribute constructor throws. It must also be in the
  future: a past date deprecates and kills the endpoint in the same change.
- If `link` is omitted, the middleware falls back to the documentation URL in
  `application.versioning` config.

Resulting response:

```http
HTTP/1.1 200 OK
Sunset: 2099-01-01
Link: https://docs.dotkernel.org/…;rel="sunset";type="text/html"
```

## Obligations that come with a deprecation

The attribute compiling is not "done". Also:

1. Mark the operation `deprecated: true` in the module's `OpenAPI.php` and name the replacement.
2. Update the documentation page describing the change and the recommended client update.
3. Note it in `CHANGELOG.md` (only if the user asks you to touch the changelog).
4. Add or extend a test asserting the `Sunset` header.
5. Keep the old path working until the sunset date. **Do not delete in the same change.**
6. Announce through the channels the project actually uses — headers, docs, release notes,
   newsletter — early enough for third-party developers to plan.

After sunset the endpoint already answers 410, so removal is a clean-up, not an emergency. Remove
the handler, its route, its authorization entry, its presentation metadata and its documentation
block in one later change: a removed endpoint should 404, not 500.

## Anti-patterns to flag

- `/v2/...` route groups, `?version=2`, or versioned media types added to a codebase that has
  chosen evolution.
- Renaming a response field in place "because the old name was wrong".
- Making an existing optional field required.
- Narrowing an enum or tightening a validator on a live route with no sunset window.
- Changing a success status code (200 → 204) on a live endpoint.
- Changing a route URL in a templated project without a permanent redirect from the old one.

If asked to do one of these, do it only after stating the breaking-change consequence and
offering the evolution alternative.
