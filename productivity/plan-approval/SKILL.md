---
name: plan-approval
description: Enforces explicit user approval at the CharlieBot master-to-user
  boundary. Use only when the CharlieBot master is producing an understanding page,
  presenting a plan, receiving plan feedback, or preparing to delegate implementation.
user-invocable: false
---

## Scope

- This skill governs only the CharlieBot master-to-user approval boundary; a
  delegated task is already past that boundary.
- Plan approval and runtime delegation authorization are separate boundaries. The
  approval interaction approves the settled plan terms; the runtime gate judges each
  later `/delegate` or `/improve` request.
- A delegated worker, reviewer, or improve-loop worker does not present another plan;
  it follows its delegated task contract.
- A delegated agent still stops and reports a blocker, contract conflict, or required
  scope expansion.
- A child whose approver is its parent node sends its divergences, when its page waits, and its plan links
  to its parent (Between Agents, `prompts/task_manager.md`).
  Its Waiting on you items stay in its own session, so the user answers them there.

## The principle

Action Boundaries in `prompts/master.md` and the host's resident memory entries in `$CHARLIEBOT_HOME/memory` set the
approval boundary of each step.
The user takes off each high-consequence step before it runs.
The agent tree carries out each reversible step and design choice directly, and states what changed and how to undo
it in the session reply or report.
The line's approver answers the reading on each understanding page that waits (Understanding section)
before work builds on it.
The approver is the user, or the parent node for a child under an e2e handover (`prompts/master.md`, `prompts/task_manager.md`).
The user also gives each explicit user approval that a rule requires, and reviews the delivered product.

**approval object = sections 1 and 3 + 4.1 Schema + resolved Trade-offs + entries
promoted from Other Details.** Plan approval covers these exact terms. The `BLOCK KIT` comment
in `prompts/plan_template.html` is the canonical grammar for the plan surface; do
not restate it here.

## Understanding

An understanding page lists the divergences of a request that admits several readings, and every request that changes
what a CharlieBot web page shows gets one (the trigger and its exemptions live in the master prompt; improve rounds
follow their direction file).

- The page is `artifacts/understanding_<slug>_v<n>.html`, reusing the head and style of
  `prompts/plan_template.html`. Five blocks: goal in one sentence carrying the why one level up; the
  deliverable through one concrete worked example and one figure, which for a request that changes what a CharlieBot
  web page shows is a demo of the changed page beside today's page, as a static picture or a clickable HTML page, with
  real content at each window size that `charliebot land --help` lists;
  acceptance criteria, each a trigger condition and an observable result in the page's natural language; non-goals; numbered
  divergences rendered as `div.fork` blocks, each carrying its options and their consequences outside folds
  and the fork grammar's folded explainer (block kit section 5, `prompts/plan_template.html`). Add the Linear block
  when the next bullet applies.
- Include the Linear block only when the repo is Linear-tracked on the memory entry
  `charliebot/workspace-repos` (that whitelist decides which repos are tracked) or a ticket already exists for the
  work. When the marker list is absent, write one line saying the whitelist is not configured instead. Use the
  `linear` skill to list candidates or prepare a ready-to-file
  draft. For a root session, the user decides which and the `linear` skill's confirmation rule applies.
  For a sub session, follow the master prompt's External System Writes rule. Fill the draft from the Linear defaults
  in memory.
  After the ticket exists, carry its identifier as a header meta chip on the understanding page and the plan that
  follows.
- Don't guess: any point the request leaves unstated where different readings lead to
  different designs must appear as a numbered divergence; never silently pick a reading.
- Map each outcome that the request names to a deliverable or a divergence.
  State the share of the problem that the deliverable covers.
- No how: an understanding contains no implementation mechanisms or technology choices;
  design content belongs to the subsequent plan.
- Facts before design: when the fix follows from why something happened, settle the
  root cause before drafting and state the case for it in one block between goal and
  deliverable, each claim carrying its evidence anchor.
- Share the page with the line's approver.
  The approver then corrects a misread request before it costs a build.
- An understanding page waits for its approver only when the estimated work exceeds about one worker-day
  (8 hours of worker time) or its result reaches other people (the reading threshold).
  This applies to root lines and child lines alike.
- A page whose approver is the user waits only while no e2e handover covers its reading (`prompts/master.md`).
- Below the reading threshold, the line proceeds on the recommended reading, and its delivery lists each divergence
  with the reply that selects the other reading.
- For a departure from the user's stated method, follow the Design section of `prompts/manager_workflows.md`.
- Before drafting, read the current system behind each option and acceptance criterion: the code and config it touches,
  and the earlier user decisions of the line.
  Check the proposal premises in `skills/file-server/source_check_spec.md` against that evidence.
  Use this read to judge whether each option and criterion can stand.
- While the page waits, continue read-only research for the plan.
- When the approver is the user and the page waits, list the page as one Waiting on you item.
- When the approver is the parent node and the page waits, send the page's divergences to the parent (Scope section).
  The parent then answers them from the reading that the user approved for the parent's line.
- The approver answers the divergences on the page.
  An unmentioned divergence keeps its recommendation.
- After the approver's reply on the page, in any wording, continue the line on the answered reading.
  One reply then releases the line, with no special approval word.
- The plan registry, the plan verify round, and plan approval start with the plan
  that follows the page.
- External system writes follow the master prompt's External System Writes rule.
- Before sharing, the page passes the mechanical assertions with
  `--genre understanding`, and it takes the Source Check of the file-server skill. Its cold read runs after sharing,
  with the originating request as the trigger, per the Cold-Read Gate of the file-server skill.
- The plan carries the understanding page's file path as a header meta chip;
  section 1 states the goal in its own words.
- Page layers follow the canonical first-draft contract in `prompts/master.md` under
  "Explaining to the user" → "Length"; each divergence keeps its question, options, and consequences visible, with
  its full rationale in the folded explainer.

## Plan

- Research the codebase first; present the plan as a decision surface following the
  template block kit, with numbered Trade-offs for the choices the user must judge.
- Contract text (rule sentences the plan lands verbatim in prompt docs, skills, or task
  specs) is drafted to the standing-reality form before `charliebot plan present`, and each
  block passes the three prompt-admission checks in `prompts/master.md` ("Text a model reads").
- Render the artifact per the USAGE note atop the BLOCK KIT comment in `prompts/plan_template.html`.
- Run the Cold-Read Gate of the file-server skill with `--genre plan`.
- Register before presenting via `charliebot plan present` (verbs per `charliebot plan --help`). The artifact's status chip is a presentation-time snapshot; the plan registry is the live truth. Record the code baseline when the plan pins one.
- An improve-loop plan follows this same contract; its approval object covers
  repo, goal, iterations, work branch, and merge-back — loop parameters with reasonable
  alternatives (iteration count, merge-back) make natural Trade-offs.
- Draft the plan to the layering contract in `prompts/master.md` under "Explaining to the user" → "Length"; keep the
  decision, necessary scope, and acceptance visible.
- Put operational history in `$CHARLIEBOT_HOME/LESSONS.md`; put supporting detail behind links or folds.
- A chat reply about a plan answers the question in at most five bullets and gives the page link.
  Detail stays on the page.

## Feedback

- Replies that touch the plan are feedback, not approval: Trade-off resolutions by
  number, added constraints, questions, changed terms.
  Fold each into the plan, and register the revision with `charliebot plan amend`.
  Continue the line after following the revision rule in Verify.
  This lets that rule determine when the revision ends.
  A revision registers with `charliebot plan amend`, which requires `--note`: the one
  line saying why this version differs from its predecessor. The note rides on the version record; the body stays the complete
  current design and carries no revision marks, and the reader gets the differences
  from `charliebot plan diff`.
- A style finding on one passage stands for its pattern: sweep the whole artifact for that
  pattern and fold every fix into the same revision.
- When the user names a text change for review, or a change touches the user's schema, show the original text
  beside its diff. In either case, write every command out in full.
- Only a user reply changes the goal. Section 1 of each version keeps the words of its lineage's most recent
  registered version; `plan amend` refuses a candidate whose section 1 differs from those words.
- A lineage first registered before the `plan amend` section 1 check took effect keeps the section 1 and non-goals
  paragraph it landed with; verify does not report them against its first version.
- A user reply that changes section 1 starts a new lineage. The new lineage's source names the replaced lineage's
  first version; verify checks the new first version against it. A lineage keeps its first version's form: later
  versions retain `p.non-goals` when it exists in the first version, and add none when it does not.
- When the user asks to control an Other Details entry, promote it; it joins the
  approval object. At approval, each unmentioned Trade-off that the approval covers takes its
  recommendation. Each decision that only the user makes then stays with the user.

## Approval

- Carry a line's work to delivery on its reading, and pause at high-consequence steps that wait for a take off.
  The reading is the answered understanding page, or the recommended reading when the task starts directly.
- For a reversible design choice, take the recommended option and name each alternative in the report.
- A user message in a running line is feedback.
- A request to stop, in any wording or language, or a cancel stops the line.
- The parent node approves a child line's plan. A root line approves its own plan.
- The parent's approval covers the plan terms other than decisions that only the user makes.
- When a plan revision or a fix round changes a look whose demo the user has seen on the understanding page, the parent
  approves it with a new demo, judging it against the demo the user saw and the user's words that the change answers;
  the user's notice shows both demos and waits for nothing.
- A fix round that answers a user's complaint about a look quotes the user's words.
  When a fix round or a plan revision changes a look the user has not seen as a demo, the round shows the user the new
  demo and waits for the user's reply before it lands.
- Each other decision that only the user makes waits for the user's answer in the child's session.
- Before each high-consequence step, ask the user for a take off that names the step.
- A pre take off names lines and steps ahead of time. It holds until those lines deliver.
- Before a take off, state the goal, blast radius, and undo plan.
- For a deletion, list each path and its size. Send each rule or code change that other nodes follow to their managers.
- Recheck every cited number and attach its result so the user can approve a step that already works.
- Give the user a diagram or worked example and list the alternatives with their consequences in one read.
- When work under a Linear ticket lands, draft one English comment for that ticket.
  The comment states the landed design, the resolved choices and the commit.
  A root session asks for its take off in the completion report. A sub session follows the master prompt's External
  System Writes rule. Delegation then waits for no ticket write.
- Post one comment per plan lineage or direct change. Work without a ticket posts nothing;
  the plan stage never creates a ticket. Linear then records the design that landed.

## Verify

- Draft and assert the plan, register it with `charliebot plan present`, complete one Improve round, then verify and
  cold-read it in the same turn. Finish the revision under the rules below, then approve it with
  `charliebot plan approve` and send the user its link.
- Verify is a read-only repo-less delegation on a registered plan. It checks fidelity, scope (the ruler in
  prompts/verify.md), and adequacy (whether an accurate, implemented design entails the outcome section 1 claims).
- A verify task's Source Files section names the lineage's first version and, when a new lineage replaces an old
  one, the replaced lineage's first version. The delegate rejects a missing or empty Source Files section; verify
  checks whether the listed file is the right source.
- Requester Words names the originating request and each session whose user replies extend the ruler, by session id
  and user-event kind. The manager chooses these sessions; the worker reads all user replies only from those named
  sessions. Neither the rule nor the code proves that the manager's list is complete.
- Verify also checks each wait, test and user question against the requirement it protects
  (prompts/manager_workflows.md, Design section), and checks each rule change against the three prompt-admission
  checks in `prompts/master.md` ("Text a model reads"). A step that names no requirement, or a rule change that
  fails a check, is a finding.
- The initial plan is revision one; versions between triggers share a revision. User feedback or a design change outside
  a findings fold starts a new revision; keep verify and cold-read folds in the current revision.
- Run verify round 1 on each revision, as full for a lineage's first revision. For a later revision declare delta or
  full, and declare full when the structure changes; a delta spec quotes its terms from `charliebot plan diff`.
  Verify an undeclared scope as full.
- Run at most two verify rounds on a revision of a plan for the user: round 1 as declared, then round 2 as delta over
  the round-1 fold only, quoting those changes from `charliebot plan diff`. A cold read started with verify counts in
  that round. When round 1 findings change nothing, finalize after round 1. When the round 1 revision only applies
  the specific items that round 1 verify and the cold read named, keeps the plan's structure, and adds no causal
  claim and no derived number, finalize after that revision and run no round 2. Otherwise run round 2, fold its
  findings, and finalize, with no third round.
- Every round measures with the same yardstick: the spec's Goal quotes the registered version's section 1 by path,
  and the spec's Requester Words names the sessions whose later replies extend the yardstick.
- Adequacy and scope findings are advisory. gap-design: says the mechanism looks short of the goal; weigh it and
  revise the design if it holds. gap-goal: says the goal itself may be misread; put that question to the user.
- A revision answers findings by correcting the plan against the goal it was registered with. Section 1 keeps the
  words of its lineage's most recent registered version; `plan amend` refuses a change to them. The non-goals
  paragraph changes only with a user reply. Report the adequacy findings when you send the user the plan link.

## Runtime delegation authorization

The runtime gate admits a delegation when the calling node is an open manager and every
ancestor on its task chain is open.
Its definitions live in `rust/crates/runtime/store/src/task_tree.rs` (`check_task_authorization` and `runtime_gate`).

## Execution

- Classify each step by Action Boundaries in `prompts/master.md` and the host's resident memory entries before it runs.
- When established practice answers a choice, follow that practice and carry the choice out as a step of the work.
  Established practice is the current production state or an earlier change of the same kind.
- When a step departs from established practice, name that practice in the step's Waiting on you item or in the
  session reply or report.
- When another node's message asks you to put a choice to the user, check the choice against established practice first.
  When the practice answers the choice, reply to that node with the practice.
- When a high-consequence step waits for a take off, list it as one Waiting on you item, and continue independent
  work in the same turn.
- Carry out reversible steps and design choices directly, and state how to undo each external or repository change
  in the session reply or report.
- List each action that only the user can perform (a browser login, an approval in another system, or information
  that only the user holds) as one Waiting on you item.
- Hold work that builds on a waiting understanding page until the approver answers the page.
- When reality forces a change that leaves the approval object intact, make it, log it as a deviation, and keep going.
- Between plan approval and the report, return to the user only at a checkpoint the plan assigns to the user, at an
  unapproved high-consequence step, or at a blocking failure.

## Report

- At completion or at a blocking failure, account for every approval-object term as delivered or deviated.
  Write each deviation as a retroactive Trade-off (approved term, what landed, and one-line reason), accepted by
  default or reverted on a new delegation when requested.
- For each reading below the reading threshold and each design choice made on a recommendation, name the alternative and the reply that switches to it.
- State how to undo each delivered change.
