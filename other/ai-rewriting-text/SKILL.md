---
name: ai-rewriting-text
description: Rewrite text to match a different tone, reading level, or audience using AI. Use when rewriting content in a different tone, simplifying legal language, adapting text for a different audience, converting technical docs to plain English, making formal text casual, adjusting reading level, matching brand voice in existing content, paraphrasing for clarity, converting jargon-heavy text to simple language, tone transformation, style transfer for text, rewriting marketing copy, making content more accessible, executive summary from technical report.
---

# ai-rewriting-text

Rewrite existing text to match a different tone, style, reading level, or audience using DSPy. The core pattern is - source text + target style/tone/audience → rewritten text. Evaluation uses a dual-judge metric that separately scores meaning preservation (fidelity) and style match.

## Step 1 - Understand the rewriting task

Before writing code, clarify:

- **What text?** — source content (paragraph, article, legal clause, doc page)
- **What target style?** — tone (casual, formal, friendly, authoritative), audience (developers, executives, general public), and reading level if applicable
- **How much liberty?** — strict paraphrase vs. free rewrite; anything that must stay verbatim
- **What to preserve?** — key facts, headings, bullet points, specific terminology, length constraints

## Step 2 - Build basic rewriter

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class RewriteText(dspy.Signature):
    """Rewrite the source text to match the specified tone and audience.
    Preserve all factual claims and key information from the original.
    Do not add new claims or information not present in the source.
    Output length should be similar to the input length unless instructed otherwise."""

    source_text: str = dspy.InputField(desc="The original text to rewrite")
    target_tone: str = dspy.InputField(desc="Desired tone - e.g. casual, formal, friendly, authoritative")
    target_audience: str = dspy.InputField(desc="Who the rewritten text is for - e.g. developers, executives, general public")
    rewritten_text: str = dspy.OutputField(desc="The rewritten text matching the specified tone and audience")

rewriter = dspy.Predict(RewriteText)

result = rewriter(
    source_text="The system leverages a multi-tiered caching architecture to minimize latency.",
    target_tone="casual",
    target_audience="general public",
)
print(result.rewritten_text)
# → "The app stores frequently used data nearby so it loads faster for you."
```

## Step 3 - Pass style examples

Provide 2-3 examples of the target style to anchor the model's output.

```python
class RewriteWithExamples(dspy.Signature):
    """Rewrite the source text to match the tone and style shown in the examples.
    Preserve all factual claims. Do not add new information.
    Output length should be similar to input length unless instructed otherwise."""

    source_text: str = dspy.InputField(desc="The original text to rewrite")
    target_tone: str = dspy.InputField(desc="Desired tone description")
    target_audience: str = dspy.InputField(desc="Target audience")
    style_examples: str = dspy.InputField(desc="2-3 example passages written in the target style, separated by ---")
    rewritten_text: str = dspy.OutputField(desc="Rewritten text matching the tone and style of the examples")

rewriter = dspy.Predict(RewriteWithExamples)

style_examples = """
Our dashboard gives you a clear picture of what's happening right now.
---
Setting up takes about two minutes. No credit card, no fuss.
---
We built this for teams who'd rather ship than configure.
"""

result = rewriter(
    source_text="The analytics module provides real-time visibility into system telemetry.",
    target_tone="casual, direct, startup-friendly",
    target_audience="small business owners",
    style_examples=style_examples,
)
```

## Step 4 - Reading level adjustment

```python
class RewriteToReadingLevel(dspy.Signature):
    """Rewrite the source text to match the specified reading level.
    Use vocabulary and sentence structures appropriate for the grade level.
    Preserve all key information. Do not add new claims.
    Output length should be similar to input length unless instructed otherwise."""

    source_text: str = dspy.InputField(desc="The original text to rewrite")
    target_reading_level: str = dspy.InputField(desc="Target reading level - e.g. '5th grade', '8th grade', 'college'")
    rewritten_text: str = dspy.OutputField(desc="Rewritten text at the target reading level")

rewriter = dspy.Predict(RewriteToReadingLevel)

result = rewriter(
    source_text=(
        "Photosynthesis is the biochemical process by which chlorophyll-containing organisms "
        "convert radiant energy from solar radiation into chemical energy stored as glucose."
    ),
    target_reading_level="5th grade",
)
```

To measure reading level programmatically, install `textstat`:

```python
import textstat

score = textstat.flesch_kincaid_grade(result.rewritten_text)
print(f"Flesch-Kincaid grade level: {score:.1f}")
```

## Step 5 - Dual-judge fidelity and style evaluation

One judge scores meaning preservation (fidelity), another scores style match.

```python
class FidelityJudge(dspy.Signature):
    """Score how well the rewritten text preserves the meaning and key facts of the original.
    Score 0-1 where 1 means all key information is preserved with no additions or omissions."""

    source_text: str = dspy.InputField()
    rewritten_text: str = dspy.InputField()
    fidelity_score: float = dspy.OutputField(desc="Float 0-1")
    reasoning: str = dspy.OutputField(desc="Brief explanation of score")

class StyleJudge(dspy.Signature):
    """Score how well the rewritten text matches the target tone and audience.
    Score 0-1 where 1 means the tone and style are a perfect match."""

    rewritten_text: str = dspy.InputField()
    target_tone: str = dspy.InputField()
    target_audience: str = dspy.InputField()
    style_score: float = dspy.OutputField(desc="Float 0-1")
    reasoning: str = dspy.OutputField(desc="Brief explanation of score")

fidelity_judge = dspy.Predict(FidelityJudge)
style_judge = dspy.Predict(StyleJudge)

def rewrite_metric(example, prediction, trace=None):
    fidelity = fidelity_judge(
        source_text=example.source_text,
        rewritten_text=prediction.rewritten_text,
    )
    style = style_judge(
        rewritten_text=prediction.rewritten_text,
        target_tone=example.target_tone,
        target_audience=example.target_audience,
    )
    return float(fidelity.fidelity_score) * float(style.style_score)
```

## Step 6 - When to rewrite vs regenerate

| Content length | Approach | Reason |
|---|---|---|
| < 200 words | Regenerate from scratch | Short enough that full regeneration is fast and clean |
| > 200 words | Rewrite preserving structure | Prevents losing details buried in long content |
| Highly technical | Rewrite with explicit preserve-facts instruction | Regeneration risks dropping precision |
| Structured (lists, tables) | Rewrite paragraph-by-paragraph | Keeps formatting intact |
| Marketing copy | Either — prefer regeneration | Creative latitude usually wanted |

## Step 7 - Brand voice matching

Pass brand guidelines and example content as inputs so the model can anchor to a specific voice.

```python
class BrandVoiceRewriter(dspy.Signature):
    """Rewrite the source text to match the brand voice described in the guidelines
    and demonstrated in the brand examples. Preserve all factual information.
    Do not add new claims. Match the vocabulary, sentence rhythm, and personality
    shown in the examples."""

    source_text: str = dspy.InputField(desc="Text to rewrite")
    brand_guidelines: str = dspy.InputField(desc="Brand voice description - tone, personality, dos and donts")
    brand_examples: str = dspy.InputField(desc="2-3 example passages written in the brand voice, separated by ---")
    rewritten_text: str = dspy.OutputField(desc="Text rewritten in the brand voice")

rewriter = dspy.Predict(BrandVoiceRewriter)
```

## Step 8 - Evaluate and optimize

```python
import dspy

trainset = [
    dspy.Example(
        source_text="Authentication uses OAuth 2.0 with PKCE flow.",
        target_tone="casual, friendly",
        target_audience="non-technical users",
        rewritten_text="Signing in is secure — we use industry-standard login protection behind the scenes.",
    ).with_inputs("source_text", "target_tone", "target_audience"),
    # add more examples
]

optimizer = dspy.BootstrapFewShot(metric=rewrite_metric, max_bootstrapped_demos=3)
optimized_rewriter = optimizer.compile(dspy.Predict(RewriteText), trainset=trainset)
```

Typical improvement: composite fidelity*style metric moves from ~0.55 baseline to ~0.78 after BootstrapFewShot with 3 demos on a trainset of 25+ examples. Run `dspy.Evaluate(devset=devset, metric=rewrite_metric)` before and after to measure.

## When NOT to use AI rewriting

- **Legal or regulatory text** — tone changes can alter legal meaning; requires human review
- **Already well-written content** — if the original is clear and appropriate, rewriting adds risk
- **Simple terminology swaps** — use find-and-replace; AI adds unnecessary variability
- **Translation between languages** — use `/ai-translating-content` instead (different task)
- **Content with precise numerical claims** — AI can silently alter figures during rewriting

## Key patterns

| Goal | Approach |
|---|---|
| Tone change | `target_tone` input + style examples |
| Reading level | `target_reading_level` + textstat measurement |
| Brand voice | Brand guidelines + example passages as inputs |
| Long content | Process paragraph-by-paragraph |
| High-fidelity | Dual-judge metric + explicit preserve-facts instruction |
| Optimization | BootstrapFewShot with composite fidelity * style metric |

## Gotchas

- **Claude regenerates instead of rewriting, losing specific facts** — always run a fidelity judge that compares key claims between source and output; add "preserve all factual claims" to the signature docstring.
- **Tone changes are inconsistent across paragraphs in long text** — split content at paragraph boundaries and rewrite each chunk with the same tone instruction, then reassemble.
- **Claude adds new information not in the original** — put "Do not add new claims or information not present in the source" in the signature docstring; the fidelity judge will catch violations.
- **Simplified text becomes much shorter, dropping important details** — include "Output length should be similar to input length unless instructed otherwise" in the signature docstring.
- **Style examples pulled from the wrong domain cause register mismatch** — examples must match both the tone AND the domain (e.g. use software product copy as examples when rewriting software product copy, not general prose).

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/dspy-refine` — iterative refinement with feedback; use when first rewrite fails fidelity or style checks and you want automatic retry with correction signals
- `/dspy-modules` — composing multi-step DSPy modules; use when chaining extraction + rewriting + validation
- `/ai-improving-accuracy` — systematic accuracy improvement techniques that apply to rewriting pipelines
- `/ai-checking-outputs` — output validation patterns; use to enforce fidelity constraints on rewritten text
- `/ai-generating-data` — generate synthetic (source, rewritten) training pairs to build a labeled trainset for optimization
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples, see [examples.md](examples.md) — technical-to-plain-English, tone adapter, and reading level adjuster.
- For API signatures and parameter tables, see [reference.md](reference.md).
