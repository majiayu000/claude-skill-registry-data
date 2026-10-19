---
name: dataset-quality
description: Audit, clean and document datasets used for training, fine-tuning, evaluation or analytics - schema and null checks, exact and near-duplicate detection, label consistency and noise, class imbalance, train/validation/test leakage, PII and licence screening, split design, and dataset cards, with Hugging Face datasets (5.x) and plain Python/pandas examples. Use when preparing or inheriting a dataset, a model's eval score looks too good, labels disagree, or before publishing or training on data. Not for CSV mechanics (csv-data-processing), spreadsheet work (xlsx-processing), model/prompt evaluation (llm-evaluation), retrieval evaluation (rag-evaluation), or database design (postgresql-development).
compatibility: Python 3.10+. Bundled script uses only the standard library. Hugging Face datasets 5.1.0 (PyPI, checked 2026-10-15) and pandas are optional. Network access is needed only to download public data the user names.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "datasets, data-quality, deduplication, data-leakage, labels, huggingface-datasets, pii"
  topics: "machine-learning, data-engineering, evaluation"
---

# Dataset Quality

A model or analysis is only as trustworthy as the data it saw and the data it was judged on. The most expensive failures are silent: duplicates across train and test, labels that contradict each other, a split that leaks the answer, personal data in a corpus you are about to publish. Measure first, then clean with a log of what you removed and why.

## Scope and boundaries

- This skill: data inspection, cleaning decisions, splitting, documentation.
- `csv-data-processing` / `xlsx-processing`: file format handling. `llm-evaluation`: how to score model outputs on a clean eval set. `rag-evaluation`: retrieval/answer scoring. `postgresql-development` / `database-migrations`: data in relational stores.

## Non-negotiable rules

1. **Never modify the source data in place.** Write cleaned output to a new path/version; keep a removal log (row id, reason).
2. **Screen for personal and secret data before sharing, uploading or sending to any third-party API** (including hosted LLM judges). Do not paste raw rows containing PII into chat or tools; show counts and row ids. Do not run `push_to_hub`, upload, or publish without explicit user authorization.
3. **Do not execute code that ships with a downloaded dataset.** Prefer data-only formats (Parquet, JSONL, CSV). Recent `datasets` releases dropped dataset-script loading and `trust_remote_code`; if an older script-based dataset is required, read the script first and ask the user.
4. **Check the licence and terms** before training or redistributing; record it. "Publicly accessible" is not "permissively licensed". Scraped, user-generated or medical/financial data may carry consent and legal constraints.
5. **Split before any fitting, tuning or feature statistics** (normalisation, vocabulary, target encoding). Group-aware splits when rows are not independent.
6. **Report evidence, not impressions**: counts, rates, row ids, and which check produced them.

## Workflow

### 1. Define the unit and the purpose
What is one row (document, user, conversation, image)? What is the target/label? What will the data be used for (train, validate, final test, analytics)? Purpose decides how strict each check is: a test set must be small, clean and frozen; a pre-training corpus tolerates more noise but not leakage of the test set.

### 2. Structural audit
- Parse errors, wrong types, missing/empty required fields, encoding problems (mojibake, replacement characters), stray control characters.
- Schema drift across files/shards. Mixed units or timestamp time zones.
- Distribution of lengths, categories and dates; implausible values (negative ages, future dates, constant columns).

Bundled stdlib script for JSONL (read-only):
```bash
python3 -I scripts/audit_jsonl.py train.jsonl --text-field text --label-field label \
        --require id,text,label --compare test.jsonl
```
It reports unparseable or non-object lines (`unparseable_or_non_object`), missing fields, exact duplicates after case/whitespace normalisation, label distribution, identical texts with conflicting labels, length outliers (4 sd rule; it cannot fire for 17 or fewer rows), and exact overlap with another file; `--compare` row numbers refer to the primary file. See [scripts/audit_jsonl.py](scripts/audit_jsonl.py).

Equivalent with Hugging Face `datasets` (5.x):
```python
from datasets import load_dataset
ds = load_dataset("json", data_files={"train": "train.jsonl", "test": "test.jsonl"})
print(ds)                                  # splits, features, num_rows
print(ds["train"].features)
empty = ds["train"].filter(lambda r: not (r["text"] or "").strip())
print(len(empty))
```

### 3. Duplicates and near-duplicates
- **Exact**: hash of normalised text (lowercase, collapsed whitespace, optional punctuation strip). Cheap; do it first, within and across splits.
- **Near-duplicate**: shingled MinHash/LSH, or embedding similarity with a threshold chosen by inspecting borderline pairs. Tune on a sample, report the threshold and the manual precision you observed. Libraries exist (for example datasketch); evaluate before adding a dependency.
- Duplicates inside train inflate memorisation and distort class balance; duplicates **across** train and test make the test score meaningless. Remove from train (or test, if it is the less trusted side) and log.
- Templated data (same template, different entity) behaves like near-duplication; check by masking numbers/entities.

### 4. Labels
- Conflicting labels for identical inputs (the script reports this).
- Class imbalance: report counts and per-class minimums. Choose metrics (macro-F1, PR-AUC, per-class recall) that do not hide minority failure; resampling is a training decision applied to train only.
- Label noise: sample and manually review disagreements between a trained model and the labels (high-confidence mismatches are the usual suspects). For human annotation, compute inter-annotator agreement (Cohen's kappa for two raters, Krippendorff's alpha for more) and write down the guideline that resolved disagreements.
- LLM-assigned labels are noisy labels: validate against a human-labelled sample before trusting them.

### 5. Leakage
Leakage is any path by which test information reaches training or features.
- Exact/near duplicates across splits (step 3).
- Temporal: random split of time-ordered data lets the model see the future. Split by time for forecasting-like tasks.
- Group: multiple rows per user/patient/document/repo. Split by group so no group spans splits.
- Feature leakage: columns derived from the label, IDs correlated with outcome, post-event fields.
- Contamination of public benchmarks into pre-training or fine-tuning corpora: check n-gram overlap between training text and benchmark items before reporting benchmark scores.
- Preprocessing fitted on all data before splitting.

### 6. Privacy, safety and licence screening
- Regex and dictionary scans for emails, phone numbers, IDs, API keys/tokens, credentials are a first filter, not a guarantee; use a vetted PII tool where stakes are high and sample manually.
- Report how many rows match, never print matched values to shared logs.
- If secrets are found, tell the user to rotate them; do not store or propagate them.
- Record source, collection method, licence and consent basis per source.

### 7. Split design
- Fixed seed, written down. `ds["train"].train_test_split(test_size=0.1, seed=42)` for i.i.d. rows; stratify (`stratify_by_column` requires a `ClassLabel` column) when classes are rare; group/time splits otherwise (implement with explicit group keys, then `select`).
- Keep a **frozen test set** touched only for final reporting. Tune on validation. If you consult test repeatedly, it has become validation data.
- Check that class and length distributions match across splits.

### 8. Document and version
Write a dataset card: purpose, sources and licences, collection and filtering steps with counts removed per step, known biases and limitations, label guideline, split method and seed, intended and out-of-scope uses, PII handling, version/hash. See [references/dataset-card-template.md](references/dataset-card-template.md). Store a checksum or commit id of the cleaned files.

## Worked example

Task: a support-ticket classifier shows 99% test accuracy.

1. `audit_jsonl.py train.jsonl ... --compare test.jsonl` reports `exact_overlap_rows=412` (counted in the primary train file: 412 train rows also appear in test) and `identical texts with conflicting labels=37`.
2. Decision: remove overlapping rows from **train** (test is the frozen artefact), log row ids, rebuild a deduplicated train set, re-train/re-evaluate. Accuracy drops to 91%, which is the credible number.
3. The 37 conflicts go to a reviewer with the labelling guideline; resolved labels are written to a new file version.
4. Remaining check: tickets from the same customer span both splits; re-split by `customer_id` and report the grouped result (88%) as the headline.
5. Dataset card updated with each step and the counts.

## Anti-patterns

- Deduplicating after splitting only within each split.
- Random split of conversational, temporal or per-user data.
- Fitting scalers/vocabularies/imputers on the full dataset.
- "Cleaning" by deleting every hard example, which inflates scores.
- Using the test set to pick thresholds or data filters.
- Treating a regex PII scan as proof of anonymity.
- Re-labelling with an LLM and not measuring its error rate.
- Loading remote dataset scripts, or uploading private data to a public hub.

## Verification checklist

- [ ] Source untouched; cleaned output versioned; removal log kept
- [ ] Structure checks run with counts; unparseable/non-object lines explained
- [ ] Exact and (if relevant) near duplicates handled within and across splits
- [ ] Conflicting labels and class balance reported; annotation quality measured where humans labelled
- [ ] Leakage paths considered (duplicate, temporal, group, feature, benchmark)
- [ ] PII/secret/licence screening done; nothing sensitive printed or uploaded
- [ ] Split method, seed and frozen test set recorded
- [ ] Dataset card written with counts per step

## References

- [scripts/audit_jsonl.py](scripts/audit_jsonl.py) - read-only JSONL audit (tested on a tiny fixture)
- [references/dataset-card-template.md](references/dataset-card-template.md)
- [references/scenarios.md](references/scenarios.md)
- [references/sources.md](references/sources.md)
