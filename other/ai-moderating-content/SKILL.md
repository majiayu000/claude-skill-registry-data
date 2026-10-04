---
name: ai-moderating-content
description: Auto-moderate what users post on your platform. Use when you need content moderation, flag harmful comments, detect spam, filter hate speech, catch NSFW content, block harassment, moderate user-generated content, review community posts, filter marketplace listings, or route bad content to human reviewers. Also used for build content moderation system, UGC moderation at scale, user-generated content filter, trust and safety tooling, hate speech detection model, NSFW detection API, toxic comment classifier, automated abuse detection, report and flag system with AI, content policy enforcement, marketplace listing moderation, DSPy classification with severity scoring, confidence-based routing, reward-based policy enforcement.
---

# Auto-Moderate What Users Post

Guide the user through building AI content moderation — classify user-generated content, score severity, and route decisions (auto-approve, human-review, auto-reject). The pattern: classify, score, route.

## When NOT to use AI moderation

- **Low-volume content** — if a human can review everything in under an hour per day, skip AI. The complexity of maintaining a moderation pipeline is not worth it.
- **Exact-match violations only** — if your policy is just a blocklist of words or regex patterns (SSNs, emails, phone numbers), use pattern matching directly. No LM needed.
- **Legal-grade decisions** — AI moderation is a first pass, not a legal ruling. If a wrong moderation decision has legal consequences (DMCA takedowns, defamation claims), always route to human review.

Consider `/ai-sorting` instead if you just need classification without severity scoring or routing logic.

## Step 1: Define your moderation policy

Ask the user:
1. **What content do you need to catch?** (hate speech, spam, NSFW, harassment, self-harm, illegal activity, PII)
2. **What are the severity levels?** (warning, remove, ban)
3. **What is the tolerance for false positives?** (over-moderating frustrates users)
4. **Is human review in the loop?** (auto-only vs. auto + human escalation)

## Step 2: Choose your approach

| Approach | When to use | Complexity |
|----------|------------|------------|
| Single-label + `dspy.Predict` | One violation type per item, simple routing | Low |
| Single-label + `dspy.ChainOfThought` | Need explanation for each decision, nuanced content | Medium |
| Multi-label + `dspy.ChainOfThought` | Content can violate multiple policies at once | Medium |
| Multi-label + confidence routing | Uncertain cases go to human review | High |
| Pattern blocks + LM assessment | Zero-tolerance patterns (PII) plus semantic analysis | High |

## Step 3: Build the moderator

Classification + severity scoring + routing decision:

```python
import dspy
from typing import Literal

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

VIOLATIONS = Literal[
    "safe", "spam", "hate_speech", "harassment",
    "violence", "nsfw", "self_harm", "illegal",
]

class ModerateContent(dspy.Signature):
    """Assess user-generated content against platform policies."""
    content: str = dspy.InputField(desc="user-generated content to moderate")
    platform_context: str = dspy.InputField(desc="where this content appears, e.g. 'product review'")
    violation_type: VIOLATIONS = dspy.OutputField()
    severity: Literal["none", "low", "medium", "high"] = dspy.OutputField()
    explanation: str = dspy.OutputField(desc="brief reason for the decision")

class ContentModerator(dspy.Module):
    def __init__(self):
        self.assess = dspy.ChainOfThought(ModerateContent)

    def forward(self, content, platform_context="social media post"):
        result = self.assess(content=content, platform_context=platform_context)

        # Route based on severity
        if result.severity == "high":
            decision = "remove"
        elif result.severity == "medium":
            decision = "human_review"
        elif result.severity == "low":
            decision = "warn"
        else:
            decision = "approve"

        return dspy.Prediction(
            violation_type=result.violation_type,
            severity=result.severity,
            decision=decision,
            explanation=result.explanation,
        )

# Usage
moderator = ContentModerator()
result = moderator(content="Great product, works exactly as described!")
print(result.decision)  # "approve"

result = moderator(content="This seller is a scammer, I'll find where they live")
print(result.decision)  # "remove"
print(result.violation_type)  # "harassment"
```

## Step 4: Multi-label moderation

Content can violate multiple policies at once (e.g., spam *and* contains PII):

```python
VIOLATION_TYPES = ["safe", "spam", "hate_speech", "harassment", "violence", "nsfw", "self_harm", "illegal"]

class MultiLabelModerate(dspy.Signature):
    """Flag all policy violations in user content. Content may have multiple violations."""
    content: str = dspy.InputField()
    platform_context: str = dspy.InputField()
    violations: list[str] = dspy.OutputField(desc=f"all that apply from: {VIOLATION_TYPES}")
    severity: Literal["none", "low", "medium", "high"] = dspy.OutputField(
        desc="overall severity based on the worst violation"
    )
    explanation: str = dspy.OutputField()

class MultiLabelModerator(dspy.Module):
    def __init__(self):
        self.assess = dspy.ChainOfThought(MultiLabelModerate)

    def forward(self, content, platform_context=""):
        return self.assess(content=content, platform_context=platform_context)

def multi_label_reward(args, pred):
    # Validate that returned violations are from the allowed set
    if all(v in VIOLATION_TYPES for v in pred.violations):
        return 1.0
    return 0.0

validated_moderator = dspy.Refine(
    module=MultiLabelModerator(),
    N=3,
    reward_fn=multi_label_reward,
    threshold=1.0,
)
```

## Step 5: Hard blocks with pattern matching

For zero-tolerance patterns, block instantly with pattern matching — no LM needed:

```python
import re

class StrictModerator(dspy.Module):
    def __init__(self):
        self.assess = dspy.ChainOfThought(ModerateContent)

    def forward(self, content, platform_context=""):
        # Pattern-based hard blocks (instant, no LM needed)
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", content):
            return dspy.Prediction(
                violation_type="illegal",
                severity="high",
                decision="remove",
                explanation="Content contains SSN pattern — auto-reject",
            )
        if re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            content,
        ):
            return dspy.Prediction(
                violation_type="illegal",
                severity="high",
                decision="remove",
                explanation="Content contains email addresses — redact before posting",
            )
        if re.search(r"\b\d{16}\b", content):
            return dspy.Prediction(
                violation_type="illegal",
                severity="high",
                decision="remove",
                explanation="Content contains potential credit card number — auto-reject",
            )

        # LM-based assessment for everything else
        return self.assess(content=content, platform_context=platform_context)
```

Pattern-based blocks are faster, cheaper, and more reliable than LM-based detection for well-defined patterns (SSNs, credit cards, emails). Use regex for structure, LMs for semantics.

## Step 6: Confidence-based routing

Route uncertain decisions to human reviewers instead of making bad calls:

```python
class ConfidentModerate(dspy.Signature):
    """Moderate content and rate your confidence in the assessment."""
    content: str = dspy.InputField()
    platform_context: str = dspy.InputField()
    violation_type: VIOLATIONS = dspy.OutputField()
    severity: Literal["none", "low", "medium", "high"] = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="0.0 to 1.0 — how sure are you about this assessment?")
    explanation: str = dspy.OutputField()

class ConfidentModerator(dspy.Module):
    def __init__(self, confidence_threshold=0.7):
        self.assess = dspy.ChainOfThought(ConfidentModerate)
        self.confidence_threshold = confidence_threshold

    def forward(self, content, platform_context=""):
        result = self.assess(content=content, platform_context=platform_context)

        # Clamp confidence to valid range
        confidence = max(0.0, min(1.0, result.confidence))

        # Route based on confidence + severity
        if confidence < self.confidence_threshold:
            decision = "human_review"  # uncertain — always escalate
        elif result.severity == "high":
            decision = "remove"
        elif result.severity == "medium":
            decision = "human_review"
        elif result.severity == "low":
            decision = "warn"
        else:
            decision = "approve"

        return dspy.Prediction(
            violation_type=result.violation_type,
            severity=result.severity,
            confidence=confidence,
            decision=decision,
            explanation=result.explanation,
        )
```

## Step 7: Metrics and optimization

### Define moderation metrics

```python
def moderation_metric(example, prediction, trace=None):
    """Weighted score: type matters more than severity."""
    type_correct = float(prediction.violation_type == example.violation_type)
    severity_correct = float(prediction.severity == example.severity)
    return 0.7 * type_correct + 0.3 * severity_correct
```

### Per-category metrics (more useful than overall accuracy)

```python
def make_category_metric(category):
    """Create a precision metric for a specific violation category."""
    def metric(example, prediction, trace=None):
        if example.violation_type == category:
            return float(prediction.violation_type == category)  # recall
        else:
            return float(prediction.violation_type != category)  # precision
    return metric

# Track each category separately
hate_speech_metric = make_category_metric("hate_speech")
spam_metric = make_category_metric("spam")
```

### Optimize the moderator

```python
trainset = [
    dspy.Example(
        content="Buy cheap watches at spam-site.com!!!",
        platform_context="product review",
        violation_type="spam",
        severity="medium",
    ).with_inputs("content", "platform_context"),
    dspy.Example(
        content="This product changed my life, highly recommend!",
        platform_context="product review",
        violation_type="safe",
        severity="none",
    ).with_inputs("content", "platform_context"),
    # 50-200 labeled examples for good optimization
]

optimizer = dspy.MIPROv2(metric=moderation_metric, auto="medium")
optimized = optimizer.compile(moderator, trainset=trainset)
```

## Step 8: Handle tricky cases

- **Sarcasm and satire** — "Oh sure, what a *great* product" is not hate speech. Context matters. The `platform_context` field helps here.
- **Quoting to criticize** — "The seller said 'you are an idiot'" is reporting harassment, not committing it. Include instructions in your signature to distinguish.
- **Code snippets** — Variable names or test strings might contain offensive words. If your platform has code, add a code-detection step before moderation.
- **Non-English content** — LMs handle major languages well but may miss nuance in less-common languages. Consider language-specific test sets.
- **Adversarial evasion** — Users will try to bypass moderation (leetspeak, Unicode tricks, word splitting). Test your moderator with `/ai-testing-safety`.

## Gotchas

- **Claude adds a `reasoning` field to signatures used with ChainOfThought.** Do not add your own `reasoning` output field — DSPy injects one automatically. Adding a second causes duplicate or conflicting reasoning outputs.
- **Use programmatic checks (not `dspy.Refine`) for hard PII blocks.** For zero-tolerance patterns like SSNs or credit card numbers, check with regex before calling the LM and return a structured rejection immediately. `dspy.Refine` is for output quality constraints that benefit from retrying the LM, not for instant pattern-based blocks.
- **Claude uses `Literal[list]` instead of `Literal[tuple(list)]` for dynamic categories.** If violation types come from a database or config, you must use `Literal[tuple(categories)]` — `Literal[list]` silently fails type validation.
- **LM confidence scores are not calibrated probabilities.** When Claude builds a confidence-based router, it treats the 0.0-1.0 confidence output as if 0.7 means 70% accurate. LM self-reported confidence is directionally useful but not calibrated — tune the threshold empirically on your dev set, not based on the number itself.
- **Over-moderating borderline content is worse than under-moderating.** Claude defaults to being cautious and tends to classify borderline content as violations. For moderation, false positives (removing safe content) hurt user engagement more than false negatives. Bias your metric toward precision over recall for low-severity categories.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **Classification patterns** for general sorting and categorization -- see `/ai-sorting`
- **Output guardrails** for moderating your own AI responses -- see `/ai-checking-outputs`
- **Adversarial testing** to stress-test your moderator -- see `/ai-testing-safety`
- **Production monitoring** to track moderation quality over time -- see `/ai-monitoring`
- **Signatures** for defining input/output contracts -- see `/dspy-signatures`
- **ChainOfThought** for the reasoning module used in moderation -- see `/dspy-chain-of-thought`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For complete worked examples, see [examples.md](examples.md)
- For API signatures and quick reference, see [reference.md](reference.md)
