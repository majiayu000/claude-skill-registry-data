---
name: spinoff
description: "PM-GATED, never EM-initiated. Fork a mid-session topic into a handoff."
allowed-tools: ["Read", "Write", "Bash", "Grep", "Glob"]
argument-hint: "<slug> [optional one-line title]"
---

# Spinoff — Fork a Workstream Into Its Own Handoff

A **spinoff** is a handoff written mid-session by the current EM, addressed to a *future* picking-up EM, describing a workstream the current session does NOT intend to execute. Synonyms used in older artifacts: "orphan-promotion handoff," "ersatz-handoff." `spinoff` is the canonical term.

The mechanical spine — deliverable/initiative id inheritance, `origin_*` provenance capture, frontmatter scaffolding, and the scoped commit — is computed for you. What follows is what it cannot resolve: the evidence is narrowed, you decide.

Compute it via `baton-assemble brief spinoff <slug> [title]`, resolved per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (Shape W on PowerShell hosts). Every `judgment_points[]` entry in the returned object carries its own guidance inline — describing what each disposition means and how to carry it out, never a recommendation to pick from; resolve each one before its gated directive(s) proceed.

Feed those resolutions back by passing `--decisions-file <path>` to `apply`: a JSON object mapping each `judgment_points[].id` to `{"disposition": "<value>"}`. The legal values for a given point are that point's own `dispositions[].value` entries from the same run's `brief` output — read them there rather than guessing. `{"value": "<v>"}` is accepted as an exact equivalent of `{"disposition": "<v>"}`, and sibling keys (a `decision_note`, for instance) are carried through; supplying both keys with disagreeing values fails loud.

---

## Step 0 — PM-authorization gate (hard requirement)

**Spinoffs require explicit PM authorization. The EM never initiates one on its own judgment.** Absent `/spinoff`, the skill name, or a trigger phrase directed at *this specific topic*, STOP — write no file. Topic drift counts: an earlier "spinoff that auth thing" does not authorize a later spinoff of "the migration cleanup."

**Paraphrase is not authorization.** Statements of *eventual intent* — "another session will do this," "we should spin that off sometime," "that's really its own workstream" — are the EM observing a spinoff *might* be warranted, not the PM invoking the primitive. Inferring authorization from intent-shaped prose is the failure this gate exists to catch.

No authorization? Surface a one-line proposal — "Candidate spinoff: `<slug>` — `<one-line topic>`. Authorize?" — and wait. Autonomous skills that previously auto-spinoffed (e.g. `/bug-blitz` Phase 2.1) obey this identically. Nothing below Step 0 runs until the PM says yes.

---

## Step 2 — Authoring discipline

**Do NOT add interactive AskUserQuestion ceremony.** The EM (you) writes the body from current session context. The PM has just told you what the spinoff covers; you have everything you need. A skill that auto-fills the body from heuristics will produce shallow spinoffs the picking-up EM can't act on.

Frontmatter and the canonical body-section skeleton are scaffolded for you; fill each section's content via Edit — the body is the value, never a placeholder stub. `coordinator-doc-new.py`'s `_spinoff_marker` already stamps the trailing greppability marker at scaffold time — do not hand-type it.

Keep a hand-written `summary:` at or under 140 characters, or pass the title through `baton-assemble` instead. `handoff_author_fork.py` truncates `summary` ahead of the claim gate, so an over-cap value does not make the baton unclaimable — but a hand-edit after scaffolding lands untruncated.

**`## Acceptance criteria` is a checkbox list — `- [ ]` / `- [x]`, never prose bullets.** The completeness gate at `/workstream-complete` counts boxes under that heading; zero boxes returns `indeterminate`, which reports as a quiet unverified rather than a wrong. A trailing colon or parenthetical on the heading is fine, and a nested `###` under it still counts — only the boxes are load-bearing.

Then mark the fork in the source session's own task tracker (or session memory) so the current EM does not accidentally absorb the work back into the active session, and surface the written path + workstream slug to the PM before returning to the work the current session was already doing. A spinoff is a fork, not a context switch.

---

## `origin_*` vs `predecessor` vs `forked_from`

**Three distinct axes — never collapse them.** `origin_*` (`origin_session`, `origin_handoff`, `origin_handoff_id`, `origin_plan_id`, `origin_goal_id`) records *where this fork was spawned from*. `predecessor` is the continuation spine — invariantly `none` for every spinoff kind, never a place to encode origin provenance. `forked_from` is branch-point ancestry, a handoff-path.

> **Producer note — `origin_*` is set for you; never hand-set it.** The `handoff.author_fork` op owns all five: it resolves `origin_session` from the current session, derives `origin_handoff`/`origin_handoff_id` from the baton that session holds (`claimed_by` match), and takes `origin_plan_id`/`origin_goal_id` from the caller. `coordinator-doc-new --type=spinoff` deliberately scaffolds **none** of them — their absence from a fresh file is correct, not a gap.
>
> **`handoff.author_fork` is an op name, not a `bin/` executable** — it appears in `directives[]` as `"cli": "handoff.author_fork"`, but nothing under `settings-home/bin` answers to it (exit 127); `baton-assemble apply` dispatches it in-process. Do NOT build a parallel auto-populator, and do NOT hand-write the fields when the directive appears to fail.

**Run `apply`, not `brief`, when you mean to author.** `baton-assemble brief` is read-only — it *emits* `directives[]` as data and executes nothing. `baton-assemble apply` is what walks that list and actually mutates. Hand-executing a brief's directives one at a time is the mistake this paragraph exists to prevent: it silently skips every in-process op in the dispatch table, so the spinoff lands with its `origin_*` provenance missing.

---

## What travels with a spinoff

A spinoff carries only what `handoff.author_fork` derives for it: `origin_*` provenance, deliverable/initiative id inheritance, and the frontmatter scaffold described above. It does NOT carry the forking session's open task list, in-flight review state, or any other session-local working state — those stay with the session that forked it. Everything else the picking-up EM needs must be written into the spinoff body by hand; nothing travels implicitly.

## Anti-scope

- **`reviewed_at_workstream_complete:` does NOT apply to spinoffs.** Spinoffs are forks authored mid-session, not continuations of a session's own work — the workstream-complete review marker tracks what the *current* EM reviewed before handing off a workstream they were executing. A spinoff has no executed diff to review; it is a brief for someone else's future session. Do not add `reviewed_at_workstream_complete:` to spinoff frontmatter.
- **Don't bake content generation into this skill.** No heuristic templates that fill `## Specification` from the slug. The body is the value — the scaffold provides the shape, the EM provides the content.
- **Don't auto-delete or auto-merge spinoffs that get picked up.** Spinoffs follow the standard handoff lifecycle on consumption: `/pickup` mutates frontmatter in place, then the picking-up session's `/handoff` (chain-archival) or `/workstream-complete` moves the file to `archive/handoffs/`. The `<!-- consumed: -->` marker is deprecated — do not write it.
- **Don't extend `kind:` to other values speculatively.** Further extension requires a documented recurring shape, not speculation — the hand-authorable set is deliberately narrower than the schema enum (see `schemas/handoff.schema.json` for the full list, including engine-only kinds no human or EM may scaffold).
- **Don't replace `/handoff` with `/spinoff`.** They serve different needs. The writer-of-spinoff still ends their own session with `/handoff`.
- **Don't migrate prior orphan-promotion handoffs.** Their lifecycle is over; renaming retroactively is churn. New spinoffs use the `kind:` field; old ones stay as-is.

`venue: workstation` marks a spinoff that needs a human or a workstation session at a terminal — a cloud pickup sweep lists it as not-claimable instead of auto-claiming it. Absent, or `venue: any`, means either venue may claim it.

## See also

- `skills/handoff/SKILL.md` — end-of-session continuation handoffs.
- `skills/pickup/SKILL.md` — picking up a handoff (recognizes `kind: spinoff` and emits a banner).
- `CLAUDE.md` § "Handoff Lineage — Single Predecessor, No Adjacency-Inference" — doctrine on why `predecessor: none` is correct for spinoffs.
- `schemas/handoff.schema.json` — frontmatter schema enumerating allowed `kind:` values.
