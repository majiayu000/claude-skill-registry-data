---
name: dataset-engineering
description: Create, clean, and optimize datasets for LLM fine-tuning. Covers formats (Alpaca, ShareGPT, ChatML), synthetic data generation, quality assessment, and augmentation. Use when preparing data for training.
---

# Dataset Engineering

Complete guide for creating, cleaning, and optimizing datasets for LLM fine-tuning.

## Overview

Quality data >> model size. This skill covers:

- **Dataset formats** - Alpaca, ShareGPT, ChatML, custom
- **Data generation** - Synthetic data with Claude/GPT-4
- **Cleaning & filtering** - Remove noise, duplicates, low-quality
- **Augmentation** - Expand datasets effectively
- **Quality assessment** - Measure and improve data quality
- **Splitting strategies** - Train/val/test splits
- **HuggingFace integration** - Load, transform, upload datasets

## Quick Start

### Format Existing Data (Alpaca)

```python
# Convert your data to Alpaca format
data = [
    {
        "instruction": "What is the capital of France?",
        "input": "",
        "output": "The capital of France is Paris."
    },
    {
        "instruction": "Translate to Spanish",
        "input": "Hello, how are you?",
        "output": "Hola, ¿cómo estás?"
    }
]

import json
with open("dataset.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Load and Use with Unsloth

```python
from datasets import load_dataset
from unsloth import FastLanguageModel, standardize_sharegpt

# Load dataset
dataset = load_dataset("json", data_files="dataset.json", split="train")

# Format for training
def formatting_func(examples):
    texts = []
    for instruction, input_text, output in zip(
        examples["instruction"],
        examples["input"],
        examples["output"]
    ):
        text = f"### Instruction:\n{instruction}\n\n"
        if input_text:
            text += f"### Input:\n{input_text}\n\n"
        text += f"### Response:\n{output}"
        texts.append(text)
    return {"text": texts}

dataset = dataset.map(formatting_func, batched=True)
```

### Generate Synthetic Data

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-...")

def generate_training_examples(topic: str, num_examples: int = 10):
    """Generate synthetic training data using Claude"""

    prompt = f"""Generate {num_examples} high-quality question-answer pairs about {topic}.

Format each as JSON:
{{
  "instruction": "The question or task",
  "input": "",
  "output": "The detailed answer"
}}

Make answers informative, accurate, and varied in style."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    return parse_json_examples(response.content[0].text)

# Generate medical Q&A data
medical_data = generate_training_examples("medical diagnosis", num_examples=100)
```

## Dataset Formats

### 1. Alpaca Format

**Best for:** Instruction following, Q&A

```python
alpaca_format = {
    "instruction": "The task or question",
    "input": "Optional context or input",
    "output": "The desired response"
}

# Example
{
    "instruction": "Explain photosynthesis",
    "input": "",
    "output": "Photosynthesis is the process by which plants..."
}

# With input field
{
    "instruction": "Summarize the following text",
    "input": "Long text here...",
    "output": "Summary here..."
}
```

### 2. ShareGPT Format

**Best for:** Multi-turn conversations, chat models

```python
sharegpt_format = {
    "conversations": [
        {"from": "human", "value": "Hello!"},
        {"from": "gpt", "value": "Hi! How can I help?"},
        {"from": "human", "value": "What's 2+2?"},
        {"from": "gpt", "value": "2+2 equals 4."}
    ]
}

# Use with Unsloth
from unsloth import standardize_sharegpt

dataset = standardize_sharegpt(dataset)
```

### 3. ChatML Format

**Best for:** OpenAI-style chat, system prompts

```python
chatml_format = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"},
        {"role": "assistant", "content": "AI stands for Artificial Intelligence..."}
    ]
}

# Convert to training format
def chatml_to_text(example):
    text = ""
    for msg in example["messages"]:
        if msg["role"] == "system":
            text += f"<|system|>\n{msg['content']}\n"
        elif msg["role"] == "user":
            text += f"<|user|>\n{msg['content']}\n"
        elif msg["role"] == "assistant":
            text += f"<|assistant|>\n{msg['content']}\n"
    return {"text": text}
```

### 4. Custom Domain Format

**Best for:** Specialized tasks, domain-specific

```python
# Medical diagnosis format
medical_format = {
    "patient_symptoms": "Fever, cough, fatigue",
    "medical_history": "No prior conditions",
    "vital_signs": "Temp: 101°F, BP: 120/80",
    "diagnosis": "Likely viral infection",
    "treatment_plan": "Rest, fluids, monitor for 48 hours"
}

# Legal document format
legal_format = {
    "document_type": "Contract Review",
    "clauses": ["Clause 1...", "Clause 2..."],
    "issues_found": ["Issue 1", "Issue 2"],
    "recommendations": ["Recommendation 1", "Recommendation 2"]
}
```

## Synthetic Data Generation

### Generate with Claude

```python
import anthropic
import json

class SyntheticDataGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_qa_pairs(
        self,
        domain: str,
        num_examples: int,
        difficulty: str = "mixed"
    ):
        """Generate Q&A pairs for a specific domain"""

        prompt = f"""Generate {num_examples} diverse question-answer pairs about {domain}.

Requirements:
- Difficulty: {difficulty}
- Varied question types (what, how, why, compare, analyze)
- Detailed, accurate answers (100-300 words)
- Cover different aspects of {domain}

Output as JSON array:
[
  {{
    "instruction": "question here",
    "input": "",
    "output": "detailed answer here"
  }}
]"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def generate_conversations(
        self,
        scenario: str,
        num_conversations: int,
        turns_per_conversation: int = 4
    ):
        """Generate multi-turn conversations"""

        prompt = f"""Generate {num_conversations} realistic conversations for: {scenario}

Each conversation should have {turns_per_conversation} turns (back-and-forth).

Format as JSON:
[
  {{
    "conversations": [
      {{"from": "human", "value": "..."}},
      {{"from": "gpt", "value": "..."}},
      ...
    ]
  }}
]

Make conversations natural, varied, and realistic."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

# Usage
generator = SyntheticDataGenerator("sk-...")

# Generate 100 medical Q&A pairs
medical_data = generator.generate_qa_pairs(
    domain="medical diagnosis",
    num_examples=100,
    difficulty="mixed"
)

# Generate customer support conversations
support_data = generator.generate_conversations(
    scenario="technical support for a SaaS product",
    num_conversations=50,
    turns_per_conversation=6
)
```

### Generate with GPT-4

```python
import openai

def generate_with_gpt4(domain: str, num_examples: int):
    """Generate training data with GPT-4"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[{
            "role": "user",
            "content": f"""Generate {num_examples} training examples for {domain}.

Output as JSON array with instruction/input/output format."""
        }],
        temperature=0.8  # Higher for diversity
    )

    return json.loads(response.choices[0].message.content)
```

### Self-Instruct Method

Generate data from existing data:

```python
def self_instruct_augmentation(base_examples: list, multiplier: int = 3):
    """
    Generate variations of existing examples using Claude
    """
    augmented = []

    for example in base_examples:
        prompt = f"""Given this training example:
Instruction: {example['instruction']}
Output: {example['output']}

Generate {multiplier} similar but distinct examples that:
1. Cover the same concept
2. Use different wording
3. Vary in complexity
4. Include different examples

Output as JSON array."""

        # Call Claude to generate variations
        variations = call_claude(prompt)
        augmented.extend(variations)

    return augmented
```

## Data Cleaning & Filtering

### Remove Low-Quality Examples

```python
def filter_quality(dataset):
    """Filter out low-quality examples"""

    def is_high_quality(example):
        instruction = example["instruction"]
        output = example["output"]

        # Too short
        if len(output) < 20:
            return False

        # Too long (likely copy-paste dumps)
        if len(output) > 2000:
            return False

        # No instruction
        if not instruction or len(instruction) < 5:
            return False

        # Output is just "I don't know" or similar
        low_quality_responses = [
            "i don't know",
            "not sure",
            "no idea",
            "cannot answer"
        ]
        if output.lower().strip() in low_quality_responses:
            return False

        # Instruction and output are identical (copy-paste error)
        if instruction.strip() == output.strip():
            return False

        return True

    return dataset.filter(is_high_quality)
```

### Remove Duplicates

```python
from collections import defaultdict

def remove_duplicates(dataset):
    """Remove duplicate or near-duplicate examples"""

    seen = set()
    unique_examples = []

    for example in dataset:
        # Create hash of instruction + output
        content = f"{example['instruction']}|||{example['output']}"
        content_hash = hash(content)

        if content_hash not in seen:
            seen.add(content_hash)
            unique_examples.append(example)

    print(f"Removed {len(dataset) - len(unique_examples)} duplicates")
    return unique_examples

# Near-duplicate detection (fuzzy matching)
from difflib import SequenceMatcher

def remove_near_duplicates(dataset, similarity_threshold=0.9):
    """Remove examples that are too similar"""

    unique = []

    for example in dataset:
        is_duplicate = False

        for unique_example in unique:
            # Compare instruction similarity
            similarity = SequenceMatcher(
                None,
                example["instruction"],
                unique_example["instruction"]
            ).ratio()

            if similarity > similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique.append(example)

    print(f"Removed {len(dataset) - len(unique)} near-duplicates")
    return unique
```

### Filter by Language

```python
from langdetect import detect

def filter_by_language(dataset, target_language="en"):
    """Keep only examples in target language"""

    def is_target_language(example):
        try:
            # Check both instruction and output
            inst_lang = detect(example["instruction"])
            out_lang = detect(example["output"])
            return inst_lang == target_language and out_lang == target_language
        except:
            return False  # If detection fails, exclude

    return dataset.filter(is_target_language)
```

### Remove PII (Personal Information)

```python
import re

def remove_pii(text: str) -> str:
    """Remove personally identifiable information"""

    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

    # Phone numbers (US format)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)

    # Social Security Numbers
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)

    # Credit card numbers
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', text)

    return text

def sanitize_dataset(dataset):
    """Remove PII from entire dataset"""

    def sanitize_example(example):
        return {
            "instruction": remove_pii(example["instruction"]),
            "input": remove_pii(example.get("input", "")),
            "output": remove_pii(example["output"])
        }

    return dataset.map(sanitize_example)
```

## Data Augmentation

### Paraphrase Augmentation

```python
def paraphrase_augmentation(dataset, augmentation_factor=2):
    """Generate paraphrased versions of examples"""

    augmented = []

    for example in dataset:
        # Keep original
        augmented.append(example)

        # Generate paraphrases
        for i in range(augmentation_factor - 1):
            paraphrased = generate_paraphrase(example)
            augmented.append(paraphrased)

    return augmented

def generate_paraphrase(example):
    """Use Claude to paraphrase an example"""

    prompt = f"""Paraphrase this training example while keeping the same meaning:

Instruction: {example['instruction']}
Output: {example['output']}

Provide a paraphrased version with:
- Different wording
- Same core meaning
- Natural language

Output as JSON with instruction and output fields."""

    # Call Claude
    response = call_claude(prompt)
    return json.loads(response)
```

### Back-Translation

```python
from googletrans import Translator

def back_translation_augmentation(text: str, intermediate_lang='es'):
    """Augment via back-translation (English -> Spanish -> English)"""

    translator = Translator()

    # Translate to intermediate language
    intermediate = translator.translate(text, dest=intermediate_lang).text

    # Translate back to English
    back_translated = translator.translate(intermediate, dest='en').text

    return back_translated

# Apply to dataset
def augment_via_back_translation(dataset):
    augmented = []

    for example in dataset:
        # Original
        augmented.append(example)

        # Back-translated version
        augmented.append({
            "instruction": back_translation_augmentation(example["instruction"]),
            "input": example.get("input", ""),
            "output": back_translation_augmentation(example["output"])
        })

    return augmented
```

### Difficulty Variation

```python
def vary_difficulty(example, target_difficulty: str):
    """Generate easier or harder versions of an example"""

    prompt = f"""Given this example:
Instruction: {example['instruction']}
Output: {example['output']}

Create a {target_difficulty} version:
- Easier: Simplify concepts, use basic language, shorter
- Harder: Add complexity, technical terms, deeper analysis

Output as JSON."""

    response = call_claude(prompt)
    return json.loads(response)

# Generate difficulty variations
def create_difficulty_variants(dataset):
    augmented = []

    for example in dataset:
        # Original (medium)
        augmented.append(example)

        # Easier version
        augmented.append(vary_difficulty(example, "easier"))

        # Harder version
        augmented.append(vary_difficulty(example, "harder"))

    return augmented
```

## Quality Assessment

### Automated Quality Scoring

```python
class QualityScorer:
    def __init__(self):
        self.criteria = {
            "length": (50, 500),  # Ideal output length
            "instruction_length": (10, 200),
            "readability": 60,  # Flesch reading ease
            "coherence": 0.7,  # Sentence similarity
        }

    def score_example(self, example):
        """Score an example on multiple criteria"""

        scores = {}

        # Length score
        output_len = len(example["output"])
        min_len, max_len = self.criteria["length"]
        if min_len <= output_len <= max_len:
            scores["length"] = 1.0
        else:
            scores["length"] = max(0, 1 - abs(output_len - (min_len + max_len) / 2) / max_len)

        # Instruction quality
        inst_len = len(example["instruction"])
        inst_min, inst_max = self.criteria["instruction_length"]
        scores["instruction"] = 1.0 if inst_min <= inst_len <= inst_max else 0.5

        # Has actual content (not just generic responses)
        generic_responses = ["i don't know", "not sure", "maybe"]
        if any(gr in example["output"].lower() for gr in generic_responses):
            scores["content"] = 0.3
        else:
            scores["content"] = 1.0

        # Overall score
        overall = sum(scores.values()) / len(scores)
        return overall, scores

    def filter_by_quality(self, dataset, min_score=0.7):
        """Keep only high-quality examples"""

        filtered = []
        for example in dataset:
            score, _ = self.score_example(example)
            if score >= min_score:
                filtered.append(example)

        print(f"Kept {len(filtered)}/{len(dataset)} examples (score >= {min_score})")
        return filtered

# Usage
scorer = QualityScorer()
high_quality_data = scorer.filter_by_quality(dataset, min_score=0.75)
```

### Human-in-the-Loop Validation

```python
def create_validation_interface(dataset, sample_size=100):
    """Sample dataset for human review"""

    import random
    sample = random.sample(dataset, min(sample_size, len(dataset)))

    print("Review these examples. Rate 1-5:")
    print("1 = Poor, 2 = Below Average, 3 = Average, 4 = Good, 5 = Excellent\n")

    ratings = []
    for i, example in enumerate(sample):
        print(f"\n--- Example {i+1}/{len(sample)} ---")
        print(f"Instruction: {example['instruction']}")
        print(f"Output: {example['output'][:200]}...")

        rating = int(input("Rating (1-5): "))
        ratings.append(rating)

    avg_rating = sum(ratings) / len(ratings)
    print(f"\nAverage rating: {avg_rating:.2f}")

    # Identify issues
    low_rated = [sample[i] for i, r in enumerate(ratings) if r <= 2]
    print(f"Low-rated examples: {len(low_rated)}")

    return avg_rating, low_rated
```

## Train/Val/Test Splits

### Basic Split

```python
from datasets import Dataset

def split_dataset(data, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """Split dataset into train/val/test"""

    assert train_ratio + val_ratio + test_ratio == 1.0

    total = len(data)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)

    # Shuffle
    import random
    random.shuffle(data)

    # Split
    train_data = data[:train_size]
    val_data = data[train_size:train_size + val_size]
    test_data = data[train_size + val_size:]

    return {
        "train": Dataset.from_list(train_data),
        "validation": Dataset.from_list(val_data),
        "test": Dataset.from_list(test_data)
    }
```

### Stratified Split

For imbalanced datasets:

```python
from sklearn.model_selection import train_test_split

def stratified_split(data, category_field="category"):
    """Split while preserving category distribution"""

    # Extract categories
    categories = [example[category_field] for example in data]

    # Stratified split
    train_data, temp_data, train_cats, temp_cats = train_test_split(
        data, categories,
        test_size=0.2,
        stratify=categories,
        random_state=42
    )

    val_data, test_data = train_test_split(
        temp_data,
        test_size=0.5,
        stratify=temp_cats,
        random_state=42
    )

    return {
        "train": train_data,
        "validation": val_data,
        "test": test_data
    }
```

### Time-Based Split

For temporal data:

```python
def time_based_split(data, timestamp_field="timestamp"):
    """Split based on timestamp to avoid data leakage"""

    # Sort by timestamp
    sorted_data = sorted(data, key=lambda x: x[timestamp_field])

    # Use oldest 80% for train, next 10% for val, newest 10% for test
    total = len(sorted_data)
    train_end = int(total * 0.8)
    val_end = int(total * 0.9)

    return {
        "train": sorted_data[:train_end],
        "validation": sorted_data[train_end:val_end],
        "test": sorted_data[val_end:]
    }
```

## Domain-Specific Datasets

### Medical Dataset

```python
def create_medical_dataset():
    """Create medical diagnosis dataset"""

    generator = SyntheticDataGenerator("sk-...")

    # Generate different types
    datasets = []

    # Symptom analysis
    datasets.extend(generator.generate_qa_pairs(
        domain="symptom analysis and differential diagnosis",
        num_examples=200
    ))

    # Treatment planning
    datasets.extend(generator.generate_qa_pairs(
        domain="medical treatment planning",
        num_examples=150
    ))

    # Drug interactions
    datasets.extend(generator.generate_qa_pairs(
        domain="drug interactions and contraindications",
        num_examples=100
    ))

    return datasets
```

### Legal Dataset

```python
def create_legal_dataset():
    """Create legal document analysis dataset"""

    # Contract review
    contract_data = generate_contract_examples(num=150)

    # Case law analysis
    case_law_data = generate_case_law_examples(num=100)

    # Legal research
    research_data = generate_legal_research_examples(num=100)

    return contract_data + case_law_data + research_data
```

### Code Dataset

```python
def create_code_dataset(languages=["python", "javascript", "java"]):
    """Create coding dataset"""

    dataset = []

    for lang in languages:
        # Code explanation
        dataset.extend(generate_code_explanation(lang, num=100))

        # Bug fixing
        dataset.extend(generate_bug_fixing(lang, num=50))

        # Code generation
        dataset.extend(generate_code_tasks(lang, num=100))

    return dataset
```

## HuggingFace Integration

### Load from Hub

```python
from datasets import load_dataset

# Load existing dataset
dataset = load_dataset("tatsu-lab/alpaca", split="train")

# Load from local
dataset = load_dataset("json", data_files="my_data.json")

# Load with streaming (for large datasets)
dataset = load_dataset("large_dataset", streaming=True)
```

### Transform Dataset

```python
# Map function to transform
def transform_to_alpaca(example):
    """Transform any format to Alpaca"""
    return {
        "instruction": example["question"],
        "input": "",
        "output": example["answer"]
    }

dataset = dataset.map(transform_to_alpaca)

# Filter
dataset = dataset.filter(lambda x: len(x["output"]) > 50)

# Shuffle
dataset = dataset.shuffle(seed=42)

# Select subset
dataset = dataset.select(range(1000))
```

### Upload to Hub

```python
from datasets import Dataset

# Create dataset
data = [...]
dataset = Dataset.from_list(data)

# Push to Hub
dataset.push_to_hub(
    "username/my-dataset",
    private=False,
    token="hf_..."
)

# With splits
from datasets import DatasetDict

splits = split_dataset(data)
dataset_dict = DatasetDict(splits)

dataset_dict.push_to_hub("username/my-dataset", token="hf_...")
```

## Best Practices

### 1. Start with Quality over Quantity

```python
# 1000 high-quality examples > 10,000 low-quality
# Focus on:
# - Clear instructions
# - Accurate outputs
# - Diverse examples
# - Proper formatting
```

### 2. Validate Everything

```python
# Before training, validate:
# - Format correctness
# - No duplicates
# - No PII
# - Quality score > threshold
# - Category balance
```

### 3. Version Your Datasets

```
datasets/
├── medical-v1.0.0.json       # Initial
├── medical-v1.1.0.json       # Added 500 examples
├── medical-v2.0.0.json       # Complete regeneration
└── README.md                 # Dataset card
```

### 4. Document Your Data

Create a dataset card (README.md):

```markdown
# Medical Q&A Dataset v1.0.0

## Overview

- Size: 1,000 examples
- Format: Alpaca
- Domain: Medical diagnosis
- License: MIT

## Data Sources

- Synthetic generation with Claude 3.5 Sonnet
- Expert validation by 3 MDs
- Quality threshold: 0.85+

## Statistics

- Avg instruction length: 25 words
- Avg output length: 150 words
- Categories: Diagnosis (40%), Treatment (30%), Prevention (30%)

## Example

...
```

### 5. Test Before Training

```python
# Always test a sample before full training
sample = dataset.select(range(100))

# Quick train to verify:
# - Format is correct
# - Model can learn
# - No obvious issues
```

## Troubleshooting

### Issue: Model Not Learning

**Check:**

```python
# 1. Is the format correct?
print(dataset[0])

# 2. Is the output length reasonable?
print(f"Avg length: {np.mean([len(x['output']) for x in dataset])}")

# 3. Are there duplicates?
unique_count = len(set(x['output'] for x in dataset))
print(f"Unique: {unique_count}/{len(dataset)}")

# 4. Is the data diverse?
# Check category distribution
```

### Issue: Poor Quality Outputs

**Solutions:**

```python
# 1. Increase quality threshold
dataset = filter_quality(dataset, min_score=0.85)

# 2. Add more examples
# More data often helps

# 3. Improve prompt engineering
# Better prompts -> better synthetic data

# 4. Human validation
# Review and fix low-quality examples
```

### Issue: Imbalanced Dataset

**Solutions:**

```python
# 1. Oversample minority class
from imblearn.over_sampling import RandomOverSampler

# 2. Undersample majority class
# 3. Generate more minority examples
# 4. Use weighted loss during training
```

## Summary

Dataset engineering workflow:

1. ✓ Define format (Alpaca/ShareGPT/custom)
2. ✓ Generate or collect data
3. ✓ Clean and filter (remove low-quality, duplicates, PII)
4. ✓ Augment if needed (paraphrase, back-translate)
5. ✓ Assess quality (automated + human)
6. ✓ Split (train/val/test)
7. ✓ Upload to HuggingFace
8. ✓ Document (dataset card)
9. ✓ Version control

Remember: Quality > Quantity. 1000 great examples beats 10,000 mediocre ones.
