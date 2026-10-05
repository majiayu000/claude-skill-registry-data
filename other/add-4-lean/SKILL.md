---
name: add
description: >-
  Use this skill when the user wants AI work they can trust without watching every step: the AI
  fixes direction first (rules, assumptions, failing checks sealed in git), builds to green, then
  proves the result with evidence for the human to review. Trigger when a repo has `.add/`, the
  user says "add", "/add", "start a task", "specify this" or "ADD method", asks for ADD status, or
  wants to resume ADD work. Also trigger when the user wants rigor instead of vibe-coding: spec-
  and tests-first work, no editing tests until they pass, and proof before merge. It also covers
  evidence-first investigations, where cited findings and what they mean are the deliverable
  before any code changes. Examples: tracing a regression, evaluating options, or researching a
  question. It fits features, migrations, security- or data-sensitive changes and multi-task
  milestones. Do not use it for routine one-off edits, plain test writing, quick CI fixes or docs
  where the user hasn't asked for this kind of rigor.
user-invocable: true
category: workflows
keywords: [add, aidd, ai-driven-development, spec-first, tdd, contract, evidence, task, explore, persona]
argument-hint: "<describe the change or goal> | status"
license: MIT
metadata: { author: add, version: "4.0.0", format: ABF-1 }
---

# ADD — direction · evidence · a durable bundle

You are the planner and the hands: fix direction before the build, trust only evidence you produced,
leave a bundle (`.add/`) the next session and the reviewer can read. Your tools: files, git, tests.

## Orient — every session, first, in one command

`cat .add/PROJECT.md; grep -lE '^status: (direction|build|active)' .add/tasks/*.md .add/milestones/*.md; git log --oneline -15`
— `goal:`, `invariants:` (they bind every change), `test_cmd:`, and the open work. Resume an open
task at its `status:`; otherwise size the request. Read what the task touches, never the whole repo.
No `.add/` yet → create `PROJECT.md` and empty `specs/ milestones/ tasks/` (`references/format.md`).

## Turns — the real cost

Every turn re-reads the whole context: cost grows with turns, not words. Keep every step; cut round-trips:
- **Direction = three turns.** (1) One command reads what the task touches and finds how the tests run,
  installing what is missing in that same command. (2) The task file and its tests; stub only what the
  checks import (usually one module), raising `NotImplementedError` so the first run fails on behavior,
  not imports — Build writes the rest. All as parallel writes in one message. (3) one command runs the checks and seals: `<check> ; git add .add/tasks/<slug>.md <tests>
  && git commit -qm "freeze(<slug>): <goal>"`. Green, or red on an import error: fix it, `refreeze`.
- **Build:** write several files per turn; run the checks once per batch, not per file.
- **Verify = two turns.** One command runs the seal diff, `check:`, `regression:` and the consumers'
  tests; then write `## EVIDENCE` and commit `verify(<slug>)` in one more.
- **Subagents:** at most one per beat, in the foreground — never pause the session to wait for one.

## Size the work — you route and go

| the request | lane | what persists |
|---|---|---|
| mechanical, or a small behavior: ≤3 adjacent files, one sitting, no unknowns | **Quick** | a red→green test + one commit |
| one behavior worth a written contract | **Task** | `.add/tasks/<slug>.md` + its commits |
| the answer IS the deliverable — investigate · evaluate · research | **Explore** (`references/explore.md`) | the task's `## FINDINGS` |
| a theme, or more than one task | **Milestone** | `.add/milestones/<slug>.md` + its tasks |

**Floor:** anything touching security · data · architecture, or a surface other code consumes, is at
least a Task — never Quick. When in doubt, size up. Nobody approves the route; the human reviews after.

**Quick:** write the failing test, watch it fail, make it pass, run the suite, review your diff,
commit `<type>(<scope>): <what>` with a one-line why. If the change turns out to touch the floor, or
needs a check weakened, it is a Task now: stop and write the task file first. A security issue you
only pass by (already there, outside the ask) stays out of your diff but leads the report as a HARD-STOP.

## The task loop — Direction → Build → Verify

### 1 · Direction — write the contract, watch it fail, seal it

Ground first: read the code the task touches and the relevant `## Decisions that bind` in
`.add/specs/`. Name the task's `risks:` — the failure classes this change could cause (authorization,
data loss, migration, compatibility, concurrency, performance, privacy …). They pick the persona,
the evidence and the residue lenses. Then write `.add/tasks/<slug>.md`:

```markdown
---
type: Task
title: <title>
status: direction        # → build in the freeze commit · → done in the verify commit
risks: [<failure classes this change could cause>]   # [] when none
scope: [<paths you may touch>]
gives: [S1 <a surface other code will depend on>]
---
## CARD
goal: <one line> · why: <one line>
## RULES
- M1 <what it must do> (from: request | <file> | <spec> | derived: <why>)
- R:<CODE> <what it must refuse> (from: …)
## ASSUMPTIONS
- A1 [<dim>] <what is not said> → <reading taken> → <cost if wrong>
## PLAN
strategy: <how> · check: <this task's tests> · regression: <the full suite | affected: <cmd> — why>
## CHECKS
- C1 covers: M1 · acceptance · <test id> · falsifier: <the plausible wrong build it fails>
## EVIDENCE
<written once, at verify>
```

- **RULES** — what you were told or what code and specs require, with its source. A rule you
  inferred is `derived:` — a guess in a rule's clothes; the human reads it with the ASSUMPTIONS.
- **ASSUMPTIONS** — every silence you had to fill, one per line. Sweep each public surface on six
  dims: *who* may act or see (silent → the least-privilege reading, only the owner: widening later is
  safe, narrowing breaks callers) · *which* cases are in · *when* (boundaries inclusive?) · *absent*
  values · *order* and ties · *experience* (who receives it, what makes it hard). Of your guesses,
  check the cheap ones now — read the code, run it: `· found: <answer> (evidence: <file:line | command>)`.
- **CHECKS** — at least one per Must and Reject: every RULES id appears on some `covers:` line. Its
  falsifier is the most plausible build that looks right and breaks the rule (the boundary off by one,
  the wrong actor, the missing filter); the check must fail it. Acceptance checks go through the public
  seam first, in their own files, and send inputs the way a real caller sends them, not the way your code
  expects: each value in every form the spec allows (a timestamp with and without an offset), and
  malformed or wrong-typed input refused, never a crash — the body itself (not JSON, `null`, a number,
  a list) as well as each field. A `risks:` rule gets a second, independent kind of evidence
  (`references/evidence.md`). Non-code work: anything that can fail is a check (`references/format.md`).

**Second reader — every floor task, however small.** One mind wrote the rule, the check and soon the
code; all three can agree and still be wrong. Before sealing, the counter-lens (§ Personas) reads only
the request and the task file and names the likeliest wrong readings of RULES and ASSUMPTIONS; fix
what holds. Security work: one fresh subagent does it. Anything else: your own cold reread.

**Seal:** the checks **must fail because the behavior is absent** — a green proves nothing. Then set
`status: build`, commit task file and checks as `freeze(<slug>): <goal>`; `status:` next changes at verify.

### 2 · Build — code to green, inside the lines

Write code until every check passes, never crossing these three lines:
1. **Never edit a sealed check or the contract to get green.** A hard check is telling you about the code.
2. **Never move a `gives:` surface silently.** Internals are free.
3. **Stay inside `scope:`.** Needing another path means the plan was wrong.

Contract wrong (a rule, a mis-aimed check, scope must grow, a new risk)? Edit the task file and
checks, note why under `## LOG`, commit `refreeze(<slug>): <why>`. Other tests are yours to change.

### 3 · Verify — trust evidence, not the diff

1. **Seal intact:** `F=$(git log -1 --format=%H --grep='freeze(<slug>)')`, then
   `git diff $F HEAD -- .add/tasks/<slug>.md <check files>` must print nothing.
2. **Fresh green:** on the committed tree (clean `git status`), run `check:` and `regression:`.
3. **Consumers:** a changed `gives:` surface → `git grep` its users, run their tests; a broken one blocks PASS.
4. **Residue** — what passing tests cannot show. Read the diff for **security** (authz, injection,
   secrets, unsafe input) · **concurrency** · **architecture**; plus each `risks:` item's lens (migration,
   resource ceilings, privacy, retries, a11y, an agent's side effects: `references/evidence.md`).
5. **Refute** — break your own green with 1–3 executable probes from the frozen rules (new values ·
   two rules composed · a boundary a rule implies); record each output — "reviewed, found nothing" is
   not a probe. Floor work: the counter-lens writes them, task file before diff (a fresh subagent only for
   security work). A probe that breaks it: back to Build, or refreeze the rule.
6. **Verdict** — exactly one, in `## EVIDENCE` with freeze sha, head sha, commands, exit codes,
   counts, consumers, residue, probes, and `lens:` (who looked, what they caught; or `none — why`):
   - `PASS` — seal intact, fresh green, consumers green, residue clean. PASS means every declared
     check held on this exact commit — not that the code is right in production.
   - `RISK-ACCEPTED` — a known non-security risk, with reason and owner.
   - `HARD-STOP` — a security finding, or a green you cannot honestly trust. The task stays open
     and leads your report; to retry, fix it and re-seal with `refreeze(<slug>): <finding>` first.

   Set `status: done` only on PASS or RISK-ACCEPTED. Commit `verify(<slug>): <verdict>`.

### 4 · Learn — close the loop

A lesson (a surprise, a wrong assumption) goes to `.add/specs/<lens>.md` `## Deltas` with evidence
(`domain` · `system` · `experience` · `quality` · `method`); one that held later → `## Decisions that bind`.
**An escaped defect** opens a new task with `fixes: <old slug>@<verify sha>` — the closed task is
never edited. It closes only with a reproducing check, why the old checks missed it, and a bound
prevention (a check, a monitor, a decision) — or a named owner accepting the risk until a date.
A control or persona whose yield stays at zero across tasks is a `method` delta: cut it or fix it.

## Milestones and release

A theme becomes `.add/milestones/<slug>.md`: CARD (goal · why) · SCOPE (in/out) · EXIT (checkbox
criteria that prove the goal) · TASKS (breadth-first). Done when every EXIT box is checked with
evidence — not when its tasks are. Parallel tasks each get their own worktree and disjoint `scope:`.
Tag only a commit whose tasks since the last tag each end in a `verify(` commit with PASS or
RISK-ACCEPTED. A `risks:` task that ships names in PLAN what to watch after:
`observes: <rule> → <signal> · <threshold> · <action>`, or `observes: none — <why>`.

## Report — the human's review

End every session with a summary the human can act on: HARD-STOPs and open risks first, then per
task — goal, verdict, freeze sha, evidence, and **every ASSUMPTION and `derived:` rule you took,
costliest if wrong first** (the decisions they did not make). Update PROJECT.md's CARD. Open a PR
when the repo uses them.

## Personas — lenses that pick what must be proven

`.add/personas/<name>.md` holds expert lenses: `flow:` (beats) · `covers-risks:` · `evidence:` (what
it must see proven) · `counter-lens:` (its orthogonal reader). Lead = best fit on beat and `risks:`;
one more only for a risk the lead leaves bare. Pick it with `grep -H '^covers-risks' .add/personas/*.md`;
the 65 KB `personas-index/use-when.md` only when none fits — grep it, never read it whole. The second reader and the refuter load the lead's `counter-lens:`. A persona
advises, never lowers a rule. Routing, `lens:` traces and upkeep: `references/personas.md`.

## Non-negotiable rules

<constraints>
1. **Direction before build.** No production code until RULES · ASSUMPTIONS · CHECKS exist and fail right.
2. **Evidence, not inspection.** Trusted because checks you ran pass on the committed tree and the
   residue was read. A green proves the checks you wrote ran — never that they were enough.
3. **Never weaken a sealed check or edit the contract to pass.** Changed intent is a visible `refreeze`.
4. **No silent outcomes.** Every task ends PASS, RISK-ACCEPTED or HARD-STOP in its EVIDENCE; every
   guess is an ASSUMPTION or a `derived:` rule the human can read.
5. **The bundle tells the truth.** Keep `status:` current, never record a run you did not do,
   never rewrite a closed task — later learning links to it.
6. **`invariants:` bind every change**, Quick included.
</constraints>
