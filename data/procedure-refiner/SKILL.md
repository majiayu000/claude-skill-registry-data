---
name: procedure-refiner
description: Iteratively refine LA-Bench experimental procedures through validation and regeneration cycles. This skill should be used when improving generated procedures by ID, validating procedure quality against LA-Bench criteria, and managing the refinement loop between procedure-checker and procedure-generator skills. Triggered by requests to refine, improve, or validate LA-Bench procedures in output JSONL files.
---

# Procedure Refiner

## Overview

Manage the iterative refinement of LA-Bench experimental procedures by orchestrating validation and regeneration cycles. This skill handles reading procedures from output JSONL files by ID, coordinating with procedure-checker and procedure-generator skills, and persisting improvements back to the same files.

## When to Use This Skill

Use this skill when:

- Refining generated experimental procedures for specific LA-Bench IDs
- Validating and improving procedures against LA-Bench evaluation criteria
- Managing iterative improvement cycles for multiple procedure entries
- Working with output JSONL files from procedure generation runs

## Core Workflow

### 1. Single Procedure Refinement

To refine a single procedure entry:

1. **Read the current procedure** using `scripts/procedure_io.py`:
   ```bash
   python scripts/procedure_io.py read <output_jsonl_path> <entry_id>
   ```

2. **Validate with procedure-checker skill**:
   - Invoke the `procedure-checker` skill with the current procedure
   - Review validation results for formal and semantic issues

3. **Regenerate if needed** using `procedure-generator` skill:
   - If validation fails, use `procedure-generator` skill to create improved version
   - Provide validation feedback to inform regeneration

4. **Update the output file**:
   ```bash
   python scripts/procedure_io.py update <output_jsonl_path> <entry_id> '<procedure_steps_json>'
   ```

5. **Repeat steps 2-4** until validation passes or maximum iterations reached

### 2. Batch Refinement

To refine multiple entries from an output JSONL file:

1. **Read all entry IDs** from the JSONL file
2. **For each entry ID**, execute the Single Procedure Refinement workflow
3. **Track progress** and maintain iteration counts per entry
4. **Report results** summarizing validation status for all entries

## Iteration Management

**Maximum iterations per entry:** 3-5 iterations recommended to prevent infinite loops

**Iteration strategy:**
- Iteration 1: Initial validation, identify major issues
- Iteration 2: Regenerate with validation feedback
- Iteration 3: Fine-tune remaining issues
- Beyond 3: Only if consistent improvement is observed

**Exit conditions:**
- Validation passes all criteria
- Maximum iterations reached
- No improvement observed between iterations

## Input/Output File Management

### Reading Procedures

Always use the `procedure_io.py` script to read from output JSONL files:

```bash
python scripts/procedure_io.py read <jsonl_path> <entry_id>
```

This ensures:
- Correct parsing of both compact and pretty-printed JSONL
- Consistent data structure handling
- Proper error messages if entry not found

### Writing Procedures

Always use the `procedure_io.py` script to persist changes:

```bash
python scripts/procedure_io.py update <jsonl_path> <entry_id> '<procedure_steps_json>'
```

**Important:** The script preserves all other entries in the JSONL file unchanged.

### File Paths

Common output JSONL file locations:
- `outputs/runs/generated_<timestamp>.jsonl` - Timestamped generation runs
- `outputs/refined/refined_<timestamp>.jsonl` - Refinement results (optional separate output)

## Integration with Other Skills

### procedure-checker Skill

**Purpose:** Validate procedures against LA-Bench criteria and Completed Protocol standards

**Validation includes:**
- Formal constraints (step count, sentence limits)
- Semantic quality (alignment with expected outcomes)
- Completed Protocol criteria (parameter explicitness, reagent flow, physical constraints)

**When to invoke:**
- After reading a procedure from JSONL
- After regenerating a procedure
- To assess current quality before deciding to regenerate

**Expected output:** Validation report with formal and semantic feedback including Completed Protocol assessment

**Gemini Validation Option:**

Before or during validation, offer the user the option to use gemini for an alternative evaluation perspective:

1. **Ask the user:** "Would you like me to also validate this procedure using gemini? (y/n)"

2. **If yes, prepare validation prompt** containing:
   - The procedure steps
   - LA-Bench evaluation criteria
   - Expected final states
   - Any specific validation focus areas

3. **Execute gemini validation:**
   ```bash
   gemini -p "Validate the following experimental procedure against LA-Bench criteria: [procedure details and evaluation criteria]"
   ```

4. **Compare and synthesize results:**
   - Review both Claude's validation (procedure-checker skill) and gemini's evaluation
   - Identify consensus issues (flagged by both)
   - Note divergent perspectives
   - Present unified validation feedback to inform regeneration

**Benefits:**
- Cross-validation with different model perspectives
- May catch issues overlooked by single evaluator
- Provides richer feedback for procedure improvement

### procedure-generator Skill

**Purpose:** Generate or regenerate procedures from LA-Bench input data following Completed Protocol standards

**Generation includes:**
- Quantitative specifications for all parameters
- Complete experimental design
- Logical temporal ordering
- Reproducibility measures
- Completed Protocol requirements (explicit parameters, reagent flow, physical constraints)

**When to invoke:**
- When validation identifies issues requiring regeneration
- When initial procedure quality is insufficient

**Required inputs:**
- LA-Bench input data (from `la-bench-parser` skill)
- Validation feedback from previous iteration (if available)
- Focus areas from Completed Protocol assessment

**Expected output:** New procedure_steps array with enhanced detail level

### la-bench-parser Skill

**Purpose:** Extract input data from LA-Bench JSONL files

**When to invoke:**
- Before regenerating a procedure (to get original input data)
- To retrieve instruction, mandatory_objects, source_protocol_steps, etc.

**Usage:**
```bash
python .claude/skills/la-bench-parser/scripts/parse_labench.py <input_jsonl> <entry_id>
```

## Example Refinement Session

**User request:** "Refine the procedure for public_test_1 in outputs/runs/generated_20251119_082022.jsonl"

**Execution steps:**

1. Read current procedure:
   ```bash
   python scripts/procedure_io.py read outputs/runs/generated_20251119_082022.jsonl public_test_1
   ```

2. Ask user: "Would you like me to also validate this procedure using gemini? (y/n)"

3. Validate the procedure:
   - Always invoke `procedure-checker` skill with the retrieved procedure
   - If user agreed, also run gemini validation:
     ```bash
     gemini -p "Validate the following LA-Bench experimental procedure: [procedure + criteria]"
     ```
   - If both validations used, synthesize and compare results

4. If validation fails:
   - Invoke `la-bench-parser` skill to get original input data
   - Invoke `procedure-generator` skill with input data + validation feedback (from Claude and/or gemini)
   - Update JSONL with new procedure:
     ```bash
     python scripts/procedure_io.py update outputs/runs/generated_20251119_082022.jsonl public_test_1 '<new_steps_json>'
     ```

5. Re-validate with `procedure-checker` skill (and gemini if user opted in)

6. Repeat until validation passes or max iterations reached

7. Report final status to user with summary of both evaluations (if dual validation was used)

## Best Practices

### Avoid Direct JSONL Manipulation

**Do not** read or write JSONL files directly. Always use `procedure_io.py` to ensure:
- Consistent parsing logic
- Proper preservation of file structure
- Error handling for missing entries

### Provide Iteration Context

When regenerating procedures, include:
- Which iteration number (e.g., "Iteration 2 of 5")
- What issues were identified in validation
- What changes are being targeted
- Specific Completed Protocol criteria to address (e.g., "Add missing centrifuge parameters", "Clarify reagent flow")

### Track Improvements

Compare validation scores across iterations:
- Monitor whether issues are being resolved
- Track improvement in Completed Protocol criteria scores
- Detect if regeneration is introducing new issues
- Decide when to stop iterating

### Focus on Completed Protocol Criteria

When validation identifies Completed Protocol issues:
- Parameter explicitness: Add specific values and ranges
- Operation parameters: Complete all missing parameters (speed, time, temperature, etc.)
- Reagent flow: Clarify defines/kills for each operation
- Physical constraints: Verify container capacities and volumes
- Termination criteria: Quantify ambiguous conditions

### Handle Errors Gracefully

If `procedure_io.py` returns errors:
- Verify file path exists
- Check that entry ID is correct
- Ensure JSONL file format is valid

## Resources

### scripts/procedure_io.py

Python script for JSONL file I/O operations supporting:

- **Read mode:** Extract a single procedure entry by ID
- **Update mode:** Modify an existing entry's procedure_steps
- **Write mode:** Add new entry or update existing (upsert operation)

**CLI usage:**
```bash
# Read
python scripts/procedure_io.py read <jsonl_path> <entry_id>

# Update
python scripts/procedure_io.py update <jsonl_path> <entry_id> '<procedure_steps_json>'

# Write (upsert)
python scripts/procedure_io.py write <jsonl_path> <entry_id> '<procedure_steps_json>'
```

**Python API:**
```python
from procedure_io import read_procedure, update_procedure, write_procedure

# Read
entry = read_procedure("outputs/runs/generated.jsonl", "public_test_1")

# Update
success = update_procedure("outputs/runs/generated.jsonl", "public_test_1", new_steps)

# Write
success = write_procedure("outputs/runs/generated.jsonl", "public_test_1", new_steps)
```
