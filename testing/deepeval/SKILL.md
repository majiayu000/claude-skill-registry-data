---
name: deepeval
description: DeepEval — LLM evaluation framework, RAG metrics, hallucination detection, red-teaming, CI/CD integration
triggers:
  - deepeval
  - deepeval metrics
  - llm evaluation deepeval
  - hallucination detection deepeval
  - deepeval rag
  - deepeval red team
  - deepeval ci
  - deepeval test
  - llm unit test
  - deepeval dataset
do_not_use_for:
  - vector storage — use qdrant
  - tracing/observability — use langfuse
  - generic benchmarks — use ragas for RAG-specific
see_also:
  - ragas
  - langfuse
  - pydantic-ai
---

# DeepEval — LLM Evaluation

## Core: Test Cases + Metrics

```python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    HallucinationMetric,
    BiasMetric,
    ToxicityMetric,
)
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is RAG?",
    actual_output="RAG stands for Retrieval-Augmented Generation...",
    expected_output="Retrieval-Augmented Generation is a technique...",
    retrieval_context=[
        "RAG is an AI framework that retrieves relevant documents...",
        "The retrieval step fetches context from a knowledge base...",
    ],
)

metrics = [
    AnswerRelevancyMetric(threshold=0.7, model="gpt-4o"),
    FaithfulnessMetric(threshold=0.8, model="gpt-4o"),
    ContextualPrecisionMetric(threshold=0.7, model="gpt-4o"),
    ContextualRecallMetric(threshold=0.7, model="gpt-4o"),
]

evaluate([test_case], metrics)
```

## Pytest Integration

```python
# test_rag.py
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

@pytest.mark.parametrize("test_case", [
    LLMTestCase(
        input="What is the capital of France?",
        actual_output=rag_pipeline("What is the capital of France?"),
        retrieval_context=["France is a country in Europe. Its capital is Paris."],
    ),
])
def test_rag_pipeline(test_case):
    answer_relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-4o")
    faithfulness = FaithfulnessMetric(threshold=0.8, model="gpt-4o")
    assert_test(test_case, [answer_relevancy, faithfulness])

# Run: deepeval test run test_rag.py
```

## Custom Metric

```python
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class ResponseLengthMetric(BaseMetric):
    def __init__(self, max_tokens: int = 200, threshold: float = 1.0):
        self.max_tokens = max_tokens
        self.threshold = threshold
        self.name = "Response Length"

    def measure(self, test_case: LLMTestCase) -> float:
        tokens = len(test_case.actual_output.split())
        self.score = 1.0 if tokens <= self.max_tokens else 0.0
        self.reason = f"Response has {tokens} tokens (max {self.max_tokens})"
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.success
```

## Hallucination Detection

```python
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="Tell me about Einstein",
    actual_output="Einstein won the Nobel Prize in Physics in 1921 for the photoelectric effect.",
    context=[
        "Einstein received the Nobel Prize in Physics in 1921.",
        "The prize was awarded for his discovery of the photoelectric effect.",
    ],
)

metric = HallucinationMetric(threshold=0.5, model="gpt-4o")
metric.measure(test_case)
print(metric.score)         # 0.0 = no hallucination, 1.0 = full hallucination
print(metric.reason)
print(metric.is_successful())
```

## Datasets

```python
from deepeval.dataset import EvaluationDataset

# Create dataset from test cases
dataset = EvaluationDataset(
    test_cases=[test_case1, test_case2, test_case3],
    alias="rag-eval-v1",
)

# Push to Confident AI (deepeval cloud)
dataset.push(overwrite=True)

# Pull existing dataset
from deepeval.dataset import EvaluationDataset
dataset = EvaluationDataset()
dataset.pull(alias="rag-eval-v1")

# Evaluate entire dataset
evaluate(dataset, metrics=[AnswerRelevancyMetric(threshold=0.7)])
```

## Red Teaming

```python
from deepeval.red_teaming import RedTeamer, AttackEnhancer, Vulnerability

red_teamer = RedTeamer(
    target_purpose="Customer support chatbot for e-commerce",
    target_system_prompt="You are a helpful customer support agent...",
)

results = red_teamer.scan(
    target_model=my_model,
    attacks_per_vulnerability=5,
    vulnerabilities=[
        Vulnerability.PROMPT_INJECTION,
        Vulnerability.PII_LEAKAGE,
        Vulnerability.JAILBREAKING,
        Vulnerability.HARMFUL_CONTENT,
    ],
    attack_enhancements={
        AttackEnhancer.BASE64: 0.25,
        AttackEnhancer.ROT13: 0.25,
        AttackEnhancer.JAILBREAK: 0.5,
    },
)
print(red_teamer.vulnerability_scores_breakdown)
```

## Use Custom LLM Judge

```python
from deepeval.models import DeepEvalBaseLLM
import anthropic

class ClaudeJudge(DeepEvalBaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic()

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return "claude-sonnet-4-6"

judge = ClaudeJudge()
metric = AnswerRelevancyMetric(threshold=0.7, model=judge)
```

## Anti-Fake-Pass Checks

- Metrics require an LLM judge (`model=`) — costs API credits per evaluation
- `threshold` is minimum passing score — `measure()` returns float, `is_successful()` checks threshold
- `retrieval_context` for RAG metrics must be the actual retrieved chunks, not all docs
- `assert_test()` in pytest raises `AssertionError` on failure — fails the test
- Red teaming requires `OPENAI_API_KEY` or custom model — scans are expensive (N attacks × M vulns)
- `dataset.push()` requires Confident AI account — use local `evaluate()` without cloud
