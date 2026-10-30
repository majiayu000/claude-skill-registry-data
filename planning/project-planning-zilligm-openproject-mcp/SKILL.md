---
name: project-planning
description: Use when planning or structuring work in OpenProject rather than just recording it — setting up a new project, scoping an initiative, breaking an epic or feature down into phases, milestones, and tasks, building a work breakdown structure, sequencing work and defining dependencies, estimating effort, laying out a roadmap or release plan, restructuring a project whose hierarchy has gone wrong, or reviewing an existing plan before work starts. Applies equally to work projects and to personal, side, or hobby projects worked on in whatever time is available. Triggers on "plan a project", "scope this work", "break this down", "create a WBS", "set up phases and milestones", "what should the tasks be", "build a roadmap", "plan the sprints", "plan my side project", "organise this personal project", "review the plan", "is anything missing from the plan", "check these tasks before we start". For executing and reporting on work that is already structured, use the openproject skill instead.
---

# Planning work in OpenProject

Creating tickets is easy; creating a structure people can actually run a project from is
not. A plan is wrong in ways that only surface weeks later: a phase that cannot start
because nobody noticed it depends on an unstarted one, a milestone with no verifiable
exit condition, forty tasks that are each one line long. This skill is the judgment that
prevents that, and the exact call order that builds it.

The mechanics of the tools — arguments, safety guards, error meanings — belong to the
**openproject** skill. Read this one for *what* to build, that one for *how to drive it*.

## The process

Plan in five steps. Do not start creating until step 4.

1. **Frame** — establish objective, deliverables, constraints, who is doing the work, and
   when they actually work. Ask about what is missing; see *Framing questions* below.
2. **Choose a playbook** — phase-gate, agile, or formal WBS. The chooser is below.
3. **Decompose and sequence** — build the tree, then the dependencies, then the dates.
   Never the other way round: dates derived from a sequence hold, dates invented first do not.
4. **Confirm** — show the user the whole plan as text and get an explicit yes.
5. **Build and verify** — create it in the documented order, then read it back.

**Step 4 is not optional.** A sixty-item tree in the wrong shape is hours of someone
else's work to unpick, and `delete_work_package` takes children with it. Present the tree
indented, with types, dates, estimates and dependencies visible, and say what you assumed.
A user who says "just do it" has confirmed; proceed. A user who says "break that down" has
**not** — that is a request for a proposal. Show it, then build it.

## Framing questions

Ask only what you cannot infer, and ask it all at once rather than over five turns. The
answers that change the structure:

| Unknown | Why the plan depends on it |
|---|---|
| **The outcome**, stated as a condition that will be true when done | Without it there is no test for whether the breakdown is complete |
| **Deliverables** — the things that will exist | Phases are named after deliverables, not after activity |
| **How the result gets used day to day** — a terminal command, a report, an interactive app, an API — and **which questions users will bring to it** | The form decides the epics, the questions decide the features. Derive features from the questions, not from whatever data happens to be available. Both are usually left implicit until the structure is already wrong |
| **Who or what can reach what** — which machines, accounts, networks, devices, credentials | Access is a scheduling constraint like any other. Work that needs the one machine with the right access has to be found before it blocks everything |
| **Hard dates** — a launch, a contract, an event, someone else waiting | An *external* date means planning backwards from it. A date you set for yourself is a target, and worth far less pressure |
| **Who is doing the work**, and how much time they really have | Decides how much can run in parallel, and whether assignees are worth setting at all |
| **Cadence** — when the work actually happens: office hours, evenings, weekends, whenever there is time | Decides how small a task should be, and whether dates will help or just go stale |
| **Known unknowns** — what needs research before it can be estimated | Becomes a spike, not a guessed estimate |
| **Definition of done** — review, testing, deployment, sign-off if anyone is signing | These are real tasks and are the ones most often missed |
| **Method already in use** — does this project run sprints? gate reviews? nothing in particular? | Match the rhythm that already exists; do not impose a new one |

If the user cannot answer a structural question, plan the part you can and leave the rest
as a single placeholder work package named for the decision that is pending. A plan with
an honest gap beats a plan with an invented one.

## Choosing a playbook

| Signals | Playbook |
|---|---|
| Sequential stages, gates or sign-offs, a fixed end date, external stakeholders, non-software work | **Phase-gate** — phases as deliverable stages, milestones as gates |
| Continuous delivery, a backlog, sprints or a cadence, scope expected to change | **Agile** — epics, stories, sprint versions |
| Contractual or audited scope, a formal baseline, cost control, someone will ask "is this 100% of the work" | **Formal WBS** — decomposition to the 100% rule, WBS dictionary, critical path |
| A project of a few weeks to a few months, one person or a few, no ceremony demanded | **Phase-gate**, lightly — it is the safe default and maps to OpenProject's native types |

Mixing is normal and correct: phases with sprint versions inside them is the most common
real shape. Full playbooks with worked examples:
[reference/playbooks.md](reference/playbooks.md).

## Rules that hold in every playbook

**1. Decompose deliverables, not activities.** "Authentication service" is a deliverable;
"working on authentication" is not. A node whose name has no noun that could be handed to
someone is a node that will never be verifiably done.

**2. A task is one person, one or a few sittings, one clear finish.** Size it to the working
session whoever does it actually gets — two hours on a weeknight, a Saturday afternoon, a
full day — so that finishing in one go is normal. Much smaller and it costs more to track
than to do; much bigger and it hides structure, so split it, or if you cannot say how, it is
a spike whose output is the breakdown. See
[reference/decomposition.md](reference/decomposition.md).

**3. Leaves hold the work; parents hold the shape.** Estimates, assignees, and progress go
on leaf tasks. OpenProject rolls them up, and an estimate set on a parent competes with
what its children say. Never assign a phase to a person.

**4. A milestone is a verifiable event on one date, with no duration and no work of its
own.** "Scope signed off", "v1.0 in production", "security review passed". If you cannot
say who checks it and how, it is not a milestone.

**5. Hierarchy is composition; relations are time.** A parent is *made of* its children.
`precedes` / `follows` means *cannot start until*. `blocks` means *cannot finish until*.
Never use nesting to express order — a task is not a subtask of the task before it. See
[reference/dependencies.md](reference/dependencies.md).

**6. Sequence before you date — and date only what you can predict.** Get the dependency
graph right, find the longest path, then place dates. Dates assigned first quietly encode a
sequence nobody agreed to, and dates on work whose timing nobody controls quietly turn into
a wall of overdue items. Sequence is almost always worth recording; dates are not. See
[reference/estimating-and-scheduling.md](reference/estimating-and-scheduling.md).

**7. Plan the unglamorous work.** Review, testing, migration, documentation, deployment,
rollback, handover, the security of what ships (who can reach it, what it can read or
change), and the wait for someone else's approval. These are where real plans
overrun, and they are absent from almost every first draft. On a project with no reviewer
but its author, they do not disappear — they just have nobody else to catch them.

**Data handling belongs on that list, as a day-one task, whenever the project touches
anything private** — network exports, customer records, credentials, logs with addresses in
them. Decide up front where raw inputs live, how raw and sanitised files are named, and what
*enforces* the separation (a `.gitignore` pattern that matches the naming convention, not a
list of individual file names). Retrofitting this is how near-misses happen: each new file
name is a fresh hole, and you only find them one at a time.

**8. Three levels is usually enough.** Phase → task → subtask. A fourth level means the
phase is really a project, or the subtasks are a checklist that belongs in a description.

## Building it

Order matters, because OpenProject resolves names against what already exists.

```
1. get_operational_diagnostics()          # reachable? acting as whom? projects restricted?
2. create_project(name, description)      # empty project; the tree comes at step 6
3. get_work_package_options(project_id)   # which types exist HERE: Phase? Milestone? Epic?
4. create_version(...) per sprint/release # must exist before any plan names it
5. list_project_members(project_id)       # principal_id → assignee_id
6. create_work_package_tree(project_id, work_packages=[...])   # hierarchy, depth-first
7. create_work_package_relation(...)      # dependencies, one call each, after IDs exist
8. generate_project_progress_report(project_id)                # read the plan back
```

**Do not collapse steps 2 to 6 into one call.** The gap between creating the project and
creating its tree is where versions get created and the project's option lists get read.
Skip it and a plan naming `"Sprint 1"` fails on an unknown version, or a type you assumed
turns out not to exist in that project.

**Verify types before using them.** `Phase`, `Milestone`, `Epic`, and `Feature` are
OpenProject defaults but any instance can remove or rename them. Read step 3's `types`
(each with `is_milestone`) and fall back to `Task` for a missing type rather than failing
the whole tree. Only a type with `is_milestone` takes a single date.

**`WorkPackagePlan` carries less than `create_work_package`.** It has `subject`, `type`,
`description`, `start_date`, `due_date`, `assignee_id`, `priority`, `version`,
`estimated_hours`, `children` — and nothing else. Set `responsible_id`, `category`, and
custom fields in a follow-up `update_work_package`, or create those items individually.

**Relations go in the same call as the tree.** `create_work_package_tree(..., relations=[...])`
names each end by its subject and creates the edges after the items, so a sequenced plan is
one call rather than one call per edge. Subjects must be unique within the plan — two items
with the same subject cannot be linked, and the result says so rather than guessing. The
result reports `relations_created` and `relations_failed`, and relations are attempted even
when the tree stopped early, so a partial build still gets the edges it can have.
Use `create_work_package_relation` for edges to work that already existed, or discovered
later. Map subjects to IDs from `created`, then one
`create_work_package_relation(source, target, "precedes")` per edge. Expect the cross-phase
edges to be few — if you are writing twenty, the hierarchy is probably wrong.

**A partial failure keeps what it made.** `create_work_package_tree` stops at the first
error and returns `created` plus `failed_subject` and `error`. Fix the failing item and
create the remainder under the right parent; do not re-run the whole tree, or you will get
duplicates. Full recovery procedure and a worked build:
[reference/build-sequence.md](reference/build-sequence.md).

## Give the plan somewhere to live

A tree records structure but not reasoning, and the reasoning is what the next person to
look needs — often the same person, months later, with no memory of it. Create one work
package per project to hold it — `type="Phase"` is wrong, use a
plain task named "Project plan" — with description sections `## Objective`,
`## Scope` / `## Out of scope`, `## Approach`, `## Risks`, `## Decisions`. Keep it current
with `update_work_package(description_section_heading=...)`, which rewrites one section and
leaves the rest alone. Project documents are read-only through the API, so this work
package is the living document.

**If the repo already has an agent context file** — `CLAUDE.md`, `AGENTS.md`, a README that
sessions read — decide explicitly which one owns decisions, and make the other link to it
rather than repeat it. Two homes become four copies within a week, and the one nobody updated
is the one the next session reads. Current status belongs in the tracker only: docs link to
it, never restate it.

Put acceptance criteria in each task's own description as `## Done when` — a checklist of
conditions, not a restatement of the subject. This is the single highest-value thing to
write at plan time and the first thing to be skipped.

**Check the project's existing description style before adopting it.** A project that writes
`**Done when**` in bold rather than `## Done when` as a heading still works, but only if the
section-update tool can find those sections — otherwise every one-character change rewrites
the whole description and risks reformatting what someone else wrote. Try one section update
before you add twenty tasks in that style, and say so if it does not work.

Where work happens in gaps rather than continuously, one more habit pays for itself: when a
task is put down unfinished, write the next concrete step into its `## Status` section. The
cost of picking a task back up is re-deriving where you were, and that cost grows with the
length of the gap. A one-line "next: wire the handler to the new column" is worth more than
any amount of progress percentage.

**Notes cannot be edited, so keep them to facts that stay true**: what was done, what was
decided, where you stopped. "Commit abc123, not pushed yet" is false within the hour and
false in the log for ever. Anything that will change belongs in the description's `## Status`
section, which is rewritable.

## Replanning

Plans change, and a changed plan is a normal event, not a failure.

- **Scope added mid-flight**: new work goes under the phase it belongs to, and the
  milestone date moves or scope comes out. Say which; do not silently do neither.
- **A phase slips**: `precedes` relations already model the knock-on. Reschedule the
  blocking item, then check what follows it with `list_work_package_relations`.
- **Restructuring**: `update_work_package(parent_id=...)` re-parents rather than
  recreating, which keeps history, comments, and logged time. Prefer it to delete-and-recreate
  every time.
- **A phase turns out to be a project**: make it a subproject (`create_project(parent_id=...)`)
  instead of growing a fourth and fifth level.
- **The project goes quiet for a while**: this is normal, not a failure state, and a plan
  should survive it. On returning, read the plan work package before the tree — it holds the
  reasoning the tree does not. Then reschedule from today rather than patching old dates one
  at a time, and close or park what you no longer intend to do. A plan carrying dates from
  three months ago reports nothing but overdue, which is the same as reporting nothing.
- **An earlier phase delivered**: before starting the next one, re-read its tasks against
  what was actually built: names and concepts, real data sizes and timings, assumptions
  still open. Tasks written before the foundation existed describe a guess of it. Make
  this review the next phase's first task so it can't be skipped.
- **Something got renamed**: when a task changes a path, a command, a file or a concept,
  search the open work packages and the docs for the old name before closing it. A task that
  still says `python validate.py` after the entry point moved will fail for whoever picks it
  up, most likely on another machine where nobody can guess what was meant. Make "references
  updated" a standard `## Done when` item on any task that renames something.
- **Record why**: post a note on the milestone or plan work package. When a replan or
  review touches many items, pass `notify=False` on each change and let this one note be
  the notification. In six weeks nobody remembers whether a date moved because of scope or
  because of an estimate that was wrong, and that difference decides whether the next
  estimate can be trusted.

## Feedback

[reference/feedback.md](reference/feedback.md) is a log of what went wrong or right when
this skill and the OpenProject tools were used on real projects. **Before planning,** skim
its `open` entries: they are known pitfalls not yet fixed here, some with workarounds.
**After a planning or replanning session,** if something in this skill, a reference file
or the tools got in the way or was missing, add an entry in the format the file describes.
Entries are evidence for the next revision. They don't override this file until applied.

## Reference

| For | Read |
|---|---|
| The three playbooks in full, with worked trees | [reference/playbooks.md](reference/playbooks.md) |
| What makes a good task; sizing, naming, anti-patterns | [reference/decomposition.md](reference/decomposition.md) |
| Hierarchy vs. relations, relation types, critical path | [reference/dependencies.md](reference/dependencies.md) |
| Estimates, dates, milestones, versions, buffers, capacity | [reference/estimating-and-scheduling.md](reference/estimating-and-scheduling.md) |
| The exact calls, with a full worked build and failure recovery | [reference/build-sequence.md](reference/build-sequence.md) |
| Tool arguments, safety guards, error meanings | the **openproject** skill |
| Known pitfalls and field feedback; where to report new ones | [reference/feedback.md](reference/feedback.md) |
