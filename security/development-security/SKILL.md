---
name: development-security
description: >-
  Security review of a change's branch, after code integrity. It runs the
  NFDR's dependency audit and answers every advisory, even in dependencies the
  change never touched. It takes an allowed fix (a bump to the fixed release, a renamed
  identifier, a major bump only with the suite green), and for an advisory the product does not reach
  it writes an exception in the product's exception record, creating the first one when there is none
  and using a stated default window when the NFDR names none, with a row in the instance upkeep
  register. It reads the change's code with a lens adapted
  from Anthropic's security review and the OWASP lists, fixes a hole when no record is
  edited, the suite stays green and nothing is redesigned, and reports the rest for the PM to decide on.
  Forbidden moves on what the product reaches are gathered and asked once, at the end. It always writes a committed security report
  whose first line says clean, fixed, reported or stopped. Halts outside a senior-engineer session or
  the senior-engineer subagent.
when_to_use: >-
  Run on a change's branch once its code-integrity step has passed, or when asked for a security review
  of a change unit. Trigger phrases are "security review of the change", "run the security step",
  "audit the dependencies on this branch", "development-security". Do not use for proving code against
  its intent (development-code-integrity), for deciding what to do about what the review left (the
  PM's), for security review of the definition documents, or for sealing a change (tobiishi-seal).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.1.2"
  created: "2026-10-23"
  category: execution
  tags: security, dependencies, advisories, review, senior-engineer, pipeline
  risk: safe
---

# Development Security

## Purpose

Review a change's branch for security before it is sealed, and **repair what may be repaired, report
the rest**:

- **Dependencies.** Every advisory the product's dependency audit reports is answered on the change's
  branch, so the repair reaches `main` at the seal — fixed where the rules allow; excepted where the
  product does not reach it, even when its only fix is forbidden (creating the product's first exception
  record if it has none, under the NFDR's window or a stated default); a question for the owner where
  it is reached and its only fix is forbidden; or reported for the PM where it is reached and has no
  fix.
- **The code.** A hole in the change's code — or one already on `main` that its trace passes through —
  is fixed when the fix edits no ADR and no product record, keeps the suite green, and needs no
  redesign; otherwise it is reported for the PM.
- **Forbidden moves** — a fix that would edit a record, or that a record blocks, on a reached advisory
  or a hole — are gathered while everything else is done, and the run stops once at the end with all
  of them as questions for the owner.

**The PM reads what is left** — unfixed holes, reached advisories with no fix, a dependency audit that
did not run, an exception under the default window or one the audit does not read, anything the review
could not do — and decides what to do with it. This skill does not decide it, and nothing it
leaves holds the seal.

**This file is the orchestrator.** It owns the posture gate, resolving the change's worktrees, the
order of the steps, the suite call, the report's file and verdict line, and the commits. It makes no
security judgment.

**The method is `prompts/rich.md`** — the one body this file points at. Read it in full before Step 2
and apply it, with `<CORE>/prompts/senior_engineer_repair_dependencies.md`, which its dependency half
points at and `dependency-repair` shares. Between them: the edge of a repair, which audit command runs,
the rules a repair is held to (quoted there word for word), the order in which an advisory is answered,
the exception record and the upkeep row, the code half's scope, threat lists, three phases, confidence floor, exclusions and hole fixes,
what every hole carries, how forbidden moves wait for the end, and what the run never does all live
there. None of it is repeated here.

**Announce at start:** "I'm using the development-security skill to review this change's branch for
security."

## Posture

**Senior Engineer only.** Run in a `senior-engineer` session or as the `senior-engineer` subagent.
Invoked from anywhere else, halt at once, say the posture is wrong, and name the way in — open a
session with the `senior-engineer:` prefix, or run the `senior-engineer` subagent. The seat's contract
is `<CORE>/roles/loaders/senior_engineer_global.md`.

The gate is here because the run writes and commits with nobody answering
(`<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to its seat*).

## Input

**The project** — `system/projects/<project>/` — and **the change's key**. Everything else is resolved
from those two.

**A relaunch after a stop** takes up only the questions the last report listed, with the owner's
answers: everything else is already done and committed.

## The work, in order

Do all allowed work first. A forbidden move met in Step 2 or Step 3 is noted as a question and the run
carries on; the stop, if there is one, comes in Step 4.

### 1. Resolve the change

Resolve the change's path contract once, as `development-code-integrity` does:

```sh
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "$WORKTREE" --project <project> --key <key>
```

`$WORKTREE` is the change's instance worktree on branch `<key>`, never the main checkout. The contract
names the `code_worktree` (the product's code — the instance worktree for a product inside the
instance, the product's own worktree for one in its own repo) and the `pipeline_worktree` (the change's
records). Read the product path from `project.md`, and the product's `docs/nfdr.md` under it. A product
with no NFDR is read as one that names no audit, no window and no threat classes.

### 2. The dependencies — `prompts/rich.md` § *Half 1*

1. Find the audit command the NFDR names. **None named** → note it for the report and go to Step 3.
2. Run it in the `code_worktree`, over the whole resolved set, and keep its output. A command that
   cannot run is not a stop: note why for the top of the report and go on to Step 3.
3. Answer every advisory in the shared file's order — *not reached* is decided before *forbidden*. Make the
   fixes and the exceptions in the `code_worktree` — at the record the NFDR's *Advisory exception
   record* line names, or `checks/deps/advisory_exceptions.toml`, creating it when the product has
   none — check that the audit reads that record, and add each
   exception's row to `system/upkeep.md` in the `pipeline_worktree`, creating the register if the
   instance has none.
4. **A major bump** is kept only on a green suite (§ *The suite*).
5. Re-run the audit after the fixes, and keep that output too: the report states what the audit says
   once the repairs are in.
6. Commit (§ *Commit*, the `dependencies` row).

### 3. The code — `prompts/rich.md` § *Half 2*

Read the change's diff in the `code_worktree` — `git -C "<code_worktree>" diff main...HEAD` and every
file it touches — and apply the prompt's three phases and its sceptical pass. Fix each hole within the
edge, each kept only on a green suite (§ *The suite*), and report the rest. Commit the fixes (§ *Commit*,
the `holes` row).

### 4. Write the report, commit, and stop if a question is owed

Write `security-report.md` (§ *The report*) and commit it with any upkeep rows (§ *Commit*, the
`report` row). Where the report lists a question for the owner, the run ends `Security: stopped`.

### The suite

A major bump and a hole fix are each kept only on a green suite run after it. Run the suite through the
gate tool, never by hand: read `<CORE>/prompts/gate_suite.md`, build its evidence file, and issue

```sh invocation
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate code-integrity --inputs "<inputs file>" \
  > "<output file>" 2> "<error file>"
```

The tool has no gate of this step's own; `code-integrity` is the step this one follows, and a gate
other than `seal` changes nothing about how the suite runs. The chain runs this skill as its `security`
step and added no `security` gate to the tool. Copy each `Environment:` line it printed
into the report as a bullet, never as a bare line. A red or refused run means the change it was proving
is undone and reported for the PM.

## The report

Write `system/projects/<project>/journey/tobiishi/<key>/security-report.md` in the
`pipeline_worktree`, beside the change's `code-integrity-report.md`, on every outcome. **Its reader is
the PM**, who decides what to do with whatever it leaves. Use exactly this shape:

```markdown
# Security report

Security: <clean | fixed | reported | stopped>

## Why the run stopped
<stopped on forbidden moves: one question per move — the reached advisory or the hole, the move it
needs, the record that forbids it, and what would be done if allowed. Stopped because the change could
not be resolved: what the resolve call said. Otherwise: none.>

## Left for the PM
<first, when it did not run: "The dependency audit did not run: <why>." Then every hole and advisory
left unfixed, each exception under the default window ("default window used — raise it into the
NFDR"), each exception the audit does not read ("wire the audit to honor the exception record"), and
anything else the review could not do, one line each with where it is detailed below. Otherwise:
none.>

## Dependency audit
<the command, cited to the NFDR line that names it, where it ran, and what it reported before and
after the repairs; or: skipped — the NFDR names no dependency audit; or: did not run — why.>

## Advisories
| Advisory | Dependency | Answer | What was done | Commit |
|---|---|---|---|---|
<one row per advisory: fixed · excepted · question for the owner · reported for the PM; an existing
exception that holds is a row too. "none" when the audit reported none.>

## Exceptions and upkeep rows
<each exception written, renewed or removed: the record and entry, its reason, its window and lapse
date, whether the audit reads the record, and the upkeep row. Say "record created" when the run created
the product's exception record, "default window used" when the NFDR named none, and "register created"
when it created `system/upkeep.md`. Otherwise: none.>

## Holes in the code
<each hole as `prompts/rich.md` § *What every hole carries* lists it, High first, each fixed or
reported for the PM. Otherwise: none — and the threat lists that were applied, so "none found" reads
differently from "never looked".>

## Not checked
<everything the review could not cover and why: an audit that was skipped or could not run, a file it
could not read, a suite that would not run. Otherwise: none.>
```

**The verdict line is bare**, the first line after the title, and takes one of four values,
lower-case, the first that applies:

| Value | When |
|---|---|
| `stopped` | the report lists a question for the owner, or the change could not be resolved |
| `reported` | something is left for the PM: an unfixed hole, a reached advisory with no fix, a dependency audit that did not run or that the NFDR does not name, an exception under the default window, or one the audit does not read |
| `fixed` | the run fixed or excepted something, and nothing is left |
| `clean` | nothing to fix, nothing left |

No heading, bullet, quote or table cell around it: a later reader takes it by its literal prefix.

## When to stop

The run ends `Security: stopped` — after all allowed work is done and committed, with the report
saying why — only when:

- one or more fixes on a reached advisory or a hole need a **forbidden move** (an ADR or a product
  record other than the exception record edited, or a fix a record blocks): every one is a question in
  the report's one list;
- the **change cannot be resolved** — no path contract for the project and key. This one stops at
  once, since nothing else can be done.

An audit that cannot run, a hole that cannot be fixed within the edge, a reached advisory with no fix,
an NFDR that names no audit or no window, an exception the audit does not read, and a missing exception
record or upkeep register are **not** stops: they are reported for the PM, or created, and the verdict
says so. The report's *Why the run stopped* section states the reason for either stop.

## Commit

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables: `<repo>` per commit (below), the files each commit carries, subject and body,
**`--actor senior-engineer`** (name it, never derive it), `--skill development-security`, and the
directional resolved as that file says. Never hand-write `git commit` or a trailer.

| Commit | Lands in | Carries |
|---|---|---|
| `security: <key> — dependencies` | `code_worktree` | the lockfile and pin bumps, the renamed identifiers, and the exception record's entries (or the record created). Only when Step 2 changed anything |
| `security: <key> — holes` | `code_worktree` | the hole fixes. Only when Step 3 fixed anything |
| `security: <key> — report` | `pipeline_worktree` | `security-report.md` and the `system/upkeep.md` rows (or the register created). Every run |

For a product inside the instance the two worktrees are one, and the commits land there in that order.
For a product in its own repo they are two repos, and each commit stages only its own repo's files. All
commit on the change's branch, never on `main`; the seal carries them there.

## Critical rules

- **Fix every advisory the rules allow**, on the change's branch, including one in a dependency the
  change never touched.
- **Fix a hole only within the edge** — no ADR or product record edited, the suite green, no
  redesign — and report the rest for the PM.
- **Except an unreached advisory** with no allowed fix, even when its only fix is forbidden, creating
  the product's first exception record when it has none, under the NFDR's window or the stated
  default, with an upkeep row; where the audit does not read the record, report it for the PM.
- **Never take a forbidden move** — gather every one on a reached advisory or a hole, do all other
  work, then stop once with one question per move.
- **The audit is the NFDR's**; with none named, or one that cannot run, the rest still runs and it is
  reported.
- **The PM decides what to do with what is left**; this skill neither decides it nor holds the seal.
- **Never call a built-in security-review command**; the lens is `prompts/rich.md`, read the same way
  on every provider.
- **Always write and commit `security-report.md`**, with its bare verdict line, on every outcome.
