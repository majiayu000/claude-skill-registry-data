---
name: edge-and-cdn-delivery
description: "A CDN is a cache that obeys your origin's instructions."
---

# Edge And CDN Delivery (Verbose)

## Core Patterns

### Why "Just Put a CDN In Front" Fails

A CDN is a cache that obeys your origin's instructions. It does not guess what is
cacheable — it reads `Cache-Control` (and friends) from the origin response and
acts on them. Turn a CDN on in front of an origin that sends `no-store`, or sends
no cache headers at all, and one of two things happens: every request still reaches
origin (you added a network hop and gained nothing), or the CDN applies a
conservative default that is wrong for your content. The work of a CDN is almost
entirely the work of setting correct headers.

```
# Fingerprinted, content-addressed asset — safe to cache indefinitely
Cache-Control: public, max-age=31536000, immutable

# Dynamic HTML — edge-cache briefly, serve stale while refreshing
Cache-Control: public, s-maxage=60, stale-while-revalidate=600

# Truly per-user, secret — never cache anywhere
Cache-Control: private, no-store
```

Two directives do different jobs and must be set independently:

- `max-age` — how long the **browser** may reuse its copy.
- `s-maxage` — how long a **shared cache** (the CDN) may. Overrides `max-age` for
  the CDN only.

A common, effective split: short `s-maxage` so the edge revalidates often, longer
or `immutable` on the fingerprinted assets the HTML references.

### Fingerprinting: Design Away Invalidation

The single highest-leverage pattern is content-hashed asset names.

```
index.html            ->  references  /static/app.9f3a1c.js
                                       /static/main.4b7e02.css
Cache-Control on those .js/.css:  max-age=31536000, immutable
Cache-Control on index.html:      s-maxage=60, stale-while-revalidate=600
```

Because a change to `app.js` produces a *new* filename (`app.aa12bc.js`), the old
and new versions coexist in cache and there is nothing to purge. A deploy only has
to publish the short-lived HTML that points at the new URLs. This moves the vast
majority of your bytes — the static assets — into permanent cacheability while
keeping deploys atomic. You never race a purge.

### The Cache Key and `Vary`

The cache key is what the CDN uses to decide whether an incoming request matches a
stored object. Get it wrong in either direction and hit rate collapses.

- **Query strings.** By default many CDNs include the full query string in the key.
  Marketing tags (`?utm_source=...`, `?fbclid=...`) then make every share a unique
  URL and a guaranteed miss, even though the response body is identical. Strip or
  ignore params that do not affect the response; keep only the ones that do
  (e.g. `?page=2`).

- **`Vary`.** Each distinct value of a `Vary`ed header forks the cache. `Vary:
  Accept-Encoding` is fine and necessary — there are a few encodings. `Vary:
  Cookie` or `Vary: User-Agent` is catastrophic: cookies and UA strings are nearly
  unique per user, so the cache stores a separate copy per visitor and the hit rate
  approaches zero. If content genuinely varies by user, it usually should not be in
  a shared cache at all (`private`).

```
Vary: Accept-Encoding          # good — small, bounded set
Vary: Cookie                   # bad — shatters the cache per user
```

### Invalidation vs Versioning

Purging is the tool people reach for and should not.

| | Versioning (fingerprints) | Invalidation (purge) |
|---|---|---|
| Propagation | Instant — new URL, new object | Eventual across all PoPs; seconds to minutes |
| Reliability | Deterministic | May be rate-limited; can partially fail |
| Fit | Routine deploys | Emergencies: leaked/wrong/legal takedown |

Purges are eventually consistent across every edge location and often
rate-limited, so a deploy pipeline that *depends* on a purge landing everywhere in
time is fragile. Design so purges are the exception — fingerprinted assets never
need one — and keep purge for the genuine emergency: a response that leaked
something, or is simply wrong and cannot wait for TTL expiry.

### Serving Stale and Shielding the Origin

Two patterns protect both latency and the origin.

`stale-while-revalidate` lets the edge return the expired copy immediately and
refresh it in the background. The user never blocks on an origin round trip; the
next user gets the fresh copy. This turns a cache miss from a latency spike into a
non-event.

Origin shielding (tiered caching) designates a single mid-tier cache that is the
only layer allowed to talk to origin. Without it, an object that expires or was
never cached triggers a fetch from *every* edge PoP that receives a request — a
thundering herd that can knock over an origin during a traffic spike or right after
a purge. With a shield, origin sees one fetch and the mid-tier fans it out.

```
client -> nearest edge PoP -> shield (single mid-tier) -> origin
                    ^                    |
                    +-- cache fill  <----+
```

### Edge Compute: What Belongs at the Boundary

Edge runtimes (CDN functions/workers) run small code at the PoP, before or instead
of hitting origin. They are excellent for boundary logic and poor for anything
heavy.

Good fits:
- Request/response rewriting, redirects, adding security headers
- Auth and token checks (reject before the request reaches origin)
- A/B and geo routing, feature-flag gating
- Lightweight personalization (assembling from cached fragments)

Poor fits:
- Anything that needs your primary database — the edge is far from your data, and
  the round trip erases the latency win
- CPU-heavy work — edge runtimes cap CPU time per request and expose a restricted
  API surface

The mental model: the edge decides *how to route and shape* a request cheaply and
close to the user; origin (or a regional service) does the *real work*. For
absorbing read load on dynamic data behind the edge, see
**distributed-caching-design**; for the bandwidth economics of what you serve, see
**cloud-cost-optimization**.

## Common Anti-Patterns

❌ **Enabling a CDN and declaring victory** while the origin sends `no-store` or no
cache headers. Origin traffic is unchanged.
✅ Set explicit `Cache-Control`/`s-maxage` per content type; verify hit rate at the edge.

❌ **Unfingerprinted assets** that force a cache purge on every deploy.
✅ Content-hash asset filenames; cache them `immutable`; version only the HTML.

❌ **`Vary: Cookie` / `Vary: User-Agent`,** or leaving tracking query params in the
cache key. Hit rate collapses toward zero.
✅ `Vary` only on headers that change the body; strip non-significant query params.

❌ **Deploy pipelines that depend on a purge propagating in time.** Purges are
eventual and rate-limited.
✅ Version to deploy; reserve purge for emergencies.

❌ **No origin shield.** A cold object or a purge causes every PoP to stampede origin.
✅ Enable tiered caching / a shield so origin sees one fill per object.

❌ **Edge functions calling a database or doing heavy compute.** Latency win lost,
runtime limits hit.
✅ Keep edge logic to routing, auth, and header/response shaping; do real work at origin.

## Delivery Checklist

- [ ] Every content type has an explicit, intentional `Cache-Control`
- [ ] `s-maxage` (edge) and `max-age` (browser) set separately and deliberately
- [ ] Static assets content-fingerprinted and cached `immutable`
- [ ] HTML entry point short-TTL so new asset URLs are picked up
- [ ] Cache key strips non-significant query params
- [ ] `Vary` limited to headers that actually change the body
- [ ] `stale-while-revalidate` used so misses don't block users
- [ ] Origin shield / tiered cache enabled to prevent stampedes
- [ ] Purge reserved for emergencies, not routine deploys
- [ ] Edge compute limited to routing, auth, and header/response shaping
- [ ] Edge cache hit rate and origin offload measured, not assumed
