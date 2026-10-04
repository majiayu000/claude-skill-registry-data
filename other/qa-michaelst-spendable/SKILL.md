---
name: qa
description: QA a change by driving the running dev app like a real QA engineer - start the server and a real browser session, write a checklist from the agreed requirements and the diff, execute every item with evidence, then go looking for anything that looks off even where the diff did not touch. Reports findings by severity and separates regressions from pre-existing problems. Use after a change is implemented and the gates pass, when the user asks to "QA this", "test it in the app", or "check it actually works".
---

# QA

Green tests say the code does what its author thought. QA says the *feature* works, in the real app,
for a user who is trying to use it — and it is the only step that catches what nobody thought to
assert. Approach it as a QA engineer, not as the author defending the change: your job is to find the
bug before the user does, and a pass with nothing found is a weaker result than a pass with three
findings.

Two halves, both required:

1. **Verify the change** against the agreed requirements, item by item, with evidence.
2. **Break it, and look around.** Edges the requirements never mentioned, and anything on adjacent
   screens that looks wrong — whether or not this change caused it.

## 1. Start the session

```bash
.claude/skills/qa/scripts/qa.sh start
```

Starts the dev server if it is down (it leaves a server you already had running alone), launches a
scratch headless Chrome, and signs in by installing a minted session cookie — Google OAuth cannot be
driven headlessly and no password is ever typed. Run every `qa.sh` command through Bash with the
sandbox disabled — Mix needs a real TCP socket.

It finds the port the way the app does: `PORT` from the environment, else this worktree's
`.env.worktree`, else 4000. **In a worktree that means it QAs that worktree's app**, on its own
database, with its own Chrome and state directory, so two worktrees can QA at once. It refuses to
start if what answers on that port is not Spendable.

The dev database must already contain at least one user; `qa.sh` signs in as the oldest one unless
you pass a UXID or Google `external_id`. If it has none, sign in once in a real browser first, or
create one through `Accounts` with `mix run` — never by inserting a row directly.

Then each check is a small script run against the still-live browser:

```bash
.claude/skills/qa/scripts/qa.sh run /path/to/scratchpad/check-01.mjs
```

Copy [scripts/example-check.mjs](scripts/example-check.mjs) and rewrite it. The session is the
[record-demo-video](../record-demo-video/SKILL.md) CDP driver (`click`, `type`, `typeDate`, `press`,
`hover`, `goto`, `evaluate`, `expect`) plus `shot(name)`, `text()`, `resize(w, h)`, and
`drainProblems()`. **Do not use the in-app Browser pane** — its synthetic clicks do not reliably fire
`phx-click`, so a check that "passes" there proves nothing; it cannot screenshot at all unless the
pane happens to be on screen; and it cannot be signed in by hand, because the session cookie is
`httpOnly` and `document.cookie` cannot overwrite one. Reach for `qa.sh`, not for a workaround.

A part of the app that only a non-browser client reaches — an API, a webhook, an MCP endpoint — is
still QA's job. Drive it with `curl` in the same pass, as the real client would, and check the effect
in the browser: the point is that the two agree.

`qa.sh log` tails the dev server log. `qa.sh stop` tears down what it started — hold off on it if a
[record-demo-video](../record-demo-video/SKILL.md) pass is next, since that needs the same server up.

## 2. Write the checklist before you touch anything

Written first, so the pass is not shaped by what happens to work. Sources, in order:

- **The requirements and the approved plan** — one row each, worded as the observable outcome, using
  the worked example numbers where there are any.
- **The diff** — every changed LiveView, route, component, action, migration, and every caller of a
  function whose behavior changed. `git diff` against the base branch.
- **The standing list below**, filtered to what this change can actually reach.

Write it to the scratchpad as a table: check, how to verify, expected, status, evidence. Show it to
the dev, note anything you deliberately left out, and get on with executing it — no approval gate.

### Standing checks

Not a form to fill in. Skip what the change cannot reach, and say you skipped it.

- **Happy path**, with realistic data. Then reload the page: did it actually persist?
- **The write really landed.** Query the DB for the row. The screen showing a number is not evidence
  the number was saved.
- **Money.** Decimal formatting, thousands separators, negatives, rounding to cents, zero. Whether
  the sign is right: an allocation *to* a budget and a spend *from* one differ only by sign, and the
  form's label flips on it. This app's whole job is arithmetic — a wrong number that renders
  beautifully is the worst outcome here.
- **Dates and months.** Budgets and spending are read per month, so drive a transaction dated on the
  first and last day of a month and confirm it lands in the right one. A date that renders one day
  off is a timezone bug, not a display bug.
- **The Spendable remainder.** Any change that touches allocations: allocate part of a transaction,
  all of it, more than it, and none of it, and confirm the remainder in **Spendable** is what is
  left over each time.
- **Validation and errors.** Required fields blank, bad formats, negative and huge amounts, a
  duplicate, a stale record edited in a second tab. Is the message specific, in the right place, and
  in the app's voice?
- **Every new error reaches a field the form renders.** An error on a field the form does not render
  is a save that silently does nothing — the user clicks save, nothing happens, nothing is said. The
  nested allocation rows on `/transactions` and `/splits` are where this bites: an error on a
  child row that the parent form never displays looks exactly like a dead button.
- **Adding and removing nested rows.** Those same allocation rows use Ecto's `sort_param` /
  `drop_param`, so add a row, remove a middle one, remove the last one, and remove all of them —
  then save and reload. This is the least test-covered mechanism in the app.
- **Ownership isolation.** Every record belongs to exactly one user and every action pins it. Take a
  record id belonging to another user, rewrite a `phx-value-id` attribute to it with `evaluate`, and
  click: the action must refuse, never act and never leak the other record's name into the page.
- **Empty, one, many.** Empty state copy, a single row, enough rows to page — then search, filter,
  and scroll in combination, and check the filter survives a reload. `/transactions` pages by
  infinite scroll, so drive it past the first page.
- **Interruptions.** Back button, refresh mid-flow, double submit, rapid clicks, Escape/cancel
  discarding, an unsaved form navigated away from.
- **Everything on the new screen goes somewhere.** Click every link, button, and tab you added, and
  check the nav highlights the tab you are actually on.
- **The browser's own complaints.** `drainProblems()` after every check: console errors, uncaught
  exceptions, 4xx/5xx responses, a LiveView socket that dropped and reconnected.
- **The server log.** `qa.sh log` — stacktraces, 500s, and anything noisy the change introduced.
  Also check nothing secret got logged: Plaid tokens and Google ids are `redact: true` on the schemas
  for a reason.
- **Narrow viewport (375px)**, long strings and long names, keyboard tab order and focus, loading
  states on a slow action. This app is used on a phone more than a desktop.
- **Looks like the rest of the app.** Spacing, alignment, button placement, capitalization, typos,
  terminology matching the context's `CONTEXT.md`.

### What is hard to drive, and what to do instead

**Bank linking.** `/banks` opens Plaid Link, a third-party JS overlay against the Plaid sandbox. Do
not try to drive it click-by-click. Verify what is on our side of the boundary — the link token
request, the bank-limit refusal, the account list after a member exists — and say in the row that the
Plaid overlay itself was not driven.

**Syncing.** Sync runs as an Oban job. Enqueue it the way the app does and check the job ran and the
rows landed, rather than waiting on a webhook.

## 3. Execute with evidence

A row goes green only with something attached: a screenshot you actually read, a queried value, a log
line. **Read the screenshots with the Read tool** — they are PNGs and they render. That is how you
catch what no assertion covers: a form error rendering white and indented instead of red and flush
left, a column clipped, `$1234.5`.

Never mark a check passed because the code looks like it should pass. If a check is impractical to
drive, say so in the row and say what you did instead.

## 4. Then go looking

The part that is actually QA rather than verification. Spend real effort here, after the checklist,
with the app already in a state the change created.

- Walk the screens **around** the change — the list it links from, the other screen that reads the
  same data, the form that writes it.
- Follow the data end to end. A transaction's amount should agree with its allocations, with each
  budget's balance, and with the month's spending. Cross-screen disagreement is the highest-value bug
  in this app.
- Poke at whatever looks fragile, and at anything that made you double-take.

Report anything off, including what this change plainly did not cause. **Do not fix pre-existing
problems here** — that is scope creep on someone else's PR. Write them up and hand them to the dev.

## 5. Report and triage

One table, most severe first:

| # | Check | Result | Severity | Caused by this change? | Evidence |

Severity: **blocker** (wrong number, data loss, one user seeing another's records, the feature does
not work), **major** (a real path is broken or badly confusing), **minor**, **nit**. Be honest about
severity — a nit inflated to a blocker costs the dev the same as a blocker missed.

Then:

- **Blockers and majors caused by this change**: fix them through the [tdd](../tdd/SKILL.md) skill —
  failing test first, since a QA finding is by definition a gap in the suite — re-run the gates from
  the top, then re-run every affected check.
- **Everything else**: present it and let the dev choose.
- Finish with what you could not check and why. A QA report that implies full coverage it did not do
  is worse than a short one.

## Data hygiene

The dev database holds data the user cares about — it is their own budget. **Never reset, drop, or
re-seed it**; any `ecto.reset` / `ecto.drop` is `MIX_ENV=test` only. Create the records your checks
need rather than editing the dev's, avoid destructive actions on data you did not create, and end the
report with the state you left behind — including anything a check deliberately broke.
