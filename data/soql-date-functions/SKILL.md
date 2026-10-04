---
name: soql-date-functions
description: "Use when writing a SOQL query that groups or filters records by a date period — day, week, calendar month/quarter/year, or fiscal month/quarter/year — with the 13 SOQL date functions (CALENDAR_MONTH/QUARTER/YEAR, DAY_IN_MONTH/WEEK/YEAR, DAY_ONLY, FISCAL_MONTH/QUARTER/YEAR, HOUR_IN_DAY, WEEK_IN_MONTH/YEAR). Covers WHERE-clause filtering with no GROUP BY, the SELECT-requires-GROUP-BY rule, the ban on comparing a date-function result to a date literal, the custom-fiscal-year restriction on FISCAL_* functions, and the dateTime-only inputs to DAY_ONLY()/HOUR_IN_DAY(). NOT for SOQL relative date literals (TODAY, LAST_N_DAYS, THIS_FISCAL_YEAR — those are literals, not functions), NOT for Apex Date/Datetime class methods, NOT for GROUP BY/ROLLUP/CUBE/HAVING mechanics (use apex/apex-aggregate-queries), and NOT for time-zone conversion internals (use apex/timezone-and-datetime-pitfalls)."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Operational Excellence
triggers:
  - "group opportunities by fiscal quarter directly in a SOQL query"
  - "filter records where the calendar year of CloseDate equals 2026 without a date literal"
  - "count rows per calendar month in the database instead of looping over them in Apex"
  - "getting an error comparing a date function to a date literal in a WHERE clause"
  - "convert a CreatedDate dateTime to just its date portion inside SOQL with DAY_ONLY"
tags:
  - soql-date-functions
  - date-functions
  - fiscal-year
  - calendar-quarter
  - group-by-date
inputs:
  - "The sObject and the date or dateTime field to group or filter by"
  - "The reporting period: day, week, calendar month/quarter/year, or fiscal month/quarter/year"
  - "The org's fiscal-year configuration (standard vs. custom fiscal years) — it gates the FISCAL_* functions"
outputs:
  - "A SOQL query that buckets or filters by the correct date function"
  - "Guidance on WHERE-only filtering vs. SELECT + GROUP BY placement, and calendar-vs-fiscal / date-vs-dateTime function selection"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-07-08
---

# SOQL Date Functions

This skill activates when a query needs to **group or filter records by a date period** — pulling the year, quarter, month, week, day, or hour out of a `Date` or `DateTime` field *inside SOQL* instead of reading every row into Apex and bucketing them by hand. The mechanism is the family of SOQL date functions (`CALENDAR_YEAR()`, `FISCAL_QUARTER()`, `DAY_ONLY()`, and ten more). They are one of the seven function categories in the SOQL `SELECT` reference, alongside aggregate functions, `convertCurrency()`, `convertTimezone()`, `FORMAT()`, `GROUPING()`, and `toLabel()`.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Know whether you are grouping or just filtering.** Both are valid. A date function can appear in a `WHERE` clause to filter results *even when the query has no `GROUP BY` clause at all* (e.g. `WHERE CALENDAR_YEAR(CloseDate) = 2026`). It does not force you into aggregation.
- **Know the field type.** Most date functions take a `Date` or `DateTime` field. Two of them — `DAY_ONLY()` and `HOUR_IN_DAY()` — accept **only a `DateTime` field**. Pointing them at a `Date` field is a query error.
- **Know the org's fiscal-year configuration.** `FISCAL_MONTH()`, `FISCAL_QUARTER()`, and `FISCAL_YEAR()` are **not supported when the org has custom (generic) fiscal years enabled.** If the org uses custom fiscal periods, these functions are unavailable and you must group by calendar periods or a formula field instead.
- **Remember the time-zone basis.** SOQL returns `DateTime` values as UTC. Date functions bucket on that raw UTC instant unless you wrap the field in `convertTimezone()`, so a record created at 11pm local can land in the "next day" bucket. See `apex/timezone-and-datetime-pitfalls` for the full treatment.

---

## Core Concepts

### The 13 date functions

Each returns a number except `DAY_ONLY()`, which returns a `Date`:

| Function | Returns | Input | Notes |
|---|---|---|---|
| `CALENDAR_MONTH(field)` | Number (1–12) | Date/DateTime | Calendar month |
| `CALENDAR_QUARTER(field)` | Number (1–4) | Date/DateTime | Calendar quarter |
| `CALENDAR_YEAR(field)` | Number | Date/DateTime | Calendar year |
| `DAY_IN_MONTH(field)` | Number | Date/DateTime | Day of month |
| `DAY_IN_WEEK(field)` | Number | Date/DateTime | Day of week |
| `DAY_IN_YEAR(field)` | Number | Date/DateTime | Day of year |
| `DAY_ONLY(field)` | **Date** | **DateTime only** | Date portion of a DateTime |
| `FISCAL_MONTH(field)` | Number | Date/DateTime | Not supported with custom fiscal years |
| `FISCAL_QUARTER(field)` | Number | Date/DateTime | Not supported with custom fiscal years |
| `FISCAL_YEAR(field)` | Number | Date/DateTime | Not supported with custom fiscal years |
| `HOUR_IN_DAY(field)` | Number (0–23) | **DateTime only** | Hour of day |
| `WEEK_IN_MONTH(field)` | Number | Date/DateTime | Ordinal week within the month |
| `WEEK_IN_YEAR(field)` | Number | Date/DateTime | Ordinal week within the year |

### Two placements: filter (`WHERE`) and group (`SELECT` + `GROUP BY`)

A date function has two independent jobs:

- **Filter** — put it in the `WHERE` clause to keep only rows in a period. This works with *no* `GROUP BY`:
  ```sql
  SELECT Id, Amount FROM Opportunity WHERE CALENDAR_YEAR(CloseDate) = 2026
  ```
- **Group** — put it in `SELECT` alongside an aggregate to bucket rows. When a date function appears in `SELECT`, it **must** also appear in `GROUP BY`:
  ```sql
  SELECT CALENDAR_YEAR(CloseDate) yr, SUM(Amount) total
  FROM Opportunity
  GROUP BY CALENDAR_YEAR(CloseDate)
  ```

### The date-literal comparison rule

A date function returns a *number* (or, for `DAY_ONLY()`, a `Date`). You **cannot compare the result of a date function to a date literal** in a `WHERE` clause. Compare to an integer instead:

```sql
-- CORRECT: compare to an integer
WHERE CALENDAR_YEAR(CloseDate) = 2026

-- WRONG: compare to a date literal (ISO date or relative literal)
WHERE CALENDAR_YEAR(CloseDate) = 2026-01-01
WHERE CALENDAR_MONTH(CloseDate) = THIS_MONTH
```

If your intent is a relative window (this fiscal year, last 90 days), you likely want a **date literal on the raw field** — `WHERE CloseDate = THIS_FISCAL_YEAR` — not a date function at all. That is a literal, not a function; it is out of scope here.

---

## Common Patterns

### Pattern: database-side period rollup

**When to use:** you need a total/count per year, quarter, or month and today you `SELECT` all rows and sum them in an Apex loop.

**How it works:** move the bucketing into SOQL with a date function in `SELECT` + `GROUP BY`, and read the results from `AggregateResult`:

```apex
for (AggregateResult ar : [
        SELECT CALENDAR_QUARTER(CloseDate) qtr, SUM(Amount) total
        FROM Opportunity
        WHERE CloseDate = THIS_YEAR
        GROUP BY CALENDAR_QUARTER(CloseDate)]) {
    Integer quarter = (Integer) ar.get('qtr');
    Decimal total   = (Decimal) ar.get('total');
}
```

**Why not the alternative:** iterating every Opportunity to bucket by quarter pulls unbounded rows into heap and burns query rows; the grouped query returns one row per quarter and does the arithmetic in the database. See `apex/apex-aggregate-queries` for the `AggregateResult`/`GROUP BY` mechanics.

### Pattern: period filter without aggregation

**When to use:** you just want the rows in a period (a fixed calendar year, a specific fiscal quarter) and no rollup.

**How it works:** put the date function in `WHERE` only — no `GROUP BY` needed:

```sql
SELECT Id, Name, Amount FROM Opportunity WHERE FISCAL_QUARTER(CloseDate) = 3
```

**Why not the alternative:** people reach for a `CloseDate >= :start AND CloseDate < :end` range and hand-compute the boundaries. `FISCAL_QUARTER(CloseDate) = 3` reads intent directly and follows the org's fiscal calendar — but only when standard fiscal years are in effect (see Gotchas).

### Pattern: collapse a DateTime to a date bucket

**When to use:** you have a `DateTime` field (e.g. `CreatedDate`) and want to count per calendar day.

**How it works:** `DAY_ONLY()` strips the time and yields a `Date` you can group on:

```sql
SELECT DAY_ONLY(CreatedDate) d, COUNT(Id) c
FROM Case
GROUP BY DAY_ONLY(CreatedDate)
```

**Why not the alternative:** grouping on the raw `DateTime` produces one bucket per distinct instant (useless); `DAY_ONLY()` is dateTime-only and returns the date part so each calendar day is one row.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Keep only rows in a period, no rollup | Date function in `WHERE`, no `GROUP BY` | A date function filters without requiring aggregation |
| Total/count per period | Date function in `SELECT` **and** `GROUP BY` | A `SELECT` date function must appear in `GROUP BY` |
| "This year / last 90 days" relative window | Date **literal** on the raw field (`WHERE CloseDate = THIS_YEAR`) | Literals express rolling windows; a date function returns a number, not a window |
| Org has custom fiscal years enabled | Group by calendar functions or a fiscal formula field | `FISCAL_*` functions are unsupported under custom fiscal years |
| Need the date part of a `DateTime` | `DAY_ONLY(dateTimeField)` | Returns a `Date`; accepts only a `DateTime` field |
| Need hour-of-day distribution | `HOUR_IN_DAY(dateTimeField)` | Hour component; accepts only a `DateTime` field |
| Buckets must follow the user's local day | Wrap in `convertTimezone(field)` before the date function | SOQL evaluates the raw UTC instant otherwise |

---

## Recommended Workflow

1. **Classify the need** — filtering a period (→ `WHERE` only), rolling up per period (→ `SELECT` + `GROUP BY`), or a relative rolling window (→ a date *literal*, which is out of scope for this skill).
2. **Pick the function by period and field type** — calendar vs. fiscal; year/quarter/month/week/day/hour. Confirm the field is a `DateTime` before choosing `DAY_ONLY()` or `HOUR_IN_DAY()`.
3. **Check fiscal configuration** — if you chose a `FISCAL_*` function, confirm the org does **not** have custom fiscal years enabled; if it does, switch to calendar functions or a fiscal formula field.
4. **Write the clause correctly** — compare a date-function result to an **integer**, never a date literal; if the function is in `SELECT`, repeat it verbatim in `GROUP BY`.
5. **Decide time-zone basis** — if buckets must follow local days rather than UTC, wrap the field in `convertTimezone()`.
6. **Validate** — run `scripts/check_soql_date_functions.py --query "<your SOQL>"` (or `--manifest-dir` over a source tree) to catch date-literal comparisons and `SELECT`-without-`GROUP BY` mistakes.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Every date function in `SELECT` also appears, unchanged, in `GROUP BY`
- [ ] No date-function result is compared to a date literal (ISO `YYYY-MM-DD` or a relative literal) in `WHERE`
- [ ] `DAY_ONLY()` / `HOUR_IN_DAY()` are applied only to `DateTime` fields, not `Date` fields
- [ ] `FISCAL_MONTH/QUARTER/YEAR` are not used if the org has custom fiscal years enabled
- [ ] Time-zone intent is explicit — `convertTimezone()` wraps the field where local-day bucketing matters
- [ ] A relative window ("this year", "last N days") uses a date **literal** on the raw field, not a date function

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Comparing to a date literal is rejected** — `WHERE CALENDAR_YEAR(CloseDate) = 2026-01-01` fails; the function yields a number, so compare to the integer `2026`. This surfaces at query compile time and often confuses developers who mix up date functions with date literals.
2. **`FISCAL_*` silently unavailable under custom fiscal years** — enabling custom (generic) fiscal years disables `FISCAL_MONTH/QUARTER/YEAR`. Code that worked in one org throws in another purely because of that org setting, not the query.
3. **`DAY_ONLY()` / `HOUR_IN_DAY()` are DateTime-only** — pointing them at a `Date` field (or a formula returning `Date`) errors; they exist specifically to extract from a `DateTime`.
4. **UTC bucketing skews the "day"** — date functions read the raw UTC value, so late-evening local records fall into the next UTC day/month/quarter unless you wrap the field in `convertTimezone()`.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| A grouped SOQL query | `SELECT <dateFn>(field), <aggregate> ... GROUP BY <dateFn>(field)` for period rollups read via `AggregateResult` |
| A filtered SOQL query | `WHERE <dateFn>(field) = <integer>` for period filtering with no aggregation |
| `scripts/check_soql_date_functions.py` output | A report of date-literal comparisons, `SELECT`-without-`GROUP BY`, and misspelled-function issues in your SOQL |

---

## Related Skills

- `apex/apex-aggregate-queries` — owns the `GROUP BY` / `ROLLUP` / `CUBE` / `HAVING` / `AggregateResult` mechanics that date-function grouping plugs into; use it for the aggregation side.
- `apex/timezone-and-datetime-pitfalls` — the UTC-vs-local-day nuance and `convertTimezone()` usage that decides which bucket a record lands in.
- `apex/soql-fundamentals` — base SOQL clause structure, and SOQL relative date **literals** (`TODAY`, `LAST_N_DAYS:n`, `THIS_FISCAL_YEAR`), which are literals, not the functions this skill covers.
- `apex/soql-format-function-localization` — `FORMAT()` for localized display of the numbers/dates these functions return.
