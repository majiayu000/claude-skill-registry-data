---
name: insolvia-design-system-bump
description: >-
  How to take a new @insolvia-ai/design-system or @insolvia-ai/tokens version
  into this repo — and the rule that the packages themselves are NOT here to
  edit. Use this whenever a task means changing a shared component (Button,
  Field, Card, Select…), changing a design token or colour, or picking up a
  design-system release: "update the design system", "bump tokens", "change the
  button's padding", "make the brand colour warmer". Reach for it BEFORE
  searching for packages/insolvia_design_system, which no longer exists — the
  packages live in github.com/insolvia-ai/design-system and reach this repo
  only as published versions. It covers which manifests and which THREE
  lockfiles must move together, and why a bump that skips `npm run tokens`
  leaves the sign-in page's colours behind. Read it too when a surface suddenly
  renders monochrome, or to change a brand colour: the package's base theme is
  deliberately unbranded, and Insolvia's palette lives in brand/colors.json.
---

# Taking a design-system or tokens version

## First: the package is not in this repo

`@insolvia-ai/design-system` and `@insolvia-ai/tokens` live in
**[`insolvia-ai/design-system`](https://github.com/insolvia-ai/design-system)**.
There is no `packages/insolvia_design_system` here any more, and there must not
be one again — see
[ADR 0010](../../../docs/adr/0010-design-system-moves-to-its-own-repository.md).

So a task that says "change the Button" is **two** pieces of work:

1. Change and release it in the design-system repo (its own CI gates the
   version bump and publishes on merge).
2. Bump the dependency here — that is what this skill covers.

**Never** short-circuit step 1 with a `file:` or `link:` path to a local
checkout, even temporarily, even uncommitted. The app used to read the
package's source through a workspace symlink; one package with two live states
is the exact failure ADR 0010 removed. To try an unpublished change, publish a
prerelease from that repo and depend on it by version.

## The bump

**Three** surfaces consume the packages, and **they do not share a lockfile** —
there are three of those too. Missing one is the usual way a bump half-lands,
and the admin portal is the one most often forgotten because it arrived last.

| File | What to change |
|---|---|
| `package.json` (root) | `devDependencies` → `@insolvia-ai/tokens` — the brand tools resolve it from here |
| `apps/insolvia_app/package.json` | `dependencies` → `@insolvia-ai/design-system`, `@insolvia-ai/tokens` |
| `apps/insolvia_marketing/package.json` | `devDependencies` → `@insolvia-ai/design-system` (marketing does not use tokens) |
| `apps/insolvia_admin/package.json` | `devDependencies` → `@insolvia-ai/design-system` (nor does admin) |
| `package-lock.json` | regenerate with `npm install` from the repo root |
| `apps/insolvia_marketing/package-lock.json` | regenerate with `npm install` **inside `apps/insolvia_marketing`** — it is deliberately outside the workspace |
| `apps/insolvia_admin/package-lock.json` | regenerate with `npm install` **inside `apps/insolvia_admin`** — outside the workspace for the same reason |

Check what you actually got, rather than trusting the range — all three
lockfiles must name the same version:

```bash
for p in . apps/insolvia_marketing apps/insolvia_admin; do node -e "const l=require('./$p/package-lock.json');for(const [k,v] of Object.entries(l.packages||{}))if(/@insolvia-ai\/(design-system|tokens)$/.test(k))console.log('$p',k,v.version)"; done
```

Installing needs a GitHub Packages token, even for public packages:

```bash
eval "$(./scripts/github-packages-auth.sh --export)"
```

## Always regenerate the brand surfaces

```bash
npm run tokens
```

Commit whatever that writes. `npm run tokens:check` is a required PR check
(`Cognito branding` — the job kept its name after it grew), and it fails on a
bump that did not regenerate.

**`brand/colors.json` is where Insolvia's colours live**
([ADR 0020](../../../docs/adr/0020-the-brand-is-a-consumer-owned-override.md)),
and it is the thing to understand before touching any of this. From tokens 0.5.0 the design system's
base theme is deliberately *unbranded*: monochrome chrome, square corners, no
display face, with `primary`/`accent`/`brand` all resolving to neutral-12. That
empty seam is the package's intent — a re-brand belongs to the consumer — so
Insolvia's navy and brass are **overrides layered on top**, not package
defaults.

`npm run tokens` renders that palette into the four surfaces that cannot read
the JSON themselves:

| Generated | Consumed by |
|---|---|
| `apps/insolvia_app/src/theme/brand-colors.ts` | the app — both `themeFor()` and the `ThemeProvider` that themes the package's `.native` leaves |
| `apps/insolvia_marketing/app/styles/brand.css` | marketing, imported after the package's `theme.css` |
| `apps/insolvia_admin/src/styles/brand.css` | the admin portal, same shape |
| `infra/modules/auth/managed-login-settings.json` | Cognito's hosted sign-in page |

**Never hand-edit one of those four** — the next `npm run tokens` overwrites it
and the drift check fails in between. Change `brand/colors.json` and regenerate.

Two things that follow, and are easy to get wrong:

- **The overrides are PARTIAL on purpose.** Only roles Insolvia actually moves
  are listed; the status colours, `dangerText`, the overlay values and the
  neutral ramp stay the package's, so a tokens release that adds a role or
  re-measures a contrast reaches every surface without an edit here. Restating
  a package default in `brand/colors.json` silently opts out of that.
- **The hover/active states are native-only.** Web derives them with
  `color-mix()` over the base role, so the CSS deliberately omits them —
  emitting them would freeze a live derivation. React Native has no blend and
  needs them stated. `tool/brand-palette.ts`'s `DERIVED` owns that split.

Skipping the regeneration leaves the sign-in page — or one app — on a different
palette from the rest, and nothing else in the tree would say so.

## Then verify, locally

```bash
npm run ci
```

```bash
npm run build --workspace @insolvia-ai/app
```

The build matters more than usual for a design-system bump: the app renders the
package's `.native` leaves on **every** platform, web included, through a Metro
`resolveRequest` override in `apps/insolvia_app/metro.config.js`. If a release
reorganises the package's internals, that override is what breaks, and it breaks
*silently* — the bundle still builds, having resolved the `.web` leaves, whose
Tailwind classes reference CSS the app never compiles. A bundle that looks fine
and renders unstyled is the failure mode to watch for.

Marketing and the admin portal each have their own gate, and neither is covered
by the root `npm run ci`:

```bash
npm run typecheck --prefix apps/insolvia_marketing && npm run build --prefix apps/insolvia_marketing
```

```bash
npm run typecheck --prefix apps/insolvia_admin && npm run build --prefix apps/insolvia_admin
```

Build both, not just typecheck: each CI job greps its bundle for `react-native`,
which is how a platform-split regression shows up. And on a release that touches
theming, check the brand actually survived into the built CSS — the base theme's
own `[data-theme='dark']` block is still in there, and ours only wins by landing
after it:

```bash
grep -o -- "--color-primary:[^;]*;" apps/insolvia_admin/dist/assets/*.css
```

## Scope

A version bump is ordinary work and does **not** need its own PR — that rule
belonged to the package while it lived here. Bundle it with the change that
needs it. What still needs care is the list above moving together: a manifest
bumped without its lockfile fails `npm ci` in CI, and a marketing lockfile left
behind means the two surfaces silently render different versions of the same
component.
