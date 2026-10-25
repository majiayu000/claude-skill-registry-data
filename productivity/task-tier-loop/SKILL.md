---
name: "task-tier-loop"
description: "Use when planning any project's work across chat, Claude Code and plain Python, to pick a tier per task and run the plan, brief, run, check, review, decide loop with .md hand-offs."
---

# Task tiers and the hand-off loop

From the user's doc "Stretching Claude Pro: A General Workflow" (a Claude chat artifact). On a flat plan the scarce thing is usage, so spend it where a mistake is expensive. The deciding question for any task: if the answer is wrong, how costly is it, and how quickly would I notice?

The user prefers Claude over local models, so tier B means a cheaper Claude model or a short focused session, not Ollama, unless they ask.

## Three tiers. Pick one before opening a session; if unsure, go one tier up.
| Tier | Who | Typical tasks | Why |
|---|---|---|---|
| A | Claude, full session | planning and architecture, hard debugging, auth, payments and security code, reviewing others' output, vague requirements | a wrong answer is costly or hard to spot |
| B | cheaper or shorter session | repetitive edits, boilerplate, formatting, tests from a clear spec, docs, data clean-up, scripts with clear input and output | easy to check, cheap to redo |
| C | plain Python, no model | counting, deduping, sorting, date maths, checking a quote is in a saved page (`verify.py`), fetching and saving pages | same answer every time, costs nothing |

Move a task down a tier only if you can describe the finished result in a paragraph AND check it in minutes by running it or reading a diff.

## The loop (every hand-off is a .md file)
1. **Plan** on Claude: split the goal into small tasks, save `plan.md`.
2. **Brief per task:** `tasks/001.md` with the goal in one sentence, files it may touch, what done looks like, what it must not change.
3. **Run** each task in a fresh session (or as a Python script for tier C). One task per session.
4. **Check with code first:** tests, the script, `verify.py`. Model output is not trusted until something other than the model checked it.
5. **Claude reviews the diff only:** the brief plus the change, not the whole project.
6. **The user decides:** accept, or send back with a note in the brief file.

Research follows the same order: save the page as a .md snapshot with url and date, record each claim with an exact quote, let `verify.py` confirm it before anyone reads it.

## Chat to Claude Code hand-off
When work moves from chat to the laptop, the hand-off is a `HANDOFF.md` in the repo: where we stopped, the ordered task briefs, what each check should print, and the open decisions. Claude Code starts from that file, not from chat history.

## Habits
Short sessions, one task per session, brief files instead of re-explaining, show only the file or diff needed, move mechanical work to code, prefer fewer larger requests.