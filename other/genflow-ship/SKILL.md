---
name: genflow-ship
description: The ship routine for GenFlow Pro — merge a tested branch into main and put it live on genflow-pro.vercel.app safely. Start check, merge --no-ff, tests/lint/build, Derek still BCC'd, no secret files tracked, push, confirm the GitHub-built production deployment, a no-email production smoke test through the real app as QA with the safety guard in prod-readonly mode, rollback by promoting the previous deployment, and a plain-English summary. Use ONLY when the owner explicitly asks to ship / merge to main / deploy to production.
---

# GenFlow Pro — ship routine

Ship only when the owner has said so in this conversation. Everything in the
`genflow-qa` skill (context, rules, safety guard) still applies; this skill
adds the production steps. Production is built by Vercel **from GitHub main**:
shipping = pushing a merge commit to main. Never `vercel deploy --prod`, and
never `vercel deploy` from the repo folder (`.vercelignore` is only a
backstop).

Write progress to `.qa-scratch/ship-progress.md` as you go, and the result to
`.qa-scratch/SHIP-SUMMARY.md` (untracked). Label every claim VERIFIED (how) or
NOT VERIFIED.

## 1. Start check (read-only, before touching git)
- `git fetch origin`; record SHAs: local `main`, `origin/main`, the branch to
  ship. main must equal origin/main, and the branch must contain main
  (`git merge-base --is-ancestor main <branch>`), or stop and report.
- Record the current production deployment — this is the **rollback target**:
  from a folder that is NOT the repo (a scratch dir with only
  `.vercel/project.json` copied in), `vercel ls --prod` / `vercel inspect
  genflow-pro.vercel.app` → note its URL (`genflow-xxxxxxxxx-…vercel.app`),
  `dpl_` id and the commit it was built from. It must match origin/main.
- Supabase MCP, plain SELECTs only: `select count(*) from public.staff` = 5,
  and the table counts match `.qa-scratch/baseline-counts.json`. Real rows
  added since: confirm none is QA-AUDIT, then update the baseline.
- Any migrations the branch needs: confirm with the owner they are applied
  (read-only SQL check of the column/index), or that the code has a safe
  fallback without them.
- `git status`: only the known untracked files (e.g. `priced_parts_update.csv`,
  `qb-verify-step2.mjs`). Never commit those.

## 2. Merge
- `git checkout main && git merge --no-ff <branch> -m "Ship <what>: <one line>"`.
- Review the merge: `git diff --stat origin/main..main`.
  - **No new files under `api/`** (Vercel Hobby function limit):
    `git diff --name-status origin/main..main -- api | grep '^A' | grep -v '^A\s*api/_lib/'` must be empty.

## 3. Tests, lint, build (all on the merged main)
- `npx vitest run` — all pass.
- `npx eslint . --quiet` — 0 errors.
- `npm run build` — succeeds.
- `node --test scripts/qa/safe-actions.unit.mjs` — guard self-test passes.
If anything fails: `git reset --hard origin/main` (the merge is local only) and
report. Do not fix on main.

## 4. Safety checks before the push
- **Derek still BCC'd:** `grep -n "BCC_ADDRESSES" api/_lib/sendEmail.js` must
  show `['contact@genshieldservice.com', 'derek.j.sainz@gmail.com']`. The
  Derek-removal patch exists only in Preview copies — it must never reach
  main.
- **No secret files tracked:**
  `git ls-files | grep -E '^(\.qa-scratch/|\.vercel/|\.env)|\.pem$|\.key$|session.*\.json$|\.qa-password|\.bypass-secret'`
  must be empty, and `git ls-files .claude` must list only `.claude/skills/…`.
- **No key material in code:** `git grep -nE 'sk_live_|sk_test_|rk_live_|whsec_|service_role.*ey[A-Za-z0-9]|re_[A-Za-z0-9]{20,}' -- . ':!*.test.*'`
  must be empty (publishable `pk_` keys come from env, not code).
- `.vercelignore` still present and its test passes (part of vitest).

## 5. Push and confirm the GitHub-built deployment
- `git push origin main`.
- Wait for Vercel's GitHub build (from the scratch folder:
  `vercel ls --prod`, or the API `GET /v6/deployments?projectId=<id>&target=production&limit=3`
  using the CLI's auth). VERIFY: the newest production deployment is
  **Ready**, its `meta.githubCommitSha` equals the merge SHA, and
  `vercel inspect genflow-pro.vercel.app` shows that deployment.
- Record the new `dpl_` id + URL.

## 6. Production smoke test — no email, QA only, guard in prod-readonly mode
- Production is refused unless the script is started with an explicit
  `--prod-smoke` flag (tracked guard, `scripts/qa/safe-actions.mjs`): e.g.
  `node s10.mjs <phase> --base https://genflow-pro.vercel.app --prod-smoke`.
  Never give a smoke script a default target; pass `--base` and the URL as two
  arguments (Run 9: a quoted `"--base <url>"` silently fell back to production).
  With the flag the guard allows only `create`, `save`, `delete`, `cancel`,
  `complete` (emails blocked) — never `send`, `charge`, `payment`, `approve`.
Playwright WebKit, iPhone 15 standalone profile, signed in as QA, on
`https://genflow-pro.vercel.app`.
- Block in the browser context: every email route (`/api/send-email`,
  `/api/send-job-summary`), every card route (`/api/create-payment-intent`,
  `/api/update-payment-intent`), every cron route (`/api/check-renewals`,
  `/api/generate-report`, `/api/generate-parts-usage-report`,
  `/api/register-apple-pay-domain`, `/api/stripe-webhook`), and intercept
  `stripedashboard://` and `tel:`. Set `page._sendsBlocked = true` only when
  the email routes really are blocked.
- Every write tap goes through
  `guardedTap(page, locator, { kind, record, item: 'ship', mode: 'prod-readonly' })`.
  Call `attachDialogGuard(page)` on every page first (never auto-accept native dialogs).
  prod-readonly allows only the production host and only QA-AUDIT records,
  refuses `send`, `charge` and `payment` outright, and refuses any write
  unless the email routes are blocked. If it throws: stop, log, never work
  around it.
- Steps (screenshot each, `QA_RUN_DIR=.qa-scratch/ship`):
  a. Open Dashboard, Jobs, Schedule, Customers, Invoices, Catalog, Finance,
     Settings: no blank screens, 0 app console errors.
  b. `POST /api/send-email` and `/api/create-payment-intent` with no token →
     401 (and with the QA token but an empty body → 400, proving the staff
     check passes without sending or charging).
  c. Create a `QA-AUDIT-SMOKE …` customer with NO email → New Job → Create &
     Skip Notification → walk what shipped (e.g. dispatch → arrived →
     signature → Complete as unpaid; "No email on file" must show).
     Log every record to `.qa-scratch/ship/created.jsonl` as it's created.
  d. No money in production: never record a payment (not even cash) and
     never charge — the guard refuses `payment`/`charge`, and labelling such
     a tap as another kind is working around the guard. Payment flows are
     proven on a Preview (Stripe test mode) before shipping. Real
     parts/records: view only.
  e. Delete all smoke test data through the app (cancel/delete job, delete
     customer). Leftovers the UI can't remove: REST delete, dry-run first,
     logged.
  f. Read-only SQL: 0 QA-AUDIT rows in every table, counts equal the
     baseline, any part touched has its original stock.

## 7. Rollback (if the smoke test fails or the owner asks)
- Promote the previous production deployment (no rebuild): from the scratch
  folder, `vercel promote <rollback-target-url>` (or Vercel → genflow-pro →
  Deployments → that deployment → ⋯ → Promote to Production). VERIFY
  genflow-pro.vercel.app now serves it (`vercel inspect genflow-pro.vercel.app`).
- main still holds the shipped code, so the next push would ship it again:
  revert the merge (`git revert -m 1 <merge-sha>`) before any further push —
  ask the owner first.
- Data: say whether any rows the new code wrote need attention (usually
  none).

## 8. Summary (`.qa-scratch/SHIP-SUMMARY.md`, plain English, short)
- Merge commit, new production deployment (`dpl_` id, URL, built from which
  GitHub SHA), rollback target — each VERIFIED (how).
- Start check, tests/lint/build counts, Derek BCC, no secret files.
- Smoke test table: step → PASS/FAIL with screenshot path.
- Cleanup table: counts vs baseline, QA-AUDIT rows = 0, emails 0, charges 0.
- Exact rollback steps, the owner's phone-check list, anything NOT VERIFIED.
