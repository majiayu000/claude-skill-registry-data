---
name: mcp-ai-wpoos-astro-forge
description: Operational guide for the NV oOS Astro Forge (Proposal 096) — the WP→Astro frontend generator in examples/nvoos-astro-forge (wp-client, Astro content-layer loader, versioned sanitizer, scaffold CLI, blog template, hermetic WP wire fixture, CI exit gate). Use when forging a customer frontend, adding a template or collection, debugging the e2e gate, or continuing Phases 1–4 (wc/v3 Woo loader, site_analyze, tokens_apply, MCP tool surface, bridge plugin).
---

# NV oOS Astro Forge — ops guide (Proposal 096 Phase 0)

## What this is

The generator that turns a WordPress/WooCommerce site into a native **Astro 7**
headless frontend. WordPress stays the CMS; the generated project pulls
content through an Astro **content-layer loader** at build time (freshness =
webhook → rebuild, never runtime fetches), renders sanitized HTML, and ships
SEO-complete static output. Pilot customer: a WooCommerce storefront — its
design language was already extracted via Proposal 098 (see the customer
notes below). Full context: `docs/project/proposals/096-astro-forge-wp-generator-mcp-proposal.md`
(+ `-implementation-plan.md`, `-research.md`).

## Architecture decisions (do NOT re-litigate)

- **Content-layer loaders, not materialized content files** — `content_materialize` stays opt-in (096 §2.3).
- **REST-first**: `wp/v2` + `wc/v3`, **never WPGraphQL**. `_fields` pruning + `_embed` are the anti-N+1 discipline.
- **Sanitization is mandatory, versioned, allowlisted, never a passthrough** — all WordPress HTML passes `lib/sanitize.ts` before `set:html` (096 §2.4).
- **No plaintext credentials** — auth comes from `.env` (`WP_APPLICATION_USER`/`WP_APPLICATION_PASSWORD`), never from the profile or the generated repo. SSRF-safe by construction: the CLI consumes operator-written site profiles only (the open-world fetch surface is the `/mcp` `design_analyze` guard, Proposal 098).
- **Never silent truncation** — `fetchAll` returns `truncated: true`, the loader warns, entries carry the flag, pages show a notice.
- **Built assets never ship** — the scaffold's gitignore gate guarantees `dist/` + `.astro/` are ignored in the customer repo.

## File map

| Path | Role |
|---|---|
| `lib/types.ts` | `SiteProfile` / `WpCollection` contracts |
| `lib/wp-client.ts` | WP REST client — `X-WP-TotalPages` pagination, typed `WpClientError` codes |
| `lib/wp-loader.ts` | Astro 7 content-layer loader (`createWpLoader`) |
| `lib/sanitize.ts` | `SANITIZE_VERSION` + allowlist + `sanitizeHtml()` |
| `lib/scaffold.ts` | Template copy, FORGE-marker rewrite, manifest, gates |
| `lib/vault.ts` | Phase 3.1 credential store — AES-256-GCM per-entry (`~/.nvoos-forge/vault.json`), `NVOOS_FORGE_VAULT_KEY` passphrase, plaintext opt-in, `maskSecret` |
| `lib/sites.ts` | Phase 3.4 multi-site registry (`sites.json`) — named profile refs + default flag |
| `lib/github.ts` | Phase 3.2 octokit deploy — private-by-default repo create, git-data commit/push, sanitized errors |
| `lib/deploy-config.ts` | Phase 3.3 generated pipeline — deploy.yml/rebuild.yml + fail-closed `verify-dispatch.mjs` |
| `lib/wizard.ts` | Phase 4 setup_wizard — analyze → register → scaffold → build → git init → pipeline |
| `lib/content-scan.ts` | §3.3 content audit scanner (htmlparser2 — embeds/alt/hosts/shortcode artifacts + unprocessed brackets) |
| `lib/redirects.ts` | §3.3 live 301-map generator (the template's exact rules, computed from REST) |
| `lib/ssrf.ts` | URL guard — private/literal-range refusal, registry allowlist + `NVOOS_FORGE_OPEN_ANALYZE` opt-in, CLI-only loopback exemption |
| `lib/project-files.ts` | Shared source collector for pushes (CLI deploy + `github_commit` tool) |
| `mcp/` | Phase 4 MCP surface (095 dual-era pattern): single-source `registry.ts` (zod + annotations + write flags; router/full modes), `bff.ts` (rate limit → Host/Origin → fail-closed write auth), `stdio.ts`, 7 tool slices |
| `scripts/forge-mcp.mjs` | MCP Streamable HTTP entry (`FORGE_MCP_PORT`, default 8472) |
| `server.json` | 061-pattern MCP registry metadata (`io.github.nvdigitalsolutions/nvoos-astro-forge`) — NOT in the npm `files` |
| `scripts/forge.mjs` | CLI (Node ≥ 22.6 — native TS type stripping, zero build step) |
| `scripts/wp-fixture-server.mjs` | Hermetic wp/v2 wire fixture — the Phase 0 CI stand-in for WordPress Playground |
| `scripts/builtin-template.mjs` | Test fixture generator (nested `main/templates/blog/` tree with a REAL loader) |
| `templates/blog/` | The production template (posts/pages, canonical + JSON-LD, sitemap/robots, `--forge-*` tokens) |
| `tests/` | `wp-client` / `sanitize` / `wp-loader` / `scaffold` unit suites + `forge-e2e.test.ts` (exit gate) |
| `.github/workflows/astro-forge.yml` | CI: typecheck + unit + e2e on Node 24 (Astro 7 needs ≥ 22.23.4 — the runner's latest 22.x is one patch short) |

## Dev loop (hermetic — no live site needed)

```sh
cd examples/nvoos-astro-forge
npm install
npm test                 # 38 unit tests (client, sanitizer, loader, scaffold)
npm run typecheck
npm run test:e2e         # exit gate: fixture WP → scaffold → npm install → astro check + build → HTML asserts (~40s, registry access for the generated project's install)
node scripts/wp-fixture-server.mjs   # :8473 — real wp/v2 wire shapes
node scripts/forge.mjs site.json --target ./out --check   # live source check (root doc + per-collection size-vs-cap)
node scripts/forge.mjs site.json --target ./out           # scaffold the project
```

## Forging a customer site (the standard loop)

1. Write `site.json` (operator allowlist): `{ url, name, collections: [{ slug, restBase, fields, embed, perPage, maxPages }] }`.
2. `--check` first — a build must never silently truncate.
3. Scaffold → `cd <target> && npm install && npm run build` with `ASTRO_SITE` set.
4. Design language (098 `design_theme` output) applies over the template's `--forge-*` tokens in `src/styles/global.css` — content is re-themed, never re-cloned.

## The exit gate (CI-enforced)

`tests/forge-e2e.test.ts` boots the fixture server on an ephemeral port,
scaffolds the **production** template, `npm install`s the generated project,
runs `astro check` + `astro build`, then asserts on `dist/`: posts/pages
rendered, `alert`/`onerror`/`javascript:` count = 0 in the xss-trap post,
allowlisted embeds survive, canonical + `BlogPosting` JSON-LD + sitemap/robots
wired. The workflow runs on `paths: examples/nvoos-astro-forge/**`.

## Gotchas (each cost a fix 2026-10-31 — do not re-hit)

- **Astro 7 spread params are flat slash-joined strings, NOT arrays** —
  `getStaticPaths` for `src/pages/posts/[...parts].astro` must return
  `params: { parts: '1/slug' }`. The route generator uses the params value as
  the path segment directly and the validator requires `typeof value === 'string'`
  (verified against astro 7.4.4 dist sources: `routing/generator.js`,
  `routing/internal/validation.js`, `render/params-and-props.js`). An array
  fails the build with `GetStaticPathsInvalidRouteParam`.
- **FORGE marker rewriting must be line-anchored** — naive
  `indexOf('// FORGE:site')` matches prose that mentions the marker inside a
  header comment and mangles `content.config.ts`. Match
  `line.trim() === '// FORGE:site'` only.
- **Template-copy filters must exclude by directory basename** — a
  `/(node_modules|dist|\.astro)$/` path regex also matches every `*.astro`
  page file (the `\.astro$` branch) and silently drops all pages. Filter on
  `path.basename(src)` ∈ {node_modules, dist, .astro}.
- **Emitting a regex literal through a JS template literal needs the
  backslash doubled** — `\\/+$/` in the scaffold source (an identity escape
  otherwise emits `//`, turning the generated line into a comment and
  breaking the parse).
- **Truncation math:** `truncated = page === maxPages && page < totalPages` —
  a catalog that ends exactly at the cap is complete, not truncated.
- **`sanitize-html` `allowedIframeHostnames` strips the disallowed `src` but
  keeps the inert `<iframe>` tag** — assert on `src` absence, not tag absence.
- **Node ≥ 22.6 native type stripping runs the CLI with zero build step** —
  `scripts/forge.mjs` imports the `.ts` libs directly. Requirements: explicit
  `.ts` extension specifiers in relative imports, erasable-only TS (no enums/
  namespaces), `allowImportingTsExtensions: true` + `noEmit` in the tsconfig.
  The generated template inherits `allowImportingTsExtensions` from
  `astro/tsconfigs/strict` — vendored `.ts`-extension imports typecheck as-is.
- **`astro check` on a generated project needs `@types/sanitize-html` and
  `@types/node` in the template devDeps** — the vendored `sanitize.ts` and
  `wp-client.ts` typecheck under the language server.
- **`--overwrite` re-scaffold is destructive** — it `rm`s the target
  including `node_modules` (reinstall after). An empty target dir is safe to
  scaffold into; a non-empty non-forge dir is refused without `overwrite: true`.
- **Woo sets `price` to the sale price while on sale** — sale state is
  `salePrice !== regularPrice`, never `salePrice !== price` (the first cut
  rendered no strike-throughs at all). wc/v3 needs consumer keys (401
  without); wp/v2 product CPTs stay public but have no commerce fields —
  both shapes share one loader via `kind: 'product'`.
- **`_embed` does not guarantee media** — resolve `featured_media` IDs via
  `wp/v2/media/{id}?_fields=source_url` with bounded concurrency (5); an
  image miss is never a build failure.
- **Template pages binding collections must be scaffold-pruned** when the
  profile omits the collection, and every remaining consumer (the sitemap
  endpoint) gates on `nvoos.json` — an undefined `getCollection()` fails
  the build.
- **The WP static front page** maps to profile `frontPage` — rendered at
  `/`, skipped by the slug route + sitemap (one canonical URL).
- **Astro ignores underscore-prefixed files in `src/pages/`** (the partial
  convention) — `_redirects.ts` never becomes a route. Emit
  `/redirects.json` and materialize `dist/_redirects` post-build.
- **Token rewrites must keep their FORGE markers** and cover every token
  the template block defines (layout tokens included) — see the
  `/* FORGE:tokens */` span contract below.
- **`inferSize` is required on Astro Image for remote sources** —
  `widths`/`sizes` alone fail the build with `missing-image-dimension`.
  The domain allowlist mirrors the content layer's env-first rule, and
  SmartImage degrades to a plain `<img>` for non-allowlisted hosts (a CDN
  image must never fail a build).
- **`process.exit()` races undici teardown on Windows** (0xC0000409) —
  graceful `exitCode` + natural drain in the CLI.
- **The scaffold CLI is operator-run and has no rate limiting** — rate
  limiting/retry belongs on the future MCP surface, not the CLI.
- **`forge.mjs` is plain JS, never TS syntax** — `.mjs` gets NO type
  stripping: `import type` and inline `type` specifiers are syntax errors
  there (strip them; the runtime DEPLOY_MODES check carries the constraint).
- **Node strip-only mode bans parameter properties** —
  `constructor(private readonly x)` fails with
  `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` at CLI runtime even though vitest
  (esbuild) accepts it. Declare the field explicitly and assign in the
  constructor. Also banned: enums/namespaces; inline `type` specifiers in
  named imports need a separate `import type` statement.
- **Secret grep gates must not match empty assignments** — `PATTERN=[^ ]+`
  matches the newline after an empty `=` (and the quote in the scaffold's
  own emission). Use value-shaped classes (`[^[:space:]"']{4,}` in GNU
  grep, `[^'"\n]{4,}` in JS) so `.env.example` placeholders and scaffold.ts
  stay clean while real values still trip.
- **SDK v2 registerTool + zod 4.6 (cost a full session 2026-10-31):** the
  SDK's deprecated raw-shape overload (`ZodRawShape = Record<string,
  z.ZodType>`) expects a zod classic surface that zod 4.6 no longer
  provides — raw shapes fail with `$ZodType`-missing-`_def` errors. The
  non-deprecated overload accepts a zod INSTANCE typed as the SDK's
  exported structural `StandardSchemaWithJSON`; type the registry field as
  that, never as `z.ZodTypeAny`/raw shapes. The `ToolCallback` generic is a
  conditional type plain function expressions cannot satisfy even when the
  return type is provably assignable (probe it!) — register through a
  cast to an exact `(name, config, cb) => unknown` signature. And the SDK
  imports types from `zod/v4` — keep the mcp files importing `z` from
  `'zod/v4'` so type identities line up.

## Template contract (FORGE markers)

`templates/blog/src/content.config.ts` carries line-anchored markers:
`// FORGE:site` … `// FORGE:collections-end`. `scaffold()` replaces that span
with env-driven `siteUrl` (`import.meta.env.WP_SITE_URL ?? '<profile url>'`),
the auth block, one `WpCollection` literal per profile collection, and the
`export const collections` block. Everything outside the span (imports,
`defineCollection` wiring) belongs to the template author. `nvoos.json`
(manifest v1: generator/url/generatedAt/collections) marks a forge project —
it is both the idempotency marker and the clobber guard.

## Customer design-language notes (feed into the forge)

From the 098 pipeline for the pilot customer (a WooCommerce storefront):

- Extracted design language: accent `#720eec` (Woo `--wc-primary`), surface
  `#ffffff`, body text `#7a7a7a`, type MuseoSansRounded/Oswald — theme name
  `pilot`. **WCAG flag:** body `#7a7a7a` on white = 4.29:1 (fails AA); the
  customer's unassigned pool has `#555555` (7.8:1) as the one-token fix — a
  ready upsell during the rebuild.
- Forge today: posts/pages collections can be forged live against the
  customer's site. Woo products need Phase 1's `wc/v3` collection.
- Keep the customer's name and URL out of skills and generated code — the
  design tokens alone are the deliverable (the 098 recreation loop is
  concept-adaptation, never cloning).

## Phase roadmap (096 §5)

- **Phase 0 — shipped** (PR #7335, merged 2026-10-31): client, loader,
  sanitizer, scaffold CLI, blog template, hermetic fixture, CI exit gate.
- **Phase 1a — shipped 2026-10-31** (PR #7337): Woo collections (`kind:
  'product'`, wc/v3 + wp/v2 shapes, wc-consumer auth env), storefront
  template pages (`/products/` + detail, Product JSON-LD), static front page
  (`frontPage`), per-collection `exclude`, `optional` sources, scaffold page
  pruning, brand name from `nvoos.json`. Live pilot forge: 49 pages from
  production.
- **Phase 1b — shipped 2026-10-31:** MIT license carve-out (owner decision
  Q7, mirrors 092 Q8 — NOTICE ships into generated projects), `tokens_apply`
  (098 design language over the `--forge-*` markers + WCAG contrast gate
  warnings), SEO suite (`/feed.xml`, `/404.html`, `/redirects.json` →
  `dist/_redirects` post-build).
- **Phase 1c — shipped 2026-10-31:** `site_analyze` (`forge.mjs analyze
  <url> [--write site.json]` — types/counts/front-page/junk/Woo/SEO/lockdown
  probes, wc/v3-auth count fallback; live-verified against the pilot — all
  ten junk pages found automatically) + the media pipeline (SmartImage:
  Astro Image with `inferSize` for same-host images, CDN passthrough).
- **Phase 1d — shipped 2026-10-31:** Pagefind search (post-build index,
  lazy-loaded `/search/` shell) + the `source: 'payload'` collection variant
  (nvoos-commerce/v1 envelope — body pagination, `oldPrice` sale semantics,
  slugify for missing slugs; discovery offers the payload candidate when
  the namespace is advertised and no product CPT exists).
- **Phase 2 — shipped 2026-10-31:** the standalone companion plugin
  **`plugins/nvoos-forge-bridge`** (Q4 naming amendment — `nvoos-astro-bridge`
  was taken by the velocity bridge addon): signed, debounced rebuild
  webhook (X-Forge-Signature, `send_pending()`/`reset_pending()` seams),
  inbound signature-verified `/rebuild` route, single-use hashed preview
  tokens, redacted health, settings page with write-only secrets,
  uninstall.php, own phpcs + PHPUnit (24/24 on WP latest in Docker; the
  payload now also carries a self-verifying `time`/`nonce`/`signature`
  proof — `payload_signature()`) + `.github/workflows/phpunit-forge-bridge.yml`
  with the PCP gate, `.distignore`, and `.wordpress-org/` listing assets.
- **Phase 3 — shipped 2026-10-31:** vault + multi-site + GitHub deploy +
  generated pipeline (see `-implementation-plan.md` §2.7): `forge vault` /
  `forge site` / `forge deploy` commands; repos private by default;
  per-invocation auth (never persisted, masked); the emitted
  `verify-dispatch.mjs` is the CI-side signature verification — the bridge
  payload proof exists because the `X-Forge-Signature` header does not
  survive GitHub's dispatch delivery. Publish: `@nvdigitalsolutions/nvoos-
  astro-forge`, tag `nvoos-astro-forge-v*` → `publish-astro-forge.yml`
  (provenance). Secret grep gates in CI + the e2e credential-hygiene walk.
- **Phase 4 — core shipped 2026-10-31:** `forge wizard` (one command, URL
  → built + deploy-ready) and the `/mcp` surface (see §2.8): 29-tool v1
  catalog (incl. the §3.3 long-tail slices — content_audit/preview,
  redirects_generate, media_audit, collections_generate, site_update,
  preview_token, webhook_verify) over the single-source registry,
  `NVOOS_FORGE_MODE=router|full` (3 meta-tools vs full), dual-era
  Streamable HTTP (`forge-mcp.mjs`) + stdio (`nvoos-forge-mcp-stdio`),
  rate limit + Host/Origin + fail-closed write auth, SSRF-guarded fetches.
  Remaining: registry publication (owner) and the Playground demo
  blueprint.

## Repo conventions

- PRs against `alpha-working`, owner-merge; explicit-path staging (`git add
  <file>`, never `-A`) — see `mcp-ai-wpoos-git-ops`.
- Adding a skill updates the inventories: `AGENTS.md` (2 spots) +
  `.github/copilot-instructions.md` (2 spots), bumping the skill count.
- Docs: the research file §0 carries the verified build learnings; the
  implementation plan §2.1 carries Phase 0 status vs plan.

## References

- `examples/nvoos-astro-forge/README.md` (layout, quick start, invariants)
- Proposal 096 trio (`docs/project/proposals/096-*`) · Proposal 098 (design
  language import — the theme input) · Proposal 092/095 (the storefront +
  ADS the template borrows from)
- Related skills: `mcp-ai-wpoos-astro-storefront` (the serving side — bridge,
  /mcp, tokens), `mcp-ai-wpoos-playground-demos` (the Phase 2 Playground
  fixture replacement), `mcp-ai-wpoos-git-ops`.
