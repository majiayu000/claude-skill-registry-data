---
name: api-security
description: "An API has no UI to hide things behind."
---

# API Security (Verbose)

## Core Patterns

### Object-Level Authorization

An API has no UI to hide things behind. Every identifier a client has ever seen
is an identifier it can replay against every endpoint. The dominant API
vulnerability class — broken object-level authorization — is not a missing
authentication check; the attacker is fully authenticated as themselves.

```python
# The check must be part of the lookup, not a step after it.
def load_invoice(invoice_id: int, principal: Principal) -> Invoice:
    row = (
        session.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .filter(Invoice.tenant_id == principal.tenant_id)   # non-negotiable predicate
        .one_or_none()
    )
    if row is None:
        raise NotFound()          # 404, not 403 — do not confirm existence
    return row
```

The structural fix is to make the unscoped query impossible to write: a
repository layer that only exposes `for_tenant(tenant_id)`, or Postgres
row-level security where the session variable carries the tenant.

```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON invoices
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

RLS is enforced by the database, so an ORM bug, a raw SQL report query, and an
ad-hoc admin script all inherit the same boundary. Note the asymmetry: `USING`
governs reads and updates of existing rows, `WITH CHECK` governs rows being
written — omit `WITH CHECK` and a tenant can insert rows attributed to another.

### Input as an Attack Surface

Validation is not about data quality here; it is about limiting what the
attacker can express.

```python
class TransferRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")   # unknown field -> 422, not ignored

    to_account: constr(pattern=r"^[0-9]{10}$")
    amount_cents: conint(gt=0, le=100_000_00)
    memo: constr(max_length=140) = ""
```

Three distinct failures this prevents:

| Failure | Mechanism | Consequence |
|---|---|---|
| Mass assignment | Body spread into model/ORM | Client sets `role`, `is_verified`, `balance` |
| Type juggling | Loose coercion of `"0"`, `[]`, `null` | Comparison and truthiness checks invert |
| Resource exhaustion | Unbounded strings, arrays, nesting | Memory blowup, regex catastrophic backtracking |

Validate at the boundary and pass the parsed object inward. Re-parsing the raw
body later invites parser-differential bugs, where the validating parser and the
consuming parser disagree about duplicate JSON keys or oversized integers.

### Server-Side Request Forgery

Any parameter that becomes an outbound request is an SSRF sink: webhook
registration, "import from URL", link unfurling, PDF/HTML rendering, XML with
external entities.

```python
BLOCKED = [ip_network(n) for n in (
    "127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
    "169.254.0.0/16", "::1/128", "fc00::/7", "fe80::/10",
)]

def assert_public(host: str) -> None:
    for info in socket.getaddrinfo(host, None):
        addr = ip_address(info[4][0])
        if any(addr in net for net in BLOCKED) or not addr.is_global:
            raise ValueError(f"blocked target: {addr}")
```

This is necessary and not sufficient. Validating a hostname then handing the URL
to an HTTP client leaves a TOCTOU window — DNS rebinding returns a public
address on the check and `169.254.169.254` on the connect. Robust designs pin
the resolved address into the connection, disable redirects (or re-validate each
hop), and put the egress behind a proxy with a destination allowlist. On AWS,
enforcing IMDSv2 removes the highest-value SSRF target, since token retrieval
requires a `PUT` that a naive proxied GET cannot perform.

### Error and Response Hygiene

```python
# ❌ Debug detail shipped to the caller
except IntegrityError as e:
    return {"error": str(e)}      # leaks table names, constraint names, values

# ✅ Correlate, don't disclose
except IntegrityError:
    ref = uuid4().hex
    log.exception("db integrity failure", extra={"ref": ref})
    return JSONResponse({"error": "conflict", "ref": ref}, status_code=409)
```

The same discipline applies to response bodies. Serializing the whole ORM object
because "the frontend ignores the extra fields" ships `password_digest`,
`internal_notes`, and other tenants' identifiers to anyone with curl. Define
explicit response schemas.

### Inventory and Lifecycle

You cannot secure endpoints you do not know about. Deprecated `/v1` routes,
staging hosts on public DNS, and internal debug handlers behind a
"nobody-knows-the-URL" assumption are the ones with the stale validation logic.
Enumerate routes from the framework's own router at build time and diff against
the published spec:

```python
routes = sorted(f"{m} {r.path}" for r in app.routes for m in sorted(r.methods))
```

Fail CI when a route exists that the OpenAPI document does not describe — the
gap is exactly where review never happened. Give deprecated versions a hard
sunset date and return `Deprecation` / `Sunset` response headers before removal.

## Common Anti-Patterns

❌ **Fetching by id, then checking ownership in the handler** — one forgotten
branch is a full cross-tenant read.
✅ Make tenant scope part of the query or enforce it in the database with RLS.

❌ **Returning 403 for another user's resource** — the status code itself
confirms the object exists and is a free enumeration oracle.
✅ 404 for anything the caller may not see.

❌ **Binding the request body directly to the persistence model.**
✅ A separate, `extra="forbid"` input schema and a separate output schema.

❌ **Trusting internal-only network position** — one SSRF or one compromised pod
puts the attacker inside that network.
✅ Authenticate service-to-service calls (mTLS or signed tokens) and authorize
them as first-class principals.

❌ **Rate limiting only unauthenticated traffic.**
✅ Per-principal quotas on expensive authenticated endpoints too — export,
search, and report generation are the usual denial-of-wallet vectors.

❌ **Validating a URL string and then following redirects with the default
client.**
✅ Re-validate every hop, or route all egress through an allowlisting proxy.

❌ **Logging the full request to debug an incident.**
✅ Redact `Authorization`, cookies, tokens, and PII at the logger, not by
convention.

## API Security Checklist

- [ ] Every object read/write is scoped by tenant or owner in the query itself
- [ ] Not-authorized and not-found are indistinguishable to the caller
- [ ] Input schemas reject unknown fields and bound string/array/nesting size
- [ ] Response schemas are explicit — no bare ORM serialization
- [ ] Function-level checks on admin/bulk endpoints, not just object-level
- [ ] All caller-supplied URLs pass an egress allowlist; redirects re-validated
- [ ] Cloud metadata endpoint unreachable from application containers
- [ ] Errors return a correlation id, never SQL, stack traces, or hostnames
- [ ] Route inventory generated from code and diffed against the spec in CI
- [ ] Deprecated API versions have a sunset date and monitored residual traffic
- [ ] Service-to-service calls are authenticated, not trusted by network position
- [ ] Auth failures, authz denials, and 429s are logged with principal and route
- [ ] Secrets come from a manager, and no credential appears in a log or URL
