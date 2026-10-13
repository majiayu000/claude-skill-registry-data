---
name: sprint-planning
description: >
  Autonomously plan a CIDCA sprint in ClickUp — pull ready backlog tickets into the
  current (not-completed) sprint up to team capacity, balance by dev skill + time
  constraints, write a sprint-goal doc, and generate follow-up tickets from sprint
  results or current context. Triggers: "/sprint-planning", "plan the sprint",
  "sprint planning", "fill the sprint", "close and plan next sprint".
metadata:
  type: reference
---

# Sprint Planning (CIDCA)

Automates the recurring 2-week sprint ceremony for the CIDCA / Nimbus team. Runs
end-to-end: read the backlog, select and assign work to capacity, document the
sprint goal, and seed the next round of tickets. Pairs with
[`ticket-brief`](../ticket-brief/SKILL.md) (rich agent-ready descriptions) —
every ticket this skill creates or fills follows that format.

## Prerequisite

- **ClickUp MCP** (`mcp__clickup__*`) — required. Check with `ToolSearch`. If
  absent, tell the user the ClickUp MCP must be connected in *this* session (it is
  not available on the headless whitepc box unless explicitly configured — see
  [Running on the home server](#running-on-the-home-server)).
- **`gh` CLI** — optional, to reconcile ticket status against merged PRs.

## Team & capacity (the model to plan against)

3 devs + 2 product/design. Nobody is full-time; agents do the bulk of the
execution, so **story points measure human oversight/review capacity, not raw
effort**. Plan conservatively.

| Person | Role | Owns | Capacity / 2-wk sprint |
|---|---|---|---|
| **Hector** (`55629838`) | Senior dev, SW architect. Writes almost all the code. | Core Django backend + service layer, cross-cutting/complex work, SW arch, the Swift iOS doctor app, anything high-risk. | 5–8 pts |
| **Nico** (`55629857`) | DevOps / SRE, very experienced. | Infra (Terraform / `cidca-infra`), AWS, observability, lambdas provisioning, cidkit provisioning/Ansible, PoCs on anything. | 5–8 pts |
| **Jorge** (`112061559`) | New to dev, learns fast, hands-on with AI. | Fullstack **T3 stack** (Next.js/tRPC/TS/Tailwind), frontend, AI/OCR PoCs, cidkit **embedded** device software, some Python. | 5–8 pts |
| **Jose** (`43028342`) | Product owner / designer. | Design, UX ideas + heavy feedback. **Rarely** produces wireframes. **Do not assign code tickets.** | Design/PO tickets only |

- **Default team target: ~18 pts/sprint** (≈6 pts each × 3 devs). Ceiling 24; floor
  15. If the sprint is already partly filled, plan only the *remaining* headroom per
  person.
- Design provides feedback/ideas, not specs — don't block a ticket waiting on a
  wireframe unless the ticket explicitly needs one.

## ClickUp coordinates (baked in)

| Thing | ID |
|---|---|
| Workspace | `9013545070` |
| Space **CIDCa** | `90132262292` |
| **Backlog Plataforma** (source list) | `901307153897` |
| **Sprints** folder | `90133894814` |
| **Documentacion Plataforma** folder (sprint docs) | `90133894812` |

Sprint lists are named `Sprint <N> (d/m/yy - d/m/yy)` inside the Sprints folder.
**Current sprint = the highest-numbered Sprint list** (fetch the folder via
`clickup_get_workspace_hierarchy(space_ids=["90132262292"], max_depth="2")` and
take the last `Sprint N`).

> **⚠️ Never create the sprint list via the API.** ClickUp's real **Sprints** are
> minted by the Sprints ClickApp (they carry sprint start/end dates, sprint points,
> and burndown). The public API — `clickup_create_list_in_folder` /
> `clickup_create_list` / `clickup_update_list` — only makes a **plain list**;
> there is no parameter for sprint dates or the sprint flag, and no way to convert
> a plain list into a Sprint afterward. A plain list in the Sprints folder looks
> right but is NOT a sprint (confirmed 2026-07: doing this produced a dud that had
> to be recreated in the UI). **The user must create the next sprint in the
> ClickUp UI** (Sprints folder → New Sprint); this skill then detects the new list
> (newest in folder `90133894814`) and moves/fills tickets into it. Likewise there
> is **no delete-list tool** — if a stray list needs removing, ask the user to
> delete it in the UI (or rename it `⚠️ DELETE ME …` and flag it).

**Statuses** (list config): `Open` → `pending` → `blocked` → `in progress` →
`in review` → `completed` / `released` / `rejected` / `Closed`.
Done = `completed` | `released` | `Closed`. Killed = `rejected`.

**Tags** in use: `backend`, `frontend`, `infra`, `cidkit`, `aws`.

## CIDCA product context (for prioritization + assignment)

CIDCA = remote ECG diagnosis. Patients get an ECG at a center on a **CIDkit**
(Orange Pi appliance) → SCP trace → cloud lambdas → the platform → a **doctor**
interprets remotely and issues a report. Repos:

- **`cidca-platform`** — `ecg_auto` (Django API) + `ecg-ui` (React). Ship lockstep.
- **`cidca-services`** — lambdas / crons / Greengrass (parsescp, OCR, IoT).
- **`cidca-infra`** — Terraform (Nico).
- **`cidca-cidkit`** — planned embedded monorepo (CITkit v2 rewrite).
- **Swift iOS doctor app** — planned native client.

**The doctor is the throughput bottleneck.** Anything that slows the doctor's
review loop (or makes the field kit unreliable at an event) is top priority.

## Prioritization order (apply top-down when selecting)

1. **Doctor-facing bugs / operational blockers** — the doctor is the constraint.
2. **Customer/event commitments** (FERIA-type dated work).
3. **Big bets in flight** — Swift doctor app, CITkit v2. *Hardware root-cause
   (autopsy/stress/telemetry) gates the enclosure/heat-sink work — sequence it.*
4. **Reliability / infra / tech-debt** — telemetry, observability, tests, migrations.
5. **Research PoCs / nice-to-haves.**

Within a tier, order by: `urgent` > `high` > `normal` > `low`, then by dependency
(unblockers first), then by quick-win (small points, high impact) to build momentum.

## Story-point sizing (Fibonacci, oversight-time based)

| Pts | Meaning |
|---|---|
| 1 | Trivial, agent one-shot, <~1h review. |
| 2 | Small, single PR, light review. |
| 3 | Medium, ~half-day of human oversight, maybe 2 PRs. |
| 5 | Large, multi-PR, real design decisions. |
| 8 | Epic-ish / spike with unknowns. **Split if possible.** |
| >8 | Not allowed — decompose into a parent + ≤5 subtasks (see `ticket-brief`). |

If a backlog ticket has no estimate, infer one from scope and **write it to the
ticket** (set an estimate custom field if present, else note pts in the description
and via `time_estimate` where 1 pt ≈ 120 min of oversight).

## Definition of Ready (a ticket is pullable only if…)

- Has a **goal**, **acceptance criteria**, and a **blast radius** (repo/files).
- Has an **estimate** and a sensible **assignee** (by the skill map above).
- **No unresolved blocker** (`blocked` status or an open dependency).

If a high-priority ticket isn't Ready, the skill **makes it Ready** (fills the
brief via `ticket-brief`, estimates, assigns) rather than skipping it — then pulls
it.

## Definition of Done

Ticket → `completed` only when **every** relevant PR (ticket + subtasks) is merged.
Any open/draft PR ⇒ stays `in review`. (Same rule as `ticket-brief`.)

## The autonomous run

Do these in order. Narrate each step; only pause for the two confirmations noted.

1. **Locate the current sprint** — hierarchy → last `Sprint N` list. Read its tasks
   (`clickup_filter_tasks(list_ids=[sprint], include_closed=true)`).
2. **Reconcile status** — if `gh` is available, flip tickets whose PRs are all
   merged to `completed`; leave the rest. Report the done/not-done split.
3. **Compute headroom** — per dev: `target(6) − points already assigned to them in
   the sprint`. Skip anyone already at ceiling.
4. **Rank the backlog** — read Backlog `901307153897`, drop `completed`/`rejected`,
   apply the prioritization order + Definition of Ready.
5. **Select to capacity** — greedily fill each dev's headroom with the highest-
   priority Ready tickets that match their skill map. Respect dependencies (pull the
   unblocker into the same or earlier sprint). Don't exceed per-dev ceiling. Leave
   ~1 pt slack each for interrupts. **⇢ Confirm the selected set with the user
   before moving tickets** (list: ticket, assignee, pts, why).
6. **Commit the plan** — for each selected ticket: `clickup_move_task` into the
   sprint list, set assignee + estimate + priority, status `Open`. Backfill briefs
   for any that were thin.
7. **Write the sprint doc** — `clickup_create_document` (or a doc page) in the
   **Documentacion Plataforma** folder titled `Sprint <N> — Plan & Goals`, using
   [`templates/sprint-doc.md`](templates/sprint-doc.md). Link it from the sprint.
8. **Generate follow-up tickets** — from (a) the just-closed sprint's results /
   spillover, (b) any context handed in (meeting transcript, PR review, incident).
   Create them in the **Backlog** with `ticket-brief` briefs. **⇢ Confirm the new-
   ticket list with the user before creating** (creating ≤ the batch is fine; large
   batches: show titles first).
9. **Report** — one compact summary: sprint N, goal, per-dev load (pts), doc URL,
   tickets moved, tickets created, anything left un-Ready and why.

### Time-constraint checks (do NOT skip)

- **Sprint window**: if a pulled ticket has a `due_date` past the sprint end,
  flag it — either it's mis-scoped or it belongs to a later sprint.
- **Dated commitments** (event/customer): schedule the unblockers early enough;
  never place a hard-dated ticket in a sprint that ends after its due date.
- **Over-commit guard**: if total selected > ceiling, drop the lowest-priority
  tickets back to backlog and say so. **Silent over-commit is a failure.**
- **Sequencing**: respect gating (e.g. dead-kit *autopsy* + *stress test* before
  committing the *heat-sink/enclosure* ticket).

## Assignment heuristics (skill → owner)

Map by tags/keywords, then balance load:

- `infra`, `aws`, terraform, App Runner, observability, provisioning, Ansible,
  lambda deploy, SRE, PoC-anything → **Nico**.
- `frontend`, T3/Next.js/tRPC, OCR/AI PoC, cidkit **device/embedded** software,
  small Python → **Jorge**.
- Core Django/backend arch, service layer, cross-cutting, high-risk, Swift app,
  migrations touching cross-repo hot-spots → **Hector**.
- Design/UX-only → **Jose** (never code).

If the best-fit owner is at ceiling, either (a) push the ticket to the next sprint,
or (b) reassign to the next-best-fit dev — prefer (a) for high-risk work.

## Guardrails

- **Confirm before**: moving the selected set into the sprint (step 5) and creating
  a batch of new tickets (step 8). Everything else runs autonomously.
- **Never** exceed 1 parent + 5 subtasks per ticket (re-scope instead).
- **Never** delete or `rejected`-kill someone else's ticket without explicit OK —
  link/flag duplicates instead (merges need user approval).
- **Never** push code or touch repos from this skill — it operates on ClickUp only.
- Keep the doctor-bottleneck lens: if a sprint has zero doctor-impact tickets while
  doctor bugs sit Ready in the backlog, say so.

## Running on the home server

For a long unattended run (e.g. planning + generating many briefs while the Mac is
closed), the compute can be offloaded to `whitepc` (see the `homeserver` skill) —
**but** the ClickUp MCP must be reachable there. Two options:

- **Simplest**: run this skill in a live session on the Mac; it's minutes of work,
  not hours. No offload needed.
- **Headless on whitepc**: only if `claude` on the box is configured with the
  ClickUp MCP + token. Launch detached: `ssh homeserver 'tmux new-session -d -s
  sprint "cd ~/work && claude -p \"/sprint-planning\" > sprint.log 2>&1"'`, then
  poll `ssh homeserver 'tmux capture-pane -pt sprint | tail -40'`. Closing the Mac
  won't kill a tmux job already launched on whitepc.

## Follow-up

After the run, ask: `Close the current sprint and start the next?` — note that the
user must **create Sprint <N+1> in the ClickUp UI** (the API can't; see the sprint-
list caveat above); once it exists this skill detects it and fills it.
