---
name: example-projects
description: Provides three production-ready ML training examples (sentiment classification, text generation, RedAI trade classifier) with complete training scripts, deployment configs, and datasets. Use when user needs example projects, reference implementations, starter templates, or wants to see working code for sentiment analysis, text generation, or financial trade classification.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# ML Training Example Projects

**Purpose:** Provide complete, runnable example projects demonstrating ML training workflows from data preparation through deployment.

**Activation Triggers:**
- User requests example projects or starter templates
- User wants to see working sentiment classification code
- User needs text generation training examples
- User mentions RedAI trade classifier
- User wants reference implementations
- User needs to understand complete training workflows

**Key Resources:**
- `scripts/setup-example.sh` - Initialize and setup any example project
- `scripts/run-training.sh` - Execute training for any example
- `scripts/test-inference.sh` - Test trained models
- `examples/sentiment-classification/` - Binary sentiment classification (IMDB-style)
- `examples/text-generation/` - GPT-style text generation with LoRA
- `examples/redai-trade-classifier/` - Financial trade classification with Modal deployment
- `templates/` - Scaffolding for new projects

## Available Example Projects

### 1. Sentiment Classification

**Use Case:** Binary sentiment analysis (positive/negative reviews)

**Features:**
- DistilBERT fine-tuning for text classification
- Custom dataset loading from JSON
- Training with validation metrics
- Model saving and inference
- Production-ready inference API

**Files:**
- `train.py` - Complete training script
- `data.json` - Sample training data (50 examples)
- `inference.py` - Inference server
- `README.md` - Setup and usage guide

**Dataset Format:**
```json
{"text": "This movie was amazing!", "label": 1}
{"text": "Terrible waste of time", "label": 0}
```

### 2. Text Generation

**Use Case:** Fine-tune GPT-2 for custom text generation

**Features:**
- GPT-2 small model fine-tuning
- LoRA (Low-Rank Adaptation) for efficient training
- Custom tokenization
- Generation with temperature/top-p sampling
- Modal deployment configuration

**Files:**
- `train.py` - LoRA training script
- `config.yaml` - Hyperparameters and model config
- `generate.py` - Text generation script
- `modal_deploy.py` - Modal deployment
- `README.md` - Complete guide

**Config Structure:**
```yaml
model:
  name: gpt2
  max_length: 512
training:
  epochs: 3
  batch_size: 4
  learning_rate: 2e-4
lora:
  r: 8
  alpha: 16
  dropout: 0.1
```

### 3. RedAI Trade Classifier

**Use Case:** Financial trade classification (buy/sell/hold)

**Features:**
- Multi-class classification for trading signals
- Feature engineering from market data
- Class imbalance handling
- Modal deployment for production inference
- Real-time prediction API

**Files:**
- `train.py` - Training with class weighting
- `modal_deploy.py` - Complete Modal deployment
- `data_preprocessing.py` - Feature engineering
- `README.md` - Trading strategy guide

**Model Input:**
- Price features (open, high, low, close)
- Volume indicators
- Technical indicators (RSI, MACD, moving averages)
- Sentiment scores

## Quick Start

### Setup Any Example

```bash
# Initialize example project
./scripts/setup-example.sh <project-name>

# Options: sentiment-classification, text-generation, redai-trade-classifier
./scripts/setup-example.sh sentiment-classification
```

**What it does:**
- Creates project directory
- Copies example files
- Installs dependencies
- Downloads/prepares sample data
- Validates environment

### Run Training

```bash
# Train model for any example
./scripts/run-training.sh <project-name>

# Examples:
./scripts/run-training.sh sentiment-classification
./scripts/run-training.sh text-generation
./scripts/run-training.sh redai-trade-classifier
```

**Monitors:**
- Training progress
- Loss curves
- Validation metrics
- GPU utilization
- Checkpoint saving

### Test Inference

```bash
# Test trained model
./scripts/test-inference.sh <project-name> <input>

# Examples:
./scripts/test-inference.sh sentiment-classification "This product is great!"
./scripts/test-inference.sh text-generation "Once upon a time"
./scripts/test-inference.sh redai-trade-classifier market_data.json
```

## Common Workflows

### Start From Example Template

1. **Choose example** based on use case:
   - Classification → sentiment-classification
   - Generation → text-generation
   - Financial ML → redai-trade-classifier

2. **Setup project:**
   ```bash
   ./scripts/setup-example.sh <example-name>
   ```

3. **Customize for your data:**
   - Update data loading in `train.py`
   - Modify model architecture if needed
   - Adjust hyperparameters in config

4. **Run training:**
   ```bash
   ./scripts/run-training.sh <example-name>
   ```

5. **Deploy:**
   - Local: Use `inference.py`
   - Production: Use `modal_deploy.py`

### Extend Example with Custom Data

1. **Prepare data** in example format
2. **Replace data files** (data.json, config.yaml)
3. **Update preprocessing** if needed
4. **Train with same script**
5. **Test inference** with new data

### Deploy Example to Production

All examples include Modal deployment:

```bash
# Deploy to Modal
cd examples/<project-name>
modal deploy modal_deploy.py

# Get endpoint URL
modal app show <app-name>
```

## Example Comparison

| Feature | Sentiment | Text Gen | Trade Classifier |
|---------|-----------|----------|------------------|
| Task Type | Binary Classification | Generation | Multi-class |
| Model | DistilBERT | GPT-2 + LoRA | Custom Transformer |
| Training Time | 5-10 min | 15-30 min | 10-20 min |
| GPU Required | Optional | Recommended | Required |
| Modal Deploy | ✅ | ✅ | ✅ |
| Custom Data | Easy | Moderate | Advanced |

## Customization Guide

### Sentiment Classification

**Change dataset:**
```python
# In train.py, update load_data()
def load_data(path):
    # Your custom loading logic
    return texts, labels
```

**Change model:**
```python
# Replace DistilBERT with other models
model_name = "bert-base-uncased"  # or roberta-base, etc.
```

### Text Generation

**Change generation style:**
```yaml
# In config.yaml
generation:
  temperature: 0.8    # Higher = more creative
  top_p: 0.9          # Nucleus sampling
  max_length: 200     # Output length
```

**Add custom prompts:**
```python
# In generate.py
prompts = [
    "Your custom prompt here",
    "Another prompt"
]
```

### Trade Classifier

**Add features:**
```python
# In data_preprocessing.py
def engineer_features(df):
    df['rsi'] = calculate_rsi(df['close'])
    df['macd'] = calculate_macd(df['close'])
    # Add your custom indicators
    return df
```

**Change strategy:**
```python
# Update labels in train.py
# 0 = sell, 1 = hold, 2 = buy
labels = your_strategy(prices, indicators)
```

## Dependencies

Each example includes its own `requirements.txt`:

**Sentiment Classification:**
- transformers
- torch
- datasets
- scikit-learn

**Text Generation:**
- transformers
- peft (LoRA)
- torch
- modal (deployment)

**Trade Classifier:**
- transformers
- pandas
- numpy
- modal
- ta (technical analysis)

## Troubleshooting

### Training Fails

**Issue:** Out of memory
**Fix:** Reduce batch size in config

**Issue:** CUDA not available
**Fix:** Use CPU or install CUDA toolkit

### Inference Errors

**Issue:** Model not found
**Fix:** Check checkpoint path in inference script

**Issue:** Wrong input format
**Fix:** Validate input matches training data format

### Deployment Issues

**Issue:** Modal authentication
**Fix:** Run `modal token new` to authenticate

**Issue:** Dependency conflicts
**Fix:** Use exact versions from requirements.txt

## Resources

**Scripts:** All scripts are in `scripts/` with execution permissions

**Examples:** Complete projects in `examples/` directory

**Templates:** Scaffolding in `templates/` for creating new projects

**Documentation:** Each example has detailed README.md

---

**Supported Frameworks:** PyTorch, Transformers, PEFT
**Deployment Platforms:** Modal, Local, FastAPI
**Version:** 1.0.0
