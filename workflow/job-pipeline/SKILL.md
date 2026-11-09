---
name: job-pipeline
description: End-to-end job application run over the Job Hunt Search tab — read every posting Claude judged fit without a browser, dry-run the forms by script, send the ones the user approves, record them in the funnel, and report what needs the user. Use when asked to "apply to everything that fits", process the search, or run the daily job-hunt pass. Needs the dashboard at http://localhost:4321 and Chrome.
---

# job-pipeline — the whole pass, cheaply

Five commands, five short tables. Nothing is read through the Chrome
extension; postings are fetched by script and forms are filled by script.
Budget: one output line per job per stage.

## 0. Preconditions

- Dashboard running (`Job Hunt.bat` or `npm run dashboard`), Search refreshed
  today (`node scripts/funnel.mjs search --refresh` if the cache is stale).
- LinkedIn Easy Apply wanted → the automation profile is logged in
  (`node scripts/apply.mjs --login`, once).
- Scratch directory for this run: `$TEMP/claude/` (or the session scratchpad).

## 1. Screen (rules) — `job-screen`

```
node scripts/funnel.mjs screen --json $S/screen.json
```

Writes nothing: the dashboard applies the same rules on every read, so their
hits are already out of the Search tab. Do not `--commit` — that makes today's
rule hits permanent hides. Claude judges new cards about ten a minute: right
after `search --refresh`, wait until the dashboard's queue is empty
(`claude:—` on many lines means it is still working).

## 2. Read the postings — no browser

```
node scripts/jobs-fetch.mjs --screen $S/screen.json --buckets apply,check --out $S/fetched.json
node scripts/jobs-fetch.mjs --retry $S/fetched.json          # re-fetch the rows that errored (LinkedIn 429)
```

One line per job: `idx | company — title | claude:<verdict>/<score> | !low-pay !applied-before | mode | lock | level/years | +stack | -neg | lang | pay:… | apply:<vendor> form:…`.
Claude's verdict comes first — it read the whole posting against
`src/verdict-criteria.md`; the rest are regexes over the same text:

- `claude:skip` → not a candidate. Report it with its reason; do not hide it
  (it waits in "Skipped by Claude", and a criteria change may bring it back).
- `claude:maybe`, `claude:…(old)` or `claude:—` → **needs-you**: something the
  user should check, as in the "Check" stack.
- `claude:apply` → a candidate, unless the line says otherwise:
  - `!low-pay` → **needs-you** (pay under the floor is the user's call);
  - `!applied-before` → **needs-you** (a role like one already applied to);
  - `hybrid «…»` / `onsite` / `lock:…` / `lang:…` that Claude did not mention →
    read the text (`--text`) and say what you found; never hide on a regex;
  - `apply:portal` / `himalayas-account` / `indeed` → **needs-you** (account needed).
- `CLOSED` → hide: `posting closed`.

Hide only closed postings, with `node scripts/funnel.mjs dismiss "<url>" --reason ".." --title ".." --company ".."`:
a hide is permanent and teaches the screening rules (same role, same company).

## 3. Apply — `job-apply`

Split the candidates into two JSON lists (`batch-ats.json`, `batch-linkedin.json`)
and dry-run them with `apply-batch.mjs`: it fills every form and sends nothing.
It also refuses on its own what should not go out unasked — no current
Claude `apply`, pay under the floor, a role like one applied to — and says why.

```
node scripts/apply-batch.mjs --fetched $S/batch-ats.json --out $S/results-ats.json [--answers $S/answers]
node scripts/apply-batch.mjs --fetched $S/batch-linkedin.json --out $S/results-linkedin.json
```

Show the user the dry-run lines (company, title, fields filled, missing
answers) and send only what they approve:
`--submit --only <idx,…>`. `--force <idx>` / `--accept-low-pay <idx>` only on
their word. Applications go out in their name; nothing is sent unseen.
Boards that e-mail a verification code (Greenhouse) run headed and need the
user at the keyboard, so run those last and say so. The dashboard's "Apply"
fills no forms: it only opens the posting.

Then clear the `missing-answers` rows: write `$S/answers/<idx>.json`, re-run
with `--only`. A label that will recur goes into the answer bank once:
`node scripts/apply.mjs --remember "<label substring>" "<answer>"`.

Every `applied` row is already in the funnel (the script posts it). Do not
add it again by hand.

## 4. Close the loop

- A second posting of a role just applied to (same company, other board) needs
  nothing: the screening rules hide it ("already applied to this role").
- `node scripts/funnel.mjs stats` and `applied | head` to confirm the count.

## 5. Report to the user

Four lists, one line each, nothing else:

1. **Applied** — company, title, board, funnel id.
2. **Needs you** — `node scripts/funnel.mjs attempts` (codes not typed, CAPTCHAs, account walls, missing answers — recorded by apply.mjs, also on the dashboard), plus hybrid-light roles and marketplaces (lemon.io, Jobgether, Proxify…) from the screen, with the URL.
3. **Claude said no** — the `claude:skip` rows, one line each with Claude's reason (they stay in "Skipped by Claude").
4. **Failed** — `submit-failed` rows with the error text and screenshot path.

## Cost rules

- Never `get_page_text` or screenshot a job page through the extension; `jobs-fetch` has the text.
- Look at a screenshot only for a `submit-failed`, once per board.
- Keep the whole run's model output under ~10 lines per job.
