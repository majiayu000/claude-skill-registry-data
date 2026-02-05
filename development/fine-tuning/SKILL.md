---
name: fine-tuning
description: LLM fine-tuning and prompt-tuning techniques
sasmp_version: "1.3.0"
bonded_agent: 05-prompt-optimization-agent
bond_type: PRIMARY_BOND
---

# Fine-Tuning Skill

**Bonded to:** `prompt-optimization-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:fine-tuning")
```

---

## Parameter Schema

```yaml
parameters:
  tuning_method:
    type: enum
    values: [full, lora, qlora, prompt_tuning, prefix_tuning]
    default: lora

  dataset_size:
    type: enum
    values: [small, medium, large]
    description: "<1k, 1k-10k, >10k examples"

  compute_budget:
    type: enum
    values: [low, medium, high]
    default: medium
```

---

## Tuning Methods Comparison

| Method | Parameters | Compute | Quality | Best For |
|--------|-----------|---------|---------|----------|
| Full Fine-tune | All | Very High | Highest | Maximum customization |
| LoRA | ~0.1% | Low | High | Resource-constrained |
| QLoRA | ~0.1% | Very Low | Good | Consumer GPUs |
| Prompt Tuning | <0.01% | Minimal | Good | Simple tasks |
| Prefix Tuning | ~0.1% | Low | Good | Generation tasks |

---

## Dataset Preparation

### Format Templates

```yaml
formats:
  instruction:
    template: |
      ### Instruction
      {instruction}

      ### Response
      {response}

  chat:
    template: |
      <|user|>
      {user_message}
      <|assistant|>
      {assistant_response}

  completion:
    template: "{input}{output}"
```

### Quality Criteria

```yaml
quality_checklist:
  - [ ] No duplicate examples
  - [ ] Consistent formatting
  - [ ] Diverse examples
  - [ ] Balanced categories
  - [ ] High-quality outputs
  - [ ] No harmful content
```

---

## Training Configuration

```yaml
training_config:
  hyperparameters:
    learning_rate: 2e-5
    batch_size: 8
    epochs: 3
    warmup_ratio: 0.1

  lora_config:
    r: 16
    alpha: 32
    dropout: 0.05
    target_modules: ["q_proj", "v_proj"]

  evaluation:
    eval_steps: 100
    save_steps: 500
    metric: loss
```

---

## Evaluation Framework

| Metric | Purpose | Target |
|--------|---------|--------|
| Loss | Training progress | Decreasing |
| Accuracy | Task performance | >90% |
| Perplexity | Model confidence | <10 |
| Human eval | Quality assessment | Preferred >80% |

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Overfitting | Small dataset | Add regularization |
| Underfitting | Low epochs | Increase training |
| Catastrophic forgetting | Aggressive tuning | Lower learning rate |
| Poor generalization | Data bias | Diversify dataset |

---

## References

See: Hugging Face PEFT, OpenAI Fine-tuning Guide
