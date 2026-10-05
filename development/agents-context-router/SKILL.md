---
name: agents-context-router
description: Split a bloated AGENTS.md / CLAUDE.md / README into a small always-loaded kernel plus task-routed wiki topics, loaded on demand by a zero-dependency script (`scripts/ai-context.py list|<topic>|check`) with byte budgets, so agents stop burning their context window on docs unrelated to the task. Use this skill whenever the user says AGENTS.md or CLAUDE.md is too long, too big or loads too much context; asks to split, slim, reorganize, route or "wiki-fy" repo docs or agent instructions; wants a docs router, progressive disclosure or context budget for coding agents; mentions milestone logs piling up in the README; or wants multiple agents (Claude Code, Codex, Cursor, Gemini) to share one instruction file, even if they never say "router".
---

# Agents context router

Coding agents load the root instruction file (AGENTS.md, CLAUDE.md) on every task. As a project ages it collects milestone logs, tool catalogs, runbooks and one-off lessons, until every task pays tens of KB of context for text it does not need. The fix is a **kernel + router** layout:

```
AGENTS.md                 kernel: rules every task needs + how to load more (≤ 8 KB)
wiki/ai-context.json      topic → sources (whole file or one exact heading); the single truth
scripts/ai-context.py     list | <topic> | check  (bundled with this skill)
wiki/README.md            human router table (mirrors the JSON)
wiki/ai-context.md        in-repo maintenance manual (works without this skill)
wiki/<topic pages>.md     how-to / reference, one per task seam
wiki/history/*.md         milestone logs, verbatim, never loaded by default
README.md                 humans: what it is, quickstart, doc map
```

An agent reads the kernel, picks the one topic that matches its task, and runs `python3 scripts/ai-context.py <topic>` to print only those sections, each marked `<!-- path § heading -->`, so it knows where to edit.

The layout also **maintains itself** once this skill is gone, because every piece lives in the repo:
- The kernel's "Keep the docs true" rule makes every agent, on every task, fix a stale doc in the same change that makes it stale.
- `wiki/ai-context.md` is the procedure.
- `check` fails on orphans and budget overruns.
- CI runs `check`, so drift breaks the build instead of rotting quietly.

Leaving out any one of these four is how routed docs decay back into a pile.

Before you start, read `references/gotchas.md`. It lists the traps that make this refactor quietly lose content or route agents to the wrong text. It is short.

## Workflow

### 1. Measure

List every file an agent loads automatically: root and nested `AGENTS.md`/`CLAUDE.md`, and anything they `@import`. Also list the files agents are told to read "first". Record their byte sizes (`wc -c`). These numbers go in your final report as before and after.

Keep a backup of each original outside the repo (or rely on git), because step 3 moves text and you will diff against it.

### 2. Classify every section

Read the whole file and put each section into exactly one bucket:

| Bucket | Test | Goes to |
|---|---|---|
| **Kernel** | Would a wrong action happen on *any* task if the agent did not know this? Examples: hard limits, safety rules, language rules, where outputs may go, the rule that says when to load a topic. | `AGENTS.md` |
| **Topic** | Needed only when doing one kind of task: build and deploy, debugging, a subsystem, a tool catalog. | `wiki/<topic>.md` |
| **History** | Dated milestone logs, acceptance runs, "what we did in M3". | `wiki/history/<milestone>.md` |
| **Human** | Intro, screenshots, setup for people. | `README.md` |

Some text changes buckets. A behaviour rule learned the hard way (for example "if every job fails the same way, suspect our code before the site") is kernel. The procedure for acting on it is topic. A history section that is still the operating manual (a "Usage" section in a milestone log) stays in history, and a topic references its exact heading.

### 3. Move, then write

1. **Before moving any log, pull out the live rules hidden in it.** Old logs often contain a rule that is still in force, written as an aside ("note: never run X on shared"). Once the log moves to history, no agent will ever see that rule again. Grep each log for imperative words in every language it uses, for example `never|always|must|do not|don't|warning|note:|avoid|forbidden|required`. For each hit that is still valid, copy it as a one-line rule into the kernel (if it applies to every task) or into its topic. List every promoted rule in your report.
2. Create `wiki/history/` and move milestone logs there **verbatim**, in their original language. Do not translate or summarise while moving. Verbatim moves are diffable and lose nothing.
3. Design topics around **tasks the agent will be doing**, not around the old file order. Aim for 5–12 topics. Each one gets a kebab-case name and a single "use when…" line. Ask: "an agent is about to do X; which pages must it see?"
4. Write the topic pages. Move reference text and runbooks in, and cut the duplication the old file had.
5. Rewrite `AGENTS.md` as the kernel. Start from `assets/AGENTS.kernel.md`. It holds:
   - the one-paragraph purpose;
   - the language rules, stated once;
   - the always-apply rules, including **Keep the docs true**, verbatim or adapted;
   - the hard limits;
   - the load-context block with a topic table;
   - the verification commands.
6. Slim `README.md` to intro, quickstart and a doc map pointing to `wiki/README.md`.

### 4. Wire the router

1. Copy `scripts/ai-context.py` from this skill to `<repo>/scripts/ai-context.py`. It resolves the repo root as the script's parent's parent.
2. Write `wiki/ai-context.json` from `assets/ai-context.json`. Use `{"path": ...}` for a whole page. Use `{"path": ..., "heading": "Exact Heading Text"}` to pull one section out of a bigger page, such as a single tool group from a catalog.
3. Write `wiki/README.md` from `assets/wiki-README.md`: the topic table for humans, plus a history index.
4. Copy `assets/wiki-ai-context.md` to `wiki/ai-context.md` and keep the `ai-context` topic that points at it. This is the manual any future agent loads to maintain the router, with or without this skill. The config location `wiki/ai-context.json` is fixed in the script. If the repo uses other directories, set `wikiDir`, `historyDir`, `routerFile` or `rootInstructions` in the JSON, and update the paths in `wiki/ai-context.md` to match.
5. **Pick the Python command for this machine and repo.** The assets and examples in this skill write `python3`, which does not exist on a typical Windows install (it is often a Microsoft Store stub that fails). Probe `python3 --version`, then `python --version`, then `py -3 --version`; the first that prints Python 3.8+ is the command. On Windows expect `python` or `py -3`. Write that same command everywhere you copy text from the assets: `AGENTS.md`, `wiki/README.md`, `wiki/ai-context.md`, and the CI/hook entries in 4b. If the repo is used from both Windows and Unix, say so in the kernel's load-context block (for example "Windows: `python` or `py -3`"). Do not add a wrapper script.
6. Run `check` with that command (`python3 scripts/ai-context.py check` below). It fails when:
   - a path or heading is missing, or a heading is ambiguous;
   - `AGENTS.md` is over its budget;
   - a topic is over its budget;
   - a topic is not named in `AGENTS.md`;
   - there is an **orphan**: a wiki page no topic loads, a history file missing from the `wiki/README.md` index, or a nested `AGENTS.md` no topic loads.

   Fix the docs, not the caps. When a topic is too big, split it. When a page really is human-only, list it under `"unrouted"` with a reason, and remove the template's example entry.

### 4b. Make drift fail the build

Wire `check` into whatever the repo already runs on every change. Use the one that exists; do not add new tooling:

| Repo has | Add |
|---|---|
| `package.json` | `"docs:check": "python3 scripts/ai-context.py check"`, chained into `test` |
| `Makefile` | a `docs-check` target, made a prerequisite of `test` or `check` |
| `.pre-commit-config.yaml` | a local hook: `entry: python3 scripts/ai-context.py check`, `pass_filenames: false` |
| `.github/workflows/*.yml` | a step `run: python3 scripts/ai-context.py check` in the existing test job |
| none of these | add the command to the kernel's Verification block and say so in the report |

### 5. Point every agent at the kernel

- **One file for every agent.** Keep the rules in `AGENTS.md`. If an agent you use does not read `AGENTS.md` natively, make its file a one-line pointer instead of a copy (for Claude Code, a `CLAUDE.md` holding `@AGENTS.md`). Two full copies drift apart within a week. Check each agent's current docs or version, because native support is changing fast.
- **Skills and scripts are adapters.** If the repo has skills, commands or prompts that restated the old docs, cut them down to workflow steps that say "load topic X". The rules live only in the kernel and the wiki.
- **Other agents' stale paths.** If other agents or sessions are working in the repo, tell them the docs moved and which topic replaces what, because their context still holds the old paths.

### 6. Verify and report

- Run `check` and show its output.
- Run `ai-context.py <topic>` for two or three topics, and read the output as an agent would. Can you do the task from this alone?
- Grep for links to old anchors and moved files, and fix them.
- Compare the byte totals between the backup and the new tree. A large drop in total bytes, not just kernel bytes, means content was lost rather than moved. Find out where it went.

Report in the user's language:

```
## Context split
- Always-loaded: <before> B → <after> B (<file list>)
- Topics: <n>; largest <name> <bytes> B; all under budget (check output below)
- Moved verbatim to wiki/history: <n> files
- Content kept: <total before> B → <total after> B (<explain any drop>)
- Adapters updated: <skills/CLAUDE.md/etc>
- Self-maintenance: kernel rule ✓, wiki/ai-context.md ✓, check in <CI/test/pre-commit> ✓
- Follow-ups: <e.g. translate zh pages, split topic X if it grows>
```

## Maintaining it later

Upkeep is the job of the repo's own `wiki/ai-context.md` and the kernel rule, not this skill, so it happens on ordinary tasks too. When this skill is triggered for maintenance (for example "add this runbook", "check is failing" or "we finished M7"), load the `ai-context` topic and follow it:
- **New knowledge:** put it in the page for its topic. If no topic fits, add a page, map it in the JSON, add it to both tables and run `check`.
- **New milestone:** add `wiki/history/<m>.md` and one row in the history index. Nothing is added to the kernel unless it is a rule for every task.
- **Kernel near its budget:** that is the signal to move something out, not to raise the cap.
- **Orphan failure:** map the page to a topic, index the history file, or, only if it is really human-only, list it under `"unrouted"` with a reason.
