---
name: provider-swap
layer: stack
description: Swap the external provider/library that backs a crouton package (e.g. the map renderer, geocoder, editor engine, storage SDK) while keeping the package's public API stable so consuming apps need no changes. Use when asked to "change the X provider", "replace library Y in package Z", "switch from <vendor A> to <vendor B>" inside packages/. Encodes the keep-the-API-stable playbook + the gotchas (dist .d.ts over docs, generator templates, fixtures, dup-dep type clashes).
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, WebSearch, WebFetch
---

# Swap a package's external provider (keep the public API)

Replacing the library/SaaS behind a crouton package — the map renderer, the
geocoder, the rich-text engine, a storage SDK — is a **refactor with an API
contract**, not a rewrite. The bar: **consuming apps (and the generator output)
keep working with zero edits.** This skill is the playbook + the traps, distilled
from the Mapbox→MapLibre swap (#538): a package consumed as a Nuxt layer leaks
its provider's types and templates into every app, so the swap has more surface
than the component files suggest.

## When to use
- "Change the maps provider", "replace mapbox-gl with maplibre", "switch the
  geocoder", "swap the editor engine in crouton-editor", "use a different upload SDK".
- Any task that changes the **library or service** a `packages/*` package wraps.
- **Not** for adding a brand-new package (use `crouton` / scaffolding) or for a
  pure version bump (use `dependency-sweep`).

## Hard gates first (don't skip)
- **ISSUE-FIRST** — open the tracking issue before editing (`github-tasks`). A
  provider swap is multi-file; an epic + the swap as the unit of work.
- **Packages boundary** — editing `packages/*` needs approval
  (`echo '<pkg>' >> .claude/.package-edit-approved`; remove it when done).
- **Decide the non-code questions up front** with `AskUserQuestion` — they change
  what you build: which library, which tile/style/host, API keys vs keyless,
  what replaces capabilities the new provider lacks (e.g. MapLibre has **no**
  geocoding; Mapbox style URLs are **incompatible**). Honour repo constraints
  (OSS, self-hostable, no mandatory SaaS — see `ecosystem-check`).

## The protocol

### 1. Map the surface before touching code
Grep the package for every public seam, and the **whole repo** for consumers:
```bash
rg -l '<old-lib>|<OldType>|<old-css-prefix>' packages/<pkg>
rg -l 'Crouton<Pkg>|use<Pkg>|<exported-const>' packages apps pocs docs
```
List: components, composables, `server/` routes, `app/types`, `nuxt.config.ts`
(modules/runtimeConfig/css), `crouton.manifest.ts` (**incl. its generator
contribution templates**), `package.json`, `CLAUDE.md`/`README`, docs site,
`.env.example`. The manifest's generator template and the docs are the bits most
often forgotten.

### 2. Learn the new library's real API — from the dist, not the docs
Docs sites often 403/whiff. The source of truth is the published types:
```bash
npm view <new-lib> version exports peerDependencies
cd /tmp && npm pack <new-lib>@<ver> && tar -xzf *.tgz
# read package/dist/index.d.ts for exact props/events/exports
```
Confirm: required peers (are the heavy ones `optional`?), whether it touches
`window` (→ client-only + `build.transpile`), and which capabilities are missing
vs the old provider (plan replacements).

### 3. Keep the public API stable (the whole point)
- Same component names, props, slots, emits; same composable names + return shapes.
- If you must rename internals, **re-export the old names as deprecated aliases**
  (e.g. `export const OLD_STYLES = NEW_STYLES`) so external imports don't break.
- Same server-route shape: if the proxy's response shape is consumed (e.g.
  `useGeocode` expects `{ features:[{center,...}] }`), **normalise the new
  provider's response back to it** rather than changing callers.
- Near-drop-in forks make this easy (maplibre-gl ↔ mapbox-gl: identical
  Marker/Popup/Map runtime API → only import strings + CSS prefixes change), but
  verify per-symbol against the `.d.ts`.

### 4. Don't forget the generator + config surface
- A package's `crouton.manifest.ts` may ship **generated form/list templates**
  (`enhanceForm`/`enhanceList`) and detection patterns. Update the template to
  the new provider, and keep its bindings consistent with the package's own
  components (e.g. the slot→marker `:map="map as any"` cast — see the type-clash
  trap below).
- Update `nuxt.config.ts`: drop the old module, add `build.transpile` for ESM
  deps that hit the DOM, replace token/runtimeConfig with the new keys.
- Update `package.json` deps + keywords + a version bump.

### 5. Sync the docs (large surface)
Package `CLAUDE.md` + `README`, the docs site page, the modules/packages tables,
and `.env.example` all name the old provider. Search and update. Add a short
**migration note** (what env vars went away, what URLs are now invalid).

### 6. Verify — and add a fixture if one is missing
- `pnpm -r --filter './apps/*' typecheck` (the consuming-app gate).
- **A package that contributes generator templates needs a fixture that actually
  generates from it.** A typecheck of existing apps can miss the generated path
  (e.g. velo uses a bespoke form, so the generated map form's type bug only
  surfaced once `with-maps` generated one). Add/extend an e2e fixture
  (`e2e/CLAUDE.md`) that exercises the swapped surface; run `e2e-smoke`.

## Gotchas (each one bit during #538)
- **Docs site blocks fetching** → `npm pack` + read `.d.ts` (step 2).
- **Capability gaps** → the new provider may not do everything the old did
  (MapLibre: no geocoding, incompatible style URLs). Decide the replacement with
  the user *before* coding (step "Hard gates").
- **CSS class prefixes change** (`.mapboxgl-*` → `.maplibregl-*`) — grep styles.
- **Duplicate-dependency type clash** — if the monorepo has two versions of the
  new lib (a transitive old one + your new one), the same class can have two type
  identities; a slot value typed by one won't satisfy a prop typed by the other
  ("missing _privateMethod from type Map$1"). Cast at the boundary (`as any`)
  consistently, matching how the package's own components already bind it.
- **Generated-template path is untyped-tested** until a fixture generates it
  (step 6).
- **Don't widen contribution scope by accident** — a package's generator
  contribution should only apply when the app uses that package; collection-name
  reservations are global footguns (see #558).

## Output
A PR (`Closes #NN`) where: the public API is byte-stable for consumers, the new
provider is keyless/self-hostable per constraints (or the key is documented),
docs carry a migration note, and a fixture proves a generated consuming surface
still boots + works. Run `postmortem` at epic close — provider swaps are exactly
the kind of first-of-their-kind work whose lessons should feed back here.
