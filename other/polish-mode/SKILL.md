---
name: polish-mode
description: Deep polish pass — act as product manager + architect over the live product to GENERATE graded, already-decided work when the backlog runs dry or the user says "polish" / "polish mode". Produces filed issues, drafted epic specs, and backlog-pinned forks for the dev-manager — it does not build the work it finds.
---

# Polish Mode — the backlog-refill engine

One polish run = **one epic / one wake** under normal loop discipline. You are not fixing
bugs this run — you are a **product manager and architect generating the next work**: graded,
decided, filed, publishable. The loop feeds itself instead of halting on an empty backlog.

**Announce at start:** "Running polish mode — PM+architect pass to refill the backlog."

## When to use

- <person.name> says **"polish"** or **"polish mode"** (any lead-dev or ad-hoc session).
- A **lead-dev** wake finds the backlog genuinely dry: no explicit target, no in-progress
  resume, no ready epic, no open actionable bug.
- **jr-dev lanes never auto-run this** — an empty lane idle-wakes and keeps checking; it never
  halts and it never refills its own queue. Refill is the
  lead-dev's duty, so two builders never generate colliding work.

## When NOT to use

- The backlog has selectable work (select it — polish is a refill, not a default).
- You want a bug-hunt on a specific known surface → that is not a polish run.
- Mid-epic (finish or park the current item first; one item per wake).

## The five steps

### 1. Ground in direction (BEFORE looking at the product)

The product direction is **<person.name>'s existing epics and standing calls** — polish mode
extends that line, it never invents a new one. Read, in order:

1. Active specs + priorities (the project's specs dir; `current_state` ≠ done/archived) —
   what's queued, deliberately parked, already decided.
2. Standing design direction: the project's design-system / brand docs (`DESIGN.md` etc.).
3. Recent shipped-epic arc: `<data_root>/projects/<name>/status/` state-file ledger + the
   vault hot cache — what just landed and what seams it left.
4. Parked questions (`…-questions.md`) — decisions already pending; NEVER re-decide or
   pre-empt one by shipping around it.
5. The state file's record of **prior polish runs** — never re-sweep the same ground blind;
   rotate surfaces.

### 2. Sweep as a USER, judge as a PM

Role-based journeys on the live app (`<project.staging.url>`) across surfaces the last polish
run did NOT cover. **Journey coherence, not a pixel hunt**: dead ends, vocabulary/affordance
inconsistency, unfinished seams between shipped epics, "works but a real customer would stall
here." Drive each journey with short briefings, scoped surfaces and repro steps — but the
report you want is *product* findings, not just defects.

Grade every finding: **impact × effort × direction-fit**. Direction-fit is the PM filter —
a high-impact idea that starts a new product line is a *pin for the dev-manager*, not a
build item.

### 3. Judge as an ARCHITECT

For the top-graded findings, ground against the code (`<canonical_repo.host_ref>` — never
`<deprecated_mirror>`): surface patch, or structural seam? Prefer work that **closes seams
shipped epics left open** — the last 10% that makes features feel finished — over new
capability. Note concrete files/seams now; they become the `## Files` sections that make
generated epics jr-dev-lane publishable.

### 4. Decide within the envelope, then file the work

**Decide autonomously** (within reason, consistent with existing direction):
- Copy/vocabulary alignment to the project's canon; layout & composition; component
  consistency; empty/loading/error-state completeness; navigation dead-end fixes.
- Grading, prioritization, and numeric priority slotting into the global queue.
- Scoping a coherent epic from related findings; choosing seams/files.
- Closing gaps *inside* an already-approved epic's evident intent.

**Never decide — surface instead as a backlog pin for the dev-manager (refinement):**
- New subsystems or capabilities not on an existing epic's line.
- Data-model, auth, tenancy, monetization; anything irreversible.
- Direction forks (two defensible product lines).
- Anything contradicting a standing decision by <person.name> (check parked questions first).

The litmus: *"would <person.name> be surprised this was decided without them?"* If plausibly
yes → pin it.

**File the output:**
- Small graded fixes → issues on `<canonical_repo.host_ref>` (the loop's bug lane), with
  repro + severity + the graded rationale, filed with `<git_host.cli> issue create --repo
  <canonical_repo.host_ref>`. Write the body per `<suite_root>/skills/_shared/PR-PROSE.md`.
- Coherent slices → epic specs in the project's specs dir with full frontmatter:
  `current_state: drafted` (NEVER approved — promotion to `approved-for-autonomous`
  stays a human/dev-manager act), numeric `priority`, `queue_class: fleet-buildable` when
  staging-buildable, disjoint `## Files`.
- Major forks → backlog pins with `queue_class: brainstorm-pin` (the dev-manager's intake).

### 5. Publish + hand off

- Publish lane-eligible generated epics per the registry `## Queue` lane-disjointness rules.
- Record the run in the loop state file: surfaces swept, findings graded, artifacts filed —
  so the next polish run rotates ground and the 2-dry-runs signal is measurable.
- Ntfy a one-line summary: `<name> · polish run — N issues / N specs / N pins (or "dry")`.

## Honest-dry-run interplay

A polish run that produces nothing actionable is a real signal, and after **2 consecutive dry
polish runs** the backlog is genuinely empty. **Say so — and keep going.** That fact goes in the
**ntfy line**, and the fleet report's WORK section states it as a sentence
(`FleetReport.NO_WORK_SENTENCE`, fired by `no_work_anywhere`, which is derived from the registry
and disk, so no lane writes it). Neither is a reason for any lane to stop, lead-dev included.

The signal is **reported, not enacted.** A halt here would be a stopping rule used as a channel:
the seat that feeds every other lane would stop only to tell someone the product has run out of
work. The ntfy line and the fleet report are that channel, and they reach the human without
stopping that seat.

## Output contract (what "done" means for a polish run)

≥1 concrete artifact (filed issue, drafted spec, or pin) **or** an explicit "dry run —
nothing actionable" record in the state file. Every generated spec passes the frontmatter
conventions unmodified. Every pin states the fork and your recommended default. Nothing
generated was built this run.
