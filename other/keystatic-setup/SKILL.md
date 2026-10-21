---
name: keystatic-setup
description: >
  Add Keystatic — a git-based CMS from the Keystone team — to a new-website Astro
  scaffold, so a non-technical person can edit content through a UI while the data
  still rests as Markdown in the GitHub repo. Wires LOCAL storage mode (edit in the
  dev server, commit/push); documents the GitHub cloud-mode upgrade for browser
  editing. Run ONCE, at scaffold time, when new-website Q3 = "a non-technical person
  edits content". Trigger phrases: "add a CMS", "Keystatic", "non-technical editor",
  "client edits content", "git-based CMS".
---

# Keystatic setup (scaffold-time, opt-in)

Adds an optional editor UI to the `new-website` Astro overlay. **Opt-in:** the default
scaffold is CMS-free (Markdown-in-git is the workflow). Run this only when new-website
§1 Q3 says a non-technical person edits after launch. Keystatic is git-based — it writes
Markdown/Markdoc into the repo, so "data rests in your GitHub" stays literally true and
the site stays free + static. (Keystatic is built by Thinkmill, the Keystone team.)

Prereq: the site uses **Content Collections** (new-website Q1) — Keystatic edits the
files those collections read. If the site is flat pages only, add a collection first.

## Local mode (what this skill wires up)

Edit via the dev server; Keystatic commits nothing on its own — you review and `git
commit`/`push`, Cloudflare deploys. The admin runs in `astro dev` only; the production
build stays fully static (no adapter, no auth, no server). Steps applied to the project:

1. **Install** (per the official Astro guide — verify current commands at keystatic.com):
   ```bash
   npm install @keystatic/core @keystatic/astro
   npx astro add react markdoc          # admin UI (React) + content format (Markdoc)
   ```
2. **`astro.config.mjs`** — add the integrations. The `keystatic()` integration injects a
   **server-rendered** `/keystatic` admin route, so adding it unconditionally fails the static
   build with `[NoAdapterInstalled]` (verified). For local mode, **gate it to `astro dev`** —
   the admin runs locally, production stays fully static, no adapter needed:
   ```js
   import react from '@astrojs/react';
   import markdoc from '@astrojs/markdoc';
   import keystatic from '@keystatic/astro';

   const isDev = process.argv.includes('dev');   // keystatic admin = dev-only

   export default defineConfig({
     // …existing site/trailingSlash/build…
     integrations: [/* existing */ react(), markdoc(), ...(isDev ? [keystatic()] : [])],
     output: 'static',
   });
   ```
   The `keystatic()` integration **auto-injects** the `/keystatic` admin route + its API —
   you do NOT hand-write route files. (Verified deps on Astro 7 — each checked via
   `npm view <pkg>`, not assumed: `@astrojs/markdoc@^2` (peer `astro: ^7.0.0` — the `^1`
   line stays capped at `astro: ^6.0.0` and will NOT install against an Astro 7 site);
   `@keystatic/astro@^5` (peer range explicitly covers `astro: 2 || 3 || 4 || 5 || 6 || 7`);
   `@astrojs/react@^6`, NOT `^5` — `^5` declares no `astro` peer so it *installs* against
   Astro 7, but its own `vite` dependency is `^7.3.2` against astro 7's `vite@^8.0.13`,
   producing a duplicate non-deduped vite tree and real build-time deprecation warnings;
   `^6.0.1`'s `vite` dependency (`^8.0.13`) matches astro 7 exactly, confirmed via
   `npm view @astrojs/react@6 dependencies.vite`; `@keystatic/core@^0.5` declares no `astro`
   peer and has no such transitive mismatch either, so it's fine as-is; `react@19`.
   `npx astro add react markdoc` (the Install step above) resolves the right majors
   automatically — this parenthetical is for anyone tempted to hand-pin an older note.)
3. **`keystatic.config.ts`** at the repo root — one collection per repeating content type,
   each `path` pointing into `src/content/`:
   ```ts
   import { config, fields, collection } from '@keystatic/core';
   export default config({
     storage: { kind: 'local' },
     collections: {
       posts: collection({
         label: 'Posts',
         slugField: 'title',
         path: 'src/content/posts/*',
         format: { contentField: 'content' },
         schema: {
           title: fields.slug({ name: { label: 'Title' } }),
           content: fields.markdoc({ label: 'Content' }),
         },
       }),
     },
   });
   ```
   **The `label:` strings ARE the CMS UI the owner sees daily** — write them in the
   owner's language, not English (a German owner gets `label: 'Beiträge'` / `'Titel'` /
   `'Inhalt'`). For a multilingual site built with `astro-i18n-setup`: per-locale
   entry dirs → mirror them as separate collections (one per locale directory — a single
   `path` glob can't span locale subdirectories, and a mis-scoped path leaves the other
   locale uneditable); a `locale` frontmatter field → keep ONE collection and add that
   field to the Keystatic schema.
   Mirror the site's real Content Collections (the same `path`/schema the Astro
   `src/content.config.ts` reads), so the CMS and the site agree on shape.
4. **Allowlist** — `Bash(npx keystatic:*)` + `WebFetch(domain:keystatic.com)` already ship
   in the template `settings.json`; just confirm they're present in the project's copy
   (don't re-add — avoid duplicates).
5. **README** — document the workflow: `npm run dev` → open `/keystatic` → edit → the files
   under `src/content/` change → `git commit && git push` → Cloudflare deploys.

## GitHub cloud mode (documented upgrade — not wired by default)

Local mode needs the editor to run a dev server. For a truly non-technical editor who
should edit in the browser, upgrade to **GitHub mode** (commits straight to the repo from
a hosted admin):
- `keystatic.config.ts`: `storage: { kind: 'github', repo: 'owner/name' }`.
- Connect Keystatic to GitHub (Keystatic Cloud, or your own GitHub App) for auth.
- The admin's auth/API routes now need **on-demand rendering** → add a server adapter
  (`@astrojs/cloudflare`) and switch the relevant routes to server output; add the
  `KEYSTATIC_GITHUB_*` env vars + OAuth callback. Follow the current keystatic.com docs.
- Trade-off: browser editing for non-technical users, at the cost of an adapter + a
  GitHub App + secrets to manage. Recommend only when local mode is genuinely too technical.

## Caveats
- Keystatic's default content format is **Markdoc** (`.mdoc`), not plain `.md` — pick
  `fields.markdoc`/`fields.mdx`/`fields.text` to match what the site renders.
- Local-mode admin is dev-only; it is not part of the deployed static site.
- Adds React + Markdoc deps — only worth it when someone actually edits via UI.

## Wiring (done once in the suite)
- `new-website/SKILL.md` §1 Q3 → "if non-technical editor: run `keystatic-setup`"; add
  the skill to the §3 bundled-skills copy list (conditional — only for CMS sites).
- `references/WEBSITE_ARCHITECTURE.md` Part 4 (Keystatic) → point at this skill.

## Verify (scaffold a throwaway CMS site in /tmp)
```
npm install && npm run build      # static prod build succeeds (keystatic gated off in build)
npm run dev                        # open http://localhost:4321/keystatic → admin loads (200)
# create an entry in the UI → a Markdown/Markdoc file appears under src/content/<collection>/
npm test                           # suite stays green
```
