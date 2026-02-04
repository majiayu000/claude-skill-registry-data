---
name: career-development
description: Data analyst career development, portfolio building, and professional growth strategies
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 07-career-coach
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  career_stage:
    type: string
    required: true
    enum: [entry, mid, senior, lead, executive]
    default: mid
  focus_area:
    type: string
    required: false
    enum: [portfolio, job_search, interviews, advancement, all]
    default: all
  industry:
    type: string
    required: false
    default: technology

# Observability
observability:
  logging_level: info
  metrics: [goal_progress, skill_acquisition, interview_success]
---

# Career Development Skill

## Overview
Navigate your data analyst career path with guidance on portfolio building, job searching, interviewing, and professional development.

## Core Topics

### Portfolio Development
- Project selection and presentation
- GitHub portfolio best practices
- Kaggle competitions and datasets
- Case study documentation

### Job Search Strategy
- Resume optimization for data roles
- LinkedIn profile enhancement
- Networking in the data community
- Remote vs on-site opportunities

### Interview Preparation
- Technical interview questions (SQL, Python, statistics)
- Case study interviews
- Behavioral interview frameworks (STAR method)
- Take-home assignment strategies

### Career Advancement
- Specialization paths (BI, data science, analytics engineering)
- Continuous learning strategies
- Certifications (Google, Microsoft, AWS)
- Building domain expertise

## Learning Objectives
- Build a compelling data analytics portfolio
- Navigate the job market effectively
- Excel in technical and behavioral interviews
- Plan long-term career growth

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Goal misalignment | Unclear objectives | Reassess values and priorities |
| Skill gap | Missing competencies | Create targeted learning plan |
| Interview rejection | Preparation gaps | Review feedback, practice more |
| Career stagnation | No growth activities | Set stretch goals, find mentor |
| Burnout | Overwork | Set boundaries, prioritize self-care |

## Related Skills
- All technical skills for interview preparation
- visualization (for portfolio presentation)
- programming (for GitHub presence)
