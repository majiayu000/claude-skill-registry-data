---
name: resume-creator
description: Create professional resumes using first-principles thinking, Google XYZ format, company research, LaTeX Harvard-style formatting, and iterative visual refinement. Use when the user wants to create, update, or optimize a resume/CV for a specific job, company, or career goal.
---

# Resume Creator

A comprehensive resume creation skill that uses first-principles thinking, Google XYZ format, web research, and iterative visual refinement to craft tailored, professional resumes.

## When to Use This Skill

- User wants to create a new resume
- User wants to update/optimize an existing resume
- User mentions a job application, job posting, or target company
- User asks about resume formatting or CV creation
- User wants to tailor their resume for a specific role

## Process Overview

### Phase 1: Information Gathering

1. **Read existing materials** (if available):
   - Existing resume (PDF, Word, or text)
   - LinkedIn profile screenshots (Claude cannot directly access LinkedIn URLs)
   - LinkedIn posts for achievements and speaking engagements
   - Portfolio or personal website

2. **Understand the target**:
   - Job description (if provided)
   - Target company and role
   - Industry/role type
   - Career goals

3. **Research the target company** using web search:
   - Company culture and values
   - Tech stack and engineering practices
   - Recent news, funding, products
   - What they look for in candidates
   - Company AUM/size/metrics for context
   - Example searches:
     - "{company} engineering blog hiring"
     - "{company} careers culture values"
     - "{role} at {company} interview what they look for"
     - "{company} AUM assets under management" (for finance)

4. **Gather missing information** by asking the user:
   - Recent experience not on resume
   - Specific achievements with metrics
   - Skills and technologies used
   - Projects and speaking engagements
   - Time spent on projects (for speed metrics)
   - Client details (AUM, size, industry)

### Phase 2: Google XYZ Format Analysis

**The XYZ Formula**: "Accomplished [X] as measured by [Y] by doing [Z]"

- **X** = Achievement/outcome (action verb: Built, Architected, Shipped, Led)
- **Y** = Quantifiable metric (%, time, money, users, accuracy)
- **Z** = How you did it (method, technology, approach)

Before writing, analyze each bullet:

| Bullet | X (What) | Y (Metric) | Z (How) | Score |
|--------|----------|------------|---------|-------|
| Example | Built connector | 2 weeks, 1000s docs | Delta API, Redis | 3/3 ✓ |

**Target: 100% of bullets should score 3/3**

Common metrics to extract from user:
- Time to build ("in 2 weeks", "in 1 week")
- Accuracy improvements ("125% improvement", "90% accuracy", "<3% error rate")
- Scale ("1000s of docs", "400+ rounds", "90+ companies")
- Cost savings ("reducing time from hours to minutes", "50% faster")
- Client context ("$100B+ AUM client", "Fortune 500")
- Audience size ("150+ builders", "100+ attendees")

### Phase 3: First-Principles Analysis

Before writing, analyze from first principles:

1. **Research what hiring managers look for**:
   - Web search: "{role} resume what hiring managers look for 2024"
   - Web search: "Google XYZ resume format"
   - Understand the <8 second resume scan reality

2. **Alignment analysis**:
   Create a table mapping:
   | Job Requirement | User's Experience | Gap/Strength |

3. **Paul Graham / YC style considerations** (for startup roles):
   - Lead with what you BUILT, not job titles
   - Show speed of execution ("shipped in X weeks", "built in 2 weeks")
   - Quantify everything (%, numbers, scale)
   - Builder tone: "Built", "Shipped", "Architected", "Won" not "Responsible for"
   - Remove corporate buzzwords

4. **Avoid redundancy**:
   - Check if metrics in bullets duplicate header/subheader info
   - Example: Don't say "Fortune 500 clients" in bullet if header says "Serving Fortune 500 clients"

### Phase 4: LaTeX Resume Creation

Use the Harvard-style LaTeX template with:
- Clean header (name, location, contact, links)
- No colored header bars - clean white background
- Section order: Experience → Projects & Speaking → Skills → Education → Leadership
- € symbol for currencies
- 1 page maximum (critical)

Key formatting:
- Font: Helvetica Neue (or similar sans-serif)
- Colors: Navy blue (#14-2D-4B / RGB 20,45,75) for sections
- Margins: ~0.5 inches
- Line spacing: 1.05
- Use `\setstretch{1.05}` for readability

**Punctuation guidelines**:
- Use commas or semicolons to connect clauses, NOT em dashes (--)
- Em dashes (--) only for date ranges in headers (e.g., "Sept 2025 -- Present")
- Use semicolons to separate distinct achievements in one bullet

**Link formatting**:
- Add `[link]` in small navy text next to items with LinkedIn/external proof
- Format: `{\color{sectioncolor}\footnotesize[\href{URL}{link}]}`

### Phase 5: Iterative Visual Refinement

**Critical**: After creating the LaTeX file, iterate visually:

1. **Compile to PDF**:
   ```bash
   xelatex -interaction=nonstopmode resume.tex
   ```

2. **Check page count**: Must be exactly 1 page
   - If 2 pages: reduce spacing, tighten text, combine bullets
   - Adjust `\titlespacing*{\section}{0pt}{6pt}{2pt}` if needed
   - Adjust `\setlist[itemize]{itemsep=1pt, parsep=0pt, topsep=1pt}`

3. **Check for issues**:
   - Does it fit on 1 page?
   - Is spacing balanced?
   - Are there overflow issues?
   - Is typography clean?
   - Any redundant information?

4. **Iterate** until perfect

### Phase 6: Final Delivery

1. Save final PDF: `Resume_[Name]_[Role]_[Year].pdf`
2. Keep .tex source file with same naming
3. Clean up temp files (.aux, .log, .out)
4. Open PDF for user

## Content Guidelines

### Experience Bullets - XYZ Examples

**Strong XYZ bullets**:
- Built SharePoint connector in 2 weeks enabling auto-indexing of 1000s of enterprise docs, reducing admin setup from hours to minutes
- Architected Snowflake sub-agent for NL-to-SQL, improving query accuracy by 125%; embedded at $100B+ AUM client, drove 4+ validation cycles
- Built agentic funding extraction with <3% error rate on 400+ rounds, validated against hand-labeled data and proprietary providers
- Delivered DSPy live optimization talk to 150+ builders, featured in global newsletter (50K+ subscribers)

**Weak bullets to avoid**:
- Responsible for platform development (no metric, no how)
- Worked on various projects (vague)
- Built connector using Redis (no metric, no outcome)

### Combining Related Bullets

When two bullets are related, combine them:
- Before: "Architected Snowflake agent" + "Embedded as Field Engineer at client"
- After: "Architected Snowflake sub-agent for NL-to-SQL, improving accuracy by 125%; embedded at $100B+ AUM client, drove 4+ validation cycles"

### Skills Organization

- **AI/ML**: LangChain, LangGraph, DSPy, MCP, OpenAI/Anthropic/Google APIs, RAG, Vector DBs, Embeddings
- **Full-Stack**: Next.js, React, TypeScript, Tailwind, Node.js, Python, REST APIs
- **Data & Infra**: Postgres, Snowflake, Redis, Microsoft Graph, GCP, Azure, Docker
- **Languages**: German (native), English (fluent)

## How Users Should Use This Skill

For best results, provide:
1. Your current resume (PDF or text)
2. LinkedIn screenshots (profile, experience, posts) — Claude cannot directly access LinkedIn URLs
3. The job posting or target company/role
4. Any recent achievements not on your resume
5. **Metrics**: time spent, accuracy numbers, scale, client details

Example:
```
Help me update my resume for the AI Engineer role at [Company].
Here's my current resume: [attach PDF]
LinkedIn posts: [attach screenshots]

Some context:
- Built the SharePoint connector in 2 weeks
- Client has $100B+ AUM
- Achieved 90% accuracy after 4 validation cycles
```
