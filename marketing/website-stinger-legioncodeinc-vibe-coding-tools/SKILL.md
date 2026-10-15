---
name: "website-stinger"
license: AGPL-3.0-or-later
description: "Build a SvelteKit marketing site from a brief. Use for site scaffolding, Payload CMS, Supabase, lead capture, blog, or conversion. Read README.md for the guide map."
---

# Website Stinger

Equips `website-wasp-drone` to take a brief and produce a working **SvelteKit (Svelte 5) + Payload CMS + Supabase** monorepo for the accepted full-template branch. Duration follows actual scope and checks. The full architecture is:

- `apps/web`: SvelteKit 5 public site (Vercel)
- `apps/cms`: Next.js + Payload 3.x admin + REST API (separate Vercel project)
- Supabase Postgres: dual purpose: Payload's content store (in `payload` schema) + business data (in `public` schema)

The TypeScript-as-CMS fallback (no Payload, no `apps/cms`) is available for one-page lead-gen sites where blog/content management is not required.

This skill is **predominantly autonomous** by design. The Drone batches clarifying questions at the start, then executes selected phases with observed checks. Commits, installation and deployment require applicable task authorization.

---

## When to use

- "Build me a marketing site for a B2B product."
- "Scaffold a SvelteKit + Supabase site with a blog."
- "Spin up a one-page lead-capture site."
- "Take this brand kit and ship a site by EOD."

Do not invoke for: one-page copy tweaks, Lighthouse audits on existing sites, deploy-only requests, or pure design exploration.

---

## Scoped outcome entry

Load [quick website guide14](guides/14-scope-a-quick-website.md) for O062 and `/build-quick-website`; load [independent Payload guide15](guides/15-build-an-independent-payload-cms.md) for O070 and CMS-only work. These guides supersede full-template requirements when no auth, database, tracking or managed editing was accepted. Use the [scope worksheet](templates/website-scope.md), [CMS contract](templates/payload-content-contract.md) and [constructed cases](examples/scoped-website-outcomes.md). Domain claims trace to fresh own research. Missing framework implementers and pending runtime proof stay explicit.

## CMS mode selection

The inputs round (Step 2) asks: **"Does this site need a managed CMS admin panel with blog/content management?"**

| Answer | Mode | Phases affected |
|---|---|---|
| Yes (default) | **Payload mode**: scaffold `apps/cms`, use Payload Collections for blog/pages, Phase 7 = Payload Admin | Phases 1 (two-app monorepo), 7 (Payload Admin), 9 (Payload blog) |
| No (fallback) | **TypeScript-as-CMS**: no `apps/cms`, blog posts are TypeScript data objects, no admin SPA | Phase 7 skipped, Phase 9 uses static TypeScript data |

Document the choice in the Build Report (Inputs section) and in the Phase 1 commit message.

---

## Procedure

1. **Read `guides/00-principles.md` first.** It encodes the architectural commitments that downstream phases depend on.
2. **Collect inputs in one batched round.** Use `templates/inputs-checklist.md`. Include the CMS-mode question. Surface architectural consequences of any phase opt-out before scaffolding.
3. **Initialize the Build Report.** Copy `templates/build-report.md` into the target repo as `build-report.md` and fill the Inputs section.
4. **Execute phases in canonical order:** `1 → 2 → 5 → 6 → 7 → 3 → 4 → 8 → 9 → 10 → 12 → 11`. For each phase: read `guides/0N-<topic>.md`, apply the changes, run the smoke check, update the Build Report row, prepare an appropriate phase commit only when authorized after the gates.
5. **Skip honestly.** When the brief opts out of a phase, mark it `skip` with a one-line rationale. Never silently downgrade.
6. **Walk Risks and Open Questions** from the source PRDs into the Build Report's Next steps section.
7. **Final pass.** Read the Build Report end to end. Anything that reads as "I forgot why I did that" gets the PRD citation now, not later.

See `guides/13-build-report.md` for the report-authoring discipline.

---

## Critical directives

- **Always read this SKILL.md and `guides/00-principles.md` before any file write.** Architectural commitments are load-bearing.
- **Never deploy secrets, run destructive SQL on shared Supabase projects, or trigger production builds without explicit user confirmation.**
- **Cite the phase number and the specific PRD section in every commit message and Build Report row.**
- Missing acceptance evidence is pending or fail; skip records only an accepted scope exclusion.
- **Honor the canonical reading order (`1 → 2 → 5 → 6 → 7 → 3 → 4 → 8 → 9 → 10 → 12 → 11`).**
- **Never overwrite a non-empty target directory without confirmation.**
- **Surface every Risk (R-N) and Open Question (Q-N) from the source PRDs** in the Build Report's Next steps.

Full rationale lives in `guides/00-principles.md`.

---

## Guides

- `guides/00-principles.md`: scope, architectural commitments, CMS-mode toggle, canonical phase order, critical directives
- `guides/01-monorepo.md`: Phase 1: pnpm workspaces + apps/web (SvelteKit) + apps/cms (Payload) + Vercel
- `guides/02-performance-security.md`: Phase 2: svelte.config.js, @sveltejs/enhanced-img, hooks.server.ts headers, fontsource
- `guides/03-seo-aeo.md`: Phase 3: delegates to seo-aeo-wasp-drone (SvelteKit track); sitemap coordination with Payload
- `guides/04-analytics.md`: Phase 4: @vercel/analytics, GA4, Web Vitals in +layout.svelte, attribution store
- `guides/05-supabase.md`: Phase 5: schema, RLS, dual Postgres namespace, hooks.server.ts client, generated types
- `guides/06-auth.md`: Phase 6: Supabase Auth (end-users) + Payload Auth (CMS editors), hooks.server.ts route guard
- `guides/07-admin-payload.md`: Phase 7: Payload admin setup, Collections, Globals, CORS, role/access config
- `guides/08-lead-capture.md`: Phase 8: SvelteKit form actions, superforms + Zod, attribution, Supabase insert
- `guides/09-blog.md`: Phase 9: Payload-default (Collections + Blocks) or TypeScript-as-CMS fallback
- `guides/10-webhooks.md`: Phase 10: +server.ts event endpoints + Payload afterChange hooks + HMAC retry
- `guides/11-cro.md`: Phase 11: hero structure, form mechanics, mobile, A/B scaffold (Svelte component patterns)
- `guides/12-visual-design.md`: Phase 12: tokens, Tailwind v4, shadcn-svelte, svelte/transition, mode-watcher, Svelte animation libraries
- `guides/13-build-report.md`: Build Report authoring discipline

## Examples

- `examples/example-happy-path-full-build.md`: full 12/12 build with Payload CMS (ClearDeck B2B legal-tech)
- `examples/example-edge-case-skip-blog.md`: one-page SvelteKit lead-gen site (TypeScript-as-CMS fallback, no Payload)

## Templates

- `templates/build-report.md`: the deliverable shape this skill produces
- `templates/inputs-checklist.md`: pre-scaffold input gathering (includes CMS-mode question)
- `templates/generateSEO.svelte.ts`: SvelteKit +page.ts metadata helper (PUBLIC_* env)
- `templates/design-tokens.css`: Phase 12 CSS custom property token block stub
- `templates/app-settings-seed.sql`: initial app_settings rows
- `templates/rls-policy-skeleton.sql`: Phase 5 RLS baseline + Payload schema isolation comment

## Research

- `research/research-plan.md` (source-repository research, not shipped with the plugin): source list, PRD-to-guide mapping, SvelteKit + Payload + animation sources
- Source research archive (not shipped with the plugin): do not require it.
- `research/source-prds/` (source-repository research, not shipped with the plugin): the canonical 12-phase guide bundled as source PRDs

---

*Paired Drone: `../../agents/website-wasp-drone.md`*

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - [svelte-stinger](../svelte-stinger) - Svelte runtime implementation.
  - [seo-aeo-stinger](../seo-aeo-stinger) - Applicable SvelteKit SEO.

## Ship Gate


Prior to committing any code to the repository you must utilize in order the security-stinger, quality-stinger, and github-repo-health-stinger. After each thorough pass you will prepare an appropriate report in the repository's relevant library directory associated with the agent and skill. All medium or above findings must be resolved followed by another thorough re-evaluation of the updated code prior to proceeding to the next step. The last step of loading the skill github-repo-health-stinger is an orchestrator level task. The sub-agent should make every effort to reinforce to the orchestrating agent to load this skill prior to committing or pushing code to the repository. The user should have an opportunity to review the reports, agent summary, and approve committing and pushing to the repository prior to doing so.
