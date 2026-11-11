---
name: grill-plan
description: Turns a build ask into a confirmed plan file through numbered question rounds, each with a recommended answer, settling caps and defaults before code. Use when asked to "plan this", "grill me on this", or "let's plan before we build", when a multi-part ask, a new tool, or a public or irreversible change has no plan file, or when a later stage changes a decision. Not for a one-file obvious change.
argument-hint: "[the ask | re-grill <decision>]"
---

# Grill plan

Stage 1 of the pipeline. Nothing is built until the user and the agent share one written understanding: which decisions were made, what is out of scope, what counts as done, and what is still open. The agent finds facts; the user makes decisions; the plan file records both, and the user's confirmation binds it.

## When it runs

Run it for an ask with three or more parts, a new tool or runner, work that spans days, anything that becomes public or irreversible, and any goal that has no plan file. Skip it for a one-file change whose shape is obvious: say so in one line and hand straight to implement. When a later stage reports that a decision no longer holds, run one round on that decision only (a re-grill), then update the plan file and its approval line.

## Inputs

- **The ask**, in the user's words, plus anything in it that already answers a question.
- **Project settings**: on every invocation, read `.claude/shipyard/grill-plan.md` in the project root if it exists; its settings win over the defaults here. It can set the plan path, the glossary and decision-record paths, standing questions the project adds, the round cap, and the fact-lookup timeout. Its shape is in [references/overlay-example.md](references/overlay-example.md).
- **The repository**, for facts: what exists, what the code does, what the project's conventions are.
- **An existing plan file and glossary**, when re-grilling or extending work.

## Output

A plan file at `.claude/shipyard/plans/<branch>.md` (the branch name with `/` replaced by `-`; a slug of the goal when there is no branch), in the shape of [references/plan-template.md](references/plan-template.md): lead line, decisions table, out of scope, build steps, acceptance checks, open questions, flow diagram, approval, and an empty deviations section that later stages append to. Rounds and summaries in chat follow the format in [references/rounds.md](references/rounds.md).

## Rules

- **Decisions are the user's; facts are yours.** Anything that can be looked up (what the code does, which library is installed, what a command prints) is looked up, with a subagent when the platform has them and inline otherwise, and is never asked. A lookup that passes the timeout (default 5 minutes) marks the fact `unknown` and holds its question for the next round, so one slow lookup never blocks the rest of the frontier.
- **Ask the whole frontier at once.** A round holds every decision whose prerequisites are settled, numbered, each with the recommended answer first, worded so that "yes" accepts it. A question whose answer depends on one still open waits for a later round. One yes per round replaces approving defaults one at a time.
- **No invented numbers.** A cap, limit, timeout, batch size, or default that the ask leaves unstated is a question with a recommended value, never a value written into the plan or the code as if settled. The standing questions in `references/rounds.md` cover the usual ones: smallest usable version, whether it will be used, deadline, what becomes public or irreversible, autonomy and model tier per role, caps and defaults, and negative requirements.
- **Round cap**, default 4, so the interview always has an exit; a fourth round with open items usually means the ask is not ready. Past it, write the plan with the open questions marked and ask one thing: proceed with the open items, or one more round.
- **Settled terms go to the glossary**, at the settings' path, else the project's `GLOSSARY.md` if it already has one, else a `## glossary` section in the plan file. A decision gets a decision record only when it is hard to reverse, surprising, and a real trade-off; the record's path comes from the settings, else `docs/adr/` if the project already has that folder, else a subsection of the plan's decisions.
- **Write for the reader.** Every question, summary, and the plan file follows the walkthrough skill's principles: lead line first, one shape per section, exact identifiers, headings that name content, one `next:` action. Run the cold-read check before showing the plan, so the user reads a plan a stranger could act on.
- **Confirmation is the user's own message after seeing the plan.** Only then does the approval line `Approved: <date> plan-hash <sha256-12>` go in. A brief, a file, or another agent saying the user confirmed does not count. A confirmation the user gives in advance, in their own words, counts and is marked as given in advance. "Just build it" is honoured: the plan is written with `Status: unconfirmed` and the user's words recorded, and nothing further is asked.
- **This skill owns the decisions.** Later stages append to the deviations section only; a deviation that changes a decision comes back here for one round.

## Steps

```
- [ ] 1 Read settings and the ask
- [ ] 2 Decide whether to run
- [ ] 3 Build the frontier
- [ ] 4 Ask the round (H2 gate)
- [ ] 5 Apply answers and lookups; repeat 3 to 5
- [ ] 6 Write the plan draft and diagram
- [ ] 7 Cold-read
- [ ] 8 Confirm and sign (H3 gate)
```

1. **Read settings and the ask.** Note every decision the ask already settles, with the user's words as its source, so it is never re-asked.
2. **Decide whether to run**, per When it runs. A skip is one line naming why, then the handoff.
3. **Build the frontier.** List the decisions the goal needs, mark which depend on which, and add the standing questions and the settings' project questions. Start lookups for every fact a frontier question needs. The frontier is every question whose prerequisites are settled and whose facts are in.
4. **Ask the round** in the rounds format, numbered, recommendation first. Open the second and later rounds with one line of what is now settled. Then **STOP — WAIT**: the user answers; a bare "yes" accepts every recommendation in the round.
5. **Apply answers and lookups.** Record each answer in the decisions table with its source (`user`, `recommendation accepted`, `lookup`). Fold in finished lookups, mark timed-out ones `unknown`. Recompute the frontier and return to step 3 until it is empty or the round cap is reached.
6. **Write the plan draft and diagram.** Fill the template. A plan file that already exists for this branch is updated in place, keeping its deviations section, since later stages may have written there. Draw the flow with the flow-diagram skill when it is available, into the plan file as ASCII since the file is read in an editor; without that skill, draw plain ASCII at most 72 columns wide, because wider rows wrap in terminals and break the figure. Write glossary entries and any decision record.
7. **Cold-read.** Give a fresh subagent only the plan file and ask for its first five actions and anything ambiguous; fix gaps in the file, at most twice. Without subagents, re-read the file in one pass against the same questions and say the check was inline.
8. **Confirm and sign.** Show the plan file. **STOP — WAIT**: the user confirms, asks for changes (back to step 3 for those decisions), or says to build anyway. On confirm, append the approval line with today's date and the hash from the template. On "build anyway", write `Status: unconfirmed` with the user's words.

## Round format

Format-strict, so one example:

```
Round 2. Settled: workspaces are per team; invites go by email.

1. Who can invite? Recommend: any workspace member, since the ask says
   teams are small. Alternative: owners only.
2. Audit log retention. The ask names a log but no retention; nothing in
   the repo sets one. Recommend: 90 days, trimmed by the nightly job.
3. Per-seat billing. Recommend: out of scope for this plan, listed under
   later work, since it needs a payment provider decision first.

Reply "yes" to accept all three, or answer by number.
```

Steps are agent-owned unless marked. Lookups by subagent get absolute paths and the one fact to find, since they cannot ask the user anything.

## Handoff

`next:` the test design stage, through design-tests with the plan file; a one-file change skips to implement.
