---
name: plan-from-spec
description: Turn a SPEC, PRD, or any stated goal into a high-level executable PLAN of outcome-shaped tasks, and regenerate that plan when execution reveals it is wrong. Use this skill whenever the user asks to plan, break down, decompose, sequence, or roadmap work from a spec/requirements document or a goal, and whenever an executor's replan gate fires because a task's postcondition failed, expected state does not exist, a planned task is impossible, or new information invalidates a later task. Runs in two modes, initial planning and replanning, and always produces the same PLAN.md format.
metadata:
  author: "Giuliano Lemes <giuice@gmail.com>"
---

# Plan From Spec

Produce a high-level plan that an executor can carry out, and keep that plan true as reality diverges from it.

This skill is domain-neutral. It plans code work, research, writing, operations, and physical-world tasks. Nothing here assumes a web page, a repository, or a programming language.

## What this skill owns

| Owns | Does not own |
|---|---|
| Task decomposition | Deciding what counts as success — the contract does |
| Task ordering and dependencies | Performing the work — the executor does |
| Postconditions that make a task checkable | Recording what happened — the ledger does |
| Regenerating the plan when it stops being true | Reporting to the user — `completion-report` does |

The single most important boundary: **replanning may change how the goal is reached; it may never redefine what counts as success.** See "Contract invariant" below.

## Working directory

All artifacts for one piece of work live in `spec-interview/<slug>/`, the same folder `spec-from-scratch` creates:

```
spec-interview/<slug>/
  SPEC.md      input   (optional — see below)
  PLAN.md      output  (this skill)
  LEDGER.md    input in replan mode  (written by execute-plan)
  REPORT.md    written by completion-report
```

### When there is no SPEC

A stated goal is enough. Derive the slug yourself — short kebab-case, from the goal (`cache-product-endpoint`, `move-office`) — create the folder, and:

- write the goal verbatim in the plan header as `Goal:`;
- set `Spec: none — the contract is this plan`;
- omit `Covers:` from every task.

With no SPEC, **the contract is the union of the `Done when` conditions — those the ledger already records as satisfied plus those in the current plan.** Downstream stages read it from `PLAN.md` and `LEDGER.md` instead of `SPEC.md`. That leaves the contract extendable by replanning, which is exactly the risk a SPEC removes — so say this out loud to the user once.

Never invent a SPEC. If the goal is too vague to produce checkable postconditions, stop: for product work, run `spec-from-scratch` first; for non-product work, ask the few questions needed to name at least one checkable outcome condition.

---

## Step 1 — Ground the plan in observation, never in assumption

**Before writing any task, inspect the actual current state.** A plan written from the goal alone is a guess.

Inspect whatever the domain makes observable: existing files and structure, current configuration, a running system's behavior, available tooling, data already present, prior work, the state of external services or people. Spend real effort here — this is the cheapest place in the whole workflow to be wrong.

The reasoning of task 1 **must** contain a concrete observation of the current state: what exists now, what is missing, and which of the goal's assumptions the observation confirms or contradicts.

If the observation contradicts the contract, stop and say so. Do not plan around a contradiction silently.

### Already-satisfied goals

If the observation shows the goal is already true, write a plan with **zero tasks** and hand straight to `completion-report`. Do not manufacture tasks to make the plan look substantial. The whole file is then:

```markdown
# PLAN: <slug>

Spec: ./SPEC.md   (or: none — the contract is this plan)
Goal: <one sentence>
Plan version: 1
Status: no-op
Already true because: <the observation that establishes it>
Evidence: <how you observed it>
```

`Status: no-op` appears only in this case. A plan with tasks omits the field.

## Step 2 — Choose task granularity

A task is a **meaningful unit of work with a single verifiable outcome**. It normally requires several low-level actions.

Cluster related actions that serve one sub-goal into one task. Prefer fewer, denser tasks.

```
TOO FINE                          RIGHT
- Open the config file            - Add Redis connection settings to the
- Add a redis section               application config, reading host and
- Save the file                     port from environment variables

- Search for papers               - Identify the three most-cited papers on
- Open each result                  retrieval-augmented generation published
- Note the citation counts          since 2023, with citation counts
```

```
TOO COARSE                        RIGHT
- Implement caching               - Add a cache abstraction with get/set/invalidate
                                  - Wire the product endpoint through the cache
                                  - Add invalidation on product update
```

Calibration rules:

- If a task cannot fail in an interesting way, it is too fine — merge it.
- If a task has more than one postcondition, it is too coarse — split it.
- A task must carry enough context to stand alone, because it may be handed to a separate agent or person.

## Step 3 — Be specific about WHAT, silent about HOW

State the intended outcome and its concrete parameters. Do not prescribe the mechanics.

```
VAGUE      Add the timeout setting.
SPECIFIC   Set the HTTP client request timeout to 30 seconds for all
           outbound calls to the payment provider.

HOW        Open PaymentClient.cs, find the HttpClient constructor, add
           a Timeout property.
WHAT       The payment client fails a request after 30 seconds instead
           of hanging.
```

Conditional tasks in plain language are allowed when the branch is genuinely unknown at plan time: *"If the existing migration tool supports rollback, use it; otherwise write the rollback script by hand."* Avoid nested or ambiguous conditions.

## Step 4 — Give every task a postcondition

This is the addition that makes the plan work outside of environments where state is observable for free.

Every task states **Done when** as an observable condition, and **Verify by** as the concrete way to check it.

```
Done when:  the product endpoint returns a cached response on the second
            identical request within the TTL window
Verify by:  run the integration test ProductCacheTests

Done when:  every interviewee has confirmed the scheduled slot in writing
Verify by:  each of the six invitations shows an accepted response
```

Rules:

- `Done when` describes **state**, never activity. Not "the cache code is written" — that is activity. "A repeated request is served from cache" is state.
- `Verify by` names something that produces evidence: a command, a test, a file check, an API response, a document, a direct observation.
- Prefer the most mechanical check available: an exit code, a passing test, a countable value outranks reading output and judging it. When only interpretive verification exists, name the artifact to inspect and the criterion to judge it by — "read the summary and confirm it names all three payers", not "check the summary looks right".
- When no automatic check exists, write `Verify by: user confirmation`. That is **valid evidence once the user actually confirms** — weaker than a machine check, and the report will label it `attested` rather than measured. A postcondition merely *awaiting* confirmation is not yet satisfied.
- A task with no possible postcondition is not a task. It is either a detail of another task or it does not belong in the plan.

Postconditions are what let the executor detect divergence. Without them, "replan when needed" is a subjective judgment the executor will not make.

---

## PLAN.md format

Write to `spec-interview/<slug>/PLAN.md`:

```markdown
# PLAN: <slug>

Spec: ./SPEC.md
Goal: <one sentence, restated from the spec or from the user's words verbatim>
Plan version: 1
Replanned because: <trigger — omit on version 1>

## T1 — <outcome-shaped title>
Reasoning: <why this task exists, why these actions group together, and — in T1 only —
the concrete observation of the current state that grounds this plan>
Task: <what must be accomplished, with concrete parameters>
Done when: <observable postcondition>
Verify by: <how to check it>
Covers: FR-001, AC-003
Depends on: —

## T2 — <outcome-shaped title>
Reasoning: ...
Task: ...
Done when: ...
Verify by: ...
Covers: FR-002
Depends on: T1
```

Field rules:

- **Task IDs are stable and never reused.** `T3` refers to the same unit of work across every plan version. A replan that keeps a task keeps its ID; a new task takes the next unused number. This is what lets the ledger join to the plan across replans.
- **Covers** maps to SPEC requirement and acceptance-criterion IDs. Omit entirely when there is no SPEC. When a SPEC exists, every acceptance criterion and every Must-priority requirement must be covered — see the quality gate.
- **Restates** (no-SPEC replans only) carries the prior `Done when` text verbatim when a task restates a pending condition more precisely. Omit otherwise.
- **Continues** (replan only) names the `partial`, `blocked`, or `failed` task whose remainder this task plans. One task ID. It is a field rather than prose in `Reasoning` because the executor counts continuation chains through it to enforce its lineage limit. Omitted on a reopening's first continuation, which carries `Reopens:` instead — see the replan rules.
- **Reopens** (reopening replans only) names the exhausted attempt the run resumes from, on the first continuation task after a `replan exhausted` exit. The historical join without the count: the executor's lineage limit follows `Continues:` alone, so `Reopens:` renews the attempt budget while keeping the episodes traceable.
- **Depends on** lists task IDs that must complete first. Use `—` when none. Order tasks so dependencies precede dependents.
- **Plan version** is a label for ledger entries, not an archive. Prior plan text is not kept — the plan file is the current strategy; version control preserves history when the folder happens to live in a repository.

---

## Mode: initial plan

Trigger: a contract or goal exists and `PLAN.md` does not.

1. Read the SPEC in full, or capture the user's goal verbatim.
2. Observe the current state (step 1 above).
3. Decompose into tasks (steps 2–4).
4. Run the plan quality gate.
5. Write `PLAN.md` at version 1.

## Mode: replan

Trigger: **the executor's replan gate fired.** Reaching the end of a task is a checkpoint for that gate, not by itself a reason to replan. A run in which no plan ever changes is a correct run.

One more trigger: a run that ended `replan exhausted` is being reopened because the user reports its blocker resolved. That report reaches this skill through the executor — the router never calls replan mode directly — and only after the executor has confirmed the resolution — observed against current state, or explicitly attested by the user. The resolution is then the trigger named in `Replanned because:`.

Inputs: the contract, the current `PLAN.md`, `LEDGER.md`, and the observed current state.

### Reflect before replanning

Start the reasoning of the first future task with an explicit reflection:

- What was actually done, according to the ledger?
- Did it succeed? **How do you know from the current observable state** — not from the executor's claim?
- What did execution discover that the previous plan could not have known?

### Then refine

1. Identify which remaining tasks are now possible, and which have become impossible.
2. Make remaining tasks specific using information now observable. This is the main job: a task that said "contact the site owner" becomes "email Alice Nguyen, the listed maintainer".
3. Remove tasks that are no longer needed.
4. Add tasks the current state revealed as necessary.
5. Fix errors and assumptions in the previous plan.
6. Adapt when an expected element, file, result, person, or capability was not found.

### Rules

- **Plan only future work.** Completed tasks leave the plan; the ledger holds them. Do not renumber survivors.
- **No attempted task survives.** Any task with a `partial`, `blocked`, or `failed` ledger entry is finished as an instruction: whatever remains of it becomes a **new** task with a **new** ID. Reusing the ID would make the executor re-run side effects that already happened — and because the executor never redispatches a task that has a ledger entry, a reused ID would simply never run again. The new task carries `Continues:` naming the prior task; its reasoning says what remains of it. **Exception — reopening.** When the trigger is a resolved blocker after `replan exhausted`, the continuation task omits `Continues:` and carries `Reopens:` naming the prior attempt instead: the `Continues:` chain is the executor's attempt counter, so a confirmed external change starts a new episode by breaking it, while `Reopens:` keeps the episodes joined in the record. Reasoning alone would not survive — attempted tasks leave the plan and the ledger does not copy reasoning.
- **Repoint dependencies.** Every surviving task whose `Depends on` names a finished-as-instruction task now points at its replacement — or drops the dependency if the part already done was all it needed. A `Depends on` left pointing at a `partial`, `blocked`, or `failed` entry can never be satisfied: the executor requires dependencies to be `done` or `no_op`, and that task will never be either.
- **Carry discovered facts forward into the plan text.** The plan is the working memory of the run. If execution learned that the top contributor is Alice, later tasks say "Alice", not "the top contributor". This is why the loop needs no separate memory mechanism. Only facts the ledger records as `[verified]` may be written into task text as fact; a `[reported, unconfirmed]` discovery either gets its own validation task or stays out of the plan — an unchecked claim written here becomes every later task's premise.
- Increment `Plan version` and fill `Replanned because` with the concrete trigger.
- If nothing material changed, say so and leave the plan untouched.

### Contract invariant

> Replanning changes the strategy. It never changes the definition of success.

If reaching the goal now requires relaxing, dropping, or reinterpreting an acceptance criterion, **stop**. Do not write a plan that quietly satisfies a weaker goal. Instead report to the user:

- which acceptance criterion cannot be met as written;
- what execution discovered that makes it unreachable;
- the options — change the contract, change the approach, or accept partial completion.

Amending the contract is the user's decision, not the planner's. A plan that silently redefines success is the failure mode this whole workflow exists to prevent.

**On a run with no SPEC**, the contract is the union of the `Done when` conditions accepted so far — those already satisfied in the ledger, plus those in the current plan. Replanning may **add** conditions and may **restate** a pending one more precisely — the restating task then carries `Restates: <the prior Done when text, verbatim>` so the reporter can join the old entry to the new. Adding strengthens the contract and needs no escalation. It may not weaken or drop one, and it may never touch a condition the ledger already records as satisfied. Dropping a pending condition is a contract change and takes the same escalation as above. The invariant is not suspended just because the contract lives in the plan file.

---

## Plan quality gate

Run before writing `PLAN.md`, in either mode:

```markdown
- Grounded in an actual observation of current state: Pass / Missing
- Every acceptance criterion covered by a completed ledger entry or a remaining task: Pass / Missing / N/A
- Every Must-priority requirement covered by a completed ledger entry or a remaining task: Pass / Missing / N/A
- Every task lists `Covers`, or a task that transitively depends on it does — no task sits outside every path to a requirement (SPEC runs only): Pass / Missing / N/A
- Every ID in `Covers` exists in the SPEC: Pass / Missing / N/A
- Every task has an observable Done when: Pass / Missing
- Every task has a Verify by: Pass / Missing
- No task describes HOW instead of WHAT: Pass / Missing
- Dependencies ordered correctly, no cycles: Pass / Missing
- No `Depends on` names a task with a `partial`, `blocked`, or `failed` ledger entry (replan only): Pass / Missing / N/A
- Task IDs stable against the previous version (replan only): Pass / Missing / N/A
- Every task planning the remainder of an attempted task carries `Continues:` naming it, except a reopening's first continuation, which carries `Reopens:` instead (replan only): Pass / Missing / N/A
- Success criteria unchanged from the contract (replan only): Pass / Missing / N/A

Verdict: Ready / Not ready
```

Coverage is evaluated against **the ledger plus the remaining plan**, never the remaining plan alone. A criterion satisfied by a completed task stays covered after that task leaves the plan.

`Not ready` means fix the plan, not ship it with a caveat.

---

## Anti-patterns

**Action lists.** A plan whose tasks are "open X", "edit Y", "run Z" is a trajectory, not a plan. The executor produces those; the planner does not.

**Unfalsifiable tasks.** "Improve error handling" has no postcondition, so nothing can detect its failure. Name the observable behavior instead.

**Planning from the goal alone.** Skipping observation produces a plan that is coherent and wrong. Most replans are caused by a planner that never looked.

**Renumbering on replan.** Every ledger entry points at a task ID. Renumber and those references now point at different work.

**Silent scope drift.** Quietly dropping a hard requirement during replan because it turned out to be difficult. Escalate instead.

**Padding.** A three-task goal gets a three-task plan. Do not manufacture tasks to make the plan look thorough. The reverse-coverage line in the quality gate exists to catch exactly this.
