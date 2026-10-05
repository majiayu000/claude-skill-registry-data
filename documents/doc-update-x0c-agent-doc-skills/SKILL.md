---
name: doc-update
description: Persist reusable findings and product decisions, repair stale documentation and missed navigation, and review session omissions. Use during work when durable knowledge emerges, including investigation-only Q&A, and at task closure.
---

# Documentation updates

Apply the documentation lifecycle contract in the installed `Project Documentation Management` block. This skill supplies the bounded update procedure; environment instructions own language, permissions and shared-document locations. When `AGENTS.md` needs a deliberate edit, route one bounded change set through the dedicated `agents-md-edit` skill; the coordinator integrates and verifies it. If unavailable, report the missing capability.

## 1. Gather and filter

Review the available session for knowledge that would otherwise disappear:

- Replay user requirements, corrections and vetoes. Check redirects, confusion, repeated requests, better-default expectations, surface-only fixes, unused available resources and inefficient paths. Separate durable intent from temporary scope, examples and unadopted suggestions.
- Replay task-level detours: failed approach, cause, successful remedy and verification. Do not record repetitive tool failures that taught nothing.
- Identify docs invalidated by changes, newly exposed contradictions, and cases where the right doc was missing, misleading or not found.
- Ask whether the workaround would still be necessary with perfect docs. If yes, record an environment-improvement item alongside the documented workaround; do not implement unrelated improvements automatically.

Then apply the precision test: would this spare a new Agent a non-obvious mistake or rediscovery? Preserve relevant business rules, hidden constraints, verified workflows, applicability and evidence. Skip code/Git restatement, duplicates and session-only narrative. Search existing docs before deciding nothing needs updating. Pure Q&A is not a skip condition.

If no new durable knowledge remains, report that no update is needed. If documentation changes are explicitly forbidden, report the unpersisted findings without writing.

## 2. Locate the authority

Read root `AGENTS.md` and follow its document navigation and declared shared standards.

| Finding | Destination |
|---|---|
| Project-wide operating requirement | Matching root `AGENTS.md` section |
| Product behavior, architecture or domain knowledge | Existing matching project doc |
| Reusable task procedure or helper | Matching skill; no product-specific names or paths |
| Cross-project platform constraint or troubleshooting knowledge | Declared shared guide; product doc retains local details and a pointer |
| Recurring environment obstacle | Existing backlog, or an indexed design/troubleshooting entry |

Prefer updating an existing authority. If none exists, use the project's registered doc types: domain KB, guide, design or troubleshooting record. Register a new type's purpose and placement when needed. Do not invent a shared filesystem location; report a missing binding.

## 3. Update and reconcile

1. Write current requirements and reusable knowledge, not a session diary. Label hypotheses and unverified steps; distinguish pending decisions from confirmed facts.
2. Check affected code/path/method anchors against the source. For KBs using the doc-init template, update the physical-path table and affected flow/validation sections after renames, deletions or entry changes; do not maintain source file counts merely to duplicate the code.
3. Correct old conclusions within the concepts touched this session. Verify against authoritative requirements and implementation; a confirmed new product decision may supersede stale implementation. Keep implementation aliases when changing business terminology.
4. When a user explicitly overrides an old source, record the current ruling, rationale and scope so the old source cannot silently reverse it. Mark unresolved contradictions with the decision required.
5. Propagate approved corrections and synchronize affected references under the current task authorization. Do not use a retrospective to overhaul unrelated docs or change unrelated global rules.

## 4. Repair navigation

For each added, moved, renamed, expanded or previously missed doc:

- Ensure exactly one navigation entry at the root or a registered secondary index. Nearby rule pointers may coexist with that entry.
- Describe each document's actual content precisely and concisely. Keep one shared index instruction to read documents whose described content is relevant to the current task; do not turn entries into trigger lists or duplicate policy.
- Update the content summary when document contents change. Preserve valid entries while merging duplicates or removing stale summaries.
- Synchronize old references after moves/deletions and add nearby pointers where the doc supports a rule.
- Keep direct links unless a group makes navigation difficult to scan. Three records alone do not require a secondary index; use doc-compact for large-scale restructuring.

Mechanical link checks can use doc-init's `scripts/doc_nav_lint.py` or doc-compact's `scripts/audit.py`. Their output does not replace checking task coverage and factual consistency.

## 5. Verify and report

Re-read changed passages and navigation; verify links, current conclusions and recorded limitations. Check that a new Agent could perform the affected task from the docs without repeating the discovered detour.

Report changed paths and what was captured or corrected. Name any unpersisted or unverified item. If the session produced no durable change, say so without forcing a document edit.
