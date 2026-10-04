---
name: refactor
description: >-
  Evidence-driven refactoring — where does structural improvement actually
  pay off, then make that change without changing behavior. Survey mode
  diagnoses by evidence, not aesthetics — git churn × complexity hotspots,
  the recurring-bug log, upcoming work — and verdicts each candidate
  REFACTOR/PREP/LEAVE/WATCH, where LEAVE is the default and "the textbook
  recommends it" is never a reason. Execute mode takes one approved
  candidate in small behavior-preserving moves, suite green after each.
  Keeps a debt register in out/refactor/tracker.md so repeat surveys open
  with what changed. Use for "clean up this module", "improve the
  architecture", "pay down tech debt" — e.g. "/refactor",
  "/refactor <target>". For new behavior use feature; for something broken
  use bugfix.
---

# refactor — earn it first, then preserve behavior

`/refactor` — survey the repo, emit a brief of where improvement pays off
`/refactor <target or goal>` — execute one candidate, safely

Answer one question: **where does structural improvement actually pay for
itself in this codebase — and how is that change made without changing
behavior?** The skill exists to prevent the two documented failure modes of
"improve the architecture": refactoring the wrong code (most ugly code is
never touched again, so cleaning it returns nothing), and **pattern-itis** —
applying design patterns because they're best practices rather than because
a problem here demands them, turning straight-line code into abstraction
lasagna.

## Survey mode — `/refactor`

### Step 1 — Evidence, not aesthetics

Candidates come from signals, never from "this code looks bad":

- **Hotspots** — churn × complexity. Churn from git itself:
  `git log --format= --name-only --since="12 months ago" | sort | uniq -c |
  sort -rn | head -30`, crossed with a complexity proxy (file length,
  indentation depth). Code that is both complex *and* frequently edited is
  where interest compounds; complex-but-cold code is a LEAVE by default.
- **The bug log** — `out/dev/bugfix-log.md` if present. A file that shows up
  repeatedly is structural debt announcing itself.
- **Upcoming work** — the user's stated goals, open specs and plans under
  `out/dev/`. These seed **PREP** candidates: make the change easy, then
  make the easy change — preparatory refactoring is the highest-payoff kind
  because the payoff is scheduled, not hoped for.
- **The map** — `AGENTS.md` gotchas and conventions; a documented gotcha is
  often a workaround for structure that could stop needing one.
- **Memory** — `out/refactor/tracker.md` if it exists: verdicts already
  made. A LEAVE with a reason isn't re-litigated unless its evidence
  changed; repeat surveys open with **"Since last survey"**.

### Step 2 — Verdicts, with the pattern gate

For each candidate: **REFACTOR / PREP / LEAVE / WATCH**.

- **LEAVE is the default.** Promotion needs positive evidence: churn, a
  recurring bug, or scheduled work in the area. "This violates a principle"
  alone promotes nothing — cold code keeps its sins.
- **The pattern gate:** a design pattern is vocabulary, not a goal. Every
  proposal that introduces one names the problem *in this codebase* (with a
  file:line locator and its evidence), why *this* pattern fits, and what
  simpler shape was considered first. "The textbook recommends it" is
  discarded, not weighed. Two quick tests: **the deletion test** — imagine
  deleting the module; if complexity vanishes it was a pass-through, if it
  reappears across N callers it was earning its keep — and **one adapter is
  a hypothetical seam, two are a real one**: don't introduce a seam until
  something actually varies across it.
- **The score is interface depth, not pattern count.** A proposal wins if
  interfaces get simpler and callers get dumber — abstractions that hide
  more than they add. A refactor that grows the number of things a reader
  must understand has failed even if every step was clean.
- Each REFACTOR/PREP carries: the problem + locator, the target shape, a
  sketch of the move sequence, effort, and risk. Candidates too big to stay
  behavior-preserving (real redesigns) are phrased as ready `/feature` or
  `/autopilot` handoffs instead — offered, never performed.

### Step 3 — Brief and register

Render the brief **in chat** per `references/brief-template.md` (read it
when you reach this step), save to `out/refactor/<slug>-<YYYY-MM-DD>.md`
(date via `date +%F`; create the folder if needed; committing is the user's
call), and update `out/refactor/tracker.md` — one row per candidate:
candidate · verdict · evidence · date · status. The user picks what to
execute; the survey never starts cutting on its own.

## Execute mode — `/refactor <target>`

### Step 1 — Safety net before scalpel

- Find the test command (`AGENTS.md`, manifests, CI config) and run the
  suite for a **green baseline**. A pre-existing red is reported and stops
  the run — refactoring on red has no arbiter.
- Area untested? Write **characterization tests** around exactly the code
  to be touched — pin current behavior *as it is, bugs included* — and
  commit them separately before any restructuring. Without them, "behavior
  preserved" is an opinion.

### Step 2 — Small named moves, green after each

Plan the sequence as named moves — extract function, move module, rename,
inline, introduce parameter object — then per move: apply it, run the
suite, checkpoint commit titled with the move. The rhythm is the safety:

- **Red after a step → revert that step.** Never patch forward to green — a
  patched-forward red is a behavior change wearing a refactor's name.
  Rethink the move or split it smaller.
- Every checkpoint leaves the tree shippable. There is no big-bang branch
  where everything is broken until the end.
- **Wide mechanical moves** (a rename or retype fanning across hundreds of
  call sites) sequence as **expand–contract**: add the new form beside the
  old so nothing breaks, migrate call sites in blast-radius-sized batches
  (per package or directory, checkpoint each), then contract — delete the
  old form once no caller remains. The tree stays shippable through the
  whole fan-out.

### Step 3 — Behavior-preserving is the definition

- **A bug found mid-refactor is logged** (`out/dev/bugfix-log.md`, offered
  as a ready `/bugfix` invocation) and its behavior deliberately preserved.
  Fixing it in flight changes behavior and poisons the diff's reviewability.
- No new features, no "while I'm here" improvements outside the stated
  goal, no public-interface changes the goal didn't name.

### Step 4 — Ship, then refresh the map

- Run **done** on the diff. The spec it reviews against is exactly:
  *behavior unchanged, structure goal met* — its evidence checklist and
  fresh-context review apply verbatim.
- Update the tracker row (status, date, commit).
- Structure changed means the map is stale: finish with `/map refresh`.

## Auto mode — under autopilot

Driven by **autopilot** (or explicit auto), the survey's brief-approval
becomes a self-approval on the record in the run's `log.md`, and only
candidates whose evidence survives the pattern gate proceed; anything
arguable parks. Execution changes nothing — the suite was already the
arbiter, and every hard rule above holds verbatim.

## State

`out/refactor/`: `tracker.md` (the debt register) and dated briefs. An
interrupted execution resumes from `git log` — the checkpoint commits *are*
the state — plus the tracker row; never from conversation memory.

## Guardrails

- **LEAVE is the default.** Payoff requires churn, bugs, or scheduled work;
  aesthetics promote nothing.
- **"The textbook recommends it" is never a reason.** A pattern needs a
  named, located problem in this codebase.
- **Behavior-preserving or it isn't refactoring.** Bugs are logged and kept,
  features wait, the goal bounds the diff.
- **Tests are the arbiter.** No suite → characterization tests first; red
  step → revert, never patch forward.
- **Interface depth is the score.** If callers didn't get simpler, adding a
  pattern made it worse — pattern count is not a metric.
- **The survey never cuts.** Diagnosis and execution are separate consents;
  the brief recommends, the user picks the target.
