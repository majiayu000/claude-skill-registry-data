---
name: cs-estimate
description: Estimate effort for a task, GitHub issue, spec or the whole ready queue from evidence in the code and the repository's own history — picks one estimation mode, sizes with the lightest honest unit (t-shirt, points, PERT range), separates discovery from delivery, says split or spike, states confidence and how the number may and may not be used. First asks who executes it — the cs-orchestrator agent fleet, a team, or both compared — and estimates for that; understands cs-spec parallel plans (critical path with N agents), checks dispatch readiness and offers to queue the issue for the orchestrator. Read-only unless the person chooses to post or queue
argument-hint: "<description | #issue | --queue> [--fleet|--team|--compare] [--post] [--calibrate] [--unit points|tshirt|days]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion, Agent
---

# Estimate

You produce **one estimate packet**: a size, an honest range, a confidence, the
evidence behind it, and the one next move. Not a deadline, not a promise, not an
agile lecture.

## Inputs

`$ARGUMENTS`:

| Input | Meaning |
|---|---|
| free text | estimate the described work |
| `#<n>` / issue URL | estimate that issue — body, comments, linked spec; a `## Parallel plan` is estimated per slot |
| `--queue` | estimate every open issue with the ready label (`.code-analyzer-config.json` → `orchestrator.readyLabel`, default `cs:ready`) as one comparison table |
| `--calibrate` | no new estimate — compare past posted estimates with what actually happened, and report the team's correction factor |
| `--post` | after the estimate, post it as an issue comment and set a `size: <XS…XL>` label. Asks first unless `--auto` is also given |
| `--fleet` / `--team` / `--compare` | who executes it — skips the Step 0 question (see below) |
| `--unit points\|tshirt\|days` | force the unit. Otherwise the project's convention wins (labels, issue templates, `CLAUDE.md`), else the mode's default |

The skill is **read-only** except `--post` and the orchestrator hand-off — both
only after the person chooses them.

## Rules that are never traded away

1. **A range, never a single number.** The recommended figure is the *expected*
   case, never the optimistic one.
2. **No silent padding.** Every buffer is a named line with its reason, so the
   reader can decide to accept the risk instead.
3. **Discovery and delivery are estimated separately.** When unknowns dominate,
   estimate the spike, and say what decision the spike unlocks. Never estimate
   the final implementation as if the unknowns were solved.
4. **Confidence is Low whenever the approach is undecided** or the core
   requirement is still open. A range built on an unmade decision is a guess.
5. **No fake precision.** Hours only for work under a day; half-day steps up to
   two weeks; weeks above that.
6. **Uncalibrated is said out loud.** With no usable history, the packet says
   "not calibrated to this team's throughput" and that lowers confidence — it
   does not get absorbed into a bigger number.
7. **Points are not a performance metric** and never convert to a date without
   stated assumptions.

## Step 0 — Who will do the work?

The same task has two different estimates: a fleet of agents is bounded by the
critical path, parallel slots and human review; a team is bounded by people,
capacity and context switching. **Ask before estimating** — unless a flag
already answered it, or `--calibrate` was given (history only, no question).

`AskUserQuestion`:

| Header | Question | Options |
|---|---|---|
| `Execution` | Will this be run through `/code-sentinel:orchestrator` (autonomous agents), or done by people? | **Orchestrator (agents)** — estimate slots, critical path with N workers, agent wall-clock and human review time; check it is ready to dispatch · **Team (people)** — estimate person-days, capacity and sprint fit · **Compare both** — side by side, to decide · **Not sure yet** — estimate for people, note what changes with the fleet |

**Look before you ask** — the recommendation must come from facts, in one
`Bash` call:

```sh
cat .code-analyzer-config.json 2>/dev/null | grep -A12 '"orchestrator"'
gh label list --limit 100 2>/dev/null | grep -E '^cs:' ; git remote -v | head -2
```

Recommend **Orchestrator** when the repository already has the orchestrator set
up (`.code-analyzer-config.json` → `orchestrator`, or `cs:*` labels exist) and
the work is a feature/bug with checkable acceptance criteria; recommend **Team**
when the work is mostly decisions, design, external coordination or discovery.

Then one follow-up round, only for what the answer needs and the repository
does not already say:

| Answer | Ask (each with a recommended default) |
|---|---|
| Orchestrator / Compare | how many parallel slots (`orchestrator.maxSlots`, default 5); who reviews and merges — the orchestrator itself (`autoMerge`) or a person; how many review hours a day that person has |
| Team / Compare / Not sure | how many people, and how familiar with this area; remaining capacity in the current sprint (person-days), or "no sprint" |

Under `--auto`: take the defaults, say which, and lower confidence one level if
capacity is assumed rather than known.

## Step 1 — Pick one primary mode

| Mode | When | Default unit |
|---|---|---|
| `triage` | fuzzy backlog item, roadmap comparison, `--queue` | t-shirt |
| `sprint` | near-term, reasonably specified work | story points (Fibonacci) |
| `forecast` | someone asks "by when" / "does it fit" | PERT range in days + assumptions |
| `spike` | unknowns dominate | time-boxed spike, plus a conditional range for delivery |
| `wave` | an issue with a `## Parallel plan` (from `cs-spec`) | per-slot range + critical path |

One mode per run. If the request mixes two, say which you chose and why.

## Step 2 — Gather the smallest credible evidence

**Context.** Read `CLAUDE.md` / `AGENTS.md` (stack, conventions, any estimation
guidance), the issue with comments, the linked spec. A request too vague to
estimate gets clarifying questions first — at most three, via
`AskUserQuestion`, each with a recommended default; under `--auto`, take the
defaults and lower the confidence.

**The code.** Locate what would change, and measure it — for a broad sweep use an
`Explore` subagent and keep only the numbers:

```sh
# where it lives
grep -rln "<keyword>" --include='*.ts' --include='*.tsx' --include='*.js' --include='*.py' --include='*.go' --include='*.rs' \
  --exclude-dir={node_modules,dist,.next,build,.git} . | head -30
# how big the touched files are
wc -l <files>
# fan-in: how many places depend on the module
grep -rn "from ['\"].*<module>" --include='*.ts' --include='*.tsx' --include='*.js' --exclude-dir=node_modules . | wc -l
# test coverage nearby
find . -path ./node_modules -prune -o -path '*<module>*' \( -name '*.test.*' -o -name '*.spec.*' \) -print | head
# churn: hot spots are risk
git log --since='6 months ago' --oneline -- <path> | wc -l
# how many people know this area
git log --format='%aN' -- <path> | sort | uniq -c | sort -rn | head -5
# debt markers
grep -rn 'TODO\|FIXME\|HACK' <path> | wc -l
```

**A precedent.** Find the nearest sibling already in the codebase (another
endpoint like this one, another screen like this one). "Copy a sibling" and "no
precedent" are the largest single swing in any estimate.

## Step 3 — Break it down, and check the burden

List concrete subtasks. Always include the work that estimates forget:

- tests (often as long as the code), review rounds, fixes from review;
- schema change and migration — and backfill on a large table;
- configuration, environment variables, feature flags, rollout and rollback;
- error and empty states, not only the happy path;
- docs, QA in staging, deployment coordination, approvals.

Score the complexity factors 1–5 and keep the table in the packet — it is the
"why this size":

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| Change surface | 1 file, <50 lines | 3–5 files | 10+ files or several apps |
| Logic | CRUD | branching, state | concurrency, algorithms, money |
| Data | none | new column / index | new tables, migration, backfill |
| Integrations | none | existing library / API | new external API, another team |
| Precedent | sibling to copy | partial | none |
| Tests | easy | some mocking | e2e, hard-to-reach states |
| Risk area | leaf code | shared module | auth, payments, tenancy, deletion |
| Rollout | normal deploy | flag or migration | coordinated / downtime |

Average ≤ 2 → small, ≤ 3 → medium, ≤ 4 → large, above → split or spike.

## Step 4 — Size it

**Relative first.** Compare with 2–3 anchors from *this* repository — a merged
PR that was small, one medium, one that should have been split (Step 5 finds
them). With no anchors, say so.

| T-shirt | Points | Typical span | Rule |
|---|---|---|---|
| XS | 1 | < 2 h | |
| S | 2 | ½ day | |
| M | 3–5 | 1–2 days | |
| L | 8 | 3–5 days | |
| XL | 13 | 1–2 weeks | **split** before committing |
| XXL | 21+ | more | **not estimable as one item** — decompose |

Undecided between two sizes → the larger.

**Then a three-point range** (PERT):

```
optimistic O · most likely M · pessimistic P
expected  E = (O + 4M + P) / 6
spread    σ ≈ (P − O) / 6
```

**Then named adjustments** — each a line, each with its reason, never folded
silently into M:

| Driver | Typical effect |
|---|---|
| no precedent in the codebase | +50–100 % |
| requirement still open | +30–50 % — or switch to `spike` |
| new external API / vendor | +25–50 % |
| no tests in the touched area | +30 % |
| migration on a large table | +25 % |
| auth / payments / tenancy / deletion | +25 % |
| another team or approval in the path | +25–50 % |

**Confidence**:

| Level | Band | When |
|---|---|---|
| High | ±10 % | precedent exists, spec complete, calibrated history |
| Medium | ±25 % | mostly understood, minor research |
| Low | ±50 % | open questions, no precedent, or uncalibrated |
| Very low | ±100 % | do not estimate delivery — estimate a spike |

## Step 5 — Calibrate against this repository's history

```sh
gh pr list --state merged --limit 50 \
  --json number,title,additions,deletions,changedFiles,createdAt,mergedAt,labels
```

- **Cycle time** per PR = `mergedAt − createdAt` (plus time since the first
  commit if the branch is visible: `git log --reverse --format=%cI <base>..<head> | head -1`).
- Pick the PRs most similar in shape (same area, similar `changedFiles`) as the
  anchors of Step 4.
- If earlier estimates were posted by this skill (comments carrying
  `<!-- cs-estimate -->`), compare expected vs actual and apply the median
  ratio as a **named** correction line.
- Fewer than five usable PRs → "not calibrated", confidence drops one level.

`--calibrate` runs only this step and reports: estimates found, median
actual/expected ratio, worst miss and what it had in common, and whether the team
under- or over-estimates by size bucket.

## Step 6 — Turn size into time, for the executor chosen in Step 0

### Team

- person-days from the PERT range, divided across the people who can actually
  work in parallel (two people on one module are not twice as fast);
- focus factor: a developer rarely gets full days — 0.6–0.8 unless the team
  states otherwise, written as a named line;
- **sprint fit** against the remaining capacity:
  ✅ fits ≤ 60 % · ⚠️ tight 60–80 % · ❌ does not fit > 80 % · 🔪 split it > 100 %.

### Orchestrator (agents)

The human cost is not the coding:

| Line | What it is |
|---|---|
| agent effort | wall-clock of a worker session; Opus for slots that decide, Sonnet for slots that execute |
| human review | reading the merge summary and the diff — scale with the diff, not with the agent time |
| human decisions | open questions and gates; each one is a wait, not effort |

Report both, and never present agent wall-clock as team capacity.

Agents change the size, not only the speed: work with a sibling to copy and
complete acceptance criteria shrinks a lot; work with open decisions does not
shrink at all — it waits on a person. Say which kind this is.

Also produce a **dispatch-readiness check** — the orchestrator's own gate:

| Check | Pass when |
|---|---|
| specified | acceptance criteria (feature) or a reproduction (bug) in the issue |
| sized for one slot | L or smaller — or a `## Parallel plan` splits it |
| no open decision | no unanswered open question in the part to be built, no `cs:needs-person` |
| dependencies | every `Depends on #n` closed by a merged PR |
| contention | no open PR touching the same files |
| checks known | `orchestrator.checks` set, or detectable from the project |

### Compare

Two columns — fleet and team — for: expected wall-clock, total effort, human
hours, confidence, and the biggest risk of each. End with a one-line
recommendation and its reason.

### `wave` mode — a parallel plan

For a `## Parallel plan`: estimate each slot (Steps 3–4), then compute the
**critical path** through `Depends on` / `Lead`:

```
wall-clock (N parallel workers) = longest chain of dependent slots
total effort                    = sum of all slots
```

Flag the slot that sits on the critical path and is the least certain — that is
where a spike pays most. A wave whose lead is XL is a wave that waits; say so.

## Step 7 — Split or spike

**Split** when: XL or larger; discovery and delivery are bundled; more than one
owner, system or approval path hides in one item; rollout or migration is
non-trivial. Propose the cut — vertical slice (thin end-to-end first), by risk
(spike first), by user story, or by layer when a contract can be fixed up front.

**Spike** when: unknowns dominate; an external API or vendor behaviour is
unclear; the approach is undecided. A spike has a time box, a question it
answers, and the decision it unlocks.

## Output — the estimate packet

```md
## Estimate — <title / #issue>
<!-- cs-estimate expected=<E> unit=<unit> confidence=<level> -->

**Answer:** <size> · <points> · <O–P range>, expected <E> · confidence <level> (±x%)
**Executor:** orchestrator (<N> slots, review by <who>) | team (<n> people, <capacity>) | compared
**Mode:** <mode> — <why>
**Next move:** commit | split into … | spike first: <question>, time-box <t>

### Evidence
- Files / modules: <paths, sizes, fan-in>
- Precedent: <sibling, or "none">
- Tests nearby: <yes/partial/no> · churn: <n commits/6 mo> · owners: <n>
- Calibration: <median ratio from n PRs | "not calibrated to this team's throughput">

### Breakdown
| # | Subtask | O | M | P | Confidence |
|---|---|---|---|---|---|
| | **Total** | | | | |

### Why this size
| Factor | Score | Note |
|---|---|---|

### Named adjustments
| Driver | Effect | Reason |
|---|---|---|

### Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

### Team  ← team / compare
person-days <x> · focus factor <f> · calendar <y> · sprint fit <✅/⚠️/❌/🔪>

### Fleet  ← orchestrator / compare
agent wall-clock <x> (<model mix>) · human review <y> · decisions pending: <n>
dispatch-ready: <yes | no — failing checks>

### Wave  ← parallel plan only
| Slot | Expected | On critical path | Confidence |
wall-clock with <N> workers: <x> · total effort: <y>

### How to use this number
- Safe: <e.g. relative prioritisation, sprint candidacy>
- Unsafe: <e.g. as a ship date — needs capacity and the open question settled>
```

For `--queue`: one table — issue, title, mode, size, expected, confidence, next
move — sorted by priority label, then a short list of items to split or spike
before they enter a sprint.

## After the packet — the orchestrator hand-off

When the executor is **Orchestrator** (or Compare recommended it), finish with
`AskUserQuestion`:

| Readiness | Options |
|---|---|
| all checks pass | **Queue it for the orchestrator (Recommended)** — post the estimate, add `size:` and the ready label · **Post the estimate only** · **Do nothing** |
| something fails | **Fix first: <the failing check>** (Recommended) — `/code-sentinel:spec #<n>` for a split or a missing spec · **Queue anyway** — the orchestrator will hold it and say why · **Post the estimate only** |

On "Queue it": do the `--post` steps below, then
`gh issue edit <n> --add-label <readyLabel>` (create the label with `--force` if
missing). Then tell the person the next command — **`/code-sentinel:orchestrator
start`** (or `next` if a fleet is already running: `tmux ls | grep '^cs-'`).
This skill never starts the orchestrator itself; that is the person's call.

Free-text estimates have no issue yet: offer **Create the issue and queue it**,
which runs `/code-sentinel:issue "<task>" --auto --ready` with the estimate
attached as a comment.

When the executor is **Team**, the closing question is only `--post` (below), if
there is an issue.

## `--post`

`AskUserQuestion` (unless `--auto`): **Post comment and label (Recommended)** ·
**Comment only** · **Don't post**. Then:

```sh
gh label create "size: M" --color c2e0c6 --force
gh issue comment <n> --body-file <tmp>
gh issue edit <n> --add-label "size: M"   # remove any other size: label first
```

The hidden `<!-- cs-estimate … -->` marker is what `--calibrate` reads later —
keep it.

## Never

- Give a single number, or the optimistic case as the recommendation.
- Pad without naming it.
- Estimate delivery when the approach is undecided — estimate the spike.
- Present points or agent hours as a date or as team capacity.
- Claim calibration you do not have.
- Write anything outside `--post` and the hand-off the person chose.
- Start the orchestrator, or queue an issue without asking.
