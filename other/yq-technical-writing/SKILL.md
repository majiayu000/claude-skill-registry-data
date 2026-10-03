---
name: yq-technical-writing
description: 编写或精简技术文档、注释、提示词和界面文案时使用。
---

# Technical Prose Standard

Write enough to preserve the contract, then remove reasoning transcripts, repetition, and decoration. A contract is an obligation, invariant, precondition, postcondition, compatibility promise, failure behavior, timing rule, or ownership rule that a caller, callee, implementer, producer, consumer, operator, or user relies on.

This skill owns sentence-level editorial judgment and required prose coverage. Use [yq-doc-maintenance](../yq-doc-maintenance/SKILL.md) for placement, source-of-truth ownership, stale/conflicting documents, and corpus structure. Use [yq-remove-reasoning-leaks](../yq-remove-reasoning-leaks/SKILL.md) when prose adopts the authoring session's vantage. This is guidance, not a mechanical shortening pass.

Terms such as `contract`, `boundary`, `shape`, `surface`, `seam`, `gate`, and `vocabulary` are useful only when they name the exact subject. Prefer the concrete API, field set, invariant, validation, timing point, component split, or failure state when that is clearer.

Comments describe non-obvious contracts or rationale that code cannot express. Let code show ordinary control flow.

## Scope, authority, and ownership

Use the narrowest scope supported by the request, current change, or named artifact. Ask only when ambiguity could cause a broad or destructive rewrite. Do not infer repository-wide scope from a request about one file or diff.

Accept `mode: automatic | interactive`; default to `automatic`. Interactive mode is for explicit calibration or questions, not permission. Audit and review tasks report findings without editing. Explicit write, fix, rewrite, or trim tasks may apply clear changes inside the authorized scope.

Read applicable agent instructions, documentation rules, style guides, owning code/config/schema, and current decision records before judging prose. Discover project-specific exclusions and derivative surfaces. Third-party sources, recorded fixtures, snapshots, and frozen archives are immutable by default. Generated surfaces must be updated through their owner and regenerated. Treat translations according to the repository's localization and pairing policy; either language may be the authored owner.

When several surfaces state the same fact, identify the owner. A generated summary, README excerpt, translated page, example output, or copied schema must not become an accidental second source of truth.

Preserve unresolved contracts. Absence from the implementation currently in view is `unknown`, not proof that a documented promise is obsolete—especially when a page covers a broader client, service, or workflow than the nearby symbol. Keep the proposition under its existing subject or report the ownership conflict. Remove it only when a current owner or explicit contract decision establishes supersession. A prose-only task does not authorize silently reconciling product behavior to whichever code was easiest to inspect.

## Preserve the complete proposition

Before editing a passage, enumerate every proposition. Preserve each relevant:

- actor and action;
- condition, timing, and ordering;
- modality such as must, may, should, or never;
- negative guarantee and exception;
- ownership and transfer of responsibility;
- side effect, failure mode, fallback, and consequence;
- scope, compatibility, durability, and security boundary;
- measured provenance or external authority when it makes a claim verifiable.

Remove adjectives, repetition, and narration only when every load-bearing clause survives and the result is clearer. A lower word count alone is not an improvement.

Keep a complete local contract at the point of use: the behavior, preconditions, failure, ownership, and consequence a reader needs there. Link to the owning document for architecture, rationale, algorithms, history, and extended examples. A link cannot replace essential local behavior, but duplicated rationale should have one home.

Keep non-obvious rationale when omitting it could plausibly cause misuse, unsafe maintenance, or an incorrect simplification. Otherwise state the operational consequence and link the rationale home.

## Required coverage by prose location

This is not a one-way deletion pass. Add or restore prose when code, types, schemas, and structure do not communicate the necessary contract.

- **Public API documentation and JSDoc:** caller-visible input distinctions, return states, throws/rejections, side effects, ownership, timing, cancellation, durability, and compatibility.
- **Internal comments:** non-local or complicated structure, including invariants, race ordering, resource ownership, security boundaries, and surprising failure behavior. Remove line-by-line control-flow narration.
- **Module comments:** role, dependencies, responsibilities, lifecycle, and non-obvious architecture choices; link long rationale to its owner.
- **Tests:** only non-obvious test design—why a fixture, assertion, platform accommodation, real entry path, negative case, or indirect observation is necessary. Let the test body show its sequence.
- **Tutorials and runbooks:** prerequisites, required actions, real entry paths, observable verification, rollback/recovery, and concise warnings appropriate to the audience.
- **READMEs and references:** consumer contract, configuration, semantics, failure modes, limitations, extension points, compatibility, and visible effects. Link generated catalogs and cross-component owners rather than copying them.
- **Decision records:** unique rationale, alternatives, consequences, shipped verification, compatibility commitments, reintroduction conditions, and named coverage gaps. Once implemented, remove obsolete planning checklists while retaining evidence that pins the decision.
- **Postmortems:** incident sequence, evidence, causal chain, impact, recovery, and prevention. Remove repeated persuasion or detail that does not establish causality.
- **Skills and agent instructions:** behavioral guardrails, scope, completion criteria, and conditional pointers. Preserve “guidance, not a checklist/script” when it changes how the workflow is applied.
- **Examples and configuration comments:** non-obvious wiring, load order, access limits, security stance, replay behavior, exceptions, and likely misuse. Let configuration show its own inventory.
- **Prompts and model-, CLI-, protocol-, or UI-visible strings:** treat wording as behavior. Check the generated or rendered outcome and run the owning behavioral assertion when one exists.
- **Diagnostics:** failing subject or path, violated rule, relevant observed value, and corrective action when it is not obvious. Remove internal execution narration.

Preserve searchable mechanism names and meaningful modal, temporal, security, or negative emphasis. Normalize decorative emphasis only.

## Workflow

1. Confirm scope, mode, write authority, current branch or comparison base when relevant, and applicable repository instructions.
2. Identify each passage's subject and owner before judging it; do not collapse a broad document onto the only nearby implementation symbol. Read the owning code or document. For calibration or unfamiliar cases, read [the distilled examples](references/examples.md).
3. Inspect the requested scope, not only its largest files. Use targeted searches, diffs, word counts, and generated-output inspection to nominate passages, then judge each semantically.
4. Classify candidates as keep, add, trim, restore, restructure, relocate, or defer. Apply only authorized clear changes; do not manufacture edits to meet a deletion target.
5. Update the owner before derivative artifacts. After learning a governing rule, recheck analogous passages inside scope.
6. Run narrow relevant documentation, generation, localization, type/schema, link, snapshot, and behavior checks. Run `git diff --check` when the scope is version-controlled and inspect the final diff for third-party, generated, archived, or out-of-scope changes.
7. Report inspected scope, substantive changes, deliberate keeps, genuine borderline cases, deferred items, derivative updates, and checks actually run.

## Borderline decisions

A case is borderline only when at least two versions preserve the complete proposition but trade accepted principles. A rewrite with one proposition-preserving answer is not borderline.

In automatic mode, apply clear edits when authorized and report genuine borderline cases without interrupting the work. Never weaken a proposition merely to make progress.

In interactive mode, group analogous passages under their governing principle. Present two or three viable versions, recommend one, and state the factual or structural difference. Do not offer inferior distractors. After the user decides, apply the chosen principle to analogous passages in scope. Record it in a project-owned style guide only when explicitly authorized and genuinely durable; never modify this installed skill as a side effect of an unrelated project task.
