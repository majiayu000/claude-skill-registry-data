---
name: token-broker-client
description: "Brokered short-lived provider credentials client in matrx-frontend (`lib/api/broker/`). Use when browser code needs a provider realtime session, a direct provider call, an ephemeral token, or a provider API key in the browser or `NEXT_PUBLIC_*`. NOT for adding a new audience server-side (use aidream's token-broker)."
---

# token-broker-client — consume brokered credentials

The primitive lives at **`lib/api/broker/`** (contract: its `FEATURE.md`; cross-repo system of record: `../common-docs/systems/architecture/token-broker/FEATURE.md`). It is complete — **consume it; never hand-roll a mint call, credential cache, or gateway fetch.**

## Decision gate — does the server support the audience?

Check `KNOWN_AUDIENCES` in `lib/api/broker/types.ts` and the live minter registry (aidream `services/token_broker/minters/`).

- **Supported** → consume through the primitive (below). Zero broker-infrastructure code.
- **NOT supported** (new provider/capability) → **STOP client-side.** The system grows **server-first**: follow the global `token-broker` skill (`~/.claude/skills/token-broker/SKILL.md`) — one minter + one registry line in aidream — then consume here through the unchanged primitive. Never work around a missing audience with client-side key handling.

## How to consume

```ts
import { brokeredFetch, resolveBrokeredTransport } from "@/lib/api/broker/transport";
import { useBrokeredCredential } from "@/lib/api/broker/hooks";

// Proxied audience (e.g. "anthropic") — provider-wire HTTP, streaming included:
const res = await brokeredFetch(
  { audience: "anthropic", tierPolicy: "none", model: "claude-sonnet-5" },
  "/v1/messages",
  { method: "POST", body: JSON.stringify(anthropicShapedBody) },
);

// Native audience (e.g. "openai_realtime") — connect directly per protocol:
const t = await resolveBrokeredTransport({ audience: "openai_realtime", tierPolicy: "none" });
if (t.mode === "native_ephemeral") connectRealtime(t.endpoint, t.token);

// Component that needs a continuously-fresh credential:
const { credential, status, error, refresh } = useBrokeredCredential(req);
```

Caching, in-flight dedup, refresh-ahead (<20% TTL), 401→one-re-mint, and sign-out clearing all happen inside the primitive — callers never manage credential lifetime.

## Non-negotiables

- **`tierPolicy` is explicit at every callsite** (`"none" | "guest" | "mid"`). Never add a default, wrapper-with-default, or omittable param.
- **Never persist or log a token.** Memory only. Never render `credential.token` — mask it (debug UIs use `useBrokerCacheSnapshot`, masked).
- **Never hardcode a gateway/provider URL** — `credential.endpoint` is the only source.
- **No provider key in client env** (`NEXT_PUBLIC_*` or otherwise). Finding one is a defect: replace it with a broker audience (server-first).
- **503 on mint = loud error** ("broker unconfigured"), never a silent fallback auth path, never a retry loop.

## Verify

Demo page `/demos/token-broker` (dev builds): mint per audience, cache inspector, live proxied Anthropic call, forced re-mint.
