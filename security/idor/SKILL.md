---
name: idor
description: IDOR — detection, authorization enforcement, ID strategy.
---

# IDOR — Insecure Direct Object Reference

IDOR occurs when an application uses user-controlled input to access objects directly without verifying the requesting user has permission to access that specific object.

---

## What It Looks Like

```http
# Attacker changes 42 → 43 and gets another user's order
GET /api/orders/43
Authorization: Bearer <attacker-token>
```

The endpoint fetches `Order::find(43)` without checking `order.user_id === currentUser.id`.

**IDOR is not just IDs.** Any reference to an object that can be guessed or enumerated is vulnerable: filenames in URLs, email addresses as keys, UUIDs if predictable or leaked.

---

## Detection Patterns

Flag these patterns in code review:

```php
// BAD — no ownership check
$order = Order::find($request->id);
return $order;

// GOOD — scope query to authenticated user
$order = Order::where('id', $request->id)
              ->where('user_id', auth()->id())
              ->firstOrFail();
```

```python
# BAD
order = Order.objects.get(pk=pk)

# GOOD
order = Order.objects.get(pk=pk, user=request.user)
```

```ts
// BAD
const invoice = await Invoice.findByPk(req.params.id)

// GOOD
const invoice = await Invoice.findOne({
  where: { id: req.params.id, userId: req.user.id }
})
```

---

## Authorization Enforcement Rules

1. **Every object fetch must be scoped to the owner or authorized principal** — never fetch then check; scope the query directly
2. **Role checks are not substitutes for ownership checks** — an admin role grants broad access by definition; a regular user with a valid token must still be scoped
3. **Soft-deleted records**: scoping to `user_id` alone is not enough if soft-delete is used — also filter `deleted_at IS NULL` to prevent accessing deleted objects
4. **Nested resources**: `/users/{userId}/orders/{orderId}` — verify both that the authenticated user is `userId` AND that the order belongs to that user
5. **Bulk endpoints**: `/orders?ids[]=1&ids[]=2` — apply ownership filter on the entire set; never return a subset silently (either all authorized or error)

---

## ID Strategy

| ID type | IDOR risk | Recommendation |
|---------|-----------|----------------|
| Sequential integer (1, 2, 3) | HIGH — trivially enumerable | Use UUIDs for external-facing IDs |
| UUID v4 | MEDIUM — not guessable, but still must enforce ownership | Always enforce ownership; UUIDs are not access control |
| UUID v7 (time-ordered) | MEDIUM — sortable; leaks creation time | Acceptable for most use cases; enforce ownership |
| Slugs | MEDIUM — guessable if predictable pattern | Enforce ownership; avoid slug = user-controlled string |
| Indirect reference (hash map on server) | LOW | Good pattern; map user-visible token → real ID server-side |

> **UUIDs prevent enumeration but do NOT prevent IDOR.** A leaked UUID (from a URL, log, or referrer header) is still exploitable without ownership checks.

---

## BOLA vs IDOR

These terms overlap — OWASP API Security Top 10 uses BOLA (Broken Object-Level Authorization):

- **IDOR** = the vulnerability (referencing objects without authorization)
- **BOLA** = the API-specific framing from OWASP API Security 2023 (#1)

Same root cause, same fix. When auditing APIs, use the BOLA framing from the `security-checklist` skill.

---

## Test Cases (Required)

For every endpoint that accepts an object ID, write these tests:

| Test | Expected result |
|------|----------------|
| Owner accesses their own object | 200 OK |
| Authenticated user accesses another user's object | 403 Forbidden or 404 Not Found |
| Unauthenticated user accesses any object | 401 Unauthorized |
| Soft-deleted object accessed by owner | 404 Not Found |
| Bulk endpoint with mixed owned/unowned IDs | 403 or only return owned subset with explicit error |

```ts
// Example test (framework-agnostic)
it('returns 403 when user accesses another users order', async () => {
  const other = await createUser()
  const order = await createOrder({ userId: other.id })

  const res = await request(app)
    .get(`/api/orders/${order.id}`)
    .set('Authorization', `Bearer ${currentUser.token}`)

  expect(res.status).toBe(403)
})
```

---

## Review Checklist

| Item | Severity |
|------|---------|
| Object fetched without user scope | CRITICAL |
| Sequential IDs on external-facing resource endpoints | HIGH |
| Role check present but ownership check absent | HIGH |
| Nested resource route missing parent ownership check | HIGH |
| Bulk endpoint returns unauthorized objects silently | HIGH |
| Soft-deleted records accessible via ID | MEDIUM |
| No IDOR test cases for new endpoints | MEDIUM |
