---
name: training-patterns
description: Templates and patterns for common ML training scenarios including text classification, text generation, fine-tuning, and PEFT/LoRA. Provides ready-to-use training configurations, dataset preparation scripts, and complete training pipelines. Use when building ML training pipelines, fine-tuning models, implementing classification or generation tasks, setting up PEFT/LoRA training, or when user mentions model training, fine-tuning, classification, generation, or parameter-efficient tuning.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# ML Training Patterns

**Purpose:** Provide production-ready training templates, configuration files, and automation scripts for common ML training scenarios including classification, generation, fine-tuning, and PEFT/LoRA approaches.

**Activation Triggers:**
- Building text classification models (sentiment, intent, NER, etc.)
- Training text generation models (summarization, Q&A, chatbots)
- Fine-tuning pre-trained models for specific tasks
- Implementing PEFT (Parameter-Efficient Fine-Tuning) with LoRA
- Setting up training pipelines with HuggingFace Transformers
- Configuring training hyperparameters and optimization
- Preparing datasets for model training

**Key Resources:**
- `scripts/setup-classification.sh` - Classification training setup automation
- `scripts/setup-generation.sh` - Generation training setup automation
- `scripts/setup-fine-tuning.sh` - Full fine-tuning setup automation
- `scripts/setup-peft.sh` - PEFT/LoRA training setup automation
- `templates/classification-config.yaml` - Classification training configuration
- `templates/generation-config.yaml` - Generation training configuration
- `templates/peft-config.json` - PEFT/LoRA configuration
- `examples/sentiment-classifier.md` - Complete sentiment classification example
- `examples/text-generator.md` - Complete text generation example

## Training Scenarios Overview

### 1. Text Classification

**Use cases:** Sentiment analysis, intent classification, topic categorization, spam detection, named entity recognition (NER)

**Key characteristics:**
- Input: Text → Output: Class label(s)
- Typically uses encoder models (BERT, RoBERTa, DistilBERT)
- Fast inference, suitable for production
- Requires labeled training data

**Setup command:**
```bash
./scripts/setup-classification.sh <project-name> <model-name> <num-classes>
```

**Example:**
```bash
./scripts/setup-classification.sh sentiment-model distilbert-base-uncased 3
```

### 2. Text Generation

**Use cases:** Summarization, question answering, chatbots, text completion, translation, code generation

**Key characteristics:**
- Input: Text (prompt) → Output: Generated text
- Uses decoder or encoder-decoder models (GPT-2, T5, BART)
- More computationally intensive
- Can be trained with or without labeled data

**Setup command:**
```bash
./scripts/setup-generation.sh <project-name> <model-name> <generation-type>
```

**Example:**
```bash
./scripts/setup-generation.sh qa-bot t5-small question-answering
```

### 3. Full Fine-Tuning

**Use cases:** When you have sufficient data and compute to retrain all model parameters

**Key characteristics:**
- Updates all model weights
- Requires significant compute (GPU with 16GB+ VRAM)
- Best for substantial domain adaptation
- Training time: hours to days

**Setup command:**
```bash
./scripts/setup-fine-tuning.sh <project-name> <model-name> <task-type>
```

**Example:**
```bash
./scripts/setup-fine-tuning.sh medical-classifier bert-base-uncased classification
```

### 4. PEFT (Parameter-Efficient Fine-Tuning)

**Use cases:** Limited compute resources, quick experimentation, domain adaptation with small datasets

**Key characteristics:**
- Only trains a small subset of parameters (LoRA adapters)
- 10-100x less memory than full fine-tuning
- Fast training (minutes to hours)
- Can fine-tune large models (7B+) on consumer GPUs
- Uses techniques like LoRA, QLoRA, Prefix Tuning, Adapter Layers

**Setup command:**
```bash
./scripts/setup-peft.sh <project-name> <model-name> <peft-method>
```

**Example:**
```bash
./scripts/setup-peft.sh efficient-classifier roberta-base lora
```

## Classification Training Pattern

### Configuration Template

**File:** `templates/classification-config.yaml`

**Key parameters:**
```yaml
model:
  name: distilbert-base-uncased
  num_labels: 3
  task_type: classification

dataset:
  train_file: data/train.csv
  validation_file: data/val.csv
  test_file: data/test.csv
  text_column: text
  label_column: label

training:
  output_dir: ./outputs
  num_epochs: 3
  batch_size: 16
  learning_rate: 2e-5
  warmup_steps: 500
  weight_decay: 0.01
  evaluation_strategy: epoch
  save_strategy: epoch
  logging_steps: 100
  fp16: true  # Mixed precision training
  gradient_accumulation_steps: 1

optimizer:
  name: adamw
  betas: [0.9, 0.999]
  epsilon: 1e-8
```

### Training Pipeline

**1. Dataset Preparation:**
```python
from datasets import load_dataset

# Load from CSV
dataset = load_dataset('csv', data_files={
    'train': 'data/train.csv',
    'validation': 'data/val.csv',
    'test': 'data/test.csv'
})

# Preprocess
def preprocess(examples):
    return tokenizer(
        examples['text'],
        truncation=True,
        padding='max_length',
        max_length=512
    )

dataset = dataset.map(preprocess, batched=True)
```

**2. Model Initialization:**
```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=num_classes,
    id2label={0: 'negative', 1: 'neutral', 2: 'positive'},
    label2id={'negative': 0, 'neutral': 1, 'positive': 2}
)
```

**3. Training:**
```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir='./outputs',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='accuracy',
    fp16=True,  # Enable mixed precision
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['validation'],
    compute_metrics=compute_metrics,
)

trainer.train()
```

**4. Evaluation:**
```python
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = predictions.argmax(axis=-1)

    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average='weighted'
    )

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Evaluate on test set
results = trainer.evaluate(dataset['test'])
print(results)
```

## Generation Training Pattern

### Configuration Template

**File:** `templates/generation-config.yaml`

**Key parameters:**
```yaml
model:
  name: t5-small
  task_type: generation
  generation_type: question-answering  # or summarization, translation, etc.

dataset:
  train_file: data/train.json
  validation_file: data/val.json
  input_column: question
  target_column: answer
  max_input_length: 512
  max_target_length: 128

training:
  output_dir: ./outputs
  num_epochs: 5
  batch_size: 8
  learning_rate: 3e-4
  warmup_steps: 1000
  weight_decay: 0.01
  evaluation_strategy: steps
  eval_steps: 500
  save_steps: 500
  logging_steps: 100
  fp16: true
  gradient_accumulation_steps: 2
  predict_with_generate: true

generation:
  max_length: 128
  min_length: 10
  num_beams: 4
  length_penalty: 2.0
  early_stopping: true
  no_repeat_ngram_size: 3
```

### Training Pipeline

**1. Dataset Preparation:**
```python
from datasets import load_dataset

# Load from JSON (question-answer pairs)
dataset = load_dataset('json', data_files={
    'train': 'data/train.json',
    'validation': 'data/val.json'
})

# Preprocess for seq2seq
def preprocess(examples):
    inputs = tokenizer(
        examples['question'],
        max_length=512,
        truncation=True,
        padding='max_length'
    )

    # Tokenize targets
    with tokenizer.as_target_tokenizer():
        targets = tokenizer(
            examples['answer'],
            max_length=128,
            truncation=True,
            padding='max_length'
        )

    inputs['labels'] = targets['input_ids']
    return inputs

dataset = dataset.map(preprocess, batched=True)
```

**2. Model & Training:**
```python
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer

model = AutoModelForSeq2SeqLM.from_pretrained('t5-small')

training_args = Seq2SeqTrainingArguments(
    output_dir='./outputs',
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    learning_rate=3e-4,
    predict_with_generate=True,
    generation_max_length=128,
    generation_num_beams=4,
    fp16=True,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['validation'],
)

trainer.train()
```

**3. Generation & Evaluation:**
```python
# Generate predictions
def generate_answer(question):
    inputs = tokenizer(question, return_tensors='pt', max_length=512, truncation=True)
    outputs = model.generate(
        **inputs,
        max_length=128,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test
question = "What is machine learning?"
answer = generate_answer(question)
print(f"Q: {question}\nA: {answer}")
```

## PEFT/LoRA Training Pattern

### Why PEFT/LoRA?

**Traditional fine-tuning challenges:**
- Requires updating all model parameters (millions to billions)
- High GPU memory requirements (often 40GB+ for 7B models)
- Slow training (hours to days)
- Risk of catastrophic forgetting

**PEFT/LoRA benefits:**
- Only trains ~0.1-1% of parameters (LoRA adapters)
- 10-100x less memory usage
- 3-10x faster training
- Can fine-tune 7B+ models on consumer GPUs (RTX 3090, 4090)
- Multiple task adapters for same base model

### Configuration Template

**File:** `templates/peft-config.json`

```json
{
  "peft_type": "LORA",
  "task_type": "SEQ_CLS",
  "inference_mode": false,
  "r": 8,
  "lora_alpha": 16,
  "lora_dropout": 0.1,
  "target_modules": [
    "query",
    "key",
    "value",
    "dense"
  ],
  "bias": "none",
  "modules_to_save": ["classifier"]
}
```

**Key parameters:**
- `r`: LoRA rank (lower = fewer parameters, typically 4-64)
- `lora_alpha`: Scaling factor (typically 2x rank)
- `lora_dropout`: Dropout for LoRA layers (0.05-0.1)
- `target_modules`: Which layers to apply LoRA (query, key, value, dense)

### Training Pipeline

**1. Install PEFT:**
```bash
pip install peft
```

**2. Setup PEFT Model:**
```python
from transformers import AutoModelForSequenceClassification
from peft import get_peft_model, LoraConfig, TaskType

# Load base model
base_model = AutoModelForSequenceClassification.from_pretrained(
    'roberta-base',
    num_labels=3
)

# Configure LoRA
peft_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    inference_mode=False,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=['query', 'key', 'value', 'dense']
)

# Apply PEFT
model = get_peft_model(base_model, peft_config)
model.print_trainable_parameters()
# Output: trainable params: 296,448 || all params: 124,940,546 || trainable%: 0.237%
```

**3. Training:**
```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir='./peft_outputs',
    num_train_epochs=3,
    per_device_train_batch_size=16,  # Can use larger batch size!
    learning_rate=1e-3,  # Higher learning rate for PEFT
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
    eval_dataset=dataset['validation'],
)

trainer.train()
```

**4. Save & Load Adapters:**
```python
# Save only LoRA adapters (tiny file, ~1-10MB)
model.save_pretrained('./lora_adapters')

# Load adapters later
from peft import PeftModel
base_model = AutoModelForSequenceClassification.from_pretrained('roberta-base', num_labels=3)
model = PeftModel.from_pretrained(base_model, './lora_adapters')
```

### QLoRA (Quantized LoRA)

For even more memory efficiency with large models:

```python
from transformers import BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    'meta-llama/Llama-2-7b-hf',
    quantization_config=bnb_config,
    device_map='auto'
)

# Apply LoRA on top of quantized model
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)

# Now can fine-tune 7B model on 16GB GPU!
```

## Setup Scripts Usage

### Classification Setup

```bash
cd /home/gotime2022/.claude/plugins/marketplaces/ai-dev-marketplace/plugins/ml-training/skills/training-patterns
./scripts/setup-classification.sh my-classifier distilbert-base-uncased 3
```

**Creates:**
- Project directory structure
- Training script with Trainer API
- Configuration file (classification-config.yaml)
- Dataset preparation script
- Requirements.txt
- README with instructions

**Arguments:**
- `project-name`: Name of training project
- `model-name`: HuggingFace model identifier
- `num-classes`: Number of classification labels

### Generation Setup

```bash
./scripts/setup-generation.sh my-generator t5-small summarization
```

**Creates:**
- Seq2Seq training pipeline
- Generation configuration
- Dataset processing for input-target pairs
- Evaluation with ROUGE/BLEU metrics
- Inference script

**Arguments:**
- `project-name`: Name of training project
- `model-name`: HuggingFace model identifier
- `generation-type`: summarization, question-answering, translation, etc.

### Fine-Tuning Setup

```bash
./scripts/setup-fine-tuning.sh domain-model bert-base-uncased classification
```

**Creates:**
- Full fine-tuning pipeline
- GPU memory optimization configs
- Gradient checkpointing setup
- Mixed precision training
- Model checkpointing strategy

**Arguments:**
- `project-name`: Name of training project
- `model-name`: HuggingFace model identifier
- `task-type`: classification or generation

### PEFT Setup

```bash
./scripts/setup-peft.sh efficient-trainer roberta-base lora
```

**Creates:**
- PEFT training pipeline with LoRA
- Adapter configuration
- Memory-efficient training setup
- Adapter save/load utilities
- Multi-adapter management

**Arguments:**
- `project-name`: Name of training project
- `model-name`: HuggingFace model identifier
- `peft-method`: lora, qlora, prefix-tuning, or adapter

## Dataset Formats

### Classification Dataset (CSV)

```csv
text,label
"This product is amazing!",positive
"Terrible experience",negative
"It's okay, nothing special",neutral
```

### Generation Dataset (JSON)

```json
[
  {
    "question": "What is the capital of France?",
    "answer": "The capital of France is Paris."
  },
  {
    "question": "How does photosynthesis work?",
    "answer": "Photosynthesis is the process where plants convert light energy into chemical energy..."
  }
]
```

### HuggingFace Datasets Integration

```python
from datasets import load_dataset

# Load from HuggingFace Hub
dataset = load_dataset('glue', 'sst2')  # Sentiment classification
dataset = load_dataset('squad')  # Question answering
dataset = load_dataset('cnn_dailymail', '3.0.0')  # Summarization

# Load local files
dataset = load_dataset('csv', data_files='data.csv')
dataset = load_dataset('json', data_files='data.json')
```

## Training Best Practices

### 1. Hyperparameter Selection

**Learning Rate:**
- Full fine-tuning: 1e-5 to 5e-5
- PEFT/LoRA: 1e-4 to 1e-3 (can be higher)
- Rule of thumb: Start with 2e-5 for full, 3e-4 for PEFT

**Batch Size:**
- As large as GPU memory allows
- Use gradient accumulation if batch size limited
- Effective batch size = batch_size × gradient_accumulation_steps

**Epochs:**
- Classification: 3-5 epochs
- Generation: 5-10 epochs
- Watch for overfitting with validation metrics

**Warmup Steps:**
- Typically 10% of total training steps
- Helps stabilize training initially

### 2. GPU Memory Optimization

**Techniques:**
- Mixed precision (fp16/bf16): 2x memory reduction
- Gradient checkpointing: 30-50% memory reduction (slower training)
- Gradient accumulation: Simulate larger batch sizes
- PEFT/LoRA: 10-100x memory reduction
- 8-bit/4-bit quantization: 2-4x memory reduction

**Example:**
```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    fp16=True,  # Mixed precision
    gradient_checkpointing=True,  # Memory optimization
    gradient_accumulation_steps=4,  # Effective batch size × 4
    per_device_train_batch_size=4,  # Small batch per GPU
)
```

### 3. Monitoring Training

**Track these metrics:**
- Training loss (should decrease steadily)
- Validation loss (should decrease, not increase)
- Validation accuracy/F1/ROUGE (should increase)
- Learning rate schedule
- GPU memory usage

**Use Weights & Biases:**
```python
training_args = TrainingArguments(
    report_to='wandb',
    run_name='my-training-run',
)
```

### 4. Early Stopping

```python
from transformers import EarlyStoppingCallback

trainer = Trainer(
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
)
```

### 5. Model Checkpointing

```python
training_args = TrainingArguments(
    save_strategy='epoch',  # Save after each epoch
    save_total_limit=3,  # Keep only best 3 checkpoints
    load_best_model_at_end=True,  # Load best after training
    metric_for_best_model='f1',  # Choose best by F1 score
)
```

## Common Training Patterns

### Pattern 1: Quick Experimentation (PEFT)

**When:** Testing ideas, limited compute, small datasets
**Approach:** LoRA with small rank (r=4-8)
**Time:** Minutes to 1 hour
**Memory:** Can fine-tune 7B models on 16GB GPU

### Pattern 2: Production Classification (Full Fine-Tuning)

**When:** Production deployment, sufficient labeled data
**Approach:** Full fine-tuning with early stopping
**Time:** 1-6 hours
**Memory:** 16GB GPU for base models (110M-340M params)

### Pattern 3: Domain Adaptation (PEFT + Full)

**When:** Adapting to specific domain, then task-specific fine-tuning
**Approach:**
1. PEFT on domain data (unlabeled or weakly labeled)
2. Full fine-tuning on task data (labeled)
**Time:** 2-12 hours total
**Memory:** 16-40GB GPU

### Pattern 4: Multi-Task Learning (Multiple LoRA Adapters)

**When:** One model for multiple tasks
**Approach:** Train separate LoRA adapters per task, swap at inference
**Time:** 1-3 hours per task
**Memory:** 16GB GPU, adapters are tiny (1-10MB each)

## Troubleshooting

**Out of Memory (OOM) Errors:**
- Reduce batch size
- Enable gradient checkpointing
- Use gradient accumulation
- Switch to PEFT/LoRA
- Use 8-bit quantization

**Training Not Converging:**
- Lower learning rate
- Increase warmup steps
- Check data quality and preprocessing
- Verify labels are correct
- Try different optimizer (AdamW vs SGD)

**Overfitting:**
- Add dropout
- Use weight decay
- Get more training data
- Use data augmentation
- Early stopping

**Slow Training:**
- Enable fp16 mixed precision
- Increase batch size
- Use gradient accumulation less
- Remove gradient checkpointing
- Use faster model variant (distilbert vs bert)

**Poor Evaluation Metrics:**
- Check data distribution (train vs val vs test)
- Verify preprocessing is consistent
- Try different model architecture
- Increase model size or training time
- Check for label imbalance

---

**Supported Models:**
- Classification: BERT, RoBERTa, DistilBERT, ALBERT, DeBERTa
- Generation: T5, BART, GPT-2, Llama-2, Mistral, Phi
- PEFT: Compatible with all transformer models

**Requirements:**
- Python 3.11+
- PyTorch 2.0+
- Transformers 4.30+
- PEFT 0.7+ (for LoRA)
- Datasets 2.14+

**Best Practice:** Start with PEFT/LoRA for quick iteration, switch to full fine-tuning only when necessary
