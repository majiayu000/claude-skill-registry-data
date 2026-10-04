---
name: shadcn-registry-first
description: >
  Bias UI work toward installing existing components from configured shadcn
  registries (the free @shadcn registry and the paid @shadcnblocks block
  registry) before hand-rolling them. Triggers when building or restyling React
  UI in a project that has a components.json with registries configured —
  heroes, navbars, footers, pricing tables, feature grids, dashboards, forms,
  auth screens, marketing sections, data tables, and other common blocks. Use
  the shadcn MCP tools to search, preview, and add, and always assemble at least
  three buildable variations with a side-by-side comparison surface before
  settling on one. Do NOT trigger for genuinely
  bespoke or domain-specific components that no registry would carry, for
  non-React stacks, or for projects with no registry configured.
---

# Shadcn registry first

Darkmatter pays for the `@shadcnblocks` block registry and wires both it and the
free `@shadcn` registry into the shadcn MCP. That means most common UI surfaces —
heroes, navbars, footers, pricing tables, feature grids, dashboards, login
screens, data tables — already exist as production-quality, accessible,
themeable blocks you can install in one command. Reaching for them first is
faster and produces better output than writing JSX from a blank file.

The default failure mode this skill corrects: an agent silently hand-rolls a
hero or a pricing table that the registry already has, burning tokens and
shipping something less polished. Before you write a new component from scratch,
check whether the registry already carries it.

## When to use

- Building a new marketing/landing section: hero, feature grid, CTA band,
  testimonial, logo cloud, footer, pricing.
- Building app chrome: navbar, sidebar, dashboard shell, settings panel.
- Building common interactive surfaces: forms, auth screens, data tables,
  command palettes, file upload, calendars, charts.
- Restyling or replacing an existing component where a cleaner registry block
  would do.
- The user says "add a X section", "build a Y page", "I need a Z component" and
  Z is a recognizable web UI pattern.

## When NOT to use

- The component is genuinely domain-specific (e.g. a liquidity-range tick chart,
  a protocol-specific position card) — no general registry will carry it, so
  build it, ideally composing registry primitives.
- The project isn't React, or has no `components.json` with registries
  configured. Check first (see below); if nothing is configured, this skill
  doesn't apply.
- A tiny one-off element (a single styled button, a label) where installing a
  block is heavier than writing the line.
- You're editing an existing component's internals, not adding a new surface.

## Workflow

### 1. Confirm registries are configured

Use the shadcn MCP `get_project_registries` tool (or read `components.json`). You
want to see `@shadcnblocks` and/or `@shadcn` listed. If `@shadcnblocks` is
present but the API key isn't resolving, see "Registry access" below — don't
fall back to hand-rolling just because the key is missing; fix the key.

### 2. Search and shortlist at least three candidates

Use `search_items_in_registries` with the pattern you need, scoped to the
configured registries. Search the _thing_, not keywords:

- `search_items_in_registries(registries=["@shadcnblocks"], query="hero dark")`
- `search_items_in_registries(registries=["@shadcnblocks"], query="pricing toggle")`
- `search_items_in_registries(registries=["@shadcnblocks"], query="dashboard analytics")`

`@shadcnblocks` is large (1000+ blocks); a search like "hero" returns hundreds.
Narrow with a qualifier ("hero split", "hero video", "hero dark") and skim the
descriptions — they're written to be skimmable and tell you layout, columns, and
notable features.

From the results, pick **at least three** distinct candidates that each plausibly
satisfy the brief. Favour genuine variety — different layouts, density, or visual
emphasis — not three near-identical blocks. The point is to give the user a real
choice, the same way you'd offer multiple font or palette options rather than
deciding silently.

The search output can be very large. If a single call returns a giant truncated
list, don't read the whole dump into your own context — delegate processing to an
`explore` agent with Grep/Read over the saved tool-output file, or re-run with a
tighter query.

### 3. Preview each candidate

For every shortlisted candidate, inspect what you're committing to:

- `get_item_examples_from_registries` — find the demo and its full source so you
  see the actual markup and props.
- `view_items_in_registries` — see the item's files, dependencies, and registry
  dependencies (other components it pulls in).

Confirm each fits the project's design system (theme tokens, fonts, radius). Many
blocks assume the default shadcn theme; if the project overrides tokens (e.g. a
terminal theme with `--radius: 0`), the block will adapt to those tokens, but
check for hardcoded colors or rounded corners you'll need to reconcile.

### 4. Install all the variations

Get each add command with `get_add_command_for_items` and run it (typically
`bunx shadcn@latest add @shadcnblocks/<name>`). This writes each component into
the project's `ui`/`components` aliases and installs dependencies. Keep the
variations isolated from each other — install them under clearly named files or a
scratch directory so swapping or deleting one doesn't disturb the others.

### 5. Build a comparison surface

Always give the user a way to see the variations side by side and built, not just
names in chat. Mirror the font-comparison pattern: render every variation on one
screen, each clearly labelled, wired with the same representative content so the
only difference is the block itself.

- **Web app with routing** (TanStack Router, Next): add a temporary route such as
  `/compare/<feature>` that imports and stacks all variations with a heading per
  option. Mark it clearly as throwaway (a `// TODO: remove after selection`
  comment) and make sure it bypasses any auth/boot gating so it's viewable.
- **Component / Storybook**: a gallery story rendering each variation in a row.
- Run the dev server and hand the user a working preview URL (e.g. the
  Tailscale-served dev URL for this environment). Don't ask them to imagine the
  result — let them look at it.

The comparison surface must build cleanly (`lsp_diagnostics`, `check-types`, and
the project build) before you present it.

### 6. Let the user choose, then adapt the winner

Present the labelled options and the preview URL, and ask which to keep. Once they
pick:

- Wire the winner to real data and routes, strip demo placeholder copy, reconcile
  theme mismatches, and remove parts you don't need.
- Delete the other variations and the temporary comparison surface so they don't
  rot in the codebase.

The win is starting from a polished, accessible structure and letting the user
choose between real, built options — not shipping the first block you found or
leaving lorem ipsum behind.

### 7. Audit

After settling on the winner and removing the rest, run the shadcn MCP
`get_audit_checklist` and work through it (imports resolve, dependencies
installed, no leftover demo data or comparison scaffolding, types clean). Then run
the project's own checks (`lsp_diagnostics`, `check-types`, build).

## Registry access

The `@shadcnblocks` registry requires an API key in the `Authorization` header
of `components.json`. In darkmatter repos this is handled per-project:

- `components.json` is gitignored and carries the resolved key (or the shadcn MCP
  reads `${SHADCNBLOCKS_API_KEY}` from the environment).
- `components.json.template` is committed with the `${SHADCNBLOCKS_API_KEY}`
  placeholder.
- The key lives in the secret store (himitsu: `himitsu read shadcnblocks-api-key`,
  or a SOPS-encrypted secret). A small `scripts/setup-components-json.ts` renders
  the template with the key.

### Before running any `bunx shadcn` command

The rendered `components.json` must exist **and be fresh** — a stale one from a
previous session may carry an expired key. Always do these two steps first:

1. **Build components.json**: run `bun scripts/setup-components-json.ts` from the repo
   root. This reads the current key from himitsu and writes the gitignored
   `components.json`. Skip this and you'll get 401 auth failures.
2. **`cd` into the app directory** (e.g. `apps/web/`) before running
   `bunx shadcn@latest add ...`. The CLI resolves registries from `components.json`
   in the current working directory. Running from the monorepo root will fail.
3. **Use `--overwrite`** flag to skip interactive prompts about existing files
   (`utils.ts`, `button.tsx`, etc.) that the block may depend on but already exist
   in the project.

Typical invocation:

```bash
# From repo root:
bun scripts/setup-components-json.ts
cd apps/web
bunx shadcn@latest add @shadcnblocks/hero253 --overwrite
```

If a registry call fails with a missing-env-var or auth error, the fix is to
populate the key from the secret store — not to abandon the registry and
hand-roll the component. See the `sops-secret-access` skill for the encrypted-
config side of this and the expected secret-handling pattern.

Graduate stable pieces from the screen into the repo's shared UI package (name
is per-repo; see [ADR-0013](../../docs/adr/0013-shared-ui-is-its-own-package.md)).

## Relationship to other skills

- `sops-secret-access` — how to _access_ the encrypted registry config and keys.
  This skill is about _preferring registry components_; that one is about the
  plumbing to reach a private registry.
- `ui-ux-pro-max` — design intelligence (styles, palettes, layout, a11y). Use it
  to decide _what_ good UI looks like; use this skill to _source_ the components
  that realize it. They compose: pick the aesthetic with `ui-ux-pro-max`, then
  search the registry for blocks that match.
- `vercel-react-best-practices` — performance patterns for the React you write
  around and inside installed blocks.
