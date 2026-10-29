---
name: interview-prep
description: Generate tailored interview questions and practice with STAR method feedback
---

# Interview Prep Skill

Generate interview questions tailored to a specific role and practice answering them with feedback.

## When to Use

- After getting an interview scheduled
- When preparing for a specific company/role
- To identify gaps in your interview stories

## Process

### 1. Generate Questions

Based on the resume and job description, generate questions across these categories:

**Behavioral** (1-2 questions):
- "Tell me about a time when..."
- Probe past experiences relevant to the role
- Focus on gaps between resume and job requirements

**Technical** (1-2 questions):
- Specific to the role requirements
- Test depth in claimed areas of expertise
- May include system design or problem-solving

**Situational** (1-2 questions):
- "How would you handle..."
- Test judgment and approach to challenges
- Relevant to the company's context

### 2. Practice Mode

For each answer the user provides, evaluate using **STAR method**:

| Component | What to Look For |
|-----------|------------------|
| **Situation** | Clear context setting (who, what, when, where) |
| **Task** | Your specific responsibility/goal |
| **Action** | What YOU did (not the team), specific steps |
| **Result** | Quantified outcome, what you learned |

### 3. Feedback Format

```markdown
## Question: [The question]

### Your Answer Summary
[Brief paraphrase of their answer]

### STAR Score: [X/10]

**Situation** [score/10]: [feedback]
**Task** [score/10]: [feedback]
**Action** [score/10]: [feedback]
**Result** [score/10]: [feedback]

### Suggestions
1. [Most impactful improvement]
2. [Second improvement]
3. [Optional third improvement]

### Stronger Version
[If helpful, suggest how to restructure the answer]
```

## Question Generation Guidelines

Questions should be:
- **Specific** to this candidate and role, not generic
- **Probing** gaps between resume and requirements
- **Challenging** but fair
- **Relevant** to what this company cares about

Bad: "Tell me about yourself"
Good: "Your resume shows experience with X, but this role requires Y. How would you bridge that gap?"

## STAR Scoring Guidelines

**9-10**: Complete STAR with quantified results and clear learning
**7-8**: Good structure, missing some specificity or quantification
**5-6**: Partial STAR, unclear on some components
**3-4**: Answer present but not structured, hard to follow
**1-2**: Rambling, off-topic, or missing key components

## Common Issues to Flag

- **"We" instead of "I"**: Interview answers should focus on YOUR contributions
- **No numbers**: "Improved performance" vs "Improved latency by 40%"
- **No ending**: Stories that trail off without results
- **Too long**: Answers should be 1-2 minutes, not 5
- **Negativity**: Blaming others or complaining

## Interview Types

Adjust approach based on interview type:

**Phone Screen**: Focus on fit and basic qualifications
**Technical**: Emphasize problem-solving process
**Behavioral**: STAR structure is critical
**System Design**: Framework and trade-off discussion
**Final/Culture**: Values alignment and enthusiasm

## Example Questions by Role Type

**Engineering**:
- "Walk me through a system you designed. What trade-offs did you make?"
- "Tell me about a time you had to debug a difficult production issue"
- "How do you approach code review? Give an example of feedback you gave"

**Data/ML**:
- "Describe a model you deployed. How did you validate it?"
- "Tell me about a time data quality issues affected your work"
- "How do you communicate technical results to non-technical stakeholders?"

**Product/PM**:
- "Tell me about a feature you shipped that didn't succeed"
- "How do you prioritize when everything is urgent?"
- "Walk me through how you'd approach [relevant problem]"

## Anti-Patterns

- Don't generate questions the candidate couldn't possibly answer
- Don't be overly harsh in feedback (this is practice, not judgment)
- Don't suggest lying or exaggerating
- Don't focus only on weaknesses; acknowledge strengths
