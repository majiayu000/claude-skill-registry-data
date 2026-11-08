---
name: forge-plan-large
description: "User-invoked only: /forge-plan-large. Plans work too big for one session (groot plan, meerdere sessies, roadmap, plan in kaart): local ticket map, frontier, fog, step briefs."
disable-model-invocation: true
---

# forge-plan-large: plan work that does not fit in one session

**Owner-invoked only** (`/forge-plan-large`). The model never loads this skill by itself. For one deliverable, use
`forge-prd` or `writing-plans` instead.

Some work is too big, and too unclear, for one agent session: the way from here to the result cannot be seen yet. This skill
charts that way as a **local markdown map** of decision tickets and resolves them **one ticket per session** until nothing is
left to decide. Then it turns the cleared route into **cold-start step briefs** that any fresh Boss can execute.

## Two phases
1. **Wayfinding** (decide): a map of decision tickets with a frontier, fog of war and an out-of-scope list. Its output is
   decisions, not deliverables.
2. **Blueprint** (build plan): once the map is clear, a numbered list of package-sized steps, each with a self-contained brief,
   a wave, a GOAT route and verification commands. Building then goes through `forge-team-orchestration`, `forge-build` or
   `forge-prd`, not through this skill.

**Plan, don't do.** If you feel the pull to just build, you have reached the edge of the map: hand off. The map's **Notes** may
explicitly allow execution inside the map for one effort. Without that note, produce decisions.

## Where it lives
`docs/plans/<slug>/MAP.md` plus one file per ticket: `docs/plans/<slug>/tickets/T-<nnn>-<short-name>.md`. These are tracked
files that the owner can read in any editor. They are **not** the Forge Ticket Board (`.claude/forge-tickets/`, which holds
implementation tickets from `forge-prd`). There are no GitHub issues and no labels. Every field is plain markdown. Templates
and the exact fields: `references/map-format.md`.

- **MAP.md** is the index, loaded once per session: Destination, Notes, Decisions so far (one line per closed ticket, linked),
  Not yet specified (fog), Out of scope, and Plan changes (the mutation log). The map never repeats a decision. It gives the
  gist and links to the ticket.
- **A ticket** is one question sized to one session, with a `Type`, `Status`, `Blocked by`, `Claimed` and, once closed, a
  `Resolution`.
- **Refer by name.** In everything the owner reads, name a ticket by its title, with the id inside the link. A list like
  "T-004, T-007, T-009" is unreadable.
- `MAP.md` is a hotspot: only the session holding the current claim edits it, and it edits only its own ticket's line plus
  newly created tickets.

## Ticket types and who resolves them
Every ticket is **HITL** (needs the owner live) or **AFK** (an agent alone).

| Type | Mode | Resolved by |
|---|---|---|
| research | AFK | A Search Boss card (sonnet/low), or the `deep-research` workflow for source-verified depth. Findings go to `docs/plans/<slug>/research/T-<nnn>.md`. Several research tickets may run in parallel. |
| prototype | HITL | A cheap, rough artifact to react to (outline, stub, mock screen), made by UI Boss or Build Boss inside `_scratch/` or the plan folder, never in product code. The owner reacts; that reaction is the answer. |
| grilling | HITL | The default type. A live interview with the owner through the `grilling` skill. The agent never answers its own questions on the owner's behalf. |
| task | AFK or HITL | Work that must happen before a decision can be made (gather data, check an API's shape). Anything owner-gated (an account sign-up, credentials, spend, outbound, production) becomes a precise checklist in the owner queue, never an agent action. |

## Frontier, claim, fog
- **Blocked:** a ticket lists `Blocked by: T-002, T-005`. It is unblocked when every ticket it lists has `Status: closed`.
- **Frontier:** the open, unblocked and unclaimed tickets. That is the edge of what is known.
- **Claim before work.** The first thing a session does is write `Claimed: <run id or session> <date>` into the ticket and
  save it. Then it re-reads the file: if a different claim is there, it backs off and picks another frontier ticket. An open
  ticket with an empty `Claimed` is free.
- **Fog of war** ("Not yet specified"): decisions you can see coming but cannot yet phrase sharply. The test is whether you can
  *state* the question precisely now, not whether you can *answer* it. A sharp question becomes a ticket even if it is blocked.
  Fog is coarser than a ticket: one patch may later become several tickets, or none.
- **Out of scope:** work beyond the destination. It never graduates from fog. When an existing ticket turns out to be out of
  scope, close it with a one-line reason, add it to Out of scope, and keep it out of Decisions so far.

## Invocation A: chart the map (one session)
1. **Name the destination** with the owner (`grilling`): the spec, decision or change this effort is heading for. It fixes the
   scope, so settle it first. Read the codebase first when it is unfamiliar (`forge-deeplearn`).
2. **Map the frontier breadth-first:** fan out across the whole space, not deep into one thread. If no fog appears and the
   whole job fits in one session, stop: no map is needed. Ask the owner how to proceed (usually `forge-prd`).
3. Write `MAP.md` with Destination and Notes filled in, Decisions so far empty, and the fog sketched.
4. Create the tickets you can state now, then wire `Blocked by` in a **second pass** (ids exist only after creation).
5. Dispatch the research tickets in parallel as routed, read-only cards. Their findings land in the plan folder.
6. Stop. Charting does not resolve other tickets.

## Invocation B: work the map (one ticket per session)
1. Load `MAP.md` only, not every ticket body. Open other tickets only when needed.
2. Take the ticket the owner named, else the first frontier ticket. **Claim it first.**
3. Resolve it according to its `Type`, and read any skills the map's Notes name.
4. Record: write the `Resolution`, set `Status: closed`, add one line to Decisions so far.
5. Create newly surfaced tickets, graduate the fog the answer cleared, rule out-of-scope tickets out, and update or close tickets
   the decision made obsolete. Log every such change under Plan changes.
6. Never resolve more than one ticket per session. Research tickets are the exception and may run in parallel.

## Invocation C: write the blueprint (when no tickets and no fog remain)
Turn the cleared route into **3 to 12 package-sized steps** in `docs/plans/<slug>/BLUEPRINT.md`:
- **Cold-start brief per step:** context, owned files, tasks, verification commands, exit criteria, rollback, and GOAT route. A
  fresh Boss must be able to run any step without reading the earlier ones or this chat.
- **Waves by "no shared files or outputs":** two steps share a wave only when their file sets are disjoint and neither consumes
  the other's output. Ownership and wave rules: `forge-team-orchestration`.
- **Invariants** checked after every step (for example "full suite green", "no import of X in core").
- **Adversarial review gate:** a deep-route reviewer (Review Boss, opus/xhigh) checks the blueprint against
  `references/step-briefs.md` before any step starts. Fix every critical finding first. This is not Fable; Fable is only the
  escalation after a failed check (GOAT).
- **Mutation protocol:** split, insert, skip, reorder or abandon a step only with a dated line under Plan changes (what, why,
  who). Steps keep their ids; an abandoned step stays visible.

Step brief template, review checklist, anti-patterns and the mutation rules in full: `references/step-briefs.md`.

## Rules
- No git push, no pull requests, no deploy and no outbound action from this skill. Hard-gates stay owner-only.
- Every research claim in a resolution links its source or `file:line`. "Unknown" is an allowed answer; an invented one is not.
- Owner-gated items wait in one batched owner list at the end, while independent tickets keep moving.

## Provenance
- **mattpocock/skills**, `skills/engineering/wayfinder/SKILL.md` (and `agents/openai.yaml`, read only for its invocation
  policy), commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, MIT (Copyright (c) 2026 Matt Pocock). Taken and rewritten: the
  destination-first map, the map as an index rather than a store, refer by name, ticket types with HITL/AFK, the frontier
  definition, claim before work, fog of war with the "fog or ticket" test, out of scope that never graduates, create-then-wire,
  one ticket per session, and model invocation off. Excluded: the GitHub issue tracker, labels, native blocking and assignees
  (replaced by local markdown fields), the `/setup-matt-pocock-skills` dependency, the `domain-modeling` and `prototype` skill
  calls (not in this project), and the pushed `research/<name>` branches.
- **affaan-m/everything-claude-code (ECC)**, `skills/blueprint/SKILL.md`, pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`, MIT (Copyright (c) 2026 Affaan Mustafa; the skill's own metadata names its origin
  as community, inspired by antbotlab/blueprint, which was not fetched). Taken and rewritten: cold-start step briefs, 3 to 12
  steps of one package each, parallel steps by "no shared files or output dependencies", a model tier per step (mapped to GOAT
  routes), invariants per step, the adversarial review gate, and the plan mutation protocol (split, insert, skip, reorder,
  abandon, with an audit trail). Excluded: the `/blueprint` command, the git/gh/branch/PR/CI pipeline, the pre-flight `gh auth`
  checks, the `plans/` folder and memory-index registration, and the install/update commands. The pinned file only names an
  anti-pattern catalog and a review checklist without listing their contents, so those lists in `references/step-briefs.md` are
  Forge-native.
- Adopted as markdown only; nothing was copied or run as code. MIT notice: "Permission is hereby granted, free of charge, to any
  person obtaining a copy of this software ... The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software."
