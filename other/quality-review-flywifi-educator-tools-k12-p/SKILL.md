---
name: quality-review
description: "Evaluate any K-12 educational artifact against the TOS Quality Gates and return a scored, evidence-based verdict. Use this whenever someone wants to review, score, QA, critique, vet, or 'check the quality of' a lesson plan, unit, assessment, rubric, slide deck, IEP support, intervention plan, or family communication — and as the mandatory final gate after any TOS capability skill generates an artifact. It scores 9 weighted dimensions 0-5 (Integrity, Accuracy, Alignment, Educational Quality, Governance, User Intent, Accessibility, Professional Quality, Safety), computes a composite, applies critical-failure overrides, and emits a decision record. Make sure to use this skill whenever the user asks 'is this good?', 'will this pass?', 'review my lesson', 'check standards alignment', or wants quality assurance on teaching materials. Do NOT use it to CREATE artifacts — route creation to lesson-planner, assessment-designer, or presentation-builder; quality-review only evaluates."
---

# quality-review — the Quality Gates executor

`quality-review` is the governance skill of the Teacher Operating System. It runs the **Quality
Gates Protocol** (`references/quality-gates.md`) on an artifact and returns a scored, auditable
decision. It is the final stage of the pipeline in `references/method.md`; nothing is "Final" until
it passes here.

## 1. Inputs
- The **artifact** to evaluate (pasted, or just produced by a capability skill).
- Its **context**: persona, grade band, subject, the standards it claims to meet, and the original
  request (for the User Intent gate). If context is missing, infer + log it
  (`references/assumptions-protocol.md`) — never invent facts about the artifact.

## 2. Score the 9 dimensions, in gate order, 0-5
Use the descriptors in `references/rubric.md`. Evaluate in this order and **stop early on a critical
failure**:

1. Integrity → 2. Safety → 3. Governance → 4. Accuracy → 5. Alignment →
6. Educational Quality → 7. Accessibility → 8. Professional Quality → 9. User Intent.

For each dimension record a 0-5 score **with evidence** (quote the artifact). 0 = critical failure.

## 3. Check critical failures first (override everything)
Any of these forces **Rejected regardless of composite** and may never be overridden:
fabricated/incorrect standard or citation, real student PII, unsafe or legal-overreach content,
or "approval" asserted without evidence. (Full list: `references/quality-gates.md`.)

For the fabricated-standard check, don't judge by eye — resolve mechanically:
`python3 tools/verify_standards.py --input <artifact.json>` (offline, committed FL corpus +
CCSS/NGSS scheme checks). `not_found`/`malformed` = this critical failure; advisory states are
scored on evidence, not treated as fabrication. The returned `statement` is the registry origin
form for the citation-mutation check (rubric, Accuracy).

## 4. Compute the composite and decision (deterministic)
Run the bundled helper so weighting + thresholds are exact and reproducible:

```bash
python3 scripts/score.py '{"integrity":5,"safety":5,"governance":4,"accuracy":4,"alignment":4,"educational_quality":4,"accessibility":4,"professional_quality":4,"user_intent":5}'
```

It applies the QG §33.1 weights, the §35.3 thresholds (Approved ≥4.0 · Conditionally Approved
3.0-3.99 · Remediation 2.0-2.99 · Rejected <2.0), and treats any 0 (or `--critical`) as an automatic
Rejected. Do not hand-compute — use the script.

## 5. Emit the decision record
Return the verdict as a decision record per `references/metadata-schema.md`: per-dimension scores +
evidence, composite, decision, rationale, and `human_review_required: true`. See
`examples/example-evaluation.md` for the exact shape. Two honesty rules (QG §93.3):
- A dimension with no findings is stated as "no issues found — checked: <what was examined>",
  never as "error-free" or "perfect".
- Always emit `residual_risk`: the dimensions/claims this review is least able to guarantee, and
  why — even on Approved. Frame it as review limits, not defects.

Also populate `human_review_focus` (metadata-schema.md): the 2-3 specific spots the teacher should
check first — drawn from the two lowest-scoring dimensions and any near-critical finding (e.g.,
"confirm MA.3.NSO.2.2 against CPALMS", "re-work answer-key item 7", "SpEd sign-off on the
accommodation section"). It prioritizes human review; it never replaces it.

## 6. On not-Approved
Give **specific, actionable remediation** per failed dimension (what to change and why). Resolve
contradictions with `protocol-layer/conflict-protocol.md` (integrity > safety > governance >
accuracy/alignment > preference > presentation). Never fabricate to make something pass
(`protocol-layer/failure-recovery.md`).

Artifacts to produce: see `references/artifact-types.md`.
