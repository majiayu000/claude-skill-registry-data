---
name: heretic
description: Heretic — automatic censorship removal (abliteration) for local LLMs via transformer weight manipulation. Removes refusal behavior from open-source models by identifying and nullifying refusal directions in residual stream.
triggers:
  - "abliterate model"
  - "remove censorship llm"
  - "uncensor model"
  - "heretic"
  - "model abliteration"
  - "remove refusal"
  - "fine tune refusal"
  - "model weight manipulation"
linksTo:
  - "ml-ops"
  - "python"
---

# Heretic — LLM Abliteration

> Fully automatic censorship removal for local language models via weight editing.
> Source: https://github.com/p-e-w/heretic | Stars: 11K+

## What It Does

Heretic removes refusal behavior from transformer models by:
1. Running the model on paired harmful/harmless prompts
2. Extracting the "refusal direction" from the residual stream
3. Projecting out that direction from specific weight matrices
4. Saving a modified model that no longer refuses on principle

**Result**: A model that responds to any prompt without safety-trained refusals.
**Note**: For research, red teaming, and local use only. Not for production deployment.

## Requirements

```bash
pip install heretic-abliterate
# or
pip install git+https://github.com/p-e-w/heretic
```

- Python 3.10+
- PyTorch with CUDA/MPS support
- HuggingFace Transformers
- Sufficient VRAM (depends on model size)

## Usage

```python
from heretic import abliterate

# Automatic abliteration
abliterate(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    output_dir="./mistral-7b-abliterated",
    # Optional: customize the layer range
    layer_fraction_start=0.2,
    layer_fraction_end=0.8,
)
```

**CLI:**
```bash
python -m heretic \
  --model "meta-llama/Llama-3.1-8B-Instruct" \
  --output ./llama-3.1-8b-abliterated \
  --device cuda
```

## How Abliteration Works

```
1. Generate activations on ~100 harmful + harmless prompt pairs
2. Compute mean difference = "refusal direction" vector
3. For each weight matrix W in target layers:
   W' = W - (W @ r @ r.T)  where r = refusal direction
4. Save modified model weights
```

The key insight: safety-trained models encode "should I refuse?" as a linear direction in representation space. Removing this direction removes the refusal behavior without degrading other capabilities.

## Use Cases

- **Red teaming**: Test what an unconstrained model produces to understand attack surfaces
- **Research**: Study how safety training affects model capabilities
- **Local inference**: Run unrestricted models for legitimate research tasks
- **Baseline comparison**: Compare restricted vs unrestricted outputs for safety research

## Integration with Promptfoo

After abliterating a model, use `promptfoo` to test the original vs abliterated behavior:

```yaml
targets:
  - id: huggingface:mistralai/Mistral-7B-Instruct-v0.3
    label: "original"
  - id: huggingface:./mistral-7b-abliterated
    label: "abliterated"

redteam:
  plugins:
    - harmful:hate
    - jailbreak
```

## Safety Considerations

- Only use on models you have rights to modify
- Do not deploy abliterated models in public-facing applications
- Abliteration removes safety filters but does NOT improve model accuracy
- Some models are more resistant than others (depends on training approach)
