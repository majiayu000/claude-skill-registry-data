---
name: "Roadmap: Add Task"
description: "Add a well-formed task, or a reviewed batch of them, to a rich-format roadmap: ID assignment, dependency wiring in both directions, graph integrity"
when_to_use: "Whenever the user wants to add a task, feature or work item to a roadmap, even phrased as 'add this to the roadmap', 'put this in the plan' or 'track this as a task'. For a batch of half-formed ideas, run roadmap:create-interview first and feed its approved proposal here as one batch."
model: opus
effort: medium
metadata:
  glyph: ᛟ
  family: roadmap
disable-model-invocation: false # invocable by Claude so "add this to the roadmap" loads this skill instead of hand-editing the JSON; Step 7's approval gate still applies
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash(python3:*)"]
arguments: ["mode", "description"]
argument-hint: "[t|c|m] [description]"
---

# Roadmap Task Adder

Adds a well-formed task to an existing rich-format roadmap. The job is not appending a line; it is placing the task correctly in the dependency graph, wiring its relationships in **both** artefacts (`.claude/roadmaps.json` and the PHASE file it names), and leaving the roadmap coherent.

Shared conventions: `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`. The CLI is `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py`.

## Batch mode

When the input is a multi-task proposal (typically `roadmap:create-interview`'s approved output), run Steps 1–6 for the batch as a whole rather than once per task: assign every ID up front, wire all edges including those between the new tasks themselves, and run the Step 5 integrity checks across the combined graph. Steps 7–9 stay singular: one consolidated proposal, one approval, one write pass, one validate. Never loop the full skill per task; fifteen approval gates for one already-reviewed proposal is ceremony, not safety.

---

## Step 0: Resolve the mode

`$mode` is `t`, `c` or `m` (aliases below), first token of `$ARGUMENTS`, case-insensitive. Remainder is `$description`.

| Token | Aliases                            | Meaning |
|-------|------------------------------------|---------|
| `t`   | `task`, `tasks`                    | One or more tasks, independence unknown: treat as unrelated unless `$description` says otherwise |
| `c`   | `chain`, `sequence`, `set`         | At least two tasks with a natural dependency order the user asserts: wire the chain in the order given |
| `m`   | `mile`, `ms`, `miles`, `milestone` | Create at least one new milestone; `$description` may also carry a seed task |

Resolution depends on how this skill was reached:

- **Explicit `/roadmap:update-tasks` invocation with no arguments or with a first token matching none of the aliases**: hard stop. Print `Usage: /roadmap:update-tasks t|c|m "<description>"` and run nothing. Never guess a mode for an explicit invocation with no recognisable token: "improve the CSS" alone is exactly this case.
- **Model-invoked from natural language** ("add this to the roadmap", with no mode token because there's no slash command to carry one): infer the mode from the request shape and say the inference aloud before proceeding: one item → `t`; "X then Y" / "after" / explicit sequential phrasing → `c`; "new milestone" / "new phase of work" → `m`. This is the only path where mode is inferred rather than typed.
- **`m` with a milestone description but no seed task**: not a stop; ask for the seed task via AskUserQuestion, then continue.

`t` and `c` both proceed into Steps 1–9 below, unchanged in step numbering; `c` additionally parses `$description` for its asserted order (the word "then", commas, "after") and wires each task's `dependsOn` to the one before it in that order, then runs the rest identically to `t`. `m` proceeds into "Milestone mode (`m`)" below before continuing into Step 3.

---

## Step 1: Locate the roadmap and check the format

Run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py detect`. Exit **3** = old simple format: **stop and tell the user to run `roadmap:migrate` first**. Exit **2** = could not locate/parse: ask the user for the path. Only proceed on exit 0.

Read the full `roadmaps.json` and the active phase's PHASE file before adding: you need the existing task graph, milestone IDs, gates and categories.

---

## Step 2: Understand what to add

Extract: **description**; **milestone** (which milestone; ask if unclear); **category** (2–3 letter prefix, reuse an existing one in that milestone where it fits); **dependencies** (what must be done first; what it unblocks); **assignee** (ask the user directly; never infer it from the description, the git author, the category owner or who is running this skill; leave it unset if the user doesn't say). Ask before proceeding if any is ambiguous: a badly placed task is worse than a delayed one.

**In milestone mode (`m`), do this instead of picking an existing milestone**: see "Milestone mode" below, then continue into Step 3 for the seed task(s).

---

## Milestone mode (`m`)

No existing skill appends a milestone to a *live* phase (`roadmap:create` builds a whole phase from scratch, including its milestones, in one pass; `roadmap:migrate` upgrades an old-format file wholesale). This is that missing procedure. Run it in place of the ordinary "pick an existing milestone" half of Step 2, then continue into Step 3 onward for the seed task(s) that populate the new milestone.

1. **Assign the milestone ID**: `M{max existing milestone number + 1}`. Never reuse a milestone ID, mirroring the task-ID rule below. This numbering rule and the milestone field-order rule both live in `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`; read it there rather than re-deriving it.
2. **Milestone object shape**: exactly `{id, name, goal, tasks: []}`; no other fields. Ask the user for `goal` (one sentence) if they haven't given one.
3. **Milestone-to-milestone gating**: milestones have no `dependsOn` field of their own; a "this milestone can't start until X finishes" gate is expressed on the seed task(s) inside it instead. If the user says the new milestone is gated on other milestones, give the seed task `dependsOn: ["M{a}", "M{b}", ...]`; it resolves once every non-`softMilestone` member of each is `done` or `out_of_scope`.
4. **Flag mid-sequence insertion rather than deciding it silently.** `M{N}` numbering is loosely coupled to task-ID category prefixes elsewhere in a roadmap (a category can span several milestones), and nothing documents what happens if a milestone is ever inserted between existing ones rather than appended at the end. Appending (this procedure) is unambiguous; if the user ever wants to insert mid-sequence, say plainly that this is an open question rather than picking a convention on the spot.
5. **Childless-milestone check**, parallel to Step 5's childless-task check below: a milestone with only one seed task is fine on its own. Flag it only if that task's own nature obviously implies more should follow soon.
6. Proceed into Step 3 for the seed task(s), exactly as for any other new task, with the milestone now resolved to the ID just assigned.

---

## Step 3: Assign a task ID

`{MilestoneNum}{Category}.{Seq}`: find the highest sequence in that category and use `next = highest + 1`. Sub-tasks: alpha suffix (`2TI.15a`). **Never reuse an ID**, even a removed one.

---

## Step 4: Identify dependencies

**Incoming** (`dependsOn`): tasks this new task requires. An entry may be a **task ID**, a **milestone ID** (`M1`: resolves done only when all its tasks are done), or an **external gate ID** (from `externalGates`). If a gate is an incoming dependency, the gate's `blocks[]` must gain this task ID (parity).

**Outgoing**: existing tasks that this new task should now block; add the new ID to their `dependsOn` (and mirror any gate parity). Completing this task may change those tasks' computed status (the recompute handles that). If one of them is claimed (it has a `started` date), say so before adding the edge: the new dependency blocks work someone has already started.

**Soft (`softDependsOn`):** an optional, best-effort link worth drawing but not worth blocking on; ask if the relationship is a real dependency or a soft one before defaulting to `dependsOn`. Renders dotted, imposes no status, no cycle constraint (see conventions reference for direction).

---

## Step 5: Graph integrity checks (before writing)

**Orphan check.** A task with no dependency edges in or out is orphaned. Warn (`"This task has no connections to the existing graph. Intentional?"`), suggest the most plausible connection, and proceed on the user's call. Some tasks genuinely stand alone.

**Childless check.** If nothing depends on the new task but its nature clearly unlocks future work, create a placeholder child in the appropriate milestone: `- [ ] **{NewID}**: {unlocked capability} _(blocked: depends on {NewTaskID})_`, `status: "blocked"`, with the dependency edge. Skip placeholders for obviously terminal tasks (deploy, final release notes). Tell the user what placeholder was created and why. In milestone mode (`m`), also run the childless-*milestone* check from that section above.

---

## Step 6: Compute the new task's status (mechanical)

The mechanical status rule applies (see conventions reference): empty `dependsOn` → `todo`; any non-`done` dependency → at least `blocked`, escalating under `deferred > paused > blocked > todo` — this covers both a dependency on a gate that `imposes: paused`/`deferred` and a dependency on a task that is itself already `paused`/`deferred`. `softDependsOn` never feeds this rule. After wiring, confirm the new task's status and any downstream changes with `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py recompute --check` (preview, no write).

---

## Step 7: Prepare the proposal (do not edit yet)

In milestone mode (`m`), lead with the milestone block, then the seed task block below it:

```text
New milestone: {ID}, {Name}
Goal: {goal}
Gated on: {milestone IDs, or "nothing"}
```

Task block (always; the only block in `t`/`c` modes):

```text
New task: {ID}, {description}
Milestone: {N} ({Milestone Name})   Status: {todo|blocked|paused|deferred}
Assignee: {name, or "unassigned"}
Dependencies (in): {IDs / milestone / gate, or "none"}
Dependencies (out): {task IDs this gets added to, or "none"}
Placeholder child: {ID and description, or "none"}

Graph changes:
  + roadmaps.json: new milestone object (m mode only); new task object; edits to {existing tasks' dependsOn}; gate blocks[] updates
  + diagram: regenerated from the JSON (node {ID}; edges {list})
```

Then ask: *"Does this look right? I'll write to the roadmap on your say-so."*

---

## Step 8: Write to both artefacts (once approved)

0. **`m` mode only, before anything else**: insert the new milestone object (`{id, name, goal, tasks: []}`) into the phase's `milestones[]` array, after the last existing milestone.
1. **`roadmaps.json`**: insert the task object in its milestone's `tasks[]` (field order per the conventions reference; tabs; British spelling). Include `assignee`/`softDependsOn`/`softMilestone` only when the user gave one; omit them entirely otherwise, exactly like `notes`. Update any existing tasks' `dependsOn`. Update any gate's `blocks[]` for parity. Add the placeholder task if any.
2. **PHASE file**: add the task line under its milestone with the status annotation (`_(blocked: depends on {IDs})_` etc.); update any existing task lines whose dependency clause changed; add the placeholder line. **`m` mode only**: first emit a full new milestone section (`## Milestone {N}: {Name}`, blank line, `**Goal:** {goal}`, blank line) before the task line, matching `roadmap:create` Step 7's shape. This is new work into an existing milestone; the section doesn't exist yet the way it does for a milestone `roadmap:create` built from scratch.
3. **Mermaid diagram**: replace the entire fenced `mermaid` block with the output of `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py graph --mermaid --direction LR`. Never hand-edit edges, sinks or class lines; the generator recomputes milestone sinks (including any former sink displaced by the new task) and the canonical colours.
4. **`ROADMAP_OVERVIEW.md`**: the task total (and, in `m` mode, the milestone total) changed, so update `**N tasks across M milestones.**`; pull *both* numbers from `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py stats --json` (`total` and `milestonesTotal`), never just the task count.

---

## Step 9: Validate and confirm

Run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py validate`; it must report clean (parity, acyclicity, status recompute). If an HTML dashboard exists (`docs/artefacts/roadmap-*.html`), refresh it with `roadmap.py render`. Then report: task added (and milestone, in `m` mode); status; edges added; existing tasks modified; placeholder created; any orphan warning. If the new task's computed status is `blocked` on a dependency that looks like it should already be `done` in reality, say so explicitly rather than reporting `blocked` as if the wiring itself is uncertain; the roadmap can lag real-world completion.

---

## Conventions

- Task line: `- [ ] **{ID}**: {description}` + annotation. Completed: `- [x] **{ID}**: {description}`.
- Milestone section: `## Milestone {N}: {Name}` + `**Goal:** {goal}`, matching `roadmap:create` Step 7.
- roadmaps.json is the source of truth; the PHASE file and overview are projections.
- Everything else (statuses, colours, graph/edge rules, formatting, milestone-ID assignment and milestone field order): `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`.

<raw-arguments value="$ARGUMENTS" />
