---
name: feature
description: >
  Runs the full feature workflow: plan, critique, implement, review, QA. Use
  this when starting a new feature. Guides you through each phase with explicit
  gates between steps.
---

# /feature — AI-Assisted Development Lifecycle

Activate this skill for non-trivial features or changes to run the full
structured development workflow: plan → critique → implement → test →
code-review → QA → PR.

---

## Workflow

### Step 1 — Draft, critique, and approve the plan

**Preconditions — check the branch first.** The workflow assumes the human
started this session on a fresh feature branch: the code review (Step 4)
diffs against the default branch (named in `AGENTS.md` → *Commands*) and
Step 9 opens a PR targeting it, neither of which works from the default
branch itself. If the session is on the default branch, STOP and ask the
user to create a feature branch — you may not create or switch branches
yourself (Rule 3 in `AGENTS.md`).

**Enter plan mode now**, before drafting. Plan mode is a structural
commitment: while in plan mode the harness blocks edit tools, so the
workflow cannot skip the approval gate even if the agent is tempted to
inline the plan and proceed. Stay in plan mode through steps 1a, 1b,
and 1c. Exit plan mode only in step 1c, after the user approves.

#### Step 1a — Draft the plan

Invoke the `planner` sub-agent to draft an implementation plan. Pass the
user's prompt verbatim — including any reference to docs or links. The
planner will fetch all external specs with its own tools (it has `WebFetch`
for URLs) and return the plan as markdown text.

Do not use tools directly — always delegate to the planner sub-agent,
regardless of which platform you are running on.

#### Step 1b — Critique the plan

Invoke the `plan-critic` sub-agent with the draft plan as input. The critic
will apply pre-mortem, inversion, load-bearing assumption analysis, and
consistency checks against ADRs and product docs, and return the critique
as markdown text.

Skip this step ONLY if the change qualifies as trivial under ALL of:
- diff is plausibly under ~50 lines of non-test code,
- touches none of the project's sensitive areas (the *Sensitive Areas*
  section in `AGENTS.md` is the canonical list),
- introduces no new public endpoints, no new persisted fields, no new
  external dependencies,
- AND the user explicitly said "skip the critic" (or equivalent) in
  this session.

If any condition fails, run the critic. When in doubt, run it. Do not
infer "trivial" from your own read of the plan — the user has to ask.

#### Step 1c — Present plan and critique for approval

Present BOTH the plan and the critique to the user for approval, using
whatever mechanism the harness provides for exiting plan mode.

**Lead with the approval screen**: the plan's **Approval Summary** first,
immediately followed by the critique's **Confidence** verdict and its top
findings (any suggested amendments the user is likely to want). This is
what the user reads on a phone. The full plan and the full critique follow
below, clearly separated — make clear which sections are the plan and which
are the critique; do not interleave them. The user reads the approval
screen (and drills into the detail only where needed) and decides whether
to approve as-is, amend the plan based on critique findings, or request a
re-plan.

Do not proceed until the plan is approved. On a substantive change (new
scope, a different approach, or reworked requirements), re-enter plan mode
and re-invoke the `planner` sub-agent to revise the plan — do not re-plan
yourself — then re-run the `plan-critic` and re-present for approval. When
re-presenting a revised plan, lead with a short **delta** section — what
changed relative to the previously presented version — so the user re-reads
only the changes, not the whole plan again.

If the user approves the plan conditional on adopting specific critique
amendments ("approved, but also address point 2"), you may fold those
specific amendments into the plan text yourself before implementing — that
is transcribing an accepted decision, not fresh planning, so it does not
need another planner round. The `code-critic` and `adversarial-qa` sub-agents receive
only the plan text — an amendment that lives only in the conversation is
invisible to them.

After approval, retain the plan text — you will pass it to the
`code-critic` and `adversarial-qa` sub-agents later.

### Step 2 — Implement

**Acceptance tests first.** Before implementing, write the end-to-end tests
from the plan's Test Strategy — at minimum the `[AC-<slug>-n]`-tagged ones. They
encode the approved contract, so drift from the plan surfaces as a failing
test during implementation instead of a surprise at review. Tests derived
from the plan may not be weakened, loosened, or rewritten to make them pass
— if one turns out to be wrong, treat it as a plan deviation (below): flag
it, don't silently adjust it.

Then implement the approved plan in small logical steps until the suite is
green. Run the test suite once a coherent unit of work is complete (e.g.,
after finishing a module or a meaningful set of related changes) — not after
every individual step.

**Look up current library/API docs instead of relying on training-time
memory for version-sensitive details.** Before writing code against an
external library or framework — especially anything that could have
changed since training (recent APIs, config shape, breaking changes) — use
the bundled `context7` MCP server — resolve the library ID, then query its
docs — to pull current docs rather than guessing. Skip it for stdlib/language-core usage you're
already confident about. This is a quality aid, not a gate like the
canonical commands in Rule 1 — if the lookup errors or the library isn't
found, note it in your summary and proceed on your best existing
knowledge rather than stopping the implementation step over it.

If you discover something during implementation that changes what needs to be built,
stop and assess the impact:

- **Minor** (an implied edge case, a small clarification): note the deviation
  and inform the user with a brief note before continuing.
- **Material** (scope change, different approach, new requirements): stop,
  re-enter plan mode, update the plan, and present it for re-approval
  before continuing.

### Step 3 — Run all tests

All tests must pass before proceeding. Run the project's run-all-tests
command (`AGENTS.md` → *Commands*).

### Step 4 — Code review

Commit your work first — the review must cover the committed state, because
`scripts/review-ok.sh` (Step 6) records the reviewed commit SHA and the pre-push
hook compares against it.

Invoke the `code-critic` sub-agent to review all changes against project
standards. Pass the approved plan text, and include the summary output of the
most recent full test-suite run (Step 3). The reviewer is not allowed to run
the test suite itself — it verifies coverage statically and needs a record
that the committed tests ran and passed on the reviewed state. That summary
comes from you, the implementer, so it is a record, not independent proof
(see *Deterministic enforcement* in the AI Workflow plugin's own
documentation) — this workflow's job ends at a well-vetted PR; whether your
project's own CI provides independent evidence on top of that is outside
this workflow's scope.

**Escalate the model on the security surface.** The `code-critic` runs on
Sonnet by default (see its wrapper). If the diff touches the security surface
— the *Sensitive Areas* section in `AGENTS.md` is the canonical list — invoke
the `code-critic` with its model overridden to `opus` for that review: Opus is
the stronger bug-finder, and this surface is where a missed finding is most
expensive. Sonnet stays the default everywhere else. (This is the model-tier
counterpart to the second-reviewer-pass recommendation in Step 9.)

### Step 5 — Relay NEEDS_DECISION items

If the reviewer flags any `NEEDS_DECISION` items, **stop and present ALL of them
to the user**. Wait for answers before proceeding.

### Step 6 — Fix FAIL items

If the reviewer found critical issues (`FAIL`), fix them and re-invoke the
`code-critic`. Repeat until no critical issues remain.

Do not push or open a PR until the `code-critic` has passed with no FAIL
items (see *Rules — non-negotiable* in AGENTS.md). Re-run the reviewer after
any later change, including fixes prompted by Step 8 QA findings.

**Record the pass.** After a pass with no FAIL items on the committed state
(see Step 4 — the review always covers a commit), run
`scripts/review-ok.sh` — it records the reviewed HEAD, and the pre-push hook
(`githooks/pre-push`) blocks pushing any other commit. Any commit made after
the review makes the marker stale by design: re-run the reviewer, then
`scripts/review-ok.sh` again on the new HEAD. Never run it without a passing
review of the current HEAD.

### Step 7 — Exploratory QA

Run this step only when the change has a **UI and/or API surface**: the diff
touches templates/views, static assets, a controller path that renders a
view, fragment, or client-driven (e.g. HTMX/AJAX) response, or exposes/changes
a REST (or other network-callable) endpoint. For changes with neither surface
(pure internal service/repository logic, migrations, build/config work), skip
this step and state in your summary that QA was skipped and why. When in
doubt, run it.

Invoke the `adversarial-qa` sub-agent for an adversarial probe of the feature
through whichever surface(s) it exposes. Its role is to catch things the plan
and the committed tests did not anticipate — NOT to re-verify the plan's
Requirements (those are locked down by the committed end-to-end tests written
during implementation). Pass the approved plan text so the agent understands
the feature, not as a checklist. Also pass the project's open deferred QA
findings — even an empty list ("none open"), never omit it: run
`AGENTS.md` → *Task Tracking* → *List open deferred QA findings* if that
bullet holds a real command or tool call (not a `[TODO:]` placeholder and
not `none`), otherwise `gh issue list --label known-issue --state open`. If
the bullet names a real command or tool call you cannot run, do not fall
back to `gh` — that would silently query the wrong tracker; STOP per Rule 2
and report it instead. You fetch and hand it over rather than leaving the
sub-agent to do it, since it has no tracker tools beyond `Bash`.

### Step 8 — Relay QA findings

If the QA agent surfaces any findings, present them to the user before opening
a PR and wait for direction on each (fix now, defer, or ignore).

For each finding the user chooses to **defer**, file a task tagged
`known-issue` — using `AGENTS.md` → *Task Tracking* → *File a deferred QA
finding* if that bullet holds a real command or tool call (not a `[TODO:]`
placeholder and not `none`), otherwise `gh issue create --label known-issue
…`. If the bullet names a real command or tool call you cannot run, do not
fall back to `gh` — STOP per Rule 2 and report it instead of filing into the
wrong tracker. Describe the behaviour, where it
lives, the QA pass that found it, and sign it with model attribution. QA
evidence under `.qa-evidence/` is session-local (gitignored), so the task
body must stand alone: include reproduction steps and describe in words what
the evidence showed. The QA skill checks that tag on every pass, so deferred
findings are reported as known instead of being re-triaged each time. Do not
file tasks for findings the user chooses to ignore outright.

### Step 9 — Open PR

Only open a PR after the code review has passed and every QA finding has
been dispositioned (fixed / deferred / ignored) — or QA was skipped because
there is no UI or API surface.

The PR body is where the human review starts — it must carry the pipeline's
conclusions so the reviewer does not have to reconstruct them from the diff
or a session transcript:

- **Plan summary** — the requirements and approach in a few sentences, plus a
  link to the source spec if there was one.
- **Acceptance criteria → test table** — one row per `AC-<slug>-n` from the
  plan's Approval Summary: the criterion, and the committed test(s) tagged
  `[AC-<slug>-n]` that prove it. This is the reviewer's traceability skim —
  a criterion without a test row must not reach the PR (the code-critic
  enforces this earlier).
- **Review outcome** — the final code-review verdict, every `NEEDS_DECISION`
  that was raised, and the decision the user made on each.
- **QA outcome** — findings with their dispositions (fixed / deferred with
  task id / ignored), or "skipped: no UI or API surface". Describe each finding
  in words — `.qa-evidence/` is gitignored and session-local, so its paths
  are dead links to anyone reading the PR; the durable record for a deferred
  finding is its `known-issue` task.
- **Test evidence** — one line: the test count and result from the final
  full test-suite run.

If the branch touches the security surface (the *Sensitive Areas* list in
`AGENTS.md`), say so explicitly in the PR body, and give that surface a
second, independent look
before merging by re-running the `code-critic` sub-agent in a fresh context.
A single reviewer pass is the last line of defense there; the project's own
review is the no-cost way to get a second.

<!-- SKILL NAMING NOTE (Claude Code): the review skill is named `code-critic`
     precisely so it does NOT shadow Claude Code's bundled `code-review` skill
     (project skills shadow bundled skills completely). The bundled
     `/code-review` — including `/code-review ultra`, the billed cloud review —
     therefore stays reachable as an optional, user-launched deep pass on an
     especially high-stakes change. It is not a standard step. Do not rename
     the skill back to `code-review` unless you want the shadowing. -->

---

## Important Rules

- NEVER skip the planner step for new features. Implementation without an approved
  plan leads to rework.
- NEVER skip the plan-critic step unless the trivial-change criteria in
  Step 1b are ALL met AND the user explicitly opted out. The default is
  always to run the critic.
- NEVER fetch external links or docs directly — always delegate to the planner
  sub-agent, regardless of platform.
- NEVER enter plan mode from within a sub-agent — only the main agent presents
  plans for review.
- NEVER present work to the user before the `code-critic` sub-agent has reviewed
  it.
- If a sub-agent flags `NEEDS_DECISION`, you MUST relay ALL flagged items to the
  user and wait. Do not make these decisions yourself.
- Sub-agents are read-only for review purposes — only the main agent implements
  changes.
