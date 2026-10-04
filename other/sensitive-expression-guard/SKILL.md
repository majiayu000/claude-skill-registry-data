---
name: sensitive-expression-guard
version: 1.0.1
description: On chapter completion, before manuscript builds, and before submission — mechanically screens sensitive expressions (absolute quantifiers, deficit-model vocabulary, author-misidentification co-occurrence, abstract register policy, presence of a non-diagnostic disclaimer) with check_sensitive_expression.py, and adds an LLM "careless adversarial reader" simulation to surface semantic short-circuit risks; author decisions accumulate in sensitive-expressions.yml. Especially important for DSR papers with self-referential case studies
---

# Sensitive Expression Guard

## Purpose
In DSR papers — above all **self-referential case studies analyzing the author's own practice** — symptom-adjacent vocabulary (diagnosis, spectrum, hyperfocus, etc.) invites readers to misidentify the author's medical status, and rhetorical absolutes can exceed the paper's declared modality ceiling. Some readers skip concessive clauses and short-circuit on keywords alone. This skill addresses the risk across **three layers**:

1. **Mechanical layer (regression prevention)**: `scripts/check_sensitive_expression.py` enforces registered rules. Only reappearance of `banned_terms` (author-finalized prohibitions) is FAIL; everything else is WARN
2. **LLM layer (semantic discovery)**: the machine only sees registered terms and sentence-level co-occurrence. The agent simulates a **careless adversarial reader**, checking metaphor-level hyperbole, concessive-clause skipping, and out-of-context quotation resilience
3. **Accumulation layer (learning)**: author decisions (fix / allowlist / ban) are recorded with rationale in `design/sot/sensitive-expressions.yml` and fed back into the mechanical layer

## Trigger timings
- When a chapter draft or revision is completed (mechanical layer is mandatory)
- When `assemble_manuscript.py` aborts a build on FAIL
- When the pre-submission gate returns WARN/FAIL for `sensitive-expression`
- When the author flags an expression risk (misidentification, overstatement, deficit-model vocabulary) — LLM review plus accumulation

## Principles
- **FAIL (banned reappearance) always blocks**: a regression of an expression the author already calibrated. Never triaged as "no action needed"
- **WARN means confirm intent**: negations, mentions (inside 「」), and quoted text are already exempted by the script. Remaining WARNs are triaged by the author
- **Reading the co-occurrence rule**: `misidentify` fires when a medicalizing term and an author self-reference share a paragraph. A disclaimer pattern in the same paragraph exempts it. Note that a pair-definition living in another chapter does NOT exempt — careless readers may read a chapter in isolation
- **The abstract is a separate register**: terms in `abstract_flagged` may be allowed in the body with pair definitions yet still WARN in the abstract (the `## 1.` section of `paper-outline.md`). This institutionalizes the policy of narrowing medically connoted vocabulary in summaries
- **Presence check**: any paper using medicalizing vocabulary at all must contain a non-diagnostic disclaimer sentence ("regardless of diagnostic status", etc.). Absence of bad words is not sufficient

## Procedure

```text
[Step 1: Mechanical scan] ➔ [Step 2: Pattern-match triage] ➔ [Step 3: LLM adversarial-reader review] ➔ [Step 4: Author decision ➔ accumulate in yml]
```

### Step 1: Mechanical scan

```bash
# All chapters (abstract section is auto-extracted from paper-outline.md and scanned under the abstract register)
python3 scripts/check_sensitive_expression.py docs/<paper-id>/chapters
# Single chapter
python3 scripts/check_sensitive_expression.py docs/<paper-id>/chapters/<file>.md
```

### Step 2: Pattern-match triage of findings

| Output pattern | Classification | Judgment criterion |
| :--- | :--- | :--- |
| `FAIL/banned` (banned reappearance) | Must fix | Regression of an author-finalized calibration. No exceptions |
| `WARN/absolute` (absolute/unbounded quantifier) | Confirm | Calibrate to a verifiable scope. Negations/mentions already exempt |
| `WARN/quantifier` (vague population quantifier, no citation) | Confirm | Attach a citation or weaken to an existence claim ("exist" not "not a few") |
| `WARN/modality` (over-ceiling claim verb) | Confirm | Align with the paper's declared modality ceiling (explore / suggest / existence proof) |
| `WARN/deficit` (deficit-model vocabulary) | Confirm | Check consistency with the neurodiversity stance; use established vocabulary such as "barrier" |
| `WARN/misidentify` (misidentification coupling) | Confirm | Add a disclaimer in the paragraph or separate the vocabularies; "no action needed" is acceptable if defined elsewhere (record rationale) |
| `WARN/abstract` (summary register violation) | Fix-leaning | Replace per the narrowed-abstract policy (body may keep the term) |
| `WARN/disclaimer` (missing non-diagnostic disclaimer) | Must fix | The disclaimer sentence is mandatory whenever medicalizing vocabulary is used |

### Step 3: LLM adversarial-reader review (short-circuits the machine cannot see)

1. **Concessive-clause skipping**: check how each clause reads in isolation when "not ... but ..." constructions are read partially
2. **Metaphor hyperbole**: semantically discover rhetorical exaggeration not covered by registered terms
3. **Quotation resilience**: check how a sentence reads when quoted alone, out of context (e.g., on social media)
4. **Author-attribute inference resistance**: check whether any path remains by which readers could infer "the author is diagnosed" from the self-referential case description

### Step 4: Author decision and accumulation in sensitive-expressions.yml

1. Record the author's decision in `docs/<paper-id>/design/sot/sensitive-expressions.yml` with a rationale comment

```yaml
banned_terms:
  - 無尽蔵 # 2026-08-18: calibrated — unbounded absolute, unverifiable
allowlist:
  - 障害|二項対立 # meta-discussion criticizing the deficit model (mention, not use)
```

2. After fixing the prose, re-run the script and confirm FAIL=0 and that remaining WARNs are justified
3. Append a decision summary to `docs/<paper-id>/design/logs/friction-log.md` (date, finding, classification, rationale, action)

## Related
- Detection script: `scripts/check_sensitive_expression.py`
- Enforced invocation: `assemble_manuscript.py` (build aborts on FAIL; bypass with `--force`), pre-submission gate `check_pre_submission.py` check #7
- Terminology drift: `terminology-consistency` skill (coordinates with the §2.5 modality ceiling)
- General WARN/FAIL triage: `pre-submission-triage` skill

## Outputs
- Sensitive-expression triage summary (presented in chat)
- `docs/<paper-id>/design/sot/sensitive-expressions.yml` (accumulated rules and decisions — source of truth)
- `docs/<paper-id>/design/logs/friction-log.md` (audit trail of decisions)
