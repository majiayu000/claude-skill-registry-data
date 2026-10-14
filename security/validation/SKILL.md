---
name: validation
description: "Validate at boundaries with Pydantic/runtime schemas; TS types do not validate runtime. Reject unknown fields where appropriate."
---

# validation

Trust nothing at the boundary: validate, then type.

## Activate when

- Handling external input: requests, webhooks, files, queue messages, CLI args, env config.

## Do NOT activate for

- Internal invariants (assertions/tests); auth decisions (see authentication/authorization).

## Procedure

1. Schema at every trust boundary (Pydantic/Zod/Bean Validation per stack, pinned versions); TypeScript types alone validate nothing at runtime.
2. Reject unknown fields on security-sensitive routes; coerce nothing silently; fail closed with one error envelope.
3. Validate files by content sniffing + limits (size, dimensions, count), never extension alone; quarantine user uploads (see security/secure-baseline).
4. Verify: invalid-input test matrix green (missing, wrong type, oversized, hostile strings), errors mapped to statuses without leaking internals.
