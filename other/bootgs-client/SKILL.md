---
name: bootgs-client
description: Explains bootgs' Virtual Transport Layer contract (how doGet/doPost events must be shaped for the router to resolve a controller method) and how to build a client that calls a bootgs backend from a web app UI, an HtmlService sidebar/dialog via google.script.run, or a deployed web app URL. Use when building a frontend that talks to bootgs controllers, or when requests aren't reaching the expected route. Not for generating or syncing the spec itself (`bootgs-openapi`), nor for wiring the server's entry points (`bootgs-quickstart`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  framework: bootgs
---

# Bootgs Client

## Available files

- **`assets/gas-http-client.ts`** — a working `callBootgsApi()` client built on `google.script.run` (see below). Copy it in and adapt.

## Why this exists

A bootgs controller method is triggered by GAS calling the native `doGet(event)`/`doPost(event)` globals — GAS hands you an event object shaped by its own trigger system, not a URL and HTTP method your `fetch` call understands. bootgs's `RequestFactory` reconstructs an `HttpRequest` (method, pathname, query, body) out of that native event. The **Virtual Transport Layer** is the convention for what to put into the event so that reconstruction resolves to the route you intend. There is no bootgs-provided client — you build the caller side yourself, against this contract.

## The contract

| Field | Where it comes from | Notes |
|---|---|---|
| `method` | a `method` parameter (`GET`, `POST`, `PUT`, `DELETE`, ...) | This is virtual — GAS itself only ever actually invokes `doGet` or `doPost`. `method` tells the router which route to match, independent of which GAS global fired. |
| `pathname` (or `path`) | a `pathname`/`path` parameter | Must include the `apiPrefix` your app was configured with (default `"/api"`) — see `bootgs-quickstart`. Route placeholders (`{id}`) must already be substituted with real values; the router does not template on the client's behalf. |
| query params | plain key/value entries in the event's `parameter`/`parameters` map | Same map that carries `method`/`pathname` — GAS doesn't distinguish "framework" params from "your" params, they're all just query-string-derived key/values. |
| body | `postData.contents` (string) + `postData.type` | Only present on `doPost`. Send a JSON string and set `postData.type` to bootgs's `ContentMimeType.JSON` so the body is parsed rather than treated as opaque text. |
| headers | not natively supported | GAS triggers don't carry HTTP headers. If you need to pass metadata that isn't a query param or body field, JSON-stringify it into a `headers` parameter — this is a workaround, not a real header channel. |

## Two transport modes

**1. Deployed web app, called over real HTTP.** If `webapp.access` allows it, the `/exec` URL accepts real requests — but GAS always receives them as `doGet` or `doPost` regardless of the actual verb the browser sent, so `method` still travels as a query/body parameter, not as the request's real HTTP verb. A plain `fetch`/`axios` call works; just always target `doGet` with `POST`/`PUT`/`DELETE` mapped through the `method` param if you want to avoid CORS preflights, or `doPost` directly if the body needs to travel as `postData`.

**2. Embedded in Sheets/Docs/Slides (sidebar or dialog), via `google.script.run`.** No real HTTP exists here — you call the global proxy directly and construct the event object yourself:

```ts
function callBootgs(fnName: "doGet" | "doPost", event: Partial<GoogleAppsScript.Events.DoGet | GoogleAppsScript.Events.DoPost>) {
  return new Promise((resolve, reject) => {
    google.script.run
      .withSuccessHandler(resolve)
      .withFailureHandler(reject)
      [fnName](event);
  });
}
```

See `assets/gas-http-client.ts` for a complete, minimal client built on this that exposes a `fetch`-like `callBootgsApi(method, pathname, { query, body })` function — copy it in and adapt the parameter-map construction to your controllers.

## Gotchas

- **`apiPrefix` mismatch is the #1 "route not found" cause.** If the app was created with the default config, every path must start with `/api` — a client calling `/widgets` instead of `/api/widgets` gets a clean miss with no obvious error pointing at the prefix.
- **Path parameters are not templated for you.** bootgs's routes use `{id}`-style placeholders server-side (OpenAPI-compatible — see `bootgs-openapi`), but the client must send the already-substituted concrete path (`/api/v1/widgets/42`), not the placeholder form.
- **`google.script.run` callbacks are not promises.** Always wrap `withSuccessHandler`/`withFailureHandler` yourself (as above) before treating the call as awaitable — awaiting the bare `google.script.run[...]` call resolves immediately with the proxy object, not the result.
- **No real headers.** Don't design an auth scheme that depends on an `Authorization` header reaching the controller — it won't. Pass tokens as a body field or query param instead.
- **This pattern is safe from the private-function-naming pitfall, but only because it always targets `doGet`/`doPost`.** If the same add-on also exposes plain `google.script.run` calls outside the bootgs router — a menu action, a settings dialog — those functions must be public (no trailing `_`) or the call silently does nothing. See `apps-script-ui`.

## Verification

Before debugging further into bootgs internals, log the exact object your client builds and check it field-by-field against the contract table above (`method`, `pathname`, query params, `postData.contents`) — a malformed transport-layer payload is a far more common cause of "wrong controller called" or "404" than a router bug.
