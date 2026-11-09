---
name: unikit-execute
description: >-
  Carry out one small task straight from its description, with no plan: the plan-free
  counterpart of /unikit-implement, and the code-execution skill the pipeline delegates
  to. It reads the project rules and the engine bridges, works out from the text whether
  the task is code, editor work (scenes, prefabs, UI, assets, project settings) or both,
  makes the change, checks that the code compiles, reads the changed editor state back,
  and ends with a report and an offer to review or commit. Use it when the user says
  "without a plan", "no plan", "just do it", "directly", "quickly add ...", "set this up
  in the editor". It reads no plan file and ticks no checkbox. For a bug use /unikit-fix;
  to carry out an existing plan from .unikit/code/plans/ use /unikit-implement; for a
  multi-step feature use /unikit-plan; to discuss an approach use /unikit-explore.
argument-hint: "<task description> [--docs=yes|no|warn] [--editor=engine-bridge|manual|direct]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(git *)
  - Bash(date *)
  - Skill
  - AskUserQuestion
---

# {{engine_name}} Task Execution

Carry out one task from its description the way `/unikit-implement` carries out a plan task — rules and bridges loaded once, the work done inline, the result checked and reported — but with no plan: no plan file is read, written or ticked.

**User questions.** Right before your first question to the user, not earlier, read `.unikit/system/user-questions.md` once and ask every question as it says, with the question tool of your agent (`AskUserQuestion`). If the file cannot be read, print `WARN [questions] user-questions contract missing — asking with the question tool` and still ask with that tool, the recommended option first.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Skill calls

Where this skill says to **invoke `<skill>`** — optionally "with the argument `<text>`" — it means one call, made in this session, now, on every runtime: not a command printed for the user and not a delegation. A call site that names no argument passes none.

1. If you have a `Skill` tool that accepts arguments, call it with that skill and the arguments of the call site, in full and unchanged, then follow the skill.
2. Otherwise — no `Skill` tool, or one that takes only a name — Read `{{skills_dir}}/<skill>/SKILL.md` in full, treat it as the instructions of this step and carry them out here, in this session, now, with the arguments of the call site as the skill's arguments.
3. When the skill has run, go on to the step the call site names. Do not print a command for the user to run and do not stop.
4. Only if that file cannot be read: print `Run: /unikit-<skill> <arguments>` for the user and stop.

## Input

`$ARGUMENTS` — the task in the user's own words, with at most two flags:

- **`--docs=yes|no|warn`** — the documentation policy of this run (Step 5.2); default `warn`.
- **`--editor=engine-bridge|manual|direct`** — how the editor changes of this run are carried out (Step 3); default by the rule of Step 3.
- **the description** — everything that is not a flag, kept as written. It may carry wishes about the bridges or the mode: "only through the command line", "leave the second bridge out", "do not touch the scene by hand".

A flag value outside its list → `ERROR [execute] invalid --docs value; expected yes|no|warn` (for `--editor`: `engine-bridge|manual|direct`) → STOP. An empty description → print `Usage: /unikit-execute <task description> [--docs=yes|no|warn] [--editor=engine-bridge|manual|direct]` → STOP.

## Workflow

### Step 0: Delegate mode

**The arguments begin with the line `Delegated hand-off:`** — a parent skill has bounded the task and keeps the start and the end of the flow for itself, and nobody reads this conversation. This is the **delegate mode**:

- there are no flags and no questions: what is unclear becomes `manual`, or the whole task goes back to the caller with the reason;
- the plan-file check (Step 2) and Step 5 are not run: the report of Step 5.3 is the reply, in English, and the caller decides about documentation, context files, review and commit;
- the `Editor:` lines of the hand-off are the card as written, and its `Editor tasks:` or `editor_mode:` line is the mode (Step 3);
- a hand-off with no `Editor:` line — a fix, a verification — is classified from its text by Step 2;
- a line the hand-off marks `manual` is never carried out;
- tests follow the hand-off: written only when it asks for them and at once, a run only when it asks for one; nothing waits for acceptance, because the caller owns it.

Any other arguments → the normal flow, which starts with the flags of **Input**.

### Step 1: Load the context

Load the project knowledge base once, before the first change. Do not print what you read.

**Development principles — BLOCKING PRE-REQUISITE.** Before producing ANY code, silently read `.unikit/system/dev-principles.md` and apply its rules to ALL subsequent output. Read everything **above** the LAZY-READ BOUNDARY (`Grep -n '^<!-- === LAZY-READ BOUNDARY === -->'`, then `Read` with `limit` set to that line): Layer A — the evidence contract (`CLAIM / EVIDENCE / VERDICT`, the claim-class → evidence-class lattice, the nine failure classes, discipline, phase order, lane, stop-conditions, the `kind` and area vocabularies, "no rules ≠ no rights"), then the engine workflow and the code conventions (engine bridge usage, comments policy, docs requirements, the test policy, TODO handling). The section **below** the boundary is read once per session, at the first call through a bridge (Step 4) — unconditionally, never gated on which rules are installed; a run that reaches no bridge never reads it.

Then, in the same pass:
- `.unikit/system/engine-bridges/BRIDGES.md` and, for each bridge whose block names a rules tree, that tree's `.unikit/system/engine-bridges/<bridge>/INDEX.md`, **base section only** — the stamp under the title (the `bridge` row) plus every section **except** the `## Check` table — access, the live failure classes, shape and cost, what is irreversible, the lane, and what to do when the file is silent. The `## Check` table is **not** read here: it is grepped per editor line, by that line's own area plus the six cross-cutting ones (`rollback · console · batch · compile · transport · visual`). Also read `.unikit/bridges.yaml` (the bridge order) and, when it exists, `.unikit/bridge-routing.md` (the routing rules); a missing order file means the default order `BRIDGES.md` states, a missing routing file means no routing rules.
- For each bridge in `BRIDGES.md`: `.unikit/bridge-notes/<bridge>.md`, **header only** (`bridge:` / `audited:`), compared against that bridge's stamp. A mismatch is one `WARN [bridges] notes header ≠ bridge (<header> ≠ <bridge>)` and nothing else — the entries are suspect, not void, and they still apply. Retiring them is `/unikit-bridge-audit`'s job.
- **Either file absent → skip it and continue with the same rights.** No rules means no known exceptions, never no capabilities: absence never disables an engine bridge and never turns a target into `⏸️ MANUAL` (`dev-principles.md` → **A9**). Say it once: `Bridge rules: <bridge> has no INDEX.md — no known exceptions for it, rights unchanged`.
- **Names never come from a file.** A name to call is chosen from the live catalog of the bridge (**D6**), its schema is requested from the bridge before the first call, and the result is closed by reading the changed state back — a response code is not evidence.

These describe the engine bridges actually configured for this project: their bootstrap protocols, which calls are real, and which report success without doing anything. They override generic assumptions about an engine bridge.

**The session started from a plan whose manifest has `## Experiment Context`, or the prompt carries a `Prototype plan:` note** → read `.unikit/system/prototype-profile.md` and follow its `## Role: quality and the rest` for the conventions above. Missing or unreadable → `WARN [prototype] profile contract missing — conventions applied as for an ordinary plan; run unikit-ai update`.

**Rules Loading.** Before writing code, load the project rules from `.unikit/`:

1. **ALWAYS read** `.unikit/DESCRIPTION.md` — project specification, tech stack, constraints
2. **ALWAYS read** `.unikit/ARCHITECTURE.md` — module boundaries, dependency directions, communication patterns. **Architecture topics:** the root now; load the topic files listed under its `## Topics` whose `Load when` matches this task; when unsure, load. A listed file that is missing → `WARN [architecture] topic file missing: .unikit/architecture/<slug>.md`, continue.
3. **Read `.unikit/memory/code/RULES_INDEX.md`**. Load rules:
   - **RULES.md**: ALWAYS read `.unikit/RULES.md` first (highest priority) **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the current task; when unsure, load.
   - **Core**: read the Core table. For EACH row where Required By = `all` or contains `{{self_name}}` — read that file from `.unikit/memory/code/core/` using the Read tool. Do NOT skip any matching row. Always re-read at skill start, never rely on prior conversation cache
   - **Stack**: load dynamically when the current task or context matches "Load When" column, or when a need arises during work
   - **The one exception to the row rule: `testing.md`.** Read it only when this run writes tests or narrows a run to affected test suites, even though its row says `all`; `references/tests.md` says when.
4. **Read `.unikit/skill-context/{{self_name}}/SKILL.md`** if it exists — project-specific rules accumulated by `/unikit-evolve`. Treat as overrides: skill-context wins over general rules on conflict.

Unless this is the delegate mode, and when `git` is available, run `git status --porcelain` once and remember the paths that already have uncommitted changes — Step 5 names them if this run touches them too.

<!-- unikit:extension-point:bootstrap -->

### Step 2: Build the task card

The card is what you understood the request to be, put in the grammar the planner writes and the executors read. Build it before the first change; Step 3 prints it.

**Plan files.** Unless this is the delegate mode, check — by existence only, with `Glob`, never reading — `.unikit/code/PLAN.md`, `.unikit/code/FIX_PLAN.md` and the folder of `.unikit/code/plans/` that belongs to the current branch (its name is, or ends with `_` or `-` plus, the part of the branch name after the last `/`). For each that exists print `WARN [execute] <path> exists but is ignored: no plan is used` and go on.

**The hand-off carries `Editor:` lines (delegate mode)** → they are the card; take them as written and do not derive them again. Otherwise classify the text.

**Class** — one of four, for the whole request:
- `question` — it asks about the code and changes nothing: answer in a few lines from the rules and the files you read, say that `/unikit-explore` is the skill for a longer discussion, and STOP. No bridge is called, nothing is written, no question is asked.
- `code` — every change is to a source, text or config file: the card lists the files.
- `editor` — every change touches the editor's serialized state: the card carries one `Editor:` line per target.
- `mixed` — both: the `Code:` lines first, then the `Editor:` lines in the order they must happen; a link between objects is a line of its own, after the lines that create them.

**An editor line** is `Editor: [kind] <container> → <target> : <action>` — the grammar of `{{skills_dir}}/unikit-plan/references/TASK-FORMAT.md` → *Editor task grammar*:
- A change is editor work **if and only if** it touches the editor's serialized state (`dev-principles.md` → **A8**). A plain text or config file is not editor work, whatever it configures; source code is always `code`.
- `kind` is one of the six words of **A8**, none other. Two kinds fit → take the default kind of `ENGINE_RULES.md` §1 and say so on the card line.
- What a container and a target are for each kind, and which signs mean editor work, is read from `{{skills_dir}}/unikit-plan/references/ENGINE_RULES.md` — §1 and §3 only — when that file exists. It does not → work from **A8** alone and print `Classification: no ENGINE_RULES.md — A8 only`.
- Look a container or a target up in the project (`Glob`, `Grep`) unless the action creates it. Several matches → ask which, one question, the matches as the options (four at most). No match → the line stays on the card marked `⏸️ MANUAL — not found: <what was looked for>`. The delegate mode asks nothing: several matches also give `⏸️ MANUAL`, with the reason.
- A wish of the text about the bridges or the mode ("only through the command line", "by hand") goes onto the card; it beats the order (**D3**).

### Step 3: Choose the mode and the order of the bridges

**The mode** of the `Editor:` lines:
- the value of `--editor`; in the delegate mode the `Editor tasks:` or `editor_mode:` line of the hand-off (`mcp` is read as `engine-bridge`);
- otherwise `engine-bridge` when `.unikit/system/engine-bridges/BRIDGES.md` lists at least one bridge, else `manual`.

**`direct` is never a default** — it is irreversible. It is chosen only by `--editor=direct` or by words in the description that ask for it plainly ("edit the file directly", "as text, no bridge"). Either way it is one request, carried out by `{{skills_dir}}/{{self_name}}/references/direct-mode.md`, which you read now and not before. In the delegate mode the same reference says when `direct` may run.

**The order of the bridges** is settled once per run by `dev-principles.md` → **D3**: the file read in Step 1, restricted to the bridges `BRIDGES.md` lists, then the other listed bridges in the default order; a word of the user, in the description or later in the session ("only the second bridge", "leave the CLI out"), beats the list. Print `INFO [bridges] order: <a> > <b> (file|default|prompt)` once — and nothing when `BRIDGES.md` lists no bridge. A routing row that applies to the step is announced by the step's own `INFO [bridge-search]` line (D6), not here.

**Print the card** once, as one block; the tokens are never localized, the sentences follow `language.ui`. The delegate mode prints none:

```
Card: <class>
  Code:   <what is written> → <file>
  Editor: [<kind>] <container> → <target> : <action>
Mode: <engine-bridge | manual | direct>
```

### Step 4: Carry out the card

Keep a running list of the files you create, modify or delete: Step 5 stages exactly those.

Work in the phase order of **A5** — `code → compilation → editor → wiring → apply → verify` — and enter a phase only after the previous one is confirmed. **Before the first call through a bridge** — a console read or an editor line — read the part of `dev-principles.md` below the LAZY-READ BOUNDARY, once per session: D3, D6, D7 and D8 live there. `BRIDGES.md` lists no bridge → it is never read.

1. **Code** — the `Code:` lines. Write the files with `Read`, `Edit` and `Write` by the rules loaded in Step 1 and the principles of `dev-principles.md`; read only what the task needs and follow the patterns of the code around it. A `// TODO:` comment you add → invoke `unikit-todo` with the argument `<the TODO text, in the language of language.artifacts>` (`dev-principles.md` → code conventions, point 8); in the delegate mode only name it in the report.
2. **Compilation** — only when you wrote code **and** `BRIDGES.md` lists a bridge. Read the console through the first bridge of the order that can, by **D3** and **D6**: a marker before the change and the delta after it when the bridge offers one, the evidence taken after the editor re-read the files (**A2**). Errors that belong to this run's code → fix them inline, read the console again, repeat until none is left; errors of other code → leave them and name them in the report. No bridge reads the console → the report says `Compilation: not checked — no bridge offers a console read`; it never says the code compiles.
3. **Editor** — the `Editor:` lines in the order of the card, each by the mode:
   - `engine-bridge` — carry out **every** line by `dev-principles.md` → **D6** (route by **D3**). A call that misled you is a finding (**D7**); the rule of the bridge and the library follow **D8**. Name the bridge of every call and of every read-back in the report. No rules file, or no check line for the area, changes nothing (**A9**).
   - `manual` — touch no file for the line: it goes to the report as `⏸️ MANUAL`, in the form `[kind] container → target : action`.
   - `direct` — as `{{skills_dir}}/{{self_name}}/references/direct-mode.md` says (Step 3).
4. **Verify** — read each changed thing back (**A2**), through the same bridge or, stronger, through another one (**D3**). A line with no read-back is NOT CONFIRMED in the report.

**A finding has no plan table to go to** (**D7**): keep it as a candidate line for the report — the `area`, what has to be confirmed, the raw call and the raw answer, and `observed` taken from `Bash(date *)`, never recalled. `.unikit/bridge-notes/<bridge>.md` is never written from here.

**A blocker** — a compilation error you cannot fix, a missing dependency, a requirement that is unclear: stop that line, say what you observed and carry it to the report as not done. Guess nothing; ask only when the answer is a choice between things you found.

**Tests are the user's choice** (`dev-principles.md` item 5): no test is written and no run is started unless the task's words or the user's answer say so. A rule of the project, or a test file beside the source, is no such word. When the description mentions tests or a test run, or this run changed logic or a system value, read `{{skills_dir}}/{{self_name}}/references/tests.md` once, after the last step above, and follow it. Otherwise say nothing about tests and report `Tests: none`. In the delegate mode Step 0 decides and the reference is not read. The file cannot be read → print `WARN [testing] test reference missing — no test is written or run; run unikit-ai update` and report `Tests: none`.

### Step 5: Close the run

Not run in the delegate mode: there the report of 5.3 is the reply and the caller does the rest.

**5.1 Context files.** Update only what the change touched: `.unikit/DESCRIPTION.md` — factual deltas for new dependencies or integrations; `AGENTS.md` — only when new modules, directories or layers were created; `.unikit/ARCHITECTURE.md` — only for a new module, directory, layer, dependency rule or contract, as one table row or list line in the topic file whose `Load when` matches, else in the root section that fits (never a paragraph, a new topic or a moved block); a decision or an explanation is not a delta — print `INFO [architecture] update suggested: <one line>`. `.unikit/ROADMAP.md` and `.unikit/RULES.md` are never edited here. In `.unikit/TODO.md` tick (`- [ ]` → `- [x]`, with `Edit`) every open item the change resolves, matched by meaning; no file or no match → nothing.

**5.2 Documentation**, by `--docs`:
- `yes` — invoke `unikit-docs`.
- `no` — print `WARN [docs] --docs=no: documentation checkpoint skipped`.
- `warn` (the default) — print `WARN [docs] documentation checkpoint skipped (default: warn only); pass --docs=yes to run it`.

**5.3 Report.** One block, in this shape; a line with nothing to say is left out, and no file is written:

```
## Execute Summary

Task: <the description>
Card: <class>

Changed:
- <file> (created | modified | deleted) — <one line>
Editor:
- <[kind] container → target : action> — <bridge> · read back: <the value observed>
Manual (editor targets):
- <[kind] container → target : action> — <the reason>
Not done:
- <the line> — <what was observed>
Compilation: <confirmed through <bridge> | not checked — <reason> | errors of other code: <list>>
Tests: <the report line of references/tests.md | none>
Bridges used: <ids, in the order used>
Search: <the INFO [bridge-search] lines of the calls, and the Docs: and Reference: lines D6 and D8 told you to print>
Documentation: <the outcome of 5.2>
Findings (candidates):
- <area> — <what has to be confirmed> — call: <raw call> — answer: <raw answer> — observed: <date>
Already changed before this run: <files this run changed that had uncommitted changes at the start>
```

**5.4 Findings.** The report holds candidate lines → ask once, with the question tool of your agent (`AskUserQuestion`): `<n> bridge findings from this run. Pass them to the notes of their bridge?` — `Pass them on` / `Leave them in the report`. The first → invoke `unikit-bridge-trap` with no argument: it takes the findings of the session first. No candidate line → say nothing.

**5.5 What next.** Asked only when the running list of Step 4 is not empty and `git` is available. Ask once, with the question tool of your agent (`AskUserQuestion`): `What next?` — `Review first (recommended)`: `/unikit-review`, then `/unikit-commit` · `Commit now`: `/unikit-commit`.

While tests wait for acceptance (`references/tests.md`), `Accept and write the tests (recommended)` comes first and `Review first` loses its mark. Taking it is the user's acceptance: do `## After acceptance`, then ask `What next?` once more without that option. Meanwhile the descriptions of `Review first` and `Commit now` say that the tests stay unwritten.

Before a review or a commit: stage the files of this run and only those — `git add -- <the files of the running list>`, never `git add .` or `git add -A`. A file of the list that had uncommitted changes at the start (Step 1) is named first: `WARN [execute] <file> had uncommitted changes before this run — they are committed with this run's edits`.
- Review first → invoke `unikit-review` with no argument (it reviews the staged changes), wait for it to return, then invoke `unikit-commit` with no argument.
- Commit now → invoke `unikit-commit` with no argument.

Then STOP: there is no summary file and no report file. `/unikit-verify` is not offered — it checks a plan.

## Important Rules

1. **No plan.** `.unikit/code/PLAN.md`, `.unikit/code/FIX_PLAN.md` and `.unikit/code/plans/` are never read, created or edited — the only touch is the existence check of Step 2. No patch is written to `.unikit/code/patches/`, no roadmap milestone is checked, no question about the deletion or the archive of a plan is asked, no PR checkpoint is run.
2. **The skills this skill invokes** are `unikit-commit`, `unikit-review`, `unikit-todo`, `unikit-docs` and `unikit-bridge-trap`, and no other: never `unikit-plan`, `unikit-fix`, `unikit-implement` or `unikit-verify` — a task that needs one of them is not this skill's.
3. **Commit only your own changes** — stage only the files of the running list of Step 4; never `git add .` or `git add -A`.
4. **Tests are the user's choice** — none written and no run started without the task's words or an answer (`references/tests.md`); chosen tests wait for acceptance, and an edit on a result you have handed over gets no new test and no suite run (`dev-principles.md` item 5a).
