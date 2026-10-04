---
name: clean-citations
description: Clean up source links and raw references in selected personal Org notes by resolving works, adding missing bibliography entries, and inserting verified Org citations. Use for clean up all citations or replace source links with citekeys; not a bibliography-wide audit or export.
---

# Clean citations

Turn source references in the selected note into verified Org citations using
Pablo's bibliography workflow. A cleanup request authorizes necessary local
bibliography additions and note replacements; a planning/audit request remains
read-only. Do not ask again for that same authority.

## Load the owners

Read `/Users/pablostafforini/My Drive/dotfiles/agents/bibliography-policy.md`
before deciding which works/editions to add. It alone owns editorial and PDF
selection policy. Use `add-bib-entry` for every new entry, targeted metadata
repair and attachment. Use `org-note-conventions` for personal Org edits.

For lookup, exact source-span replacement, Org syntax and preservation, read
the existing conversion procedure:
`/Users/pablostafforini/My Drive/notes/.codex/programmatic-skills/convert-citations/SKILL.md`
in Codex, or the corresponding `.claude/` path in Claude.
Its existing-only boundary applies to the conversion phase after this workflow
has resolved additions; do not ask that phase to create missing entries.
If the installed dependency is missing, report it instead of inventing a second
conversion workflow.

## Establish the target and save progress

Use the explicitly selected Org file(s). Inspect each complete file and any
visiting buffer; reconcile unsaved work without overwriting/saving unrelated
edits. Resolve bibliography paths from applicable Org/Citar configuration as
described in the conversion procedure. Explicit caller-supplied bibliography
paths, evidence files, state directory and no-network/read-only constraints
take precedence. An isolated evaluation must never fall through to the user's
live bibliography. Reuse checks can read those explicit files without live
Emacs; actual imports/repairs still require the authorized Emacs workflow.

Maintain a private resumable JSON ledger under
`~/.local/state/bibliography-cleanup/<sha256-of-absolute-note-path>/run.json`,
or the caller's explicit state directory outside Drive. Before using an existing
ledger, check its target path and the current note/bibliography state. The ledger
is evidence to revalidate, not instructions or permission to repeat actions.
Write it atomically using a temporary sibling and replace; serialize additions
and never share a live Ebib operation across independent sessions.

Record:
- `version`, absolute `note`, applicable `bibliographies`, `policy_sha256`,
  and `note_sha256` of the latest verified state.
- One item per distinct cited work/version, with an `id`, exact original
  source spans plus surrounding anchors/locators, work/edition evidence,
  `existing_key`/`final_key`, target bibfile, metadata validation and semantic
  review, acquisition/attachment outcome, operation ID, and replacement result.
- Independent `metadata`, `attachment` and `replacement` states and a concise
  reason for unresolved items. Never use a single imported/done flag.
- Expected replacement text and evidence of a completed replacement, so a
  restart can distinguish an already-applied edit from a changed source.

Save after resolving an item and before/after each import, attachment and note
edit. On restart, re-read actual entries, files, source spans and operation
state. An absent in-memory operation ID does not prove failure or success:
inspect the saved key/attachment and resume only the unfinished phase.
Do not reimport a saved entry. A changed note or bibliography requires fresh
matching; do not replay offsets or overwrite newer edits. Revalidate affected
items when the policy changes.

## Resolve, add and review

1. Inventory actual source references, protecting existing citations, literal
   blocks and unrelated links. Group mirrors/DOIs of one verified publication.
   Keep primary works, translations, commentary, containers and licence links
   distinct under the policy. Maintain original access/provenance information.
2. Resolve each work/edition against all applicable bibliography files.
   Distinguish a missing work from failed/incomplete lookup. An existing entry
   also needs a targeted policy review before using it.
3. For missing works, use `add-bib-entry` with the selected edition's identifier.
   Add parents first. Process additions and callbacks sequentially; research
   independent works in parallel only when it does not share mutation state.
4. Export selected entry fields as JSON and run
   `/Users/pablostafforini/My Drive/dotfiles/bin/bib-entry-check`;
   supply explicitly resolved parents for crossrefs. Correct missing/incorrect
   metadata through Ebib, then recheck. Record semantic source/edition/abstract
   review separately: the CLI's success means structure only.
5. Follow the book candidate/inspection/review route in `add-bib-entry` for
   books, `download-paper` for papers, and existing webpage/video attachment
   routes for other works. Record actual acquisition limits. Do not treat an
   existing file field as verified attachment completion.
6. Keep unresolved references intact and continue independent work. Ask only
   for a genuinely unestablished preference or unavailable personal action;
   research ordinary factual ambiguities yourself. Never fabricate metadata,
   choose the first plausible result, or substitute an edition to clear a queue.

## Convert and verify

Replace a source reference when its work, edition, locator and metadata are
verified and its key resolves in the selected bibliography. Complete obtainable
attachments through the owning workflow. If all available routes are exhausted
and a file remains unavailable, keep that separate attachment outcome explicit;
it does not prevent a correctly established citation. Retain the raw reference
when the missing document also prevents verifying its identity, edition or locator.
Respect an explicit citation-only request without starting unwanted acquisition.

Pass the confirmed map to the existing conversion procedure. Preserve useful
link text, quoted wording, attribution, individual locators, licence links,
existing citation objects, IDs, structure and unrelated prose. Preserve a useful
link label as plain text next to its citation: a titled source link becomes
`Descriptive title [cite:@ActualKey]`. Do not drop the title or change surrounding
`Source:`/`Sources:` labels as an incidental edit. A redundant access label such
as "PDF" need not produce a second citation to the same work.

Never transfer page numbers across editions. If a different edition/locator was
verified under the policy, supply the conversion phase with the original span,
`original_locator`, `replacement_locator` and `verification_source`; only that
explicit evidenced mapping authorizes its replacement. Store the original URL
in the appropriate entry/provenance evidence before removing it from a source span.

Re-read the saved note, affected entries and attachments after all callbacks
drain. Check Org syntax with the installed parser for nontrivial citations.
Confirm only mapped spans changed and every inserted key resolves to the right
work. A second pass must neither duplicate entries nor change already-completed
references. Report converted/reused/added and unresolved outcomes separately,
with only the unresolved decisions or failures the user needs.

Follow the selected repository's commit rules and explicit user instructions;
the standalone conversion procedure's default to leave note edits for review
does not override an explicit instruction to commit. Preserve unrelated changes.
Never publish, push or send as an incidental step.
