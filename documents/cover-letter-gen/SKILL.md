---
name: cover-letter-gen
description: |
  Generate ATS-optimized, company-specific cover letters for career-ops job applications. Paste a
  job description or provide a company name/URL → tailored cover letter in markdown, ready to attach
  or submit. Trigger when: the user asks to "generate cover letter", "write cover letter", "cover
  letter for this job", "/cover-letter", "tailor cover letter", or "company-specific cover letter";
  the user pastes a job description; the user names a company and wants a targeted application letter;
  or the user wants to apply to a role with a customized, ATS-safe cover letter. Key capabilities:
  extracts company intel from JD (pain points, tech stack, culture signals, repeated keywords);
  scores achievements from cv.md against JD keywords (3pt direct match, 2pt relevant, 1pt loose,
  0pt irrelevant); archetype-based narrative framing (LLMOps, Agentic, Technical AI PM, Solutions
  Architect, FDE, Transformation); 4-paragraph structure (hook with role+company, proof with top
  scored achievements, company-specific reasoning, close with next step). Style: confident,
  specific, peer-to-peer, no clichés, no "thank you for your consideration", 350-word max, plain
  text for ATS safety. Ideal for: job seekers applying to targeted roles who need personalized,
  high-quality cover letters at scale. Also for: drafting cover letter variations per archetype;
  auditing existing cover letters against JD keyword density.
user_invocable: true
args: company-name-or-url
argument-hint: "[company name or job description URL — optional; paste JD text directly for fastest results]"
triggers:
  - "generate cover letter"
  - "write cover letter"
  - "cover letter for this job"
  - "/cover-letter"
  - "tailor cover letter"
  - "company-specific cover letter"
---

# Cover Letter Generator — career-ops Mode

## Core Mission
Generate a compelling, ATS-optimized, company-specific cover letter that complements the career-ops PDF CV. One cover letter per application — never generic. Stops before submission.

---

## Input Resolution (in priority order)

1. **Pasted JD text** — if the user pasted raw JD text, use it directly
2. **URL** — if a job URL was provided, fetch via WebFetch or Playwright
3. **Company name** — if only a company name was given, search for the active JD in `data/pipeline.md` or `reports/`
4. **Context files to read always:**
   - `cv.md` — canonical CV
   - `config/profile.yml` — candidate narrative, archetype, target roles
   - `data/applications.md` — check if an evaluation report exists for this company

---

## Step 1 — Company Intel Extraction

From the JD, extract:
- Company name and industry
- Role title and seniority level
- Top 3 pain points / challenges the role solves
- Must-have tech stack requirements
- Culture signals (startup / enterprise / remote-first / etc.)
- Tone of the JD writing (formal, direct, playful, technical)
- 2-3 specific keywords or phrases used repeatedly

---

## Step 2 — Achievement Scoring

From `cv.md`, extract all achievements / bullet points.

**Score each achievement** against the JD keywords:
- 3 pts: direct tech stack match + quantified result
- 2 pts: relevant skill match (non-quantified) OR quantified result (no skill match)
- 1 pt: loosely relevant
- 0 pts: irrelevant

Select the **top 3-4 scored achievements** for the proof paragraph.

---

## Step 3 — Archetype + Narrative Alignment

From `config/profile.yml` and the archetype:
- **Primary framing**: use the detected archetype (LLMOps, Agentic, Technical AI PM, Solutions Architect, FDE, Transformation)
- **Exit story**: one sentence on why the candidate is motivated to move — specific, not vague
- **Superpower statement**: the single strongest match to this role, framed as a capability, not a trait
- **Company-specific hook**: one specific thing about this company that resonates — name a product, a stated value, a published challenge

---

## Step 4 — Draft the Cover Letter

### Paragraph 1 — Hook (3 sentences)

```
Sentence 1:  Name the role + company specifically.
              "I'm writing to apply for the Senior LLMOps Engineer role at Acme AI."
Sentence 2:  Name the strongest alignment, quantified if possible.
              "My background building production RAG pipelines that serve 10M+ daily
              queries maps directly to your need for someone who can own the full
              inference stack."
Sentence 3:  State the motivation in one line.
              "After five years optimizing AI infrastructure at [current company], I'm
              ready to bring that depth to Acme's platform-scale challenges."
```

### Paragraph 2 — Proof (4-5 sentences, prose, no bullets)

Weave in the top-scored achievements. Vary sentence structure — short, medium, long. Mirror the JD's tone.

### Paragraph 3 — Company-Specific Reasoning (2-3 sentences)

Name something specific about this company. Connect it to a candidate strength. Not generic flattery.

### Paragraph 4 — Close (2 sentences)

- Reiterate fit in one sentence
- Propose a specific next step
- **Never write**: "Thank you for your consideration"

---

## Style Rules

| Rule | Details |
|------|---------|
| Tone | Confident, specific, peer-to-peer |
| "I" statements | Own every claim — no "we" or passive voice |
| Clichés → cut | "Results-oriented team player" "Excellent communication skills" "Passionate about..." |
| Word limit | 350 words max (prose, no bullet list) |
| JD keywords | Weave 2-3 naturally — not stuffed |
| Language match | English / Spanish / German — match the JD language |
| ATS safety | Plain text, no tables, no images, standard fonts |

---

## Output

1. **Save** to `output/{company-slug}-cover-letter.md`
2. **Register** in `data/applications.md` — add `cover-letter.md` path to the Notes column for this company
3. **Show** the cover letter inline to the user
4. **Stop** — do not submit or send anything

---

## Quality Checklist (run before saving)

- [ ] Hook names the role AND company specifically
- [ ] At least one quantified achievement is included
- [ ] Cover letter references something specific about the company
- [ ] Zero clichés or generic phrases
- [ ] Under 350 words
- [ ] 2-3 JD keywords woven in naturally
- [ ] Same language as the JD
- [ ] File saved to `output/{company-slug}-cover-letter.md`
- [ ] applications.md updated with cover letter path

---

## Error Handling

- **No JD found**: Ask the user to paste the job description or provide a URL
- **No evaluation report**: Generate without archetype framing — fall back to generic archetype
- **Cover letter exists**: Ask "A cover letter already exists for [Company]. Overwrite it?"
- **Language mismatch**: If the JD is Spanish but profile is English, match the JD (the company's language wins)