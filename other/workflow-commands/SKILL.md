---
name: workflow-commands
description: Procedures for `kickoff`, `fullrun`, `halfrun`, `prrun`, `backlogrun` (with or without `#N` / `new`). Read it before running, explaining, resuming or repairing one.
---

# Issue-driven workflow commands

Each rule is stated once, in the file its row names.

## 0. The rule that fires before any of them — explicit invocation

Its single source is `CLAUDE.md` → "Explicit invocation required (MANDATORY)", resident because it
holds when this skill is not loaded. **A session cut inside a declared budget is not a new invocation — for `backlogrun`
alone**: `backlogrun-steps.md` → "The session cut is inside the invocation".

**Consultation main-session scope and implementation handoff follow
`prompts/collaboration-workflow/principles.md` → "consult-vs-execute".** A keyword selects the
existing procedure below; it does not turn the consultation main session into an implementation lane.

Instruction to file there → `pnpm josh run:handoff kickoff new --brief-file .josh/tmp/brief.md` (`CLAUDE.md` → "Explicit invocation required (MANDATORY)").

## 1. Which file to read

Read this file, then the files the typed command's row names. A command file is a **manifest** of
terse triggers and pointers; `pnpm josh run:step <N>` prints the run's next single action and the
section that governs it; a section it prints is not fetched again.

| Typed keyword                            | Read                                        |
| ---------------------------------------- | ------------------------------------------- |
| `kickoff` / `kickoff #N` / `kickoff new` | `kickoff.md`                                |
| `fullrun` / `fullrun #N` / `fullrun new` | `fullrun.md` + `entry-sequence.md`          |
| `halfrun` / `halfrun #N` / `halfrun new` | `halfrun.md` + `entry-sequence.md`          |
| `prrun` / `prrun #N` / `prrun new`       | `prrun.md` — the difference over `fullrun.md`, read with it and `entry-sequence.md` |
| `backlogrun` / `backlogrun #N…` / `backlogrun #E…` | `backlogrun.md` — its dispatched child reads `fullrun.md` + `split-assessment.md` in its own unit, not the parent at entry |

`entry-sequence.md` holds the entry sequence and stop branches `fullrun`, `halfrun` and `prrun` share;
each manifest carries only its difference. `split-assessment.md` → "The question" is printed by
`pnpm josh run:entry` at the entry, its split-handling detail read only when a split is found.

### The fetch is one `Read` call per file

**Fetch each file above with one `Read` call of its own — never `cat`, never two in one command.**
`pnpm josh doc:read <file>` is the cap-safe whole-file read.

### Four documents are read at the point of use, not at the entry

**`followup.md`, `latest-gate.md`, `chain-rule.md` and `background-commands.md` are not entry reads.**
Each is fetched at its named scope, in the same turn, by the named command that has to obey it:

| Document                | Read it when                                                                   |
| ----------------------- | ------------------------------------------------------------------------------ |
| `latest-gate.md`        | `run:prep` answers `latest: required` — before `josh latest:if-required` runs  |
| `followup.md` → "Run `pnpm josh followup`" | Never fetched: `pnpm josh followup` prints it as it starts, once per session — none in a followup any `josh ship` runs, a repeat names the section in one line |
| `chain-rule.md` → "Run the review-to-merge chain" | Before the first `pnpm josh gate` launch (`fullrun` / `prrun` / `backlogrun`), never fetched: `run:step` prints it at `implement`, `run:review` (which launches the gate) and `ship` once per session — a lane child gets "A lane child" alone, a repeat names the section in one line |
| `background-commands.md` → "Background the gate and push" | Before backgrounding `pnpm josh gate` — the first long-running command a run detaches (`fullrun` / `halfrun` / `prrun` / `backlogrun`) |

A `latest: skip` answer reads nothing. **A lane child that parks reads
`backlogrun-park.md` → "park and continue" at that point of use**, and **every implementing run starts
`pnpm josh run:progress --wait` once its hold is claimed** — `progress-watcher.md` → "Progress while
the run is quiet" is never fetched: `run:entry` prints it.

### A section reference is read as a section

**A pointer written `` `X.md` → "Heading" `` is read as that section, never by opening `X.md` whole:**

```bash
pnpm josh doc:section <file.md> "<heading>"   # the section, verbatim
pnpm josh read:set [<keyword>]                # what an entry reads, and what it costs
```

## 2. What every one of them shares

Each shared rule is a **trigger, a one-line action, and the single source** read at that trigger.

| Trigger | Action | Single source |
| --- | --- | --- |
| Consultation main (Fable / Astra), excluding lane and `run:handoff` children | `pnpm josh run:handoff <keyword> … --brief-file .josh/tmp/brief.md`; an instruction to file → `kickoff new` | `docs/josh-commands-board.md` → "josh run:handoff" |
| A file passed as a `*-file` argument (body, plan, brief, rationale, human-steps, review note) | Write it under `.josh/tmp/` | `prompts/collaboration-workflow/shell-body.md` → "安全な書き方" |
| First call of any entry | `#N`: `pnpm josh run:entry <N> --to <command>` (claims the tree, except `kickoff`); `new` (not `kickoff`): `pnpm josh run:hold`; `busy` / `unknown` stop | `working-tree-hold.md` |
| `run:entry` prints its stage line | The command sets how far a run goes, the Issue where it starts; **`start: reached` redoes nothing** — stop (at `merged`, the next line answers) | `docs/how-to/run-issues.md` |
| Same turn as the hold (not a dispatched child, not `kickoff`) | `pnpm josh cost --cut`; `under` continues, `over` stops — `run:entry` notifies and runs `run:release` (`new`: `--adopt`) | `backlogrun-progress.md` → "The hand-off" (model-priced threshold) |
| An entry typed with an `owner/repo#` prefix or a short `repo#` name | Resolve the target and its checkout; an explicit foreign owner stops the run | `target-repository.md` |
| A `new` entry typed with an `into <target>` suffix | Insert the artifact into the named epic with `pnpm josh epic --add <E> <N>` | `into-target.md` |
| Before any work starts (every entry) | The split assessment; the default is not to split — separability **and** a scope over the size guide must hold together; a `fullrun` / `halfrun` that finds a split files the epic and **stops** | `split-assessment.md` → "The question" |
| Before implementing (every implementing entry) | `pnpm josh run:prep <N>` (`run:entry` bundles it; `kickoff` reads `pnpm josh issue:read <N>`) — the body and the comments; the later of a body and a comment wins | `issue-comments.md` |
| `run:prep` answers `human_review: yes` | Implement and gate, run `pnpm josh test:e2e`, then stop before the commit with `pnpm josh run:hold <N> --human-review-stop`; the label is applied only by a person | `needs-human-review.md` |
| `run:prep` answers `latest: required` | `pnpm josh latest:if-required` — it prints the `dependency-update` check | `latest-gate.md` (read whole, only on `required`) |
| Before delegating any run step | `pnpm josh delegate <step>` decides eligibility, never you | `delegation.md` |
| The pre-implementation reading reaches 3 unedited files | Delegate the unread investigation; a file this run will edit is read in the main line | `delegation.md` → "The pre-implementation reading" |
| Immediately before implementation | Present the two-layer work summary (once per Issue); `kickoff` posts a plan instead | `prompts/collaboration-workflow/report-format.md` |
| While implementing | Re-run one check by name, not the whole gate — `pnpm josh lint:related`, `pnpm josh cspell:dot`, `pnpm josh test:related` (`--touched` in a lane; `check:related` is full reach); `pnpm josh review:brief` refuses a brief on a tree the last two were not green on | `chain-rule.md` |
| Implementation is done | Refactor → `main:merge` (no lane child) → `pnpm josh gate`, then (green) a subagent `/code-review` → round cap → PR → merge | `chain-rule.md` → "Run the review-to-merge chain" |
| A review has run | Its verdict counts only once `pnpm josh review:attest --check` answers `ok`; `missing` / `mismatch` are refusals `pnpm josh followup` blocks the merge on | `chain-rule.md` → "The brief names the checkout, and a review that read another one is refused" |
| A command can take minutes | Issue it in the background; the turn never ends at the push (`pnpm josh followup` stays foreground) | `background-commands.md` → "Background the gate and push" |
| E2E gate | The CI E2E job where the command ends in a PR (`fullrun` / `prrun` / `backlogrun`, enforced by `pnpm josh followup`); you run `pnpm josh test:e2e` yourself where it does not (`halfrun`) | `prompts/testing-guide.md` → "Closing the E2E gate without a human run" |
| Filing any new Issue | `pnpm josh issue:file` — it runs the `issue:scout` scan; read its duplicate and epic answers | `issue-scout.md` |
| Another Issue here must land first | A prerequisite is a dependency, not a park — file it, stash, record the dependency; `fullrun` / `halfrun` stop, `backlogrun` continues | `prerequisite.md` |
| Something worth filing, none of the three | Unattended: file it (Tier A, first-party); else ask; a delegated child returns it to the parent instead | `observation-filing.md` |
| A defect in kit's own verification turns up | It runs alone when all three conditions hold; a batch resumes once it merges | `backlogrun-lanes.md` → "A solo run" |
| Under `backlogrun`, a stop that would end a batch, or a named non-epic item | Park one child and continue; run a named non-epic item as a `fullrun` | `backlogrun-park.md` → "park and continue"; `backlogrun-child.md` → "When `#N` is not an epic" |
| `backlogrun`'s authorization | The whole `auto-ok` opted-in pool as well as its named items; `pnpm josh backlog:next` offers them | `backlogrun.md` |
| `run:step` prints the retrospective step (a run drained its backlog and stopped, not a lane child) | Run what it prints once, file 0–2 improvements, then `pnpm josh run:carry --retrospective` | `retrospective.md` |
| Any artifact prose (Issue bodies, comments, Telegram) | Session language (`JOSH_SESSION_LANG`, default `ja`); Issue/PR titles stay English | `prompts/collaboration-workflow/overview.md` |
| Any mid-workflow stop | `stop:guard` sends the `confirmation` Telegram; on its refusal, send it | `rule-delivery.md` → "stop-notify" |

## 3. What stays resident, and what is read from here

**The residency criterion is `prompts/collaboration-workflow/residency.md`, its single source — read
only when a rule is placed, moved or retired, never during a run.** Its questions — question 0
(`pnpm josh oracle:list`), the ordering question (`pnpm josh run:step`), the first and the second —
are asked there in order; none is restated here.
