---
name: ai-redacting-data
description: Strip PII and sensitive data from text before processing with AI. Use when redacting personal information, GDPR compliance, anonymizing customer data, masking credit cards, redacting PHI for HIPAA, stripping emails and phone numbers, de-identifying medical records, removing names from transcripts, PII detection and replacement, building a data anonymization pipeline, sanitizing text before sending to LLMs, pre-processing sensitive documents, privacy-preserving AI pipelines.
---

# Redacting PII and Sensitive Data with DSPy

Strip personal information and sensitive data from text before it reaches an LM — or before it leaves your system.

## Step 1 - Understand What to Redact

Before writing code, answer three questions:

1. **What PII types?** Names, emails, phones, SSNs, credit cards, addresses, dates of birth, IP addresses, medical record numbers (MRNs), or all of the above.
2. **Replacement strategy?** See the table in Step 3.
3. **Compliance requirement?** GDPR (EU personal data), HIPAA (US health data), PCI-DSS (payment data), or internal policy.

The answers drive which pipeline path you need.

---

## Step 2 - Set Up DSPy

```python
import dspy
import re
from dataclasses import dataclass, field
from typing import Literal

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)
```

---

## Step 3 - Replacement Strategies

| Strategy | Example output | Best for |
|---|---|---|
| Category placeholder | `[EMAIL]`, `[PHONE]` | Readability, compliance audits |
| Indexed placeholder | `[PERSON_1]`, `[PERSON_2]` | Preserving co-references across text |
| Hash | `[a3f9…]` | Pseudonymization, re-linkable with key |
| Synthetic / fake | `John Smith` → `Alex Turner` | Testing pipelines with realistic-looking data |
| Blank / mask | `████████` | Display-layer redaction |

---

## Step 4 - Choose Your Approach

| Approach | When to use | Tradeoff |
|---|---|---|
| Regex only | Emails, SSNs, credit cards, phones — fixed-format PII | Fast, deterministic, zero LM cost; misses names and free-form data |
| LM only | Unstructured text, multilingual names, complex context | High recall on contextual PII; slow, costly, and sends raw PII to the LM |
| Two-pass (recommended) | Mixed text with both structured and contextual PII | Regex first masks structured PII so the LM never sees raw values; best recall + lowest exposure |

The examples below use the two-pass pattern. Use regex-only when all PII is structured and you cannot afford any LM calls.

## Step 5 - Regex First for Structured Patterns

Regex is fast, deterministic, and never sends PII to an external API. Always run it before the LM pass.

```python
# Patterns for structured PII
PATTERNS = {
    "EMAIL":       re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'),
    "PHONE":       re.compile(r'\b(\+?1[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b'),
    "SSN":         re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    "CREDIT_CARD": re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
    "IP_ADDRESS":  re.compile(r'\b\d{1,3}(?:\.\d{1,3}){3}\b'),
    "DATE_OF_BIRTH": re.compile(r'\b(?:DOB|Date of Birth|born)[:\s]+\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b', re.IGNORECASE),
    "ZIP_CODE":    re.compile(r'\b\d{5}(?:-\d{4})?\b'),
}

@dataclass
class PIIMatch:
    pii_type: str
    value: str
    start: int
    end: int

def regex_detect(text: str) -> list[PIIMatch]:
    matches = []
    for pii_type, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            matches.append(PIIMatch(pii_type=pii_type, value=m.group(), start=m.start(), end=m.end()))
    return matches
```

---

## Step 6 - LM Signature for Contextual PII

Use the LM only for PII that requires reading context — names, addresses, and other free-form entities.

```python
class DetectContextualPII(dspy.Signature):
    """Identify personal information in text that requires context to detect.
    Return a JSON list of objects with fields: pii_type, value.
    PII types to detect - PERSON_NAME, ADDRESS, MEDICAL_RECORD_NUMBER, ORG_NAME (when linked to a person).
    Do not flag generic words that happen to resemble names."""

    text: str = dspy.InputField(desc="Text to scan for personal information")
    pii_entities: list[dict] = dspy.OutputField(
        desc='JSON list - [{"pii_type": "PERSON_NAME", "value": "Jane Doe"}, ...]'
    )

detect_pii = dspy.Predict(DetectContextualPII)
```

---

## Step 7 - Full Redaction Module

```python
class PIIRedactor(dspy.Module):
    def __init__(self, strategy: Literal["placeholder", "indexed", "blank"] = "placeholder"):
        self.strategy = strategy
        self.detect = dspy.Predict(DetectContextualPII)

    def _make_replacement(self, pii_type: str, entity_index: dict) -> str:
        if self.strategy == "indexed":
            key = pii_type
            n = entity_index.get(key, 0) + 1
            entity_index[key] = n
            return f"[{pii_type}_{n}]"
        elif self.strategy == "blank":
            return "████"
        else:
            return f"[{pii_type}]"

    def forward(self, text: str) -> dspy.Prediction:
        entity_index: dict[str, int] = {}
        seen: dict[str, str] = {}  # value → replacement (for consistency)

        # Pass 1 - regex for structured patterns
        regex_hits = regex_detect(text)

        # Pass 2 - LM for contextual PII (only send text with structured PII pre-masked)
        pre_masked = text
        for hit in sorted(regex_hits, key=lambda h: h.start, reverse=True):
            pre_masked = pre_masked[:hit.start] + f"[{hit.pii_type}]" + pre_masked[hit.end:]

        lm_result = self.detect(text=pre_masked)
        lm_entities = lm_result.pii_entities or []

        # Build replacement map from LM entities
        for entity in lm_entities:
            val = entity.get("value", "")
            pii_type = entity.get("pii_type", "PII")
            if val and val not in seen:
                seen[val] = self._make_replacement(pii_type, entity_index)

        # Apply LM replacements to original text
        redacted = text
        for val, replacement in sorted(seen.items(), key=lambda kv: len(kv[0]), reverse=True):
            redacted = redacted.replace(val, replacement)

        # Apply regex replacements
        for hit in sorted(regex_hits, key=lambda h: h.start, reverse=True):
            if hit.value not in seen:
                seen[hit.value] = self._make_replacement(hit.pii_type, entity_index)

        # Re-apply to get a clean final pass
        final = text
        for val, replacement in sorted(seen.items(), key=lambda kv: len(kv[0]), reverse=True):
            final = final.replace(val, replacement)

        return dspy.Prediction(
            redacted_text=final,
            entities_found=seen,
        )
```

---

## Step 8 - Validate Redaction Quality

Do not use `dspy.Assert` or `dspy.Suggest` here — they are deprecated. Use `dspy.Refine` with a reward function.

```python
class ValidateRedaction(dspy.Signature):
    """Check whether any PII survived redaction. Return True if clean, False if PII remains."""

    original_text: str = dspy.InputField()
    redacted_text: str = dspy.InputField()
    is_clean: bool = dspy.OutputField(desc="True if no PII remains, False otherwise")
    leaked_examples: list[str] = dspy.OutputField(desc="Examples of PII that leaked through, empty list if clean")

def redaction_reward(example, prediction, trace=None) -> float:
    validator = dspy.Predict(ValidateRedaction)
    result = validator(
        original_text=example.text,
        redacted_text=prediction.redacted_text,
    )
    return 1.0 if result.is_clean else 0.0
```

---

## Step 9 - GDPR and HIPAA Compliance Patterns

**GDPR - Right to erasure**
```python
# Store the entity map so you can reverse-map or fully erase later
redactor = PIIRedactor(strategy="indexed")
result = redactor(text=document)
# Persist result.entities_found keyed by document ID
# On erasure request - delete the mapping; ciphertext becomes permanently anonymized
```

**HIPAA - Safe Harbor de-identification**

HIPAA Safe Harbor requires removing 18 PHI identifiers. Add these patterns:

```python
HIPAA_PATTERNS = {
    "MRN":        re.compile(r'\bMRN[:\s#]+\w+\b', re.IGNORECASE),
    "NPI":        re.compile(r'\bNPI[:\s#]+\d{10}\b', re.IGNORECASE),
    "DEVICE_ID":  re.compile(r'\b(?:device|serial)[:\s#]+[A-Z0-9\-]{6,}\b', re.IGNORECASE),
    "URL":        re.compile(r'https?://\S+'),
    "ACCOUNT":    re.compile(r'\baccount[:\s#]+\w+\b', re.IGNORECASE),
}
PATTERNS.update(HIPAA_PATTERNS)
```

---

## Step 10 - When NOT to Use AI Redaction

- **Structured fields with known formats** - regex alone is sufficient and faster (emails, SSNs, credit cards).
- **Already-tokenized data** - if PII was never collected as free text, there is nothing to redact.
- **When you can avoid collecting PII in the first place** - the best redaction is prevention.
- **High-stakes legal documents without human review** - LM redaction can miss things; always add a human-in-the-loop audit step for compliance filings.

---

## Key Patterns

```python
# Quick usage
redactor = PIIRedactor(strategy="indexed")
result = redactor(text="Call Jane Doe at 555-123-4567 or jane@example.com")
print(result.redacted_text)
# "Call [PERSON_NAME_1] at [PHONE_1] or [EMAIL]"
print(result.entities_found)
# {"Jane Doe": "[PERSON_NAME_1]", "555-123-4567": "[PHONE_1]", "jane@example.com": "[EMAIL]"}
```

---

## Gotchas

- **The LM sees the PII you are trying to hide** - sending raw text to an external LM for detection defeats the purpose if the PII itself is sensitive. Run regex first and send only the pre-masked text to the LM, or use a locally hosted model.

- **Common words misidentified as names** - Claude flags "Will" (a verb), "Mark" (a noun), "Faith" (a concept) as `PERSON_NAME`. Prompt the signature to exclude words that are clearly not names in context, and validate detections against a stoplist.

- **Inconsistent placeholders break co-reference** - without a `seen` mapping dict, the same person can appear as `[PERSON_1]` in paragraph 1 and `[PERSON_2]` in paragraph 3. Always deduplicate entity values before assigning replacements.

- **Non-English and transliterated names are missed** - Claude's contextual PII detection is weakest on names from languages with different romanization conventions (e.g., Chinese pinyin, Arabic transliteration). Add language-specific name lists or a multilingual NER model for those cases.

- **Using `dspy.Assert`/`dspy.Suggest` for validation is outdated** - those APIs are removed in DSPy 2.5+. Use `dspy.Refine` with a reward function as shown in Step 7.

---

## Cross-References

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/ai-parsing-data` - extract structured fields from text (complementary pattern)
- `/ai-checking-outputs` - validate that outputs meet quality criteria
- `/dspy-refine` - iterative refinement with a reward function for validation loops
- `/dspy-retrieval` - if you need to redact before indexing documents
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional Resources

- For DSPy API signatures and parameter tables, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md):
  1. Customer support email redactor
  2. Medical record de-identifier (HIPAA Safe Harbor)
  3. Pre-LLM sanitizer for third-party API calls
