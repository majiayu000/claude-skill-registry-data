---
name: refresh-status
description: Resynthesize STATUS.md from the already-committed benchmark reports, PLAN docs, README claims, and the latest CI pipeline on main, without running any benchmark or editing any source doc. Invoke when a new report or pipeline has landed, a PLAN doc changed status, or the operator asks to refresh STATUS.md.
---

# refresh-status — regenerate STATUS.md from the committed reports and the latest CI run

This skill resynthesizes `STATUS.md` (repo root), the one-page capability summary, from whatever
`reports/BENCHMARK_*.md` reports are already committed, the root
`PLAN_*.md` design docs, `README.md`'s own claims, and the most recent CI pipeline result on
`main`. **It never runs a benchmark itself, never triggers a pipeline, and never edits any of the
source documents it reads.** If a source is stale, that staleness is what the refreshed STATUS.md
must say, honestly, not paper over — running a sweep or fixing a README gap is separate work
this skill's output should prompt, not silently substitute for.

STATUS.md lives at the repo root, not inside `reports/` — it's the front door that points into
that directory, not one of the reports itself.

> **Invoke it by telling a session:** *"Follow the `refresh-status` skill"*, or "refresh STATUS.md".

## When to run this

- A new or updated `reports/BENCHMARK_*.md` has landed (a fresh sweep, a re-measurement, a new
  axis).
- A new pipeline has resolved on `main` since STATUS.md's own cited pipeline ID.
- STATUS.md's "measured tree" line has fallen materially behind `package.json`'s current
  `version` — real capability work has landed since the last sweep and a reader deserves to know
  the gap exists, even before anyone re-benchmarks.
- A root `PLAN_*.md` changed status (a slice shipped, a plan retired to `archive/`, a new plan
  appeared).
- `README.md` changed, or enough time/capability drift has passed that its claims-vs-reality
  table is worth re-checking.
- The operator asks for it directly.

## Part 1 — the benchmark summary

1. **Enumerate the reports, don't hardcode the axis list.** `ls reports/BENCHMARK_*.md` (or
   equivalent) — whatever exists today is the whole input set. An axis added or retired since
   this skill was last run changes what gets enumerated, not this file.
2. **Read `reports/BENCHMARK_SUMMARY_*.md` first, if one exists.** A summary report is already a
   synthesis pass over the individual axis reports — prefer its cross-axis table as the primary
   source rather than re-deriving every number from each axis's own file independently. Spot-check
   two or three individual reports against the summary's claims for consistency before trusting it
   wholesale.
3. **For any axis with no summary entry** (a report exists but predates the summary, or there is
   no summary at all), read that report's own headline section directly: result, comparison to
   its prior baseline if stated, and its current gate/ceiling. Extract only what the report
   states — never estimate, round favorably, or infer a number the report doesn't contain.
4. **Cite every row's source file by name**, e.g. `reports/BENCHMARK_<AXIS>_<version>.md`.
   STATUS.md's whole value is that a reader can go verify any claim — a row without a source
   pointer next to it is a defect in the refresh, not a stylistic choice.
5. **Stamp the measured-tree version honestly.** Pull it from the newest report's own stated
   measurement version (usually named in the filename or the report's opening lines), not from
   `package.json`'s current version — those two numbers are allowed to differ, and the gap
   between them is exactly what the banner at the top of STATUS.md exists to say. Name
   concretely what has landed since the measured tree, in one or two sentences, drawn from
   `NEXT.md`'s recent history or `git log` — not a vague "things have changed."
6. **Carry forward the gates-ranked-by-leverage list** from the summary if one exists, or compose
   one from each axis's stated gate if not.

## Part 2 — the last CI pipeline

7. **Fetch the most recent pipeline on `main`**: `glab ci status --branch=main --compact` for a
   quick read, or `glab ci get --branch=main --output json` for the pipeline id/sha/timestamps,
   then `glab api "projects/<url-encoded-path>/pipelines/<id>/jobs?per_page=100"` for the full
   job list with per-job status and duration — the default page size silently truncates a
   pipeline over 20 jobs to 20, so always pass `per_page=100` or paginate. This repo's own
   pipeline already exceeds that count and keeps growing; read the real total fresh from the
   fetched pipeline rather than citing a fixed number.
8. **Report only a pipeline that actually finished** (`status: success` or a named failure), not
   one still running — if the latest is mid-flight, use the one before it and say so.
9. **Map every job to what it exercises at the consumer surface**, not just pass/fail. A job name
   alone doesn't tell a reader what got tested — say what page, CLI surface, or shipped artifact
   it covers. Group jobs sensibly (e.g. all `e2e-web-*` rows, then CLI/TUI, then package/deploy
   hygiene, then repo hygiene) rather than dumping the raw job list. If the CI config's job set
   has changed since this skill was last run (a channel added/split/removed), read
   `.gitlab-ci.yml` fresh rather than reusing a stale mapping from the last refresh.
10. **State the real numbers**: job count, pass count, wall-clock (pipeline `created_at` to
    `updated_at`, not the sum of job durations — jobs run in parallel), and the longest single
    job if it's a meaningful fraction of the wall-clock. Note any job that didn't run (gated on
    paths this push didn't touch, or schedule-only) rather than omitting it silently.
11. **If the pipeline had failures**, report them honestly — which jobs, and (if known) why —
    rather than only ever reporting a green run. STATUS.md's job is to say what's true, not to
    look reassuring.

## Part 3 — the design docs

12. **Enumerate `PLAN_*.md` at the repo root fresh each run** — `ls PLAN_*.md`, never a hardcoded
    list. A plan that ships fully retires to `archive/` (it stops being a root `PLAN_*.md`) and a
    new one can appear; both change what this table covers automatically.
13. **Read each plan's own opening status line first** — this project's convention is that every
    `PLAN_*.md` states its status in its opening lines. That's usually enough for the goal and
    delivered/remaining split; read further only when the status line doesn't already say what's
    shipped vs proposed vs design-only.
14. **Classify every remaining piece into exactly one of two buckets, never a third "impossible"
    bucket:**
    - **Design horizon** — an approach is known or straightforward to work out; what's missing is
      time, not a solved problem. Most `PROPOSED`/`DESIGN`-status items are this.
    - **Research horizon** — the plan itself names an open problem with no settled engineering yet
      (its own text says the literature doesn't cover some real combination the plan needs). Only
      classify something here if the plan's own text supports it — don't invent a research gap the
      doc doesn't name, and don't downgrade a real one to "just needs engineering" either.
    Per this project's own `CLAUDE.md` discipline: name the open problem plainly, never claim it
    is permanently unreachable — a research horizon is where the literature currently ends, not a
    wall.
15. **One table row per plan**, columns: plan, goal (one line), delivered, design horizon,
    research horizon (`—` if none). Cite nothing beyond what each plan's own text supports.

## Part 4 — the README audit

16. **Walk every `##` section of `README.md`** and extract its headline capability claim — not
    every sentence, the section's actual claim. Twenty sections is the going size; re-count
    fresh each run (`grep -n '^## ' README.md`), don't assume the prior count still holds.
17. **For each claim, fill three columns:**
    - **Implemented** — does the code exist? Name the module (`src/domain/...`,
      `src/services/...`).
    - **Consumer surface** — where does a real user actually meet it? Name it specifically: a CLI
      flag, a named web page (`chat.html`, `plan.html`, …), a published npm export, an MCP-style
      tool name. "The product" is not specific enough.
    - **Tested** — which tier, named: a unit test file/directory, an e2e file, a corpus lane. "It's
      tested" without a path is not verifiable.
18. **Then check the reverse direction**: real, shipped, tested capability that README's own
    narrative doesn't mention. This is the harder, more valuable half — a stale README under-sells
    what tmct does at least as often as it over-sells. Two known-good techniques:
    - Grep for a page's own filename (`research.html`, `ingest.html`, …) in README; a shipped page
      (check what `scripts/build-demo-site.mjs` actually emits) with zero mentions is a strong
      candidate — confirm it's genuinely undocumented (not just referred to by a different name)
      before reporting it.
    - Cross-check a fully-`BUILT`/shipped `PLAN_*.md` slice against README's narrative for the
      same capability area; a slice shipped and corpus/unit-tested with nothing in README
      describing what a user can now ask or do is a real omission.
    Report every finding as evidence (the grep, the file, the test), not an assertion — and don't
    claim exhaustiveness this skill's own procedure doesn't deliver; say what was actually checked.
19. **Note staleness in README's own numbers separately** (e.g. an inline benchmark table citing
    an old version) — that's a different defect from a missing claim, and conflating the two makes
    both harder to act on.

## Part 5 — write and ship

20. **Write `STATUS.md`** at the repo root, matching its existing section order (measured-tree
    banner → CI pipeline section → at-a-glance axis table → gates ranked → design docs table →
    README audit table → omissions list → site weight pointer → methodology pins → this refresh
    pointer) so a diff against the prior version shows only what actually changed.
21. **Commit** with the specific report filenames, pipeline ID, plan docs, and/or README sections
    that motivated the refresh named in the message. Update `NEXT.md` in the same commit if the
    refresh closes or narrows an item (e.g. a found README omission worth fixing separately).

## Execution — coordinator model

This skill's four read-heavy parts have different depth requirements; per `CLAUDE.md`'s
coordinator/sub-agent ladder, match the model tier to each, and don't staple a hard part onto an
easy batch (that prices the whole batch at the top tier). Running this skill solo end-to-end is
fine for a small drift (one new report, one pipeline); dispatch it when several parts need
refreshing at once.

- **Parts 1 and 2** (benchmark summary, CI pipeline) are largely mechanical: enumerate, read,
  cite, tabulate against an existing template. Sonnet-tier, or Haiku if the prior STATUS.md's own
  structure is given as a worked example to follow.
- **Part 3** (PLAN docs) needs real judgment — the design-horizon-vs-research-horizon call is a
  substantive read of each plan's own reasoning, not a lookup. Sonnet at minimum; Opus if several
  plans changed status since the last refresh and the classification calls are non-obvious.
- **Part 4** (the README audit) is the widest-reaching part — it requires cross-referencing a
  1000+ line README against `src/`, `test/`, and `test-e2e/`. This is
  a good candidate for its own dispatched sub-agent (worktree-isolated is unnecessary — this
  skill only reads, never edits source files) or a `fork` if run from an interactive coordinator
  session, since the grep/read legwork is high-volume and doesn't need to stay in the
  coordinator's own context. Sonnet is sufficient for the forward direction (claim → evidence);
  the reverse direction (finding omissions) benefits from a more capable model or a second
  independent pass, since it's the part most likely to under-deliver on a first try.
- **Part 5** (write and ship) is the coordinator's own job — it's synthesizing multiple
  sub-agents' output into one coherent page with a consistent voice and section order, which is
  exactly the kind of integration step that shouldn't be delegated further.

A reasonable dispatch shape for a full refresh: run Parts 1+2 and Part 3 as two parallel
sub-agents (no shared files — both only read and report back), Part 4 as a third parallel
sub-agent or fork, then the coordinator does Part 5 itself once all three report back.

## What NOT to do

- Don't touch any `reports/BENCHMARK_*.md` file itself — this skill only reads them.
- Don't backfill a number for an axis with no report. Say "not yet measured", and check
  `.claude/skills/` fresh for a `benchmark-*` skill that would produce it. Say that
  plainly rather than inventing one or leaving the axis out silently.
- Don't silently advance the "measured tree" version to match `package.json`'s current version
  without a real new report backing every number that changes — that would make STATUS.md's own
  central promise (numbers you can go verify) false.
- Don't trigger a new pipeline run to get fresher CI data — report the latest one that already
  ran, honestly dated.
- Don't touch any `PLAN_*.md` file itself — this skill only reads them and summarizes.
- Don't classify a design doc's remainder as "research horizon" unless the plan's own text names
  a real open problem; don't call a genuine open problem "just needs engineering" either. Both
  directions misrepresent what's actually left.
- Don't edit `README.md` as part of this skill — a found gap or a stale number is a finding to
  report, and real enough to fold into the current work per this project's "don't narrow scope on
  your own judgment" rule, but fixing README is a separate, reviewable change, not something to
  slip in silently while regenerating STATUS.md.
- Don't claim the README audit is exhaustive when it covered section headlines, not every
  sentence — say what was actually checked.
- Don't dispatch Part 5 (the write-up) to a sub-agent — synthesizing several parts into one
  consistent page is the coordinator's own integration work.
