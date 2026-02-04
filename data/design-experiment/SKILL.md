---
name: design-experiment
description: Plan LLM fine-tuning and evaluation experiments. Use when the user wants to design a new experiment, plan training runs, or create an experiment_summary.yaml file.
---

# Design Experiment

You help users plan experiments for fine-tuning and evaluating LLMs. Create a plan that specifies the complete workflow from training through evaluation, verifies resources, and documents all steps in a structured YAML configuration.

## Your Task

Guide the user through designing their experiment by asking questions, verifying resources, and creating a comprehensive `experiment_summary.yaml` file that documents the complete plan.

## Workflow

Follow the three-stage process:

### 1. Parameter Selection → `param_selection.md`

Guide the user through 9 interactive steps to gather all experiment parameters:
1. Determine experiment purpose and location (workflow test vs research experiment)
2. Understand the experiment (scientific question, variables)
3. Confirm tool choices (torchtune for preparation, inspect-ai for evaluation)
4. Design training runs (models, datasets, hyperparameters)
5. Design evaluation runs (tasks, epochs, evaluation matrix)
6. Establish naming (experiment name, run names)
7. Verify resources (models, datasets, eval scripts exist)
8. Get approval (validate first, then present)
9. Create files (proceed to generation stage)

**See `param_selection.md` for:**
- Complete question flow for each step
- Auto-detection logic for experiment location
- Resource verification commands
- Conversation patterns

### 2. Validation → `validation.md`

Before presenting plan to user (step 8), validate completeness:
- ✓ All YAML sections present and properly structured
- ✓ All run names follow convention
- ✓ All parameters documented (variables and controls)
- ✓ Evaluation plan is consistent (0-indexed epochs, base vs fine-tuned)
- ✓ **System prompt matches between training and evaluation** (critical!)
- ✓ All resources verified (or noted as prerequisites)

**See `validation.md` for:**
- Complete validation checklist
- Common issues to check
- How to handle missing prerequisites

### 3. Experiment Generation → `experiment_generation.md`

After user approves, create output files:
1. `experiment_summary.yaml` - Structured experiment configuration (use `templates/experiment_summary.yaml`)
2. `design-experiment.jsonl` - Machine-readable audit trail (see `logging.md`)

Then ask about next steps (scaffold-experiment?).

**See `experiment_generation.md` for:**
- File creation instructions
- YAML formatting guidance
- Next steps conversation pattern
- Prerequisites handling

---

## Cross-Cutting Concerns

### Logging → `logging.md`

**IMPORTANT:** Throughout param_selection and generation, create detailed log at `{experiment_dir}/design-experiment.jsonl`.

**What to log:**
- ✓ Resource verification (ls, du, df commands and results)
- ✓ Prior run searches (if performed)
- ✓ Decisions (naming, recipe, configuration)
- ✓ File creation

**Format:** JSON Lines (.jsonl) - one JSON object per line

**See `logging.md` for:**
- Complete log format specification
- All action types with schemas
- Example entries for each action type
- When to log during workflow

### Templates → `templates/`

Reference materials for output generation:
- `templates/experiment_summary.yaml` - YAML schema and structure for experiment plan

---

## Important Reminders

- **Use paths from `claude.local.md`** for models, datasets, scratch directories
- **Always verify resources** exist before finalizing plan (log all verification)
- **System prompt consistency is critical** - must match between training and evaluation for inspect-ai
- **Epochs are 0-indexed** - Use [0, 1, 2] in evaluation matrix
- **Base models** use `epochs: null`, **fine-tuned models** use `epochs: [0, 1]`
- **Document tool choices** in YAML - torchtune for training, inspect-ai for evaluation
- **Handle missing resources gracefully** - note as prerequisites, don't block the plan
- **If inspect-ai task doesn't exist** - note that `create-inspect-task` skill should be run first
- **Generate YAML, not Markdown** - Use structured YAML format with proper indentation

---

## Module Organization

This skill uses the **param_selection → validation → generation** pattern:

| Module | Purpose | Lines |
|--------|---------|-------|
| param_selection.md | 9-step interactive workflow | ~340 |
| validation.md | Completeness checklist | ~140 |
| experiment_generation.md | Create YAML and JSONL files | ~125 |
| logging.md | JSONL audit trail specification | ~400 |
| templates/experiment_summary.yaml | YAML schema and structure | ~150 |

**Pattern:** Three action verbs (selection, validation, generation) matching scaffold/run skills, plus cross-cutting logging and templates.

**See `README.md` for:** Complete pattern documentation and rationale.
