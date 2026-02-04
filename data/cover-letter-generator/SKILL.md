---
name: cover-letter-generator
description: |
  Generate tailored AI-focused cover letters using the PSI (Problem-Solution-Impact) methodology.
  Use when: (1) User wants to create cover letters for AI/ML job applications, (2) User provides a resume and wants LinkedIn job matching, (3) User asks for personalized cover letters based on job postings, (4) User mentions applying for AI Engineer, ML Engineer, or similar technical roles.
  Integrates market intelligence, LinkedIn research via Playwright, and professional writing standards.
---

# Cover Letter Generator

Generate PSI-formatted cover letters tailored to LinkedIn AI job postings.

## Workflow

### Step 1: Analyze Resume

Extract and analyze the applicant's resume:

```bash
python3 scripts/extract_resume.py "<path_to_resume.docx>"
```

Identify from the resume:
- **Core technical stack**: Languages, frameworks, platforms
- **Quantified achievements**: Metrics, percentages, business outcomes
- **Domain experience**: Industries, project types, team sizes
- **AI/ML specific skills**: Models, pipelines, tools

### Step 2: Market Intelligence

Based on the resume profile, identify the **top 3 AI skills currently in demand**:

Common high-demand AI skills (2024-2025):
- RAG (Retrieval-Augmented Generation) pipelines
- Agentic AI workflows (LangGraph, AutoGen, CrewAI)
- LLMOps / MLOps (deployment, monitoring, fine-tuning)
- Prompt engineering & context optimization
- Vector databases & semantic search
- Multi-modal AI systems

Match resume skills to market demand to identify positioning strategy.

### Step 3: LinkedIn Research

Use `browsing-with-playwright` skill or Playwright MCP to search LinkedIn for relevant jobs:

**Search Strategy:**
1. Navigate to LinkedIn Jobs: `https://www.linkedin.com/jobs/`
2. Search terms combining: `[Primary Skill] + [Secondary Skill] + [Location/Remote]`
   - Example: "Agentic AI Developer Remote"
   - Example: "RAG Engineer LLMOps"
3. Find **2 relevant job postings** matching the profile
4. For each job, extract:
   - Company name and job title
   - Key technical requirements
   - Company's AI focus/challenges (from description)
   - Hiring manager name (if visible)

### Step 4: Bridge the Capability Gap

For each job posting, create a **PSI mapping**:

| Component | Source | Action |
|-----------|--------|--------|
| **Problem** | Job posting | Identify the organization's technical bottleneck |
| **Solution** | Resume | Map applicant's skills as the solution |
| **Impact** | Resume | Extract metrics proving ROI capability |

**Constraint**: Never fabricate experience. Reframe existing resume data to address the job's specific challenges.

### Step 5: Generate Cover Letters

Create 2 cover letters using the PSI template. See [references/psi_template.md](references/psi_template.md).

**Requirements:**
- Follow PSI format strictly (Problem -> Solution -> Impact)
- Integrate all 5 quality pillars from [references/quality_pillars.md](references/quality_pillars.md)
- Maintain professional, technical, impact-oriented tone
- Ensure "Translation Layer" is evident (explaining AI to stakeholders)
- Hyper-personalize to each company's context

**Quality Checklist:**
- [ ] Problem identifies company's specific AI challenge
- [ ] Solution uses concrete tools/methods from resume
- [ ] Impact includes quantified metrics
- [ ] Mentions Responsible AI / ethics alignment
- [ ] Demonstrates learning velocity (current tech awareness)
- [ ] References company-specific information
- [ ] Written with clarity for non-technical readers

## Output Format

Deliver 2 complete cover letters, each with:
1. Header (name, LinkedIn, GitHub)
2. Subject line targeting company's challenge
3. PSI body paragraphs
4. Professional closing

Save as: `cover_letter_[company_name].md`
