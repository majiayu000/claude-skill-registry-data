---
name: ats-review
description: Analyze resume against job description for ATS optimization and keyword gaps
---

# ATS Review Skill

Score a resume against a job description. Identify keyword gaps, suggest improvements, and estimate ATS pass likelihood.

## When to Use

- Before submitting an application
- When response rates are low
- To understand why applications aren't getting traction

## Process

### 1. Extract Job Requirements

From the job description, identify:

**Hard Requirements** (must-have):
- Required years of experience
- Required technologies/tools
- Required certifications/degrees
- Deal-breakers if missing

**Soft Requirements** (nice-to-have):
- Preferred skills
- Bonus qualifications
- Culture fit indicators

**Keywords** (exact matches matter):
- Technical terms (languages, frameworks, tools)
- Role-specific jargon
- Industry terminology

### 2. Analyze Resume

Score the resume on:

| Category | Weight | Description |
|----------|--------|-------------|
| **Keyword Match** | 30% | Exact keyword presence from job description |
| **Experience Alignment** | 25% | Years + relevance of experience |
| **Skills Coverage** | 20% | Hard requirements coverage |
| **Achievement Evidence** | 15% | Quantified results, not just duties |
| **Format Compatibility** | 10% | ATS-parseable format |

### 3. Generate Report

```markdown
## ATS Score: [X/100]

### Keyword Analysis
**Present**: [keywords found in resume]
**Missing**: [critical keywords not in resume]
**Partial**: [related but not exact matches]

### Gap Analysis
1. [Most critical gap and how to address it]
2. [Second gap]
3. [Third gap]

### Quick Wins
- [Easy change that would improve score]
- [Another easy change]

### Recommendation
[STRONG MATCH / MODERATE MATCH / WEAK MATCH / NOT RECOMMENDED]

[Brief explanation of recommendation]
```

## Scoring Guidelines

- **90-100**: Excellent match, high likelihood of passing ATS
- **75-89**: Good match, likely to pass with minor tweaks
- **60-74**: Moderate match, needs keyword optimization
- **40-59**: Weak match, significant gaps to address
- **Below 40**: Not recommended, fundamental mismatch

## Important Notes

- ATS systems vary widely; this is a heuristic, not a guarantee
- Keyword stuffing backfires if a human reviews it
- Focus on honest representation of actual skills
- Some gaps can be addressed in cover letter instead

## Example Output

```markdown
## ATS Score: 72/100

### Keyword Analysis
**Present**: Python, machine learning, data analysis, SQL, AWS
**Missing**: Kubernetes, CI/CD, Airflow
**Partial**: "distributed systems" (resume says "parallel computing")

### Gap Analysis
1. **Kubernetes** - Listed as required. If you have any container orchestration experience (Docker Swarm, ECS), mention it and add "familiar with Kubernetes concepts"
2. **CI/CD** - Do you use GitHub Actions, Jenkins, etc.? Add this explicitly
3. **Airflow** - If you've used any workflow orchestration, mention it

### Quick Wins
- Add "CI/CD" to your skills section (you mention GitHub Actions in a bullet point)
- Change "parallel computing" to include "distributed systems"

### Recommendation
MODERATE MATCH

Strong technical foundation but missing some DevOps/MLOps keywords they're looking for. Worth applying if you can honestly add the CI/CD reference.
```

## Anti-Patterns

- Don't recommend adding skills the candidate doesn't have
- Don't optimize so heavily the resume becomes unreadable
- Don't ignore the "why" - a 95 score on a miserable job is still miserable
- Don't treat ATS score as the only factor
