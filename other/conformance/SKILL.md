---
name: conformance
layer: stack
description: The crouton-conformance gate — the SECOND acceptance axis of graduation (the first is the experience side-by-side, /graduate stage C1). Checks a graduated app is a REAL crouton app — CLI-scaffolded, real collections, consumes the correct packages without reinventing them — by composing the existing probes (frontend-review, a11y, e2e-smoke, typecheck) plus crouton-structural checks, then renders a required, signed-off checklist on the graduation PR. Use at /graduate stage C2, or when asked "is this app crouton-native", "run the conformance gate", "check graduation conformance".
argument-hint: "<app-path> [--comment]"
allowed-tools: Bash, Read, Grep, Glob, Agent, mcp__github__add_issue_comment, mcp__github__pull_request_read
---

# Conformance Skill — the crouton-conformance gate (graduation axis C2)

A graduated app needs **two** signed-off acceptance axes (`/graduate`): **experience**
(it matches the signed-off spec — the side-by-side comparison, C1) and
**crouton-conformance** (it's a *real crouton app*, not a hand-assembled look-alike). This
skill is the second one. It exists because "it matches the POC" alone let v1 ship a
hand-assembled scaffold that **500'd at runtime on a green build** (missing
`server/db/schema.ts`, #988) and reimplemented what packages already provide.

**This is a gate, not a finding-rater.** Unlike `/frontend-review` and `/a11y` (which
*find and rate* issues), this **composes** those probes with crouton-structural checks and
renders a **required, signed-off checklist**. It doesn't replace the probes — it *runs*
them and refuses to go green until each line is checked and a human has signed off
(`lgtm`, the #310 loop). Status is **derived** from that sign-off, never self-asserted
(the done-rule, `AGENTS.md`).

## When to run

- `/graduate` **stage C2**, after the experience gate (C1) is walking green.
- Any time you need to certify an app under `apps/`/`pocs/` is crouton-native before promotion.

It needs an environment that can run `pnpm typecheck` + the e2e smoke. From a sandbox that
can't, run the **structural** checks (deterministic, static) and hand the **probe** lines to
the human to run — mark them `⏳ needs-human`, never `✅`.

## The checklist (each line is a gate, each needs a sign-off)

Resolve `<app-path>` (e.g. `apps/builder`), then work the four groups. **Structural** is
deterministic and you run it; **Probes** compose existing skills; **Docs** is a grep + a
human read.

### 1. CLI-scaffolded (correct-by-construction, not hand-built)
The #988 class — a hand-assembled scaffold silently omits standard files and 500s at runtime.
- [ ] `crouton init` scaffold present — **`<app>/server/db/schema.ts` exists** (the one whose
      absence 500'd every auth/team/i18n query in #988), plus `server/`, `app/`, `nuxt.config.ts`.
- [ ] `package.json` `postinstall` is the **guarded** form (`nuxt prepare 2>/dev/null || true`),
      never a bare `nuxt prepare` (a bare one aborts the whole monorepo install — root `CLAUDE.md`).
- [ ] `wrangler.jsonc` follows the Workers pattern (no `pages_build_output_dir`; `nodejs_compat`;
      id-less bindings + an `env.staging` block) — copy `apps/velo`, don't invent.
- [ ] **Team-scoped routes** — team-data pages live under a `[team]` param (`app/pages/**/[team]/…`,
      e.g. `/dashboard/[team]/…`), so `getTeamId()` resolves **synchronously from the route** via
      `team-context.global`. A **root** route with no `[team]` (a POC crutch) makes team context resolve
      **async from the session** — the list query silently skips and a mutation *rejects* until the
      session bootstrap sets an active org, so a control "does nothing" on an early tap (the
      crouton-builder `/builder` New-page bug). Prefer the `[team]` route; if a root route is deliberate,
      the app must gate team-dependent actions on readiness, not fire them blind.

```bash
test -f <app>/server/db/schema.ts && echo "✅ schema.ts" || echo "❌ MISSING server/db/schema.ts (the #988 500)"
grep -q 'nuxt prepare 2>/dev/null' <app>/package.json && echo "✅ guarded postinstall" || echo "❌ unguarded postinstall"
```

### 2. Real collections (not demo/stub blocks)
The collections ARE the data model the app composes — backend-free demo blocks are a POC crutch.
- [ ] A real schema source (`<app>/crouton.config.*` or `<app>/schemas/*.json`) **and** the
      generated collection layers it produces (`<app>/layers/<collection>/` with `server/api`,
      `app/components`) — not hand-written stub components standing in for them.
- [ ] A migration exists for the collections (`<app>/server/db/migrations/` populated).

### 3. Consumes the correct packages — doesn't reinvent them (DRY)
The most important conformance check and the least mechanical: the app must **use** the
graduated package(s) + the standard stack, not re-implement what they export.
- [ ] The graduated package(s) are in `<app>/package.json` deps **and imported** (grep the app
      for the package's public entrypoints).
- [ ] The app does **not** locally re-implement a package's job. For each graduated package, list
      its **public exports** (its `package.json` `exports` + `CLAUDE.md` "Key Files"), then grep the
      app for local components/utils that duplicate them. Any duplicate is a ❌ — fold it back to the
      package. (#983 WS4 lesson: the package already provided the sanitiser/bridge/storage; the app
      must consume, not re-derive.) **This line is a human read** — surface the candidates, don't auto-pass.

### 4. The probes (compose, don't duplicate) + docs
- [ ] **`pnpm --filter <app> typecheck`** green (per-app; never `npx nuxt typecheck` from root — false positives).
- [ ] **`/frontend-review --scope <app>`** clean (Nuxt UI 4 / crouton component conventions).
- [ ] **`/a11y --scope <app>`** clean (no 🔴/🟡 left).
- [ ] **`/e2e-smoke`** green for the app's fixture (boots → authenticates → CRUD).
- [ ] **Docs updated** — app `CLAUDE.md`; new package ⇒ its `CLAUDE.md` + `node scripts/gen-package-catalog.mjs` + a `pkg:*` label in `.github/labels.yml`.

## Render + gate

Render the four groups as one checklist with per-line status — `✅` pass · `❌` fail (with the
one-line reason) · `⏳ needs-human` (a probe you couldn't run here). Then:

1. **Any `❌`** → the gate is **red**. Fix and re-run; do not present it as passable.
2. **All `✅`/`⏳`** → post the checklist on the **graduation PR** (`--comment`) and **hold on
   `status:blocked`** for sign-off. The conformance axis is "done" only on a reply comment
   containing `lgtm`/`approve` that names this gate — not a green build, not your own read
   (the done-rule). A `⏳` line can't be signed off until a human runs it and flips it to `✅`.

The app is promotable when **both** axes are signed off — this gate (C2) **and** the experience
comparison (C1). Never one, never a proxy.

## Conventions

Defers to the root `CLAUDE.md` / `AGENTS.md` for the done-rule + the sign-off loop (#310/#572).
Composes `/frontend-review`, `/a11y`, `/e2e-smoke`, and `pnpm typecheck` rather than reimplementing
them. Invoked by `/graduate` at stage C2; the experience axis (C1) is the side-by-side comparison,
not this skill. Mirrors the review-family split (a focused, CI-gateable skill beside `/review`).
