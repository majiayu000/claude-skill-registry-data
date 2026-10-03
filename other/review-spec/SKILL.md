---
name: review-spec
description: Use when the user says "review this spec", "/review-spec", "check for overlap", "is this spec consistent with our ADRs", or asks to validate a new Gherkin spec or ADR against the existing corpus before it lands. Searches all .feature files and ADRs in the repo, flags duplicate scenarios, conflicting decisions, overlapping feature areas, missing ADR cross-links, and contradictions with the base architecture. Read-only - produces a report, never modifies files.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Bash(fd:*), Read, Grep, Glob
---

# review-spec - find overlap and conflicts before they ship

A spec or ADR is most useful when it's the **only** document making its
claims. Two specs that cover the same feature area drift; two ADRs that
contradict each other create silent ambiguity; a spec that ignores a
relevant ADR ships behaviour that breaks an earlier decision.

`review-spec` reads a target spec or ADR (the one being reviewed) and
audits the existing corpus around it. It surfaces:

- **Duplicates** - scenarios already covered in another `.feature` file.
- **Overlaps** - the new doc and an existing doc cover related ground in
  ways that will drift over time.
- **Conflicts** - the new doc contradicts an existing ADR or another spec.
- **Missing cross-links** - relevant ADRs not referenced; relevant specs
  not referenced.
- **Orphan decisions** - the new doc relies on assumptions that should
  themselves be ADRs.

The skill is **read-only**. It writes nothing; it produces a report with
file paths, line numbers, and quoted excerpts so the user can decide
what to merge, split, or update.

## Phase 0 - Identify the target

Resolve what's being reviewed. The skill accepts:

- A path to a `.feature` file: `/review-spec specs/order-cancellation.feature`
- A path to an ADR: `/review-spec docs/adr/0042-order-cancellation.md`
- Nothing - review the most recently modified spec/ADR (`git log -1 --name-only`).
- A PR context - review specs/ADRs added/modified in the current PR
  (`gh pr diff --name-only`).

For each target, read it in full first. You're going to compare every
scenario, every keyword, every decision against the rest of the corpus -
you need to know what's in scope.

## Phase 1 - Build the corpus

Find every existing spec and ADR in the repo. These are what the target
is compared against.

```bash
# All .feature files
fd --type f --extension feature . | grep -v node_modules

# All ADRs - broad search
fd --type f --extension md . docs/adr docs/architecture/decisions \
  docs/decisions docs/architecture adr 2>/dev/null \
  | grep -E '/[0-9]+|/ADR-' | head -100

# Fallback for non-standard locations
rg -l --type md '^# ADR-?\d+|^## *Status|^---\nstatus:' docs/ . 2>/dev/null | head -100
```

If the corpus is large (>100 docs), you do NOT need to read every one
in full. Use targeted search (Phase 2) and only Read files that match a
keyword from the target.

## Phase 2 - Extract signals from the target

Pull out the things that anchor the comparison:

| Signal | How to find it |
| --- | --- |
| **Feature area / domain keywords** | `Feature:` / `Rule:` titles, common nouns in scenarios. |
| **Actor / role** | `As a <role>`, subjects of `When` steps. |
| **External systems** | Steps naming systems: "payment provider", "webhook", "queue". |
| **State changes** | Verbs in `Then` steps: "is cancelled", "is refunded". |

See references/finding-examples.md for the full signal table (incl. ADR-specific rows).

Build a list of 8-15 search keywords from these signals. These drive the
corpus search.

## Phase 3 - Search the corpus

For each keyword, find files that contain it:

```bash
rg -l --type md --type feature -i "<keyword>" \
  specs/ features/ docs/adr/ docs/architecture/ 2>/dev/null
```

Aggregate the hits. Files that hit multiple keywords are the most likely
overlaps - prioritise reading those.

Read each candidate file (use `tslsp outline` if available, or `Read`
selectively). Look for the five finding types below. See
references/finding-examples.md for worked examples + report-quote
formats for each.

### Duplicates

A scenario in the target whose `Given/When/Then` shape matches a
scenario in an existing file. Semantic match, not just textual.

### Overlaps (feature-area drift)

Two files that cover the same feature area at different levels of
abstraction or with subtly different terminology. They will drift.

### Conflicts (with ADRs or other specs)

A scenario or decision that contradicts another (spec vs. ADR, ADR vs.
ADR, or spec vs. spec). Highest severity. Surface with explicit quotes
from both sides.

### Missing cross-links

The target talks about things owned by an existing ADR / spec but
doesn't link to it. Use the corpus to find ADRs that own the area the
target touches; check whether the target references them.

### Orphan decisions

The target makes an implicit architectural claim that isn't backed by
an ADR (e.g. "customer can cancel via email" with no ADR for the
channel choice).

## Phase 4 - Build the report

Group findings by severity. Concrete, file-and-line specific, quotable.

```
review-spec audited <target> against <N> specs, <M> ADRs.

P0 Conflicts:        <quoted findings or "none">
P1 Duplicates:       <quoted findings or "none">
P2 Overlaps:         <quoted findings or "none">
P3 Missing links:    <file -> other-file pairs or "none">
P4 Orphan decisions: <line refs or "none">

Clean checks passed: <list>
Did not check:       <list with reason>
```

See references/finding-examples.md for the full template.

If there are zero findings, say so plainly. Don't fabricate findings to
look thorough.

## Phase 5 - Suggest follow-ups

For each finding, point at the fix-it skill: conflicts / orphan
decisions -> `/write-adr` or `/write-spec`; duplicates -> consolidate;
overlaps -> consolidate or clarify boundary; missing cross-links ->
add manually (this skill doesn't edit).

## Operating rules

- **Read-only.** Never edits files; produces a report.
- **Don't fabricate.** Findings need real quotes at real line numbers.
- **Severity is for prioritisation.** P0 = correctness; P1-2 =
  maintainability; P3-4 = hygiene. Don't inflate.
- **Don't enforce taste.** Different but reasonable verbs ("cancel" vs
  "abort") are a style note, not a P0.
- **Honour `@deprecated` tags.** Skip from conflict checks; note as
  "deprecated, scheduled for removal".

## Composing with other skills

- `/plan-change` writes a fresh ADR + spec; run `/review-spec` after.
- `/backfill-feature` writes a retroactive ADR + characterization spec;
  worth running `/review-spec` after that too to catch overlap with
  existing docs.
- `/write-spec`, `/write-adr` - fix what review-spec surfaces.
- `/review-feature` - run after `/review-spec` confirms the spec is
  coherent.
