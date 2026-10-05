---
name: pre-deploy
description: Run the full local verify (lint, library and package builds with the publish lint, story tests, Storybook build, website lint + build, the built-HTML validators, and the served-site checks) and confirm the site is safe to push to Vercel. Use when asked whether changes are ready to push, deploy, or ship, or for a pre-deploy check.
icon: rocket_launch
displayDescription: "Runs the same checks as CI before a push to Vercel: lint, the library type-check, the publishable npm package build, every Storybook story as a render, interaction, *and* accessibility test (Vitest + headless Chromium + axe, with story play functions asserting behavior), the Storybook build, the website lint + build (Next.js), the validators that read the built HTML, and the served-site checks: a hydration smoke in a real browser and a page-level axe pass in both themes. Knows the npm-workspace layout and watches for SSR-unsafe code, portal regressions, and static generation failures."
invoke: ["is this ready to push?","run the build","pre-deploy check","check before I push"]
---

# pre-deploy

Run the full local verify and confirm the site is safe to push to Vercel.

## When invoked

Use this skill when asked to check if changes are ready to push, deploy, or ship — phrases like "is this ready to push?", "run the build", "pre-deploy check", "check before I push".

## Instructions

1. **Run the full verify** from the repo root:
   ```
   npm run verify
   ```
   This is the single source of truth for local checks and mirrors the CI jobs in `.github/workflows/ci.yml`, minus the CI-only checks CLAUDE.md's **CI & Local Verify** section records as deliberate exceptions (its list is authoritative) — so a green verify can still meet a red CI on news from outside, like a fresh advisory. It runs, in order: ESLint, the library type-check, the publishable package build (`build:lib` — vite lib mode + d.ts into `dist/`), the story tests (every Storybook story rendered in headless Chromium, **with axe asserting WCAG 2.1 AA on each one** and any story `play` function asserting behavior — an accessibility violation or a failed interaction assertion fails the suite exactly like a render error), the Storybook build, the website lint, the website build, and then the checks that need the finished build rather than source — the tail of the `verify` entry in the root `package.json` is the authoritative list of these, same as the registry chain below. Some read the prerendered HTML (a space lost between JSX and render, say, or an href pointing at a route that no longer exists); the rest serve the build and load it in a real browser — hydration must succeed and every checked page must be visible with content, because a build can be green while the rendered site is blank (the hydration smoke's doc block records the outage that proved it), and the served pages must pass axe in both themes at the same rule set Storybook enforces. That is why all of them follow the website build instead of riding the registry chain. (The library half gains one post-build check of its own: `validate-package-publish.mjs`, publint and arethetypeswrong over `dist/` after `build:lib`.) The registry validators run via the builds' `prebuild` hooks, so a registry-drift failure surfaces before the compiles even start. The `validate-registry` entry in the root `package.json` is the authoritative list of what runs; read the failing script's own doc block for what it guards, because the failures do not share a family resemblance — one means an unregistered component, another that a prose edit removed a fact the chat eval depends on (`validate-chat-coverage.mjs`), another that the ambient background references a colour token that no longer exists (`validate-shader-background.mjs`). This list used to be enumerated here and went stale twice; a pointer cannot. The prebuild also regenerates the derived surfaces owned by the `validate-registry` chain (the generator scripts at the front of its entry in the root `package.json` are the authoritative list) — if any come out modified, commit them with the work that changed their source.

   Note: the repo is an npm workspace — one `npm install` at the root covers the website too, and the website resolves `@robr0/design-system` through a symlink to the repo root. The website build is a plain `next build`; there is no separate install step inside `website/`.

2. **Check the output of each step for:**

   **Lint failures:**
   - Any ESLint `error` lines (warnings don't fail the run, but mention them)

   **TypeScript errors:**
   - Any `error TS` lines
   - Type mismatches, missing props, invalid imports

   **Next.js-specific issues:**
   - `"use client"` missing on components that use browser APIs (`window`, `document`, `localStorage`, `useEffect`, `useState`, etc.)
   - SSR-unsafe code running outside client guards — particularly watch `website/src/app/layout.tsx` (the inline `themeScript`)
   - Portal/modal components that reference `document` at module or render scope — these have caused past static-build failures (AlertDialog and Toast both needed fixes; watch for regressions if portal-based components change)
   - Pages that fail static generation (look for `Error occurred prerendering page`)

   **General failures:**
   - Any non-zero exit code
   - `Build failed` or `Compiled with errors`

3. **Report result:**

   If everything passes:
   > Verify passed (lint + story tests + library, package, Storybook, and website builds, plus the publish lint, the built-HTML validators, and the served-site checks). Safe to push.

   **Visual regressions are the one thing `verify` cannot see.** There is no automated visual gate in this repo: Chromatic snapshotted Storybook, and Storybook went to the design system's repo with the library. If the change touched layout or styling, offer a `visual-review` pass instead.

   If any step fails, show:
   - Which step failed (lint, component library, story tests, Storybook, website lint, website build, or one of the checks that run after it — the built-HTML validators or the served-site checks; the tail of the `verify` entry in the root `package.json` is the authoritative list)
   - If the **served-site axe pass** failed, say which rule and on which page. An axe failure names the rule (e.g. `button-name`, `nested-interactive`) and the offending markup; contrast is deliberately excluded from the gate.
   - The exact error message(s)
   - File path and line number if available
   - A brief diagnosis of likely cause

4. **Do not push** — this skill only checks and reports. Pushing is Rob's decision.
