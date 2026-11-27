---
name: scaffold
description: "The file list for a new project skeleton, in order. Use for the scaffold thread of operator step 4."
---

# Scaffold

**Stack for new projects** (moved here from `CLAUDE.md`, S11a): an existing repo's choices win. New: TypeScript, Node 24, npm; Nuxt 4 or Vue 3 + Vite, Pinia, Tailwind v4, `@nuxtjs/i18n` (de, en); D1/SQLite or Postgres with prepared statements; Vitest, Playwright, `vue-tsc`. Deploys: `publish`. Know-how by domain: `docs/MAP.md` (Expertise); story games with renders: `docs/game-pipeline.md` first.

One thread, branch `scaffold`, one PR. Read `PLAN.md` first: it names the framework, whether the app
has D1, logins, payments and which languages. Skip a line only when PLAN.md says the app doesn't
need it, and say so in the PR. Follow the order; each step commits on its own.

1. `.node-version`: `24`.
2. `package.json`: `type: module`, `engines.node >=24`, scripts `dev`, `lint`, `typecheck`,
   `test`, `build`, `check` (= lint + typecheck + unit tests, no browser tests), and `verify` (= lint + typecheck + test +
   build). `verify` starts with a secret scan, script `secrets` = `! git grep -nIE
   '(sk|rk)_live_[A-Za-z0-9]|whsec_[A-Za-z0-9]{16}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{30}'
   -- . ':(exclude)*.md' ':(exclude)package-lock.json'` (cloud threads have no secret hook, so CI is
   the net). D1 apps add `deploy` and `deploy:preview` (step 6).
3. Framework per PLAN.md: Nuxt 4 (SSR or static) or Vue 3 + Vite (SPA/PWA). Plus Tailwind v4,
   Pinia, `@nuxtjs/i18n` with `de` (default) and `en`, Vitest, `vue-tsc`, and Playwright when
   PLAN.md has e2e criteria. UI text goes through i18n from the first page (a literal `@`, `{`,
   `}` or `|` in a locale string is written `{'@'}` etc.).
4. `app/` skeleton: one home page, the layout, the two legal routes (step 8), a health route
   `/api/config` returning the build `commit` (`WORKERS_CI_COMMIT_SHA`) for the live check.
5. `design/DESIGN.md` and `design/refs/` from the design team's pick (empty folder with a
   `.gitkeep` until the design thread delivers), with its `## Bar` section filled
   (`operator/roles/designer.md`, UI/UX bar); no UI beyond the skeleton before that.
6. `wrangler.jsonc` per the `publish` skill: `name`, `workers_dev` and `preview_urls` true, a
   `previews` block (even empty), D1 `DB` plus `<name>-preview` with committed ids when PLAN.md
   has data. D1 scripts: `deploy` = migrate live, `wrangler deploy`, migrate preview;
   `deploy:preview` = migrate preview, `wrangler preview`. The Workers Builds commands (Build
   `npm run check && npm run build`, Deploy, Preview) and the live check by commit go into brief
   (b) exactly as `publish` writes them.
7. Repo setup from `onboard-project`: `CLAUDE.md` (under 60 lines), `.claude/settings.json`,
   `.claude/skills/verify/SKILL.md`, and `.github/workflows/ci.yml` running only `npm run
   verify` (no keys in GitHub). The loop's inbox from the operator's `templates/loop/`:
   `scripts/loop.mjs` and `.github/workflows/loop.yml` (its only key, the read-only report
   token, lives in the `loop` GitHub environment); the app's error and feedback tables and the
   owner report come with the first slice that has users (`docs/LOOP.md`).
8. Impressum and Datenschutz pages per the `legal` skill, in German and English, linked from the
   footer of every page; texts with placeholders for what only yskills can supply.
9. `PLAN.md`, `features.json`, `PROGRESS.md` from the operator's `templates/` (PLAN.md and
   features.json already exist from step 3 of `operator`; copy the rest).
10. `.env.example` with every variable the code reads and no values (`VITE_*` and
    `NUXT_PUBLIC_*` are public); `.gitignore` with `node_modules`, `.output`, `.nuxt`, `dist`,
    `.env*` (not `.env.example`), `.dev.vars`, `.wrangler`, `.shots/`.
11. `README.md`, ten lines at most: what it is, `npm install`, `npm run dev`, `npm run verify`,
    where it deploys.
12. Per-project plugins via `toolbox` (`claude plugin install <id> --scope project`), only what
    PLAN.md's picks name.

## PR checklist

- [ ] `npm run verify` passes locally; CI is green.
- [ ] Every step above is done or named as skipped with the PLAN.md line that allows it.
- [ ] No secret, no real `.env`, no value in `.env.example`.
- [ ] Phone (390px) and desktop (1440px) screenshots of the home page in the PR.

Its gate is CI only (`gate.md`); don't merge, the gate does.
