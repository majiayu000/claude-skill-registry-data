---
name: manage-plan
description: Create, update, or check the plan for one issue — what gets done, in what order, and why, never how — written to the issue's STM as specs/plan.md in the canonical plan format. Called by an agent after it has gathered the plan context (the issue, its parent, its child issues, any plan already on disk). Use before work starts (create), whenever work finishes, starts, or the order changes (update), and before an issue is called done (check). The check runs a script, so a play's done check can rely on it.
user-invocable: false
model: sonnet
allowed-tools: Bash, Read, Write, Edit
---

# manage-plan

Plan mode for Garura (#619). Every drive and every play works from a plan on disk: it writes the plan before it works, keeps it current while it works, and is done only when the plan is done. A plan says **what** gets done, **in what order**, and **why that order**. It never says **how** — that is design, and it belongs in each item's own issue.

You write and update the plan. You do NOT gather context (the calling agent did that) and you do NOT decide what the work is (the issue and its context say that).

## Input

Receive from the agent:

| Field | Required | Meaning |
|-------|----------|---------|
| `action` | yes | `create` · `update` · `check` |
| `issue` | yes | the issue number the plan is for |
| `plan_path` | yes | `{stm_base}{issue}/specs/plan.md` |
| `context_path` | `create`, `update` | the plan context file the agent wrote (see below) |
| `change` | `update` | what happened, in plain words — e.g. "item 2 is finished", "Kapil moved #619 to the front", "item 4 is dropped: covered by #612" |
| `report_path` | yes | where to write the check report (e.g. `{stm_base}{issue}/context/plan-check.json`) |
| `template_path` | no | the work-plan format; default `~/.garura/core/memory/standards/templates/work-plan.md` |
| `rules_path` | no | the work-plan rules; default `~/.garura/core/memory/standards/rules/work-plan.md` |

The **plan context file** (written by the agent, YAML or JSON) holds:

- `issue` — number, type, title, full body
- `tree_available` — `false` when the tracker could not report type, parent or children (GitLab, or gh older than 2.94.0); then those are unknown, not empty
- `parent` — number, type, title (or null)
- `children` — each child issue's number, type, title, state, and its own children
- `linked` — issues the agent found linked by the tracker's parent/child link only, never body mentions
- `existing_plan` — the path of a plan already on disk, or null
- `parent_plan` — the path of the parent issue's plan, or null
- `decisions` — paths to decision records the issue points at (ADRs, spike notes), if any
- `notes` — anything the user said about order or priority, quoted, with the date

## Process

Read both files first, every time: the format at `template_path` and the rules at `rules_path` (defaults in Input). They are the single source; this skill applies them and never restates them. A work plan is not `/implement`'s build plan.

### Action: `create`

1. If `existing_plan` is set, write nothing: run the check on the existing plan and return its paths. A plan is never written twice; the caller sends `update` with a `change` if it wants the plan changed.
2. Read the context file and every decision record it lists.
3. Write `plan_path` in the canonical format:
   - **What we are trying to reach** — what is true today, what should be true instead, and why, in plain words.
   - **When this plan is done** — observable outcomes. For a business intent, say that it is met by its outcome, not by its children closing.
   - **Where we are now** — what is already done or decided, and the next step.
   - **The plan, in order** — finished children under `### Done`; open children as numbered items. Each item carries **Issue**, **What**, **Why here**, **Done when**, **Needs**. Order follows the context's dependencies and the user's quoted notes; where neither settles it, put decisions before the builds that depend on them.
   - Mark exactly one item `— now`, and set the same number in the front matter.
   - Every finished item says what kind of done it is — decided, built, or shipped — and what is still not done.
   - If `tree_available` is `false`, say in **Where we are now** that the parent and children could not be read, and list only what the context does hold.
   - Unless the issue is a business intent, set `serves_plan` to the parent issue's number and `serves_item` to this issue's item in the parent's plan (the context's `parent_plan` says where that plan is). If the parent has no plan yet, say so in the log and leave both out.
   - **Log** — one dated line: the plan was created, and from what.
4. Run the check (below). Fix anything it reports before returning.

### Action: `update`

1. Read the plan and the `change`.
2. Apply only that change:
   - a finished item moves to `### Done` as one line, **keeping its number** (`**{n}. Decided | Built | Shipped: …**`), saying what it settled or delivered and what is still not done;
   - a dropped item is removed, and the log says why;
   - a reorder moves items and fixes every **Needs** that pointed at them;
   - move `— now` and the front matter `now` to the next item that can start.
3. Set `updated` to today. Add one dated log line saying what changed and why.
4. When no numbered item is left, set `status: done` and `now: -`.
5. A big update (rules file: adding, dropping or reordering items; a play finishing inside a drive; a linked issue completing) is logged as big. Outside a drive, the calling play routes it to `approve-change` (planned, #622); this skill does not ask the human.
6. Run the check. Fix anything it reports before returning.

### Action: `check`

Run the bundled script. It is deterministic: no git, no network, no judgment.

```bash
python3 <skill-dir>/scripts/check_plan.py --plan <plan_path> --out <report_path>
```

`<skill-dir>` is this skill's folder (`.claude/skills/manage-plan/` once installed). Its tests: `python3 <skill-dir>/scripts/test_check_plan.py`.

Exit `0` — valid and done. Exit `1` — valid, not done (the normal state while work runs). Exit `2` — not valid: the report lists every problem. Exit `3` — the file cannot be read.

## Output

Every action writes files and returns their paths — never the content:

```yaml
plan_path: {stm_base}{issue}/specs/plan.md        # create / update
report_path: {stm_base}{issue}/context/plan-check.json
```

The report at `report_path` is the script's output, unchanged:

```json
{ "valid": true, "done": false, "status": "active", "now": "2",
  "open_items": [2, 3, 4], "serves_plan": "<parent plan path or null>",
  "problems": [], "plan": "<plan_path>" }
```

Never report a plan as done unless that file says `done: true`.

## Constraints

The plan's own rules are in `rules_path`. This skill adds three of its own:

- **Change only what the `change` says.** An update is not a rewrite.
- **Create never overwrites a plan.** With a plan already on disk, `create` writes nothing and returns the existing plan's paths.
- **The script decides done.** Not you.
