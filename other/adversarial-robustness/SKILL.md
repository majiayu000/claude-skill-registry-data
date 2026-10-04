---
name: adversarial-robustness
description: Review an AI system's robustness against adversarial evasion attacks — covering input perturbation, semantic-preserving transformations that flip classifier decisions, transferability of attacks across model versions, and robustness evaluation methodology.
last_reviewed: 2026-04-29
---

# Adversarial Robustness

## First Principle

**Adversarial examples reveal the gap between what a model computes and what humans intend. A classifier that correctly labels "invoice" may fail on "ınvoice" (Unicode I). That gap is an attack surface.**

Adversarial robustness is the property of being resistant to inputs that are slightly modified to cause incorrect model behavior, while remaining semantically unchanged to a human observer. In security contexts, this matters because input classifiers, content filters, and guardrail models all operate on model inferences — and all of them can be fooled by carefully crafted perturbations that a human would read as identical to the original.

## Attack Mental Model

1. **Evasion attacks on classifiers** — small perturbations to text (character substitution, spacing, Unicode normalization) cause a safety classifier to change its decision from "blocked" to "allowed" while the human-readable meaning is unchanged.
2. **Transferable adversarial examples** — an adversarial example crafted to fool one model version often transfers to related model versions. An attacker who discovered a working perturbation against an older deployment version may reuse it after an update.
3. **Semantic-preserving transformation** — paraphrasing, synonym substitution, and syntactic restructuring preserve meaning while evading token-matching filters and keyword blocklists.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Safety classifiers and content filters are evaluated on adversarial test sets — not just clean inputs — and robustness metrics are part of the acceptance criteria. |
| **Scope** | Input normalization is applied before classification — Unicode normalization, homoglyph replacement, whitespace canonicalization — reducing the perturbation surface available to attackers. |
| **Isolate** | Multiple independent classifiers are used in sequence where possible. An adversarial example that fools one classifier may not fool a different model architecture or a rules-based secondary check. |
| **Enforce** | Classifier decisions include a confidence score. Low-confidence decisions on security-critical categories trigger human review rather than automatic pass. |

## ARB.1 Input Normalization and Perturbation Surface Reduction

**The core vulnerability:** Text-based content filters and safety classifiers operate on the token sequence the model produces from the input. Unicode normalization, whitespace handling, and character encoding are preprocessing steps that happen before the model sees the text. An attacker who can inject characters that are visually identical to ASCII but are different Unicode code points can cause a classifier to miss a keyword it is looking for.

### Check

- Is Unicode normalization (NFKC or NFC) applied to all user inputs before they are passed to safety classifiers or keyword filters?
- Are homoglyphs — Unicode characters visually similar to ASCII — detected and mapped to their ASCII equivalents before classification?
- Are whitespace characters (zero-width space, non-breaking space, soft hyphen) removed or normalized before keyword matching?
- Is the normalization applied before the input reaches the LLM, not only before it reaches downstream systems?

### Action

- **Apply NFKC normalization and homoglyph mapping as the first preprocessing step:**

```python
import unicodedata
import re

# Common homoglyph mappings (extend as needed)
HOMOGLYPHS = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c',  # Cyrillic lookalikes
    'ı': 'i', 'ϲ': 'c', 'ᴀ': 'a',
}

def normalize_input(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = "".join(HOMOGLYPHS.get(c, c) for c in text)
    text = re.sub(r'[​‌‍﻿­]', '', text)  # zero-width + soft hyphen
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

- **Normalize before all classification steps.** The normalization pipeline should run before: keyword filters, safety classifiers, embedding generation for RAG, and the LLM itself. Applying normalization only at one step leaves the others exposed.
- **Test normalization with adversarial inputs.** Maintain a set of normalization test cases: inputs with Cyrillic homoglyphs, zero-width characters, base64 segments, and URL encoding. Confirm that each normalizes to the expected canonical form.

### Failure Modes

- A keyword blocklist blocks "bomb" but not "b​omb" (with a zero-width space between b and omb). The filter sees two words; a human reads one.
- A safety classifier is trained on clean English text. Inputs with Cyrillic characters substituted for visually identical Latin characters score below the blocking threshold.

## ARB.2 Robustness Evaluation and Defense-in-Depth

**The core vulnerability:** A classifier's clean-input accuracy does not predict its adversarial robustness. A model that correctly classifies 99% of standard inputs may be evaded by 80% of adversarially perturbed versions of the same inputs. Robustness must be measured explicitly — it is not implied by standard performance metrics.

### Check

- Is robustness against adversarial perturbations measured as part of the evaluation suite for every safety classifier in use?
- Are at least two independent classification mechanisms applied in sequence for high-severity content categories — where an adversarial example that evades one must also evade the other to pass?
- Is classifier confidence tracked? Are low-confidence decisions on blocked categories routed to human review rather than automatically allowed?

### Action

- **Build an adversarial evaluation set for each classifier.** For a content moderation classifier, generate adversarial variants of your test set using:
  - Character-level perturbations: swap one character for a homoglyph
  - Word-level paraphrasing: synonym substitution
  - Syntactic restructuring: passive voice, sentence reversal, embedded clauses
  
  Measure: what fraction of adversarially perturbed blocked inputs still score above the blocking threshold?

```python
def evaluate_adversarial_robustness(classifier, clean_inputs, adversarial_inputs):
    clean_blocked = sum(1 for x in clean_inputs if classifier.score(x) > THRESHOLD)
    adv_blocked = sum(1 for x in adversarial_inputs if classifier.score(x) > THRESHOLD)
    bypass_rate = 1 - (adv_blocked / clean_blocked)
    return {"clean_block_rate": clean_blocked/len(clean_inputs), "adversarial_bypass_rate": bypass_rate}
```

- **Apply defense-in-depth.** For any content category with high harm potential, use at least two classifiers with different architectures (e.g., a fine-tuned BERT classifier + an LLM-based semantic classifier). An adversarial example optimized against one rarely transfers perfectly to both.
- **Gate on confidence, not just decision.** For security-critical categories, a prediction just above the blocking threshold is suspicious. Route low-confidence classifications (within 10% of the threshold in either direction) to a second-stage classifier or human review.

### Minimum Deliverable Per Review

- [ ] Normalization pipeline: NFKC, homoglyph mapping, zero-width removal — applied before all classifiers
- [ ] Adversarial evaluation metrics: bypass rate per perturbation type for each classifier
- [ ] Defense-in-depth: secondary classifier or rule-based check for critical categories
- [ ] Confidence gating: low-confidence decisions on blocked categories go to human review
- [ ] Normalization test suite: canonical adversarial input pairs checked in CI

## Quick Win

**Add NFKC normalization to your input pipeline today.** It takes one line (`unicodedata.normalize("NFKC", text)`) and closes the Unicode homoglyph substitution class of attacks entirely — one of the most common simple evasion techniques against keyword filters.

## References

- Jailbreak technique families → [jailbreak-taxonomy/SKILL.md](../jailbreak-taxonomy/SKILL.md)
- Red-teaming methodology → [prompt-injection-red-teaming/SKILL.md](../prompt-injection-red-teaming/SKILL.md)
- Input filtering controls → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
