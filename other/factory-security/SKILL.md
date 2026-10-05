---
name: factory-security
description: Security conventions for builds that touch sensitive data, regulated industries, or AI-generated code paths. Covers KMS encryption at rest, BAA verification for PHI in email/SMS, safe URL redirects, admin-client bypass guardrails, in-memory rate-limiter caveats, the "read-only by default" stance for AI-generated code, mandatory-review-queue pattern, and request tracing for support workflows.
---

# Factory security

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the KMS / Resend / Upstash shape we use), and **Failure mode** when there's one to name.

## Sensitive data at rest — encrypted with context binding

**Principle.** Sensitive data (SSN, government IDs, PHI fields, financial accounts) is KMS-encrypted at rest, with encryption context bound to the row's identity.

**Why.** Encryption alone protects against database exfiltration but not against row-shuffling — an attacker who can write to the database can swap encrypted blobs between rows, and the system decrypts each happily. Binding the encryption context to the user ID (or org ID) means KMS refuses to decrypt the blob when the context doesn't match — the row-shuffling failure mode becomes a decryption failure, which is loud.

**Recipe.**

```ts
// Encrypt on write
const encryptedSSN = await kms.encrypt(plaintext, {
  keyId: KMS_KEY_ID,
  context: { userId },
});
await db.update(users).set({ ssnEncrypted: encryptedSSN }).where(eq(users.id, userId));

// Decrypt on read — only in the handler that actually needs plaintext
const plaintext = await kms.decrypt(user.ssnEncrypted, { context: { userId } });

// Mask for display — never decrypt for display surfaces
const masked = `***-**-${plaintext.slice(-4)}`;
```

## PHI in email/SMS — BAA at runtime, not in comments

**Principle.** Provider BAA status for PHI-bearing channels (email, SMS) is asserted at runtime; comments don't enforce.

**Why.** A `// TODO: confirm Resend BAA before prod` comment in the email helper is exactly as enforced as no comment at all. A runtime assertion that refuses to send PHI when the BAA-signed env var isn't `true` is enforcement: the bug becomes an outage, which is loud and gets fixed. Comments rot; assertions don't.

**Recipe.**

```ts
// In src/lib/email/resend.ts
if (process.env.RESEND_BAA_SIGNED !== 'true' && containsPHI(message)) {
  throw new Error('Cannot send PHI without signed BAA. Set RESEND_BAA_SIGNED=true after confirmation.');
}
```

**Failure mode.** Kairos shipped the BAA check as a comment; the comment rotted, PHI was nearly sent in staging before someone noticed.

## Safe URL redirects

**Principle.** Validate any redirect URL that comes from user input; never trust query-param `next=` values.

**Why.** Same principle as `factory-auth.md §OAuth callback safety`. Open-redirect is a recurring bug class; the defense is a small allowlist check.

**Recipe.**

```ts
function safeNext(next: string | null): string {
  if (!next) return '/';
  if (next.startsWith('//')) return '/';     // protocol-relative
  if (!next.startsWith('/')) return '/';     // not relative
  return next;
}
```

Apply in OAuth callbacks, login redirects, post-signup redirects, and any place a URL comes in from a query param.

## Admin-client bypass — always wrapped, never at module scope

**Principle.** Service-role / RLS-bypass clients live behind a wrapper that re-checks privilege; never at module scope.

**Why.** Same principle as `factory-auth.md §admin client — always wrapped`. Module-scope admin client is a loaded gun; the wrapper makes the privilege check unavoidable at every call site.

**Recipe.**

```ts
export async function withAdmin<T>(
  fn: (admin: AdminClient) => Promise<T>,
): Promise<T> {
  await requireAdmin();           // verify caller is admin first
  return fn(createAdminClient());
}
```

## Rate limiting — Redis on serverless, in-memory only as prototype

**Principle.** Production rate limiting on serverless uses Redis (or equivalent shared store); in-memory limiters don't survive horizontal scaling.

**Why.** A `Map<key, count>` in module scope works fine on one server. On Vercel, AWS Lambda, or any platform with horizontal scaling, each instance has its own memory — the limiter resets across instances, and the effective limit is `(per-instance limit) × (instance count)`. The fix is a shared store. Upstash Redis is the lowest-friction option; the migration is a one-day swap.

**Recipe.**

```ts
const ratelimit = new Ratelimit({
  redis: new Redis({ url: process.env.UPSTASH_URL, token: process.env.UPSTASH_TOKEN }),
  limiter: Ratelimit.fixedWindow(10, '60 s'),
});

const { success } = await ratelimit.limit(`${bucket}:${subject}`);
if (!success) throw new RateLimitError();
```

In-memory rate limiters are acceptable for prototype phase only.

**Failure mode.** Kairos shipped an in-memory rate limiter to prod with a comment acknowledging it; the comment didn't migrate to Upstash until a user-facing incident.

## AI-generated code — read-only by default

**Principle.** Code paths reachable by AI-generated code default to read-only; write access is opt-in per feature and surfaces in a review queue.

**Why.** ~45% of AI-generated code has vulnerabilities (Veracode). The harness layer carries the defense, not the model. Read-only by default means a runaway agent can't corrupt production data; opt-in writes per feature means the write paths are auditable; mandatory review means the human stays in the loop. The cost is some friction on the happy path; the benefit is the catastrophic failure mode never ships.

**Recipe.**

1. **Read-only by default.** Database connections, file system access, external APIs default to read-only. Write access is opt-in per feature and surfaces in the review queue.
2. **Mandatory review before prod.** No code path that mutates production data ships without explicit human approval. Lift from the Stripe Minions Blueprint / Cursor PR-flow pattern.
3. **Version snapshots.** Every AI-generated change has a "last working" rollback target. A versioned blob is enough.
4. **Token budget per customer.** Per-customer cap on agent invocations to prevent runaway loops.

This is the explicit differentiator vs. consumer vibe-coding tools (Lovable, Replit, v0). The harness's job is to make AI-generated code *safe to ship*.

**Failure mode.** Base44, Replit prod-DB wipe, Cursor RCE — public incidents where the model touched production state without a review queue.

## Auth surface — DB-backed members, JWT signatures, fallback user-linking

**Recipe only** — the principles live in `factory-auth.md`:

- DB-backed members table from day one (not hardcoded allowlist) — see `factory-auth.md §hardcoded email allowlists`.
- Verify JWT signatures on every request — see `factory-auth.md §JWT signature verification`.
- Fallback user-linking on first valid-token request — see `factory-auth.md §fallback user-linking on first valid token`.

## Secrets management

**Principle.** Customer secrets never live in the factory's repo; they live in the customer's cloud secrets manager.

**Why.** The single-tenant customer-cloud model (see `factory-deployment.md`) is the commercial wedge — customer data residency, customer-controlled secrets. Putting customer secrets in the factory's repo defeats the model, makes the factory's compliance posture cover the customer's compliance posture, and creates a leak surface that the customer can't audit.

**Recipe.**

- Use env vars validated through `t3-oss/env-nextjs` for the project's own env.
- Customer secrets at the customer-deployed harness level: AWS Secrets Manager or GCP Secret Manager.
- RDS IAM authentication for AWS DBs (see `factory-deployment.md §RDS IAM authentication`).

## Logging — log actions and IDs, not payloads

**Principle.** Audit logs record *what* happened, not *the full payload*. PII in logs creates compliance scope creep.

**Why.** Once a payload with PII lands in the log stream, the log stream inherits the PII's protection requirements — same access controls as the source database, same retention policy, same audit trail. The cost of getting this wrong is that the logging system becomes a compliance surface. The fix is to log structurally: `{ user_id, action, timestamp }`, never `{ user_id, action, payload }`.

**Recipe.**

- **Log:** `{ user_id, action: 'updated_ssn', timestamp }`
- **Don't log:** `{ user_id, action: 'updated_ssn', old_value: '123-45-6789' }`

Redact at the logger layer if you can't avoid it at the call site.

## Request tracing — trace ID at the boundary

**Principle.** Every request carries a trace ID, attached at the middleware boundary, propagated through downstream calls, surfaced in response headers.

**Why.** When something breaks at a customer, the trace ID is what unblocks the support conversation — the customer sees the ID in a response header, the engineer greps it across logs. Without the ID, support becomes "approximately when did this happen?" and "can you reproduce?" — both expensive questions. The cost is one middleware function; the savings are every incident.

**Recipe.**

```py
@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response
```

Log it everywhere. See `factory-observability.md` for the broader observability frame.

## Audit logging at the mutation boundary — fire-and-forget

**Principle.** Audit logs never block the mutation. Log delivery is best-effort; surface failures to ops, not to users.

**Why.** Same principle as `factory-api.md §audit logging at mutation boundary` and `factory-data-layer.md §activity log table`. Awaiting the audit log makes one slow log call into one slow mutation.

**Recipe.**

```ts
export async function updateFoo(input: FooUpdateInput) {
  await requireAuth();
  const updated = await db.update(foo).set(input).where(eq(foo.id, input.id)).returning();

  // Fire-and-forget — swallow errors so the mutation succeeds
  logAdminAction({ action: 'foo.update', subject_id: input.id, actor_id: user.id })
    .catch((err) => console.error('audit log failed', err));

  return updated;
}
```

## Source patterns

Kairos (safeNext, admin-client wrapping, in-memory rate limit acknowledgement, BAA comment, activity logging), duezy (KMS for SSN, RDS IAM auth, encrypted-at-rest pattern), cothon (request logging middleware, JWT verification with fallback user linking, soft-delete mixin), encode/monorepo (email allowlist anti-pattern), Obsidian software-factory-idea (AI-code-risk stance, read-only-by-default, mandatory review queue).
