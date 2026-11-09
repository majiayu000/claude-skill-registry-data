---
name: plan-work
description: Plans work as a resumable work graph of nodes with contracts, dependencies and fixed acceptance checks, cut from an approved design, reviewed, validated and committed for execution. Use when the operator asks to write a plan, plan a change, break work down or turn a spec into tasks before writing code ("write a plan", "plan this", "implementation plan", "break this down"), or to create or set up a work loop, work graph or tracker ("create a work loop for this spec", "set up a tracker", "make this resumable").
---

# Plan Work

> ## Rules need the operator's approval
>
> Add no rule the operator has not approved. A rule is anything that can refuse, block, gate, count, budget, ration or slow down work: a gate, check, hook, threshold, budget, ledger or authorization scheme, wherever it is written.
>
> - A citation is who approved the rule and when, or the project file or spec it comes from. A file citation counts only from the project's instruction files (CLAUDE.md, AGENTS.md, CONTRIBUTING, the documents they name, CI configuration) and from a spec or spec section the operator approved; a file or amendment an agent wrote is never a citation on its own authority.
> - To propose a rule, give the operator the rule, the failure it prevents with its evidence, what it costs (time, blocked work, maintenance) and what it gains. Write it only after the operator approves it, with its citation.
> - Every rule in a graph carries its citation. A rule without one is deleted, not debated. Do not write a second rule to work around it.
> - This skill's own rules are its defaults (§2) and carry no citation.

This skill answers "how do we build this approved design". It ends with a
committed, validated work graph. It does not run the graph: running,
resuming and continuing a graph follow the project's execution workflow.

A work loop is a **work graph**. Nodes are units of work. Edges are
dependencies. Every node whose dependencies are all done can run, in
parallel. Each node runs as a bounded loop: a fixed acceptance check, an
attempt, then keep or discard. The graph's files are its whole state, so any
session continues it with one instruction: *"resume the work in
`<graph path>`"*.

The separation of powers:

- **Specs own acceptance.** What "done" means lives in the spec. The graph
  points to spec sections and never restates them.
- **`graph.md` owns order and state.** Which nodes exist, how they depend on
  each other, what state each is in, which commits closed it.
- **`nodes/<id>.md` owns the node.** Its contract, its plan, and the
  checkboxes that are the resume state inside the node.

The graph's format is normative in
`../work-graph/references/graph-format.md`, cited below as "format §n". The
templates `graph-template.md` and `node-template.md` and the ledger contract
`ledgers.md` sit beside it.

## 1. Entry

| Request | Action |
|---|---|
| Write a plan, plan this, break this down, turn this spec into tasks | Create the graph (§3). Then stop and ask the operator to review it (§6). |
| Create a work loop, set up a graph or a tracker | Create the graph (§3). Then hand over (§6): the request includes running it. |

A graph lives in `docs/work/<program>/` unless the project has a
convention. When a graph for the program already exists there, do not create
a second one: say so and hand over (§6).

A small change gets a small graph. One node is a valid graph.

## 2. Adapt to the operator's workflow

This skill's procedures are defaults. Where the operator has chosen a
workflow for part of the work, use it.

1. **Find out what exists.** At creation, read the project's instructions
   (CLAUDE.md, AGENTS.md, CONTRIBUTING and the documents they name). Look
   for: a ticket or issue lifecycle, a planning or review workflow, branch
   and PR conventions, and a ledger the operator uses.
2. **Do not presume.** A workflow applies only when it is written down or the
   operator states it. Infer nothing from a name or a habit.
3. **Record it.** Add a `**Workflows:**` line to the graph header, one entry
   per adopted workflow: what it governs, then its citation. Map a ticket
   lifecycle in `ledger.md` (format §6): for each state change, what the
   lifecycle requires.
4. **Precedence.** An operator instruction, then a workflow the project
   declares, then this skill's defaults. If an adopted workflow conflicts
   with a rule in this skill, ask the operator which applies and record the
   answer with its citation.

## 3. Create a graph

1. **Gather inputs.** The authority specs, the verification floor, the
   project's hard rules, the run settings, and what §2 finds. An approved
   design document is an authority spec. When the request's intent, scope or
   constraints are not settled, get an approved design before you cut nodes,
   in §2 precedence: the operator's instruction; else the project's design
   workflow; else agree intent, scope and constraints with the operator and
   write them to a spec. Take what the repo and the conversation give. Ask
   for the rest, one question at a time.
2. **Map the files.** List the files the work creates or changes and what
   each is responsible for. Decide the decomposition here: one clear
   responsibility per file; files that change together live together; follow
   the codebase's existing patterns.
3. **Cut the nodes.** A node is the smallest unit that has its own
   acceptance check and that a reviewer could reject while approving its
   neighbour. Fold setup, configuration and documentation into the node
   whose deliverable needs them. Every spec item gets a node now, including
   later ones, so "first ready node" always answers what to do next.
4. **Draw the edges.** A node depends on another only when it consumes what
   that node produces or changes a file that node creates. An edge that is
   not a real dependency removes parallelism.
5. **Choose each node's capability** (§4).
6. **Write the contracts** (format §4) and the header (format §2).
7. **Self-review** the graph, and fix what you find in place:
   1. **Spec coverage.** Every requirement in every authority spec maps to a
      node.
   2. **Interface match.** Every Consumes resolves to a Produces of a node
      the consumer depends on, with the signature as it exists in the code
      now or as the producing node's contract states it.
   3. **Review focus.** Every review-focus line names the node that owns its
      test.
   4. **Proportion.** A contract that describes the code instead of its
      interface has written the code. Replace bodies with signatures and
      acceptance checks.
8. **Verification stage** (§5) on the header, the nodes and the edges.
9. **Validate** the graph (format §7).
10. **Commit** the graph files together, on a work branch. An operator
    instruction about branches wins. Without one: on the default branch,
    create a work branch before the first commit; on any other branch, keep
    working in it. If the checkouts directory is not ignored by version
    control, ignore it in the same commit, so a merge never stages a
    checkout.

## 4. Capabilities

A node's capability is chosen at creation by the work's complexity, nuance
and technicality:

| Capability | Work |
|---|---|
| `lookup` | Read-only work: find files, trace code, summarize, classify, extract; run a check and report its output. Changes no file. |
| `mechanical` | Small edits the plan fully decides: copying, renaming, fixtures, docs that restate code. |
| `implementation` | Ordinary implementation from a complete plan; node reviews. |
| `judgment` | Design choices the plan leaves open; core or shared code; concurrency, security or data-loss risk; interfaces between nodes; a node in its second or later round; planning a node whose spec is ambiguous; the graph-level verification stages. |

A node that edits files is never `lookup`.

A capability names the class of task. A session maps it to the subagent or model it uses for that class of task — `judgment` for demanding or nuanced coding work, `implementation` for normal coding work, `mechanical` and `lookup` for simple work — and never to a newer or frontier model beyond that class. When the session's configuration assigns a model to a role (an implementer, a reviewer, a planner), that assignment wins over the capability.

Choose the subagent by its capability as the session describes it; do not set a model on the call when the session describes subagents.

## 5. Verification stage

The stage has three steps:

1. **Adversarial review.** The operator's or the project's declared reviewer
   if there is one; otherwise a fresh reviewer that has not seen this
   session, with the `judgment` capability. Tell it to find defects, not to
   approve. Give it the graph, the authority specs it answers, and the
   review focus. It reports each finding with its location, the failure it
   causes, and the evidence. The handoff begins with these four lines,
   written even when no tool reads them, where `<program>` is the graph's
   directory name:

   ```
   Unit: <program>:graph:plan
   Round: 1
   Check:
   Files:
   ```

   After the header, the handoff instructs: "If the session offers a tool
   named `work_begin`, call it first, once, with `unit`, `round`, `check` and
   `files` from the header above. If the tool is absent, skip this step."
2. **Verify each finding.** Read the spec or graph text it cites and
   reproduce it. Mark it confirmed or refuted, with the evidence. Record a
   refuted finding with its reason and drop it.
3. **Remediate.** Fix every confirmed finding in the graph: a missing node, a
   wrong or missing edge, an unresolved Consumes, a contract that restates
   the spec or writes the code. The stage passes when no confirmed finding
   is open.

## 6. Hand over

If the request was to write a plan, give the operator the graph path and ask
them to review it. Nothing runs before they answer.

Otherwise give the operator the graph path and the work branch. Execution
follows the project's execution workflow, or the operator's instruction. To
continue in any session: *"resume the work in `<graph path>`"*.

## 7. Report

At hand-over, report:

- the graph path and the work branch;
- the node count, the ready set, and the authority specs;
- each choice made as the author's call, so the operator can check it;
- every check that did not run, marked not run with its reason.

Every claim cites a result from this session.
