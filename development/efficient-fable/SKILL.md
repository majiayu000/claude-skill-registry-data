---
name: efficient-fable
description: >
  Use when running an expensive frontier model on codebase-heavy or
  token-heavy work and the user wants that model to orchestrate,
  architect, synthesize, and final-judge while cheaper helper agents
  do bounded heavy lifting (large repo scans, long log reduction,
  narrow code patches, browser/test verification, etc.). Trigger on
  requests like "delegate this efficiently", "save tokens on this",
  "use cheap subagents for the heavy parts", or any task where the
  expensive model's judgment matters but its throughput does not.
  Treat subagent reports as leads, not facts — always vet before
  shipping. Do NOT trigger for trivial single-step work, for
  high-stakes single-source-of-truth tasks (medical, legal, financial
  advice), or when no cheap subagents are available.
---

# Efficient Fable (retweaked)

Use a high-cost frontier model as the **orchestrator, architect,
synthesizer, and final judge**. Use cheaper subagents for the
**bounded heavy lifting** that does not require the orchestrator's
full judgment. The orchestrator retains truth-judgment; the
subagents retain signal-gathering.

> This is the retweaked version adapted for the
> [skill-x](https://github.com/<your-org>/skill-x) collection. The
> original lives at
> [BuilderIO/skills](https://github.com/BuilderIO/skills/tree/main/skills/efficient-fable);
> this version generalizes the orchestrator role beyond Claude
> Fable, adds an explicit when-NOT-to-use section, and cross-references
> the other skills in this collection.

## When this skill shines

Reserve the orchestrator for:

- **Decomposing ambiguous work into clean parallel slices.**
- **Architecture, product, and safety tradeoffs** that need full judgment.
- **Reading conflicting subagent reports** and deciding what matters.
- **Integrating partial implementations** into one coherent plan.
- **Final review, risk assessment, and user-facing synthesis.**

## When NOT to use this skill

Skip the delegation pattern if any of these is true:

- The work cannot be sliced into independent chunks (one tightly
  coupled piece of logic).
- No cheap subagents are available (you ARE the orchestrator and
  the only worker).
- The task is high-stakes single-source-of-truth (medical, legal,
  financial advice) — keep all reasoning with the orchestrator.
- The validation requires reading the entire output carefully (a
  30-page legal memo, a 100k-line refactor diff).
- The task is trivial — overhead exceeds value.

For the above, run in single-agent mode.

## The 5-step delegation pattern

1. **Name the expensive-token risk.** Large repo search, long logs,
   broad docs, repetitive edits — anything where naive execution
   would burn orchestrator tokens.
2. **Split independent work into subagents BEFORE reading everything
   yourself.** Parallel slices for independent work; keep blocking
   or highly coupled work local.
3. **Use cheap subagents** for: research scans, inventory, search
   summaries, narrow bug hunts, browser/testing passes, test output
   reduction, bounded code edits.
4. **Ask subagents for concise evidence.** Files, line references,
   commands run, diffs, failures, screenshots, uncertainties, stop
   conditions they hit. See handoff packet format (§below).
5. **Spend orchestrator tokens on the decision layer.** Compare
   results, resolve conflicts, choose the implementation path, review
   the final patch.

**Parallelize only independent actions.** Do not run actions in
parallel when one depends on the result, identifier, decision, or
side effect of another.

## The vetting protocol (CRITICAL)

**Treat subagent reports as leads, not facts.**

Before using a high-impact finding, opening a PR, or telling the
user the work is done, the orchestrator should:

1. **Reopen the important cited files** — confirm the subagent looked
   at the right thing.
2. **Confirm the relevant line refs or failures** — line numbers and
   error messages must match the actual state.
3. **Review the final diff against the task** — does the change
   actually solve the problem, not just something adjacent?
4. **Test the change if material** — run the verification, don't
   trust the subagent's "it worked" report.
5. **Look for silent assumptions** — subagents often invent defaults
   that the orchestrator wouldn't.

**Let lighter agents gather signal; keep truth-judgment with the
orchestrator.** This is the line that, if dropped, makes delegation
unsafe.

## Handoff packet format

Write delegated prompts as if the subagent has no useful chat context.
Include only the context it needs:

- **The repo path and exact objective.** What does "done" look like?
- **The files, packages, or surfaces in scope and anything
  explicitly out of scope.** Boundaries reduce drift.
- **The evidence format to return.** Files, line refs, commands,
  diffs, failures, screenshots, uncertainty.
- **The verification commands or browser flows to run**, plus what
  success should look like when knowable.
- **Stop conditions.** If the code does not match the prompt, a
  command fails after a reasonable retry, or the task needs
  out-of-scope files, **stop and report instead of improvising**.

## Soft scenario defaults

Treat these as defaults, not rigid rules. Adapt to the task.

### Research
- Ask lighter agents to scan docs, prior art, APIs, and repo surfaces.
- Orchestrator decides what evidence changes the plan.
- Subagent output: list of relevant files + 1-line summary each, or
  detailed answer to a narrow question.

### Coding
- Give cheaper agents bounded edits or candidate patches.
- Orchestrator owns: shared-file coordination, integration, final
  review.
- Subagent output: diff with before/after, line refs, test run results.

### Testing
- Orchestrator suggests validation direction and the scripts / browser
  checks that matter.
- Lighter agents run targeted tests, browser flows, screenshots, log
  reduction.
- Subagent output: exact commands, failures, likely causes, whether
  failures look flaky, environmental, or real.

### Debugging
- Use cheaper agents to cluster logs, reproduce issues, try small
  fixes.
- Orchestrator decides which diagnosis is most trustworthy.
- Subagent output: ranked list of likely root causes with evidence.

**If a task is tiny or the validation itself needs delicate judgment,
keep it with the orchestrator.**

## Diagram

See `assets/fable-orchestrator.png` for the orchestrator-helpers
diagram.

## Claims (workload-dependent estimates, not guarantees)

For codebase-heavy work, this pattern is "up to 3-5× more
cost-efficient and 2-4× faster" when independent research, coding,
or testing slices can run in parallel. Actual savings depend on:
how parallelizable the work is, the cost ratio between the
orchestrator and subagents, and the overhead of handoff packets +
vetting.

## How this fits the rest of the skill-x collection

- Use **think-like-gpt-5-6** when you need full auditable
  task-execution rigor (intake record, requirement IDs, risk
  register, validation report, completion note). Delegation is a
  cost optimization; rigor is a quality optimization. They are
  compatible.
- Use **super-skill** when you want both: the GPT-5.6 Sol rigor
  framework as the outer loop, with the Efficient Fable delegation
  pattern as a fast lane when parallelizable.
- Use **skill-zero** when your task is specifically about probing
  the hidden states of a coding agent (mechanistic interpretability
  via linear probes).

## Pointers

- Source of this retweak:
  [BuilderIO/skills/efficient-fable](https://github.com/BuilderIO/skills/tree/main/skills/efficient-fable)
- Sister skill: [super-skill](../super-skill/SKILL.md) — rigor +
  delegation, with self-evolution
- Sister skill: [think-like-gpt-5-6](../think-like-gpt-5-6/SKILL.md)
  — full rigor framework
