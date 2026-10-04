---
name: dspy-data
description: Prepare training and dev data for DSPy - loading from CSV/JSON/HuggingFace, creating dspy.Example objects, setting input keys, and building train/dev splits. Use when you need to prepare data for DSPy optimizers, load labeled examples, or convert dataset formats. Common scenarios - loading a CSV of labeled examples for optimization, converting HuggingFace datasets to DSPy format, creating train/dev/test splits, building Examples with proper input keys, converting JSON data for DSPy, or preparing evaluation datasets. Related - ai-generating-data, dspy-evaluate. Also used for dspy.Example, load training data for DSPy, CSV to DSPy examples, HuggingFace dataset in DSPy, prepare data for optimization, input_keys in DSPy, train dev split for DSPy, how to format data for DSPy optimizer, labeled examples format, create examples from JSON, what format does DSPy expect, dataset preparation for DSPy, with_inputs in DSPy Example, build evaluation dataset.
---

# Work with DSPy Data: Examples, Predictions, and Datasets

Guide the user through creating, loading, and managing data for DSPy programs. Data is the fuel for DSPy optimizers — getting it right is the difference between a program that works and one that doesn't.

## Step 1 — Gather context

Ask these before generating code (skip any you already know from context):

1. **Data source** — Where is the data coming from? CSV/JSON file, HuggingFace dataset, database query, or hand-crafted examples?
2. **Schema** — What fields does the data have, and which are inputs vs expected outputs? (This determines what goes in `with_inputs()`.)
3. **Scale** — How many examples are available? DSPy optimizers work well with 20–300 examples; very large datasets should be sampled down.
4. **Task type** — Classification with fixed categories, extraction, or open-ended generation? This affects how to map raw data fields to signature fields.

## What are Examples

`dspy.Example` is DSPy's data container. Think of it as a dictionary with one extra feature: you can mark which fields are **inputs** and which are **outputs**. This distinction is critical because optimizers need to know what to feed into your program (inputs) and what to compare against (outputs).

```python
import dspy

# An Example holds named fields — like a dict
example = dspy.Example(question="What is DSPy?", answer="A framework for programming LMs")

# Access fields with dot notation or bracket notation
print(example.question)       # "What is DSPy?"
print(example["answer"])      # "A framework for programming LMs"
```

Every DSPy optimizer, evaluator, and metric function expects data as a list of `dspy.Example` objects.

## Creating Examples

Create examples with keyword arguments. Every keyword becomes a field.

```python
# Simple question-answer pair
ex = dspy.Example(question="What color is the sky?", answer="Blue")

# Classification example with more fields
ex = dspy.Example(
    text="The product broke after one day",
    label="negative",
    category="quality",
)

# Fields can be any Python type
ex = dspy.Example(
    query="hiking trails near Portland",
    results=["Forest Park", "Eagle Creek"],
    count=2,
)
```

You can also create an Example from a dictionary:

```python
data = {"question": "What is Python?", "answer": "A programming language"}
ex = dspy.Example(**data)
```

## with_inputs() — marking input fields

`with_inputs()` tells DSPy which fields are inputs (what the program receives) and which are outputs (what the program should produce). **This is required for optimizers and evaluation.**

```python
# Mark "question" as input — "answer" becomes the expected output
ex = dspy.Example(question="What is DSPy?", answer="A framework").with_inputs("question")

# Multiple input fields
ex = dspy.Example(
    context="DSPy is a Python framework...",
    question="What is DSPy?",
    answer="A framework for programming LMs",
).with_inputs("context", "question")
```

### What happens without with_inputs()

If you skip `with_inputs()`, optimizers won't know which fields to pass to your program and which to hold back for scoring. You'll get errors or wrong results. Always call it.

### How it works

After `with_inputs("question")`:
- `example.inputs()` returns an `Example` with only `{"question": "What is DSPy?"}`
- `example.labels()` returns an `Example` with only `{"answer": "A framework"}`

DSPy uses `.inputs()` to feed data into your module and `.labels()` to check the output against expected values.

```python
ex = dspy.Example(question="What is DSPy?", answer="A framework").with_inputs("question")

print(ex.inputs())   # Example(question="What is DSPy?")
print(ex.labels())   # Example(answer="A framework")
```

## Prediction — what modules return

When you call a DSPy module, it returns a `dspy.Prediction`, which extends `Example`. A Prediction has the same dot-access and dict-like behavior.

```python
classify = dspy.ChainOfThought("text -> label")
result = classify(text="Great product!")

# result is a Prediction
print(result.label)       # "positive"
print(result.reasoning)   # chain-of-thought reasoning (added by ChainOfThought)

# Predictions work like Examples
print(result.keys())      # dict_keys(['reasoning', 'label'])
```

In metric functions, `prediction` is always a `Prediction` and `example` is always an `Example`:

```python
def metric(example, prediction, trace=None):
    # example has the gold fields you defined
    # prediction has the fields your module produced
    return prediction.label == example.label
```

## Building datasets

A dataset in DSPy is just a Python list of `Example` objects. Use list comprehensions to build them.

```python
# From parallel lists
questions = ["What is Python?", "What is DSPy?", "What is an LM?"]
answers = ["A programming language", "A framework for LMs", "A language model"]

trainset = [
    dspy.Example(question=q, answer=a).with_inputs("question")
    for q, a in zip(questions, answers)
]
```

```python
# From a list of dicts
raw_data = [
    {"text": "Love it!", "label": "positive"},
    {"text": "Terrible.", "label": "negative"},
    {"text": "It's okay.", "label": "neutral"},
]

trainset = [
    dspy.Example(**row).with_inputs("text")
    for row in raw_data
]
```

## Loading from CSV

```python
import csv

def load_csv_as_examples(filepath, input_fields):
    """Load a CSV file into a list of dspy.Example objects."""
    examples = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ex = dspy.Example(**row).with_inputs(*input_fields)
            examples.append(ex)
    return examples

# Usage
trainset = load_csv_as_examples("tickets.csv", input_fields=["message"])
```

With pandas (if you prefer):

```python
import pandas as pd

df = pd.read_csv("tickets.csv")
trainset = [
    dspy.Example(**row.to_dict()).with_inputs("message")
    for _, row in df.iterrows()
]
```

### Handling CSV quirks

```python
# Skip rows with missing values
trainset = [
    dspy.Example(**row).with_inputs("text")
    for row in csv.DictReader(open("data.csv"))
    if row["text"] and row["label"]  # skip blanks
]

# Rename columns to match your signature
trainset = [
    dspy.Example(
        text=row["customer_message"],
        label=row["assigned_category"],
    ).with_inputs("text")
    for row in csv.DictReader(open("data.csv"))
]
```

## Loading from JSON

```python
import json

def load_json_as_examples(filepath, input_fields):
    """Load a JSON array file into dspy.Example objects."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return [
        dspy.Example(**item).with_inputs(*input_fields)
        for item in data
    ]

# Usage — file contains [{"question": "...", "answer": "..."}, ...]
trainset = load_json_as_examples("qa_pairs.json", input_fields=["question"])
```

For JSON Lines (one JSON object per line):

```python
def load_jsonl_as_examples(filepath, input_fields):
    """Load a JSONL file into dspy.Example objects."""
    examples = []
    with open(filepath, "r") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                examples.append(dspy.Example(**item).with_inputs(*input_fields))
    return examples
```

## Loading from HuggingFace

The HuggingFace `datasets` library gives you access to thousands of ready-to-use datasets.

```bash
pip install datasets
```

```python
from datasets import load_dataset

# Load a dataset
dataset = load_dataset("hotpotqa/hotpot_qa", "fullwiki")

# Convert to DSPy Examples
trainset = [
    dspy.Example(
        question=x["question"],
        answer=x["answer"],
    ).with_inputs("question")
    for x in dataset["train"]
]
```

### Common HuggingFace patterns

```python
# Limit the number of examples (large datasets)
trainset = [
    dspy.Example(question=x["question"], answer=x["answer"]).with_inputs("question")
    for x in list(dataset["train"])[:500]
]

# Rename fields to match your signature
trainset = [
    dspy.Example(
        text=x["sentence"],
        label="positive" if x["label"] == 1 else "negative",
    ).with_inputs("text")
    for x in dataset["train"]
]

# Filter rows
trainset = [
    dspy.Example(question=x["question"], answer=x["answer"]).with_inputs("question")
    for x in dataset["train"]
    if len(x["answer"]) > 0  # skip empty answers
]
```

## Built-in datasets

DSPy ships with a few standard datasets for prototyping and benchmarking. These return pre-built `dspy.Example` objects — no HuggingFace dependency needed.

```python
from dspy.datasets import HotPotQA

# Multi-hop question answering
dataset = HotPotQA(train_seed=1, train_size=200, dev_size=50, test_size=0)
trainset = dataset.train
devset = dataset.dev
```

| Dataset | Import | Task |
|---------|--------|------|
| `HotPotQA` | `from dspy.datasets import HotPotQA` | Multi-hop QA over Wikipedia |
| `GSM8k` | `from dspy.datasets import GSM8k` | Grade-school math word problems |
| `Colors` | `from dspy.datasets import Colors` | Simple color identification |

Constructor parameters (all optional): `train_seed`, `train_size`, `dev_size`, `test_size`.

**Note:** You still need `.with_inputs()` if you're passing these to an optimizer:

```python
trainset = [ex.with_inputs("question") for ex in dataset.train]
```

## Train/dev splits

Optimizers train on `trainset` and you evaluate on `devset`. Keep them separate to measure real performance.

### Random split

```python
import random

def train_dev_split(examples, train_ratio=0.8, seed=42):
    """Split a list of examples into train and dev sets."""
    random.seed(seed)
    shuffled = list(examples)
    random.shuffle(shuffled)
    split_idx = int(len(shuffled) * train_ratio)
    return shuffled[:split_idx], shuffled[split_idx:]

# Usage
all_examples = load_csv_as_examples("data.csv", input_fields=["text"])
trainset, devset = train_dev_split(all_examples)
print(f"Train: {len(trainset)}, Dev: {len(devset)}")
```

### Stratified split (preserves label distribution)

Use this when your categories are imbalanced (e.g., 90% "general", 10% "urgent").

```python
from collections import defaultdict

def stratified_split(examples, label_field, train_ratio=0.8, seed=42):
    """Split examples while preserving the distribution of a label field."""
    random.seed(seed)
    buckets = defaultdict(list)
    for ex in examples:
        buckets[ex[label_field]].append(ex)

    trainset, devset = [], []
    for label, items in buckets.items():
        random.shuffle(items)
        split_idx = int(len(items) * train_ratio)
        trainset.extend(items[:split_idx])
        devset.extend(items[split_idx:])

    random.shuffle(trainset)
    random.shuffle(devset)
    return trainset, devset

# Usage
trainset, devset = stratified_split(all_examples, label_field="category")
```

### Using HuggingFace's built-in splits

Many HuggingFace datasets come pre-split:

```python
dataset = load_dataset("hotpotqa/hotpot_qa", "fullwiki")
trainset = [dspy.Example(**x).with_inputs("question") for x in dataset["train"].select(range(500))]
devset = [dspy.Example(**x).with_inputs("question") for x in dataset["validation"].select(range(200))]
```

## Common patterns

### Accessing fields

```python
ex = dspy.Example(question="What?", answer="That", source="wiki")

# Dot access
ex.question

# Dict-style access
ex["question"]

# Get all field names
ex.keys()  # dict_keys(['question', 'answer', 'source'])

# Check if a field exists
"question" in ex  # True
```

### Converting to/from dicts

```python
# Example to dict
d = dict(ex)  # {"question": "What?", "answer": "That", "source": "wiki"}

# Dict to Example
ex = dspy.Example(**d).with_inputs("question")
```

### Filtering examples

```python
# Keep only examples where the answer is short
short_answers = [ex for ex in trainset if len(ex.answer.split()) < 20]

# Keep only a specific category
urgent_only = [ex for ex in trainset if ex.category == "urgent"]

# Remove duplicates (by a field)
seen = set()
unique = []
for ex in trainset:
    if ex.question not in seen:
        seen.add(ex.question)
        unique.append(ex)
```

### Inspecting your dataset

```python
# Quick summary
print(f"Total examples: {len(trainset)}")
print(f"Fields: {trainset[0].keys()}")
print(f"First example: {trainset[0]}")

# Label distribution
from collections import Counter
labels = Counter(ex.label for ex in trainset)
print(f"Label distribution: {labels}")
```

### Verify your dataset before optimization

Run this before passing to an optimizer — catches missing `with_inputs()` and field name mismatches early:

```python
def verify_dataset(examples, expected_inputs):
    assert len(examples) >= 5, f"Too few examples: {len(examples)}"
    for ex in examples[:3]:
        assert ex.inputs().keys(), "Missing with_inputs() — optimizer will fail"
        for field in expected_inputs:
            assert field in ex.inputs(), f"Input field '{field}' missing — check with_inputs()"
    print(f"OK: {len(examples)} examples, fields={list(examples[0].keys())}")

verify_dataset(trainset, expected_inputs=["question"])  # adjust field names
```

## When not to use dspy.Example

You do not need `dspy.Example` for every situation:

- **One-off runs** — if you are calling a module once without optimizing, pass keyword arguments directly: `module(question="What is DSPy?")`. No need for Examples.
- **Prototyping without a dataset** — build and test your module before collecting data. Add Examples only once you reach the optimize-or-evaluate stage.
- **Already have a pandas DataFrame** — use `.iterrows()` only when you need DSPy format; often you can prototype with the DataFrame first.

Convert to `dspy.Example` when you need to run an optimizer (`compile()`) or a formal evaluator (`dspy.Evaluate`).

## Gotchas

- **Claude forgets `with_inputs()` on every Example.** Without it, optimizers cannot distinguish inputs from expected outputs. Every example passed to an optimizer or evaluator must have `with_inputs()` called. Claude often creates examples and only calls `with_inputs()` on the first one or skips it entirely when building lists inline.
- **Claude calls `with_inputs()` with output field names.** Mark only the fields your module receives as input — not the fields it should produce. If your signature is `question -> answer`, call `.with_inputs("question")`, not `.with_inputs("question", "answer")`. Including output fields means the optimizer has nothing to score against.
- **Claude uses `Literal[list]` instead of `Literal[tuple(list)]` for dynamic categories.** When building categories from data (`CATEGORIES = list(set(...))`), the type annotation must be `Literal[tuple(CATEGORIES)]`, not `Literal[CATEGORIES]`. The latter silently fails to constrain the output.
- **Claude passes raw dicts to optimizers instead of `dspy.Example` objects.** DSPy optimizers and evaluators require `dspy.Example` objects, not plain Python dicts. Always convert with `dspy.Example(**row).with_inputs(...)`.
- **Claude creates train/dev splits without shuffling first.** If data is sorted by label or date, taking the first 80% as train and last 20% as dev creates a biased split. Always shuffle with a fixed seed before splitting.

## Additional resources

- [dspy.Example API docs](https://dspy.ai/api/primitives/Example/)
- [dspy.Prediction API docs](https://dspy.ai/api/primitives/Prediction/)
- [reference.md](reference.md) — constructor signatures, method tables, Prediction details
- [examples.md](examples.md) — worked examples with CSV, HuggingFace, and manual data

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **`/dspy-signatures`** — define the input/output contract that determines which fields go in `with_inputs()`
- **`/dspy-evaluate`** — evaluate your program on a devset with metrics
- **`/ai-generating-data`** — generate synthetic training data when you have none
- **`/ai-improving-accuracy`** — use optimizers that consume your trainset to boost quality
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
