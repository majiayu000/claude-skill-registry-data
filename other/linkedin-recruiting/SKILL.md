---
name: "linkedin-recruiting"
description: "Find, evaluate, and engage candidates on LinkedIn and LinkedIn Recruiter. Use when sourcing candidates, writing InMails, reviewing profiles, building Boolean search strings, building talent pipelines, analyzing markets, or managing InMail performance on LinkedIn."
---

# LinkedIn Recruiting Skill

You are an expert recruiting researcher and LinkedIn power user. Apply these workflows whenever the user is sourcing, evaluating, or engaging talent via LinkedIn, LinkedIn Recruiter, or LinkedIn Sales Navigator.

---

## Boolean Search — Core Operators

| Operator | What it does | Example |
|---|---|---|
| `AND` | Both terms must appear | `Python AND "machine learning"` |
| `OR` | Either term appears (broadens) | `"software engineer" OR "SWE"` |
| `NOT` | Exclude a term | `engineer NOT intern` |
| `"quotes"` | Exact phrase match | `"product manager"` |
| `( )` | Groups terms; controls order of operations | `("VP" OR "Director") AND Sales` |

**Critical rules (confirmed by LinkedIn's own product team):**
- Always use ALL CAPS for AND, OR, NOT — lowercase versions are ignored
- Always use parentheses; LinkedIn reads left-to-right without them and logic breaks
- Do NOT use `+` or `-` operators — they are not officially supported and produce unpredictable results
- Certain "stop words" (common words like "and," "the") are ignored in keyword fields — if you search "after sales," LinkedIn returns results for "sales" only
- Long strings can exceed field limits — if you see "No results found" for a string you know should work, try shortening it

---

## LinkedIn Recruiter: Filter-Level Boolean

In LinkedIn Recruiter, specific filters natively support Boolean dropdowns:
- **Must have** = AND
- **Can have** = OR
- **Doesn't have** = NOT

Use filter-level targeting for Title, Skills, Company, and School fields instead of cramming everything into the keyword field. This is more precise and avoids stop-word issues.

**Boolean-supported filters:** Keywords, Title, Company, School, Skills
**Not supported:** Project filter

---

## Boolean String Architecture — 3-Layer Framework

Build every search in three layers:

```
Layer 1 — Title synonyms (who they are):
("product manager" OR "PM" OR "product lead" OR "head of product")

Layer 2 — Must-have skills or context (what they know/have done):
(SQL OR "data analysis" OR analytics OR "A/B testing")

Layer 3 — Company / seniority signal (where they've been):
("Series B" OR "Series C" OR "growth stage" OR startup OR scaleup)

Exclusions (who to remove):
NOT (intern OR student OR "looking to hire" OR recruiter OR HR OR consultant)
```

**Full combined example:**
```
("product manager" OR "PM" OR "product lead") AND (SQL OR analytics OR "data analysis") AND ("Series B" OR "Series C" OR startup) NOT (intern OR student OR recruiter)
```

---

## Role-Specific Boolean Templates

**Software Engineer (Backend):**
```
("software engineer" OR "backend engineer" OR "SWE" OR "software developer") AND (Python OR Go OR Rust OR Java) AND ("microservices" OR "distributed systems" OR "API") NOT (intern OR "junior developer" OR QA)
```

**Data Scientist / ML Engineer:**
```
("data scientist" OR "ML engineer" OR "machine learning engineer" OR "AI engineer") AND (Python OR PyTorch OR TensorFlow OR "scikit-learn") AND ("production models" OR "deployed" OR "real-world") NOT (student OR PhD OR "looking for internship")
```

**Product Manager:**
```
("product manager" OR "PM" OR "product lead" OR "group PM") AND ("roadmap" OR "OKRs" OR "go-to-market" OR "launch") AND (B2B OR SaaS OR fintech OR "consumer tech") NOT (intern OR "associate PM")
```

**UX / Product Designer:**
```
("UX designer" OR "product designer" OR "UI/UX" OR "interaction designer") AND (Figma OR Sketch OR "design systems") AND ("user research" OR "usability" OR "prototyping") NOT (intern OR freelance OR "graphic designer")
```

**Head of / Executive Search:**
```
("Head of Engineering" OR "VP Engineering" OR "CTO" OR "Director of Engineering") AND ("team building" OR "scaled" OR "org design") AND (startup OR "Series C" OR "growth stage") NOT (consultant OR advisor OR "fractional CTO")
```

**Recruiting / Talent Acquisition:**
```
("recruiter" OR "talent acquisition" OR "TA partner" OR "technical recruiter") AND ("full cycle" OR "sourcing" OR "pipeline") AND (tech OR engineering OR "high volume") NOT (staffing OR agency OR "RPO")
```

**Spotlights to use in LinkedIn Recruiter:**
- "Open to Work" candidates respond 35% more than average
- "Recommended Matches" respond 35% more than average
- Company followers respond 81% more to InMails from that company

---

## InMail Strategy — Data-Backed Best Practices

**Key benchmarks (from LinkedIn's analysis of tens of millions of InMails):**
- Average InMail response rate: 18–25%; top performers hit 35–40%
- Messages under 400 characters get 22% higher response rates than average
- Messages over 1,200 characters get 11% lower response rates
- Individually sent InMails see ~15% higher response rates vs. bulk sends
- Best send days: Monday and Tuesday — avoid Friday and Saturday (13% response delay)
- Most responses arrive within 24 hours
- Subject line sweet spot on mobile: 16–27 characters (3–5 words)
- Combining InMail with multi-channel outreach improves engagement by up to 287%

**InMail credit rules:**
- You earn a credit back if the recipient responds within 90 days (even a "no thanks" counts)
- LinkedIn may temporarily suspend InMail if response rate drops below 13%

---

## InMail Templates

**Cold outreach (first touch):**
```
Subject: [Specific thing you noticed about their work — 4–5 words]

Hi [Name],

[One specific observation from their profile or public work — not flattery.]
We're hiring a [Role] at [Company] to [one-line description of the problem they'd solve].

Worth a 15-min call this week?

[Your name]
```
Target: under 400 characters. Reference exactly two things from their profile for a 15% lift.

**Follow-up (no reply after 7 days):**
```
Hi [Name],

Just circling back on my note from last week about [Role] at [Company].

One thing I didn't mention: [new piece of value — comp range, team detail, recent launch, or funding news].

Still happy to connect if the timing works.

[Your name]
```

**Re-engagement (past candidate, 6+ months later):**
```
Hi [Name],

We spoke back in [month] about [role/team]. A lot has changed since then — [what changed: new scope, new funding, new team structure].

The role is different now and I thought of you first. No pressure either way — happy to catch up if you're open to it.

[Your name]
```

**Rejection responder (they said no — keep warm):**
```
Hi [Name],

Totally understand — appreciate you taking the time to respond either way.

I'll keep you in mind as things evolve on our end. Feel free to reach out if anything changes on your side too.

[Your name]
```

---

## Profile Evaluation Framework

When reviewing a LinkedIn profile, assess in this order:

1. **Role fit** — title trajectory, tenure pattern, level progression (upward = strong)
2. **Skill match** — hard skills against JD must-haves vs. nice-to-haves
3. **Signal quality** — recommendations (specific > generic), endorsements, publications, open-source contributions, speaking engagements
4. **Company context** — stage alignment (startup vs. enterprise), team size, relevant industry
5. **Culture indicators** — volunteer work, side projects, writing/content creation
6. **Red flags** — unexplained gaps >12 months, multiple tenures <6 months, vague descriptions throughout, no measurable accomplishments listed

**3-line evaluation output format:**
- Fit: Strong / Moderate / Weak
- Top 2 reasons for the rating
- One open question to probe in screening

---

## Talent Market Analysis

When asked to map a talent pool or market:
1. Estimate total addressable pool by geography, title, and YoE using LinkedIn Talent Insights or Recruiter filters
2. Identify top 5 feeder companies (where this talent clusters)
3. Note top feeder schools for the target role
4. Flag compensation benchmarks from LinkedIn Salary data where available
5. Assess supply/demand tension: how many active openings exist for this profile type?
6. Recommend sourcing strategy based on pool size (broad for large pools, narrow targeted for scarce roles)

---

## Network Building for Sourcers

Proactively build your LinkedIn network to improve sourcing:
- Connect with "talent magnets" — HR leaders, tech evangelists, community organizers who already have large relevant networks
- Join and participate in industry groups — active participation makes your profile visible to candidates
- Thoughtfully comment on posts from target talent pools — this creates visibility and often leads to unsolicited connection requests
- Use second-degree connections strategically — they dramatically increase response rates

---

## Data Hygiene Before ATS Entry

Always extract these fields before logging a sourced candidate to your ATS:
- Full name, current title, current company, location, LinkedIn URL
- Years of relevant experience
- Key skills (top 5)
- Source date and source channel
- Initial outreach status (not contacted / contacted / responded / declined)

Never copy-paste full profile text into ATS notes — write a structured 3-sentence summary instead.
