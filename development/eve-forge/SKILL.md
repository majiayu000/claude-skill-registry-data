---
name: eve-forge
category: orchestration
version: 1.0.2
author: broomva
description: >-
  Forge a personalized eve agent for a business end-to-end — absorb the
  business's artifacts, author the eve agent/ dir, validate, deploy to
  Vercel (or a VPS), smoke-test against ground truth, register, and evolve.
  The deterministic core is three safety gates distilled from a driven
  benchmark (BRO-1677): deploy-safety (never ship auth:none), validate
  (eve info --json → 0 diagnostics + tools registered), and smoke
  (drive the deployed agent, assert vs a ground-truth example). USE WHEN
  building/onboarding an eve agent for a tenant, "forge an eve agent",
  "deploy an eve agent", "onboard <business> onto eve", or when the
  Claude-Code orchestrator/forge must turn absorption inputs into a running
  eve operator. NOT FOR benchmarking frameworks (that's a one-off), running
  the operator itself (the forge builds it; the operator runs cheap on eve),
  or non-eve agent frameworks.
tags:
  - eve
  - agent-forge
  - meta-agent
  - vercel
  - deployment
  - claude-agent-sdk
  - dogfood
  - agent-substrate
compounding: each forged tenant is a versioned agent/ dir + tenant-spec.json (authored-agents-as-data); re-onboard/evolve = a diff
provenance:
  - docs/reports/2026-07-04-life-vs-eve-benchmark.html
  - research/entities/concept/eve-agent-orchestrator.md
  - BRO-1677
---

# eve-forge — turn a business into a deployed eve agent

The orchestrator/forge (a Claude Agent SDK program) produces a **deployed,
tenant-scoped eve agent** from a business's absorption inputs. This skill
encodes the real eve workflow + every trap learned dogfooding it, and gates
the consequential steps so the forge cannot repeat the benchmark's mistakes.

**Latent vs deterministic split:**
- **Latent (agent judgment, this SKILL.md):** `absorb` (Word template + transcript
  + examples → `tenant-spec.json`) and `author` (write the eve `agent/` files in
  the business's voice from the templates).
- **Deterministic (`scripts/`, tested):** `preflight` (Node ≥ 24), `deploy-safety`
  (never ship unlocked auth), `validate` (eve info clean), `smoke` (output vs
  ground truth). Precision work lives in code; the latent space invokes it.

## The 8-stage pipeline

| # | Stage | How | Gate |
|---|---|---|---|
| 1 | **Absorb** | read the template + 1–2 transcripts + 2–3 filled examples → write `tenant-spec.json` (see `references/templates/tenant-spec.example.json`) + a ground-truth `truth.json` (required substrings + case-scoped `forbidden`). **Stage these OUTSIDE the tenant dir** — `eve init` refuses a non-empty target ("has no package.json") | latent |
| 2 | **Scaffold** | `python3 scripts/eve_forge.py preflight` **then** `nvm use 24 && npx eve@latest init <slug>`, then move `tenant-spec.json`/`truth.json` in | **preflight blocks if Node < 24** (the npx trap) |
| 3 | **Author** | fill from `tenant-spec.json`: copy `references/templates/{fill_document,send_document}.ts` → `agent/tools/`; write `agent/instructions.md` (business voice + **"strip HTML comments from the output"**); **EDIT the scaffolded `agent/channels/eve.ts`** — remove `placeholderAuth()` → `auth: [vercelOidc(), localDev()]` (never `none()`). Do NOT hand-write `defineChannel`; the scaffold already ships `eveChannel` | latent |
| 4 | **Validate** | `npx eve info --json \| python3 scripts/validate.py --expect-tools fill_document,send_document` (validate.py strips eve's banner + reads the real dict-`diagnostics`/`status` schema) + `npm run typecheck` | **0 diagnostic errors + tools registered, or iterate** |
| 5 | **Deploy** | `python3 scripts/eve_forge.py gate agent/` (point at the **`agent/` dir**, not the project root) **before** `vercel deploy --scope <team>`; use the **production alias** (the raw URL 302s to SSO) | **deploy-safety denies if auth not locked** |
| 6 | **Smoke** | drive the deployed agent (see **§Smoke against a locked channel**) → `python3 scripts/smoke.py --output <filled.txt> --truth truth.json` | **assert vs ground truth (evidence-gated)** |
| 7 | **Register** | commit `freelance/<slug>/` (agent dir + `tenant-spec.json` + `truth.json` + `smoke-receipt.json`: `{url, verdict, coverage, at}`); report URL + evidence | tenant = versioned data |
| 8 | **Evolve** | owner draft→approve corrections → forge proposes a diff to `instructions.md`/skills | **propose → test vs fixtures → owner-approve → commit** |

## The deploy-safety gate (the incident-derived check)

A benchmark run shipped a **public, `auth: none()`, Gateway-billed** eve endpoint —
anyone could spend credits. This skill makes that structurally unreachable. In the
Claude-Code orchestrator, wire it as a **PreToolUse hook** that runs
`scripts/deploy_safety.py <agent_dir>` before any `vercel deploy` and **denies the
tool call on a non-zero exit**. Rule (prod): the channel `auth:` array must contain a
real authenticator (`vercelOidc`) and must NOT contain `none()`/`placeholderAuth()`;
a lone `localDev()` is dev-only. Fail-closed if no `auth:` array is found.

## Smoke against a locked channel

A correctly-locked channel returns **401** to anonymous callers — so the smoke driver must
authenticate (the only reason a naive smoke "worked" in the benchmark was the `auth: none()`
incident). On the Vercel deploy:

```bash
vercel env pull /tmp/<slug>.env --environment=production --scope <team>   # mints VERCEL_OIDC_TOKEN
TOKEN=$(grep VERCEL_OIDC_TOKEN /tmp/<slug>.env | cut -d= -f2- | tr -d '"')
# POST a turn — payload field is `message` (NOT `input`); returns 202 + sessionId:
curl -s -XPOST "https://<slug>.vercel.app/eve/v1/session" -H "Authorization: Bearer $TOKEN" \
     -H 'content-type: application/json' -d '{"message":"<transcript>"}'
# GET the stream (it long-polls at session.waiting → cap it), extract the fill_document output:
curl -s --max-time 60 "https://<slug>.vercel.app/eve/v1/session/<sessionId>/stream?startIndex=0" \
     -H "Authorization: Bearer $TOKEN" > /tmp/<slug>.stream
```
Delete `/tmp/<slug>.env` after (it holds a live token).

## Deterministic scripts

- `scripts/eve_forge.py preflight` — Node ≥ 24 or fail (the `npx eve init` trap).
- `scripts/eve_forge.py gate <agent_dir> [--info info.json --expect-tools a,b]` — runs deploy-safety (+ validate) as one pre-deploy gate.
- `scripts/deploy_safety.py <agent_dir> [--env prod|dev]` / `--stdin` — the auth-lock check.
- `scripts/validate.py --expect-tools a,b` (reads `eve info --json` on stdin) — diagnostics + tools.
- `scripts/smoke.py --output <file> --truth <json>` — deployed-output vs ground-truth (strips HTML comments; `truth.json` `forbidden` encodes case-scoped negatives, e.g. no `"bloodwork"` for a non-senior patient).

## Gotchas (see `references/gotchas.md`)

Node-24 hard requirement (npx silently uses the wrong Node) · non-TTY `eve dev` errors
(scaffold succeeds, the auto-dev-launch fails) · fail-closed default auth + Vercel
Deployment-Protection SSO (use the production alias, keep auth locked) · eve not
auto-detected as a Vercel framework ("No framework detected" → its native Agent-Runs
observability may not activate) · AI-Gateway auth works via project OIDC at runtime
(zero keys). Pin the eve + claude CLI versions (eve is beta).

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "Deploy it, I'll lock auth later." | The deploy-safety gate is binary and PreToolUse-wired. `auth: none()` never reaches prod. |
| "eve info was clean when I wrote it." | Re-run `validate` after every author edit; typecheck drift is silent. |
| "It looks right, ship it." | Smoke-test against the business's own ground-truth example, or it's prose, not evidence. |
| "npx eve init failed weirdly." | Run `preflight` — it's the Node-24 trap 9 times out of 10. |

## References

- `references/gotchas.md` — the full benchmark gotcha list.
- `references/templates/` — the 4 eve agent file templates the author stage fills.
- `research/entities/concept/eve-agent-orchestrator.md` — the orchestrator design + provenance.
- `docs/reports/2026-07-04-life-vs-eve-benchmark.html` — the driven benchmark this distills.
