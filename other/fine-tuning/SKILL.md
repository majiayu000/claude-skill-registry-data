---
name: fine-tuning
description: Use when considering fine-tuning a model. Covers when fine-tuning beats prompting or RAG, dataset construction, LoRA and full fine-tuning, evaluation, and the failure modes that waste the effort.
metadata:
  category: ai
  version: 1.0.0
  tags: [fine-tuning, lora, training, dataset, evaluation]
---

# Fine-Tuning

## Purpose

Decide whether fine-tuning is warranted, and do it properly if it is. Most fine-tuning projects should have been prompt engineering or retrieval, and the ones that should be fine-tuning usually fail on dataset quality rather than on the training.

## When to Use

- A task where prompting has plateaued below the required accuracy.
- A specific output format, style, or domain vocabulary the model will not adopt reliably.
- Reducing cost by making a small model do what currently requires a large one.
- Evaluating an existing fine-tuned model that underperforms.

## Capabilities

- Deciding between prompting, RAG, and fine-tuning.
- Dataset construction, curation, and splitting.
- LoRA and QLoRA versus full fine-tuning.
- Hyperparameter selection and overfitting detection.
- Evaluation against the base model on the same set.

## Inputs

- The task, and the accuracy prompting achieves on it.
- Available training data — its volume, and honestly, its quality.
- Latency and cost constraints.

## Outputs

- A justified decision to fine-tune, or not to.
- A curated dataset with clean train/validation/test splits.
- A model measurably better than the base model on a held-out set.

## Workflow

1. **Exhaust prompting first** — Few-shot examples, a clearer output contract, a better model. Fine-tuning cannot teach knowledge the model lacks; it teaches behavior. If the problem is that the model does not *know* something, use retrieval instead.
2. **Decide what fine-tuning is actually for** — Format adherence, tone, a domain-specific classification boundary, or distilling a large model's behavior into a small one. Those are the cases where it works.
3. **Build the dataset carefully** — This is where the project succeeds or fails. A thousand clean, consistent examples beat fifty thousand noisy ones. Inconsistent labels teach the model to be inconsistent.
4. **Split before you look** — Train, validation, test. The test set is touched once, at the end. Selecting a checkpoint on the test set is how you produce a model that scores well and performs badly.
5. **Start with LoRA** — It is cheap, fast, and sufficient for the majority of tasks. Full fine-tuning is warranted rarely.
6. **Compare against the base model on the same test set** — With the same prompt. A fine-tuned model that does not beat a well-prompted base model is a liability, not an asset.

## Best Practices

- Fine-tuning teaches form, not facts. A model fine-tuned on your documentation will produce text that *sounds* like your documentation, with invented details. Use RAG for facts.
- Dataset quality dominates every other factor. Inconsistent labeling in the training set is the most common cause of a fine-tune that underperforms.
- Watch the validation loss. When it rises while training loss falls, you are overfitting — stop, do not train longer.
- A fine-tuned model is a maintenance liability: it must be re-trained when the base model updates, and it is a fixed artifact while prompts are editable in minutes.
- Distillation — fine-tuning a small model on a large model's outputs — is the most reliably valuable use of fine-tuning, because the training data can be generated at scale and is internally consistent by construction.
- Keep the training data. When you need to retrain in a year, reconstructing it will be impossible.

## Examples

**The decision, made honestly:**

```text
Task: classify support tickets into 40 internal categories.

Baseline (prompt only, large model):     71% accuracy
+ 8 few-shot examples:                   79%
+ clarified overlapping category defs:   86%     <- the definitions were the problem
+ RAG over past labeled tickets:         88%
Large model, cost:                       $0.011/ticket, 1.9s latency

Fine-tune (LoRA, small model, 4k examples): 91%
Fine-tuned small model, cost:            $0.0004/ticket, 210ms latency

Decision: FINE-TUNE. Not for the 3-point accuracy gain — that alone would not
justify the maintenance burden. The justification is a 27x cost reduction and
a 9x latency reduction at higher accuracy, on a task running 200,000 times a
month. That is $2,200/month becoming $80/month.

Note that 15 of the original 29 points of improvement came from fixing the
category definitions — free, and available before any training. This is
usually where the gain is.
```

**Dataset construction that will not undermine the training:**

```python
# Consistency is worth more than volume. Two annotators disagreeing on 12% of
# examples means the model learns to be 12% arbitrary.
def audit_dataset(examples: list[Example]) -> DatasetReport:
    return DatasetReport(
        total=len(examples),

        # Near-duplicates inflate the count and cause memorization.
        duplicates=count_near_duplicates(examples, threshold=0.95),

        # Class balance: a category with 4 examples will not be learned.
        per_class=Counter(e.label for e in examples),
        underrepresented=[c for c, n in Counter(e.label for e in examples).items() if n < 30],

        # The critical check: do two annotators agree?
        inter_annotator_agreement=cohens_kappa(annotator_a, annotator_b),

        # Leakage between splits is the most embarrassing failure mode.
        train_test_overlap=count_overlap(train, test),
    )

# Fix before training:
#   kappa < 0.8            -> the labeling guidelines are ambiguous. Fix them and relabel.
#   underrepresented       -> gather more, or merge the category.
#   train_test_overlap > 0 -> the test score is meaningless. Re-split.
```

## Notes

- Cohen's kappa below 0.8 between annotators means the task itself is under-defined. No amount of training will make the model more consistent than its training data.
- LoRA adapters are small (megabytes) and can be swapped at inference. Several task-specific adapters over one base model is usually a better architecture than several fully fine-tuned models.
- The most valuable output of a failed fine-tuning project is usually the evaluation set that was built for it. Keep it — it makes every subsequent prompt change measurable.
