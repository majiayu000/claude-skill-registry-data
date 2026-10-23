---
name: flask-pitfalls
description: "Use when a Flask application is written, configured or deployed: async views and what they do and do not buy on a WSGI worker, tasks spawned from a view, app and request context errors and proxies handed to another thread, teardown callbacks, debug mode and the interactive debugger, the development server reaching production, SECRET_KEY and key rotation, request size and form limits, trusted hosts, session cookie settings and the signed client-side session, and running behind a reverse proxy with ProxyFix."
---

# flask-pitfalls

A defensive block for a Flask service. The three parts share one premise:
**Flask is a WSGI application whose worker handles one request at a time, and almost every default is chosen
for the development server**. What bites in production is a development default that stayed (debug, no size
limit, any `Host`), a request-scoped object used outside the request (a context proxy, a task started by a
view), and a proxy that was never declared. Generic web hardening is in `skills/security-hardening`; Python
language and tooling points are in `skills/python-conventions` and `skills/python-hygiene-pitfalls`; blocking
calls inside async Python code are in `skills/python-async-no-blocking-calls`.

## When
- A Flask view, error handler or hook is made `async`, or a background task is started from a request.
- `RuntimeError: Working outside of application context` or `... request context` appears, or a proxy such as
  `request` or `g` is passed to a thread.
- An app factory initialises an extension, a database or a CLI command that reads `current_app`.
- The service is configured for production: debug, secret key, session cookie, upload and form limits, hosts.
- The service sits behind a reverse proxy or a hosting platform, and a URL, scheme or client address is wrong.

## Steps

**Read only the part the task meets.** They are independent.

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Async views, background tasks, extensions, context errors, proxies across workers, teardown | a view is `async`, work outlives a request, or a context error appears | [`01-async-and-context.md`](./references/01-async-and-context.md) |
| 2 | Debug mode, secret key and rotation, size and form limits, trusted hosts, session cookie | configuration is written or reviewed for production | [`02-config-limits-and-sessions.md`](./references/02-config-limits-and-sessions.md) |
| 3 | Development server and debugger, WSGI server entry point, reverse proxy | the service is started, deployed or put behind a proxy | [`03-running-in-production.md`](./references/03-running-in-production.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: an `async` view was called under the real WSGI server and a
task it spawned was shown to finish or not (part 1.2), a request with a body over the configured limit got a
413 and a request with an unlisted `Host` got a 400 (part 2.3, 2.4), the app was started the way production
starts it and the interactive debugger page was not reachable (part 3.1), and a request through the proxy
showed the real client address and scheme in the application (part 3.3). A configuration that was only read is
not verified.

## Guardrails
- Never leave debug mode or the interactive debugger on in a deployed service, and never serve production
  traffic from `flask run` (part 2.1, part 3.1).
- Never spawn a task from a view with `asyncio.create_task` and expect it to finish (part 1.2).
- Never pass `request`, `session`, `g` or `current_app` to another thread; pass the value, or the real object
  (part 1.4).
- Never commit or paste a real `SECRET_KEY`, and never reuse the documentation example (part 2.2).
- Never leave the request size and form limits unset on an endpoint that accepts uploads (part 2.3).
- Never add `ProxyFix` when there is no proxy, and never guess how many proxies set each header (part 3.3).
- This block states the Flask documentation as of the commit read on the date in
  [`references/origin.md`](./references/origin.md); configuration defaults can differ in another Flask
  version, and nothing was run while writing the block.

## Origin
Rewritten from the Flask documentation (pallets/flask, BSD-3-Clause), read 2026-10-16. 🟡: never run by us; open
points are in [`references/origin.md`](./references/origin.md).
