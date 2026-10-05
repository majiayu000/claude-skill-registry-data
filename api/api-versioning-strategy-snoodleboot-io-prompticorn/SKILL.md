---
name: api-versioning-strategy
description: "Versioning exists because you cannot deploy your clients."
---

# API Versioning Strategy (Verbose)

## Core Patterns

### The Compatibility Contract

Versioning exists because you cannot deploy your clients. Once a third party — or
your own mobile app sitting in an app store review queue — depends on a response
shape, that shape is a contract, and the only safe assumption is that some caller
depends on every observable detail of it.

Classify every proposed change before you write it:

| Change | Compatible | Why |
|---|---|---|
| New optional request field | Yes | Old clients omit it; server defaults |
| New response field | Yes | Provided clients tolerate unknown keys |
| New endpoint | Yes | Nothing referenced it before |
| Relaxing a validation rule | Yes | Previously rejected input now succeeds |
| Removing / renaming a field | No | Client dereferences a missing key |
| Making a field required | No | Existing requests start failing |
| Tightening validation | No | Previously valid input now 400s |
| Changing a default | No | Behavior changes for callers who never opted in |
| New enum value in a response | No | Exhaustive client switches fall through |
| Changing pagination semantics | No | Cursors and page sizes are load-bearing |

The subtle entries matter most. Adding `status: "partially_refunded"` to an order
API is technically additive and practically a breaking change: every client with
`switch (status)` and no default branch now throws. If your enum will grow, say so
in the contract from day one and require clients to handle an unknown member.

### Choosing a Versioning Mechanism

| Mechanism | Example | Cacheable | Visible in logs | Verdict |
|---|---|---|---|---|
| URI path | `/v2/orders` | Naturally | Yes | Default choice |
| Custom header | `X-API-Version: 2` | Needs `Vary` | Only if logged | Workable |
| Accept header | `Accept: application/vnd.acme.v2+json` | Needs `Vary` | Rarely | Purist, painful |
| Query parameter | `/orders?version=2` | Yes | Yes | Muddles resource identity |

The REST-purity argument for content negotiation is real: `/orders/8812` names an
order, and `v1` versus `v2` is a representation of it, so it belongs in `Accept`.
Every practical force pushes the other way. URI versions are copy-pasteable into a
bug report, greppable in access logs, trivially routable at the gateway, and cached
correctly by every intermediary without a `Vary` header you will eventually forget.
Public APIs that chose header versioning almost universally ended up documenting a
URI shortcut anyway.

Whichever you pick, make the version explicit and required. "No version means
latest" guarantees that an unversioned integration written today will break on
your next release.

### Expand, Migrate, Contract

The only safe way to change an existing field is to never change it — add the new
one, move traffic, then remove the old one.

```python
# Phase 1 — EXPAND. Both shapes valid. Deployed alone.
def serialize_customer(c):
    return {
        "name": c.full_name,          # legacy, still populated
        "full_name": c.full_name,     # new canonical field
    }

def parse_customer(body):
    # accept either; prefer the new one
    name = body.get("full_name") or body.get("name")
    if name is None:
        raise Validation("full_name is required")
    return name
```

```python
# Phase 2 — MIGRATE. Instrument reads of the legacy field.
if "full_name" not in body and "name" in body:
    metrics.increment("legacy_field_read", tags={"field": "name",
                                                 "client": client_id})
```

Phase 3 removes `name` — but only when that counter has been flat at zero for
longer than your slowest client's release cycle. Mobile clients routinely have a
long tail of installs a year old; "zero for two weeks" is not zero.

The discipline that makes this work is that expand and contract are separate
deploys. Combined, they are a rename, and a rename has no rollback: the moment you
ship it, in-flight requests from old clients fail, and rolling back does not undo
the client-side errors already surfaced to users.

The same shape applies to database columns and to event schemas. It is the general
answer to "how do I change something two systems agree on when I only control one."

### Deprecation and Sunset

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: Sun, 01 Nov 2026 00:00:00 GMT
Sunset: Wed, 01 Apr 2027 00:00:00 GMT
Link: <https://api.acme.com/docs/migrate-v1-v2>; rel="deprecation"
Warning: 299 - "GET /v1/orders is deprecated; migrate to /v2/orders by 2027-04-01"
```

`Sunset` is standardized in RFC 8594 and names the moment the resource stops
responding. Machine-readable headers are what let a client's own monitoring flag
the problem; a human-readable changelog reaches nobody who is not already looking.

A workable timeline for an external API:

| Stage | Internal API | Public API |
|---|---|---|
| Announce + headers live | T | T |
| Direct outreach to top consumers | T + 1 week | T + 2 weeks |
| Brownout (short scheduled 410s) | T + 1 month | T + 4 months |
| Sunset | T + 3 months | T + 12 months |

Brownouts are the underused tool: return `410 Gone` for fifteen minutes on an
announced date. Every remaining integration discovers its dependency while there is
still time, instead of on the final cutover at 2am.

### Measuring Who Is Still There

You cannot retire a version you cannot see.

```
http_requests_total{api_version="v1", client_id="acct_8812", endpoint="/orders"}
```

Require an authenticated client identity on every request and label metrics with
it. This converts sunset from a political argument into a list of accounts to email,
and it is the only evidence that makes "no one uses that field" a fact rather than
a hope.

### Versioning Events, Not Just Endpoints

Published events are an API with a worse failure mode: consumers are asynchronous,
so a breaking change surfaces as a silently dead consumer rather than a 400. Put the
version in the payload and keep consumers tolerant readers — ignore unknown fields,
never fail on an unexpected enum:

```json
{"event": "order.created", "schema_version": 2, "data": {"order_id": "8812"}}
```

Route incompatible shapes to a new topic (`order.created.v2`) rather than mutating
the existing one in place; that is the expand/contract pattern applied to a bus.
See `microservices-communication-patterns` for consumer-side handling.

## Common Anti-Patterns

❌ **Renaming a field in one deploy.**
"It's a small change, we'll just rename `name` to `full_name`." There is no
rollback and every old client 500s on a missing key.
✅ Expand, migrate on telemetry, contract in a later release.

❌ **Adding an enum value to an existing field.**
`status` grows a `partially_refunded` member; clients with exhaustive switches
crash on an unhandled case.
✅ Document from day one that enums are open and clients must tolerate unknown
values, or introduce the new state in a new version.

❌ **Version-per-endpoint.**
`/v1/orders`, `/v3/customers`, `/v2/payments` — nobody can state what "the API"
is, and the test matrix is the product of every axis.
✅ One version for the whole surface, bumped rarely.

❌ **Treating "no version specified" as "latest".**
An integration written against today's latest silently breaks on your next
release, with no signal at integration time.
✅ Require the version. Reject unversioned requests with a 400 naming the fix.

❌ **Silently ignoring unknown request fields.**
A client sends `emailAddress` instead of `email_address`; you drop it, the request
succeeds, and the bug surfaces in production months later.
✅ Reject unknown fields with a 400 that names them.

❌ **Semver on a REST API.**
`/v1.4.2/orders` invites callers to pin patch versions and multiplies your live
surface.
✅ Integers for the URI (`v1`, `v2`). Reserve semver for SDKs and libraries.

❌ **Deprecating in the changelog only.**
✅ `Deprecation` and `Sunset` headers on every response, plus a brownout.

❌ **Maintaining old versions by forking the codebase.**
Two copies drift, and a security fix has to land twice.
✅ One implementation, with a thin translation layer mapping the old shape onto
the current internal model at the edge.

## API Versioning Checklist

- [ ] Every change classified as breaking or non-breaking before implementation
- [ ] Version required and explicit on every request; unversioned calls rejected
- [ ] Version in the URI path, applied to the whole API surface
- [ ] Enum growth policy stated in the contract; clients required to tolerate unknowns
- [ ] Field changes shipped as expand → migrate → contract, in separate releases
- [ ] Legacy field reads instrumented before any removal
- [ ] `Deprecation`, `Sunset`, and `Link` headers on deprecated responses
- [ ] Sunset window ≥ 12 months for public APIs, with a scheduled brownout
- [ ] Per-client, per-version request metrics available and reviewed
- [ ] At most two major versions live simultaneously
- [ ] Old versions served by a translation layer, not a forked codebase
- [ ] Unknown request fields rejected with a 400 naming the field
- [ ] Published events carry a schema version; incompatible shapes get a new topic
- [ ] Contract tests run old-client fixtures against the current server on every build
