---
name: yq-doc-maintenance
description: 文档出现腐化、冲突、重复、导航或归档混乱时使用。
---

# Documentation Governance

Maintain a coherent documentation system whose claims have clear owners and can be checked against the project. Start with ownership and structure; edit prose only after the source of truth is known. This skill covers Markdown, READMEs, tutorials, runbooks, reference docs, decision records, postmortems, JSDoc, and code comments. Use [yq-technical-writing](../yq-technical-writing/SKILL.md) for sentence-level coverage and clarity, and [yq-remove-reasoning-leaks](../yq-remove-reasoning-leaks/SKILL.md) for authoring-session residue. If the audit exposes implementation, test, or gate complexity rather than a documentation-ownership problem, invoke `$yq-simplify-code` for that candidate instead of hiding a behavior change inside documentation cleanup.

This is guidance, not a universal folder layout. Discover and preserve the repository's own documentation contract.

## Establish the documentation contract

1. Confirm the requested scope and whether the task is an audit, a proposal, or an authorized edit. Use the narrowest defensible scope from the request and current diff; do not silently expand a focused task into a repository-wide rewrite.
2. Snapshot the audit identity: repository, checkout or worktree, branch, revision, dirty state, and applicable instructions. Recheck it before reporting. If the worktree changes during the audit, stop combining observations, anchor completed findings to the captured revision, and list later changes as uninspected.
3. Read applicable `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, root and package READMEs, documentation indexes, architecture/decision records, contribution guides, and CI or package scripts that validate docs.
4. Identify excluded or derivative areas: third-party sources, generated catalogs, build output, recorded fixtures, snapshots, vendored documentation, and frozen archives. Edit an owner before regenerating a derivative artifact.
5. Record how this repository expresses intended behavior, observed behavior, rationale, and process. Code or runtime evidence can establish what happens; it does not automatically overrule a current product specification. When those disagree, label the mismatch instead of silently choosing one.

Treat dates, file size, link count, and directory location as discovery clues, not proof that a document is authoritative or obsolete.

For a long-lived repository, multiple documentation roots, or reports of widespread rot and conflict, read [the large-repository audit playbook](references/large-repository-audit.md) before changing files.

## Map the corpus before restructuring it

Inventory tracked documentation and relevant untracked files without traversing dependency stores, build caches, or unrelated large artifacts. Include ignored-but-relevant documents or evidence only through bounded, known roots. Prefer the Git index and constrained `rg --files` queries over a whole-drive scan. Audit each relevant worktree against its own revision and status; never merge conflicting observations from different worktrees into one unlabeled fact set.

For each document in scope, determine:

- its subject and intended reader;
- its form: orientation, tutorial, runbook, reference, decision record, postmortem, generated/recorded artifact, or archive;
- the canonical owner of each important claim;
- its authority tier and lifecycle: canonical, summary, derivative, historical, task-state, or external evidence; active, frozen, generated, or local-only;
- its freshness contract: owner, as-of point, invalidation event, and explicit supersession relation when one exists;
- its direct children and inbound links;
- the code, config, schema, command, runtime evidence, or decision that can verify it;
- any referenced spreadsheet, PDF, JSON, screenshot, bundle, or external artifact needed to verify a claim, without treating that evidence as ordinary prose to rewrite;
- whether it is current, partially stale, fully superseded, duplicated, conflicting, misplaced, or intentionally historical.

A document can be structurally misplaced while every sentence is correct. Fix information architecture before polishing those sentences.

## Review structure before prose

Apply this order to each human-facing document:

1. State the document's own subject and keep full detail about that subject.
2. Summarize direct children by purpose and responsibility; link deeper mechanisms to their owning documents.
3. Classify the document by intended use rather than filename. A tutorial leads ordered work to an observable result. A runbook supports an operational procedure and recovery. A reference supports lookup without sequential reading. A decision record preserves rationale and alternatives. A postmortem preserves incident evidence and causality.
4. Trace tutorial prerequisites and move optional or advanced material out of the critical path.
5. Split substantial mixed forms. Keep a small secondary form only when a clearly labeled section is easier to use than another file.

Do not impose a new taxonomy when the repository already has a coherent one. Propose a taxonomy only when missing ownership is itself causing duplication or conflict.

## Treat documentation budgets as routing signals

When the repository enforces word, line, section, or file-count budgets, inspect the gate's report before editing and apply this order:

1. **Relocate** detail owned by a child component, advanced guide, decision record, postmortem, generated reference, or historical artifact.
2. **Condense** duplication, narration, obsolete status, and implementation walkthroughs while preserving every load-bearing proposition.
3. **Raise or refine the budget** only when the remaining material belongs on that surface and the repository permits an explicit, justified exception.

Do not optimize prose to an arbitrary number, delete contracts to make a gate green, or treat an unbudgeted large file as automatically defective. When the project tracks documentation size, report the measured delta and any deliberately long exception.

## Reconcile stale, duplicated, and conflicting claims

Work at the claim level rather than declaring whole files "good" or "bad."

1. Build a conflict set containing the claim, every location that states it, the evidence available now, the intended owner, and the unresolved question.
2. Choose the owner by responsibility and audience, not by whichever copy is newest or longest. Preserve a concise consumer-facing contract locally when readers need it; link to the owner for rationale, algorithms, history, and extended examples.
3. Repair the owner first, then update summaries, translations, generated references, examples, and navigation. A generated catalog is changed through its source or generator.
4. Replace redundant explanations with links. Keep necessary local facts such as preconditions, failures, ownership, and consequences even when their rationale lives elsewhere.
5. Classify supersession precisely. Partial supersession keeps surviving contracts and cross-links. Full supersession requires that no current behavior, compatibility obligation, schema, migration, supported workflow, or unique rationale remains solely in the older document.
6. Archive or delete only within the task's authority and the repository's retention rules. Frozen history remains frozen; repair active inbound links rather than modernizing an archive.

An outdated command, renamed path, missing target, contradictory default, or unsupported status claim is evidence of rot. Age alone is not. If documentation describes intended behavior that implementation does not satisfy, report or fix the product mismatch under the appropriate task instead of rewriting the promise to match the bug.

Before moving or renaming a document, find inbound links, path references, and heading fragments. Treat the move as one atomic change: new home, old-home removal or redirect if the project supports one, navigation update, and every resolvable inbound reference repaired.

## Classify decision records by future value

Judge proposals, ADRs, design notes, and implementation records by the decisions they can still inform. Age, size, and completion status are discovery clues, not archive criteria.

- **Proposed:** keep an active proposal available while the decision remains open. Reject it honestly when it is no longer worth pursuing; do not archive an unresolved proposal as if it were settled.
- **Implemented — keep active:** retain rationale, alternatives, negative guarantees, ownership boundaries, compatibility rules, security constraints, or reintroduction conditions that can guide a future change.
- **Implemented — archive:** archive a completed record when current behavior is owned elsewhere and its remaining content is one-off implementation or process history with little future decision value.
- **Rejected — keep as a guardrail:** retain a rejection when the losing option remains a plausible, tempting mistake and the record explains why it loses.
- **Rejected — remove:** remove it when the idea is obsolete, superseded, no longer plausible, and unlikely to prevent repeated debate. Repair or remove inbound links at the same time.

When a new record supersedes an older one, inspect the related active records in the same scope. Cross-link partial supersession; for full supersession, transfer unique rationale, alternatives, obligations, and reintroduction conditions to the current owner before archiving or deleting the older record. Follow the repository's existing retention format. This classification does not require a new archive layout, manifest, hash, or validation gate.

## Keep durable evidence, remove sediment

Keep non-obvious contracts, rationale, alternatives, consequences, operational recovery, compatibility obligations, verification evidence, and named coverage gaps. Remove or relocate:

- duplicated explanations and hand-written inventories owned by code or generators;
- completed migration checklists presented as current work;
- temporary status reports that claim to be evergreen reference;
- authoring-session narration, review choreography, and dead citations;
- implementation walkthroughs that add no contract beyond the code;
- stale examples whose commands or outputs no longer reproduce.

If removing prose would change a promised behavior rather than its explanation, treat it as a product or architecture decision. Use the repository's existing ADR, RFC, issue, proposal, or decision-note mechanism; do not hide that decision inside a documentation cleanup.

## Validate against this repository

Discover the actual validators from package manifests, task runners, CI, contribution docs, and `--help` output. Classify their side effects before execution. In a read-only audit, run only checks proven not to rewrite docs, generate output, mutate databases, or create runtime state; otherwise inspect the check and report it as unrun. Select checks for the surfaces touched and do not transplant commands from another project. If no validator exists, use the bounded fallback checks in the large-repository playbook.

At minimum when applicable:

- run the repository's documentation generator or sync check;
- run link and anchor validation, including code references to documentation paths;
- execute or smoke-test changed commands and examples through their real entry path;
- update paired/localized documents according to the repository's own policy;
- run tests or snapshots for model-, CLI-, or UI-visible wording;
- run `git diff --check` and search for old paths or distinctive superseded claims;
- inspect the final diff for derivative, archive, vendor, or out-of-scope changes.

Report the corpus boundary, audit revision and status stability, documents and claim families inspected, canonical owners chosen, conflicts resolved or deferred, files moved/archived/deleted, deliberate keeps, and checks actually run. A successful link checker is structural evidence, not proof that the prose is true.
