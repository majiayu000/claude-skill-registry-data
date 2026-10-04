---
name: pipeline-auto
description: Use when the user wants a substantial feature taken from idea through implementation in one run with as little interruption as possible ("just build it", "don't keep asking me"), or when controlling such a run and a worker question, quorum responses, the drift budget, a human decision, a review class or a completeness item needs a decision, especially under deadline pressure. Not for a run where the user is consulted at each decision; that is superb:pipeline.
argument-hint: "[resume|status]"
---

# pipeline-auto: controller rules

Machines may unblock work. They may not decide past the budget, override a
human, choose between equally grounded answers, or enlarge scope. When a rule
says escalate, escalating **is** the decisive action. Deadline, billing and "too
cautious" pressure change none of these rules.

## The rule this skill reverses

`superb:pipeline` forbids "a Brain Agent that decides user requirements"
(`skills/pipeline/references/planning.md:177-181`), and its zero-assumption law
(`skills/pipeline/SKILL.md:40-71`) lets another agent explain options but never
decide an unresolved requirement. **This skill is that Brain Agent**, built on
purpose. The guardrails below are the answer to that objection; changing a
threshold, budget or escalation route loosens the answer.

| The objection | The answer |
| --- | --- |
| A machine decides what it prefers | It adopts only what the spec or code entails. `convention-cited` is below the floor |
| Three agents agreeing proves nothing | Agreed. The bar is grounding rung, not votes; reading assignments decorrelate the three |
| It will decide more and more | 3 adoptions per phase, 10 per run, checked before dispatch; only a human extends, at most twice |
| It will overrule the user | A candidate contradicting `Provenance: human` is rejected at any rung |
| It will build what nobody asked for | Stage 06 seals the phase set; the tracker creates phases only at stage 07 and only for sealed ids (the ids themselves are not checked against the master plan); `MISSING-FROM-SPEC` is frozen |
| It will drift from the request | Depth cap 2 from the last human answer |
| It grades its own homework | Every adoption is labelled `Provenance: quorum`; the terminal report leads with them, weakest first |

Want the user consulted at each decision? Use `superb:pipeline`. This is a
different trade, not a better version.

## Invocation

Trim `$ARGUMENTS` and select exactly one mode:

| Argument | Mode |
| --- | --- |
| empty | Full run from stage 01 |
| `resume` | Resume one compatible `pipeline-auto/v1` run from its files and Git. Never create or replace a run |
| `status` | Strictly read-only: no lock, write, reconcile, dispatch, test, fix or initialize |
| anything else | Ask what the user meant. Do not guess a verb |

For `resume` and `status`, use [references/persistence.md](references/persistence.md).
No identifiable run: say so. Several: ask which. Recency is not selection
authority.

## The one gate, and files as the authority

**Stage 03 asks at most four questions in one `AskUserQuestion` call.** Those
answers are the only unimpeachable requirements. Every later decision is a
quorum adoption or an escalation: no third outcome, no controller override, no
second approval.

Reconstruct the next action from `progress.md`, `decisions.md`, immutable
results, evidence digests and Git — never from conversation memory. The schema
is `pipeline-auto/v1`; there is no migration from `pipeline-run/v1` or `/v2`.
Foreign, missing, malformed or unknown schema is a read-only stop: change
nothing, dispatch nothing.

## Stage routing

Load only the reference the active stage needs. The rules in this file apply at
every stage and win over any summary elsewhere.

| Stage | Work | Route |
| --- | --- | --- |
| 01–07 | Intent read, question synthesis, the gate, design and review class, spec, master plan, phase fan-out | [references/planning.md](references/planning.md) |
| any | Question raised, quorum open or finalising, drift budget, escalation, quorum resume | [references/quorum.md](references/quorum.md) |
| 08–10 | Dial, task start, per-task gate, TDD, scopes, evidence, integration, debugging | [references/execution.md](references/execution.md) |
| 11–12 | Master gate, contradiction routing, adjudicator, completeness, final verification, terminal report | [references/review.md](references/review.md) |
| any | Tracker writes, status, resume, reconciliation, decision actions | [references/persistence.md](references/persistence.md) |

| Dispatch | Template / agent | When |
| --- | --- | --- |
| Intent readers | `pipeline-auto-intent-reader` ×3 | stage 01 |
| Brains | `pipeline-auto-brain` ×3 with `prompts/brain.md` | every quorum |
| Proposal brains | `pipeline-auto-brain` ×3 with `prompts/brain-proposal.md` | stage 02 |
| Implementer | `prompts/implementer.md`, brief from `scripts/task-brief RUN_DIR PLAN_FILE TASK_NUMBER` | stage 09, one fresh per task |
| Task reviewer | `prompts/task-reviewer.md`, package from `scripts/review-package RUN_DIR BASE HEAD` | the per-task gate |
| Adversarial reviewer | `prompts/adversarial-reviewer.md` | any fired trigger, any `review_class` |

Both agents run with exactly `Read`, `Grep`, `Glob`. Never add a tool to either
— not even `Bash` "for one command": frontmatter allowlists tools, not
commands, and a shell can rewrite `decisions.md` or the intent brief. Never
substitute `brainstorm-architect`.

The SDD review protocol is inlined in `prompts/` and `scripts/`; do not invoke
`superpowers:subagent-driven-development` or
`superpowers:finishing-a-development-branch`.

## Rungs, strongest first

`specified` > `code-evidenced` > `convention-cited` > `engineering-judgement` > `speculation`

"Stronger" always means **earlier in this list**. A cluster's rung is its
strongest member's rung, after demoting any member whose citation does not
resolve to its claim. The adoption floor starts at `code-evidenced` and rises one
rung for the rest of the run once five or more adoptions average above 0.90 —
read it from `current_floor`, never assume it.

## Escalating, exactly

Finalise the question as `escalated`, queue it now for the next stage boundary
(even mid-phase), and set `next_action: await-escalation-batch`. Escalating never
draws on the adoption budget.

Recording `unresolved`, `open`, `deferred`, or carrying it in the handover is
**not** escalating. It asks nobody.

While a question is escalated, every task blocked on it stays blocked and
**nothing** is dispatched on its axis — no trace, no fact-finding, no fresh
quorum, no "safe", "additive" or "reversible" subset of the work. The hold lasts
until a human answers, not until you judge the work cheap to undo.

## Before opening a quorum, in this order

These checks run **before** a quorum opens. Once a quorum has returned, judge it
by the adoption rules below — never retroactively un-ask it.

1. **Already answered?** If the approved spec or an adopted decision answers it,
   the question is not admitted to a quorum. Cite the line on the question
   record and resume the worker. No quorum, no decision entry, no budget.
2. **Budget.** Read `quorum_budget(run_dir, phase=...)` before any dispatch.
   Ceilings are `BUDGET_PER_PHASE` (3) and `BUDGET_PER_RUN` (10). Only a human
   answering an escalation raises one, to a stated finite value; at most two
   extensions per run, then the budget is terminal. If a ceiling is reached:
   open no quorum of any size — no worker anywhere opens one — lower no bar,
   and escalate with the adopted decisions listed. Hold dispatch and
   integration within the question's blast radius (in-flight work there
   finishes, publishes and is imported); independent work continues. A
   terminal budget stops the run resumably: nothing new is dispatched. You
   never grant yourself an extension.
3. **Admissible** (`check_admissible`), all of:
   - it blocks named work — a question blocking nothing is an opinion; discard it;
   - it is decidable from the repository, the spec and `decisions.md` — if it
     needs what only the user knows (budget, deadline, users, purpose), escalate;
   - it carries an axis and a blast radius from `task | phase | run | contract`;
   - it passes the options test and is one decision.

   Then dispatch exactly three brains.

## Evaluating a quorum

**Three valid responses is a precondition, not a strength.** With fewer, the
quorum is not evaluated — not now, not at a deadline, not through any guard,
timeout or policy you write in advance. Two agreeing, well-cited responses are
two responses.

- **A missing response** (its worker died, or context was lost): re-dispatch only
  the missing index, re-sent from its own persisted payload and checked against
  its digest — never rebuilt from current state. This is recovery, not a second
  chance. Never re-dispatch
  a brain that answered; never discard an answer to get a tidier set.
- **A schema-invalid value** (for example a rung not in the list above): never
  map, default or demote it. Re-dispatch that index **once**, with its full
  rebuilt payload — never "just fix that field", never with its answer pinned.
  The quorum waits on it. A second invalid response is a non-response: escalate.
- **A brain's own question** has no field in the schema; `blocker` is the only
  exit. A response asking for something else to be decided first is a
  non-response. Do not open a quorum on it, do not answer it yourself — not even
  "the other responses imply it" — do not re-dispatch with the premise supplied.
  Escalate the original question, naming the premise.

**Adoption.** Cluster by `answer_key` when options were named; without named
options, answers share a cluster only if their consequences do not contradict
(when in doubt they are different answers). Then compare rungs. Adopt only when the
winning cluster is **strictly stronger** than the runner-up, at or above the
current floor, fewer than two responses carry a blocker, nothing forecloses an irreversible
axis, depth is within the cap, budget remains, and `check_contradiction` returns
nothing.

- **One cluster** (unanimity) has no runner-up: the floor alone decides.
- **Equal rungs never adopt**, at the floor or at the top. No tie-break —
  not headcount, subset consequences, citations, recency, length or "least
  foreclosing". Escalate.
- **Different answers alone are no reason to escalate.** One cluster strictly
  stronger than the rest adopts, however many clusters there are.
- An adoption records the answer, the winning rung and the rung it beat, and
  `Provenance: quorum`; it consumes one phase and one run adoption. The
  adoption `Q-<qid>` is itself the grant: resume the blocked task with
  `resume_task(..., decision_ref="Q-<qid>")`. A re-asked question's adoption
  resumes the task too, under its new qid. After an escalation, the human's
  `task.resume` `H-<n>` resumes it once the escalation row is `answered` with
  that `Resolution`.

## Recorded human decisions

If the winning answer — consequences included — requires a different option on
an axis where an adopted decision has `Provenance: human`, reject it. No rung and
no unanimity outranks a human's recorded answer. Record
`rejected-contradicts-human` naming that decision's ID; it stays `Adopted`; no
budget is spent; escalate (`finalize_quorum` queues the row). Every task blocked on that axis stays blocked — "the
human decision is still in force, so work against it" is dispatch on a contested
axis.

## Review dial

The adversarial triggers — `concurrency`, `authz`, `crypto`, `schema`,
`migration`, `delete`, `regulated`, `public-api`, `large-surface` — fire
independently: any one suffices, whatever the diff's size and whatever the
phase's `review_class`. `final-only` decides whether routine review runs; it
never switches the trigger check off. A fired trigger dispatches the adversarial
reviewer before the task completes.

You set each phase's `review_class` **once, at stage 04, from the plan's
classification**, and never move it afterwards except through a ratchet whose
trigger already exists — for the adversarial route, a CONFIRMED or unrefuted
PLAUSIBLE finding returned by that reviewer. A ratchet record you write from
your own reading of the diff is not a trigger. Never downward. The tracker
enforces the move: `(final-only, plan)` → `(required, ratchet)` once, with a
trigger from the closed list, and `adversarial-finding` or
`low-confidence-dependency` only when the tracker already held that fact before
the ratchet's transition. Lowering and withdrawing are refused, and so is
deleting an imported phase row to re-add it.

## Completeness critic items

The critic's classification is not yours to change. `SPEC-NOT-MET` is a finding
for the fix loop. `MISSING-FROM-SPEC` is frozen, and the output **is**:

1. A section appended to the run's `completeness-proposals.md`, headed with the
   **next unused** proposal number (`## CP-1`, `## CP-2`, … — never the literal
   `<n>`): Statement, Evidence (the critic's text), `Traces to: none`,
   `Status: Frozen`, classification verbatim.
2. That proposal ID listed in the terminal report.
3. Once every other item is finished — an open fix round completes first —
   `next_action: complete-with-proposals`. `derive_next_action` derives it from
   that file, and never while a fix round or other item is still open.

Nothing else: no task, phase, fix-round finding, quorum, backlog or handover
note, and no disposition — `deferred`, `out-of-scope`, `declined` and `closed`
are all reclassifications. The proposal is the user's to decide.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "Two agree at a strong rung — the strongest quorum available." | Three valid responses is a precondition. |
| "I record the degraded count (2 of 3) honestly." | An honestly recorded illegal finalisation is still illegal. |
| "Sealing at the deadline is arithmetic; the rule is written in advance." | A violation scheduled is the same violation. |
| "The re-dispatch completes the record; it is not a gate." | It is the gate. |
| "The other responses already settle the premise the brain raised." | You do not answer questions you are routing. |
| "Only evidence-gathering, no adoption." / "The tie shows the question is malformed." | Nothing is dispatched on a tied axis. It is `escalated`. |
| "The human decision stays in force, so work proceeds against it." | Blocked until a human answers. |
| "Escalation is for questions the repository cannot answer." / "Idle brains cost nothing." | An exhausted budget escalates regardless. It caps authority, not cost. |
| "I decline it, closed in this run; reviewers can reverse it." | Declining is a disposition. Record the proposal. |
| "It crosses a trust boundary, that *is* the trigger, and I wrote the ratchet record." | A self-authored trigger is no trigger. |
| "Three different answers means the question is underdetermined." | Only when they tie on rung. A strict gap adopts. |
| "The spec already answered this, so the quorum's adoption is void." | The check runs before dispatch. A returned quorum is judged by the adoption rules. |

## Red flags — stop and re-read the rule

- Acting on fewer than three valid responses, now or "if it has not returned by…".
- Writing "not a gate", "non-blocking" or "degraded count".
- Dispatching anything on an escalated or contradicted axis.
- Writing `unresolved`, `deferred` or "carry to handover" instead of `escalated`.
- Opening a quorum without comparing the budget counters to the ceilings.
- Changing `review_class` after stage 04, a ratchet record with no fired
  trigger, or a label over a critic's classification.
- Pushing, publishing, opening a pull request, or merging into `main`/`master`.
  Success is a clean committed feature branch and a report that leads with every
  decision the run made without asking.
