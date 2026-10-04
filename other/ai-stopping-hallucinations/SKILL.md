---
name: ai-stopping-hallucinations
description: Stop your AI from making things up. Use when your AI hallucinates, fabricates facts, is not grounded in real data, does not cite sources, makes unsupported claims, or you need to verify AI responses against source material. Also use when your LLM makes up facts, responses are disconnected from the input, or outputs are not grounded in source documents. Covers citation enforcement, faithfulness verification, grounding via retrieval, confidence thresholds, and evaluation of anti-hallucination quality. Also used for AI makes up citations, LLM fabricates data, ground AI in source documents, RAG but AI still hallucinates, force AI to cite sources, factual accuracy for AI, prevent AI from inventing facts, AI confident but wrong, LLM confabulation, hallucination detection, verify AI claims against documents.
---

# Stop Your AI From Making Things Up

Guide the user through making their AI factually grounded. The core principle: never trust a bare LM output — always verify against sources.

## When NOT to use anti-hallucination patterns

- **Creative tasks** (brainstorming, fiction, ideation) — hallucination is the feature, not the bug
- **Simple extraction** where the answer is a direct copy from input — citation overhead adds cost without benefit
- **You have no source documents and cannot add them** — self-consistency checks help but retrieval-grounded approaches are far more effective. Consider `/ai-searching-docs` first to add a knowledge base

## Step 1: Understand the grounding situation

Ask the user:
1. **Do you have source documents?** (knowledge base, docs, database) → use retrieval-grounded answers
2. **Is it general knowledge?** (no docs, just the model's knowledge) → use self-consistency checks
3. **How bad is a hallucination?** (annoying vs. dangerous) → determines how strict the checks should be

## Step 2: Citation enforcement

Force the AI to cite sources for every claim. Uses `dspy.Refine` to retry generation until citation quality meets the threshold.

```python
import dspy
import re

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class CitedAnswer(dspy.Signature):
    """Answer the question using the provided sources. Cite every claim with [1], [2], etc."""
    context: list[str] = dspy.InputField(desc="Numbered source documents")
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="Answer with inline citations like [1], [2]")

def citation_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer
    context = args["context"]

    # Check citation ratio — at least half of sentences must have citations
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', answer) if s.strip()]
    citations_found = [bool(re.search(r"\[\d+\]", s)) for s in sentences]
    ratio = sum(citations_found) / max(len(sentences), 1)

    # Check all cited numbers exist in context
    cited_nums = set(int(n) for n in re.findall(r"\[(\d+)\]", answer))
    valid_nums = set(range(1, len(context) + 1))
    all_valid = cited_nums.issubset(valid_nums)

    if not all_valid:
        return 0.0
    return ratio  # 0.0 to 1.0

answerer = dspy.ChainOfThought(CitedAnswer)
citation_enforcer = dspy.Refine(answerer, N=3, reward_fn=citation_reward, threshold=0.5)

# Usage
result = citation_enforcer(context=context, question=question)
```

`dspy.Refine` retries up to `N` times, passing the reward score back as feedback so the model can improve its citations on each attempt.

## Step 3: Faithfulness verification

After generating an answer, use a second LM call to check if it's actually supported by the sources. Wraps the answerer with `dspy.Refine` so unfaithful answers are retried.

```python
class CheckFaithfulness(dspy.Signature):
    """Check if every claim in the answer is supported by the context."""
    context: list[str] = dspy.InputField(desc="Source documents")
    answer: str = dspy.InputField(desc="Generated answer to verify")
    is_faithful: bool = dspy.OutputField(desc="Is every claim supported by the context?")
    unsupported_claims: list[str] = dspy.OutputField(desc="Claims not found in context")

class FaithfulAnswerer(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought(CitedAnswer)
        self.verify = dspy.Predict(CheckFaithfulness)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)
        check = self.verify(context=context, answer=result.answer)
        # Expose faithfulness on the prediction so reward_fn can read it
        return dspy.Prediction(
            answer=result.answer,
            is_faithful=check.is_faithful,
            unsupported_claims=check.unsupported_claims,
        )

def faithfulness_reward(args: dict, pred: dspy.Prediction) -> float:
    return 1.0 if pred.is_faithful else 0.0

faithful_responder = dspy.Refine(
    FaithfulAnswerer(), N=3, reward_fn=faithfulness_reward, threshold=1.0
)

# Usage
result = faithful_responder(context=context, question=question)
```

## Step 4: Self-check pattern

Generate an answer, then ask the model to verify its own claims against the sources. Uses a reward function that gives partial credit for faithfulness — good for cases where you want the best available answer rather than a hard block.

```python
class SelfCheckedAnswerer(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought("context, question -> answer")
        self.check = dspy.ChainOfThought(CheckFaithfulness)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)
        verification = self.check(context=context, answer=result.answer)
        return dspy.Prediction(
            answer=result.answer,
            is_verified=verification.is_faithful,
            unsupported=verification.unsupported_claims,
        )

def partial_faithfulness_reward(args: dict, pred: dspy.Prediction) -> float:
    """Partial credit - 1.0 if faithful, 0.5 if partially faithful, 0.0 if not."""
    if pred.is_verified:
        return 1.0
    # Give partial credit if there are few unsupported claims
    unsupported = pred.unsupported or []
    if len(unsupported) <= 1:
        return 0.5
    return 0.0

self_checked = dspy.Refine(
    SelfCheckedAnswerer(), N=3, reward_fn=partial_faithfulness_reward, threshold=0.5
)
```

## Step 5: Cross-check pattern

Generate the answer multiple times independently and pick the one most consistent with itself. `dspy.BestOfN` samples N candidates and selects the highest-scoring one according to a reward function.

```python
class CompareAnswers(dspy.Signature):
    """Check if two independently generated answers agree on the facts."""
    answer_a: str = dspy.InputField()
    answer_b: str = dspy.InputField()
    agree: bool = dspy.OutputField(desc="Do they agree on all factual claims?")
    discrepancy: str = dspy.OutputField(desc="What they disagree on, if anything")

class GroundedAnswerer(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought("context, question -> answer")
        self.verify = dspy.Predict(CheckFaithfulness)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)
        check = self.verify(context=context, answer=result.answer)
        return dspy.Prediction(
            answer=result.answer,
            is_faithful=check.is_faithful,
            unsupported_claims=check.unsupported_claims,
        )

def faithfulness_reward(args: dict, pred: dspy.Prediction) -> float:
    return 1.0 if pred.is_faithful else 0.0

# BestOfN samples N candidates and returns the one with the highest reward
cross_checked = dspy.BestOfN(
    GroundedAnswerer(), N=3, reward_fn=faithfulness_reward, threshold=0.5
)

# Usage — returns the most faithful of the 3 sampled answers
result = cross_checked(context=context, question=question)
```

Best for high-stakes outputs where the cost of hallucination is high. Uses N LM calls but picks the most faithful result rather than retrying on failure.

## Step 6: Confidence thresholds

Flag low-confidence outputs for human review instead of showing them to users.

```python
class ConfidenceGated(dspy.Signature):
    """Answer the question and rate your confidence."""
    context: list[str] = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="0.0 to 1.0, how confident are you?")
    reasoning: str = dspy.OutputField(desc="Why this confidence level?")

class GatedResponder(dspy.Module):
    def __init__(self, threshold=0.7):
        self.respond = dspy.ChainOfThought(ConfidenceGated)
        self.threshold = threshold

    def forward(self, context, question):
        result = self.respond(context=context, question=question)

        if result.confidence < self.threshold:
            return dspy.Prediction(
                answer=result.answer,
                needs_review=True,
                confidence=result.confidence,
                reason=result.reasoning,
            )

        return dspy.Prediction(
            answer=result.answer,
            needs_review=False,
            confidence=result.confidence,
        )
```

## Step 7: Loading source data for verification

Anti-hallucination patterns need source documents. Here's how to load common formats:

### From transcript files

```python
import json, re

def load_vtt(path):
    """Extract text from a VTT transcript, stripping timestamps and cues."""
    text = open(path).read()
    lines = [line.strip() for line in text.split("\n")
             if line.strip() and not line.startswith("WEBVTT")
             and not re.match(r"\d{2}:\d{2}", line)
             and not line.strip().isdigit()]
    return " ".join(lines)

def load_livekit_transcript(path):
    """Extract text from a LiveKit transcript JSON export."""
    data = json.load(open(path))
    segments = data.get("segments", data.get("results", []))
    return " ".join(seg.get("text", "") for seg in segments)

def load_recall_transcript(transcript_data):
    """Extract text from a Recall.ai transcript response."""
    return " ".join(
        entry["words"] for entry in transcript_data if entry.get("words")
    )
```

### From Langfuse traces

```python
from langfuse import Langfuse

def load_langfuse_generations(trace_id):
    """Load LM generations from a Langfuse trace for verification."""
    langfuse = Langfuse()
    trace = langfuse.get_trace(trace_id)
    generations = []
    for obs in trace.observations:
        if obs.type == "GENERATION" and obs.output:
            generations.append({
                "input": obs.input,
                "output": obs.output,
                "model": obs.model,
            })
    return generations
```

### Breaking source documents into numbered passages

Most patterns here expect `context: list[str]` — numbered source passages. Split long documents into chunks so citations are meaningful:

```python
def chunk_document(text, max_chars=500):
    """Split a document into numbered passages for citation."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) > max_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current:
        chunks.append(current.strip())
    return [f"[{i+1}] {chunk}" for i, chunk in enumerate(chunks)]

# Use with any source
transcript_text = load_vtt("meeting.vtt")
context = chunk_document(transcript_text)
result = citation_enforcer(context=context, question="What was decided about the timeline?")
```

## Step 8: Evaluating anti-hallucination quality

You need metrics to know if your verification actually works. The key question: does the system catch hallucinations and produce faithful answers?

### Faithfulness metric

```python
def faithfulness_metric(example, prediction, trace=None):
    """Score: does the answer stick to the sources?"""
    verifier = dspy.Predict(CheckFaithfulness)
    check = verifier(context=example.context, answer=prediction.answer)

    # Binary: is it faithful?
    if not check.is_faithful:
        return 0.0

    # Bonus: does it actually answer the question?
    relevance = dspy.Predict("question, answer -> is_relevant: bool")
    rel = relevance(question=example.question, answer=prediction.answer)
    return 1.0 if rel.is_relevant else 0.5

evaluator = dspy.Evaluate(devset=devset, metric=faithfulness_metric, num_threads=4)
score = evaluator(my_grounded_qa)
```

### Citation coverage metric

```python
def citation_metric(example, prediction, trace=None):
    """Score citation quality: coverage + validity."""
    answer = prediction.answer
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', answer) if s.strip()]
    cited = [bool(re.search(r"\[\d+\]", s)) for s in sentences]
    coverage = sum(cited) / max(len(sentences), 1)

    # Check all cited sources exist
    cited_nums = set(int(n) for n in re.findall(r"\[(\d+)\]", answer))
    valid_nums = set(range(1, len(example.context) + 1))
    all_valid = cited_nums.issubset(valid_nums)

    if not all_valid:
        return 0.0
    return coverage  # 0.0 to 1.0
```

### Optimizing the verification pipeline

```python
# Create training data: questions with source context and gold answers
trainset = [
    dspy.Example(
        context=["[1] The meeting is on March 5.", "[2] Budget is $50k."],
        question="When is the meeting?",
        answer="The meeting is on March 5 [1]."
    ).with_inputs("context", "question"),
    # ... more examples
]

# Optimize the citation enforcer
optimizer = dspy.BootstrapFewShot(metric=faithfulness_metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(FaithfulAnswerer(), trainset=trainset)
optimized.save("optimized_faithful_answerer.json")

# Load later
enforcer = FaithfulAnswerer()
enforcer.load("optimized_faithful_answerer.json")
```

### Using a cheap LM for verification

The verification step doesn't need an expensive model — a smaller model checking claims against sources works well and cuts costs:

```python
class CostEfficientVerifier(dspy.Module):
    def __init__(self):
        self.answer = dspy.ChainOfThought(CitedAnswer)
        self.verify = dspy.Predict(CheckFaithfulness)

        # Use a cheaper model for the verification step
        cheap_lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-haiku-4-5-20251001", etc.
        self.verify.set_lm(cheap_lm)

    def forward(self, context, question):
        result = self.answer(context=context, question=question)
        check = self.verify(context=context, answer=result.answer)
        return dspy.Prediction(
            answer=result.answer,
            is_faithful=check.is_faithful,
            unsupported_claims=check.unsupported_claims,
        )

def faithfulness_reward(args: dict, pred: dspy.Prediction) -> float:
    return 1.0 if pred.is_faithful else 0.0

cost_efficient = dspy.Refine(
    CostEfficientVerifier(), N=3, reward_fn=faithfulness_reward, threshold=1.0
)
```

## Step 9: Batch verification

When you need to verify many responses at once (e.g., auditing a transcript Q&A system):

```python
import json

def verify_batch(qa_pairs, context, output_path="verification_results.json"):
    """Verify a batch of question-answer pairs against source context."""
    verifier = dspy.Predict(CheckFaithfulness)
    results = []

    for qa in qa_pairs:
        check = verifier(context=context, answer=qa["answer"])
        results.append({
            "question": qa["question"],
            "answer": qa["answer"],
            "is_faithful": check.is_faithful,
            "unsupported_claims": check.unsupported_claims,
        })

    # Summary
    faithful_count = sum(1 for r in results if r["is_faithful"])
    print(f"Faithful: {faithful_count}/{len(results)} "
          f"({faithful_count/len(results):.0%})")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    return results
```

## How Refine works

When `dspy.Refine` is used:
1. The wrapped module generates a candidate prediction
2. The reward function scores the prediction (0.0 to 1.0)
3. If the score meets the threshold, Refine returns that prediction immediately
4. If not, it retries up to N times, using the score as feedback signal
5. After N attempts, it returns the highest-scoring candidate seen

`dspy.BestOfN` is similar but always samples all N candidates and returns the best — useful when you want consistent sampling rather than early exit on success.

Good reward functions make Refine work better — specific scores tied to measurable properties (citation ratio, faithfulness check) outperform vague binary pass/fail.

## Choosing the right pattern

| Pattern | Cost | Latency | Best for |
|---------|------|---------|----------|
| Citation enforcement (Refine) | 1-3 LM calls | Low-Medium | When you have numbered sources |
| Faithfulness verification (Refine) | 2-6 LM calls | Medium | RAG systems, doc Q&A |
| Self-check (Refine) | 2-6 LM calls | Medium | General fact-checking |
| Cross-check (BestOfN) | N LM calls | High | High-stakes, critical outputs |
| Confidence gating | 1 LM call | Low | Human-in-the-loop systems |
| Cheap verifier (Refine) | 1 expensive + 1-3 cheap | Low-Medium | Cost-sensitive production |

## Gotchas

- **Sentence splitting on `.` breaks on abbreviations and decimals.** Naive `.split(".")` breaks on "Dr. Smith", "$50.00", and URLs, inflating the uncited sentence count and producing incorrect reward scores. Use `re.split(r'(?<=[.!?])\s+', text)` for sentence splitting instead.
- **Citation regex misses grouped citations.** When models write `[1, 2]` or `[1-3]`, the standard `\[(\d+)\]` pattern only catches `[1]` format. Extend the pattern to handle ranges and comma-separated lists, or normalize citation format in the signature instructions.
- **The faithfulness verifier defaults to the same expensive LM.** Verification is a classification task — cheaper models handle it well. Always call `.set_lm()` on the verifier predictor to use a smaller model. This typically cuts verification cost by 5-10x with minimal accuracy loss.
- **`dspy.Retrieve` requires a configured retriever.** `dspy.Retrieve` requires a retrieval model configured via `dspy.configure(rm=...)`. Without it, the call fails at runtime. Either configure a retriever or pass context directly as a function parameter.
- **Reward functions must handle missing fields gracefully.** If the module raises an exception or returns a prediction without an expected field, the reward function will error. Add `getattr(pred, "is_faithful", False)` style defensive access to avoid crashing Refine's retry loop.
- **Refine with threshold=1.0 requires a perfect score to short-circuit.** For partial-credit reward functions (0.0 to 1.0), set a threshold below 1.0 or use `BestOfN` instead — otherwise Refine always runs all N attempts.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Retrieval-augmented generation (RAG) setup — see `/ai-searching-docs`
- General output validation (format, safety, quality) — see `/ai-checking-outputs`
- Enforcing business rules and content policies — see `/ai-following-rules`
- Iterative refinement with reward functions — see `/dspy-refine`
- Sampling and selecting best outputs — see `/dspy-best-of-n`
- Retrieval model configuration and search — see `/dspy-retrieval`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For complete worked examples, see [examples.md](examples.md)
- For API signatures and parameter tables, see [reference.md](reference.md)
