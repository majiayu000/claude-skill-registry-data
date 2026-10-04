---
name: token-broker-client
description: "Brokered short-lived provider credentials client in matrx-extend (`src/lib/broker/`). Use when a feature needs a provider realtime session, a direct provider call via the aidream gateway, or a provider API key in the extension. NOT for adding a new audience server-side (use aidream's token-broker)."
---

# token-broker-client — consuming brokered credentials in matrx-extend

The primitive lives at [src/lib/broker/](../../../src/lib/broker/) (read its
FEATURE.md). Cross-repo contract:
`/Users/armanisadeghi/code/common-docs/systems/architecture/token-broker/FEATURE.md`.

## Rule 0 — does the server support the audience?

Server-supported audiences live in aidream's
`aidream/services/token_broker/minters/__init__.py` (v1: `openai_realtime`
native, `anthropic` proxied). **If the audience you need isn't there, STOP
client-side** and follow the global `token-broker` skill
(`~/.claude/skills/token-broker/SKILL.md`): the server grows first (one
minter + one registry line), then you consume it here with zero primitive
changes.

## Consuming (never hand-roll)

```ts
import { getBrokeredCredential, callProxiedJson, brokeredFetch, nativeConnectionInfo } from '@/lib/broker';
```

- **`getBrokeredCredential(audience, tierPolicy, opts?)`** — works in ANY
  context (SW direct; sidepanel/offscreen auto-route to the SW's shared
  cache). Caching, refresh-ahead, and single-flight are inside — never add
  your own cache or mint call.
- **`tierPolicy` is a REQUIRED explicit argument** (`'none' | 'guest' | 'mid'`).
  Never write a wrapper that defaults it — the explicit-access contract holds
  at every layer.
- **Proxied one-shot JSON** → `callProxiedJson(...)` (executes in the SW;
  token never leaves it). **Proxied streaming (SSE)** → mint + `brokeredFetch`
  in the context that owns the stream. You speak the PROVIDER's wire protocol
  (e.g. Anthropic Messages), swapping only base URL + Bearer.
- **Native realtime** → `nativeConnectionInfo(cred)` and open your own
  WebRTC/WS session against `endpoint`.
- React components → `useBroker()` from `@/hooks/use-broker`.

## Invariants

- Tokens: memory only. Never persist (no chrome.storage/localStorage/DB),
  never log. UI displays only the token-free snapshot.
- `credential.endpoint` is data — never hardcode gateway/provider URLs.
- 503 from mint = broker unconfigured server-side → surface loudly; never
  silently fall back to another auth path or a client-held key.
- Endpoint rejects the grant (401) → `invalidateBrokeredCredential` + one
  re-mint (or just use `callProxiedJson`, which does this), then fail loudly.
- No raw provider API key may ever ship in this extension's env/config.

## Testing

Admin sidepanel → **Broker** tab (KeyRound icon) exercises mint, cache,
invalidate, and a proxied Anthropic round-trip. Manual steps:
`docs/feature-tests.md` → "Token broker — demo surface". Unit tests:
`tests/unit/broker-cache.test.ts`.
