---
name: om-prepare-test-env
description: Repo-local extension of om-prepare-test-env - how this app boots for QA (local D1, throwaway .dev.vars, the seed, the 3011-3020 port pool) and what the committed entrypoints encode.
---

# om-prepare-test-env (money-tracker.online)

This file extends the shared `om-prepare-test-env` skill installed at
`.claude/skills/om-prepare-test-env/SKILL.md`. The generated entrypoints are **committed**:
`.ai/scripts/test-env-up.sh` and `.ai/scripts/test-env-down.sh`. Run them. Regenerate only with
`--regenerate`, and keep every fact below when you do.

## How this app runs

- Mode `dev`: `pnpm exec vite dev --port <port> --strictPort --host 127.0.0.1`. The Worker runs in
  workerd through `@cloudflare/vite-plugin` against local D1, KV and R2 under `.wrangler/state/`.
  No Docker, no external service.
- Preparation chain, in order: `HUSKY=0 pnpm install --frozen-lockfile --prefer-offline`,
  `pnpm generate-routes`, `pnpm db:migrate:local`. Migrations are idempotent and run on every boot.
  `HUSKY=0` keeps `pnpm install` from rewriting `core.hooksPath` in the git config the worktrees
  share.
- Port: the first free port in **3011-3020**. 3010 belongs to the developer's own `pnpm dev`
  (`vite.config.ts` binds it with `strictPort`), and `playwright.config.ts` refuses a base URL
  outside 3010-3020.
- Host `127.0.0.1`, never `localhost`: the server binds v4 only, and Node's fetch in the seed
  resolves `localhost` differently from curl.
- `.dev.vars`: the script writes a throwaway file (`BETTER_AUTH_SECRET`, `APP_URL`, and the fixed `UNSUBSCRIBE_TOKEN_SECRET` that `e2e/unsubscribe.spec.ts` signs with) whose first
  line is a marker. A `.dev.vars` without the marker was written by a person and is never
  overwritten: the script keeps it and warns when its `APP_URL` does not match the chosen port.
  Billing QA needs Polar **sandbox** credentials in that human-written file, all seven or none
  (`POLAR_ACCESS_TOKEN`, `POLAR_WEBHOOK_SECRET`, `POLAR_SERVER` in `.dev.vars`; the four
  `VITE_POLAR_PRODUCT_*` in `.env.local`). The script never handles them.
- Seed: `node scripts/seed/seed.mjs --url <baseUrl>` creates the demo owner through the real
  sign-up endpoint and writes the fixture; `node scripts/seed/verify.mjs` audits it. Demo identity
  `demo@money-tracker.online`; the password is the `TEST_OWNER_PASSWORD` reference in
  `.ai/qa/test-env.env`.
- Readiness: `GET /` answers within 120 s on a cold boot. The deep probe is
  `POST /api/auth/sign-in/email` with the demo credentials; the rate limiter allows ten attempts a
  minute, so probe once.
- Freshness: `vite dev` hot-reloads `src/**`, so only `drizzle/`, `package.json` and
  `pnpm-lock.yaml` newer than the descriptor make a running environment stale.

## Rules

- Never boot on 3010, and never stop a server the descriptor did not start.
- The agent never reads `.dev.vars`, `.env.local` or `.ai/qa/test-env.env`.
