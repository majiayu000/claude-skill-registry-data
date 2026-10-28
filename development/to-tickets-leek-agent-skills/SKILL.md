---
name: to-tickets
description: Break a spec into tracer-bullet vertical-slice tickets with explicit blocking edges, settle the build's open decisions, and save one markdown file per ticket beside the spec. Use when the user asks to break a spec or map into tickets.
argument-hint: "[spec path or wayfinder map] (defaults to the conversation)"
---

# To Tickets

Break one spec into **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it. A ticket is one session of build work, and it is the smallest unit the pipeline tracks.

Pipeline position: `wayfinder` (decide) → `to-spec` (write the spec) → **`to-tickets`** (break it into tickets) → `implement` (build one ticket per session).

## Process

### 1. Gather context

Work from whatever is already in the conversation. If the user passes a reference (a spec path, or a `wayfinder` **map** when the effort skips the spec) fetch it and read its full body and comments. On a map, the source is the map plus every closed decision ticket's `## Resolution`.

### 2. Explore the codebase when applicable

When the work targets an existing codebase and you haven't already explored it, inspect the current state. Ticket titles and descriptions use the project's domain vocabulary (`GLOSSARY.md`, or the older `CONTEXT.md`, if present) and respect ADRs in the area. For greenfield or non-code work, continue from the gathered context.

Look for opportunities to **prefactor**: restructure first so the feature lands cleanly. "Make the change easy, then make the easy change." Prefactors become the first tickets.

### 3. Draft the tickets

Cut the spec into **tracer bullet** tickets:

- Each ticket cuts a narrow but COMPLETE path through every layer it needs: for a typical Laravel feature: migration → model/factory → behavior (controller / FormRequest / action / job / Livewire / Filament) → route → feature test. Vertical, never a horizontal slice of one layer ("all migrations", "all the tests").
- A completed ticket is demoable or verifiable on its own; a route you can hit, a command you can run, a test you can watch pass.
- Each ticket is sized to fit one fresh agent session.
- When a spec exists, each ticket points to the parent's **Build Contract** and only the additional spec headings it needs; those heading links route progressive context, they do not restate the spec. On the spec-less path there is no Build Contract to link: carry the decisions the ticket needs inline instead.
- Prefactoring tickets come first.

Give each ticket its **blocking edges**: the tickets that must complete before it can start. A ticket with no blockers can start immediately.

List the **files** each ticket expects to create or edit, from step 2's exploration. Two tickets with no edge between them that edit the same file conflict when built in parallel, so `implement-spec` builds them one after the other; the list is how it knows. A shared registration line (a route, a provider, a translation key) counts too.

**Wide refactors are the exception to vertical slicing.** A wide refactor is one mechanical change (rename a column, retype a shared value object) whose blast radius fans across the codebase so no vertical slice can land green. Sequence it as **expand–contract**:

1. **Expand**: add the new form beside the old so nothing breaks (new nullable column + dual-write; new method delegating to old).
2. **Migrate**: move call sites/data over in batches sized by blast radius (per module, per directory), each batch its own ticket blocked by the expand. A data backfill is its own ticket, a one-time operation leaving no permanent infra.
3. **Contract**: drop the old form once no caller remains, in a ticket blocked by *every* migrate batch. The contract migration is the only destructive step and lands last.

When even batches can't stay green alone, keep the sequence but share an integration branch, all blocking a final integrate-and-verify ticket: green is promised only there.

**Close every breakdown with a delivery ticket.** The last ticket, blocked by all the others, traces each spec requirement to a ticket and lists the before-merge checks and the after-deploy steps (commands, backfills, flags, smoke checks). A requirement it cannot trace is a gap: add a ticket for it. Draft it per [DELIVERY-TICKET.md](DELIVERY-TICKET.md). On a wide refactor, the integrate-and-verify ticket is this ticket.

### 4. Settle the build's open decisions

**Granularity, blocking edges, and the axis you cut along are yours to settle.** Step 3's rules decide them, so don't run a review round on each: `grilling`'s **What still earns a question** keeps mechanical judgment off the user's plate.

Questions a builder would otherwise raise mid-build belong here, while nothing is waiting on them. Run one read-only subagent (a domain-expert agent type when the harness offers one for the spec's domain) over the spec, the drafted breakdown, and the effort's `decisions/` and `research/`. Its brief: list every choice the build will have to make that these documents leave open, each with the tickets it touches, the line that leaves it open, and a recommended answer. Settled choices and pure implementation detail are not open decisions.

Ask them in `AskUserQuestion` batches of up to 4 where available, recommended answer first (otherwise one message in chat), and fold each answer into the tickets it touches. When the sweep finds nothing open, say so. This is the effort's last decision pass: `implement-spec` skips its own sweep while no later commit changes the spec or tickets.

### 5. Publish

Present the finished breakdown as a numbered list: per ticket: **Title**, **Blocked by**, **What it delivers** (the end-to-end behavior it makes work). Then publish without asking: until a build claims a ticket, the user adjusts the published files, or asks you to, as cheaply as a draft.

Write one markdown file per ticket into `.scratch/<slug>/tickets/` (the `tickets/` directory **beside the spec**, created with `mkdir -p` before the first write): there is no external tracker. Read the layout from `.agents/issue-tracker.md` (written by `/setup`) when the repo has one (`docs/agents/issue-tracker.md` is the legacy path); suggest running `/setup` once to make the paths durable. Set each ticket's `status` to `ready-for-agent`, or the AFK-ready role string from `.agents/triage-labels.md` when that mapping differs.

Publish in dependency order (**blockers first**) so each ticket's edges reference real identifiers. Publish idempotently: before writing, read what `tickets/` already holds, if this spec was already broken down, don't mint a second set. A re-run fills gaps a failed mid-loop run left behind, or brings the tickets in line with an in-place spec revision: edit each open, unclaimed ticket whose text the revision changes, add tickets for what it introduces, and name each edit and addition in the report (a claimed or closed ticket the revision invalidates gets a new ticket instead). A new ticket takes the delivery ticket's number, and the delivery ticket moves to the next free one (`git mv` its file and update its `# <NN>` heading), so it stays the highest. A re-run adds each new ticket to the delivery ticket's `blocked-by` and its lists, sets it back to `ready-for-agent` when it was `closed` (a `ready-for-human` one keeps its after-deploy hold, and its new blockers keep it waiting), and adds a delivery ticket when an older breakdown has none.

Write step 4's answers to `decisions/` as one closed decision ticket titled **Build decisions**, per the tracker's format (`type: grilling`, `status: closed`, numbered after the existing decisions, the answers under `## Resolution`, or `None open` when the sweep found nothing), so every file there stays a decision ticket and `implement-spec` can tell the sweep ran.

Do NOT close or modify the parent spec. Invoked directly on a spec-less map, set that `map.md`'s frontmatter to `status: closed`: `to-tickets` is then the handoff that ends the map. Invoked on a spec, leave the already-closed map alone.

Commit the tickets where the spec is committed, so `implement` finds both in one place, with `docs(scratch): <slug> tickets`. Unless `git check-ignore -q .scratch` says the repo ignores it: when the branch `docs/<slug>-spec` exists (`git rev-parse --verify -q docs/<slug>-spec`), follow `to-spec`'s worktree steps on that branch; otherwise commit them exactly as `to-spec` commits a spec, its check for commits this session did not make included, so tickets never ride along on an unrelated branch. `implement` carries a committed but unpushed effort directory onto its PR branch; an uncommitted one it cannot reach from a worktree.

## Ticket template

This template is canonical.

```markdown
---
title: <Ticket title>
status: ready-for-agent
claimed-by:
blocked-by: []
deploy-gate: false
---

# <NN>: <Ticket title>

## Parent

Relative path to the spec (`../spec.md`), or omit on the spec-less path.

## Parent context

Only when a spec exists, omit this whole section otherwise:

- [Build Contract](../spec.md#build-contract)
- [<only another spec heading this ticket needs>](../spec.md#<heading-anchor>)

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, 
not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Behavior statements: what a user/caller can now do, what data is
      persisted, what is forbidden (authorization), never presentation
      ("page shows heading X") or implementation ("uses a repository")

## Files

- `<path this ticket expects to create or edit>`
```

Keep comments out of the frontmatter: an empty `claimed-by` means unclaimed. Blockers live in the `blocked-by` frontmatter (ticket numbers, `[]` to start at once), not a body section. The delivery ticket has its own template in [DELIVERY-TICKET.md](DELIVERY-TICKET.md).

When the spec sequences deploys (expand/migrate/contract, "ship A, deploy, then B", a command that must exist in production before the enforcement that calls it), set `deploy-gate: true` on every ticket that must be live before its dependents are built. Blockers alone do not express this: a worker can close ticket A and start ticket B on the same branch, collapsing three deploys into one PR. `autopilot` stops with `needs_input` after closing a deploy-gate ticket; a human session should likewise commit, deploy, and only then pick up the dependents.

Files are numbered from `01` in topological order: every blocker has a lower number than the ticket it blocks. Numbers order dependencies; they do not serialize independent tickets.

## After publishing

Work the **frontier** (any ticket whose blockers are all done) with `implement`, one ticket per fresh session, or build the whole graph in parallel with `implement-spec`. Unblocked, unclaimed tickets can run in parallel in the same checkout. `implement` claims each ticket before building, by setting its frontmatter `status: in-progress` and `claimed-by:` to a session-unique value (compare-after-write, per the tracker's Claim operation), so a second session skips work already in progress instead of colliding with it.

## When you're done

Print the end-of-session block using the frame in [`wayfinder/references/pipeline-end-block.md`](../wayfinder/references/pipeline-end-block.md).

```text
---
Pipeline: decide → spec → **tickets** → build   (3 of 4)
Done: <how many tickets, how many on the frontier, with refs>
Next:
  • <condition> → /<skill> <ref>
```

Stage-specific **Next** conditions (only those that apply, most likely first):

- **Tickets published with a frontier** → `/implement <frontier ticket>` in one fresh session per ticket; parallelize only independent frontier tickets
- **The user wants the whole spec built in one go** → `/implement <spec path> all` (one branch, a worktree when asked, one PR or a stack of PRs)
- **The frontier is wide and the user wants it fast** → `/implement-spec <spec path>` (parallel implementers, one integration branch, one PR or a stack of PRs)
- **Every ticket is blocked by another that is still open** → `/implement <that blocker>` first; name it
- **A ticket turned out to be a decision, not a build** → `/grill-me` on it (or `/wayfinder` if there are several)
- **Cutting the tickets exposed a gap the spec never settled** → `/grill-me` on the gap, then re-run `/to-spec`
- **Stopped before publishing** → say which tickets exist, which are drafted only, and which blocking edges are unwired
