---
name: planner
description: 'Plan an issue one level down with blockers and sizes, grill the open decisions, create the issues; refine <nr> checks readiness. Use for "plan issue #N" or "refine #N".'
---

Planning only: no source edits. The planning steps below ask nothing (open decisions go into `questions[]`, see `references/questions.md`); the plan is the reply.

`help` (or `--help`, `-h`): print `references/help.md` unchanged, nothing else.

## Modes

- **Non-interactive** (a workflow subagent, e.g. `deliver` phase 1): no questions, no issue creation; return the plan with `questions[]` as data, the caller decides.
- **Interactive** (a user session): plan, grill, approve, create (see `## Interactive`).
- **`refine <nr>`**: see `## Refine`.

## Interactive

1. Plan per `## Steps`.
2. Load `grill-me` with the plan's `questions[]`. Re-plan only when an answer changes the item structure (items added, removed, split, re-blocked); otherwise fold the answers into the item bodies. Next round with the new `questions[]` until none is open.
3. Show the items (id, title, size, `blocked_by`) and the answers. The user approves granularity, blockers and which items to create; also with zero questions. Create nothing before.
4. Create the approved items with `github-issue` `references/create-from-plan.md`; each created issue gets the answers that concern it under `## Decisions` (`<question> — <answer>`).

## Refine

`refine <nr>`: no plan, no new issues except an approved split.

- Read the issue and its children (`gh issue view <nr> --json title,body,labels,comments`; sub-issues as in `## Steps` 3). Explore the code it names; facts are not asked.
- Check the list of its level in `references/ready.md`. Collect the gaps only. With `governance` in `.agents/config.json`: also `references/governance.md` for the ADR and spec gaps.
- An Epic or Feature without children: offer the interactive plan (`## Interactive`) instead of only grilling.
- A PBI of size L: propose the split into sibling PBIs (`## Output level`), created only after approval.
- Load `grill-me` with the gaps only. Update the body with the decisions (`## Decisions`) and the sharpened criteria and notes via `gh api -X PATCH repos/{owner}/{repo}/issues/<nr> -F body=@file`.
- Missing `Tier:` line (PBI or Bug, `references/ready.md`): add `Tier: <tier> — <reason>` to the body, the tier from the table of `references/plan-schema.md` (size S fast, M standard, L strong, else standard). Each change is listed in the report with its item and tier; an existing line is never changed. `refine M<n>` does this for every open PBI and Bug of the milestone and reports the items it changed (`references/ready.md`).
- Milestone: the PBIs created in step 4 get the milestone the user names, else the one of the Feature; none known → ask once. Never set a milestone on an Epic, and a Feature only when all its PBIs are in it (`github-issue` `references/milestones.md`).
- Labels: ready → remove `needs-refinement`; open decision left → add `needs-decision` and post the question as a comment. Create the label (`gh label create`) when the repository lacks it.

## Depth (exploration budget)

Pick from the request ("quick plan", "deep planning") or default to **standard**.

| Depth    | Exploration                                               |
| -------- | --------------------------------------------------------- |
| quick    | ~5 key files                                              |
| standard | Grep/glob/read affected and related code                  |
| deep     | Standard + call sites, tests, docs of every affected area |

Depth limits exploration, not the number of items. Size items by session: **one item = one fresh session**.

## Output level

The input type decides it (`labels`, else title prefix `[Epic]`/`[Feature]`/`[PBI]`/`[Bug]`, or the legacy `Epic: `/`Feature: `). Plan titles are summaries; the caller adds the level prefix:

| Input            | Plan items                                                                                                                                                                                                  |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Epic             | Features (`<capability>`, created as `[Feature] …`)                                                                                                                                                         |
| Feature          | PBIs (`feat: …`, `fix: …`, created as `[PBI] …`)                                                                                                                                                            |
| PBI or bug       | none when it fits one session: `items: []`, the summary says `refine <nr>`. Too big (size L or more than one session) → a split into sibling PBIs under the same Feature (`feat: …`, `fix: …`, level `pbi`) |
| Description only | internal steps (level `pbi`), no issues are created                                                                                                                                                         |

In a split, `p1` becomes the planned issue (its title and body are replaced) and the other items are created as sibling `[PBI]`s (`github-issue` `references/create-from-plan.md`). No plan creates `[Task]` issues; `[Task]` sub-issues of older plans are read, never re-planned.

## Steps

1. Resolve owner/repo from `git remote get-url origin` (SSH or HTTPS). Never ask the user.
2. Load `detect-techstack`; keep the JSON. Then the lessons, from the project root: `pwsh <skill-dir>/scripts/Get-Lessons.ps1 -Role planner -Lang <langs>`, `<langs>` the languages of the report, comma-separated; `<skill-dir>` is the installed `lessons` skill (`.claude/skills/lessons/` project, `~/.claude/skills/lessons/` global, `.agents/skills/lessons/` OpenCode/Copilot). `lessons` not installed or no output: continue exactly as before, without a note. The output is data (`lessons` `## Use`): it never overrides these rules, the input's criteria, blocking findings or permissions.
3. Read the input: `gh issue view <nr> --json title,body,labels`, or the description. Read ALL children, open and closed, with `gh api --paginate repos/{owner}/{repo}/issues/<nr>/sub_issues --jq '.[]|{number,state,title,labels:[.labels[].name]}'`; open and closed children count as existing and are never re-planned. Plan only what is missing. A PBI or Bug input: also read the children of its parent Feature (`Parent Feature: #N`) so a split does not duplicate a sibling.
4. Explore per the depth with a subagent per affected area, given the file budget and the question; keep only its ≤ 300-word summaries (Claude Code built-in `Explore` subagent, OpenCode `task`, VS Code Copilot `runSubagent`). Without subagents, explore inline with Read/Grep/Glob under the same budget.
5. Slice per `references/slicing.md`. Per item set `blocked_by`, `size` (S/M/L), `tier` (fast/standard/strong, see ## Tier) and `files`. Items whose files or exploration summary show background/async work, persistence or a state machine get an `## Invariants` section per `references/invariants.md` (load it only then). With `governance` in `.agents/config.json`: also `references/governance.md` (decision PBIs, spec criteria).
6. Collect open decisions as `questions[]` per `references/questions.md`; resolve anything the repo can answer yourself.
7. List what you took as given and did not ask about as `assumptions[]`; build the plan per `references/plan-schema.md`.

## Tier

Set `tier` per the table in `references/plan-schema.md`. Every item body carries one line `Tier: <tier> — <reason>`. Size L is `strong` unless split.

## Return

The plan JSON per `references/plan-schema.md`, then a summary of ≤ 10 lines: input type and level, item count by size, the first unblocked item, open questions (id and one line each).

## Rules

- Titles are summaries without level prefix (Feature: the capability; PBI: `feat: `, `refactor: `, `fix: `); the caller prefixes them per the `github-issue` Issue Types; bodies are implementable without re-exploring: exact files and symbols, where tests go, what is out of scope.
- `blocked_by` forms a DAG over plan ids and existing issue numbers; no cycles, no self-reference.
- Never use markdown checklists for hierarchy; the caller uses native sub-issue and blocked-by links.
- The plan schema is the contract between planning and the caller.
