---
name: todoHelp
description: "Print the Prompt TODO cheat sheet, most important first: what to type to work an item (#12, #new, #newCam, #new1, a pasted line), how to finish one (works, fixed, works #12) and what that does, then the skills table from the flow readme (/todoFromTicket, /todoIdealPrompt, /todoReverse, /todoArchive …). Read-only; touches nothing. Use when the user asks how the todo flow works or what to type — phrases like '/todoHelp', 'todo help', 'how do I use the todo', 'what do I type to work an item', 'how do I finish an item', 'which todo skills are there'."
argument-hint: ""
allowed-tools: Read
---

# /todoHelp

One screen, ordered by how often it is needed: the two things typed every day first, the
skills after. Print it and stop — no questions, no edits. The full explanation is in
`.claude/prompt-todo/README.md`; the exact rules in `.claude/prompt-todo/RULES.md`.

## What Claude does

1. **Read `.claude/prompt-todo/config.json`** (`Read` tool) for the confirm words
   (`confirmWords`; the sheet shows the first two), the tracker (`tracker.kind`), the
   app-navigation state (`appNavigation.mode`), the code markers (`codeMarkers`), the
   prompt scores (`promptScores`) and the line width (`maxLineLength`). Read `.claude/prompt-todo/README.md` and take the
   `### Skills` table — the markdown table right under that heading, header row to the last
   `|` line. If the config is missing, say `install.sh` has not been run here and print the
   sheet with the defaults.

2. **Print the sheet**: the block below as written — `<user.name>` stays literal, it means
   `git config user.name` — with the confirm words from step 1, then the Skills table
   verbatim, then one line for each thing that is off:
   `tracker.kind = none` → `/todoFromTicket takes pasted ticket text only — /todoSetup tracker connects Jira or GitHub`;
   `appNavigation.mode = none` → `/appNavigation is not connected — /todoSetup appNavigation`;
   `codeMarkers = off` → `Code markers are off — /todoMarkCode on`;
   `promptScores = off` → `Prompt scores are off — /todoScore on`;
   `maxLineLength = 0` → `Line width is off — set maxLineLength in .claude/prompt-todo/config.json and re-render`.

## The sheet

```
TODO.<user.name>.md — one item per line: `- [ ] #12 text`  (done: `- [x]`)

Work      #12 · #12 plus an addendum · #new / #newCam / #new1 (number it, then work it) · a pasted line
Hold      #12 #wait … paste logs, more text … #go
Finish    works / fixed → tick + rewrite to the ideal prompt · works #12 names it · ok → tick only
Markers   every change for #12 carries `[<user.name>#12]` in a comment, so grep leads back to the prompt · /todoMarkCode on|off
Scores    the rewrite appends (N/5) — how close your prompt was to the ideal · /todoScore on|off
```

Then the `### Skills` table from `.claude/prompt-todo/README.md`, as is.

## Notes

- The confirm words in the `Finish` line are the configured ones; the sheet never invents others.
- The skills table is never retyped here; it comes from the readme so the two cannot disagree.
