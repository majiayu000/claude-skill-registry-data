---
name: fine-tuning
description: LLM fine-tuning with LoRA, QLoRA, and instruction tuning for domain adaptation.
sasmp_version: "1.3.0"
bonded_agent: 04-fine-tuning
bond_type: PRIMARY_BOND
---

# Fine-Tuning

Adapt LLMs to specific tasks and domains efficiently.

## Quick Start

### LoRA Fine-Tuning with PEFT
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset
from trl import SFTTrainer

# Load base model
model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Configure LoRA
lora_config = LoraConfig(
    r=16,                          # Rank
    lora_alpha=32,                 # Alpha scaling
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%

# Training arguments
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    logging_steps=10,
    save_strategy="epoch"
)

# Train
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    max_seq_length=512
)
trainer.train()
```

### QLoRA (4-bit Quantized LoRA)
```python
from transformers import BitsAndBytesConfig
import torch

# Quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Apply LoRA on top of quantized model
model = get_peft_model(model, lora_config)
```

## Dataset Preparation

### Instruction Dataset Format
```python
# Alpaca format
instruction_format = {
    "instruction": "Summarize the following text.",
    "input": "The quick brown fox jumps over the lazy dog...",
    "output": "A fox jumps over a dog."
}

# ChatML format
chat_format = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Summarize this text: ..."},
    {"role": "assistant", "content": "Summary: ..."}
]

# Formatting function
def format_instruction(sample):
    return f"""### Instruction:
{sample['instruction']}

### Input:
{sample['input']}

### Response:
{sample['output']}"""
```

### Data Preparation Pipeline
```python
from datasets import Dataset
import json

class DatasetPreparer:
    def __init__(self, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def prepare(self, data_path: str) -> Dataset:
        # Load raw data
        with open(data_path) as f:
            raw_data = json.load(f)

        # Format samples
        formatted = [self._format_sample(s) for s in raw_data]

        # Create dataset
        dataset = Dataset.from_dict({"text": formatted})

        # Tokenize
        return dataset.map(
            self._tokenize,
            batched=True,
            remove_columns=["text"]
        )

    def _format_sample(self, sample):
        return f"""<s>[INST] {sample['instruction']}

{sample['input']} [/INST] {sample['output']}</s>"""

    def _tokenize(self, examples):
        return self.tokenizer(
            examples["text"],
            truncation=True,
            max_length=self.max_length,
            padding="max_length"
        )
```

## Fine-Tuning Methods Comparison

| Method | VRAM | Speed | Quality | Use Case |
|--------|------|-------|---------|----------|
| Full Fine-Tune | 60GB+ | Slow | Best | Unlimited resources |
| LoRA | 16GB | Fast | Very Good | Most applications |
| QLoRA | 8GB | Medium | Good | Consumer GPUs |
| Prefix Tuning | 8GB | Fast | Good | Fixed tasks |
| Prompt Tuning | 4GB | Very Fast | Moderate | Simple adaptation |

## LoRA Hyperparameters

```yaml
rank (r):
  small (4-8): Simple tasks, less capacity
  medium (16-32): General fine-tuning
  large (64-128): Complex domain adaptation

alpha:
  rule: Usually 2x rank
  effect: Higher = more influence from LoRA weights

target_modules:
  attention: [q_proj, k_proj, v_proj, o_proj]
  mlp: [gate_proj, up_proj, down_proj]
  all: Maximum adaptation, more VRAM

dropout:
  typical: 0.05-0.1
  effect: Regularization, prevents overfitting
```

## Training Best Practices

### Learning Rate Schedule
```python
from transformers import get_cosine_schedule_with_warmup

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4)
scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=100,
    num_training_steps=total_steps
)
```

### Gradient Checkpointing
```python
# Save memory by recomputing activations
model.gradient_checkpointing_enable()

# Also enable for LoRA
model.enable_input_require_grads()
```

### Evaluation During Training
```python
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    # Shift for causal LM
    predictions = predictions[:, :-1]
    labels = labels[:, 1:]

    # Calculate perplexity
    loss_fct = torch.nn.CrossEntropyLoss(reduction='mean')
    loss = loss_fct(predictions.view(-1, vocab_size), labels.view(-1))
    perplexity = torch.exp(loss)

    return {"perplexity": perplexity.item()}
```

## Merging and Deploying

### Merge LoRA Weights
```python
# After training, merge LoRA into base model
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")
```

### Multiple LoRA Adapters
```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained("base_model")

# Load and switch between adapters
model = PeftModel.from_pretrained(base_model, "adapter_1")
model.load_adapter("adapter_2", adapter_name="code")

# Switch adapters at runtime
model.set_adapter("code")  # Use code adapter
model.set_adapter("default")  # Use default adapter
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Loss not decreasing | LR too low/high | Adjust learning rate |
| OOM errors | Batch too large | Reduce batch, use gradient accumulation |
| Overfitting | Too many epochs | Early stopping, more data |
| Catastrophic forgetting | Too aggressive LR | Lower LR, shorter training |
| Poor quality | Data issues | Clean and validate dataset |

## Error Handling & Recovery

```python
from transformers import TrainerCallback

class CheckpointCallback(TrainerCallback):
    def on_save(self, args, state, control, **kwargs):
        # Always keep last 3 checkpoints
        pass

    def on_epoch_end(self, args, state, control, **kwargs):
        if state.best_metric is None:
            # Save checkpoint on each epoch
            control.should_save = True
```

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| NaN loss | LR too high | Lower to 1e-5 |
| No improvement | LR too low | Increase 10x |
| OOM mid-training | Batch too large | Enable gradient checkpointing |

## Unit Test Template

```python
def test_lora_config():
    config = LoraConfig(r=16, lora_alpha=32)
    model = get_peft_model(base_model, config)
    assert model.print_trainable_parameters() < 1%
```
