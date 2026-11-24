---
name: "google-scholar-sourcing"
description: "Source researchers, PhDs, and domain experts via Google Scholar, ResearchGate, academia.edu, and university lab pages. Use when finding academic talent, interpreting h-index and citation signals, targeting candidates about to graduate, or building outreach to researchers."
---

# Google Scholar & Academic Sourcing Skill

You are an expert at sourcing researchers, PhD candidates, and domain experts from academic databases and university platforms. Apply these workflows when the user needs to find highly technical or research-oriented candidates.

---

## Why Academic Sourcing Works

Researchers are among the most passive candidates in existence — they rarely appear on job boards, often have outdated LinkedIn profiles, and are best reached through their published work. Google Scholar, ResearchGate, and university lab pages give direct access to:
- Current affiliation and contact details
- Proof of expertise (published, peer-reviewed work)
- Career stage signals (PhD candidate vs. postdoc vs. faculty)
- Co-author networks (find one, find many)

**Best roles for academic sourcing:** ML/AI engineers, data scientists, computational biologists, NLP researchers, quant researchers, cryptographers, materials scientists, biostatisticians.

---

## Platform Overview

| Platform | Best for | Key signal |
|---|---|---|
| **Google Scholar** | Discovering researchers by topic, h-index, institution | Citation count, h-index, affiliation |
| **ResearchGate** | Finding contact details, messaging researchers | Often lists institutional email directly |
| **academia.edu** | Broader humanities + social sciences reach | Profile pages with contact info |
| **University lab pages** | Finding PhD students close to graduation | Advisor name, thesis topic, expected year |
| **arXiv** | Cutting-edge ML/AI/physics researchers pre-publication | Recency signal — paper from last 30 days |
| **Semantic Scholar** | Cross-validating h-index, finding adjacent researchers | More rigorous citation data than Google Scholar |

---

## Google Scholar X-Ray Strings

```bash
# General researcher search by topic
site:scholar.google.com "machine learning" "PhD" ("MIT" OR "Stanford" OR "CMU") -assistant -professor

# Finding candidates about to graduate
site:scholar.google.com "PhD candidate" OR "doctoral student" "expected graduation 2026" "deep learning"
site:scholar.google.com "PhD candidate" "reinforcement learning" "2026" OR "2027"

# Postdocs (often open to industry — strong target)
site:scholar.google.com "postdoctoral researcher" "natural language processing" ("Google" OR "Meta" OR "industry")
site:scholar.google.com "postdoc" "computer vision" "available" OR "seeking"

# Research scientists at companies
site:scholar.google.com "research scientist" "OpenAI" OR "DeepMind" OR "Google Brain" "machine learning"

# By field + institution tier
site:scholar.google.com "computational biology" "PhD" ("Harvard" OR "MIT" OR "Broad Institute")
site:scholar.google.com "quantum computing" ("postdoc" OR "research scientist") 2024 OR 2025
```

---

## ResearchGate X-Ray Strings

```bash
# Find researchers with contact info visible
site:researchgate.net "computational biology" "postdoctoral" ("email" OR "@") -course -syllabus

# Specific domain + seniority
site:researchgate.net "natural language processing" "PhD" -course -template

# Researchers publishing in 2024-2025 (active)
site:researchgate.net "machine learning" "reinforcement learning" 2025

# Find co-authors of a known researcher (find one, find network)
site:researchgate.net "[known researcher name]" "co-author"
```

---

## University Lab Pages

```bash
# PhD students by department
site:cs.stanford.edu "PhD student" "machine learning"
site:*.mit.edu "PhD candidate" "computer vision" "graduating 2026"
site:*.cmu.edu "doctoral student" "NLP" OR "natural language processing"

# Broader university sweep for a topic
site:*.edu "PhD candidate" "deep learning" "graduating 2025" OR "graduating 2026"
site:*.edu "postdoctoral researcher" "reinforcement learning" ("available" OR "seeking opportunities")

# Find entire lab rosters
site:cs.[university].edu lab "machine learning" "students"
```

---

## arXiv for Cutting-Edge Researchers

```bash
# Recent papers in specific domain (last 6 months)
site:arxiv.org "reinforcement learning from human feedback" 2025
site:arxiv.org "diffusion models" "generative AI" 2025
site:arxiv.org "large language models" "fine-tuning" 2025

# Find first authors (usually PhD students or postdocs — most mobile)
# Cross-reference author name from arXiv with LinkedIn/GitHub for contact
```

**arXiv workflow:** Find a cutting-edge paper in your domain → note first author (most likely to be PhD student or early postdoc) → cross-reference their name on LinkedIn/Google Scholar for current affiliation and contact.

---

## Interpreting h-index as a Talent Signal

The h-index is the largest number h such that the researcher has h papers each cited at least h times.

**Practical benchmarks:**

| h-index | Signal | Typical career stage |
|---|---|---|
| 1–5 | Early career, limited output | PhD student, new postdoc |
| 5–10 | Active researcher, solid output | Mid PhD, postdoc |
| 10–20 | Strong contributor, widely cited | Senior postdoc, research scientist |
| 20+ | Field leader | Principal researcher, faculty |

**Critical caveat:** Google Scholar inflates h-index via self-citations and non-peer-reviewed preprints. One validated case showed an h-index drop from 19 to 9 (50%+) when self-citations and preprints were excluded.

**Cross-reference with:**
- **Semantic Scholar** — more conservative, excludes self-citations
- **Scopus** or **Web of Science** — most rigorous (requires institutional access)
- **Clarivate Highly Cited Researchers list** — gold standard for top 1% globally

**Practical shortcut:** For most recruiting purposes, use Scholar h-index as a directional signal, not a precise score. A researcher with 10+ citations on 3+ papers has demonstrated real impact.

---

## Timing: When to Target PhD Candidates

The optimal sourcing window is **6–18 months before expected graduation.** At this point:
- They're actively thinking about career paths
- They're often open to industry conversations for the first time
- Competition from other recruiters is low (most wait until graduation)
- You can build a relationship before they're actively job hunting

**How to find graduation timing:**
- Search `"expected graduation 2026"` or `"expected 2026"` in department pages
- Look for thesis defense announcements on lab pages
- Check if they've recently started a postdoc (signals PhD completed)
- LinkedIn "Education" end date field (if they've filled it in)

---

## Contacting Researchers

**In order of effectiveness:**

1. **Institutional email** — Most universities list faculty/postdoc emails on department pages. Cross-reference Scholar profile affiliation with the university's CS/biology/etc. department page.
2. **ResearchGate messaging** — Many researchers are active and respond via ResearchGate's internal messaging.
3. **Twitter/X** — Many computational researchers are active on X and DMs are often open.
4. **LinkedIn** — Lower response rate from academics; many profiles are outdated, but still worth trying.
5. **Academia.edu** — Good for humanities/social science researchers, less so for STEM.
6. **GitHub** — Computational researchers often list their email in their GitHub profile or README.

**Email template for researchers:**

```
Subject: [Their research topic] — industry opportunity at [Company]

Hi [Name],

I came across your paper on [specific paper title or topic] — particularly
[one specific finding or technique they used]. It's directly relevant to
work we're doing on [one-line description of the problem].

I'm a recruiter at [Company]. We're building [specific team/product], and
your background in [specific skill/area] is exactly what we're looking for.

Would you be open to a 20-minute call to hear more? No pressure — happy
to share details about the role first if you'd like to assess the fit.

[Your name]
```

**What works with researchers:**
- Reference the specific paper, not generic flattery
- Be explicit about the technical problem — they want intellectual challenge
- Don't oversell the company; lead with the problem
- Respect their time — short emails, clear ask
- Mention remote/flexible options (many are location-constrained by current lab)

---

## Schol arGPS and Clarivate

- **[ScholarGPS](https://scholargps.com/highly-ranked-scholars)** — Browse 30M+ scholar profiles with institutional ranking and field-specific context. Free tier available.
- **[Clarivate Highly Cited Researchers 2025](https://clarivate.com/highly-cited-researchers/)** — Annual list of top 1% most-cited researchers globally, by field and institution. Gold standard for executive-level research talent.

---

## Workflow: Sourcing a Research Talent Pool

1. **Define the research domain** — be specific (e.g. "RLHF for LLMs" not "AI")
2. **Find feeder institutions** — which universities have the strongest programs? (MIT, Stanford, CMU, UCL, ETH Zurich, etc.)
3. **Run Scholar + lab page X-Ray** — find PhD students graduating in 12–18 months
4. **Cross-reference on LinkedIn** — find contact info and current status
5. **Check arXiv for recent papers** — signals active, current work
6. **Validate h-index on Semantic Scholar** — before citing impact in outreach
7. **Outreach via institutional email** — reference specific paper
8. **Build co-author network** — one willing researcher can introduce others
