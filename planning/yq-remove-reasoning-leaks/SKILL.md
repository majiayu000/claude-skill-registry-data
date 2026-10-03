---
name: yq-remove-reasoning-leaks
description: 技术文本残留评审过程、草稿引用或推理旁白时使用。
---

# Trim Reasoning Leakage

Reasoning leakage is durable repository prose written from the authoring session's vantage rather than the project's current, resolvable state. It cites artifacts only that session could see, narrates a change instead of the resulting behavior, argues with a departed reviewer, or walks through reasoning already expressed by code.

The fix is not indiscriminate deletion. [Technical prose standard](../yq-technical-writing/SKILL.md) owns the complete-proposition rule: restate every surviving factual clause so it stands at the current revision, then remove the transcript around it. Delete a passage outright only when it carries no durable proposition.

This is guidance, not a script. Pattern searches nominate candidates; semantic review decides them.

## The one test

For every suspect passage ask:

> Could a reader at the current revision, without the session transcript, review conversation, branch stack, or uncommitted draft, resolve every reference and verify every claim?

If not, restate the surviving facts from the repository's vantage and remove the unresolvable framing. If yes, the passage is not reasoning leakage merely because it mentions history. Current-state surfaces can still contain unnecessary change narration; move durable history to the repository's sanctioned decision, release-note, migration, or postmortem surface.

## Taxonomy

1. **Dead design-session citations** — `(decision 7)`, `(audit C2)`, `design §4.7`, phase labels, “the design ledger,” or names of drafts not committed anywhere. Cite the real committed owner by name and path, or remove the citation while preserving its factual clause.
2. **Branch, stack, and PR vantage** — “a later PR in this stack,” “this PR adds,” “the previous commit.” State the resulting mechanism or extension point. When repository edits are authorized, put pending work in an owned TODO. Create or update an external issue only with explicit authorization; otherwise report the proposed deferral and owner.
3. **Change narration and indexical version stamps** — “used to,” “no longer,” “the old implementation,” “this cut,” “today,” or “now” contrasting with a deleted state. State present behavior. Turn a useful regression history into a present-tense counterfactual such as “without the byte-length guard, multibyte labels double-encode.”
4. **Review choreography** — “rejected in review,” “the reviewer confirmed,” draft ordinals, or round attributions. Keep the decision and rationale in the appropriate decision-record genre; remove who said it and when.
5. **Reviewer-addressed justification** — “the cast is safe—it simply…” or “this is correct because…”. State the invariant that makes the operation safe, or remove the comment when code/types already express it.
6. **Restatement and derivation transcripts** — control-flow narration, obvious proofs, test walkthroughs, and line-by-line previews. Keep only non-obvious contracts, invariants, or assertion rationale.
7. **Hedges and ownerless planning residue** — “probably fine for now,” “should be enough,” vague roadmap claims, and deferrals without an owner. State a measured bound and failure behavior. When repository edits are authorized, add a concrete owned TODO; create or update an external issue only with explicit authorization. Otherwise report the proposed marker, or delete the hedge when it carries no durable proposition.
8. **Authoring-language slips** — working-language fragments, private separators, and draft annotations embedded in prose of another language. Translate the durable fact or remove the residue.

## What is not reasoning leakage

Apply these keep rules before trimming:

- **Resolvable issue references and owned TODOs** remain durable when the tracker is part of the repository workflow.
- **Merged change references in decision records, migrations, release notes, and postmortems** can be legitimate evidence when that genre owns the history.
- **Suppression and exception justifications** are required prose. Correct a false reason; do not delete the explanation needed to keep the suppression safe.
- **Counterfactual-present regression pins** such as “without X, Y happens” preserve an invariant without narrating repository archaeology.
- **Measured bounds** retain their provenance; “measured” distinguishes observation from a guess.
- **Runtime old/new states** describe two live objects during handover, not old and new repository versions.
- **Historical stage names inside explicitly historical artifacts** are valid when the artifact owns that chronology. Bare indexical stamps remain unstable.
- **External references that resolve by design**—standards sections, specifications, ticket URLs, or design-frame names—are valid evidence.
- **Project voice and genre language** such as “we” or an “Alternatives considered” section are not automatically transcripts.
- **Recorded model output, fixtures, and snapshots** preserve their original voice when they are evidence rather than maintained explanatory prose.

Resolvability clears only this skill's bar. A resolved story can still be duplicated, misplaced, or too detailed under [documentation governance](../yq-doc-maintenance/SKILL.md).

## Workflow

1. Confirm the exact scope and edit authority. Use the exclusions and ownership rules from [yq-technical-writing](../yq-technical-writing/SKILL.md). Treat third-party sources, generated artifacts, recorded fixtures, snapshots, and frozen archives as immutable unless the request and repository policy explicitly include them.
2. Audit read-only first. For a supplied sentence, comment, or small file, inspect that exact passage directly. For a multi-file or corpus audit, run the [recall batteries](references/recall-batteries.md), judge every hit semantically, and also read the densest prose in scope—module docs, READMEs, decisions, runbooks, and comments—without a pattern in hand; every fixed battery under-detects new forms.
3. Fix the owner first. Generated catalogs point back to source prose or generator templates. Copied schemas and synchronized pages follow their owner. Localized pairs follow the repository's pairing policy. Model-, CLI-, protocol-, and UI-visible strings are behavior, so use their owning snapshots or behavioral tests rather than silently rewording them.
4. Before deleting or rewriting a passage, enumerate its propositions and check [the overcorrection traps](references/examples.md#overcorrection-traps). Preserve modality, conditions, timing, ownership, negative guarantees, true facts, and provenance.
5. Re-run any batteries used and inspect the diff. Every remaining hit should be a sanctioned keep, quoted calibration/evidence, or a reported unresolved case. Confirm citations resolve at the current revision and run the documentation, localization, generation, type-equivalence, snapshot, or behavior checks for the surfaces touched.

Report the inspected scope, candidate count, changed passages, sanctioned keeps, unresolved references, owner/derivative updates, and checks actually run. A zero-hit search is not proof of a clean corpus unless the patterns were calibrated and dense prose was also reviewed.
