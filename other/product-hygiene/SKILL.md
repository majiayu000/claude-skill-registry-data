---
name: product-hygiene
description: Clean a product funnel before anyone makes a decision from it. Establishes what a person is, removes non-customers from the denominator, runs the standard leak checks, ranks losses by people rather than percentages, reconciles two independent sources, and prescribes what to log next. Use when the user says /product-hygiene, asks "why did our activation drop", brings a funnel or an analytics export, wants to know which numbers can be trusted, or is about to plan a sprint from a dashboard.
---

# Product Hygiene

Cleans a funnel so a decision can be made from it.

Not "build a dashboard". Not "find growth opportunities". One job: **which of these numbers can carry
a decision, and which cannot** — plus the one thing to log so next month's answer is better than
this month's.

## The three hard rules

**1 · Every rate is printed with its denominator.** A percentage without the population it was
computed over is not a finding, it is a rumour.

**2 · Every conclusion is graded.** `MEASURED` (computed from the given data) · `OBSERVED` (seen in a
recording or a log, n small) · `ASSUMED` (a mechanism you believe but did not verify). Never let an
ASSUMED wear the tone of a MEASURED.

**3 · An empty cell is a finding, not a gap.** What you cannot check is half the value of this skill.
Say it out loud, and say what would fix it.

⚠️ **Do arithmetic in code, never in your head.** Write and run a script. You are a language model;
percentages done by reasoning are exactly the class of error this skill exists to catch in others.

⚠️ **Check what you have before you write, and never `pip install`.** Run
`python3 -c "import pandas"` once. If it succeeds, use pandas. If it fails, use `csv` and
`collections.Counter` — everything this skill asks for fits in them. **Do not install anything and
do not stall**: the machine may be a laptop whose `python3` is the one Apple ships, which has no
pandas, and an install mid-session costs minutes and can fail behind a proxy. Say in one line which
one you are using.

⚠️ **Slice timestamps, do not parse them.** Apple ships Python 3.9, where `datetime.fromisoformat`
rejects the trailing `Z` most exports use. `created_at[:7]` is the month, `[:10]` is the day, and ISO
strings sort correctly as strings. If you must parse, strip the `Z` first.

---

## Step 0 — Inventory: what can I actually check?

**Before computing anything**, walk the check catalogue below and mark each one:

| | |
|---|---|
| ✅ **CAN** | the column exists and is populated |
| ⚠️ **PARTIAL** | the column exists but is populated on N% of rows — *any finding is about that N%, and must say so* |
| ❌ **CANNOT** | the column does not exist. **This is a row in the report** |

The `PARTIAL` verdict is the one people skip and it is where false findings come from. A `device`
column filled on 41% of rows gives you a device breakdown about 41% of your users, presented as if
it were about all of them.

## Step 1 — Premise audit

**Recompute every number the human gave you, from the raw data, before any analysis.**

The output shape, on an unrelated checkout funnel:

```
CLAIM                          GIVEN     RECOMPUTED    VERDICT
"checkout conversion fell 12%" −12%      −3.1%         REFUTED — most of the drop is one week of bot traffic
"we have 50k monthly actives"  50,000    31,400        REFUTED — 50k counts devices, not accounts
"returns are up"               (no number given)  —    UNVERIFIABLE — no returns table in this export
```

Print `CONFIRMED` / `REFUTED` / `UNVERIFIABLE` per claim, and **analyse on the recomputed values
only**. A wrong premise does not fall out of an analysis later; it becomes the axis of it.

## Step 2 — Identity: what is one person here?

Do not build a funnel until this is answered explicitly. There are usually several defensible
answers and they differ by a lot:

- distinct **device/cookie ids** (GA4 `user_pseudo_id`, Amplitude device id) — these are *browsers*
- distinct **logged-in ids** (`user_id`) — these are *accounts*, and usually only after login
- rows in the **production database** — accounts, including ones nobody ever used
- **actual humans** — requires work

Report the ladder with all its numbers. Then **declare the unit and use it everywhere.**

⚠️ **Watch for the unit break.** Pre-login events usually carry no account id at all, so the top of
the funnel is countable only in device ids while every later step is countable in account ids. If so,
say it plainly: *the funnel mixes units and cannot not mix them with this instrumentation* — and put
the fix in Step 8. It is a tracking problem, not a query problem.

## Step 3 — Population: who is not a customer?

Four layers. **Report every rule with the number of rows it removed** — a silent filter is just
another undeclared denominator, and now it is yours.

| layer | signals |
|---|---|
| **Automation** | headless/library user agents · datacenter geo · sub-2s form completion · zero engagement time · one page view, zero clicks · disposable email domains |
| **Internal** | staff email domains · an admin-created flag · office IPs · sales-demo accounts |
| **Duplicate identity** | one human, two device ids (phone → laptop) · retries that mint a second account |
| **Test** | seed data, load tests, e2e runs |

⚠️ **Do not filter on one signal.** Check whether independent signals select the same rows. If they
do, say so — that is what makes the cut defensible. If they disagree, the boundary is a judgment
call and must be reported as one.

⚠️ **Some automation converts.** Scanners follow redirects and fire real events. A rule like "remove
accounts with zero activity" will leave them in.

⚠️ **Removing internal accounts often makes the funnel look worse**, because sales demos run deeper
than customers. That is correct. Do it anyway.

## Step 4 — The positive pass, and it goes FIRST

Not "who dropped out" but **"who got all the way through, and what do they have in common?"**

Compare the people who reached the final step against everyone else, on every available attribute.
Report anything where the completers differ sharply from the base.

**Why this is first:** the negative pass can only find things that are wrong with the step you asked
about. The positive pass can find a property of the people who succeed that nobody asked about at
all — a permission they hold, a channel they came from, a thing they did in the first five minutes.
**Those are the findings that change the strategy rather than the button.**

## Step 5 — The negative pass: the standard checks, crossed

For **every step**, cut by **every available dimension**:

| dimension | catches |
|---|---|
| device category | layout, tap targets |
| **browser** — and in-app/embedded browsers separately | **blocked popups and OAuth redirects in webviews** |
| browser version | a regression that shipped |
| OS + version | old webviews, missing APIs |
| viewport / screen size | a control below the fold |
| geography | payment rails, blocked CDNs, missing locale |
| language | untranslated blocking copy |
| traffic source | a channel sending the wrong people |
| account age / cohort month | **immature cohorts — see below** |

> 🔴 **Cross the dimensions, do not walk them one at a time.**
> A device-only cut says "mobile is broken" in cases where mobile is fine and one *browser* is not.
> One dimension at a time produces a confident, expensive, wrong answer.

⚠️ **Rank by people, never by percentage gap.** A cell at 22% against a 61% base is dramatic and may
be nine people. Report the count next to every rate, and where n is small enough that the interval
covers the base rate, **say that instead of reporting a finding**.

⚠️ **The most recent cohort always looks worst.** Before reporting a decline in any step with a long
lag, check the observation window against the p90 time-to-event. If the window is shorter, the
decline is censoring and you must say so.

⚠️ **A branch is not a step.** An optional action that some users take instead of continuing does not
belong in a linear funnel; putting it there corrupts everything below it.

## Step 6 — Reconcile two sources

Compare **sets of ids**, not totals. `402 = 402` proves nothing if they are different 402.

| verdict | when |
|---|---|
| `RECONCILED` | the id sets agree, and the two sources are captured independently |
| `CONSISTENT — NOT INDEPENDENT` | they agree because one is derived from the other. **Agreement here means nothing** |
| `DISCREPANCY n%` | explained down to the row, or filed as unexplained with its size |

⚠️ **Agreement is not confirmation.** Two instruments fed by the same pipeline will agree while both
are wrong. Always state *why* the sources are independent, or admit that they are not.

## Step 7 — The funnel, and the loss ledger

Output the funnel in the declared unit, with each step's **actual definition** attached — what the
event fires on, not what it is called.

⚠️ **Check the event names against their definitions.** An event called `x_connected` that fires when
a dialog *opens* is not a record of connection. Where two events could serve as a step, report both
counts and make the human choose.

⚠️ **If any source code is available, read the call site — it beats every written event dictionary.**
Grep for the tracking function and read the lines around each call: what runs before it, what runs
after it, and which branch it sits in. An event fired *before* the thing it names has a chance to
succeed measures attempts, not outcomes. **The branch with no call is the finding** — a failure path
that logs to a server log, or logs nothing, is a step you cannot count. Carry each one to Step 8.

⚠️ **A call site is evidence, not proof, and grading it `MEASURED` for a past window is the same
error this skill exists to prevent.** Before you trust it, say which of these you actually checked:

| | |
|---|---|
| **which revision** | you are reading today's code. Unless you checked history, you do not know what fired in your window. Grade the *definition* `ASSUMED` for any period you did not verify |
| **all the emitters** | grep the alias too (`analytics.track`, `logEvent`, `gtag`), plus tag managers and any server-side send. One call site is not all of them |
| **the wrapper** | a thin wrapper can drop, rename or re-route events. Read it, not just the call |
| **what is imported** | if the hook or helper that decides the branch is not in front of you, you cannot claim what the branch does |

Then the ledger, ranked by **people lost per month**:

```
LOSS   STEP                    SEGMENT             RATE vs BASE     n    HYPOTHESIS       CHECK TODAY                GRADE
 210   cart → payment          Safari 15 and older  11% vs 62%     412   card form is       open the cart in an old     ASSUMED
                                                                        blank on that      Safari via BrowserStack
                                                                        engine
```

**"Check today" must be an action for today**, not a project. "Instrument this properly" is bad;
"reproduce the checkout on the oldest browser in the segment" is good.

## Step 8 — The tracking plan 🔴

**Every `CANNOT` and `PARTIAL` from Step 0 becomes a concrete change.** This is the step that makes
the skill worth running again.

```
#1  <WHAT IS NOT LOGGED>
    Today      what exists now
    Cost now   what it costs you, in people or in a decision you cannot make
    Log this   one event, or one attribute. Be specific enough to hand to an engineer
    Then       the question it makes answerable
    Payback    when it starts working — and say plainly if it cannot recover history
```

**Rules:** every entry names what it costs *today* — never "best practice". One event or one
attribute per entry; a twenty-item tracking plan does not ship. And where a change fixes next month
but not last month, **say so**.

## Refusal

You may return **`WITHHELD — decision not supported`**, with one blocker, one owner, one date. An
instrument that always produces an answer is not an instrument.

## Outputs

| file | |
|---|---|
| `funnel/funnel-<date>.md` | the funnel, declared unit, real definitions, denominators |
| `findings/leaks-<date>.md` | the loss ledger |
| `gaps/tracking-plan-<date>.md` | Step 8 |
| `CLAUDE.md` §1 | the contract: unit, exclusion rules, step definitions, window |

**Never modify the raw exports.** Read them, never write them.

**On re-run:** diff against the previous dated report and **separate a changed definition from a
changed product**. Data rots — new bots, new campaigns, silently broken tracking. This is the smoke
detector.

## How not to do it

- ❌ a conversion rate with no denominator printed next to it
- ❌ a filter applied without reporting how many rows it removed
- ❌ ranking leaks by percentage gap
- ❌ one dimension at a time
- ❌ "the data is insufficient" as a stopping point — say what is missing and what to log
- ❌ more than five findings; that is a backlog, not a diagnosis

## How to do it

- ✅ "62% — of the 1,340 accounts that reached the previous step, after removing 210 automated sign-ups (rule: headless user-agent OR disposable mail domain, both agreeing)"
- ✅ "Two sources agree, but one is generated from the other. That is not confirmation."
- ✅ "This cell is 22% against a 61% base — and n=9. I cannot distinguish it from the base rate."
- ✅ "I could not check whether the person had permission to complete this step. Nothing in either
  export records a refusal. Log a `<step>_denied` event with a reason, and next month it is a column."
