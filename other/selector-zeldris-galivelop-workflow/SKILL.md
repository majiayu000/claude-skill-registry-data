---
name: selector
description: Pick the skill and models for the task that is starting. Use at the start of every task, when a bug or a design request arrives, before reviewing a diff for the protected branch, when a block or phase closes, and whenever the user asks which workflow or model fits.
license: MIT
compatibility: Claude Code or any Agent Skills agent; reads .claude/gw.json when present
metadata:
  version: "0.4.3"
  source: "Galivelop workshop; generalised from the Tarkor, installer and portal selectors"
---

# Selector

If `.claude/gw/selector.md` exists in the project, read it first: it holds what is specific to the project.

Classify the task with the table, then act on its row. Reply in the project's `language` (`.claude/gw.json`).

| Case | Skill(s) | Session model | Subagent model |
|---|---|---|---|
| Design: new feature, open decision, architecture, UX, anything the user must decide | `grilling` + `domain-modeling`; `prototype` when numbers, rules or screens need trying | large (Opus) | light (Haiku) for `Explore` searches |
| Bug, red or flaky test, something visibly broken | `diagnosing-bugs` | large if the cause is not obvious; medium (Sonnet) if it shows at first sight | none |
| Large change: several systems, data, migration, concurrency, build or routing | the project's plan for it | large | light, to find usages |
| Scoped change: one component, one adjustment, one test, one small endpoint | none | medium | none |
| Mechanical: docs, log, renames, adapting tests to a new signature, converting files | none | medium or light | light |
| Bring something from another repo (a workflow, skills, documents) | `orchestrate-dealer` | large, to decide what to adapt | light `Explore` that reads the other repo and returns a summary with paths; the main session never reads the files whole |
| Apply or update the workflow (`gw-init`, `gw-update`, `gw-doctor`) | `orchestrate-dealer` | large, to decide | light, to read the workflow's guide and scripts and return the decisions with paths |
| Review before the protected branch | `/code-review`, then `pr` for the description | large | none |
| Closing a block or phase | `retro` (Claude runs it, the user confirms its proposals); now and then `improve-codebase-architecture` | large | none |
| Social posts about the project (what to post, a post, an announcement or an image about something that just happened) | `gw-media-content` to propose, `gw-media-content-now` to produce one piece | medium | none |
| Writing for agents (`AGENTS.md`, `CLAUDE.md`, skills, docs agents read) | `writing-for-agents` | medium | none |

Use a skill only if it exists in this repo's `skills/` (or `.claude/skills/`) or the project declares it; otherwise
do the case without it and say so.

## Rules

- **The user picks the session model** (`/model`); an agent cannot switch it. State in **one line** which model and
  skill the case calls for ("large model and `diagnosing-bugs`") and carry on. Wait for an answer only when the risk is
  high: data migration, deleting, rewriting published content.
- **Subagent model:** pass the table's subagent column as the `model` parameter. Delegate searches, long reads and
  mechanical work; design and decisions stay in the main session.
- **Closed plan, scoped implementation:** goes to a `sonnet` subagent and the main session reviews its diff before
  the commit. The fixes from a review are a closed plan too (`sonnet`); `opus` only to debug something non-obvious. Anything of more than one step runs through `orchestrate-dealer`.
- **Subagent ladder:** `sonnet low` → `sonnet medium` → `opus medium` → `opus high`. Start at the lowest rung that
  fits; when a subagent does not finish its brief, the next attempt climbs one rung. **Two failures at one rung: stop
  and ask the user.** A subagent that never starts (tool error) is retried on the same rung and does not count as a
  failure. Unattended long work that closes nothing in a batch stops and writes the state to the log.
- **When in doubt between two rows, take the one with higher risk.**
- **Closing a task or PR:** with everything pushed and the log up to date, ask the user for a `/clear` in one line,
  saying why (a long context is almost all the spend; the log is enough to resume).
- **Compaction budget:** at the start of a task, estimate how many compactions it should need (0–5) and write it in
  the log next to the count the session already has (`recuperar.py --estado` prints it). Going over the budget is the
  signal to deal more work out with `orchestrate-dealer`, not to keep going.
- **Design references:** if `.claude/gw.json` lists `designReferences`, design rows contrast each proposal with them
  and name the source (see `grilling`).
- Decisions reached in a design session go to the project's plan or log (`log` in the config); glossary terms to
  `GLOSSARY.md`; decisions hard to reverse to `docs/adr/`.

## Project rows: `selector.cases`

`.claude/gw.json` may add rows under `selector.cases`. Read them at the start and treat them like the table above,
matching them before the generic rows. Shape of one entry:

```json
{ "selector": { "cases": [
  { "case": "Change to the installer's process spawning",
    "skill": "diagnosing-bugs",
    "sessionModel": "large",
    "subagentModel": "sonnet medium" }
] } }
```

- `case`: when the row applies, in one sentence a task can be matched against.
- `skill`: skill name(s) or `none`.
- `sessionModel`: `large`, `medium` or `light` (or a model name).
- `subagentModel`: a rung of the ladder, a model name, or `none`.

A project row overrides the generic row it overlaps; the rules above apply to both.
