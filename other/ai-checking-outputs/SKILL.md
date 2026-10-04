---
name: ai-checking-outputs
description: Verify and validate AI output before it reaches users. Use when you need guardrails, output validation, safety checks, content filtering, fact-checking AI responses, catching hallucinations, preventing bad outputs, or quality gates. Also used for - AI output looks right but is wrong, how to validate JSON from LLM, LLM returns invalid data, catch bad AI outputs before users see them, output quality gate, AI guardrails for production, verify LLM did not hallucinate fields, post-processing LLM responses. Uses dspy.Refine (iterative with feedback) and dspy.BestOfN (sampling, pick best).
---

# Check AI Output Before It Ships

Guide the user through adding verification and guardrails so bad AI outputs never reach users. The pattern: generate, check, fix or reject.

## Step 1: Understand what to check

Ask the user:
1. **What could go wrong?** (hallucinations, wrong format, offensive content, missing info, factual errors?)
2. **How strict does it need to be?** (reject bad outputs vs. try to fix them?)
3. **What's the cost of a bad output reaching users?** (annoyance vs. legal/safety risk)

## Step 2: Quick wins — Pydantic validation + dspy.Refine

The simplest way to add checks combines Pydantic for structure and `dspy.Refine` for iterative self-correction. Define a reward function that returns a float (1.0 = pass, 0.0 = fail), then wrap the module:

```python
import dspy

class GenerateResponse(dspy.Signature):
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

class CheckedResponder(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(GenerateResponse)

    def forward(self, question):
        return self.respond(question=question)

def response_quality_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer or ""
    word_count = len(answer.split())

    # Hard requirements — return 0.0 if violated
    if len(answer) == 0:
        return 0.0
    if word_count > 200:
        return 0.0

    # Soft preferences reduce score
    score = 1.0
    if "i don't know" in answer.lower():
        score -= 0.3
    if any(w in answer.lower() for w in ["definitely", "absolutely", "100%"]):
        score -= 0.2
    return max(score, 0.0)

# Wrap with Refine — retries up to N times feeding back the reward signal
checked = dspy.Refine(CheckedResponder(), N=3, reward_fn=response_quality_reward, threshold=0.8)
result = checked(question="What is the boiling point of water?")
```

`dspy.Refine` retries the module up to `N` times, passing reward feedback to guide self-correction. `dspy.BestOfN` generates `N` candidates in parallel and returns the one with the highest reward — use it when you want diversity rather than iterative refinement.

## Step 3: Format validation

### Type-based validation (automatic)

DSPy validates typed outputs automatically:

```python
from typing import Literal
from pydantic import BaseModel, Field

class Response(BaseModel):
    answer: str = Field(min_length=1, max_length=500)
    confidence: float = Field(ge=0.0, le=1.0)
    category: str

class MySignature(dspy.Signature):
    question: str = dspy.InputField()
    response: Response = dspy.OutputField()
```

Pydantic catches malformed JSON, out-of-range values, and wrong types before your code ever sees them.

### Custom format validation with dspy.Refine

```python
import re

class ExtractContact(dspy.Signature):
    text: str = dspy.InputField()
    email: str = dspy.OutputField()
    phone: str = dspy.OutputField()

class ContactExtractor(dspy.Module):
    def __init__(self):
        self.extract = dspy.ChainOfThought(ExtractContact)

    def forward(self, text):
        return self.extract(text=text)

def contact_format_reward(args: dict, pred: dspy.Prediction) -> float:
    email_ok = bool(re.match(r"[^@]+@[^@]+\.[^@]+", pred.email or ""))
    phone_digits = len(re.sub(r"\D", "", pred.phone or ""))
    phone_ok = phone_digits >= 10

    if not email_ok or not phone_ok:
        return 0.0
    return 1.0

validated = dspy.Refine(ContactExtractor(), N=3, reward_fn=contact_format_reward, threshold=1.0)
result = validated(text="Call me at 555-1234567 or email bob@example.com")
```

## Step 4: Factual verification

### Self-check — ask the AI to verify its own output

```python
class VerifyFacts(dspy.Signature):
    """Check if the answer is supported by the given context."""
    context: list[str] = dspy.InputField(desc="Source documents")
    answer: str = dspy.InputField(desc="Generated answer to verify")
    is_supported: bool = dspy.OutputField(desc="Is the answer fully supported by the context?")
    unsupported_claims: list[str] = dspy.OutputField(desc="Claims not found in context")

class GroundedResponder(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=5)
        self.answer = dspy.ChainOfThought(AnswerFromDocs)
        self.verify = dspy.Predict(VerifyFacts)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

def faithfulness_reward(args: dict, pred: dspy.Prediction) -> float:
    context = args.get("context", [])
    # Use a verify module to check grounding — instantiate outside for efficiency
    check = verify_module(context=context, answer=pred.answer)
    if not check.is_supported:
        return 0.0
    return 1.0

# Note: build verify_module once at the module level
verify_module = dspy.Predict(VerifyFacts)

grounded = dspy.Refine(GroundedResponder(), N=3, reward_fn=faithfulness_reward, threshold=1.0)
result = grounded(question="What did the report say about Q3 revenue?")
```

### Cross-check — generate two ways, compare

```python
class CompareAnswers(dspy.Signature):
    """Check if two independently generated answers agree."""
    question: str = dspy.InputField()
    answer_a: str = dspy.InputField()
    answer_b: str = dspy.InputField()
    agree: bool = dspy.OutputField(desc="Do the answers substantially agree?")
    discrepancy: str = dspy.OutputField(desc="What they disagree on, if anything")

class CrossCheckedAnswer(dspy.Module):
    def __init__(self):
        self.answer_b = dspy.ChainOfThought(AnswerQuestion)
        self.compare = dspy.ChainOfThought(CompareAnswers)

    def forward(self, question, answer_a):
        b = self.answer_b(question=question)
        comparison = self.compare(
            question=question,
            answer_a=answer_a,
            answer_b=b.answer,
        )
        return comparison

# Use BestOfN to generate N candidates then pick the most consistent one
def consistency_reward(args: dict, pred: dspy.Prediction) -> float:
    # Higher confidence answers score better; refine toward agreement
    return 1.0 if pred.agree else 0.0
```

## Step 5: Safety and content filtering

### Block harmful outputs with dspy.Refine

```python
import re

BLOCKED_PATTERNS = [
    r"\b(password|secret|api.?key)\b",
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
]

class SafeResponder(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(GenerateResponse)

    def forward(self, question):
        return self.respond(question=question)

def safety_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer or ""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, answer, re.IGNORECASE):
            return 0.0
    return 1.0

safe_responder = dspy.Refine(SafeResponder(), N=3, reward_fn=safety_reward, threshold=1.0)
result = safe_responder(question="Tell me about our API authentication setup")
```

### AI-as-safety-judge

```python
class SafetyCheck(dspy.Signature):
    """Check if the response is safe and appropriate."""
    question: str = dspy.InputField()
    response: str = dspy.InputField()
    is_safe: bool = dspy.OutputField()
    concern: str = dspy.OutputField(desc="Safety concern if not safe, empty if safe")

safety_judge = dspy.Predict(SafetyCheck)

class SafetyCheckedResponder(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought(GenerateResponse)

    def forward(self, question):
        return self.respond(question=question)

def ai_safety_reward(args: dict, pred: dspy.Prediction) -> float:
    check = safety_judge(question=args["question"], response=pred.answer)
    return 1.0 if check.is_safe else 0.0

safe_checked = dspy.Refine(SafetyCheckedResponder(), N=3, reward_fn=ai_safety_reward, threshold=1.0)
```

## Step 6: Sampling and picking best — BestOfN

For high-stakes outputs, use `dspy.BestOfN` to generate multiple independent candidates and keep the highest-scoring one:

```python
class GenerateAnswer(dspy.Signature):
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

class AnswerModule(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        return self.generate(question=question)

def answer_quality_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer or ""
    if len(answer) == 0:
        return 0.0
    word_count = len(answer.split())
    if word_count > 200:
        return 0.0
    # Reward concise, substantive answers
    score = min(word_count / 50.0, 1.0)
    return score

# Generate 5 candidates, return the one with the highest reward
best = dspy.BestOfN(AnswerModule(), N=5, reward_fn=answer_quality_reward, threshold=0.5)
result = best(question="Explain why the sky is blue")
```

Use `BestOfN` when diversity matters — it does not feed one attempt's feedback into the next. Use `Refine` when you want iterative self-correction with prior context.

## How Refine/BestOfN works

`dspy.Refine`:
1. Runs the module once and scores the output with `reward_fn`
2. If the score is below `threshold`, it retries — passing the reward signal back as feedback context
3. Repeats up to `N` times total
4. Returns the best-scoring output, or raises if `fail_count` is set and too many attempts fail

`dspy.BestOfN`:
1. Runs the module `N` times independently (no shared feedback between runs)
2. Scores each output with `reward_fn`
3. Returns the output with the highest score above `threshold`
4. Raises if none meet the threshold (or if `fail_count` is hit)

This is why **reward functions must be specific** — a score of 0.3 vs 0.9 signals very different things to Refine's retry logic. Return 0.0 for hard failures, partial scores for soft preferences.

When combined with optimization (`/ai-improving-accuracy`), the model learns to satisfy reward functions on the first try, reducing retries in production.

## When NOT to use output checking

Do not reach for Refine/BestOfN when simpler approaches work:

- **Pydantic alone is enough for pure format validation.** If you only need type/range/length checking, DSPy's typed signatures with Pydantic models handle this automatically with retries — no reward function needed.
- **You have < 50ms latency budget.** Each Refine retry doubles LM latency. If speed matters more than perfection, optimize prompts instead (`/ai-improving-accuracy`).
- **The failure is in the prompt, not the output.** If the model consistently produces bad output on the first attempt, fixing the signature or adding demonstrations is more effective than retrying 3 times and hoping for luck.
- **You need human review anyway.** If outputs go through human QA before reaching users, adding AI-as-judge adds cost without reducing risk.

Consider `/ai-following-rules` for declarative constraint enforcement, or `/ai-improving-accuracy` for systematic prompt optimization that reduces the need for post-hoc checking.

## Key patterns

- **dspy.Refine for iterative correction** — format, length, safety. Retries with feedback automatically.
- **dspy.BestOfN for diversity** — generate many independently, pick the best-scoring one.
- **Pydantic for structure** — catches malformed output automatically before reward evaluation.
- **Self-verification for facts** — ask the AI "is this grounded in the sources?" inside the reward function.
- **Cross-checking for reliability** — generate twice independently, compare in reward function.
- **Regex for sensitive data** — block SSNs, API keys, passwords in the reward function.
- **threshold=1.0 for hard requirements** — only accept a perfect score (binary pass/fail checks).
- **threshold < 1.0 for soft requirements** — accept good-enough outputs with partial scores.

## Checklist: what to check

| Check | When to use | How |
|-------|------------|-----|
| Non-empty output | Always | return 0.0 in reward_fn if len(answer) == 0 |
| Length limits | User-facing text | return 0.0 if word count exceeds N |
| Valid format | Structured output | Pydantic model + reward_fn format check |
| Grounded in sources | RAG / doc search | Verification signature inside reward_fn |
| No sensitive data | Any user-facing output | Regex patterns in reward_fn |
| Safe content | Public-facing apps | AI safety judge inside reward_fn |
| Consistent | Critical decisions | Cross-check two generations in reward_fn |
| High quality | High-stakes outputs | dspy.BestOfN with quality reward_fn |

## Expected improvement

| Approach | Bad output rate (typical) | Notes |
|----------|--------------------------|-------|
| Typed signature only | ~15-25% format errors | Pydantic retries handle most |
| + Refine with reward_fn (N=3) | ~2-5% | Iterative feedback fixes most remaining |
| + BestOfN (N=5) with quality reward | ~1-3% | Best for creative/high-stakes tasks |
| + AI-as-judge in reward_fn | < 1% | Highest quality, 2x LM cost per attempt |

Exact numbers depend on task difficulty and model capability. Measure your baseline first with `dspy.Evaluate` before adding checks.

## Gotchas

- **Reward functions must return float, not bool.** `dspy.Refine` and `dspy.BestOfN` expect a float from `reward_fn(args, pred)`. Returning `True`/`False` or raising an exception will cause unexpected behavior. Always return `0.0` for failure and `1.0` (or a partial score) for success.
- **args contains the module's input kwargs.** The `args` dict passed to `reward_fn` holds the keyword arguments the module was called with. Access them by name: `args["question"]`, `args["context"]`. Don't assume positional order.
- **AI-as-judge inside reward_fn multiplies LM calls.** If your reward function calls another LM to verify, each Refine/BestOfN attempt costs two LM calls. For low-stakes outputs (summaries, suggestions), regex or Pydantic checks are sufficient. Reserve AI-as-judge for high-stakes outputs.
- **threshold=1.0 causes frequent failures on partial scores.** If your reward function returns partial scores (0.3, 0.7, etc.), a threshold of 1.0 means only perfect scores pass — Refine will retry every time. Set threshold to a realistic pass mark for your scoring scale, e.g. 0.8 for a 0–1 quality score.
- **Don't instantiate LM modules inside reward_fn.** Creating a `dspy.Predict` or `dspy.ChainOfThought` inside the reward function creates a new module object on every call. Instantiate verification modules once at the module or class level and reference them in the closure.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/ai-stopping-hallucinations` — citation enforcement, faithfulness verification, grounding AI in facts
- `/ai-following-rules` — defining and enforcing content policies, format rules, and business constraints
- `/ai-building-pipelines` — wire checks into multi-step systems
- `/ai-making-consistent` — output consistency (not correctness)
- `/ai-testing-safety` — stress-test your guardrails with adversarial attacks
- `/ai-scoring` — evaluate human work against criteria
- `/ai-improving-accuracy` — measure and improve quality systematically
- `/dspy-refine` — deep-dive on iterative refinement with reward functions
- `/dspy-best-of-n` — deep-dive on sampling N candidates and picking the best
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples, see [examples.md](examples.md)
- For Refine/BestOfN API details, see [reference.md](reference.md)
