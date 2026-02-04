---
name: lab-notebook
description: This skill should be used when creating a new experiment, starting lab notebook, recording experimental results, documenting observations, or exporting notebooks to PDF/typst. Triggered by requests like "start experiment", "create lab notebook", "record results", "新しい実験を始める", "export notebook to PDF", "typst出力", "PDFに変換", or "notebook to PDF". For PDF export, use scripts/notebook_to_pdf.sh (pandoc + typst).
---

# Lab Notebook Management

## Overview

Provides lab notebook creation and management for individual bioinformatics experiments. Supports both Jupyter notebooks (.ipynb) for Python-based experiments and Markdown (.md) for non-Python experiments.

## Core Capabilities

### 1. Create New Lab Notebook

Create a new experiment notebook using templates through **interactive dialogue** to ensure high-quality, narrative documentation.

**When to use**: When starting a new experiment or analysis.

**CRITICAL PRINCIPLE**: Do NOT simply copy templates with placeholders. Engage in **interactive dialogue** with the user to create narrative content for each section, especially:
- Experiment purpose and objectives
- Background information and context
- Experimental procedures
- Results interpretation and discussion (after execution)

**Workflow**:

#### Step 1: Basic Setup
1. Determine experiment number (check existing `notebook/labnote/` files)
2. Ask user:
   - Experiment title/description
   - Format preference (Jupyter vs Markdown)

#### Step 2: Interactive Content Creation - Core Questions

**MANDATORY: Ask these core questions** to build high-quality narrative content. Do NOT skip any question.

**2.1 Purpose & Motivation** (fills Background):
- "What problem or question does this experiment address?"
- "Why is this important to the broader research goal?"
- "What motivated you to run this experiment now?"

**2.2 Prior Work & Context** (fills Background):
- Check `STEERING.md` and previous notebooks for related experiments
- "What prior experiments led to this? (e.g., Exp01 showed X, so now we test Y)"
- "What literature findings inform this experiment?"
- "How does this fit into the overall research narrative?"

**2.3 Hypothesis & Expected Outcome** (fills Hypothesis):
- "What is your testable prediction?"
- "What specific outcome do you expect?"
- Engage in dialogue to refine:
  - Is it specific enough? (variables, relationships, expected magnitude)
  - Is it testable with available data/methods?
- Reference `references/notebook-guidelines.md` for quality standards

**2.4 Success Criteria & Effect Size** (fills Hypothesis/Methods):
- "What quantitative change would confirm success?" (e.g., fold-change > 2, p < 0.05, AUC > 0.8)
- "What is the minimum effect size you consider biologically meaningful?"
- "How will you know if the experiment 'worked'?"

**2.5 Primary Endpoints** (fills Methods):
- "What are the main measurements or variables?"
- "Which endpoint is most critical to the hypothesis?"

**2.6 Controls & Replication** (fills Methods):
- "What are the control conditions (positive/negative controls)?"
- "How many replicates will you run?"
- "What normalization or baseline comparisons will you use?"

**2.7 Anticipated Risks & Rescue Plans** (fills Discussion/Next Steps):
- "What could go wrong with this approach?"
- "What alternative methods exist if the primary approach fails?"
- "What confounding factors might affect interpretation?"

**Synthesize Narrative**: Use dialog answers to write Hypothesis and Background as **coherent prose paragraphs**, not bullet lists.

**For Materials and Methods Section**:
- Ask the user about:
  - Data sources and versions
  - Tools and software versions
  - Step-by-step procedure
  - Parameters and settings
- Engage in dialogue to ensure completeness:
  - Are all data sources specified with versions?
  - Are all tools and versions documented?
  - Is the procedure detailed enough for reproducibility?
  - Are all parameters explicitly stated?
- Write narrative text documenting the complete procedure
- Include subsections: Data, Tools, Procedure

**For Results Section**:
- Create placeholder structure
- Note: Results will be filled in after experiment execution
- Include guidance on:
  - Factual observations only (no interpretation)
  - Figure saving best practices (`results/` directory)
  - Quality control documentation

**For Discussion Section**:
- Create placeholder structure with guidance
- Note: Discussion will be filled in after results are available
- Prepare structure for:
  - Interpretation
  - Hypothesis Evaluation
  - Limitations
  - Next Steps

#### Step 3: Template Customization
1. Copy appropriate template:
   - Jupyter: `assets/templates/labnote-template.ipynb` → `notebook/labnote/Exp##_[title].ipynb`
   - Markdown: `assets/templates/labnote-template.md` → `notebook/labnote/Exp##_[title].md`
2. **Replace placeholders** with the narrative content created through dialogue
3. Ensure all sections contain **narrative text**, not just TODO comments

#### Step 4: Post-Creation
1. Update `notebook/tasks.md` with new experiment entry
2. Inform user about:
   - Next steps (filling in results after execution)
   - Quality standards to maintain
   - When to return for discussion section completion

**Naming convention**:
```
Exp##_[brief-description].ext

Examples:
Exp01_rnaseq-differential-expression.ipynb
Exp02_protein-quantification.md
Exp03_pathway-enrichment.ipynb
```

**Command**: `/research-exp`

### 2. Notebook Structure Guidance

Guide users on proper notebook structure using `references/notebook-guidelines.md`.

**Standard sections**:

1. **Header**:
   - Experiment title (Exp##_[description])
   - Date
   - Experimenter name

2. **Hypothesis**:
   - Testable statement
   - Expected outcome

3. **Background**:
   - Context and rationale
   - Related experiments
   - References

4. **Materials and Methods**:
   - Data sources and versions
   - Tools and versions
   - Step-by-step procedure
   - Parameters

5. **Results**:
   - Observations (factual)
   - Figures and tables
   - Quality control checks

6. **Discussion**:
   - Interpretation
   - Hypothesis evaluation
   - Limitations
   - Next steps

### 3. Quality Checks

Ensure notebooks maintain scientific quality standards.

**Key principles** (from `references/notebook-guidelines.md`):
- **Facts first**: Results section = observations only
- **Separate interpretation**: Discussion section = analysis and reasoning
- **Document everything**: Include failed attempts and unexpected results
- **Reproducibility**: Complete procedure for replication
- **Version control**: Track changes with meaningful commits

**Pre-finalization checklist**:
- [ ] Hypothesis clearly stated
- [ ] Methods reproducible
- [ ] All parameters documented
- [ ] Figures properly labeled
- [ ] Results are factual observations
- [ ] Discussion separates facts from interpretation
- [ ] Limitations acknowledged
- [ ] Next steps identified

### 4. Integration with Workflow

Connect lab notebooks with broader project workflow.

**Before creating notebook**:
- Check `STEERING.md` for current phase and priorities
- Review `notebook/tasks.md` for planned experiments
- Ensure hypothesis aligns with research question

**After completing experiment**:
- **CRITICAL**: Engage in interactive dialogue to complete Results and Discussion sections
- Update `notebook/tasks.md` with status
- Consider if results warrant report generation (`/research-report`)
- Identify if hypothesis needs refinement (`hypothesis-driven` skill)
- Update `STEERING.md` if experiment completes a milestone

### 5. Post-Execution Checklist (MANDATORY)

When user returns after running the experiment, **ask these questions** to ensure complete documentation:

**5.1 Observation Questions** (ask all):
1. "What are the 3 most important observations from this experiment?"
2. "Were there any unexpected or surprising results?"
3. "Did anything differ from your initial expectations?"

**5.2 Data & Artifact Questions**:
4. "What figures/tables were generated? Please list with file paths."
5. "Where are the output files saved? (expected: `results/exp##_*.{png,csv,etc}`)"
6. "What intermediate files should be preserved?"

**5.3 Quality Control Questions**:
7. "What QC checks were performed? (e.g., normalization, outlier detection)"
8. "Were there any anomalies, warnings, or errors during execution?"
9. "Did all samples/replicates pass QC?"

**5.4 Deviation Questions**:
10. "Did you deviate from the planned procedure? If so, document the changes."
11. "Were any parameters changed from the original plan?"
12. "Any failed attempts or troubleshooting steps to document?"

**5.5 Forward-Looking Questions**:
13. "Based on these results, what is the most logical next step?"
14. "Does this confirm, refute, or modify the original hypothesis?"

Use answers to fill Results and Discussion sections with **narrative content**.

---

### 6. Completing Results Section (Post-Checklist)

When user returns with experimental results, engage in **interactive dialogue** to document observations.

**Workflow**:
1. Review results with the user:
   - What were the key observations?
   - What figures/tables were generated?
   - What quality control checks were performed?
2. Guide factual documentation:
   - Ensure observations are stated factually (no interpretation)
   - Help structure results logically
   - Guide figure saving to `results/` directory
3. Write narrative text documenting observations
4. Reference `references/notebook-guidelines.md` for Results section standards

**Key principles**:
- Results = observations only (Level 1 facts)
- No interpretation in Results section
- All figures must be saved and properly referenced
- Include quality control checks

### 7. Completing Discussion Section (Post-Checklist)

**CRITICAL**: The Discussion section must be created through **interactive dialogue** with the user. Do NOT fill with generic text.

**Workflow**:

#### 6.1 Interpretation
- **Engage in dialogue** about what the results mean:
  - What do these observations mean biologically?
  - How do results relate to the original hypothesis?
  - How do results connect to literature?
  - What mechanistic explanations are plausible?
- **Ask probing questions**:
  - "What does this finding suggest about the biological process?"
  - "How does this relate to what we expected?"
  - "What alternative explanations could account for these results?"
- **Write narrative text** that synthesizes the dialogue into coherent interpretation
- Reference `references/notebook-guidelines.md` for interpretation standards

#### 6.2 Hypothesis Evaluation
- **Engage in dialogue** to evaluate the original hypothesis:
  - Was the hypothesis supported, rejected, or inconclusive?
  - What evidence supports this conclusion?
  - Were there any unexpected findings?
- **Write narrative text** with explicit evaluation:
  - State original hypothesis
  - Present evaluation (supported/rejected/inconclusive)
  - Provide reasoning based on results

#### 6.3 Limitations
- **Engage in dialogue** about constraints and caveats:
  - What are the limitations of this experiment?
  - What confounding variables were not controlled?
  - What are the generalizability constraints?
- **Ask questions**:
  - "What constraints might affect these conclusions?"
  - "What alternative explanations haven't been ruled out?"
  - "What are the limitations of the methods used?"
- **Write narrative text** acknowledging limitations honestly

#### 6.4 Next Steps
- **Engage in dialogue** about follow-up experiments:
  - What questions remain unanswered?
  - What experiments would address these questions?
  - How do next steps build on current findings?
- **Ask questions**:
  - "What would be the most important follow-up experiment?"
  - "What question does this address?"
  - "How does this build on what we learned?"
- **Write narrative text** with specific, actionable next steps

**Key principles**:
- Discussion = interpretation and reasoning (Level 2 statements)
- Must be created through dialogue, not generic text
- Help user develop thoughtful analysis
- Ensure proper separation from Results (facts vs. interpretation)

## Resources

### assets/templates/

- `labnote-template.ipynb`: Jupyter notebook template for Python experiments
- `labnote-template.md`: Markdown template for non-Python experiments

### commands/

- `research-exp.md`: New experiment creation command (`/research-exp`)

### references/

- `notebook-guidelines.md`: Detailed guidelines for each notebook section

## PDF Export

Export Jupyter notebooks to PDF using the provided shell script.

**When to use**: When user requests PDF output from a notebook.

**Script location**: `scripts/notebook_to_pdf.sh`

**Usage**:
```bash
# Basic export (output: Exp01_analysis.pdf)
/path/to/plugins/lab-notebook/scripts/notebook_to_pdf.sh Exp01_analysis.ipynb

# Custom output filename
/path/to/plugins/lab-notebook/scripts/notebook_to_pdf.sh Exp01_analysis.ipynb report.pdf

# Exclude code cells (output only)
/path/to/plugins/lab-notebook/scripts/notebook_to_pdf.sh --no-input Exp01_analysis.ipynb

# Keep intermediate markdown
/path/to/plugins/lab-notebook/scripts/notebook_to_pdf.sh --keep-md Exp01_analysis.ipynb
```

**Workflow**: `.ipynb` → `.md` (nbconvert) → `.pdf` (pandoc + typst)

**Prerequisites**: nbconvert, pandoc, typst
```bash
uv pip install nbconvert
brew install pandoc typst
```

## Usage Notes

### Format Selection

**Use Jupyter (.ipynb) when**:
- Experiment involves Python code
- Need inline visualization
- Require iterative analysis
- Want to execute code cells

**Use Markdown (.md) when**:
- Experiment is non-Python (e.g., command-line tools, R, manual procedures)
- Documentation-heavy with minimal code
- Prefer plain text format
- Simple version control

### Best Practices

1. **One experiment = One notebook**
   - Don't combine multiple experiments in one file
   - Split large experiments into sub-experiments (Exp01a, Exp01b)

2. **Sequential numbering**
   - Exp01, Exp02, Exp03, ...
   - Don't reuse numbers
   - Gaps are OK (deleted experiments)

3. **Descriptive titles**
   - Good: `Exp03_tcga-survival-analysis`
   - Bad: `Exp03_analysis` or `Exp03_test`

4. **Regular commits**
   - Commit after each major step
   - Use meaningful messages
   - Don't commit huge result files (use .gitignore)

5. **Document as you go**
   - Don't wait until the end
   - Record observations immediately
   - Note unexpected findings

### Common Workflow

Typical experiment workflow:

1. **Planning**:
   ```
   /research-status  # Check current priorities
   ```

2. **Creation**:
   ```
   /research-exp  # Create new notebook
   ```

3. **Execution**:
   - Run experiment
   - Document observations
   - Save results

4. **Review**:
   - Check quality standards
   - Update tasks.md

5. **Follow-up**:
   - Refine hypothesis if needed
   - Plan next experiment
   - Generate report if ready
