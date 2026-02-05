---
name: unsloth-tokenizer
description: Analyze, compare, and work with tokenizers using Unsloth tools. Compare different tokenizers, analyze token efficiency, and integrate with Unsloth models. For SuperBPE training, see the 'superbpe' skill.
---

# Unsloth Tokenizer Tools

Expert guidance for tokenizer comparison, analysis, and integration using Unsloth's tokenizer utilities.

## Overview

Unsloth provides powerful tools for:

- **Comparing tokenizers** - Measure token efficiency across different tokenizers
- **Analyzing tokenization** - Understand how text is tokenized
- **Integration** - Use tokenizers with Unsloth models
- **Optimization** - Find the most efficient tokenizer for your use case

> **Note**: For SuperBPE tokenizer training, see the dedicated `superbpe` skill.

## Quick Start

### Compare Two Tokenizers

```python
from unsloth.tokenizer import compare_tokenizers

results = compare_tokenizers(
    text="The quick brown fox jumps over the lazy dog",
    tokenizer1="meta-llama/Llama-3.2-1B",
    tokenizer2="gpt2"
)

print(f"Llama-3.2: {results['tokenizer1']['tokens']} tokens")
print(f"GPT-2: {results['tokenizer2']['tokens']} tokens")
print(f"Difference: {results['reduction']}")
```

### Analyze Tokenization

```python
from unsloth.tokenizer import analyze_tokenization

analysis = analyze_tokenization(
    text="Your text here...",
    tokenizer="meta-llama/Llama-3.2-1B"
)

print(f"Total tokens: {analysis['total_tokens']}")
print(f"Unique tokens: {analysis['unique_tokens']}")
print(f"Token breakdown: {analysis['tokens']}")
```

### Batch Compare Multiple Tokenizers

```python
from unsloth.tokenizer import compare_multiple_tokenizers

tokenizers = [
    "meta-llama/Llama-3.2-1B",
    "meta-llama/Llama-3.2-3B",
    "mistralai/Mistral-7B-v0.1",
    "gpt2",
    "./tokenizers/custom_superbpe.json"
]

results = compare_multiple_tokenizers(
    text="Your text...",
    tokenizers=tokenizers
)

# Results sorted by efficiency
for result in results:
    print(f"{result['name']}: {result['tokens']} tokens")
```

## Use Cases

### 1. Find Most Efficient Tokenizer

**Problem:** Need to choose the best tokenizer for your use case

**Solution:**

```python
# Test multiple candidates
candidates = [
    "meta-llama/Llama-3.2-1B",
    "mistralai/Mistral-7B-v0.1",
    "google/gemma-2b",
    "./tokenizers/custom_superbpe.json"
]

# Use representative sample
sample_text = get_production_sample(size_kb=100)

results = compare_multiple_tokenizers(
    text=sample_text,
    tokenizers=candidates
)

# Choose most efficient
best = min(results, key=lambda x: x['tokens'])
print(f"Best tokenizer: {best['name']} with {best['tokens']} tokens")
```

### 2. Analyze Domain-Specific Tokenization

**Problem:** Understand how your domain-specific text is tokenized

**Solution:**

```python
# Medical text example
medical_text = """
Patient presents with acute myocardial infarction.
ECG shows ST-segment elevation. Troponin elevated.
"""

analysis = analyze_tokenization(
    text=medical_text,
    tokenizer="meta-llama/Llama-3.2-1B",
    show_breakdown=True
)

# Check how medical terms are tokenized
for term in ["myocardial", "infarction", "troponin"]:
    tokens = analysis['term_breakdown'][term]
    print(f"{term} → {tokens} (fragmented)" if len(tokens) > 1 else f"{term} → 1 token (good)")
```

### 3. Estimate API Costs

**Problem:** Predict API costs before making calls

**Solution:**

```python
from unsloth.tokenizer import estimate_tokens

# Your prompt
prompt = """
Your long prompt here...
"""

# Estimate for different APIs
estimates = {
    "OpenAI GPT-4": estimate_tokens(prompt, "gpt2") * 0.00003,  # $30 per 1M
    "Anthropic Claude": estimate_tokens(prompt, "gpt2") * 0.000015,  # $15 per 1M
    "Llama-3.2": estimate_tokens(prompt, "meta-llama/Llama-3.2-1B") * 0.000001  # Self-hosted
}

for api, cost in estimates.items():
    print(f"{api}: ~${cost:.4f}")
```

### 4. Validate Custom Tokenizer

**Problem:** After training a custom tokenizer, validate it's better

**Solution:**

```python
# Compare your custom tokenizer with baseline
test_corpus = load_test_corpus()

baseline_tokens = 0
custom_tokens = 0

for sample in test_corpus:
    result = compare_tokenizers(
        text=sample,
        tokenizer1="meta-llama/Llama-3.2-1B",  # Baseline
        tokenizer2="./tokenizers/my_custom.json"  # Your tokenizer
    )
    baseline_tokens += result['tokenizer1']['tokens']
    custom_tokens += result['tokenizer2']['tokens']

reduction = ((baseline_tokens - custom_tokens) / baseline_tokens) * 100
print(f"Average reduction: {reduction:.1f}%")
print(f"Pass" if reduction >= 20 else f"Fail - needs optimization")
```

## Integration with Unsloth Models

### Load Model with Custom Tokenizer

```python
from unsloth import FastLanguageModel
from transformers import AutoTokenizer

# Load Unsloth model
model, default_tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True
)

# Replace with custom tokenizer
custom_tokenizer = AutoTokenizer.from_pretrained("./tokenizers/custom.json")
model.resize_token_embeddings(len(custom_tokenizer))

# Use custom tokenizer for inference
inputs = custom_tokenizer("Your prompt", return_tensors="pt")
outputs = model.generate(**inputs)
response = custom_tokenizer.decode(outputs[0])
```

### Fine-Tune with Custom Tokenizer

```python
from unsloth import FastLanguageModel
from transformers import AutoTokenizer

# Load model
model, _ = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.2-1B-bnb-4bit",
    max_seq_length=2048
)

# Load custom tokenizer
custom_tokenizer = AutoTokenizer.from_pretrained("./tokenizers/custom.json")

# Resize embeddings
model.resize_token_embeddings(len(custom_tokenizer))

# Prepare LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth"
)

# Tokenize dataset with custom tokenizer
def tokenize_function(examples):
    return custom_tokenizer(
        examples["text"],
        truncation=True,
        max_length=2048
    )

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Train with custom tokenizer
trainer = SFTTrainer(
    model=model,
    tokenizer=custom_tokenizer,
    train_dataset=tokenized_dataset,
    # ... other trainer args
)
trainer.train()
```

## Tokenizer Comparison Strategies

### Strategy 1: Quick Single-Sample Test

Fast check for one piece of text:

```python
result = compare_tokenizers(
    text="Your sample text",
    tokenizer1="baseline",
    tokenizer2="candidate"
)

if float(result['reduction'].strip('%')) > 10:
    print("Candidate is more efficient")
```

### Strategy 2: Comprehensive Corpus Analysis

Thorough evaluation across many samples:

```python
from unsloth.tokenizer import compare_on_corpus

results = compare_on_corpus(
    corpus_path="test_corpus.txt",
    tokenizer1="meta-llama/Llama-3.2-1B",
    tokenizer2="./tokenizers/custom.json",
    num_samples=1000
)

print(f"Mean reduction: {results['mean_reduction']:.1f}%")
print(f"Median reduction: {results['median_reduction']:.1f}%")
print(f"Min: {results['min_reduction']:.1f}%, Max: {results['max_reduction']:.1f}%")
```

### Strategy 3: Domain-Specific Benchmark

Test on specific domains:

```python
domains = {
    "medical": "./corpus/medical_test.txt",
    "legal": "./corpus/legal_test.txt",
    "technical": "./corpus/technical_test.txt"
}

for domain_name, corpus_path in domains.items():
    results = compare_on_corpus(
        corpus_path=corpus_path,
        tokenizer1="baseline",
        tokenizer2="custom"
    )
    print(f"{domain_name}: {results['mean_reduction']:.1f}% reduction")
```

## Analyzing Tokenizer Efficiency

### Token-to-Character Ratio

Measure how efficiently a tokenizer encodes text:

```python
def calculate_efficiency(text: str, tokenizer_name: str):
    """
    Calculate token-to-character ratio
    Lower is better (fewer tokens per character)
    """
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tokens = tokenizer.encode(text)

    ratio = len(tokens) / len(text)
    chars_per_token = len(text) / len(tokens)

    return {
        'tokens': len(tokens),
        'characters': len(text),
        'ratio': ratio,
        'chars_per_token': chars_per_token
    }

# Compare multiple tokenizers
tokenizers = ["meta-llama/Llama-3.2-1B", "gpt2", "./custom.json"]

for tok in tokenizers:
    eff = calculate_efficiency(sample_text, tok)
    print(f"{tok}: {eff['chars_per_token']:.2f} chars/token")
```

### Vocabulary Coverage

Check how well a tokenizer covers your domain:

```python
def check_vocabulary_coverage(
    corpus_path: str,
    tokenizer_name: str,
    min_frequency: int = 10
):
    """
    Check what percentage of frequent terms are single tokens
    """
    from transformers import AutoTokenizer
    from collections import Counter

    # Load corpus
    with open(corpus_path, 'r') as f:
        text = f.read()

    # Find frequent terms
    words = text.lower().split()
    frequent_terms = [word for word, count in Counter(words).most_common(1000)
                      if count >= min_frequency]

    # Check tokenization
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    single_token_count = 0
    for term in frequent_terms:
        tokens = tokenizer.tokenize(term)
        if len(tokens) == 1:
            single_token_count += 1

    coverage = (single_token_count / len(frequent_terms)) * 100

    return {
        'total_frequent_terms': len(frequent_terms),
        'single_token_terms': single_token_count,
        'coverage_percent': coverage
    }

coverage = check_vocabulary_coverage(
    corpus_path="domain_corpus.txt",
    tokenizer_name="meta-llama/Llama-3.2-1B"
)

print(f"Vocabulary coverage: {coverage['coverage_percent']:.1f}%")
# Target: >60% for domain-specific, >40% for general
```

## Common Patterns

### Pattern 1: Tokenizer Selection for New Project

```python
# 1. Gather representative samples
samples = collect_representative_samples(count=100)

# 2. Define candidate tokenizers
candidates = [
    "meta-llama/Llama-3.2-1B",
    "meta-llama/Llama-3.2-3B",
    "mistralai/Mistral-7B-v0.1",
    "google/gemma-2b"
]

# 3. Benchmark all candidates
results = {}
for candidate in candidates:
    total_tokens = 0
    for sample in samples:
        analysis = analyze_tokenization(sample, candidate)
        total_tokens += analysis['total_tokens']
    results[candidate] = total_tokens

# 4. Select best
best_tokenizer = min(results, key=results.get)
print(f"Selected: {best_tokenizer}")

# 5. Consider training custom SuperBPE if needed
# See 'superbpe' skill for training
```

### Pattern 2: Cost Estimation Before Deployment

```python
def estimate_monthly_costs(
    expected_prompts_per_month: int,
    avg_prompt_length_chars: int,
    tokenizer_name: str,
    cost_per_million_tokens: float
):
    """
    Estimate monthly API costs given tokenizer choice
    """
    # Estimate tokens per prompt
    sample_text = "a" * avg_prompt_length_chars  # Dummy text
    analysis = analyze_tokenization(sample_text, tokenizer_name)
    tokens_per_prompt = analysis['total_tokens']

    # Calculate costs
    total_tokens = expected_prompts_per_month * tokens_per_prompt
    monthly_cost = (total_tokens / 1_000_000) * cost_per_million_tokens

    return {
        'prompts_per_month': expected_prompts_per_month,
        'tokens_per_prompt': tokens_per_prompt,
        'total_monthly_tokens': total_tokens,
        'monthly_cost': monthly_cost,
        'yearly_cost': monthly_cost * 12
    }

# Example
costs = estimate_monthly_costs(
    expected_prompts_per_month=1_000_000,
    avg_prompt_length_chars=500,
    tokenizer_name="meta-llama/Llama-3.2-1B",
    cost_per_million_tokens=20
)

print(f"Monthly cost: ${costs['monthly_cost']:,.2f}")
print(f"Yearly cost: ${costs['yearly_cost']:,.2f}")
```

### Pattern 3: Multi-Tokenizer Workflow

```python
# Route to different tokenizers based on content type
def get_optimal_tokenizer(text: str) -> str:
    """
    Select best tokenizer based on text characteristics
    """
    # Check content type
    if has_medical_terms(text):
        return "./tokenizers/medical_superbpe.json"
    elif has_code(text):
        return "./tokenizers/code_superbpe.json"
    elif is_multilingual(text):
        return "meta-llama/Llama-3.2-3B"  # Better multilingual support
    else:
        return "meta-llama/Llama-3.2-1B"  # General purpose

# Use in production
optimal_tokenizer = get_optimal_tokenizer(user_input)
tokens = tokenize_with(user_input, optimal_tokenizer)
```

## Troubleshooting

### Issue: compare_tokenizers Returns Unexpected Results

**Solution:**

```python
# Ensure tokenizers are loaded correctly
from transformers import AutoTokenizer

# Test manually
tok1 = AutoTokenizer.from_pretrained("tokenizer1")
tok2 = AutoTokenizer.from_pretrained("tokenizer2")

text = "test text"
print(f"Tok1: {len(tok1.encode(text))} tokens")
print(f"Tok2: {len(tok2.encode(text))} tokens")
```

### Issue: Custom Tokenizer Not Loading

**Solution:**

```python
# Check file exists and format is correct
import os
from pathlib import Path

tokenizer_path = "./tokenizers/custom.json"
if not Path(tokenizer_path).exists():
    print(f"File not found: {tokenizer_path}")

# Try loading directly
try:
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    print(f"✓ Loaded successfully: {len(tokenizer)} tokens in vocab")
except Exception as e:
    print(f"✗ Error: {e}")
```

### Issue: Token Counts Don't Match API

**Solution:**

```python
# Different APIs may use different tokenizers
# Always use the correct tokenizer for your target API

api_tokenizers = {
    "openai_gpt4": "gpt2",  # Approximation
    "anthropic_claude": "gpt2",  # Approximation
    "llama3.2": "meta-llama/Llama-3.2-1B",
    "mistral": "mistralai/Mistral-7B-v0.1"
}

# Use appropriate tokenizer for estimation
```

## Best Practices

### 1. Always Validate Before Production

```python
# Test on representative sample
test_corpus = load_production_sample()
validation = compare_on_corpus(
    corpus=test_corpus,
    tokenizer1="current",
    tokenizer2="new_candidate"
)

# Only proceed if better
if validation['mean_reduction'] > 5:
    print("✓ New tokenizer is better, proceed with integration")
else:
    print("✗ Marginal improvement, stick with current")
```

### 2. Consider Multiple Metrics

Not just token count:

- Token reduction percentage
- Vocabulary coverage
- Tokenization quality (important terms)
- Integration complexity
- Model compatibility

### 3. Test with Actual Model

```python
# Token efficiency doesn't always mean better model performance
# Always test end-to-end with your actual model
```

### 4. Version Control Tokenizers

```
./tokenizers/
├── production.json -> llama3.2_v1.json
├── llama3.2_v1.json
├── custom_superbpe_v1.json
├── custom_superbpe_v2.json
└── README.md  # Document which tokenizer is used where
```

### 5. Monitor Token Usage in Production

```python
# Track actual token usage
import logging

def log_token_usage(prompt, tokenizer_name):
    analysis = analyze_tokenization(prompt, tokenizer_name)
    logging.info(f"Tokens: {analysis['total_tokens']}, Tokenizer: {tokenizer_name}")

# Aggregate and analyze to find optimization opportunities
```

## Additional Resources

- **SuperBPE Training**: See the `superbpe` skill for comprehensive SuperBPE tokenizer training
- **Unsloth Fine-tuning**: See the `unsloth-finetuning` skill for integration with model training
- **MCP Server**: See the `unsloth-mcp-server` skill for codebase-specific guidance

## Summary

Unsloth's tokenizer tools enable:

- ✓ Quick comparison of tokenizers
- ✓ Detailed tokenization analysis
- ✓ Cost estimation and ROI calculation
- ✓ Seamless integration with Unsloth models
- ✓ Production validation and testing

Use these tools to select, validate, and optimize tokenizers for your specific use case.
