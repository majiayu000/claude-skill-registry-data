---
name: fix-next
description: Take the top open row from `fli next` (or a named id, or `--pkg <name>`) and carry it from re-probe to closed; a choice it meets is filed as a question the row waits on, or put to the user with `--ask`. Use when asked to fix the next issue.
disable-model-invocation: true
---

# Fix next

The loop from *what is open* to *closed with proof*, run without a person copying a row in. Arguments: none (top row), an `FJS-###` (that row), or `--pkg <name>` (top row of that package), and `--ask` with any of them (step 4).

## 1. Pick

`fli next --json --limit 5`, with `--pkg` forwarded. Take the first entry of `ready` unless an id was named. **Say the id and its title before doing anything else**, so a person watching can redirect before the work starts.

Skip a row another session is plainly working on — its files dirty in `git status` and not yours — and end with status `busy`. Two sessions picking the same top row is the likeliest collision here. **When the arguments say an earlier attempt left those edits, they are yours**: read `git diff` and build on them.

## 2. Brief

**The context this row needs is read by one `Explore` subagent, never in this session.** A package `CLAUDE.md` runs to 160 KB and a hazards skill to 55 KB, and a row needs a few paragraphs of either; read whole here, they cost 70–90k tokens before the first edit. Hand the agent the id, the `ISSUES.md` line and the packages, and ask for a brief of at most 60 lines holding exactly:

- **The row**, verbatim.
- **Rulings and rows it cites** — each `FJS-D###` from `DECISIONS.md` and `FJS-###` from `ISSUES.md` or `ISSUES_ARCHIVE.md`, one line each on what it settles for this fix. A ruling the row leans on is usually where the fix's shape already lives.
- **Hazards that apply** — the matching paragraphs of the realm skill for each package (`.claude/skills/{data,api,ui}-hazards/SKILL.md`, and `bridge-index` if the row crosses a package), found by grepping for the row's files, functions and attributes, quoted in the shortest form that keeps the rule.
- **Where the code is** — `file:line` for the functions involved, and the owner the package's `CLAUDE.md` names for that concern.
- **Whether it still reproduces** — what the agent saw reading the current code, stated as *still present*, *looks fixed* or *unclear*, with the lines that decide it.
- **A red test** — which test file it belongs in, the nearest existing test to copy the setup from, and the assertion that fails today.

**When the arguments carry a `## Pre-brief`** (`fix:loop` builds one by script), it IS the brief: the row, what it cites, where its identifiers are, the tests naming them and the hazard entries naming them are already found, so send no agent. Open a hazard's reference line only when the fix touches that rule; whether it reproduces and the red test are step 3's.

Read a file here only when the brief points at it and the edit needs it, and **read code by `fli outline <file> <name|line>`**: it prints the whole function holding that line, from the comment above it to its last line, in one call. The pre-brief's `→` lines are those calls already written. Bare, `fli outline <file>` lists a file's functions with their line ranges, so a function you cannot name is found by its range rather than by guessed `sed -n` windows.

## 3. Re-probe

**Reproduce the defect before fixing it.** The register drifts toward closed faster than its rows do — a row can be fixed in the tree, or describe a neighboring bug. Write the brief's red test and run it. If it will not go red, stop: the row is wrong or already fixed, and the answer is `fli close <id> --how "<what the probe showed>"` or a corrected row, not a fix.

**A `test.failing` with the row's id in a comment above it is that red test already written** — it passes while the defect lives, so a green suite there is the reproduction, never proof of a fix. The fix turns it red; change it to `test` and it must pass. A `test.failing` that is already red means the row looks fixed — re-probe before closing.

## 4. Stop for a ruling

If the fix adds an option, coins a noun, or picks between two designs, run `decision-rules`. **Where it leaves a genuine choice, the session's job ends at the question**, since a ruling made mid-fix is graded by the code already written. Undo your own edits to source files first, so the tree carries no half-built fix; the red test's assertion goes into the question instead.

**With `--ask`, put the options to the user in the session** and end with `ruling`.

**Otherwise file it, so the row waits and the next row can start:**

```
fli file --sev decision --blocks FJS-### --area <pkg> --title "<the question, one sentence>" --detail "Found fixing FJS-### · [IDEAS/owed-rulings.md](IDEAS/owed-rulings.md)"
```

It answers with a `FJS-D###`. Write the options under a bullet whose lead names that id — in the `## Open questions` of the paper the row cites when that paper argues this, otherwise at the end of `IDEAS/owed-rulings.md`:

```
- **FJS-D### — <the question>?** <what forced it: the code, the red test's assertion>
  - **A** — <a real alternative, grounded in the tree>
  - **B** — <another>
  - **Recommend A** — <why, in one sentence>
```

**When the ruling the row needs is already open**, file nothing: end the row's Detail cell with `` · blocked by `FJS-D###` `` (what `--blocks` writes) and confirm `fli next --json` lists the row under `blocked`. Without that marker the loop reads your `blocked` as `failed` and pays a high-effort session to write it.

`fli decisions --json` then lists it `decidable`. `fli decide` answers it under that id and closes the row, and `fli next` hands the held row back naming the ruling. End with `blocked`.

## 5. Fix and prove

Fix at the owner (Invariant 4). Run the package's own `test` script from its directory, piped through `tail -40`; read further only when the tail shows a failure. Stub the fix once and watch the new test go red, then restore it. A row's `test.failing` marker is removed in the fix, along with its id comment. Then **`fli prove <every file you changed>`**, one call. Name the files, since the tree is shared and a bare `fli prove` proves every session's edits. It runs each drive `fli proves` names for them, starting what each needs first and stopping it after, and ends with one ✓/✗ line per drive, so `| tail -20` keeps the verdict and it never needs a second run. A failure an open row already names says `open: FJS-###` — known before this change; confirm it against HEAD only if the failure looks like yours. A drive an open row's title names is `skipped — open: FJS-###` and runs only when your change touches the drive's own file. **A prove whose every ✗ carries `open:` is finished**: a second run prints the same tags and costs two minutes. It refuses a server port that already answers — report that, rather than starting servers by hand around it. A drive that cannot start is reported, not skipped silently.

**A failure outside your diff that reads as the machine is filed, not fixed.** A test or drive your change does not touch that times out, hangs, fails under the full suite and passes alone, or finds a port taken is load or a leftover process — the loop runs lanes, and other sessions run suites in this tree. File it and go on: `fli find <test name>` first, then `fli file --sev S3 --area <pkg> --title "<file> <what it did> under <where>" --detail "env: <cause>"`, cause one of `port` · `shared db` · `stale process` · `timing` · `real machine` · `network` (`ENV_CAUSES` in `packages/cli/core/next.js`); `fli amend <id> --detail "env: <cause>"` when the row exists. Do not rerun it to see, do not raise its timeout, and do not take it as the fix's failure: the prove is finished once every ✗ carries `open:` or is filed.

**A drive that fails is asked whether it failed before the change, and HEAD is read in a worktree, never written over this one.** The `open:` tag is that register search already done. If a baseline run is still needed, `git worktree add` a HEAD checkout outside the repo and run it there. Copying HEAD's bytes over your files for the length of a drive loses the fix if the run is killed, and shows another session sharing this tree code it did not write.

## 6. Record and close

No change-log entry: history is git (`FJS-D675`). A fix that leaves correct-but-surprising behavior behind adds it to its realm's hazard skill.

```
fli close FJS-### --how "<the cause, the fix, and the test or drive that proves it>"
fli file --sev S3 --area <pkg> --title "<the defect, one sentence>" --detail "<how it was measured · [file](path)>"
```

The How column is the closed row's whole explanation, in the register's own prose voice. `fli file` is for what the fix found and did not fix; it takes the next id and tops that severity's table. `fli find <terms>` first — a defect already filed takes `fli amend <id> --detail` rather than a second row. Finish with `fli done` and clear what it lists **for the files you changed**; it reads the whole tree, so an item from another session's edits gets one sentence saying so and nothing more.

## 7. Report

The id, the cause in one sentence, what proves it, and anything found along the way filed as its own `FJS-###` (`fli file`) rather than folded in. **The last line of the report is exactly `fix-next: <id> <status>`**, status one of `closed`, `blocked` (step 4 filed the question the row now waits on), `ruling` (step 4 under `--ask`), `corrected` (step 3 found the row wrong and rewrote it), `busy` (step 1 found another session on it) or `failed`. `scripts/fix-loop.mjs` reads it: `failed` is retried at higher effort, `busy` and `blocked` go on to the next row, `ruling` ends the loop.

Then end the session. **One row per session**: a second row in the same context carries every file the first one read. A batch is `bun run fix:loop`, which gives each row a fresh session; with `--lanes N` it runs N rows at once, each in its own worktree, and the prompt's `## Lane` section says what that changes.
