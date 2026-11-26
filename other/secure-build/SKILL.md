---
name: secure-build
description: Secure-by-default rules to follow while writing a web app or API, so vibe-coded and agent-built apps start out safe. Use whenever you create or materially change a web app, API, route handler, login or signup flow, database access, file upload, payment flow, admin page, or an AI feature that calls a model or tools. Covers access control, injection, secrets, sessions, CORS, headers, rate limits, uploads, SSRF, AI features, dependencies and backend-as-a-service rules.
allowed-tools: Read, Grep
---

# NightVision Secure Build

Rules to apply while you write the code, not after. They cover the mistakes that show up most often in apps built quickly with an AI agent. Following them does not make an app secure on its own: before you call the work done, offer `ship-check` (or run it, when the developer asked for a security check or their organization requires one), which scans the running app with NightVision and proves what holds up.

Apply these silently as you build. Do not lecture the developer or ask permission to write secure code; just write it that way, and mention a rule only when it changes something they asked for (for example, you refused to put an API key in frontend code).

## Access control (the most common failure)

- Deny by default. Every route that reads or changes user data requires an authenticated identity, established on the server from the session or token, never from a user ID, role or tenant sent by the client.
- Check ownership on every object. When a route takes an ID (`/orders/{id}`, `?userId=`, a body field), scope the lookup to the caller: `WHERE id = ? AND owner_id = ?`, or the framework's policy or permission layer. Checking after fetching is easy to forget on the next route; scoping the query is not. Return 404 for objects the caller does not own.
- List and search endpoints filter by the caller's user or tenant too, not only detail routes.
- Never bind request bodies straight onto models. Allowlist writable fields so a client cannot set `role`, `is_admin`, `owner_id`, `price` or `tenant_id`.
- Admin and internal routes sit behind an explicit role check on the server. Hiding a link in the UI is not access control.
- Run `authz-review` after adding routes that take object IDs.

## Injection

- Database access goes through parameterized queries or the ORM's query builder. Never build SQL, NoSQL filters or LDAP queries by concatenating or formatting user input, including column names and sort orders (allowlist those).
- No `eval`, `exec`, `Function()`, `pickle.loads`, unsafe YAML loaders or shell commands built from user input. When a subprocess is unavoidable, pass an argument list, never a shell string.
- Keep the template engine's auto-escaping on. Do not render user content with `dangerouslySetInnerHTML`, `v-html`, `|safe`, `html_safe` or `innerHTML` unless it went through a sanitizer such as DOMPurify.
- Validate input at the edge with a schema (types, lengths, formats), and reject what does not fit.

## Secrets

- Secrets come from environment variables or a secret manager. Never hardcode API keys, database passwords, JWT signing keys or webhook secrets, and never commit `.env` files: add them to `.gitignore` when you create them, and commit a `.env.example` with placeholder values instead.
- Anything bundled into frontend code is public. Variables prefixed `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_` and similar ship to every browser, so never put a server secret or a service-role key in them. Calls that need a secret go through a server route.
- If you find a secret already committed, tell the developer it must be rotated; deleting it from the latest commit does not remove it from history.

## Authentication and sessions

- Use the framework's or a well-known auth library (Auth.js, Django auth, Devise, Spring Security, ASP.NET Identity, a hosted IdP). Do not write your own password hashing, token format or session store.
- Hash passwords with bcrypt, scrypt or Argon2. Never MD5, SHA-1 or unsalted SHA-256.
- Session cookies are `HttpOnly`, `Secure` and `SameSite=Lax` or `Strict`. Do not keep session tokens in `localStorage` when a cookie will do.
- JWTs: verify the signature and the algorithm on every request, reject `alg: none`, set a short expiry, and keep the signing key server-side.
- Rate-limit login, signup, password reset and one-time-code routes, and give the same response whether or not the account exists.
- State-changing requests that rely on cookies need CSRF protection (the framework's middleware, or `SameSite` plus an origin check).

## Browser-facing settings

- CORS lists explicit trusted origins. Never reflect any origin, and never combine `*` with credentials.
- Send security headers: a Content-Security-Policy, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, and `frame-ancestors` (or `X-Frame-Options`). Use the stack's middleware (helmet, Django `SecurityMiddleware`, Spring Security headers) rather than hand-setting them per route.
- Debug mode, stack traces, verbose errors, GraphQL introspection in production, admin consoles and framework debug toolbars are off outside local development. Errors return a generic message and log the detail server-side.

## Files and outbound requests

- Uploads: check type by content, not only extension; cap the size; store outside the web root or in object storage under a generated name; never execute or serve them from the app's own origin without a safe `Content-Type` and `Content-Disposition`.
- Paths built from user input are resolved and checked against an allowed base directory before use.
- Server-side requests to a URL the user supplied (webhooks, link previews, image fetchers, import-from-URL) go through an allowlist, and block private ranges and cloud metadata addresses (169.254.169.254 and the cloud equivalents).

## AI features

- Treat model output as untrusted input: never pass it to `eval`, a shell, a SQL string or raw HTML.
- Tools a model can call get the least privilege that works. URL-fetching tools use an allowlist and block metadata addresses; tools that write data check the end user's permissions, not the app's.
- Keep secrets, other users' data and system credentials out of prompts and retrieved context.
- Put rate and cost limits on endpoints that call a model.

## Backend-as-a-service and data stores

- Supabase: enable Row Level Security on every table and write policies scoped to `auth.uid()`. The anon key is public by design, so a table without RLS is readable by anyone. The service-role key never reaches the client.
- Firebase: never ship test-mode rules (`allow read, write: if true`). Rules check `request.auth.uid` against the document's owner.
- Storage buckets are private unless the content is meant to be public.
- Databases, caches and admin panels are not exposed to the internet with default or empty credentials.

## Dependencies

- Use well-known, maintained packages and check that a package name is the real one before installing it. A plausible name you have not seen before may not exist, or may be a look-alike.
- Pin versions through the lockfile and do not downgrade a dependency to make an error go away.

## When you finish

Offer `ship-check` before telling the developer the app is done, or run it when a security check was asked for or is required. For a check of the source itself, the `source-intelligence` skill can also report hardcoded credentials and weak cryptography.
