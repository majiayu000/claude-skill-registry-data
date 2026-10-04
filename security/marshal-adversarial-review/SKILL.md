---
name: marshal-adversarial-review
description: >
  Get a candidate judged by a panel of independent, read-only reviewer agents - each pinned to the
  model that is actually good at its lens - and act on their reports. Use before a high-stakes
  merge, on a plan you are about to commit to, on a commit range you did not write, or to audit a
  repo. The engine runs the panel and hands you one report per reviewer plus a unified one; it
  computes no verdict. This playbook is the judgment: which panel to reach for, how to write a
  lens, and how to read several independent reviews and decide.
---

# Reviewing with an adversarial panel

One reviewer gives you one opinion, and an agent asked for "overall quality" reliably produces a
polite paragraph. A **team** is a panel of reviewers that each hold ONE lens and review the SAME
subject in parallel isolation, each writing its own report. Disagreement between them is the
product - it is where the real risk usually is.

`run_team` does the mechanism: fan-out, isolation, collecting the reports, persisting them. You do
the judgment - all of it. There is **no verdict, no tally, and no pass/fail**: a decision derived
from reviewer prose can be forged by the material under review, and it hides exactly the
disagreement you convened the panel to see. The engine never integrates either.

## When to reach for a panel
- Before integrating a risky or valuable diff - a public API, a migration, a security-sensitive path.
- On a **plan**, before anyone writes code. The cheapest place to kill a bad idea.
- On a **commit range** you did not write, or an **audit** of an unfamiliar repo.
- Not for every change. A panel costs N agent runs; a one-line fix does not need three opinions.
  For a single second opinion, `marshal-orchestrate` step 4 is enough.

## 1. Pick the team
`list_teams()` shows the declared panels with their target and roles. Teams live in
`<repo>/teams/*.yaml`; two starters ship in `examples/teams/`. Match the team's `target` to what you
are actually reviewing (`run` / `plan` / `range` / `audit`) - a mismatch is refused up front.

If no team fits, author one. A team is:

```yaml
description: what this panel is for
target: run
roles:
  - name: correctness
    client: codex-readonly   # MUST be a read-only client
    rubric: |
      <one lens, stated as what to hunt and what counts as evidence>
```

### Writing a lens (this is where panels live or die)
- **One lens per role.** "Correctness" or "tests" or "operability" - never "quality" or "review this".
  A broad rubric collapses the panel back into one opinion wearing three hats.
- **Say what counts as blocking.** The best rubrics define the evidence bar: "describe each defect
  as a concrete failure case - the inputs and the wrong result", "call something blocking only with
  a cited rule clause". Without that you get vibes, and vibes read exactly like findings.
- **Route each lens to a different model.** This is the whole point of a heterogeneous panel - one
  model's blind spot is another's strength, and the ledger then tells you what each provider cost
  per finding. Three roles on the same client is three samples of one opinion.
- **Reviewers must be read-only clients.** A role pointed at a `safe-edit` client is a config error
  raised before anything spawns. Add dedicated `permission: read-only` entries to
  `fleet.config.yaml` - a reviewer that can edit is not a reviewer.

## 2. Run it
```
run_team(name="hard-gate", target="run", run_id="<candidate>")
run_team(name="plan-review", target="plan", text="<the plan>")
run_team(name="hard-gate", target="range", base="main", head="feature")
```
All roles go out together under one `task_id`, so they cannot see each other and `usage()` prices the
whole review as one unit.

**Scope a large `range` review with `paths`.** The subject is truncated at the *tail*, and git orders
paths alphabetically - so on a big change `src/` and `tests/` are exactly what gets cut. But scoping
is a trade: a reviewer that cannot see `docs/` or `CHANGELOG.md` will correctly report that it cannot
verify whether they were updated. Include the paths a lens needs to reach its conclusion, and read
"could not check" in a report as the honest signal it is, not as a finding against the code.

## 3. Read the unified report first, then the individual ones
`unified_report` is written for you: it shows the panel's shape, who reviewed from which lens, every
review inline, and who did not report. Read it to orient, then open the individual reports
(`reviews[].review`, or the files under `report_dir`) for any lens whose objection matters.

Then do the work the engine deliberately does not:

1. **Collect the objections.** Walk each report's Blocking and Findings sections and pull out what
   is actually claimed. Two reviewers naming the same problem is a much stronger signal than one.
2. **Weigh them.** A finding with a concrete failure case ("given X, this produces Y") outranks a
   stylistic worry, regardless of how confidently either is phrased. An objection you cannot follow
   is not automatically wrong - go look at the code it cites.
3. **Notice disagreement.** If one lens is satisfied and another is alarmed, that gap is usually
   where the real risk lives. Nothing has averaged it away for you.
4. **Decide, and say why.** You are the only one who can.

Two things to check before you trust the panel at all:

- **`incomplete_roles`** - reviewers that produced no whole report (broke, timed out, backend
  missing, exited cleanly having narrated instead of reviewing, or had their report cut off by the
  record's text cap). That lens is simply **missing**, not satisfied. Re-run it, or proceed knowing
  what was never looked at. Check `review_truncated` to tell the two apart: a narrator has nothing
  worth reading and should be re-run, while a cut-off report is real findings as far as it got -
  read the rest with `get_run_log` rather than spending another run.
- **`truncated`** - the subject exceeded the reviewer size cap and was cut, so the reviews cover
  only the visible part. On a large diff, split it and review the pieces.

`report_dir` holds `<role>.md` per reviewer plus `README.md` - link it when you hand the outcome to
a human.

## 4. Act
- **If you accept an objection:** dispatch ONE fix task addressing **only** what you accepted (quote
  the reviewer verbatim so the worker sees the original claim, not your paraphrase). Re-review the
  new candidate. Cap at ~2-3 rounds - stop and bring in a human if the same objection survives twice,
  or if two lenses demand opposite changes.
- **If you reject an objection:** say so and why, in your own summary. A dismissed finding that you
  can articulate a reason against is a decision; one you skipped silently is a gap.
- **If you proceed:** you still read the diff yourself. A panel is several second opinions, not a
  substitute for looking. Then `integrate(run_id)`, one run at a time (see `marshal-orchestrate`
  step 5 for `merged` / `conflict` / `blocked` / `empty` / `error`).
- **Judge the reviewers themselves:** `set_outcome(<reviewer_run_id>, "advisory", note?)` for each
  panel member whose report you actually used. Reviewers merge nothing by definition, so
  `advisory` is their verdict - `abandoned` reads as giving up, and would count a review you acted
  on against that client's integration rate for a merge it could never have produced. Use
  `rejected` when the findings were wrong or off-contract; leave a missing lens unjudged, since
  nobody reviewed it. This is what makes `routing` able to tell you which reviewer is worth
  spending on.

## Invariants to respect
- Reviewers are headless and read-only: the rubric + subject is all they get; no questions possible.
- Never show a reviewer another's report, and never re-run a panel with the earlier reports in the
  prompt - that destroys the independence the whole thing rests on.
- A missing report is a missing lens, never approval. `completed` describes the *run*, not the
  review's merits - it says an agent finished cleanly AND wrote a whole report that answers the
  contract, nothing about whether it liked what it saw. An agent that exits 0 without reporting is
  incomplete, not approving; so is one whose report stops mid-way.
- `succeeded` is not `correct`, and "nobody objected" is not `correct` either. Main is untouched
  until you integrate.
