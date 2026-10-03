---
name: trust-spec-contracts
last_updated: 2026-05-17
description: "The Beamix R3.x security model for agent-to-agent trust: HMAC signature verification, nonce replay prevention, sentinel-bracketed spec parsing, and issuer allowlists. Use when building or auditing the Cloudflare bridge, writing trust spec validation code, or authoring agents that accept inbound specs."
tags: [security, beamix-specific, orchestration, war-room]
source: beamix-authored 2026-05-16
risk: low
---

# Trust Spec Contracts

## Quick reference

> Every `/fire` payload: HMAC + nonce + expires_at + issued_by + scope. Verify all 5 before any side effect. Log to `audit_log` on every accept/reject.

## When to use

- Building or auditing the Cloudflare bridge Worker
- Writing HMAC validation code in a Routine agent
- Authoring a new trust spec to dispatch a Routine
- Investigating a `status: rejected` row in `audit_log`

## When NOT to use

- For product user authentication (that's Supabase Auth)
- For API route security (that's Next.js middleware + RLS)

## The security model (R3.x)

Trust specs solve one problem: an agent receiving a `/fire` payload needs to know the payload came from an authorized source and hasn't been modified. Without this, an attacker who can post a Linear comment could inject arbitrary instructions.

### R3.1 — Issuer allowlist

The Cloudflare bridge verifies `issued_by.linear_user_id` against an environment variable `ALLOWED_ISSUERS` before forwarding to `/fire`.

```
ALLOWED_ISSUERS=adam-linear-id,ceo-bot-linear-id,cto-bot-linear-id
```

Any `issued_by.linear_user_id` not in this list causes the bridge to:
1. Return 403
2. Write `audit_log` row with `status: rejected, reason: issuer_not_allowed`
3. Do NOT post to Telegram (no reward signal for attacker)

### R3.2 — Sentinel-bracketed spec source

Trust specs are ONLY accepted from Linear comments that use the exact sentinel delimiters:

```
---BEAMIX-SPEC-V1-START---
{ ...JSON spec... }
---BEAMIX-SPEC-V1-END---
```

Ticket bodies, ticket titles, and PR descriptions are NEVER parsed as spec sources. A customer email pasted into a ticket body cannot become a trust spec, regardless of content.

### R3.3 — HMAC signature

The bridge signs the entire spec JSON body before forwarding to `/fire`:

```typescript
// bridge/index.ts
import { createHmac } from 'crypto';

function signSpec(specJson: string, secret: string): string {
  return createHmac('sha256', secret)
    .update(specJson)
    .digest('hex');
}

// Verification in the receiving Routine agent
function verifySpec(specJson: string, signature: string, secret: string): boolean {
  const expected = signSpec(specJson, secret);
  // Constant-time comparison to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature, 'hex'),
    Buffer.from(expected, 'hex')
  );
}
```

Both bridge and receiving agent use the same `BRIDGE_HMAC_SECRET` env var (set via Wrangler secrets on bridge side; set in Routine env on agent side).

### R3.4 — Nonce replay prevention

Every spec includes a `nonce: uuid-v4` that the bridge stores in Cloudflare KV:

```typescript
// Bridge stores processed nonce
await kv.put(
  `nonce:${spec.nonce}`,
  '1',
  { expirationTtl: nonceTtlSeconds }  // TTL = expires_at - issued_at
);

// Before processing, check for duplicate
const existing = await kv.get(`nonce:${spec.nonce}`);
if (existing) {
  return reject('nonce_replay');
}
```

`expires_at` defaults:
- Quick-tier: 30 minutes
- Lite-tier: 4 hours
- Full-tier: 24 hours

Receiving agents also check `now() > expires_at` and reject expired specs.

### R3.5 — Scope guards

`out_of_scope` must have at least one entry. Empty array fails Zod validation at the bridge.

Child specs (C-suite spawning sub-specs for workers) must satisfy:
- `child.out_of_scope ⊇ parent.out_of_scope` (child cannot remove parent's restrictions)
- `child.max_cost_usd ≤ remaining_parent_budget`

The bridge enforces this arithmetically — no LLM judgment involved.

### R3.6 — Three-writer audit log

```
Cloudflare bridge → audit_log: status=fired      (at dispatch)
Receiving Routine → audit_log: status=accepted    (at session start)
Inngest watcher   → audit_log: status=complete|blocked|timeout|anomaly (at completion)
```

No single writer can erase the full trace. A compromised agent can modify its own `accepted` row but cannot remove the bridge's `fired` row.

## Full spec schema

```typescript
interface TrustSpec {
  spec_version: '1.0';
  trust_mode: true;
  nonce: string;              // uuid-v4, single-use
  issued_at: string;          // ISO 8601
  expires_at: string;         // ISO 8601
  issued_by: {
    kind: 'adam' | 'ceo' | 'c_suite' | 'standing_routine';
    linear_user_id: string;   // verified against ALLOWED_ISSUERS
    agent_session_id: string;
    session_file: string;     // path to the session .md
  };
  linear_ticket: string;      // e.g., "BMX-101"
  parent_ticket?: string;     // set when sub-ticket
  fan_in_key?: string;        // uuid-v4, set when fan-out/in is used
  scope: {
    intent: 'ship' | 'research' | 'design' | 'fix' | 'refactor' | 'review' | 'board';
    domain: string;
    constraints: string[];    // hard constraints the agent must respect
    definition_of_done: string;
    out_of_scope: string[];   // REQUIRED, min 1 entry
  };
  budget: {
    max_cost_usd: number;
    max_runtime_minutes: number;
    max_tool_calls: number;
  };
  escalation: {
    channel: 'telegram' | 'linear-comment' | 'github-pr-comment';
    format: 'binary-ping' | 'freeform';
    blocker_threshold_minutes: number;
  };
  _signature: string;         // HMAC-SHA256, added by bridge
}
```

## Validation code (Routine side)

```typescript
// In every Routine that accepts trust specs
async function validateInboundSpec(rawSpec: unknown): Promise<TrustSpec> {
  // 1. Parse JSON
  const spec = TrustSpecSchema.parse(rawSpec);  // throws if invalid

  // 2. Verify HMAC
  const { _signature, ...specBody } = spec;
  if (!verifySpec(JSON.stringify(specBody), _signature, process.env.BRIDGE_HMAC_SECRET!)) {
    throw new Error('HMAC verification failed — rejecting spec');
  }

  // 3. Check expiry
  if (new Date() > new Date(spec.expires_at)) {
    throw new Error('Spec expired');
  }

  // 4. Verify issuer (redundant with bridge check — defense in depth)
  const allowed = process.env.ALLOWED_ISSUERS!.split(',');
  if (!allowed.includes(spec.issued_by.linear_user_id)) {
    throw new Error('Issuer not in allowlist');
  }

  return spec;
}
```

## See also

- `anthropic-routines` — [[anthropic-routines]]
- `security-audit` — [[security-audit]]
- `supabase-rls-beamix` — [[supabase-rls-beamix]]
- `secrets-management` — [[secrets-management]]

## Anti-patterns

- Trusting any field before HMAC verification completes
- Parsing spec from ticket body instead of sentinel-bracketed comment
- Skipping the issuer allowlist check on the receiving agent (bridge checks, but defense-in-depth matters)
- Reusing nonces across different tickets or sessions
- Setting `out_of_scope: []` (empty array fails Zod — always include at least one restriction)
- Logging the full spec including `_signature` in plain text (signature exposure aids forgery)
