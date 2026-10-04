---
name: go-live
disable-model-invocation: true
description: Guided, stateful provisioning of a product's production stack — deep-links, key-format validation, a secrets backend (fnox recommended, or user-touched .env.local), a resumable ledger, CLI automation after signup, and a blocking A1–A10 live gate. Hands off to /security-check → /ship. The walked version of SETUP.md.
---

# /go-live

Usage: `/go-live <slug>`

The guided provisioning flow that takes a **local-first** product (built with `/builder-mode`, running with zero accounts) to a **production-ready** one — then hands off to deploy. It operationalizes `templates/product-starter-nextjs/SETUP.md` (the service list) and `factory/playbooks/ai-native-2026/go-live-provisioning.md` (the env-var → service map), but *walked, validated, and resumable* instead of a static checklist.

Where it sits in the chain:
`/builder-mode` (build local) → **`/go-live` (wire the stack)** → `/security-check` (gate) → `/ship` (deploy) → `/web-launch` (verify the launch).

## Preconditions

1. Resolve the product: `$ARGUMENTS` is the slug. If empty, ask (or `Read products/_portfolio.md`).
2. Resolve the **code path** from `products/<slug>/product.config.json` → `code_path` (maps via `code-paths.local.json`). All provisioning happens **in that product's code repo** — that's where secrets get wired.
3. **Pick the secrets backend** (see next section). Default recommendation: **fnox** — no plaintext secrets file on disk. Fallback: user-touched `.env.local`. Either way, **Claude never creates, reads, or writes a plaintext secrets file itself** (hook-enforced), and never writes secrets to anything tracked.

## Secrets backend — fnox (recommended) vs `.env.local` (fallback)

**Recommend fnox first** (jdx/en.dev — `brew install fnox`). It removes the *root cause* of the 2026-07-03 leak: with fnox there is **no plaintext `.env.local` to be harness-watched**. `fnox.toml` holds only age/KMS ciphertext or remote-provider references (1Password, AWS/GCP/Azure secret managers, Vault, Doppler, …) and is safe to commit. The app runs via `fnox exec -- <cmd>`, which injects secrets into the child process env only at run time.

**Agents access secrets only through fnox's MCP server, exec-only.** The product repo's `.mcp.json` runs `fnox mcp` with `[mcp] tools = ["exec"]`; its `exec` tool redacts resolved values from stdout/stderr, so `printenv`/`echo $SECRET` return `[REDACTED]` in the transcript.

**Honest threat model (red-teamed 2026-07-04 — see `brain/decision-log/2026-07-04-fnox-secrets-backend.md`).** fnox's MCP redaction is literal string-matching. It closes the **accidental-leak class** (the watcher-echo / `printenv` incident) — which is the one that actually bit us — but **not adversarial exfiltration** (base64/reverse/write-to-file all recover the value). Layer these, weakest to strongest:

- **The real boundary — key out of agent reach.** This is the only layer robust against a *determined/injected* agent. Prefer a **remote provider (1Password/KMS)** whose auth the agent can't complete, so no local key exists. A local age key must live **outside the repo and unreadable to the agent** (reading it fully decrypts `fnox.toml`).
- **Shell deny-rules (best-effort).** The committed `.claude/settings.json` denies **all** `fnox` at the agent's shell (`Bash(fnox)`, `Bash(fnox:*)`) — the agent has no legitimate shell use of fnox; it goes through MCP. Note this is *best-effort*, not a security boundary: Claude Code deny-rules are bypassable (option injection, env-var prefixes, `eval`, absolute paths — per the permissions docs). It stops the naive path, not a determined one.
- **`tools = ["exec"]` + explicit `secrets` allowlist** in `fnox.toml` — never the permissive default; blocks `get_secret`/`get` through MCP.
- **`guard-secrets-files.sh` stays** as defense-in-depth.
- **JSON config caveat:** `.claude/settings.json` and `.mcp.json` use strict validation — **no `_comment` keys** (an unknown key rejects the whole file, silently dropping the deny-rules). Document rationale outside the JSON.

Setting a secret (the **user** runs this themselves, value never in chat): `fnox set STRIPE_SECRET_KEY --provider age` (prompts for the value). Verify non-printing: `fnox list` (names only) or `fnox check`.

**Fallback — `.env.local`:** if the user declines fnox, use the user-touched flow below. Confirm there's an `.env.local` (`test -s .env.local`); if missing, the **user** creates it (`cp .env.local.example .env.local`) and pastes keys themselves. `.env.local` is gitignored.

## The state ledger (resume)

Maintain `.hamzaish-go-live.json` in the product's code repo (gitignored — add to `.gitignore` if absent). Shape:

```json
{ "updated": "<date>", "services": { "supabase": "done", "stripe": "skipped", "resend": "pending", "...": "..." } }
```

On every run: read it, **skip services already `done`/`skipped`**, resume at the first `pending`. State values: `pending` · `done` · `skipped` · `later`. This is what makes `/go-live` resumable across sessions — never re-ask a settled service.

## The guided loop

Group services into **required-to-deploy** first, **optional** second. For each not-yet-settled service, do exactly this:

1. **Explain in one line** what it's for and the cheapest skip ("no payments yet? skip Stripe").
2. **Open the deep-link** (print it; the user signs up — you can't create accounts for them).
3. **Name exactly what to copy from where** — the key's VALUE never enters chat and Claude never touches a secrets file. **Store it — steps 3–4 depend on the chosen backend:**
   - **fnox (recommended):** tell the user to run `fnox set STRIPE_SECRET_KEY --provider age` (or their provider) — value omitted, so fnox **prompts with hidden input** (never in chat, never in shell history). First run: `cp fnox.toml.example fnox.toml` and set the provider.
   - **`.env.local` (fallback):** give the exact line to add, e.g. "in your editor, add `STRIPE_SECRET_KEY=<the sk_test_… key you just copied>` to `.env.local`". First run: the user creates it with `cp .env.local.example .env.local`.
4. **User stores the key themselves** (fnox prompt, or paste into `.env.local`) and says "done".
5. **Validate presence + format with NON-PRINTING checks only** — boolean/count/names output, never the value:
   - **fnox:** `fnox list` (names + ciphertext only, no plaintext) and `fnox check` (health verdict). Never `fnox get`/`export`/`exec` — those return raw values and are deny-listed for the agent anyway.
   - **`.env.local`:** `grep -qE '^STRIPE_SECRET_KEY=sk_(live|test)_' .env.local && echo OK` (table below). Never Read/Write/Edit or `cat` it (the `guard-secrets-files.sh` hook blocks it anyway — incident 2026-07-03: a Claude-created `.env.local` got harness-watched and the user's pasted keys were echoed into the transcript; both keys rotated).
6. **Mark the service `done`** in the ledger. Offer `skip`/`later` at every step (records the choice, moves on).

### Service catalog (deep-links · keys · validation)

| Service | For | Signup | Env vars | Key format check |
|---|---|---|---|---|
| **Supabase** *(req. to leave local mode)* | DB + auth | supabase.com/dashboard → New project | `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` | URL `https://<ref>.supabase.co`; keys are JWTs (`eyJ…`) |
| **Vercel + Domain** *(req. to deploy)* | hosting + DNS | vercel.com → import repo; cloudflare.com for the domain | (Vercel project; `NEXT_PUBLIC_APP_URL`) | APP_URL is a valid https URL |
| **Stripe** | payments | dashboard.stripe.com (test mode first) | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `sk_(live\|test)_…`, `whsec_…`, `pk_(live\|test)_…` |
| **Resend** | email | resend.com → verify domain | `RESEND_API_KEY`, `RESEND_FROM_EMAIL` | `re_…`; FROM is an email |
| **PostHog** | analytics | posthog.com → new project | `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST` | `phc_…` |
| **Sentry** | errors | sentry.io → new Next.js project | `NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_ORG`, `SENTRY_PROJECT`, `SENTRY_AUTH_TOKEN` | DSN `https://…@…ingest.sentry.io/…` |
| **GA4 / Plausible** | web analytics | analytics.google.com / plausible.io | `NEXT_PUBLIC_GA4_MEASUREMENT_ID`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` | GA4 `G-…` |
| **GSC / Ahrefs** | SEO | search.google.com/search-console / ahrefs.com/webmaster-tools | `NEXT_PUBLIC_GSC_VERIFICATION` (Ahrefs = DNS verify, no key) | meta content string |
| **DataForSEO** *(optional)* | keyword data | dataforseo.com | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | non-empty |

## Automate after signup (the part that *is* fast)

Account creation is manual; everything after the key exists, automate — **with explicit confirmation before each mutation**:

- **Vercel**: `vercel link`, then push the local env up: `vercel env add <NAME> production` (or `vercel env pull`/`add` in a loop). `vercel domains add <domain>`.
- **GitHub**: `gh secret set <NAME>` for CI secrets.
- **Cloudflare**: DNS records via API if a token is provided.

State plainly what you can't do: you can't sign the user up, accept their ToS, or enter their card.

## Verify, then hand off

When the **required-to-deploy** set is `done`:
1. **Verify**: every required var is present and well-formed (re-run the format checks). On fnox: `fnox check` + `fnox list` (names only). On `.env.local`: non-printing `grep -qE` checks. Confirm `LOCAL_MODE` will now be off (Supabase set).
2. **Verify the server is actually up before sharing any localhost link** (global rule: never hand over a dead localhost link). If the product uses **pitchfork**, `pitchfork start web` (idempotent) then `pitchfork status web` — or curl the port for a 2xx — before emitting the URL. pitchfork keeps the server supervised across sessions, so the link stays live. Multiple products: distinct ports (a readiness check confirms "something answers," not "*this* server" — a collision can false-positive).
3. **Offer the handoff**: "Stack wired. Run `/security-check <slug>` (gate), then `/ship <slug>` (deploy)?" — `/go-live` provisions; `/ship` deploys. Don't deploy from here.

## The live gate — A1–A10 (blocking; go-live is not done at handoff)

Provisioned-and-shipped is still only *declared* live. `/go-live` closes when the
product is **provably** live: after `/ship` reports deployed, run the assertion
harness from `factory/playbooks/ai-native-2026/go-live-provisioning.md` against
the real production URL:

```bash
bun ${HAMZAISH_ROOT:-$HOME/Claude/Hamzaish}/scripts/verify-live.ts https://<domain> \
  --sha <deployed short-sha> [--authed-route </api/…>] [--resend-domain <domain>]
```

It checks A1–A10 (DNS apex+www, TLS on both, `/api/health` ok + buildSha + db
probe, auth gate 401s, `pk_live_` not dev-mode, cron gated, no server-secret in
the client payload) and emits a scorecard — `EVAL: n/N`, per-assertion
PASS/FAIL/PENDING/MANUAL with remediation.

**A11 — Trackable (MANUAL until `verify-live.ts` learns it; blocking like the
rest).** *A product that isn't trackable isn't shareable* — if nobody can answer
"which screens do users visit and what do they do there?", user data is being
lost from the first shared link, and it's the founder who ends up noticing
(it happened on every product until this gate existed). Check on the LIVE site:
1. Every screen/tab/mode reports its own path — SPAs need virtual `page_view`s
   or analytics shows one "/" row forever.
2. The spec's Trackability events fire on the core flows (dataLayer or GA4
   Realtime while you click through).
3. **Every app** in the product carries the tag (grep the measurement id in each
   deployed `index.html` — main site AND any subpath tool).
4. Third-party params are registered (GA4 custom dimensions) or the founder has
   the clickable steps to do it.
5. The first-party events table receives the same events (the dual-sink helper —
   `/user-analytics` Recipe F + Definition of Done #7).

Rules:

- **Any FAIL → not live.** Fix, re-run; exit 1 blocks. Never close the ledger or
  tell the user "you're live" over a failing scorecard.
- **PENDING/MANUAL are named, never dropped** (e.g. "A8 PENDING: Resend DNS
  propagating, recheck in 1h" — the A7b throwaway-signup stays a human step).
- **Record the verdict in the ledger** (`"live_gate": "EVAL: 9/9 …"` + date), and
  append every FAIL to `brain/learnings/` with assertion id + cause + fix —
  recurring misses get promoted into the playbook as pre-checks.
- Products scaffolded before the health convention report A3/A4/A6 as PENDING —
  the starter now ships `/api/health` (`ok`, `buildSha`, `probes.db`); backfill
  the route when touching an older product.

## Honest rules

- Never commit a real key. Only `.env.local` (gitignored) or the platform's secret store. The `.env.example` stays placeholders-only.
- **Secrets files are user-touched only.** Claude edits only `.example` templates; the user copies + pastes their own keys; verification is non-printing (`grep -q/-c`, `test`). Key values never enter chat in either direction. Enforced machine-wide by `~/.claude/hooks/guard-secrets-files.sh`; see `brain/anti-patterns/claude-touched-secrets-file.md` (incident 2026-07-03).
- Record skips honestly in the ledger; a skipped service is a deliberate choice, not a gap.
- This flow lives at `factory/skills/go-live/SKILL.md` — the single source for `/go-live` (user-invoked; `disable-model-invocation` keeps its description out of session context, and CLAUDE.md's command table is the router).
