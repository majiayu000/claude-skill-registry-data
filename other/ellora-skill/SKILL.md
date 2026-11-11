---
name: ellora-skill
description: Fine-tune a language model with a LoRA adapter using the Ellora recipes (codelion/ellora), which generate their own training data instead of needing a labeled dataset. Use when the user wants to fine-tune, train a LoRA or adapter, recover accuracy lost to 4-bit quantization, teach a model step-by-step reasoning or tool calling, extend context for long code repositories, make generated code more secure, add execution awareness (predicting variable states), or go from a one-sentence data description to a fine-tuned model. Covers data generation, training, before/after evaluation and optional publishing, with scripts for CUDA and an MLX route for Apple silicon.
license: Apache-2.0
---

Fine-tune a model for one capability with a LoRA adapter, using a recipe from
[codelion/ellora](https://github.com/codelion/ellora). Every recipe follows the same
shape: the model (or a tool) generates the training data, a LoRA adapter is trained on
it, and the adapter is compared with the base model on held-out data. Seven recipes, each
with a reference file and a script in `scripts/`.

## 1. Pick the recipe

| The user wants to... | Recipe | Method | Notebook base model |
|---|---|---|---|
| Get a 4-bit model's quality back toward full precision | [1: quantization recovery](references/recipe-1-quantization-recovery.md) | Self-distillation, FP16 teacher to NF4 student | Qwen/Qwen3-0.6B |
| Make a model reason step by step in `<think>` tags | [2: reasoning GRPO](references/recipe-2-reasoning-grpo.md) | Self-scored preference pairs, pairwise loss (named GRPO in the repo) | google/gemma-3-1b-it |
| Teach tool or function calling over a codebase | [3: tool calling](references/recipe-3-tool-calling.md) | Scripted scenarios + real tool execution, SFT | meta-llama/Llama-3.2-1B-Instruct (gated) |
| Handle long inputs such as whole repositories | [4: long context](references/recipe-4-long-context.md) | Progressive context curriculum | Qwen2.5-Coder-0.5B-Instruct |
| Write secure code by default | [5: secure code](references/recipe-5-secure-code.md) | Preference pairs scored by Semgrep and regex rules, pairwise loss | Qwen2.5-Coder-0.5B-Instruct |
| Predict how code executes (variable states per line) | [6: execution world model](references/recipe-6-execution-world-model.md) | GRPO on real Python execution traces | Qwen3-4B-Thinking-2507 |
| Fine-tune on a new domain with no dataset yet | [7: invented dataset](references/recipe-7-invented-dataset.md) | Rows invented by DataInventor, SFT | Qwen2.5-1.5B-Instruct |

Open the matching reference before doing anything else. It has the data method, exact
settings, what the notebook measured, the published adapter, and the pitfalls. If no
recipe fits, recipe 7 is the general pattern: describe or collect prompt/completion rows,
train with loss on replies only, evaluate on rows held out from training.

If the user only wants to use an existing Ellora adapter rather than train one, the
reference lists its Hub name; load it with `PeftModel.from_pretrained(base, adapter)`.

## 2. Check the hardware first

State this plainly to the user before starting:

- The notebooks target an NVIDIA GPU (Colab T4 or L4; recipe 4 ran on an H100). Recipes
  1 to 6 load models in 4-bit (bitsandbytes or Unsloth), and some also use vLLM or
  flash-attention.
  None of these run on Apple silicon or CPU as written.
- Recipe 7's PyTorch script runs on CUDA, and on CPU in fp32 (slow).
- On an Apple silicon Mac, use `scripts/recipe_7_mlx.py` (mlx-lm LoRA). It is the only MLX
  route in this skill and the only one smoke-tested on a Mac. For other recipes on a Mac,
  say that they need a CUDA machine (Colab works) rather than improvising a port.
- Check what is already running before starting a long job (`nvidia-smi`, or `ps` for
  python/mlx processes on a Mac). Training competes with any model server on the machine.

Each script prints its options with `--help` and needs no packages for that. The
requirements are listed at the top of each script. Tell the user what is missing and
install only with their OK, into a virtual environment, never globally.

## 3. The shared workflow

1. **Data.** Generate it the recipe's way, or reuse the dataset the notebook published
   (most scripts do this by default; regenerating can take hours). Look at 5 to 10 rows
   before training. Say where the data came from.
2. **Baseline.** Score the base model on the held-out set first, with the same settings
   the adapter will get. Without a baseline there is no result.
3. **Train.** Start small (fewer samples, one epoch) to check that loss falls and memory
   fits, then run the full settings.
4. **Evaluate.** Same held-out data, same decoding settings, base vs adapter. Read some
   generations side by side; metrics like perplexity or ROUGE-L measure closeness to
   reference text, not correctness.
5. **Publish (optional).** Pushing to the Hugging Face Hub happens only with
   `--push-to-hub REPO` and only after the user asks for it and names the repo.

## 4. Ask before

- Downloading model weights or datasets (name the model and its size).
- Sending data to a hosted service (recipe 7's DataInventor app, an LLM judge endpoint).
- Running model-written code. Recipes 3, 5 and 6 execute generated code or tools; run
  them in a container or throwaway environment.
- Pushing anything to the Hub.

## 5. Report

Give the base and adapter numbers side by side on the same held-out data, the model,
sample counts, steps and wall time, and where the adapter was saved. Quote the
notebook's own results only as what that notebook measured, never as an expected
outcome. Name what was not evaluated.

## Files

- `references/recipe-N-*.md`: one per recipe.
- `scripts/recipe_N_*.py`: script versions of the notebooks (CUDA unless stated).
- `scripts/recipe_7_mlx.py`: recipe 7 on Apple silicon with mlx-lm.
