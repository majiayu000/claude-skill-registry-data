---
title: "ARC: AI2 Reasoning Challenge for Grade-School Science Questions"
description: "ARC (AI2 Reasoning Challenge) benchmark for evaluating grade-school science reasoning with multiple-choice questions."
benchmark_howto:
  name: "ARC (AI2 Reasoning Challenge)"
  description: "Tests scientific reasoning with 7,787 grade-school level multiple-choice science questions, split into a Challenge set of hard questions and an Easy set."
  benchmark_id: "arc"
faq:
  - q: "What is the difference between ARC-Challenge and ARC-Easy?"
    a: "ARC-Challenge contains questions that require multi-step reasoning and cannot be answered by simple retrieval or word co-occurrence. ARC-Easy contains the remaining questions. By default, mcpbr uses ARC-Challenge. Use filter_difficulty with 'easy' or 'challenge' to switch subsets."
  - q: "How many answer options does each ARC question have?"
    a: "ARC questions have between 3 and 5 answer options, typically labeled A through E. The model must respond with the letter of the correct answer."
  - q: "How does ARC evaluation extract the model's answer?"
    a: "The evaluation uses regex to find standalone letters (A-E) or digits (1-5) in the model's response, takes the last match, and compares it case-insensitively against the answer key."
---

# ARC (AI2 Reasoning Challenge)

## Overview

| Property | Value |
|----------|-------|
| **Benchmark ID** | `arc` |
| **Dataset** | [allenai/ai2_arc](https://huggingface.co/datasets/allenai/ai2_arc) |
| **Tasks** | 7,787 questions (Challenge + Easy) |
| **Evaluation** | Letter match against answer key |
| **Output Type** | Single letter (A-E) |
| **Timeout** | 60-180 seconds |

!!! tip "Quick Start"
    ```bash
    mcpbr run -c config.yaml --benchmark arc -n 20
    ```

## Overview

The AI2 Reasoning Challenge (ARC) is a benchmark consisting of 7,787 genuine grade-school level science questions assembled from standardized tests. The dataset is partitioned into two subsets:

- **ARC-Challenge** (default): 2,590 questions that require multi-step reasoning, scientific knowledge, and cannot be answered through simple statistical co-occurrence or retrieval methods. These questions were specifically filtered to be difficult for both retrieval-based and word co-occurrence algorithms.

- **ARC-Easy**: 5,197 questions that are answerable with simpler approaches. While still grade-school science questions, they tend to require less complex reasoning.

Each question is multiple-choice with 3 to 5 answer options labeled with letters (A through E) or occasionally numbers (1 through 5). The questions cover topics such as:

- Physical science (forces, energy, matter)
- Life science (biology, ecosystems, human body)
- Earth and space science (weather, geology, astronomy)
- Scientific reasoning and experimental design

ARC is useful for evaluating:

- **Scientific knowledge** at a foundational level
- **Multi-step reasoning** ability
- **Question comprehension** and inference
- **Answer selection** from plausible distractors

## Task Structure

Each ARC task contains the following fields:

- **id**: Unique question identifier
- **question**: The science question text
- **choices**: An object with `label` (list of letters) and `text` (list of answer texts)
- **answerKey**: The correct answer letter (e.g., "A", "B", "C", "D", or "E")

The agent receives the question with all labeled answer options and must respond with the letter of the correct answer.

### Example Task

```text
Answer the following science question:

A student is studying the properties of different materials. Which of the
following is the best conductor of electricity?

Options:
  (A) Glass rod
  (B) Copper wire
  (C) Rubber band
  (D) Wooden stick

Correct Answer: B
```

## Running the Benchmark

=== "CLI"

    ```bash
    # Run ARC-Challenge (default)
    mcpbr run -c config.yaml --benchmark arc

    # Run a small sample
    mcpbr run -c config.yaml --benchmark arc -n 20

    # Run ARC-Easy subset
    mcpbr run -c config.yaml --benchmark arc --filter-difficulty easy

    # Explicitly run ARC-Challenge
    mcpbr run -c config.yaml --benchmark arc --filter-difficulty challenge

    # Run with verbose output and save results
    mcpbr run -c config.yaml --benchmark arc -n 50 -v -o results.json
    ```

=== "YAML"

    ```yaml
    benchmark: "arc"
    sample_size: 10
    timeout_seconds: 120

    # Optional: select the Easy subset instead of Challenge
    filter_difficulty:
      - "easy"
    ```

### Difficulty Filtering

ARC uses `filter_difficulty` to select between the two subsets:

| Filter Value | Subset | Questions | Description |
|--------------|--------|-----------|-------------|
| `challenge` | ARC-Challenge | 2,590 | Hard questions requiring reasoning (default) |
| `easy` | ARC-Easy | 5,197 | Simpler questions answerable with retrieval |

When no `filter_difficulty` is specified, ARC-Challenge is used by default. If multiple values are provided, the last recognized value takes precedence.

## Evaluation Methodology

ARC evaluation uses letter-matching:

1. **Answer extraction**: The evaluation uses a regex pattern `\b([A-E1-5])\b` to find all standalone letters (A-E) or digits (1-5) in the model's uppercase response.

2. **Last-match selection**: The **last** matching letter or digit is used as the model's answer. This accommodates reasoning where the model discusses multiple options before settling on a final answer.

3. **Case-insensitive comparison**: The extracted answer is compared to the `answerKey` field. Both are uppercased before comparison.

### Scoring

```
resolved = (extracted_answer.upper() == answer_key.upper())
```

Where:
- `extracted_answer`: Last letter in [A-E] or digit in [1-5] found via regex
- `answer_key`: The correct answer from the dataset

### Answer Format

The model should respond with a single letter. The evaluation handles various response formats:

- `"B"` (direct answer)
- `"The answer is B."` (sentence format)
- `"B) Copper wire"` (letter with option text)
- `"After analyzing the options, I believe the answer is B because copper is a metal and metals conduct electricity."` (reasoned answer)

## Example Output

### Successful Evaluation

```json
{
  "resolved": true,
  "agent_answer": "B",
  "correct_answer": "B"
}
```

### Failed Evaluation (Wrong Answer)

```json
{
  "resolved": false,
  "agent_answer": "A",
  "correct_answer": "B"
}
```

### Failed Evaluation (No Answer Extracted)

```json
{
  "resolved": false,
  "error": "Could not extract answer from solution"
}
```

This occurs when the model's response does not contain any standalone letter in A-E or digit in 1-5.

## Troubleshooting

### Model discusses all options without clear final answer

If the model provides analysis of each option without stating a final letter, the regex extraction uses the last letter mentioned, which may be incorrect. Configure your prompt to enforce a clear final answer:

```yaml
agent_prompt: |
  {problem_statement}

  Think through the science carefully, then respond with ONLY the letter of the correct answer (A, B, C, D, or E).
```

### Evaluation extracts wrong letter from verbose response

Since the evaluation takes the **last** letter match, a response like "The answer is B. Options A and D are clearly wrong." would extract `D` instead of `B`. Instruct the model to place its final answer at the end of the response, or to respond with only the letter.

### Switching between Challenge and Easy returns unexpected counts

When using `filter_difficulty`, ensure you pass exactly one value. If both "easy" and "challenge" are specified, the implementation checks for "easy" first, then "challenge". The last matching condition sets the subset.

### Questions with numeric answer labels (1-5)

Some ARC questions use numeric labels (1, 2, 3, 4, 5) instead of letters (A, B, C, D, E). The evaluation handles both formats automatically through the regex pattern.

## Best Practices

- **Use ARC-Challenge for meaningful evaluation**: ARC-Easy questions can often be answered through pattern matching. ARC-Challenge provides a more discriminating measure of scientific reasoning.
- **Keep answers concise**: Single-letter responses eliminate extraction errors. If you need reasoning, instruct the model to state the letter first, then explain.
- **Start small**: Run 10-20 questions from each subset to establish a baseline before running larger evaluations.
- **Compare subsets**: Running both ARC-Challenge and ARC-Easy provides a useful difficulty gradient. Large accuracy gaps between the two subsets indicate the model may be relying on shortcuts rather than genuine reasoning.
- **Short timeouts are sufficient**: ARC questions are straightforward multiple-choice. A timeout of 60-120 seconds is typically more than enough.
- **Use for rapid model comparison**: ARC's well-established baselines and simple evaluation make it excellent for quickly comparing model capabilities before investing in more expensive benchmarks.

## Related Links

- [Benchmarks Overview](index.md)
- [HellaSwag](hellaswag.md) - Commonsense reasoning benchmark
- [TruthfulQA](truthfulqa.md) - Truthfulness evaluation benchmark
- [GAIA](gaia.md) - General AI assistant benchmark
- [ARC Dataset](https://huggingface.co/datasets/allenai/ai2_arc)
- [ARC Paper](https://arxiv.org/abs/1803.05457)
- [AI2 ARC Project](https://allenai.org/data/arc)
- [Configuration Reference](../configuration.md)
- [CLI Reference](../cli.md)
