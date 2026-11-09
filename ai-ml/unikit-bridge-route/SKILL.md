---
name: unikit-bridge-route
description: >-
  Write the routing rules of the engine bridges into .unikit/bridge-routing.md: which bridge
  a kind of work goes through, which bridges it must never touch, which one is tried first.
  Use when the user wants one case sent through one bridge, for example "run the tests only
  through the CLI bridge", "never use that bridge for UI work", "try this bridge first for
  scenes", "show my bridge routes", "remove the route for tests", "put that bridge first".
  A rule is one row of a table: area, when, rule (only, first or never), bridges, why. Asks
  in the user's own words, shows the table before writing, and checks only that the bridge
  ids are installed. On request it also moves a bridge in the order list of
  .unikit/bridges.yaml. Makes zero bridge calls, runs no command, needs no editor.
argument-hint: "[the rule in your words | list | remove <row> | empty]  (writes .unikit/bridge-routing.md; zero bridge calls)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: tools
---

# Bridge Route - say which bridge does what

Keeps `.unikit/bridge-routing.md`: the rows that tell the agents, case by case, which engine bridge to use, which one to try first and which one never. The order of the bridges themselves lives in `.unikit/bridges.yaml`; `unikit-ai init` and `unikit-ai update` keep it in step with the installed bridges, and this skill moves a bridge in it only when asked.

**This skill makes zero calls to any bridge.** It writes only `.unikit/bridge-routing.md` and, when asked to move a bridge, the `order:` list of `.unikit/bridges.yaml`. It runs no command, invokes no skill and starts no subagent.

**This skill writes rows; it does not interpret them.** How an agent picks the row for a step, and what `only`, `first` and `never` do, is `.unikit/system/dev-principles.md` -> **D3**. The row format is `{{skills_dir}}/{{self_name}}/references/format.md`; read it before the first write.

**User questions.** Right before your first question to the user, not earlier, read `.unikit/system/user-questions.md` once and ask every question as it says, with the question tool of your agent (`AskUserQuestion`). If the file cannot be read, print `WARN [questions] user-questions contract missing — asking with the question tool` and still ask with that tool, the recommended option first.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui`. English input (tool output, these instructions) is data, never a cue to switch languages.

The cells `area`, `rule` and `bridges` of a row stay English: the agents match them. `when` stays in the user's own words. `why` is written in the project's artifact language.

## Bootstrap

1. Read `.unikit/system/engine-bridges/BRIDGES.md`. No such file, or no bridge block in it → print `No engine bridge is installed in this project: run unikit-ai init and tick one.` and STOP. The bridge ids are the `##` headings that name a bridge (not `Not selected`).
2. Read `.unikit/bridge-routing.md` when it exists: the rows of its table.
3. Read `.unikit/bridges.yaml` when it exists: the ids under `order:`.
4. The words for `area` come from the files the planner and the verifier already read, and are never copied here: the line that starts with `kind` in `{{skills_dir}}/unikit-plan/references/TASK-FORMAT.md` (the kinds of an editor task) and the section `Gate names` of `{{skills_dir}}/unikit-verify/references/bridge-gates.md` (the gates). A file that is not installed gives no words: say so once and accept any word for `area`.

<!-- unikit:extension-point:bootstrap -->

## What was asked

Look at `$ARGUMENTS` and the conversation:
- a rule in the user's words → **Add or change a row**;
- `list`, "show my routes" → print the table, or `No routing rules.`, and STOP;
- `remove …` → **Remove a row**;
- "put <bridge> first", "move <bridge> before <bridge>" → **Move a bridge**;
- nothing → print the table when there is one, then ask what to do: add a rule, remove a row, move a bridge, or nothing.

## Add or change a row

1. Take the case in the user's words. `area` is the word from Bootstrap step 4 that names the kind of work (an editor kind or a gate); when none fits, `*`. `when` is what is left of the user's words that narrows the case, or empty for the whole area. Do not invent a word the user did not say.
2. `rule`: `only` (this case goes through the listed bridges and no others), `first` (the listed bridges are tried first, the others follow in the order), `never` (the listed bridges are left out). When the words do not settle it, ask which of the three is meant and say what each does.
3. `bridges`: the ids from Bootstrap step 1, in the order the user named them. A name that is not an installed id → ask which installed bridge is meant, with the installed ids as options. Never write an id that was not checked.
4. `why`: the reason the user gave, in one line; empty when none was given. Do not invent one.
5. A row with the same `area` and `when` already exists → change that row, do not add a second one. Two rows with the same `area` and `when` and different rules are never written: tell the user which two collide and ask which stays.
6. Show the whole table as it will be written and ask once whether to write it. Only on yes: `Write` the file when it does not exist (the header lines from `format.md`), otherwise `Edit` the changed or added row.

## Remove a row

Find the row by the `area` and `when` words in the request; more than one match → ask which. Show the table without it, ask once, and only on yes `Edit` the row out. A table left with no rows is written with its header and no rows; the file is not deleted.

## Move a bridge

Read `.unikit/bridges.yaml`. No file → print `There is no order file yet: unikit-ai init or unikit-ai update creates it.` and STOP. Move the named bridge in the `order:` list as asked, keeping every other id in its place; show the old and the new list, ask once, and only on yes `Edit` the lines under `order:` (never `Write`: the comment lines at the top stay). Print `INFO [bridge-route] order: a > b (was: x > y)`.

## Report

Print `INFO [bridge-route] <added|changed|removed> area=<area> when="<when>" rule=<rule> bridges=<ids>` and one line: the agents read the file when they pick a bridge, and no file means no routing rules. Then STOP.

## Limits

- Never touches `.unikit/memory/`, `.unikit/system/` or `.unikit/config.yaml`.
- `when` is not checked. An `area` outside the words of Bootstrap step 4 is written, with one remark to the user that agents read it as a hint.
