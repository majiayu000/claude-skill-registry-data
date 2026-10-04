---
name: llm
description: "Build and evaluate LLM prompts. Use when crafting system prompts, comparing variants, estimating tokens, or managing prompt templates."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - llm
  - prompt-engineering
  - tokens
  - templates
  - evaluation
---

# llm

LLM Prompt Engineering Toolkit. Build structured prompts from role/context/task components, compare prompt variations side by side, estimate token counts, manage reusable prompt templates, chain multi-step prompts, and evaluate prompt quality with a scored breakdown. All commands run locally in bash with no API keys or network access required.

## Commands

### `prompt` — Build a Structured Prompt

Assembles a prompt from modular components: role, context, task, constraints, and output format. The `--task` flag is required; all others are optional.

**Flags:**
- `--role <text>` — Define the AI's persona (e.g., "senior developer")
- `--context <text>` — Provide background information
- `--task <text>` — **(required)** The main instruction
- `--constraints <text>` — Rules or limitations
- `--format <text>` — Desired output format

```bash
bash scripts/script.sh prompt --role "senior developer" --context "Python Flask app" --task "write unit tests"
bash scripts/script.sh prompt --task "summarize this article" --constraints "max 3 sentences" --json
```

### `compare` — Compare Prompt Variations

Compare two or more prompt files side by side. Shows each variant with word/line/char/token stats, then a `diff --side-by-side` of the first two variants, plus a summary table.

**Flags:**
- `--prompts <file1> <file2> [file3...]` — Two or more prompt text files to compare

```bash
bash scripts/script.sh compare --prompts prompt_a.txt prompt_b.txt
bash scripts/script.sh compare --prompts v1.txt v2.txt v3.txt
```

### `tokenize` — Estimate Token Count

Estimate the token count for a given text using a cl100k_base-compatible heuristic. Reports characters, words, lines, and estimated tokens.

**Input methods:**
- `--input <text>` — Inline text string
- `--file <path>` — Read from a file
- Pipe via stdin

```bash
bash scripts/script.sh tokenize --input "Your prompt text here"
bash scripts/script.sh tokenize --file prompt.txt
echo "some text" | bash scripts/script.sh tokenize
bash scripts/script.sh tokenize --file prompt.txt --json
```

### `template` — Manage Prompt Templates

Save, list, load, and delete reusable prompt templates. Templates are stored as `.txt` files in `~/.llm-skill/templates/`.

**Actions:**
- `--save <name> --file <path>` — Save a template from a file (or pipe via stdin)
- `--list` — List all saved templates with sizes
- `--load <name>` — Output the contents of a saved template
- `--delete <name>` — Remove a saved template

```bash
bash scripts/script.sh template --save my_template --file prompt.txt
bash scripts/script.sh template --list
bash scripts/script.sh template --list --json
bash scripts/script.sh template --load my_template
bash scripts/script.sh template --delete my_template
echo "Write a haiku about {{topic}}" | bash scripts/script.sh template --save haiku
```

### `chain` — Multi-Step Prompt Chains

Run a sequence of prompt steps where each step's output feeds into the next via the `{{previous_output}}` placeholder. Steps can be specified as individual files or loaded from a JSON config.

**Flags:**
- `--steps <file1> <file2> [...]` — Ordered list of step files
- `--from <config.json>` — Load steps from a JSON configuration file

```bash
bash scripts/script.sh chain --steps step1.txt step2.txt step3.txt
bash scripts/script.sh chain --from chain_config.json
bash scripts/script.sh chain --steps brainstorm.txt refine.txt format.txt --json
```

### `evaluate` — Score Prompt Quality

Score a prompt on four dimensions (0–100 each): **Clarity**, **Specificity**, **Structure**, and **Completeness**. Returns an overall score (0–100) and letter grade (A–F) with actionable suggestions.

**Scoring heuristics:**
- **Clarity** — Penalizes vague words ("something", "stuff"), rewards action verbs ("write", "create", "analyze") and structural markers
- **Specificity** — Rewards concrete numbers, quoted examples, and sufficient length
- **Structure** — Rewards headers, bullet lists, numbered steps, and paragraph breaks
- **Completeness** — Checks for role definition, output format spec, constraints, and examples

```bash
bash scripts/script.sh evaluate --input "Explain quantum computing"
bash scripts/script.sh evaluate --file my_prompt.txt
bash scripts/script.sh evaluate --file my_prompt.txt --json
```

### `help` — Show Help

```bash
bash scripts/script.sh help
```

## Global Flags

- `--json` — Output in JSON format (supported by `prompt`, `tokenize`, `template --list`, `chain`, and `evaluate`)

## Data Storage

- **Templates:** `~/.llm-skill/templates/*.txt`
- No other persistent state. All commands are stateless except `template` which manages saved files.

## Requirements

- Bash 4+ (uses arrays, `[[ ]]`, process substitution)
- Standard Unix utilities: `wc`, `grep`, `diff`, `cat`, `basename`, `tr`, `sed`, `rm`, `mkdir`
- No external dependencies, API keys, or network access required

## When to Use

1. **Crafting system prompts** — Use `prompt` to build well-structured prompts from role/context/task components instead of writing them freehand.
2. **A/B testing prompt variants** — Use `compare` to see side-by-side diffs and token counts for two or more prompt versions before committing to one.
3. **Estimating API costs** — Use `tokenize` to get token estimates before sending prompts to paid LLM APIs, helping you stay within budget.
4. **Building reusable prompt libraries** — Use `template` to save, organize, and reuse your best prompts across projects.
5. **Quality-checking prompts before use** — Use `evaluate` to score your prompts on clarity, specificity, structure, and completeness, with actionable improvement suggestions.

## Examples

```bash
# Build a structured prompt for code review
bash scripts/script.sh prompt \
  --role "senior code reviewer" \
  --context "React TypeScript project" \
  --task "review this pull request for bugs and performance issues" \
  --constraints "focus on security vulnerabilities" \
  --format "numbered list of findings"

# Estimate tokens for a long prompt
bash scripts/script.sh tokenize --file system_prompt.txt

# Save a template and reuse it
echo "You are a {{role}}. Your task: {{task}}" | bash scripts/script.sh template --save generic
bash scripts/script.sh template --load generic

# Evaluate prompt quality
bash scripts/script.sh evaluate --input "You are an expert Python developer. Write a function that sorts a list of dictionaries by a given key. Include type hints, docstring, and 3 unit tests."
```

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
