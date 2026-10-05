---
name: quality-assurance
description: "\"Quality\" is unmanageable until it is a set of numbers with agreed definitions."
---

# Quality Assurance (Verbose)

## Core Patterns

### Defining Quality Operationally

"Quality" is unmanageable until it is a set of numbers with agreed definitions.
Four measures cover most of what teams need, and each answers a different
question.

**Defect escape rate.** Of all defects discovered for a release, the share found
after it reached customers.

```
escape_rate = defects_found_in_production
              / (defects_found_pre_release + defects_found_in_production)
```

Measure per release and trend it. A team that finds 90 defects internally and 10
in production has a 10% escape rate. Absolute defect counts are noise — they move
with feature volume, reporting culture, and how many people looked. The ratio is
what tells you whether your pre-release testing is aimed correctly.

Cut it by area, too. A 10% overall escape rate that is 45% in the billing module
tells you where to spend, which the aggregate hides.

**Change failure rate.** The share of deployments that cause degraded service —
requiring a rollback, a hotfix, or a forward fix under time pressure.

```
cfr = failed_deployments / total_deployments
```

Define "failed" before you measure: a rollback, an unplanned patch within N
hours, or an SLO breach attributable to the deploy. Whatever you pick, keep it
stable, or the trend is meaningless. Elite performers sit under 15%; teams above
30% usually have a release-safety problem, not a testing problem, and more test
cases will not move it.

**MTTR.** Median wall-clock time from customer impact beginning to customer
impact ending. Not from ticket creation — from impact. Detection time is usually
the largest component, which makes MTTR as much a monitoring metric as a repair
metric. Use the median, not the mean, and publish p90 beside it; one 14-hour
incident distorts a mean permanently.

**Defect age.** Median time between a defect being introduced (from `git blame`
on the fixing commit) and being detected. This is the honest measure of whether
shift-left worked. Escape rate can improve because you shipped less; defect age
improves only when feedback genuinely moved earlier.

A trap worth naming: any of these becomes a target and then a lie. If escape rate
is a team objective, defects get reclassified as "enhancements". Treat them as
instruments for the team's own steering, not as performance management inputs.

### Shift Left, Concretely

Shifting left means moving each check to the earliest stage that can run it,
because cost per defect rises with every stage it survives.

| Stage | Checks | Feedback | Cost of a defect caught here |
|---|---|---|---|
| Editor / pre-commit | Format, lint, types, secret scan | < 5 s | Seconds |
| Pre-merge CI | Unit, contract, changed-line coverage, migration up/down | < 10 min | Minutes, author still in context |
| Post-merge | Integration against containerised dependencies | < 30 min | An hour, context partially lost |
| Pre-release | Smoke and E2E on staging with production-scale data | < 1 h | Hours, plus a rebuild |
| Production | Canary metrics, synthetic checks, error-budget alerts | Minutes | Hours to days, plus customer impact |

Two rules make this real rather than aspirational. First, **every production
defect earns a test at the earliest stage that could have caught it** — not at
the stage where it was found. A null-handling bug caught in staging should
produce a unit test, not another E2E case. Second, **keep the pre-merge gate
under ten minutes**. Past that, engineers batch changes and start merging on
red, and the gate stops functioning regardless of what it contains.

Shift left also covers requirements. Ambiguity is a defect that has not been
written into code yet, and the cheapest place to find it is in a three-amigos
conversation about acceptance criteria before anyone opens an editor.

### Risk-Based Prioritisation

Testing effort is finite, so it must be allocated by expected loss rather than
spread evenly.

**Likelihood (1–5)** rises with change frequency, cyclomatic complexity, defect
history in that module, number of integration points, and how recently the team
touching it learned the code.

**Impact (1–5)** rises with revenue exposure, data-loss or corruption potential,
number of users affected, regulatory consequence, and how hard the failure is to
detect once live. A silent data-corruption bug outranks a loud crash.

| Area | L | I | Risk | Strategy |
|---|---|---|---|---|
| Payment capture and refunds | 3 | 5 | 15 | Unit + contract with PSP + E2E happy and failure paths + exploratory charter each release + rollback rehearsal |
| Authentication and session | 2 | 5 | 10 | Unit + integration + security review (`api-security`) + no flag-gated shortcuts |
| Order state machine | 4 | 4 | 16 | Property-based tests over transitions + integration + exploratory on partial/mixed orders |
| Search ranking | 4 | 2 | 8 | Offline evaluation set with regression thresholds; no E2E |
| Admin CSV export | 2 | 2 | 4 | One integration test on the happy path |
| Marketing footer links | 1 | 1 | 1 | Visual diff only |

Note the order state machine outranking payments here: it changes constantly and
corrupts data quietly. Rank by the product, not by which system feels most
important in the abstract.

Re-score quarterly and after any significant production incident. Risk is a
moving property — a stable module that gets a new owner and three refactors
becomes a high-likelihood area even though its code did not get worse.

### Exploratory Testing With Charters

Scripted and automated tests verify expectations you already had. They cannot
find a defect nobody imagined, and that class is where high-impact production
surprises live: unusual state combinations, cross-system workflows, timing
interleavings, and anything the spec left vague.

Exploratory testing is disciplined, not casual. Structure a session as:

> **Charter:** Explore partial refunds on multi-currency orders that were
> shipped in more than one parcel, using accounts with a stored card and a wallet
> balance, to discover rounding, ledger-imbalance, and double-refund defects.
>
> **Time-box:** 90 minutes.
>
> **Notes to capture:** setup used, actions taken, observations, bugs raised,
> areas left unexplored, new questions for the product owner.
>
> **Debrief:** 15 minutes with the developer who wrote the feature.

Charter selection follows the risk matrix, plus three heuristics: areas where the
specification is thin, workflows that cross service boundaries, and anything
recently rewritten. The output is not just bugs. Sessions routinely surface
missing requirements and gaps in the automated suite, and those gaps become the
next tests.

Session-based test management makes the activity reportable: charters attempted,
time on charter versus time on setup and bug investigation, defects found per
session. That is enough to justify the time without turning it back into a
scripted phase.

### Entry and Exit Criteria That Bite

A criterion that has never blocked anything is documentation, not a gate. Write
each as a binary condition with an owner and an enforcement mechanism.

**Entry to release validation:**
- All pre-merge checks green on the release commit — enforced by branch protection.
- Database migrations rehearsed forward *and* backward against a production-sized
  restore.
- New behaviour behind a flag defaulting to off.
- Rollback procedure written as an executable command, not a paragraph.
- Observability in place: the new code paths emit metrics and structured logs.

**Exit from release validation:**
- Zero open sev-1 or sev-2 defects. Not "triaged" — closed or explicitly
  accepted by a named person with a deadline.
- Smoke suite green against staging with production-scale data.
- Escape rate not worsening across the last two releases.
- On-call engineer briefed on what changed, what could break, and how to disable
  it.

The test of these criteria is whether anything has ever failed them. If not, they
are either trivially true or being waived silently, and both mean you do not have
a gate. Waivers are fine — they must be explicit, named, and time-boxed.

### Replacing the End-of-Cycle QA Phase

A dedicated testing phase after development fails structurally, not because the
testers are weak:

- Defects are found at maximum distance from their cause, when repair is most
  expensive and the author has lost context entirely.
- It creates a queue, and queues get compressed when dates slip — so the phase is
  always shortest exactly when the release is riskiest.
- It makes quality one group's responsibility, which reduces everyone else's care
  and converts the relationship into negotiation over severity.
- Feedback arrives too late to change design, so architectural testability
  problems are never fixed.

What replaces it is a set of gates spread through the flow: a definition of ready
that includes testable acceptance criteria; tests written alongside the code and
reviewed with it (see `code-review-practices`); contract tests at every service
boundary; progressive delivery behind flags; canary releases with automated
rollback on SLO burn; and production monitoring treated as the final test stage.

QA specialists do not disappear in this model — their work moves upstream and
becomes higher-leverage: risk analysis, charter design and execution, test
architecture, coaching developers on testability, and owning the quality metrics
themselves. That is a harder job than executing a regression script, and it is
the one worth staffing.

## Common Anti-Patterns

❌ **Reporting code coverage as the quality metric.** Coverage measures execution,
not assertion; a suite can execute every line and verify nothing.
✅ Track escape rate, change failure rate, MTTR and defect age; use coverage only
to find untested areas.

❌ **A hardening sprint before every release.** It is a scheduled admission that
defects are being batched to the end.
✅ Gate quality inside the flow so there is nothing left to harden.

❌ **Uniform test depth across the codebase.** The footer and the payment path get
equal attention, so the payment path is under-tested.
✅ Allocate by likelihood × impact and re-score after incidents.

❌ **Exit criteria nobody has ever failed.** They provide the feeling of control
without the function.
✅ Write binary, enforced criteria and record explicit, time-boxed waivers.

❌ **"Exploratory testing" meaning unscripted clicking.** Nothing is reproducible
and coverage is unknowable.
✅ Time-boxed charters with recorded notes and a debrief.

❌ **Re-running flaky tests until green.** The suite stops carrying information
and real regressions get re-run away.
✅ Quarantine and fix; treat flakiness as a defect (`flaky-test-remediation`).

❌ **Bug triage as a debate about severity.** Effort goes into classification
rather than repair.
✅ Publish severity definitions tied to customer impact and apply them mechanically.

❌ **Defect metrics used to evaluate individuals.** Reporting drops, defects get
reclassified, and the data becomes fiction.
✅ Keep the metrics as team-owned steering instruments.

## Quality Assurance Checklist

- [ ] Escape rate, change failure rate, MTTR and defect age defined in writing and tracked per release
- [ ] "Failed deployment" and defect severity levels defined and applied consistently
- [ ] Escape rate broken down by module, not only reported in aggregate
- [ ] Risk matrix exists with likelihood and impact scored per area
- [ ] Test depth allocated from the risk matrix; matrix re-scored quarterly and after incidents
- [ ] Pre-merge gate runs in under ten minutes
- [ ] Every production defect produces a test at the earliest stage that could have caught it
- [ ] Migrations rehearsed forward and backward on production-sized data
- [ ] Entry and exit criteria are binary, enforced, and have blocked something at least once
- [ ] Waivers explicit, named, and time-boxed
- [ ] Exploratory sessions chartered, time-boxed, and debriefed
- [ ] Charters targeted at thin specs, cross-system workflows, and recent rewrites
- [ ] Flaky tests quarantined and fixed rather than re-run
- [ ] Rollback path executable and rehearsed, not merely documented
- [ ] Production monitoring treated as a test stage with owned alerts
- [ ] No recurring hardening or stabilisation sprint on the calendar
