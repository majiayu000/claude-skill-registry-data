---
name: "ai-recruiting-prompts"
description: "Ready-to-use AI prompts for recruiting and sourcing tasks. Use when generating Boolean strings, writing outreach, screening resumes, benchmarking salaries, researching candidates or companies, building interview questions, or any task where ChatGPT, Claude, Perplexity, or Gemini can accelerate recruiting work."
---

# AI Recruiting Prompts Skill

You are an expert at applying AI tools to recruiting and sourcing workflows. When the user asks for help with a recruiting task, provide the best prompt for the right tool, or execute the task directly using the most appropriate approach.

---

## Tool Selection Guide

| Task | Best tool | Why |
|---|---|---|
| Boolean string generation | ChatGPT | Structured output, precise logic |
| Real-time salary benchmarking | Perplexity | Live web data with citations |
| Company intelligence / news | Perplexity | Real-time, cited sources |
| Long-form outreach that sounds human | Claude | Best writing quality, long context |
| Sensitive communications (rejections, negotiations) | Claude | Nuanced tone |
| Structured outputs (tables, JSON, scoring) | ChatGPT | Reliable formatting |
| Resume batch scoring | ChatGPT or Claude | Large context handling |
| Interview question generation | Any | Gemini if in Google Workspace |
| Google Workspace integration | Gemini | Native Gmail/Docs/Sheets |
| Multi-source research dossier | Perplexity Deep Research | 200+ sources, cited |
| Outreach sequence (3+ emails) | Claude | Natural variation, human tone |
| Job description drafting | Claude or ChatGPT | Both strong |

---

## ChatGPT Prompts

### Boolean String Generation
```
Act as a senior technical recruiter specializing in [industry]. Generate 3 variations
of a LinkedIn Boolean search string for a [role] in [location] with [skill 1],
[skill 2], and [skill 3] experience who has worked at a [company type].
Exclude candidates from [exclusions]. Provide: one short string (under 100 chars),
one comprehensive string, one X-Ray string for Google.
```

### Outreach — 3 Style Variations
```
Act as a recruiter. Write 3 outreach messages to a [role]. Styles: (1) Direct value,
(2) Mission-driven, (3) Career-arc. Constraints: 80-120 words each, one clear CTA,
subject line under 55 characters. Return as a table with columns: Style | Subject | Message.
```

### Skills Map from Job Description
```
Summarize this job spec into a skills map with three tiers:
- Tier 1: Must-have (dealbreaker if missing)
- Tier 2: Nice-to-have (differentiator)
- Tier 3: Bonus (rare upside)
Return JSON with fields: role, tier1[], tier2[], tier3[], boolean_linkedin, boolean_xray.
Include two Boolean strings: one for LinkedIn, one for Google X-Ray.

[Paste JD here]
```

### Title and Synonym Expansion
```
I'm sourcing for a "[title]" at a [stage] [industry] company. List 15 alternative
job titles this person might currently hold across both startup and enterprise contexts.
Then list the top 12 skills to include in a Boolean search, including industry-specific
jargon and abbreviations.
```

### Resume Batch Scoring
```
I have [N] resumes for a [role]. Score each on a 1-5 scale.

Must-haves (instant 5 if present, instant 1 if missing): [X, Y, Z]
Nice-to-haves (add 0.5 each): [A, B, C]
Dealbreakers (instant 1): [list]

For each resume I paste, return:
- Score: [1-5]
- Rationale: [2 sentences]
- Recommend: [Yes / No / Maybe]

Only recommend moving forward candidates scoring 4 or 5.
```

### 3-Email Follow-Up Sequence
```
Create a 3-email follow-up sequence for a candidate who has not responded to my
initial outreach for a [role] at [company type].
- Follow-up 1: 3 days after initial
- Follow-up 2: 5 days after that
- Final: polite "breakup" email leaving door open
Tone: persistent but not pushy. Each email must feel human and different — not templated.
Total word count: under 100 words per email.
```

### Candidate Persona
```
Develop a recruiter persona for an ideal candidate for a [role] in [industry].
Include:
- Typical career background and trajectory
- Motivations for changing jobs right now
- Likely objections to accepting an offer
- Preferred communication style and channels
- Red flags that would disqualify them
- Questions that would reveal their true fit
Format as bullet points under each heading.
```

### Interview Question Bank
```
Write 20 behavioural interview questions for a [role]. Include:
- 5 questions testing [specific competency 1]
- 5 questions testing [specific competency 2]
- 5 situational questions about [challenge common to this role]
- 5 culture/values questions
Format each question with: Question | What good looks like | What a red flag sounds like
```

---

## Claude Prompts

Claude excels at nuanced, human-sounding writing and processing large documents. Use Claude when quality of language matters more than structure.

### Personalised InMail (Reference-Based)
```
Act as a recruiter at [Company]. Write a 150-word LinkedIn InMail to [Name],
a [current role] at [current company], referencing their [specific post/article/
project/talk] about [topic].

Connect their work on [topic] to a challenge we're solving at [Company] around [problem].
End with a low-pressure CTA for a 20-minute call.

Tone: respectful, curious, not salesy. Never use the phrase "I came across your profile."
```

### Rejection Email (Candidate Experience First)
```
Write a rejection email for a candidate who reached the final interview stage for a
[role]. They were strong but we went with someone with more [specific thing].
Tone: warm, specific, respectful. Include:
- Genuine acknowledgement of their time and quality
- One specific positive observation from their process
- A door-left-open closing for future roles
- No empty phrases like "we'll keep your CV on file"
Keep under 150 words.
```

### Compensation Benchmarking Letter
```
Act as a compensation specialist. Given:
- Role: [title]
- Location: [city]
- Company stage: [seed / Series B / public]
- Team: [size and context]

Provide a realistic compensation package with:
- Base salary range (25th / 50th / 75th percentile)
- Target bonus %
- Equity range (options or RSUs, with vesting)
- Key benefits to mention for this profile

Explain your reasoning and flag any regional/industry adjustments.
```

### Offer Letter Narrative
```
Write the "why join us" narrative section of an offer letter for a [role].
The candidate cares about [their motivations]. We offer [key things].
Our mission is [mission]. The team they'd join is [team description].
Make it feel like a genuine invitation, not a legal document. Under 200 words.
```

### Outreach Sequence (5 touches, multi-channel)
```
Build a 5-touch outreach sequence for a passive [role] candidate across multiple
channels. Spread over 3 weeks. Channels: LinkedIn connection request, InMail,
Twitter/X DM, email, final "breakup."
Each touch: different angle, new piece of value added (not just "following up").
Include: channel | timing | subject/opening | full message | what value is being added
```

### Candidate Debrief Notes
```
I just finished a [stage] interview for a [role]. Here are my raw notes:
[paste notes]

Structure these into a formal candidate debrief with sections:
- Overall recommendation (Strong Yes / Yes / No / Strong No)
- Summary (2 sentences)
- Strengths (3 bullets with evidence from the interview)
- Concerns (2 bullets with evidence)
- Suggested next steps
Use behavioural evidence only — no gut-feel language.
```

---

## Perplexity Prompts

Use Perplexity for anything requiring real-time data. Always use **Deep Research mode** (Pro) for dossiers and market intelligence — it draws from 200+ sources.

### Pre-Outreach Company Dossier
```
Research [Company Name]. Provide:
1. Recent funding history and current estimated headcount
2. Primary tech stack (based on job postings and engineering blog)
3. Top 3 competitors
4. Any recent news: layoffs, expansions, pivots, leadership changes
5. Key engineering or product challenges they're publicly discussing
6. Glassdoor sentiment summary if available
Cite all sources. Flag anything published in the last 90 days.
```

### Real-Time Salary Benchmarking
```
What is the current market compensation for a [role] in [city] at a [stage] company
in 2025? Break down:
- Base salary (25th / 50th / 75th percentile)
- Target bonus %
- Equity (startup options vs. public RSUs)
- Total comp range
Compare startup vs. public company norms. Cite sources published within the last
6 months only. Flag if data is thin or lagged.
```

### Talent Market Intelligence
```
How has the hiring market for [role] in [industry/region] changed over the past
12 months? Cover:
- Which companies are the top hirers?
- Which companies have had layoffs and may have available passive talent?
- What is supply/demand tension like for this skill set?
- What sourcing channels are most effective for this profile?
Cite sources. Focus on 2025 data.
```

### Competitive Talent Mapping
```
Which companies in [city/region] employ the largest concentrations of [role type]
engineers with expertise in [tech stack]? List top 10 employers by estimated headcount
for this skill set. Note any hiring freezes, expansions, or recent headcount changes.
```

### Candidate Background Research
```
Research [Person Name], currently [Title] at [Company]. Provide:
1. Career trajectory summary
2. Notable achievements or projects they're publicly associated with
3. Published work, talks, or content they've created
4. Any public commentary about their career interests
5. Potential conversation hooks for a cold outreach
6. Likely motivations for a move right now (based on company context)
Keep to one page. Cite sources.
```

### Niche Talent Landscape
```
Who are the 20-30 most prominent practitioners and thought leaders in [specific domain]
globally in 2025? For each, include:
- Current affiliation
- How to find them online (LinkedIn, GitHub, Twitter, personal site)
- What makes them notable (papers, products, talks)
Focus on active practitioners, not just academics. Prioritise people likely to be
reachable.
```

---

## Gemini Prompts (Google Workspace)

Gemini's advantage is native integration with Gmail, Google Docs, and Sheets. Use it for workflows that live in Google Workspace.

### Job Description Draft (in Docs)
```
Create a job description for a [title] role requiring [X] years experience in [skills].
Include: responsibilities, requirements, team context, culture section.
Add keywords for job board SEO. Keep to 500 words. Use active voice throughout.
```

### Interview Scorecard (in Sheets)
```
Build an interview scorecard template for a [role] in Google Sheets format.
Columns: Competency | Weight | Score (1-4) | Weighted Score | Evidence/Notes
Include 6 competencies appropriate for this role, with weighting that sums to 100%.
Add a legend: 1=Strong No, 2=No, 3=Yes, 4=Strong Yes.
```

### Offer Letter Template (in Docs)
```
Create an offer letter template for a [role] at a [stage] startup.
Include placeholders for: name, role, start date, base salary, bonus, equity,
benefits summary, reporting line, offer expiry date.
Tone: warm but professional. Add a 2-sentence "why join us" paragraph placeholder.
```

### Candidate Pipeline Summary (in Sheets)
```
Build a candidate pipeline tracker in Sheets for a [role] search.
Columns: Name | Source | Stage | Last Activity | Next Action | Due Date |
Recommendation | Notes
Include a summary row at top that counts candidates per stage automatically.
```

---

## AI Tool Prompting Principles

**Regardless of tool, these principles improve output quality:**

1. **Assign a role first** — "Act as a senior technical recruiter" sets context and improves specificity
2. **Define constraints explicitly** — word count, tone, format, what NOT to include
3. **Ask for format** — table, JSON, bullets, numbered list — specify it
4. **Provide examples** — "Like this: [example]" dramatically improves output quality
5. **Iterate in the same conversation** — refine the output rather than restarting; AI remembers context
6. **Request variations** — "Give me 3 versions" then pick; always better than editing one
7. **Paste the JD** — always include the full job description for role-specific outputs
8. **Specify the candidate type** — passive vs. active, seniority, industry context
