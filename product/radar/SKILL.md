---
name: radar
description: >-
  Per-repo SDLC process coach and strategic compass over the last 2-3 weeks of activity.
  Delivers a user-friendly narrative that celebrates high-level wins, evaluates engineering momentum,
  diagnoses process health, and identifies potential regressions alongside recurring defect clusters.
  Under the hood, it rigorously analyzes Run/Grow/Transform flow distribution, checks open-PR collisions,
  and flags release plan drift. Scans for historical reports across RADAR/, docs/radar/, or
  PROJECT/1-INBOX/ to track multi-week trajectory arcs and offers long-horizon retrospectives.
  Analysis is read-only; findings persist to two sinks (an immutable dated report doc + one live
  radar-labeled issue checklist) so they survive across sittings. Use when the operator asks
  "how is our development cycle going", "what have we actually been doing", "are we just fixing bugs",
  "what keeps breaking", "did we introduce any regressions", "summarize radar history", "radar arc",
  "summarize radar reports", "what should we fix once to stop the bleeding", "is the plan still right",
  "strategic review", "impact review", "run the radar", "/radar", or "/radar --arc". Not for end-user
  shipped recaps (weekly-shipped), not for ranking marathon candidates (start-marathon), not for
  maturity assessment (/honest), and it never executes fixes (/10days does that).
---

# radar

A per-repo SDLC process coach and strategic compass: pairs a friendly, constructive engineering narrative
(celebrating high-level wins, coaching process health, and spotting potential regressions) with three
rigorous empirical lenses over one window, persisting to a reconcilable report.
Every claim cites a commit, file, or issue. Tracking issue: GH-442.

---

## Recite this — verbatim, as the first thing in your first response

> **Radar Discipline:**
> 1. **Frame window & discover historical arc (Step 0).** Default to 21 days on trunk (`main`/`development`); discover prior reports in `RADAR/`, `docs/radar/`, or `PROJECT/1-INBOX/` to extract historical baseline RGT metrics and multi-week trajectory.
> 2. **Prove flow distribution & RGT mix (Step 1 — Lens 1).** Pipe trunk commit subjects to a verified tally file, prove counts sum to `wc -l`, isolate Harness machinery from the denominator, classify Run/Grow/Transform (Transform strictly declared via `rgt: transform`), and report Unclassified drift.
> 3. **Cluster defects, detect regressions & check PR collisions (Steps 2–2b — Lens 2).** Mine 9 evidence signals to isolate chronic debt and short-cycle regressions (applying $\ge 2$ days / $\ge 2$ PRs recurrence discriminator); score targets, and cross-check open PRs to prevent duplicate scheduling.
> 4. **Audit release alignment & orphan backlog (Step 3 — Lens 3).** Read `releases.db` and open milestones read-only; measure orphan issue share and surface roadmap plan-vs-execution drift without modifying database state.
> 5. **Deliver coaching memo & persist dual sinks on confirmation (Steps 4–5).** Present the SDLC Process Coach narrative (celebrate wins, coach process friction, highlight regressions, offer multi-week arc); upon single operator confirmation, write immutable Sink A (`RADAR-REPORT-*.md`) and sync live Sink B (`radar` issue checklist).
>
> **Overall Goal:** SDLC process momentum evaluated across 3-lens empirical evidence (RGT flow, defect/regression clusters, release alignment), synthesized into an actionable coaching memo, and persisted to dual historical/live sinks on operator approval with zero unconfirmed mutations.

Then begin work.

---

## Guardrails

- **Analysis reads; only the report writes.** The two report sinks (Step 5) are the *only* writes.
  Never edit an existing doc, never edit ROADMAP.md, never commit, never push.
- **Never edit releases.db.** Absent, sparse, or stale are all valid states (its §GH-381 forbids
  topping it up). Report drift; stop there.
- **Transform is declared, never inferred.** No commit prefix promotes work to Transform — only an
  explicit `rgt: transform` frontmatter key on the governing `PROJECT/**` doc. Auto-promoting
  `perf:`/`refactor:` would inflate the one number this exercise exists to keep honest.
- **Cite or drop.** An uncited target is a guess.
- **No targets and no umbrella observations → write nothing.** Report the flow distribution
  in-session and stop. A clean run that manufactures paperwork trains the operator to ignore
  the artifacts. An umbrella observation (Lens 2 signal 8) is a finding in its own right: a run
  with zero ordinary targets and one tracked umbrella still writes both sinks.
- **Degrade loudly.** Missing `gh`, no `PROJECT/**`, no conventional commits → run the lenses you
  can and state plainly which signal was unavailable and what that costs the verdict (table below).

## Step 0 — Frame the window & discover prior reports

Default **21 days**; honor an operator override. Resolve to explicit dates and state them.
Read the repo's trunk (`main`, or `development` where that is the declared WIP branch), not the
current feature branch. Compute the prior window of equal length for the trend comparison.

**Discover prior reports and historical arc:**
Scan the repository for historical Radar reports across standard locations:
- `RADAR/`
- `docs/radar/` or `docs/RADAR/`
- `PROJECT/1-INBOX/RADAR-REPORT-*.md`
- Repo root fallback (`RADAR-REPORT-*.md`)

When prior reports exist:
- Sort chronologically by date/run.
- Extract historical RGT percentages, identified target IDs, and retirement states.
- If ≥2 prior reports exist spanning multiple weeks, use them to compute the multi-week macro-arc
  for Lens 1 and the SDLC Process Coach narrative (Step 4).

## Step 1 — Lens 1: flow distribution

**Compute the tally once, into a file, and prove it sums.** Write subjects with
`/usr/bin/git log --no-merges --since=<start> --until=<end> --pretty='%s' <trunk> > <tmpfile>`,
then assert `wc -l <tmpfile>` equals the sum of the bucket counts before reporting anything.
Two reasons, both observed, and the second one independently in two repos: shell wrappers/hooks may
rewrite or **silently truncate** `git` output — a `tail` view of a piped tally returned counts
contradicting the `head` view of the same pipeline, and on another machine-repo the RTK proxy
capped `git log` at exactly **50 lines for both windows of a 548-commit repo**, which would have
bucketed 50 commits and reported a confidently wrong distribution with no visible symptom. A
partial read is indistinguishable from a real distribution; the sum check is the only thing that
tells them apart. Cross-check the total against `git rev-list --no-merges --count` as well when the
numbers matter.
An unproven tally is exactly the reads-as-authoritative-while-wrong failure this tool exists to
catch; do not let the radar commit it.

Then bucket by conventional-commit prefix, into **five** buckets:

| Bucket | Prefixes / rule |
|---|---|
| **Harness** | `relay*:` `marathon*:` `plan:` `capture:` `triage:` `wip:` — machine-generated turn/render commits, matched as **prefix families** (`relay-pkg:` is harness; exact-match lists leak — first calibration run caught exactly this). Report the count, then **exclude from the RGT denominator**: they are the machinery running, not work chosen. In a harness-driven repo they can outnumber everything else (validated here: 178 of 438 commits) and silently swamp the signal. |
| **Run** (KTLO) | `fix:` `chore:` `docs:` `refactor:` `test:` `ci:` `hotfix:` `cleanup:` — or the governing doc says `rgt: run` / `doc_type: bugfix` |
| **Grow** | `feat:` — or the governing doc says `rgt: grow` |
| **Transform** | **only** an explicit `rgt: transform` on the governing `PROJECT/**` doc. **Always report `rgt:` adoption alongside the figure** — at zero adopting docs, "Transform 0%" means *nobody has declared anything*, not *no transformative work happened*, and the number cannot become non-zero until the key is adopted. Print it as `0% (rgt: adoption: N docs)` so the distinction is never left to the reader. |
| **Unclassified** | everything else, including unprefixed. Reported, never silently bucketed — a large share is itself a finding (inconsistent conventional commits). |

An explicit `rgt:` key on the governing doc always beats prefix inference. Report the ratio over
the RGT denominator (Run+Grow+Transform+Unclassified), the trend vs. the prior window, and a
one-line verdict. No threshold blocks anything.

**Two malformed-prefix families are common enough to check for by name**, because both are
correctly-typed work that a strict parser silently discards into Unclassified:

- **component-as-type** — `3-Eyes: adopt registry overlay`, `stay-focused: add session-anchor skill`
- **missing colon after scope** — `fix(GH-169) Phase 2: stop the collector evicting events`, where
  the type and scope are both right and only the `:` is absent. Third calibration run: this dropped
  **four** correctly-typed commits from one active workstream.

When either family appears more than once, report it as a **source-fixable measurement defect**, not
just an inference miss — the convention is what should change, and saying so is more useful than
silently compensating forever.

**Always print the Unclassified subjects verbatim, then give an adjusted read beside the
mechanical one.** Second calibration run: mechanical inference read 5% Grow where the adjusted read was 19%,
a ~4x undercount in the one direction that flatters nobody. Report both; label which is which.

## Step 2 — Lens 2: recurring defects & regression detection

Build clusters, then rank. This lens has two essential jobs:
1. **Find chronic recurring defects**: long-standing friction, architectural debt, or seams that repeatedly break over weeks or months.
2. **Detect potential regressions**: fresh breakage, short-cycle bouncebacks, or destabilized tests/guards introduced by recent work in the window.

Signals in order of precision:

**Signal precision is repo-dependent — measure it, don't assume it.** The order below is a
starting prior, not a ranking. Run every signal, report each one's **yield** (how many clusters it
produced), and rank targets by the evidence that actually materialized. Validated across two repos
whose sharpest signals were exact inverses: in `xyz-3-agents-swarm` signal 1 was decisive and
signal 2 flat; in `giant-brains-claude-skills` signal 1 yielded nothing and signal 2 carried the run.

1. **`related:` frontmatter** in `PROJECT/**/GH-*.md` — human-authored sibling links. **Two shapes
   exist and both must be parsed**: a block array of prose entries citing `#refs`, and a scalar
   pointing at a sibling *filename* (`related: GH-8-FOO.md`) with no issue number at all — resolve
   filename form to its issue via the target doc's `gh_issue:` key. **Report the extraction yield
   explicitly**: "N docs carry `related:`, M references extracted." *M=0 while N>0 is a parser
   failure, not an absent signal* — say so out loud. (Second calibration run hit exactly this: 2
   docs carried the key, the array-shaped extractor returned silence, and the skill nearly reported
   "no kinship signal" when the signal was there in a shape it could not read — the same
   reads-as-active-while-nothing-runs class this tool exists to find.)
   Citation count also **conflates two things**: defect kinship ("same seam", "same family",
   "opposite direction", "same class") and infrastructure context (a FROZEN-twin contract, a
   release issue, an SOP cited as background). Only kinship forms clusters — first calibration run:
   #308 drew 11 citations, all context, zero kinship.
2. **Shared seam** — `fix:` commits in the window grouped by touched file/function. **Group by
   issue, not by commit**: one commit fixing five shims is one data point per seam.
   **Then apply the recurrence discriminator, which is the whole point of this signal:**
   a hot seam counts as *recurring* only if its fixes span **≥2 distinct calendar days** AND
   **≥2 distinct originating PRs/branches/issues**. Otherwise it is **concentrated authoring** —
   one hardening pass on one component — and must be excluded from targets and labeled as such.
   (Second calibration run: 13 of 13 window `fix:` commits landed on one directory, which reads as
   an overwhelming top target until you check the dates — all 13 on a single day, all from PR #10.
   That is a skill being written, not a defect recurring.)
3. **Issue-text similarity** across `gh issue list --state all --json number,title,labels,body`.
4. **False closes, then reopens** — a capture doc recording a *doc-only / no-code-change*
   resolution for a code defect is the primary form of this signal and greps cheaply. Reopen
   events need per-issue `gh api` timeline calls — expensive; sample them only for cluster
   members already found by other signals. Treat doc-only closure as a strong recurrence
   predictor: first confirmed instance is #18, closed doc-only within 2 hours, same seam
   re-fired at day 34 (#314) and day 44 (#440).
   **This signal is structurally unavailable in a repo with zero closed issues** — check the closed
   count first and say so rather than reporting a clean sweep. Nothing has had time to recur.
5. **Cross-repo re-reports** — the `reported_from:` frontmatter key. The same harness bug reported
   from three vendored repos is one target, not three.
6. **Operational evidence** — runtime logs, health captures, collector outcomes (`temp/logs/*.log`,
   `*-degraded` captures, sync-outcome records). **A product repo has an evidence source a tooling
   repo does not: proof a class is firing *right now*.** Grep the recent log tail for the failure
   string a cluster predicts, and count how many of the last N runs show it. This converts a target
   from "6 issues over 12 days" into "6 issues, and it refused to start in 5 of the last 9 nightly
   runs" — the difference between a backlog item and an active outage. Third calibration run found
   its top target this way; neither tooling repo had the signal at all.
7. **Recent seam bounceback & regression heuristic** — check for short-cycle regressions:
   - Identify files modified by recent feature or refactoring work (`feat:`, `refactor:`) within the
     window (especially the last 7–14 days, measured backward from the window end date or run date).
   - Look for subsequent `fix:`, `hotfix:`, or `revert:` commits touching those same files or functions.
   - **Apply the regression recurrence discriminator (prevent false positives on in-branch authoring):**
     a bounceback counts as a potential regression only if the `fix:`/`hotfix:`/`revert:` commit originates
     from a **different PR/branch** than the original `feat:`/`refactor:` commit, OR lands on a
     **different calendar day**. (Otherwise it is ordinary in-branch authoring, not a regression).
   - Look for fast-follow issues filed shortly after a PR merge complaining about broken pre-existing
     functionality or degraded performance.
   - When detected, flag them specifically as **Potential Regressions** rather than generic tech debt:
     they indicate that recent changes skipped sufficient edge-case testing, lacked automated guards,
     or broke assumptions made by other components.
8. **Umbrella re-score** — the completion check for `whack-a-mole`'s output. An umbrella issue
   says a class of bugs has one root cause; "umbrella closed" is not evidence the class stopped
   (the #591 chain closed two fixes and each exposed the next break). Radar is the only thing
   that measures it.
   - Discover: `gh issue list --state all --limit 200 --search 'Umbrella: in:title'`, then keep
     only titles that **begin** with `Umbrella:` (case-insensitive) — whack-a-mole's
     `gh issue create --title "Umbrella: <mechanism>"` form. `MARATHON umbrella:`,
     `[Umbrella]`, `… — tracking umbrella` and the like are other tools' groupings with no
     churn claim and are excluded, not reconstructed. Report the yield as `N hits, M
     whack-a-mole-form` (witnessed: 10 hits, 1 umbrella).
   - Read each body's `### Cluster signature` block — the contract lives in
     `skills/3-weekly/whack-a-mole/SKILL.md` §6 (keys `cluster run window weights paths errors issues
     commits signals`, JSON-array lists). A block present but unparseable is a **parser
     failure**; no block at all (an umbrella filed before the template carried one) is
     **legacy**: reconstruct a signature from the body's "Symptoms this explains" list and
     named paths, label it `reconstructed`, and treat `filed at` as unavailable.
   - Cutoff: the merge time on the trunk of the PR the umbrella's Remediation **Fix** task names,
     or that its closing comment cites (`gh pr view <m> --json mergedAt`). A docs/reconcile commit
     that merely mentions the umbrella number is not a cutoff. No such PR → no cutoff. A reverted
     or superseded fix voids its cutoff. Merge is not deployment: if signal 6 shows the class
     still firing after the cutoff, the umbrella cannot read as solved whatever the score.
   - Count with whack-a-mole's counting rules (§6 of that file, "Counting rules for a
     re-score"): interval = this radar window intersected with strictly-after-cutoff; membership
     = its §3 two-signal rule and it gates every count (a `fix:` that merely touches a
     signature path is adjacency, not a repeat fix); the six raw fields as counted; score with
     the **default** weights
     (`3·reopens + 3·repeat_fixes + 4·reverts + size + floor(comments/5) + floor(open_days/7)`)
     even when the block's `weights:` line differs — a non-default line only marks the baseline
     `filed-custom (non-comparable)`.
   - An unavailable input (no `gh`, timeline calls refused, signature unreadable) is reported as
     unavailable per the yield rule below — it is never a score of 0 and never earns quiet credit.
   - The umbrella *row* (Step 5) is a completion ledger and stays out of the target ranking
     above; the activity that re-scored it is ordinary Lens 2 evidence and may form or feed a
     `RADAR-<id>` target, which the row then links as `class RADAR-<id>`. One class, two
     ledgers — never a second numeric target because an umbrella exists.

9. **Trunk CI health** — a red trunk is a live regression, and no signal above reads CI (GH-779;
   rebalanceOS `development` failed `lint` + `root-noembed` on every push for 9 days unnoticed).
   - Read: `gh run list --branch <trunk> --limit 200 --json databaseId,headSha,conclusion,createdAt,name`,
     filtered to the window; for failed runs, `gh run view <id> --log-failed` and keep only the
     failing test ids (`FAILED tests/...`) and lint findings (`path:line:col: CODE`).
   - Report: **consecutive red days** up to the window end, the **first red commit** (sha, subject,
     PR), and the failing tests/findings that persist across those runs.
   - Red for **≥2 calendar days** is a **Potential Regression** target, ranked above every backlog
     cluster: a red trunk hides every new failure behind the old ones.
   - No `gh`, no workflow runs, or an unreadable log is **structurally unavailable**, stated as such
     — never reported as green.

**Guard against corpus drift when comparing runs.** Signal 1's citation graph is scoped to a set of
directories, so a *lifecycle* action — a PDDA sweep moving docs from `2-WORKING` to `3-COMPLETED`
or `4-MISC`, a bulk rename, an archive — changes the citation counts with no defect having changed
at all. Observed: one sweep relocated 39 docs and repointed 51 roadmap entries in a single commit.
**Record the doc-corpus size per bucket in every report**, and when it moves between runs, say so
before attributing any citation delta to defect activity. Same species as symptom masking: a change
in the instrument reading that did not come from the thing being measured.

**Report each signal's yield as one of three states, never collapsed:** *parser failure*
(`M=0 while N>0` — say so loudly), *structurally unavailable* (no closed issues, no `reported_from:`
docs, no logs — state it rather than implying a clean sweep), or *available and genuinely empty*
(e.g. 81 closed issues exist and none was a doc-only close — that is a real negative result and
worth reporting as one).

**Clusters come in two shapes; support both.** *Seam-shaped*: N issues circling one file or
function (e.g. three issues on one `ensure_gitignore()`). *Class-shaped*: N issues sharing a defect
class across different files (e.g. "guards that cannot report red" — the shape this repo's Litmus
release was hand-derived from). A radar that only sees seams misses the class clusters, which the
first hand-run showed are where the largest verdicts live.

Rank crudely; refine only if it misranks in practice:

```
target score ≈ (distinct issues in cluster)
             × (blast radius: repos / lanes the seam or class touches)
             ÷ (fix cost: the cluster's median effort rating)
             × 1.5 if any member was closed without a code change
             × 1.3 if identified as a recent regression (bounceback from a recent feat/refactor)
```

For each target report: the cluster (issue numbers + docs), the shared seam or class, the span in
days, whether it represents a **recent regression** or **chronic tech debt**, why it recurs, and what a
single durable fix would retire.

## Step 2b — Open-PR collision check

Run this pass after finding targets and before recommending a new plan. Landed commits tell Radar
what happened; open pull requests tell it what is already in flight. This is the duplicate-work
check: a proposed target may be urgent without being available to schedule again.

First enumerate the current landscape:

    gh pr list --state open --limit 100 --json number,title,url,headRefName,baseRefName,isDraft,updatedAt,mergeable,mergeStateStatus,body,labels

For each PR that names a target issue or its documented seam, inspect the changed-file list and
current status before calling it an overlap:

    gh pr view <number> --json number,title,url,isDraft,headRefName,baseRefName,updatedAt,mergeable,mergeStateStatus,body,files,statusCheckRollup

Match in this order: an exact target issue number in the PR title/body; then a changed file that is
the target's named seam; then a class target whose documented issue numbers and changed files both
support the same class. Do not call a vague keyword or a similarly named file a match. Record the
PR number, URL, base branch, age, draft/mergeability/check status, matching evidence, and the
target it overlaps.

**An open PR is never a completed fix.** Do not reduce a target's score, strike it through, close
its checklist, or call its release plan aligned just because a PR exists. Classify an evidence-backed
overlap as one of these states and act accordingly:

| PR state | What it means | Required recommendation |
|---|---|---|
| Ready and verified | The work may retire the target soon, but has not landed. | **Do not schedule a duplicate.** Inspect/merge the PR, then rerun Radar against the merge commit before retiring the target. |
| Draft, failing, conflicted, or stale | The work is a collision risk, not reliable progress. | **Do not assume this is covered.** Ask the PR owner to update, split, or close it; keep the target open and plan a replacement only after that decision. |
| PR targets the wrong base branch | It may be valid work, but is not on the path Radar is evaluating. | **Rebase or retarget it before counting it as in flight.** Until then, do not let it block the target's plan. |
| No confident overlap | No current work claims the target. | **Schedule or assign the target** if the other lenses say it matters. |

Report only PRs that change the operator's next step. In the in-session reply, translate the
result as "Already being worked on," "Blocked or stale work," or "No work underway" — not a raw
PR inventory. A plan recommendation must name any matching PR and say whether the operator should
merge it, unblock it, close it, or deliberately schedule a non-duplicate follow-up. Carry the PR
classification results directly into Step 4.3 for the "In-Flight Work & Open PRs" summary.

### New-guard re-run (collisions with zero file overlap)

File overlap misses the costliest collision: a check lands, then an older PR that predates it lands
and turns trunk red (GH-779: GH-241's script ratchet vs rebalanceOS #231, no shared files). For each
check, ratchet, lint rule, or CI job **added or tightened in the window**, run it against every open
PR head merged with current trunk (disposable clone: `git merge --no-commit origin/<trunk>`, then the
guard's own command). A PR that fails a guard it predates is a **collision** — classify it
"Draft, failing, conflicted, or stale" above and name the guard, the failing line, and the fix
owner. A guard that cannot be run locally is reported as unavailable, never as a pass.

## Step 3 — Lens 3: release recalibration

Read the DB using `releases check`, `releases list`, and the `python3 utils/timeline/export_timeline.py --json` payload. Cite the DB generation numbers in the report.

Skip silently if the DB is absent, has no unshipped releases, or contains only the installer's seed block (e.g., a release whose description says EXAMPLE / "replace this", or that has an empty target date and tracking issue). Reporting drift against a seed is precisely the "do not treat a sparse file as an incomplete one" failure §GH-381 forbids.

Otherwise, for each unshipped release in the payload: join its `milestoneRef` (or `milestone`) to its issue set
(`gh issue list --milestone "<title>" --state open`).

**If `milestoneRef` is empty, or the repo has no milestones at all, the join is impossible — fall
back to reading claim status from the release's `blurb` or `exit` prose and say that is what you did.**
Do not report a 100% orphan share as backlog drift in that case: with no milestones to belong to,
that number measures a **missing binding**, and the actionable finding is "bind a milestone (or
create the milestones) so the next run can join" — not "the backlog is unplanned."

Then compare the planned theme against the observed flow distribution and the top targets, and
surface:

- Does the arc's `Description:` still describe where effort actually goes?
- Is a top radar target unclaimed by any planned band? Mark each reported target **claimed by
  <band>** or **UNCLAIMED** — a claimed target is context, an unclaimed one is the finding.
- Has the milestone's issue set drifted from its stated theme?
- The **orphan share**: what fraction of open issues belong to no milestone at all? A large
  unassigned majority means the bands describe less of the backlog than they appear to. Only
  meaningful once at least one real band exists — 100% orphan in a repo with no milestones is a
  young repo, not a planning failure.

Advisory only. Say "the plan says X, the repo is doing Y" and stop.

## Step 4 — Report in-session

Treat the in-session reply as an **SDLC Process Coach & Strategic Decision Memo**, not a cold forensic data dump.
Speak in the voice of an experienced, encouraging Principal Engineer or Agile Process Coach who cares about
developer momentum, team health, and sustainable delivery velocity.

When no targets and no umbrella observations were found, report only the flow distribution (§3) and the all-clear recommendation; skip the multi-paragraph coaching narrative and retrospective sections. Umbrella observations alone still get the Structured Evidence section and Step 5.

Lead directly with a warm, insightful two-paragraph executive narrative, followed by prioritized coaching recommendations and a clean summary of the evidence. Keep the raw commit tallies, mathematical proofs, and forensic debug traces in the persisted evidence report unless specifically requested.

### 1. The SDLC Process Coach Narrative (The Opening Two Paragraphs)

The first two paragraphs set the human context and direction for the entire report. Avoid dense cybernetic jargon, cold acronyms, or adversarial auditor language.

#### Paragraph 1 — High-Level Wins & Velocity (Celebrate Momentum)
- **Acknowledge and celebrate progress first**: Recap what actually went well during this window. Highlight newly shipped user-facing features (`feat:`), major architectural milestones, closed blockers, and performance or DX wins.
- **Affirm team effort**: Give the engineering team genuine credit for moving the needle, recognizing where delivery momentum is strong and durable improvements were made.

*Example*: "Over the past three weeks, the team has sustained impressive feature momentum—landing major capabilities including the GitHub Pages documentation portal and the cross-device AgentChorus bridge. Crucially, the team also demonstrated excellent follow-through on quality by knocking out repeat blockers in the telemetry subsystem, turning hard-won operational lessons directly into durable repo policies."

#### Paragraph 2 — SDLC Health, Flow Friction & Potential Regressions (Process Coaching)
- **Assess process health & the RGT trajectory (The Arc)**: Contextualize where engineering energy is actually going over time. Compare the current Run/Grow/Transform (RGT) mix against predecessor runs or the prior window (see §3 below for the full trajectory numbers), evaluating whether the team is gradually escaping high-maintenance "Run" churn to unlock more "Grow" feature velocity, or if the arc has remained stalled in firefighting across multiple sittings.
- **Spotlight potential regressions & hot spots**: Explicitly identify any **regressions** (e.g. recently modified files or new features that suffered rapid follow-up hotfixes, broken test guards, or reopened tickets) as well as chronic recurring defects that keep pulling developers away from forward progress.
- **Provide empathetic coaching**: Explain the real-world impact on team velocity, cognitive load, or release stability, pointing out whether the team needs a focused stabilization sprint, better guard tests, or unblocking on stuck PRs.

*Example*: "At the same time, our delivery rhythm is feeling the strain of reactive maintenance: over 75% of recent non-harness commits were consumed by bug fixes and chores (essentially unchanged from 76.7% in our previous run, showing that our maintenance arc has remained stubbornly flat). More importantly, we're seeing signs of short-cycle regressions in the root resolution logic, where three separate follow-up fixes had to be applied within days of landing. Left unchecked, this churn will continue to siphon bandwidth away from our next milestone; taking a dedicated stabilization pass here will restore smooth sailing."

### 2. Prioritized Coaching Action Items

Follow the coach's narrative with 2–3 clear, high-leverage recommendations framed constructively. Every recommendation must specify an actionable step and how to know it succeeded:

    Recommended next step: <specific, high-leverage action, owner/decision when known, and completion condition>

*Example*: "Recommended next step: Pause new feature branches in the vendoring area for one work cycle to implement a unified path resolver, retiring the cluster of 12 recurring resolution issues once and for all."

### 3. Structured Evidence & Technical Highlights

Translate the underlying analytical lenses into clean, easily digested human takeaways:
- **Flow Balance & RGT Arc**: Summarize the Run/Grow/Transform effort mix alongside the trend across prior runs or windows (e.g. "Run/Maintenance: 76.9% [vs 76.7% in Run 2] · Grow/Features: 14.2% [vs 14.4%] · Transform: 0% (rgt: adoption: 0 docs) · Denominator: 607 commits"), clearly illustrating whether the development arc is trending toward feature momentum or stuck in KTLO.
- **Top Recurring Targets & Regressions**: List the top 2–4 defect clusters in a simple bulleted format, clearly distinguishing **Recent Regressions** (bounceback on recently touched code) from **Chronic Tech Debt** (long-standing multi-week issues). Include why each recurs and what a single clean fix accomplishes.
- **Regressed After Declared Fixed**: one row per class that was declared fixed and came back
  (GH-779; format of HiQS-Labs/rebalanceOS#257). Evidence is signal 4 (false closes) plus a closed
  issue whose class recurs in a later issue or target:

  | Class | Declared fixed | Came back | Rule | Mechanical guard |
  |---|---|---|---|---|
  | DB bypasses | #27 (08-17) | #136 (08-30) | One gateway; no raw `sqlite3.connect` | SQLite gateway ratchet |

  **Rule** is one portable sentence another project could adopt. **Mechanical guard** names the
  test, ratchet, or CI check that fails when the class returns; `prose only` is itself a finding —
  classes that regressed almost always had only a principle, an SOP, or a closed issue. Carry the
  same table into Sink A.
- **In-Flight Work & Open PRs**: State clearly whether current PRs are actively addressing these targets, blocked by conflicts/stale reviews, or if the targets are completely unowned.
- **Release Plan Alignment**: Highlight in one or two sentences whether actual work matches the active roadmap milestone, calling out any untracked orphan work.

If no action or intervention is needed, affirm that cleanly: "Recommended next step: Keep current course; the flow balance is healthy and no significant regressions were detected."

### 4. Multi-Week Retrospective Arc (Offer & Invocation)

When prior reports spanning multiple weeks (or runs) are discovered across `RADAR/`, `docs/radar/`, or `PROJECT/1-INBOX/`, conclude the in-session response with a proactive offer:

> *"Found <N> prior radar reports spanning the last <X> weeks (<start_date> → <end_date>). Would you like a high-level multi-week retrospective summarizing our long-term RGT trajectory, defect retirement rate, and roadmap convergence?"*

If invoked directly with `/radar --arc`, `/radar --summary`, or when the operator accepts the offer, produce a dedicated **Multi-Week Arc Retrospective** formatted as follows:

1. **The Macro-Arc Narrative (SDLC Process Coach)**:
   A 2-paragraph retrospective framing the team's multi-week journey: how the balance of feature delivery vs maintenance has shifted over the full horizon, acknowledging major systemic wins, and evaluating whether tech debt is draining or compounding over time.
2. **Longitudinal Flow Trajectory (RGT Across Weeks)**:
   A compact comparison table tracking the progression across every recorded report:

   | Report / Date | Window | Run (KTLO) | Grow (Feat) | Transform | Context / Milestone |
   |---|---|---|---|---|---|
   | `2026-08-07` (Run 1) | Jul 17 → Aug 07 | 94.0% | 6.0% | 0% | Gate-repair cycle |
   | `2026-08-28` (Run 2) | Aug 07 → Aug 28 | 76.7% | 14.4% | 0% | Core feature unlock |
   | `2026-09-02` (Run 3) | Aug 12 → Sep 02 | 76.9% | 14.2% | 0% | Steady flow, resolver churn |

3. **Defect & Regression Scorecard**:
   - **Total Unique Targets Tracked**: Count of all targets across all historical runs.
   - **Durable Retirements**: Targets struck through citing fixing commits (and verified quiet).
   - **Recent Regressions vs. Chronic Debt**: Targets that bounced back vs targets remaining open across multiple runs.
   - **Symptom-Masked / Unresolved**: Targets marked quiet without verified code fixes.
4. **Strategic Recommendation for the Next Arc**:
   One high-leverage strategic recommendation for engineering leadership advising where to focus team energy in the upcoming cycle or quarter.

## Step 5 — Persist the report (two sinks, one confirmation)

Skip entirely when there are no targets **and** no umbrella observations (signal 8). An
umbrella-only run writes both sinks: the report carries the re-score evidence, the live issue
gets the umbrella row.

### Target IDs — stable across runs

A target is identified by what it centers on, never by its prose:

- **Seam-shaped, one function:** `RADAR-<function-name-slug>` (function name preferred over file
  path — it survives file moves).
- **Seam-shaped, one file:** `RADAR-<basename-sans-extension>`.
- **Class-shaped:** `RADAR-class-<short-class-slug>`, chosen once at first sighting.

Slug rule: lowercase, non-alphanumerics → hyphens. **Never re-slug a live target.** If its seam is
renamed, keep the original ID and add a `formerly <old name>` note under the target's heading in
the issue body — an alias that fails visibly beats a silent identity split that resets the aging
clock exactly when it matters.

### Sink A — evidence, immutable

Write `PROJECT/1-INBOX/RADAR-REPORT-YYYY-MM-DD.md` — **if that filename already exists, this is the
Nth run of the same day: append `-runN` (`RADAR-REPORT-2026-08-07-run2.md`) rather than overwriting.
A same-day rerun is a distinct immutable snapshot, and "never edit a prior report" outranks the
one-doc-per-date convention.** PDDA frontmatter
(`title status created updated owner goal` + `doc_type: report`), the full three-lens analysis
with citations, and the checklist as it stands at generation time (a historical record, not a
second live copy). Never edit a prior report; a new run writes a new dated doc. No ROADMAP pointer
— 1-INBOX carries no coverage requirement. If the repo has no `PROJECT/` tree, offer repo root as
a fallback location and say so in the report header.

**Executive Summary Requirement for the Report Document**:
The written report doc must open with the identical **two-paragraph SDLC Process Coach Executive Summary**
(Paragraph 1: High-Level Wins & Velocity; Paragraph 2: SDLC Health, Flow Friction & Potential Regressions)
immediately below the frontmatter and window metadata header. This guarantees that anyone browsing
`PROJECT/1-INBOX/` immediately encounters an encouraging, insightful overview of the cycle before diving
into the technical lens tables, degradation matrix, and forensic commit citations.

### Sink B — completion state, live

The checklist only, plus a link to the newest report doc. Search first:

    gh issue list --label radar --state open

- **none** → `gh issue create --label radar --title "radar: <repo> — recurring targets"`
  (create the `radar` label first if the repo lacks it)
- **exactly one** → update in place: carry unchecked items forward by ID, append new targets,
  strike through targets whose seam went quiet citing the fixing commit, update each target's
  `first-seen: <date> · runs: <n>` line, then comment with the run delta and the new report link.
  Never open a second radar issue.

  **Never strike through on symptom disappearance alone — require a citable fix.** A target may go
  quiet because a *different* target's fix masked it, not because its own defect was addressed.
  Third calibration run found a live instance: a store-bloat class was a plausible cause of the
  memory pressure tripping a separate unbounded-ceiling class, so shipping the reclaim work would
  have silenced the ceiling's symptom while its defect — no enforced bound — stayed exactly where
  it was. A false strike-through is worse than a missed one: it resets the aging clock on a live
  defect and destroys the one signal reconciliation exists to produce.
  So: strike through only when a commit or PR **names the seam**. If the symptom stopped but no
  such commit exists, keep the target open, increment `runs:`, and annotate it
  **`quiet, unexplained — possible symptom masking by <other target>`**. Where two targets are
  causally linked, say so under both.
- **more than one** → stop and ask the operator which is canonical.

Checklist items are grouped under their target heading and each names a file, a function, and an
acceptance condition, so a different agent in a later session can execute one cold:

```md
## RADAR-ensure-gitignore — 3 issues over 47 days · first-seen: 2026-08-07 · runs: 1

- [ ] Fix `ensure_gitignore()` to handle both directions (add-ignore and un-ignore) — `relay-automation/xyz-vendor.sh`
- [ ] Add a regression test asserting both directions on a fresh vendor
- [ ] Close #18 / #314 / #440 with the commit SHA — none of them doc-only this time
```

**`## Umbrellas — re-scored` — one section, appended after the target sections, one row per
umbrella found by signal 8.** The first line is the fixed row; the second is a continuation:

```md
## Umbrellas — re-scored

- [ ] #<n> — filed at <score> (<run>), now <score> (<window>), fix merged <YYYY-MM-DD PR #m | not yet> → holding | class survived — recommend reopening | solved
      cluster <slug> · baseline observed | legacy — no signature (reconstructed) | filed-custom (non-comparable) · quiet <k>/2 (<report-a>, <report-b>) · class RADAR-<id> | none
```

- `filed at legacy` when the umbrella has no signature (the baseline is reconstructed and can
  show `class survived`, but never earns quiet credit until an operator adds a real signature —
  radar never edits the umbrella).
- **holding** — the fallback: every observation that is neither `class survived` nor `solved`.
  That includes an open umbrella with no fix yet, an open umbrella whose fix merged but whose
  post-cutoff score is still ≥ 5 (the displayed score says the class is alive; the umbrella
  is still open so there is nothing to reopen), and an observation whose evidence was
  unavailable. `quiet k/2` counts consecutive below-5 observations *after* the cutoff; an
  active (≥ 5) or unavailable observation earns 0 and resets the streak.
- **class survived — recommend reopening** — the umbrella is **closed** and the post-cutoff
  score is ≥ 5 (whack-a-mole's own floor is "no cluster *above* 5"; radar deliberately keeps
  the conservative boundary). Radar recommends; it never reopens.
- **solved** — the only state that is struck through, and only on `quiet 2/2` **and** a `fix
  merged` PR. This is the umbrella form of the "names the seam" rule above: a citable fix plus
  two quiet observations. "Consecutive" means the two most recent Sink A reports (filename
  date/run suffix, UTC) on **distinct dates** — a same-day `-runN` rerun is not a second
  observation. The streak resets to 0 on any run scoring ≥ 5, on an unavailable input, on a
  changed cutoff, or on a changed signature or weights (two low scores over different
  memberships or scales are not one streak). Two observations is what the rule asks; it is not a
  claim about elapsed exposure.

### Confirmation

Preview both artifacts, write on **one** confirmation covering both sinks. Never ask twice.
Then offer — do not assume — to hand the targets to `start-marathon`.

## Degradation table

| Missing | Lost | Still runs |
|---|---|---|
| `gh` / auth | Lens 2 signals 3-5, open-PR collision check, Lens 3 joins, Sink B | Lenses 1-2 (signals 1-2), Sink A; state that no in-flight-work check or live checklist was available this run |
| `PROJECT/**` | Lens 2 signal 1, `rgt:` overrides, Sink A's normal location | Lenses 1-3 from git + `gh`; offer repo-root fallback for Sink A |
| Conventional commits | Lens 1 inference | Report the Unclassified share as the finding it is |
| `releases.db` absent, or seed-only | Lens 3 | Everything else; PLAN reads "no release plan" — a valid state, not a gap |
| Closed issues (zero) | Lens 2 signal 4 entirely | Everything else; say "nothing has had time to recur" rather than implying a clean sweep |
| History < ~2 windows | The trend line, and most of Lens 2 | Lens 1 for the current window only; state that recurrence is structurally unobservable this young |

Always state which rows applied and what they cost the verdict.

## Boundaries

| Tool | Owns | Radar's difference |
|---|---|---|
| `weekly-shipped` | Outward recap of what shipped | Inward, diagnostic, judgmental |
| `start-marathon` | Ranking and preparing marathon candidates | Radar asks what deserves to be a candidate; feeds it, never requires it |
| `/honest` | Whole-repo maturity read | Windowed (21 days) and mix-focused |
| `pdda.sh glance` / `releases-current` | Doc-state inventory | A verdict across git + issues + docs + releases, not an inventory |
| `/10days` | Sweeps issues then **executes** | Radar never executes anything |
| `whack-a-mole` | Files one umbrella per run for a churn cluster, with a Cluster signature | Radar re-measures that signature on every run (signal 8) and is the only thing that calls the class solved — never issue closure |
