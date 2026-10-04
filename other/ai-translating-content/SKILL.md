---
name: ai-translating-content
description: Translate text between languages with AI while preserving brand voice and terminology. Use when translating app copy to Spanish, localizing marketing content, multilingual support tickets, i18n with AI, machine translation with brand voice, translating product descriptions, localizing help docs, batch translating i18n JSON files, glossary-enforced translation, AI-powered localization pipeline, translate content without losing tone, bilingual customer support, auto-translate user-facing strings, locale-aware content generation.
---

# AI Translating Content

Translate text between languages while preserving brand voice, enforcing glossary terms, and supporting batch i18n workflows — using DSPy signatures and optimizers.

## Step 1 - Understand the translation task

Before writing any code, ask:

- **What content?** UI strings, marketing copy, support tickets, help docs, legal text?
- **What languages?** Specific locales (e.g., `es-MX` vs `es-ES`) or open-ended?
- **Do you have a glossary?** Brand terms, product names, and technical terms that must not be translated?
- **Tone/formality?** Casual app copy vs formal documentation vs friendly support replies?
- **Volume?** One-off translation vs batch i18n file processing?
- **Quality bar?** Best-effort draft vs publication-ready?

The answers determine whether you need a simple signature or a full pipeline with glossary enforcement and quality scoring.

## Step 2 - Build a basic translator

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class Translate(dspy.Signature):
    """Translate source_text into the target_language. Preserve formatting, tone, and meaning."""
    source_text: str = dspy.InputField(desc="Text to translate")
    target_language: str = dspy.InputField(desc="Target locale, e.g. 'Spanish (Mexico)' or 'fr-FR'")
    translated_text: str = dspy.OutputField(desc="Translation in the target language")

translator = dspy.Predict(Translate)

result = translator(
    source_text="Get started for free",
    target_language="Spanish (Mexico)"
)
print(result.translated_text)
# → "Comienza gratis"
```

## Step 3 - Add glossary enforcement

Brand terms and product names must survive translation unchanged. Pass them explicitly — do not rely on the model to infer them.

```python
from pydantic import BaseModel

class TranslationResult(BaseModel):
    translated_text: str
    glossary_terms_used: list[str]  # terms from the glossary preserved as-is

class TranslateWithGlossary(dspy.Signature):
    """Translate source_text into target_language. Terms listed in glossary must appear
    verbatim in the output — do not translate them."""
    source_text: str = dspy.InputField()
    target_language: str = dspy.InputField()
    glossary: list[str] = dspy.InputField(
        desc="Terms that must NOT be translated (product names, brand terms, technical terms)"
    )
    result: TranslationResult = dspy.OutputField()

translator = dspy.Predict(TranslateWithGlossary)

result = translator(
    source_text="Upgrade to Acme Pro to unlock unlimited Workspaces.",
    target_language="Spanish (Mexico)",
    glossary=["Acme Pro", "Workspaces"]
)
print(result.result.translated_text)
# → "Actualiza a Acme Pro para desbloquear Workspaces ilimitados."
print(result.result.glossary_terms_used)
# → ["Acme Pro", "Workspaces"]
```

## Step 4 - Locale-aware tone

Pass tone as an explicit input field. Do not rely on the model to infer formality from the locale.

```python
class TranslateLocaleAware(dspy.Signature):
    """Translate source_text into target_language using the specified tone.
    Glossary terms must appear verbatim."""
    source_text: str = dspy.InputField()
    target_language: str = dspy.InputField(desc="Target locale, e.g. 'pt-BR' or 'German (formal)'")
    tone: str = dspy.InputField(
        desc="One of: casual, neutral, formal. Controls register and vocabulary."
    )
    glossary: list[str] = dspy.InputField(default=[])
    translated_text: str = dspy.OutputField()

translator = dspy.Predict(TranslateLocaleAware)

result = translator(
    source_text="Hey! Check out what's new this week.",
    target_language="French (France)",
    tone="casual",
    glossary=[]
)
```

## Step 5 - Batch translation for i18n files

Translate each key individually. Do not concatenate all strings into one call — that degrades quality and makes glossary enforcement unreliable.

```python
import json

def translate_i18n_file(
    source_path: str,
    target_language: str,
    glossary: list[str],
    tone: str = "neutral"
) -> dict:
    with open(source_path) as f:
        strings = json.load(f)  # {"key": "English string", ...}

    translator = dspy.Predict(TranslateLocaleAware)
    translated = {}

    for key, text in strings.items():
        result = translator(
            source_text=text,
            target_language=target_language,
            tone=tone,
            glossary=glossary
        )
        translated[key] = result.translated_text

    return translated

# Usage
es_strings = translate_i18n_file(
    source_path="locales/en.json",
    target_language="Spanish (Mexico)",
    glossary=["Pro", "Workspace", "Dashboard"],
    tone="casual"
)

with open("locales/es-MX.json", "w") as f:
    json.dump(es_strings, f, ensure_ascii=False, indent=2)
```

For large files, add a progress bar and rate-limit retries:

```python
from tqdm import tqdm

for key, text in tqdm(strings.items(), desc="Translating"):
    ...
```

## Step 6 - Quality estimation per segment

Add a confidence score output to flag segments that need human review.

```python
class TranslationWithQuality(BaseModel):
    translated_text: str
    confidence: float  # 0.0–1.0
    needs_review: bool
    review_reason: str  # empty string if needs_review is False

class TranslateWithQuality(dspy.Signature):
    """Translate source_text into target_language. Also estimate translation confidence:
    1.0 = straightforward, <0.7 = ambiguous or idiom-heavy, flag for human review."""
    source_text: str = dspy.InputField()
    target_language: str = dspy.InputField()
    glossary: list[str] = dspy.InputField(default=[])
    result: TranslationWithQuality = dspy.OutputField()

translator = dspy.Predict(TranslateWithQuality)

result = translator(
    source_text="We'll circle back on this once we've boiled the ocean.",
    target_language="Japanese",
    glossary=[]
)

if result.result.needs_review:
    print(f"Review needed: {result.result.review_reason}")
```

## Step 7 - Test and optimize

### Glossary compliance metric

```python
def glossary_compliance(example, pred, trace=None):
    glossary = example.glossary
    translated = pred.result.translated_text if hasattr(pred, "result") else pred.translated_text
    # All glossary terms must appear verbatim in the translation
    return all(term in translated for term in glossary)
```

### Meaning preservation judge

```python
class MeaningPreservationJudge(dspy.Signature):
    """Given a source text and its translation, judge whether the meaning is fully preserved.
    Return a score from 0 to 1."""
    source_text: str = dspy.InputField()
    translated_text: str = dspy.InputField()
    target_language: str = dspy.InputField()
    score: float = dspy.OutputField(desc="0.0 = meaning lost, 1.0 = meaning fully preserved")

judge = dspy.Predict(MeaningPreservationJudge)

def meaning_preserved(example, pred, trace=None):
    translated = pred.result.translated_text if hasattr(pred, "result") else pred.translated_text
    result = judge(
        source_text=example.source_text,
        translated_text=translated,
        target_language=example.target_language
    )
    return result.score >= 0.8
```

### Combined metric and optimization

```python
def translation_metric(example, pred, trace=None):
    return (
        glossary_compliance(example, pred) and
        meaning_preserved(example, pred)
    )

trainset = [
    dspy.Example(
        source_text="Upgrade your plan today.",
        target_language="German",
        glossary=["Pro", "Dashboard"]
    ).with_inputs("source_text", "target_language", "glossary"),
    # add more examples...
]

optimizer = dspy.MIPROv2(metric=translation_metric)
optimized_translator = optimizer.compile(
    dspy.Predict(TranslateWithGlossary),
    trainset=trainset
)
```

## When NOT to use AI translation

| Situation | Better approach |
|---|---|
| High-volume, low-stakes strings (e.g., product descriptions at scale) | DeepL API or Google Cloud Translation |
| Legal, medical, or regulated documents | Certified human translators |
| Single-word lookups or dictionary queries | Static lookup table or dictionary API |
| Real-time chat translation at high throughput | Streaming DeepL/Google with caching |

DSPy shines when you need glossary enforcement, tone control, quality estimation, or want to optimize translation prompts against a metric.

## Key patterns

| Pattern | When to use |
|---|---|
| `dspy.Predict` | Single-string translation |
| `dspy.Predict` + Pydantic output | Glossary enforcement, quality scoring |
| Batch loop per key | i18n JSON/YAML file translation |
| `dspy.MIPROv2` | Optimize for glossary compliance or fluency |
| `dspy.Refine` | Retry failed glossary terms or low-confidence segments |

## Gotchas

**Claude translates glossary terms instead of keeping them as-is.** Name the field `glossary` and state in the docstring "do not translate these terms — they must appear verbatim." Listing them inline in the docstring also helps. If terms still get translated, switch to `dspy.ChainOfThought` so the model reasons about each term explicitly.

**Claude outputs the source language when target languages are closely related.** For pairs like `en` → `pt-PT` or `es-ES` → `es-MX`, Claude sometimes returns the source text unchanged or barely modified. Always use the full locale label (`"Portuguese (Portugal)"`, `"Spanish (Mexico)"`) rather than a BCP-47 tag alone.

**Claude uses `dspy.Assert`/`dspy.Suggest` for glossary enforcement — use `dspy.Refine` instead.** Assert/Suggest are deprecated in DSPy 3.x. Use `dspy.Refine` with a reward function that checks glossary term presence. See `/dspy-refine` for the pattern.

**Claude generates overly formal translations for casual UI copy.** Pass `tone` as an explicit input field with a value like `"casual"`. Do not rely on the model to infer register from the locale. French and German LM outputs default to formal register unless explicitly instructed otherwise.

**Claude batch-translates by concatenating all strings into a single LM call.** This causes glossary drift, misattributed translations, and subtle meaning errors across long batches. Translate each string individually or in small batches of 3-5 closely related strings (e.g., a dialog's button labels together).

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/dspy-refine` - retry low-confidence segments or failed glossary enforcement with a reward function
- `/dspy-best-of-n` - sample N translations and select the best by glossary compliance + fluency score
- `/ai-improving-accuracy` - optimize translation prompts with MIPROv2 against a labeled dataset
- `/ai-checking-outputs` - validate translated output structure, glossary compliance, and format
- `/ai-generating-data` - generate synthetic parallel sentences to build a translation training set

- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples, see [examples.md](examples.md) — marketing copy translator, i18n JSON batch, support ticket with confidence scoring
- For full API signatures and parameter tables, see [reference.md](reference.md)
