---
name: roadmap-review
description: Collaborative review, grooming, and scheduling of GitHub Project issues for pre-PMF startups. Use to reassess priorities, restructure milestones, close stale or superseded issues, judge whether an issue is ready to plan, or (re)build the roadmap timeline — Start/Target dates, implementation order, and developer capacity — on the board. Especially useful when capacity changes, strategy shifts, or after completing major work.
model: opus
effort: xhigh
---

# Roadmap Review, Grooming & Scheduling

## Overview

Help founders review and restructure their GitHub Project to focus on what matters most for reaching product-market fit. Three altitudes, one pass:

1. **Groom** — work the open backlog issue-by-issue: is it stale (superseded by completed work → close), not ready (needs a split / acceptance criteria / a spike), or ready to plan?
2. **Prioritize** — sequence the ready survivors against the single PMF goal and real capacity.
3. **Schedule** — write the resulting timeline back to the board: Start/Target dates, implementation order, and the developer's concurrent-capacity ceiling.

This skill **recommends** — it writes a prioritization doc and STOPs. It makes **no GitHub changes itself**; the `github-project` agent applies them on the founder's explicit OK (see [Applying the changes](#applying-the-changes)).

**When to use:**
- Feeling overwhelmed by too many priorities
- Capacity has changed (more or less time available)
- Strategy shift (e.g., moving from building to validating)
- Stale backlog — issues that may be superseded by shipped work, or "is this ready to plan?"
- The roadmap timeline/dates are out of sync with the real plan
- Quarterly/monthly planning, or after completing a major milestone

## Pre-PMF Prioritization Framework

### The Core Principle

> "Pre-PMF, your single goal should be to make 10 customers very happy. Everything you prioritize should serve this goal."

### Six Prioritization Commandments

1. **Single Priority Focus**: Concentrate all resources on one goal
2. **Stones-First Planning**: Address major bets before minor improvements
3. **Ambitious Swings**: Pursue high-impact work, not incremental gains
4. **Shortened Deadlines**: Plan every 6 weeks instead of every quarter
5. **Just-in-Time Estimation**: Define work immediately before execution
6. **Consistent Debt Allocation**: Reserve 10-30% for maintenance

### What to Focus On Pre-PMF

- **Validation over building**: Learning > shipping features
- **Depth over breadth**: 3-5 customers who desperately need you
- **Pain points over feature requests**: Build for problems, not wishlists
- **Manual over automated**: Do things that don't scale first

### Common Pre-PMF Mistakes

| Mistake | Why It Hurts |
|---------|--------------|
| Scaling too early | Burns cash before validation |
| Too many priorities | Dilutes limited time |
| Building without customers | No feedback loop |
| Premature marketing/lead gen | You need 1 customer, not 100 |
| Infrastructure before validation | Optimizing the wrong thing |

### Signs You Should Deprioritize Something

- It assumes you have paying customers (you don't yet)
- It's about "scaling" or "efficiency" (premature)
- It's not directly helping your current pilot/customer
- You're building it "just in case" or "for later"
- A competitor doing it is not validation that you need it

## The Review Process

### Step 1 — Gather Context

Fetch the current state of the GitHub Project **and** the completed-work corpus needed to detect "superseded by shipped work":

```bash
# Open issues + project fields (the live board)
gh project item-list 2 --owner samjmarshall --format json --limit 200
gh project field-list 2 --owner samjmarshall --format json
gh issue list --repo samjmarshall/personal-finance --state all --json number,title,state,createdAt,updatedAt,milestone,labels --limit 200

# Completed-work corpus (bounded ~6 months) — the comparison set for staleness
gh issue list --repo samjmarshall/personal-finance --state closed --json number,title,closedAt,labels --limit 200
gh pr list   --repo samjmarshall/personal-finance --state merged --json number,title,mergedAt,files   --limit 200
git log --since="6 months ago" --oneline
```

Also read:
- `thoughts/docs/` — non-technical project docs (strategy, messaging, pilot feedback)
- `thoughts/designs/` + `docs/adr/` — recent decisions and pivots (these tell you which areas changed)

### Step 2 — Health Pass (grooming — runs *before* discovery)

The discovery questions only matter for prioritizing *ready* survivors, so groom first. Don't deep-dive all N issues — filter cheaply, investigate only the suspicious.

**2a. Heuristic pre-filter → candidates.** Flag an issue as a candidate by cheap signals:
- *Staleness:* age by **`createdAt`** ≥ ~90 days — **not `updatedAt`**: a board-wide field write (e.g. a scheduling pass that sets/clears dates) resets `updatedAt` on dozens of issues at once, so it under-flags genuinely-old work; count `updatedAt` as activity only when it reflects a substantive edit. **OR** the issue sits in an area a recent pivot touched (infer from recent ADRs / `thoughts/designs/` / strategy docs), **OR** it overlaps a lot of recently-Done work — **this overlap signal is load-bearing**: a *recently-created* issue can still be superseded by shipped work (e.g. a seeder issue filed after the seeder merged), which the age clock alone misses. Draw staleness candidates from corpus-overlap, not age alone.
- *Readiness:* missing Priority or Size, Size = XL, or no acceptance criteria. **Exempt epics / umbrella issues** (label `epic`) — they're envelopes (Step 5), not splittable work, so XL or no-Size doesn't flag them.

Issues that pass the filter clean are **assumed Ready** — no deep-dive.

**2b. Deep-dive candidates only.** For each candidate, investigate whether shipped work already covers it: spawn `codebase-locator` + `codebase-analyzer` to check whether the feature exists, and search the closed-issue / merged-PR corpus for the same scope. Run candidates in parallel. Each returns one verdict:
- `superseded-by #X` / `delivered-by PR #X` — **with** merged-PR or commit evidence. (The deliverer is often a **PR not linked to the issue**, not a superseding issue — e.g. a CI feature an issue asked for, shipped by an unrelated PR. Cite that PR/commit, not a phantom issue number.)
- `still-relevant`
- `uncertain`

**2c. Safety rail.** An `uncertain` verdict → **Needs-investigation**, *never* Remove. A borderline issue is never recommended for closure without clear evidence.

**2d. Categorize — flat 5-bucket, precedence-ordered (first match wins):**

1. **Remove (stale)** — superseded / already-delivered / no-longer-relevant / duplicate. Tag `superseded-by #X` *or* `delivered-by PR #X` with merged-PR or commit evidence.
2. **Needs-investigation (not ready)** — relevant but not plannable. Reason from a light set: *under-specified* (no acceptance criteria) · *too coarse* (Size XL / multi-week → must be split) · *has unknowns* (needs a spike). Also catches `uncertain` staleness.
3. **Ready** — passes to discovery + prioritization (Active Now / Blocked / Post-PMF, below).

The readiness bar is deliberately light — the whole test is **"Could work start on this tomorrow without another decision?"** If no → Needs-investigation. Don't impose a heavy Definition-of-Ready; it stalls a solo dev.

### Step 3 — Collaborative Discovery (one question at a time)

Run *only for the Ready survivors* — sequencing decisions. One question at a time, multiple-choice where possible.

**Question 1: Current Reality**
> "What stage is your [current priority] at?"
> A) Haven't started · B) In progress but early · C) Actively building · D) Live and getting data

**Question 2: Blockers**
> "What's blocking you from [the most important thing]?"
> A) Nothing — just hadn't prioritized it · B) Need to finish [dependency] first · C) Don't feel ready — need to build more · D) Time/capacity · E) Something else

**Question 3: Capacity (weekly hours)**
> "How many hours per week can you dedicate to this?"
> A) <5 · B) 5-10 · C) 10-20 · D) 20+
> *(This is `H`, the scheduler's weekly-hours input in Step 5.)*

**Question 4: Time Constraints**
> "Any upcoming time off or constraints I should know about?"
> (Open-ended — capture specific dates; the scheduler skips these windows.)

**Question 5: Warm Leads**
> "Do you have any warm leads or prospects ready to engage?"
> A) Yes, [details] · B) Some possibilities but not confirmed · C) No, need to find them

**Question 6: Validation of Approach**
> "Does focusing 100% on [recommended priority] feel right?"
> A) Yes · B) Mostly, but [concern] · C) Hesitant because [reason] · D) Disagree because [reason]

**Question 7: Concurrent capacity (WIP limit)**
> "How many issues can you genuinely have in flight at once?"
> A) 1 — strict single-thread · B) 2 — one main + one small parallel (typical solo) · C) 3+
> *(Default 2. This is the scheduler's WIP input. For a solo dev, parallel lanes don't add throughput — see Step 5.)*

Also confirm **every Ready issue has a Size** (XS/S/M/L). Missing Size or Size = XL → send it back to **Needs-investigation** (not schedulable until sized/split) — **except epics**, which are envelopes (Step 5), not sized work.

### Step 4 — Prioritize the Ready survivors

Sort the Ready issues into:

- **Active Now** — directly supports the current pilot/customer, doable with current capacity, clear deliverable.
- **Blocked/Waiting** — depends on something else first; keep in backlog with the dependency noted.
- **Post-PMF / Post-Pilot (Deprioritize)** — assumes paying customers, about scaling/efficiency/marketing, or "nice to have" but not validation-critical.

(Remove and Needs-investigation were already separated in Step 2.)

### Step 5 — Scheduling Pass

Turn the prioritized **Active Now** list into a real timeline. Inputs: the Active-Now issues in priority order; each one's Size; weekly hours `H` (Q3); time-off windows (Q4); WIP limit (Q7, default 2).

**Procedure:**

1. **Size → effort-hours:** `XS=2 · S=4 · M=8 · L=20`. (XL never reaches here — Step 2 routed it to Needs-investigation. A Ready issue with no Size is not schedulable.)
2. **Daily rate** = `H / 5` working days.
3. **Walk the issues in priority order** on a calendar clock starting the next working day (or an explicit start date), skipping weekends + time-off windows:
   - `duration_days = ceil(effort_hours / daily_rate)`
   - `Start` = next free working day in lane 1; `End` = `Start + duration_days − 1` working day.
4. **WIP overlay:** default everything to **lane 1** (sequential). Mark an XS/S item as a *fill-in parallel* to the current lane-1 item to place it in **lane 2**, overlapping — capped so at most `WIP` bars overlap on any day.
   - ⚠ **Throughput stays `H`/week.** For a solo dev, parallel lanes do **not** add hours — the overlay buys *visibility of a slotted-in small task*, not speed. **The only real compression lever is Size, not WIP.** If one large item dominates the sprint (as the two L legal drafts did on 2026-06-08), flag it for re-sizing or splitting rather than reaching for parallelism.
5. **Epics / umbrella containers** aren't scheduled as work — **envelope** them: `Start` = earliest child start, `End` = latest child end.
6. **Make the capacity reality explicit.** Sum the effort and compare the computed span to the prose plan, e.g. *"this '4-week' plan is really ~7.5 weeks at 15 h/wk"*. Surfacing that gap is the point of writing the schedule back — it's what catches an over-optimistic sprint before it's committed.
7. **Parked issues** (Remove / Needs-investigation / Blocked / Post-PMF) get **dates cleared** — a dateless issue correctly drops off the Roadmap view (Just-in-Time: dateless = not-yet-scheduled).

**Output** — a **Schedule** table: `issue · Size · lane · Start · End`, plus the total span and the capacity-reality note.

### Step 6 — Propose Changes (section by section)

Present in sections, validating each before continuing:

1. **Remove candidates** — issue, `superseded-by #X` / `delivered-by PR #X`, one-line evidence, recommended close.
2. **Needs-investigation** — issue, the gap (under-specified / too coarse / has unknowns), suggested next action (spike / split / add acceptance criteria), and a pointer to `/write-tickets`. (The skill drafts nothing — recommendation only.)
3. **Deprioritize** — issues moving to Post-PMF / Post-Pilot: number, title, current milestone, one-line rationale.
4. **Keep Active** — issue, proposed Priority, dependencies.
5. **Schedule** — the Step-5 table (Start/End per Active-Now issue + epic envelopes).
6. **Milestone cleanup** — which milestones are active vs paused vs removed.
7. **Weekly Focus** — week-by-week table for the human's reading (the board carries the machine-readable dates).

### Step 7 — Confirm & Document

After the founder approves each section, write the full prioritization to:
`thoughts/roadmap/YYYY-MM-DD-roadmap-prioritization.md`

Include: context/constraints discovered · strategic rationale · the 5-bucket results (Remove / Needs-investigation / Deprioritize / Keep-Active) · the **Schedule** table · milestone restructure · weekly focus · an **implementation checklist** for the `github-project` apply step · success criteria.

## Applying the changes

**The skill makes NO GitHub changes.** It writes the doc and STOPs. After the founder approves, hand the changes to the **`github-project` agent** to apply (on the founder's explicit OK). Map each bucket to board actions:

| Bucket | Board action |
|---|---|
| **Remove** | Close as `not_planned`; record the `superseded-by #X` / `delivered-by PR #X` evidence in a closing comment. |
| **Needs-investigation** | Leave open in Backlog; **no date**; recommend `/write-tickets` to the founder. |
| **Active Now** | Set Priority; set Status → Ready/In progress; set **Start + Target dates** per the Schedule table. |
| **Blocked** | Status → Blocked; note the dependency; no date until unblocked. |
| **Deprioritize / Post-PMF / Post-Pilot** | Set milestone; **clear** Priority, Start date, Target date, Iteration. |
| **Iteration field** | **Dropped** — clear it everywhere. Iterations can't be created via API (UI-only); the board runs one timeline via dates, not two. |

**This project's Projects v2 IDs** (Project #2, `PVT_kwHOAHz9qs4AjXIr`; re-introspect with `gh project field-list` if they drift):

| Field | ID | Notes |
|---|---|---|
| Start date (DATE) | `PVTF_lAHOAHz9qs4AjXIrzgbvEgA` | `gh project item-edit --field-id … --date YYYY-MM-DD`; `--clear` to empty |
| Target date (DATE) | `PVTF_lAHOAHz9qs4AjXIrzgbvEgE` | same |
| Iteration | `PVTIF_lAHOAHz9qs4AjXIrzgbvEf8` | clear everywhere |
| Size | `PVTSSF_lAHOAHz9qs4AjXIrzgbvEf0` | XS `eff732af` · S `9592a5a3` · M `9728cbdc` · L `c53df028` · XL `7b141a16` |
| Priority | `PVTSSF_lAHOAHz9qs4AjXIrzgbvEfw` | P0 `79628723` · P1 `0a877460` · P2 `da944a9c` |
| Status | `PVTSSF_lAHOAHz9qs4AjXIrzgbvEfE` | Backlog `f75ad846` · Ready `08afe404` · In progress `47fc9ee4` · In review `4cc61d42` · Done `98236657` · Blocked `ea0591e4` |

## Key Principles

- **One question at a time**: don't overwhelm with multiple questions.
- **Multiple choice preferred**: easier to answer than open-ended.
- **Evidence before closure**: never recommend Remove without merged-PR/commit evidence; `uncertain` → Needs-investigation.
- **Light readiness bar**: "could work start tomorrow without another decision?" — nothing heavier.
- **Sizing is the schedule's only real lever** (for a solo dev): WIP/parallelism buys visibility, not throughput. Re-size or split the long pole instead.
- **Challenge assumptions**: "Do you really need X before Y?"
- **Protect focus**: fewer priorities = faster progress.
- **Validate incrementally**: check each section before continuing.

## After Documentation

**STOP after writing the prioritization document.** The skill does **not**:
- Make any GitHub changes (no close, no field edits, no date writes, no milestone moves)
- Create implementation plans or tickets

The founder reviews the doc, then explicitly directs the **`github-project` agent** to apply the changes (per [Applying the changes](#applying-the-changes)), and uses `/write-tickets` for Needs-investigation items.

## References

- Grooming design: `thoughts/designs/2026-06-07-backlog-grooming-in-roadmap-review.md`
- Scheduling / timeline design: `thoughts/designs/2026-06-08-roadmap-scheduling-timeline-writeback.md`
- [OpenView: Pre-PMF Product Management](https://openviewpartners.com/blog/the-pre-pmf-guide-to-product-management/)
- [First Round: How Superhuman Found PMF](https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/)
- [Paul Graham: Do Things That Don't Scale](https://paulgraham.com/ds.html)
- [Sequoia: Arc PMF Framework](https://sequoiacap.com/article/pmf-framework/)
- [First Round: Levels of PMF](https://www.firstround.com/levels)
