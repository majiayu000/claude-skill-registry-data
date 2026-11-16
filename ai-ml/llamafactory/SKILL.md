---
name: llamafactory
description: "Use when fine-tuning, training, or doing LoRA/QLoRA on LLMs. Triggers on: 'fine-tune LLM', 'LoRA', 'QLoRA', 'llamafactory', 'llama factory', 'train model', 'SFT', 'RLHF', 'DPO', 'fine tuning', 'custom model', 'instruction tuning', 'finetuning'."
---

# LlamaFactory Skill

Fine-tune 100+ LLMs (Llama, Qwen, Gemma, Mistral...) với zero-code CLI hoặc Web UI.
Source: [hiyouga/LlamaFactory](https://github.com/hiyouga/LlamaFactory) (71K⭐, Apache 2.0)

## Install

```bash
pip install llamafactory
# hoặc với CUDA
pip install llamafactory[torch,metrics]
```

## Workflow

### Step 1 — Chuẩn bị dataset

Format Alpaca (phổ biến nhất):

```json
[
  {
    "instruction": "Dịch câu sau sang tiếng Anh",
    "input": "Tôi yêu Việt Nam",
    "output": "I love Vietnam"
  }
]
```

Format ShareGPT (multi-turn):
```json
[
  {
    "conversations": [
      {"from": "human", "value": "Bạn là ai?"},
      {"from": "gpt", "value": "Tôi là trợ lý AI."}
    ]
  }
]
```

Đăng ký dataset trong `data/dataset_info.json`:
```json
{
  "my_dataset": {
    "file_name": "my_data.json",
    "formatting": "alpaca"
  }
}
```

### Step 2 — Train với CLI (LoRA SFT)

```bash
llamafactory-cli train \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --stage sft \
  --do_train \
  --dataset my_dataset \
  --template qwen \
  --finetuning_type lora \
  --lora_rank 8 \
  --output_dir outputs/my-model \
  --num_train_epochs 3 \
  --per_device_train_batch_size 4 \
  --learning_rate 1e-4 \
  --fp16
```

### Step 3 — Train với config YAML (khuyên dùng)

```yaml
# train_config.yaml
model_name_or_path: Qwen/Qwen2.5-7B-Instruct
stage: sft
do_train: true
dataset: my_dataset
template: qwen
finetuning_type: lora
lora_rank: 8
output_dir: outputs/my-model
num_train_epochs: 3
per_device_train_batch_size: 4
gradient_accumulation_steps: 4
learning_rate: 1.0e-4
lr_scheduler_type: cosine
fp16: true
logging_steps: 10
save_steps: 500
```

```bash
llamafactory-cli train train_config.yaml
```

### Step 4 — Chat với model sau training

```bash
llamafactory-cli chat \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --adapter_name_or_path outputs/my-model \
  --template qwen \
  --finetuning_type lora
```

### Step 5 — Export / merge LoRA weights

```bash
llamafactory-cli export \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --adapter_name_or_path outputs/my-model \
  --export_dir outputs/merged-model \
  --finetuning_type lora \
  --export_size 4   # số GB mỗi shard
```

### Step 6 — Web UI (không cần code)

```bash
llamafactory-cli webui
# Mở http://localhost:7860
```

## Training approaches được support

| Method | Dùng khi |
|--------|----------|
| SFT (Supervised) | Instruction following, task-specific |
| DPO | Align với human preference (pairwise) |
| PPO | RLHF với reward model |
| ORPO | DPO không cần reference model |
| LoRA | VRAM thấp, chỉ train adapter |
| QLoRA | VRAM rất thấp (4-bit base model) |
| Full fine-tune | Tất cả params, cần GPU lớn |

## Template cho các model phổ biến

```
qwen      → Qwen2/Qwen2.5
llama3    → Llama-3.x
gemma     → Gemma 2/3
mistral   → Mistral/Mixtral
phi       → Phi-3/4
```

## Yêu cầu VRAM (ước tính LoRA)

| Model size | QLoRA | LoRA |
|------------|-------|------|
| 7B | 8GB | 16GB |
| 13B | 12GB | 24GB |
| 70B | 48GB | 80GB+ |
