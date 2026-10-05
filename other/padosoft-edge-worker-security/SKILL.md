---
name: padosoft-edge-worker-security
description: >-
  Use this skill when code runs at the edge in front of an origin — a Cloudflare Worker or equivalent that
  proxies, renders or caches on behalf of a backend. It covers who owns a control when two layers could
  implement it, cross-site request forgery validated at the edge, the two-hop client-address model, header
  forwarding and what must never reach the origin, private caching and key design, cross-origin policy,
  cookies, server-side rendering at the edge, secrets and bypass tokens, and edge rate limiting. Also when
  the user says a request is blocked and nobody knows by which layer, a header is being spoofed, a cached
  page showed another user's data, a bypass works with only a user agent, or asks whether a control is
  really on. Do not use it for the origin application's own review, for CDN configuration, or for edge
  performance tuning.
license: MIT
compatibility: >-
  Written for a Cloudflare Worker with KV, native rate-limiting bindings and a template engine; the
  reasoning applies to any reverse-proxy layer that can make decisions before the origin sees the request.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: When two layers could enforce a control, each assumes the other does and nobody does.
  profiles: node, api
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: cloudflare, worker, edge, csrf, cors, cache, kv, ssr, rate limiting, proxy, headers
---

# Edge worker security

An edge worker is not a thin proxy. It terminates the request, decides things the origin will never see,
renders pages, and caches. It is a **security boundary of its own** — and the failure mode that produces
most of the damage is not a bug in it, it is the ambiguity between it and the origin.

**The rule: every control has exactly one owner, written down. When two layers could enforce it, each
assumes the other does, and nobody does.**

---

## 1. Split-brain is the headline risk

Anti-forgery, header trust, rate limiting, redirect policy, security headers: the edge and the origin can
each implement them. Whenever they both can:

- **Name the owner in both repositories**, in a comment at the place where the other layer would have done
  it. A reader of either side must learn, from that side, who actually enforces it.
- **If both sides keep a list** — exclusions, allow-lists, trusted paths — those lists are one artefact with
  two copies, and they drift. Align them in the same change, or generate one from the other. An exclusion
  added on one side only leaves the route uncovered on **both**.
- **Do not assume a control is on. Open the file and read the flag.** A switch built as a literal in the
  source is the production value; a switch read from configuration may be absent. When the origin delegates
  to the edge and the edge is disabled, the control does not exist anywhere — and everything looks normal.

## 2. Anti-forgery, when the edge is the gate

Six invariants. Each one has been violated in a shipped implementation that looked correct.

1. **Path matching for exclusions is one-way and anchored to a segment.** The question is *does the request
   path fall under an excluded prefix*, never the reverse — the reverse excludes the **ancestors** of every
   entry. Anchor on the separator, or `/checkout-evil` falls under `/checkout`. Normalise trailing wildcards:
   compared as a literal segment, `*` matches nothing, which is an exclusion that never excluded anything.
2. **The token cookie and the server-side secret share one expiry, read from the store.** Recomputing the
   cookie's lifetime on every page while the secret keeps its original one makes the token outlive the
   secret: every write then fails, permanently, with no way out but clearing cookies. Issue from **one
   function** that re-issues when the secret is gone, rather than returning an orphan token.
3. **Validate before the fetch to the origin.** A check after it can only replace the response — the write
   already happened. Forgery is **blind** by definition: the attacker does not need to read the answer, only
   to cause the effect.
4. **The token must arrive through a channel a third-party site cannot populate**: a request header, or a
   form field. A value that comes **only from cookies proves nothing**, because the browser attaches cookies
   to forged cross-site requests too — that is not double-submit, and what was actually blocking those
   requests was the cookie's same-site attribute. Check the origin header (falling back to the referrer)
   as well, and check provenance **before** reading the body.
5. **Identity cookie strictly server-only; token cookie deliberately readable.** The front end has to read
   the token to send it back in a header. That is not weaker than putting it in the page, which is equally
   reachable by script — and a cross-site scripting flaw defeats every anti-forgery token in every design.
6. **Constant-time comparison, and a refusal that identifies the layer without describing internal state.**
   Use `403`, never `401` — that one means *not authenticated* and can trigger login flows or a browser
   prompt. Put a **marker and a code** in the message: a bare 403 on a write is indistinguishable from the
   origin's, the firewall's or the platform's, and whoever is debugging cannot even tell which layer
   answered. The code says *which check failed*; it never says what the backend holds.

Before switching it on: the front end must already send the token on every tenant, the exclusion lists must
be aligned, then enable on staging and watch the refusal codes — they distinguish "the channel is missing"
from "the provenance is wrong" immediately.

## 3. The client address is a two-hop model

There is no single true header for every hop.

| Hop | Trust | Because |
|---|---|---|
| Client → edge | the header the platform sets itself | it is overwritten at the edge, so an inbound value cannot survive |
| Edge → origin | the header the **edge forwarded** | at the origin, the platform's own header now contains the *edge's* address |

An "enterprise" variant that carries the client address is **spoofable inbound** until a managed transform
is guaranteed to overwrite it; until then, refuse it at the edge.

And the whole model holds only while **the origin refuses traffic that did not come through the edge**.
Without that, every forwarded address header is attacker-controlled — see **`padosoft-security-baseline`**.

## 4. Forwarding is a deny-list, so every new internal header is a decision

Everything not listed passes to the origin. Therefore:

- **Strip every worker-only and bypass header before each fetch**, from one helper, applied at *every*
  forwarding point — there is always more than one.
- **Mock-authentication headers must be on that list.** If public traffic can forward them, anyone
  impersonates any customer or operator. This is the single highest-severity item on the list.
- **Do not strip the client's genuine authorisation header** — it belongs to the origin.
- **Any new internal header is added to the deny-list in the same change**, or it reaches the origin.
- **Diagnostic headers are stripped globally in production** and emitted only behind an explicit gate.

## 5. Caching, and keys

- **Anything that depends on a user, a body, a market or a cookie is private and not stored.** A shared
  cache keyed on the URL alone serves one customer's page to another.
- **The dynamic subrequest to the origin needs the same policy**, not only the response: disable caching,
  turn off cache-everything, and strip any caching directives the caller supplied. Remove the downstream
  cache-control variants from the response too.
- **A key built from a client-supplied identifier is an object-reference flaw** — see
  **`padosoft-tenant-isolation`**.
- **Keys need bounded cardinality.** Reject over-long paths, reduce long ones to a digest, and do not write
  a persistent entry for a lookup whose input is unbounded — that is a storage amplification anybody can
  trigger.
- **A purge endpoint is authenticated by a header in production**, never a query parameter, and its route
  match is **anchored**, never a substring. Prefix purges stay restricted to known prefixes.
- Before introducing a genuinely public cache: a complete key (user, market, language) and an isolation test
  across users and markets.

## 6. Cross-origin policy

- **Never reflect an arbitrary origin with credentials**, and never a wildcard with credentials.
- Reflection goes through one resolver that accepts only a **canonical origin** — the parsed origin must
  equal the input — then matches exactly against the allow-list, then by host suffix **only over HTTPS**.
- **Validate the configured suffixes fail-closed**: at least two labels, a restricted character set, no
  leading or trailing hyphen, an alphabetic or punycode top label, and refuse bare addresses and top-level
  domains.
- Emit the allow headers **only** when the resolver returns a value; on refusal, remove them.
- **Merge the vary header rather than appending**, and put expose-headers on the real response, not only on
  the preflight.
- The preflight's allowed headers are an explicit allow-list — and internal or mock headers never go in it.

## 7. Cookies

One factory, with secure on by default, a same-site value, HTTP-only opt-in, and **no-store forced when
same-site is none**. Sanitise name and value against header splitting.

Identity cookies are HTTP-only; the anti-forgery token cookie is the deliberate exception. And **the
encoding of a cookie shared with another system is a contract**: changing it unilaterally breaks the reader
on the other side.

## 8. Rendering at the edge

- **Pick the sink, not a generic escape**: HTML, a value inside a script block, a quoted string in
  JavaScript, a URL. They are different encodings, and using one for another is the vulnerability.
- **Templates escape by default**; the raw form is only for content already made safe by those helpers.
- **Never hand-roll a sanitiser with a regular expression** for rich HTML or for URLs. Refuse
  script-bearing and data schemes, network-path references, backslashes, embedded credentials, control
  characters, and anything over a length cap.
- **An unknown content component fails closed** into a placeholder, with every field truncated **before**
  escaping.
- **Per-request context, never module-level mutable state.** This is the trap specific to a long-lived
  isolate: a helper that caches something in module scope leaks it into the next request, which belongs to
  somebody else. Carry the context explicitly, or in the runtime's request-scoped storage.

## 9. Secrets and bypasses

- **Nothing in the repository**, and the secret fields in versioned configuration stay empty strings.
  Runtime values come from the platform's secret store, with every variable documented by name in the
  example file.
- **A user agent is never authentication.** An identifier that on its own grants access **is a password**,
  and it is one that gets logged, shared and copied into a support ticket.
- **Verify in this order: length cap → exact format → constant-time comparison.** The cap comes first, so a
  huge value costs nothing. Salts come from the cryptographic random source, never the ordinary one.
- A bypass that has been temporarily reduced to something weaker is a **dated debt**, not a design. Do not
  extend it to a second surface.

## 10. Rate limiting at the edge

- **Use the platform's native counters.** An in-memory counter protects one isolate; an eventually-consistent
  store gives an answer that was true somewhere, a moment ago.
- **Three modes, and the default is off.** A dark rollout touches nothing. A *log* mode consumes the buckets
  exactly as enforcement would and never blocks, which is the only way to learn the real thresholds. Only
  then, enforce.
- **An unrecognised or absent mode value must never block traffic.** A typo in a variable is not a reason to
  return errors to everybody.
- **Key on the platform's own address header plus the tenant.** Never on a forwarded or client-supplied
  value — that is a limiter the client chooses the bucket for.
- **Verified crawlers bypass every bucket, in every mode.** Rate-limiting a verified search crawler is
  direct, self-inflicted damage. Accept only the explicit positive signal.
- **Payment callbacks are exempt from the write bucket and stay under the global cap.** An allow-list
  derived from the real routes, not a pattern.
- **In enforcement, a missing binding or a malformed address fails closed with a server error**, not a pass.
- **Starting thresholds are guesses** until log mode has shown the peak per address, the shape of
  shared-address traffic and the clients' burst behaviour.

---

## Gotchas

- **Combining a zero cache lifetime with a no-store directive throws** in at least one runtime, which turns
  a privacy fix into an outage. Set the policy one way.
- **"It is behind the edge" is a statement about the origin's firewall**, not about your code.
- **There is always more than one forwarding point.** The helper that strips headers must be applied at all
  of them; grep for the fetch, not for the helper.
- **A refusal without a layer marker costs hours.** Three layers can return the same status for different
  reasons on the same request.
- **A long-lived isolate keeps module state between requests from different people.** Everything that looks
  like a harmless memo is a cross-request leak.
- **Configuration built as a literal in the source cannot be overridden at runtime**, whatever the
  environment suggests — which is good for a security floor and surprising for everything else.

## Checklist

- [ ] Every shared control has one named owner, stated on both sides
- [ ] Duplicated lists aligned in the same change, or generated from one source
- [ ] The enabling flag was **read**, not assumed
- [ ] Anti-forgery: anchored one-way matching · one expiry from the store · validated before the origin fetch
      · token from a non-cookie channel · provenance checked before the body · constant-time · 403 with a marker
- [ ] Client address: platform header at the edge, forwarded header at the origin, origin closed to the outside
- [ ] Deny-list applied at every forwarding point; mock-auth headers on it; authorisation not stripped
- [ ] Diagnostic headers stripped in production
- [ ] Personalised responses private and not stored, on the response **and** the subrequest
- [ ] No key from a client identifier; cardinality bounded; purge endpoint anchored and header-authenticated
- [ ] Cross-origin: canonical resolver, no reflection with credentials, suffixes validated, vary merged
- [ ] Cookies through one factory; shared-cookie encoding unchanged
- [ ] Correct sink per context; no hand-rolled sanitiser; unknown components fail closed
- [ ] No module-level mutable state shared between requests
- [ ] Secrets absent from the repository; no user-agent-only bypass; cap → format → constant-time
- [ ] Rate limiting on native counters, default off, unknown mode never blocks, verified crawlers exempt

## Final report

```
Worker: <name>  ·  origin(s): <…>
Ownership: csrf <edge|origin> · headers <…> · rate limit <…> · redirects <…>
Flags read: <flag> = <value> (from source | config)
Duplicated lists: <which, aligned? how>
Forwarding points: <n> — deny-list applied at all: yes | no
Cache: personalised responses <policy> · subrequest <policy> · keys <shape, cardinality>
Rate limiting: mode <off|log|enforce> · key <…> · exemptions <…>
Origin closed to non-edge traffic: yes | no | unknown  ← everything above depends on it
```
