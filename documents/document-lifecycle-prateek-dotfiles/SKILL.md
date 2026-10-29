---
name: document-lifecycle
description: Manage repository document lifecycles when creating plans or ADRs, updating documented progress, settling or abandoning work, retiring docs, or adopting the workflow in another repo. Ordinary prose edits follow existing conventions.
---

# Document lifecycle

Keep current guidance easy to find and retire work documents when their job is
done. Apply lifecycle changes to the documents affected by the task, in the same
change as the work they describe.

## Choose the boundary

Read the repository's agent instructions and documentation conventions first.
Existing policy wins. In an adopted repo, use this skill as available in your
environment with the repo's lifecycle commands and paths. If the repo selects a
folder with `DOCUMENT_LIFECYCLE_SKILL`, continue from that folder. Only when no
copy is available, run the repo's docs setup command and continue from its
repo-local fallback. A repo that authors this skill uses its own source folder.
Shared policy and tooling live in the skill folder; local guidance records only
configuration and exceptions.
For explicit adoption or migration, read [adoption](references/adoption.md).
In a repo without a lifecycle contract, keep ordinary edits within its existing
structure; do not turn a writing task into a repo-wide migration.

For the adopted schema, state rules, and retirement record, read
[the contract](references/contract.md). The bundled
[validator](scripts/validate-doc-lifecycle.py) provides inventory generation,
Git-history checks, and an advisory review report. It does not decide whether
work is complete.

## While creating or working on docs

1. **Classify the change.** Select the document type using the contract's
   [creation criteria](references/contract.md#frontmatter-and-types). For new
   documents, supply metadata and real related links before drafting the body.
   Finish with a chosen durable home or an explicit decision that the work
   needs no new document.
2. **Reconcile the work.** Compare acceptance items with evidence from the
   implementation, tests, deployment, and required human acceptance. Set the
   document's state using the [state rules](references/contract.md#frontmatter-and-types).
   Finish when every affected acceptance item has evidence or a named open gate.
3. **Update durable guidance.** Put changed operational facts in their owning
   reference, runbook, or skill. Link that home from affected work documents.
   Finish when each changed fact has one authoritative home and affected links
   reach it.
4. **Resolve closure.** Apply the [closure criteria](references/contract.md#navigation-and-retirement)
   to completed work and the [ADR preservation rules](references/contract.md#adr-preservation)
   to decisions. Retire eligible documents below. Preserve uncommitted user edits
   and unresolved acceptance items; report uncertain closure instead of guessing.

## Retire in one change

Follow the [ledger contract](references/contract.md#navigation-and-retirement):

1. Move remaining useful facts to their durable homes. Finish when each fact
   is retained or explicitly judged obsolete.
2. Repair editable incoming links, including frontmatter. Finish when all
   incoming links resolve under the contract's locked-document allowance.
3. Append the retirement row and delete the eligible document. Finish when the
   ledger identifies its destination and the old file is absent.
4. Regenerate the inventory and run current-tree and branch-history validation
   against the repo's actual base. Finish when both pass or a failure is reported
   as unresolved.

## Before handoff

Finish when every document affected by the task has reconciled state, current
guidance, valid links, and passing lifecycle checks, or is explicitly left open
with its missing evidence, acceptance gate, or validation failure. Report those
exceptions and which checks ran. Use the advisory due report for adoption or
broader review; keep ordinary edits scoped to the task.

Automatic skill discovery helps agents reach this workflow. The repo instruction
and validation wiring in the adoption guide make it repeatable across sessions;
a skill alone is not a scheduler or a mandatory hook.
