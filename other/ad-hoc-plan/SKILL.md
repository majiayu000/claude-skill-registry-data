---
name: ad-hoc-plan
description: >-
  Tech Lead-posture skill that plans a hand-opened 飛び石 Tobiishi end to end, so the chain can
  carry it from the content step, or from implementation when the change publishes no text, onward.
  Takes a quote-checked brief beside the change's change_request.md — confirmed by the owner in a
  session, or the Request itself when unattended — grounds every claim against the repository, opens
  the change's worktree, and writes a stub change_spec.md, a stub change_design.md, and a full
  tl_instruction.md in development-plan's shape, with a report beside the brief. Requires Tech Lead posture and
  halts outside a tech-lead session or the tech-lead subagent. The run itself never interviews — when
  the repository cannot settle something it stops and says what would settle it. Use when a change has been opened by hand
  and should be planned in one pass rather than walked through development-specs, development-design
  and development-plan.
when_to_use: >-
  Trigger phrases — "ad-hoc-plan", "plan this tobiishi", "write the tl_instruction for this change",
  "plan the change I just opened", "spec, design and plan this in one go". It also fires when a
  Tobiishi folder holds only a change_request.md and the ask is to make it ready for implementation.
  Do not use for opening the Tobiishi (tobiishi-open, or by hand), cutting an idea into seeds
  (seeds-from-idea), planning inside a running change pipeline (development-plan), executing a plan
  (development-implementation), or a change whose branch already exists.
license: MIT
metadata:
  author: Eyal Golan
  version: "2.0.0"
  created: "2026-09-11"
  category: planning
  tags: tobiishi, tl_instruction, change_design, change_spec, tech-lead, development
  risk: safe
---

# ad-hoc-plan

## Purpose

A change opened by hand has a `change_request.md` and nothing else. The change pipeline would spend
three stages turning it into a plan — a spec, a design, an instruction, each written by a different
seat.
This skill writes all three in one pass, as one author, so the pipeline can start at the first stage after planning: the Content Editor's `content` step when the
change publishes text, and the stage that writes code when it does not.

What arrives: a project, its one active Tobiishi, and a brief that says what the owner asked beyond
the request — or, unattended, the request alone. What leaves, committed on the change's own branch in its own worktree:

| File | Shape | Who reads it next |
|---|---|---|
| `change_spec.md` | **stub** — § *The stub spec* | `development-code-integrity`, as the behavioural intent behind the plan |
| `change_design.md` | **stub** — § *The stub design* | `development-implementation` Step 1b, which cross-checks the instruction against it |
| `tl_instruction.md` | **full** — planned by the body `development-plan` follows (Step 6) | `development-implementation`, as its primary contract |
| `ad_hoc_plan_report.md` | `templates/report.md` — § *The run's report*; on a stop, committed on `main` instead | the owner, or whoever comes to the change next |

**This file owns the run, not the plan.** How a `tl_instruction.md` is planned and written — the
review, its header, its layout, its task shapes and their exact `#### Implement` markers, its review
notes, its corrections — is `<CORE>/prompts/tech_lead_create_tl_instruction.md`, the planning body `development-plan` follows too.
This run follows it once its stub spec and design are written, so the two skills differ in their
input and nothing else they plan by. The design's shape is
`<CORE>/../skills/architect/.claude/skills/development-design/references/change_design_template.md` (or `.preserving.md`); the
spec's is `<CORE>/../skills/product-owner/.claude/skills/development-specs/references/change_spec_template.md` (or `.preserving.md`).
None of them is restated here. What is this skill's own is the brief, which parts of the spec and
design a stub keeps, and when the run stops.

## Posture

**Tech Lead only.** Run in a `tech-lead:` session or as the `tech-lead` subagent. Invoked from
anywhere else, halt at once, say the posture is wrong, and name the way in.

The gate exists because the run writes and commits with nobody answering part-way through: its
judgment is the seat's, so the seat is checked (`<CORE>/doctrine/setup/authoring_layers.md`
§ *A skill that acts unattended gates to its seat*). The instruction is the Tech Lead's artifact; the
stub spec and design exist so the instruction has what the next stages cross-check it against.

## Inputs

- **The project** `<project>` — the `system/projects/<project>/` folder. Required.
- **The active Tobiishi** — the single `<key>/` folder under
  `system/projects/<project>/journey/tobiishi/` (ignore `trail/`) holding a `change_request.md`. It
  may have been placed by `tobiishi-open` or by hand; either is fine. Its **Request**, **Category**
  and **Behaviour** are read, never set.
- **The brief** — `ad_hoc_plan_brief.md` in the change folder, in the shape of `templates/brief.md`,
  which extends `<CORE>/templates/brief_template.md`. In a session it is required, and § *Writing the
  brief in a session* says how it is made. **Unattended there is none, and the Request is the brief**
  — the owner's call, 2026-10-24: the run plans from `change_request.md` alone, as it always has.
  **A run is unattended when the prompt that invoked it says `unattended`**, as the launcher's does
  (`launcher.md`); a spawning session that cannot put the brief to the owner says so the same way.
  Any other invocation is a session. A brief found in the folder is read either way.
- **The repository as it stands** — every file, symbol, command and count the Request and the brief
  name. **Where the brief and the repository disagree, the repository wins.**
- **`system/projects/<project>/project.md`** — `Product path:`, `Execution type:`, `Test command:`,
  `Languages:`, and `Setup command:`, which Step 4's command runs in the new worktree.
- **The product's decision files, where they exist** — `adr/`, `nfdr.md`, `fdr.md` and the parts
  table of `SDD.md` § 3, under the product's `docs/`. Read, and bound by, exactly as
  `<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Pre-flight — Read decision files* says: optional context, and their absence
  is never an error. The product is in this repository (a relative `Product path:`) or in its own
  (an absolute one); both are planned.

## Writing the brief in a session

**The session drafts the brief and the owner confirms it** — the owner's call, 2026-10-24, the same
way `seeds-from-idea` takes its brief. Write it from `templates/brief.md`, by the rules in
`<CORE>/templates/brief_template.md`'s DRAFTING ONE IN A SESSION block. Before it goes to the owner,
run Step 1's quote check on it (item 6), and fix every line it reports. Once the owner says it stands,
commit it on the main working tree, in the change folder beside `change_request.md`, through the
builder (`<CORE>/doctrine/governance/commit_via_builder.md`): Step 4 forks the branch from that tree's
`HEAD`, and a brief that is not there is not on the branch. That commit is the session's, before the
run begins, and from Step 1 on, the run asks nothing.

## The run's report

**Every run writes `ad_hoc_plan_report.md`, but for the three stops named below**, in the shape of `templates/report.md`, in the change
folder beside the brief — beside `change_request.md` when the Request was the brief. The owner's
call, 2026-10-24: unattended, nobody reads the closing message, and the report is what stays on disk.
The closing message still says what it says.

- **On a plan**, it is written in `$WORKTREE` and committed in Step 8 with the three files, so the
  branch carries it and the seal lands it on `main`.
- **On a stop**, it is written in the main working tree and committed there on its own, through the
  builder, with `--add` naming it alone, `--actor tech-lead`, `--skill ad-hoc-plan`, and a subject of
  `tech-lead: <key> — ad-hoc plan stopped (<the case>)`: a stop before Step 4 has no branch to hold it, and Step 4's
  stop may leave one that is not the run's to keep. A later run of the same change overwrites it, and
  on a plan its branch carries the new one.
- **Three stops write none**, and report in the closing message only — the owner's call, 2026-10-24.
  The wrong posture, and no single active Tobiishi, because there is nothing to write into. And the
  change's branch or worktree already existing (Step 1, item 4), because that branch holds, or will
  hold, the change's own report: a stop report committed on `main` at the same path would collide
  with it when the seal takes `main`'s advance, and would say the change stopped when it is
  planned.

## Workflow

Steps 1–3 read and decide; nothing is written until Step 4, apart from the brief a session commits
before Step 1 and the report a stop commits (§ *The run's report*). **A stop in Steps 1–3 leaves no
worktree, no branch and no file behind but its report, where it writes one.** Step 4's stop — the worktree command or the path tool
refusing — and a stop in Step 6 come after something exists, and report what does (§ *When you stop*).

**The checkout is the instance's main working tree** — the first entry `git worktree list` prints,
the same answer from any linked worktree of it. Step 4's command cuts the branch from that tree's
`HEAD`, so Steps 1 and 2 read that tree and no other.

### Step 1 — Gate, then resolve the change

1. Check the posture (§ *Posture*).
2. Find the active Tobiishi. None → stop. More than one → stop and name every key found; picking one
   would plan a change nobody asked for now.
3. **`change_request.md` is committed on the main working tree.** The change's branch forks from its `HEAD`
   (`<CORE>/tools/create_change_worktree.py`, which Step 4 runs), and `tobiishi-seal` Step 1
   refuses to seal a branch where the file is missing. Check `git ls-files --error-unmatch` on it
   and that `git status --porcelain` shows it clean; if not, stop and say so — committing the
   opener's file is the opener's move. The same holds for `ad_hoc_plan_brief.md` where one is
   there.
4. **The change has not entered the pipeline.** If branch `<key>` or `.worktrees/<key>` already
   exists — in this repository, or in the repository holding an absolute `Product path:` — stop: this
   skill plans a fresh change, and Step 4's command would refuse anyway.
5. **Read the classification; do not make it.** `Category` and `Behaviour` come from
   `change_request.md` and are validated against the closed vocabulary in
   `<CORE>/doctrine/flow/change_classification.md`. Missing, out of vocabulary, `refactor` with
   `changing`, or `feature` with `preserving` → stop. Classification is set at entry, by whoever opened the change, and every later
   file copies it verbatim.
6. **Read the brief, and check its quotes before anything else is read.** In a session with no
   brief in the folder, write one now, as § *Writing the brief in a session* says, and begin Step 1
   again once it is committed. Unattended with none, the Request is the brief; skip to Step 2.
   Otherwise run

       python3 <CORE>/tools/check_brief_quotes.py <brief> --root "$(git rev-parse --show-toplevel)"

   It prints one line per citation whose quote is not at its lines, and ends with a count on stderr
   of the citations it checked and the ones it skipped as unresolvable. **Any line it prints before
   that count stops the run**, and so does a skipped citation naming a file in this
   instance — the root was wrong, and nothing was checked. Only a citation into another repository,
   such as an external product, may stay skipped. A brief whose `## The ask` is empty or `none`
   stops the run the same way: it was never finished. So does a `## The change` that names another
   project or key than the folder the brief sits in.

### Step 2 — Ground every claim

Resolve the product for reading on the main working tree, which holds what the branch will fork
from (for a product in its own repository, its checkout at `Product path:`): `PROJECT_DOCS` = `<Product path>/docs` and `PROJECT_ROOT` = its parent, a relative
`Product path:` resolving from the instance root and an absolute one read as written
(`development-specs` Step 1). Read the decision files that exist, as
`<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Pre-flight — Read decision files* says.

Then open everything the Request and the brief name, and resolve each claim the way
`<CORE>/prompts/principal_pm_cut_seeds.md` § *Ground every claim before you cut — holds, holds
smaller, does not hold* resolves an idea's, with "the plan" in place of "the seed". **The plan asks for nothing the
Request, the brief's `## The ask` and its `## Rulings` do not**: its scope and its rules or
invariants rest on them, while the picks Step 3 makes for itself stay its own and are recorded. What
the brief's `## Evidence` marks `(session's)` may point the run at a file, and grounds nothing it
writes. A new thing the owner asked
for stays new, rather than becoming a change to something the owner did not name. Each claim is:

- **It holds** → plan against it.
- **It holds smaller** → plan the smaller thing, and record the measurement and the divergence in the
  spec's `## Locked Answers`.
- **It does not hold** → stop.

A claim about what a command *decides* is verified by running the command, never by reading it — the
reason, and how such a run is made, are `development-specs` Step 6, *Claims about existing code (both
modes)*. Where it holds smaller, `## Locked Answers` records the run.

### Step 3 — Decide the change as one decision

The spec and the design are two views of one decision, and this run makes it once; Step 6 cuts the
tasks from them. Settle, in this order:

1. **One change.** If removing part of the request would leave a shippable, independently testable
   change, it is two changes → stop.
2. **What is observable** — the rules (changing) or the invariants and structural goal (preserving),
   at the altitude `development-specs` Step 5 holds a spec to. Rule identifiers continue the project's
   `CP-<n>` series, per that step's *The series belongs to the project, not to the change*.
   A direction the request leaves open is picked conservatively where the pick is reversible, and
   recorded in `## Locked Answers`; where no safe default exists → stop.
3. **Where it lands** — blast radius, sub-jobs, build order, a hint only where the approach is
   non-obvious, and the tests each sub-job adds. Each new piece of logic goes in the part that owns
   it, by the placement row of `<CORE>/prompts/tech_lead_create_tl_instruction.md` Step 2. Where `nfdr.md § 1.2` fixes the module set, it binds:
   a change that needs a module the set does not have → stop, since that decision belongs to the
   records' owner. Where no records exist, the design's module boundaries are this run's to decide.

**Too thin to plan** — the request and the brief together do not say what a task would verify, and the
repository does not either → stop. Never write a plan around the gap.

### Step 4 — Open the worktree

Run the command `development-specs` Step 4 runs, with the main checkout's top level, the project and
the key:

```bash
python3 "<CORE>/tools/create_change_worktree.py" \
  --instance "$(git rev-parse --show-toplevel)" --project <project> --key <key>
```

It creates branch `<key>` and the instance worktree, and for a product in its own repository a second
worktree there on the same key. `$WORKTREE` is the `worktree` of the `repos` entry whose `role` is
`instance`, taken as printed. A non-zero exit is a stop: report the command's `error`, `message`,
`changed` and `repos` as printed, and do not retry or create anything by hand.

From here on `$WORKTREE` is the working root. Resolve `PROJECT_DOCS` and `PROJECT_ROOT` exactly as
`<CORE>/prompts/tech_lead_create_tl_instruction.md` § *Resolve the product* does: the path tool's contract, never a path composed by hand, so an external product's
docs and code are read in its product worktree. Every file below is written under
`$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`.

### Step 5 — Write the stub spec and design

In order: spec, design. **They are stubs**: they exist so the chain enters past the steps that would
write them, and so Step 6 and the stages after it have the input they read. They hold no more. The
chain does not audit them — `development-specs` and `development-design` did not run — and knows them
by their `**Planned by:** ad-hoc-plan` line (`<CORE>/tools/chain_development.py`
`DiskReader.stubbed`), so that line is never left out. The owner's call, 2026-10-24.

#### The stub spec

`change_spec.md`, from the spec template for the change's `Behaviour`. Keep:

- **the header** — `Date`, `Category`, `Behaviour` and `Request` exactly as the template lays them
  out, the two labels copied verbatim from `change_request.md`, then one line more:
  `**Planned by:** ad-hoc-plan — stub spec; development-specs did not run on this change.` and
  `**Brief:** <its repo-relative path>`, or `**Brief:** none — the Request is the brief.`;
- `## Change Summary`;
- `## Rules` with their `CP-<n>` identifiers (changing), or `## Invariants` and `## Structural Goal`
  (preserving);
- `## Out of Scope` — always, at least one boundary, the brief's `## Out` first;
- `## Locked Answers` — whenever the spec went beyond the request, a claim held smaller, or the
  brief carries a ruling: each of its `## Rulings` is one line here, quoted.

#### The stub design

`change_design.md`, from the design template for the change's `Behaviour`. **Short, not
missing:** keep every section the template has, and write each as briefly as the change allows.
`development-implementation` Step 1b cross-checks the instruction against §3, §4 and §5, so a section it looks for must be there to find.

- the header, `Category` and `Behaviour` copied verbatim from the spec, and the `Publishes text:` line on
  the line after `Behaviour:`, **decided by this run** from the spec: `yes — <the places the words live>`
  when the change puts text in front of a person to read, `no` otherwise, and always `no` for a
  `Behaviour: preserving` change (the rule is `development-design`'s Step 6). The chain reads its first
  word, which must be exactly `yes` or `no`. Below it in the header:
  `**Planned by:** ad-hoc-plan — stub design; development-design did not run on this change.`;
- §1–§5 (§3 omitted when one module is affected, as the template says);
- `## Records this change makes false` — always, its zero form naming what was read.

### Step 6 — Plan

Follow `<CORE>/prompts/tech_lead_create_tl_instruction.md` from § *Pre-flight — Read decision files* through its Step 3, with
the spec and design Step 5 wrote as its input: the same pass `development-plan` makes over the
pipeline's. After the plan header's `**Scope:**` line, one line more:
`**Planned by:** ad-hoc-plan — development-plan did not run on this change; written to its rules.`
That body's Step 4 commit is Step 8's.

### Step 7 — Check the stub files

Before committing, read the spec and design as the stages after this one will:

- **Headers.** `Category` and `Behaviour` read the same in all three files and in `change_request.md`,
  each file carries its `**Planned by:** ad-hoc-plan` line, and
  `change_design.md` carries a `Publishes text:` line whose first word is exactly `yes` or `no`, with a
  `yes` naming its places.

A miss here is this run's own output, so fix it in place and check again.

Then write `ad_hoc_plan_report.md` in the change folder under `$WORKTREE` (§ *The run's report*), so
Step 8's commit carries it.

### Step 8 — Commit

One commit on the change branch, by `<CORE>/prompts/tech_lead_create_tl_instruction.md` Step 4, with `--add` naming the three
files and `ad_hoc_plan_report.md` by **repo-relative** path; `--skill ad-hoc-plan`; a
subject of `tech-lead: <key> — ad-hoc plan (spec, design, instruction, report)`; and the directional
`<CORE>/doctrine/governance/commit_via_builder.md` item 6 resolves for a project artifact. Never hand-write `git commit` or a trailer.

### Step 9 — Close

Report the key, the worktree, the three files and the report by path, and name the next move. **Do not run it**
— running the pipeline is the owner's call, as it is after `tobiishi-open`.

The next move is the chain, with no entry argument and no key:

```
<CORE>/launchers/chain-development/launcher.sh <project>
```

The chain takes the project's single active Tobiishi and enters at the first step whose artifact is
missing on the branch (`<CORE>/tools/chain_development.py` `DiskReader.is_done` and
`DiskReader.entry_step`, cited by name because their lines move). With `change_spec.md`,
`change_design.md` and `tl_instruction.md` committed on branch `<key>`, that is:

- **`content`** when the design's `Publishes text:` line reads `yes`, so the Content Editor writes
  `change_text.md` before any code, and the Developer places that text;
- **`implementation`** when it reads `no`, because the engine passes the `content` step with no launch.

This is the entry `chain_development.py --describe` prints as `entry=` for such a change. The worktree
this run opened is entered, not re-created. Code-integrity, security and the
seal run as usual. The audit runs on the plan, the implementation and, when the change publishes
text, its text; the chain leaves out the stub spec and design (Step 5).

## When you stop

**You stop the moment the plan needs a decision the repository cannot make.** The run never
interviews: it does not ask part-way, does not park an item for later, and does not plan around the
gap. A stop reports which case fired, the file or claim that fired it, the check that produced the
verdict, and what would settle it, in the report file and in the closing message (§ *The run's
report*) — then halts.

| Case | Fired at |
|---|---|
| Wrong posture | Step 1 |
| No active Tobiishi, or more than one | Step 1 |
| `change_request.md` uncommitted, or the brief beside it | Step 1 |
| A brief whose quote is not at its lines, whose ask is empty, or whose change is another folder's | Step 1 |
| Branch or worktree `<key>` already exists | Step 1 |
| Classification missing, out of vocabulary, `refactor` + `changing`, or `feature` + `preserving` | Step 1 |
| A claim the plan rests on does not hold, or cannot be reached | Step 2 |
| Two changes in one request | Step 3 |
| An open direction with no safe default | Step 3 |
| A module the records' module set does not have | Step 3 |
| Too thin to plan | Step 3 |
| The worktree command refuses, or the path tool cannot resolve the product | Step 4 |
| A task that fits no sanctioned shape, or any other stop the shared planning body names | Step 6 |

**Step 4's stop is the one that can leave something behind.** The command checks every repository
before it changes any, so a refusal in those checks leaves nothing. A refusal once it has started
changing things — writing the local exclude, adding a worktree, confirming the result, running the
setup command, checking the test interpreter — can leave a branch or a worktree, in one repository
or both, and its `changed` and `repos` say what exists. The path tool refusing comes after the
worktrees exist, so it leaves them too. Report what exists as the command printed it.

**A stop in Step 6 leaves the worktrees and the stub spec and design in them, uncommitted.** The
shared planning body's own stops fire there. Report them as they are; a re-run stops at Step 1
item 4 until the owner removes the branch and its worktrees.

## Critical Rules

- **Tech Lead posture, or halt.**
- **Nothing is written before Step 4, and every stop but Step 4's and Step 6's comes before it.** The
  exceptions are the brief, which a session commits on `main` before Step 1, and a stop's report.
- **It invokes no other skill.** Other skills' files are read for their rules; the worktree is
  opened by `create_change_worktree.py` and the product resolved by `development_path.py`, the
  programs the chain uses.
- **The shapes are the pipeline's.** The instruction is planned by the body `development-plan` follows, exact but for its `Planned by` line; the stub
  files are that stage's templates with the parts named in Step 5 kept. Never invent a section, a
  marker or a gate subsection.
- **Classification is copied, never decided.**
- **The brief is the owner's words.** The plan grounds nothing in what the session added; unattended,
  the Request stands in for it.
- **The repository wins.** Every claim is opened before it is planned against; one that holds smaller
  is planned smaller and recorded; one that does not hold stops the run.
- **The plan is planned like any other.** Step 6 is the shared planning body, reading the stubs as
  `development-plan` reads the pipeline's, and a divergence from them is logged as that body says.
- **The change arc is on the branch.** Every file is written under `$WORKTREE` and committed with
  `git -C "$WORKTREE"`, never on `main` — the session's brief and a stop's report excepted.
- **Existing skills are read, never edited.** This skill writes three files and a report in one
  change folder, and in a session the brief beside them, and touches nothing else.
- **The pipeline is the owner's to run.** Report the launcher command; do not run it.
