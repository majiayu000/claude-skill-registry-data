---
name: rag
description: >
  Use when the user has already provided source material and needs a cited,
  evidence-constrained answer from that material. Not for external retrieval.
---

# OpenRAG-Skill

Skill invocation remains `$rag`.

Use this skill only when the relevant material is already in context:
- The user pasted one or more documents into the chat.
- The conversation already contains policies, manuals, contracts, specs, or FAQs.
- The task requires a cited answer, extraction, comparison, or audit grounded only in that material.

Do not use this skill for:
- Web search or external knowledge retrieval
- Large corpora that are not already present in context
- Embeddings, vector search, BM25, indexing, or reranking
- Repository-wide code navigation as the primary task

## Input Modes

### Raw Context Mode

Use this when the user provides unstructured source material.

```markdown
[CONTEXT]
Source A:
...

Source B:
...

[TASK]
What should be answered or extracted?

[OUTPUT_MODE]
answer | extract | compare | audit
```

First package the material into `Evidence Units`, then answer from those units.

### Packaged Context Mode

Use this when the user already provides labeled evidence.

```markdown
[E1] Source: ...
Section: ...
Content: ...

[E2] Source: ...
Section: ...
Content: ...
```

Skip packaging and move directly to localization, reconciliation, and answering.

## Evidence Unit Format

An `Evidence Unit` is a citation container, not a retrieval chunk.

Required fields:
- `ID` (`E1`, `E2`, ...)
- `Source`
- `Section`
- `Content`
- Optional `Notes` for date, scope, version, or jurisdiction

## Core Protocol

Execute these stages in order.

### Stage 1: Context Packaging

Purpose: turn raw material into stable, referenceable `Evidence Units`.

Rules:
- Preserve source boundaries.
- Preserve headings, numbering, and clause labels.
- Split only on visible structure such as headings, bullets, numbered clauses, or paragraph breaks.
- For long documents, package hierarchically: source -> section -> clause.

Deliverable:
- `Evidence Register`: the numbered evidence list (`E1`, `E2`, `E3`, ...)

### Stage 2: Query Decomposition and Coverage Planning

Purpose: define what must be proven before answering.

Rules:
- State the core question.
- Break it into atomic sub-questions.
- Classify the task as `fact`, `rule`, `comparison`, `extraction`, or `audit`.
- Mark which sub-questions are mandatory for a complete answer.

Deliverable:
- `Coverage Table`: each sub-question mapped to the evidence needed to support it

### Stage 3: Evidence Localization and Extraction

Purpose: identify the smallest sufficient evidence set.

Rules:
- Prefer direct statements over inference.
- Track unresolved sub-questions separately instead of guessing.
- Preserve exact wording for policy, contract, and compliance tasks.
- If support is indirect, treat it as lower-confidence support.

Deliverable:
- `Evidence Ledger`: direct support, indirect support, and unresolved gaps for each sub-question

### Stage 4: Cross-Check and Reconciliation

Purpose: prevent unsupported synthesis and hidden contradictions.

Rules:
- Check whether evidence units agree, narrow, or conflict.
- Track normative force for each controlling claim (`SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `MAY`).
- Prefer more specific evidence over summaries.
- Prefer time-bounded or versioned evidence when recency is explicit in the source.
- Never merge claims with different normative force as if they were equivalent.
- Do not flatten unresolved conflicts into one rule.

Deliverable:
- `Conflict Ledger`: scope, date, version, exception, and contradiction notes used in the final response

### Final Sweep

Before drafting, run one explicit omission check:
- Scan for exception terms such as `except`, `unless`, `however`, `only if`, and `notwithstanding`.
- Scan for dates, effective times, and version labels.
- Scan for scope boundaries such as role, region, product tier, or approval authority.
- Scan for wording that is legally or operationally sensitive, especially modal force.

If the sweep finds a missing constraint, add it to the ledgers before answering.

### Stage 5: Cited Answer Generation

Purpose: produce a stable, reviewable output.

Rules:
- Every material claim must be citation-backed.
- Unsupported claims must be omitted.
- Missing support triggers a partial answer or a refusal.
- Do not add outside knowledge unless the user explicitly asks for reasoning beyond the provided material.
- If a detail is absent, say `not specified in the provided evidence` instead of inferring from terminology, category, or common practice.
- Return the answer directly in the response; do not create helper files or external artifacts unless the user explicitly asks.

Deliverable:
- A contract-formatted answer with aligned evidence IDs

## Normative Force Lock

When the source uses modal or normative language:
- Preserve `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` exactly in meaning.
- Do not rewrite `SHOULD` or `MAY` as if they were mandatory.
- Do not rewrite `SHALL NOT` or `SHOULD NOT` as softer preference language.
- If two sources discuss the same topic with different force, surface that as a difference or conflict.
- In normative comparisons, name the force explicitly inside each differing requirement.

## Internal Work Products Stay Internal

`Evidence Register`, `Coverage Table`, `Evidence Ledger`, and `Conflict Ledger` are internal work products by default.

Do not emit them as extra top-level sections unless the user explicitly asks to see the intermediate reasoning artifacts.
Do not emit TODO lists, planning notes, or scratch reasoning.

## Output Modes

`OUTPUT_MODE` changes the structure inside the `Answer` section.

### `answer`

Use for direct conclusions.
- Return the shortest sufficient conclusion set.
- Keep each conclusion explicitly cited.

### `extract`

Use for field extraction or direct pull-through.
- Return field names, extracted values, and `not found` where evidence is missing.
- Avoid narrative unless the task explicitly asks for it.

### `compare`

Use for side-by-side source comparison.
- Organize the `Answer` section as `Shared Ground`, `Differences`, `Conflicts`, then `Bottom Line`.
- Put a point in `Shared Ground` only when both scope and normative force match across the cited evidence.
- If one source says `SHALL` and another says `SHOULD` or `MAY`, that belongs in `Differences`, not `Shared Ground`.
- If force differs and the overlap is only topical, prefer `Shared Ground` = `None.` instead of a vague common denominator.
- Never use words like `require`, `must`, or `prohibit` in `Shared Ground` unless all cited evidence support the same mandatory force.
- In normative text, each bullet in `Differences` should name the force explicitly, such as `Passwords [SHALL]: ...`.
- `Bottom Line` may restate only already-cited differences; do not introduce new rankings, causes, or unstated rationale.
- Keep scope attached to the source that owns it.

### `audit`

Use for policy, controls, and compliance-style reviews.
- Organize the `Answer` section as `Requirements`, `Exceptions`, `Gaps`, then `Risks` when relevant.
- Do not omit scattered constraints that narrow the main rule.

## Response Contract

Use these top-level sections in this exact order:
1. `Answer`
2. `Evidence Map`
3. `Conflicts or Gaps`
4. `Need More Material` (only when partial or refused)

Rules:
- Use no extra top-level sections before `Answer`.
- Every non-trivial claim in `Answer` must end with one or more evidence IDs such as `[E3]` or `[E2][E5]`.
- `Evidence Map` must map each major conclusion to the exact evidence IDs that support it.
- If a claim cannot be supported, it must not appear in `Answer`.
- Do not emit `Need More Material` when the answer is complete.
- Never emit placeholder text such as `None.` inside `Need More Material`.
- Keep the wording stable and easy to score.

## Refusal Contract

If the provided material does not support the core question:
- Set `Answer` to `INSUFFICIENT_EVIDENCE`.
- State exactly what is missing.
- List the additional material needed.
- Do not provide a speculative fallback.

## Conflict Contract

When evidence conflicts:
- Cite the conflicting evidence IDs directly.
- Explain whether the conflict is caused by scope, date, version, or an irreconcilable contradiction.
- Use conditional conclusions instead of a flattened summary.

Preferred patterns:
- `If E2 governs, then ...`
- `If E5 is the current version, then ...`
- `The sources conflict and do not support a single unconditional conclusion.`

## Operating Defaults

- Optimize for long-form documents first.
- Prefer complete traceability over broad coverage.
- Use exact wording when a small wording change would alter the meaning.
- If only part of a multi-part request is supported, answer only that supported part and mark the rest as a gap.

## References

Use these bundled references as needed:
- `references/protocol.md` for the detailed operating procedure
- `references/templates.md` for copy-paste templates
- `references/failure-modes.md` for failure handling
- `references/methodology.md` for positioning and limits

See the `examples/` and `evals/` folders for worked examples and test cases.
