---
name: ai-following-rules
description: Make your AI follow rules and policies. Use when your AI breaks format rules, violates content policies, ignores business constraints, outputs invalid JSON, exceeds length limits, includes forbidden content, or does not comply with your specifications. Also use when LLM JSON output is unreliable, you get inconsistent formatting with random spaces and line breaks, or there is extraneous text and conversational fluff around the JSON. Covers dspy.Refine and dspy.BestOfN for hard and soft rule enforcement, content policies, format enforcement, retry mechanics, and composing multiple constraints. Also used for - AI will not follow my system prompt, LLM keeps breaking format, enforce JSON schema on AI output, AI generates prohibited content, constraint violation from LLM, make AI obey business rules, AI ignores my constraints.
---

# Make Your AI Follow the Rules

Guide the user through defining and enforcing rules their AI must follow. The key insight: don't ask the AI to follow rules — **program constraints that enforce them automatically**.

## Step 1: Identify your rules

Ask the user:
1. **What rules does the AI break?** (too long? wrong format? forbidden content? missing fields?)
2. **Which rules are hard requirements vs nice-to-haves?** (Refine with threshold vs lower reward weight)
3. **What should happen when a rule is broken?** (retry with feedback, pick best attempt, fail loudly)

## Step 2: The two enforcement patterns

DSPy 3.x provides two constraint primitives — `dspy.Refine` and `dspy.BestOfN`:

| | `dspy.Refine` | `dspy.BestOfN` |
|--|--------------|----------------|
| **Behavior** | Iterative - retries with feedback until threshold met | Parallel - runs N times, picks best score |
| **Use for** | Strict rules where feedback helps the LM self-correct | Rules where sampling variation is more useful than feedback |
| **On failure** | Retries up to N times; raises error if threshold never met | Always returns best result out of N attempts |
| **PM translation** | "It **must** meet the bar — keep trying" | "Give me the best of several tries" |

```python
import dspy

# dspy.Refine — retry with feedback until reward_fn score meets threshold
refine = dspy.Refine(
    module,       # The DSPy module to wrap (required)
    N=3,          # Max number of attempts (required, int)
    reward_fn=reward_fn,   # Callable(args_dict, prediction) -> float (required)
    threshold=1.0,         # Accept output when reward reaches this score (required, float)
    fail_count=3,          # Raise error after this many failures (optional, defaults to N)
)

# dspy.BestOfN — run N times independently, return highest-scoring result
best_of_n = dspy.BestOfN(
    module,
    N=5,
    reward_fn=reward_fn,
    threshold=0.8,         # Early-stop if any attempt clears this score
)
```

**Reward function signature** - takes the input args dict and the prediction, returns a float:

```python
def reward_fn(args: dict, pred: dspy.Prediction) -> float:
    # args contains the inputs passed to the module (e.g. args["question"])
    # pred contains the module outputs (e.g. pred.answer)
    # return 1.0 for pass, 0.0 for fail, or a score in between
    ...
```

## Step 3: Writing reward functions for rule checking

**Binary reward** — pass/fail single rule:

```python
def length_reward(args: dict, pred: dspy.Prediction) -> float:
    return 1.0 if len(pred.answer.split()) <= 280 else 0.0
```

**Graduated reward** — partial credit encourages improvement:

```python
def length_reward_graduated(args: dict, pred: dspy.Prediction) -> float:
    words = len(pred.answer.split())
    if words <= 280:
        return 1.0
    elif words <= 350:
        return 0.5   # Close — reward partial compliance
    else:
        return 0.0
```

**Multi-rule reward** — combine hard and soft rules in one function:

```python
def policy_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer
    score = 1.0

    # Hard rules — disqualify immediately if broken
    if len(answer.split()) > 280:
        return 0.0
    if any(word in answer.lower() for word in BLOCKED_WORDS):
        return 0.0

    # Soft rules — deduct points but don't disqualify
    if not answer[0].isupper():
        score -= 0.1
    if not (answer.endswith(".") or answer.endswith("!") or answer.endswith("?")):
        score -= 0.1

    return score
```

## Step 4: Content policy example

Enforce what the AI can and cannot say.

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

BLOCKED_WORDS = ["competitor_name", "profanity1", "profanity2"]  # your list

class PolicyCheckedResponse(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.respond(question=question)

def content_policy_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer
    score = 1.0

    # Hard rules — must comply
    if len(answer.split()) > 280:
        return 0.0
    if any(word in answer.lower() for word in BLOCKED_WORDS):
        return 0.0
    if "disclaimer" in answer.lower():
        return 0.0

    # Soft rules — prefer compliance but don't block
    if not answer[0].isupper():
        score -= 0.1
    if not (answer.endswith(".") or answer.endswith("!") or answer.endswith("?")):
        score -= 0.1

    return score

# Wrap with Refine for strict enforcement
enforced = dspy.Refine(
    PolicyCheckedResponse(),
    N=3,
    reward_fn=content_policy_reward,
    threshold=0.8,
)

result = enforced(question="What is your return policy?")
print(result.answer)
```

## Step 5: Format rules example

Enforce output structure — valid JSON, required fields, correct types. Combine Pydantic (catches type/structure errors) with a reward function (catches logic errors) for the strongest format enforcement.

```python
import dspy
from pydantic import BaseModel, Field
from typing import Literal

class QuizQuestion(BaseModel):
    question: str = Field(min_length=10)
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    difficulty: Literal["easy", "medium", "hard"]

class GenerateQuiz(dspy.Signature):
    """Generate a quiz question about the topic."""
    topic: str = dspy.InputField()
    quiz: QuizQuestion = dspy.OutputField()

class QuizGenerator(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought(GenerateQuiz)

    def forward(self, topic):
        return self.generate(topic=topic)

def quiz_logic_reward(args: dict, pred: dspy.Prediction) -> float:
    quiz = pred.quiz

    # Correct answer must be one of the options
    if quiz.correct_answer not in quiz.options:
        return 0.0

    # All options must be unique
    if len(set(quiz.options)) != 4:
        return 0.0

    return 1.0

# Pydantic handles structure; Refine enforces logic rules
enforced = dspy.Refine(
    QuizGenerator(),
    N=3,
    reward_fn=quiz_logic_reward,
    threshold=1.0,
)

result = enforced(topic="Python programming")
print(result.quiz)
```

## Step 6: Business constraint example

Translate business requirements into a multi-criteria reward function.

```python
import dspy

COMPETITORS = ["competitor_a", "competitor_b"]

class PricingResponse(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought("customer_question, pricing_docs -> answer")

    def forward(self, customer_question, pricing_docs):
        return self.respond(
            customer_question=customer_question,
            pricing_docs=pricing_docs,
        )

def pricing_policy_reward(args: dict, pred: dspy.Prediction) -> float:
    answer = pred.answer
    score = 1.0

    # Never mention competitor pricing (hard rule)
    if any(comp in answer.lower() for comp in COMPETITORS):
        return 0.0

    # Never offer unauthorized discounts (hard rule)
    if "discount" in answer.lower() and "authorized" not in answer.lower():
        return 0.0

    # Should include a CTA (soft rule - deduct but don't disqualify)
    cta_words = ["contact", "sign up", "learn more", "get started"]
    if not any(cta in answer.lower() for cta in cta_words):
        score -= 0.2

    return score

enforced = dspy.Refine(
    PricingResponse(),
    N=3,
    reward_fn=pricing_policy_reward,
    threshold=0.8,
)
```

## Step 7: Combining hard and soft rules in one reward function

The pattern: hard violations return 0.0 immediately; soft violations deduct from a starting score of 1.0.

```python
def tweet_reward(args: dict, pred: dspy.Prediction) -> float:
    tweet = pred.tweet
    key_facts = args["key_facts"]
    score = 1.0

    # Hard rules — return 0 immediately if broken
    if len(tweet) > 280:
        return 0.0
    if "#" in tweet:
        return 0.0
    if not any(fact.lower() in tweet.lower() for fact in key_facts):
        return 0.0

    # Soft rules — deduct points
    if tweet.startswith("Did you know"):
        score -= 0.15
    if any(ord(c) > 127 for c in tweet):
        score -= 0.1

    return score

class TweetWriter(dspy.Module):
    def __init__(self):
        self.write = dspy.ChainOfThought("topic, key_facts -> tweet")

    def forward(self, topic, key_facts):
        return self.write(topic=topic, key_facts=key_facts)

enforced = dspy.Refine(
    TweetWriter(),
    N=4,
    reward_fn=tweet_reward,
    threshold=0.8,
)

result = enforced(topic="climate tech", key_facts=["30% emissions cut", "solar costs fell 90%"])
print(result.tweet)
```

When rules conflict (e.g., "include all key facts" vs "stay under 280 chars"), make the **harder constraint return 0.0** so the model prioritizes it.

**Verify reward functions in isolation** before wrapping with Refine — create a `dspy.Prediction` directly to unit-test edge cases:

```python
# Test each rule path before you wrap with Refine
test_pass = dspy.Prediction(tweet="Solar costs fell 90% — a decade of progress.")
test_fail = dspy.Prediction(tweet="Solar costs fell 90% #renewable http://link.com — too long text here exceeding limits for this platform, really long")
assert tweet_reward({"key_facts": ["Solar costs fell 90%"]}, test_pass) == 1.0
assert tweet_reward({"key_facts": ["Solar costs fell 90%"]}, test_fail) < 1.0
```

## Step 8: Optimizing with rules

DSPy optimizers work alongside Refine and BestOfN. Combine the rule reward function with a quality metric so the optimizer learns prompts that naturally comply with constraints — reducing how often Refine needs to retry in production.

```python
import dspy

def combined_metric(example, pred, trace=None):
    # Quality component
    quality = 1.0 if pred.answer.strip() == example.expected_answer.strip() else 0.0
    # Rule compliance component (reuse the reward function)
    compliance = tweet_reward({"key_facts": example.key_facts}, pred)
    return 0.5 * quality + 0.5 * compliance

optimizer = dspy.MIPROv2(metric=combined_metric, num_threads=4)
optimized = optimizer.compile(
    TweetWriter(),           # Optimize the base module, not the Refine wrapper
    trainset=trainset,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
)

# Then wrap the optimized module with Refine for production
production = dspy.Refine(
    optimized,
    N=3,
    reward_fn=tweet_reward,
    threshold=0.8,
)
```

## When NOT to use Refine or BestOfN

- **Output is already a Pydantic model with full validation.** If your constraints are purely structural (types, field presence, enum values), Pydantic handles it natively. Only add Refine for logic constraints Pydantic cannot express (e.g., "correct_answer must be in options").
- **You need real-time content moderation at scale.** Refine retries are LM calls — expensive and slow. For high-throughput moderation, use a dedicated classifier (`/ai-moderating-content`) and reserve Refine for the final generation step.
- **The constraint is vague or subjective.** "Be more creative" or "sound professional" cannot be scored programmatically. Use optimization (`/ai-improving-accuracy`) to improve subjective quality rather than a reward function that has no reliable signal.
- **N=1 with threshold=1.0 and a strict binary reward.** This is equivalent to a single pass — if it fails, you get an error. Either increase N, lower the threshold, or use a graduated reward function.

## Gotchas

- **Claude writes the reward function to take `(pred)` instead of `(args, pred)`.** The reward function signature must be `(args: dict, pred: dspy.Prediction) -> float`. The `args` dict contains the input fields passed to the module. Omitting it causes a TypeError at runtime.
- **Claude places the reward function call inside the module's `forward` method.** The reward function is passed to Refine/BestOfN as a callback — it is called by the framework, not by the module itself. Calling it in `forward` breaks the retry loop.
- **Claude uses `assert` (Python builtin) or old `dspy.Assert`/`dspy.Suggest` from DSPy 2.x.** These are removed in DSPy 3.x. Use `dspy.Refine` and `dspy.BestOfN` with a reward function instead.
- **Claude wraps the Refine result in another try/except that swallows failures.** If Refine exhausts all attempts without meeting the threshold, it raises an error. Catching it silently hides compliance failures. Let it propagate — or handle it explicitly to fall back or log.
- **Claude puts conflicting hard rules in the reward function and is surprised the LM never meets threshold.** If "include all facts" and "stay under 100 words" cannot both be true for the given inputs, Refine will always fail. Relax one rule or increase N and lower the threshold to get a best-effort result.
- **Claude optimizes the Refine wrapper instead of the base module.** Pass the base module to the optimizer, then wrap the optimized result with Refine. Compiling the wrapper directly wastes N*attempts LM calls per training example.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Output verification** for quality gates beyond rules — see `/ai-checking-outputs`
- **Grounding in facts** to prevent hallucination — see `/ai-stopping-hallucinations`
- **Measuring accuracy** after adding rules — see `/ai-improving-accuracy`
- **Adversarial testing** to verify rules hold — see `/ai-testing-safety`
- **Content moderation** at scale — see `/ai-moderating-content`
- **dspy.Refine API** for deeper reference — see `/dspy-refine`
- **dspy.BestOfN API** for deeper reference — see `/dspy-best-of-n`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For complete worked examples, see [examples.md](examples.md)
- For API signatures, parameter tables, and threshold guidance, see [reference.md](reference.md)
