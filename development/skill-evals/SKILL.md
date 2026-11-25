---
name: skill-evals
description: Build evals for an AI agent that already does real work. Use when someone asks "how do I know my agent is right", wants to test an agent before trusting it, compare models on cost versus quality, or turn production failures into tests. Walks from first tasks and yes/no verifiers, to isolated environments, to a trace-driven improvement loop.
---

# Agent evals

An eval answers one question: did the agent do the job correctly?
Everything below is a way to ask that question more reliably, more cheaply, and more often.

Built from the evals masterclass by Alex Lieberman with Viv (LangChain), 2026:
youtube.com/watch?v=zLeG-XJtbIE. The structure (easy, hard, god mode) is theirs. Mistakes in this skill are ours.

## Start by asking the user three things

1. What real job does the agent do? Name the system it touches (CRM, inbox, repo, database).
2. Who in the company is best at that job today? Their judgment is the ground truth.
3. Does the agent run in production yet? If yes, are traces stored anywhere?

Pick the mode from the answers. Do not skip to god mode without tasks and verifiers.

## Easy mode: tasks and verifiers

A **task** is a small, checkable piece of the real job.
A **verifier** says whether that task was done right.

1. Write 10 to 30 tasks that copy what real colleagues do. Examples for a sales agent:
   - add a note to a CRM record after a call
   - find a prospect who is not in the obvious table
   - draft a reply email without sending it
2. For each task, write the verifier. Prefer, in order:
   - **State check** (a script): the field was empty before and holds the right value after; the tag `email_sent` exists.
   - **Checklist** (a model or a human): for anything not directly verifiable, break "good" into yes/no questions. "Three paragraphs or fewer?" "Uses the brand tone rules?"
3. Keep every judgment binary. Models asked for a 1 to 10 score cluster around 7 and hedge. Yes/no cannot hedge.
4. Get the checklist from the best person at the job, in writing. Run the agent, review a sample by hand. If an output passes the checklist but still feels wrong, the checklist is incomplete. Add the missing question.

Output of easy mode: a folder of tasks, each with an instruction and a verifier, and a pass rate.

## Hard mode: environments

An **environment** is where the agent does the work: its files, tools, data and permissions.
Never eval against production data. An agent that fails the eval also edits the real CRM.

1. Build a copy that looks real to the agent: same tables, same tools, fake records. Package it so it resets to the same state every run (a container is the usual choice).
2. One task = instruction + environment + verifier. Store them together.
3. Do not roll your own runner if you can avoid it. Harbor (github.com/harbor-framework/harbor) has shared formats for tasks, environments and verifiers, and many published tasks you can adapt.
4. **Test the environment itself.** Your first one is wrong. Run several different agents or models through it and look for strange patterns:
   - a strong model fails where a weak one passes
   - an agent finds the answer somewhere it should not be (a placeholder row, a leaked file). Agents will take any shortcut to pass. Remove the leak.
5. **Tag every task by family** (coding, sales, code review). When a new model ships, run only the families it might be good at.
6. **Pick models with a table, not a feeling.** Run each candidate on the same tagged tasks. Record pass rate, cost, and speed side by side. Then a human decides: is 5 points of accuracy worth 3x the cost for this family? User-facing tasks usually justify the top model; internal ones often do not.

Output of hard mode: an eval suite you can rerun on any model in one command, with a results table per task family.

## God mode: the improvement loop

The loop: the agent runs, produces traces, failures become new tasks, the agent gets fixed, repeat.

1. **Turn on tracing.** A trace is the log of every action: each tool call, each message, each result. Nobody can predict what an agent will do. Everybody can judge what it did.
2. **Store traces in one place.** For a single developer, the agent's own logs on disk are enough. For a team, use a tracing product with permissions.
3. **Point a second agent at the traces.** Its only job is finding patterns. Give it a short brief of good and bad behavior. Ask it for:
   - failed or repeated tool calls
   - instructions it ignored or half-followed
   - a recurring wrong path (always searching the wrong table, doing one company when asked for three)
4. **Turn each confirmed failure into a task** in the eval suite, so it can never silently come back.
5. **Fix the agent**, cheapest lever first:
   - harness: prompt, tool descriptions, tool set, model choice
   - fine-tuning a small open model on the narrow task, once the suite proves it matches the large model
6. **Keep a human on what "good" means.** Agents can propose fixes and draft tasks. A human still decides which tasks matter to the business and reviews new ones. Writing that down is the highest-leverage part of the loop.

## Rules

- No eval without a named real job. Generic benchmarks do not tell you if your agent works.
- Binary verifiers only. Split any score into yes/no questions.
- Never let an eval touch production data.
- A suite that everything passes is a broken suite. Check for leaks.
- Report pass rates with the task count next to them ("21 of 30"), never a bare percentage.
