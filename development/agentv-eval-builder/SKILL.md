---
name: agentv-eval-builder
description: Create and maintain AgentV YAML evaluation files for testing AI agent performance. Use this skill when creating new eval files, adding eval cases, or configuring custom evaluators (code validators or LLM judges) for agent testing workflows.
---

# AgentV Eval Builder

## Schema Reference
- Schema: `references/eval-schema.json` (JSON Schema for validation and tooling)
- Format: YAML with structured content arrays
- Examples: `references/example-evals.md`

## Feature Reference
- Rubrics: `references/rubric-evaluator.md` - Structured criteria-based evaluation
- Composite Evaluators: `references/composite-evaluator.md` - Combine multiple evaluators
- Tool Trajectory: `references/tool-trajectory-evaluator.md` - Validate agent tool usage
- Structured Data + Metrics: `references/structured-data-evaluators.md` - `field_accuracy`, `latency`, `cost`
- Custom Evaluators: `references/custom-evaluators.md` - Code and LLM judge templates
- Batch CLI: `references/batch-cli-evaluator.md` - Evaluate batch runner output (JSONL)
- Compare: `references/compare-command.md` - Compare evaluation results between runs

## Structure Requirements
- Root level: `description` (optional), `execution` (with `target`), `evalcases` (required)
- Eval case fields: `id` (required), `expected_outcome` (required), `input_messages` (required)
- Optional fields: `expected_messages`, `conversation_id`, `rubrics`, `execution`
- `expected_messages` is optional - omit for outcome-only evaluation where the LLM judge evaluates based on `expected_outcome` criteria alone
- Message fields: `role` (required), `content` (required)
- Message roles: `system`, `user`, `assistant`, `tool`
- Content types: `text` (inline), `file` (relative or absolute path)
- Attachments (type: `file`) should default to the `user` role
- File paths: Relative (from eval file dir) or absolute with "/" prefix (from repo root)

## Custom Evaluators

Configure multiple evaluators per eval case via `execution.evaluators` array.

### Code Evaluators
Scripts that validate output programmatically:

```yaml
execution:
  evaluators:
    - name: json_format_validator
      type: code_judge
      script: uv run validate_output.py
      cwd: ../../evaluators/scripts
```

**Contract:**
- Input (stdin): JSON with `question`, `expected_outcome`, `reference_answer`, `candidate_answer`, `guideline_files` (file paths), `input_files` (file paths, excludes guidelines), `input_messages`
- Output (stdout): JSON with `score` (0.0-1.0), `hits`, `misses`, `reasoning`

**TypeScript evaluators:** Keep `.ts` source files and run them via Node-compatible loaders such as `npx --yes tsx` so global `agentv` installs stay portable. See `references/custom-evaluators.md` for complete templates and command examples.

**Template:** See `references/custom-evaluators.md` for Python and TypeScript templates

### LLM Judges
Language models evaluate response quality:

```yaml
execution:
  evaluators:
    - name: content_evaluator
      type: llm_judge
      prompt: /evaluators/prompts/correctness.md
      model: gpt-5-chat
```

### Tool Trajectory Evaluators
Validate agent tool usage patterns (requires `output_messages` with `tool_calls` from provider):

```yaml
execution:
  evaluators:
    - name: research_check
      type: tool_trajectory
      mode: any_order       # Options: any_order, in_order, exact
      minimums:             # For any_order mode
        knowledgeSearch: 2
      expected:             # For in_order/exact modes
        - tool: knowledgeSearch
        - tool: documentRetrieve
```

See `references/tool-trajectory-evaluator.md` for modes and configuration.

### Multiple Evaluators
Define multiple evaluators to run sequentially. The final score is a weighted average of all results.

```yaml
execution:
  evaluators:
    - name: format_check      # Runs first
      type: code_judge
      script: uv run validate_json.py
    - name: content_check     # Runs second
      type: llm_judge
```

### Rubric Evaluator
Inline rubrics for structured criteria-based evaluation:

```yaml
evalcases:
  - id: explanation-task
    expected_outcome: Clear explanation of quicksort
    input_messages:
      - role: user
        content: Explain quicksort
    rubrics:
      - Mentions divide-and-conquer approach
      - Explains the partition step
      - id: complexity
        description: States time complexity correctly
        weight: 2.0
        required: true
```

See `references/rubric-evaluator.md` for detailed rubric configuration.

### Composite Evaluator
Combine multiple evaluators with aggregation:

```yaml
execution:
  evaluators:
    - name: release_gate
      type: composite
      evaluators:
        - name: safety
          type: llm_judge
          prompt: ./prompts/safety.md
        - name: quality
          type: llm_judge
          prompt: ./prompts/quality.md
      aggregator:
        type: weighted_average
        weights:
          safety: 0.3
          quality: 0.7
```

See `references/composite-evaluator.md` for aggregation types and patterns.

### Batch CLI Evaluation
Evaluate external batch runners that process all evalcases in one invocation:

```yaml
description: Batch CLI evaluation
execution:
  target: batch_cli

evalcases:
  - id: case-001
    expected_outcome: Returns decision=CLEAR
    expected_messages:
      - role: assistant
        content:
          decision: CLEAR
    input_messages:
      - role: user
        content:
          row:
            id: case-001
            amount: 5000
    execution:
      evaluators:
        - name: decision-check
          type: code_judge
          script: bun run ./scripts/check-output.ts
          cwd: .
```

**Key pattern:**
- Batch runner reads eval YAML via `--eval` flag, outputs JSONL keyed by `id`
- Each evalcase has its own evaluator to validate its corresponding output
- Use structured `expected_messages.content` for expected output fields

See `references/batch-cli-evaluator.md` for full implementation guide.

## Example
```yaml
description: Example showing basic features and conversation threading
execution:
  target: default

evalcases:
  - id: code-review-basic
    expected_outcome: Assistant provides helpful code analysis
    
    input_messages:
      - role: system
        content: You are an expert code reviewer.
      - role: user
        content:
          - type: text
            value: |-
              Review this function:
              
              ```python
              def add(a, b):
                  return a + b
              ```
          - type: file
            value: /prompts/python.instructions.md
    
    expected_messages:
      - role: assistant
        content: |-
          The function is simple and correct. Suggestions:
          - Add type hints: `def add(a: int, b: int) -> int:`
          - Add docstring
          - Consider validation for edge cases
```
