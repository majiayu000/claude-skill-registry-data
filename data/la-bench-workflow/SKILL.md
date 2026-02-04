---
name: la-bench-workflow
description: Orchestrate the complete LA-Bench experimental procedure generation workflow from JSONL input to validated output. This skill should be used when processing LA-Bench format experimental data to generate and validate detailed experimental procedures. It coordinates parsing, reference fetching, procedure generation, and quality validation with 10-point scoring.
---

# LA-Bench Workflow

## Overview

Orchestrate the complete LA-Bench experimental procedure generation and validation pipeline. This skill coordinates four specialized components:

1. **la-bench-parser**: Extract experimental data from JSONL
2. **web-reference-fetcher**: Fetch reference materials
3. **procedure-generator**: Generate detailed experimental procedures
4. **procedure-checker**: Validate and score generated procedures (10-point scale)

All intermediate and final outputs are saved to standardized directory structure: `workdir/{filename}_{entry_id}/`

## When to Use This Skill

Use this skill when:
- Processing LA-Bench JSONL files (public_test.jsonl, private_test_input.jsonl, etc.)
- Generating experimental procedures from LA-Bench format data
- Validating generated procedures against LA-Bench quality standards
- Batch processing multiple LA-Bench entries
- Testing or evaluating procedure generation capabilities

## Workflow

### Step 1: Parse LA-Bench Entry

Extract experimental data from JSONL file using la-bench-parser skill.

**Input:**
- JSONL file path (e.g., `data/public_test.jsonl`)
- Entry ID (e.g., `public_test_1`)

**Execution:**
```bash
# Extract filename without extension
filename=$(basename "data/public_test.jsonl" .jsonl)  # "public_test"

# Create working directory
mkdir -p workdir/${filename}_${entry_id}

# Parse entry
python .claude/skills/la-bench-parser/scripts/parse_labench.py \
  data/public_test.jsonl ${entry_id} \
  > workdir/${filename}_${entry_id}/input.json
```

**Output:**
- `workdir/{filename}_{entry_id}/input.json`

**Content:**
- instruction
- mandatory_objects
- source_protocol_steps
- expected_final_states
- references
- measurement.specific_criteria (if available)

### Step 2: Fetch Reference Materials (Optional)

Fetch reference URLs using web-reference-fetcher skill if references exist in input.json.

**Input:**
- Reference URLs from input.json

**Execution:**
```bash
mkdir -p workdir/${filename}_${entry_id}/references

# For each reference URL (ref_1, ref_2, ...)
python3 .claude/skills/web-reference-fetcher/scripts/fetch_url.py \
  "${reference_url}" \
  --output workdir/${filename}_${entry_id}/references/ref_${i}.md
```

**Output:**
- `workdir/{filename}_{entry_id}/references/ref_1.md`
- `workdir/{filename}_{entry_id}/references/ref_2.md`
- ... (one file per reference)

**Note:** If references cannot be fetched or URLs are inaccessible, proceed to Step 3 without reference materials.

### Step 3: Generate Experimental Procedure

Generate detailed procedure using procedure-generator skill.

**Input:**
- `workdir/{filename}_{entry_id}/input.json`
- `workdir/{filename}_{entry_id}/references/ref_*.md` (if available)

**Process:**
1. Read input.json
2. Read all reference files (if exist)
3. Invoke experiment-procedure-generator subagent with detailed prompt
4. Save generated procedure
5. Verify output (≤50 steps, ≤10 sentences/step)

**Output:**
- `workdir/{filename}_{entry_id}/procedure.json`

**Format:**
```json
[
  {"id": 1, "text": "First step with quantitative details..."},
  {"id": 2, "text": "Second step with quantitative details..."},
  ...
]
```

### Step 4: Validate, Score, and Iteratively Improve Procedure

Validate procedure using procedure-checker skill with 10-point scoring system. **Automatically improve procedure until score ≥ 8/10 or maximum iterations reached.**

**Target Quality**: Score ≥ 8/10 points (Good or Excellent)

**Input:**
- `workdir/{filename}_{entry_id}/input.json`
- `workdir/{filename}_{entry_id}/procedure.json`

**Iterative Improvement Process:**

#### Iteration Loop (Max 3 attempts)

For each iteration (attempt 1, 2, 3):

1. **Formal Validation (Script-based)**
   ```bash
   # Create wrapped version
   python3 -c "
   import json
   with open('workdir/${filename}_${entry_id}/procedure.json', 'r') as f:
       steps = json.load(f)
   wrapped = {'procedure_steps': steps}
   with open('workdir/${filename}_${entry_id}/procedure_wrapped.json', 'w') as f:
       json.dump(wrapped, f, ensure_ascii=False, indent=2)
   "

   # Run validation
   python .claude/skills/procedure-checker/scripts/validate_procedure.py \
     workdir/${filename}_${entry_id}/procedure_wrapped.json
   ```

2. **Semantic Evaluation (Subagent-based)**
   - Invoke procedure-semantic-checker subagent
   - Evaluate with 10-point scoring system:
     - Common Criteria (5 points)
     - Individual Criteria (5 points)
   - Generate comprehensive review

3. **Combine Results**
   - Merge formal validation + semantic evaluation
   - Save review to `workdir/{filename}_{entry_id}/review_v{iteration}.md`

4. **Check Score**
   - Extract total score from review
   - If **score ≥ 8**: ✅ **Success** → Proceed to Step 5
   - If **score < 8** AND **iteration < 3**: 🔄 **Improve** → Continue to sub-step 5
   - If **score < 8** AND **iteration = 3**: ⚠️ **Max iterations reached** → Proceed to Step 5 with warning

5. **Generate Improvement Instructions (if score < 8)**

   Extract specific issues from review and create targeted improvement prompt:

   **Analysis:**
   - Read `review_v{iteration}.md`
   - Extract "Critical Issues" section
   - Extract "Must-Fix Recommendations"
   - Identify specific scoring deficiencies:
     - Which common criteria failed? (0-5 points)
     - Which individual criteria failed? (0-5 points)
     - What deductions were applied?
     - Was excessive safety penalty triggered?

   **Improvement Prompt Template:**
   ```
   The previous procedure (v{iteration}) scored {score}/10 points.

   Regenerate the procedure addressing these specific issues:

   ## Failed Common Criteria:
   {list of failed criteria with specific examples from review}

   ## Failed Individual Criteria:
   {list of failed criteria with specific examples}

   ## Critical Issues to Fix:
   {numbered list from review}

   ## Must-Fix Recommendations:
   {numbered list from review}

   ## Specific Corrections Required:
   {detailed corrections extracted from review}

   Maintain all strengths from the previous version while addressing these issues.
   ```

6. **Regenerate Procedure**
   - Invoke procedure-generator skill again
   - Pass improvement instructions to experiment-procedure-generator subagent
   - Save to `workdir/{filename}_{entry_id}/procedure.json` (overwrite)
   - Archive previous version to `workdir/{filename}_{entry_id}/procedure_v{iteration}.json`

7. **Loop Back to Step 4.1** (next iteration)

#### Outputs

**Per Iteration:**
- `workdir/{filename}_{entry_id}/procedure_v{N}.json` (archived versions)
- `workdir/{filename}_{entry_id}/review_v{N}.md` (archived reviews)

**Final:**
- `workdir/{filename}_{entry_id}/procedure.json` (best version)
- `workdir/{filename}_{entry_id}/review.md` (final review, symlink or copy of best)
- `workdir/{filename}_{entry_id}/procedure_wrapped.json` (temporary)

**Review Format:**
- Scoring Results (10-point breakdown)
- Formal Validation Results
- Semantic Quality Assessment
- Identified Strengths
- Issues and Recommendations
- Overall Assessment
- Conclusion
- Iteration History (if multiple attempts)

### Step 5: Report Results

Report completion with comprehensive summary including iteration history:

```
Successfully processed: {entry_id}

Directory: workdir/{filename}_{entry_id}/
├── input.json              ✅
├── references/
│   ├── ref_1.md           ✅ (if applicable)
│   └── ref_2.md           ✅ (if applicable)
├── procedure.json          ✅ (final version)
├── procedure_v1.json      ✅ (if improved)
├── procedure_v2.json      ✅ (if improved)
├── review.md               ✅ (final review)
├── review_v1.md           ✅ (if improved)
└── review_v2.md           ✅ (if improved)

Iteration History:
┌─────────────┬────────┬──────────┬──────────────┬────────────┐
│ Iteration   │ Score  │ Common   │ Individual   │ Status     │
├─────────────┼────────┼──────────┼──────────────┼────────────┤
│ v1 (Initial)│ 6/10   │ 4/5      │ 2/5          │ 🔄 Improve │
│ v2          │ 7/10   │ 5/5      │ 2/5          │ 🔄 Improve │
│ v3 (Final)  │ 8/10   │ 5/5      │ 3/5          │ ✅ Accept  │
└─────────────┴────────┴──────────┴──────────────┴────────────┘

Final Procedure Quality:
- Total Score: 8/10 points (⬆️ +2 from initial)
- Common Criteria: 5/5 points (✅ Perfect)
- Individual Criteria: 3/5 points (Improved from 2/5)
- Rating: ⭐⭐⭐⭐ (Good)
- Recommendation: ✅ ACCEPT
- Iterations Required: 3 attempts

Improvements Made:
1. v1→v2: Fixed calculation errors, improved parameter reflection (+1pt)
2. v2→v3: Enhanced individual criteria compliance (+1pt)

Next Steps: Procedure is ready for use. Review review.md for detailed feedback.
```

**Success Scenarios:**

1. **Immediate Success (Score ≥ 8 on first attempt)**
   ```
   Iteration History: ✅ Single attempt (v1: 9/10)
   Status: Excellent quality achieved immediately
   ```

2. **Improvement Success (Score ≥ 8 after iterations)**
   ```
   Iteration History: 🔄 3 attempts (v1: 6→v2: 7→v3: 8)
   Status: Target quality achieved through iterative improvement
   ```

3. **Partial Success (Score < 8 after max iterations)**
   ```
   Iteration History: ⚠️ 3 attempts (v1: 5→v2: 6→v3: 7)
   Status: Max iterations reached. Best score: 7/10 (Needs manual review)
   Warning: Target quality (8/10) not achieved. Manual refinement recommended.
   ```

## Batch Processing

To process multiple entries from the same JSONL file:

**Example:**
```bash
# Process public_test_1, public_test_2, public_test_3
for entry_id in public_test_1 public_test_2 public_test_3; do
  echo "Processing ${entry_id}..."
  # Run la-bench-workflow skill for each entry
done
```

**Directory Structure:**
```
workdir/
├── public_test_public_test_1/
│   ├── input.json
│   ├── references/
│   ├── procedure.json
│   └── review.md
├── public_test_public_test_2/
│   └── ...
└── public_test_public_test_3/
    └── ...
```

## Error Handling

### Common Issues

**Issue**: JSONL file not found
- **Fix**: Verify file path and ensure it exists

**Issue**: Entry ID not found in JSONL
- **Fix**: Check entry ID spelling and verify it exists in the file

**Issue**: Reference fetch fails
- **Fix**: Proceed without references or use cached references if available

**Issue**: Procedure generation fails formal validation
- **Fix**: Review errors and regenerate with adjusted parameters

**Issue**: Low quality score (<5/10)
- **Fix**: Review semantic evaluation feedback and regenerate with improvements

## Quality Standards

### LA-Bench 10-Point Scoring System

**Common Criteria (5 points):**
1. Parameter Reflection (+1pt): All instruction parameters correctly reflected
2. Object Completeness (+1pt): All mandatory objects used correctly
3. Logical Structure Reflection (+1pt): Source protocol structure maintained
4. Expected Outcome Achievement (+1pt): Final states achievable
5. Appropriate Supplementation (+1pt): Missing details appropriately filled

**Deductions:**
- Unnatural Japanese/Hallucination (-1pt)
- Calculation Errors (-1pt)
- Procedural Contradictions (-1pt)

**Special Restriction:**
- Excessive safety → Common criteria capped at 2pts

**Individual Criteria (5 points):**
- Based on measurement.specific_criteria (if provided)
- General quality assessment (if not provided)

**Quality Thresholds:**
- 9-10 pts: Excellent (⭐⭐⭐⭐⭐) - Ready for use
- 7-8 pts: Good (⭐⭐⭐⭐) - Minor improvements recommended
- 5-6 pts: Needs Improvement (⭐⭐⭐) - Significant revisions needed
- 3-4 pts: Insufficient (⭐⭐) - Major issues
- 0-2 pts: Unacceptable (⭐) - Complete regeneration required

## Best Practices

### General Workflow

1. **Always verify input.json**: Ensure all required fields exist before proceeding
2. **Check reference availability**: Some entries may not have fetchable references
3. **Review formal validation first**: Fix constraint violations before semantic evaluation
4. **Preserve intermediate files**: Keep all outputs for debugging and analysis

### Iterative Improvement

5. **Trust the iteration process**: The workflow automatically iterates up to 3 times to achieve target quality (≥8/10)
6. **Analyze iteration history**: Compare review_v1.md, review_v2.md, review.md to understand improvement trajectory
7. **Learn from failures**: If max iterations reached without target, review all versions to identify persistent issues
8. **Use version control**: Archived versions (procedure_v1.json, procedure_v2.json) allow rollback if needed

### Scoring Strategy

9. **Prioritize common criteria**: These 5 points are achievable through careful attention to input data
10. **Address deductions early**: Fix calculation errors, hallucinations, and contradictions in early iterations
11. **Understand individual criteria**: Read measurement.specific_criteria carefully if provided
12. **Avoid excessive safety**: Don't add unnecessary steps or extreme safety margins (triggers 2pt cap)

### Debugging Low Scores

**If stuck at low scores (<6/10) after iterations:**
- Check if instruction parameters are fully reflected
- Verify all mandatory_objects are used
- Confirm source_protocol_steps logic is preserved
- Validate all calculations manually
- Review for hallucinations or invented information

**If stuck at medium scores (6-7/10):**
- Focus on individual criteria improvements
- Enhance cost efficiency (reduce reagent waste)
- Improve work efficiency (optimize step order)
- Add precision measures (quality controls)

### Batch Processing Best Practices

13. **Process in parallel if possible**: Independent entries can be processed simultaneously
14. **Monitor iteration counts**: High iteration rates may indicate dataset complexity
15. **Compare across entries**: Identify common failure patterns for systematic improvements

## Integration with Other Skills

This skill orchestrates:
- **la-bench-parser** (Step 1): JSONL parsing
- **web-reference-fetcher** (Step 2): Reference retrieval
- **procedure-generator** (Step 3): Procedure generation via experiment-procedure-generator subagent
- **procedure-checker** (Step 4): Validation via validate_procedure.py + procedure-semantic-checker subagent

See individual skill documentation for detailed specifications.

## Directory Naming Convention

All outputs use the standardized pattern: `workdir/{filename}_{entry_id}/`

**Examples:**
| JSONL File | Entry ID | Directory |
|------------|----------|-----------|
| data/public_test.jsonl | public_test_1 | workdir/public_test_public_test_1/ |
| data/private_test_input.jsonl | private_test_5 | workdir/private_test_input_private_test_5/ |
| data/validation.jsonl | exp_042 | workdir/validation_exp_042/ |

**Filename extraction:**
```python
from pathlib import Path
filename = Path("data/public_test.jsonl").stem  # "public_test"
entry_id = "public_test_1"
dir_name = f"{filename}_{entry_id}"  # "public_test_public_test_1"
```

## Example Usage

### Example 1: Immediate Success (Score ≥ 8 on first attempt)

```
User: "Process public_test_1 from data/public_test.jsonl"

Assistant workflow:
1. Parse: Extract entry to workdir/public_test_public_test_1/input.json ✅
2. Fetch: Download 2 references to workdir/public_test_public_test_1/references/ ✅
3. Generate: Create procedure.json (40 steps) ✅
4. Validate (Iteration 1):
   - Formal: ✅ PASSED (40/50 steps, all ≤10 sentences)
   - Semantic: 9/10 points (Common: 5/5, Individual: 4/5)
   - Status: ✅ TARGET ACHIEVED (≥8/10)
5. Report: Procedure rated "Excellent" (⭐⭐⭐⭐⭐)

Result: Single iteration achieved excellent quality
Next: Review workdir/public_test_public_test_1/review.md for detailed feedback
```

### Example 2: Iterative Improvement (Score improves to ≥ 8)

```
User: "Process public_test_5 from data/public_test.jsonl"

Assistant workflow:
1. Parse: Extract entry ✅
2. Fetch: Download references ✅
3. Generate: Create initial procedure ✅
4. Validate and Improve:

   Iteration 1:
   - Formal: ✅ PASSED
   - Semantic: 6/10 points (Common: 4/5, Individual: 2/5)
   - Issues: Missing parameter specifications, incomplete object usage
   - Status: 🔄 IMPROVE (score < 8)

   Iteration 2:
   - Regenerate with fixes for missing parameters
   - Formal: ✅ PASSED
   - Semantic: 7/10 points (Common: 5/5, Individual: 2/5)
   - Issues: Individual criteria still weak (cost efficiency)
   - Status: 🔄 IMPROVE (score < 8)

   Iteration 3:
   - Regenerate with cost efficiency improvements
   - Formal: ✅ PASSED
   - Semantic: 8/10 points (Common: 5/5, Individual: 3/5)
   - Status: ✅ TARGET ACHIEVED

5. Report: Final score 8/10 after 3 iterations (⬆️ +2 from initial)

Result: Iterative improvement achieved target quality
Files: procedure_v1.json, procedure_v2.json, procedure.json (final)
Reviews: review_v1.md, review_v2.md, review.md (final)
```

### Example 3: Partial Success (Max iterations without reaching target)

```
User: "Process complex_experiment_1 from data/validation.jsonl"

Assistant workflow:
1-3. [Parse, Fetch, Generate] ✅
4. Validate and Improve:

   Iteration 1: 5/10 (Critical issues with quantitative accuracy)
   Iteration 2: 6/10 (Improved accuracy, but logical structure issues)
   Iteration 3: 7/10 (Further improvements, but individual criteria still weak)

   Status: ⚠️ MAX ITERATIONS REACHED

5. Report:
   - Best Score: 7/10 (Good, but below target)
   - Recommendation: ⚠️ REVISE with manual review
   - Warning: Automatic improvement could not achieve 8/10
   - Action: Manual refinement recommended

Result: Best effort achieved 7/10
Recommendation: Review all iteration histories to identify persistent issues
```

## Important Context

This workflow is conducted for **academic research purposes** to evaluate and improve experimental planning quality and safety. All generated procedures should prioritize:
- Scientific accuracy
- Reproducibility
- Safety considerations
- Cost and time efficiency
- Adherence to research ethics guidelines
