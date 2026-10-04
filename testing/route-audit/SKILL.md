---
name: route-audit
description: >-
  Walk, verify, repair, and sign off Movemental Studio / ZenWrite UI routes using Chrome DevTools MCP
  (diagnose) and Playwright specs (certify). Use for any portion of the app: a single view
  (?view=create, Money, Home), a phase (1-public, 3-studio-content), public reader URLs
  (/articles/:slug, /pricing), or a full pre-launch sweep. Triggers include: route audit, walk the
  app, check every page, are the routes working, audit Create/Organize/Reach/Money, sign off routes,
  resume route audit, verify routes.manifest, run audit:routes, or "is /?view=X broken?". Reads
  routes.manifest.yaml + docs/audit/routes/STATE.md; never marks signed_off on the same turn as a fix.
---

# Route Audit (ZenWrite)

Prove that every route (or the portion the user named) renders what the manifest requires, signed in
when needed, and leave a Playwright ratchet behind.

**First actions every invocation**

1. Read `references/zenwrite-portions.md` (this repo’s phase map + commands).
2. Read `docs/audit/routes/STATE.md` and `docs/audit/routes/state.json` if they exist — resume, do not restart.
3. Run preflight from `references/setup-and-install.md` (port 9222 / app up / git SHA / Playwright).
4. Resolve the user’s **portion** → phase id(s) or single fixture URL. If unclear, ask once.

Then follow the loop below for that portion only (unless they asked for a full sweep).

## The one idea

| Job | Tool |
|---|---|
| **Certify** — does this route pass? | `pnpm exec playwright test e2e/routes/<phase>.spec.ts` |
| **Diagnose** — *why* does it fail? | Chrome DevTools MCP on an already signed-in browser |

A route is `signed_off` only when a **committed** spec passes on the **current SHA** in a **later turn**
than the fix. Never self-certify from a snapshot.

## Resolve portion → work

| Ask | Do |
|-----|-----|
| Named phase (`1-public`, `3-studio-content`, …) | That phase only |
| Studio surface (Create, Money, Home, …) | Map via `zenwrite-portions.md` → one phase |
| Single URL / `?view=` | Single-route fast path |
| “Did the refactor break routes?” | `pnpm audit:routes:all` — DevTools only on reds |
| “Everything” / pre-launch | Phases in order; fresh context per 12–15 routes |
| Public reader / pricing | `1-public` and/or `7-public-content` (fixtures required) |

## The loop (scoped to the portion)

```
manifest ──► walk with DevTools (evidence only — fix nothing yet)
                 ▼
            triage: cluster root causes
                 ▼
            repair source ──► update manifest must_render ──► gen-route-specs
                 ▼
            playwright test e2e/routes/<phase>.spec.ts
                 ▼
            later turn: green + committed SHA → STATE signed_off
```

### Repo scripts (ZenWrite)

Prefer **repo root** scripts (AppView + reader aware):

```bash
pnpm exec node scripts/build-route-manifest.mjs
pnpm exec node scripts/gen-route-specs.mjs --phase <id>
pnpm audit:routes
pnpm audit:routes:all
```

Skill copies under `.cursor/skills/route-audit/scripts/` are for install/generic; ZenWrite enumeration
lives in `scripts/build-route-manifest.mjs`.

### Walk (DevTools)

Per fixture: `navigate_page` → `take_snapshot` → `list_console_messages` → `list_network_requests`
(non-2xx) → assert each `must_render` → `take_screenshot` →
`docs/audit/routes/evidence/<phase>/<slug>.png`.

Record failures **verbatim** in `state.json`. Do not fix mid-walk.

### Sign-off gates

All five required (see `references/state-and-signoff.md`): spec exists, committed, playwright green,
`verified_commit` = current SHA, verification turn **after** fix turn.

## Non-negotiables

- Signed-in by **attachment** (`--browserUrl` / profile), not scripted login.
- Pin real fixtures for `:slug` routes — never invent.
- Evidence before verdict (actual console text, status, URL).
- Scope: note adjacent issues under `observed_not_fixed`; do not redesign mid-phase.
- Run signed-out (`auth` phase) when auditing public vs private behavior.

## Fast paths

- **Single route** — preflight, walk one fixture, report; any fix still updates the phase spec.
- **Regression** — Playwright first; DevTools only for failures.
- **New route** — regenerate manifest, author `must_render`, gen spec, walk, later sign-off.

## References

- `references/zenwrite-portions.md` — **read first in this repo**
- `references/setup-and-install.md` — install, Chrome attach, preflight
- `references/manifest-spec.md` — contract schema
- `references/state-and-signoff.md` — six states + gates
- `references/phase-prompts.md` — copy-paste prompts (bootstrap / walk / triage / repair / sign-off / rerun)
- `docs/audit/routes/README.md` — operator how-to in-repo
