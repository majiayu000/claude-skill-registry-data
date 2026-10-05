---
name: nlp-in-task-pretraining
description: >
  Further pretrains a transformer with masked language modeling on the target task's own text before fine-tuning.
---
# In-Task Pre-Training (ITPT)

## Overview

Before fine-tuning a pretrained transformer on your target task, run additional masked language modeling (MLM) on the task's own text corpus. This adapts the model's language understanding to the domain and vocabulary of your specific data, often improving downstream performance by 0.5-2% RMSE.

## Quick Start

```python
from transformers import (
    AutoModelForMaskedLM, AutoTokenizer,
    DataCollatorForLanguageModeling, TrainingArguments, Trainer
)

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelForMaskedLM.from_pretrained("roberta-base")

# Tokenize task text
def tokenize(examples):
    return tokenizer(examples["text"], truncation=True, max_length=256)

dataset = dataset.map(tokenize, batched=True)
collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)

args = TrainingArguments(
    output_dir="./itpt", num_train_epochs=5,
    per_device_train_batch_size=16, learning_rate=5e-5,
)
trainer = Trainer(model=model, args=args, train_dataset=dataset, data_collator=collator)
trainer.train()
model.save_pretrained("./itpt-roberta")
```

## Workflow

1. Collect all text from train + test (no labels needed)
2. Run MLM pre-training for 3-10 epochs with 15% masking
3. Save the adapted checkpoint
4. Fine-tune from the adapted checkpoint on the labeled task

## Key Decisions

- **Epochs**: 3-10; watch perplexity on held-out text, stop when it plateaus
- **Include test text**: Yes — MLM is unsupervised, no leakage
- **MLM probability**: 0.15 is standard; 0.20 for very domain-specific text
- **Learning rate**: Same as pre-training (5e-5), not fine-tuning rate

## References

- CommonLit Readability Prize (Kaggle)
- Source: [commonlit-readability-prize-roberta-torch-itpt](https://www.kaggle.com/code/rhtsingh/commonlit-readability-prize-roberta-torch-itpt)
