---
name: ragas
description: Evaluate RAG pipelines with Ragas — measure faithfulness, answer relevancy, context precision/recall, and noise sensitivity using LLM-as-judge metrics; run automated test suite generation with TestsetGenerator; integrate with LangChain, LlamaIndex, and CI pipelines.
triggers:
  - "ragas"
  - "rag evaluation"
  - "evaluate rag pipeline"
  - "ragas metrics"
  - "faithfulness metric"
  - "answer relevancy"
  - "context precision"
  - "context recall"
  - "ragas testset"
  - "llm evaluation framework"
  - "rag benchmark"
  - "ragas score"
  - "automated rag testing"
do_not_use_for:
  - Agent evaluation — use deepeval or custom eval instead
  - LLM fine-tuning evaluation — use llamafactory instead
  - General LLM benchmarks (MMLU etc.) — use lm-evaluation-harness instead
see_also:
  - langgraph
  - litellm
  - dspy
---

# Ragas — RAG Pipeline Evaluation

**Source:** explodinggradients/ragas (Apache 2.0) — evaluation framework for RAG applications

## Core Metrics

| Metric | What it measures | Range |
|--------|-----------------|-------|
| `Faithfulness` | Does the answer contain only info from context? | 0–1 |
| `AnswerRelevancy` | How relevant is the answer to the question? | 0–1 |
| `ContextPrecision` | Are retrieved contexts ranked by relevance? | 0–1 |
| `ContextRecall` | Does context cover all facts in ground truth? | 0–1 |
| `AnswerCorrectness` | Factual + semantic similarity to ground truth | 0–1 |
| `AnswerSimilarity` | Semantic similarity to ground truth answer | 0–1 |
| `ContextEntityRecall` | Entities from ground truth present in context | 0–1 |
| `NoiseSensitivity` | How much noise in context affects answer | 0–1 |

## Install

```bash
pip install ragas
pip install ragas[all]   # all integrations
```

## Basic Evaluation

```python
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness,
)

# Prepare evaluation dataset
# Each sample: question + answer + contexts + ground_truth
data = {
    "question": [
        "What is the capital of France?",
        "Who invented the telephone?",
    ],
    "answer": [
        "The capital of France is Paris.",
        "Alexander Graham Bell invented the telephone in 1876.",
    ],
    "contexts": [
        ["Paris is the capital and most populous city of France."],
        ["Alexander Graham Bell was the inventor of the telephone.",
         "Bell made the first successful telephone call in 1876."],
    ],
    "ground_truth": [
        "Paris",
        "Alexander Graham Bell",
    ],
}

dataset = Dataset.from_dict(data)

# Evaluate — uses OpenAI by default; configure below for other LLMs
result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness,
    ],
)

print(result)
# {'faithfulness': 0.97, 'answer_relevancy': 0.95, ...}
df = result.to_pandas()
```

## Configure Evaluation LLM (Anthropic/Custom)

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings

# Use Claude as evaluator
evaluator_llm = LangchainLLMWrapper(
    ChatAnthropic(model="claude-sonnet-4-5", api_key="your-key")
)
evaluator_embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(model="text-embedding-3-small")
)

# Apply to metrics
faithfulness.llm = evaluator_llm
answer_relevancy.llm = evaluator_llm
answer_relevancy.embeddings = evaluator_embeddings

result = evaluate(dataset=dataset, metrics=[faithfulness, answer_relevancy])
```

## Testset Generation (Auto-create Q&A pairs)

```python
from ragas.testset import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader

# Load your documents
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()

# Configure generator
generator_llm = ChatAnthropic(model="claude-sonnet-4-5")
critic_llm = ChatAnthropic(model="claude-opus-4-5")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings,
)

# Generate test set with different question types
testset = generator.generate_with_langchain_docs(
    documents,
    test_size=20,
    distributions={
        simple: 0.5,       # straightforward factual questions
        reasoning: 0.25,   # questions requiring reasoning
        multi_context: 0.25,  # questions spanning multiple docs
    },
)

# Export to pandas
df = testset.to_pandas()
print(df[["question", "ground_truth", "contexts"]].head())
```

## Evaluate a LangChain RAG Pipeline

```python
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall

# Build RAG
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

rag_chain = RetrievalQA.from_chain_type(
    llm=ChatAnthropic(model="claude-sonnet-4-5"),
    retriever=retriever,
    return_source_documents=True,
)

# Run questions through RAG
questions = ["What is X?", "How does Y work?"]
ground_truths = ["X is ...", "Y works by ..."]

answers, contexts = [], []
for q in questions:
    result = rag_chain(q)
    answers.append(result["result"])
    contexts.append([doc.page_content for doc in result["source_documents"]])

# Evaluate
dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})

scores = evaluate(dataset=dataset, metrics=[faithfulness, answer_relevancy, context_recall])
print(scores)
```

## Single Sample Evaluation

```python
from ragas.metrics import faithfulness
from ragas import SingleTurnSample

sample = SingleTurnSample(
    user_input="What is photosynthesis?",
    response="Photosynthesis is the process by which plants convert sunlight into energy.",
    retrieved_contexts=[
        "Photosynthesis is a biological process used by plants, algae and cyanobacteria to convert light energy into chemical energy stored as glucose.",
        "The process uses carbon dioxide, water, and light to produce glucose and oxygen.",
    ],
)

scorer = faithfulness
score = await scorer.single_turn_ascore(sample)
print(f"Faithfulness: {score:.2f}")
```

## CI/CD Integration

```python
import pytest
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

FAITHFULNESS_THRESHOLD = 0.85
RELEVANCY_THRESHOLD = 0.80

def test_rag_quality():
    dataset = load_eval_dataset()  # your eval set
    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy],
    )

    assert result["faithfulness"] >= FAITHFULNESS_THRESHOLD, (
        f"Faithfulness {result['faithfulness']:.2f} below threshold {FAITHFULNESS_THRESHOLD}"
    )
    assert result["answer_relevancy"] >= RELEVANCY_THRESHOLD, (
        f"Relevancy {result['answer_relevancy']:.2f} below threshold {RELEVANCY_THRESHOLD}"
    )
```

## Anti-Fake-Pass Checks

- [ ] `contexts` must be `list[list[str]]` — outer list per question, inner list of retrieved chunks
- [ ] `context_recall` requires `ground_truth` — other metrics can run without it
- [ ] Default evaluator uses OpenAI — explicitly set `metric.llm` for non-OpenAI providers
- [ ] `evaluate()` makes LLM API calls per metric per sample — costs scale with dataset size
- [ ] `result["faithfulness"]` is the mean across all samples — check `result.to_pandas()` for per-sample
- [ ] `TestsetGenerator` requires `critic_llm` separate from `generator_llm` — both needed
- [ ] Scores of 1.0 on small datasets often indicate degenerate cases — test with ≥20 samples
