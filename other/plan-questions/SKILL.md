---
name: plan-questions
description: Question-quality rubric for AskUserQuestion calls during /plan mode. Triggers when the developer says /plan-questions, "ask better questions", "that question was confusing", or as a mid-session reset. Invoke it by name; the plugin no longer injects it automatically (the plan-question advisor hook was retired in 0.7.0).
---

# Plan-Mode Question Quality Rubric

Every `AskUserQuestion` call during `/plan` mode MUST satisfy these 10 rules.
If a question fails any rule, rewrite it before sending.

## The 10 rules

1. **Frame the WHY in one sentence.** The question body opens with what
   decision this affects in the implementation. Not "Which library?" but
   "We need to format trade timestamps for the CSV export endpoint at
   `OrderExportController.cs:88` — which library?"

2. **Reference concrete files/symbols.** Use `path/to/file.cs:42` or
   `ClassName.MethodAsync` in the question body or in option descriptions.
   No abstract phrasing like "the existing service" or "the relevant component".

3. **Each option states the concrete consequence.** What gets added,
   modified, or deleted. "Adds `XxxState` signal service + refactors
   `dashboard.component.ts`." Not "Use signals."

4. **Each option states the cost.** Lines touched, migrations created, new
   dependencies, blast radius. If two options have identical costs you are
   not really offering a choice — collapse them.

5. **One AskUserQuestion = one decision.** If the answer to question B
   depends on the answer to question A, split them and ask sequentially.
   Never bundle "which library AND which migration strategy?" into one call.

6. **Use `preview` for visual/structural differences.** Layout choices,
   code-structure variants, schema shapes — populate the `preview` field
   with an ASCII mockup, a code snippet, or a schema sample. Text labels
   alone cannot communicate visual differences.

7. **Recommend when you have an opinion.** First option = recommended.
   Suffix the label with " (Recommended)". The description must state
   *why* it is recommended in one phrase.

8. **Headers are the concrete artifact name.** "Index strategy", "Auth
   method", "Migration name" — not "Approach", "Strategy", "Option".
   Max 12 chars (per the AskUserQuestion schema).

9. **Bound open-ended questions.** If asking "which fields go in this
   DTO?", list the candidate fields. Never ask the user to invent the set
   from scratch — propose, then let them edit.

10. **Skip the question if you can read the answer.** Before asking, grep
    `CLAUDE.md`, the active concept contract under
    `.claude/concepts/`, the recent git log, the existing
    config file. Asking what is already documented wastes the user's time.

## Worked examples

### Example A — Library choice

**Bad:**

> Question: Which date library?
> Header: Library
> Options:
>   - date-fns
>   - dayjs
>   - luxon

**Good:**

> Question: We need to format trade timestamps for the CSV export at
> `OrderExportController.cs:88`. The output must round-trip through Excel
> (NYC time, no DST surprises). Which library?
>
> Header: Date library
>
> Options:
>   - dayjs + timezone plugin (Recommended) — 7kb, already a transitive
>     dep via `@angular/material`. Cost: 1 new import line.
>   - luxon — 22kb, native Intl API, no plugin needed. Cost: new
>     dependency in `package.json` + 1 import line.
>   - date-fns + date-fns-tz — 13kb, tree-shakeable. Cost: 2 new
>     dependencies, no Intl support without the tz package.

### Example B — Migration strategy

**Bad:**

> Question: How should we add the new column?
> Header: Approach
> Options:
>   - Nullable
>   - Default value
>   - Backfill

**Good:**

> Question: Adding `LastReviewedAt` (datetime2) to `Strategies` table
> (~50k rows). EF migration goes in `Persistence/Migrations/`. Which
> approach?
>
> Header: Column add
>
> Options:
>   - Nullable, no default (Recommended) — zero downtime, no row lock,
>     existing queries unaffected. Cost: every read must `??` the value.
>     Reversible.
>   - NOT NULL with `GETUTCDATE()` default — backfills 50k rows during
>     migration, ~2s table lock at our row size. Cost: irreversible
>     without manual SQL.
>   - Nullable now, backfill in a follow-up job, ALTER to NOT NULL later —
>     three deploys. Cost: highest operational complexity, safest for
>     >10M-row tables.

### Example C — Layout choice (uses preview)

**Bad:**

> Question: Which layout?
> Header: Layout
> Options:
>   - Two-column
>   - Stacked

**Good:**

> Question: The strategy-detail page at `features/strategies/detail/`
> needs to show metadata + live PnL chart. Viewport target is 1440px.
> Which layout?
>
> Header: Detail layout
>
> Options (with preview):
>
>   - Side-by-side (Recommended) — metadata 1/3, chart 2/3. Cost: 1
>     new `<div class="grid grid-cols-3 gap-4">` wrapper.
>     Preview:
>     ```
>     +---------------+-------------------------+
>     | Name          |                         |
>     | Status        |     PnL chart           |
>     | Symbol        |     (live signal)       |
>     | Last fill     |                         |
>     +---------------+-------------------------+
>     ```
>
>   - Stacked — metadata row above chart. Cost: same wrapper, easier
>     mobile reflow. Hurts dense-information feel.
>     Preview:
>     ```
>     +-------------------------------------------+
>     | Name  Status  Symbol  Last fill           |
>     +-------------------------------------------+
>     |                                           |
>     |              PnL chart                    |
>     |                                           |
>     +-------------------------------------------+
>     ```

## When to invoke

- Developer types `/plan-questions` or says "that question was confusing" /
  "ask better questions".
- Mid-plan, before any `AskUserQuestion` call, mentally walk the 10 rules.
- Plan mode is active and no reminder will arrive: the plan-question advisor hook that used to
  inject one at every prompt was retired in 0.7.0, so invoke this skill yourself.
