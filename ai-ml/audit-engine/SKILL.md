---
name: audit-engine
description: >
  Activate when the user wants to audit a paper's empirical or technical claims
  against a linked code repository — checking whether experiments, datasets,
  models, metrics, and hyperparameters described in the paper actually exist
  and match the code. Produces a structured audit report classifying each claim
  as CONFIRMED, PARTIAL, MISSING, or MISMATCH, with file/line evidence. Useful
  for reproducibility checks, reviewer due diligence, and pre-submission
  self-audits of ML/CS/empirical papers that ship code.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Audit Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (audit-engine)
> **Input:** [paper + repo being audited]
> **Output:** [brief summary — e.g., "Audited 18 claims: 12 CONFIRMED, 3 PARTIAL, 2 MISSING, 1 MISMATCH"]
> ```

# Audit Engine

## Core Principle

Papers make claims. Code embodies what was actually done. This engine systematically
checks whether the two agree. For every empirical or technical claim in the paper —
datasets used, models trained, metrics reported, hyperparameters set, ablations run —
the engine locates supporting evidence in the linked repository and classifies the
match.

This is the complement to `verification-engine`, which checks citations against
external sources. Audit-engine checks *the paper's own claims* against *the paper's
own code*. Together they cover both failure modes of LLM-assisted writing: mis-cited
prior work and unsupported own-work claims.

Inspired by the `/audit` command in the Feynman research agent (Companion AI, 2026),
adapted to the IS/CS methodological style of this plugin.

## When to Activate

- User says "audit the paper", "check paper vs. code", "verify my experiments",
  "reproducibility audit", "does the code match what I wrote"
- Before submitting a paper with an accompanying code release
- Before open-sourcing the repo of a published paper
- When reviewing someone else's paper + artifact
- As optional Phase 7.5 of the paper machine pipeline (after verify-citations,
  before prepare-submission)

## When NOT to Activate

- The paper has no code artifact (pure theory, position paper, qualitative study
  without computational analysis) → say so and exit
- The user wants to verify *citations* → activate `verification-engine` instead
- The user wants to check *writing quality* → activate the writing-engine
  `/analyze-writing` command

---

## Inputs

Required:
1. **Paper source** — `paper.tex`, `draft.md`, or explicit `$ARGUMENTS` path
2. **Code repository** — one of:
   - Local path (`./experiments/`, `~/repos/myproject`)
   - GitHub URL (clone or use `gh repo view` / `WebFetch` on raw files)
   - Archive link (Zenodo, OSF) — ask user to download locally first

If the repo location is not supplied, scan the paper for common signals:
- "Code available at [URL]" / "Our implementation is at [URL]"
- GitHub URLs in footnotes or acknowledgements
- A `code_availability` section
- A `REPRODUCIBILITY.md`, `ARTIFACT.md`, or similar file sibling to the paper

If still not found: ask the user once, then exit.

---

## Step 1: Extract Auditable Claims

Scan the paper for claims that can be checked against code. Ignore claims that are
purely conceptual, historical, or theoretical.

### Claim Categories (check in order)

| Category | What to look for | Priority |
|----------|------------------|----------|
| **Dataset** | Named datasets, split sizes, sample counts, data sources | HIGH |
| **Model** | Model names, architectures, parameter counts, checkpoints | HIGH |
| **Training** | Epochs, batch size, learning rate, optimizer, hardware | HIGH |
| **Metrics** | Reported numbers (accuracy, F1, BLEU, loss values, percentages) | HIGH |
| **Experiments** | Named experimental conditions, ablations, baselines | HIGH |
| **Hyperparameters** | Specific values in tables or "Training Details" | MEDIUM |
| **Preprocessing** | Tokenization, normalization, filtering steps | MEDIUM |
| **Evaluation** | Test protocol, prompt templates, judge models, seeds | MEDIUM |
| **Infrastructure** | GPUs, training time, framework versions | LOW |
| **Figures** | Plots claimed to come from "our experiments" | MEDIUM |

### Extraction Pattern

For each claim, record:
```
{
  id: "C01",
  category: "Model",
  section: "4.2 Model Training",
  claim_text: "We fine-tune LLaMA-3-8B for 3 epochs with a learning rate of 2e-5.",
  testable_facts: [
    "model == LLaMA-3-8B",
    "epochs == 3",
    "learning_rate == 2e-5"
  ],
  priority: "HIGH"
}
```

Claims with concrete numbers, names, or identifiers are testable. Vague claims
("we use a standard transformer") are not auditable — mark them as `NOT_AUDITABLE`
and skip.

**Output:** `outputs/audit_claims.md` — numbered list of all testable claims.

---

## Step 2: Map the Repository

Before searching, build a lightweight mental map of the repo. Do not read every file.

1. **Top-level listing** — `Glob` on `**/*.{py,ipynb,yaml,yml,json,toml,sh,md}`
   at depth 2-3
2. **Identify key files** by name convention:
   - `train.py`, `main.py`, `run_experiments.py`, `eval.py` → entry points
   - `config.yaml`, `hparams.json`, `sweep.yaml`, `*.toml` → configuration
   - `requirements.txt`, `pyproject.toml`, `environment.yml` → dependencies
   - `README.md`, `REPRODUCE.md`, `docs/` → documentation
   - `results/`, `outputs/`, `logs/`, `wandb/` → experiment artifacts
   - `datasets/`, `data/`, `load_data.py` → data loaders
3. **Detect framework** — PyTorch, JAX, TensorFlow, HuggingFace, scikit-learn —
   this guides search patterns
4. **Detect experiment tracking** — wandb, mlflow, tensorboard, plain CSV logs

Record this as an internal map; do not output it unless the user asks.

---

## Step 3: Search for Evidence (per claim)

For each testable claim, systematically search for supporting code evidence.

### Search Strategy

Use `Grep` and `Read` — NOT an agent — for transparency. Each lookup should produce
a file path and line number that can be cited in the report.

**Example — Model claim "`LLaMA-3-8B, 3 epochs, lr=2e-5`":**

1. Search for the model name: `Grep "llama-?3-?8b|Llama-3-8B" --type py`
2. Search for learning rate: `Grep "2e-?5|0.00002|learning_rate.*2e-5"`
3. Search for epochs: `Grep "epochs\s*[:=]\s*3|num_epochs.*3"`
4. Check config files: `Read config/*.yaml` for matching values
5. If wandb/mlflow logs exist, grep those too

**Example — Metric claim "`we report an F1 of 0.87`":**

1. Search results files: `Grep "0\.87" --type json --type csv --type md`
2. Search eval scripts: `Grep -l "f1_score|F1" eval*.py`
3. Check if the number appears in a logged output

**Example — Dataset claim "`trained on 12,000 examples from OpenReview`":**

1. Search for dataset loader: `Grep "openreview" -i`
2. Check size assertions: `Grep "12000|12_000|len\(.*\).*12"`
3. Read the data loading function to confirm source

### Record Evidence

For each claim, record:
```
{
  id: "C01",
  searches: ["llama-3-8b", "lr=2e-5", "epochs=3"],
  hits: [
    {file: "train.py", line: 42, snippet: "model_name = 'meta-llama/Llama-3-8B'"},
    {file: "config/train.yaml", line: 7, snippet: "learning_rate: 2e-5"},
    {file: "config/train.yaml", line: 8, snippet: "epochs: 5"}  // NOTE mismatch
  ]
}
```

Do not hallucinate hits. If Grep returns nothing, record an empty hits list.

---

## Step 4: Classify Each Claim

### Classification Rubric

| Status | Criteria | Evidence |
|--------|----------|----------|
| **CONFIRMED** | Every testable fact in the claim has matching code evidence | File + line for each fact |
| **PARTIAL** | Some facts confirmed, others missing or unchecked | Confirmed facts listed; gaps called out |
| **MISSING** | No code evidence found for any fact in the claim | Which searches returned empty |
| **MISMATCH** | Code evidence exists but contradicts the claim | Side-by-side: paper says X, code says Y |
| **NOT_AUDITABLE** | Claim is too vague to check, or code is not available | Brief reason |

### Rules of Engagement

- **Be conservative.** If you're not sure a search hit actually supports the claim,
  mark PARTIAL and explain what's missing.
- **Never mark CONFIRMED without a file:line reference.** "I think it's probably
  in the training script" is not evidence.
- **Treat MISMATCH as load-bearing.** Even a single MISMATCH is worth flagging
  prominently — these are the findings the user most needs to know.
- **Distinguish MISSING from NOT_AUDITABLE.** MISSING means the claim is
  checkable but no evidence exists (red flag). NOT_AUDITABLE means the claim
  itself is too vague (usually fine, but worth rewriting).
- **Do not run code.** This engine is a static audit. Running experiments is the
  job of a separate replication step (future extension point).

---

## Step 5: Generate Audit Report

Save to `outputs/audit_report.md`.

### Report Template

```markdown
# Paper-vs-Code Audit Report

**Paper:** [paper title]
**Paper source:** [paper.tex | draft.md | path]
**Code repository:** [local path or URL]
**Commit / version audited:** [git SHA if available, else "working tree"]
**Date:** [YYYY-MM-DD]
**Auditor:** audit-engine (Open Academic Paper Machine v6.4)

## Summary

| Status | Count | % |
|--------|-------|---|
| CONFIRMED | [n] | [%] |
| PARTIAL | [n] | [%] |
| MISSING | [n] | [%] |
| MISMATCH | [n] | [%] |
| NOT_AUDITABLE | [n] | [%] |

**Overall signal:** [one sentence — e.g., "Core experiments check out; 2 mismatches
in reported hyperparameters need attention before submission."]

## Critical Findings

### MISMATCH — Paper and Code Disagree

#### [C03] [Section 4.2] "We train for 3 epochs with learning rate 2e-5"
- **Paper says:** epochs = 3, lr = 2e-5
- **Code says:**
  - `config/train.yaml:8` → `epochs: 5`
  - `config/train.yaml:7` → `learning_rate: 2e-5`  ✓
- **Recommendation:** Update the paper to say 5 epochs, or re-run with 3 and
  re-check the reported numbers.

[repeat for each mismatch]

### MISSING — Claim Not Supported by Code

#### [C07] [Section 5.1] "We evaluate on the held-out 10% split (1,200 examples)"
- **Paper says:** held-out split of 1,200 examples
- **Searched:** `held.out`, `test_split`, `1200`, `0\.1`
- **Result:** No split logic found in `data/loader.py`. `eval.py` loads the entire
  dataset without stratification.
- **Recommendation:** Either add split logic to the repo or remove the claim from
  the paper.

[repeat for each missing]

## Detailed Findings by Section

### Section 4 — Method

| # | Claim | Category | Status | Evidence |
|---|-------|----------|--------|----------|
| C01 | LLaMA-3-8B model | Model | CONFIRMED | `train.py:42` |
| C02 | 2e-5 learning rate | Training | CONFIRMED | `config/train.yaml:7` |
| C03 | 3 epochs | Training | MISMATCH | see Critical Findings |
| C04 | AdamW optimizer | Training | CONFIRMED | `train.py:88` |

### Section 5 — Experiments

| # | Claim | Category | Status | Evidence |
|---|-------|----------|--------|----------|
| C05 | F1 = 0.87 on test set | Metric | CONFIRMED | `results/test_metrics.json:12` |
| C06 | 3 random seeds | Training | PARTIAL | seeds {42,43} found in `run.sh`, third seed unclear |
| C07 | Held-out 10% split | Dataset | MISSING | see Critical Findings |

[repeat for each section]

## Not Auditable

Claims that are too vague to check or depend on external state:

| # | Claim | Reason |
|---|-------|--------|
| C12 | "A standard transformer architecture" | Vague — no specific config to check |
| C15 | "Comparable to human performance" | Depends on external human benchmark |

## Repository Map (for context)

- **Entry points:** `train.py`, `eval.py`, `run_sweep.sh`
- **Configs:** `config/train.yaml`, `config/eval.yaml`
- **Data loading:** `data/loader.py`
- **Dependencies:** `requirements.txt` (53 packages)
- **Experiment tracking:** wandb (runs in `wandb/`)
- **Results:** `results/` (JSON + CSV logs)

## Methodology Note

This audit was a **static audit**: code was read and grepped, but no experiments
were re-run. Matches indicate that the paper's claims are consistent with the code
*as written*, not that the code was verified to produce the reported numbers.

A full reproducibility check would additionally:
1. Install dependencies in a clean environment
2. Re-run training with the exact config
3. Re-run evaluation and compare numbers to the paper

See Extension Points below.

## Extension Points

- **Dynamic replication:** re-run the training/eval pipeline in a Docker container
  and compare metrics to the paper (Feynman-style `/replicate`, not yet implemented
  in this plugin)
- **Diff-based re-audit:** after fixing mismatches, re-run on changed claims only
- **Multi-repo audits:** audit a paper that uses code from multiple repos (e.g.,
  baseline models from external sources)
```

---

## Prioritization Strategy

If the paper has many claims, process in this order and save intermediate results
after each tier so the user can act early:

**Tier 1 — High-stakes claims (verify first)**
- Reported numbers in tables and abstract
- Model identifier and size
- Dataset identifier and size
- Any claim the paper's contribution depends on

**Tier 2 — Method details**
- Hyperparameters, optimizers, schedulers
- Preprocessing, tokenization
- Evaluation protocol

**Tier 3 — Context**
- Infrastructure (GPUs, training time)
- Framework versions
- Figure provenance

After Tier 1, present a progress snapshot:

```
AUDIT PROGRESS
Tier 1 (High-stakes):  [12/12] Complete
  CONFIRMED: 9 | PARTIAL: 1 | MISSING: 1 | MISMATCH: 1
  >> 1 mismatch found — see audit_report.md

Tier 2 (Method):       [0/8]  Queued
Tier 3 (Context):      [0/4]  Queued

Continue to Tier 2? [proceeding unless you redirect]
```

---

## Limitations

### What This Engine Can Do
- Check named entities (datasets, models) against code references
- Verify hyperparameter values in configs match the paper
- Confirm metrics appear in logged results
- Catch contradictions between paper and code (MISMATCH)
- Catch unsupported claims (MISSING)
- Flag vague claims that should be rewritten (NOT_AUDITABLE)

### What This Engine Cannot Do
- Run the code and reproduce the numbers (static audit only)
- Detect whether the code would actually produce the claimed behaviour if run
- Audit closed-source or paywalled dependencies
- Audit manual/qualitative steps ("we prompted GPT-4 iteratively until...")
- Replace a human artifact reviewer

### Failure Modes to Watch For
- **Config vs. code divergence** — the YAML says one thing, `train.py` hard-codes
  another. Always check both.
- **Scripts that override configs** — `run.sh` may pass `--epochs 10` that overrides
  the YAML. Grep shell scripts too.
- **Multiple configs** — papers often report one experiment; the repo has ten.
  Match the config to the paper, not the other way around.
- **Notebooks** — `.ipynb` files are JSON; `Grep` works but read carefully.

---

## Relationship to Other Skills

- **`verification-engine`** — checks external citations against sources.
  `audit-engine` checks own-work claims against own code. Run both before
  submission for full coverage.
- **`review-engine`** — simulated peer review. An audit report is a natural
  input to a simulated reviewer.
- **`prepare-submission`** — a clean audit report is a strong artifact to include
  with submissions to venues that accept reproducibility statements (e.g. NeurIPS
  Reproducibility Checklist, ML Reproducibility Challenge).
