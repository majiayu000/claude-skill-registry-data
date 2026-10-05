---
name: planning
description: >
  Use BEFORE building anything non-trivial: multi-phase or multi-file work, a new
  feature, a migration, anything estimated beyond a quick edit — or whenever the
  user asks for a plan or says "let's plan this". Drives the required workflow:
  research → written plan → ALL questions asked upfront in one batch → user
  approval → autonomous execution. Do not use for trivial single-step changes
  (just do those), and do not start writing implementation code while this skill's
  approval gate is still open.
---

# Planning & Execution Workflow

Goal: once building starts, execution runs autonomously to the end — no mid-stream
questions, no re-litigated decisions. The plan phase absorbs ALL the uncertainty;
the execution phase is mechanical. The collaboration rhythm is:
**plan → refine (batched questions) → approve → execute**.

> **Who executes the plan:** when implementation is delegated to another agent that
> **cannot ask questions mid-run**, this shapes the plan itself: every brief it receives
> must be decision-complete. An unresolved choice is not something the implementer can
> work around — it is a blocker, and resolving it is what the batched-question round is
> for. (Who executes in this install: `LOCAL.md` beside this skill, when your copy keeps
> one.)

## Workflow

### 1. Research until mid-stream questions become unlikely

Read the actual code and sources — trace data flows, dependencies, and the blast
radius of the change. Consult the relevant skills (project-config for how the
project runs; domain skills for conventions). Ambiguity resolved now is an
interruption avoided later. Rule of thumb: if you can't yet name the files you'll
touch and the order you'll touch them in, keep researching.

- **Read the code before proposing a design.** A confident wrong design costs more than
  a slow one — it gets approved, and the approval makes it expensive to revisit.
- **Read the ticket, not just the screenshot.** Planning from the artifact you were
  handed rather than the request behind it produces a plan for the wrong problem.
- **Research the DESTINATION, not only the subject matter** — the target repo's git
  posture (branch, uncommitted foreign work, whether it even has a remote) shapes what
  you can deliver and, when a repo gains shareability, what is safe to write in it.
- **Repo absence ≠ live absence.** A thorough research agent "verified zero references
  across all jobspecs" and concluded nothing consumed the service; a live-verified memory
  showed a hand-deployed job — not in the repo at all — holding a live upstream to it.
  Both were right about what they checked; only the live one answers "what breaks if we
  move this". Reconcile every "nothing uses X" claim against live state before it becomes
  a plan premise, and when an agent's finding contradicts a live-verified memory, **the
  memory wins until re-probed** — surface the conflict rather than silently picking one.
- **Check the requester's own data slice before approving scope** — a request framed
  around data that turns out to be empty, stale, or an artifact changes the whole plan.
- **A per-person decision propagates: check whether the NEXT question inherits its
  shape** before asking it as if it were independent.

### 2. Write the plan down — a committed file, not a chat message

A non-trivial plan is a **committed markdown file in the project's `plans/`
directory** (e.g. `plans/pending/<slug>.md`, linked to its ticket; per-project locations
are in `LOCAL.md` beside this skill, when your copy keeps one), because a plan that
lives in chat can't be resumed, reviewed, or audited. Include:

- **Phases/steps** in execution order, each with its own verification step
  ("how we'll know this phase worked"). Per step, capture: acceptance criteria,
  a **named** verification command, files-likely-touched, and dependency links.
- **Files to touch** per phase (this also enables sub-agent partitioning — see
  the orchestration skill).
- **Decision log**: each decision with the chosen option and why.
- **Always / Never**: what is always in scope and what is explicitly never in
  scope, so scope creep is a plan violation, not a judgment call.
- **A Progress table** to be updated as phases land.

Size each step by files touched (XS/S/M/L/XL); anything L or larger must be
broken down further (execution goes cleanest on S/M). Break a step down when it
would run past one focused session (~2hr), needs more than 3 acceptance bullets,
spans 2+ subsystems, or has an "and" in its title. **Slice vertically** — one
complete path end-to-end (schema→API→UI for one feature) — not all-DB-then-all-
API-then-all-UI. Order the highest-risk steps first (fail fast) and checkpoint
every 2-3 steps.

### 3. Front-load EVERY question — one batch, before approval

Surface all decisions that need the user's input **upfront, batched together**,
regardless of which phase they touch or whether they technically block anything.
Treat anything that would require user input mid-execution as blocking now. For
each question, give a recommendation, not an open-ended survey. Sub-agents can't
ask questions at all, so an unresolved decision also blocks all delegation.

Alongside the questions, surface an explicit **Assumptions I'm making: 1…N →
correct me now or I proceed** list — silent assumptions are the questions you
forgot to ask. Reframe any vague requirement as a measurable success criterion
before you plan to it ("make it faster" → "LCP < 2.5s on 4G — right target?").
Every "ask-first" item belongs in this batch and must be settled here, never
deferred to mid-execution.

Make each question cheap to answer — the recommendation IS the technique: attach
your best guess to every question, because a user reacts to a wrong guess faster
than they generate an answer from scratch. Listen for **want vs. should-want**:
buzzword answers ("scalable", "clean", "modern") are usually the should-want — probe
with "if you didn't have to justify this to anyone, what would you actually want?".
End the batch with a one-line restate that **always includes an explicit
Out-of-scope line** (what you are deliberately NOT doing). Treat a non-answer as
unresolved, not assent: "whatever you think" is delegation, not a decision, and
"sounds good" is not the explicit yes the approval gate needs — press for the
actual call on anything load-bearing.

**The planning round's job is to FIND the questions, not just ask the known ones.** A
handed-down open-items list is a **floor, not a ceiling** — it records what the last
session knew it didn't know. In one round, three of four questions came from reading the
code rather than from the plan: two bullets written days apart each claimed the same
feature; a recorded item ("nothing auto-opens a cycle for a new paycheck") understated
its own scope so badly that one user's entire cadence had never had a cycle at all; and
an "already shipped" read path returned a raw row cast to a type it never populated,
making a card the plan treated as pure UI into backend work. **Treat every inherited
item's *scope* as a claim to re-verify, not just its answer as a question to ask** — and
treat a one-sentence bullet written weeks ago as a hypothesis about the work, not a spec.

**One question, one axis.** Ownership ("which slice owns this") and granularity ("how
many PRs, in what sequence") are independent; mixing them means a rejected option no
longer tells you what was rejected. Ask granularity *after* scope is settled — the scope
answers usually determine it anyway.

**Front-loading resolves decisions; it cannot resolve other people's actions.** A yes
from the user is **not** a yes from a third party. "Can she file one?" → "yes, asking her
now" *feels* like a locked decision but is a commitment to a future action by someone not
in the conversation. For any plan whose critical path routes through another person, add
an explicit **"confirm the human actually did it"** step between the ask and the
measurement — otherwise a negative result is uninterpretable and the timeout carries no
information. Let the human's latency set that timeout, not the machine's cadence.

**Write down what you assume happens on the far side of any boundary you don't own** —
another person, another device, another vendor's sync — then check it. Two consecutive
misses on one project had exactly this shape.

**Ask the trade-off before you act on it, not after.** A version-pinning choice (install
the newest, or the newest compatible with the other tool) was predictable at plan time,
went unasked, and produced exactly the mid-stream churn front-loading exists to prevent.
Any install, pin, or irreversible environment choice is a question, not a step.

### 4. The approval gate

Do not start implementation until the user has approved the plan. Refine the plan
through their feedback first; approval converts the plan from proposal to
contract. (Genuinely trivial work is exempt — but then you shouldn't be in this
skill at all.)

### 5. Execute autonomously, tracking progress

- Follow the plan's phase order; verify each phase with its named check before
  moving on. Don't re-run an unchanged check for reassurance — a green check on
  code that hasn't moved tells you nothing new.
- Slice risk-first: prove the risky dependency works before building on it. Keep
  the tree compilable/green between slices, and keep increments rollback-friendly
  (migrations get down paths; don't delete-and-replace in one commit).
- Before each slice, run a simplicity check: are the abstractions earning their
  complexity? Three similar lines beat a premature abstraction; if a staff
  engineer would say "why didn't you just…?", do the simpler thing.
- Keep the trackers current as phases land: the plan file's Progress table, and
  the repo's plan lifecycle files where they exist (e.g. `plans/PROGRESS`,
  pending/done lists) — stale trackers make the plan lie to the next session.
- When a decision changes mid-flight, update the plan file's decision log first,
  then reference it in the PR — the plan is a living spec, not a frozen proposal.
- If context runs low mid-program, hand off at a phase boundary (handoff skill)
  rather than degrading through the tail of the window.

### 5b. A locked decision can expire

"Locked" means *don't re-litigate*; it does not mean *don't re-derive*. A decision made
in an earlier phase was made in a world that no longer exists.

- **Before executing a decision locked in an earlier phase, ask what has shipped since
  that changes its consequences** — new guards, constraints, immutability rules,
  permission checks; anything that makes a previously-cheap action expensive or
  irreversible. A program locked "back-fill and close all 38 historical cycles"; three
  slices later a *different* slice shipped an immutability guard, so executing that
  decision literally would have closed the user's current cycle and handed her an app
  that 409'd her own edits — a user-visible breakage, faithfully implementing an
  approved decision. Nothing flagged it: the two decisions lived in different sections,
  both marked LOCKED.
- **Re-litigating asks "was this the right call?"; re-deriving asks "does this still do
  what we thought it would do?"** Only the second is your job.
- **Bring it back as a question, not a unilateral override.** The decision is still the
  user's; what changed is the information. "D13 said all 38, but here is the consequence
  the guard now creates, and here's what I'd do instead" got an immediate correction.
  Silently obeying *or* silently overriding would both have been failures.
- **A locked decision can also be simply un-implementable.** When ground truth
  invalidates it — a target that turns out to be a hand-edited artifact with no coherent
  definition — **stop and bring numbers.** Front-loading buys autonomy on *what to
  build*; it is never a mandate to build something you have since learned is wrong.
- **Then prove the consequence rather than asserting it.** A three-line observed output
  (`closed → 409` vs `newest → edit allowed`) is what makes the decision reviewable later.

### 6. Mid-stream surprises: handle, then feed back

If something genuinely unforeseeable surfaces mid-build, don't guess on a real
decision — ask. But treat it as a **planning miss**: record what should have been
asked upfront (in this skill's LEARNINGS.md), so future plans catch that class of
question earlier. The interruption rate should trend to zero.

**Grade the misses honestly, because mid-stream questions cluster where you didn't
look — not where the plan was vague.** In one session three well-formed upfront
questions were followed by three mid-stream ones: one was genuinely undiscoverable
without probing the code (fine), but two came from an unexamined dependency the plan had
*told* me was healthy. **The upfront-questions discipline fails silently at the edges of
what you chose to look at**, so a "this part is already done" boundary is exactly where
to spend a verification minute.

**"X was verified working" is only true as of the moment it was written.** A plan opened
"Phase 1 is DONE, so Phase 2 is unblocked" and the handoff memory said the dependency was
live; both were taken at their word, a whole phase was built, a PR merged and a package
published — and only then did the dependency turn out to have been down for 2.5 hours.
The work was correct and unverifiable, and the session ended blocked. A liveness check
takes seconds and belongs in the **research** step, before the plan is even confirmed.

### 7. Close the loop

When the plan finishes: move the plan file to that same `plans/` tree's `archive/` with a short
execution record (what shipped, deviations from plan, verification evidence), and
update the lifecycle trackers. An unarchived finished plan pollutes the pending
list for every future session.

## Common failure modes

- **Building while "planning".** Writing implementation code before approval
  voids the gate — the user ends up reviewing a fait accompli.
- **Trickling questions.** Asking one question, building, asking another — each
  interruption is exactly what front-loading exists to prevent.
- **Questions without recommendations.** "Option A or B?" pushes the research
  back onto the user; recommend one and say why.
- **A plan with no per-phase verification.** "Then it works" is not a check; name
  the command/observation that proves each phase.
- **Chat-only plans.** Not resumable, not reviewable; commit the file.
- **Finished plan never archived / trackers stale.** The next session trusts the
  trackers; keep them true in the same turn the state changes.

## Before you call this done

- [ ] Plan exists as a committed `plans/` file with phases, files, decisions, verification
- [ ] All user decisions were asked in ONE upfront batch, each with a recommendation
- [ ] User approved before implementation began
- [ ] Each phase's verification ran and passed (or the failure is reported honestly)
- [ ] Progress table + lifecycle trackers current; finished plan archived with an execution record
- [ ] Any mid-stream question was recorded as a planning miss in LEARNINGS.md

## Related skills

- [idea-refine](../idea-refine/SKILL.md): when the idea itself is still vague, refine it there first; its one-pager is this skill's input.
- [project-manager](../project-manager/SKILL.md): a plan is linked to its ticket; that skill makes sure the ticket exists and reads well.
- [information-architecture](../information-architecture/SKILL.md): where content, pages and nav items live is a plan-time decision; lock it in the batched question round.
- [security-and-hardening](../security-and-hardening/SKILL.md): its "Ask first" list is a plan-time question set; fold it into the same round.
- [source-driven-development](../source-driven-development/SKILL.md): a docs-vs-codebase conflict is raised here, at plan time, not mid-build.

## Capturing learnings (session-handoff protocol)

Accumulate planning lessons in `LEARNINGS.md` beside this skill, when your copy keeps
one: classes of questions
that surfaced mid-stream (so future plans front-load them), plan structures that
executed cleanly, phase-sizing that fit a session. Dedupe; read before writing
the next plan.
