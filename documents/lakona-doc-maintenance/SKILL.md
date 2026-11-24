---
name: lakona-doc-maintenance
description: Audit Lakona contributor documentation and report findings, or apply authorized cleanup to stale plans, duplicate authorities, and documentation maps within the requested scope.
metadata:
  internal: true
---

# Lakona Doc Maintenance

Keep the contributor path focused on current rules and architecture. During
authorized cleanup, preserve useful present-day contracts and delete obsolete
material instead of archiving it.

## Mode And Authorization

- **Audit:** inspect and report findings, evidence, and proposed dispositions.
  Do not edit or delete project files, move contracts, update maps, or advance
  versions. An audit or review request alone does not authorize cleanup.
- **Cleanup:** an explicit cleanup request or request to fix identified findings
  authorizes changes within that scope. Reuse existing authorization; do not ask
  again for routine edits it covers. Unselected findings remain proposals.

Honor instructions to report first and wait for confirmation. If only an audit
is requested, finish with its report; do not continue into cleanup automatically.

## Scope And Reading

Follow `CONTRIBUTING.md` and reuse applicable instructions already read.
`docs/**` contains durable maintainer documentation. User-facing content,
including root and package README files, is outside cleanup scope unless
requested, except for link repairs needed by the authorized cleanup. Repair
those links and any directly associated link labels without expanding into a
user-facing content rewrite.

| Work | Reference to read |
| --- | --- |
| Classify a document, merge duplicates, or decide what to remove | [classification.md](references/classification.md) |
| Assess documentation quality | [audit-checklist.md](references/audit-checklist.md) |
| Run a full audit's inventory, searches, and link verification | [operations.md](references/operations.md) |

A full audit completes six independent passes: factual consistency, ownership,
stale plans, duplication, competing authorities, and transitional wording.
Read the complete audit checklist for that mode. For reduced scope, read and run
each affected pass; justify any not-applicable decision with evidence. The full
operations reference is not required reading for a small scoped correction.

## Work And Completion

1. Identify the requested documents and their incoming references. Use `rg` to
   discover maintained files, references, and relevant headings.
2. Apply the relevant classification and audit guidance. Check factual claims
   against implementation, tests, configuration, or generated output.
3. For audit mode, report evidence, findings, proposed dispositions and coverage
   limitations. Give clear/findings/not-applicable results for each required
   pass, then stop without applying the proposals. Full audits also complete
   the operations reference's audit verification.
4. For authorized cleanup only, check incoming links before deleting. Move any
   durable rule into its current authority and update affected links and the
   `CONTRIBUTING.md` map.
5. Edit within scope. Repeat affected checks after edits; leave no conflicting
   authority, broken incoming reference, or duplicate mutable fact caused by
   the cleanup. Remove temporary planning docs created during the cleanup.
6. Report the applied changes, evidence and results for affected passes.
   Scoped corrections verify affected links and `git diff --check`.

Follow the repository's validation stopping rules. Do not present a partial
audit as complete or infer correctness merely from repeated documentation.
