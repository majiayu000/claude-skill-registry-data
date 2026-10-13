---
name: api-mass-assignment
description: >
  Mass assignment / auto-binding privilege escalation. Load when an API binds JSON directly to
  a model (Rails, Spring, Django REST, Node/Mongoose), on signup/profile-update/create endpoints,
  or when responses expose fields you didn't send (role, isAdmin, balance, verified). Signals:
  ORM object binding, extra fields accepted silently.
domain: api
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp_api: [API3:2023-BOPLA]
cwe: [CWE-915]
tools: [burp, postman]
schema_version: 1
---

# Mass assignment (BOPLA)

## When it applies
An endpoint deserializes client JSON straight into a data object without an allowlist of
writable fields. You add sensitive properties the developer never meant to be client-writable.

## Why it works
Frameworks that auto-bind request bodies to models will set *any* matching attribute unless
explicitly restricted. If `role`, `isAdmin`, `account_balance`, `email_verified`, or
`user_id` are bindable, you set them by just including them in the body.

## Method
1. **Learn the object shape**: read a GET response for the object — every returned field is a
   candidate writable property. Also mine JS, mobile apps, and API docs for hidden fields.
2. **Inject sensitive fields** into create/update requests:
   `{"username":"x","password":"y","role":"admin"}` or `"isAdmin":true`, `"verified":true`,
   `"balance":999999`, `"user_id":<victim>`.
3. **Guess conventions** when fields aren't leaked: `is_admin`, `admin`, `roleId`, `groups`,
   `permissions`, `account_type`, `tenant_id` — try nested objects too (`{"role":{"id":1}}`).
4. **Chain**: set `user_id`/`owner_id` to a victim to combine with IDOR, or flip `verified`
   to skip email/2FA gates.

## Gotchas
- Extra fields silently ignored ≠ safe — confirm by reading the object back for your change.
- Some frameworks need the exact case/nesting; mirror the GET response structure.
- The writable field may only take effect on a specific endpoint/verb (create vs update).

## Verify success
A privileged attribute you supplied is persisted — re-fetch the object and see `role:admin`,
`verified:true`, or the elevated value reflected, and confirm the new capability works.

## References
OWASP API Security Top 10 (2023) API3; framework strong-params/allowlist docs.
