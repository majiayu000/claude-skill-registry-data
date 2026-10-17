---
name: demo-data-generation
description: Use when modifying, extending, or regenerating the demo SQLite database that powers Demo Mode and the test fixtures. Covers the story the data tells (the Cohen family), the conventions every new record must follow, and — critically — how each individual's pension and Keren Hishtalmut deposits are derived from their gross salary under Israeli law. Triggers on "demo data", "regenerate demo", "add demo transaction", "demo fixture", "generate_demo_data", "Cohen family", "demo pension", "demo KH", "demo keren hishtalmut".
---

# Demo Data Generation

The demo database (`backend/resources/demo_data.db`) is produced by a single script — `scripts/generate_demo_data.py` — and is the dataset users see when they toggle **Demo Mode** in the UI. It also backs many UI-level smoke tests. Regenerate with:

```bash
poetry run python scripts/generate_demo_data.py
```

## The story the data tells

The dataset models **the Cohens**, a dual-income Israeli couple with two kids (one in daycare, one in elementary school) who own an apartment, save steadily every month, take an annual family vacation, and are **planning their wedding** in the last ~10 months of the tracked period.

| Span | `START_DATE = REFERENCE_DATE − 3 years − 1 day` → `REFERENCE_DATE` |
|---|---|
| Reference date | 2026-02-25 (hard-coded) |
| Tracked window | Feb 2023 → Feb 2026 (3 years) |

### Household cashflow
- **Two salaries deposited monthly** to the primary bank account:
  - *Tech Company* (1st of the month) — net ≈ 18,000 (gross **22,000**)
  - *School District* (5th of the month) — net ≈ 12,000 (gross **14,000**)
- **Annual Tech bonus** every December (~30k)
- Occasional **freelance income** (3–4 months per year)
- One-time **Prior Wealth** deposit early in the tracked window (tagged `Other Income / Prior Wealth`)

### Monthly fixed outflows
- Mortgage (Liabilities / Mortgage) — constant amortization payment
- Car loan (received mid-period, then monthly payments)
- CC bill payments (Max + Visa Cal), posted on the 2nd of the following month with small ±2–3% variance vs. the itemized totals — this is the source of the "CC gap" in the Sankey
- Standing orders every other month (Bituach Leumi / Arnona)
- Monthly transfer from *hapoalim* Main Account → *leumi* Savings Account (tagged `Ignore / Internal Transactions`)

### Seasonal patterns (deliberate, so charts look "alive")
- **Summer vacation each August** — flights + hotel + on-trip food, rotating destination (Greece / Cyprus / Italy)
- **Short winter getaway each December** (domestic hotel)
- **Back-to-school supplies surge** in August/September
- **Holiday gifts** in December (Hanukkah) and March/April (Passover)
- **Kids birthday parties** in March and October
- **Annual car service** in the spring

### Long-running arcs
- **Investments** (manual, monthly): Stock Market Fund −2,000, Savings Plan −1,500, and a Corporate Bond that was deposited ~12 months ago and matured/withdrawn ~6 months ago (closed)
- **Home Renovation** transactions in the last 6 months (project budget: `Home Renovation`)
- **Wedding planning** in the last ~10 months (project budget: `Our Wedding`, 120,000 ILS across 7 tags — Venue, Catering, Photography, Attire, Rings, Invitations, Honeymoon). Small/medium vendor payments on the Max CC; large deposits (venue, catering) via bank transfer.
- **Paid-off Personal Loan** earlier in the window + active Mortgage + active Car Loan — exercises all three liability states.

### Savings goals

Five goals, each with the money the Cohens put into it — one dated
`savings_goal_entries` row on the 5th of each month of saving, up to the
target — and a `monthly_amount`, so the card offers this month's "Fund"
suggestion (the current month is left unfunded on purpose):

| # | Goal | Entries | Demonstrates |
|---|---|---|---|
| 1 | Emergency Fund | 2,500/mo until 60k | a goal that filled — "Achieved 🎉" |
| 2 | Kids' Education Fund | 1,500/mo | `monthly_needed` off a long `target_date` |
| 3 | Wedding Fund | 3,000/mo, two wedding bank transfers linked as **spending** | money set aside *and* since spent, without the target shrinking |
| 4 | Home Renovation Fund | a 260k first entry, then 4,000/mo to 350k | money already set aside when tracking began; achieved |
| 5 | New Car Fund | a 110k first entry, then 3,000/mo | a goal still filling |

What the goals do not hold is **free cash** (bank + cash − goals), which
stays comfortably positive: the app counts a **loan receipt as income**
(`kpi_calculations.md`), and the demo's 450k mortgage and 120k car loan
arrive without a matching purchase ever leaving the accounts. If you raise
the entries, check free cash stays positive — a negative demo would greet
every visitor with a red shortfall.

Entry `date`s are real dates: `_shift_dates` moves them by the day offset,
while `savings_goals.start_month` / `closed_month` (YYYY-MM strings) move by
whole months and `target_date` by the day offset (see "How Demo Mode
re-anchors the data" below). A new date-ish column on these tables needs
adding there too, or it freezes at the snapshot's build date while
everything around it moves.

### How Demo Mode re-anchors the data

Demo Mode never serves the snapshot as generated. `prepare_demo_database`
copies it and `_shift_dates` moves it forward by
`date.today() − DEMO_REFERENCE_DATE`, so the story always ends today.
`DEMO_REFERENCE_DATE` in `backend/demo_setup.py` must equal the generator's
`REFERENCE_DATE`. Columns move in one of three ways:

| Column kind | Examples | Moves by |
|---|---|---|
| Real dates | transaction `date`, balance-snapshot `date`, `target_date`, savings-goal entry `date`, investment/liability dates, `categories.created_at` | the raw day offset |
| Calendar-month periods | `budget_rules.year`/`month`, `savings_goals.start_month`/`closed_month` | whole months, `REFERENCE_DATE`'s month → today's month (yearly rules: whole years) |
| Month relative to a transaction | `budget_month_overrides` | the shifted transaction's month ± its original direction |

Month periods must **not** move by the day offset. Anchoring them to day 1 and
adding days put them a month behind on every day before the 25th (the
reference day). The snapshot's newest budget month then landed on *last*
month, the current month had no Total Budget rule, and every category-rule
create was rejected. Consequences for the generator:

- **The newest monthly budget rules must sit in `REFERENCE_DATE`'s month** —
  that is the month Demo Mode shows as current. `create_budget_rules` builds
  the 6 months ending there; keep it that way.
- **Classify a new column by what it means, not its SQL type.** A calendar
  month goes in the month-shift group; a moment in time goes in the day-shift
  group.
- Regression tests for both groups, including the shipped snapshot checked on
  a spread of "today" dates, live in `tests/backend/unit/test_demo_setup.py`.

### Other coverage guaranteed by the script
- Multiple bank accounts (hapoalim Main + leumi Savings) and multiple cash envelopes (Petty Cash + Kids Envelope)
- Untagged CC transactions so auto-tagging and manual-tagging flows can be demoed
- Splits across 2 sources (CC + cash) — a couple of CC parents converted into different categories
- 7 pending refunds covering all statuses (pending / partial / resolved / closed) + multi-link + a 150 ILS refund txn with leftover money available for other refunds + one `source_type='split'`
- Tagging rules exercising 5 different operators (`contains`, `equals`, `starts_with`, `less_than`, `between`)
- Budget rules: category-only, tag-level, and two project budgets (Home Renovation + Our Wedding) over the 6 months ending in the `REFERENCE_DATE` month (the month Demo Mode shows as current)
- 5 insurance accounts (see next section) + a `RetirementGoal` tied to them

---

## Pension and Keren Hishtalmut — the rules

**Full reference: `.claude/skills/israeli-salary-knowledge/SKILL.md`.** That skill is the canonical source of truth for percentages, caps, and legal thresholds — this section tells you how those rules are applied to the demo couple and what invariants to preserve.

**Every individual's pension and KH deposits are derived from that individual's own gross salary** via the legally-defined percentages in the reference skill. Each employee has their **own separate pension and KH accounts** — spouses' accounts are never pooled. Treat `generate_insurance_data` as the single source of truth; keep balances and monthly contributions consistent with the percentages below.

### Makifa vs Mashlima — per individual

- The first **25,000 ILS/month of gross salary** (≈ 2× שכר ממוצע) routes pension deposits to **Keren Pensia Makifa** (קרן פנסיה מקיפה — the main fund with disability + life insurance).
- Gross salary **above** the cap routes the same 18.5% percentages to **Keren Pensia Mashlima** (pure savings, no insurance).
- A worker below the cap has **only** a Makifa account. A worker above the cap has **both**, each fed from its own slice of the gross.

### How this maps to the demo couple

| Individual | Gross | Makifa base | Makifa deposit | Mashlima base | Mashlima deposit | KH base (capped at 15,712) | KH deposit |
|---|---|---|---|---|---|---|---|
| Tech Company (above cap) | **28,000** | 25,000 | 4,625 | 3,000 | 555 | 15,712 | 1,571 |
| School District (below cap) | **14,000** | 14,000 | 2,590 | 0 (no account) | — | 14,000 | 1,400 |
| Tech — previous employer (frozen) | 12,000 (assumed) | — | — | — | — | 12,000 | 1,200 |

Account layout:
- **Tech**: PN-DEMO-001 (Makifa) + PN-DEMO-003 (Mashlima) + KH-DEMO-001 (active) + KH-DEMO-OLD (frozen, previous employer)
- **Teacher**: PN-DEMO-002 (Makifa) + KH-DEMO-002

Memo string written to every pension transaction:
`"עובד: {employee} / מעסיק: {employer_savings} / פיצויים: {severance}"` — the three Hebrew sub-amounts **must sum to the transaction's `amount`**.

All derived numbers (individual shares, memo breakdowns, monthly totals) come from the same constants at the top of `generate_insurance_data`. If you change `tech_gross`, `teacher_gross`, `makifa_salary_cap`, or any percentage, the rest of the account propagates automatically — **don't hand-edit monthly amounts and leave the percentages stale**, and vice versa.

### Account-balance calibration

Balances reflect approximately **5 years of contributions** (2 before the tracked window + 3 inside it) plus **~5–6%/yr real growth**:

```
balance ≈ monthly_contribution × 60 months × (1.13 .. 1.19 growth factor)
```

Use this as a sanity check whenever a balance is edited. If you change a monthly contribution or the gross salary it derives from, recompute the target balance with this rule of thumb. The `RetirementGoal` row's `keren_hishtalmut_balance` and `keren_hishtalmut_monthly_contribution` must equal the sum across the three KH accounts — they are already computed this way; don't hard-code them again.

### KH accounts are ALSO investments (auto-sync — don't double count)

The demo DB contains **six** rows in `investments`: the three manual ones
(Stock Market Fund, Savings Plan, Corporate Bond) **plus three
`type='hishtalmut'` investments** (`insurance_policy_id` = KH-DEMO-001/002/OLD)
with `scraped` balance snapshots — mirroring what
`InsuranceSyncMixin.sync_from_insurance` creates for real users when KH
policies are scraped. Because net worth values investments snapshot-first,
**the 255k KH is part of the demo's tracked net worth**. The early-retirement
plan (`FirePlanService`) holds each of them as a keren hishtalmut row and
leaves them out of its portfolios, so they count once. Keep the
synced-investment balances identical to the `insurance_accounts` balances,
and never add the KH as extra manual-investment *transactions* — its value
must flow only through the scraped snapshots.

### The retirement goal seeds the demo's early-retirement plan

No page reads the demo `RetirementGoal` directly any more. It seeds the
early-retirement plan `FirePlanService` derives while none is saved: its
`current_age` becomes the plan's date of birth, `target_retirement_age` the
latest retirement age the search allows, and `monthly_expenses_override`
(22,000, the steady state without the wedding and renovation arcs) and
`monthly_expenses_in_retirement` (16,500) become today's and retirement's
spending rows. Without it the demo plan has no date of birth, and the
dashboard card (`dashboard-retirement-card.spec.ts`) shows the setup prompt
instead of a projection — a CI failure.

After a change to demo balances, insurance accounts or the goal, check the
derived plan still runs:

```python
# against the freshly generated backend/resources/demo_data.db
from backend.services.fire_plan_service import FirePlanService
assert FirePlanService(session).runnable_fields() is not None
```

### Mashlima account rule

A Mashlima account should exist **only if** that individual's gross salary exceeds `makifa_salary_cap` (25,000). Do not create a Mashlima account for someone below the cap — the teacher, for instance, has only a Makifa account. If you change `tech_gross` below the cap, delete the Tech Mashlima account (PN-DEMO-003) or the script will emit 0-amount transactions.

### Yields on investment tracks

The per-track `yield_pct` values under `investment_tracks` JSON reflect **long-term realistic returns**, not cherry-picked single-year numbers. Stay in these ranges unless you have a specific reason:

| Track type | Realistic range |
|---|---|
| General / mixed pension track | 5–6% |
| Bonds-heavy track | 3–4% |
| Equity / S&P 500 track | 6–8% |
| Default (frozen, previous employer) | 4–5% |

---

## Generator structure

```
scripts/generate_demo_data.py
├── Constants: REFERENCE_DATE, START_DATE, DB_PATH, random.seed(42)
├── CATEGORIES_DATA, TAGGING_RULES_DATA
├── generate_cc_transactions        ← itemized CC (Max + Visa Cal), seasonal events, wedding CC vendors
├── generate_untagged_transactions  ← 8 deliberately-untagged CC entries for auto-tagging demos
├── generate_bank_transactions      ← salaries, mortgage, CC bills, bonuses, wedding bank transfers
├── generate_cash_transactions      ← Petty Cash + Kids Envelope
├── generate_investment_transactions
├── create_investments              ← 3 investments + prior-wealth recalc from transactions
├── create_investment_snapshots
├── create_budget_rules             ← last 6 months + 2 project budgets
├── create_split_transactions       ← 4 splits (3 CC + 1 cash)
├── create_bank_balance             ← 2 bank accounts
├── create_cash_balance             ← 2 cash envelopes
├── create_pending_refunds          ← 7 refunds covering all statuses + split source
├── create_liabilities              ← Mortgage, Car Loan, paid-off Personal Loan
├── create_retirement_goal          ← derives KH totals from insurance-account constants
├── create_savings_goals            ← 5 goals with monthly entries + utilizations
├── create_scraping_history
├── generate_insurance_data         ← pension + KH per Israeli law (see rules above)
└── main()                          ← orchestrates, drops+recreates the DB, prints row counts
```

`random.seed(42)` is set at module load so every regeneration produces the same data — commits to the `.db` file stay deterministic. If you add new randomness, keep it seeded so diffs remain small.

---

## When to touch this script

Regenerate and commit the `.db` along with script edits whenever you:
- Add a new transaction pattern, story arc, or category that Demo Mode users should see
- Find a missing use case while auditing the data flow page (e.g., a new KPI that needs seed data)
- Fix a realism bug (wrong percentages, wrong category names, etc.)
- Add support for a new table (scaffold fixture rows alongside the schema change)
- **Write or fix a UI/e2e test whose scenario the existing demo data can't
  exercise.** Demo Mode backs the Playwright e2e suite, so a test is only as
  good as the rows it can find. If the data forces a test to `test.skip(...)`
  or fall back to "whatever happens to sort first", that's a coverage gap —
  extend the generator so the scenario is deterministic, don't weaken the test.

### Extending demo data for a test scenario

When an e2e/UI test needs data the dataset lacks:

1. **Find the closest existing generator** (`generate_untagged_transactions`,
   `generate_cc_transactions`, etc.) and add rows there, keeping them in
   character with the Cohen-family story — realistic merchant names, amounts,
   and recent-month dates so they surface in the UI.
2. **Make the new rows unambiguous for the test.** Give them properties no
   other row shares (a distinctive merchant prefix, a category nothing else
   uses) so the test can target them by stable text rather than by position.
   Example: the 3 trailing *rule-free* untagged CC rows (`CASTRO FASHION`,
   `FOX HOME`, `STEIMATZKY BOOKS`) exist purely so the auto-tagging "Add Rule"
   quick-action e2e can drive the create-rule (not view-rule) path and assert
   OR-chaining across distinct merchants — the original 8 untagged rows all
   matched a seeded rule, so they only ever exercised the "View Rule" path.
3. **Mind pagination.** The transactions table shows ~10 date-sorted rows per
   page, so a test should locate new rows via the in-table search filter, not
   assume they land on page 1.
4. **Update the count in the generator's docstring** (e.g. "Generate N untagged
   CC transactions") and re-run the checks below.
5. Keep additions **seeded/deterministic** — no unseeded randomness (see "When
   NOT to touch this script").

## When NOT to touch this script

- Never introduce non-seeded randomness
- Never hand-edit the `.db` file — always go through the script so the DB is reproducible
- Never hardcode monthly pension/KH amounts; derive them from a gross salary and the percentages above
- Never let `RetirementGoal.keren_hishtalmut_balance` drift from the sum of the three KH accounts

## After every change — checks

1. `poetry run python scripts/generate_demo_data.py` — must print non-zero row counts for every table it touches and end without exceptions.
2. `poetry run pytest tests/backend/ -x -q` — must stay green; the full suite does not depend on the exact numbers but does load the DB in some fixtures.
3. Sanity-check totals against the story (`SELECT SUM(amount) FROM ...`): salaries over 3 years should be ~1.2M; investments deposited ~125k; wedding paid ≥ 90k of the 120k budget; each pension/KH balance should sit within the `monthly × 60 × 1.13..1.19` band.
4. Re-verify the retirement plan is still **on_track** (see "Retirement plan must stay ON TRACK" above) — the dashboard retirement-card e2e asserts it.
4. Commit the `.db` and the `.py` together so the bundled template always matches the generator.

## Common pitfalls

- **"Transport" vs "Transportation"** — the category is `Transportation`; writing `Transport` creates orphan rows that never render in the category pie chart. Auto-tagged transactions and refund back-payments have hit this bug before.
- **Date anchors that assume 14 months** — several thresholds (home renovation last 6 months, wedding last 10 months) were originally tied to a shorter window. When extending the span, verify each `timedelta(days=…)` still picks the intended slice.
- **CC bill variance** — bank CC bill amounts are deliberately `cc_total × uniform(0.98, 1.03)` so the Sankey's CC gap is non-zero. Don't "fix" this to exact totals.
- **Prior wealth in investments** — after any change to investment transactions, the per-investment `prior_wealth_amount` must be recalculated as `−sum(txns)`. The script does this in `create_investments`; don't bypass it.
- **Memo sum must equal transaction amount** — a pension deposit of 4,070 whose memo reads `עובד: 1320 / מעסיק: 1430 / פיצויים: 1320` is valid; if the three Hebrew fields don't sum to the `amount`, the UI will display an inconsistent breakdown.
