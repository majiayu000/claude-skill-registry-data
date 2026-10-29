---
name: handoff
description: Turn a finished brainstorm or research thread into a handoff for a separate builder agent — pin the scope, verify assumptions with read-only subagents, grill the user only on what is still undecided, agree the item graph, then write a self-contained HANDOFF.md whose work items carry owned paths and acceptance commands so /run-handoff can build them in parallel. Use when the user asks for a handoff, or for a plan another agent will implement in a long-running session.
disable-model-invocation: true
argument-hint: "[scope]"
arguments: scope
---

# handoff

The reader is a builder agent that never saw this conversation. It runs `/run-handoff <dir>`, which owns the operating loop: progress tracking, subagent briefs, worktrees, merging, gates and stopping. This skill writes only what is specific to the project. Don't restate that loop in the handoff.

`scope` is free text naming what to hand off (`1-4`, `options 2 and 3`, `all but the migration`). Empty means what the conversation just settled on.

## Spine

1. **Pin the scope.** In one message: each selected item restated in full from the conversation, an explicit out-of-scope list, a kebab-case topic, and the directory. The directory is wherever the user's instructions keep long-lived agent notes, otherwise `.agents/handoffs/<topic>/` in the repo. If it already holds a `HANDOFF.md`, ask before overwriting. Wait for a go or a correction.
2. **Harvest decisions.** Every choice the conversation already made, with its why, becomes a locked decision. Don't reopen them.
3. **Research.** Fan out read-only subagents, one per area rather than per item. Each gets an objective, an output format and explicit boundaries ("X is another subagent's"). Verify what the plan leans on:
   - the files, modules and APIs each item will touch;
   - real interfaces and versions, from installed source or type definitions rather than READMEs;
   - the exact build, test and run commands, that they work today, and how long they take;
   - repo conventions, the constraints in its agent instructions, and the skills it expects agents to use.

   Findings too long to restate inline go to `research/<area>.md`, written by the subagent, which returns only the path.

4. **Grill the gaps.** Invoke `grill-me` with only the decisions research couldn't settle and that are the user's to make, including where tests attach (the highest seam that proves the outcome). If there are none, say so and skip it.
5. **Decompose** by the rules below.
6. **Confirm the graph.** Show every item as one line: ID, title, blocked by, `Owns`, outcome. Ask whether the granularity is right, whether each edge really blocks, and what to merge or split. Iterate until the user approves.
7. **Write `HANDOFF.md`** from the template below.
8. **Cold read.** Spawn a fresh subagent given only the directory path, with no conversation context. Ask it to:
   - list everything it couldn't act on without asking: undefined terms, references to the discussion, items without runnable acceptance, missing run commands;
   - map every in-scope line to the items that deliver it, and every review-focus risk to the item whose acceptance covers it, and report what maps to nothing;
   - flag items that could be in flight together but share `Owns`.

   Fix what it finds. Reopen the grill only for a real decision gap.

9. **Report** the path, the open questions, and the kickoff line: `/run-handoff <dir>`, plus `--auto` to run it unattended.

## Decomposition

- **Vertical slices.** Each item cuts a narrow but complete path through every layer it needs (schema, logic, interface, tests) and is verifiable on its own. Items split by layer only meet at the end, which is where parallel builders' hidden assumptions collide.
- **Wide refactors go expand–contract.** A mechanical change whose blast radius crosses the codebase can't keep `Owns` disjoint or land green as one slice. Expand (add the new form beside the old), migrate callers in batches each blocked by the expand, then contract (delete the old form) blocked by every batch.
- **Freeze contracts first.** Any interface two concurrently running items code against (schema, types, CLI flags, file format, API shape) is a contract, frozen at gate `G0` before work fans out. Items never change a contract; they propose changes.
- **Concurrency comes from the graph.** Items whose blockers are done and whose `Owns` are disjoint run at once; there are no lanes or phases to declare. Shared hotspots (lockfiles, registries, central config) belong to one item or to `G0`. A mostly linear graph is a fine answer; don't cut edges to look parallel.
- **Unknowns become spikes** (`S1`…): a question, a timebox, and the criteria for keeping or discarding the result. They block the items that depend on them.
- **No implementation steps.** A "how" that matters is a locked decision; an unknown "how" is a spike.
- **Size:** one subagent can finish and verify an item in one fresh context.
- **Acceptance is observable:** a command, its working directory and the expected result. For a behaviour change, a test that fails before and passes after. "Tests pass" alone is not acceptance. If no reliable check exists, the first item builds one: builders optimise for whatever the check rewards.
- **Review focus:** the three to five failure classes most likely to slip past happy-path acceptance (bad input, partial failure, concurrency, upgrade paths), each assigned to the item whose acceptance must cover it.

## HANDOFF.md

Self-contained: define each term where it first appears, restate findings instead of linking to them, never write "as discussed". Use repo-relative paths and exact commands with their working directory. Redact secrets, tokens and personal data; name where to find them instead. IDs are stable and never renumbered, because `/run-handoff` tracks status by ID. Status never goes in this file.

```markdown
# <Title>: handoff

## Mission

<One paragraph: what exists when this is done, and why it matters.>

## Scope

In: … Out: …

## Context

<Repo, base branch, how to build/test/run (exact commands, cwd, measured duration), conventions, terms.>
Skills: <skills the builder and its subagents should invoke, e.g. tdd, and when.>

## Locked decisions

Do not re-litigate. If evidence shows one is wrong, raise it; don't deviate.

- D1 <decision>. Why: <reason>.

## Contracts

- C1 <interface>: <shape, where it lives>. Frozen at G0.

## Work items

### A1 <title>

- Blocked by: G0, S1
- Owns: <paths only this item changes>
- Outcome: <1–3 sentences of behaviour>
- Acceptance: `cd <dir> && <cmd>` → <expected>
- Constraints: D1, C1
- Research: research/<area>.md (if needed)

### S1 <question> (spike, timebox <n>)

- Keep if … / discard if …

### G0 Contracts frozen

- Acceptance: C1… committed; <items> pass; reviewer signs off.

## Review focus

- <Failure class> → covered by <item ID>'s acceptance.

## Concurrency

Max items in flight: <n> (default 3; lower if tests contend for a cluster, ports, disk).

## Rules for this project

<Never/always beyond the generic loop: services not to call, files not to read or touch, time budgets.>

## Stop conditions

<Project-specific; the generic ones live in /run-handoff.>

## Gotchas

<Verified facts that will bite.>

## Open questions

<Not the builder's to decide; how to proceed meanwhile.>

## Amendments

<Owner appends dated entries here; they override everything above.>
```
