---
name: compact-dev-environment
description: 'Compact the Senzing Bootcamp plugin development environment — propose consolidating overlapping or superseded invariants (as blocks for /review-invariants), census the frozen specs archive read-only, merge redundant test traversals, and prune stale feedback — without losing the reasoning future development depends on. Use when the maintainer wants to clean up, tidy, prune, consolidate or de-duplicate the dev environment, when INVARIANTS.md has grown unwieldy, or when the specs/tests backlog is slowing work down. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[asset class: invariants | specs (read-only census) | tests | feedback] (omit to census all four)"
---

# Compact the development environment

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It reviews the four things that accumulate — **invariants, specs, tests,
feedback** — and reduces what future development must carry, without losing what
future development needs to know.

**Why "compact" and not "clean".** Cleaning implies removal; the job here is
compaction in the database sense — same information, less to drag along. Almost
every good outcome of this skill is a *merge*, not a delete: invariants consolidated
through `/review-invariants`, test traversals combined. Specs take no part in it: they
are read, never moved, annotated or deleted (INV-307). The name matters because the
failure mode is a maintainer who runs a "clean" skill and loses the reason a rule
exists.

## The one thing to understand before touching anything

The four asset classes look similar and behave completely differently, because
each is either an **address** other things point at, or a **record** that stands
alone. Measured in this repo on 2026-10-24 (#808; the 2026-07-31 figures were 4,981 and 813):

| Asset | What it is | Citations | Safe operation |
|---|---|---|---|
| Invariant `INV-NNN` | an **address**: 27,660 live citations across plugin text, specs, tests and skills (`citations.py census`) — **plus 3,246 in commit messages, which cannot be edited** | very high | propose a merge, supersession or demotion as a block for `/review-invariants` — **never renumber casually** |
| Spec file | a **record** in the frozen archive (INV-307); its address is the `## <name>` heading in `IMPLEMENTED.md` | moderate | read only: never moved, annotated or deleted |
| Test | **enforcement**; deleting one silently removes a guarantee | n/a | merge traversals, never merge assertions |
| Feedback archive | a **record**; its address is the `entry_id` hash in `feedback/PROCESSED.jsonl` | low | prune files, **never prune ledger lines** |

**Never break an address. Feedback records may be pruned; spec records stay as they are
(INV-307).** That single rule decides most calls this skill has to make.

⚠️ **Re-measure these numbers; do not cite them.** The 2026-07-30 versions of the
two figures above were **wrong the day they were written** — the table claimed
5,210 live citations and Step 2 claimed 43 uncited invariants, while the tools
shipped in that same commit (`f4a8e56`) reported **4,587** and **93**. Neither
tool has been modified since, so there is no counting-method explanation; they
were simply never measured. The 43 was the costlier one, because Step 2 built a
whole guidance section on it: a later maintainer seeing 91 would reasonably infer
that ~48 invariants had lost their enforcement, when the real movement was
93 → 91, i.e. slightly better. This is the failure Step 4's first item describes —
a false claim made load-bearing — occurring in this skill's own prose, where
re-measuring never reaches it because a reader trusts the stated figure instead.
So: run Step 1, use what it prints, and treat every number in this file as a
dated illustration of scale.

## Renumbering invariants: read this before proposing it

Renumbering is the operation maintainers ask for most and the one with the worst
cost/benefit in this repo. `specs/INVARIANTS.md` forbids it in its own rules
("IDs are permanent references"), and the reason is measurable rather than
stylistic:

- **Thousands of `INV-NNN` citations live in commit messages** — 2,321 when last
  measured, 2026-09-24, and one more with every commit that cites one. Git history is
  immutable, so none of them can be corrected. ⚠️ **Re-measure rather than quoting that
  figure**; it is here to show the order of magnitude, and the argument does not depend
  on the exact value.
- After a renumber, those citations do not dangle — they **silently resolve to a
  different real invariant**. A 2026-07-30 commit explaining a fix to "INV-132"
  would, post-renumber, point at whatever now holds 132. Dangling references get
  noticed; wrong-but-plausible ones do not.
- The same applies to the three archived feedback files and to any spec text
  quoting a historical decision.

So: **the default is consolidation without renumbering.** Merging two invariants
into one new ID and marking both superseded achieves "consistent, coherent,
concise" with no address broken — the file gets shorter and every old citation
still resolves to something true.

If the maintainer directs a renumber anyway, it is a separate, explicitly
authorized operation and it MUST:

1. Be **all at once** — never a partial renumber; two numbering schemes in flight
   is unrecoverable.
2. Ship a permanent, machine-readable `RENUMBERING.md` map (`old → new`, with the
   date) **at the repository root**, kept forever, so a historical citation can be
   resolved by hand. ⛔ **Not under `specs/`** — it holds live records only (INV-307), the
   table in `specs/README.md` is the list of the files that belong there, and the frozen
   archive of the spec files is in the repository `specs/README.md` names. The instruction
   this replaced put the map under `specs/` while that directory was the frozen archive, so
   it could not be carried out at all: following it turned the suite red. ⚠️ Not under
   `docs/` either: this repository's `docs/` is not published.
   `python3 -m tools.bootcamp_build promote` writes only every assistant's package under
   `plugins/`, each assistant's catalog file, the public repository's `docs/` from `site/`,
   and each file under `public/` at the same path from the root. The root is inside a
   tagged release — which is what a child needs, since children key their
   inherited-invariant registers on the parent's `INV-NNN`.
3. Rewrite every live citation mechanically (never by eye) and then pass
   `citations.py verify` with zero unresolved and zero unexpected IDs.
4. State in the report, plainly, that every `INV-NNN` citation in a commit message is
   now wrong and that `RENUMBERING.md` is the only way to read them. **Measure the
   figure at renumber time and give it with its date** — do not quote one from this
   file. `git log --format=%B | grep -oE 'INV-[0-9]{3}' | wc -l` is the count.
   ⚠️ This step used to name a literal **813**, measured 2026-07-31 and never
   re-measured; by 2026-09-24 the real figure was **2,321** and rising with every
   commit. A number a document tells you to quote stops being a dated illustration
   whatever the caveat above says — which is the failure the section two above this
   one exists to describe, reproduced here.

Item 4 is not a formality. A maintainer who has not been told this will later
read old commits and be misled by them.

## Scope and guardrails

- **Report first, change second.** The default run produces a plan and changes
  nothing. Every destructive step is separately confirmed by the maintainer, one asset
  class at a time.
- **Compaction targets duplication *across* invariants, never rationale *within*
  one.** These invariants read long because each carries the failure that produced
  it — that narrative is what stops the rule being re-argued or re-broken. Cutting
  it makes the file shorter and the project dumber. Merge overlapping rules; keep
  every "observed:" clause that names a real defect.
- **Nothing is removed before a citation census.** `citations.py census` first,
  always. An invariant cited by shipped plugin text or by a test is load-bearing
  whatever it looks like in isolation.
- **A test is a guarantee.** Deleting one removes a promise. Merge traversals for
  speed; never merge two assertions into one, and never delete a test without
  naming which invariant or behavior loses its enforcement.
- **`IMPLEMENTED.md` and `PROCESSED.jsonl` are append-only.** They are the ledgers
  that make specs and feedback re-findable. Archived feedback files they point at may
  be pruned, and the specs they point at stay where they are (INV-307); the ledger
  lines never go.
- **Git is not a backup for the working set.** "It's in history" is true and
  nearly useless — nobody greps history for a rule they don't know exists. Use it
  to justify pruning *records*, never to justify dropping a *rule*.
- **Respect `@INVARIANTS.md`** — including its own maintenance section, which this
  skill is uniquely positioned to violate.

## Step 1: Take the census

**The argument scopes the assessment, never the census.** With no argument, take the full
census and assess all four classes, then propose a plan: breadth is cheap here, and it is
the *acting* that is expensive. With an argument naming a class (`invariants`, `specs`,
`tests` or `feedback`), still take the full census, because the census is what makes any
removal safe, and scope only the assessment and the plan to that class.

```bash
python3 .claude/skills/compact-dev-environment/citations.py census
python3 .claude/skills/compact-dev-environment/citations.py verify
python3 .claude/skills/dry-run/coverage_reports.py invariants   # invariants no test cites
```

`census` reports every `INV-NNN` with where it is cited (plugin / specs / tests /
skills), every spec file against its ledger heading, and the feedback archive
against its ledger. `verify` is the referential-integrity check — run it again
after every change in this skill and require it to stay clean.

Record the baseline numbers. The report in Step 6 is meaningless without a
before/after.

## Step 2: Assess the invariants

Read `specs/INVARIANTS.md` in full. Sort every invariant into one of five:

| Verdict | Means | Action |
|---|---|---|
| `load-bearing` | states a rule still true, cited or enforced | keep, untouched |
| `mergeable` | two or more invariants state **one** rule from different angles | propose a merge (below) |
| `superseded` | its rule is now stated by a later invariant | propose a supersession (below); never delete |
| `unenforced` | no test cites it and none could | see below — usually a keep |
| `not-an-invariant` | guidance or preference, not a testable MUST | propose a demotion (below) |

**Merging is the main win.** Two invariants that say one thing become one new
invariant, with both originals marked superseded by it. The file gets shorter, the
rule gets clearer, and every existing citation still resolves. Propose merges only
where the rules are genuinely the same — an invariant that is a *special case* of
another is not a duplicate, and collapsing it loses the case.

### Merges, supersessions and demotions are blocks for `/review-invariants`

⛔ **This skill never edits `specs/INVARIANTS.md` and never mints an id.** (INV-365) It
proposes, and `/review-invariants` decides. After the maintainer's explicit yes in Step 6,
it appends one dated entry to `specs/IMPLEMENTED.md` holding the blocks below, then tells
the maintainer to run `/review-invariants`. A run that finds nothing mergeable,
superseded or demotable writes no entry.

- **A merge:** one `DEFERRED INVARIANT` block for the merged rule, with its drafted id
  written as `INV-NNN`, and one `PROPOSED AMENDMENT` block per original, marking it
  superseded by the merged rule.
- **A supersession:** one `PROPOSED AMENDMENT` block on the superseded invariant, naming
  the later invariant that now states its rule.
- **A demotion** (`not-an-invariant`): one `PROPOSED AMENDMENT` block marking the
  invariant demoted. A change to `ground-rules.md` wording is filed as a GitHub issue
  instead, because that file is plugin text, and plugin text changes through an issue.

Write each block as [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one)
shows (INV-300). An amendment names the real id it
amends; only the merged rule's drafted id is `INV-NNN`. Then run
`python3 .claude/skills/review-invariants/pending_invariants.py list` and confirm every
block is queued.

**Why they are routed this way.** Minting an id is the maintainer's alone,
through `/review-invariants`, and `INVARIANTS.md` changes only by a dated correction
appended beneath the original. A merge needs a new id, and a supersession or a demotion
changes a rule already in force, so each one is a decision rather than mechanical work.
Sending one to `/implement-github-issue` *(user level)* does not help: that command
cannot mint either (INV-309), and it writes a block in place of the change. Writing the block here
puts the decision in the queue `/review-invariants` already walks, with the census this
run took beside it.

**On the ~91 invariants no test cites** (measured 2026-07-31): "no test cites it"
is a prompt, not a verdict. Three different things produce it:

- The invariant governs **prose the tests do not read** (module wording, question
  phrasing) — add a test if one is cheap, otherwise keep it and say so.
- The invariant is **enforced by a test that does not name it** — the guarantee is
  real, the citation is missing. Fix the citation, not the invariant.
- The invariant is **unenforceable by construction** (it constrains a live
  bootcamp run). Keep it. An unenforceable rule is still the thing that stops the
  next person doing it wrong.

Only the third case with *no* remaining relevance is a demotion candidate.

## Step 3: Census the specs (read-only)

⛔ **Specs are read, never moved, annotated or deleted (INV-307).** `specs/` holds live
records only: the table in `specs/README.md` is the list of the files that belong there,
and no new file is written there. The spec files, frozen since 2026-09-15, are in the
archive repository `specs/README.md` names, at the commit it pins. A spec
is a record of a decision; the ledger heading is what makes it findable, and this step
checks that link without acting on it.

So the `specs` class has one verdict, **leave**, and the Step 6 report says so. `census`
still reports every spec file against its `IMPLEMENTED.md` heading. What it can surface
is a broken link — a heading with no spec file, or an invariant `Source:` that does not
resolve — and that is a `verify` problem to report, never a spec to change.

- **Implemented and stable** → leave them. ⛔ **Archiving was measured on 2026-07-30
  and rejected**; an earlier draft of this skill recommended it, wrongly. Three
  findings: (a) the benefit is **3.5 ms** — spec discovery over 215 files is a glob,
  and no maintainer reads 212 spec files, they read the computed list; (b)
  `feedback-to-issues` Step 4 lists **every** `specs/*.md` to deduplicate against, so
  hiding implemented work from that list would let it write duplicates of solved
  problems, silently; (c) `tests/test_spec_ledger_invariants.py` resolves an
  invariant's `Source:` via `SPECS / f"{name}.md"`. The reading burden is
  `IMPLEMENTED.md` (2,986 lines) regardless. The 2026-09-15 freeze then settled the
  question for good, so there is nothing here to revisit.
- **Implemented but the change was later reverted or superseded** → leave the spec as
  it is. It now reads as describing shipped behavior, so name it in the report; the
  correction lives where live work records it (the issue that superseded it, and that
  issue's `IMPLEMENTED.md` entry), never in the spec.
- **Cited as a `Source:` by an invariant** → leave. The name must stay resolvable, and
  `verify` checks that it does.
- **Never implemented and no longer wanted** → leave, and name it in the report. If
  the maintainer decides not to build it, that decision is recorded in
  `specs/DECLINED.md`, the live record for it; the spec file stays.

⛔ **No spec changes to make a count smaller (INV-307).** `IMPLEMENTED.md` was 2,986
lines on 2026-07-31 and is the actual reading burden; the spec files are looked at one
at a time, so even before the freeze, removing one helped nothing and cost provenance.

## Step 4: Assess the tests

⛔ **Speed is not the reason to touch these tests.** Measured 2026-07-30: the four
files that walk the corpus more than once run in **~0.3 s each** against 42 files /
786 KB, while the suite's 67 s is dominated by PDF rendering (six tests at ~1.5 s
doing real fpdf2 work). An earlier draft of this skill cited "17 separate walks" and
implied consolidating them mattered; the count conflated `glob` with `rglob`, the real
figure is nine files, and the saving is unmeasurable. **Do not consolidate for
performance** — the churn risks the failure messages, which in this suite are most of
a test's value. Consolidate only where one file genuinely re-reads the corpus for
checks that belong together.

When you do combine, **combine the traversal, never the assertions.** The right shape reads each file
once and runs N independent checks, each in its own `subTest`:

```python
for path in shipped_markdown():
    text = path.read_text(encoding="utf-8")
    for name, check in CHECKS:
        with self.subTest(check=name, file=path.name):
            self.assertEqual([], check(text), ...)
```

One walk, N results, and a failure still names *which* check on *which* file.
The anti-pattern is `assertTrue(a and b)`: it halves the walk and destroys the
diagnosis, which in this repo is most of a test's value — the suite's failure
messages routinely explain the defect better than the code does.

**The findings that are actually worth hunting**, in value order — the 2026-07-30 pass
took item 4 and left the rest standing:

1. **A test pinning a premise that has gone stale.** Worse than no test: it makes
   a false claim load-bearing and fails the suite when someone corrects the truth.
   Three were found on 2026-07-30, all asserting the plugin still *said* something
   the MCP server had since contradicted. Look for assertions that pin the
   *absence* of a capability, or that quote wording rather than behavior.
2. **A test whose subject was deleted** — passes vacuously forever.
3. **Duplicate coverage** — two files asserting the same guarantee. Keep the one
   whose failure message is better; delete the other only after saying which
   invariant it cited.
4. **A vacuous scan** — a glob that no longer matches. Every corpus-walking test
   needs a not-vacuous guard, and this repo already uses that idiom
   (`test_the_scan_is_not_vacuous`); add it where it is missing.

   ⚠️ **Grep cannot find this — read every hit, or report nothing.** On 2026-07-31 a
   line-based scan for a count assertion flagged **ten** files as unguarded. On reading
   them, **all ten were false positives** and the real answer was *zero* — every
   corpus-walking test in this repo is already guarded. Four distinct reasons, each of
   which will recur:

   - **The guard spans lines.** `assertGreaterEqual(\n  len(...)` does not match a
     single-line pattern (`test_markdown_is_actually_being_scanned`,
     `test_the_check_is_actually_scanning_deferrals`).
   - **The guard names a member instead of counting.**
     `test_generated_html_deliverables.py` asserts two specific filenames are in the
     sweep's result. That is *stronger* than a count — a count passes on the wrong
     files — so a detector looking for `assertGreater` scores the better idiom as absent.
   - **Empty is the pass condition.** `test_verbatim_check_limitation.py` asserts
     `assertEqual([], PLUGIN.rglob("sz_verbatim_check*.py"))` — the plugin must ship no
     copy of the checker. A not-vacuous guard there would invert the test.
   - **The glob is over a fixture the test just created**, not the corpus
     (`test_feedback_ledger.py` globs its own tmpdir). Vacuity is impossible.

   So do not report this class from a grep at all. The signal is narrow — a glob over a
   **real** corpus path whose results are *iterated* rather than *asserted about*, with
   no count check **and** no named-member check anywhere in the file — and confirming it
   means reading the file. A ten-hit list relayed as ten findings is how a clean result
   gets reported as a backlog.

## Step 5: Assess the feedback

Check the actual size before proposing anything. On 2026-07-31 the archive was
**4 files, 80.4 KB, 28 ledger entries** — not a burden, and no pruning was
warranted. Say so rather than inventing work; a skill that always finds something
to delete is a liability.

The more useful check at this size is not the total but **whether every entry has a
disposition**: `census` reports that, and an entry left at `unrecorded` has lost the
entry→spec link the ledger exists to hold. Correct one with
`feedback_ledger.py annotate <entry_id> <disposition>`, which appends a superseding
line — the ledger reads last-wins and is never edited in place.

⚠️ **Read the ledger last-wins, and do not trust a single `unrecorded` line.** On
2026-07-31 `census` reported one entry with no disposition; the *next line in the
ledger* already named its spec, because it had been corrected on 2026-07-28. The bug
was in `census`, which read raw lines instead of collapsing by `entry_id` — and the
run wasted an append "fixing" a ledger that was already right. `feedback_state()` now
collapses last-wins and reports how many lines were superseded, and
`tests/test_citation_census.py` pins it. The general lesson outlives the bug: in an
append-only ledger, **the presence of a bad line is not evidence of a bad state** —
only the last line for a key means anything.

When it does grow:

- **`feedback/PROCESSED.jsonl` is never pruned.** It is content-addressed dedup;
  dropping a line makes an old feedback file re-processable, and the next
  `feedback-to-issues` run re-files work already done.
- **Archived `.md` files may be pruned** once every entry they carry is in the
  ledger with a disposition, and every spec they produced exists. `census` checks
  exactly that.
- **Pruning does not remove the PII.** These files are committed deliberately
  (see `feedback/README.md`) and contain bootcamper details; deletion from the
  working tree leaves them in history. Never offer pruning as a privacy measure —
  if privacy is the goal, that is a history-rewrite conversation, not this skill.

## Step 6: Report, then act on the confirmed subset

Report before/after numbers per asset class, then the plan as a table:

| Asset | Verdict | Proposed | Citations at risk |
|---|---|---|---|
| `INV-0xx` + `INV-0yy` | `mergeable` | blocks for `/review-invariants`: a merged rule at `INV-NNN`, an amendment per original | 14 live, 0 broken |
| `specs/` | frozen archive (INV-307) | leave | ledger headings resolve |
| `tests/test_a.py` + `test_b.py` | duplicate walk | one traversal, subTest per check | — |
| feedback | below threshold | no action | — |

Then:

- **Invariant changes go to `/review-invariants` as blocks** — merging invariants,
  superseding one, demoting one (Step 2). After the maintainer's yes, append the entry
  holding the blocks to `specs/IMPLEMENTED.md`, confirm `pending_invariants.py list`
  queues each one, and tell the maintainer to run `/review-invariants`.
  ⛔ **Never edit `specs/INVARIANTS.md` here.** (INV-365)
  ⛔ (INV-309) Never send an invariant change to `/implement-github-issue` *(user level)*,
  which cannot mint either.
- **Other semantic changes go through a GitHub issue** — deleting a test, or the
  `ground-rules.md` wording a demotion needs. File it once the maintainer has said yes
  to that issue's exact text (INV-314), or one yes for the whole list shown in one message
  (INV-314, 2026-10-13 note), under the conditions in
  `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes", and let
  `/implement-github-issue` *(user level)* execute it. The issue is where the reasoning survives.
  ⛔ **(INV-318) Never apply the `unattended-ok` label to an issue this run files.** Choosing
  what `/unattended-issue-loop` *(user level)* works with nobody watching is the maintainer's
  decision alone.
- **Mechanical changes may be executed here**, one class at a time, each with the
  maintainer's explicit yes: merging test traversals, pruning feedback files. After
  each, run `citations.py verify` and the full suite, and report both.
- **Renumbering, if authorized at all, is last** and is its own confirmation.

⛔ **Never batch a delete with a move.** If a run does both, a maintainer
reviewing the diff cannot tell which was which, and the delete is the one that
needed the attention. This binds the feedback files, the only records this skill
prunes; specs are neither moved nor deleted.

Close by stating what was *not* compacted and why — an asset class you examined
and left alone is a result, and saying so stops the next run re-deriving it.
