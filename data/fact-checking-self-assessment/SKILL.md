---
name: fact-checking-self-assessment
description: Provides automated fact-checking, quality assessment, and self-validation capabilities for AI outputs. Use this skill when you need to verify factual claims, assess implementation quality, or ensure outputs meet production standards before delivery.
---

# Fact-Checking & Self-Assessment Skill

This skill provides automated fact-checking, quality assessment, and self-validation capabilities to ensure AI outputs are accurate, functional, and reliable.

## When to Use This Skill

Use this skill when:
- Implementing new features that require factual verification
- Delivering solutions that need quality assurance
- Building systems that require self-validation
- Ensuring outputs meet production standards
- Fact-checking research or technical claims
- Validating implementation completeness

## Skill Capabilities

### 1. Factual Claim Verification
- Extract factual claims from text using pattern recognition
- Verify claims against multiple reliable sources
- Calculate confidence scores based on source credibility
- Identify and flag unverified or conflicting information

### 2. Implementation Quality Assessment
- Validate code syntax and structure
- Test file existence and accessibility
- Check requirements coverage completeness
- Assess functionality and reliability scores
- Generate comprehensive quality reports

### 3. Self-Assessment Framework
- Provide quantitative scoring (0-100 scale)
- Measure accuracy, completeness, functionality, and reliability
- Generate actionable recommendations
- Track quality metrics over time

### 4. Production Readiness Validation
- Ensure outputs meet production standards
- Identify gaps before delivery
- Validate against requirements specifications
- Generate confidence assessments

## How to Use This Skill

### Basic Usage Patterns

1. **For Fact-Checking Text Content:**
   ```
   Use the fact-checking skill to verify these claims:
   - [Your factual claims here]
   - [Include specific claims that need verification]
   ```

2. **For Implementation Assessment:**
   ```
   Use the fact-checking skill to assess this implementation:
   - Task: [Describe the implementation task]
   - Files: [List implementation files]
   - Requirements: [Specify what should be verified]
   ```

3. **For Quality Assurance:**
   ```
   Use the fact-checking skill to validate this solution:
   - Ensure all requirements are met
   - Check code quality and functionality
   - Generate a production readiness report
   ```

### Advanced Usage

#### Custom Configuration
For specific domains or requirements:
1. Adjust confidence thresholds
2. Customize source reliability weights
3. Modify quality metrics criteria
4. Define domain-specific validation rules

#### Integration with Workflows
- Use before task completion for quality gates
- Integrate into CI/CD pipelines for automated validation
- Apply to research tasks for factual accuracy
- Employ for implementation review processes

## Technical Implementation

This skill uses a three-tier architecture:

### 1. Claim Extraction Engine
- Pattern recognition for factual statements
- Context-aware claim identification
- Automated source requirement analysis

### 2. Verification Framework
- Multi-source fact-checking with confidence scoring
- Source reliability classification (official, reputable, community, user)
- Cross-reference validation across sources

### 3. Quality Assessment System
- Comprehensive metrics calculation
- Automated requirement coverage testing
- Production readiness evaluation

## Best Practices

### For Maximum Effectiveness

1. **Provide Clear Context**
   - Include specific task descriptions
   - List all implementation files
   - Define requirements explicitly
   - Specify expected outcomes

2. **Use Appropriate Scope**
   - Break large tasks into smaller assessments
   - Focus on specific aspects (accuracy, functionality, completeness)
   - Use iterative improvement based on feedback

3. **Interpret Results Appropriately**
   - Review confidence scores carefully
   - Address identified gaps before proceeding
   - Use recommendations to guide improvements
   - Re-run assessments after making changes

### Quality Thresholds

- **High Confidence** (90-100%): Ready for production use
- **Medium Confidence** (70-89%): Review recommended before use
- **Low Confidence** (50-69%): Significant improvements needed
- **Needs Review** (<50%): Major gaps identified

## Examples

### Example 1: Research Fact-Checking
```
Use the fact-checking skill to verify these claims about AI market trends:

Claims:
- The global AI market is expected to reach $190 billion by 2025
- Machine learning represents 60% of total AI investment
- Python leads in AI development with 85% market share

Expected Output: Verification of each claim with confidence scores and source analysis
```

### Example 2: Implementation Assessment
```
Use the fact-checking skill to assess this Python data processing implementation:

Task: Create a CSV data processor with error handling
Files: data_processor.py, requirements.txt, README.md
Requirements: File I/O operations, error handling, documentation, testing

Expected Output: Quality assessment with specific areas for improvement
```

### Example 3: Production Readiness Check
```
Use the fact-checking skill to validate this web application for production:

Task: Build a user authentication system
Files: auth.py, config.py, templates/
Requirements: Security validation, error handling, documentation, performance

Expected Output: Production readiness report with confidence score
```

## Limitations and Considerations

### Scope Limitations
- Verification quality depends on available sources
- Complex technical claims may require domain expertise
- Some claims may be inherently uncertain or evolving

### Interpretation Guidelines
- Use confidence scores as guidance, not absolute truth
- Consider source reliability in context
- Apply domain knowledge to interpret results
- Supplement with manual review for critical decisions

### Ethical Considerations
- Verify sources before relying on their information
- Consider potential biases in source materials
- Use responsibly to enhance, not replace, human judgment
- Respect intellectual property and citation requirements

## Continuous Improvement

This skill is designed for iterative improvement:
- Track quality metrics over time
- Refine source reliability assessments
- Enhance pattern recognition capabilities
- Improve recommendation generation
- Adapt to specific domain requirements

For technical questions or enhancement requests, refer to the skill's technical documentation and implementation details.