---
name: plan
description: use when user asks to write a plan or says "chat plan"/"md plan"/"linear plan"
---

<instructions>

plan location:

- user asks for a chat plan -> output the plan in chat
- user asks for a md plan -> put the plan in the `plans/` directory
- otherwise -> create the plan as a linear issue

before writing:

- explore the repo first
- eliminate uncertainty by verifying (rails runner, prod reads, repro), then record the conclusion, not the investigation
- sketch the seams the work will be tested at (`/codebase-design` vocabulary): prefer existing seams; place new ones at the highest point possible; the fewer seams, the better - the ideal number is 1. a new seam is unresolved-question material
- use the domain vocabulary from `GLOSSARY.md`

helpers and prototypes:

- read and follow [/helper-sub-agents](../helper-sub-agents/SKILL.md), with output under `playground/plans/<slug>/helpers/` and at most 5 at once. spawn helpers wherever they save your context or time, e.g. research, reading, data analysis, prototypes. do small things yourself when spawning would cost more than it saves
- prototype proactively wherever trying something answers a question the plan depends on better than reading can, e.g. a backend flow, a library install, a state model
- each prototype gets its own helper in its own worktree. that helper is the exception that commits and pushes, to its own throwaway branch only. link the branch from the plan next to the decision it settled
- multi-variant UI prototypes (the UI branch of `/prototype`) only when the user asks

structure:

- 'tl;dr' must stand alone: it gives the full picture of the change without reading further
- 'tl;dr' may repeat facts from the body. below it, each fact lives in exactly 1 place - a PR's contract is its expected behaviour, so state behaviour there and nowhere else
- use <plan-template> as the format source; existing plans may deviate, don't read them

depth is earned:

- go deep only where the answer is non-obvious and a mistake is expensive:
  - traps where the obvious approach is wrong, with the evidence that proves them (runner output, repro, prod query)
  - prod measurements that picked a design
  - ordering and irreversibility constraints: deploy order, revert order, data that can't be reconstructed
  - invariants nothing in the code enforces
- everything else gets 1 line or nothing: assume routine tests and commands like `pnpm lint`; a competent agent installs deps, adds routes and writes the obvious tests unprompted

durability - plans outlive the code they describe, so state decisions in terms that survive implementation:

- name modules and their interfaces, not file paths - paths go stale fast, and the implementer will find them
- describe schema changes as the changed tables/columns with their types, not as migration code
- code belongs in the plan only where its exact form is the contract, or a prototype/verification produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape) - trim to the decision-rich parts
- also allow short annotated call trees when they explain a non-obvious flow across UI, API, service and job boundaries - show changed calls and boundaries rather than every function

misc:

- the plan will be executed by an ai coding agent, so eliminate the need for human input where possible
- add a staging deploy only when a verification can't run locally (real provider callbacks, prod-like infra or data volume); then deploy to staging and do those verifications there (as many times as needed)
- supporting material (research dossiers, measurements, prototypes) must outlive this worktree: push it to a separate branch and link that branch. `playground/` is gitignored and worktree-local, so never link it
- the plan can reference un-gitignored files, PRs, branches, links. the plan must not reference chat history
- before writing the file, prune: delete every line whose removal changes nothing the implementer builds or the reviewer checks
- use `/git` skill

PRs:

- split work into PRs depending on the complexity/risk/size
- each PR is a tracer bullet: a narrow but complete vertical path through every layer it touches (schema, API, UI, tests), demoable or verifiable on its own, sized to fit a single fresh context window
- prefactor first: when a preparatory reshape makes the implementation easier, make it the first PR - "make the change easy, then make the easy change"
- wide refactors are the exception to tracer bullets: 1 mechanical change whose blast radius fans across the codebase (rename a column, retype a shared symbol) can't land green as 1 slice. sequence it as expand-contract: expand (add the new form beside the old), migrate call sites in batches sized by blast radius (each batch its own PR blocked by the expand), contract (delete the old form once no caller remains, blocked by every batch)
- edge cases: only traps a competent implementer could plausibly miss; "none beyond existing behaviour" is valid only for mechanical changes

linear plans (default):

- 1 backlog issue carries the whole plan, even when it has multiple PRs
- use [linear-project-map](../linear-project-map/SKILL.md) to select and verify exactly 1 project and any applicable request and group-company labels before creating the issue
- create the issue with only these fields: `team` (the workspace team), `title` = the plan title, `description` = the plan with the `# [title]` heading removed, `state: "Backlog"`, `assignee` = the current user, `project` = the selected project id, `labels` = the applicable verified labels when present
- if a user provided a relevant issue, add `relatedTo` = the user-provided issues, and their sub-issues, that the plan delivers any part of. don't search linear for related issues
- no cycle or parent
- after creating the issue, append its id to every PR title in it. example: "feat: add red button (ARI-123)"

"md plan":

- path: `plans/yyyy-mm-dd-title-plan.md`
- `yyyy-mm-dd` is today's date
- end with `-plan.md`

</instructions>

<plan-template>

# [title]

created: yyyy-mm-dd
edited: yyyy-mm-dd
x PRs

## tl;dr

[15 lines max of plain prose readable in 1 pass - no dense fragments, no vocabulary coined further down]
[problem in 1-2 sentences from the user's perspective, with the measured number]
[the solution and its shape - most of the section]
[1 line: exclusions a reader would otherwise assume are included]
[overall risk]
[total est. code diff]

## user stories

[numbered, each "as a <actor>, i want <feature>, so that <benefit>"]
[cover every aspect of the feature - the implementer reads them as acceptance criteria]
[write "none - mechanical change" for refactors and plumbing rather than omitting the section]

## unresolved questions

[multiple-choice questions (with 1 recommended answer) that can't be answered with code and terminal]
[keep all questions in this section; for each, explain the recommended answer, the tradeoff and the consequence of choosing differently]
[candidates: a new seam, PR granularity (too coarse/too fine), blocking edges]
[write "none" rather than omitting the section]

## rollout

- pr1 -> pr3
- pr2 -> run `bin/backfill-x` on prod -> pr3

[the list above is the format: 1 line per parallel track, `->` for blocking edges - stacked PRs and inline non-PR actions]
[a PR named in 2+ tracks starts only when every track reaching it is done; a PR with nothing pointing at it can start immediately]
[staging and production deployments are manual; show a deployment only when a later step depends on it (a migration or backfill before the next PR, a staging check that can't run locally); merging and deploying to prod at the end is not a rollout step]

## current behaviour

[only surprises: behaviour an implementer reading the code would still get wrong - dual-purpose columns, races, dead guards - each with its evidence]
[the implementer will read the code; skip file tours]

## out-of-scope

[rejected alternatives, each with a 1-clause reason]

## implementation decisions

[only what the PR sections can't carry: modules built/modified and their interfaces, schema changes (tables/columns with types), API contracts, shared data types, cross-PR traps, domain language]
[omit the section when the PR sections carry everything]

## testing decisions

[the seam(s) the tests exercise, and prior art: similar tests in the codebase]
[`/tdd` skill defines what makes a good test; routine coverage is assumed, record only the decisions]

## PRs

### PR 1/2: "[title]"

```text
code est. diff:                    +xxx -xxx; net: +xxx
tests/docs/stories/etc. est. diff: +xxx -xxx; net: +xxx
```

contract:

- [the end-to-end behaviour this PR makes work - observable invariant or behaviour, stated here and nowhere else]

edge cases:

- [traps and non-happy paths a competent implementer could miss]

risk: low|medium|high - [must name the main failure mode or review focus; generic labels like "small change" are insufficient]

steps: [omit the section when the contract already implies them]

- [in-PR ordering constraints, exact commands, discovered environment constraints]

### PR 2/2: "[title]"

...

</plan-template>
