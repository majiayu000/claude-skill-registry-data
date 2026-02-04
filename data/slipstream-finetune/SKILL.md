---
name: slipstream-finetune
description: Finetune LLMs to speak Slipstream natively - complete guide with GLM-4-9B
---

# Slipstream Finetuning Guide

Train LLMs to communicate using the Slipstream protocol natively. This guide covers dataset generation, model finetuning, and releasing on HuggingFace.

## Recommended Model: GLM-4-9B-0414

**Why GLM-4-9B-0414?**
- MIT licensed (can release finetuned weights commercially)
- 9B parameters - good balance of capability and trainability
- Specifically optimized for function calling and agentic tasks
- Excellent instruction following

## Quick Start

### 1. Generate High-Quality Dataset

**Option A: Template-based (fast, free)**
```bash
python -m slipcore.finetune -n 1000 -f sharegpt -o slipstream_train.jsonl
```

**Option B: LLM-enhanced (higher quality, requires API)**
```bash
# Using Claude API (recommended for quality)
export ANTHROPIC_API_KEY="your-key"
python -m slipcore.finetune_llm -n 1000 --provider anthropic -o slipstream_train.jsonl

# Using OpenAI (good quality, widely available)
export OPENAI_API_KEY="your-key"
python -m slipcore.finetune_llm -n 1000 --provider openai --model gpt-4o-mini -o slipstream_train.jsonl

# Using Together.ai (cheaper, good for large datasets)
export TOGETHER_API_KEY="your-key"
python -m slipcore.finetune_llm -n 2000 --provider together --model meta-llama/Llama-3.3-70B-Instruct-Turbo -o slipstream_train.jsonl

# Using DeepSeek (very cheap, good quality)
export DEEPSEEK_API_KEY="your-key"
python -m slipcore.finetune_llm -n 2000 --provider deepseek -o slipstream_train.jsonl
```

**Cost Estimates for 1000 examples:**
| Provider | Model | ~Cost |
|----------|-------|-------|
| Anthropic | claude-sonnet-4-20250514 | ~$0.50 |
| OpenAI | gpt-4o-mini | ~$0.15 |
| Together | Llama-3.3-70B | ~$0.10 |
| DeepSeek | deepseek-chat | ~$0.02 |

### 2. Finetune GLM-4-9B with Unsloth

```python
from unsloth import FastLanguageModel
import torch

# Load GLM-4-9B-0414
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="THUDM/GLM-4-9B-0414",
    max_seq_length=2048,
    dtype=None,  # Auto-detect
    load_in_4bit=True,  # QLoRA - fits in ~8GB VRAM
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

# Load dataset
from datasets import load_dataset
dataset = load_dataset("json", data_files="slipstream_train.jsonl", split="train")

# GLM-4 chat template
def format_glm4(example):
    convs = example["conversations"]
    text = ""
    for conv in convs:
        if conv["from"] == "system":
            text += f"[gMASK]<sop><|system|>\n{conv['value']}"
        elif conv["from"] == "human":
            text += f"<|user|>\n{conv['value']}"
        elif conv["from"] == "gpt":
            text += f"<|assistant|>\n{conv['value']}"
    return {"text": text}

dataset = dataset.map(format_glm4)

# Train
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        max_steps=200,  # ~1000 examples, 2 epochs
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        output_dir="slipstream_glm4",
        optim="adamw_8bit",
        seed=42,
    ),
)

trainer.train()

# Save LoRA adapter
model.save_pretrained("slipstream_glm4_lora")
tokenizer.save_pretrained("slipstream_glm4_lora")
```

### 3. Test the Finetuned Model

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="slipstream_glm4_lora",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

# Test
prompt = """[gMASK]<sop><|system|>
You communicate using the Slipstream protocol.<|user|>
Tell the backend team to review the authentication code<|assistant|>
"""

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=64)
print(tokenizer.decode(outputs[0]))
# Expected: SLIP v1 agent backend RequestReview auth_code
```

### 4. Export and Release

**Option A: LoRA adapter only (~200MB)**
```python
model.push_to_hub("your-username/slipstream-glm4-9b-lora")
tokenizer.push_to_hub("your-username/slipstream-glm4-9b-lora")
```

**Option B: Merged full model (~18GB)**
```python
# Merge LoRA into base model
merged_model = model.merge_and_unload()
merged_model.push_to_hub("your-username/slipstream-glm4-9b")
tokenizer.push_to_hub("your-username/slipstream-glm4-9b")
```

**Option C: GGUF for Ollama/llama.cpp (~5-9GB)**
```python
# Save as GGUF quantized
model.save_pretrained_gguf(
    "slipstream_glm4_gguf",
    tokenizer,
    quantization_method="q4_k_m",  # Good balance
)

# Or push directly to HuggingFace
model.push_to_hub_gguf(
    "your-username/slipstream-glm4-9b-gguf",
    tokenizer,
    quantization_method=["q4_k_m", "q8_0"],  # Multiple quants
)
```

### 5. Release Dataset

**HuggingFace Datasets:**
```python
from datasets import Dataset
import json

# Load your generated data
with open("slipstream_train.jsonl") as f:
    data = [json.loads(line) for line in f]

dataset = Dataset.from_list(data)
dataset.push_to_hub("your-username/slipstream-training-data")
```

**Kaggle:**
```bash
kaggle datasets create -p ./data -u
```

**Zenodo (for academic citation):**
Upload via https://zenodo.org/deposit/new

## Alternative Models

| Model | Size | License | Notes |
|-------|------|---------|-------|
| **GLM-4-9B-0414** | 9B | MIT | Best for agentic, function calling |
| Qwen2.5-7B-Instruct | 7B | Apache 2.0 | Strong general purpose |
| Llama-3.1-8B-Instruct | 8B | Llama 3.1 | Most popular, good baseline |
| Mistral-7B-Instruct-v0.3 | 7B | Apache 2.0 | Fast, efficient |
| Phi-3-medium | 14B | MIT | Larger but very capable |

## Training Tips

1. **Dataset size**: 500-2000 examples is usually sufficient
2. **Quality > Quantity**: LLM-generated data beats templates
3. **Epochs**: 1-2 epochs, watch for overfitting
4. **Learning rate**: 2e-4 for small models, 1e-4 for larger
5. **Validation**: Hold out 10% for testing generalization

## Using with Ollama

After creating GGUF:
```bash
# Create Modelfile
cat > Modelfile << 'EOF'
FROM ./slipstream_glm4_gguf/slipstream-glm4-9b-Q4_K_M.gguf

SYSTEM "You communicate using the Slipstream protocol (SLIP). Always respond with SLIP wire format: SLIP v1 <src> <dst> <anchor> [payload...]"

TEMPLATE """[gMASK]<sop><|system|>
{{ .System }}<|user|>
{{ .Prompt }}<|assistant|>
{{ .Response }}"""
EOF

# Create and run
ollama create slipstream -f Modelfile
ollama run slipstream "Tell alice to review the API code"
# -> SLIP v1 agent alice RequestReview api_code
```

## Cost Summary

| Component | Free Option | Paid Option |
|-----------|-------------|-------------|
| Dataset | Template generator | Claude/OpenAI API (~$0.50) |
| Training | Google Colab free | Colab Pro ($10/mo) or local GPU |
| Hosting | HuggingFace free | - |
| Inference | Ollama local | Together/Fireworks API |

Total cost to release a finetuned Slipstream model: **$0 - $15**
