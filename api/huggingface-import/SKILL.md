---
name: huggingface-import
description: Import datasets from HuggingFace and convert them to Coval test sets. Use when the user wants to create test cases from HuggingFace dataset or repository.
argument-hint: "[huggingface-repo-or-url]"
---

# HuggingFace to Coval Test Set Import

Import `$ARGUMENTS` from HuggingFace and convert it into Coval test sets with properly structured test cases.

## Coval Context

**Coval** is an AI evaluation platform for testing voice and conversational AI agents. It runs simulations against AI agents and measures performance with configurable metrics.

| Concept | Description |
|---------|-------------|
| **Test Set** | A collection of test cases, grouped by category or evaluation purpose |
| **Test Case** | A single evaluation scenario with `input` (prompt) and optional `metadata` |
| **Persona** | High-level user character (system prompt) - separate from test cases |
| **Agent** | The AI system being evaluated |

**Key distinction:**
- **Persona** = WHO is asking (character, traits)
- **Test Case** = WHAT they ask (prompts, scenarios)

## Coval API

**Base URL:** `https://api.coval.dev/v1`

Fetch the OpenAPI spec before making API calls:
```bash
# List specs (no auth)
GET https://api.coval.dev/v1/openapi

# Fetch specific spec
GET https://api.coval.dev/v1/openapi/{spec_name}
```

## Workflow

### Step 1: Identify the HuggingFace Source

If `$ARGUMENTS` is provided, navigate to it. Otherwise ask:
> What is the HuggingFace repository, space, or dataset you want to import?

Then:
1. Navigate to the HuggingFace source
2. Find data files (CSV, JSON, Parquet)
3. Examine structure and fields

### Step 2: Analyze Data Structure

Report to the user:
- Total records
- Available fields/columns
- Existing categorization
- 2-3 sample records

### Step 3: Interactive Field Mapping

Ask these questions to map HuggingFace data to Coval format:

**Q1: Input Field**
> Which field contains the question/prompt for the test case `input`?

**Q2: Categorization**
> How should test cases be organized into test sets?
> - By existing category field
> - Single test set
> - Custom logic

**Q3: Metadata**
> Which fields should be preserved in `metadata` JSON?
> (Recommend: preserve original IDs like `question_id`)

**Q4: Multi-turn** (if applicable)
> How to handle multi-turn conversations?
> - First turn only
> - Concatenate turns
> - Separate test cases per turn

### Step 4: Generate CSVs

Create Coval-compatible CSVs:

```csv
input,metadata
"Your question here","{""question_id"": ""123"", ""source"": ""mt-bench""}"
```

**Requirements:**
- `input` column MUST be first
- Proper quote escaping (double quotes)
- `metadata` as valid JSON string
- UTF-8 encoding
- One CSV per category (recommended)

**Naming:** `{source}_{category}.csv`

### Step 5: Upload to Coval

**Manual:** Upload CSVs via Coval dashboard test sets page.

**API:** Fetch OpenAPI spec and use test set endpoints programmatically.

## Common HuggingFace Sources

### General Language Understanding

| Dataset | Description |
|---------|-------------|
| `cais/mmlu` | 15k+ multiple-choice questions across 57 subjects (STEM, humanities, law) |
| `nyu-mll/glue` | Sentence-level tasks: sentiment, entailment, linguistic acceptability |
| `tau/commonsense_qa` | Reasoning tests for everyday world knowledge |
| `Rowan/hellaswag` | Common-sense inference and completion |

### Reasoning & Problem-Solving

| Dataset | Description |
|---------|-------------|
| `openai/gsm8k` | ~8k grade-school math word problems (multi-step arithmetic) |
| `ucinlp/drop` | Reading comprehension with discrete operations |
| `lukaemon/bbh` | BigBench Hard - challenging reasoning subset |

## Supporting Files

- For Python transformation example, see [examples/huggingface-import.py](examples/huggingface-import.py)

## Checklist

- [ ] Identified input field
- [ ] Determined categorization
- [ ] Preserved original IDs in metadata
- [ ] Proper quote escaping
- [ ] Valid JSON in metadata
- [ ] Separate CSVs per category
