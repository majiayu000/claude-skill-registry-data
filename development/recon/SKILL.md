---
name: recon
description: >-
  Trace an existing system end to end — entry points, call paths, every read and
  write of the state involved, the contracts crossed, the failure and rollback
  paths — and write it down as a Recon Map before a plan for changing it is
  drafted. Fires when the user asks to plan, spec, design, refactor, migrate, or
  size a change to code that already exists: "write a plan", "plan this out",
  "how should we build X into this", "refactor X", "migrate X", "what would it
  take to change X", "will this break anything". Also self-trigger before you
  write any plan step whose blast radius names code you have not read. Uses the
  codebase-memory knowledge graph when installed, falls back to grep, and fans
  wide traces out across parallel read-only subagents. Produces a Recon Map file
  and hands off. Skip greenfield work with
  no existing system to trace, on a change confined to a file already read in
  full, on a typo or copy edit, on a non-code plan, or when a current Recon Map
  for the same subsystem already exists.
---

# Recon

Read the system before you plan a change to it. A plan written from the prompt plus three grepped files is fiction with headings — its steps reference call paths nobody traced, state nobody inventoried, and contracts nobody knew were there, and its blast radius section is invented. Recon makes the trace a deliverable with named artifacts, produced before the first plan heading.

**The one rule:** no plan step may name a blast radius that includes code nobody read. If a step touches a caller, the caller is in the map at `file:line`. If it cannot be found, it is in the Unknowns list — never silently assumed absent.

## When to run it

**Run recon when** the ask is to plan, design, spec, refactor, migrate, or size a change to a system that already exists, and the change plausibly reaches beyond a file you have already read in full.

**Skip recon when** — the calibration counter-example, and it matters as much as the trigger:

- **Greenfield** — there is no existing system to trace. Recon has nothing to read; go plan.
- The change is confined to a file you have **already read in full** — and one lookup says so. Spend the single call (`search_graph`, or one grep for the symbol name) before claiming this skip; any external reference it returns and the skip does not apply. Asserting the negative without the lookup is the easiest dishonest exit in this list.
- A typo, copy edit, comment, or formatting change.
- The plan is not about code (a process, a doc, a rollout schedule).
- A Recon Map for this subsystem exists and no relevant commit has landed since. Re-read it; do not re-run.
- You traced this exact subsystem earlier in this session, nothing has landed since, and the edges are still in your context. Write the map from what you hold rather than re-running the fan-out.
- The user hands you the edges. Skip the fan-out, not the map: fold their edges into the map, cite them to the user, and mark them `supplied` — unverified until read.

Say "recon skipped — [one-line reason]" and go. A recon on a contained rename whose references are already enumerated is ceremony, and ceremony is how a gate gets ignored when it counts. A rename whose callers are *not* yet enumerated is exactly what recon is for.

## Step 1 — Scope the trace

Name the **subject** in one line: the function, module, table, endpoint, or feature the change lands on. Name the **change class**: local edit, cross-module change, contract change, state/authority change, or replacement. If the class is state/authority, run [spike-360](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/4-occasional/spike-360/SKILL.md) first — it decides whether a new source of truth should exist at all; recon maps the system either way once that is settled.

Ask at most one clarifying question. If the subject is ambiguous, pick the likeliest reading, state it, and trace that — **unless the two readings sit on opposite sides of a boundary** (application versus infrastructure, this service versus another). There, guessing wrong spends the whole fan-out on the wrong system, so name both readings and ask.

## Step 2 — Seed from the knowledge graph if it is installed

If the `codebase-memory` MCP server is available, use it first — it answers "who touches this" in one call instead of twenty greps:

- `index_status` / `list_projects` — indexed, and **indexed at what revision?** Compare it to current HEAD and the dirty worktree; an index older than the last relevant commit is a stale lead, and every edge from it is unconfirmed until read. If unindexed and the repo is large, offer `index_repository` once with its cost; if declined, fall through to grep and record the degraded mode in the map.
- `get_architecture` — the shape of the system before the details.
- `search_graph(name_pattern | label | qn_pattern)` — locate the subject's symbols.
- `trace_path(function_name, mode=calls | data_flow | cross_service)` — the edges. This is the tool that earns the skill its name.
- `get_code_snippet(qualified_name)` / `search_code(pattern)` — exact source, and graph-augmented grep for the rest.

**The graph is a lead, not a citation.** Every edge a plan step will depend on gets confirmed by reading the file; an edge that exists only in the graph is marked `graph-only`. Depending on the indexer, it **may miss** config, SQL strings, templates, shell and CI scripts, cron, IaC and deploy manifests, generated code and its generator, database triggers/views/procedures, macros, runtime registries, reflection and dynamic dispatch, and consumers in other repositories. Anything in that list you did not verify by hand is an Unknown — in graph mode and grep mode alike.

No graph installed? Say so in one line and trace with grep, glob, and reads. The output contract does not change.

## Step 3 — Fan out, sized to the radius

Recon is wide, shallow, and parallel — the ideal sub-agent shape. Launch the lanes **in one message so they run concurrently**, each read-only, each returning the Step 4 envelope. Use sub-agents available to the current model through its own runtime and model provider; inherit the current model where supported, without requiring a named model, model lab, or vendor-specific agent type.

Scale the lane count to the radius, and say which you ran: a two-file change with one caller is one lane in your own context; a subsystem with external consumers is all four.

| Lane | Question it answers | Owns |
| --- | --- | --- |
| **A. Entry & call paths** | How does control reach this code? | Callers and entry points — routes, CLI, cron, hooks, event handlers, tests — plus runtime registration, plugin dispatch, reflection, and anything invoked by name from config |
| **B. State & data** | What reads and writes the state involved? | Read sites and *write* sites, active readers and writers, schema, migrations, caches, serialized formats, database triggers/views/procedures, and whether there is a single write path |
| **C. Contracts & boundaries** | What crosses a line if this changes? | Public APIs, exported symbols with external consumers, events/queues, background worker queues, delayed/asynchronous consumers, config keys, env vars, feature flags, cross-service and cross-repository consumers |
| **D. Build, failure & operations** | How is this built, how does it fail, who notices? | Build/CI config and package metadata, generated code and its generator, IaC and deploy manifests, error paths, retries, timeouts, operational tripwires, lock budgets, existing tests covering the subject, logs/metrics/traces, and the reverse-sync rollback path |

Budget each lane: **read-only, no edits, roughly 8 minutes, report what you found and what the budget cut off.** The budget is a prompt instruction, not a timeout — which is exactly why the report-what-you-cut rule is the part that has to hold. An empty lane is a finding, not a failure. Give every lane the same honesty instruction: *`file:line` for everything claimed; anything inferred, unverified, or graph-only is listed as an unknown, never smoothed into the findings.*

No sub-agent capability? Run the lanes serially in the main context, same budget, same schema — and name in the map which lanes you curtailed and where you stopped. Serial is not licence to go shallow; it is licence to record what you skipped.

## Step 4 — What each lane returns

A common envelope plus that lane's own fields from the table above:

```
LANE: <A|B|C|D>
FINDINGS:
  - <file:line> — <what it is> — <why it matters to the change> — [confirmed | graph-only | supplied]
    confirmed = you read the file · graph-only = the index says so, nobody read it · supplied = the user gave it
UNKNOWNS: <what could not be verified, and the one command or file that would settle it>
CUT OFF AT: <where the budget stopped the lane, or "nothing">
```

## Step 5 — Reconcile into the Recon Map

Merge the lanes yourself; do not paste them. Dedupe by `file:line`, resolve contradictions by reading the file, and write the map to `recon-<subject-slug>.md` beside where the plan will live. Long output belongs in the file, never in chat.

```markdown
# Recon Map — <subject>
Commit: <sha> · Mode: <graph+read | grep-only> · Lanes: <which ran>

## Subject and change class
## The seams — where a change here escapes this file
| Seam | Location | Crosses | Breaks if |
## Call paths in
<entry point -> ... -> subject, with file:line>
## State
<read sites / write sites; the single write path, or the fact that there is not one>
## Contracts
<name — consumer — breaking-if — where it is declared>
## Build, failure and rollback today
## Unknowns
| Unknown | Why it matters | What would settle it |
## Current-state radius, one line
<the systems, data, and people that today depend on what this change touches — named, not "various downstream">
```

The Unknowns table is load-bearing. Zero unknowns is an honest result on a small, fully verified subject and a warning sign on a large one — say which case you are in rather than manufacturing a gap to look thorough.

## Step 6 — Hand off

Recon stops at the map. In chat: the verdict line (`Recon complete — N seams, M unknowns, current-state radius: <one line>.`), the file path, the one or two unknowns that would change the plan if they resolve the other way, and the next step.

If the user asked for a plan in the same breath, write it next — recon does not withhold the plan, it grounds it. The plan is a separate artifact from the map, drafted against [swe](../swe/SKILL.md), and its Blast section *starts* from the map's current-state radius and then adds what the plan itself introduces. Copying the radius across unchanged is a Blast failure, not a shortcut.

## Escalation and neighbors

- **recon** — "What is actually there?" Read-only reconnaissance of the current system, before a plan exists.
- **[spike-360](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/4-occasional/spike-360/SKILL.md)** — "Should this authority exist?" Classify first when state is moving; recon then maps what the approved shape has to live with.
- **[swe](../swe/SKILL.md)** — "Does the plan embody our standards?" Its Pillar 0 is satisfied by recon's map; its Blast pillar extends that map per decision.
- **`phase-0-spike`** (`~/.claude/workflows/phase-0-spike.js`) — the deep seam map with contract owners and rollout invariants, for a refactor already committed to. Recon is the cheap universal pass; that is the expensive committed one.
- **`blast-radius` (not shipped here)** — prices a one-way door the map exposes.
- **[debug-mantra](../debug-mantra/SKILL.md)** — traces a fail path for a bug happening now; recon traces edges for a change that has not happened yet.
