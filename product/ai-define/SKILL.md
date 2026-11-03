---
name: ai-define
description: Define an AI feature — the job it does, for whom and when, whether AI is the right tool at all, success criteria a check could test, the failure modes that matter, and latency and cost budgets. Use when a product team wants to add an AI feature and has not yet pinned down what good looks like. Not for assessing AI regulation; see /compliance-eu-ai-act.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ai
  phase: 1
  artifact: 01-define.md
---

# Define

Pin down what the AI feature in "$ARGUMENTS" must do, and what would make it fail, before anyone writes a prompt.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ai-define","workflow":"ai","phase":1,"project":"<project>","event":"skipped","artifact":"01-define.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Define) of the AI Feature Lifecycle workflow (`ai`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ai` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole AI Feature Lifecycle workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-define","workflow":"ai","phase":1,"project":"<project>","event":"started","artifact":"01-define.md","note":""}`.

None — this is the first phase.

## Process

1. **Read what exists:** artifacts in `.singularskills/research/<project>/`, `.singularskills/support/<project>/` and `.singularskills/analytics/<project>/`, for the users, their problems and the metrics already agreed.

2. **Ask the user what you could not find**, once and together:
   - What should the feature do, for whom, and at what moment in their work?
   - What do users do today instead?
   - What content, data or tools could it use?
   - What would make it embarrassing or harmful if it went wrong?
   - How fast must it answer, and what may one use cost?

3. **Describe the job:** the user, the moment, the input they give, the output they get, and what they do next with it.

4. **Check whether AI is the right tool at all.** A rule, a search, a form or a template may do the job more reliably and cheaply. Say which, and why AI is or is not needed; if it is not, say so plainly and stop recommending the rest of the workflow.

5. **Write the success criteria**, each phrased so a check could tell pass from fail ("cites the help-centre article it used", not "is helpful").

6. **List the failure modes that matter,** each with an example and its harm: wrong, made up, unsafe or offensive, off-task, leaks data, ignores the user's constraint, too slow, too costly.

7. **Set the budgets:** latency per use, cost per use and per month, each labelled `target`.

8. **Write the artifact** to `.singularskills/ai/<project>/01-define.md` with sections:
   - **Job** — user, moment, input, output, next step
   - **Is AI the right tool?** — the alternatives and the answer
   - **Success criteria** — each testable
   - **Failure modes** — example and harm for each
   - **Budgets** — latency and cost

## Output

The definition written to `.singularskills/ai/<project>/01-define.md`. Present a summary to the user highlighting:
- Whether AI is the right tool, and why
- The success criteria
- The two failure modes with the worst harm

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ai-define","workflow":"ai","phase":1,"project":"<project>","event":"finished","artifact":"01-define.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: ai-define
workflow: ai
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
