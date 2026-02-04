---
name: experiment-report
description: This skill should be used when generating integrated reports from lab notebooks, improving existing reports, or exporting reports to PDF/typst. Triggered by requests like "generate report", "create summary", "refine report", "improve report", "export to PDF", "typst出力", "PDFに変換", "レポートを作成", or "export report to PDF". For PDF export, use scripts/export_pdf.sh (pandoc + typst).
---

# Experiment Report Management

## Overview

Provides comprehensive report generation and refinement capabilities. Following the skill-creator pattern, this plugin handles both:
1. **Init (Generation)**: Mechanical extraction and templating from lab notebooks
2. **Refine (Improvement)**: AI-guided improvement for scientific rigor and clarity

## Core Capabilities

### 1. Report Generation

Create integrated reports from completed lab notebooks using `init_report.py`.

**Execution context**: All commands assume execution from **project root** (where STEERING.md is located).

**When to use**: When ready to synthesize multiple experiments into a cohesive report.

#### Pre-Generation Checklist (MANDATORY)

Before running init_report.py, verify these requirements:

**Step 1: Notebook Completeness**
- [ ] All included notebooks have completed Results sections
- [ ] All included notebooks have completed Discussion sections
- [ ] All figures saved to `results/exp##/` directory

**Step 2: Project Alignment**
- [ ] Report scope aligns with STEERING.md objectives
- [ ] Primary hypothesis/research question identified
- [ ] Notebooks collectively address the research question

**Step 3: Evidence Verification**
- [ ] List all figures needed for each finding
- [ ] Verify figure paths exist: `ls ../results/exp##/`
- [ ] Identify key statistics for each claim
- [ ] Note any missing evidence to address

**Pre-Generation Questions** (ask user):
1. "Which experiments are included?" (list Exp## numbers)
2. "Is the Discussion section complete in each notebook?"
3. "What is the main research question this report addresses?"
4. "What are the 2-3 key claims you want to make?"
5. "Are all figures saved to results/exp##/ directories?"

#### Workflow

1. Complete pre-generation checklist above
2. Run init script (from project root):
   ```bash
   # If plugin repo is cloned via ghq:
   python ~/ghq/github.com/dakesan/bioinformatics-research-plugins/plugins/experiment-report/scripts/init_report.py \
     --labnote notebook/labnote/Exp*.ipynb --output notebook/report/

   # Or copy script to project and run locally:
   python scripts/init_report.py --labnote notebook/labnote/Exp*.ipynb --output notebook/report/
   ```
3. Script generates template with claim-evidence structure
4. Fill in evidence tables for each finding (verify paths exist)
5. Complete quality gate checklists in each section
6. Output: `notebook/report/Report_[title].md`

**Mapping rules** (from lab notebooks to report):

| Lab Notebook Section | Report Section | Transformation |
|---------------------|----------------|----------------|
| Hypothesis + Background | Background | Synthesize context |
| Materials & Methods | Methods Summary | Consolidate procedures |
| Results (observations) | Findings | Structure by theme |
| Discussion (interpretation) | Synthesis | Integrate interpretations |
| Limitations | Limitations | Consolidate caveats |
| Next Steps | Future Directions | Prioritize follow-ups |
| Key conclusion | Executive Summary | Distill to 3-5 sentences |

**Command**: `/research-report`

### 2. Report Refinement

Improve existing reports using `references/refinement-guide.md` criteria.

**When to use**: After initial report generation or when report needs improvement.

**Workflow**:
1. User specifies existing report to refine
2. Read current report content
3. Evaluate against refinement criteria:
   - **Structure**: Logical flow, clear sections
   - **Scientific rigor**: Fact/interpretation separation, evidence-based claims
   - **Clarity**: Concise writing, proper terminology
4. Provide specific improvement suggestions
5. Implement improvements (with user approval)

**Refinement dimensions**:

1. **Structure & Organization**:
   - Executive Summary: 3-5 sentences, captures essence
   - Logical flow: Each section builds on previous
   - Redundancy: No unnecessary repetition
   - Completeness: All findings addressed

2. **Scientific Accuracy**:
   - Facts vs interpretation: Clearly separated
   - Evidence: Every claim supported by data
   - Limitations: Acknowledged appropriately
   - Alternatives: Considered and discussed
   - Statistics: Properly reported

3. **Writing Quality**:
   - Clarity: Precise, unambiguous language
   - Conciseness: Efficient communication
   - Terminology: Consistent and appropriate
   - Figures: Properly referenced
   - Citations: Accurate and complete

**Command**: `/research-refine`

### 3. Report Structure

Standard report structure:

```markdown
# [Report Title]

**Date**: YYYY-MM-DD
**Report Type**: Integrated Analysis Report

---

## Executive Summary

[3-5 sentences capturing key findings and implications]

## Background

[Research question, context, and rationale]

## Materials and Methods

[Consolidated methods from experiments]

## Findings

### Finding 1: [Title]
- **Observation**: [Factual description]
- **Evidence**: [Lab notebook references, figures]

### Finding 2: [Title]
[Repeat structure]

## Synthesis

[Integrated interpretation of findings]

## Limitations

[Acknowledged constraints and caveats]

## Future Directions

[Prioritized next steps]

## Conclusion

[Final synthesis and key takeaways]

## References

[Citations]

---

## Appendix

### Lab Notebooks
- Exp01_[name].ipynb
- Exp02_[name].md

### Supplementary Figures
[Links]
```

### 4. Quality Standards

Reports maintain separation between facts and interpretation (from research-project quality-standards.md):

**In Findings section** (Level 1: Facts):
- Present observations directly
- Reference source notebooks
- Include exact measurements
- Avoid interpretation

**In Synthesis section** (Level 2: Interpretation):
- Connect observations to meaning
- Cite supporting evidence
- Acknowledge assumptions
- Consider alternatives

**In Conclusion section** (Level 3: Broader implications):
- Synthesize evidence
- State confidence appropriately
- Suggest applications
- Identify unknowns

### 5. Figure Integration

Integrate figures from lab notebooks and analysis outputs into reports.

**Figure sources**:
- Jupyter notebooks: Inline outputs saved to `results/exp##/`
- Command-line tools: Output images in `results/exp##/`
- External analysis: Imported figures with proper attribution

**Directory structure**:
```
notebook/
├── labnote/
│   ├── Exp01_analysis.ipynb
│   └── Exp02_validation.md
├── report/
│   └── Report_Exp01-02_integrated.md
└── results/
    ├── exp01/
    │   ├── fig01_heatmap.png
    │   └── fig02_volcano.png
    └── exp02/
        └── fig01_validation.png
```

**Markdown figure syntax**:
```markdown
![Figure 1: Heatmap of differential expression](../results/exp01/fig01_heatmap.png)

*Figure 1: Heatmap showing top 50 differentially expressed genes (Exp01).*
```

**Figure naming convention**:
- Format: `fig##_description.{png,pdf,svg}`
- Examples: `fig01_heatmap.png`, `fig02_volcano_plot.pdf`
- Use descriptive names for clarity

**Best practices**:
1. Save all figures to `results/exp##/` during experiment execution
2. Use relative paths from report location (`../results/...`)
3. Include figure captions with experiment reference
4. Prefer PNG for raster, PDF/SVG for vector graphics
5. Number figures sequentially within each experiment

**Extracting figures from Jupyter notebooks**:
```python
# In notebook cell, save figure explicitly
import matplotlib.pyplot as plt
fig.savefig('../results/exp01/fig01_heatmap.png', dpi=150, bbox_inches='tight')
```

### 6. PDF Export

Export final reports to PDF using the provided shell script.

**When to use**: When user requests PDF output from a report.

**Script location**: `scripts/export_pdf.sh`

**Usage**:
```bash
# Basic export (output: Report_Exp01-02_integrated.pdf)
/path/to/plugins/experiment-report/scripts/export_pdf.sh Report_Exp01-02_integrated.md

# Custom output filename
/path/to/plugins/experiment-report/scripts/export_pdf.sh Report_Exp01-02_integrated.md custom_output.pdf
```

The script automatically:
- Detects template location (`assets/templates/report.typ`)
- Validates prerequisites (pandoc, typst)
- Reports file size on success

**Prerequisites**: pandoc, typst
```bash
brew install pandoc typst
```

**Export workflow**:
1. Complete and refine Markdown report
2. Verify all figure paths are correct (relative paths)
3. Run the shell script
4. Review PDF output for formatting issues
5. Iterate if needed

**Troubleshooting**:
- **Missing figures**: Check relative paths from report directory
- **Font issues**: Ensure typst has access to required fonts
- **Long tables**: Consider splitting or using landscape orientation

## Workflow Patterns

### Pattern 1: Single Experiment Report

**Scenario**: Document one completed experiment

**Steps**:
1. Ensure lab notebook complete
2. Run: `/research-report` specifying single notebook
3. Review generated report
4. Refine: `/research-refine` to improve clarity

**Use case**: Individual experiment worthy of formal documentation

### Pattern 2: Integrated Multi-Experiment Report

**Scenario**: Synthesize multiple related experiments

**Steps**:
1. Identify notebooks to include (e.g., Exp01-Exp05)
2. Run: `/research-report` specifying all notebooks
3. Script extracts and consolidates content
4. AI synthesizes findings across experiments
5. Refine: `/research-refine` to improve integration

**Use case**: Project milestone, manuscript preparation

### Pattern 3: Iterative Refinement

**Scenario**: Improve existing report quality

**Steps**:
1. Identify report needing improvement
2. Run: `/research-refine` on existing report
3. Review suggestions organized by category:
   - Structure improvements
   - Scientific rigor issues
   - Writing clarity enhancements
4. Approve and implement changes
5. Iterate if needed

**Use case**: Preparing for presentation, submission, or review

## Resources

### scripts/

- `init_report.py`: Report generation script (executable)

### commands/

- `research-report.md`: Report generation command (`/research-report`)
- `research-refine.md`: Report refinement command (`/research-refine`)

### references/

- `mapping-rules.md`: Lab notebook → report section mapping
- `refinement-guide.md`: Quality criteria for report improvement

## Usage Notes

### Generation Best Practices

1. **Timing**: Generate reports when:
   - Multiple related experiments complete
   - Ready for project milestone
   - Preparing manuscript
   - Need formal documentation

2. **Scope**: Include notebooks that:
   - Address related questions
   - Build on each other
   - Collectively tell a story

3. **Preparation**: Before generating:
   - Ensure all lab notebooks complete
   - Review notebook quality
   - Identify key findings

### Refinement Best Practices

1. **Multiple passes**: Refine in stages:
   - First pass: Structure and organization
   - Second pass: Scientific rigor
   - Third pass: Writing quality

2. **Specific feedback**: Request targeted improvements:
   - "Improve executive summary"
   - "Check fact/interpretation separation"
   - "Enhance clarity in Methods"

3. **Version control**: Commit before and after refinement

### Common Improvements

**Executive Summary**:
- ❌ Too long (>5 sentences) or too vague
- ✅ Concise (3-5 sentences), captures essence

**Findings**:
- ❌ Mixed facts and interpretation
- ✅ Pure observations, references to notebooks

**Synthesis**:
- ❌ Unsupported claims, circular reasoning
- ✅ Evidence-based, acknowledges limitations

**Limitations**:
- ❌ Missing or too apologetic
- ✅ Honest, constructive, identifies solutions

**Future Directions**:
- ❌ Vague ("more research needed")
- ✅ Specific next experiments with rationale

### Integration with Workflow

**Typical flow**:
1. Complete experiments → Lab notebooks (lab-notebook)
2. Refine hypotheses → Hypothesis validation (hypothesis-driven)
3. Generate report → Synthesis (experiment-report: init)
4. Improve quality → Refinement (experiment-report: refine)
5. Update project → STEERING.md (research-project)

**Report triggers phase transitions**:
- Generating report often signals end of Execution phase
- Moving to Integration or Publication phase
- Update STEERING.md accordingly

## Examples

### Example 1: Quick Single-Experiment Report

```
User: "Create a report for Exp03"