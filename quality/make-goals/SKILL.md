---
name: make-goals
description: Turn a design doc into a /goal-executable goal doc.
disable-model-invocation: true
---

Read a design document, then write a goal document next to it. The goal document is a task list an agent works
through with `/goal` — one task per sub-agent, ticking boxes as it goes.

# Step 1 — Find the source document

- If `/make-goals` was given an argument, that is the path to the source document.
- If not, use the document currently open in the editor.
- If neither exists, ask which document. Do not guess.

Read the whole document, not just the headings. The goal document must be able to stand on the reasoning inside it.

# Step 2 — Look up current best practices

Search the web for how to write a good Claude Code `/goal` prompt, then apply what you find. Search terms that work:
"Claude Code /goal command best practices", "/goal autonomous loop verification".

At minimum confirm these still hold, and pick up anything newer:

- **State the finish line as checkable state, not effort.** "No call to `fetch()` remains in `src/`" beats "try to
  remove the deprecated calls." A grep can settle the first one.
- **Give every step a verification command.** Without one there is no signal, and errors compound across turns.
- **Name the scope and the file paths.** Vague scope drifts.
- **Write constraints that close shortcuts.** The agent takes the shortest path to the condition. Say what it must not
  do: never delete a test to make it pass, never tick an unproved box, never edit the design document.

# Step 3 — Learn how this project proves things

A checkbox is worthless if nobody can prove it. Before writing anything, find the real commands for build, lint or
format, and test. Look in `CLAUDE.md`, the README, `package.json` scripts, a Makefile, the solution file, the CI
workflow. Run them once if that is cheap.

Write the exact commands into the goal document. If you cannot find one, ask rather than inventing it.

# Step 4 — Write the goal document

Save it beside the source, named after it: `fix_run_design.md` → `fix_run_goal.md`. If that file already exists, ask
before overwriting.

Sections, in this order.

## 1. Title and pointer

One line naming the source design document and saying it holds the reasoning. This file holds only the work.

## 2. The problems

Summarise what we are solving. One short numbered paragraph per problem, each with a bold one-line headline first.
State the cost of the problem, not just its shape. A reader must finish this section knowing why the work is worth
doing.

## 3. The solutions

A numbered list, one entry per decision, each with a bold one-line headline. Every solution must trace back to a
problem above. This is the design in summary — no new invention.

## 4. Task breakdown

Open with one line saying how many tasks there are and how they are ordered.

**Size each task so a junior developer can pick it up and finish it.** A task is one shippable slice: the code plus
the tests that prove it.

- Good: "Create the Widget repository and add local integration tests." "Implement `GET /widgets` and add tests."
- Too tiny — fold these into the task that uses them: "Add models." "Declare interfaces."
- Too big — split these: "Build the API." "Do the frontend."

Order the tasks so each one leaves the build green and the tests passing. Later tasks may depend on earlier ones;
never the reverse.

Give every task a `### Task N — <short name>` heading and these parts:

- **Do.** What to build, in plain sentences. Include the decisions the implementer would otherwise have to guess.
- **Files.** The files to add or change, by path.
- **Tests.** What proves it works. Name the cases, not just "add tests".
- **Verify.** Any check beyond the standard commands — a grep that must come back empty, a `terraform validate`.
  Skip this part when there is nothing extra.

Then end every task with exactly this checklist, copied verbatim:

```
- [ ] Code Formatted
- [ ] Linting pass.
- [ ] Build pass.
- [ ] Tests pass
- [ ] Output code reviewed with `/code-review` for critical bugs
- [ ] All critical bugs fixed
- [ ] Code reviewed with a fresh sub-agent for coding standard violations
- [ ] Coding standard violations fixed
```

Add a short table under the task breakdown heading mapping the first three boxes to this project's real commands,
from step 3.

## 5. Goal complete

A final checklist. The goal is done when every technical task is done — nothing more, nothing less.

- One box for "all N tasks above are ticked."
- One box per whole-project command from step 3, run from a clean tree.
- Boxes for any end-state fact that a grep or a command can settle. These catch work that passed its own task but was
  undone later.

## 6. Out of scope

Only if the design names exclusions. List them, and say plainly: do not start these, and do not let a review push you
into them.

## 7. Open questions

List everything that could change or affect the implementation above. For each one: the question, why it matters, and
what changes depending on the answer.

If everything is clear, write "None." and stop. Do not invent questions to fill the section.

## 8. Execution instructions

End the document with this, in the document's own words:

1. Each task is executed independently by the code-implementer sub-agent, with fresh context per task.
2. The main thread observes progress only. Sub-agents do the work.
3. The code-implementer sub-agent must end its report with the exact list of files it added or changed for that task.
4. Pass only that file list to the reviews below — never the whole repo's diff.
5. When a task completes, update this document to tick off completion.
6. The goal is not complete until every item in this document is ticked.
7. Before executing any task, ask the clarifying questions from "Open questions" (if any).

Then add the paste-able goal prompt in a fenced block, so the user can run it straight away:

```
/goal Work through <goal-file> in <directory>. Done means every checkbox in that file is ticked, including the final
"Goal complete" list. For each task the proof is: <build command> succeeds, <lint command> reports no findings, <test
command> passes, and the file is edited to tick that task's boxes. Never tick a box you have not proved in this
session. Never edit or delete a test to make it pass. Never change <design-file>. Stop after <N> turns and report
what is left.
```

Note that two of the seven boxes are reviews, each run separately. For critical bugs, run `/code-review` on the file
list. For coding standard violations, launch a fresh sub-agent that loads the project's standards skills and checks
only that file list. Neither review sees the whole repo. After a review finds something, fix it with the
code-implementer sub-agent, then re-run build, lint and tests before ticking.

# Step 5 — Tell the user

Do not stop after saving the file. The user should never have to open the document to find out what to run next.

End the turn with a short congratulation and the runnable command. No summary of the document, no restating the task
list.

````
Congrats. Your goal doc is created at <path>.

To execute it, run with

```
/goal <the same prompt written into the document's execution section>
```
````

Rules for that block:

- The printed `/goal` prompt is the same one written into the document. Do not write two different versions.
- Fill it in. Real file path, real directory, real build, lint and test commands from step 3. No `<placeholder>` left
  anywhere in it.
- If "Open questions" is not empty, say so in one line above the command. Instruction 5 says those get answered before
  any task starts.

# How to write it

Follow the house style: short sentences, plain words, active voice, point first. No filler, no hedging, no
"comprehensive" or "robust". A junior developer is the reader.

Do not change the source design document. If the design is missing something a task needs, that is an open question,
not a decision for you to make.
