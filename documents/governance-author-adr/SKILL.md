---
name: governance-author-adr
description: >
  Suggest and author Architecture Decision Records (MADR-style) in docs/adrs/.
  Use when a load-bearing decision is being made or has just been made ("we
  decided to...", "let's go with X over Y", "should this be an ADR?", "record
  this decision", "write an ADR", "supersede ADR NNNN"), or when reviewing a
  plan/change that implies an unrecorded architectural choice. Also use to
  detect and flag decisions that ought to be recorded. Do NOT use for the
  project-wide constitution (that is the governance-constitution skill), for
  ordinary feature docs, or for tracker tickets.
---

# Author ADR

Owned by the **Architect** persona (also serves the architecture step in elaboration). Invoked as `/governance-author-adr`.

Detect, suggest, and author **Architecture Decision Records**. An ADR captures *why* a
load-bearing choice was made, so a future reader (or agent) does not re-litigate it or
unknowingly violate it. ADRs are decision history: append-only, superseded but not
deleted, read on demand (never preloaded into context).

## Use the repo's own template and rules

Before writing, **read the repo's ADR template and index** so output matches what is
already there:
- Template: `docs/adrs/0000-template.md` (or the repo's equivalent). Mirror its exact
  sections and frontmatter. Do not invent a different format. If `0000-template.md` exists
  but is missing required sections (Context, Decision, Consequences, Alternatives considered,
  Verification, References), notify the user of the specific missing sections and ask whether
  to proceed using the MADR standard template as a fallback or to fix the repo template first.
- Index/README: `docs/adrs/README.md`. Follow its conventions for listing and status.

If the repo has no `docs/adrs/` directory, stop and tell the user: "No ADR directory found.
Before authoring an ADR, I will create `docs/adrs/` with a `README.md` index and a
`0000-template.md`." Do not author the target ADR until the user confirms and the directory
is created.

Respect the repo's documentation rules, which for these repos include: **no source line
numbers anywhere** (reference code by file path + symbol name), and **no em-dashes** (use
commas, colons, parentheses, or " - "). Link to artefacts; do not paste them in.

## What counts as "load-bearing" (when to suggest an ADR)

Suggest an ADR when a change does any of these, and there is no existing ADR covering it:
- introduces, replaces, or splits an architectural pattern or boundary (e.g. a new
  handler/service split, a persistence choice, an auth model);
- makes a cross-cutting tradeoff a future reader would ask "why" about;
- **deviates from an existing convention or a constitution clause** (this especially
  needs a record, or a constitution amendment);
- chooses one technology/approach over a viable alternative with lasting consequences.

Do not propose ADRs for routine, reversible, or local choices. Noise erodes the corpus.
When unsure, ask: "would someone six months from now be confused or annoyed if this
choice were undocumented?"

## Mode selection

If the user has not explicitly requested authoring (e.g. said "write", "author", "draft",
or "record") and no existing ADR is mentioned as the target for supersession, default to
**suggest** mode and ask for confirmation before proceeding to **author** mode.

## Modes

- **suggest** - state that a decision looks load-bearing, summarise it in one or two
  lines, and ask whether to author an ADR. Do not write anything yet.
- **author** - draft a new ADR and (on confirmation) write it.
- **supersede** - author a new ADR that replaces an older one.

## author workflow

0. **Check for duplicates.** Before allocating a number, scan existing ADR titles and Context sections for substantial overlap with the proposed decision. If a likely duplicate is found, surface it to the user and ask whether to supersede the existing ADR, complement it with a narrower record, or cancel.
1. **Allocate the number.** List `docs/adrs/`, find the highest `NNNN`, increment, zero-pad to 4 digits. Filename: `NNNN-<kebab-short-title>.md`. If no numbered ADR files exist yet (only `0000-template.md` or an empty directory), start numbering at `0001`.
2. **Fill the template from reality.** Complete every section of the repo template:
   - **Context** - the forces and constraints *as they are now*; verify load-bearing facts against the code before stating them (read the file/symbol). If a file or symbol cited in the decision cannot be read or does not exist, record it as an open question in the Context section using the format: "[UNVERIFIED: <claim> - could not read <path/symbol>]" and notify the user before confirming the draft. If the Context references a previous implementation or migration that was abandoned or reverted, identify it by its merged PR number or a short descriptive phrase (e.g. "the Redis-based session store introduced in the Q1 refactor"). Never reference an unmerged commit hash, as it may be rebased or force-pushed away.
   - **Decision** - what was decided, plainly; include a short code or config excerpt (max 10 lines) only when the Decision section would otherwise leave the exact interface, schema, or config key unspecified; name the files/types/patterns it touches.
   - **Consequences** - Positive, Negative (be honest; this is the section readers trust most), Neutral.
   - **Alternatives considered** - each with a one-sentence "rejected because".
   - **Verification** - how someone confirms a change in this area is correct; what tests do and do not cover.
   - **References** - files by path + symbol, merged PR numbers, external links.
3. **Confirm the draft with the user.** Present the draft for review. During confirmation, ask whether the decision status should be `Proposed` (team has not yet formally agreed) or `Accepted` (team has already agreed). Default to `Proposed` if uncertain. Set the date to the current date.
4. **Write the file** once the user confirms the draft and status.
5. **Update the index** (`docs/adrs/README.md`): add the new ADR with its status.
6. **Offer the backlinks.** Suggest running `governance-enrich-ticket` to link this ADR onto the originating story, and `governance-constitution` if the decision implies a new or changed non-negotiable. Do not perform those writes from here.

## supersede workflow

1. Author the new ADR as above; in its frontmatter set `Supersedes: ADR NNNN`.
2. In the old ADR, set `Status: Superseded` and `Superseded by: ADR <new>`. Keep the old ADR's body intact - it is history. If the old ADR cannot be found at the expected path, or its frontmatter lacks a `Status` field, stop and report the problem to the user before making any writes. Do not infer or reconstruct the old ADR.
3. Update the index to reflect both statuses.
4. Confirm both diffs before writing.

## Guardrails

- **Verify before asserting.** Every load-bearing fact in Context/Decision must be checked against the codebase first. If you cannot confirm it, write it as an open question, not a fact.
- **Confirm before writing**, and never overwrite an existing ADR's history when superseding - only flip its status fields.
- **One decision per ADR.** If a change carries two independent decisions, write two.
- **No line numbers, no em-dashes, no pasted artefacts.** Match the repo template exactly.

## Next steps

- `/governance-enrich-ticket` (any) - backlink the new ADR onto its originating story and add a dated decision-log line.
- `/governance-constitution` (Lead) - only if the decision implies a new or changed non-negotiable.
- `/governance-check-graph` (Lead) - once the ADR is linked, confirm its `story:` and `relates:` front-matter resolves.
