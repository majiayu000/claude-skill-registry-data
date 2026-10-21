---
name: test-plan-score-test-function
description: Score generated test function code for completeness, quality, and convention adherence using a 5-criteria rubric. Use for validating generated test code quality before including in the final implementation.
context: fork
allowedTools: Read, Write
model: claude-sonnet-4-6
user-invocable: false
---

# Test Function Quality Scorer

Internal scorer sub-agent that evaluates generated test function code using a 5-criteria quality rubric. Forked by `test-plan.case-implement` in Step 5.6.

## Usage

This skill is not user-invocable. It is called by:
- `test-plan.case-implement` (Step 5.6) for quality assurance of generated tests

## Inputs

### From arguments
Parse `$ARGUMENTS` to extract:
1. **`--test-code-file`**: Path to file containing generated test code
2. **`--tc-file`**: Path to TC-*.md specification
3. **`--conventions-file`**: Path to repository conventions markdown
4. **`--framework`**: Test framework (pytest, Go testing, Jest, etc.)
5. **`--output-file`**: Path where assessment should be written (for revision feedback)
6. **`--calibration-file`**: Path to preloaded calibration examples from
   `load_calibration.py` (parent writes JSON `.calibration_text` to this file; this
   skill has no Bash). Read it as score anchors. Do not glob `calibration/`. Adding a
   pair is a new file under `calibration/core/`, `calibration/ui/`, or
   `calibration/<team>/` — no SKILL.md edit.

## Process

### Step 1: Read Scoring Instructions

Read the detailed scoring rubric from `${CLAUDE_SKILL_DIR}/prompts/score-test-function.md`.

### Step 2: Execute Scoring

Apply the prompt with substitutions:
- `{TEST_CODE_FILE}` = `--test-code-file` argument
- `{TC_FILE}` = `--tc-file` argument
- `{CONVENTIONS_FILE}` = `--conventions-file` argument
- `{FRAMEWORK}` = `--framework` argument
- `{OUTPUT_FILE}` = `--output-file` argument
- `{CALIBRATION_FILE}` = `--calibration-file` argument (Read this file as score anchors)

The scoring rubric evaluates:
1. **Coverage** (0-2): All TC requirements implemented?
2. **Assertions** (0-2): Specific and meaningful?
3. **Convention Adherence** (0-2): Follows repo patterns?
4. **Test Data** (0-2): Uses realistic values from TC?
5. **Code Quality** (0-2): Clean, no excessive TODOs?

### Step 3: Write Assessment to File

Write the structured markdown assessment to the `--output-file` path.

The output includes:
- Per-criterion scores with issues
- Total score (0-10)
- Verdict (Ready/Good/Revise/Rework)
- Coverage analysis (preconditions, steps, assertions implemented)
- Specific issues found
- Revision recommendations (if needed)

**IMPORTANT**: The orchestrating skill needs this file to:
1. Extract the verdict to decide if revision is needed
2. Extract specific issues to pass as feedback to the test generator
3. Keep an audit trail of quality assessments

## What This Skill Does NOT Do

- Does NOT modify the generated test code (only assesses it)
- Does NOT trigger auto-revision (that's handled by the orchestrating skill)
- Does NOT make the revision decision (returns verdict, orchestrating skill decides)
- For scoring + auto-revision, the orchestrating skill (`test-plan.case-implement`) handles the revision loop

$ARGUMENTS
