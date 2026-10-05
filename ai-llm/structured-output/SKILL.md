---
name: structured-output
description: Use when an LLM must return machine-readable data. Covers schema design for models, native structured-output modes, validation and repair, and extraction that survives contact with messy input.
metadata:
  category: ai
  version: 1.0.0
  tags: [structured-output, json, extraction, schema, validation]
---

# Structured Output

## Purpose

Get reliably parseable, correctly typed data out of a language model. The naive approach — asking for JSON in the prompt and calling `json.loads` — fails often enough to be a production incident.

## When to Use

- Extracting fields from unstructured text.
- Classification with a fixed set of labels.
- Any LLM output consumed by code rather than read by a human.
- A pipeline that fails intermittently on parse errors.

## Capabilities

- Schema design that models follow reliably.
- Native structured output: JSON schema mode, tool calling, constrained decoding.
- Validation, repair, and retry.
- Confidence and abstention: letting the model say it does not know.
- Extraction from long, messy, or partially irrelevant documents.

## Inputs

- The target schema and the semantics of each field.
- The input text and how messy it actually is.
- What should happen when a field is genuinely absent.

## Outputs

- Validated, typed objects.
- An explicit representation of absence, distinct from a guess.
- A measured extraction accuracy per field.

## Workflow

1. **Use the API's native mechanism** — JSON schema mode or tool calling constrains the decoder so that malformed output is structurally impossible. Asking for JSON in prose does not.
2. **Design the schema for a model, not a database** — Descriptive field names, enums instead of free strings, and a description on every field explaining what belongs in it. The schema is documentation the model reads.
3. **Make absence representable** — A nullable field with a clear meaning. Without one, the model will invent a plausible value rather than leave it out, because that is what the schema demanded.
4. **Validate, then repair, then fail** — Parse against the schema. On a semantic failure (a valid date that is in the future when it must be past), send the error back for one repair attempt, then give up cleanly.
5. **Measure per field** — Aggregate extraction accuracy hides the one field that is wrong 40% of the time.

## Best Practices

- Structured-output mode makes the output *parseable*, not *correct*. It guarantees the shape; it guarantees nothing about the values. Validate the semantics separately.
- An enum is more reliable than a string with instructions. If there are five valid categories, the schema should permit exactly five values.
- Deeply nested schemas degrade accuracy. Flatten where you can; a model fills a flat object of ten fields far more reliably than a three-level tree.
- Always allow null, and say what null means. Forcing a value into every field is how you get hallucinated data that looks perfectly well-formed.
- Ask for a confidence score, and act on it. Below a threshold, route to a human rather than writing a guess to the database.
- Extract the source span alongside the value when the extraction must be auditable. It makes verification possible and hallucination visible.

## Examples

**A schema that guides the model:**

```python
from pydantic import BaseModel, Field
from typing import Literal

class ExtractedInvoice(BaseModel):
    invoice_number: str | None = Field(
        description="The invoice number exactly as printed. Null if not present. "
                    "Do not construct one from the filename or the date."
    )
    total_cents: int | None = Field(
        description="The final amount due, in minor units (cents/pence). "
                    "Use the TOTAL, not the subtotal and not any line item."
    )
    currency: Literal["USD", "EUR", "GBP"] | None = Field(
        description="ISO code, inferred from the currency symbol or explicit code. "
                    "Null if genuinely ambiguous — do not assume USD."
    )
    due_date: date | None
    confidence: float = Field(
        ge=0, le=1,
        description="Your confidence that every extracted field is correct. "
                    "Below 0.7 if the document is unclear, is not an invoice, "
                    "or if you had to guess any field."
    )
    source_quotes: dict[str, str] = Field(
        description="For each non-null field, the exact text from the document "
                    "that supports it. This is used for audit."
    )
```

**Extraction with validation, one repair attempt, and a human fallback:**

```python
async def extract(document: str) -> ExtractedInvoice | HumanReview:
    result = await model.complete(
        EXTRACTION_PROMPT.format(document=document),
        response_format=ExtractedInvoice,   # native constrained decoding
    )

    # Structurally valid by construction. Now check that it is semantically sane.
    errors = validate_semantics(result, document)
    if errors:
        # One repair attempt, with the specific errors fed back.
        result = await model.complete(
            REPAIR_PROMPT.format(document=document, previous=result, errors=errors),
            response_format=ExtractedInvoice,
        )
        errors = validate_semantics(result, document)

    if errors or result.confidence < 0.7:
        return HumanReview(document=document, draft=result, reasons=errors)

    return result


def validate_semantics(inv: ExtractedInvoice, document: str) -> list[str]:
    errors = []
    if inv.total_cents is not None and inv.total_cents <= 0:
        errors.append("total_cents must be positive")
    if inv.due_date and inv.due_date.year < 2000:
        errors.append(f"due_date {inv.due_date} is implausible")
    # The strongest check available: every quoted span must exist in the source.
    for field, quote in inv.source_quotes.items():
        if quote not in document:
            errors.append(f"source_quote for '{field}' does not appear in the document — "
                          f"this field is likely hallucinated")
    return errors
```

## Notes

- The `source_quotes` check above is the most effective anti-hallucination mechanism available for extraction: a value the model cannot quote from the document is a value it invented, and a simple substring check catches it.
- Confidence scores from LLMs are poorly calibrated in absolute terms but useful relative to each other. Set the threshold by measuring on real data, not by intuition.
- If accuracy is critical, extract twice with different prompts and flag disagreements for review. It doubles the cost and catches most of what a single pass misses.
