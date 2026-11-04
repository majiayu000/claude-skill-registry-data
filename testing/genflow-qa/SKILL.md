---
name: genflow-qa
description: How to test GenFlow Pro (the GenShield field service app) safely — the project context, the "use the real app like a tech" test method with the safety guard (scripts/qa/safe-actions.mjs), and the hard rules (no real data changes, read-only Supabase MCP, QA-AUDIT test data only, email limits, cleanup deadline). Use before building, testing or verifying anything in this repo, running Playwright against a Preview, or creating any test data.
---

# GenFlow Pro — QA context, test method and rules

The three sections below are the owner's own instructions, copied verbatim
from the Run 6 prompt. The only change: the safety guard now lives in the
repo at `scripts/qa/safe-actions.mjs` (tracked, never deployed — see
`.vercelignore`) instead of `.qa-scratch/lib/safe-actions.mjs`.

How to apply them in a new run:
- "run6" in paths means the current run's folder: use `.qa-scratch/<run>/`
  (untracked) and point the guard at it with `QA_RUN_DIR=.qa-scratch/<run>`
  (it then logs to `<run>/actions.log` and saves shots under `<run>/shots/`).
- The CONTEXT facts were true at Run 6. Re-check what is shipped
  (`git log main`, the production deployment) before relying on them.
- Staff check (since Run 6, B6): the API (`api/_lib/staffAuth.js`) and the
  app's sign-in gate both call the database's `public.is_staff()` with the
  user's own token. `public.staff` is the only list; `src/lib/allowedUsers.js`
  no longer exists.
- Guard self-test: `node --test scripts/qa/safe-actions.unit.mjs`.
- Usage: `import { guardedTap, checkHost, GuardError } from '<repo>/scripts/qa/safe-actions.mjs'`;
  `guardedTap(page, locator, { kind, record, item, label, recipient?, noEmail?, stripeAppIntercepted?, mode? })`.
  kinds: save, delete, cancel, complete, send, charge, approve, payment, create.
  `record` = the QA-AUDIT name exactly as visible on screen (page text or a
  form field's value). `mode: 'prod-readonly'` is only for the production
  smoke test in the genflow-ship skill.
- Native dialogs (Run 7): the app still uses window.confirm() for deletes
  and "remove the card surcharge?". NEVER auto-accept dialogs
  (no `page.on('dialog', d => d.accept())`). Call
  `attachDialogGuard(page)` (same module) right after creating each page:
  it dismisses and logs every dialog, unless the guarded tap that opened it
  passed `{ dialog: true }` and the dialog text names that tap's QA-AUDIT
  record (or matches `dialogMatch`, e.g. /credit card surcharge/).
  guardedTap refuses to run on a page without it. A trash icon tapped
  outside guardedTap therefore can't delete anything while the "Confirm
  before deleting" preference is on (the default) — never turn it off.

═══ CONTEXT (you are a fresh session) ═══
GenFlow Pro is the field service app for my generator company 
(2 techs, Jeremy and Alex, iPhones, installed as a home-screen web 
app). Production: genflow-pro.vercel.app, built from GitHub main.
- Every table is staff-only via public.staff + is_staff() (staff = 
  Jeremy, Alex, Derek, Sean, QA). New sign-ups are off. 
  /api/send-email and the payment routes require a staff login via 
  api/_lib/staffAuth.js.
- Shipped: Batches 1-3, then Run 4 (Service Summary + Check all + 
  feel Phases 0-1), if Run 5 Part 1 succeeded.
- Run 5 Parts 2-3 (empty-Service-Summary reminder, "Internal Notes" 
  label, feel Phase 2 scrolling) were built on branch feel/phase-2, 
  unmerged.
- QA login: .qa-scratch/qa-signin.mjs, password in 
  .qa-scratch/.qa-password. Vercel bypass secret: 
  .qa-scratch/.bypass-secret.
- There is NO direct DB connection. The Supabase MCP is the only DB 
  access.
- Vercel Hobby is at its function limit: do NOT add files under 
  /api. Put new server logic in api/_lib or behind an existing 
  route.
- Previews share the PRODUCTION database. Preview has Stripe TEST 
  keys; production has LIVE keys.
- Previews are built from a clean copy of tracked files (git 
  ls-files) plus the uncommitted Derek-BCC removal in 
  api/_lib/sendEmail.js, IN THE COPY ONLY. Never vercel deploy from 
  the repo folder. Never commit the Derek edit.
- Website repo: /Users/jwoke/Downloads/genshield-website (static 
  HTML, deploys to genshieldservice.com from GitHub).

═══ HOW YOU TEST: USE THE REAL APP LIKE A TECH ═══
Every feature is built, then proven by USING THE REAL APP the way 
Jeremy or Alex would: Playwright WebKit, iPhone 15 standalone 
profile (SE for layout), signed in as QA on the Preview, tapping 
through the actual screens.
- Create, edit, complete, cancel and delete ALL test data through 
  the app's own screens. Not REST, not SQL. REST/storage API is 
  allowed ONLY for (a) reading/checking results and (b) deleting 
  leftovers the UI can't remove (e.g. storage files). Log every 
  such call.
- Walk each feature END TO END as a real workflow (e.g. build a 
  quote > approve > schedule > dispatch > on site > signature > 
  collect > complete), not just the one screen that changed. Save a 
  screenshot at every step to .qa-scratch/run6/shots/<item>/.

SAFETY GUARD (build this first, use it for every write action):
Use scripts/qa/safe-actions.mjs. Every tap on a button that 
saves, deletes, cancels, completes, sends, charges, approves or 
records payment MUST go through it. Before the tap it must:
1. Assert the page hostname is the Preview, never 
   genflow-pro.vercel.app or any production alias. Otherwise 
   throw.
2. Assert the record on screen (customer/job/quote/invoice/part 
   name) starts with "QA-AUDIT". Otherwise throw.
3. For send buttons: assert the recipient shown is 
   jdalessio2777@gmail.com (or that no email will send). For 
   charge buttons: assert Stripe is test mode (pk_test_ in the 
   bundle) and only use test cards; "Charge via Stripe App" is 
   always intercepted, never opened.
4. Save a screenshot, then tap, then save a screenshot of the 
   result.
5. Append a line to .qa-scratch/run6/actions.log (time, URL, 
   record, button, result).
Unit-test the guard so it provably refuses a production URL and a 
non-QA-AUDIT record. If the guard throws during a run, STOP that 
flow, log it, and never work around the guard.

Other test-data rules:
- Every test customer is named "QA-AUDIT-<item> ..." with email 
  jdalessio2777@gmail.com (or no email when no send is needed). 
  Prefer Create & Skip Notification.
- Test parts and catalog items are QA-AUDIT ones only; real parts 
  may be searched and viewed, never added, edited or restocked.
- Real records may be viewed, never edited.
- Log every created record (type, id, name) to 
  .qa-scratch/run6/created.jsonl the moment it's created.

═══ RULES ═══
- Supabase MCP: READ-ONLY SELECTs only. Nothing that triggers an 
  approval pop-up; nobody is awake to click it.
- NO real data changes tonight at all.
- No schema/policy changes: write migrations to 
  .qa-scratch/fixes/ for my review and build everything else to 
  work without them (with a safe fallback).
- New tables: from 2026-10-30 Supabase no longer gives NEW tables in 
  "public" Data API grants automatically (existing tables keep 
  theirs). Any migration that CREATEs a table must, in the same 
  file: (1) enable RLS; (2) grant select/insert/update/delete 
  explicitly to authenticated and service_role; (3) add the 
  staff-only policy using (select public.is_staff()). NEVER grant 
  to anon by default (revoke all from anon), unless a public 
  website form genuinely needs insert; then grant only insert, 
  with an insert-only anon policy, and say why in the file. 
  Privilege or audit tables (staff, history logs) keep writes 
  blocked with select-only policies and say so in a comment.
- Emails only to jdalessio2777@gmail.com, 6 max total; log Resend 
  IDs.
- No merge to main, no push to either repo, no production deploy.
- Never print secrets. Never call cron/scheduled endpoints on any 
  deployment. No debug routes.
- Label every claim VERIFIED (how) or NOT VERIFIED. An agent's 
  report is not evidence: open its screenshots and re-walk at least 
  one of its flows yourself before trusting it.
- Before ANY script that writes, run it in a dry-run mode first 
  that only lists what it will touch, and check the list.
- TIME: production's renewal check runs at 14:00 UTC against the 
  shared DB, and techs use the app in the morning. ZERO test data 
  may exist after 12:45 UTC. Whatever isn't finished by 12:15 UTC 
  gets logged as unfinished; then clean up, verify the baseline, 
  and write the summary.
- Cleanup must never wait on an agent finishing (Run 6: a suspended 
  agent's data stayed in the DB until 17:17 UTC). Before launching 
  agents, check `date -u`; each agent deletes its own data within 
  60 min of creating it, and the main session cleans up every 
  QA-AUDIT row by the cutoff itself, whatever agents are still 
  running.
- START CHECK (read-only): staff = 5; counts match 
  baseline-counts.json (real rows added since: confirm they're not 
  QA-AUDIT, then update the baseline).
