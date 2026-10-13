---
name: knowledgebase-authoring
description: Where a piece of MythiStone knowledge lives (the code, one short comment, a gotcha, AGENTS.md or nowhere) so that every fact is written once, and how to write a gotcha. Use when adding or editing a gotcha, a domain skill, an agent file or AGENTS.md, or deciding whether to record something after a task.
kind: workflow
files:
  - .claude/skills/*
  - .claude/agents/*
  - .claude/kb/*
  - AGENTS.md
---

# Authoring the knowledgebase

Every fact has one hand-written home. Store knowledge only when it is not available by reading the
relevant passage of code, meaning the passage the kb tools point to.

## Where a fact lives

| The fact is | Home |
|---|---|
| What code does: behavior, signatures, columns, constants, lists of files or commands, call chains | Nowhere. The kb derives it live |
| A reason or trap at one site | The code, as one comment of one or two lines, and only when a reader of that passage would otherwise break it |
| A coupling across files, domains or runtimes: shared connector code that the collector, the bot and the pages all call, a Python hash that SQL must reproduce, a Jinja macro mirrored in JS | A gotcha, `kind: coupling` |
| Outside the code: external API behavior, host and ops setup, tool environment traps, rejected approaches | A gotcha, `kind: external` |
| A procedure: adding a page or a table, a verify recipe | A gotcha or skill, `kind: workflow` |
| Always-on constraints, routing, shared agent rules | `AGENTS.md` |
| A domain's skills and verify step | Its agent file, `.claude/agents/<domain>.md` |
| Which paths a domain owns | The path globs at the top of `.claude/kb/kb.py` |

- **A gotcha names code and states the rule that connects it. It never restates what the named code
  contains.** `kb_gotcha` prints the live location of every symbol the body puts in backticks, and
  `kb_symbol` and `kb_file` print the docstring or header comment found there.
- When the code and a gotcha say the same thing, the code wins and the sentence leaves the gotcha.
- Never add a comment that repeats what the code does.
- If the kb reports a fact wrongly, fix the parser in `kb.py`.
- The gotcha table that ends each domain `SKILL.md` and the routing table in `AGENTS.md` are
  generated. `python .claude/kb/kb.py --index` rewrites them. Do not edit them by hand.

## When to record

The ask-first rule is in `AGENTS.md` ("Recording new knowledge"). A domain agent proposes findings
in its handoff note and the main session asks the user. Skip the ask when nothing is new:
planning-only work, or behavior a gotcha already documents.

## How to write a gotcha

```markdown
---
name: <id, kebab-case, unique across all domains>
description: <one sentence stating the rule>. Use when <the trigger>.
kind: <coupling | external | workflow>
files:
  - <repo-relative glob of every file where this rule bites>
---

# Title

Body: the rule, why it holds, and how to work with it.
```

- One file per gotcha, `.claude/skills/<domain>/ref/<id>.md`, under the domain skill that owns it.
  Only domain skills appear in the per-turn skill listing, so never add a new top-level skill for a
  single gotcha.
- `files:` decides where the gotcha is surfaced (`kb_file`, the edit hook, the domain index). A
  gotcha with an empty or wrong `files:` list is never surfaced.
- `kind:` is required. A `coupling` names at least two code sites in backticks: functions, procs,
  SQL constants or files. Lint rejects a coupling with one site, a restated signature and a
  restated column list.
- After adding, renaming or editing a gotcha, run `python .claude/kb/kb.py --index` and
  `python .claude/kb/kb.py lint` until it is clean. `python .claude/kb/kb.py --strict` adds the
  checks that need a reader: sentences that echo a comment of the cited code, oversized gotchas,
  and cited names that appear nowhere in the source (a renamed function only shows up there.
  External API fields and placeholders are expected).
- Quote a `description` that contains `: ` or ` #` (`description: "..."`). Unquoted, YAML rejects
  the first and silently truncates at the second.
- **State only the current truth, never history.** No "this used to be X", changelogs, migration
  notes or dated lines. When behavior changes, edit the gotcha so it reads as if the new behavior
  was always the behavior.
- **No line-number references.** Identify code by file, function, proc, SQL constant, class or CSS
  selector.
- **One rule per gotcha.** Link a related gotcha with `[[id]]` instead of repeating it. Lint rejects
  links to ids that do not exist.
