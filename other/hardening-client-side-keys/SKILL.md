---
name: hardening-client-side-keys
description: >
  Removes provider API keys from browser / client-side tools by putting a fail-closed edge
  proxy (Cloudflare Worker) in front of the LLM or API call, then rewiring the tool to call
  the proxy instead of the provider. Activates on: API key in the browser, client-side key,
  key in the frontend bundle, secret in client code, de-key a tool, harden the client-side-key
  tools, browser calls the Anthropic / OpenAI / Google API directly, anthropic-dangerous-direct-browser-access,
  BYOK hardening, move keys server-side, server-side proxy for an LLM call, Cloudflare Worker proxy,
  Turnstile gate on an API, harden a single-file HTML tool, stop shipping secrets to the client,
  keys pasted in a browser modal. NOT for rotating a leaked credential (use managing-credential-lifecycle)
  or building a full app from scratch (use kyle-vibe-coding).
version: "1.0.0"
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# Hardening Client-Side Keys

Move provider API keys out of the browser and behind a **fail-closed edge proxy**, then rewire the tool to call the proxy. Production-seed: the proxy in `templates/worker/` is TypeScript-strict, fail-closed, and ships with 12 passing unit tests.

## When to Use / When NOT

**Use when** — a browser/HTML tool embeds a provider key, calls a provider API directly from the client (`fetch("https://api.anthropic.com/...")`), sets `anthropic-dangerous-direct-browser-access`, or is BYOK and you want the key off the client. "Harden the client-side-key tools", "the browser is holding my OpenAI key", "de-key this HTML app".

**Do NOT use when** — rotating a *leaked* credential (that's `managing-credential-lifecycle`); building a new app from scratch (`kyle-vibe-coding`); or the "key" is a *publishable/anon* key **designed** to be public (Supabase `anon`, Stripe *publishable*, PostHog project key) — those belong client-side and moving them proxies nothing. A `service_role`, secret, or provider API key never belongs in the client.

## TL;DR

The only correct fix is a **fail-closed server-side proxy**. Two traps to refuse: (1) an *open* proxy holding your keys is an uncapped wallet — worse than BYOK; (2) a *static bearer token* shipped to a public page is extractable — security theater. Pick the auth mode by public-vs-private. Keep a **paid core** (image/3D/video generation) BYOK if proxying would put its per-call cost on the operator's bill — flag that, don't silently absorb it.

## Decision tree — auth mode

```
Who calls the proxy?
  ├─ A PUBLIC browser tool (anyone can load the page)
  │     → Turnstile mode: the browser proves human+origin, no reusable secret shipped
  │       + origin allowlist + model allowlist + max_tokens cap + body cap + per-IP rate + daily spend cap
  ├─ A PRIVATE tool (you / a known set of people)
  │     → Cloudflare Access in front of the Worker (real identity gate, session cookie not a static secret)
  └─ A SERVER-TO-SERVER caller only (no browser)
        → Bearer token (FF_PROXY_TOKEN). NEVER embed this in client HTML.
```

## Architecture — always present these three

| Option | Verdict |
|---|---|
| **A. Open proxy holding your keys** | ❌ Uncapped wallet; anyone spends your key. Worse than BYOK. |
| **B. Static bearer token in the browser** | ❌ Extractable from any public page. Theater. |
| **C. Fail-closed edge proxy** | ✅ Auth (Turnstile / Access / bearer) + origin lock + model allowlist + `max_tokens` cap + body-size cap + per-IP rate limit + global daily spend cap + upstream timeout + no secret logging. |

Model the boundaries before writing code: **browser → proxy → provider**. The browser holds *no* provider key; the proxy holds keys as Worker secrets and is the only thing that talks to providers.

## Golden path

1. **Inventory the leak.** `grep -nE "api\.(anthropic|openai)\.com|generativelanguage|<keyVarNames>|dangerous-direct-browser-access" tool.html`. Note every call site and every retired model string.
2. **Decide auth mode** (tree above). State the **who-pays** flag out loud. Keep the paid core BYOK if proxying moves its cost onto the operator.
3. **Drop in the Worker** from `templates/worker/` — it is fail-closed by construction. Set `ALLOWED_MODELS` in `src/lib.ts` to *current* IDs; delete retired ones (this doubles as the model-deprecation fix).
4. **Rewire the tool** — repoint each `fetch` to `${PROXY_BASE}/v1/<provider>`, delete provider keys + auth headers, add the Turnstile token in the body (`_turnstile`), and make provider availability depend on `PROXY_BASE`, not on browser keys. Remove the now-dead key inputs. Full before/after recipe in `references/rewiring-browser-tools.md`.
5. **Verify the tool** — the inventory grep must now return **zero** provider hosts, **zero** client key references, **zero** retired models. Syntax-check inline JS (extract `<script>` blocks, `node --check`).
6. **Gate the Worker** — `npm test` and `npx tsc --noEmit` both green before hand-off.
7. **6-persona audit** (Security, Architect, QA, Performance, DevOps, A11y/UX). 0 P0 findings to ship. This is a hard gate.
8. **Configure + deploy (operator step, held for explicit proceed):** set `PROXY_BASE` + Turnstile sitekey in the tool, `ALLOWED_ORIGINS` + KV id in `wrangler.toml`, `wrangler secret put` the provider keys + `TURNSTILE_SECRET`, then `wrangler deploy`. You (the operator) run deploy — the skill never holds cloud creds.

## The Worker (canonical template)

`templates/worker/` is the drop-in. Controls, all on by default:

- **Fail closed** — no auth mode configured → every request `503`. Never runs open.
- **Auth** — Turnstile (browser) *or* bearer (server-to-server); pick one via secrets.
- **Origin lock** — POST from a non-allowlisted origin → `403`.
- **Model allowlist** (`src/lib.ts`) — unknown/retired model → `400`. Single source of truth for the model-deprecation fix.
- **Caps** — `max_tokens` cap, body-size cap, per-IP rate limit, global daily spend cap (KV) → `429`/`413`.
- **Timeout** — 30s upstream abort → `502`. **No secret or user-content logging.**
- Keys are Worker **secrets** (`wrangler secret put`), never in code, `wrangler.toml`, or git.

Pure logic is factored into `src/lib.ts` and covered by `test/lib.test.ts` (runs under plain Vitest, no Workers runtime needed).

## Security hard rules (zero tolerance)

- **Never** ship a static gate token in a public bundle. Public → Turnstile/Access, not a bearer.
- **Fail closed**: unconfigured auth → 503, never open.
- Origin lock + model allowlist are **always on**.
- **Never** log the key or user content.
- Provider keys live as Worker secrets only. `.dev.vars` is gitignored; `.dev.vars.example` carries placeholders.

## FAIL conditions (each is a hard stop)

- Shipping a **static bearer token** to a public browser tool → extractable, no real gate.
- Deploying the proxy with **no auth mode** → open wallet, anyone spends your keys.
- **Proxying the paid core** (image/3D/video gen) onto the operator's bill without flagging who-pays.
- Marking the tool done while the **inventory grep still finds** a provider host or client key.
- An internet-facing proxy with **no spend cap / no rate limit**.
- Putting a provider key in `wrangler.toml`, source, or a committed `.env`.

## Evals

**SHOULD trigger**
1. "This HTML tool has my Anthropic key pasted into a modal in the browser — harden it."
2. "Our prompt-lab page calls the OpenAI API directly from the client. Move the key server-side."
3. "De-key these single-file tools behind a Cloudflare Worker proxy with a Turnstile gate."

**SHOULD NOT trigger**
1. "Rotate the Stripe secret key, it may be compromised." → `managing-credential-lifecycle` (credential lifecycle, not a proxy build).
2. "Is it fine to put my Supabase anon key in the frontend?" → publishable/anon key is *meant* to be public; no proxy needed (answer directly).

## Self-verification

1. Auth mode chosen by public-vs-private and stated; who-pays flagged.
2. Worker is fail-closed (503 with no auth mode); origin + model allowlist + caps present.
3. No static gate token in any client bundle.
4. Tool inventory grep returns zero provider hosts / client keys / retired models.
5. `npm test` + `tsc --noEmit` green; inline JS syntax-checks.
6. 6-persona audit run; 0 P0 open.
7. Deploy + Project/file overwrites held for the operator's explicit proceed.

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS
- *Claim:* A fail-closed proxy with Turnstile + caps is the correct fix for a public client-side-key tool. **[GENERATED — reasoned from the abuse-vector analysis; the template's logic is [SOURCED] by its own passing tests.]**
- *Claim:* A static bearer token on a public page provides no real gate. **[SOURCED — any value shipped to the browser is readable in devtools/network.]**
- *Counterexample:* If the tool is genuinely private (Cloudflare Access in front), the identity gate replaces Turnstile and the internal calls can carry a session — the tree's "public" branch does not apply.
- **! Contradiction:** "move the key server-side" and "keep the paid core BYOK" both apply to the same 3D-style tool — resolve by proxying the *LLM* calls and leaving the *generation* key BYOK, and say so explicitly.

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS
- The template's KV rate-limit counters are read-then-write, not strictly atomic — a burst can slightly overshoot a cap (documented in the Worker README; use a Durable Object for exact accounting).
- No streaming in the template — buffered responses; add SSE passthrough if a tool needs token streaming.
- The model allowlist is manual — it must be updated when providers ship/retire models; a stale allowlist silently 400s a valid new model.
- Turnstile UX (managed vs invisible) is sitekey-config dependent and not tuned by the skill.
