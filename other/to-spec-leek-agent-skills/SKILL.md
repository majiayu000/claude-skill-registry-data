---
name: to-spec
description: "Turn the current conversation into a spec (PRD) and save it as markdown under .scratch/: no interview, just synthesis, with Laravel test seams chosen from the tdd ranking rules rather than asked about. Use when the user wants a spec or PRD written from what was just discussed, when a grilling or wayfinder session has settled its decisions, or when an existing spec needs revising in place."
---

# To Spec

Take the current conversation context and codebase understanding and produce a spec (a PRD). Do **not** interview the user: the interview already happened (usually a `grilling` session); this skill synthesizes it.

**Carry the source material through.** Every link, doc, or reference the user brought into the conversation (a vendor guide, API docs, an issue, a thread) is cited in the spec where it applies. Material that was pasted rather than linked has no other home, so save it verbatim beside the spec (`.scratch/<slug>/research/<name>.md`) and link that file. The spec is the only artifact the build sessions inherit: a fact left out of both is gone.

If a load-bearing decision is genuinely unresolved (one the spec cannot be written without) don't guess and don't launch a full interview. Ask just that decision (via `AskUserQuestion` where available, otherwise a plain question in chat: recommended option first, trade-offs per option), or suggest a `grill-me` round if several are open.

**Written once per effort, revised in place after.** One spec covering everything the effort builds, written in a single session. If it came from a `wayfinder` map, that first write closes the map and does not run on it again. Later, if downstream work exposes a wrong or missing decision, re-run to **edit this spec in place**: never write a second spec beside it, and never reopen or re-close the map.

Pipeline position: `grill-with-docs`/`wayfinder` (decide) → **`to-spec`** (write the spec) → `to-tickets` (break it into tickets) → `implement` (build one ticket per session).

## Process

### 1. Explore the repo

Understand the current state of the codebase if you haven't already. Use the project's domain vocabulary throughout the spec (read `GLOSSARY.md`, or the older `CONTEXT.md`, if one exists: `domain-modeling` maintains it) and respect any ADRs in the area being touched (including migration and data-backfill rules in `CLAUDE.md` / `AGENTS.md`). When the conversation relies on a simplifying data or usage claim ("no active subscriptions", "dead table", "zero rows") to drop schema or skip an expand–contract step, verify it against the codebase (`rg` for live callers, admin resources, and seeders) and a read-only count on the configured database before encoding it in the spec.

**Invoked with a `wayfinder` map, read the map and every closed decision ticket's `## Resolution` first**: those resolutions are the authoritative decisions the spec must encode. Don't synthesize from conversation memory alone; a fresh session may not hold what earlier ticket sessions decided.

Check the **constraints** the spec must honour before drafting, since each one found at build time costs a re-grill:

- **Data handling**: which vendors may process this data (a PHI or residency rule can fix the AI or email provider).
- **Launch gating**: anything user-visible that waits on an outside approval, a listing, or a date ships behind a switch.
- **Deploy safety**: the repo's expand–contract and migration rules, for every drop or rename.
- **Architecture rules**: the repo's architecture tests and naming rules (suffixes, locations), which every class and location the draft names must pass.

Each settled constraint goes in the Build Contract. An unsettled one goes in the Needs decision list, and into the Build Contract only once accepted.

Finish exploring only when you can name the domain terms, ADRs, and constraints that bind the spec, the closest existing implementation and tests to imitate (or confirm none exist), and the tracker destination step 3 will use.

### 2. Sketch the test seams

A **seam** is the public boundary the feature will be tested at (`codebase-design` holds the full deep-module vocabulary). Before proposing seams, consult and apply the ranking and selection rules in the `tdd` skill's **Seams: where tests go** section; it is the single source of truth. While sketching seams, look for a **deepening opportunity** (functionality worth hiding behind a smaller, more stable interface) and record it under Implementation Decisions.

**Decide the seams yourself: don't ask.** Seam placement is test structure, which `grilling`'s **What still earns a question** hands to you: the ranking rules settle it, so apply them and move on. Record the chosen set in the spec with a one-line why per seam; the user reviews them as part of the step 3 draft, which is the only gate this step needs. Ask only on a genuine fork, two placements the rules rank equally that would make materially different work, and then ask just that one.

### 3. Write and publish the spec

Write the spec using the template below. Every decision the draft would make that the conversation did not (a new table, flag, setting, switch, or user-visible behavior) goes into a **Needs decision** list above the draft, one line each with your recommendation, and stays out of the draft body. Show the list and the complete draft, then ask each Needs decision item as its own question, your recommendation first (via `AskUserQuestion` where available, with each option's `preview` showing the draft section that choice changes where that helps; otherwise one numbered question per item in chat), and close with one question: publish, or adjust first. Wait for the user to approve publication or request changes. Publish only when every Needs decision item is accepted, replaced, or left open. Write the accepted ones into the body. An item the user left open (skipped, declined the question, or said "publish anyway") goes under **Open questions**, never into the body as decided behaviour. Before publishing, reread the body once: anything the conversation did not settle moves to Open questions. More than three items, or any that touches an ADR, money, or data loss, means the grill ended early: recommend `/grill-me` on them instead.

A spec is a markdown file under `.scratch/`: there is no external tracker. Read the layout from `.agents/issue-tracker.md` (written by `/setup`). If it's missing, try `docs/agents/issue-tracker.md` (legacy), then the path below; suggest running `/setup` once to make it durable.

After approval, publish to `.scratch/<slug>/spec.md` with `status: ready-for-agent` in its YAML frontmatter (or the AFK-ready role string from `.agents/triage-labels.md` when that mapping differs). **Invoked with a map, reuse that map's directory** and set `map.md`'s frontmatter to `status: closed`: the map's job is done. A later in-place revision leaves the map closed.

Approval to publish covers the commit. Unless `git check-ignore -q .scratch` says the repo ignores it, commit only `.scratch/<slug>`. Its parent is `origin/<default>`, or a commit this session made on top of that. Run `git fetch origin` and `git rev-list origin/<default>..HEAD`. When it lists any sha you did not commit in this session (a fresh session committed none, so any listed sha counts), leave the checkout where it is and put the spec on its own branch `docs/<slug>-spec`: `git worktree add -b docs/<slug>-spec .claude/worktrees/docs-<slug>-spec origin/<default>`, or, when that branch already exists (an in-place revision), `git worktree add .claude/worktrees/docs-<slug>-spec docs/<slug>-spec`. Copy `.scratch/<slug>` into that worktree, commit it there with the message below, then `git worktree remove` that path (no `--force`; the branch keeps the commit) and name the branch in the report. `implement` picks the spec up from that branch. Otherwise commit on the current branch: `git add -- .scratch/<slug>`, then `git commit --only -m "docs(scratch): <slug> spec" -- .scratch/<slug>`. The add comes first because `--only` skips untracked files. `implement` carries a committed spec onto its PR branch even before it is pushed.

The spec covers the whole effort. Its short **Build Contract** is the canonical home for invariants, ordering, and shared seams every implementation ticket needs; detailed decisions below it hold ticket-specific context without repeating that contract. If the effort feels too big for one spec, say so and recommend narrowing it rather than writing a second spec beside the first.

## Spec template

```markdown
## Problem Statement

The problem the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## Build Contract

- The cross-ticket invariants every implementation must preserve
- Delivery or expand–contract ordering that constrains more than one ticket
- Shared public seams later tickets can rely on
- Links to named sections below that workers should load only when their ticket reaches them

## User Stories

A LONG, numbered list covering all aspects of the feature:

1. As an <actor>, I want <a feature>, so that <benefit>

## Implementation Decisions

The detailed decisions that were made. Keep Build Contract material in that section only; link to it instead of repeating it here. Examples:

- Schema changes (expand–contract sequencing for live tables)
- Eloquent models and relationships to add or modify
- Validation (FormRequest rules) and authorization (policies, record-level scoping)
- Events, listeners, jobs, notifications
- API contracts (routes, resources, payload shapes)
- Filament resources/pages or Livewire components affected
- Config/env keys, feature flags
- Architectural decisions and their reasoning

## Testing Decisions

- The chosen seams (from step 2) and which behaviors each covers
- Prior art: similar tests already in the codebase to imitate
- Ground rules: test behavior through public interfaces, never presentation
  (no assertions on copy, layout, or CSS); don't test framework behavior;
  do test business rules, validation, persisted data, record-level
  authorization, and side effects (via Queue/Mail/Storage/Event fakes)

## Open questions

Decisions the conversation did not settle, one line each with the recommendation. Tickets that depend on one are blocked until it is answered. Omit the section when there are none.

## Out of Scope

What this spec deliberately excludes.

## Further Notes

Anything else future readers need.
```

## When you're done

Print the end-of-session block using the frame in [`wayfinder/references/pipeline-end-block.md`](../wayfinder/references/pipeline-end-block.md).

```text
---
Pipeline: decide → **spec** → tickets → build   (2 of 4)
Done: <what exists now, with its reference; whether a map was closed>
Next:
  • <condition> → /<skill> <ref>
```

Stage-specific **Next** conditions (only those that apply, most likely first):

- **Spec published, work spans several tickets** → `/to-tickets <spec ref>`
- **Spec revised after its tickets were published** → `/to-tickets <spec ref>` to edit and add tickets for the change; name which existing tickets the revision touches
- **Spec published, work fits one session** → `/implement <spec ref>`
- **A load-bearing decision is still open** → `/grill-me` on that decision, naming it; re-run `/to-spec` after
- **Several decisions open, or the effort is bigger than one spec** → `/wayfinder` to chart it first, on a narrower destination
- **Blocked on knowledge someone else holds** → `/to-questionnaire`; **on a fact worth reading for** → `/research`
- **Stopped before publishing** → say what the draft covers, where it lives, and which sections are unwritten
