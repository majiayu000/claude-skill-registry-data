---
name: bb-csrf
description: Hunt modern CSRF — content-type-blocklist bypasses (typeless Blob POSTs, Chromium safelist additions like message/ad-auction-trusted-signals-request, missing-Content-Type-means-JSON parsers), GraphQL CSRF via GET and APQ hash smuggling, alias-amplified timing XS-Leaks, OAuth/MCP consent-screen CSRF, and classic token/Referer check gaps. Use whenever the user mentions CSRF, XSRF, cross-site request forgery, state-changing endpoints without tokens, content-type defenses, preflight bypasses, or "can I trigger this action from another site".
---

# Modern CSRF Hunter

CSRF was declared dead and isn't. The modern defense is "the request isn't a simple request, so the browser sends a preflight" — that defense breaks at three layers: the server's parser, the browser's safelist, and GraphQL's transport quirks. Techniques below from Voorivex Team research (2026) and paid/CTF-grade cases.

## Break 1 — The server parses more than the safelist allows

**Typeless Blob POST (works everywhere, paid on FastAPI):** a Blob with no `type` sends NO Content-Type header at all — no preflight, cookies attached:
```js
fetch(url, { method: "POST", credentials: "include",
             body: new Blob([JSON.stringify({email: "attacker@x.tld", action: "update"})]) });
```
FastAPI's (since-patched) `if not content_type_value: json_body = await request.json()` parsed the typeless body as JSON. Audit targets for "missing Content-Type falls back to JSON" parsing.

**Headerless primitives:** anything that posts without settable headers — `<form>` (urlencoded/multipart/text-plain), navigation requests, `no-cors` fetch with Blob — combined with lenient parsing is the attack surface.

## Break 2 — The browser safelist is bigger than the server thinks

Fetch spec simple-request Content-Types: `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`. Servers blocklist exactly these three — but Chromium's `IsCorsSafelistedLowerCaseContentType` briefly had a FOURTH, default-on entry: `message/ad-auction-trusted-signals-request` (Protected Audience API):
```js
fetch(url, { method: "POST", credentials: "include",
             headers: { "Content-Type": "message/ad-auction-trusted-signals-request" },
             body: JSON.stringify({...}) });
```
No preflight on unpatched Chrome/Edge/Brave — sailed past every server blocklist including Apollo Server's `NON_PREFLIGHTED_CONTENT_TYPES`. Lesson: diff browser source against the spec — Chromium-only safelist additions are default-on bypasses. Re-test "blocked" content-type CSRF on browser updates.

## Break 3 — GraphQL transports

- **POST blocked, GET isn't**: Apollo Server's `preventCsrf` only fires on non-simple content types; mutations via GET with `query`/`variables`/`operationName` as URL params skip it entirely (body-parser only guards POST).
- **APQ defeats URL length limits**: prime persisted queries server-to-server (POST full query + `extensions.persistedQuery.sha256Hash`), then the victim's browser needs only `/graphql?extensions={"persistedQuery":{"version":1,"sha256Hash":"<hash>"}}` — tiny URL, arbitrary query content.
- **Timing XS-Leak turns unreadable responses into an oracle**: `performance.getEntriesByName(url).duration` measures download time. Amplify hit-vs-miss with aliases — thousands of `h123:text@include(if: true)` fields balloon a matching response to tens of KB. SLOW (>10ms, 5 trials) = character match → append to the leaked prefix, re-prime, walk secrets character by character. Works because GET+APQ is a simple request the victim's browser performs cross-site with cookies.

## Classic checks (60-second pass, still pays)

- State-changing GET (`GET /api/user/delete?...`) — tokens "verified" only on POST.
- Token present but unvalidated / not bound to session / accepted from any account.
- `Referer` check: missing-Referer accepted? `<meta name="referrer" content="no-referrer">` on your attacker page makes it absent.
- `SameSite=Lax` blocks cross-site POST but NOT top-level navigation GET — any state change reachable by GET link-click is still exploitable; also check cookie exceptions (Lax+POST 2-minute window after link click).
- Consent screens and OAuth DCR flows (registration endpoints have no CSRF token — see bb-oauth MCP section).

## Workflow

1. Inventory state-changing endpoints (authenticated browser pass; js-recon for the full API surface).
2. For each: identify the defense (token? content-type requirement? SameSite? Referer?).
3. Try the matching break: typeless Blob → fourth-safelist content type → GET transport → classic gaps.
4. PoC from a separate origin (local file or your page): the action must complete with the victim's cookies and NO user interaction beyond visiting.
5. Impact: state what changed (email/password change → ATO-grade; settings change → justify).

## Verdict + evidence

- Deliverable: standalone HTML PoC that performs the action on a logged-in victim, plus before/after evidence on YOUR OWN test account.
- A CSRF that only changes cosmetics = Low; email/password/2FA/MFA-method change = High (chain to ATO via bb-chains).
- Never fire PoCs at other users' accounts — self-account before/after is the accepted proof.
