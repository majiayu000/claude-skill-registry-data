---
name: secure-coding
description: Use when writing code that handles untrusted input, authentication, or sensitive data. Covers injection prevention, authentication and session handling, authorization, cryptography, and the defaults that make code safe by construction.
metadata:
  category: security
  version: 1.0.0
  tags: [security, owasp, injection, authentication, crypto]
---

# Secure Coding

## Purpose

Write code where the secure path is the default path. Most vulnerabilities are not clever — they are a string concatenated into a query, an authorization check that was never written, or a password hashed with the wrong algorithm.

## When to Use

- Writing code that handles user input, authentication, or sensitive data.
- Implementing authorization.
- Handling passwords, tokens, or encryption.
- Reviewing code for vulnerabilities.

## Capabilities

- Injection prevention: SQL, command, template, LDAP, XSS.
- Authentication: password storage, session management, MFA, token handling.
- Authorization: enforcing it at the right layer, and the object-level checks people forget.
- Cryptography: choosing the right primitive and not implementing it yourself.
- Secure defaults: headers, cookies, TLS.

## Inputs

- The code, and where untrusted data enters it.
- The authentication and authorization model.
- Compliance requirements, if any.

## Outputs

- Parameterized queries and encoded output, everywhere.
- Authorization enforced on every object access, not just at the route.
- Secrets and credentials handled with the correct primitives.

## Workflow

1. **Identify the trust boundaries** — Every place data enters from outside: HTTP, files, queues, environment, third-party APIs. Everything crossing one is untrusted, including data from your own other services.
2. **Parameterize, never concatenate** — Every query, command, and template. String interpolation into SQL is the oldest vulnerability there is, and it is still the most common.
3. **Authorize on the object, not the route** — A route guard checks that you are logged in. It does not check that *this* order belongs to *you*. Broken object-level authorization is the most prevalent API vulnerability in practice.
4. **Use the right crypto primitive** — Argon2id or bcrypt for passwords. AES-GCM or libsodium for encryption. HMAC for signing. Never design your own scheme, and never use MD5, SHA-1, or plain SHA-256 for passwords.
5. **Fail closed** — On error, deny. An authorization check that throws and is caught by a generic handler returning 200 has granted access.
6. **Set the defaults** — Secure cookies, CSP, HSTS, and TLS configuration. These are one-time changes that eliminate whole vulnerability classes.

## Best Practices

- An ORM does not make you safe from SQL injection if you use its raw-query escape hatch with an f-string.
- Never log a password, token, session ID, or full card number — including in an exception's message or a request dump.
- Comparing secrets with `==` leaks their length and content through timing. Use a constant-time comparison.
- A JWT with `alg: none` accepted by your verifier is a full authentication bypass. Pin the algorithm; never trust the header's claim about it.
- Validate on an allowlist, not a denylist. You cannot enumerate every malicious input, but you can enumerate every valid one.
- Rate-limit authentication endpoints. Without it, a leaked password list is a working login.

## Examples

**The vulnerability that route-level auth does not catch:**

```python
# The route requires a login. It does not check that the order is the user's.
@router.get("/orders/{order_id}")
@requires_auth                                   # authenticated, but not authorized
async def get_order(order_id: str, user: User = Depends(current_user)):
    return await db.orders.get(order_id)         # any user can read any order

# Correct: authorization is a property of the object, not the route.
@router.get("/orders/{order_id}")
async def get_order(order_id: str, user: User = Depends(current_user)):
    order = await db.orders.get(order_id)
    if order is None or order.customer_id != user.id:
        # Same response for "does not exist" and "not yours": do not leak existence.
        raise HTTPException(404, "Order not found")
    return order
```

**Passwords and token comparison:**

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import hmac

ph = PasswordHasher()                            # Argon2id, correct parameters by default

def hash_password(plain: str) -> str:
    return ph.hash(plain)                        # salt is generated and embedded

def verify_password(plain: str, stored: str) -> bool:
    try:
        ph.verify(stored, plain)
        return True
    except VerifyMismatchError:
        return False

def verify_webhook(signature: str, expected: str) -> bool:
    # `==` on secrets leaks information through timing. This does not.
    return hmac.compare_digest(signature, expected)
```

**Parameterized, always:**

```python
# Injectable. The ORM does not save you here.
await db.execute(f"SELECT * FROM orders WHERE status = '{status}'")

# Safe.
await db.execute("SELECT * FROM orders WHERE status = :status", {"status": status})
```

## Notes

- Broken object-level authorization (BOLA/IDOR) is consistently the top API vulnerability. Every endpoint that takes an ID must check that the caller may access *that* object. A route guard is not enough.
- Returning 404 rather than 403 for objects the user may not access prevents enumeration — a 403 confirms the object exists.
- Argon2id is the current recommendation for password hashing. bcrypt remains acceptable. PBKDF2 is acceptable where required by compliance. A bare hash — even SHA-256 — is not password hashing, it is a lookup table waiting to be built.
