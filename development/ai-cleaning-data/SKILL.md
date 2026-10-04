---
name: ai-cleaning-data
description: Normalize and fix messy data fields using AI. Use when normalizing addresses, standardizing company names, fixing inconsistent date formats, cleaning CSV data before import, correcting typos in bulk data, normalizing phone number formats, standardizing job titles, cleaning up free-text fields, data quality improvement with AI, fixing formatting inconsistencies, bulk data normalization, preparing messy data for analysis, AI-powered data wrangling.
---

# ai-cleaning-data

Use DSPy to normalize and fix messy data fields at scale. The core pattern - messy field value + field type/context → cleaned value + confidence - lets you handle inconsistent addresses, company names, dates, phone numbers, and free-text fields without writing a rule for every edge case.

The most effective approach: sample anomalies first, infer normalization rules, then apply deterministically where possible and use the LM only for ambiguous cases.

## Step 1 - Understand the Cleaning Task

Before writing code, clarify:

- **What fields** need cleaning? (addresses, phone numbers, dates, company names, free-text?)
- **What inconsistencies** exist? (typos, format variations, abbreviations, mixed languages?)
- **What is the target format?** Always define this explicitly — otherwise the LM improvises
- **How many rows?** This determines whether to use LM for each row or rule inference + deterministic apply
- **Is there a gold standard?** Even 50 manually-cleaned examples make optimization possible

## Step 2 - Build a Single-Field Cleaner

Start with one field type. The signature takes the messy value plus explicit format instructions.

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class CleanField(dspy.Signature):
    """Clean a messy data field to match the target format exactly.
    Do not change values that are already correct.
    Do not add, remove, or infer information not present in the input.
    """
    messy_value: str = dspy.InputField(desc="The raw field value to clean")
    field_type: str = dspy.InputField(desc="Type of field, e.g. 'US phone number', 'company name', 'ISO 8601 date'")
    target_format: str = dspy.InputField(desc="Exact target format with example, e.g. '+1 (555) 123-4567'")
    cleaned_value: str = dspy.OutputField(desc="The cleaned value in the target format, or the original if already correct")
    confidence: float = dspy.OutputField(desc="Confidence score 0.0-1.0 that the cleaned value is correct")
    change_made: bool = dspy.OutputField(desc="True if the value was changed, False if it was already correct")

cleaner = dspy.Predict(CleanField)

result = cleaner(
    messy_value="(555)123-4567",
    field_type="US phone number",
    target_format="+1 (555) 123-4567"
)
print(result.cleaned_value)   # "+1 (555) 123-4567"
print(result.confidence)      # 0.97
```

## Step 3 - Common Cleaning Patterns

### Address Normalization

```python
class NormalizeAddress(dspy.Signature):
    """Normalize a US mailing address to USPS standard format.
    Expand abbreviations (St → Street, Ave → Avenue, Apt → Apartment).
    Capitalize properly. Do not infer or add missing components.
    Preserve all components including suite/unit numbers.
    """
    raw_address: str = dspy.InputField(desc="Raw address string")
    city_hint: str = dspy.InputField(desc="City context if known, or empty string")
    state_hint: str = dspy.InputField(desc="State context if known, or empty string")
    normalized: str = dspy.OutputField(desc="USPS-format address: '123 Main Street, Suite 100, Springfield, IL 62701'")
    confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")

address_cleaner = dspy.Predict(NormalizeAddress)
```

### Company Name Standardization

```python
class StandardizeCompany(dspy.Signature):
    """Resolve a company name variant to its canonical legal name.
    Examples - 'IBM Corp.' → 'IBM', 'I.B.M.' → 'IBM', 'Mickey D' → 'McDonald's'.
    Use the canonical_name field for the authoritative form.
    If the variant is unrecognizable, return it unchanged.
    """
    variant: str = dspy.InputField(desc="Company name variant to standardize")
    canonical_name: str = dspy.OutputField(desc="Canonical company name")
    confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")
    is_recognized: bool = dspy.OutputField(desc="True if the company was confidently identified")

company_cleaner = dspy.Predict(StandardizeCompany)
```

### Date Format Conversion

```python
class NormalizeDate(dspy.Signature):
    """Convert a date string to ISO 8601 format (YYYY-MM-DD).
    Handle formats like '05/04/26', 'May 4th 2026', '4-May-26', '20260504'.
    If the date is ambiguous (e.g. 01/02/03), flag it.
    """
    raw_date: str = dspy.InputField(desc="Raw date string in any format")
    iso_date: str = dspy.OutputField(desc="Date in YYYY-MM-DD format, or empty string if unparseable")
    is_ambiguous: bool = dspy.OutputField(desc="True if the date could be interpreted multiple ways")
    confidence: float = dspy.OutputField(desc="Confidence 0.0-1.0")

date_cleaner = dspy.Predict(NormalizeDate)
```

## Step 4 - Rule Inference Pipeline

For large datasets, use the LM to infer rules from a sample, then apply deterministically.

```python
class InferNormalizationRules(dspy.Signature):
    """Analyze a sample of messy field values and infer the normalization rules needed.
    Output rules as a Python-executable list of (pattern, replacement) pairs where possible.
    Identify which cases require LM judgment vs. deterministic transformation.
    """
    field_type: str = dspy.InputField(desc="Type of field being analyzed")
    target_format: str = dspy.InputField(desc="Target format with example")
    sample_values: list[str] = dspy.InputField(desc="20-50 sample messy values")
    deterministic_rules: list[str] = dspy.OutputField(desc="Rules expressible as regex/replace, one per line")
    ambiguous_patterns: list[str] = dspy.OutputField(desc="Patterns that need LM judgment, one per line")
    rule_coverage_estimate: float = dspy.OutputField(desc="Estimated % of rows covered by deterministic rules")

import pandas as pd
import re

def build_cleaning_pipeline(df: pd.DataFrame, column: str, field_type: str, target_format: str):
    # Sample anomalies (skip already-clean values)
    sample = df[column].dropna().sample(min(50, len(df))).tolist()

    rule_inferrer = dspy.Predict(InferNormalizationRules)
    rules = rule_inferrer(
        field_type=field_type,
        target_format=target_format,
        sample_values=sample
    )

    print(f"Deterministic rules cover ~{rules.rule_coverage_estimate:.0%} of rows")
    print("Rules:", rules.deterministic_rules)
    print("Needs LM:", rules.ambiguous_patterns)
    return rules
```

## Step 5 - Validated Outputs with Pydantic

Use typed outputs to catch format violations before they reach your database.

```python
from pydantic import BaseModel, field_validator
import re

class CleanedPhone(BaseModel):
    original: str
    cleaned: str
    confidence: float

    @field_validator("cleaned")
    @classmethod
    def must_match_e164(cls, v):
        if v and not re.match(r"^\+1 \(\d{3}\) \d{3}-\d{4}$", v):
            raise ValueError(f"Phone '{v}' does not match target format +1 (NNN) NNN-NNNN")
        return v

class CleanPhoneTyped(dspy.Signature):
    """Clean a US phone number to +1 (NNN) NNN-NNNN format."""
    raw: str = dspy.InputField()
    result: CleanedPhone = dspy.OutputField()

phone_cleaner = dspy.Predict(CleanPhoneTyped)
```

## Step 6 - Batch Processing with Confidence Routing

Route high-confidence results to auto-accept and low-confidence ones to a human review queue.

```python
def clean_batch(
    values: list[str],
    field_type: str,
    target_format: str,
    auto_accept_threshold: float = 0.90,
    flag_threshold: float = 0.70,
) -> dict:
    cleaner = dspy.Predict(CleanField)
    accepted, flagged, rejected = [], [], []

    for val in values:
        result = cleaner(
            messy_value=val,
            field_type=field_type,
            target_format=target_format
        )
        entry = {"original": val, "cleaned": result.cleaned_value, "confidence": result.confidence}

        if result.confidence >= auto_accept_threshold:
            accepted.append(entry)
        elif result.confidence >= flag_threshold:
            flagged.append(entry)  # send to human review
        else:
            rejected.append(entry)  # too uncertain, keep original or escalate

    return {"accepted": accepted, "flagged": flagged, "rejected": rejected}
```

## Step 7 - Evaluate and Optimize

If you have a gold standard (even 50 rows), use it to optimize prompts.

```python
# Build a gold standard dataset
trainset = [
    dspy.Example(
        messy_value="(555)123-4567",
        field_type="US phone number",
        target_format="+1 (555) 123-4567",
        cleaned_value="+1 (555) 123-4567"
    ).with_inputs("messy_value", "field_type", "target_format"),
    # ... more examples
]

def exact_match_metric(example, prediction, trace=None):
    return example.cleaned_value == prediction.cleaned_value

optimizer = dspy.BootstrapFewShot(metric=exact_match_metric, max_bootstrapped_demos=4)
optimized_cleaner = optimizer.compile(dspy.Predict(CleanField), trainset=trainset)
```

## When NOT to Use AI Cleaning

Use regex, pandas, or deterministic transforms instead when:

- **Structured patterns cover 95%+ of cases** - phone number regex, pandas `pd.to_datetime`, stripping whitespace
- **Simple type coercion** - `int()`, `float()`, `strip()`, `lower()`
- **Already-clean data with a few outliers** - just filter or drop the outliers
- **You need 100% reproducibility** - LM outputs are non-deterministic; use deterministic rules when the format is fully specified
- **Cost matters at extreme scale** - 10M rows × LM call is expensive; infer rules on a 1K sample and apply them

## Key Patterns

| Task | DSPy approach |
|---|---|
| Single field, ad hoc | `dspy.Predict(CleanField)` |
| Validated output format | `dspy.Predict` with a Pydantic-typed OutputField |
| Iterative refinement on failures | `dspy.Refine` with format-check reward |
| Optimize on gold standard | `BootstrapFewShot` with exact-match metric |
| Rule inference at scale | Sample anomalies → infer rules → apply deterministically |

## Gotchas

**Calling the LM on every row instead of inferring rules first.** For 10K+ rows, sample 20-50 anomalous values, ask the LM to infer normalization patterns, then apply them with pandas/regex. Reserve LM calls for the ambiguous remainder.

**Not specifying the target format explicitly.** If you write "clean the phone number" without showing the exact target format (e.g., `+1 (555) 123-4567`), Claude will pick a format. Always include a concrete example in `target_format`.

**Using `dspy.Assert`/`dspy.Suggest` for format validation.** These are deprecated. Use `dspy.Refine` with a reward function that checks the cleaned value against your format regex:

```python
import re
TARGET_RE = r"^\+1 \(\d{3}\) \d{3}-\d{4}$"

def format_reward(args, pred):
    return 1.0 if re.match(TARGET_RE, pred.cleaned_value or "") else 0.0

cleaner = dspy.Refine(dspy.Predict(CleanField), N=3, reward_fn=format_reward, threshold=1.0)
```

**Cleaning related fields independently.** Address components (street, city, state, zip) must be normalized together — passing only the street loses context needed to expand abbreviations correctly. Pass all related fields in a single signature.

**Destructive normalization.** Claude may silently drop components it considers "noise" (e.g., "Suite 100", "c/o Jane Smith", legal suffixes like "LLC"). Add a `meaning_preserved` output field and reject or flag any cleaned value where it is `False`.

## Cross-References

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/ai-parsing-data` - extract structured fields from unstructured text (complement to cleaning)
- `/ai-checking-outputs` - validate cleaned values against schemas or business rules
- `/dspy-refine` - iterative refinement with a reward function, for format-check loops
- `/dspy-modules` - understand Predict, ChainOfThought, and other DSPy primitives
- `/ai-generating-data` - generate synthetic dirty data to build eval sets
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (address normalizer, company name standardizer, CSV batch cleaner), see [examples.md](examples.md)
- For API signatures and parameter tables (dspy.Predict, dspy.Refine, dspy.BootstrapFewShot, module.batch), see [reference.md](reference.md)
