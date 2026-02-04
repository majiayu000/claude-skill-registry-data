---
name: finetune-train
description: Use when training a fine-tuned model and evaluating improvement over base model. Triggers - have filtered training data, ready to submit training job, need to convert to GGUF. Requires finetune-generate first.
---

# Fine-tune Train

Train the model and verify improvement over base model.

## Prerequisites

Complete [finetune-generate](../finetune-generate/SKILL.md) first. You need:

- [ ] `training_data.jsonl` — Filtered, validated training examples
- [ ] Model choice from finetune-design
- [ ] Evaluation rubric (for comparing base vs fine-tuned)

## Scope: SFT Only

This skill covers **Supervised Fine-Tuning (SFT)** only. Other training methods (DPO, GRPO, GEPA) will hopefully be added in the future.

## Related HuggingFace Skills

Use these HuggingFace skills for an integrated workflow:

| Skill | When to Use |
|-------|-------------|
| `model-trainer` | **Primary training skill** — Trackio integration, TRL patterns, HF Jobs submission |
| `hugging-face-dataset-creator` | Push/manage datasets on HF Hub |
| `hugging-face-evaluation-manager` | Add eval results to model cards after training |

## Outputs

By the end of this phase, you will have:

- [ ] Fine-tuned model (adapter on HuggingFace Hub)
- [ ] Merged GGUF file for local deployment
- [ ] GGUF uploaded to HuggingFace Hub (for others to download)
- [ ] `evaluation_report.md` — Statistical comparison of base vs fine-tuned

---

## Workflow

### Step 1: Dataset Preparation

Format and upload your training data:

1. **Verify format** matches training framework expectations:
   ```json
   {"messages": [
     {"role": "system", "content": "..."},
     {"role": "user", "content": "..."},
     {"role": "assistant", "content": "..."}
   ]}
   ```

2. **Push to HuggingFace Hub** using the datasets library:
   ```python
   from datasets import Dataset
   import json

   # Load your JSONL
   examples = [json.loads(line) for line in open("training_data.jsonl")]

   # Keep only the messages field for training
   training_data = [{"messages": ex["messages"]} for ex in examples]

   # Push to Hub
   dataset = Dataset.from_list(training_data)
   dataset.push_to_hub("username/dataset-name", private=True)
   ```

3. **Verify access** — test loading the dataset before submitting training job:
   ```python
   from datasets import load_dataset
   ds = load_dataset("username/dataset-name", split="train")
   print(f"Loaded {len(ds)} examples")
   ```

**Optional:** Use `hugging-face-dataset-creator` skill for streamlined HF Hub dataset management.

**Gate:** Dataset uploaded and accessible

---

### Step 2: Choose Training Approach

| Approach | Best For |
|----------|----------|
| **HuggingFace Jobs** | Fast iteration, serverless GPU, minimal setup |
| **MLX Local** | Apple Silicon, no cloud dependency |
| **Cloud GPU** | Full control, large jobs |

**HuggingFace Jobs** is recommended for most projects.

Also consider Thinking Machines.

**Reference:** [training-guide.md](training-guide.md)

---

### Step 3: Select GPU Based on Context Length

**Critical: Vocabulary size dominates memory at long contexts.**

Logits are computed in FP32 regardless of quantization:
- Formula: `vocab_size × sequence_length × 4 bytes`

| Model | Vocab Size | Logits @ 16k tokens | GPU Required |
|-------|-----------|---------------------|--------------|
| **Gemma 3 12B** | 262K | ~17 GB | **A100** |
| **Qwen3 14B** | 152K | ~10 GB | **A100** |
| **Llama 3 8B** | 128K | ~8 GB | A10G or A100 |

**GPU Selection Guide:**

| Context Length | Gemma 3 (262K vocab) | Qwen3 (152K vocab) | Llama 3 (128K vocab) |
|---------------|----------------------|--------------------|-----------------------|
| 2048 tokens | A10G (24GB) | A10G (24GB) | A10G (24GB) |
| 8192 tokens | A100 (80GB) | A10G (24GB) | A10G (24GB) |
| 16384 tokens | **A100 (80GB)** | **A100 (80GB)** | A100 (80GB) |

**Rule of thumb:** If your conversations average 8k+ tokens and you're using Gemma 3, use A100.

---

### Step 4: Configure Training

**QLoRA parameters (typical):**
```python
peft_config = LoraConfig(
    r=64,
    lora_alpha=128,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
```

**Training hyperparameters with Trackio:**
```python
config = SFTConfig(
    output_dir="model-name",
    push_to_hub=True,
    hub_model_id="username/model-name",
    hub_strategy="every_save",  # Push checkpoints

    # Quantization
    model_init_kwargs={
        "load_in_4bit": True,
        "bnb_4bit_quant_type": "nf4",
        "bnb_4bit_compute_dtype": torch.bfloat16,
        "bnb_4bit_use_double_quant": True,
        "device_map": "auto",
    },

    # Training
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    max_length=16384,  # Adjust based on GPU (see Step 3)
    bf16=True,
    gradient_checkpointing=True,
    optim="adamw_8bit",

    # Logging & checkpointing
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=2,

    # Trackio monitoring (RECOMMENDED)
    report_to="trackio",
)
```

**Reference:** [training-guide.md#configuration](training-guide.md#configuration)

---

### Step 5: Submit Training

**Use `hf jobs uv run` CLI:**

```bash
# CRITICAL: Flags MUST come BEFORE script path
hf jobs uv run \
    --flavor a100-large \
    --timeout 6h \
    --secrets HF_TOKEN \
    scripts/train_model.py
```

**Common mistakes:**
```bash
# ❌ WRONG: flags after script (will be ignored!)
hf jobs uv run train.py --flavor a100-large

# ❌ WRONG: --secret (singular) instead of --secrets (plural)
hf jobs uv run --secret HF_TOKEN train.py

# ✅ CORRECT: flags before script
hf jobs uv run --flavor a100-large --secrets HF_TOKEN train.py
```

**Monitor training:**
```bash
hf jobs ps                    # List jobs
hf jobs logs <job_id>         # View logs
hf jobs inspect <job_id>      # Job details
```

**Trackio dashboard:** `https://huggingface.co/spaces/username/trackio`

**Reference:** [training-guide.md#hf-jobs](training-guide.md#hf-jobs)

---

### Step 6: GGUF Conversion & Upload

Convert the fine-tuned adapter to GGUF and optionally upload to Hub.

**Memory requirements:** Merging requires ~28GB RAM for 14B model (bfloat16).

**Manual Workflow (Recommended for macOS):**
```bash
# 1. Clone llama.cpp (NOT Homebrew - version mismatch issues)
git clone https://github.com/ggerganov/llama.cpp ~/llama.cpp
pip install -r ~/llama.cpp/requirements.txt

# 2. Download base model (resumable)
hf download Qwen/Qwen3-14B --local-dir ~/models/qwen3-14b-base

# 3. Download adapter
hf download username/my-finetuned-qwen3-14b --local-dir ./models/qwen3-finetuned/adapter

# 4. Merge adapter (bfloat16, ~28GB RAM)
uv run python scripts/merge_lora_adapter.py \
    --base-model ~/models/qwen3-14b-base \
    --adapter-path ./models/qwen3-finetuned/adapter \
    --output-dir ./models/qwen3-finetuned/merged

# 5. Convert to GGUF
uv run python ~/llama.cpp/convert_hf_to_gguf.py \
    --outtype bf16 \
    --outfile ./models/qwen3-finetuned/model-bf16.gguf \
    ./models/qwen3-finetuned/merged

# 6. Quantize (Homebrew llama-quantize works)
llama-quantize \
    ./models/qwen3-finetuned/model-bf16.gguf \
    ./models/qwen3-finetuned/model-q4_k_m.gguf \
    Q4_K_M
```

**Automated Script (Alternative):**
```bash
uv run python scripts/convert_to_gguf.py \
    --adapter-repo username/my-finetuned-qwen3-14b \
    --base-model Qwen/Qwen3-14B \
    --output-dir ./models/qwen3-finetuned \
    --upload
```

**Test locally:**
```bash
llama-server -m ./models/qwen3-finetuned/model-q4_k_m.gguf --port 8080 -ngl 99
```

**Reference:** [training-guide.md#gguf-conversion](training-guide.md#gguf-conversion)

---

### Step 7: Evaluation

Compare fine-tuned model against base model using pairwise full-conversation assessment.

**Evaluation methodology:**
1. Generate NEW personas using seeds not in training data (e.g., seeds 9000+)
2. Run BOTH models on the same personas with the same user simulator
3. Assess all conversations with your rubric (same assessor, same criteria)
4. Compare scores pairwise using statistical test (paired t-test)

**Why this methodology:**
- **New seeds:** Prevents evaluation on training distribution — tests generalization
- **Pairwise comparison:** Same persona + same user simulator = controlled comparison
- **Full conversations:** Tests multi-turn dynamics, not just single-turn quality

**Multi-Model Comparison Workflow:**

```bash
# Step 1: Generate evaluation personas (uses seeds 9000+, not in training)
uv run python scripts/generate_eval_personas.py --count 15
# Output: data/eval/personas.json

# Step 2: Start model servers on different ports
# Terminal 1: Baseline
llama-server -m gemma-3-12b-it.gguf --port 8080 -ngl 99
# Terminal 2: Fine-tuned Gemma
llama-server -m finetuned-gemma.gguf --port 8081 -ngl 99
# Terminal 3: Fine-tuned Qwen (if comparing multiple)
llama-server -m finetuned-qwen.gguf --port 8082 -ngl 99

# Step 3: Run evaluation
uv run python scripts/run_model_evaluation.py \
    --personas data/eval/personas.json \
    --output-dir data/eval/results

# Step 4: Review report at data/eval/results/evaluation_report.md
```

**Evaluation scripts:**

| Script | Purpose |
|--------|---------|
| `scripts/generate_eval_personas.py` | Generate NEW personas for evaluation |
| `scripts/run_model_evaluation.py` | Run multi-model comparison with statistical tests |
| `scripts/merge_lora_adapter.py` | Merge LoRA adapter with base model (bfloat16) |
| `scripts/convert_to_gguf.py` | End-to-end: download, merge, convert, upload |

**Success criteria:**
- **Improvement:** ≥10% absolute improvement over baseline
- **Significance:** p < 0.05 (paired t-test)
- **Safety:** No regressions on safety criteria

**Statistical comparison:**
```python
from scipy import stats
import numpy as np

# Paired t-test (same personas, same user simulator)
t_stat, p_value = stats.ttest_rel(finetuned_scores, base_scores)
improvement = np.mean(finetuned_scores) - np.mean(base_scores)
```

**Reference:** [training-guide.md#evaluation](training-guide.md#evaluation)

**Optional:** Use `hugging-face-evaluation-manager` skill to add evaluation results to your model card on HF Hub.

---

### Step 8: Sanity Checks

Before declaring success, verify:

| Check | Purpose |
|-------|---------|
| Perplexity on held-out set | Did training actually work? |
| Small human eval (5-10 convos) | Does LLM-as-judge agree with humans? |
| Capability regression test | Didn't break general abilities |
| Safety regression | No new harmful patterns |

**Warning signs:**
- Fine-tuned worse than base → Training issue, check data quality
- Huge improvement (>30%) → Suspiciously high, verify evaluation
- Safety regressions → Do not deploy

---

## Decision: Ship or Iterate?

| Result | Action |
|--------|--------|
| ≥10% improvement, p<0.05, no regressions | Ship it |
| <10% improvement | Consider more/better training data |
| Not significant (p>0.05) | More evaluation data or training data |
| Safety regressions | Do not deploy, investigate |

### Red Flags: Rationalizations to Resist

| Rationalization | Reality |
|-----------------|---------|
| "Perplexity improved, we're done" | Low perplexity ≠ good conversations. Full-conversation eval required. |
| "It feels better, ship it" | Feelings aren't evidence. Run statistical comparison (p<0.05). |
| "Default hyperparameters are fine" | Large-vocab models (Gemma 3) OOM with defaults. Check max_length and GPU. |
| "Skip GGUF, we'll deploy later" | GGUF conversion is the deployment. Test locally before declaring success. |
| "Safety check is paranoid" | Fine-tuning can introduce regressions. Safety audit is mandatory. |
| "A10G is fine for everything" | Gemma 3 with 16k context needs A100 due to 262K vocabulary. |

---

## Model Naming Conventions

Different model families use different naming conventions for instruction-tuned variants:

| Family | Base Model | Instruction-Tuned |
|--------|-----------|-------------------|
| **Gemma 3** | `google/gemma-3-12b` | `google/gemma-3-12b-it` (add `-it`) |
| **Qwen3** | `Qwen/Qwen3-14B-Base` | `Qwen/Qwen3-14B` (base has `-Base` suffix) |
| **Llama 3** | `meta-llama/Llama-3-8B` | `meta-llama/Llama-3-8B-Instruct` |

**For SFT fine-tuning, always use the instruction-tuned variant** to preserve instruction-following capabilities.

---

## Done When

- [ ] Training completed successfully
- [ ] GGUF converted and tested locally
- [ ] GGUF uploaded to HuggingFace Hub
- [ ] Evaluation shows significant improvement (≥10%, p<0.05)
- [ ] No safety regressions
- [ ] `evaluation_report.md` documents results

---

## Resources

| Resource | What It Contains |
|----------|------------------|
| [training-guide.md](training-guide.md) | Complete training guide with Trackio, CLI syntax, troubleshooting |
| [code/SETUP-REFERENCE.md](../code/SETUP-REFERENCE.md) | Project structure, script templates |
| [code/infrastructure.py](../code/infrastructure.py) | Copy-paste ready: token counting, slice generation |
| [examples/therapy-domain.md](../examples/therapy-domain.md) | Complete therapy example: evaluation results, model choice |

**HuggingFace Hub integration (skills):**
| Skill | Use For |
|-------|---------|
| `model-trainer` | Primary HF training skill with Trackio, TRL patterns |
| `hugging-face-dataset-creator` | Push/manage datasets on HF Hub |
| `hugging-face-evaluation-manager` | Add eval results to model cards |

---

## What's Next?

After successful fine-tuning:
- Deploy model locally (Ollama, llama.cpp)
- Monitor real-world usage for issues
- Collect feedback for future iterations
- Consider DPO/RLHF if further refinement needed
