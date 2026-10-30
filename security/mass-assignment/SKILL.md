---
name: mass-assignment
description: Detects ORM create/update calls that spread request bodies without an explicit
  field allowlist. Use when writing code that creates or updates database
  records from request body, form data, or JSON input. Also invoke when
  spreading, merging, or destructuring request payloads directly into ORM
  model create/update calls without an explicit field allowlist.
---

# Mass Assignment Check (API3:2023)

## What this checks

Protects against mass assignment (also called auto-binding or object injection) where
an attacker adds unexpected fields like `role=admin` or `is_verified=true` to a request
body and the ORM blindly persists them. Exploitation leads to privilege escalation,
account takeover, and data corruption.

## Vulnerable patterns

- ORM create or update call that spreads, merges, or destructures the raw request body, deserialized payload, or query parameters into the model
- DTO-to-entity copy utility invoked with no field allowlist or exclude list, copying every matching field
- Decoded payload bound directly into a database struct or record that includes privileged columns
- Endpoint that lets the caller set fields like role, permissions, admin flags, verification status, balance, or tenant id from the payload

## Fix immediately

Flag the vulnerable pattern and explain the risk. Then suggest a fix that establishes
these properties:

1. **No ORM create/update call receives the raw request body.** Requests land in a
   dedicated input type (DTO, validated schema, typed struct, sealed class) that
   contains only the fields external callers may set. Fields the input type does
   not mention are silently dropped by the deserializer.
2. **Privileged fields are set server-side, never from input.** Roles, permissions,
   admin flags, verification status, balances, owner ids, and tenant ids come
   from the authenticated session or database defaults — never from the payload,
   even after "validation".
3. **DTO-to-entity copy utilities copy only named fields** or explicitly exclude
   protected ones. A blanket field-by-field copy with no ignore list is the exact
   bug — the safe form names the fields.
4. **The allowlist lives next to the type, not scattered at call sites.** A
   filter set repeated at every endpoint is brittle; the typed input pattern
   makes omission a compile-time (or deserialization-time) guarantee.

Translate these principles to the ORM, validation library, and deserializer of the
audited file's language. Use the framework's documented allowlist or typed-input
mechanism — do not hand-roll field filtering at the call site.

## Verification

Confirm the following properties hold (language-agnostic):

- [ ] No ORM create/update call receives the raw request body, deserialized payload, or spread/merged object without an explicit field allowlist or a dedicated input type that excludes sensitive columns
- [ ] Privileged fields (role, permissions, is_admin, is_verified, balance, owner_id) are never settable from external input — they are set server-side or omitted from the input type
- [ ] If a DTO-to-entity copy utility is used, it either copies only named fields or explicitly excludes protected fields

## References

- CWE-915 ([Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html))
- [OWASP API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
