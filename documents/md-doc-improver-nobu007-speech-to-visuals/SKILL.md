---
name: md-doc-improver
description: >
  Technical documentation improvement skill that provides purpose-oriented, multi-perspective
  review and iterative enhancement of markdown documents. Use when you need to improve the quality,
  completeness, and usability of technical documentation such as API docs, README files, guides,
  or tutorials. The skill analyzes documents from technical, UX, and educational perspectives
  and provides actionable improvement recommendations through an iterative self-improvement loop.
---

# MD Document Improver

## Overview

The MD Document Improver skill systematically enhances technical markdown documentation through multi-perspective analysis and iterative improvement loops. It evaluates documents from technical accuracy, user experience, and educational effectiveness viewpoints, providing comprehensive quality assessment and actionable enhancement recommendations.

## Quick Start

### Basic Document Improvement
```bash
# Improve a markdown document with default settings
python md-doc-improver/scripts/improve_document.py README.md

# Custom settings
python md-doc-improver/scripts/improve_document.py docs/api.md \
  --max-iterations 3 \
  --threshold 0.85 \
  --output-dir ./reviews
```

### Document Validation
```bash
# Validate document quality
python md-doc-improver/scripts/document_validator.py README.md

# Export validation results
python md-doc-improver/scripts/document_validator.py README.md \
  --export-json validation_results.json \
  --severity error,warning
```

## Core Capabilities

### 1. Multi-Perspective Analysis System

The skill evaluates documents from three complementary perspectives:

#### Technical Reviewer (40% weight)
- **Accuracy**: Code syntax, technical claims, API references
- **Completeness**: Error handling, security considerations, performance
- **Best Practices**: Industry standards, framework conventions
- **Technical Depth**: Appropriate level of technical detail

#### UX Writer (30% weight)
- **Clarity**: Readability, language quality, unambiguous explanations
- **Information Architecture**: Logical flow, organization, navigation
- **User Focus**: Task-oriented content, practical examples
- **Visual Structure**: Formatting, consistency, scannability

#### Educational Designer (30% weight)
- **Learning Progression**: Concept building, simple to complex
- **Example Quality**: Diverse, practical, working examples
- **Knowledge Retention**: Reinforcement, practice opportunities
- **Accessibility**: Beginner-friendly, clear prerequisites

### 2. Purpose-Driven Improvement Framework

#### Document Purpose Analysis
- **Objective Identification**: What should users be able to do?
- **Target Audience Definition**: Who is this documentation for?
- **Success Criteria**: How do we know the documentation is effective?
- **Use Case Mapping**: What specific tasks and scenarios are covered?

#### Improvement Prioritization Matrix

| Priority Level | Impact | Effort | Focus Areas |
|---------------|--------|--------|-------------|
| **Critical** | High | Low | Missing required sections, code errors |
| **High** | High | Medium | Example quality, error coverage |
| **Medium** | Medium | Low | Structure improvements, language clarity |
| **Low** | Low | Any | Minor formatting, cosmetic improvements |

### 3. Iterative Self-Improvement Loop

#### Improvement Cycle Structure
```
Iteration N:
  1. Document Analysis → DocumentAnalysis
  2. Multi-Perspective Review → List[ReviewResult]
  3. Score Calculation → Overall Quality Score
  4. Improvement Planning → ImprovementPlan
  5. Plan Execution → Enhanced Document
  6. Convergence Check → Continue or Exit
```

#### Convergence Criteria
- **Quality Threshold**: Overall score ≥ 0.85 (default)
- **Diminishing Returns**: Improvement < 0.05 between iterations
- **Maximum Iterations**: 5 iterations (configurable)
- **User Satisfaction**: Manual acceptance at any point

## Usage Patterns

### Pattern 1: New Document Enhancement
**When to use**: Creating or significantly revising technical documentation

**Workflow**:
1. **Initial Assessment**: `document_validator.py` for baseline quality
2. **Improvement Loop**: `improve_document.py` for systematic enhancement
3. **Final Validation**: `document_validator.py` for quality verification
4. **Review Integration**: Incorporate human feedback and recommendations

**Example**:
```bash
# Step 1: Assess current quality
python md-doc-improver/scripts/document_validator.py new_api_docs.md

# Step 2: Run improvement process
python md-doc-improver/scripts/improve_document.py new_api_docs.md \
  --max-iterations 4 \
  --threshold 0.85

# Step 3: Final validation
python md-doc-improver/scripts/document_validator.py new_api_docs.md \
  --export-json final_validation.json
```

### Pattern 2: Quality Audit and Maintenance
**When to use**: Periodic quality checks for existing documentation

**Workflow**:
1. **Batch Validation**: Validate multiple documents
2. **Quality Dashboard**: Aggregate results and identify trends
3. **Targeted Improvements**: Focus on documents below quality thresholds
4. **Continuous Monitoring**: Set up periodic validation schedules

**Example**:
```bash
# Validate all documentation in a directory
for file in docs/*.md; do
  python md-doc-improver/scripts/document_validator.py "$file" \
    --export-json "validation_$(basename "$file" .md).json"
done

# Identify documents needing improvement
grep -l '"overall_score": [0-7]\.' validation_*.json
```

### Pattern 3: Integration with Development Workflow
**When to use**: Automated quality checks in CI/CD pipelines

**Workflow**:
1. **Pre-commit Validation**: Check documentation changes before commits
2. **PR Validation**: Validate documentation in pull requests
3. **Release Validation**: Ensure documentation meets quality standards
4. **Continuous Monitoring**: Track quality metrics over time

**Example** (CI/CD integration):
```yaml
# GitHub Actions example
- name: Validate Documentation Quality
  run: |
    python md-doc-improver/scripts/document_validator.py docs/*.md \
      --severity error,warning \
      --format json \
      --export-json validation_report.json

    # Fail build if quality is too low
    score=$(jq '.overall_score' validation_report.json)
    if (( $(echo "$score < 0.7" | bc -l) )); then
      echo "Documentation quality too low: $score"
      exit 1
    fi
```

## Quality Scoring System

### Overall Score Composition
```
Overall Score = (
  Accuracy × 0.30 +
  Completeness × 0.30 +
  Clarity × 0.25 +
  Usability × 0.15
)
```

### Score Interpretation
- **0.90-1.00**: Excellent - Production-ready, comprehensive documentation
- **0.80-0.89**: Good - High quality with minor improvements needed
- **0.70-0.79**: Fair - Functional but needs significant improvement
- **0.60-0.69**: Poor - Major issues affecting usability
- **0.00-0.59**: Very Poor - Incomplete or incorrect documentation

### Dimension Breakdown

#### Accuracy (30%)
- Code example correctness (40%)
- Technical information accuracy (25%)
- Error handling coverage (25%)
- Security and performance considerations (20%)

#### Completeness (30%)
- Required sections coverage (35%)
- Content depth and explanation quality (30%)
- User journey coverage (20%)
- Edge case and exception handling (15%)

#### Clarity (25%)
- Information architecture and flow (25%)
- Language quality and consistency (25%)
- Visual structure and formatting (25%)
- Navigation and accessibility (25%)

#### Usability (15%)
- Task completion guidance (30%)
- Example quality and variety (25%)
- Troubleshooting support (25%)
- Learning effectiveness (20%)

## Advanced Features

### Custom Quality Thresholds
```bash
# Production documentation (high standards)
python md-doc-improver/scripts/document_validator.py docs/api.md \
  --threshold 0.90

# Internal documentation (moderate standards)
python md-doc-improver/scripts/document_validator.py internal/guide.md \
  --threshold 0.75

# Draft documentation (minimum standards)
python md-doc-improver/scripts/document_validator.py draft/tutorial.md \
  --threshold 0.60
```

### Document Type Customization
The skill automatically adapts its evaluation criteria based on document content:

#### API Documentation Focus
```python
api_weights = {
    'technical': 0.6,    # Higher emphasis on accuracy
    'ux': 0.2,          # Lower emphasis on educational aspects
    'educational': 0.2  # Lower emphasis on learning progression
}
```

#### Tutorial Documentation Focus
```python
tutorial_weights = {
    'technical': 0.2,    # Lower emphasis on deep technical accuracy
    'ux': 0.3,          # Higher emphasis on user experience
    'educational': 0.5  # Highest emphasis on learning effectiveness
}
```

### Export and Integration
```bash
# Export detailed analysis for custom processing
python md-doc-improver/scripts/improve_document.py README.md \
  --export-json improvement_analysis.json

# Integration with external tools
python md-doc-improver/scripts/document_validator.py README.md \
  --format json | jq '.issues[] | select(.severity == "error")'
```

## Resources

### scripts/
Core automation scripts for document improvement and validation.

#### `improve_document.py`
Main improvement engine that implements the iterative enhancement loop. Performs multi-perspective analysis, generates improvement plans, and applies systematic enhancements through configurable iterations.

#### `document_validator.py`
Comprehensive validation tool that assesses document quality across multiple dimensions. Provides detailed scoring, issue identification, and actionable recommendations for improvement.

### references/
Detailed documentation and framework specifications.

#### `improvement_framework.md`
Comprehensive guide to the improvement methodology, including multi-perspective review system, quality metrics, and implementation details. Essential for understanding how the skill makes improvement decisions.

#### `quality_standards.md`
Complete specification of quality criteria, scoring rubrics, and evaluation standards. Defines what constitutes high-quality technical documentation and how it's measured.

## Best Practices

### Before Using This Skill
1. **Define Purpose**: Clearly understand what the document should help users accomplish
2. **Identify Audience**: Know who will be reading and using the documentation
3. **Set Quality Goals**: Determine appropriate quality thresholds for your use case
4. **Gather Context**: Collect related documentation and standards

### During Improvement Process
1. **Iterative Approach**: Run multiple improvement cycles with human review between iterations
2. **Focus on Impact**: Prioritize improvements that provide the greatest user value
3. **Maintain Voice**: Preserve the original document's tone and style while improving clarity
4. **Validate Changes**: Ensure improvements don't introduce new issues

### After Improvement
1. **Human Review**: Always have technical experts and target users review improvements
2. **Test Examples**: Verify that all code examples work as described
3. **Monitor Feedback**: Collect and incorporate user feedback over time
4. **Regular Updates**: Schedule periodic quality checks and improvements

### Integration Tips
- **CI/CD Integration**: Use validation in pull requests to maintain documentation quality
- **Quality Dashboards**: Track quality metrics across documentation sets
- **Peer Review**: Combine automated improvements with human expertise
- **User Testing**: Validate that improvements actually help users accomplish their tasks

---

**The MD Document Improver skill provides a systematic, evidence-based approach to enhancing technical documentation quality through multi-perspective analysis and iterative improvement.**