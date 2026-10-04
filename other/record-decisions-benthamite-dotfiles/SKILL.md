---
name: record-decisions
description: Extract and record architectural, algorithmic, or design decisions from the current session. Use for an explicit ADR/decision request, authorized end-of-session bookkeeping, or a significant chosen trade-off within an implementation task; not for unchosen proposals or read-only reviews.
user-invocable: true
argument-hint: "[optional: specific decision to record]"
---

# Record decisions

Create or update concise records of actual choices grounded in the current session or an explicit recording request. Loading this skill during an audit or a read-only review does not authorize writing records. Use it for an explicit recording request, authorized bookkeeping, or a significant chosen trade-off within an implementation task's scope.

## Prerequisite and evidence

Resolve the project root and its instructions first. This skill requires an existing `decisions/` directory there. If absent, report `no decisions/ directory` without creating it or invoking `update-log`; first-run setup belongs to an explicitly requested bookkeeping workflow. Reject unexpected symlink destinations before writing.

Use `$ARGUMENTS`, when supplied, to focus the review. Read the existing `decisions-summary.md` and records relevant to the same question before deciding whether anything needs writing. If the summary is missing, defer its creation until a qualifying creation or update exists. Do not manufacture an empty artifact on a no-op run.

A decision normally qualifies when alternatives were considered and one was chosen for non-obvious reasons: architectural choices, algorithmic choices, failed approaches, or design trade-offs. An actual decision the user explicitly asks to record also qualifies without discussed alternatives; state that limit instead of inventing rejections. An unchosen proposal is not a decision. A provisional choice is a decision, but is not final.

By default, exclude routine edits and choices obvious from code; an explicit request to record an actual decision overrides those filters. General session summaries and TODOs without a choice are not decision records. A re-proposed alternative is a reason to check both records and retrieval, not proof that its rejection was never recorded. If the choice is already recorded unchanged, do not duplicate it.

Distinguish observed evidence, reported constraints, inference, and pending validation. Include useful specifics without secrets, private correspondence, or unrelated personal/employer data. Sanitize commands and errors, use repository-relative file references, and apply the repository's publication constraints. Do not copy raw session transcripts.

## Record and summary format

Preserve a documented existing scheme; the following is the default for new records. Keep the record concise without omitting material rationale or uncertainty:

```markdown
## NNN: Title (YYYY-MM-DD)

**Status:** Final | Tentative | Re-evaluate | Superseded

**Decision:** The chosen approach and its consequences.

**Rejected:** Alternatives actually discussed and why; or "Not discussed."

**Evidence:** Relevant observations and any validation still pending.
**Files:** Useful repository-relative paths, if any.
```

Choose one status, not the literal list. `Final` means the choice is settled, not that every claimed result was verified. Use `Tentative` for provisional choices awaiting validation; `Re-evaluate` requires a stated trigger or review date. `Superseded` identifies an old choice replaced by a linked newer record. If an existing project restricts statuses, follow its schema and express supersession with an explicit linked note instead.

Keep the original decision date. Record later amendments with their own dates. Use the current local session date for choices made now; if recording an earlier choice, use its evidenced date or explicitly distinguish the recording date from an unknown decision date.

The default root summary is:

```markdown
# Decisions summary

| ID | Topic | One-line decision | Status |
| --- | --- | --- | --- |
| NNN | Topic | Concise chosen approach | Tentative |
```

Keep rows compact and escape table delimiters in content. The summary is an index, not a replacement for rationale. It is loaded automatically only if the project's actual context configuration arranges that; do not add hooks or instruction imports as part of recording decisions.

## Creation and updates

1. Inventory the directory's filenames and summary IDs. For the default numeric `NNN.md` scheme, parse the entire numeric stem and allocate one above the numeric maximum, with a minimum width of three digits: `999.md` and `1000.md` imply `1001.md`. Never restrict discovery to exactly three digits or reuse gaps. Account for all IDs already reserved in the summary as well.

   This inventory is read-only. If filenames use another scheme, follow its documented allocation rule. Do not silently ignore numbered variants such as `007-topic.md`, duplicate numeric IDs, or dangling/mismatched summary entries. Plan reconciliation from the records where unambiguous, but write only after qualifying work is identified below. Otherwise stop allocation and explain the specific inconsistency. Do not renumber existing history.

2. Classify each qualifying item as a new choice, a supported amendment, or unchanged. Supported evidence/status updates may qualify even when no new choice was made. If every item is unchanged or nothing qualifies, leave every file unchanged, including a missing summary.

3. For an amendment, preserve the original choice, rationale, and date. Add a dated amendment identifying new evidence, corrected factual claims, or the supported status change; update the summary to match. Do not silently replace history. For a substantive reversal, create a new record linked to the old one and add a dated supersession link to the old record. Do not represent the old choice as still current.

4. Allocate and write one new record at a time. Check existing paths and preimages again immediately before changes. Use an available project-supported lock covering record and summary updates when writers may overlap, or exclusive no-clobber publication for new files and equivalent protected updates for existing files; an existence/preimage check alone is not concurrency protection. If the permitted tools cannot protect a conflicting write, stop that write rather than overwrite another record. A newly occupied ID requires re-reading the inventory and reallocating, not force replacement.

5. Add or update the matching summary row without disturbing other rows or unrelated text. For a missing summary, build its index from the existing records plus the qualifying change, not just the latest record; verify their identities/statuses instead of guessing. Recheck the summary's preimage before writing and reconcile concurrent changes rather than replacing them with a stale copy.

   Record and summary writes are not inherently one transaction. If interrupted or partially unsuccessful, report and reconcile the specific mismatch from the surviving records. Do not claim success with a missing row, delete a valid record to conceal partial failure, or roll back another writer's work.

## Verification and report

Re-read every affected record and the summary. Confirm unique identities, correct allocation, preserved historical dates/rationale, supported statuses, matching rows, and valid amendment/supersession links. Check the final diff for unrelated changes and sensitive material. Report the created or amended files only after this reconciliation.

For a no-op, report `no decisions/ directory`, `no qualifying decision or update`, or `already recorded`. Report unresolved numbering, concurrent-write, and partial-write problems explicitly; they are not successful no-op runs.
