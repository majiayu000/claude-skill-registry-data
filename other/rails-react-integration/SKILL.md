---
name: rails-react-integration
description: Use when React/TypeScript code talks to a Rails backend — choosing the integration mode (Inertia, JSON API, or islands), typing and validating Rails JSON on the client, sending CSRF and session credentials from fetch, mapping Rails 422 validation errors into forms, and paginating Rails collections.
license: MIT
---

# Rails ↔ React Integration

## Purpose
Own the contract between a Rails server and a React/TypeScript client so neither side assumes what the other sends. The server side of each contract belongs to the Rails skills; this skill owns the client side and the fit between the two.

Composes with:
- `rails-api-integration` for the server wire contract, versioning, and error shape;
- `rails-authentication` and the `browser-api-auth-boundary` pattern for session versus token credentials;
- `rails-validations` and the `validation-error-contract` pattern for the 422 body;
- `react-agent-skills / typescript-runtime-contracts` for runtime validation of untrusted JSON (separate pack);
- `react-agent-skills / react-data-fetching` for cache identity, invalidation, and mutations (separate pack).

## Composing with react-agent-skills
Full-stack work uses this pack for the server and the boundary, and `react-agent-skills` for everything inside the client. Neither pack owns the other's side.

| Concern | Owner |
|---|---|
| Serializer, wire shape, versioning, error body | this pack (`rails-api-integration`) |
| Session, CSRF, forgery protection, token issuance | this pack (`rails-authentication`, `rails-security`) |
| Validation rules and the 422 contract | this pack (`rails-validations`) |
| Integration mode, client parser fit, field-to-attribute mapping, cache-key inputs | this pack (`rails-react-integration`) |
| Components, hooks, state, client caching, client tests, accessibility | `react-agent-skills` |

Client-side skill for each seam concern (all in `react-agent-skills`, installed separately with `npx skills add shubhamtaywade82/react-agent-skills`):

| Seam concern | Load from react-agent-skills |
|---|---|
| Typed client for Rails JSON | `react-agent-skills / typescript-api-contracts`, `react-agent-skills / typescript-runtime-contracts` |
| Query cache, mutations, pagination keys | `react-agent-skills / react-data-fetching` |
| Forms showing Rails 422 errors | `react-agent-skills / react-forms-validation` |
| Session cookie, CSRF, logout, expiry in the browser | `react-agent-skills / browser-authentication` |
| 401/403/5xx recovery UX | `react-agent-skills / react-error-resilience` |
| Action Cable consumers | `react-agent-skills / frontend-realtime` |
| Inertia versus JSON API versus islands, client side | `react-agent-skills / react-architecture` |
| Generated client from a Rails OpenAPI document | `react-agent-skills / openapi-tooling` |
| Client and end-to-end tests | `react-agent-skills / react-testing-engineering`, `react-agent-skills / frontend-e2e` |

Hand-off rules:
- A contract change starts on the Rails side, then the client parser and types move in the same change.
- A client-only change, such as a component, a hook, or a render-performance fix, does not route here.
- When `react-agent-skills` is installed, load the row's skills for the client side instead of using this skill's reference example as frontend guidance.
- When only this pack is installed, do the boundary work here and name the client-side follow-up and the react-agent-skills skill that owns it, rather than improvising frontend guidance.

## Activate when
- a React component or hook calls a Rails endpoint;
- choosing or changing how Rails serves React (Inertia, JSON API with a separate client, or React islands in ERB/Hotwire pages);
- a React form submits to Rails and must show Rails validation errors;
- adding pagination, filtering, or sorting that crosses the boundary;
- a request fails with 401, 403, 422 (`InvalidAuthenticityToken` or validation), or a shape mismatch between Rails JSON and TypeScript types.

## Repository inspection
- Integration mode: `Gemfile` (`inertia_rails`, `vite_rails`, `jsbundling-rails`, `importmap-rails`), `app/frontend` or `app/javascript`, and how React mounts (Inertia page components, a separate client repo, or `data-*` mount points in ERB).
- Server contract: the controllers and serializers (`as_json`, Jbuilder, serializer classes) that produce the JSON, `config/routes.rb` API namespaces and versions, and the error-rendering convention (`rescue_from`, 422 body shape).
- Auth: `protect_from_forgery` settings, `csrf_meta_tags` in the layout, `ActionController::API` versus `Base` controllers, CORS configuration, and any token model.
- Client: the existing HTTP wrapper, runtime-validation approach (hand-written guards, a schema library, or generated types), query/cache library, and form library.

## Decision rules
- Use one integration mode per application or clearly bounded area, and record it. Inertia keeps Rails routing, sessions, and authorization and has no public API; a JSON API plus separate client needs a versioned contract and an explicit auth decision; islands receive already-authorized props from the server-rendered page.
- The Rails serializer is the source of truth for the wire shape. TypeScript types describe what the client expects; a runtime check at the boundary is what catches drift. Generated types (OpenAPI or similar) are fine if the repository already produces them — do not add a generator for one endpoint.
- Map snake_case to camelCase and parse dates exactly once, at the boundary, never in components.
- Same-origin browser clients authenticate with the Rails session cookie and send `X-CSRF-Token` from `csrf_meta_tags` on every non-GET request. Do not disable `protect_from_forgery` to make fetch work, and do not store session or bearer tokens in `localStorage`.
- Cross-origin or third-party clients use the token path from `browser-api-auth-boundary`, not the session cookie.
- Treat 401 (re-authenticate), 403 (not permitted), 404, and 422 (fix input) as distinct outcomes. A 422 from `InvalidAuthenticityToken` is a CSRF bug, not a validation error.
- Map each Rails validation error to a form field through an explicit attribute-to-field table; errors on `base` or unmapped attributes are shown, never dropped.
- Client-side validation is a usability aid; Rails validations and database constraints remain authoritative.
- Paginate with a stable, unique server-side ordering. The page cursor or number, filters, and sort are all part of the client cache key.
- UI visibility is not authorization: hiding a button never replaces the Rails policy check on the endpoint.

## Implementation procedure
1. Identify the integration mode and the Rails endpoint, serializer, and error convention that own the contract.
2. Write or extend the TypeScript type and the runtime parser for the response, including nullability and enum values.
3. Route requests through the repository's HTTP wrapper; add CSRF and `credentials: "same-origin"` there if it is the session path.
4. Handle 401, 403, 404, 422, and unexpected statuses explicitly; map 422 bodies to field and base errors.
5. Put every result-changing input into the query key and the request URL.
6. Test the boundary: parser acceptance and rejection, CSRF header present on mutations, error mapping, and a Rails request test that pins the JSON shape the client parses.

## Anti-patterns / failure modes
- `as Order` casts on `response.json()` with no runtime check, so a renamed Rails attribute becomes `undefined` in the UI;
- `skip_forgery_protection` or `protect_from_forgery with: :null_session` added to silence `InvalidAuthenticityToken`;
- session or API tokens in `localStorage`, readable by any injected script;
- dropping Rails `base` errors or errors for attributes the form does not render;
- converting casing or parsing dates ad hoc inside components;
- offset pagination over a non-unique sort, producing duplicate or skipped rows;
- mixing Inertia pages, a JSON API, and islands for the same resource without a recorded reason.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```ts
// Submitting a React form to a Rails endpoint in a same-origin app.
type FieldErrors = Partial<Record<"sku" | "quantity", string[]>>;
type SubmitResult =
  | { kind: "created"; id: string }
  | { kind: "invalid"; fields: FieldErrors; base: string[] }
  | { kind: "unauthenticated" };

const FIELD_FOR_ATTRIBUTE: Readonly<Record<string, keyof FieldErrors>> = { sku: "sku", quantity: "quantity" };

export async function createOrder(input: { sku: string; quantity: number }): Promise<SubmitResult> {
  const token = document.querySelector<HTMLMetaElement>('meta[name="csrf-token"]')?.content;
  if (!token) throw new Error("csrf-token meta tag missing");

  const response = await fetch("/api/v1/orders", {
    method: "POST",
    credentials: "same-origin", // Rails session cookie; no token in localStorage
    headers: { "Content-Type": "application/json", Accept: "application/json", "X-CSRF-Token": token },
    body: JSON.stringify({ order: input }), // matches params.expect(order: [:sku, :quantity])
  });

  if (response.status === 401) return { kind: "unauthenticated" };
  if (response.status === 422) {
    const body = (await response.json()) as { errors?: { attribute: string; message: string }[] };
    const result: SubmitResult = { kind: "invalid", fields: {}, base: [] };
    for (const error of body.errors ?? []) {
      const field = FIELD_FOR_ATTRIBUTE[error.attribute];
      if (field) (result.fields[field] ??= []).push(error.message);
      else result.base.push(error.message); // never drop an error the user cannot see
    }
    return result;
  }
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const created = (await response.json()) as { id?: unknown };
  if (typeof created.id !== "string" && typeof created.id !== "number") throw new Error("created.id missing");
  return { kind: "created", id: String(created.id) };
}
```

## Agent review checklist
- Is the integration mode identified and consistent with the rest of the application?
- Does the client validate the Rails response at runtime, not only by type annotation?
- Do state-changing requests carry the CSRF token, and are no credentials stored in `localStorage`?
- Are 401, 403, 422, and CSRF failures handled as different outcomes?
- Does every Rails validation error reach the user, including `base` and unmapped attributes?
- Do cache keys and request URLs include every pagination, filter, and sort input?
- Is there a Rails request test pinning the JSON shape the client depends on?

## Verification
Run the client boundary tests (parser, error mapping, CSRF header, 401/422 handling) and a Rails request test for the same endpoint that asserts the status and JSON keys. When the mode is Inertia, assert the Inertia component name and props in a request test instead of a JSON body.

## Source foundation
- Rails Security Guide, CSRF: https://guides.rubyonrails.org/security.html#cross-site-request-forgery-csrf
- Action Controller `protect_from_forgery`: https://api.rubyonrails.org/classes/ActionController/RequestForgeryProtection/ClassMethods.html
- Active Model Errors: https://api.rubyonrails.org/classes/ActiveModel/Errors.html
- Inertia Rails: https://inertia-rails.dev/
- Fetch API, credentials: https://developer.mozilla.org/en-US/docs/Web/API/RequestInit#credentials

## Book cross-reference: *Modern Front-End Development for Rails*

Chapters 4, 6–8, and 11–15 cover React integration, TypeScript, bundling, server communication, state management, and Cypress testing. Use these as design prompts, not mandates to add React, Redux, TypeScript, or Cypress. Choose the smallest frontend boundary matching the application and compose with the separately owned React/TypeScript skills for component internals. Validate tool/API guidance against current repository dependencies; the book describes Rails 7 and React 17-era tooling.
