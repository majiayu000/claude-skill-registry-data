---
name: qwen38-think
description: "The thinking a small model skips, as steps it must write down: before the first edit, an assumptions table and a three-flaw check on the brief (contradiction, missing fact, impossible ask), each flaw checked by a command; when stuck, one observation, one hypothesis, one falsifying command; and a THINK report line. Pushback is a written line in the report, never a question that stops the work. Slice 2 of xeno-skills #355."
target-model: Qwen3.8
triggers:
  - /qwen38-think
  - think first
  - ตรวจโจทย์ก่อนทำ
  - โจทย์นี้มีอะไรผิดไหม
---

# Think first (`qwen38-think`)

**Before the first edit, write the two tables below into your answer. Then build. End with the THINK line.** Doing the work first and the tables after is a fail of this skill.

## 1. Assumptions table

Everything the brief leaves open that changes what you would build. Take the assumption; do not ask.

| open in the brief | the assumption you take | why this one |
|---|---|---|
| e.g. "ordering when quantities tie" | by sku, ascending | the brief orders by quantity; a stable secondary key is the usual reading |

Zero rows is allowed only if you write "none — the brief fixes every choice" and can point to where.

## 2. Three-flaw check — each one checked, not guessed

| flaw type | what you looked for | the command you ran | found? |
|---|---|---|---|
| **contradiction** — two sentences of the brief cannot both hold | e.g. "return None" and "return the remaining quantity" | `grep -n "return" <file>` / re-read the brief | yes / no |
| **missing fact** — a file, function, endpoint or value the brief names does not exist | e.g. `inventory/report.py` | `ls <path>` · `grep -rn "<name>" .` | yes / no |
| **impossible ask** — the brief forbids the only way to do what it asks | e.g. "make X O(1) without changing Y" | read the code path; name the line that makes it impossible | yes / no |

**When a flaw is found:** do not stop, do not ask, do not invent the missing thing. Write one line under the table — *"Pushback: the brief says A and B; I build A because …"* / *"Pushback: `inventory/report.py` does not exist; I did not create it; the nearest file is …"* / *"Pushback: not possible as stated because …; I did the possible part: …"* — and build the part that stands. The developer reads the report; a question asked **instead of** the work only stops it. In an interactive session you may ask once the report is delivered; in an unattended run there is nobody to answer, so the report is the whole channel.

## 2b. Thinking is for decisions, not for code

Decide in thinking — the structure, the file order, the risks — then build with tools. For work that spans files, write the order in one line (`index.html → css → js/scene.js → js/main.js`), then Write the first file. A file drafted in thinking is written twice (the draft, then the `Write`) and lost if the turn is cut: one GSQ turn was a 43,564-character thinking block with the whole page and both shaders in it, hit the output limit and wrote nothing; from the next turn, one file per turn after short thinking, all four files were done in 15 minutes (#377). Check what you built by running the check (`node --check`, the tests, the gate), not by re-reading it in thinking.

## 3. When stuck (a command fails twice, or the output makes no sense)

Write three lines before the next attempt:

```
Observed: <the exact last line of the failing output>
Hypothesis: <one cause>
Falsify: <one command whose result would rule it out>
```
Run the falsifying command. If the cause is a missing tool or package: one line "`<tool>` is not installed; continuing without it" — **never install, never search for an alternative, never spawn an agent** (`using-qwen38`).

## Report

```
THINK: assumptions <k> · flaws checked 3 · found <n> · pushback: <yes: the line | no>
```
The line is the **first** line of the final report, before the task's own gate line (`CODE GATE`, `GATE`) when there is one — a gate report that starts with "Done." and no `THINK:` line dropped a correct pushback on 2026-09-05 17:38.

## What this does not touch

How to build the thing — the task's own skill and gate. This file only makes the model write down what it would otherwise silently assume, and say what is wrong with a brief instead of working around it.
