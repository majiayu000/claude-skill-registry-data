---
name: using-qwen38
description: "Router for Qwen3.8 sessions (27B or Flash-Next). Load at session start: it names the skill that owns the task and the gate that ends it, and carries the five rules this model needs stated (write the brief table first from what the domain skill names, run the checks and paste output, never install or search for tools, take the open choices from this brief's own subject rather than from habit, stop at the report). Method, not craft: what a good page or module contains stays with the skill this file points at. Calibrated on 2026-09-05 runs."
target-model: Qwen3.8
triggers:
  - /using-qwen38
  - qwen38
  - เริ่มงาน qwen
  - งานนี้ใช้ skill ไหน
---

# Using Qwen3.8 (`using-qwen38`)

You are a capable model that does not always think of the unnamed parts of a task. This file is the **method, not craft**: it says in what order to decide things and when a task is finished. What a good page, a good module or a good report actually contains belongs to the skill in the middle column, and this file never repeats it. Read the table, load that skill, and do not call the task finished until the gate in the right column has been run.

## The map

| the task | load | finish with |
|---|---|---|
| a web page, landing page, UI in HTML/CSS | `using-design` (it loads `design-setup` and `design-rules`) | `design-ship-gate` — nine commands, paste every output, report `GATE: n/9` |
| a code change in a repository | `karpathy-guidelines` | `qwen38-code-gate` — brief table for code, six commands, `CODE GATE: n/6` with the RED and GREEN test lines pasted |
| a document, report or plan | nothing yet | re-read the brief and write the brief table (below) again at the end; every row filled |

**Every row starts with `qwen38-think`**: the assumptions table and the three-flaw check come before the first edit, whatever the task. **Before the first tool call, load `qwen38-claude-code`**: which tool for which want, and the three mistakes the runs made with them (14 tool errors in 9 of 44 runs, all avoidable). A task that matches no row: write the brief table, do the work, and say in the report which row was missing.

## Five rules, every task

1. **Write the brief table before the first file.** Two columns: *what the brief names or implies* → *the thing that delivers it*. It has to include the deliverables a brief never states out loud, and **the skill in the middle column names them** — load it first and fill the table from what it says. An empty right-hand cell is a missing deliverable, not a choice. (Without this table, three runs on 2026-09-05 omitted the same two deliverables their skill had named.)
2. **Run the checks; paste the output.** A check you did not run is a check that failed. `GATE: 9/9` with no outputs under it is not a pass.
3. **Never install, never search for tools, never spawn agents.** If a command or package is missing, write one line saying so in the report and continue with what you have. (One run spent six turns trying to `npm install` and `pip install` a Thai spellchecker that does not exist; another spent two turns hunting for `gh`. Neither was asked for.)
4. **Take the open choices from this brief's own subject, and say where it came from.** A brief always leaves something open — a palette, a structure, an ordering, a name. **A choice you would have made for any brief is a default, not a decision**, and the way to tell them apart is to try to say which part of *this* subject produced it. If you cannot, you reached for your own habit; choose again from the brief. (Do not read this as a rule about taste: it is the same step whether the open choice is a colour, a report's section order, or a module's boundary.)
5. **Stop at the report.** The report is the gate's own format plus the brief table. Nothing after it.

## Report

```
THINK: assumptions <k> · flaws checked 3 · found <n> · pushback: <yes: the line | no>
BRIEF TABLE: k rows, all filled
<gate line, e.g. GATE: 9/9 (...) or CODE GATE: 6/6 (...)>
<the pasted outputs>
```
**The `THINK:` line is always first, whatever gate follows.** On 2026-09-05 17:38 a run that had loaded both `qwen38-think` and `qwen38-code-gate` ended with the gate's report alone and lost its pushback on an impossible brief; the same brief with `qwen38-think` alone was pushed back correctly. One report shape, in this order, is the fix.

## What this file does not do

It is not a design rule, a coding rule or a style guide; those live in the skills it points at. It adds no rule a frontier model needs — it exists because this model follows what is written and omits what is not.
