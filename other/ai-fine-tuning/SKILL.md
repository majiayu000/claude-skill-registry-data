---
name: ai-fine-tuning
description: Fine-tune models on your data to maximize quality and cut costs. Use when prompt optimization hit a ceiling, you need domain specialization, you want cheaper models to match expensive ones, you heard fine-tuning will make us AI-native, you have 500+ training examples, or you need to train on proprietary data. Also use when you have spent weeks of manual iteration with no systematic improvement path, or manual prompt tuning got you to a working system but quality plateaued. Covers DSPy BootstrapFinetune, BetterTogether, model distillation, and when to fine-tune vs optimize prompts, LoRA vs full fine-tune, when to fine-tune vs few-shot, distill GPT-4 into a smaller model, teacher-student model training, custom model training with DSPy, model distillation, make a cheap model as good as GPT-4.
---

# Fine-Tune Models on Your Data

Guide the user through deciding whether to fine-tune, preparing data, running fine-tuning with DSPy, distilling to cheaper models, and deploying. Fine-tuning is powerful but expensive — always confirm prerequisites first.

## Should you fine-tune?

Before writing any code, walk through these questions with the user:

1. **Have you optimized prompts first?** If not, use `/ai-improving-accuracy` — prompt optimization is 10x cheaper and often sufficient.
2. **Do you have 500+ labeled examples?** Fine-tuning with less data usually overfits. Collect more data first.
3. **Is your baseline accuracy above 50%?** If your prompt-optimized program is below 50%, your task definition or data has problems. Fix those first.
4. **What's the goal — quality or cost?**
   - **Quality**: You've maxed out prompt optimization and need more accuracy
   - **Cost**: You want a small cheap model to match an expensive one

### When to fine-tune

- You've already optimized prompts with MIPROv2 and hit a ceiling
- You have 500+ labeled examples (1000+ is better)
- Your baseline is >50% and you need to push higher
- You want to distill an expensive model into a cheaper one (10-50x cost savings)
- Your domain has specialized vocabulary or patterns the base model doesn't know
- You need faster inference (smaller fine-tuned models are faster)

### When NOT to fine-tune

- You haven't tried prompt optimization yet — start with `/ai-improving-accuracy`
- You have fewer than 500 examples — need more data? Use `/ai-generating-data` to bootstrap synthetic examples, or use BootstrapFewShot or MIPROv2 instead
- Your baseline is below 50% — your data or task definition needs work
- You're still iterating on what the task is — fine-tuning locks you in
- You don't have a clear metric — you can't evaluate fine-tuning without one
- Your use case changes frequently — fine-tuned models don't adapt to new instructions easily

## Prerequisites checklist

Before starting, confirm:

- [ ] **Data**: 500+ labeled examples (1000+ recommended), split 80/10/10 (train/dev/test)
- [ ] **Baseline**: Prompt-optimized program with measured accuracy (use `/ai-improving-accuracy`)
- [ ] **Metric**: Clear, automated metric that scores predictions
- [ ] **Compute**: API access (OpenAI fine-tuning API) or local GPUs (for open-source models)
- [ ] **Budget**: OpenAI fine-tuning costs ~$0.008/1K tokens for GPT-4o-mini; local needs 1+ GPU

## Step 1: Prepare your data and baseline

### Build a strong baseline first

Always compare fine-tuning against a prompt-optimized baseline:

```python
import dspy

lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# Define your program
class Classify(dspy.Signature):
    """Classify the support ticket."""
    text: str = dspy.InputField()
    category: str = dspy.OutputField()

program = dspy.ChainOfThought(Classify)

# Prepare data
import json
with open("labeled_data.json") as f:
    data = json.load(f)

examples = [dspy.Example(text=x["text"], category=x["category"]).with_inputs("text") for x in data]

# Split: 80% train, 10% dev, 10% test
n = len(examples)
trainset = examples[:int(n * 0.8)]
devset = examples[int(n * 0.8):int(n * 0.9)]
testset = examples[int(n * 0.9):]

# Measure baseline
def metric(example, prediction, trace=None):
    return prediction.category.lower() == example.category.lower()

from dspy.evaluate import Evaluate
evaluator = Evaluate(devset=devset, metric=metric, num_threads=4, display_progress=True)
baseline_score = evaluator(program)
print(f"Baseline: {baseline_score:.1f}%")
```

### Optimize prompts first (your comparison point)

```python
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
prompt_optimized = optimizer.compile(program, trainset=trainset)
prompt_score = evaluator(prompt_optimized)
print(f"Prompt-optimized: {prompt_score:.1f}%")
```

If prompt optimization gets you to your quality goal, stop here. Fine-tuning is only worth it if you need to go further.

## Step 2: BootstrapFinetune (core fine-tuning)

The main fine-tuning workflow in DSPy. It bootstraps successful reasoning traces from your training data, filters them by your metric, and fine-tunes the model weights.

```python
optimizer = dspy.BootstrapFinetune(metric=metric, num_threads=24)
finetuned = optimizer.compile(program, trainset=trainset)

# Evaluate the fine-tuned model
finetuned_score = evaluator(finetuned)
print(f"Baseline:         {baseline_score:.1f}%")
print(f"Prompt-optimized: {prompt_score:.1f}%")
print(f"Fine-tuned:       {finetuned_score:.1f}%")
```

### How it works

1. **Bootstrap traces**: Runs your program on each training example, keeping traces where the metric passes
2. **Filter by metric**: Only successful traces become training data
3. **Fine-tune weights**: Sends traces to the model provider's fine-tuning API
4. **Return optimized program**: The program now uses the fine-tuned model

### Requirements

- A fine-tunable model (OpenAI `gpt-4o-mini`, `gpt-4o`; or local open-source models)
- 500+ training examples (more traces bootstrapped = better fine-tuning)
- A metric that reliably identifies good outputs

## Step 3: Model distillation (expensive to cheap)

Train a small, cheap model to mimic an expensive model. This is the biggest cost saver — 10-50x reduction with 85-95% quality retention.

### Teacher-student pattern

```python
# Step 1: Teacher — expensive model, high quality
teacher_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=teacher_lm)

# Build and optimize the teacher
teacher = dspy.ChainOfThought(Classify)
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
teacher_optimized = optimizer.compile(teacher, trainset=trainset)

teacher_score = evaluator(teacher_optimized)
print(f"Teacher (GPT-4o): {teacher_score:.1f}%")

# Step 2: Student — fine-tune cheap model on teacher's outputs
student_lm = dspy.LM("openai/gpt-4o-mini")  # or another fine-tunable model
dspy.configure(lm=student_lm)

student = dspy.ChainOfThought(Classify)
ft_optimizer = dspy.BootstrapFinetune(metric=metric, num_threads=24)
student_finetuned = ft_optimizer.compile(student, trainset=trainset, teacher=teacher_optimized)

student_score = evaluator(student_finetuned)
print(f"Student (GPT-4o-mini, fine-tuned): {student_score:.1f}%")
```

### Typical results

| Model | Quality | Cost per 1M tokens |
|-------|---------|-------------------|
| GPT-4o (teacher) | 85% | ~$5.00 |
| GPT-4o-mini (no tuning) | 70% | ~$0.15 |
| GPT-4o-mini (fine-tuned) | 81% | ~$0.15 |

The fine-tuned student costs 33x less and retains ~95% of teacher quality.

**Small models can dramatically outperform frontier models on narrow tasks.** In a Yale project parsing 3.6M historical names, GPT-4 and Gemini achieved ~70% accuracy. Fine-tuned Qwen models (0.8B-4B parameters) hit 94-96% — beating frontier models by 25+ points while running locally. The key insight: for well-defined extraction tasks with enough training data (500K+ synthetic examples), tiny fine-tuned models dominate.

## Step 4: BetterTogether (maximum quality)

BetterTogether alternates between prompt optimization and weight optimization, getting more out of both. Based on the BetterTogether paper (arXiv 2407.10930v2), this approach yields 5-78% gains over either technique alone.

```python
optimizer = dspy.BetterTogether(
    metric=metric,
    p=dspy.MIPROv2(metric=metric),
    w=dspy.BootstrapFinetune(metric=metric),
)
best = optimizer.compile(program, trainset=trainset, strategy="p -> w -> p")

best_score = evaluator(best)
print(f"Prompt-only:    {prompt_score:.1f}%")
print(f"Fine-tune-only: {finetuned_score:.1f}%")
print(f"BetterTogether: {best_score:.1f}%")
```

### How it works

The strategy string `"p -> w -> p"` controls the sequence — `p` maps to MIPROv2 (prompt optimizer) and `w` maps to BootstrapFinetune (weight optimizer):

1. **Round 1 (p)**: Optimize prompts (instructions + few-shot examples)
2. **Round 2 (w)**: Fine-tune weights using the optimized prompts
3. **Round 3 (p)**: Re-optimize prompts for the fine-tuned model
4. Each round builds on the previous, creating synergy between prompt and weight optimization

If you omit the optimizer kwargs, BetterTogether defaults to `p=BootstrapFewShotWithRandomSearch` and `w=BootstrapFinetune`.

### When to use BetterTogether

- You want the absolute best quality and have the compute budget
- Fine-tuning alone didn't close the gap to your quality target
- You have 500+ examples and a reliable metric

## Step 5: Evaluate and deploy

### Thorough evaluation

Always evaluate on the held-out **test set** (not dev set):

```python
test_evaluator = Evaluate(devset=testset, metric=metric, num_threads=4, display_progress=True)

print(f"Test set results:")
print(f"  Baseline:         {test_evaluator(program):.1f}%")
print(f"  Prompt-optimized: {test_evaluator(prompt_optimized):.1f}%")
print(f"  Fine-tuned:       {test_evaluator(finetuned):.1f}%")
```

### Save and load for production

```python
# Save
finetuned.save("finetuned_program.json")

# Load later
from my_module import MyProgram
production = MyProgram()
production.load("finetuned_program.json")
result = production(text="New support ticket...")
```

## When fine-tuning goes wrong

### Can't bootstrap enough traces

If the base model fails on most training examples, there aren't enough successful traces to fine-tune on.

**Fixes:**
- Use a stronger model for bootstrapping (GPT-4o instead of GPT-4o-mini)
- Relax your metric during bootstrapping (accept partial credit)
- Simplify your task (break multi-step into single steps)

### Output format errors from small models

Small fine-tuned models (<4B params) often produce JSON syntax errors — unclosed braces, missing quotes, trailing commas. Switch to YAML output format during fine-tuning to eliminate these entirely. YAML is more forgiving to generate and parses reliably from small models.

### Model overfits (high train accuracy, low test accuracy)

**Fixes:**
- Add more training data
- Reduce fine-tuning epochs (if provider allows)
- Use a larger base model (less prone to overfitting)
- Simplify your output format

### Fine-tuning didn't improve over prompt optimization

**Fixes:**
- Check that bootstrapping produced enough successful traces (need 200+)
- Try BetterTogether instead of BootstrapFinetune alone
- Verify your metric actually correlates with quality
- Try a different base model

## Infrastructure choices

### OpenAI API (easiest)

Works with `gpt-4o-mini` and `gpt-4o`. DSPy handles the fine-tuning API calls automatically:

```python
lm = dspy.LM("openai/gpt-4o-mini")  # or any fine-tunable model via API
```

- Pros: No GPU needed, simple setup, fast
- Cons: Data sent to OpenAI, ongoing per-token costs, limited model choices

### Local fine-tuning (own your model)

For open-source models (Llama, Mistral, etc.) using LoRA/QLoRA:

```python
lm = dspy.LM("together_ai/meta-llama/Llama-3-70b-chat-hf")
```

- Pros: Data stays private, no per-token costs after training, full control
- Cons: Needs GPU(s), more setup, slower iteration

### Cloud GPU platforms

AWS SageMaker, Google Cloud, Lambda Labs, or Together AI for training:

- Pros: Scalable, no hardware to manage
- Cons: Costs vary, setup per platform

## Gotchas

- **Skipping prompt optimization and jumping straight to fine-tuning.** Claude defaults to recommending fine-tuning when users mention quality issues. Always confirm the user has run MIPROv2 or similar prompt optimization first — fine-tuning without a prompt-optimized baseline wastes compute and makes it impossible to measure whether fine-tuning actually helped.
- **Using the dev set for final evaluation.** Claude often evaluates the fine-tuned model on the same dev set used during optimization. Always evaluate on a held-out test set that was never seen during training or prompt optimization. Report both dev and test scores so the user can spot overfitting.
- **Passing `teacher=` without an optimized teacher program.** When using `BootstrapFinetune` for distillation, Claude sometimes passes the unoptimized base program as the teacher. The teacher must be the prompt-optimized version — otherwise the student learns from mediocre traces and fine-tuning underperforms.
- **Forgetting that `BootstrapFinetune` needs a fine-tunable model.** Not all models support fine-tuning via API. Claude sometimes configures `dspy.LM("anthropic/claude-sonnet-4-5-20250929")` for `BootstrapFinetune`, but Anthropic does not offer a fine-tuning API. Use OpenAI models or local open-source models for weight optimization.
- **Not checking how many traces were bootstrapped.** If bootstrapping only produces 50 successful traces from 1000 examples, the fine-tuning data is too small. Check the bootstrap log output and aim for 200+ successful traces. If too few succeed, use a stronger teacher model or relax the metric.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Build a strong baseline before fine-tuning — see `/ai-improving-accuracy`
- BootstrapFinetune API details — see `/dspy-bootstrap-finetune`
- BetterTogether optimizer — see `/dspy-better-together`
- Cost reduction beyond distillation — see `/ai-cutting-costs`
- Generate synthetic training data — see `/ai-generating-data`
- Fix fine-tuning or evaluation errors — see `/ai-fixing-errors`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (classification, distillation, BetterTogether), see [examples.md](examples.md)
- For BootstrapFinetune, BetterTogether, and MIPROv2 API details, see [reference.md](reference.md)
